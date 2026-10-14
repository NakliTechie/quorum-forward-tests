# Forward Test 10 — registration (2026-10-14)

**Status: REGISTRATION. Bars and claims fixed here before any FT10 forecast existed
(this section written before the emission ran); numbers and hashes stamped below after.**
Target: the first *Economist*/YouGov weekly poll to begin fielding after the public push
(expected Oct 16–19, publishing ~Oct 20). If the push lands after that wave begins
fielding, the target is the following wave (expected Oct 23–26), by the same rule.

## What FT10 carries, and why

FT10 is FT9's registration re-run on a fresh mechanical anchor. No Chirag decision since the Oct 8 review
changes the design (plan/history.md), so every arm, map, bar and head-to-head is FT9's:

- 14B arms A–D, direction arm E (`direction_dk`, s = 0.308) and ballot arms F raw / F cal, as FT9.
- The public parallel arm `ygdk` (B's map, YouGov RV frame, E35 not-sure shrink s = 0.5618), as FT9.
- Poll-only rules Z1 and Z3 as registered arms with A's topline and net bars; Z2 reported, no bar.
- Ballot arm F2 (the "Other" cap at 3.0%), a reported arm, as FT9.
- The measurement companion `ygframe`, not counted, as FT9.
- The tracking measure, scored with `--prev-ft 9`: the engine's own change since FT9's registered numbers
  against the poll's change from FT9's target wave (Oct 9–12) to FT10's. ygdk's predecessor is FT9's
  registered ygdk (38.0, `ft9/forecast-ft9-approval_ygdk.json`, passed with `--prev-ygdk`).
- The per-wave tally of 8 (raw 3 bars + calibrated 4 bars + H2H1). ygdk, Z1, Z3 and F2 are reported
  beside the tally, not in it.

**One engineering change, no design change.** Every GPU pass now loads Qwen/Qwen3-14B at the pinned revision
`40c069824f4251a91eefaf281ebe4c544efd3e18` (`forecast.py --revision`), and the box checks the loaded snapshot
before it banks each pass. Codex asked for this in FT9's second confirmation; FT9 logged it for FT10 so FT9's
command shape stayed equal to FT1–FT8's. The weights are the same ones FT1–FT9 loaded (Hugging Face `main` is
that revision), so the change guards provenance and should not move a number.

## Arms (all on the Oct 14 mechanical anchor; every calibrated or re-weighted arm a CPU transform of its raw rows)

| Arm | Method | Bars |
|---|---|---|
| A 14B raw | frozen FT method | topline ±5 · net ±8 · 9-cell ≤6 |
| B 14B cal | Platt `approval_pooled_2019_2025` (3.6133, 1.3759) | A's bars + party MAE ≤12 (registered) |
| C 14B raw+dk | E35 shrink s = 0.5618 | A's bars; H2H2 (NS err < A's AND topline not worse by >0.3) |
| D 14B no-anchor | empty anchor | A's bars — **registered expectation: topline FAILS** |
| **Y ygdk** | B's map, YouGov RV frame (`build_yg_frame.py --rv`), E35 shrink 0.5618 | topline ±5 · net ±8 (9-cell and party reported) |
| **Z1** | the last E/YouGov topline published before the push (stamped below) | topline ±5 · net ±8 |
| **Z3** | the mean of the last four published before the push (stamped below) | topline ±5 · net ±8 |
| E direction_dk | 14B direction raw, dk-shrink s = 0.308 (frozen 09-10) | right-direction ±5 — **measurement** |
| F ballot raw / cal | `HOUSE_BALLOT_NS` (2.7534, 0.4401) | D-share ±4, margin ±4; cal party ≤12 |
| **F2 ballot cap** | F-cal + "Other" capped at 3.0% | D-share ±4, margin ±4, party ≤12 |

Head-to-heads, all two-sided, reported at equal volume either way:
1. B party MAE < A party MAE (series continuity; in the tally).
2. C vs A on abstention (as FT4–9).
- **H2H-Y:** |ygdk topline err| < |B topline err|.
- **H2H-Z:** |B topline err| < |Z3 topline err| — registered expectation: **NOT upheld** (B has beaten
  Z3 in 2 of 8 scored waves).
- **H2H-F2:** |F2 D-share err| < |F-cal D-share err|.

Structure bar (FT3 form) reported for A, B, C and ygdk, with a persistence column beside every
quantity. **Tracking measure** reported for A, B, C and ygdk against FT9's registered numbers and FT9's
target poll (Oct 9–12).

**Scoring.** As FT9: `score_ft.py` with `--prev-ft 9 --prev-ygdk ft9/forecast-ft9-approval_ygdk.json
--poll-rules 10 --ygdk … --ballot-f2 …`. Scored on the base as printed (RV for the last five scored waves), disclosed.

