# Forward Test 14 — registration (2026-11-18)

**Status: REGISTRATION. Bars and claims fixed here before any FT14 forecast existed
(this section written before the emission ran); numbers and hashes stamped below after.**
Target: the first *Economist*/YouGov weekly poll to begin fielding after the public push
(expected about Nov 20–23, publishing about Nov 24–25). If the push lands after that wave begins
fielding, the target is the following wave, by the same rule.

## What FT14 carries, and why

FT14 is FT13's registration re-run on a fresh mechanical anchor dated Nov 18. It is the weekly forward test under
Chirag's standing autopilot (2026-09-24), resumed on 2026-11-09 with FT13. Nothing in the method changes: every
arm, map, bar, head-to-head and scoring rule is FT13's (and so FT12's), including FT13's two post-election rules
(the anchor's election slot is empty by rule 4; the ballot arms are scored against the House question the target
prints, or reported not scorable).

- 14B arms A–D, direction arm E (`direction_dk`, s = 0.308) and ballot arms F raw / F cal, as FT13.
- The public parallel arm `ygdk` (B's map, YouGov RV frame, E35 not-sure shrink s = 0.5618), as FT13.
- Poll-only rules Z1 and Z3 as registered arms with A's topline and net bars; Z2 reported, no bar.
- Ballot arm F2 (the "Other" cap at 3.0%), a reported arm, as FT13.
- The measurement companion `ygframe`, not counted, as FT13.
- The tracking measure, scored with `--prev-ft 13`: the engine's own change since FT13's registered numbers
  against the poll's change from FT13's target wave (Nov 13–16) to FT14's. ygdk's predecessor is FT13's
  registered ygdk (36.7, `ft13/forecast-ft13-approval_ygdk.json`, passed with `--prev-ygdk`).
- The per-wave tally of 8 (raw 3 bars + calibrated 4 bars + H2H1). ygdk, Z1, Z3 and F2 are reported
  beside the tally, not in it.

Same weights, same pinned revision (`40c069824f4251a91eefaf281ebe4c544efd3e18`, through
`quorum.twin.forecast_pinned`), same prompts, same aggregation, the same Quorum-only box role and the same region
rules as FT13.

## Arms (all on the Nov 18 mechanical anchor; every calibrated or re-weighted arm a CPU transform of its raw rows)

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
| F ballot raw / cal | `HOUSE_BALLOT_NS` (2.7534, 0.4401) | D-share ±4, margin ±4; cal party ≤12 — on the House question printed |
| **F2 ballot cap** | F-cal + "Other" capped at 3.0% | D-share ±4, margin ±4, party ≤12 — on the House question printed |

Head-to-heads, all two-sided, reported at equal volume either way:
1. B party MAE < A party MAE (series continuity; in the tally).
2. C vs A on abstention (as FT4–13).
- **H2H-Y:** |ygdk topline err| < |B topline err|.
- **H2H-Z:** |B topline err| < |Z3 topline err| — registered expectation stamped below from the midpoint rule
  (B has beaten Z3 in 3 of 12 scored waves, `score_ft.py --benchmark-series`, FT12 verdict; FT13 is not yet scored).
- **H2H-F2:** |F2 D-share err| < |F-cal D-share err|.

Structure bar (FT3 form) reported for A, B, C and ygdk, with a persistence column beside every
quantity. **Tracking measure** reported for A, B, C and ygdk against FT13's registered numbers and FT13's
target poll (Nov 13–16).

**Scoring.** As FT13: `score_ft.py` with `--prev-ft 13 --prev-ygdk ft13/forecast-ft13-approval_ygdk.json
--poll-rules 14 --ygdk … --ballot-f2 …`. Scored on the base as printed, disclosed (disclosure 63: the two waves
after FT13's push printed their headline tables on U.S. citizens, not registered voters). If the target begins
fielding more than 8 days after the push, the scorer needs `--gap-evidence` naming why no wave fielded between,
and records it. If it prints no House question, the ballot arms are reported `not scorable`.

## Registered expectations
- The level prior is rigid. FT13 registered 32.7 raw / 33.3 calibrated, the lowest since FT3. We register no view
  on the wave's level.
- Tracking measure: engine change within ±1.5 of zero for A, B and C, as in every registration since FT4. The
  anchor changes only in its date, its gas price ($4.01 → $3.78) and its Wikipedia revision (disclosure 62).
  FAIL on any wave whose poll moves more than about 3 points from the Nov 13–16 wave (35 approve) while the engine
  stays still.
- ygdk sits about 3 points above B (FT13: 36.7 against 33.3). H2H-Y goes to ygdk unless approval prints below the
  midpoint of the two.
- H2H-Z follows the midpoint of B and Z3 (stamped below): upheld only if approval prints below it.
- Arm D: −6 to −12, FAIL. Arm E: PASS if right direction prints near 21 as in the two waves since FT13's push
  (21 and 21); FAIL if it moves back near 29–30 as in FT8 and FT11.
- F2 and F-cal: we register no view. FT12's target printed a recalled vote; FT13's target has not been scored.

## Disclosures
1–35 as FT9; 39–41 as FT10 (39's pin through `forecast_pinned`); 45 and 46 as FT11; 51–54 as FT12; 57, 58 and 60
as FT13 (58 now names FT14's anchor as the anchor for UQ1 slot w1123); plus:
61. **Two waves published after FT13's push, and FT13 is not yet scored.** The Nov 9–11 wave (1,685 U.S. citizens)
   began fielding on FT13's push day (Nov 9, US Eastern), so by `score_ft.py`'s strict-after rule it is not FT13's
   target; no registration aimed at it. The Nov 13–16 wave (1,628 U.S. citizens) began four days after the push and
   is FT13's target. FT13's verdict waits for the UQ1 study forecast on the same wave to be pushed (R16 order: its
   House-ballot table is a UQ1-eligible item and stays unread until then). So FT14 is declared before FT13's
   verdict. The 14B arms take no poll input; the two waves reach FT14 only through Z1 and Z3, by rule, and through
   the tracking measure's baseline.
62. **The anchor differs from FT13's in three ways.** (a) The date (Nov 10 → Nov 18). (b) The AAA gas price
   ($4.0093 → $3.7818, AAA "Current Avg." with "Price as of 11/17/26", read 2026-11-18 IST; the sentence prints
   $4.01 → $3.78). (c) The pinned Wikipedia revision (1384645106 → 1386344048). Its changes in the conflict
   entries: sanctions on eight Canadian money-services firms (a spelling fix), a Nov 9 evacuation of U.S. military
   aircraft from RAF Mildenhall after a reported Iranian threat, the relocation of the Treasury Secretary over
   threats, and Nov 16 reports of possible Iranian attack plans against officials, which Iran dismissed. None ends
   the state of war, and "strikes and attacks have continued since" still holds, so the conflict clause is
   unchanged. CPI-U stays at the September vintage (3.7%) and average hourly earnings at the October vintage
   (3.1%): the BLS API's newest months on 2026-11-18. The election slot stays empty (next federal election
   2028-11-07). The anchor rebuilds offline byte for byte.
63. **The printed base changed.** The Nov 9–11 and Nov 13–16 toplines print "U.S. Citizens" (the last eight scored
   waves printed registered voters). FT13's rule "scored on the base as printed" applies, so FT13 and FT14 are
   scored against the citizens base when that is what prints. The ygdk arm keeps its registered-voter frame
   (registered method, unchanged); the mismatch is disclosed, not repaired.
64. **One week had no session.** No Quorum session ran from the evening of Nov 10 to Nov 17. The E52-F forecast for
   the Nov 13–16 wave (timer Fri Nov 13) never ran, so that week is lost to E52-F. Nothing in FT13 or FT14 depends on
   it.
65. **What was read before this declaration.** For the waves ledger I read the Nov 9–11 wave's approval and
   direction tables (32 / 63 approve / disapprove; party approve D 4 / I 18 / R 75; right direction 21) and the
   Nov 13–16 toplines' approval and direction questions (35 / 61; right direction 21). While printing the Nov 9–11
   approval table I also saw the first lines of the next table (Trump approval on foreign policy). The Nov 9–11
   wave is not a UQ1 study wave (slot w1109 is filled by the Nov 4–6 wave under R16). No other table of the
   Nov 13–16 wave was read; its tab report was not published at declaration.
66. Infrastructure as FT13 (disclosures 51 and 60), with `launch_ft14.sh` copied from `launch_ft13.sh` (two attempts at
   most, the third needs Chirag). The AWS-side reaper is still in dry run: Chirag's admin sign-in has not happened.
   The laptop guards, the boot timer and the run's own timer stand behind this run as they did behind FT13.

## Registration (2026-11-18) — numbers and hashes

Target: the first Economist/YouGov weekly poll to begin fielding after the public push (expected about Nov 20–23).
At declaration the newest published wave was Nov 13–16 (toplines created Tue Nov 17 19:48 IST), so
`KNOWN_AT_PUSH[14] = w1116` stands.

Run: `quorum-ft14`, us-west-2b g6e.xlarge (L40S:1) spot, submitted 07:13 IST through `bash scripts/launch_ft14.sh ft14-a1`
(attempt 1 of 2 in `plan/ft14-attempts.log`). The request waited 24 minutes for spot capacity (placement scores 1 of
10 in Seoul, Spain, Oregon and Ohio at 07:39 IST). Instance `i-0409c9c4c11b016a0` launched 07:37:02, job 1 started
07:44. All four 14B raw passes banked with verified mirrors 07:50–07:58 (approval raw 07:50:14, no-anchor 07:52:15,
direction 07:55:13, ballot 07:58:19), the run manifest at 07:58:20; job 1 SUCCEEDED 07:58. No reclaim. I terminated
the box at 07:59:19 IST after the S3-API download: about 0.37 h at $1.861/h (us-west-2b spot price), ≈ $0.69. The run
manifest is byte-identical to FT12's and FT13's (`dc17341d…`: same model, pinned revision and adapter). I did not
fetch the box's setup log before teardown, so this stamp does not quote its boot-deadline and model-check lines;
the launcher passed the boot-deadline config, and every pass manifest records the pinned revision.

**Three tracked files were edited on the box.** All four pass manifests record `8617199…+dirty` with 276 tracked
files absent (exactly the upload rule's list: 276 excluded, 0 unexplained, 0 excluded and present) and three files
edited: `scripts/method_ledger.py`, `docs/ledger/waves.json` and `docs/ledger/README.md`. They are my fixes for Codex's
FT14 pre-run findings, written in the working tree while the launch waited for capacity; SkyPilot uploads the
workdir only when the box is up (07:37), after the launcher's clean-tree check (07:13). Each edited file hashes to
its version committed in `18de2dd`. No pass reads them: the emission runs `quorum.twin.forecast_pinned` on the
anchor, the frame and the adapter, and none of the three is in that path. The forecasts are unaffected; the record
is disclosed.

The four passes were downloaded through the S3 API (17 files), and `ft_companions.sh` verified each against its box
DONE stamp (anchor, forecast, rows, manifest hashes; 3,170 rows) before building the seven calibrated, shrunk,
re-weighted or capped arms, and wrote its acceptance record. Anchor: protocol v1, 2026-11-18, four sentences, sha256
`0d5c45cb59fa76e2…`, revid 1386344048, AAA $3.7818, CPI-U September and AHE October vintage. YouGov RV frame for Y and
ygframe: `data/yg/frame_yg_rv.csv` sha256 `374860befc4ec156…` (unchanged since FT8).

**Run-to-run check on the pinned revision.** The no-anchor arm's prompts are identical to FT13's. Its FT14 rows differ
from FT13's by 0.62 points per answer option on average (largest simulated person's average 1.65; largest single
option difference 4.13; 32 of 3,170 identical). Its topline moves by 0.1 (28.6 / 58.9 / 12.5 → 28.5 / 59.0 / 12.5):
the LoRA serving noise of disclosure 35.

**Approval — 14B arms, the ygdk arm, the poll-only arms and the companion**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | **Y ygdk** | Z1 | Z3 | ygframe (companion) |
|---|---|---|---|---|---|---|---|---|
| Approve | **32.9** | **33.6** | **34.6** | **28.5** | **37.0** | **35** | **35.5** | 35.4 |
| Disapprove | 55.8 | 55.0 | 59.0 | 59.0 | 56.6 | 61 | 61.0 | 53.4 |
| Net | -22.9 | -21.4 | -24.4 | -30.5 | -19.6 | -26 | -25.5 | -18.0 |
| Not sure | 11.4 | 11.4 | 6.4 | 12.5 | 6.3 | — | — | 11.2 |
| Party D/I/R | 24.3 / 31.6 / 43.4 | 10.4 / 28.3 / 64.2 | 26.0 / 33.4 / 45.1 | 23.8 / 28.7 / 33.1 | 11.1 / 30.1 / 66.8 | — | — | 10.4 / 28.5 / 64.3 |

**Direction (arm E, measurement) and House ballot (arms F, F2)**

| Quantity | E raw | **E direction_dk (s 0.308)** | F raw | F cal | **F2 cap 3.0%** |
|---|---|---|---|---|---|
| Positive (right direction / Democrat) | 18.2 | **23.4** | 34.1 | **38.9** | **45.7** |
| Negative | 52.5 | 67.6 | 35.7 | 30.9 | 35.3 |
| Not sure | 29.3 | **9.0** | 9.2 | 9.2 | 9.2 |
| Party D/I/R (positive) | 14.6 / 17.0 / 23.5 | 18.8 / 22.0 / 29.8 | 52.0 / 34.1 / 17.1 | 69.4 / 43.0 / 4.3 | 79.8 / 51.8 / 4.7 |

Forecast shas (sha256, first 12): approval_raw `baaec20be086` · approval_cal `27d808cf9377` · approval_dk `9012d5473b6e` ·
approval_noanchor `0da8bc3a8715` · approval_ygdk `e9f4c83f8484` · approval_ygframe `998dd72dd558` · direction_raw
`b477a2059bb4` · direction_dk `6f270a3c7493` · ballot_raw `e37c7e246e70` · ballot_cal `4b3a0c952f74` · ballot_f2
`8fb021fc656c`.

**Registered expectations, live in the numbers:** the 14B level is 32.9 raw / 33.6 cal. The engine's own change since
FT13 is +0.2 (A), +0.3 (B), +0.1 (C) and +0.3 (ygdk, 36.7 → 37.0), inside the registered ±1.5. The tracking measure
passes only if the poll's change from FT13's target wave (Nov 13–16, 35) to FT14's lies within 3 of those values: A
and B pass on an approval print of 33 to 38. H2H-Y goes to ygdk only if approval prints above 35.3 (the midpoint of
33.6 and 37.0). H2H-Z (B beats Z3) is upheld only if approval prints below 34.55 (the midpoint of 33.6 and 35.5).
Arm D 28.5: FAIL for any wave above 33.5. Arm E 23.4: a pass needs right direction at 28.4 or below. F2 45.7 hits the
D-share bar if the Democratic share prints 41.7 to 49.7; F-cal 38.9 only at 42.9 or below. Z1 = 35 / 61 and Z3 = 35.5 /
61.0 are fixed by rule (`score_ft.py` `KNOWN_AT_PUSH[14] = w1116`).
