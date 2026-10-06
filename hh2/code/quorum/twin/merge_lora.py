"""Merge a PEFT LoRA adapter into its base model's weights (UQ1 determinism, 2026-10-04).

Why: vLLM 0.8.5 serves a LoRA adapter through Triton kernels whose shrink step splits the inner
dimension (SPLIT_K 64 for small batches) and sums the partial products with tl.atomic_add
(vllm/lora/ops/triton_ops/kernel_utils.py:243). Atomic float addition has no fixed order, so two
runs of the same prompts give slightly different probabilities under every engine setting. A
merged checkpoint needs no LoRA kernels.

    python scripts/merge_lora.py --base Qwen/Qwen3-14B --revision <sha> --adapter /adapters/14b --out merged/

Each target weight becomes W + (alpha / r) * B @ A, computed in float32 on the CPU and rounded to
bfloat16 once. Non-target tensors are copied unchanged. Tokenizer files come from the adapter
directory when it has them (vLLM serves a LoRA request with the adapter's tokenizer), otherwise
from the base. The output holds merge_manifest.json: inputs, scale, and every file's sha256.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import sys
from pathlib import Path

PREFIX = "base_model.model."
TOKENIZER_FILES = ("tokenizer.json", "tokenizer_config.json", "vocab.json", "merges.txt",
                   "special_tokens_map.json", "added_tokens.json")


def sha(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 24), b""):
            h.update(b)
    return h.hexdigest()


def check_config(cfg: dict) -> float:
    """The scale alpha / r, refusing adapter features this merge does not implement."""
    bad = {k: cfg.get(k) for k in ("use_rslora", "use_dora", "fan_in_fan_out") if cfg.get(k)}
    bad |= {k: cfg.get(k) for k in ("modules_to_save", "rank_pattern", "alpha_pattern", "layers_to_transform")
            if cfg.get(k)}
    if cfg.get("bias", "none") != "none":
        bad["bias"] = cfg["bias"]
    if cfg.get("peft_type") != "LORA":
        bad["peft_type"] = cfg.get("peft_type")
    if bad:
        raise ValueError(f"unsupported adapter settings: {bad}")
    return cfg["lora_alpha"] / cfg["r"]


def plan(adapter_keys: list[str], base_keys: set[str]) -> dict[str, tuple[str, str]]:
    """base weight name -> (lora_A key, lora_B key); every adapter tensor must map to a base weight."""
    pairs: dict[str, tuple[str, str]] = {}
    for k in adapter_keys:
        if not k.startswith(PREFIX) or not k.endswith((".lora_A.weight", ".lora_B.weight")):
            raise ValueError(f"unexpected adapter tensor {k}")
    for k in adapter_keys:
        if k.endswith(".lora_A.weight"):
            target = k[len(PREFIX):].removesuffix(".lora_A.weight") + ".weight"
            b = k.removesuffix(".lora_A.weight") + ".lora_B.weight"
            if b not in adapter_keys:
                raise ValueError(f"no lora_B for {k}")
            if target not in base_keys:
                raise ValueError(f"adapter targets {target}, absent from the base")
            pairs[target] = (k, b)
    if 2 * len(pairs) != len(adapter_keys):
        raise ValueError("adapter has lora_B tensors without a lora_A")
    return pairs


def merge(base_dir: Path, adapter_dir: Path, out: Path, meta: dict) -> dict:
    import torch
    from safetensors import safe_open
    from safetensors.torch import load_file, save_file

    torch.set_num_threads(4)  # fixed, so the float32 CPU products are summed the same way every time
    out.mkdir(parents=True, exist_ok=False)
    scale = check_config(json.loads((adapter_dir / "adapter_config.json").read_text()))
    lora = load_file(adapter_dir / "adapter_model.safetensors")
    index = json.loads((base_dir / "model.safetensors.index.json").read_text())
    pairs = plan(list(lora), set(index["weight_map"]))
    done = set()
    for shard in sorted(set(index["weight_map"].values())):
        tensors = {}
        with safe_open(base_dir / shard, "pt") as f:
            for name in f.keys():
                w = f.get_tensor(name)
                if name in pairs:
                    a, b = (lora[k].to(torch.float32) for k in pairs[name])
                    w = (w.to(torch.float32) + scale * (b @ a)).to(w.dtype)
                    done.add(name)
                tensors[name] = w.contiguous()
            fmeta = f.metadata()
        save_file(tensors, out / shard, metadata=fmeta)
        print(f"MERGE shard {shard}: {len(tensors)} tensors", flush=True)
    if done != set(pairs):
        raise RuntimeError(f"{len(set(pairs) - done)} target weights not found in any shard")
    for p in base_dir.iterdir():
        if p.is_file() and not p.name.endswith(".safetensors") and p.name not in TOKENIZER_FILES:
            shutil.copyfile(p, out / p.name)
    tok_src = adapter_dir if (adapter_dir / "tokenizer.json").exists() else base_dir
    for n in TOKENIZER_FILES:
        if (tok_src / n).exists():
            shutil.copyfile(tok_src / n, out / n)
    files = {p.name: sha(p) for p in sorted(out.iterdir()) if p.is_file()}
    from importlib.metadata import version

    manifest = meta | {"merge_script_sha256": sha(Path(__file__)),
                       "versions": {k: version(k) for k in ("torch", "safetensors")}, "scale": scale, "n_merged": len(done), "tokenizer_from": str(tok_src),
                       "adapter_sha256": {n: sha(adapter_dir / n) for n in ("adapter_model.safetensors",
                                                                             "adapter_config.json")},
                       "files_sha256": files}
    (out / "merge_manifest.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"MERGE DONE {len(done)} weights, scale {scale}, {len(files)} files", flush=True)
    return manifest


def verify(ckpt: Path, base: str, revision: str, adapter_dir: Path | None) -> list[str]:
    """Problems with a merged checkpoint: every file re-hashed against its manifest, and the manifest's
    base, revision and adapter hashes against what the caller expects. Empty list = verified."""
    mf = ckpt / "merge_manifest.json"
    if not mf.exists():
        return ["merge_manifest.json missing"]
    man = json.loads(mf.read_text())
    probs = []
    if man.get("base") != base or man.get("revision") != revision:
        probs.append(f"built from {man.get('base')}@{man.get('revision')}, expected {base}@{revision}")
    if adapter_dir is not None:
        want = {n: sha(adapter_dir / n) for n in ("adapter_model.safetensors", "adapter_config.json")}
        if man.get("adapter_sha256") != want:
            probs.append("built from a different adapter")
    files = man.get("files_sha256") or {}
    present = {p.name for p in ckpt.iterdir() if p.is_file() and p.name != "merge_manifest.json"}
    if present != set(files):
        probs.append(f"files differ from the manifest: {sorted(present ^ set(files))[:6]}")
    probs += [f"hash mismatch {n}" for n in sorted(present & set(files)) if sha(ckpt / n) != files[n]]
    return probs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--base", default="Qwen/Qwen3-14B")
    ap.add_argument("--revision", required=True)
    ap.add_argument("--adapter", required=True)
    ap.add_argument("--out")
    ap.add_argument("--verify", metavar="CKPT", help="re-hash a merged checkpoint against its manifest")
    a = ap.parse_args()
    if a.verify:
        probs = verify(Path(a.verify), a.base, a.revision, Path(a.adapter))
        for x in probs:
            print("VERIFY FAIL:", x, flush=True)
        print("VERIFY OK" if not probs else f"VERIFY FAILED ({len(probs)} problems)", flush=True)
        return 0 if not probs else 1
    if not a.out:
        sys.exit("--out or --verify is required")
    from huggingface_hub import snapshot_download

    base_dir = Path(snapshot_download(a.base, revision=a.revision,
                                      allow_patterns=["*.json", "*.safetensors", "*.txt", "*.model"]))
    merge(base_dir, Path(a.adapter), Path(a.out), {"base": a.base, "revision": a.revision})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
