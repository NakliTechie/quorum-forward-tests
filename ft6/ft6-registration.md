# Forward Test 6 — registration (2026-09-16)

**Status: REGISTRATION. Bars and claims fixed here before any FT6 forecast existed
(this section written before the emission ran); numbers and hashes stamped below after.**
Target: the first *Economist*/YouGov weekly poll to begin fielding after the public push
(expected Sep 18–21, publishing ~Sep 23).

## What FT6 carries, and why

FT5 (scored 2026-09-16) was the first model-vs-model wave: the phi-4 challenger won both
registered head-to-heads (party MAE 7.2 < 8.0; topline 4.1 < 5.4) and beat persistence on
subgroup structure, while failing its net bar by +13.2. The 14B calibrated arm missed its
topline for the first time (−5.4) on a wave that moved +3. Chirag's decision (2026-09-16,
history.md): phi-4 **continues as a parallel arm** with the same two head-to-heads
(two-sided) **plus a third on net error** — a bar the challenger would have lost on FT5,
added after seeing that, and disclosed as exactly that. Not promoted to spine on one wave.

## Arms (all on the Sep 16 mechanical anchor; every calibrated arm a CPU transform of its raw rows)

| Arm | Method | Bars |
|---|---|---|
| A 14B raw | frozen FT method | topline ±5 · net ±8 · 9-cell ≤6 |
| B 14B cal | Platt `approval_pooled_2019_2025` (3.6133, 1.3759) | A's bars + party MAE ≤12 (registered) |
| C 14B raw+dk | E35 shrink s = 0.5618 | A's bars; H2H2 (NS err < A's AND topline not worse by >0.3) |
| D 14B no-anchor | empty anchor | A's bars — **registered expectation: topline FAILS** |
| P phi-4 raw | E45 adapter, same frame/anchor/instrument | A's bars |
| P-cal phi-4 cal | Platt `phi4_approval_pooled_2019_2025` (1.5655, 0.2642) | A's bars + party MAE ≤12 (registered) |
| E direction_dk | 14B direction raw, dk-shrink s = 0.308 (frozen 09-10; backtest −1.1/−3.1/−5.1) | right-direction ±5 — **measurement**; the Platt arm is DROPPED; family benched if this misses |
| F ballot raw / cal | `HOUSE_BALLOT_NS` (2.7534, 0.4401) | D-share ±4, margin ±4; cal party ≤12 |

Head-to-heads, all two-sided, reported at equal volume either way:
1. B party MAE < A party MAE (series continuity).
2. C vs A on abstention (as FT4/5).
3. **P-cal party MAE < B party MAE.** FT5: phi-4 won (7.2 < 8.0).
4. **|P-cal topline err| < |B topline err|.** FT5: phi-4 won (4.1 < 5.4); we had called it for the 14B.
5. **NEW: |P-cal net err| < |B net err|.** FT5 would have gone to the 14B (2.8 < 13.2). Added
   after FT5 (decision (b)); registered so the challenger's known weakness is a scored claim.
   Registered expectation: the 14B wins this leg.

Structure and movement bars (FT3 form) reported for A, B, C, P, P-cal; persistence column
beside every quantity. Scored on the base as printed (RV for the last two waves), disclosed.

## Registered expectations
- The 14B level sits ~34–35 and does not move; if the +3 holds at ~40 (RV), B misses the
  topline again and phi-4's ~44 is inside the bar. If the wave reverts to ~37, both are inside.
  We register no view on which; the movement bar will fail for every arm either way.
- phi-4's net will be too positive by ~10; H2H5 to the 14B. Its party structure should
  again be inside ≤12 with Republicans close and Democrats ~14 high.
- Arm D: −8 to −12, FAIL. Arm E: −1 to −5 on the backtest — this is its one public test.

## Disclosures
1–13 as FT5, plus: 14. H2H5 is a post-result addition (see above). 15. Second wave for the
challenger; spine decision deferred to ≥2 waves. 16. E-cal dropped after 0/8 across FT4–5;
E's abstention repair's *s* is fit on the Aug 21–24 published DK (in-sample for that number).

## Registration (2026-09-16) — numbers and hashes

Run: `quorum-ft6`, ap-northeast-2b L40S:1 spot. Attempt 1 spot-reclaimed at ~35 min before
any pass banked; attempt 2 completed all five GPU passes in 21 min. The box's S3 mirror
(`cp -ru` to the mounted bucket) failed silently on attempt 2 — outputs were recovered by
rsync from the box before teardown and then banked; disclosed as an ops fault, not a data
one (row counts 3,170 × 5, shas below). Anchor: protocol v1, 2026-09-16, sha256
`c895fecf65aca4be…`, revid 1375208859, AAA $4.3672, CPI-U and AHE at the **August** vintage.
Every calibrated/dk arm is a CPU transform of its raw rows (scripts committed).

**Approval — 14B spine and phi-4 challenger**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | P phi-4 raw | P-cal phi-4 |
|---|---|---|---|---|---|---|
| Approve | **33.3** | **33.9** | **34.9** | **28.6** | **42.3** | **44.1** |
| Disapprove | 56.6 | 56.0 | 59.5 | 59.0 | 50.7 | 49.0 |
| Net | -23.3 | -22.1 | -24.6 | -30.4 | -8.4 | -4.9 |
| Not sure | 10.1 | 10.1 | 5.6 | 12.5 | 6.9 | 6.9 |
| Party D/I/R | 25.0 / 31.9 / 43.6 | 11.1 / 28.5 / 64.6 | 26.5 / 33.5 / 45.2 | 23.9 / 28.7 / 33.1 | 23.1 / 34.1 / 74.2 | 17.8 / 33.3 / 86.7 |

**Direction (arm E, measurement) and House ballot (arm F)**

| Quantity | E raw | **E direction_dk (s 0.308)** | F raw | F cal |
|---|---|---|---|---|
| Positive (right direction / Democrat) | 18.7 | **23.9** | 33.5 | **37.7** |
| Negative | 52.2 | 67.1 | 36.0 | 31.8 |
| Not sure | 29.1 | **9.0** | 9.6 | 9.6 |
| Party D/I/R (positive) | 15.2 / 17.1 / 24.3 | 19.6 / 22.2 / 30.6 | 51.9 / 32.4 / 17.4 | 69.5 / 39.3 / 4.5 |

Forecast shas (sha256, first 12): approval_raw `359fc28f71b0` · approval_cal `3fab815121fc` · approval_dk `a744b67bcfed` · approval_noanchor `fa145032a561` · phi_raw `c3a480f61167` · phi_cal `cac19093cd3d` · direction_raw `eafe4d0de1aa` · direction_dk `d15165ecabfa` · ballot_raw `fe601953c6f9` · ballot_cal `04a611b091c2`.

**Registered expectations, live in the numbers:** the 14B level is 33.3 raw / 33.9 cal for
the third straight registration — flat to the decimal under three different anchors. If
the wave holds at ~40 (RV), B misses the topline by ~6 and phi-4's 44.1 is inside the bar;
if it reverts to ~37, both are inside. H2H5 (net): B's net is -22.1 vs P-cal's
-4.9 against a series at −18 to −24 — the 14B wins this leg unless disapproval
collapses. Arm D 28.6: FAIL registered. Arm E direction_dk 23.9 against a series at 27–29:
expected −3 to −5, inside or at the bar's edge — its one public test.

## Verdict
*(dated file `verdict-ft6-<date>.md`)*
