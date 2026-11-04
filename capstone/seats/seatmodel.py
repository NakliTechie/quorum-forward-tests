"""Core of the seats-by-margin model: fit, turnout weights, calibration, simulation.

Margins are in points, Democratic minus Republican, on the two-party vote.
lean = 2 * Cook PVI. inc = +1 Democratic incumbent running, -1 Republican, 0 open.
"""
import numpy as np
import pandas as pd

NO_BALLOT_LINE = {"FLORIDA", "OKLAHOMA", "LOUISIANA"}  # an unopposed candidate gets no recorded votes
KNOT = 30.0


def design(lean, inc, spec):
    lean = np.asarray(lean, float)
    inc = np.asarray(inc, float)
    if spec == "linear":
        return np.c_[lean, inc]
    if spec == "hinge":
        return np.c_[lean, np.maximum(lean - KNOT, 0), np.minimum(lean + KNOT, 0), inc]
    raise ValueError(spec)


def fit(panel, years, spec="linear"):
    """Estimate slope, incumbency, residual sizes and turnout terms from contested seats in `years`."""
    c = panel[panel.year.isin(years) & panel.contested].copy()
    yd = pd.get_dummies(c.year).values.astype(float)
    D = design(c.lean, c.inc, spec)
    X = np.c_[yd, D]
    beta, *_ = np.linalg.lstsq(X, c.margin.values, rcond=None)
    resid = c.margin.values - X @ beta
    k = yd.shape[1]
    dof = len(resid) - X.shape[1]
    s2 = resid @ resid / dof
    cov = s2 * np.linalg.inv(X.T @ X)
    c["res"] = resid

    # One-way variance split of the residual into a state-by-year part and a district part.
    grp = c.groupby(["year", "state"]).res
    n_g, m_g, v_g = grp.size(), grp.mean(), grp.var()
    multi = n_g >= 2
    within = np.average(v_g[multi], weights=n_g[multi] - 1)
    big_n = n_g.sum()
    n0 = (big_n - (n_g**2).sum() / big_n) / (len(n_g) - 1)
    msb = (n_g * (m_g - np.average(m_g, weights=n_g)) ** 2).sum() / (len(n_g) - 1)
    s_state2 = max((msb - within) / n0, 0.0)

    # Turnout: log two-party votes on lean, with a state-by-year mean removed.
    c["lv"] = np.log(c.tv)
    c["L2"] = c.lean**2 / 100.0
    dm = c[["lv", "lean", "L2"]] - c.groupby(["year", "state"])[["lv", "lean", "L2"]].transform("mean")
    g, *_ = np.linalg.lstsq(dm[["lean", "L2"]].values, dm.lv.values, rcond=None)

    # Votes cast in a seat with one major party, relative to what a contested seat with the
    # same lean in the same state would cast.
    c["fe"] = c.lv - g[0] * c.lean - g[1] * c.L2
    fe = c.groupby(["year", "state"]).fe.mean().rename("fe")
    u = panel[panel.year.isin(years) & ~panel.contested & ~panel.state.isin(NO_BALLOT_LINE)]
    u = u.join(fe, on=["year", "state"]).dropna(subset=["fe"])
    k_unc = float((u.tv / np.exp(u.fe + g[0] * u.lean + g[1] * u.lean**2 / 100)).median())

    return {
        "spec": spec, "years": list(years), "coef": beta[k:], "year_fx": dict(zip(sorted(c.year.unique()), beta[:k])),
        "se": np.sqrt(np.diag(cov))[k:], "sigma_total": float(np.sqrt(s2)), "sigma_state": float(np.sqrt(s_state2)),
        "sigma_district": float(np.sqrt(max(s2 - s_state2, 1e-9))), "g": g, "k_unc": k_unc, "n": len(c),
    }


def mean_part(df, par):
    """Model mean of the district margin before the national shift a."""
    return design(df.lean, df.inc, par["spec"]) @ par["coef"]


def turnout_weights(df, prior, par):
    """Expected two-party votes for each seat, from state levels in the prior same-type election.

    df needs state, lean, seat_type ('contested', 'D', 'R'). `prior` is the panel slice for
    the prior same-type election. Only relative sizes matter.
    """
    g1, g2 = par["g"]
    pc = prior[prior.contested]
    fe = (np.log(pc.tv) - g1 * pc.lean - g2 * pc.lean**2 / 100).groupby(pc.state).mean()
    base = df.state.map(fe).fillna(fe.mean()).values
    w = np.exp(base + g1 * df.lean.values + g2 * df.lean.values**2 / 100)
    fixed = df.seat_type.values != "contested"
    w = np.where(fixed, w * par["k_unc"], w)
    w = np.where(fixed & df.state.isin(NO_BALLOT_LINE).values, 0.0, w)
    return w


def calibrate(mu, vote_type, w, M):
    """Find the shift a so the vote-weighted district margins equal the national margin M.

    vote_type holds 'contested', 'D' or 'R' for how the seat enters the national vote.
    """
    con = vote_type == "contested"
    fixed = 100.0 * (w[vote_type == "D"].sum() - w[vote_type == "R"].sum())
    total = w.sum()

    def gap(a):
        return (w[con] * np.clip(a + mu[con], -100, 100)).sum() + fixed - M * total

    lo, hi = -80.0, 80.0
    for _ in range(70):
        mid = 0.5 * (lo + hi)
        if gap(mid) > 0:
            hi = mid
        else:
            lo = mid
    return 0.5 * (lo + hi)


class Draws:
    """Common random numbers, so that the curve is smooth across M."""

    def __init__(self, n_seats, state_codes, n_sims, seed):
        rng = np.random.default_rng(seed)
        n_states = int(state_codes.max()) + 1
        self.shared = rng.standard_normal(n_sims).astype(np.float32)
        self.state = rng.standard_normal((n_sims, n_states)).astype(np.float32)[:, state_codes]
        self.district = rng.standard_normal((n_sims, n_seats)).astype(np.float32)


def simulate(a, mu, seat_race, fixed_d, draws, s_shared, s_state, s_district):
    """Democratic seats per draw. seat_race marks seats whose winner is uncertain."""
    noise = s_shared * draws.shared[:, None] + s_state * draws.state[:, seat_race] + s_district * draws.district[:, seat_race]
    return ((a + mu[seat_race])[None, :] + noise > 0).sum(axis=1) + fixed_d


def seat_frame_from_panel(g):
    """Prepare one past year for the model, using only pre-election facts."""
    f = g.copy()
    f["seat_type"] = np.where(f.contested, "contested", np.where(f.dv >= f.rv, "D", "R"))
    f["vote_type"] = f.seat_type
    return f


def competitive_offset(f, a, mu, band=15.0):
    """Mean of actual minus modelled margin in contested seats modelled within `band` points."""
    pred = a + mu
    sel = (f.seat_type.values == "contested") & (np.abs(pred) <= band)
    return float(np.mean(f.margin.values[sel] - pred[sel])), int(sel.sum())
