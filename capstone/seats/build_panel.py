"""Build the 2014-2024 district panel from MEDSL returns and the archived Wikipedia tables.

Usage: python -I build_panel.py <medsl.csv> <wiki_hist_rows.json> <out_panel.csv>
Columns: year, state, dist, pvi, lean (2*pvi, margin points), inc (+1 D, -1 R, 0 open),
dv, rv, tv (two-party votes), margin, contested, d_on_ballot, r_on_ballot, redrawn.
"""
import json
import re
import sys

import numpy as np
import pandas as pd

STATES = {
    "ALABAMA", "ALASKA", "ARIZONA", "ARKANSAS", "CALIFORNIA", "COLORADO", "CONNECTICUT", "DELAWARE",
    "FLORIDA", "GEORGIA", "HAWAII", "IDAHO", "ILLINOIS", "INDIANA", "IOWA", "KANSAS", "KENTUCKY",
    "LOUISIANA", "MAINE", "MARYLAND", "MASSACHUSETTS", "MICHIGAN", "MINNESOTA", "MISSISSIPPI", "MISSOURI",
    "MONTANA", "NEBRASKA", "NEVADA", "NEW HAMPSHIRE", "NEW JERSEY", "NEW MEXICO", "NEW YORK",
    "NORTH CAROLINA", "NORTH DAKOTA", "OHIO", "OKLAHOMA", "OREGON", "PENNSYLVANIA", "RHODE ISLAND",
    "SOUTH CAROLINA", "SOUTH DAKOTA", "TENNESSEE", "TEXAS", "UTAH", "VERMONT", "VIRGINIA", "WASHINGTON",
    "WEST VIRGINIA", "WISCONSIN", "WYOMING",
}
# Maps first used in that year. 2022 is the national redraw; the rest are the states that
# adopted a new map for that election.
REDRAWN = {
    2016: {"FLORIDA", "NORTH CAROLINA", "VIRGINIA"},
    2018: {"PENNSYLVANIA"},
    2020: {"NORTH CAROLINA"},
    2022: STATES,
    2024: {"ALABAMA", "GEORGIA", "LOUISIANA", "NEW YORK", "NORTH CAROLINA"},
}


def parse_pvi(s):
    s = s.replace(" ", "")
    m = re.fullmatch(r"(D|R)\+(\d+)", s)
    if m:
        return int(m.group(2)) * (1 if m.group(1) == "D" else -1)
    if s.upper() == "EVEN":
        return 0
    return np.nan


def parse_location(loc):
    m = re.match(r"(.+?)\s+(\d+|at-large|At-large|at large)\b", loc)
    if not m:
        return None, None
    st = m.group(1).upper()
    d = 1 if not m.group(2).isdigit() else int(m.group(2))
    return st, d


def party_of(p):
    p = (p or "").lower()
    if p.startswith(("democrat", "dfl")):
        return "D"
    if p.startswith("republican"):
        return "R"
    return "O"


RUNNING = re.compile(r"re-?elected|lost re-?election|lost reelection|lost general", re.I)


def incumbency(rows):
    """Return +1, -1 or 0 from the table rows for one district and year."""
    d = any(party_of(r.get("party")) == "D" and RUNNING.search(r.get("status", "")) for r in rows)
    r_ = any(party_of(r.get("party")) == "R" and RUNNING.search(r.get("status", "")) for r in rows)
    return int(d) - int(r_)


def main():
    medsl, wiki, out = sys.argv[1:4]
    d = pd.read_csv(medsl, low_memory=False)
    d = d[(d.year >= 2014) & (d.stage == "GEN") & (~d.special.astype(bool)) & d.state.isin(STATES)].copy()
    d["dist"] = d.district.astype(int).replace(0, 1)
    # Florida records an unopposed winner as a vote count of 1 or, once, -1 (FL-25 in 2020).
    d["candidatevotes"] = d.candidatevotes.abs()
    d["p"] = d.party.fillna("").astype(str).str.upper()
    d["isD"] = d.p.str.startswith("DEMOCRAT")
    d["isR"] = d.p.str.startswith("REPUBLICAN")
    key = ["year", "state", "dist"]
    # Fusion: a candidate's votes on minor-party lines join that candidate's major-party line.
    named = d[~d.candidate.fillna("").str.upper().isin(["BLANK", "VOID", "SCATTERING", "WRITEIN", "OVERVOTES", "UNDERVOTES"])]
    cand = named.groupby(key + ["candidate"]).agg(
        votes=("candidatevotes", "sum"), isD=("isD", "max"), isR=("isR", "max"), wi=("writein", "min")
    ).reset_index()
    cand["dv"] = np.where(cand.isD, cand.votes, 0)
    cand["rv"] = np.where(cand.isR & ~cand.isD, cand.votes, 0)
    cand["d_ballot"] = cand.isD & ~cand.wi.astype(bool)
    cand["r_ballot"] = cand.isR & ~cand.wi.astype(bool)
    g = cand.groupby(key).agg(dv=("dv", "sum"), rv=("rv", "sum"), d_on_ballot=("d_ballot", "max"), r_on_ballot=("r_ballot", "max")).reset_index()
    g["tv"] = g.dv + g.rv
    g["margin"] = 100 * (g.dv - g.rv) / g.tv.where(g.tv > 0)

    rows = [r for r in json.load(open(wiki)) if r["year"] >= 2014]
    bucket = {}
    for r in rows:
        st, dist = parse_location(r.get("loc", ""))
        if st in STATES:
            bucket.setdefault((r["year"], st, dist), []).append(r)
    recs = []
    for (y, st, dist), rs in bucket.items():
        recs.append({"year": y, "state": st, "dist": dist, "pvi": parse_pvi(rs[0].get("pvi", "")), "inc": incumbency(rs),
                     "member": "; ".join(x.get("member", "") for x in rs), "status": " / ".join(x.get("status", "")[:60] for x in rs)})
    w = pd.DataFrame(recs)
    p = g.merge(w, on=key, how="outer", indicator=True)
    print(p._merge.value_counts().to_dict())
    print(p[p._merge != "both"][key + ["dv", "rv", "pvi", "_merge"]].to_string())
    p = p[p._merge == "both"].drop(columns="_merge")
    p["lean"] = 2 * p.pvi
    # Contested: both major parties on the ballot, and neither below 2 percent of the two-party vote.
    p["contested"] = p.d_on_ballot & p.r_on_ballot & (p.dv > 0.02 * p.tv) & (p.rv > 0.02 * p.tv)
    p["redrawn"] = [int(st in REDRAWN.get(y, set())) for y, st in zip(p.year, p.state)]
    p.to_csv(out, index=False)
    print(p.groupby("year").agg(n=("dist", "size"), contested=("contested", "sum"), incD=("inc", lambda s: (s == 1).sum()),
                                incR=("inc", lambda s: (s == -1).sum()), open=("inc", lambda s: (s == 0).sum()), pvi_na=("pvi", lambda s: s.isna().sum())))
    n = p.groupby("year").apply(lambda x: pd.Series({"M": 100 * (x.dv.sum() - x.rv.sum()) / x.tv.sum(), "dv": x.dv.sum(), "rv": x.rv.sum()}), include_groups=False)
    print(n.round(3))


if __name__ == "__main__":
    main()
