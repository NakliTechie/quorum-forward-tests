# Forward Test 4 — protocol (declared 2026-09-02 morning; forecasts stamped 2026-09-02 afternoon)

**Status: REGISTRATION — becomes the record of registration when pushed to the public
repository (quorum-forward-tests), BEFORE the target begins fielding.** Bars and claims
were fixed in the morning draft (main-repo commit `9e64f50`, before any forecast existed);
the numbers and hashes below were added after the emission run, with no bar changed.

Target: **the first *Economist*/YouGov weekly poll to begin fielding after this document's
public push** (order-based, as FT1–FT3). FT3's target (fielded ~Aug 28–31) scores first;
FT4 registers after that verdict is public, so the two never share a wave.

## Why this registration differs from FT3

Five results since FT3 was declared change what is worth registering:

- **E48 (2026-08-30, 22-wave walk-forward backtest, retrodiction grade)**: the calibrated
  engine beats last-wave persistence on topline over a season (mean |approve error| 1.59
  vs 1.77) — by *shrinkage* (its band 34.4–36.6 against a published 33–40), with a
  wave-level split of only 12–10. Movement slope +0.106: the mechanical anchor moves the
  forecast ~1 point per 10 of real movement. Level claims are therefore allowed, in
  shrinkage-grade wording; movement claims stay capped near a tenth of the real change.
- **E47 (2026-08-29)**: the anchor is a switch, not a dial — no anchor 28.6, date-only
  28.5, protocol anchor 34.1, protocol + 8 more sentences 34.3. The five-sentence
  mechanical anchor is sufficient; a no-anchor arm is a known ~6-point miss.
- **E35 (2026-08-22)**: the "Not sure" over-hedge (disclosure 3 on every registration)
  is repairable by a population abstain-shrink *s* = 0.5618, fit on one wave and held out
  on eight: NS error 6.55 → 1.88, approve error 3.44 → 2.00, net within 0.3. Pre-declared
  to ship into FT4+ as a raw-paired variant arm. It does NOT pair with calibration
  (cal + dk degrades net to 6.22).
- **E16 (2026-08-24; calibrations frozen 08-26)**: direction of country and the House
  generic ballot pass the family entry gate on Nationscape gold (uAUC 0.765 / 0.950,
  party ordering correct) with per-family Platt maps frozen before any target was chosen.
  Both are asked weekly in the same E/YouGov poll (Q1 and Q9 in the Aug 21–24 toplines).
- **Anchor protocol v1** is already in public use (GS1 + HH1, 2026-08-29, mechanical
  builder, manifest + facts file). FT4 is the first *E/YouGov* registration under it,
  which is what §6 of the paper committed to "from the fourth registration onward".

## Registered arms

| Arm | Instrument | Method | Status |
|---|---|---|---|
| A | approval | raw, frozen FT method | continuity (FT1–3) |
| B | approval | calibrated: Platt a = 3.6133, b = 1.3759 (`approval_pooled_2019_2025`) | continuity (FT1–3) |
| C | approval | **raw + dk**: arm A's per-profile rows with abstain mass shrunk by *s* = 0.5618, freed mass redistributed within-cell proportional to the four substantive options; no Platt | NEW — E35 variant |
| D | approval | **no-anchor ablation**: raw method, anchor file empty | NEW — expected FAIL |
| E | direction (right/wrong track) | raw + calibrated (Platt a = 1.6630, b = 0.2835, `DIRECTION_NS`) | NEW family |
| F | House generic ballot | raw + calibrated (Platt a = 2.7534, b = 0.4401, `HOUSE_BALLOT_NS`) | NEW family |

Everything else is frozen as in FT3: Qwen3-14B + the incumbent adapter, soft first-token
elicitation, ATP W161 frame (3,170 weighted profiles), one GPU run per (instrument ×
anchor) pair; arms B, C, E-cal and F-cal are CPU transforms of the same rows, so every
arm within an instrument shares its GPU output byte for byte.

## Registered quantities and bars

### Approval (arms A, B, C)
- Topline Approve error ≤ 5; Net error ≤ 8; sex/age/race 9-cell MAE ≤ 6 — each of A, B, C.
- Party MAE ≤ 12 — arm B only (registered); A and C party cuts published, unscored.
- Head-to-head 1 (continuity): B's party MAE < A's.
- **Head-to-head 2 (NEW, the E35 claim): C's |Not-sure error| < A's, AND C's topline
  Approve error is not worse than A's by more than 0.3.** Both halves or the claim fails.
- Structure bar (FT3 bar B, kept as a measurement): 9-cell deviation MAE vs
  persistence-of-deviations, arms A and B. Backtest expectation unchanged: lean against us.
