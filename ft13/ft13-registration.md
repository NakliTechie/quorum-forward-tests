# Forward Test 13 — registration (2026-11-10)

**Status: REGISTRATION. Bars and claims fixed here before any FT13 forecast existed
(this section written before the emission ran); numbers and hashes stamped below after.**
Target: the first *Economist*/YouGov weekly poll to begin fielding after the public push
(expected Nov 13–16, publishing about Nov 17–18). If the push lands after that wave begins
fielding, the target is the following wave, by the same rule.

## What FT13 carries, and why

FT13 is FT12's registration re-run on a fresh mechanical anchor, the first after the Nov 3 election. Chirag's
decisions of 2026-11-09 (plan/history.md) make two changes; every other arm, map, bar and head-to-head is FT12's
(and so FT9's to FT11's):

1. **The anchor's election slot is empty.** Anchor rule 4 names "the next scheduled federal election within 12
   months of D"; from 2026-11-04 the next is 2028-11-07, so the rule yields no sentence. `quorum/twin/anchor_builder.py`
   now applies the rule mechanically (it refuses an election sentence outside the window, and still requires one
   inside it; FT12's anchor rebuilds byte for byte). The anchor is four sentences, not five (disclosure 56).
2. **The ballot arms F and F2 are scored against the House question the target poll prints.** After the election,
   YouGov printed a recalled vote ("who did you vote for", FT12's target), not an intention. A recalled vote is
   scored as FT12 scored it, with the disclosure repeated; if the target prints no House question, F and F2 are
   reported as not scorable. The ballot arms were never in the core tally, so the tally of 8 is unchanged.

- 14B arms A–D, direction arm E (`direction_dk`, s = 0.308) and ballot arms F raw / F cal, as FT12.
- The public parallel arm `ygdk` (B's map, YouGov RV frame, E35 not-sure shrink s = 0.5618), as FT12.
- Poll-only rules Z1 and Z3 as registered arms with A's topline and net bars; Z2 reported, no bar.
- Ballot arm F2 (the "Other" cap at 3.0%), a reported arm, as FT12.
- The measurement companion `ygframe`, not counted, as FT12.
- The tracking measure, scored with `--prev-ft 12`: the engine's own change since FT12's registered numbers
  against the poll's change from FT12's target wave (Nov 4–6) to FT13's. ygdk's predecessor is FT12's
  registered ygdk (37.6, `ft12/forecast-ft12-approval_ygdk.json`, passed with `--prev-ygdk`).
- The per-wave tally of 8 (raw 3 bars + calibrated 4 bars + H2H1). ygdk, Z1, Z3 and F2 are reported
  beside the tally, not in it.

Same weights, same pinned revision (`40c069824f4251a91eefaf281ebe4c544efd3e18`, through
`quorum.twin.forecast_pinned`), same prompts, same aggregation, the same Quorum-only box role and the same region
rules as FT12.

## Arms (all on the Nov 10 mechanical anchor; every calibrated or re-weighted arm a CPU transform of its raw rows)

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
2. C vs A on abstention (as FT4–12).
- **H2H-Y:** |ygdk topline err| < |B topline err|.
- **H2H-Z:** |B topline err| < |Z3 topline err| — registered expectation stamped below from the midpoint rule
  (B has beaten Z3 in 3 of 12 scored waves, `score_ft.py --benchmark-series`, FT12 verdict).
- **H2H-F2:** |F2 D-share err| < |F-cal D-share err|.

Structure bar (FT3 form) reported for A, B, C and ygdk, with a persistence column beside every
quantity. **Tracking measure** reported for A, B, C and ygdk against FT12's registered numbers and FT12's
target poll (Nov 4–6).

**Scoring.** As FT12: `score_ft.py` with `--prev-ft 12 --prev-ygdk ft12/forecast-ft12-approval_ygdk.json
--poll-rules 13 --ygdk … --ballot-f2 …`. Scored on the base as printed (RV for the last eight scored waves), disclosed.
If the target begins fielding more than 8 days after the push, the scorer needs `--gap-evidence` naming why no
wave fielded between, and records it. If it prints no House question, the ballot arms are reported `not scorable`.

## Registered expectations
- The level prior is rigid: the 14B has sat 33–35 for nine straight registrations. We register no view
  on the wave's level.
- Tracking measure: engine change within ±1.5 of zero for A, B and C, as in every registration since FT4, unless the
  four-sentence anchor itself moves the level (disclosure 56; not tested separately, so a larger change is reported,
  not explained). FAIL on any wave whose poll moves more than about 3 points from the Nov 4–6 wave (36 approve)
  while the engine stays still.
- ygdk sits ~3 points above B (FT12: 37.6 against 34.5). H2H-Y goes to ygdk unless approval prints
  below the midpoint of the two.
- H2H-Z follows the midpoint of B and Z3 (stamped below): upheld only if approval prints below it.
- Arm D: −6 to −12, FAIL. Arm E: FAIL if right direction prints near 29–30 as in FT8 and FT11; PASS if it prints
  near 22 as in FT12.
- F2 and F-cal on a recalled vote: both miss the D-share bar unless the recalled Democratic share prints within 4 of
  them (FT12: F2 −8.0, F-cal −14.6 against 52).

## Disclosures
1–35 as FT9; 39–41 as FT10 (39's pin through `forecast_pinned`); 45 and 46 as FT11; 51–54 as FT12 (the box role and
the Mumbai exclusion, the spend and relaunch bound, the checks added after FT12's pre-run review); plus:
55. **FT12's target wave has published and been scored.** The Nov 4–6 wave (3,166 RV, fielded Wed–Fri after the
   election) published Sat Nov 7; FT12 was scored against it on Nov 8 (`verdict-ft12-2026-11-08.md`: approval 36 / 62
   / 2, party D 3 / I 23 / R 75, right direction 22, recalled House vote D 52). The 14B arms take no poll input (their
   prompt is the anchor and the persona), so this reaches FT13 only through Z1 and Z3, by rule, and through the
   tracking measure's baseline. No E/YouGov wave fielded Oct 30–Nov 2; YouGov's site showed no wave newer than
   Nov 4–6 at this declaration (read 2026-11-09 IST).
56. **The anchor differs from FT12's in four ways.** (a) The date (Oct 28 → Nov 10). (b) The AAA gas price ($4.2661 →
   $4.0093, AAA "Current Avg." with "Price as of 11/9/26", read 2026-11-09 IST; the sentence prints $4.27 → $4.01).
   (c) Average hourly earnings move to the **October** vintage (3.0% → 3.1%, CES0500000003, newest month 2026-10);
   CPI-U stays at the **September** vintage (3.7%, CUUR0000SA0; the BLS API's newest CPI-U month was 2026-09 at this
   declaration). (d) **The election sentence is gone** (rule 4, above), so the anchor has four sentences. E47 found the
   anchor works as a switch (no anchor 28.6, protocol anchor 34.1, protocol + 8 sentences 34.3), but no run has
   measured removing one sentence, and the Nov 5 date finding (`capstone/date-sensitivity/`) showed one date moving the
   House margin about 2.6 points. So the size of this anchor change on the level is unknown; FT13 does not test it.
57. Pinned Wikipedia revision 1384645106 against FT12's 1382246874. The page's lead is byte-identical. Its October–
   November entries add a letter from the Vice President seeking to resume talks with Iran, small "defensive" and
   "minor" U.S. strikes on Iranian positions, new sanctions, a CENTCOM reward for information on Iran's nuclear
   programme and, on Nov 7, a CENTCOM task force widening the interdiction beyond the naval blockade. None ends the
   state of war, and "strikes and attacks have continued since" still holds, so the conflict clause is unchanged.
58. **The same anchor serves the main test's later weeks.** The UQ1 protocol fixes each study wave's anchor as the FT
   anchor registered for that week's E/YouGov target, so FT13's anchor is the anchor for UQ1 slot w1116 (its S1 origin
   and its study wave) and for the news-by-party control arm of week w1116. It is the first post-election anchor any
   of them use.
59. **The FT series lapsed for one week.** No FT13 registered when the expected Oct 30–Nov 2 wave failed to field, so
   FT12's rule carried its target to Nov 4–6. Chirag decided on Nov 9 ("yes, register FT13") to resume the series.
60. Infrastructure as FT12 (disclosure 51), with one addition: `launch_ft13.sh` reserves each attempt in an attempt log
   and refuses a third without Chirag's approval (Codex FT13 pre 4). The AWS-side reaper is still in dry run at this declaration: Chirag
   approved switching it live on Nov 9, and the switch needs his admin sign-in, which had not happened. The laptop
   guards, the boot timer and the run's own timer stand behind this run as they did behind FT12.

## Registration (2026-11-10) — numbers and hashes

Target: the first Economist/YouGov weekly poll to begin fielding after the public push (expected Nov 13–16). YouGov's
Economist/YouGov page showed no wave newer than Nov 4–6 when re-read at 07:03 IST on Nov 10, before the launch, so
`KNOWN_AT_PUSH[13] = w1106` stands.

Run: `quorum-ft13`, ap-northeast-2b g6e.xlarge (L40S:1) spot, submitted 07:05 IST through
`QUORUM_IDLE_MIN=45 bash scripts/launch_ft13.sh ft13-a1` (attempt 1 of 2 in `plan/ft13-attempts.log`; the 45-minute
idle stop leaves room for HH3 on the same box). Instance launched 07:07:04, box up 07:10, job 1 started 07:13. All four
14B raw passes banked with verified mirrors 07:20–07:28 (approval raw 07:20:14, no-anchor 07:22:22, direction 07:25:32,
ballot 07:28:48), the run manifest at 07:28:53 after the model-snapshot check; job 1 SUCCEEDED 07:29. No reclaim.
FT13's share of the box is about 0.37 h at $1.3788/h (ap-northeast-2b spot price), ≈ $0.51; the box then ran HH3
(its own record). **Cloud-side timer on the box:** cloud-init scheduled the power-off for 11:07:46 IST at first boot,
and setup logged it ("CLOUD DEADLINE from boot … MODE=poweroff"). Box checks as FT12: adapter weights `4cabea94…` and
config `563a0337…`; W161 `443ee779…` (checked on the box; the laptop's copy hashes the same, enforced by
`ft_companions.sh`); Hugging Face `main` = `40c069824f42…` before the passes ("MODEL REVISION OK"); every pass loaded
that revision through `quorum.twin.forecast_pinned`, and the snapshot check after the passes printed "MODEL SNAPSHOT
OK". The run manifest is byte-identical to FT12's (`dc17341d…`: same model, revision and adapter). Git `f0a2fbe`;
three pass manifests record `f0a2fbe…+dirty`, and the first (approval raw) records `(unknown)`: `commit_sha()` in
`quorum/twin/evidence.py` returns that when a git call raises, for example on its 5-second timeout (inferred; the
first git call on a fresh box is the likeliest to be slow; not checked). All four record the same list of **276
tracked files absent on the box, 0 edited**; the 276 are exactly the tracked files the upload rule leaves out
(`scripts/hh3_box_tree.py` rule checked on the laptop: 276 excluded, 0 absent and unexplained, 0 excluded and
present). FT12 had 268; the 8 more are files tracked since under ignored paths. The four passes were downloaded
through the S3 API (17 files), and `ft_companions.sh` verified each against its box DONE stamp (anchor, forecast,
rows, manifest hashes; 3,170 rows) before building the seven calibrated, shrunk, re-weighted or capped arms, and wrote
its acceptance record. Anchor: protocol v1, 2026-11-10, four sentences, sha256 `913c6645db67402d…`, revid
1384645106, AAA $4.0093, CPI-U September and AHE October vintage. YouGov RV frame for Y and ygframe:
`data/yg/frame_yg_rv.csv` sha256 `374860befc4ec156…` (unchanged since FT8).

**Run-to-run check on the pinned revision.** The no-anchor arm's prompts are identical to FT12's (empty anchor). Its
FT13 rows differ from FT12's by 0.62 points per answer option on average (the largest simulated person's average over
its five options is 1.59 points; the largest single option difference is 3.74 points; 43 of 3,170 identical). Its
topline moves by 0.1 (28.5 / 59.0 / 12.5 → 28.6 / 58.9 / 12.5), where FT12's repeated FT11's exactly: the LoRA serving
noise of disclosure 35.

**Approval — 14B arms, the ygdk arm, the poll-only arms and the companion**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | **Y ygdk** | Z1 | Z3 | ygframe (companion) |
|---|---|---|---|---|---|---|---|---|
| Approve | **32.7** | **33.3** | **34.5** | **28.6** | **36.7** | **36** | **38.25** | 35.0 |
| Disapprove | 55.8 | 55.2 | 59.0 | 58.9 | 57.0 | 62 | 60.0 | 53.7 |
| Net | -23.1 | -21.9 | -24.5 | -30.3 | -20.3 | -26 | -21.75 | -18.7 |
| Not sure | 11.6 | 11.6 | 6.5 | 12.5 | 6.4 | — | — | 11.4 |
| Party D/I/R | 24.4 / 31.4 / 43.0 | 10.6 / 28.0 / 63.2 | 26.1 / 33.2 / 44.6 | 23.9 / 28.7 / 33.2 | 11.4 / 29.8 / 65.8 | — | — | 10.6 / 28.2 / 63.2 |

**Direction (arm E, measurement) and House ballot (arms F, F2)**

| Quantity | E raw | **E direction_dk (s 0.308)** | F raw | F cal | **F2 cap 3.0%** |
|---|---|---|---|---|---|
| Positive (right direction / Democrat) | 18.0 | **23.2** | 34.0 | **38.8** | **45.6** |
| Negative | 52.6 | 67.7 | 35.6 | 30.9 | 35.3 |
| Not sure | 29.4 | **9.1** | 9.2 | 9.2 | 9.2 |
| Party D/I/R (positive) | 14.5 / 16.8 / 23.1 | 18.7 / 21.9 / 29.4 | 51.8 / 34.0 / 17.2 | 69.2 / 42.8 / 4.3 | 79.7 / 51.6 / 4.8 |

Forecast shas (sha256, first 12): approval_raw `ff7dc8e6de46` · approval_cal `588e6f9a1256` · approval_dk `0984b9923c68` ·
approval_noanchor `8556f4ae9efd` · approval_ygdk `42ef47988937` · approval_ygframe `551416fa61d3` · direction_raw
`a5393ae52403` · direction_dk `0eba31f5bb3b` · ballot_raw `4415c7121be3` · ballot_cal `9e332245f335` · ballot_f2
`44ff29f2f54d`.

**Registered expectations, live in the numbers:** the 14B level is 32.7 raw / 33.3 cal. Raw is below 33 for the first
time since FT3 (32.6), and calibrated is the lowest since FT3; both changes are inside the registered ±1.5. The
engine's own change since FT12 is −0.8 (A), −1.2 (B), −0.6 (C) and −0.9 (ygdk, 37.6 → 36.7). FT13 does not test
whether the four-sentence anchor (disclosure 56) caused this, so it is reported, not explained. The tracking measure
passes only if the poll's change from FT12's target wave (Nov 4–6, 36) to FT13's lies within 3 of those values: A passes
on an approval print of 33 to 38, B on 32 to 37. H2H-Y goes to ygdk only if approval prints above 35.0 (the midpoint of 33.3 and
36.7); at exactly 35 the two errors tie, and the strict rule does not uphold it. H2H-Z (B beats Z3) is upheld only if
approval prints below 35.78 (the midpoint of 33.3 and 38.25). Arm D 28.6: FAIL for any wave above 33.6. Arm E 23.2:
a pass needs right direction at 28.2 or below. F2 45.6 hits the D-share bar if the Democratic share prints 41.6 to
49.6; F-cal 38.8 only at 42.8 or below. Z1 = 36 / 62 and Z3 = 38.25 / 60.0 are fixed by rule (`score_ft.py`
`KNOWN_AT_PUSH[13] = w1106`: the Nov 4–6 wave published Sat Nov 7, before the push).
