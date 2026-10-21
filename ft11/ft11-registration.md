# Forward Test 11 — registration (2026-10-21)

**Status: REGISTRATION. Bars and claims fixed here before any FT11 forecast existed
(this section written before the emission ran); numbers and hashes stamped below after.**
Target: the first *Economist*/YouGov weekly poll to begin fielding after the public push
(expected Oct 23–26, publishing about Oct 27–28). If the push lands after that wave begins
fielding, the target is the following wave (expected Oct 30–Nov 2), by the same rule.

## What FT11 carries, and why

FT11 is FT10's registration re-run on a fresh mechanical anchor. No Chirag decision since the Oct 8 review
changes the design (plan/history.md), so every arm, map, bar and head-to-head is FT10's (and so FT9's):

- 14B arms A–D, direction arm E (`direction_dk`, s = 0.308) and ballot arms F raw / F cal, as FT10.
- The public parallel arm `ygdk` (B's map, YouGov RV frame, E35 not-sure shrink s = 0.5618), as FT10.
- Poll-only rules Z1 and Z3 as registered arms with A's topline and net bars; Z2 reported, no bar.
- Ballot arm F2 (the "Other" cap at 3.0%), a reported arm, as FT10.
- The measurement companion `ygframe`, not counted, as FT10.
- The tracking measure, scored with `--prev-ft 10`: the engine's own change since FT10's registered numbers
  against the poll's change from FT10's target wave (Oct 16–19) to FT11's. ygdk's predecessor is FT10's
  registered ygdk (37.5, `ft10/forecast-ft10-approval_ygdk.json`, passed with `--prev-ygdk`).
- The per-wave tally of 8 (raw 3 bars + calibrated 4 bars + H2H1). ygdk, Z1, Z3 and F2 are reported
  beside the tally, not in it.

**One engineering change, no design change.** FT10 pinned the model revision by adding `--revision` to
`quorum/twin/forecast.py`. That file is part of the UQ1 freeze, so the edit broke UQ1's frozen code hash (Codex
uq1-w1012 pre 1, 2026-10-15); the file is back to its frozen bytes and the pin lives in a separate entry point,
`python -m quorum.twin.forecast_pinned --revision <sha> …`, which passes every other argument to the frozen
`forecast.py` unchanged. The pinned revision is FT10's (`40c069824f4251a91eefaf281ebe4c544efd3e18`), and the box
still checks the loaded snapshot before it banks each pass. Each pass manifest now also lists every tracked file
that differs from the commit, with its sha256 (`git_dirty_files`; Codex FT10 post 2). Same weights, same prompts,
same aggregation: the change records provenance and should not move a number.

## Arms (all on the Oct 21 mechanical anchor; every calibrated or re-weighted arm a CPU transform of its raw rows)

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
2. C vs A on abstention (as FT4–10).
- **H2H-Y:** |ygdk topline err| < |B topline err|.
- **H2H-Z:** |B topline err| < |Z3 topline err| — registered expectation: **NOT upheld** (B has beaten
  Z3 in 2 of 9 scored waves).
- **H2H-F2:** |F2 D-share err| < |F-cal D-share err|.

Structure bar (FT3 form) reported for A, B, C and ygdk, with a persistence column beside every
quantity. **Tracking measure** reported for A, B, C and ygdk against FT10's registered numbers and FT10's
target poll (Oct 16–19).

**Scoring.** As FT10: `score_ft.py` with `--prev-ft 10 --prev-ygdk ft10/forecast-ft10-approval_ygdk.json
--poll-rules 11 --ygdk … --ballot-f2 …`. Scored on the base as printed (RV for the last six scored waves), disclosed.

## Registered expectations
- The level prior is rigid: the 14B has sat ~33–35 for seven straight registrations. We register no view
  on the wave's level.
- Tracking measure: engine change within ±1.5 of zero for A, B and C; FAIL on any wave whose poll moves
  more than ~4.5 points from the Oct 16–19 wave.
- ygdk sits ~3 points above B (FT10: 37.5 against 34.2). H2H-Y goes to ygdk unless approval prints
  below the midpoint of the two.
