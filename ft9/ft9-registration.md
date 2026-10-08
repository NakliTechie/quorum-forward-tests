# Forward Test 9 — registration (2026-10-08)

**Status: REGISTRATION. Bars and claims fixed here before any FT9 forecast existed
(this section written before the emission ran); numbers and hashes stamped below after.**
Target: the first *Economist*/YouGov weekly poll to begin fielding after the public push
(expected Oct 9–12, publishing ~Oct 13). If the push lands after that wave begins
fielding, the target is the following wave (expected Oct 16–19), by the same rule.

## What FT9 carries, and why

FT9 is FT8's registration re-run on a fresh mechanical anchor, with the Oct 8 review's decisions
(Chirag, 2026-10-08, recorded in plan/history.md before any FT9 forecast existed):

- **phi-4 is retired** (Chirag 2026-10-01: "Phi is badly off. We should drop it."). No P / P-cal
  arms and no H2H3/4/5. Record at retirement, FT5–FT8: calibrated 6 of 16 bars against the 14B's
  15 of 16; head-to-heads 2 of 11 (`verdict-ft8-2026-10-07.md`).
- **New public parallel arm: `ygdk`** (E53 amendment 1). The 14B calibrated rows re-weighted to
  YouGov's printed targets (party 31 D / 33 R, registered voters only), then the E35 not-sure
  shrink (s = 0.5618). A CPU transform of FT9's raw approval rows. It met its declared candidate
  rule on FT1–FT7 (approve MAE 1.56 against B 2.34 and Z1 2.29; net MAE 3.90; no wave beyond ±8).
- **Poll-only rules registered as arms.** Z1 (the last E/YouGov topline published before the push)
  and Z3 (the mean of the last four) carry A's topline and net bars. Z2 (the wave just before the
  target, known only at scoring) is reported beside every quantity, with no bar.
- **Ballot arm F2: the "Other" cap.** F-cal with each profile's "Other" scaled so the population
  "Other" is 3.0%, the removed mass given to D and R in that profile's own D:R ratio
  (`scripts/ballot_other_cap.py`). A reported arm.
- **Measurement companion: `ygframe`** (the re-weighting without the not-sure shrink), as FT8. Not
  counted.
- Everything else is FT8's: arms A–F, maps, bars, the tracking measure (scored with `--prev-ft 8`)
  and the per-wave tally of 8 (raw 3 bars + calibrated 4 bars + H2H1). ygdk, Z1, Z3 and F2 are
  reported beside the tally, not in it, until a separate decision adds them.
- Not in FT9: Jev J-cal stays private (Chirag 2026-10-08: "Keep it private"); the irregular-item
  bank in the earlier draft became UQ1's S1 arm (frozen separately); the E54 drift constant is
  reported beside Z1–Z3 only; vote-aware personas stay a research leg.

## Arms (all on the Oct 8 mechanical anchor; every calibrated or re-weighted arm a CPU transform of its raw rows)

| Arm | Method | Bars |
|---|---|---|
| A 14B raw | frozen FT method | topline ±5 · net ±8 · 9-cell ≤6 |
| B 14B cal | Platt `approval_pooled_2019_2025` (3.6133, 1.3759) | A's bars + party MAE ≤12 (registered) |
| C 14B raw+dk | E35 shrink s = 0.5618 | A's bars; H2H2 (NS err < A's AND topline not worse by >0.3) |
| D 14B no-anchor | empty anchor | A's bars — **registered expectation: topline FAILS** |
| **Y ygdk** | B's map, YouGov RV frame (`build_yg_frame.py --rv`), E35 shrink 0.5618 | topline ±5 · net ±8 (9-cell and party reported) |
| **Z1** | 38 approve / 60 disapprove (Oct 2–5, published Oct 6) | topline ±5 · net ±8 |
| **Z3** | 37.25 / 60.5 (mean of Sep 11–14, Sep 18–21, Sep 25–28, Oct 2–5) | topline ±5 · net ±8 |
| E direction_dk | 14B direction raw, dk-shrink s = 0.308 (frozen 09-10) | right-direction ±5 — **measurement** |
| F ballot raw / cal | `HOUSE_BALLOT_NS` (2.7534, 0.4401) | D-share ±4, margin ±4; cal party ≤12 |
| **F2 ballot cap** | F-cal + "Other" capped at 3.0% | D-share ±4, margin ±4, party ≤12 |

