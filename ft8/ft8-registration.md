# Forward Test 8 — registration (2026-09-29)

**Status: REGISTRATION. Bars and claims fixed here before any FT8 forecast existed
(this section written before the emission ran); numbers and hashes stamped below after.**
Target: the first *Economist*/YouGov weekly poll to begin fielding after the public push
(expected Oct 2–5, publishing ~Oct 6). If the push lands after that wave begins
fielding, the target is the following wave (expected Oct 9–12), by the same rule.

## What FT8 carries, and why

FT8 is FT7's registration re-run on a fresh mechanical anchor, with **one change** decided by
Chirag on 2026-09-29, before any FT8 forecast existed: **movement bar C is replaced by the
tracking measure.**

- **Why bar C goes.** Bar C took the forecast's change and the poll's change from the same
  previous poll. The previous poll cancels, so |predicted change − actual change| reduced to
  |forecast − poll|: a ±3 topline bar. It never tested tracking. The scorer shows the identity
  (`scripts/score_ft.py`, bar C note "equals |topline error|; not a tracking test"); the public
  repo's `ERRATA.md` (2026-09-29) records it. FT1–FT7 are scored with bar C as registered, and
  bar C is never reported as tracking evidence.
- **What replaces it.** The tracking measure: |(FT8 forecast − FT7 forecast, same arm) −
  (target poll − previous poll)| ≤ 3, for A, B, C, P and P-cal. It compares the engine's own
  week-over-week change with the poll's. It is a **measurement registered as expected to FAIL**
  on any wave that moves: the level prior is rigid (season slope of engine change on poll
  change 0.158 calibrated, 0.078 raw, FT1–FT6, `score_ft.py --tracking-series`). Scored with
  `score_ft.py --prev-ft 7`. On a wave that moves less than ~3 points it can pass without the
  engine tracking anything; the slope across waves, not one wave's pass, is the evidence.
- Everything else is unchanged: every arm, map and bar is FT7's. phi-4 continues as a parallel
  arm (Chirag 2026-09-24: keep for now, review ~Oct 8). `direction_dk` continues. E50 (Jev)
  and E52-F stay private (Chirag 2026-09-29: FT8 unchanged; J-cal decided Oct 8).

## Arms (all on the Sep 29 mechanical anchor; every calibrated arm a CPU transform of its raw rows)

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

Head-to-heads, all two-sided, reported at equal volume either way (identical to FT7):
1. B party MAE < A party MAE (series continuity).
2. C vs A on abstention (as FT4–7).
3. P-cal party MAE < B party MAE.
4. |P-cal topline err| < |B topline err|.
5. |P-cal net err| < |B net err|.

Structure bar (FT3 form) reported for A, B, C, P, P-cal, with a persistence column beside every
quantity. **Tracking measure** (replaces movement bar C) reported for A, B, C, P, P-cal against
FT7's registered numbers and the FT7 target poll. Scored on the base as printed (RV for the
last four waves), disclosed. The per-wave tally stays 8 (raw 3 bars + calibrated 4 bars +
H2H1); the tracking measure is a measurement and is not in the tally.

## Registered expectations
- The level prior is rigid: the 14B sits ~33–35 for the fifth straight registration and
  phi-4 ~42–44. We register no view on the wave's level.
- Tracking measure: engine change within ±1.5 of zero for every arm; FAIL on any wave whose
  poll moves more than ~4.5 points from the FT7 target.
- H2H4 and H2H5 to the 14B unless approval rises past ~39. H2H3 (party) is the open contest.
- Arm D: −6 to −12, FAIL. Arm E: −1 to −5, as FT6–7.

## Disclosures
1–19 as FT7, plus: 20. FT8 was declared on Sep 29 (IST) before FT7's target (fielded
Sep 25–28) published; no FT7 outcome is known at declaration. 21. The anchor differs from
FT7's in the date and the AAA gas price ($4.4744 → $4.4558; the sentence prints $4.47 → $4.46);
CPI-U and AHE stay at the **August** vintage. 22. Pinned Wikipedia revision 1377272614
(2026-09-28T17:01Z) against FT7's 1376395930: the war's status is unchanged, so the conflict
clause is unchanged. The newer revision adds that Trump rejected Iran's seven-day ceasefire
proposal and that the *Wall Street Journal* reports he expects U.S. bombing to resume after the
midterms; neither changes the page's description of a state of war. 23. Movement bar C →
tracking measure (above); the change is Chirag's (2026-09-29), made on the scorer's own
identity, not on any wave's outcome. 24. Fourth consecutive RV-base target is expected; the
frame (W161 adults) is unchanged. 25. Codex pre-run review (docs/reviews/2026-09-29-ft8-pre-codex.md):
FT7's box ran at git `b8a0c14`, not the `85ec877` its protocol names; the two differ in no file
under `quorum/` (scorer, docs, plans), so FT7's engine code was the declared one. FT8 stamps the
git field its manifests record. The review's resume, shutdown-timer, run-id, scorer and
anchor-facts fixes touch no arm, map or bar. 26. The direction companion's s = 0.308 was fit on
the Aug 21–24 published direction DK (FT6 protocol); `dk_shrink.py` labels every transform
"E35", which is wrong for direction.