- H2H-Z is NOT upheld: Z3 beats B on the topline unless approval prints below the midpoint of B and Z3.
- Arm D: −6 to −12, FAIL. Arm E: about −6 if the direction series holds near 30 (FAIL).
- F2 hits the D-share bar if the Democratic share prints within 4 of it; F-cal misses unless the
  Democratic share prints within 4 of F-cal.

## Disclosures
1–35 as FT9; 39–41 as FT10 (39's pin now through `forecast_pinned`); plus:
42. **FT10's outcome was NOT known at this declaration.** The Oct 16–19 wave had not published when this
   protocol was written: YouGov's tracking-data page listed Oct 10–12 as its newest poll (read 2026-10-21
   22:00 IST), and no article for the Oct 16–19 wave was found. If it publishes before the public push, the
   registration section says so and Z1/Z3 use it.
43. The anchor differs from FT10's in the date, the AAA gas price ($4.3413 → $4.2644, AAA "Current Avg." as of
   10/21/26, read 2026-10-21 IST; the sentence prints $4.34 → $4.26) and CPI-U, which moves to the **September**
   vintage (3.4% → 3.7%, BLS series CUUR0000SA0, 2026-09 vs 2025-09; the BLS API's newest CPI-U month was 2026-09
   at this declaration). Average hourly earnings stay at the September vintage (3.0%; the next release is in
   November).
44. Pinned Wikipedia revision 1381293025 (2026-10-21T11:10:22Z) against FT10's 1380127824. The page's lead and its
   June-memorandum and 60-day-deadline wording are unchanged, so the conflict clause is unchanged. The newer
   revision adds: the U.S. destroying an Iranian-connected boat conducting surveillance; Iranian officials telling
   Reuters that Iran launched new strikes on tankers to keep oil prices high before the midterms; new U.S.
   sanctions on 16 individuals and 10 entities (Oct 15); CENTCOM's commander saying the naval blockade has kept at
   least $25 billion of Iranian crude off the market; Iranian officials saying Tehran prolonged talks to influence
   the midterms; and a Financial Times report that Trump opposed an Israeli offensive planned for the weekend of
   Oct 10. None changes the page's description of a state of war.
45. Engineering: the pinned entry point and `git_dirty_files` above. The launcher still refuses uncommitted
   changes under `scripts/`, `quorum/`, `infra/` and `docs/`, so the dirty files recorded should be planning
   notes only; the manifests now show it. Two checks added after Codex's pre-run review: (a) the pinned entry
   point refuses to finish a pass whose rows hold any answer distribution that is missing, negative, non-finite
   or not summing to 1 — the frozen predictor returns all zeros when no option token appears — so such a pass is
   never banked (Codex FT11 pre 1; FT10's four passes had 0 such rows of 12,680); (b) the box checks the W161
   frame against its frozen hash (`443ee779…`) before any GPU pass, the hash of the copy the laptop's CPU
   companions reload, so both paths use the same frame and weights (Codex FT11 pre 3). The laptop downloads every
   banked file through the S3 API and checks it against the box's stamps before any companion runs (Codex FT11
   pre 5).
46. Spend and relaunch as FT10: an $8.28 ceiling per launch attempt (g6e.xlarge / g6e.2xlarge spot only, capped
   at $2.76/h), one relaunch on a spot reclaim, so at most $16.56; no third attempt without Chirag. Each attempt
   writes to its own S3 folder (`runs/ft11-2026-10-21-<run name>`) and re-runs all four passes. The $8.28 figure
   is a **compute** bound that holds while the laptop guards run and AWS answers their termination calls; the
   150 GB gp3 disk (about $0.02 an hour) and data transfer are extra. **Cloud-side timers (Codex FT11 pre 2,
   confirm 1–2):** the launch passes a SkyPilot project config for this launch only
   (`infra/skypilot/ft11-boot-deadline.config.yaml`, `aws.post_provision_runcmd`), so cloud-init schedules a
   systemd shutdown 4 h after it runs; setup keeps that schedule (it adds one, 3 h 35 min ahead, only if none
   exists), every setup step has a forced-kill timeout, and the run's own 3 h timer stays. A spot instance
   terminates on shutdown. The project config reaches only this launch's request, not the shared SkyPilot server's
   environment, so other projects' boxes do not get it. **Not guaranteed:** cloud-init runs that command in its
   final stage, which is not ordered before SSH, so SkyPilot may start uploading before the timer exists; and with
   retry-until-up, if the laptop guards die while the SkyPilot server lives, SkyPilot can start replacement
   instances, each with its own timer. So there is no single cloud-side expiry for the whole launch request; each
   instance that reaches cloud-init's final stage stops within about 4 h. Closing this needs an AWS-side reaper
   (logged in `plan/pending.md`); every earlier registration ran without even the per-instance timer.
