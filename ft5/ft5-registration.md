# Forward Test 5 — registration (2026-09-06)

**Status: REGISTRATION. Bars and claims were fixed before any FT5 forecast existed (draft commit 4b0e5b4, 2026-09-06 morning); numbers and hashes stamped below after emission, no bar changed.** Registers
when pushed to the public repository with forecasts and hashes, BEFORE the target begins
fielding. Target: the first *Economist*/YouGov weekly poll to begin fielding after the
public push. Timing note: FT5 registers BEFORE FT4 scores (Chirag armed the emission on
2026-09-06); the targets do not overlap — FT4's wave began fielding 2026-09-04, before
any FT5 push, so FT5's target is the following wave (~Sep 11–14). Nothing in FT5's
arms depends on FT4's outcome.

## What FT5 adds: a challenger backbone, in public

E45 (2026-08-28) trained `microsoft/phi-4` under the byte-identical Stage-B recipe and
found it at or above the incumbent Qwen3-14B on 5 of 6 families (uAUC), with half the
abstention (4.6% vs 9.2%); E46 corroborated the one family where the 14B had looked
better (ETHICSDJT) as the 14B's own unlucky draw. Chirag's decision (2026-09-06, "phi-4
as a challenger arm"): phi-4 enters the public series as a **challenger beside the 14B
spine**, not in place of it. The honest test of a bench result is a registered head-to-head
on a wave neither engine has seen.

## Arms

**Continuity (14B spine, exactly FT4):** A raw · B calibrated (Platt a 3.6133, b 1.3759)
· C raw + dk (s = 0.5618) · D no-anchor ablation (expected FAIL) · E direction raw/cal ·
F House ballot raw/cal. Bars, head-to-heads 1–2, structure and movement bars as in FT4.

**Challenger (phi-4 + its E45 adapter, `runs/e45-phi/adapter`, sha stamped at registration):**

| Arm | Method | Status |
|---|---|---|
| P | phi-4 raw — same frame, anchor, instrument, elicitation as arm A | NEW |
| P-cal | phi-4 + its own Platt map, fitted on W161 (Feb 2025) per-person approval gold — the same gold, split and machinery as the 14B's map (E16 pattern: seed-fixed half for validation, full gold for the frozen params) | NEW |

Bars for P and P-cal: topline ±5, net ±8, 9-cell MAE ≤ 6; **party MAE ≤ 12 registered for
P-cal**. Head-to-head 3: **P-cal party MAE < B party MAE.** Head-to-head 4: **P-cal topline
error < B topline error.** Both are two-sided claims: if the 14B wins, the challenger is
reported as beaten at the same volume.

## Registered expectations from the bench (written before any FT5 number)
- E45's phi-4 raw approval under an August-2026 anchor read 43.3 approve (party 23.2 /
  33.7 / 78.0) — a level ~7 points above the published series and a raw party spread of
  55 points (the 14B's raw spread is 19). Expect **arm P to FAIL the topline bar and to
  carry near-published party structure uncalibrated**; expect P-cal to fix the level.
- The phi-4 abstention share (~5%) is close to the published "Not sure" (4–7); arm C's
  dk repair is therefore not registered for phi-4.
- Level rigidity is universal (E22/E24/E34/E40/E44/E45): phi-4's bare prior sat at 33–51
  across eras; its trained prior relocated by +25.5 points under the recipe. The anchor
  does the era work for both engines.

## Pre-registration work (committed before the push)
1. **Platt fit for phi-4** (`scripts/fit_phi4_platt.py`): transport `APPROVAL_W161` under
   the phi-4 adapter with the **February-2025 anchor** the 14B fit used (the gold is Feb
   2025, so the fit is era-matched); seed-fixed half validation (held-out party MAE and
   topline, raw vs calibrated, reported), full-gold freeze; (a, b) stamped here.
2. **Calibrated companion** (`scripts/cal_companion.py`): CPU transform of arm P's rows
   with the frozen (a, b) — reproducible by anyone holding the public rows.
3. Scorer: `scripts/score_ft.py` already grades any raw/calibrated pair; P/P-cal are scored
   with the same `_arm` path as A/B (a `--challenger-raw/--challenger-cal` flag pair to add,
   plus head-to-heads 3–4).

## Emission plan (one box, ~1.5 h, ~$2)
`infra/skypilot/quorum-ft5.sky.yaml`: 14B raw passes (approval, no-anchor, direction,
ballot) + phi-4 passes (transport `APPROVAL_W161` under the Feb-2025 anchor for the fit;
raw approval under the FT5 anchor). **Every calibrated arm (B, E-cal, F-cal, P-cal) is a
CPU transform of its raw rows** (`scripts/cal_companion.py`), and arm C a transform of
A's — one GPU pass per instrument, every companion reproducible from the public rows.
This changes FT1–4's practice, where the calibrated arm was a second GPU pass with
`--platt`; FT4's rows show two passes of identical prompts differ per row (vLLM batch
nondeterminism; arm B 34.1 vs 34.0 for the transform of arm A's rows). Disclosure 12.

## Disclosures carried at registration
1–8 as FT4, plus:
9. The challenger's calibration is fitted on the same 2025 gold as the incumbent's; neither
   sees 2026 data.
10. phi-4's adapter is one training draw (E45 seed 17); E46 showed the incumbent's draws
    reproduce within ±0.012 AUC, phi-4's draw-to-draw variance is not measured.
11. The challenger enters only the approval instrument in FT5; direction/ballot stay 14B.
12. GPU-pass nondeterminism: FT1–4's calibrated arms were separate passes; from FT5 the
    companions are transforms of the raw rows. The FT4 verdict will report arm B as
    registered (its own pass) and, beside it, the transform of arm A's rows (34.0) so the
    0.1-point pass-to-pass difference is on the record.

## Not registered, and why
- phi-4 on direction/ballot — no phi-4 family diagnostics on those instruments (E16 was
  14B-only); entry rule not yet applied.
- Mistral-7B — E45: structurally broken twin (party cuts flat at 40/40/40).

## Registration (2026-09-06) — numbers and hashes

Run: `quorum-ft5` (us-east-2c, L40S:1 spot, launched via the Python API — CLI 0.13.0
`sky launch` is broken, memory `sky-cli-launch-false-backend`) + fix-up box
`quorum-ft5-phins` (us-east-2b) for the phi-4 Nationscape pass (the first cluster's exec
task got an empty `/nationscape` mount; disclosed). Anchor: mechanical protocol v1,
`data/forward/ft5/anchor-ft5.txt` sha256 `f9c319d1da5508d8…`, revid 1373494658, AAA
$4.1473, CPI-U July 3.4, AHE August 3.1. Every calibrated arm is a CPU transform of its
raw rows (`scripts/cal_companion.py`); arm C a transform of A (`scripts/dk_shrink.py`).

**14B spine (frame W161, 3,170 profiles):**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | E dir raw/cal | F ballot raw/cal |
|---|---|---|---|---|---|---|
| Positive | **33.6** | **34.6** | **35.1** | **28.6** | 18.7 / 14.2 | D 33.4 / 37.3 |
| Not sure | 10.0 | 10.0 | 5.6 | 12.6 | — | — |
| Party D/I/R | 25.1/32.1/44.2 | 11.0/29.0/66.1 | 26.6/33.6/45.8 | 23.9/28.7/33.0 | 9.3/11.9/21.9 (cal) | 69.5/38.5/4.6 (cal) |

**phi-4 challenger (same frame, anchor, instrument, elicitation):**

| Quantity | P raw | P-cal |
|---|---|---|
| Approve | **42.4** | **44.1** |
| Not sure | 6.9 | 6.9 |
| Party D/I/R | 23.1/34.0/74.2 | 17.9/33.2/86.6 |
| Sex F/M | 40.8/44.3 | 41.9/46.8 |
| Age 18-29/30-44/45-64/65+ | 37.7/40.9/45.4/45.5 | 37.9/42.3/48.3/48.2 |
| Race Black/Hisp/White | 27.9/37.5/47.1 | 24.3/37.5/50.4 |

phi-4 Platt map **`phi4_approval_pooled_2019_2025` a = 1.5655, b = 0.2642**, fitted by
weighted MLE on pooled W161 (Feb 2025) + Nationscape (2019-20) per-person approval gold —
the same two-era recipe as the 14B's `approval_pooled_2019_2025`, refit for phi-4's own
soft outputs. Validation (seed-17 half held out, n = 3,630): party MAE **9.78 → 5.50**,
topline 45.6 → 47.8 vs gold 47.2. No 2026 data entered the fit.

Forecast shas (sha256, first 16): A `52df0b72cd8e962b` · B `da1512f4e5be8048` ·
C `7b1e73c3e17d2c1f` · D `524f81b19c842788` · E-raw `c72b1b5f344f2a26` ·
E-cal `5130c7dd1804afcc` · F-raw `7c3fe395879e57ae` · F-cal `881461021c8a5198` ·
P `26e9884979f4c0c5` · P-cal `6f398b4da3421366`.

**Registered expectations, live in the numbers before the target fields:**
- Arm D (no-anchor) 28.6 — ~7 below the series; the topline FAIL is registered.
- The challenger sits HIGH: P-cal 44.1 approve against a series at ~36. phi-4's pooled
  map centers ~8 points above the 14B's because phi-4's 2025 gold anchor pulls harder;
  **expect P-cal to MISS the topline bar and B to beat it (head-to-head 4 goes to the
  14B).** Head-to-head 3 (party MAE) is the open contest — phi-4's held-out party MAE
  5.50 is worse than the 14B's 5.63-era map on its own gold, so this is a genuine test,
  not a foregone win either way. Registered two-sided.
- phi-4 abstention 6.9 (vs 14B 10.0), closer to the published 4-7; no dk arm for phi-4.

Disclosure 13: the 14B's pooled-fit per-person rows are not archived locally, so the
challenger's "same recipe" is replicated by the stated method (weighted MLE on the two
eras), not byte-identical to the 14B's original fit call.

## Verdict
*(empty at registration)*

