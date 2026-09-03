# HH1-B — Harvard CAPS/Harris companion registration (2026-09-03)

**Status: REGISTRATION — the record of registration once pushed to this repository
(quorum-forward-tests, `hh1/`) with forecasts and hashes, BEFORE the target begins
fielding.** Target: **the same as HH1** — the first Harvard CAPS/Harris poll to begin
fielding after HH1's public push (`4881748`, 2026-08-29); their next wave is expected
late September 2026. HH1's registered arms are untouched and score as registered; HH1-B
adds companion arms built from the same frozen emission rows by CPU transforms alone.

## Why a companion

The August 2026 wave (fielded Aug 28–30, one day before HH1's push — an out-of-registration
shadow, recorded in `hh1-registration.md`) showed the HH1 arms unusable for structure:
raw approval −6.7 with party MAE 16.3; the house-adjusted companion had been built by
adding +7.2 to the topline only, leaving its party cuts identical to raw; direction
missed by −12.5 on a 29.3% DK. Each defect has a frozen repair elsewhere in the stack;
HH1-B registers them on the HH target.

## Registered arms and bars

| Arm | Built as | Bars |
|---|---|---|
| approval_cal | Platt on the conditional approve share, `approval_pooled_2019_2025` (a 3.6133, b 1.3759) — the FT-series calibrated method, unchanged | approve ±5 · net ±8 · **party MAE ≤ 12 (registered)** |
| approval_cal_house | approval_cal + one logit intercept shift solved so the topline = approval_cal + 7.2 (HH1's declared house offset, applied inside the distribution) | approve ±5 · net ±8 · party MAE ≤ 12 |
| direction_dk | E35-form abstain-shrink, *s* solved so aggregate DK = 11.0 (the August wave's DK) — in-sample for that one number, disclosed; no Platt | right track ±5 (measurement) |
| ballot_cal | Platt `HOUSE_BALLOT_NS` (a 2.7534, b 0.4401) on the two-row forced-choice share | Democrat share ±4 |

Head-to-head claims: (1) approval_cal party MAE < HH1 raw party MAE; (2) approval_cal_house
approve error < approval_cal approve error (the house offset earns its place or not);
(3) direction_dk right-track error < HH1 direction error.

## Disclosures
1. Surrogate validation: the approval map is fitted on Pew/Nationscape gold, the ballot map
   on Nationscape 2019; neither on HH microdata (none public).
2. The house offset (+7.2) is HH1's, from a five-wave HH-vs-E/YouGov gap computed
   2026-08-19; it conflates frame and house effects. Here it moves party cuts consistently
   (one intercept shift), unlike HH1's topline-only companion.
3. direction_dk's *s* is solved on the August wave's published DK — the only number in
   this registration touched by a post-registration observation; it targets the abstain
   share, not the right-track level, and is disclosed as in-sample for DK.
4. Pre-registration expectation from the August shadow (stamped below): what each arm
   would have scored on the wave that was not the target.
5. The frame remains the W161-recomposed hybrid of HH1 (disclosure 1 there).

## Registration (2026-09-03) — numbers, shadow expectation, hashes

Built by `scripts/build_hh1b.py` from HH1's frozen rows (row shas recorded inside each
forecast JSON); anchor unchanged from HH1 (`d0a4a8b6`, 2026-08-29). Public files
`hh1/forecast-hh1b-<arm>.json`, shas in `SHA256SUMS`.

| Quantity | approval_cal | approval_cal_house | direction_dk | ballot_cal |
|---|---|---|---|---|
| Positive (approve / right track / Democrat) | **42.0** | **49.2** | **30.8** | **52.4** |
| Negative | 51.4 | 44.3 | 58.3 | 47.6 |
| Net | −9.4 | +4.9 | −27.5 | +4.8 |
| DK | 6.5 | 6.5 | **10.9** (raw 29.3; *s* = 0.3735) | — |
| Party D / I / R (positive share) | **16.0 / 33.9 / 73.5** | 22.5 / 43.5 / 79.0 | 23.8 / 27.6 / 40.1 | 88.3 / 63.7 / 8.8 |

Transform constants: Platt approval a 3.6133 / b 1.3759; house intercept shift
δ = +0.4352 (solved: 42.0 → 49.2); direction *s* = 0.3735 (solved: DK 29.3 → 11.0);
ballot Platt a 2.7534 / b 0.4401. Identity checks: δ = 0 and *s* = 1 reproduce HH1's
registered raw toplines (37.3 approve; 29.3 DK).

**Pre-registration expectation — what each arm would have scored on the August wave
(44 / 52 / DK 4; party 13 / 36 / 80; right track 37; ballot D 51 RV), the shadow that was
not the target:**

| Arm | approve / positive err | net err | party MAE | would |
|---|---|---|---|---|
| approval_cal | −2.0 | −1.4 | **3.9** | pass all three |
| approval_cal_house | +5.2 | +12.9 | 6.0 | miss approve and net |
| direction_dk | −6.2 (vs HH1's −12.5) | — | — | miss by 1.2, halving HH1's miss |
| ballot_cal | +1.4 | — | — | pass |

**Registered in advance from the shadow: head-to-head 2 is expected to FAIL** — the
house offset was measured raw-vs-E/YouGov, and the calibration already removes most of
that gap; adding both double-counts it. We register the arm anyway: if the next wave
moves the way the offset predicts, that is informative, and the claim is on the record
either way. Head-to-heads 1 and 3 are expected to hold.

## Verdict
*(empty at registration)*
