"""SUBGROUP COMPRESSION — diagnosis and the one-parameter fix (CPU, frozen artifacts only).

Forward Test 1 exposed the engine's sharpest remaining weakness: its party-conditional
spread is far narrower than any real poll's. We forecast Dem 24 / Rep 46 (22 points apart)
where published waves run ~60-80 points apart. This module measures that on data where we
hold real gold — Pew ATP W161 (Feb 2025), which carries per-person approval answers, party
labels, and survey weights — and tests whether the cause is MECHANICAL (averaging
probabilities destroys spread) or SEMANTIC (the model does not condition on party).

The distinction decides the fix, so it must be measured, not assumed:
- mechanical  -> a single scalar recovers the spread, and it transfers across waves;
- semantic    -> no scalar helps, and the prompt/model must change.

The scalar under test is LOGIT SCALING (Platt slope, no intercept):
    p' = sigma(k * logit(p))
k = 1 is the untouched engine. k > 1 sharpens every person's probability away from 0.5,
which widens between-group spread without ever reordering individuals — it cannot invent
signal, only stop discarding it.

Honesty constraints wired in, not optional:
- k is fit on a FIT half of the panel and scored on the HELD half (persons split by a
  seeded shuffle), so the reported gain is out-of-sample.
- Fit and evaluation both use Pew's survey weights.
- Topline error is reported alongside subgroup error: a fix that widens subgroups by
  breaking the topline is not a fix.
"""

from __future__ import annotations

import json
import math


def _sigmoid(x: float) -> float:
    if x >= 0:
        return 1.0 / (1.0 + math.exp(-x))
    e = math.exp(x)
    return e / (1.0 + e)


def scale(p: float, k: float, eps: float = 1e-6) -> float:
    """Logit scaling: sharpen (k>1) or flatten (k<1) a probability about 0.5."""
    p = min(max(p, eps), 1.0 - eps)
    return _sigmoid(k * math.log(p / (1.0 - p)))


def read_rows(path: str) -> list[dict]:
    """Frozen arm rows. Unweighted runs (Nationscape) default to weight 1.0 so the same
    weighted estimators work across instruments."""
    out = []
    for line in open(path):
        r = json.loads(line)
        r.setdefault("weight", 1.0)
        out.append(r)
    return out


def wrate(rows: list[dict], key, k: float = 1.0) -> float:
    """Weighted predicted approve rate (percent) under logit scaling k."""
    tw = sum(r["weight"] for r in rows)
    return 100.0 * sum(r["weight"] * scale(r[key], k) for r in rows) / tw if tw else float("nan")


def wgold(rows: list[dict]) -> float:
    tw = sum(r["weight"] for r in rows)
    return 100.0 * sum(r["weight"] * bool(r["gold_approve"]) for r in rows) / tw if tw else float("nan")


