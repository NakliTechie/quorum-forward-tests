# HH1 — Harvard CAPS/Harris Registration DRAFT (not yet registered)

**Status: DRAFT 2026-08-27. Becomes a registration when pushed to the public repository
(quorum-forward-tests) with forecasts and hashes, BEFORE the target begins fielding.**
Target: **the first Harvard CAPS/Harris poll to begin fielding after the public push**
(order-based; their cadence is irregular — 25-57 day gaps, next wave expected late Aug
to mid-Sep 2026; recon: docs/harvard-harris-recon.md).

## Registered quantities and bars

| Quantity | Arm | Bar |
|---|---|---|
| Trump approval topline (M3ALT convention) | raw + house-adjusted | error ≤ 5 |
| Approval net | raw + house-adjusted | error ≤ 8 |
| Right track % (M1) | raw + house-adjusted | error ≤ 5 |
| Generic ballot Democrat share (CON2026B, two-row) | raw + house-adjusted | error ≤ 4 |
| Approval party cuts D/I/R | house-adjusted only | MAE ≤ 12 |

Head-to-head claim: the house-adjusted arm beats raw on approval topline error.

## Method (frozen at registration)

- Engine: the frozen FT-series method (Qwen3-14B + FT adapter, soft first-token).
- Frame: **W161 recomposed to Harvard-Harris's own printed standing composition**
  (party Dem 33 / Rep 35 / Ind 28 / Other 3 — their decks' fixed weighting targets;
  composition facts, not polling results). `scripts/build_hh_frame.py`,
  frame sha `6653915b47277578d2170c275c57699fe6538e93d347cd5ba990d112a2bd5743`.
- Instruments: `hh_approval`, `hh_direction`, `hh_generic_ballot` — wording verbatim
  from their topline decks (M3ALT / M1 / CON2026B), including the disapprove-first
  approval question and the forced two-row ballot.
- Era anchor: fresh at registration (mechanical builder), sha-pinned, no polling numbers.
- **House-adjusted arm, declared now**: approve +7.2, disapprove −7.0 (and net +14.2)
  added to the raw forecast — the recon's measured five-wave mean frame-plus-house gap
  vs Economist/YouGov (computed 2026-08-19 from waves published BEFORE this
  registration; never refitted after). Right-track and ballot carry no offset (no
  measured gap available; disclosed).

## Disclosures

1. Frame hybrid: theirs is registered voters weighted to general-adult targets; ours is
   the W161 adult frame recomposed to their printed party targets only — other margins
   inherit W161. A coarse approximation, disclosed as such.
2. The house offset is a naive fixed additive from a five-wave cross-publisher gap; it
   conflates frame and house effects (recon section 5 caveat, carried verbatim).
3. Family validation is surrogate: approval (W161 gold), direction + generic ballot
   (Nationscape gold, E16, uAUC 0.765/0.950) — not validated on HH microdata, which
   does not exist publicly.
4. No per-person gold from the publisher; party cuts come from their key-results decks.
5. Registration-day inputs: fresh anchor + one GPU micro-run (3 instruments × HH frame,
   ~20 min; rides the GS1 box as job 3).

## Registration-day checklist
1. Fresh era anchor (mechanical builder) → sha.
2. Emit raw forecasts (3 instruments, HH frame); apply the declared offsets → the
   house-adjusted companion JSONs.
3. Stamp shas here; drop DRAFT; copy to quorum-forward-tests with SHA256SUMS +
   tracking.csv rows (HH1 ids); **Chirag pushes**.

## Registration stamps (2026-08-29)

- Era anchor: shared with GS1 same-day — sha256 `d0a4a8b614090b908d25d52edc1ae202e58a48ea84d299fdfb28e2afcb579b95` (mechanical builder manifest `20d0c1e2…df1326`).
- Raw forecasts (frame sha `6653915b…d743`, W161 recomposed to HH party targets):
  - approval (M3ALT): 37.3 approve / 56.1 disapprove / 6.5 NS, net −18.8 — sha256 `b2e23b3cef00a912b51fcb9642a003aa5a7ca35325bb388153ec3d627512ec5c`
  - direction (M1): 24.5 right / 46.1 wrong / 29.3 DK — sha256 `7538cb6ff52ffebcee8ee7e8e2bdb748e80b38698d29cc407d7241263d9bd941`
  - generic ballot (CON2026B): D 46.6 / R 53.4 — sha256 `8bbe6de377482c820eac4eb208eddd9dd3d369e9f423d4e9debb23c8de9aadd8`
- House-adjusted companion (declared offsets applied as arithmetic, approval only):
  44.5 approve / 49.1 disapprove, net −4.6 — sha256 `bc07954a795e6188b31cceb3987b44a00a6ac0914a91eeec52d1eb7b7d0798b4`
- Known-defect note carried at registration: the 29.3% DK on direction is the
  disclosed not-sure over-hedge (E35 repair not registered for this family).

## Verdict
*(empty at registration)*

## Out-of-registration shadow comparison — August 2026 wave (added 2026-09-03)

The Harvard CAPS/Harris August poll (fielded **August 28–30**, n = 2,100 RV, released
September 2; key results `HHP_Aug2026_KeyResults.pdf`, approval p.8, right track p.4)
**began fielding one day before this registration's public push** (commit `4881748`,
2026-08-29 12:08 IST). Under the registered order-based rule it is therefore **not HH1's
target**; the target remains the first Harvard-Harris poll to begin fielding after the
push (their next wave, ~late September). Because the forecasts above were public before
any of this wave's results existed, we report the comparison here at reduced volume, as a
shadow — it is not a scored verdict and does not enter the tally.

| Quantity (registered bar) | Published Aug 28–30 | Registered forecast | Shadow error |
|---|---|---|---|
| Approve, raw (±5) | 44 | 37.3 | −6.7 — would miss |
| Approve, house-adjusted (±5) | 44 | 44.5 | **+0.5** — would hit |
| Net, raw (±8) | −8 | −18.8 | −10.8 — would miss |
| Net, house-adjusted (±8) | −8 | −4.6 | +3.4 — would hit |
| Right track (±5) | 37 (DK 11) | 24.5 (DK 29.3) | −12.5 — would miss |
| Generic ballot, Democrat share RV (±4) | 51 | 46.6 | −4.4 — would miss by 0.4 |
| Approval party cuts D / I / R, adjusted (MAE ≤ 12) | 13 / 36 / 80 | 28.4 / 34.4 / 48.2 | cells +15.4 / −1.6 / −31.8, MAE 16.3 — would miss |

Two things the shadow teaches before the true target fields. The fixed house offset
(+7.2 approve, from a five-wave cross-publisher gap) landed the adjusted topline within
half a point — the one clean signal. And the adjusted arm's party cuts are the raw arm's
(the offset was applied to the topline only, an omission in how the companion JSON was
built — disclosed here); the raw party compression (Republicans 48.2 vs 80) is the same
defect the E/YouGov series corrects with calibration, which HH1 did not register. The
direction miss (−12.5, DK 29.3 vs 11) is the same abstention over-hedge disclosed at
registration and, on the E/YouGov side, at FT4. Head-to-head (adjusted beats raw on
approval topline): would have been upheld.
