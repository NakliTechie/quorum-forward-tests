# Forward Test 3 — protocol, declared 2026-08-19 (forecast numbers added at registration)

**Bars and claims are fixed here, before the forecast exists.** The run happens on
2026-08-25; only the numbers and hashes are added then. Target: the first
*Economist*/YouGov weekly poll to begin fielding after this document is pushed publicly.

## Why this registration differs from FT1 and FT2

Two diagnostics run since FT1 changed what is worth registering:

- **E22 (2026-08-19)**: the engine's absolute level is a fixed prior. Twelve date-only
  anchors spanning 2017-2026, against a real 15-point range, produced 29.7-33.2 —
  slope +0.004. It does not track the era, and FT1's topline pass was substantially a
  coincidence. This is already disclosed publicly.
- **E23 (2026-08-19)**: the engine's *structure* is worth 2-5x beyond simply knowing the
  level, on families whose structure is sound — measured against a no-structure baseline
  on held-out respondents.

So registering another level claim tests almost nothing. FT3 keeps the frozen pair for
series continuity and adds two bars that test what the evidence says is actually there,
plus one we expect to fail.

## Registered quantities and bars

### A. Frozen pair — continuity (unchanged from FT1/FT2)
Raw and calibrated forecasts, same frozen method, same bars: topline Approve error ≤ 5;
Net error ≤ 8; sex/age/race 9-cell MAE ≤ 6; party MAE ≤ 12 for the calibrated engine
only, plus the head-to-head claim that calibrated beats raw on party.

### B. Structure bar — NEW, kept as a measurement (backtest leans AGAINST us; see disclosure 6)
**Conditional on the published topline**, our subgroup *deviations from that topline*
beat the naive alternative of repeating the previous published wave's cells.

- Scored as: for each of the nine sex/age/race cells, compare |our deviation − published
  deviation| against |previous wave's deviation − published deviation|.
- **Registered claim: our mean absolute deviation error is lower than persistence's.**
- Rationale: this isolates what the engine contributes once the level is supplied
  externally, which after E22 is the only level-independent claim we are entitled to make.
- Declared in advance: this bar can be *lost* even when the topline bar is passed, and
  vice versa.
- **Measured expectation (backtest run 2026-08-22, before this document went public;
  disclosure 6): a near-coin-flip with a lean AGAINST us.** Across the four published
  transitions Jul 20 -> Aug 17, mean 9-cell deviation error: calibrated engine 2.78,
  persistence-of-deviations 2.61; we won one transition of four (raw: 4.43, zero of
  four). On the party axis the same test is not close (11.40 vs 2.50): party deviations
  on a weekly tracker are nearly frozen, so persistence-of-structure is close to
  unbeatable there — the E28 persistence law extends to structure on polled questions.
  We keep the bar as a falsifiable measurement of exactly that limit, not as a claim
  the evidence supports; the engine's structure claim lives on unpolled questions and
  interaction cells (E27, E30), where no previous wave exists.

### C. Movement bar — NEW, and we expect to fail it
The frozen engine's predicted **change** from the previous published wave's topline,
against the actual change.

- **Registered prediction: we expect to FAIL this bar.** E22 measured a slope of +0.004,
  so the engine cannot move; its predicted change will be near zero regardless of what
  the poll does. E24 (2026-08-19, run before this document was pushed) removed the
  adapter and re-ran the identical sweep: the bare base is also flat (slope -0.037
  against the same 15-point real range), so this limitation is general to the method
  class at this scale, not an artifact of our fine-tune.
- Bar as declared for scoring purposes: |predicted change − actual change| ≤ 3.
- Rationale for registering a bar we expect to lose: a method's known limits should be
  put on the public record as a falsifiable prediction, not only in prose. If we somehow
  pass it, that is informative too.

## Disclosures carried at registration
1. The level-prior finding (E22) and its consequence for any topline claim.
2. The persistence benchmark, published beside the verdict as since FT1.
3. The "Not sure" over-hedge (~10.5 predicted vs ~3 published), a tracked defect that
   the E19 abstention repair failed to fix without trading another bar.
6. The structure-bar backtest above (four transitions, party axis and 9-cell axis),
   run and recorded before this registration went public.
4. The anchor is hand-built for FT3; from FT4 it is produced by the mechanical protocol
   in `docs/anchor-protocol-draft.md`.
