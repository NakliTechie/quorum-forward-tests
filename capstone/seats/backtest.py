"""Backtest: parameters from earlier elections only, the actual national margin as input.

Usage: python -I backtest.py <panel.csv> <official_seats.json> [out.csv]
The seat_type of each past seat (contested or not, and which party holds an uncontested seat)
was fixed by the ballot before the election, so it is a pre-election fact.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import seatmodel as sm

SIMS, SEED = 20000, 20261102
ELECTIONS = [2014, 2016, 2018, 2020, 2022, 2024]


def in_sample_shared(panel, par):
    """Root mean square of the competitive-seat offset in the training years."""
    offs = []
    for y in par["years"]:
        f = sm.seat_frame_from_panel(panel[panel.year == y])
        mu = sm.mean_part(f, par)
        w = np.where(f.tv > 0, f.tv, 0.0).astype(float)
        M = 100 * (f.dv.sum() - f.rv.sum()) / f.tv.sum()
        a = sm.calibrate(mu, f.vote_type.values, w, M)
        offs.append(sm.competitive_offset(f, a, mu)[0])
    return offs


def run_year(panel, T, window, spec, s_shared=None):
    prior = [y for y in ELECTIONS if y < T][-window:]
    par = sm.fit(panel, prior, spec)
    offs = in_sample_shared(panel, par)
    shared = float(np.sqrt(np.mean(np.square(offs)))) if s_shared is None else s_shared
    f = sm.seat_frame_from_panel(panel[panel.year == T]).reset_index(drop=True)
    mu = sm.mean_part(f, par)
    w = sm.turnout_weights(f, panel[panel.year == T - 4], par)
    M = 100 * (f.dv.sum() - f.rv.sum()) / f.tv.sum()
    a = sm.calibrate(mu, f.vote_type.values, w, M)
    race = f.seat_type.values == "contested"
    fixed_d = int((f.seat_type == "D").sum())
    codes = pd.factorize(f.state)[0]
    dr = sm.Draws(len(f), codes, SIMS, SEED + T)
    seats = sm.simulate(a, mu, race, fixed_d, dr, shared, par["sigma_state"], par["sigma_district"])
    off, n_band = sm.competitive_offset(f, a, mu)
    # Fitted intercept for that year, for comparison with the calibrated shift.
    r = (f.margin.values - mu)[race]
    return {
        "year": T, "train": f"{prior[0]}-{prior[-1]}", "M": round(M, 2), "a_cal": round(a, 2), "a_fit": round(float(r.mean()), 2),
        "b": round(float(par["coef"][0]), 3), "c": round(float(par["coef"][-1]), 2),
        "sig_dist": round(par["sigma_district"], 2), "sig_state": round(par["sigma_state"], 2), "sig_shared": round(shared, 2),
        "mean": round(float(seats.mean()), 1), "median": float(np.median(seats)), "p10": float(np.percentile(seats, 10)),
        "p90": float(np.percentile(seats, 90)), "offset_competitive": round(off, 2), "n_band": n_band,
        "train_offsets": [round(x, 2) for x in offs],
    }


def main():
    panel = pd.read_csv(sys.argv[1])
    actual = {int(k): v for k, v in json.load(open(sys.argv[2])).items()}
    rows = []
    for spec in ("linear", "hinge"):
        for window in (4, 2):
            for T in (2018, 2020, 2022, 2024):
                r = run_year(panel, T, window, spec)
                r["spec"], r["window"], r["actual"] = spec, window, actual[T]
                r["err"] = round(r["mean"] - actual[T], 1)
                r["inside80"] = bool(r["p10"] <= actual[T] <= r["p90"])
                rows.append(r)
    t = pd.DataFrame(rows)
    show = ["spec", "window", "year", "train", "M", "a_cal", "a_fit", "b", "c", "sig_dist", "sig_state", "sig_shared", "mean", "p10", "p90", "actual", "err", "inside80", "offset_competitive", "n_band"]
    pd.set_option("display.width", 250)
    print(t[show].to_string(index=False))
    print(t.groupby(["spec", "window"]).agg(mae=("err", lambda s: s.abs().mean()), bias=("err", "mean"), inside=("inside80", "sum")).round(2))
    print(t[t.spec == "linear"][["year", "window", "train_offsets"]].to_string(index=False))
    if len(sys.argv) > 3:
        t.drop(columns=["train_offsets"]).to_csv(sys.argv[3], index=False)


if __name__ == "__main__":
    main()
