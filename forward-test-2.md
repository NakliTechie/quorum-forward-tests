# Quorum Forward Test 2 — Registered Pre-Field Forecast (Economist/YouGov approval)

**Second in the series.** Forward Test 1 (registered 2026-08-13) targeted the wave that
fielded August 14–17, 2026 and is awaiting publication; its verdict will be appended to its
own document. This registration is prepared independently and BEFORE its own target fields.

## Target

The **first Economist/YouGov weekly poll to begin fielding after this document's public
timestamp** (expected to field on or about **August 21–24, 2026**, on the series' standing
Friday–Monday cadence), presidential job approval question, wording and options identical to
Forward Test 1 (verbatim from the Economist/YouGov toplines).

## Registered quantities, bars, and scoring

Identical to Forward Test 1/1-B, restated: topline Approve error ≤ 5, Net error ≤ 8;
sex/age/race 9-cell MAE ≤ 6. Party cuts: **registered for the calibrated forecast only**
(bar: party MAE ≤ 12, and the head-to-head claim that calibrated beats raw). Scored by the
same committed scorer; published pass or fail.

## Registered forecasts

Same frozen method as FT1 (Qwen3-14B + adapter, soft first-token, ATP W161 weighted frame,
n = 3,170 profiles); a fresh era anchor dated 2026-08-17 (facts verified against news
sources that day; **no polling numbers**); calibration parameters identical to FT1-B
(fitted on 2019 + 2025 approval gold only).

| Quantity | FT2 (raw) | FT2-B (calibrated) |
|---|---|---|
| Approve | 33.3 | **34.1** |
| Disapprove | 56.3 | **55.5** |
| Net | −23.0 | **−21.4** |
| Not sure | 10.4 | 10.4 |

| Cut | FT2 (raw) | FT2-B (calibrated) |
|---|---|---|
| Party: Dem / Ind / Rep | 24.8 / 31.7 / 43.9 | **10.8 / 28.3 / 65.1** |
| Sex: Male / Female | 35.5 / 31.3 | — (raw registered for 9-cell) |
| Age: 18-29 / 30-44 / 45-64 / 65+ | 32.2 / 33.0 / 33.9 / 33.9 | — |
| Race: White / Black / Hispanic | 35.0 / 27.9 / 31.7 | — |

## Corrections and disclosures

- **FT1's era anchor contained a factual error**, discovered while preparing this test: it
  stated the Iran war began "June 2026"; the war began **February 2026** (a preliminary
  peace agreement was reached in June, with intermittent fighting since). FT1 stands as
  registered — its anchor is part of its frozen record — and this test's anchor states the
  corrected timeline. Model-era effects of the error are expected to be minor (the anchor's
  function is era identification, which was correct); FT1's verdict will show.
- The anchor also reflects the week's verified facts: July CPI 3.4% with wage growth 3.2%,
  gasoline above $4.
- Anchor file sha256: `da7840408b0c5e55a8b10ea3350f0f5dbb5408336aadb13208cbaa61d2def596`
  (stripped-content sha, as recorded inside the forecast JSON:
  `b1204029a4fd20a3…` — same text, two conventions, both stated to avoid ambiguity).
- Forecast JSON sha256 (raw): `6267783227a2529939dee2126103a42e77ddc542554b81c0d4d2c9722c207bb8`
- Forecast JSON sha256 (calibrated): `e5e6a84598596336e2b9119f9bfa03070f2ca1400dbab8a7d6e7331e21f94b90`

## Verdict

*(appended when the target wave publishes)*

## Verdict (scored 2026-08-27, target published 2026-08-26)

**PASS + PASS — every registered bar, both engines** (target: Aug 21-24 wave, published
36 approve / 57 disapprove / net −21; tab report table 17; scored by the committed
scorer `scripts/score_ft.py` in the main repo, identity-gated against FT1's record;
full score JSON: `score-ft2-2026-08-27.json`).

| Quantity (bar) | FT2 raw | FT2-B calibrated |
|---|---|---|
| Topline approve error (≤5) | −2.7 | **−1.9** |
| Net error (≤8) | −2.0 | **−0.4** |
| 9-cell sex/age/race MAE (≤6) | 5.2 | **2.78** |
| Party MAE (≤12, calibrated only) | 21.9 (exploratory, unregistered) | **9.0** |
| Head-to-head (calibrated party < raw) | — | **UPHELD** |

Published beside the verdict, per standing rule: the persistence benchmark (previous
wave 35/61 re-used) scores topline error 1.0 and net error 5.0 — better than our
calibrated topline again, worse than our net. And one advance prediction FAILED: the
FT3 protocol's disclosure 5 (from the eight-wave backtest) predicted the calibrated arm
would underperform raw on the topline; this wave it outperformed (−1.9 vs −2.7). The
falsifiable prediction was wrong here and is reported as such. The calibrated Rep cell
carries the wave's largest party miss (−14.9: predicted 65.1 vs published 80).
