"""FT4 arm C — the E35 abstain-shrink applied to a registered RAW run's rows.

Reads arm A's run directory (rows.jsonl + forecast.json), shrinks each profile-cell's
abstain mass by s (frozen 0.5618, fit on wave wD only — E35), redistributes the freed
mass within the cell proportional to the substantive options, and writes a forecast.json
of the same schema so the committed scorer grades it like any other arm. No Platt: E35's
pairing rule is raw-only (cal + dk degrades net).

Reproducibility: anyone holding the public rows.jsonl and the W161 frame regenerates the
arm byte for byte —

  PYTHONPATH=. python3 scripts/dk_shrink.py --raw-dir <armA dir> --out <armC dir>
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os

from quorum.twin.forecast import aggregate, load_frame
from quorum.twin.instruments import INSTRUMENTS

S_DK = 0.5618  # E35, frozen 2026-08-22


def dk_shrink(dist: dict[int, float], spec: dict, s: float = S_DK) -> dict[int, float]:
    """Shrink the abstain digits by s; freed mass goes to the substantive digits in
    proportion to their existing mass. Total mass is conserved. Cells with zero
    substantive mass are returned unchanged (nothing to redistribute onto)."""
    options = spec["options"]
    abstain = {i + 1 for i, o in enumerate(options) if o in spec["abstain"]}
    held = sum(p for d, p in dist.items() if d not in abstain)
    if held <= 0 or not abstain:
        return dict(dist)
    freed = sum(dist.get(d, 0.0) for d in abstain) * (1 - s)
    out = {}
    for d, p in dist.items():
        out[d] = p * s if d in abstain else p + freed * p / held
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--raw-dir", required=True, help="arm A run dir: rows.jsonl + forecast.json")
    ap.add_argument("--sav", default="data/pew/atp/w161/W161_Feb25/ATP W161.sav")
    ap.add_argument("--s", type=float, default=S_DK)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    raw = json.load(open(os.path.join(a.raw_dir, "forecast.json")))
    # FT1/FT2-era forecast.json predates the instrument/calibration blocks: raw approval.
    if raw.get("calibration", "raw") != "raw":
        raise SystemExit("dk_shrink pairs with a RAW run only (E35 pairing rule)")
    key = raw.get("instrument", {}).get("key", "yougov_approval")
    spec = INSTRUMENTS[key]
    raw.setdefault("instrument", {"key": key, "question": spec["question"],
                                  "options": spec["options"],
                                  "provenance": spec["provenance"]})
    n_opts = len(spec["options"])

    cells = load_frame(a.sav)
    rows = [json.loads(l) for l in open(os.path.join(a.raw_dir, "rows.jsonl"))]
    missing = [r["profile"] for r in rows if r["profile"] not in cells]
    if missing:
        raise SystemExit(f"{len(missing)} row profiles not in the frame — wrong --sav?")
    softs = {r["profile"]: dk_shrink({i: r[f"p{i}"] for i in range(1, n_opts + 1)}, spec, a.s)
             for r in rows}
    sub = {k: cells[k] for k in softs}

    res = aggregate(sub, softs, key)
    res["instrument"] = raw["instrument"]
    res["calibration"] = {"method": "dk_shrink", "s": a.s, "fit": "E35 — wave wD only",
                          "pairs_with": "raw", "source_rows_sha256":
                          hashlib.sha256(open(os.path.join(a.raw_dir, "rows.jsonl"), "rb")
                                         .read()).hexdigest()}
    for k in ("anchor_sha256", "anchor_text", "frame"):
        if k in raw:
            res[k] = raw[k]
    os.makedirs(a.out, exist_ok=True)
    path = os.path.join(a.out, "forecast.json")
    json.dump(res, open(path, "w"), indent=2)
    sha = hashlib.sha256(open(path, "rb").read()).hexdigest()
    t = res["topline"]
    print(f"raw  topline: {raw['topline']}")
    print(f"dk   topline: {t}")
    print(f"FORECAST WRITTEN {path} sha256={sha}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