- Movement bar (FT3 bar C, kept): |predicted change − actual change| ≤ 3, arms A and B.
  **Registered expectation from E48: predicted change ≈ 0.1 × actual** — we pass only
  when the published wave moves ≤ ~3 points, which on this tracker is most weeks. Passing
  it therefore says little; failing it would say the wave moved, not that we tracked it.

### No-anchor ablation (arm D) — a registered expectation of failure
- Scored on the same three bars as arm A. **Registered prediction: topline FAILS
  (error ≈ −6, from E47's 28.6 against a 33–40 season).** 9-cell structure is expected
  to hold (E47: pooled six-family uAUC unchanged without the anchor).
- Rationale: the anchor's contribution has been measured retrodictively three times
  (backtest rounds 1–2, E47, E48); this puts it on the public record prospectively, in
  the same falsifiable form as FT3's movement bar. If D passes, the anchor is not doing
  what we claim and that is the finding.

### Direction of country (arm E)
- Right-direction % error ≤ 5 — raw and calibrated.
- Party cuts (D/I/R right-direction, published in the tabs) MAE ≤ 12 — calibrated only.
- Head-to-head: calibrated party MAE < raw's.
- Disclosed: the DK over-hedge is expected to be large on this family (HH1 registered
  29.3% DK on the same question form; E/YouGov publishes ~9%). The dk repair is NOT
  registered for direction (E35 fit approval only); right-direction is scored as printed.

### House generic ballot (arm F)
- Democratic-candidate share error ≤ 4 and D−R margin error ≤ 4 — raw and calibrated,
  scored against the **toplines row as printed among adult citizens** (Q9 form: Dem /
  Rep / Other / Not sure / Will not vote).
- Party cuts MAE ≤ 12 — calibrated only. Head-to-head: calibrated party MAE < raw's.
- Disclosed frame note: the tabs also report a registered-voter cut; we register against
  the adult-citizen row because our frame is adults. Our instrument's abstain set (Other,
  Not sure, Will not vote) is scored as one abstain mass; the bars are on D and R shares
  of the full column, not of the two-party vote.

### Persistence baseline — standing scoreboard column (all instruments)
Every registered quantity is published at verdict beside **last-wave persistence** (the
previous published wave's value for the same quantity). No bar is registered against
persistence on a single wave — E48's 12–10 split says one wave is a coin flip — but the
private method ledger (`docs/ledger/`) appends the wave for every arm, and the promotion
rule stands: a method earns a registered persistence claim only after four consecutive
ledger wins on a quantity it actually moves on. Standing ledger at declaration (six
scored E/YouGov waves, Jul 20 – Aug 24):

| method | mean \|approve err\| | mean \|net err\| | mean party MAE |
|---|---|---|---|
| raw | 2.67 | 2.52 | 22.53 |
| calibrated | 3.60 | 3.37 | 10.15 |
| persistence | 2.00 (5w) | 4.20 (5w) | 2.33 (5w) |

E48's season-scale result (calibrated 1.59 vs persistence 1.77, n = 22) is the
disclosed context for why the calibrated topline bar is kept rather than dropped.

## Era anchor — protocol v1, binding from this registration

The anchor is produced by `quorum/twin/anchor_builder.py` for the registration date, per
`docs/anchor-protocol-draft.md` (which becomes protocol v1 when this document is pushed):
date + office sentence; standing-conflict status from the pinned "2026 in the United
States" revision; latest BLS CPI-U and AHE 12-month changes and the EIA/AAA gasoline
price, verbatim; the next federal election. No polling numbers; no news events; no
adjectives outside the sources. Published with the registration: the anchor text, its
sha256, the builder manifest (Wikipedia revid, BLS series ids and vintages, gas citation)
and `anchor-facts.json`, exactly as GS1/HH1 did. The hand-authored anchor of FT1–3 is not
built; the registered delta between authored and mechanical anchors is therefore not
measurable here and is not claimed.

## Disclosures carried at registration
1. The level prior is rigid (E22/E24/E34/E40/E44/E45: seven configurations, slopes ≈ 0);
   every topline rides the anchor plus calibration.
2. Persistence is published beside every quantity (standing column above).
3. The "Not sure" over-hedge is repaired in arm C only; arms A, B, E, F carry it as before.
4. E48 mechanism: the calibrated arm's season-scale edge over persistence is shrinkage
   toward the mean, not tracking; movement response ≈ 0.1.
5. Direction and ballot are validated on Nationscape gold (Dec 2019), not on E/YouGov
   microdata; their calibrations are cross-era by construction (the same transport the
   approval map survived 2019 ↔ 2025, untested for these families).
6. Ballot frame mismatch (adult citizens vs registered voters), and the three-way abstain
   set, as above.
7. Arm D's registered expectation of failure, and the E47 curve it rests on.
8. This is the incumbent 14B's registration. phi-4 entered the engine bench (E45,
   5/6 families, abstention 4.6%); its promotion into the public series is a separate
   registered decision and is not part of FT4.

