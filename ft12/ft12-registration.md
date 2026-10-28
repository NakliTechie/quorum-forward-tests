# Forward Test 12 — registration (2026-10-28)

**Status: REGISTRATION. Bars and claims fixed here before any FT12 forecast existed
(this section written before the emission ran); numbers and hashes stamped below after.**
Target: the first *Economist*/YouGov weekly poll to begin fielding after the public push
(expected Oct 30–Nov 2, publishing about Nov 3–4). If the push lands after that wave begins
fielding, the target is the following wave (expected Nov 6–9), by the same rule.

## What FT12 carries, and why

FT12 is FT11's registration re-run on a fresh mechanical anchor. No Chirag decision since the Oct 8 review
changes the design (plan/history.md), so every arm, map, bar and head-to-head is FT11's (and so FT9's and FT10's):

- 14B arms A–D, direction arm E (`direction_dk`, s = 0.308) and ballot arms F raw / F cal, as FT11.
- The public parallel arm `ygdk` (B's map, YouGov RV frame, E35 not-sure shrink s = 0.5618), as FT11.
- Poll-only rules Z1 and Z3 as registered arms with A's topline and net bars; Z2 reported, no bar.
- Ballot arm F2 (the "Other" cap at 3.0%), a reported arm, as FT11.
- The measurement companion `ygframe`, not counted, as FT11.
- The tracking measure, scored with `--prev-ft 11`: the engine's own change since FT11's registered numbers
  against the poll's change from FT11's target wave (Oct 23–26) to FT12's. ygdk's predecessor is FT11's
  registered ygdk (37.3, `ft11/forecast-ft11-approval_ygdk.json`, passed with `--prev-ygdk`).
- The per-wave tally of 8 (raw 3 bars + calibrated 4 bars + H2H1). ygdk, Z1, Z3 and F2 are reported
  beside the tally, not in it.

**No design change; two infrastructure changes.** (1) The box runs under a Quorum-only AWS role (`quorum-box`, set by
SkyPilot's `aws.remote_identity` in `scripts/launch_guarded.sh`) instead of SkyPilot's shared `skypilot-v1`; it can use
only the Quorum bucket and cannot start instances. (2) No Quorum box may run in AWS Mumbai (Chirag, 2026-10-25); the
task file's region list already excluded it, and the launcher now refuses any task file that names Mumbai or no
region. Same weights, same pinned revision (`40c069824f4251a91eefaf281ebe4c544efd3e18`, through
`quorum.twin.forecast_pinned`), same prompts, same aggregation: neither change should move a number.

## Arms (all on the Oct 28 mechanical anchor; every calibrated or re-weighted arm a CPU transform of its raw rows)

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
2. C vs A on abstention (as FT4–11).
- **H2H-Y:** |ygdk topline err| < |B topline err|.
- **H2H-Z:** |B topline err| < |Z3 topline err| — registered expectation: **NOT upheld** (B has beaten
  Z3 in 2 of 10 scored waves, `score_ft.py --benchmark-series` read 2026-10-28 IST).
- **H2H-F2:** |F2 D-share err| < |F-cal D-share err|.

Structure bar (FT3 form) reported for A, B, C and ygdk, with a persistence column beside every
quantity. **Tracking measure** reported for A, B, C and ygdk against FT11's registered numbers and FT11's
target poll (Oct 23–26).

**Scoring.** As FT11: `score_ft.py` with `--prev-ft 11 --prev-ygdk ft11/forecast-ft11-approval_ygdk.json
--poll-rules 12 --ygdk … --ballot-f2 …`. Scored on the base as printed (RV for the last seven scored waves), disclosed.

## Registered expectations
- The level prior is rigid: the 14B has sat ~33–35 for eight straight registrations. We register no view
  on the wave's level.
- Tracking measure: engine change within ±1.5 of zero for A, B and C; FAIL on any wave whose poll moves
  more than ~4.5 points from the Oct 23–26 wave (39 approve).
- ygdk sits ~3 points above B (FT11: 37.3 against 34.2). H2H-Y goes to ygdk unless approval prints
  below the midpoint of the two.
- H2H-Z is NOT upheld: Z3 beats B on the topline unless approval prints below the midpoint of B and Z3.
- Arm D: −6 to −12, FAIL. Arm E: about −6 if the direction series holds near 30 (FAIL).
- F2 hits the D-share bar if the Democratic share prints within 4 of it; F-cal misses unless the
  Democratic share prints within 4 of F-cal.

## Disclosures
1–35 as FT9; 39–41 as FT10 (39's pin through `forecast_pinned`); 45 and 46 as FT11 (the pinned entry point, the
probability check, the W161 hash check, S3-API downloads; the per-launch boot timer); plus:
48. **FT11's target wave HAS published before this declaration, so its approval and direction are known; its
   House-ballot table is not.** The Oct 23–26 wave (1,440 RV) was posted at about 00:34–00:46 IST today (PDF
   Last-Modified Tue Oct 27 19:04–19:16 UTC). Claude read its approval table (table 44: 39 approve / 58 disapprove /
   2 not sure; party D 4 / I 27 / R 81) and direction table (table 1: right direction 29) at about 07:10 IST for the
   E52-F score (`15b44b5`), both weekly-core tables that UQ1 never forecasts. The House-ballot table (12, "2026
   Congressional Vote") is a UQ1 study item and stays unread until the UQ1 w1026 forecasts are pushed, so FT11's
   ballot outcome was unknown here. The 14B arms take no poll input (their prompt is the anchor and the persona), so
   the known approval reaches FT12 only through Z1 and Z3, by rule. Chirag (2026-10-27): "Typically we do that after
   the yougov piece comes out", so this registration waited for the poll.
49. The anchor differs from FT11's in the date and the AAA gas price ($4.2644 → $4.2661, AAA "Current Avg." as of
   10/27/26, read 2026-10-28 IST; the sentence prints $4.26 → $4.27). CPI-U stays at the **September** vintage (3.7%,
   BLS series CUUR0000SA0; the BLS API's newest CPI-U month was 2026-09 at this declaration) and average hourly
   earnings at September (3.0%, CES0500000003, newest month 2026-09).
50. Pinned Wikipedia revision 1382246874 (2026-10-27T15:07:23Z) against FT11's 1381293025. The page's lead is
   byte-identical, and its June-memorandum and 60-day-deadline entries are unchanged, so the conflict clause is
   unchanged. The newer revision is shorter (436,305 → 399,534 characters of wikitext; older entries condensed or
   removed) and adds one Iran item in October: U.S. sanctions on a Panama- and Greece-based law firm said to have
   facilitated Iran's shadow fleet. Nothing in it changes the page's description of a state of war.
51. Infrastructure (above): the `quorum-box` role and the Mumbai exclusion, both tested on Oct 27 by a box-role smoke
   test (a t3.small in Seoul printed `IDENTITY SMOKE PASSED` and terminated itself through SkyPilot's autostop
   before its laptop deadline; `docs/reviews/2026-10-27-aws-reaper-no-mumbai-install-post-codex.md`). The launcher
   also starts an output watcher on the run's S3 folder (alerts on no first output in 75 min or no growth in 30 min)
   and waits for it before submitting. The AWS-side reaper (a Lambda every 10 minutes that terminates any
   `quorum=true` instance past its `quorum-deadline` tag) was installed on Oct 27 in dry run, which logs and does
   not terminate; switching it live is Chirag's step and was not confirmed at this declaration. The laptop guards,
   the boot timer and the run's own timer stand behind this run as they did behind FT11.
52. Spend and relaunch as FT11: an $8.28 bound per launch attempt (g6e.xlarge / g6e.2xlarge spot only, capped at
   $2.76/h), one relaunch on a spot reclaim, so $16.56 for two attempts; no third attempt without Chirag. Each attempt
   writes to its own S3 folder (`runs/ft12-2026-10-28-<run name>`) and re-runs all four passes. FT11 cost about $0.60
   (0.47 h at $1.28/h), about $0.15 per raw pass. **As in FT11, the $8.28 figure is a compute bound that holds while
   the laptop guards run and AWS answers their termination calls**; the 150 GB gp3 disk (about $0.02 an hour) and
   data transfer are extra. The launch retries until a box is up, so if the laptop guards die while the SkyPilot server
   lives, SkyPilot can start replacement instances; each carries the boot timer (power-off 4 h after cloud-init's final
   stage) and the request's `quorum-deadline` tag, but with the AWS-side reaper still in dry run (disclosure 51) there
   is no cloud-side terminator for the whole request, so the per-attempt bound is not guaranteed without the laptop
   (Codex FT12 pre 6).
54. Checks added after Codex's pre-run review (`docs/reviews/2026-10-28-ft12-pre-codex.md`), before any FT12 forecast:
   (a) `score_ft.py` gains FT12's poll-only cutoff (`KNOWN_AT_PUSH[12] = w1026`), so Z1 and Z3 are scorable;
   (b) the companions refuse to run unless the local W161 and YouGov RV frames match their frozen hashes and every raw
   pass matches the box's DONE stamp (anchor, forecast, rows, manifest hashes; 3,170 rows), checked on the copy
   downloaded through the S3 API — FT11's seven companions rebuilt byte for byte through the new checks; (c) the
   watchdog sends a desktop and phone alert when a job fails, is cancelled or is preempted, and the output watcher
   reports FAILED (with alerts) if the box disappears before all four passes are banked; (d) the scorer's target check
   uses the confirmed push time and refuses a later wave when an earlier one began after the push. None touches the
   forecast path.
53. This registration runs from the pinned Quorum chat's 07:03 IST in-chat timer, on the morning the target of FT11
   published.

## Registration (2026-10-28) — numbers and hashes

Target: the first Economist/YouGov weekly poll to begin fielding after the public push (expected Oct 30–Nov 2).

Run: `quorum-ft12`, ap-northeast-2a g6e.xlarge (L40S:1) spot, submitted 07:24 IST through `scripts/launch_ft12.sh ft12-a1`
(a first submission at 07:19 refused before launching anything: the new output watcher could not list the empty run
folder; fixed in `4c03db9`, no spend). Instance launched 07:25:53, box up 07:29, all four 14B raw passes banked with
verified mirrors 07:38–07:46, the run manifest mirrored after the model-snapshot check. **AWS reclaimed the spot
instance at 07:47:28 IST** ("Service initiated"), after everything was banked, so no relaunch was needed; the output
watcher closed with "4 of 4 passes banked", and an EC2 sweep of the six Quorum regions found no instance and no open
spot request. About 0.36 h at $1.3555/h (ap-northeast-2a spot price), ≈ $0.49. **Cloud-side timer on the box:**
cloud-init scheduled the power-off for 11:26 IST before setup ran, and setup logged it and kept it. Box checks as
FT11: adapter weights `4cabea94…` and config `563a0337…`; W161 `443ee779…` (checked on the box; the laptop's copy
hashes the same, now enforced by `ft_companions.sh`); Hugging Face `main` = `40c069824f42…` before the passes; every
pass loaded that revision through `quorum.twin.forecast_pinned` and passed the probability check. Git `4c03db9`; each
manifest records `4c03db9+dirty` with **268 tracked files absent on the box, 0 edited** (the ignore rules keep `plan/`
and `data/` out of the workdir upload, as FT11). The four passes were downloaded through the S3 API (17 files), and
`ft_companions.sh` verified each against its box DONE stamp (anchor, forecast, rows, manifest hashes; 3,170 rows)
before building the seven calibrated, shrunk, re-weighted or capped arms. Anchor: protocol v1, 2026-10-28, sha256
`1a280c1591c502cb…`, revid 1382246874, AAA $4.2661, CPI-U and AHE September vintage. YouGov RV frame for Y and
ygframe: `data/yg/frame_yg_rv.csv` sha256 `374860befc4ec156…` (unchanged since FT8).

**Run-to-run check on the pinned revision.** The no-anchor arm's prompts are identical to FT11's (empty anchor). Its
FT12 rows differ from FT11's by 0.63 points per answer option on average (the largest simulated person's average over
its five options is 1.89 points; the largest single option difference is 4.46 points; 31 of 3,170 identical), and its
topline repeats exactly (28.5 / 59.0 / 12.5): the LoRA serving noise of disclosure 35.

**Approval — 14B arms, the ygdk arm, the poll-only arms and the companion**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | **Y ygdk** | Z1 | Z3 | ygframe (companion) |
|---|---|---|---|---|---|---|---|---|
| Approve | **33.5** | **34.5** | **35.1** | **28.5** | **37.6** | **39** | **38.75** | 36.2 |
| Disapprove | 56.5 | 55.6 | 59.3 | 59.0 | 56.8 | 58 | 59.5 | 54.0 |
| Net | -23.0 | -21.1 | -24.2 | -30.5 | -19.2 | -19 | -20.75 | -17.8 |
| Not sure | 10.0 | 10.0 | 5.6 | 12.5 | 5.5 | — | — | 9.8 |
| Party D/I/R | 25.2 / 32.3 / 43.7 | 11.5 / 29.5 / 64.3 | 26.8 / 33.8 / 45.1 | 23.8 / 28.7 / 33.1 | 12.2 / 31.2 / 66.4 | — | — | 11.5 / 29.7 / 64.4 |

**Direction (arm E, measurement) and House ballot (arms F, F2)**

| Quantity | E raw | **E direction_dk (s 0.308)** | F raw | F cal | **F2 cap 3.0%** |
|---|---|---|---|---|---|
| Positive (right direction / Democrat) | 18.5 | **23.7** | 33.4 | **37.4** | **44.0** |
| Negative | 52.5 | 67.4 | 36.0 | 32.1 | 36.9 |
| Not sure | 29.0 | **8.9** | 9.5 | 9.5 | 9.5 |
| Party D/I/R (positive) | 15.0 / 16.9 / 24.1 | 19.3 / 21.9 / 30.3 | 51.5 / 32.3 / 17.4 | 69.1 / 38.9 / 4.5 | 79.5 / 47.1 / 5.0 |

Forecast shas (sha256, first 12): approval_raw `3a66615a98f7` · approval_cal `bcc7e0dc45aa` · approval_dk `35ff8bf765e9` ·
approval_noanchor `8723736fc7ad` · approval_ygdk `e4a238567951` · approval_ygframe `32f98d9ff02f` · direction_raw
`df1ccf56abf5` · direction_dk `34d5e406179d` · ballot_raw `086dc285dee5` · ballot_cal `49393aaa3f9d` · ballot_f2
`5ed213e21067`.

**Registered expectations, live in the numbers:** the 14B level is 33.5 raw / 34.5 cal, the ninth straight
registration between 33 and 35. The engine's own change since FT11 is +0.1 (A), +0.3 (B), +0.2 (C) and +0.3 (ygdk,
37.3 → 37.6): it did not move. So the tracking measure passes only if the poll's change from FT11's target wave
(Oct 23–26, 39) to FT12's lies within 3 of those values. H2H-Y goes to ygdk unless approval prints below 36.05 (the
midpoint of 34.5 and 37.6). H2H-Z (B beats Z3) is upheld only if approval prints below 36.63. Arm D 28.5: FAIL for any
wave above 33.5. Arm E 23.7: a pass needs right direction at 28.7 or below. F2 44.0 hits the D-share bar if the
Democratic share prints 40.0 to 48.0; F-cal 37.4 only at 41.4 or below. Z1 = 39 / 58 and Z3 = 38.75 / 59.5 are fixed
by rule (`score_ft.py` `KNOWN_AT_PUSH[12] = w1026`: the Oct 23–26 wave published Wed Oct 28 00:34 IST, before the push).
