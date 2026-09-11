"""Midterm capstone — turnout multipliers from the CPS November 2022 Voting and
Registration Supplement (public-use microdata, U.S. Census Bureau), declared once in
docs/midterm-capstone-protocol.md (Chirag 2026-09-11: CPS 2022).

Cells match the W161 profile strings the engine saw: Age {18-29, 30-49, 50-64, 65+} x
Ethnicity {White non-Hispanic, Black non-Hispanic, Hispanic, Asian non-Hispanic, Other} x
Education {H.S. graduate or less, Some College, College graduate+}.

Turnout rate per cell = weighted "reported voted" (PES1 == 1) over weighted citizens 18+
(PRCITSHP in 1..4) — the Census "citizen population" basis, nonresponse counted as not
voted. Multiplier = cell rate / overall rate (so the frame's total weight is roughly
preserved and the electorate's composition replaces the adult population's). Cells with
fewer than 100 unweighted citizen records fall back to the age x ethnicity marginal,
declared in the output.

    PYTHONPATH=. python3 scripts/turnout_weights.py \
        --csv data/cps/nov22pub.csv --out docs/capstone-turnout-2022.json
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict

AGE = lambda a: "18-29" if a < 30 else "30-49" if a < 50 else "50-64" if a < 65 else "65+"


def race(hisp: int, r: int) -> str:
    if hisp == 1:
        return "Hispanic"
    return {1: "White non-Hispanic", 2: "Black non-Hispanic", 4: "Asian non-Hispanic"}.get(r, "Other")


def educ(e: int) -> str:
    return "H.S. graduate or less" if e <= 39 else "Some College" if e <= 42 else "College graduate+"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", default="data/cps/nov22pub.csv")
    ap.add_argument("--out", default="docs/capstone-turnout-2022.json")
    ap.add_argument("--min-n", type=int, default=100)
    a = ap.parse_args()
    num, den, n = defaultdict(float), defaultdict(float), defaultdict(int)
    mnum, mden = defaultdict(float), defaultdict(float)
    tot_num = tot_den = 0.0
    with open(a.csv, newline="") as f:
        for r in csv.DictReader(f):
            try:
                age = int(r["PRTAGE"]); cit = int(r["PRCITSHP"]); pes1 = int(r["PES1"])
                w = float(r["PWSSWGT"]); e = int(r["PEEDUCA"]); rc = int(r["PTDTRACE"]); h = int(r["PEHSPNON"])
            except (KeyError, ValueError):
                continue
            if age < 18 or cit not in (1, 2, 3, 4) or w <= 0 or e < 31:
                continue
            key = (AGE(age), race(h, rc), educ(e)); mkey = (AGE(age), race(h, rc))
            v = w if pes1 == 1 else 0.0
            num[key] += v; den[key] += w; n[key] += 1
            mnum[mkey] += v; mden[mkey] += w
            tot_num += v; tot_den += w
    overall = tot_num / tot_den
    table, fallback = {}, []
    for key in sorted(den):
        if n[key] >= a.min_n:
            rate = num[key] / den[key]
        else:
            rate = mnum[key[:2]] / mden[key[:2]]; fallback.append(" | ".join(key))
        table[" | ".join(key)] = {"turnout": round(rate, 4), "multiplier": round(rate / overall, 4),
                                  "unweighted_n": n[key]}
    out = {"source": "U.S. Census Bureau, Current Population Survey, November 2022 Voting and "
                     "Registration Supplement, public-use microdata (nov22pub.csv, "
                     "www2.census.gov/programs-surveys/cps/datasets/2022/supp/)",
           "basis": "reported voted (PES1==1) / citizens 18+ (PRCITSHP 1-4), weight PWSSWGT; "
                    "nonresponse counted as not voted (Census citizen-population basis)",
           "overall_turnout_citizens_18plus": round(overall, 4),
           "cells": table, "fallback_to_age_x_ethnicity": fallback,
           "declared": "docs/midterm-capstone-protocol.md (Chirag 2026-09-11: CPS 2022, once)"}
    json.dump(out, open(a.out, "w"), indent=1)
    print(f"overall citizen turnout {overall:.3f}; {len(table)} cells, {len(fallback)} fell back; wrote {a.out}")
    for k, v in table.items():
        print(f"  {k:60s} turnout {v['turnout']:.3f}  mult {v['multiplier']:.3f}  n={v['unweighted_n']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