## Not registered, and why
- **Trump favorability.** Calibration frozen (E16, a = 3.2278, b = 1.2575) but the
  E/YouGov weekly toplines do not carry a Trump favorability item every wave (absent from
  Aug 21–24); no target, no registration.
- **An enriched anchor arm.** E47: +0.2 points beyond the protocol anchor. Nothing to learn.
- **A news-digest arm.** Backtest round 3 + E47: valence steering, no accuracy. Unchanged.
- **A two-stage / per-party-intercept arm.** On a weekly-polled question it reduces to
  persistence (E28); it belongs in an unpolled-question demonstration.
- **phi-4 as a challenger arm.** Open decision (pending.md); registering it here would
  pre-empt the decision by drift.

## Pre-registration work (must be committed before the public push)
1. **Scorer extension**: `scripts/score_ft.py` grades approval only. Add per-instrument
   scoring for direction (right-direction topline + party cuts) and ballot (D share, D−R
   margin, party cuts), and the arm-C head-to-head (NS error + topline delta ≤ 0.3).
   Identity gate `--verify-ft1` must still pass. Committed pre-registration, sha cited.
2. **dk transform as a committed script**: `dkfix` from `scripts/e35_dk_repair.py` /
   `scripts/backtest_methods_full.py` (s = 0.5618) lifted into a CLI that reads arm A's
   `rows.jsonl` and writes arm C's `forecast.json` — so arm C is reproducible from the
   public rows by anyone.
3. **Published-JSON transcription schema** extended with `direction` and `house_ballot`
   blocks (topline + party), so the verdict is scored from one cited file per wave.

## Registration-day checklist
1. FT3 verdict public (this document does not push before it).
2. `anchor_builder.py --date <D> --out data/forward/ft4/anchor-ft4.txt` → sha256 + manifest
   + facts.json; empty `anchor-none.txt` for arm D.
3. One GPU session (L40S:1 spot, `quorum-monday` pattern): `forecast.py` × {approval,
   direction, house_ballot} × protocol anchor, plus approval × no-anchor — four GPU
   passes; calibrated and dk arms as CPU transforms of the same rows.
4. Stamp forecast shas here; drop DRAFT; copy protocol + forecasts + anchor set + SHA256SUMS
   + `tracking.csv` rows (FT4 ids per arm) to quorum-forward-tests; **Chirag pushes.**

---

## Open scope decision (Chirag)

**Option 1 — three instruments (recommended, drafted above).** Approval (A–D) +
direction (E) + ballot (F). Cost: one extra GPU pass per family (~20 min each), the
scorer extension, and two new families' worth of public miss risk — both disclosed
as surrogate-validated. Value: the first cross-family public test, on the same wave.

**Option 2 — approval only (A–D).** Drop E and F; keep the E35 arm and the no-anchor
ablation. Direction/ballot wait for HH1's verdict as their first public score.

Default if unanswered: Option 1, with E and F carried as **measurements** (bars scored
and published, no headline claim) rather than claims, on first registration.

## Registration (2026-09-02) — numbers and hashes

Scope decision: **Option 1 (three instruments)**, Chirag 2026-09-02 ("A"); FT3 verdict
public at `96ba833` before this registration.

**Era anchor (protocol v1, now binding)** — built `2026-09-02` by
`quorum/twin/anchor_builder.py` from `anchor-facts.json`; five sentences, linter clean:
- file `anchor-ft4-2026-09-02.txt` sha256
  `3dce5884ce95dcc647e8afd4c2e93cabbcf11544e70f0dd5e4320f5927c0a98d`
- Wikipedia "2026 in the United States" revid **1372707519** (2026-09-01T22:28:53Z);
  conflict clause phrased from that revision (war since February; MoU to end it signed
  June; 60-day deadline expired August; strikes and attacks continued since)
- BLS `CUUR0000SA0` 2026-07 vs 2025-07 → 3.4%; `CES0500000003` → 3.2% (latest releases
  before D; the August releases post ~Sep 10)
- AAA national average 2026-09-01 $4.0954 (rendered $4.10)
- arm D anchor: empty file (0 bytes), E47 precedent

Emission: `quorum-ft4` box (L40S:1 spot; `infra/skypilot/quorum-ft4.sky.yaml`), seven
`forecast.py` passes on the W161 frame (3,170 profiles); arm C by `scripts/dk_shrink.py`
on arm A's rows. Forecast shas stamped below when the run lands.

