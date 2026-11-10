"""HH2 and HH3 — calibrated arms for the Harvard CAPS/Harris registrations (docs/hh2-registration-draft.md,
docs/hh3-registration-draft.md).

CPU-only transforms of one registration's emission rows, by HH1-B's frozen functions (scripts/build_hh1b.py).
HH2 (October 2026) declared two changes from HH1-B before any number existed: the source rows are HH2's, and the
direction DK target is the September 2026 wave's published right-track DK (10.0); the house-shift arm is
dropped. HH3 (November 2026) re-runs HH2's method unchanged on FT13's anchor, with the DK target taken from the
October 2026 wave (10.0). `--registration` picks the registered constants (anchor sha, the anchor's file name in
the emission manifests, DK target and its source, arm names; for HH3 also the frozen inference-source hashes, and
the emission commit becomes a required argument). HH2's constants and checks are unchanged, so HH2's six forecasts
rebuild byte for byte. Raw arms are the emission's own forecast.json files, copied unchanged.

    PYTHONPATH=. .venv/bin/python scripts/build_hh2.py --src artifacts-approval/hh2-registration --out artifacts-approval/hh2
    PYTHONPATH=. .venv/bin/python scripts/build_hh2.py --registration hh3 --emission-commit <40-char sha> \\
        --src artifacts-approval/hh3-registration --out artifacts-approval/hh3 --frame <quorum-forward-tests>/hh2/frame_hh.csv
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import shutil
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build_hh1b as b  # noqa: E402
from dk_shrink import dk_shrink  # noqa: E402

from quorum.twin.forecast import aggregate, calibrate_soft, load_frame_csv  # noqa: E402
from quorum.twin.instruments import INSTRUMENTS  # noqa: E402

FRAME_SHA = "6653915b47277578d2170c275c57699fe6538e93d347cd5ba990d112a2bd5743"  # = HH1's frame (HH2 and HH3)
REVISION = "40c069824f4251a91eefaf281ebe4c544efd3e18"
# registered adapter hashes (the GPU job hashes the real files; CPU acceptance needs no binaries: Codex HH2 clear 1)
ADAPTER_SHA = {"adapter_model.safetensors": "4cabea94d18b882addd903e1ed6bc749592362ea2538cada4d8e7b974d59b8e5",
               "adapter_config.json": "563a0337c96020f4d40ee703fa821eef45b6172ea8745b37719fe9abbd3282bb"}
# inference source the box ran; hashed there into run-manifest.json and compared here (Codex HH2 confirm 2)
SOURCE_FILES = ("quorum/twin/forecast.py", "quorum/twin/predict.py", "quorum/twin/instruments.py",
                "quorum/twin/compression.py", "quorum/twin/evidence.py")
# Registered constants per registration. anchor_sha is the file bytes; anchor_name is the anchor's file name in each
# instrument manifest's datasets (the box copies the anchor under this name); dk_target is the previous wave's
# published right-track Don't know, which direction_dk's shrink is solved to hit. source_sha256 (HH3 onward) fixes the
# inference source as registered constants, as ADAPTER_SHA fixes the adapter, and makes acceptance require the
# registered emission commit (Codex HH3 pre 4); HH2's acceptance is unchanged (source compared with the checkout).
REGISTRATIONS = {
    "hh2": {"anchor_sha": "df3caf8a224ed80ac347f11bcdb2f6fcc446554c1dc3c49b583e00b7a40c80b0",
            "anchor_name": "anchor-hh2.txt", "anchor_path": "data/forward/hh2/anchor-hh2.txt",
            # hh1/published-2026-09-26-28.json
            "dk_target": 10.0, "dk_wave": "HH September 2026 wave"},
    "hh3": {"anchor_sha": "913c6645db67402d199b023c1d9afaf0b4cb881b54bf1b143acd64084c5e1a26",  # = FT13's anchor
            "anchor_name": "anchor-ft13.txt", "anchor_path": "data/forward/ft13/anchor-ft13.txt",
            # hh2/published-2026-10-24-26.json (direction topline Don't know, Oct 26 point of the p.4 trend chart)
            "dk_target": 10.0, "dk_wave": "HH October 2026 wave",
            # = HH2's run (quorum-forward-tests/hh2/emission/run-manifest.json) and this checkout at registration
            "source_sha256": {"quorum/twin/forecast.py": "38609cbeb5df03c1ce0cf52e6cff285f47cf72527c6daaa10fd5d7d52d6d01dd",
                              "quorum/twin/predict.py": "d415df3a722c09974f9062b8b951f8bf991d30e4962a9ba0e6c1aa9c8bb900e9",
                              "quorum/twin/instruments.py": "6c66dabfd685dba2a844eb0a94e4947b5deb4041cb8ab45410b0c9214befdec6",
                              "quorum/twin/compression.py": "0f5e8bfca3e4480df26b8ea8a910fd4d842a86a141bf49b56ee5b79ad8d31d9f",
                              "quorum/twin/evidence.py": "84938adba839f66957e664ae43fc1dfd42872a28db2c480543e1677abc47eb1c"}},
}
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
INSTS = ("hh_approval", "hh_direction", "hh_generic_ballot")


def raw_names(reg: str) -> dict[str, str]:
    return {"hh_approval": f"{reg}_approval_raw", "hh_direction": f"{reg}_direction_raw",
            "hh_generic_ballot": f"{reg}_ballot_raw"}


def sha(p: Path) -> str:
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def check_source(src: Path, frame: Path, anchor: Path, cells: dict, reg: str, commit: str | None = None) -> list[str]:
    """Provenance and completeness of the emission before any transform (Codex HH2 pre-review 5)."""
    probs = []
    want_anchor = REGISTRATIONS[reg]["anchor_sha"]
    if sha(frame) != FRAME_SHA:
        probs.append(f"frame sha {sha(frame)[:12]} is not the registered {FRAME_SHA[:12]}")
    if sha(anchor) != want_anchor:
        probs.append(f"anchor sha {sha(anchor)[:12]} is not the registered {want_anchor[:12]}")
    text = anchor.read_text().strip()
    for inst in INSTS:
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
    probs += check_emission(src, cells, reg, commit)
    return probs


def check_emission(src: Path, cells: dict, reg: str, commit: str | None = None) -> list[str]:
    """Manifests, instrument specs, forecasts recomputed from rows, and no zeroed options
    (Codex HH2 confirmation review 1 and 3); for HH3 also the registered commit and source (Codex HH3 pre 4)."""
    probs = []
    regd = REGISTRATIONS[reg]
    root = Path(__file__).resolve().parents[1]
    rm = src / "run-manifest.json"
    if not rm.exists():
        return probs + ["run-manifest.json missing"]
    run = json.loads(rm.read_text())
    if run.get("revision") != REVISION or run.get("adapter_sha256") != ADAPTER_SHA:
        probs.append("run manifest: revision or adapter hashes differ from the registration")
    if "source_sha256" in regd:
        if run.get("registration") != reg:
            probs.append(f"run manifest: registration {run.get('registration')}, not {reg}")
        probs += check_commit_and_source(src, run, regd["source_sha256"], commit, root)
    else:  # HH2, as registered
        if not run.get("code_commit"):
            probs.append("run manifest: no code commit")
        want_src = {f: sha(root / f) for f in SOURCE_FILES}
        if run.get("source_sha256") != want_src:
            probs.append("run manifest: inference source on the box differs from this checkout")
    for inst in INSTS:
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
        if ds.get("frame_hh.csv") != FRAME_SHA or ds.get(regd["anchor_name"]) != regd["anchor_sha"]:
            probs.append(f"{inst}: manifest dataset hashes differ from the registered frame and anchor")
        # `+dirty` comes only from untracked generated files: check_commit_and_source requires the box's tracked
        # files unchanged before and after the emission
        if "source_sha256" in regd and commit and man.get("commit") not in (commit, commit + "+dirty"):
            probs.append(f"{inst}: manifest commit {man.get('commit')} is not the registered emission commit")
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


def check_commit_and_source(src: Path, run: dict, registered: dict, commit: str | None, root: Path) -> list[str]:
    """The emission commit is given explicitly and matches the run manifest; the inference source on the box and in
    this checkout equals the registered constants; the box's workdir passed scripts/hh3_box_tree.py before and after the
    emission with the same absences (the FT method: 0 edited, 0 untracked outside the job's paths, absences only where
    the upload rule leaves files out; Codex HH3 confirm 1); HH3-DONE names this SHA256SUMS.box (Codex HH3 confirm 2)."""
    probs = []
    if not commit or not COMMIT_RE.match(commit):
        return ["the registered emission commit (--emission-commit, 40 hex characters) is required"]
    if run.get("code_commit") != commit or run.get("box_git_head") != commit:
        probs.append(f"run manifest: commit {run.get('code_commit')} / box head {run.get('box_git_head')} "
                     f"is not the registered emission commit {commit[:12]}")
    if run.get("source_sha256") != registered:
        probs.append("run manifest: inference source on the box differs from the registered hashes")
    if {f: sha(root / f) for f in SOURCE_FILES} != registered:
        probs.append("this checkout's inference source differs from the registered hashes")
    before = run.get("box_tree_before") or {}
    after_p = src / "box-tree-after.json"
    after = json.loads(after_p.read_text()) if after_p.exists() else {}
    for name, t in (("before", before), ("after", after)):
        if t.get("mode") != "box" or t.get("ok") is not True or t.get("edited") != [] \
                or t.get("untracked_outside") != [] or t.get("absent_not_excluded") != []:
            probs.append(f"box workdir {name} the emission is not HH3_COMMIT as uploaded ({t or 'no record'})")
    if before and after and (before.get("absent"), before.get("absent_sha256")) != (after.get("absent"), after.get("absent_sha256")):
        probs.append("box workdir: tracked absences differ before and after the emission")
    sums, done = src / "SHA256SUMS.box", src / "HH3-DONE"
    if not done.exists() or not sums.exists():
        probs.append("HH3-DONE or SHA256SUMS.box missing: the box did not finish its checks")
    else:
        f = dict(kv.split("=", 1) for kv in done.read_text().split() if "=" in kv)
        if f.get("sums") != sha(sums) or f.get("commit") != commit or f.get("edited") != "0" \
                or f.get("untracked_outside") != "0" or f.get("absent") != str(after.get("absent")):
            probs.append(f"HH3-DONE does not match this emission ({done.read_text().strip()})")
    return probs


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--src", required=True, help="emission folder with <instrument>/rows.jsonl + forecast.json")
    ap.add_argument("--out", required=True)
    ap.add_argument("--registration", choices=sorted(REGISTRATIONS), default="hh2",
                    help="whose registered constants to apply (default hh2, HH2's published command)")
    ap.add_argument("--frame", default=str(b.FRAME), help="the registered HH frame (sha checked)")
    ap.add_argument("--anchor", help="the registered anchor (sha checked); default: the registration's anchor_path")
    ap.add_argument("--emission-commit", help="the registered emission commit (HH3 onward: required)")
    a = ap.parse_args()
    reg = a.registration
    regd = REGISTRATIONS[reg]
    anchor = Path(a.anchor or regd["anchor_path"])
    b.SRC = Path(a.src)  # build_hh1b's load_rows/emit read this module global
    b.FRAME = Path(a.frame)
    out = Path(a.out)
    cells = load_frame_csv(str(b.FRAME))
    probs = check_source(b.SRC, Path(a.frame), anchor, cells, reg, a.emission_commit)
    if probs:
        for x in probs:
            print("REFUSED:", x)
        return 1

    for inst, name in raw_names(reg).items():  # raw arms: the emitted files, unchanged
        d = out / name
        d.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(b.SRC / inst / "forecast.json", d / "forecast.json")
        print(f"{name:20s} copied  sha {hashlib.sha256((d / 'forecast.json').read_bytes()).hexdigest()[:12]}")

    inst = "hh_approval"
    spec = INSTRUMENTS[inst]
    softs, _ = b.load_rows(inst)
    sub = {k: cells[k] for k in softs}
    cal = {k: calibrate_soft(d, spec, b.A_APPR, b.B_APPR) for k, d in softs.items()}
    b.emit(out, f"{reg}_approval_cal", aggregate(sub, cal, inst), inst,
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
    target = regd["dk_target"]
    if not dk_at(0.0) <= target <= raw_dk:
        print(f"REFUSED: DK target {target} outside the reachable range {dk_at(0.0):.2f}-{raw_dk:.2f}")
        return 1
    s = b.solve(dk_at, target, 0.0, 1.0, iters=200)
    dks = {k: dk_shrink(d, spec, s) for k, d in softs.items()}
    b.emit(out, f"{reg}_direction_dk", aggregate(sub, dks, inst), inst,
           {"method": "dk_shrink", "s": s, "solved_on": "unrounded aggregate DK", "fit": f"solved so aggregate DK = {target} "
            f"({regd['dk_wave']}, right-track DK; in-sample for that one number, disclosed)",
            "raw_dk": round(raw_dk, 1)})
    print(f"  direction DK {raw_dk:.1f} -> {target} (s {s:.4f})")

    inst = "hh_generic_ballot"
    spec = INSTRUMENTS[inst]
    softs, _ = b.load_rows(inst)
    sub = {k: cells[k] for k in softs}
    bal = {k: calibrate_soft(d, spec, b.A_BAL, b.B_BAL) for k, d in softs.items()}
    b.emit(out, f"{reg}_ballot_cal", aggregate(sub, bal, inst), inst,
           {"a": b.A_BAL, "b": b.B_BAL, "family": "HOUSE_BALLOT_NS"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
