"""Produce seats_by_margin.csv, curve_detail.csv, sensitivity.csv and parameters.json.

Usage: python -I run_curve.py <panel.csv> <district_baseline.csv> <out_dir>
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import backtest as bt
import seatmodel as sm

SIMS, SEED = 40000, 20261102
TRAIN = [2018, 2020, 2022, 2024]
GRID = np.round(np.arange(-2.0, 16.01, 0.5), 1)
PROBE = [0.0, 4.0, 8.0, 12.0]


def frame_2026(b):
    f = pd.DataFrame({
        "state": b.state.str.upper(), "po": b.state_po, "dist": b.district, "lean": b.baseline_margin.astype(float),
        "inc": b.incumbent_running.map({"D": 1, "R": -1, "I": -1, "open": 0}).astype(float), "new_map": b.map_new_for_2026,
    })
    f["seat_type"] = b.uncontested.map({"no": "contested", "no_republican": "D", "no_democrat": "R"})
    f["vote_type"] = f.seat_type
    # CA-6: Democrat against an independent incumbent (formerly Republican). No Republican votes
    # exist there, so it enters the national vote like an uncontested seat, but the seat is a real race.
    kiley = (b.incumbent_running == "I").values
    f.loc[kiley, "seat_type"] = "contested"
    return f


def weights_for(f, prior, par):
    g = f.copy()
    g["seat_type"] = g.vote_type
    return sm.turnout_weights(g, prior, par)


def curve(f, w, par, s_shared, draws, grid, a_add=0.0, seat_shift=None, s_state=None):
    mu = sm.mean_part(f, par)
    race = f.seat_type.values == "contested"
    fixed_d = int((f.seat_type == "D").sum())
    extra = np.zeros(len(f)) if seat_shift is None else seat_shift
    st = par["sigma_state"] if s_state is None else s_state
    rows, seats_by_m = [], {}
    for M in grid:
        a = sm.calibrate(mu, f.vote_type.values, w, M)
        s = sm.simulate(a + a_add, mu + extra, race, fixed_d, draws, s_shared, st, par["sigma_district"])
        seats_by_m[float(M)] = s
        margins = np.where(f.seat_type == "D", 100.0, np.where(f.seat_type == "R", -100.0, a + a_add + mu + extra))
        rows.append({
            "M": float(M), "mean": round(float(s.mean()), 1), "median": float(np.median(s)), "p10": float(np.percentile(s, 10)), "p90": float(np.percentile(s, 90)),
            "p_majority": round(float((s >= 218).mean()), 3), "shift_a": round(a, 2), "median_district_margin": round(float(np.median(margins)), 2),
        })
    return pd.DataFrame(rows)


def breakeven(t):
    """Interpolate the M where the probability of a Democratic majority crosses one half."""
    return float(np.interp(0.5, t.p_majority.values, t.M.values))


def main():
    panel = pd.read_csv(sys.argv[1])
    b = pd.read_csv(sys.argv[2])
    out = sys.argv[3]
    f = frame_2026(b)
    par = sm.fit(panel, TRAIN, "linear")
    offs = bt.in_sample_shared(panel, par)
    s_shared = float(np.sqrt(np.mean(np.square(offs))))
    prior = panel[panel.year == 2022]
    w = weights_for(f, prior, par)
    codes = pd.factorize(f.state)[0]
    draws = sm.Draws(len(f), codes, SIMS, SEED)

    t = curve(f, w, par, s_shared, draws, GRID)
    t[["M", "mean", "median", "p10", "p90", "p_majority"]].to_csv(os.path.join(out, "seats_by_margin.csv"), index=False)
    t.to_csv(os.path.join(out, "curve_detail.csv"), index=False)

    json.dump({
        "train_years": TRAIN, "slope_on_lean": float(par["coef"][0]), "slope_se": float(par["se"][0]), "incumbency_margin_points": float(par["coef"][-1]), "incumbency_se": float(par["se"][-1]),
        "sigma_total": par["sigma_total"], "sigma_district": par["sigma_district"], "sigma_state": par["sigma_state"], "sigma_shared": s_shared,
        "training_year_offsets": offs, "turnout_lean_terms": [float(x) for x in par["g"]], "uncontested_vote_ratio": par["k_unc"], "n_contested_seat_years": par["n"],
        "year_effects": {str(k): float(v) for k, v in par["year_fx"].items()}, "breakeven_M": breakeven(t),
        "fixed_d_seats": int((f.seat_type == "D").sum()), "fixed_r_seats": int((f.seat_type == "R").sum()),
        "share_of_votes_fixed_d": float(w[f.vote_type == "D"].sum() / w.sum()), "share_of_votes_fixed_r": float(w[f.vote_type == "R"].sum() / w.sum()),
    }, open(os.path.join(out, "parameters.json"), "w"), indent=1)

    # Sensitivity: each row changes one assumption and leaves the rest at the base case.
    grid = np.round(np.arange(-2.0, 10.01, 0.5), 1)
    cases = {"base": t[t.M <= 10].reset_index(drop=True)}
    for name, yrs, spec in (("fit on 2020-2024", [2020, 2022, 2024], "linear"), ("fit on 2014-2024", bt.ELECTIONS, "linear"), ("bent line in lean, knots at +/-30", TRAIN, "hinge")):
        p = sm.fit(panel, yrs, spec)
        cases[name] = curve(f, weights_for(f, prior, p), p, s_shared, draws, grid)
    # Incumbents on redrawn turf: the measured discount, then a stress case at half the effect.
    c = panel[panel.year.isin(TRAIN) & panel.contested]
    X = np.c_[pd.get_dummies(c.year).values.astype(float), c.lean, c.inc, c.inc * c.redrawn]
    disc = float(np.linalg.lstsq(X, c.margin.values, rcond=None)[0][-1])
    g = f.copy()
    g["inc"] = g.inc * np.where(g.new_map == 1, 0.5, 1.0)
    cases["incumbents on the 9 new maps get half the usual effect"] = curve(g, w, par, s_shared, draws, grid)
    cases[f"competitive seats beat calibration by the 2018-24 mean ({np.mean(offs):+.2f})"] = curve(f, w, par, s_shared, draws, grid, a_add=float(np.mean(offs)))
    cases["state turnout levels from 2018, not 2022"] = curve(f, weights_for(f, panel[panel.year == 2018], par), par, s_shared, draws, grid)
    cases["state turnout levels from 2024, not 2022"] = curve(f, weights_for(f, panel[panel.year == 2024], par), par, s_shared, draws, grid)
    p18 = dict(par)
    p18["g"] = sm.fit(panel, [2018], "linear")["g"]
    cases["turnout gap between blue and red seats as flat as in 2018"] = curve(f, weights_for(f, prior, p18), p18, s_shared, draws, grid)
    new = (f.new_map == 1).values
    cases["seats on the 9 new maps run 2 points more Democratic than baseline"] = curve(f, w, par, s_shared, draws, grid, seat_shift=np.where(new, 2.0, 0.0))
    cases["seats on the 9 new maps run 2 points more Republican than baseline"] = curve(f, w, par, s_shared, draws, grid, seat_shift=np.where(new, -2.0, 0.0))
    cases["no state-level error"] = curve(f, w, par, s_shared, draws, grid, s_state=0.0)
    rows = []
    for name, c_ in cases.items():
        r = {"case": name}
        for M in PROBE[:3]:
            r[f"mean_at_M{M:+.0f}"] = float(c_.loc[c_.M == M, "mean"].iloc[0])
        r["breakeven_M"] = round(breakeven(c_), 2)
        rows.append(r)
    s = pd.DataFrame(rows)
    s.to_csv(os.path.join(out, "sensitivity.csv"), index=False)
    pd.set_option("display.width", 200, "display.max_colwidth", 80)
    print(s.to_string(index=False))
    print("redrawn incumbency term", round(disc, 2))
    print("seat flips per point near break-even:", round(float(np.interp(breakeven(t) + 1, t.M, t["mean"]) - np.interp(breakeven(t) - 1, t.M, t["mean"])) / 2, 2))


if __name__ == "__main__":
    main()