Run: `quorum-ft4`, L40S:1 spot; attempt 1 (ap-northeast-2b) reclaimed 08:57 IST after
arm A banked; attempt 2 (ap-northeast-2b again, after capacity misses in eu-south-2c and
ap-south-1a) resumed from the bank and SUCCEEDED 09:34 IST; teardown EC2-verified.
Seven GPU passes at git `9c0dd4e`; arm C by `scripts/dk_shrink.py` on arm A's rows.
Forecast files are `ft4/forecast-ft4-<arm>.json` in the public repo; shas in `SHA256SUMS`.

**Approval (W161 frame, 3,170 profiles) — arms A / B / C / D**

| Quantity | A raw | B calibrated | C raw + dk | D no-anchor |
|---|---|---|---|---|
| Approve | **33.3** | **34.1** | **34.8** | **28.5** |
| Disapprove | 56.7 | 55.9 | 59.5 | 59.0 |
| Net | −23.4 | −21.8 | −24.7 | −30.5 |
| Not sure | 10.0 | 10.0 | **5.6** | 12.5 |
| Party D / I / R | 25.0 / 31.8 / 43.7 | **11.0 / 28.7 / 64.9** | 26.6 / 33.5 / 45.2 | 23.8 / 28.7 / 33.1 |
| Sex F / M | 31.5 / 35.4 | 28.9 / 40.0 | 32.9 / 36.9 | 27.5 / 29.7 |
| Age 18-29 / 30-44 / 45-64 / 65+ | 32.3 / 33.0 / 34.0 / 33.8 | 31.4 / 33.5 / 36.2 / 35.4 | 34.0 / 34.7 / 35.5 / 35.3 | 28.2 / 28.5 / 28.7 / 28.8 |
| Race Black / Hispanic / White (Other unscored) | 27.9 / 31.7 / 35.1 (31.9) | 18.5 / 29.4 / 39.3 (29.5) | 29.5 / 33.4 / 36.6 (33.5) | 25.7 / 27.8 / 29.4 (27.7) |

Movement-bar reference (bar C): previous published wave (Aug 28–31) approve 36 —
registered predicted change raw −2.7, calibrated −1.9 (E48 expectation: ≈ 0.1 × actual).
Arm D sits 7.5 below the last published wave — the registered expectation of a topline
FAIL is live in the numbers before the target fields.

**Direction of country — arm E** (raw / calibrated, DIRECTION_NS a = 1.6630, b = 0.2835)

| Quantity | E raw | E calibrated |
|---|---|---|
| Right direction | **18.7** | **14.1** |
| Wrong track | 52.3 | 56.8 |
| Not sure | 29.1 | 29.1 |
| Party D / I / R (right direction) | 15.1 / 17.2 / 24.2 | 9.4 / 12.0 / 21.6 |

**House generic ballot — arm F** (raw / calibrated, HOUSE_BALLOT_NS a = 2.7534, b = 0.4401;
adult-citizen row: Dem / Rep / Other / Not sure / Will not vote)

| Quantity | F raw | F calibrated |
|---|---|---|
| Democratic candidate | **33.6** | **37.7** |
| Republican candidate | 35.9 | 31.8 |
| D − R margin | −2.3 | +5.9 |
| Other / Not sure / Will not vote | 14.5 / 9.6 / 6.4 | 14.5 / 9.6 / 6.4 |
| Party D / I / R (Democratic share) | 51.7 / 32.4 / 17.6 | 69.4 / 39.2 / 4.7 |

### Registration-day disclosures (added with the numbers, before the target fields)

9. **Direction, calibrated, moves the wrong way.** The Nationscape-fitted map lowers
   right-direction from 18.7 to 14.1, while the last three published waves read 25–27.
   Both E arms sit 8–13 points below the last wave against a ±5 bar; the calibrated arm
   sits further. The DK share (29.1 vs published ~11) is the disclosed over-hedge, and a
   cross-era calibration fitted in Dec 2019 (right-direction then ~40%) does not transport
   the level. Registered anyway, as a measurement, exactly as the protocol said it would
   be; a public miss here is the expected outcome and is priced in now.
10. **Ballot, raw, orders the parties backwards** (R 35.9 > D 33.6 against a published
   D 36 / R 31); the calibrated arm restores the ordering (D 37.7 / R 31.8, margin +5.9
   vs the last wave's +5). The raw instrument also puts 14.5% on "Other" — the abstain
   set absorbs mass the published column keeps at 1% — so the raw D-share bar and margin
   bar are both at risk. The calibrated arm is inside both bars against the last wave.
11. **Approval, raw vs FT3**: the anchor's contemporaneous facts moved the raw topline
   +0.7 from FT3 (32.6 → 33.3) with the published series flat at 36 — within the E48
   movement response. The race cells that broke FT3's raw 9-cell bar are unchanged in
   shape (Black 27.9 raw / 18.5 calibrated / 29.5 dk against a last-wave 11).

## Verdict
*(empty at registration)*
