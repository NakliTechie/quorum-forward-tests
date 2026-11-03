"""Capstone voter-group shares — the two-party House vote by voter group, computed from the published
capstone rows (registered 2026-09-11) with the same calibration and turnout weights as the registered
national margin, and the scorer for the election-night voter surveys (docs/capstone/groups-2026-11-03/).

    PYTHONPATH=. python3 scripts/capstone_groups.py forecast --rows <rows-capstone-2026-09-11.jsonl> --out <json>
    PYTHONPATH=. python3 scripts/capstone_groups.py score --forecast <json> --survey <json> \
        [--baseline <json>] --out <json>

A survey or baseline file is {"source": ..., "overall": [D, R], "groups": {name: [D, R], ...}} with the
percentages as printed; only D and R are used (two-party convention). The forecast reads no frame file:
each row carries its frame weight, so the public rows alone reproduce the registered numbers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re

from quorum.twin.forecast import calibrate_soft
from quorum.twin.instruments import INSTRUMENTS

A_BAL, B_BAL = 2.7534, 0.4401  # HOUSE_BALLOT_NS, frozen 2026-08-26 (as scripts/capstone_forecast.py)
LEVEL_BAR, LEAN_BAR = 6.0, 4.0
NO_DEGREE = ("Some College", "H.S. graduate or less")
GROUPS = {   # name -> test on the profile's lines; age bands are the frame's (30-49 and 50-64 have no survey match)
    "Women": lambda a: a["Gender"] == "Woman",
    "Men": lambda a: a["Gender"] == "Man",
    "Age 18-29": lambda a: a["Age"] == "18-29",
    "Age 65+": lambda a: a["Age"] == "65+",
    "White": lambda a: a["Ethnicity"] == "White non-Hispanic",
    "Black": lambda a: a["Ethnicity"] == "Black non-Hispanic",
    "Hispanic": lambda a: a["Ethnicity"] == "Hispanic",
    "Asian": lambda a: a["Ethnicity"] == "Asian non-Hispanic",
    "College graduate": lambda a: a["Education"] == "College graduate+",
    "No college degree": lambda a: a["Education"] in NO_DEGREE,
    "White college graduate": lambda a: a["Ethnicity"] == "White non-Hispanic" and a["Education"] == "College graduate+",
    "White no college degree": lambda a: a["Ethnicity"] == "White non-Hispanic" and a["Education"] in NO_DEGREE,
    "Income under $50,000": lambda a: a["Income"] in ("Less than $30,000", "$30,000 to less than $40,000",
                                                      "$40,000 to less than $50,000"),
    "Income $100,000 or more": lambda a: a["Income"] == "$100,000 or more",
    "Democrats": lambda a: a["Party affiliation"] == "Democrat",
    "Republicans": lambda a: a["Party affiliation"] == "Republican",
    "Independents": lambda a: a["Party affiliation"] == "Independent",
}
GAPS = {"Gender (women - men)": ("Women", "Men"), "Age (18-29 - 65+)": ("Age 18-29", "Age 65+"),
        "Education (college - no degree)": ("College graduate", "No college degree"),
        "White education (college - no degree)": ("White college graduate", "White no college degree"),
        "Black - White": ("Black", "White"), "Hispanic - White": ("Hispanic", "White")}
FIELDS = ("Age", "Gender", "Ethnicity", "Education", "Income", "Party affiliation")


def _line(profile: str, key: str) -> str | None:
    m = re.search(rf"- {key}: (.+)", profile)
    return m.group(1).strip() if m else None


def two_party(d: float, r: float) -> float:
    return 100 * d / (d + r)


def forecast(rows_path: str, turnout_path: str) -> dict:
    spec = INSTRUMENTS["yougov_house_ballot"]; n = len(spec["options"])
    mult = {k: v["multiplier"] for k, v in json.load(open(turnout_path))["cells"].items()}
    cells = []
    for line in open(rows_path):
        r = json.loads(line); p = r["profile"]
        s = calibrate_soft({i: r[f"p{i}"] for i in range(1, n + 1)}, spec, A_BAL, B_BAL)
        a = {k: _line(p, k) for k in FIELDS}
        key = " | ".join(a[k] or "" for k in ("Age", "Ethnicity", "Education"))
        w = r["w"] * (mult.get(key, 1.0) if all(a[k] for k in ("Age", "Ethnicity", "Education")) else 1.0)
        cells.append((w, s[1], s[2], a))
    total = sum(c[0] for c in cells)

    def share(test) -> dict:
        sel = [c for c in cells if test(c[3])]
        w = sum(c[0] for c in sel); d = sum(c[0] * c[1] for c in sel); r = sum(c[0] * c[2] for c in sel)
        return {"D": round(100 * d / w, 2), "R": round(100 * r / w, 2), "D_two_party": round(two_party(d, r), 2),
                "weight_share": round(w / total, 4), "n_profiles": len(sel)}

    groups = {g: share(t) for g, t in GROUPS.items()}
    overall = share(lambda a: True)
    return {"overall": overall, "groups": groups,
            "lean": {g: round(v["D_two_party"] - overall["D_two_party"], 2) for g, v in groups.items()},
            "gaps": {k: round(groups[a]["D_two_party"] - groups[b]["D_two_party"], 2) for k, (a, b) in GAPS.items()},
            "inputs": {os.path.basename(p): hashlib.sha256(open(p, "rb").read()).hexdigest() for p in (rows_path, turnout_path)},
            "calibration": {"a": A_BAL, "b": B_BAL, "family": "HOUSE_BALLOT_NS"}}


def _survey_shares(s: dict) -> tuple[float, dict]:
    missing = [g for g in GROUPS if g not in s["groups"]]
    if missing:
        raise SystemExit(f"survey file lacks groups {missing}: record each as printed, or as null when the source has none")
    overall = two_party(*s["overall"])
    return overall, {g: two_party(*v) for g, v in s["groups"].items() if v is not None and g in GROUPS}


def score(fc: dict, survey: dict, baseline: dict | None = None) -> dict:
    overall, sv = _survey_shares(survey)
    ours = {g: fc["groups"][g]["D_two_party"] for g in sv}
    ours_lean = {g: fc["lean"][g] for g in sv}
    sv_lean = {g: v - overall for g, v in sv.items()}
    level = {g: round(ours[g] - sv[g], 2) for g in sv}
    lean = {g: round(ours_lean[g] - sv_lean[g], 2) for g in sv}
    mae = lambda d: round(sum(abs(v) for v in d.values()) / len(d), 2)
    out = {"source": survey["source"], "groups_scored": len(sv), "survey_overall_D_two_party": round(overall, 2),
           "level_error": level, "lean_error": lean, "level_mae": mae(level), "lean_mae": mae(lean),
           "level_bar": LEVEL_BAR, "lean_bar": LEAN_BAR,
           "level_pass": mae(level) <= LEVEL_BAR, "lean_pass": mae(lean) <= LEAN_BAR,
           "gaps": {k: {"ours": fc["gaps"][k], "survey": round(sv[a] - sv[b], 2)}
                    for k, (a, b) in GAPS.items() if a in sv and b in sv}}
    if baseline is not None:   # persistence: the same source's 2022 leans for the same groups
        b_overall, bv = _survey_shares(baseline)
        both = [g for g in sv if g in bv]
        pers = {g: round((bv[g] - b_overall) - sv_lean[g], 2) for g in both}
        out["head_to_head"] = {"baseline": baseline["source"], "groups": len(both),
                               "ours_lean_mae": mae({g: lean[g] for g in both}), "persistence_lean_mae": mae(pers),
                               "persistence_lean_error": pers}
        out["head_to_head"]["upheld"] = out["head_to_head"]["ours_lean_mae"] < out["head_to_head"]["persistence_lean_mae"]
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("forecast"); f.add_argument("--rows", required=True)
    f.add_argument("--turnout", default="docs/capstone-turnout-2022.json"); f.add_argument("--out", required=True)
    s = sub.add_parser("score"); s.add_argument("--forecast", required=True); s.add_argument("--survey", required=True)
    s.add_argument("--baseline"); s.add_argument("--out", required=True)
    a = ap.parse_args()
    if os.path.exists(a.out):
        raise SystemExit(f"{a.out} exists; never overwritten")
    if a.cmd == "forecast":
        res = forecast(a.rows, a.turnout)
    else:
        res = score(json.load(open(a.forecast)), json.load(open(a.survey)),
                    json.load(open(a.baseline)) if a.baseline else None)
    os.makedirs(os.path.dirname(a.out) or ".", exist_ok=True)
    json.dump(res, open(a.out, "w"), indent=2); print(f"wrote {a.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
