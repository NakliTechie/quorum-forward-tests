"""HH1-B — companion arms for the Harvard CAPS/Harris registration (Chunk E, 2026-09-03).

CPU-only transforms of the HH1 emission rows (artifacts-approval/gallup-registration/
hh_*; frame = W161 recomposed to HH party targets, quorum-forward-tests/hh1/frame_hh.csv).
HH1's original arms are untouched; these are registered as a companion, scored on the
same target wave (the first HH poll to begin fielding after the public push).

Arms (declared in docs/hh1b-registration-draft.md before any number existed):
  approval_cal        Platt on the conditional approve share, family approval_pooled_2019_2025
                      (a = 3.6133, b = 1.3759) — the E/YouGov calibrated method, unchanged.
  approval_cal_house  the same, plus a single logit intercept shift delta solved so the
                      TOPLINE approve equals approval_cal's topline + 7.2 (HH1's declared
                      house offset, applied INSIDE the calibrated distribution so party
                      cuts move consistently; HH1's original companion added it to the
                      topline only — disclosed).
  direction_dk        abstain-shrink s (E35 form) solved so the aggregate DK equals the
                      August 2026 published DK (11.0) — one number fit in-sample on the
                      shadow wave, disclosed; freed mass redistributed right/wrong
                      proportionally. No Platt (FT4 disclosure 9: the direction map
                      moves the wrong way).
  ballot_cal          Platt HOUSE_BALLOT_NS (a = 2.7534, b = 0.4401) on the two-row
                      forced-choice share.

    PYTHONPATH=. python3 scripts/build_hh1b.py --out artifacts-approval/hh1b
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from dk_shrink import dk_shrink  # noqa: E402

from quorum.twin.forecast import aggregate, calibrate_soft, load_frame_csv  # noqa: E402
from quorum.twin.instruments import INSTRUMENTS  # noqa: E402

REPO = Path(__file__).resolve().parents[1]
SRC = REPO / "artifacts-approval" / "gallup-registration"
FRAME = Path.home() / "Code" / "quorum-forward-tests" / "hh1" / "frame_hh.csv"
A_APPR, B_APPR = 3.6133, 1.3759          # approval_pooled_2019_2025 (FT1-4)
A_BAL, B_BAL = 2.7534, 0.4401            # HOUSE_BALLOT_NS (E16, frozen 2026-08-26)
HOUSE_OFFSET = 7.2                       # HH1 declared (recon, five-wave gap)
AUG_DK = 11.0                            # HH August 2026 wave, right-track DK (p.4)


def load_rows(inst: str) -> tuple[dict[str, dict[int, float]], int]:
    n = len(INSTRUMENTS[inst]["options"])
    rows = [json.loads(l) for l in open(SRC / inst / "rows.jsonl")]
    return {r["profile"]: {i: r[f"p{i}"] for i in range(1, n + 1)} for r in rows}, n


def positive_topline(cells, softs, inst) -> float:
    return aggregate(cells, softs, inst)["topline"]["Positive"]


def solve(fn, target: float, lo: float, hi: float, iters: int = 60) -> float:
    """Bisection on a monotone-increasing fn(x) -> value."""
    for _ in range(iters):
        mid = (lo + hi) / 2
        lo, hi = (mid, hi) if fn(mid) < target else (lo, mid)
    return (lo + hi) / 2


def emit(out_dir: Path, name: str, res: dict, src_inst: str, calibration: dict) -> str:
    src = json.load(open(SRC / src_inst / "forecast.json"))
    res["instrument"] = src["instrument"]
    res["calibration"] = calibration
    for k in ("anchor_sha256", "anchor_text"):
        res[k] = src[k]
    res["frame"] = {"source": "W161 recomposed to Harvard-Harris printed party targets "
                              "(quorum-forward-tests/hh1/frame_hh.csv)",
                    "n_profiles": src["frame"]["n_profiles"]}
    res["source_rows_sha256"] = hashlib.sha256(
        open(SRC / src_inst / "rows.jsonl", "rb").read()).hexdigest()
    d = out_dir / name
    d.mkdir(parents=True, exist_ok=True)
    p = d / "forecast.json"
    json.dump(res, open(p, "w"), indent=2)
    sha = hashlib.sha256(open(p, "rb").read()).hexdigest()
    t = res["topline"]
    print(f"{name:20s} Positive {t['Positive']:5.1f}  Negative {t['Negative']:5.1f}  "
          f"Net {t['Net']:+5.1f}  party " +
          " / ".join(f"{g} {res['by']['party'][g]['Positive']:.1f}" for g in ("Dem", "Ind", "Rep"))
          + f"  sha {sha[:12]}")
    return sha


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default="artifacts-approval/hh1b")
    a = ap.parse_args()
    out = Path(a.out)
    cells = load_frame_csv(str(FRAME))

    # --- approval ---
    inst = "hh_approval"
    spec = INSTRUMENTS[inst]
    softs, _ = load_rows(inst)
    sub = {k: cells[k] for k in softs}
    raw_top = positive_topline(sub, softs, inst)
    cal = {k: calibrate_soft(d, spec, A_APPR, B_APPR) for k, d in softs.items()}
    cal_top = positive_topline(sub, cal, inst)
    emit(out, "hh1b_approval_cal", aggregate(sub, cal, inst), inst,
         {"a": A_APPR, "b": B_APPR, "family": "approval_pooled_2019_2025"})

    target = cal_top + HOUSE_OFFSET
    delta = solve(lambda d: positive_topline(
        sub, {k: calibrate_soft(x, spec, A_APPR, B_APPR + d) for k, x in softs.items()}, inst),
        target, -4.0, 4.0)
    calh = {k: calibrate_soft(d, spec, A_APPR, B_APPR + delta) for k, d in softs.items()}
    emit(out, "hh1b_approval_cal_house", aggregate(sub, calh, inst), inst,
         {"a": A_APPR, "b": B_APPR, "family": "approval_pooled_2019_2025",
          "house_logit_shift": round(delta, 5), "house_offset_pts": HOUSE_OFFSET,
          "house_offset_source": "HH1 registration (five-wave HH vs E/YouGov gap, recon 2026-08-19)",
          "note": "offset applied inside the calibrated distribution (single intercept shift), "
                  "not to the topline"})
    print(f"  raw topline {raw_top:.1f} -> cal {cal_top:.1f} -> cal+house {target:.1f} "
          f"(delta {delta:+.4f})")

    # --- direction ---
    inst = "hh_direction"
    spec = INSTRUMENTS[inst]
    softs, _ = load_rows(inst)
    sub = {k: cells[k] for k in softs}
    dk_key = spec["abstain"][0]

    def dk_at(s):
        agg = aggregate(sub, {k: dk_shrink(d, spec, s) for k, d in softs.items()}, inst)
        return agg["topline"][dk_key]
    raw_dk = dk_at(1.0)
    s = solve(dk_at, AUG_DK, 0.0, 1.0)          # dk_at is increasing in s
    dks = {k: dk_shrink(d, spec, s) for k, d in softs.items()}
    emit(out, "hh1b_direction_dk", aggregate(sub, dks, inst), inst,
         {"method": "dk_shrink", "s": round(s, 5), "fit": f"solved so aggregate DK = {AUG_DK} "
          "(HH August 2026 wave, right-track DK; in-sample for that one number, disclosed)",
          "raw_dk": round(raw_dk, 1)})
    print(f"  direction DK {raw_dk:.1f} -> {AUG_DK} (s {s:.4f})")

    # --- ballot ---
    inst = "hh_generic_ballot"
    spec = INSTRUMENTS[inst]
    softs, _ = load_rows(inst)
    sub = {k: cells[k] for k in softs}
    bal = {k: calibrate_soft(d, spec, A_BAL, B_BAL) for k, d in softs.items()}
    emit(out, "hh1b_ballot_cal", aggregate(sub, bal, inst), inst,
         {"a": A_BAL, "b": B_BAL, "family": "HOUSE_BALLOT_NS"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
