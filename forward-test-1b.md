# Quorum Forward Test 1-B — Registered companion forecast (calibrated)

**Registered 2026-08-13, before the target poll begins fielding.** This is a *companion* to
Forward Test 1, not a replacement. **Forward Test 1 stands exactly as registered and will be
scored exactly as registered.** Its forecast file is unchanged and its hash is unchanged.

## Why a second forecast

Forward Test 1's protocol disclosed a known weakness: the engine's party-conditional spread
is compressed relative to any published poll (we forecast Dem 24.1 / Rep 46.3, where real
waves run 60–80 points apart). We moved the party cuts out of FT1's registered set for that
reason.

After registering FT1 we investigated the cause using only pre-existing gold-bearing data,
and found something more useful than expected — reported in full below. FT1-B registers the
correction as a **falsifiable prediction on the same poll**, so a single real-world event
adjudicates between the uncorrected and corrected engine.

## The finding behind it

On Pew ATP W161 (Feb 2025), where per-person approval gold exists:

- The engine's **ranking** of respondents is strong — pooled AUC **0.896**; within party it
  is still 0.68–0.73, so there is genuine individual signal.
- Its **probabilities** are severely miscalibrated: Democrats average 0.289 for a group that
  approves at 7.2%; Republicans average 0.559 for a group that approves at 92.1%. Predicted
  party spread 27.0 against a true 83.6 — a **compression ratio of 0.32**.
- Slope-only sharpening fails (it fixes Democrats, overshoots Independents, and drives the
  topline from 41.4 to 31.9 against a gold 48.1).
- **Two-parameter logit calibration** — `p' = σ(a·logit(p) + b)`, monotone, therefore unable
  to reorder anyone or invent signal — fixes it. Fit on one random half of the panel and
  scored on the other: party MAE **20.25 → 5.63** points, compression **0.33 → 0.80**,
  topline error **6.7 → 1.0** points.
- **It transports.** Fitted independently on Nationscape (2019–20, a different survey, a
  different era, different respondents) the parameters are near-identical (intercept 1.366
  vs 1.387). Cross-applied with no refit: Pew-fit parameters take Nationscape's party MAE
  from 17.17 to 5.35 and its compression from 0.34 to 0.91.

The distortion is therefore a stable property of the model, not an artefact of one wave.

## Registered forecast (calibrated)

Calibration applied: `a = 3.6133`, `b = 1.3759`, fit by weighted maximum likelihood on
**pooled Pew ATP W161 (Feb 2025) + Nationscape (2019–20) approval gold. No 2026 data of any
kind entered the fit.** The calibrated forecast is computed on CPU from the *same frozen
model outputs* as FT1 — nothing was re-generated, so the two forecasts differ only by the
calibration map.

| Quantity | FT1 (raw, registered) | **FT1-B (calibrated)** |
|---|---|---|
| Approve | 33.6 | **34.9** |
| Disapprove | 55.8 | **54.5** |
| Net | −22.2 | **−19.7** |
| Not sure | 10.6 | 10.6 |

| Cut | FT1 (raw) | **FT1-B (calibrated)** |
|---|---|---|
| Party: Dem / Ind / Rep | 24.1 / 31.4 / 46.3 | **9.8 / 27.3 / 70.4** |
| Sex: Male / Female | 36.0 / 31.4 | **41.2 / 29.1** |
| Age: 18-29 / 30-44 / 45-64 / 65+ | 32.3 / 33.3 / 34.4 / 34.3 | **31.3 / 34.0 / 37.3 / 36.9** |
| Race: White / Black / Hispanic | 35.6 / 27.2 / 31.8 | **40.6 / 17.1 / 29.6** |

## The registered claim

1. **Party cuts are registered this time** (they were explicitly not, in FT1). Bar: party
   mean absolute error ≤ **12 points**. Held-out and cross-instrument MAE was 5.4–6.5; the
   bar is set wider to allow for 18 months of drift between the calibration data and the
   target wave.
2. **Head-to-head:** FT1-B's party MAE will be **lower than FT1's**. This is the actual
   scientific claim, and it is the one a single published poll can refute.
3. Topline bars unchanged from FT1: Approve error ≤ 5 points, Net error ≤ 8 points.
4. Registered subgroup (sex/age/race, 9 cells) MAE ≤ 6 points, as in FT1.
5. **Published pass or fail, both forecasts, side by side.**

## Disclosure

The compression was noticed *because of* FT1's own output, so the calibration was developed
after FT1 was registered — but it is fitted exclusively on 2019 and 2025 gold, and the
target wave had not been fielded when this document was published. FT1 was not modified.
Both forecasts are timestamped publicly before fielding, and both will be scored.

Failure modes we would report as failures: party MAE above 12; FT1-B doing no better than
FT1 on party; topline breaking the FT1 bars it currently meets.

## Artefacts

- `forecast-ft1b.json` — this forecast, with its calibration parameters recorded inside.
- Method: `quorum/twin/compression.py` (private repo, at the registration commit).
- The calibration is monotone: it changes no individual's rank, only the mapping from the
  engine's probability to a population rate.

*Registered 2026-08-13. Verdict appended here when the target wave publishes.*
