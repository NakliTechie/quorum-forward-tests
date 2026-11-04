"""Extract the state-by-state district tables from an archived Wikipedia House page.

Reads only tables whose header has a PVI column and a Candidates heading. The
poll aggregate table and the infobox are never touched.
Usage: python3 -I parse_2026_page.py <file.html> <out.json>
"""
import json
import re
import sys

from bs4 import BeautifulSoup


def clean(t):
    t = re.sub(r"\[\s*[a-z0-9 ]{1,8}\s*\]", "", t)
    return re.sub(r"\s+", " ", t).strip()


def expand(table):
    """Expand a table with rowspan and colspan into a dense grid of cell tags."""
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


soup = BeautifulSoup(open(sys.argv[1], encoding="utf-8", errors="replace"), "html.parser")
content = soup.find(id="mw-content-text")
out = []
for t in content.find_all("table", class_="wikitable"):
    head = clean(" ".join(x.get_text(" ") for x in t.find_all("tr")[:2]))
    if "PVI" not in head or "Candidates" not in head:
        continue
    grid = expand(t)
    hdr = [clean(c.get_text(" ")) for c in grid[1]]
    idx = {}
    for i, h in enumerate(hdr):
        for key in ("Location", "PVI", "Member", "Party", "First elected", "Status"):
            if key in h and key not in idx:
                idx[key] = i
    cand_i = len(grid[1]) - 1
    for r in grid[2:]:
        if len(r) <= cand_i:
            continue
        cand_cell = r[cand_i]
        cands = [clean(li.get_text(" ")) for li in cand_cell.find_all("li")]
        if not cands:
            cands = [clean(cand_cell.get_text(" "))]
        rec = {k: clean(r[i].get_text(" ")) for k, i in idx.items() if i < len(r)}
        rec["candidates"] = cands
        rec["status_full"] = rec.get("Status", "")
        out.append(rec)
json.dump(out, open(sys.argv[2], "w"), indent=0)
print("rows", len(out))