47. This registration ran by hand from the pinned Quorum chat on Wednesday evening. The 07:03 IST in-chat timer
   was lost when the app restarted (in-chat timers do not survive a restart), so FT11 is registered about 15
   hours later than FT10 was in its week; the target rule above is unchanged.

## Registration (2026-10-21) — numbers and hashes

Target: the first Economist/YouGov weekly poll to begin fielding after the public push (expected Oct 23–26).

Run: `quorum-ft11`, ap-northeast-2a g6e.xlarge (L40S:1) spot, launched 22:44 IST through `scripts/launch_ft11.sh ft11-a1`
(Chirag, 22:20 IST: launch with the laptop-failure residual of disclosure 46 disclosed); box up 22:47, job running 22:53,
all four 14B raw passes banked and the job SUCCEEDED 23:08, torn down 23:08 and terminated by 23:14 with six regions
checked empty; 0 reclaims; about 0.47 h at $1.2777/h (ap-northeast-2a spot price at launch), ≈ $0.60. **Cloud-side timer confirmed on the box:** cloud-init
scheduled the power-off for 02:46 IST (4.0 h after the 22:45:55 IST launch) before setup ran, and setup logged it and kept
it. Box checks: adapter weights `4cabea94…` and config `563a0337…` as UQ1 records; W161 `443ee779…` (the laptop's copy
hashes the same); Hugging Face `main` = `40c069824f42…` before the passes; every pass loaded that revision through
`quorum.twin.forecast_pinned` (recorded under `params.revision` in each manifest) and the loaded snapshot was checked
before each pass was banked; every pass passed the probability check (0 invalid rows of 12,680). Git `ece3852`; each
manifest records `ece3852+dirty` and, new this week, the files behind the suffix: **268 tracked files absent on the box,
0 edited** (plan 110, docs 101, data 47, `quorum/data/` 5, data-spec 3, `.python-version`, one transport manifest).
The repository's ignore rules (`/plan`, `data/` — which also matches `quorum/data/` — and two CSV folders under
`docs/`) keep them out of SkyPilot's workdir upload; the forecast imports none of them. **Correction to FT10
(inferred, Codex FT11 post 2):** FT10's `+dirty` most likely had the same cause, not only planning notes as its Codex
triage said: same launcher, same ignore rules, same workdir sync. FT10's manifests list no paths, so this is an
inference, not a record. Every pass's box stamp (anchor, forecast, rows, manifest hashes; 3,170 rows) was re-derived on the
laptop from a copy downloaded through the S3 API, not the mount, and matched. The seven calibrated, shrunk, re-weighted
or capped arms are CPU transforms of those raw rows by `scripts/ft_companions.sh`, which rebuilt FT10's seven arms byte
for byte tonight before it ran on FT11. Anchor: protocol v1, 2026-10-21, sha256 `cea062b6b0cf3715…`, revid 1381293025,
AAA $4.2644, CPI-U September vintage (3.7%), AHE September vintage (3.0%). YouGov RV frame for Y and ygframe:
`data/yg/frame_yg_rv.csv` sha256 `374860befc4ec156…` (unchanged since FT8).