Head-to-heads, all two-sided, reported at equal volume either way:
1. B party MAE < A party MAE (series continuity; in the tally).
2. C vs A on abstention (as FT4–8).
- **H2H-Y:** |ygdk topline err| < |B topline err|.
- **H2H-Z:** |B topline err| < |Z3 topline err| — registered expectation: **NOT upheld** (B has beaten
  Z3 in 2 of 8 waves; mean error 2.51 against 1.72).
- **H2H-F2:** |F2 D-share err| < |F-cal D-share err|.

Structure bar (FT3 form) reported for A, B, C and ygdk, with a persistence column beside every
quantity. **Tracking measure** reported for A, B, C and ygdk against FT8's registered numbers and the
FT8 target poll (38). ygdk's predecessor is FT8's ygdk built by FT9's own method (`cal_companion.py` on
FT8's frozen raw rows, `artifacts-approval/forward-test-8/ft8_approval_ygdk/forecast.json`): **37.7**. The
private ledger value committed on Oct 1 (`e856c00`) rounds differently, 37.8; it is disclosed, not used
(Codex FT9 pre 3).

**Scoring.** ygdk is scored by A's bar function (topline ±5, net ±8; 9-cell and party reported, not
barred); Z1 and Z3 by the same topline and net bars; F2 by the ballot function (D-share ±4, margin ±4,
party ≤12); H2H-Y, H2H-Z and H2H-F2 as defined above. `score_ft.py` gains these before the public push and
is tested on FT8's files (Codex FT9 pre 2).
Scored on the base as printed (RV for the last five waves), disclosed.

## Registered expectations
- The level prior is rigid: the 14B sits ~33–35 for the sixth straight registration. We register
  no view on the wave's level.
- Tracking measure: engine change within ±1.5 of zero for A, B and C; FAIL on any wave whose poll
  moves more than ~4.5 points from 38.
- ygdk sits ~3 points above B (FT8: 37.8 against 34.4). H2H-Y goes to ygdk unless approval
  prints below ~36, the midpoint of the two.
- H2H-Z is NOT upheld: Z3 (37.25) beats B on the topline unless approval prints below ~35.8.
- Arm D: −6 to −12, FAIL. Arm E: about −6 if the direction series holds at 30 (FAIL); a pass needs
  right direction at 29 or below. (FT8's E expectation, −1 to −5, proved wrong.)
- F2 hits the D-share bar if the Democratic share prints between 40 and 48; F-cal misses it unless
  it prints 41 or below.

## Disclosures
1–26 as FT8, plus:
27. **FT8's outcome was known at this declaration.** FT8 was scored on Oct 7 (`9d26473`): approval
   38. The review that added ygdk saw that verdict and ygdk's private FT8 forecast (37.8, error
   −0.2, committed Oct 1 before that wave fielded). The candidate rule ygdk met was declared on
   Oct 1 on FT1–FT7.
28. The Oct 8 review ran by hand at 18:40 IST. The scheduled review and registration runs were
   disabled on Oct 7: the app's scheduler was jammed by other tasks' runs waiting on approvals.
29. The anchor differs from FT8's in the date, the AAA gas price ($4.4558 → $4.3612; the sentence
   prints $4.46 → $4.36) and the wage figure: BLS published September average hourly earnings on
   Oct 2, so AHE moves to the September vintage (3.1% → 3.0%; 37.81 / 36.70, series
   CES0500000003). CPI-U stays at the **August** vintage (September CPI publishes mid-October).