## Registration (2026-09-29) — numbers and hashes

**Public timestamp of record:** *(stamped after the public push)*

Run: `quorum-ft8`, ap-northeast-2b L40S:1 spot (g6e.xlarge: sky's cheapest L40S shape; FT7 ran on
g6e.2xlarge — same GPU, fewer CPUs). Launched 14:54 IST by Python API with retry-until-up; sky
tried eu-south-2c, then ap-northeast-2a (no capacity), and the box came up in ap-northeast-2b at 14:56.
All five GPU passes ran at git `ef91442` (this declaration plus the Codex pre-review fixes; the
manifests record `ef91442…+dirty`, the dirty part being an uncommitted plan note) in ~29 min,
0 reclaims; every pass banked to S3 with a size-verified mirror (15 files, run id
`ft8-2026-09-29`). Every downloaded forecast's sha matches the box log; every rows file has 3,170
rows. Anchor: protocol v1, 2026-09-29, sha256 `d95996b8ede85bd0…`, revid 1377272614, AAA $4.4558,
CPI-U and AHE at the **August** vintage. Every calibrated/dk arm is a CPU transform of its raw rows;
before running them on FT8, the same five commands reproduced FT7's five registered companions
byte for byte. 27. Disclosure: since FT7's box, `quorum/twin/forecast.py` gained an opt-in Jev
backend (`--backend jev`, E50); the default vLLM path FT8 ran is unchanged in behaviour.
28. Codex post-run review (docs/reviews/2026-09-29-ft8-post-codex.md): `forecast.py` rounds each
option before it sums the toplines, so a summed figure can differ by 0.1 from the unrounded sum
(D approve 28.6 vs 28.5; A net −23.0 vs −23.1). FT1–FT7 carry the same rounding; FT8 keeps it so
the series stays comparable. The review reproduced all five raw aggregates and all five
companions byte for byte.

**Approval — 14B spine and phi-4 challenger**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | P phi-4 raw | P-cal phi-4 |
|---|---|---|---|---|---|---|
| Approve | **33.5** | **34.4** | **35.0** | **28.6** | **42.3** | **44.0** |
| Disapprove | 56.5 | 55.6 | 59.3 | 59.0 | 50.8 | 49.0 |
| Net | -23.0 | -21.2 | -24.3 | -30.4 | -8.5 | -5.0 |
| Not sure | 10.0 | 10.0 | 5.6 | 12.5 | 7.0 | 7.0 |
| Party D/I/R | 25.1 / 32.1 / 44.0 | 11.2 / 29.0 / 65.4 | 26.6 / 33.7 / 45.4 | 23.9 / 28.7 / 33.1 | 23.1 / 33.9 / 74.1 | 17.9 / 33.1 / 86.5 |

**Direction (arm E, measurement) and House ballot (arm F)**

| Quantity | E raw | **E direction_dk (s 0.308)** | F raw | F cal |
|---|---|---|---|---|
| Positive (right direction / Democrat) | 19.0 | **24.3** | 33.4 | **37.4** |
| Negative | 52.0 | 66.8 | 36.1 | 32.1 |
| Not sure | 29.0 | **8.9** | 9.5 | 9.5 |
| Party D/I/R (positive) | 15.3 / 17.3 / 24.9 | 19.6 / 22.4 / 31.3 | 51.8 / 32.2 / 17.3 | 69.4 / 38.8 / 4.4 |

Forecast shas (sha256, first 12): approval_raw `98c13115efc9` · approval_cal `db6e8c4133e3` · approval_dk `e97423a42f17` · approval_noanchor `37279d950170` · phi_raw `c0952f0008c6` · phi_cal `61d6b4b28aeb` · direction_raw `86b7a586dec9` · direction_dk `5c3072c46653` · ballot_raw `3b8e6e1da823` · ballot_cal `fc16b3312dc0`.

**Registered expectations, live in the numbers:** the 14B level is 33.5 raw / 34.4 cal, the fifth
straight registration between 33 and 35. The engine's own change since FT7 is 0.0 (A), +0.1 (B),
0.0 (C), 0.0 (P) and −0.1 (P-cal): it did not move. So the tracking measure passes only if the
poll's change from the FT7 target wave (Sep 25–28) to FT8's (Oct 2–5) lies in these intervals:
A, C and P [−3.0, +3.0]; B [−2.9, +3.1]; P-cal [−3.1, +2.9]. Any bigger move fails, in either
direction. A pass on a flat wave is not evidence of tracking. Arm D 28.6: FAIL for any wave above 33.6. Arm E direction_dk 24.3.

## Verdict
*(dated file `verdict-ft8-<date>.md`)*
