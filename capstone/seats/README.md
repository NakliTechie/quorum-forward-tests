# Seats from the national margin

**This is a conversion, not a forecast.** It was run on 2026-11-04, between 09:28 and 09:57 IST, after the polls had closed.

A separate AI agent built [`seats_by_margin.csv`](seats_by_margin.csv): Democratic House seats at every national margin from
-2 to +16, on the maps in force for November 2026. Its inputs were past votes, Cook 2026 PVI and candidate lists. It used no
polls, race ratings or seat forecasts. We then read the table at our registered national margin of D +8.54.

| National two-party margin | Mean Democratic seats | 80% range |
|---|---|---|
| D +8.54 (our registered forecast) | 234.5 | 227 to 242 |
| D +8.9 | 236.0 | 229 to 244 |

- **Method:** [`method.md`](method.md), the agent's own report, unedited and addressed to whoever briefed it. It has the model, the backtest and the sensitivity cases.
- **Blinding:** [`exposure.md`](exposure.md), the agent's log of what it saw, unedited. Its start-up context showed D +8.54 and one early voter-poll comparison, which was our error in setting it up. It saw no 2026 seat count or national vote total.
- **By state:** [`seats_by_state_at_8.54.csv`](seats_by_state_at_8.54.csv), the same simulations grouped by state. These are not state forecasts.
- **To rerun:** `seatmodel.py`, `run_curve.py` and `seats_by_state.py` need only numpy and pandas, and run from `panel_2014_2024.csv` and `district_baseline.csv`. `fetch_data.sh` refetches the raw inputs. The default interpreter in `run_all.sh` was changed to `python3` for publication; nothing else was changed.

Sources: MIT Election Data and Science Lab, US House returns 1976-2024 (CC0); Wikipedia tables for Cook PVI, candidates and maps, read from archive.org snapshots dated before the election (CC BY-SA); FiveThirtyEight partisan lean (cross-check only).
