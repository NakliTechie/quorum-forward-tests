"""Independent checks on the deliverables. Usage: python -I verify_outputs.py <folder>
Exit code 0 only when every check passes."""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
import seatmodel as sm
import run_curve as rc

d = sys.argv[1]
t = pd.read_csv(f'{d}/seats_by_margin.csv'); b = pd.read_csv(f'{d}/district_baseline.csv'); p = pd.read_csv(f'{d}/panel_2014_2024.csv')
par_j = json.load(open(f'{d}/parameters.json'))
ok = []
def check(name, cond, info=''):
    ok.append(bool(cond)); print(('PASS' if cond else 'FAIL'), name, info)
check('columns', list(t.columns) == ['M', 'mean', 'median', 'p10', 'p90', 'p_majority'])
check('grid -2..16 by 0.5', np.allclose(t.M.values, np.arange(-2, 16.01, .5)), f'{len(t)} rows')
check('mean rises with M', (np.diff(t['mean']) > 0).all())
check('p10<=median<=p90', ((t.p10 <= t['median']) & (t['median'] <= t.p90)).all())
check('p_majority nondecreasing in [0,1]', (np.diff(t.p_majority) >= 0).all() and t.p_majority.between(0, 1).all())
check('435 baseline rows', len(b) == 435)
seats = p[p.year == 2024].groupby('state').size()
mine = b.groupby(b.state.str.upper()).size()
check('seats per state equal the 2024 apportionment', (seats.sort_index() == mine.sort_index()).all())
check('no missing baseline', b[['pvi', 'baseline_margin', 'incumbent_running', 'uncontested', 'source']].notna().all().all())
check('unique seats', not b.duplicated(['state', 'district']).any())
# Calibration reproduces M, recomputed from scratch.
par = sm.fit(p, rc.TRAIN, 'linear'); f = rc.frame_2026(b); w = rc.weights_for(f, p[p.year == 2022], par); mu = sm.mean_part(f, par)
err = 0
for M in t.M:
    a = sm.calibrate(mu, f.vote_type.values, w, M)
    m = np.where(f.vote_type == 'contested', np.clip(a + mu, -100, 100), np.where(f.vote_type == 'D', 100., -100.))
    err = max(err, abs((w * m).sum() / w.sum() - M))
check('vote-weighted district margins reproduce M', err < 1e-6, f'max abs error {err:.2e}')
# Simulated mean against a closed-form sum of win probabilities.
s_tot = math.sqrt(par_j['sigma_shared']**2 + par_j['sigma_state']**2 + par_j['sigma_district']**2)
race = (f.seat_type == 'contested').values
Phi = np.vectorize(lambda z: .5 * (1 + math.erf(z / 2**.5)))
gaps = []
for M in t.M:
    a = sm.calibrate(mu, f.vote_type.values, w, M)
    e = Phi((a + mu[race]) / s_tot).sum() + (f.seat_type == 'D').sum()
    gaps.append(float(t.loc[t.M == M, 'mean'].iloc[0]) - e)
check('simulated mean matches closed form', max(map(abs, gaps)) < 0.25, f'max gap {max(map(abs, gaps)):.3f} seats')
# Panel totals against the national votes printed on the archived pages (Democratic, Republican).
off = {2014: (35624357, 40081282), 2016: (61417454, 62772225), 2018: (60572245, 50861970), 2020: (77122690, 72466576), 2022: (51280463, 54227992), 2024: (70571330, 74390864)}
for y, (dv, rv) in off.items():
    g = p[p.year == y]; m_p = 100 * (g.dv.sum() - g.rv.sum()) / g.tv.sum(); m_o = 100 * (dv - rv) / (dv + rv)
    check(f'{y} margin close to official', abs(m_p - m_o) < 0.35, f'panel {m_p:.2f} official {m_o:.2f}')
print('median lean', b.baseline_margin.median(), 'mean lean', round(b.baseline_margin.mean(), 2), 'vote-weighted mean lean', round(float((w * f.lean).sum() / w.sum()), 2))
print('seats with lean in [-10,+10]:', int(b.baseline_margin.between(-10, 10).sum()), ' on new maps:', int(b[b.map_new_for_2026 == 1].shape[0]))
print('breakeven', round(par_j['breakeven_M'], 2), 'share fixed D', round(par_j['share_of_votes_fixed_d'], 4), 'fixed R', round(par_j['share_of_votes_fixed_r'], 4))
print(t[t.M.isin([-2, 0, 2, 3, 3.5, 4, 4.5, 5, 6, 8, 10, 12, 14, 16])].to_string(index=False))
sys.exit(0 if all(ok) else 1)