30. Pinned Wikipedia revision 1379188592 (2026-10-08T12:42Z) against FT8's 1377272614. The war's
   status is unchanged, so the conflict clause is unchanged. The newer revision adds stalled talks,
   the Iranian UN delegation ordered out (Oct 1, Oct 4), new sanctions (Sep 29, Oct 1, Oct 5) and
   about 9,000 troops sent to the Middle East as Trump weighs new strikes (Oct 1); none changes
   the page's description of a state of war.
31. The box is pinned to g6e.xlarge / g6e.2xlarge spot (FT8 allowed any L40S shape; the same GPU),
   so the hourly price is bounded at $2.76. Launched through `scripts/launch_guarded.sh` (identity
   check, watchdog and both deadline guards armed before submission).
32. Model identity (Codex FT9 pre 5): at this declaration Hugging Face's `main` for Qwen/Qwen3-14B is
   `40c069824f4251a91eefaf281ebe4c544efd3e18` (last modified 2025-07-26), the revision UQ1 pins. The box
   aborts unless the adapter's weights and config hash to UQ1's recorded values (`4cabea94…`, `563a0337…`),
   and writes the resolved model snapshot to `run_manifest.json`.
33. Spend and relaunch (Codex FT9 pre 1 + 4, confirm 1): the $8.28 ceiling is per launch attempt; a spot reclaim
   may be relaunched once (`RESTART=1`), so the bound across attempts is $16.56. No third attempt without Chirag.
   Each attempt writes to its own S3 folder (`runs/ft9-2026-10-08-<run name>`) and re-runs all four passes; no
   pass is resumed from an earlier attempt. The box also aborts before any GPU pass unless Hugging Face `main` for
   Qwen/Qwen3-14B is the pinned revision, and again after the passes unless the loaded snapshot is that revision.
34. ygdk and ygframe frame (Codex FT9 pre 6): YouGov's printed targets (31 D / 33 R) are applied to the
   W161 frame BEFORE the registered-voter filter, so the final shares differ from 31/33; the frame CSV's
   sha256 and its final party shares are stamped in the registration section.
35. The engine serves the 14B adapter as LoRA, as FT1–FT8 did, not UQ1's merged checkpoint. The
   determinism probe (Oct 4) measured run-to-run noise of about 1 point per simulated person and
   at most 0.3 points on a group total under this serving.

## Registration (2026-10-08) — numbers and hashes

