"""Extract district tables (Cook PVI, incumbent, status) from archived past House pages.

Usage: python3 -I parse_history_pages.py <downloads_dir> <out.json> 2014 2016 ...
Output: list of rows {year, location, pvi, member, party, status, candidates}.
"""
import json
import re
import sys

from bs4 import BeautifulSoup


def clean(t):
    t = re.sub(r"\[\s*[a-z0-9 ]{1,8}\s*\]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def expand(table):
    """Expand rowspan and colspan into a dense grid of cell tags."""
    grid, spans = [], {}
    for tr in table.find_all("tr"):
        row, col = [], 0
        cells = tr.find_all(["td", "th"], recursive=False)
        ci = 0
        while ci < len(cells) or col in spans:
            if col in spans:
                cell, left = spans[col]
                row.append(cell)
                if left <= 1:
                    del spans[col]
                else:
                    spans[col] = (cell, left - 1)
                col += 1
                continue
            cell = cells[ci]
            ci += 1
            rs = int(re.sub(r"\D", "", cell.get("rowspan", "1")) or 1)
            cs = int(re.sub(r"\D", "", cell.get("colspan", "1")) or 1)
            for _ in range(cs):
                row.append(cell)
                if rs > 1:
                    spans[col] = (cell, rs - 1)
                col += 1
        grid.append(row)
    return grid


def parse(path, year):
    soup = BeautifulSoup(open(path, encoding="utf-8", errors="replace"), "html.parser")
    content = soup.find(id="mw-content-text")
    out = []
    for t in content.find_all("table", class_="wikitable"):
        head = clean(" ".join(x.get_text(" ") for x in t.find_all("tr")[:2]))
        if "PVI" not in head or "Candidates" not in head:
            continue
        grid = expand(t)
        if len(grid) < 3:
            continue
        hdr = [clean(c.get_text(" ")) for c in grid[1]]
        hdr0 = [clean(c.get_text(" ")) for c in grid[0]]
        idx = {}
        for i, (h, h0) in enumerate(zip(hdr, hdr0 + [""] * len(hdr))):
            for key, names in (
                ("loc", ("Location",)),
                ("pvi", ("PVI",)),
                ("member", ("Member", "Representative", "Incumbent")),
                ("party", ("Party",)),
                ("first", ("First elected",)),
                ("status", ("Status", "Results", "Result")),
            ):
                if key not in idx and any(n in h for n in names):
                    idx[key] = i
        if "loc" not in idx or "pvi" not in idx:
            continue
        cand_i = len(grid[1]) - 1
        for r in grid[2:]:
            if len(r) <= cand_i:
                continue
            rec = {k: clean(r[i].get_text(" ")) for k, i in idx.items() if i < len(r)}
            cc = r[cand_i]
            lis = [clean(li.get_text(" ")) for li in cc.find_all("li")]
            rec["candidates"] = lis or [clean(cc.get_text(" "))]
            rec["year"] = year
            out.append(rec)
    return out


rows = []
for y in sys.argv[3:]:
    y = int(y)
    r = parse(f"{sys.argv[1]}/wiki_house_{y}.html", y)
    print(y, "rows", len(r), "unique locations", len({x['loc'] for x in r}))
    rows += r
json.dump(rows, open(sys.argv[2], "w"), indent=0)
