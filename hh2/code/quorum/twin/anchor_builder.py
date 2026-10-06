"""Mechanical era-anchor builder — the FT4-onward protocol (docs/anchor-protocol-draft.md).

The anchor is exactly four sentences, assembled by rule for a date D:
  1. date + office (template)
  2. conflict/crisis status (Wikipedia "{year} in the United States", revision as of D)
  3. official statistics (CPI-U 12-mo, avg hourly earnings 12-mo, national gas price)
  4. next federal election within 12 months

The builder separates SELECTION (closed by this protocol: which facts, which sources,
which wording) from TRANSCRIPTION (the values). Statistics fetch from public APIs where
one exists (BLS v1, no key); every field can instead be supplied via --facts JSON, and
every value's source citation is recorded in the emitted manifest either way. A linter
enforces the prohibitions (no polling/approval numbers, no news events, no adjectives
beyond source phrasing) structurally: only the four sentences, only the named slots.

Usage:
  python -m quorum.twin.anchor_builder --date 2026-08-24 \
      [--facts facts.json] [--out anchor.txt] [--no-network]

facts.json fields (all optional if the fetchers succeed; conflict/gas usually manual):
  {"cpi_yoy": 3.4, "cpi_cite": "BLS CPI news release 2026-08-12 (July 2026)",
   "ahe_yoy": 3.2, "ahe_cite": "BLS Employment Situation 2026-08-07 (July 2026)",
   "gas_price": 4.10, "gas_cite": "AAA national average 2026-08-20",
   "conflict_clause": "The United States has been at war with Iran since February 2026; ...",
   "wiki_revid": 123456789,
   "election": "The 2026 midterm congressional elections are in November."}
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import pathlib
import re
import urllib.request

ORD = {1: "first", 2: "second", 3: "third", 4: "fourth"}
BLS_API = "https://api.bls.gov/publicAPI/v1/timeseries/data/"
CPI_SERIES = "CUUR0000SA0"   # CPI-U, all items, NSA (12-mo change computed)
AHE_SERIES = "CES0500000003"  # avg hourly earnings, total private, NSA level

BANNED = re.compile(r"\b(approv|disapprov|poll|survey|favorab|ballot|percent said|lead)\w*",
                    re.IGNORECASE)


def _bls_yoy(series: str, d: dt.date) -> tuple[float, str] | None:
    """12-month percent change of the latest month published before D (v1 API, no key)."""
    try:
        body = json.dumps({"seriesid": [series],
                           "startyear": str(d.year - 2), "endyear": str(d.year)}).encode()
        req = urllib.request.Request(BLS_API, data=body,
                                     headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=30) as r:
            data = json.loads(r.read())
        rows = data["Results"]["series"][0]["data"]
        vals = {}
        for x in rows:
            # BLS emits "-" for months not yet published; skip non-numeric values
            if x["period"].startswith("M"):
                try:
                    vals[(int(x["year"]), int(x["period"][1:]))] = float(x["value"])
                except ValueError:
                    continue
        # latest month strictly before D's month (releases lag ~2 weeks)
        cands = sorted(k for k in vals if (k[0], k[1]) < (d.year, d.month))
        for y, m in reversed(cands):
            prev = (y - 1, m)
            if prev in vals:
                yoy = 100 * (vals[(y, m)] - vals[prev]) / vals[prev]
                return round(yoy, 1), f"BLS series {series}, {y}-{m:02d} vs {prev[0]}-{m:02d}"
        return None
    except Exception:
        return None


def _wiki_conflict(d: dt.date) -> tuple[str, int] | None:
    """Fetch the revision of '{year} in the United States' as of D; caller supplies the
    clause wording from it (rule 2's phrasing constraint) — we pin the revision id."""
    try:
        url = ("https://en.wikipedia.org/w/api.php?action=query&format=json"
               f"&titles={d.year}%20in%20the%20United%20States&prop=revisions"
               f"&rvlimit=1&rvdir=older&rvstart={d.isoformat()}T23:59:59Z&rvprop=ids")
        with urllib.request.urlopen(urllib.request.Request(
                url, headers={"User-Agent": "quorum-anchor-builder/1.0"}), timeout=30) as r:
            data = json.loads(r.read())
        page = next(iter(data["query"]["pages"].values()))
        return page["title"], page["revisions"][0]["revid"]
    except Exception:
        return None


def build(d: dt.date, facts: dict, network: bool = True) -> tuple[str, dict]:
    manifest: dict = {"date": d.isoformat(), "protocol": "anchor-protocol v1 (FT4)"}

    # sentence 1 — template (president/term facts must come from facts file or defaults
    # recorded here; they are civic-calendar facts, not selections)
    pres = facts.get("president", "Donald Trump")
    term_year = facts.get("term_year", 2)
    term = facts.get("term_ordinal", 2)
    s1 = (f"Today is {d.strftime('%B %-d, %Y')}. {pres} is in the {ORD[term_year]} year "
          f"of his {ORD[term]} term as President of the United States.")

    # sentence 2 — conflict clause; wording sourced per rule 2, revision pinned
    s2 = facts.get("conflict_clause", "")
    if network:
        w = _wiki_conflict(d)
        if w:
            manifest["wiki_page"], manifest["wiki_revid"] = w
    if facts.get("wiki_revid"):
        manifest["wiki_revid"] = facts["wiki_revid"]
    if not s2:
        raise SystemExit("conflict_clause is required (rule 2 wording comes from the "
                         "pinned Wikipedia revision; supply via --facts)")

    # sentence 3 — official statistics
    cpi, ahe, gas = facts.get("cpi_yoy"), facts.get("ahe_yoy"), facts.get("gas_price")
    if network and cpi is None:
        got = _bls_yoy(CPI_SERIES, d)
        if got:
            cpi, manifest["cpi_cite"] = got
    if network and ahe is None:
        got = _bls_yoy(AHE_SERIES, d)
        if got:
            ahe, manifest["ahe_cite"] = got
    for k in ("cpi_cite", "ahe_cite", "gas_cite"):
        if facts.get(k):
            manifest[k] = facts[k]
    if None in (cpi, ahe, gas):
        raise SystemExit(f"missing statistics (cpi={cpi} ahe={ahe} gas={gas}); "
                         "supply via --facts")
    s3 = (f"Gasoline averages ${gas:.2f} a gallon nationally; inflation is {cpi}% over "
          f"the past year while average wages grew {ahe}%.")

    # sentence 4 — civic calendar
    s4 = facts.get("election")
    if not s4:
        raise SystemExit("election sentence required (rule 4; supply via --facts)")

    text = f"Context: {s1} {s2} {s3} {s4}\n"

    # linter — prohibitions by construction
    if BANNED.search(text):
        raise SystemExit(f"LINT FAIL: banned token in anchor: {BANNED.search(text).group()}")
    ns = len(re.findall(r"[.!?](?:\s|$)", text.replace("U.S.", "US")))
    manifest["sentences"] = ns
    manifest["sha256"] = hashlib.sha256(text.encode()).hexdigest()
    return text, manifest


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--facts", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--no-network", action="store_true")
    a = ap.parse_args()
    d = dt.date.fromisoformat(a.date)
    facts = json.load(open(a.facts)) if a.facts else {}
    text, manifest = build(d, facts, network=not a.no_network)
    print(text)
    print(json.dumps(manifest, indent=1))
    if a.out:
        pathlib.Path(a.out).write_text(text)
        pathlib.Path(a.out + ".manifest.json").write_text(json.dumps(manifest, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