def by_party(rows: list[dict]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for r in rows:
        p = str(r.get("party", "")).strip()
        if p in ("Democrat", "Republican", "Independent"):
            out.setdefault(p, []).append(r)
    return out


def subgroup_error(rows: list[dict], k: float) -> float:
    """Weighted mean absolute error (points) across party groups at scaling k."""
    groups = by_party(rows)
    errs = [abs(wrate(g, "soft", k) - wgold(g)) for g in groups.values()]
    return sum(errs) / len(errs) if errs else float("nan")


def fit_k(rows: list[dict], lo: float = 0.5, hi: float = 12.0, steps: int = 231) -> float:
    """k minimizing party-subgroup MAE on the given rows (grid search; convex enough)."""
    best, best_e = 1.0, float("inf")
    for i in range(steps):
        k = lo + (hi - lo) * i / (steps - 1)
        e = subgroup_error(rows, k)
        if e < best_e:
            best, best_e = k, e
    return best


def platt(p: float, a: float, b: float, eps: float = 1e-6) -> float:
    """Two-parameter calibration: p' = sigma(a*logit(p) + b). Monotone in p — it can only
    remap the model's probabilities, never reorder people, so it cannot manufacture signal
    the model did not already have."""
    p = min(max(p, eps), 1.0 - eps)
    return _sigmoid(a * math.log(p / (1.0 - p)) + b)


def fit_platt(rows: list[dict], iters: int = 200, eps: float = 1e-6) -> tuple[float, float]:
    """Weighted maximum-likelihood Platt scaling by Newton-Raphson on (a, b).

    Slope-only scaling (fit_k) failed on W161 because the engine's probabilities are both
    too narrow AND mis-centred; the intercept is what fixes the centring.

    Each Newton step is halved until the weighted log-loss does not rise (added 2026-09-29):
    Jev's probabilities pile up at 0 and 1, and plain Newton overshot to a = -25,085 (E50).
    Where plain Newton converged (the 14B and phi-4 maps), the full step is always taken and
    the result is unchanged.
    """
    xs = [math.log(min(max(r["soft"], eps), 1 - eps) / (1 - min(max(r["soft"], eps), 1 - eps)))
          for r in rows]
    ys = [1.0 if r["gold_approve"] else 0.0 for r in rows]
    ws = [r["weight"] for r in rows]

    def loss(a: float, b: float) -> float:
        tot = 0.0
        for x, y, w in zip(xs, ys, ws):
            z = a * x + b
            tot += w * (max(z, 0.0) + math.log1p(math.exp(-abs(z))) - y * z)
        return tot

    a, b = 1.0, 0.0
    cur = loss(a, b)
    for _ in range(iters):
        g_a = g_b = h_aa = h_ab = h_bb = 0.0
        for x, y, w in zip(xs, ys, ws):
            p = _sigmoid(a * x + b)
            d = w * (p - y)
            g_a += d * x
            g_b += d
            v = w * p * (1 - p)
            h_aa += v * x * x
            h_ab += v * x
            h_bb += v
        det = h_aa * h_bb - h_ab * h_ab
        if abs(det) < 1e-12:
            break
        da = (g_a * h_bb - g_b * h_ab) / det
        db = (g_b * h_aa - g_a * h_ab) / det
        if abs(da) < 1e-10 and abs(db) < 1e-10:
            a, b = a - da, b - db
            break
        step = 1.0
        while step > 1e-12 and loss(a - step * da, b - step * db) > cur:
            step /= 2
        a, b = a - step * da, b - step * db
        cur = loss(a, b)
    return a, b


def report_platt(rows: list[dict], label: str, a: float, b: float) -> dict:
    """Same report as `report`, with Platt calibration applied instead of slope scaling."""
    cal = [{**r, "soft": platt(r["soft"], a, b)} for r in rows]
    out = report(cal, label, 1.0)
    out["a"], out["b"] = round(a, 3), round(b, 3)
    return out


def calibrated_forecast(ft_rows: list[dict], a: float, b: float) -> dict:
    """Apply the calibration to a frozen forward-test run's per-profile option probabilities.

    The five options are Strongly/Somewhat approve, Somewhat/Strongly disapprove, Not sure.
    Calibration was fit on approve-vs-disapprove gold, so it is applied to the CONDITIONAL
    approve probability among those expressing an opinion; the "not sure" mass is carried
    through untouched. CPU-only: no re-generation, so the calibrated forecast is derived
    from exactly the same model outputs as the raw one.
    """
    import re

    def groups(profile: str) -> dict:
        def field(name):
            m = re.search(rf"- {name}: (.+)", profile)
            return m.group(1).strip() if m else None
        party = {"Democrat": "Dem", "Republican": "Rep", "Independent": "Ind"}.get(
            (field("Party affiliation") or "").split()[0] if field("Party affiliation") else "")
        gender = field("Gender")
        sex = {"Man": "Male", "Woman": "Female"}.get(gender)
        agec = field("Age")
        age = {"18-29": "18-29", "30-49": "30-44", "50-64": "45-64", "65+": "65+"}.get(agec)
        eth = (field("Ethnicity") or "").lower()
        if "non-hispanic" in eth or "non hispanic" in eth:
            race = "Black" if "black" in eth else ("White" if "white" in eth else "Other")
        elif "hispanic" in eth:
            race = "Hispanic"
        else:
            race = "Black" if "black" in eth else ("White" if "white" in eth else "Other")
        return {"party": party, "sex": sex, "age": age, "race": race}

    cells = []
    for r in ft_rows:
        p = [float(r[f"p{i}"]) for i in range(1, 6)]
        tot = sum(p) or 1.0
        p = [x / tot for x in p]
        opinion = p[0] + p[1] + p[2] + p[3]
        q_raw = (p[0] + p[1]) / opinion if opinion > 0 else 0.5
        q_cal = platt(q_raw, a, b)
        ns = p[4]
        cells.append({"w": float(r["w"]), "approve": (1 - ns) * q_cal,
                      "disapprove": (1 - ns) * (1 - q_cal), "ns": ns,
                      **groups(r["profile"])})

    def agg(sub):
        tw = sum(c["w"] for c in sub)
        if tw <= 0:
            return {}
        ap = 100 * sum(c["w"] * c["approve"] for c in sub) / tw
        di = 100 * sum(c["w"] * c["disapprove"] for c in sub) / tw
        ns = 100 * sum(c["w"] * c["ns"] for c in sub) / tw
        return {"Approve": round(ap, 1), "Disapprove": round(di, 1),
                "Net": round(ap - di, 1), "Not sure": round(ns, 1)}

    out = {"topline": agg(cells), "by": {}}
    for dim in ("party", "sex", "age", "race"):
        gs: dict[str, list] = {}
        for c in cells:
            if c[dim]:
                gs.setdefault(c[dim], []).append(c)
        out["by"][dim] = {g: agg(v) for g, v in sorted(gs.items())}
    out["calibration"] = {"a": round(a, 4), "b": round(b, 4),
                          "fit_on": "Pew ATP W161 (Feb 2025) + Nationscape (2019-20) "
                                    "approval gold, pooled; no 2026 data"}
    return out


def split_persons(rows: list[dict], seed: int = 42) -> tuple[list[dict], list[dict]]:
    """Deterministic half-split BY PERSON (qkey), so fit and held share no respondent."""
    import random

    keys = sorted({r["qkey"] for r in rows})
    rng = random.Random(seed)
    rng.shuffle(keys)
    fit_keys = set(keys[: len(keys) // 2])
    return ([r for r in rows if r["qkey"] in fit_keys],
            [r for r in rows if r["qkey"] not in fit_keys])


def report(rows: list[dict], label: str, k: float = 1.0) -> dict:
    groups = by_party(rows)
    order = ["Democrat", "Independent", "Republican"]
    pred = {g: wrate(groups[g], "soft", k) for g in order if g in groups}
    gold = {g: wgold(groups[g]) for g in order if g in groups}
    spread_p = pred.get("Republican", float("nan")) - pred.get("Democrat", float("nan"))
    spread_g = gold.get("Republican", float("nan")) - gold.get("Democrat", float("nan"))
    return {"label": label, "k": round(k, 3), "n": len(rows),
            "topline_pred": round(wrate(rows, "soft", k), 1),
            "topline_gold": round(wgold(rows), 1),
            "party_pred": {g: round(v, 1) for g, v in pred.items()},
            "party_gold": {g: round(v, 1) for g, v in gold.items()},
            "spread_pred": round(spread_p, 1), "spread_gold": round(spread_g, 1),
            "compression": round(spread_p / spread_g, 3) if spread_g else None,
            "party_mae": round(subgroup_error(rows, k), 2)}
