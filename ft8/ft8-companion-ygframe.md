# FT8 measurement companion — the YouGov-weighted frame (published 2026-10-01, before fielding)

**Status: MEASUREMENT ONLY.** It is published before FT8's target (the Oct 2–5 wave) begins
fielding. It does not enter the core tally and changes nothing in `ft8-registration.md`. It
is scored and reported beside FT8 at the same volume, hit or miss.

## What it is

The same FT8 registered emission (`forecast-ft8-approval_raw.json`, rows sha256
`788583183c53cb77…`) under the same calibration map as arm B (3.6133, 1.3759). The answers
do not change; only the weights do. The frame is re-weighted to Economist/YouGov's own printed
weighting targets:
- baseline party ID **31% Democratic / 33% Republican**, 36% everything else;
- **registered voters only**, which matches the RV base YouGov has printed since Sep 4.

These targets appear verbatim in every toplines methodology block from Aug 14–17 to
Sep 25–28, 2026. They are the pollster's design, not poll results. YouGov's 2024 and 2020
vote targets are not matched: our Pew frame has no vote variable.

| Quantity | B (registered, W161 weights) | **YG frame (this companion)** |
|---|---|---|
| Approve | 34.4 | **36.2** |
| Disapprove | 55.6 | 54.0 |
| Net | −21.2 | −17.8 |
| Not sure | 10.0 | 9.8 |
| Party D / I / R | 11.2 / 29.0 / 65.4 | 11.2 / 29.2 / 65.5 |

File: `forecast-ft8-approval_ygframe.json` (sha256 in `SHA256SUMS`). Built with
`scripts/build_yg_frame.py --rv` and `scripts/cal_companion.py --frame-csv` (private repo).

## Why it is published

Over FT1–FT7, all 7 of B's topline misses were low (mean −2.36). A backtest on the registered
FT1–FT7 rows (retrodiction: answers known, method declared before computing) gives:

| FT1–FT7 | Mean approve miss | Mean net miss | Waves with net beyond ±8 |
|---|---|---|---|
| B | 2.34 | 3.06 | 0 |
| YG frame | **1.43** | **5.20** | **3** |
| Last week's poll | 1.86 | 3.86 | 1 |

Removing the low offset breaks the net. The engine puts about 10% on "not sure" against a
published 2%, and shifting weight toward Republicans lowers an already-low disapprove. **Net
is therefore expected to miss ±8 on many waves; this is stated before fielding.**

## How it will be scored, and what would promote it

- Reported every wave beside B and the poll-only benchmarks Z1–Z3: approve error (±5) and net
  error (±8) as measurements, plus party MAE.
- Promotion to a scored arm follows the standing rule in our private method ledger: beat
  last week's poll on the approval topline **four waves in a row**. It has done so on the last
  two (Sep 18–21, Sep 25–28, both in retrodiction). Anything else is decided at a dated review.
