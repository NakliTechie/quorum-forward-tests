# Forward Test 7 — registration (2026-09-24)

**Status: REGISTRATION. Bars and claims fixed here before any FT7 forecast existed
(this section written before the emission ran); numbers and hashes stamped below after.**
Target: the first *Economist*/YouGov weekly poll to begin fielding after the public push
(expected Sep 25–28, publishing ~Sep 29). If the push lands after that wave begins
fielding, the target is the following wave (expected Oct 2–5), by the same rule.

## What FT7 carries, and why

FT6's target (fielded Sep 18–21, RV base, published Sep 22) printed approval at **35**, down
5 from FT5's 40. On the published toplines the 14B calibrated arm sits inside its topline
and net bars again and the phi-4 challenger misses both; FT6's dated verdict file is scored
from the full tab report by the committed scorer, separately. FT7 changes **no arm, no map,
no bar**: it is FT6's registration re-run on a fresh mechanical anchor, so the series gets a
third identical wave for the challenger and a second public test for `direction_dk`.
Nothing in FT7's design is fit to FT6's outcome.

- phi-4 **continues as a parallel arm**, not the spine. After two waves it is 1-for-2 on the
  topline head-to-head and its net error is the worst on the board; the spine question is
  a decision for Chirag, not an automatic consequence of either wave.
- `direction_dk` continues: FT6's bench rule ("benched if it misses") did not trigger on the
  published topline (23.9 vs 27, inside ±5).

## Arms (all on the Sep 24 mechanical anchor; every calibrated arm a CPU transform of its raw rows)

| Arm | Method | Bars |
|---|---|---|
| A 14B raw | frozen FT method | topline ±5 · net ±8 · 9-cell ≤6 |
| B 14B cal | Platt `approval_pooled_2019_2025` (3.6133, 1.3759) | A's bars + party MAE ≤12 (registered) |
| C 14B raw+dk | E35 shrink s = 0.5618 | A's bars; H2H2 (NS err < A's AND topline not worse by >0.3) |
| D 14B no-anchor | empty anchor | A's bars — **registered expectation: topline FAILS** |
| P phi-4 raw | E45 adapter, same frame/anchor/instrument | A's bars |
| P-cal phi-4 cal | Platt `phi4_approval_pooled_2019_2025` (1.5655, 0.2642) | A's bars + party MAE ≤12 (registered) |
| E direction_dk | 14B direction raw, dk-shrink s = 0.308 (frozen 09-10) | right-direction ±5 — **measurement** |
| F ballot raw / cal | `HOUSE_BALLOT_NS` (2.7534, 0.4401) | D-share ±4, margin ±4; cal party ≤12 |

Head-to-heads, all two-sided, reported at equal volume either way (identical to FT6):
1. B party MAE < A party MAE (series continuity).
2. C vs A on abstention (as FT4–6).
3. P-cal party MAE < B party MAE.
4. |P-cal topline err| < |B topline err|.
5. |P-cal net err| < |B net err|.

Structure and movement bars (FT3 form) reported for A, B, C, P, P-cal; persistence column
beside every quantity. Scored on the base as printed (RV for the last three waves), disclosed.

## Registered expectations
- The level prior is rigid: the 14B sits ~33–35 for the fourth straight registration and
  phi-4 ~42–44. If the wave holds near 35–38, B is inside the topline bar and P-cal is not;
  if it rebounds to ~40, the FT5 pattern repeats. We register no view on which.
- H2H4 and H2H5 to the 14B unless approval rises past ~39. H2H3 (party) is the open contest.
- Arm D: −6 to −12, FAIL. Arm E: −1 to −5, as FT6.

## Disclosures
1–16 as FT6, plus: 17. FT7 was declared on Sep 24 with FT6's target already published and
its toplines read; the arms are unchanged from FT6, so that knowledge enters no design
choice. 18. The anchor differs from FT6's in the date, the AAA gas price ($4.37 → $4.47) and
the pinned Wikipedia revision (1376395930; no change in the conflict's status between the
revisions); CPI-U and AHE stay at the **August** vintage (September CPI publishes mid-October).
19. Third consecutive RV-base target is expected; the frame (W161 adults) is unchanged.

## Registration (2026-09-24) — numbers and hashes

Run: `quorum-ft7`, ap-south-1b L40S:1 spot (g6e.2xlarge). The first launch at 10:05 IST found
no L40S spot capacity in any of the 13 allowed zones; a retry-until-up launch on the same
spec came up at 10:17. All five GPU passes ran at git `85ec877` (this protocol's declaration)
in 17 min, 0 reclaims; every pass was banked to S3 with a size-verified mirror (15 files).
Anchor: protocol v1, 2026-09-24, sha256 `40f96221ebd377a3…`, revid 1376395930, AAA $4.4744,
CPI-U and AHE at the **August** vintage. Every calibrated/dk arm is a CPU transform of its raw
rows; the transform commands reproduce FT6's five registered companions byte for byte.

**Approval — 14B spine and phi-4 challenger**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | P phi-4 raw | P-cal phi-4 |
|---|---|---|---|---|---|---|
| Approve | **33.5** | **34.3** | **35.0** | **28.5** | **42.3** | **44.1** |
| Disapprove | 56.6 | 55.6 | 59.4 | 59.0 | 50.8 | 49.0 |
| Net | -23.1 | -21.3 | -24.4 | -30.5 | -8.5 | -4.9 |
| Not sure | 10.0 | 10.0 | 5.6 | 12.5 | 6.9 | 6.9 |
| Party D/I/R | 25.1 / 32.0 / 43.9 | 11.3 / 28.8 / 65.2 | 26.7 / 33.6 / 45.3 | 23.8 / 28.7 / 33.1 | 23.1 / 34.1 / 74.0 | 17.8 / 33.2 / 86.6 |

**Direction (arm E, measurement) and House ballot (arm F)**

| Quantity | E raw | **E direction_dk (s 0.308)** | F raw | F cal |
|---|---|---|---|---|
| Positive (right direction / Democrat) | 18.9 | **24.1** | 33.4 | **37.5** |
| Negative | 52.2 | 67.0 | 36.1 | 32.1 |
| Not sure | 29.0 | **8.9** | 9.5 | 9.5 |
| Party D/I/R (positive) | 15.2 / 17.2 / 24.7 | 19.6 / 22.3 / 31.0 | 51.8 / 32.2 / 17.4 | 69.5 / 38.9 / 4.4 |

Forecast shas (sha256, first 12): approval_raw `57087b410a46` · approval_cal `5258d91961b1` · approval_dk `3377e9b0aed3` · approval_noanchor `0ebc7ebbe912` · phi_raw `3518489292a9` · phi_cal `3fed5a04dc25` · direction_raw `422298b3a80a` · direction_dk `37bdc8154b74` · ballot_raw `e429eddfd9b5` · ballot_cal `75686ec7cf84`.

**Registered expectations, live in the numbers:** the 14B level is 33.5 raw / 34.3 cal, the
fourth straight registration between 33 and 35. Against last week's 35, B is inside the
topline bar for any wave from 29.3 to 39.3; P-cal's 44.1 is inside only if approval reaches
39.1. H2H4 and H2H5 go to the 14B unless approval rises past ~39. Arm D 28.5: FAIL for any
wave above 33.5. Arm E direction_dk 24.1 against last week's 27: −2.9 on a flat wave.

## Verdict
*(dated file `verdict-ft7-<date>.md`)*
