# GS1 — Gallup Satisfaction Registration (registered 2026-08-29)

*Series code GS1 (Chirag, 2026-08-27): the first non-YouGov, non-approval registration; scored and tracked beside the FT series.*

**Status: REGISTERED 2026-08-29 (draft frozen 2026-08-18). Final
document, forecast JSONs, and hashes are pushed to the public repository BEFORE the
target poll begins fielding (~September 1, 2026).** Everything operational is frozen
here; the only registration-day inputs are a fresh era anchor and the GPU micro-run.

## Why this instrument, on this evidence

Entry was decided by a rule declared before the diagnostic ran (AUC ≥ 0.75 and no party
sign error): the satisfaction family passed — AUC 0.795 on W161 gold (n = 2,543), party
ordering correct (gold Dem 9.2 / Ind 35.6 / Rep 71.7), and a held-out family fit cut
party MAE from 16.71 to 3.77 with topline error 0.5 points. The Economic Confidence
Index is **excluded entirely** — its economic-conditions component carries a party sign
error that no calibration can repair (confirmed unrepaired at 32B scale, probe of
2026-08-18); we do not register any quantity built on it.

## Target

Gallup's monthly "satisfaction with the way things are going in the United States"
tracker, **September 2026 poll** (fields approximately September 1–19; publishes late
September). Scored against Gallup's published national % satisfied and party breakdown.

## Method (frozen)

- Engine: the frozen FT-series method — Qwen3-14B + the FT adapter, soft first-token
  distribution; ATP W161 weighted frame (3,170 distinct profiles). Same commit
  discipline as FT1/FT2.
- Instrument wording from the registry (`quorum/twin/instruments.py`,
  `gallup_satisfaction`): "In general, are you satisfied or dissatisfied with the way
  things are going in the United States at this time?" — options Satisfied /
  Dissatisfied.
- Era anchor: fresh at registration, dated, facts verified against news sources that
  day, **no polling numbers**, sha-pinned.
- Two forecasts, mirroring the FT1/FT1-B pattern:
  - **Raw** (registered for topline).
  - **Calibrated companion** via `--platt 3.2448,2.0482` — the satisfaction-family
    Platt parameters fitted on the FULL W161 satisfaction gold (weighted MLE,
    `fit_platt`, n = 2,543). Registered for topline AND party cuts.

## Registered quantities and bars

| Quantity | Bar |
|---|---|
| Topline % Satisfied (raw) | error ≤ 5 points |
| Topline % Satisfied (calibrated) | error ≤ 5 points |
| Party cuts Dem/Ind/Rep (calibrated only) | MAE ≤ 12 points |
| Head-to-head | calibrated party MAE < raw party MAE |

Scored by the committed scorer pattern; published pass or fail, at the same volume
either way.

## Disclosures (part of the registration)

1. **Reconstructed wording.** Gallup's questionnaire PDF is not public; the item is
   assembled from Gallup's own trend-page description. Wording effects are a real,
   undismissable error source.
2. **One-wave family fit.** The calibration is fitted on a single wave (W161, February
   2025) of a different survey (Pew ATP, web panel) than the target (Gallup, phone).
   House effects and 19 months of drift are untested for this family; that is what this
   forward test measures.
3. **Form-split n.** The W161 satisfaction gold covers the form-split subset
   (n = 2,543 of 5,086).
4. **Two-option convention.** Our forecast distributes 100% across
   Satisfied/Dissatisfied; Gallup's published figures include a small no-opinion share
   (typically 2–3%). We compare our Satisfied% against Gallup's published Satisfied%
   as-is, and accept the convention mismatch inside the bar.
5. **Calibration provenance.** a = 3.2448, b = 2.0482, fitted 2026-08-18 on the full
   satisfaction gold — parameters chosen before the target fields, never touched after.

## Registration-day checklist (~Aug 30–31)

1. Fresh era anchor → sha.
2. GPU micro-run: raw + `--platt 3.2448,2.0482 --platt-family satisfaction_W161`
   (single L40S, ~20 min, ~$1–2).
3. Stamp forecast shas into this document; drop the DRAFT header; commit to the public
   repository; Chirag pushes.

## Registration stamps (2026-08-29)

- Anchor (mechanical builder, protocol v1): sha256 `d0a4a8b614090b908d25d52edc1ae202e58a48ea84d299fdfb28e2afcb579b95`
  — builder manifest sha256 `20d0c1e28c7b5076429a96b7639070511c956821a5ee45cc6b74e90908df1326`
  (BLS CPI CUUR0000SA0 3.4% / AHE CES0500000003 3.2% auto-fetched; AAA gas $4.09
  2026-08-28; wiki revid 1371854689; facts JSON in the public bundle).
- Raw forecast: Satisfied 35.7 / Dissatisfied 64.3 —
  sha256 `ac8199d74c6647bf0a83c601ce66c661e3cfe8019e32438741a64e4fe1ee9a66`
- Calibrated forecast: Satisfied 48.7 / Dissatisfied 51.3 —
  sha256 `8679b475603570690931c1f691b51ad84d12336ba4379a0a60e7b1f3c4a08fa7`
- Emission box: quorum-gallup (Seoul L40S:1 spot), job 1 of the 2026-08-29
  registration run; W161 frame (3,170 cells, weight share 1.0).

## Verdict

*(appended when Gallup publishes, late September)*