**Run-to-run check on the pinned revision.** The no-anchor arm's prompts are identical to FT10's (empty anchor). Its
FT11 rows differ from FT10's by 0.6 points per answer option on average (the largest simulated person's average over
its five options is 1.65 points; the largest single option difference is 4.13 points; 37 of 3,170 identical), and its topline repeats exactly (28.5 / 59.0 / 12.5): the LoRA serving noise of disclosure 35, through the
new entry point.

**Approval — 14B arms, the ygdk arm, the poll-only arms and the companion**

| Quantity | A raw | B cal | C raw+dk | D no-anchor | **Y ygdk** | Z1 | Z3 | ygframe (companion) |
|---|---|---|---|---|---|---|---|---|
| Approve | **33.4** | **34.2** | **34.9** | **28.5** | **37.3** | **38** | **36.75** | 35.9 |
| Disapprove | 56.7 | 55.8 | 59.4 | 59.0 | 57.2 | 61 | 61.25 | 54.4 |
| Net | -23.3 | -21.6 | -24.5 | -30.5 | -19.9 | -23 | -24.5 | -18.5 |
| Not sure | 10.0 | 10.0 | 5.6 | 12.5 | 5.5 | — | — | 9.7 |
| Party D/I/R | 25.3 / 32.1 / 43.4 | 11.6 / 29.0 / 63.9 | 26.8 / 33.7 / 44.8 | 23.8 / 28.7 / 33.1 | 12.3 / 30.6 / 66.0 | — | — | 11.6 / 29.2 / 64.0 |

**Direction (arm E, measurement) and House ballot (arms F, F2)**

| Quantity | E raw | **E direction_dk (s 0.308)** | F raw | F cal | **F2 cap 3.0%** |
|---|---|---|---|---|---|
| Positive (right direction / Democrat) | 18.4 | **23.6** | 33.4 | **37.5** | **44.1** |
| Negative | 52.6 | 67.5 | 36.0 | 32.0 | 36.8 |
| Not sure | 29.0 | **8.9** | 9.5 | 9.5 | 9.5 |
| Party D/I/R (positive) | 14.9 / 16.9 / 24.0 | 19.1 / 21.9 / 30.2 | 51.7 / 32.3 / 17.4 | 69.3 / 39.1 / 4.5 | 79.7 / 47.4 / 5.0 |

Forecast shas (sha256, first 12): approval_raw `ff02a5d566db` · approval_cal `ccd222482844` · approval_dk `0bf19ff51973` ·
approval_noanchor `d84ed2e094bb` · approval_ygdk `0c606cc428d1` · approval_ygframe `22f1585d7567` · direction_raw
`7e2622e0b48e` · direction_dk `8a9f57c977a1` · ballot_raw `554976986de4` · ballot_cal `11324a312fb4` · ballot_f2
`e98b69edc2e4`.

**Registered expectations, live in the numbers:** the 14B level is 33.4 raw / 34.2 cal, the eighth straight
registration between 33 and 35. The engine's own change since FT10 is +0.1 (A), 0.0 (B), 0.0 (C) and −0.2 (ygdk,
37.5 → 37.3): it did not move. So the tracking measure passes only if the poll's change from FT10's target wave
(Oct 16–19) to FT11's lies within 3 of those values. H2H-Y goes to ygdk unless approval prints below 35.75 (the midpoint
of 34.2 and 37.3). H2H-Z (B beats Z3) is upheld only if approval prints below 35.48. Arm D 28.5: FAIL for any wave above
33.5. Arm E 23.6: a pass needs right direction at 28.6 or below. F2 44.1 hits the D-share bar if the Democratic share
prints 40.1 to 48.1; F-cal 37.5 only at 41.5 or below. Z1 = 38 / 61 and Z3 = 36.75 / 61.25 are fixed by rule
(`score_ft.py` `KNOWN_AT_PUSH[11] = w1012`: the Oct 16–19 wave had not published at the push; YouGov's tracking page
re-read 2026-10-21 23:2x IST listed Oct 10–12 as its newest poll; FT10's Z1/Z3 recomputed by the same function give its
registered 38 / 37.25).
