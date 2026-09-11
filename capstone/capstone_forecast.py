"""Midterm capstone forecast — national two-party House margin (D − R) from the ballot
instrument, calibrated (HOUSE_BALLOT_NS Platt), with the frame reweighted by the declared
CPS-2022 turnout multipliers (scripts/turnout_weights.py). Two-party convention: Other /
Not sure / Will not vote mass is dropped and D, R renormalized.

    PYTHONPATH=. python3 scripts/capstone_forecast.py --raw-dir <ballot raw run dir> \
        --turnout docs/capstone-turnout-2022.json [--identity]   # --identity: multipliers=1

--identity must reproduce the registered calibrated ballot arm's D/R shares (the dry-run
test against FT5 arm F-cal).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re

from quorum.twin.forecast import aggregate, calibrate_soft, load_frame
from quorum.twin.instruments import INSTRUMENTS

A_BAL, B_BAL = 2.7534, 0.4401  # HOUSE_BALLOT_NS, frozen 2026-08-26


def cell_key(profile: str) -> str | None:
    """Age | Ethnicity | Education as the profile states them; None if any line is absent
    (such profiles keep multiplier 1 and are counted in the run's 'missing' figure)."""
    f = {}
    for k in ("Age", "Ethnicity", "Education"):
        m = re.search(rf"- {k}: (.+)", profile)
        if not m:
            return None
        f[k] = m.group(1).strip()
    return f"{f['Age']} | {f['Ethnicity']} | {f['Education']}"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", required=True)
    ap.add_argument("--turnout", default="docs/capstone-turnout-2022.json")
    ap.add_argument("--sav", default="data/pew/atp/w161/W161_Feb25/ATP W161.sav")
    ap.add_argument("--identity", action="store_true", help="multipliers = 1 (reproduce the F-cal arm)")
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    spec = INSTRUMENTS["yougov_house_ballot"]; n = len(spec["options"])
    cells = load_frame(a.sav)
    rows = [json.loads(l) for l in open(os.path.join(a.raw_dir, "rows.jsonl"))]
    mult = {} if a.identity else {k: v["multiplier"] for k, v in json.load(open(a.turnout))["cells"].items()}
    softs, sub, missing = {}, {}, 0
    for r in rows:
        k = r["profile"]
        softs[k] = calibrate_soft({i: r[f"p{i}"] for i in range(1, n + 1)}, spec, A_BAL, B_BAL)
        c = dict(cells[k])
        if not a.identity:
            ck = cell_key(k)
            m = mult.get(ck) if ck else None
            if m is None:
                missing += 1; m = 1.0
            c["w"] = c["w"] * m
        sub[k] = c
    res = aggregate(sub, softs, "yougov_house_ballot")
    t = res["topline"]
    d, rr = t["Positive"], t["Negative"]
    two = {"D_two_party": round(100 * d / (d + rr), 2), "R_two_party": round(100 * rr / (d + rr), 2)}
    two["margin_D_minus_R"] = round(two["D_two_party"] - two["R_two_party"], 2)
    print(f"{'identity (mult=1)' if a.identity else 'CPS-2022 reweighted'}: D {d} R {rr} "
          f"(Other/NS/WNV {round(100 - d - rr, 1)}) -> two-party D {two['D_two_party']} R {two['R_two_party']} "
          f"margin {two['margin_D_minus_R']:+.2f}; party D-share " +
          " / ".join(f"{g} {res['by']['party'][g]['Positive']}" for g in ("Dem", "Ind", "Rep")) +
          (f"; {missing} profiles without a turnout cell (mult 1)" if missing else ""))
    if a.out:
        res["two_party"] = two
        res["turnout"] = "identity" if a.identity else {"file": a.turnout,
                          "sha256": hashlib.sha256(open(a.turnout, "rb").read()).hexdigest()}
        res["calibration"] = {"a": A_BAL, "b": B_BAL, "family": "HOUSE_BALLOT_NS"}
        os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
        json.dump(res, open(a.out, "w"), indent=2); print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