## Registered expectations
- The level prior is rigid: the 14B has sat ~33–35 for six straight registrations. We register no view
  on the wave's level.
- Tracking measure: engine change within ±1.5 of zero for A, B and C; FAIL on any wave whose poll moves
  more than ~4.5 points from the Oct 9–12 wave.
- ygdk sits ~3 points above B (FT9: 38.0 against 34.7). H2H-Y goes to ygdk unless approval prints
  below the midpoint of the two.
- H2H-Z is NOT upheld: Z3 beats B on the topline unless approval prints below the midpoint of B and Z3.
- Arm D: −6 to −12, FAIL. Arm E: about −6 if the direction series holds near 30 (FAIL).
- F2 hits the D-share bar if the Democratic share prints within 4 of it; F-cal misses unless the
  Democratic share prints within 4 of F-cal.

## Disclosures
1–35 as FT9, plus:
36. **FT9's outcome was NOT known at this declaration.** The Oct 9–12 wave had not published when this
   protocol was written: YouGov's approval tracker's newest point was Oct 5 (read 2026-10-14 07:05 IST), and
   no article for that wave was listed. If it publishes before the public push, the registration section
   says so.
37. The anchor differs from FT9's in the date and the AAA gas price ($4.3612 → $4.3413, AAA "Current Avg."
   as of 10/13/26, read 2026-10-14 IST; the sentence prints $4.36 → $4.34). CPI-U stays at the **August**
   vintage: the BLS API's newest CPI-U month was 2026-08 at this declaration (September CPI publishes
   mid-October). Average hourly earnings stay at the September vintage (published Oct 2; the next release
   is in November).
38. Pinned Wikipedia revision 1380127824 (2026-10-13T23:30:25Z) against FT9's 1379188592. The page's lead and
   its June-memorandum and 60-day-deadline wording are unchanged, so the conflict clause is unchanged. The
   newer revision adds: the Pentagon told to be ready in case direct operations against Iran resume, with
   Trump saying strikes would not renew before the Nov 3 midterms (Oct 7–8); new sanctions on Iran's
   shadow fleet (Oct 8); Trump saying the war will "be over soon, one way or the other"; the U.S. military
   disabling a cargo ship that tried to run its naval blockade of Iran (Oct 11); and Trump saying the U.S.
   would "make a decision on Iran very soon" (Oct 13). None changes the page's description of a state of war.
39. The model revision is pinned in every pass and the loaded snapshot is checked before each pass is
   banked (above). The box also keeps FT9's checks: Hugging Face `main` must equal the pinned revision before
   any GPU pass, the adapter's weights and config must hash to UQ1's recorded values (`4cabea94…`,
   `563a0337…`), and `run_manifest.json` records the snapshot.
40. Spend and relaunch as FT9: an $8.28 ceiling per launch attempt (g6e.xlarge / g6e.2xlarge spot only,
   capped at $2.76/h), one relaunch on a spot reclaim, so at most $16.56; no third attempt without Chirag.
   Each attempt writes to its own S3 folder (`runs/ft10-2026-10-14-<run name>`) and re-runs all four passes.
   The ceiling assumes the laptop guards run (teardown at 2.5 h, direct EC2 termination at 2.75 h, both with
   forced kills on hung calls). If the laptop dies, the box's own timer stops it 3 h after its run starts, and
   setup is time-bounded at about 30 min, so the worst case per attempt is about 3.5 h, or $9.66 (Codex FT10 pre 1).
41. This registration ran from an in-chat timer in the Quorum working session (the app scheduler was
   retired for Quorum on 2026-10-11 after it stopped firing), on Wednesday, not Tuesday.

## Registration (2026-10-14) — numbers and hashes

Target: the first Economist/YouGov weekly poll to begin fielding after the public push (expected Oct 16–19).

