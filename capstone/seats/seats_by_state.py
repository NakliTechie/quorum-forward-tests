"""Read the frozen seat model state by state at one national margin. No parameter is changed or tuned.

Usage: python seats_by_state.py <panel.csv> <district_baseline.csv> <margin> <out.csv>
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import numpy as np
import pandas as pd

import backtest as bt
import run_curve as rc
import seatmodel as sm


def main():
    panel = pd.read_csv(sys.argv[1])
    b = pd.read_csv(sys.argv[2])
    M = float(sys.argv[3])
    f = rc.frame_2026(b)
    par = sm.fit(panel, rc.TRAIN, "linear")
    s_shared = float(np.sqrt(np.mean(np.square(bt.in_sample_shared(panel, par)))))
    w = rc.weights_for(f, panel[panel.year == 2022], par)
    codes = pd.factorize(f.state)[0]
    d = sm.Draws(len(f), codes, rc.SIMS, rc.SEED)   # same seed and draws as the curve
    mu = sm.mean_part(f, par)
    a = sm.calibrate(mu, f.vote_type.values, w, M)
    race = f.seat_type.values == "contested"
    noise = s_shared * d.shared[:, None] + par["sigma_state"] * d.state[:, race] + par["sigma_district"] * d.district[:, race]
    win = np.zeros((rc.SIMS, len(f)), dtype=bool)
    win[:, race] = ((a + mu[race])[None, :] + noise) > 0
    win[:, (f.seat_type == "D").values] = True
    rows = []
    for po, idx in f.groupby("po").indices.items():
        s = win[:, idx].sum(axis=1)
        p = win[:, idx].mean(axis=0)
        rows.append({"state": po, "seats": len(idx), "dem_mean": round(float(s.mean()), 1), "dem_p10": float(np.percentile(s, 10)),
                     "dem_p90": float(np.percentile(s, 90)), "toss_ups_25_75": int(((p > .25) & (p < .75)).sum())})
    t = pd.DataFrame(rows).sort_values("seats", ascending=False)
    t.to_csv(sys.argv[4], index=False)
    tot = win.sum(axis=1)
    print("M", M, "shift", round(a, 2), "total mean", round(float(tot.mean()), 1), "p10", np.percentile(tot, 10), "p90", np.percentile(tot, 90), "sum of states", round(t.dem_mean.sum(), 1), "seats", t.seats.sum())
    print(t.head(14).to_string(index=False))
    print("states with a seat in play:", int((t.toss_ups_25_75 > 0).sum()), "seats in play:", int(t.toss_ups_25_75.sum()))
    print(t.sort_values("toss_ups_25_75", ascending=False).head(8)[["state", "seats", "dem_mean", "toss_ups_25_75"]].to_string(index=False))


if __name__ == "__main__":
    main()