Run: `quorum-ft9`, ap-northeast-2b g6e.xlarge (L40S:1) spot, launched 18:39 IST through `scripts/launch_ft9.sh ft9-a1`;
box up 18:42, job running 18:48, all four 14B raw passes banked by 19:03, torn down 19:04 with six regions checked
empty; 0 reclaims. Box checks: adapter weights `4cabea94…` and config `563a0337…` as UQ1 records; Hugging Face `main`
= `40c069824f42…` before the passes and the only cached snapshot after (`run_manifest.json`). Git `c6e257c` (+dirty:
uncommitted plan notes only). Every pass's box stamp (anchor, forecast, rows, manifest hashes; 3,170 rows) was
re-derived on the laptop from the downloaded S3 copy and matched. Every calibrated, shrunk, re-weighted or capped arm
is a CPU transform of those raw rows (commands in `scripts/` as named in the arms table); the same commands rebuilt
FT8's B, C, F-cal and ygdk byte for byte before this run. Anchor: protocol v1, 2026-10-08, sha256 `c9eed0e506001f9c…`,
revid 1379188592, AAA $4.3612, AHE September vintage, CPI-U August vintage. YouGov RV frame for Y and ygframe:
`data/yg/frame_yg_rv.csv` sha256 `374860befc4ec156…` (unchanged since FT8's companion); final weighted shares after
the RV filter D 32.94 / I 22.89 / R 35.66 / none 8.51 (targets 31 / 33 applied before the filter, disclosure 34).

**Approval — 14B arms, the ygdk arm, the poll-only arms and the companion**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | **Y ygdk** | Z1 | Z3 | ygframe (companion) |
|---|---|---|---|---|---|---|---|---|
| Approve | **33.6** | **34.7** | **35.1** | **28.5** | **38.0** | **38** | **37.25** | 36.5 |
| Disapprove | 56.4 | 55.2 | 59.2 | 59.0 | 56.5 | 60 | 60.5 | 53.7 |
| Net | -22.8 | -20.5 | -24.1 | -30.5 | -18.5 | -22 | -23.25 | -17.2 |
| Not sure | 10.1 | 10.1 | 5.7 | 12.5 | 5.5 | — | — | 9.8 |
| Party D/I/R | 25.2 / 32.2 / 43.9 | 11.4 / 29.4 / 65.5 | 26.7 / 33.8 / 45.5 | 23.8 / 28.7 / 33.1 | 12.1 / 30.9 / 67.8 | — | — | 11.4 / 29.6 / 65.6 |

**Direction (arm E, measurement) and House ballot (arms F, F2)**

| Quantity | E raw | **E direction_dk (s 0.308)** | F raw | F cal | **F2 cap 3.0%** |
|---|---|---|---|---|---|
| Positive (right direction / Democrat) | 18.6 | **23.8** | 33.4 | **37.3** | **43.9** |
| Negative | 52.4 | 67.3 | 36.0 | 32.0 | 36.9 |
| Not sure | 29.0 | **8.9** | 9.6 | 9.6 | 9.6 |
| Party D/I/R (positive) | 14.9 / 17.1 / 24.3 | 19.1 / 22.2 / 30.6 | 51.6 / 32.1 / 17.6 | 69.2 / 38.7 / 4.6 | 79.5 / 47.0 / 5.2 |

Forecast shas (sha256, first 12): approval_raw `ff924b1ebf8c` · approval_cal `c4a1bc287ee1` · approval_dk `aa94916bf445` ·
approval_noanchor `69e61516e0fc` · approval_ygdk `d5c478f3f8ff` · approval_ygframe `24123a2c488a` · direction_raw
`24c9760d99a5` · direction_dk `f7b6374f0cae` · ballot_raw `e93cb646361b` · ballot_cal `05568b6e138f` · ballot_f2
`2480c1fb29cf`. ygdk's tracking predecessor (FT8's ygdk companion, 37.7) is published beside them as
`predecessor-ft8-approval_ygdk.json`.

**Registered expectations, live in the numbers:** the 14B level is 33.6 raw / 34.7 cal, the sixth straight
registration between 33 and 35. The engine's own change since FT8 is +0.1 (A), +0.3 (B), +0.1 (C) and +0.3 (ygdk,
37.7 → 38.0): it did not move. So the tracking measure passes only if the poll's change from the FT8 target wave
(Oct 2–5, 38) to FT9's lies within 3 of those values. H2H-Y goes to ygdk unless approval prints below 36.35 (the
midpoint of 34.7 and 38.0). H2H-Z (B beats Z3) is upheld only if approval prints below 35.98. Arm D 28.5: FAIL for
any wave above 33.5. Arm E 23.8: a pass needs right direction at 28.8 or below. F2 43.9 hits the D-share bar if the
Democratic share prints 39.9 to 47.9; F-cal 37.3 only at 41.3 or below. Z1 = 38 and Z3 = 37.25 are fixed by rule
(`score_ft.py` `KNOWN_AT_PUSH[9] = w1005`).

Codex post-run review (`docs/reviews/2026-10-08-ft9-post-codex.md`): no BLOCKS; it reproduced all 11 aggregates and
the four box stamps. Four scorer and metadata findings were fixed before this push; none changed a registered number.