Run: `quorum-ft10`, ap-northeast-2b g6e.xlarge (L40S:1) spot, launched 07:16 IST through `scripts/launch_ft10.sh ft10-a1`;
box up 07:21, job running 07:27, all four 14B raw passes banked by 07:41, torn down 07:42 with six regions checked empty;
0 reclaims. Box checks: adapter weights `4cabea94…` and config `563a0337…` as UQ1 records; Hugging Face `main` =
`40c069824f42…` before the passes; every pass loaded that revision (`--revision`, recorded in each pass's manifest) and
the loaded snapshot was checked before each pass was banked; `run_manifest.json` records the only cached snapshot. Git
`3e7cecd`; each pass's manifest records `3e7cecd+dirty`. At launch the only uncommitted changes were planning notes under
`plan/` (three deleted summaries and edits to the pending, history and workplan notes); the launcher refuses any
uncommitted change under `scripts/`, `quorum/`, `infra/` or `docs/`, and that check passed at 07:15 IST. The manifests
do not list the dirty paths themselves; recording them is logged for FT11 (Codex FT10 post 2). Every pass's box stamp (anchor, forecast, rows, manifest hashes; 3,170 rows) was re-derived on the laptop
from the downloaded S3 copy and matched. Every calibrated, shrunk, re-weighted or capped arm is a CPU transform of those
raw rows, by the commands that rebuilt FT9's seven such arms byte for byte this morning. Anchor: protocol v1,
2026-10-14, sha256 `a4a6a9aba1f03471…`, revid 1380127824, AAA $4.3413, AHE September vintage, CPI-U August vintage.
YouGov RV frame for Y and ygframe: `data/yg/frame_yg_rv.csv` sha256 `374860befc4ec156…` (unchanged since FT8); final
weighted shares after the RV filter D 32.94 / I 22.89 / R 35.66 / none 8.51.

**Run-to-run check on the pinned revision.** The no-anchor arm's prompts are identical to FT9's (empty anchor). Its
FT10 rows differ from FT9's by 1.2 points per simulated person on average (largest 3.7; 38 of 3,170 identical), and its
topline repeats exactly (28.5 / 59.0 / 12.5). That is the run-to-run noise disclosure 35 describes for LoRA serving,
so pinning the revision did not move the engine.

**Approval — 14B arms, the ygdk arm, the poll-only arms and the companion**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | **Y ygdk** | Z1 | Z3 | ygframe (companion) |
|---|---|---|---|---|---|---|---|---|
| Approve | **33.3** | **34.2** | **34.9** | **28.5** | **37.5** | **38** | **37.25** | 36.0 |
| Disapprove | 56.5 | 55.6 | 59.3 | 59.0 | 56.9 | 60 | 60.5 | 54.0 |
| Net | -23.2 | -21.4 | -24.4 | -30.5 | -19.4 | -22 | -23.25 | -18.0 |
| Not sure | 10.2 | 10.2 | 5.7 | 12.5 | 5.6 | — | — | 10.0 |
| Party D/I/R | 25.2 / 32.1 / 43.4 | 11.5 / 29.0 / 64.3 | 26.8 / 33.6 / 45.0 | 23.8 / 28.7 / 33.0 | 12.1 / 30.7 / 66.5 | — | — | 11.5 / 29.2 / 64.3 |

**Direction (arm E, measurement) and House ballot (arms F, F2)**

| Quantity | E raw | **E direction_dk (s 0.308)** | F raw | F cal | **F2 cap 3.0%** |
|---|---|---|---|---|---|
| Positive (right direction / Democrat) | 18.7 | **23.9** | 33.5 | **37.5** | **44.2** |
| Negative | 52.3 | 67.2 | 36.0 | 31.9 | 36.7 |
| Not sure | 29.0 | **8.9** | 9.6 | 9.6 | 9.6 |
| Party D/I/R (positive) | 15.2 / 17.1 / 24.1 | 19.6 / 22.2 / 30.4 | 51.7 / 32.3 / 17.6 | 69.3 / 39.2 / 4.6 | 79.6 / 47.5 / 5.2 |

Forecast shas (sha256, first 12): approval_raw `eb33cfcd3696` · approval_cal `caf5123a509b` · approval_dk `93481434b086` ·
approval_noanchor `e16fd110e158` · approval_ygdk `e66ae4cb45d3` · approval_ygframe `c6c6f6eddcce` · direction_raw
`6585fffd6fe4` · direction_dk `71cd4a4acb8f` · ballot_raw `a2299531554c` · ballot_cal `6c3cdbefdb2c` · ballot_f2
`3f68f39d0337`.

**Registered expectations, live in the numbers:** the 14B level is 33.3 raw / 34.2 cal, the seventh straight
registration between 33 and 35. The engine's own change since FT9 is −0.3 (A), −0.5 (B), −0.2 (C) and −0.5 (ygdk,
38.0 → 37.5): it did not move. So the tracking measure passes only if the poll's change from FT9's target wave (Oct 9–12)
to FT10's lies within 3 of those values. H2H-Y goes to ygdk unless approval prints below 35.85 (the midpoint of 34.2 and
37.5). H2H-Z (B beats Z3) is upheld only if approval prints below 35.73. Arm D 28.5: FAIL for any wave above 33.5.
Arm E 23.9: a pass needs right direction at 28.9 or below. F2 44.2 hits the D-share bar if the Democratic share prints
40.2 to 48.2; F-cal 37.5 only at 41.5 or below. Z1 = 38 and Z3 = 37.25 are fixed by rule (`score_ft.py`
`KNOWN_AT_PUSH[10] = w1005`: the Oct 9–12 wave had not published at the push; re-checked immediately before it).