5. **Advance prediction from the E28 backtest (2026-08-20, five scored waves): the
   calibrated arm will underperform the raw arm on the TOPLINE** — mean |approve error|
   3.94 vs 2.66 across the series; FT1-B's -0.1 was its best-case wave. The calibrated
   arm's registered value is party structure (its party MAE halves raw's on every scored
   wave: 10.4-12.1 vs 21.4-24.4). Registering the expected weakness in advance is the
   same falsifiable-prediction pattern as the movement bar: if calibrated BEATS raw on
   topline here, that contradicts our own backtest and is informative.

## Not registered, and why
- **A news-digest variant.** Backtest round 3 (five waves) measured news as valence
  steering with no accuracy gain (3.00 vs 3.04 mean topline error, net worse). There is
  nothing left to learn from registering it.
- **An anchored two-stage forecast.** Tested 2026-08-19 on the scored wave: on a
  weekly-polled question its topline reduces to persistence and its subgroups are level
  with the calibrated engine. It belongs in an unpolled-question demonstration, not here.

---

## Registration (2026-08-24) — numbers and hashes, added per this protocol

Run: `quorum-monday` box, job SUCCEEDED (47m), git commit `c3fc167` on the box.
Anchor: `data/forward/ft3/anchor-ft3.txt` — file sha256 `89c47035d4fe295bbb65b9b7292bb0a982fe2725d2d788a455f62d6d56f55c9b`;
forecast-internal text sha256 `6a7969ab65d4cbd95a08883a9cf664fc93af0d9f90c3c6457a21c20b42d430dc`.
Facts verified same morning (MOU deadline expired Aug 17 without a final deal; blockade
continuing; gasoline $4.10 national average, AAA Aug 20; CPI 3.4% July; wage growth 3.2%).
No polling numbers in the anchor.

| Quantity | RAW (sha `8b0af7a596ea55bd…`) | CALIBRATED (sha `36a0577c59bd8b9f…`) |
|---|---|---|
| Topline Approve | **32.6** | **32.6** |
| Disapprove | 56.5 | 56.6 |
| Net | −23.9 | −24.0 |
| Not sure | 10.9 | 10.9 |
| Party Approve D / I / R | 24.3 / 31.1 / 43.1 | 10.2 / 26.6 / 63.4 |
| Sex F / M | 30.7 / 34.7 | 27.2 / 38.5 |
| Age 18-29 / 30-44 / 45-64 / 65+ | 31.6 / 32.4 / 33.2 / 33.2 | 29.8 / 31.8 / 34.7 / 34.1 |
| Race Black / Hispanic / White (Other recorded, unscored) | 27.3 / 31.1 / 34.4 (31.1) | 17.6 / 28.0 / 37.5 (28.3) |

Movement-bar reference (bar C): previous published wave (fielded Aug 14–17) topline 35 —
**registered predicted change: raw −2.4, calibrated −2.4** (the bar we expect to fail is
scored on |predicted − actual change| ≤ 3; a near-zero predicted change was the declared
expectation, and −2.4 is the anchor-fact channel moving it slightly).

Calibration: Platt a=3.6133, b=1.3759, family `approval_pooled_2019_2025`, untouched
since declaration. Frame: ATP W161, 3,170 weighted profiles. The registered "Not sure"
over-hedge is visible at 10.9 (disclosure 3). The party-spread signature is live:
raw 18.8-point D–R spread, calibrated 53.2 — the §5 compression and its correction,
on the record before the target fields.

Target: the first Economist/YouGov weekly approval poll to begin fielding after this
document's public push. Scoring: the committed FT scorer, bars as declared above,
published pass or fail at equal volume.

## Registration-mechanism correction (2026-08-26, appended before any target fielding)

This document and its forecasts were committed to the program's PRIVATE working
repository on 2026-08-24 (commit `506b5ac`, its timestamp verifiable there on request).
The series' declared mechanism of record is THIS public repository (decision recorded in
forward-test-1.md, 2026-08-13); the 08-24 push failed to include it — an execution
error, disclosed here rather than papered over. **The public timestamp of record for
FT3 is this repository's commit adding this file.** The target definition is unchanged
and unharmed by the correction: the first Economist/YouGov weekly approval poll to
begin fielding AFTER this public push (expected field open ~2026-08-28). No wave began
fielding between 08-24 and this correction; the forecasts, anchor, and hashes are
byte-identical to the 08-24 private commit.
