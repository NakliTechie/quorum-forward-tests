"""HH2 — calibrated arms for the October 2026 Harvard CAPS/Harris registration (docs/hh2-registration-draft.md).

CPU-only transforms of the HH2 emission rows, by HH1-B's frozen functions (scripts/build_hh1b.py) with two
changes declared in the registration before any number existed: the source rows are HH2's, and the
direction DK target is the September 2026 wave's published right-track DK (10.0). The house-shift arm is
dropped. Raw arms are the emission's own forecast.json files, copied unchanged.

    PYTHONPATH=. .venv/bin/python scripts/build_hh2.py --src artifacts-approval/hh2-registration --out artifacts-approval/hh2
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_hh1b as b  # noqa: E402
from dk_shrink import dk_shrink  # noqa: E402

from quorum.twin.forecast import aggregate, calibrate_soft, load_frame_csv  # noqa: E402
from quorum.twin.instruments import INSTRUMENTS  # noqa: E402

FRAME_SHA = "6653915b47277578d2170c275c57699fe6538e93d347cd5ba990d112a2bd5743"  # = HH1's frame
ANCHOR_SHA = "df3caf8a224ed80ac347f11bcdb2f6fcc446554c1dc3c49b583e00b7a40c80b0"  # file bytes, data/forward/hh2/anchor-hh2.txt
REVISION = "40c069824f4251a91eefaf281ebe4c544efd3e18"
# registered adapter hashes (the GPU job hashes the real files; CPU acceptance needs no binaries: Codex HH2 clear 1)
ADAPTER_SHA = {"adapter_model.safetensors": "4cabea94d18b882addd903e1ed6bc749592362ea2538cada4d8e7b974d59b8e5",
               "adapter_config.json": "563a0337c96020f4d40ee703fa821eef45b6172ea8745b37719fe9abbd3282bb"}
# inference source the box ran; hashed there into run-manifest.json and compared here (Codex HH2 confirm 2)
SOURCE_FILES = ("quorum/twin/forecast.py", "quorum/twin/predict.py", "quorum/twin/instruments.py",
                "quorum/twin/compression.py", "quorum/twin/evidence.py")
SEP_DK = 10.0  # HH September 2026 wave, right-track Don't know (hh1/published-2026-09-26-28.json)
RAW = {"hh_approval": "hh2_approval_raw", "hh_direction": "hh2_direction_raw",
       "hh_generic_ballot": "hh2_ballot_raw"}


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check_source(src: Path, frame: Path, anchor: Path, cells: dict) -> list[str]:
    """Provenance and completeness of the emission before any transform (Codex HH2 pre-review 5)."""
    probs = []
    if sha(frame) != FRAME_SHA:
        probs.append(f"frame sha {sha(frame)[:12]} is not the registered {FRAME_SHA[:12]}")
    if sha(anchor) != ANCHOR_SHA:
        probs.append(f"anchor sha {sha(anchor)[:12]} is not the registered {ANCHOR_SHA[:12]}")
    text = anchor.read_text().strip()
    for inst in RAW:
        f = json.loads((src / inst / "forecast.json").read_text())
        if (f.get("instrument") or {}).get("key") != inst:
            probs.append(f"{inst}: forecast.json is for {(f.get('instrument') or {}).get('key')}")
        if f.get("calibration") != "raw":
            probs.append(f"{inst}: emission is not raw ({f.get('calibration')})")
        if f.get("anchor_text", "").strip() != text or f.get("anchor_sha256") != hashlib.sha256(f.get("anchor_text", "").encode()).hexdigest():
            probs.append(f"{inst}: emitted with a different anchor")
        n = len(INSTRUMENTS[inst]["options"])
        rows = [json.loads(ln) for ln in (src / inst / "rows.jsonl").read_text().splitlines()]
        keys = [r["profile"] for r in rows]
        if len(keys) != len(set(keys)):
            probs.append(f"{inst}: {len(keys) - len(set(keys))} duplicate profiles")
        if set(keys) != set(cells):
            probs.append(f"{inst}: rows cover {len(set(keys) & set(cells))} of {len(cells)} frame profiles")
        bad_w = sum(1 for r in rows if r["profile"] in cells and not math.isclose(r["w"], cells[r["profile"]]["w"], rel_tol=1e-9))
        if bad_w:
            probs.append(f"{inst}: {bad_w} row weights differ from the frame")
        bad_p = sum(1 for r in rows if not (all(isinstance(r.get(f"p{i}"), (int, float)) and math.isfinite(r[f"p{i}"])
                                                and 0 <= r[f"p{i}"] <= 1 for i in range(1, n + 1))
                                            and abs(sum(r[f"p{i}"] for i in range(1, n + 1)) - 1) < 1e-6))
        if bad_p:
            probs.append(f"{inst}: {bad_p} rows with invalid probabilities")
    probs += check_emission(src, cells)
    return probs


def check_emission(src: Path, cells: dict) -> list[str]:
    """Manifests, instrument specs, forecasts recomputed from rows, and no zeroed options
    (Codex HH2 confirmation review 1 and 3)."""
    probs = []
    root = Path(__file__).resolve().parents[1]
    rm = src / "run-manifest.json"
    if not rm.exists():
        return probs + ["run-manifest.json missing"]
    run = json.loads(rm.read_text())
    if run.get("revision") != REVISION or run.get("adapter_sha256") != ADAPTER_SHA:
        probs.append("run manifest: revision or adapter hashes differ from the registration")
    if not run.get("code_commit"):
        probs.append("run manifest: no code commit")
    want_src = {f: sha(root / f) for f in SOURCE_FILES}
    if run.get("source_sha256") != want_src:
        probs.append("run manifest: inference source on the box differs from this checkout")
    for inst in RAW:
        d = src / inst
        man = json.loads((d / "manifest.json").read_text()) if (d / "manifest.json").exists() else None
        if man is None:
            probs.append(f"{inst}: manifest.json missing")
            continue
        pm = man.get("params", {})
        if pm.get("stub") is not False or pm.get("platt") or pm.get("instrument") != inst \
                or not str(pm.get("hf_id", "")).endswith("/snapshots/" + REVISION) or pm.get("adapter") != "/adapters/14b":
            probs.append(f"{inst}: manifest params {{stub, platt, instrument, hf_id, adapter}} differ from the registration")
        ds = {Path(x["path"]).name: x["sha256"] for x in man.get("datasets", [])}
        if ds.get("frame_hh.csv") != FRAME_SHA or ds.get("anchor-hh2.txt") != ANCHOR_SHA:
            probs.append(f"{inst}: manifest dataset hashes differ from the registered frame and anchor")
        f = json.loads((d / "forecast.json").read_text())
        spec = INSTRUMENTS[inst]
        if {k: (f.get("instrument") or {}).get(k) for k in ("question", "options", "provenance")} != \
                {k: spec[k] for k in ("question", "options", "provenance")}:
            probs.append(f"{inst}: forecast instrument text differs from the registered instrument")
        n = len(spec["options"])
        softs = {r["profile"]: {i: r[f"p{i}"] for i in range(1, n + 1)}
                 for r in (json.loads(ln) for ln in (d / "rows.jsonl").read_text().splitlines())}
        if set(softs) != set(cells):
            continue  # coverage already reported by check_source
        zeros = sum(1 for dist in softs.values() if any(v == 0.0 for v in dist.values()))
        if zeros:
            probs.append(f"{inst}: {zeros} profiles have an option at exactly 0 (top-20 truncation)")
        again = aggregate({k: cells[k] for k in softs}, softs, inst)
        if again["topline"] != f.get("topline") or again["by"] != f.get("by"):
            probs.append(f"{inst}: forecast.json does not match the aggregate recomputed from its rows")
    return probs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="emission folder with <instrument>/rows.jsonl + forecast.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--frame", default=str(b.FRAME), help="the registered HH frame (sha checked)")
    ap.add_argument("--anchor", default="data/forward/hh2/anchor-hh2.txt", help="the registered anchor (sha checked)")
    a = ap.parse_args()
    b.SRC = Path(a.src)  # build_hh1b's load_rows/emit read this module global
    b.FRAME = Path(a.frame)
    out = Path(a.out)
    cells = load_frame_csv(str(b.FRAME))
    probs = check_source(b.SRC, Path(a.frame), Path(a.anchor), cells)
    if probs:
        for x in probs:
            print("REFUSED:", x)
        return 1

    for inst, name in RAW.items():  # raw arms: the emitted files, unchanged
        d = out / name
        d.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(b.SRC / inst / "forecast.json", d / "forecast.json")
        print(f"{name:20s} copied  sha {hashlib.sha256((d / 'forecast.json').read_bytes()).hexdigest()[:12]}")

    inst = "hh_approval"
    spec = INSTRUMENTS[inst]
    softs, _ = b.load_rows(inst)
    sub = {k: cells[k] for k in softs}
    cal = {k: calibrate_soft(d, spec, b.A_APPR, b.B_APPR) for k, d in softs.items()}
    b.emit(out, "hh2_approval_cal", aggregate(sub, cal, inst), inst,
           {"a": b.A_APPR, "b": b.B_APPR, "family": "approval_pooled_2019_2025"})

    inst = "hh_direction"
    spec = INSTRUMENTS[inst]
    softs, _ = b.load_rows(inst)
    sub = {k: cells[k] for k in softs}
    dk_digit = spec["options"].index(spec["abstain"][0]) + 1
    tw = sum(sub[k]["w"] for k in softs)

    def dk_at(s):  # unrounded aggregate DK, so the solve lands on the target (Codex HH2 pre-review 6)
        return 100 * sum(sub[k]["w"] * dk_shrink(d, spec, s).get(dk_digit, 0.0) for k, d in softs.items()) / tw
    raw_dk = dk_at(1.0)
    if not dk_at(0.0) <= SEP_DK <= raw_dk:
        print(f"REFUSED: DK target {SEP_DK} outside the reachable range {dk_at(0.0):.2f}-{raw_dk:.2f}")
        return 1
    s = b.solve(dk_at, SEP_DK, 0.0, 1.0, iters=200)
    dks = {k: dk_shrink(d, spec, s) for k, d in softs.items()}
    b.emit(out, "hh2_direction_dk", aggregate(sub, dks, inst), inst,
           {"method": "dk_shrink", "s": s, "solved_on": "unrounded aggregate DK", "fit": f"solved so aggregate DK = {SEP_DK} "
            "(HH September 2026 wave, right-track DK; in-sample for that one number, disclosed)",
            "raw_dk": round(raw_dk, 1)})
    print(f"  direction DK {raw_dk:.1f} -> {SEP_DK} (s {s:.4f})")

    inst = "hh_generic_ballot"
    spec = INSTRUMENTS[inst]
    softs, _ = b.load_rows(inst)
    sub = {k: cells[k] for k in softs}
    bal = {k: calibrate_soft(d, spec, b.A_BAL, b.B_BAL) for k, d in softs.items()}
    b.emit(out, "hh2_ballot_cal", aggregate(sub, bal, inst), inst,
           {"a": b.A_BAL, "b": b.B_BAL, "family": "HOUSE_BALLOT_NS"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
