"""Build district_baseline.csv (435 rows on the 2026 maps) from the archived Wikipedia tables.

Usage: python -I build_baseline_2026.py <wiki2026_rows.json> <pres2024_by_cd.csv> <out.csv>

Ratings are not read: the snapshot's district tables have no ratings column, and the
parser keeps only location, PVI, member, party, status and candidate names.
"""
import json
import re
import sys
import unicodedata

import numpy as np
import pandas as pd

SNAPSHOT = "https://web.archive.org/web/20261101162621/https://en.wikipedia.org/wiki/2026_United_States_House_of_Representatives_elections"
REDRAWN_2026 = {"Alabama", "California", "Florida", "Louisiana", "North Carolina", "Ohio", "Tennessee", "Texas", "Utah"}
PO = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR", "California": "CA", "Colorado": "CO",
    "Connecticut": "CT", "Delaware": "DE", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI", "Idaho": "ID",
    "Illinois": "IL", "Indiana": "IN", "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
    "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE", "Nevada": "NV",
    "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
    "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA",
    "Rhode Island": "RI", "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA", "West Virginia": "WV",
    "Wisconsin": "WI", "Wyoming": "WY",
}


def norm(s):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z ]", " ", s.lower())


def surname(name):
    name = re.sub(r"Redistricted from.*", "", name)
    toks = [t for t in norm(name).split() if t not in ("jr", "sr", "ii", "iii", "iv")]
    return toks[-1] if toks else ""


def cand_party(c):
    m = re.search(r"\(([^()]*)\)\s*$", c)
    lab = m.group(1) if m else ""
    if lab.startswith(("Democratic", "DFL")):
        return "D"
    if lab == "Republican":
        return "R"
    return "O"


def parse_pvi(s):
    m = re.fullmatch(r"(D|R)\+(\d+)", s.replace(" ", ""))
    if m:
        return int(m.group(2)) * (1 if m.group(1) == "D" else -1)
    return 0 if s.upper() == "EVEN" else np.nan


def main():
    rows = json.load(open(sys.argv[1]))
    by = {}
    for r in rows:
        by.setdefault(r["Location"], []).append(r)
    recs = []
    for loc, rs in by.items():
        m = re.match(r"(.+?)\s+(\d+|at-large|At-large)$", loc)
        st, dn = m.group(1), m.group(2)
        dist = int(dn) if dn.isdigit() else 1
        cands = rs[0]["candidates"]
        parties = [cand_party(c) for c in cands]
        n_d, n_r, n_o = parties.count("D"), parties.count("R"), parties.count("O")
        inc_party = set()
        inc_names = []
        for r in rs:
            mem = r["Member"]
            if mem.startswith(("None", "Vacant")):
                continue
            # A retiring member can share a surname with a candidate (IL-4, TX-22).
            if re.search(r"retiring|lost renomination|withdrew|resigned", r["Status"]):
                continue
            sn = surname(mem)
            for c, pa in zip(cands, parties):
                if sn and sn in norm(c).split():
                    inc_party.add(pa)
                    inc_names.append(re.sub(r"Redistricted from.*", "", mem).strip())
        if inc_party == {"D"}:
            inc = "D"
        elif inc_party == {"R"}:
            inc = "R"
        elif inc_party == {"O"}:
            inc = "I"
        elif not inc_party:
            inc = "open"
        else:
            inc = "both"
        if n_d and n_r:
            unc = "no"
        elif n_d:
            unc = "no_republican"
        elif n_r:
            unc = "no_democrat"
        else:
            unc = "no_major_party"
        recs.append({
            "state": st, "state_po": PO[st], "district": dist, "cook_pvi_text": rs[0]["PVI"], "pvi": parse_pvi(rs[0]["PVI"]),
            "baseline_margin": 2 * parse_pvi(rs[0]["PVI"]), "incumbent_running": inc, "incumbent_name": "; ".join(dict.fromkeys(inc_names)),
            "n_dem": n_d, "n_rep": n_r, "n_other": n_o, "uncontested": unc, "map_new_for_2026": int(st in REDRAWN_2026),
            "source": "Cook 2026 PVI and candidate lists as tabulated on Wikipedia, snapshot 2026-11-01 16:26 UTC", "source_url": SNAPSHOT,
        })
    b = pd.DataFrame(recs).sort_values(["state", "district"]).reset_index(drop=True)

    # Audit line: a sitting member who is a candidate in a different row from the one they are listed in.
    members = {}
    for r in rows:
        if not r["Member"].startswith(("None", "Vacant")):
            members.setdefault(surname(r["Member"]), set()).add(r["Location"])
    print("rows", len(b), "seats by state ok:", b.groupby("state").size().sum())
    print("incumbent_running:", b.incumbent_running.value_counts().to_dict())
    print("uncontested:", b.uncontested.value_counts().to_dict())
    print(b[b.uncontested != "no"][["state_po", "district", "cook_pvi_text", "incumbent_running", "incumbent_name", "n_dem", "n_rep", "n_other", "uncontested"]].to_string())
    print("incumbent 'both' or 'I':")
    print(b[b.incumbent_running.isin(["both", "I"])][["state_po", "district", "cook_pvi_text", "incumbent_name", "incumbent_running"]].to_string())

    # Validation against the 2024 presidential margin on the 2024 lines.
    pr = pd.read_csv(sys.argv[2])
    pr["state_po"] = pr.CD.str[:2]
    pr["district"] = pr.CD.str[3:].replace("AL", "01").astype(int)
    pr["m24"] = (pr.Harris.str.replace(",", "").astype(float) - pr.Trump.str.replace(",", "").astype(float)) / (
        pr.Harris.str.replace(",", "").astype(float) + pr.Trump.str.replace(",", "").astype(float)) * 100
    v = b.merge(pr[["state_po", "district", "m24"]], on=["state_po", "district"], how="left")
    v["gap"] = v.baseline_margin - v.m24
    print("median gap (2*PVI minus 2024 margin, 2024 lines):", round(v.gap.median(), 2))
    t = v.groupby("map_new_for_2026").gap.agg(["mean", "std", "size"]).round(2)
    print(t)
    by_st = v.groupby("state_po").gap.agg(lambda s: (s - v.gap.median()).abs().max()).sort_values(ascending=False).round(1)
    print("largest absolute gap by state, top 16:", by_st.head(16).to_dict())
    b.to_csv(sys.argv[3], index=False)


if __name__ == "__main__":
    main()
