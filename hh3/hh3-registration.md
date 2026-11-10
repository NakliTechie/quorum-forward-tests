# HH3 — Harvard CAPS/Harris Registration, November 2026

**Status: REGISTRATION 2026-11-10 (Chirag 2026-11-09: "Register HH3 (Harvard CAPS/Harris November)", plan/history.md
decision 5 of that night). Written as a draft on 2026-11-09 before any HH3 number existed; the method, bars, rules,
expectations and disclosures above the stamps are unchanged from that draft. Numbers and hashes are stamped below
after the emission passed acceptance, and the registration takes effect at its public push.**
Target: **the first Harvard CAPS/Harris poll to begin fielding after HH3's public push** (order-based, as HH1 and
HH2). The last wave fielded October 24–26, 2026. At 2026-11-09 22:00 IST harvardharrispoll.com listed "October 2026"
as its latest poll. In 2025 they fielded November 4–6 and December 2–4 (`docs/harvard-harris-recon.md`), so the
November 2026 poll can field this week. If the push lands after November's
fieldwork starts, the rule moves the target to the next poll to begin fielding after the push, expected in December.
The deck's printed field dates decide which wave is the target.

## What changed since HH2 (decided before any HH3 number exists)

Chirag decided on 2026-11-09 to register HH3 as a re-run of HH2's frozen method. Five decisions follow.

1. **A fresh anchor, shared with FT13.** HH3 uses FT13's mechanical anchor, `data/forward/ft13/anchor-ft13.txt`
   (dated 2026-11-10, sha256 `913c6645db67402d199b023c1d9afaf0b4cb881b54bf1b143acd64084c5e1a26`). HH2 built its own
   anchor dated its registration day. HH3 registers on the same day as FT13, under the same anchor rules. The builder
   makes one anchor from one date and one facts file, so a second build for November 10 would repeat FT13's reads and
   give the same bytes. The anchor has four sentences, not five. Anchor rule 4 names "the next scheduled federal
   election within 12 months" of the date; after November 3 the next is 2028-11-07, so the rule gives no sentence.
2. **The benchmark "same as last month's poll" is fixed now from the October 24–26 wave**: approve 39, net −20,
   right track 31, Democrat share 52, party approve 9 / 27 / 77. Every number comes from
   `quorum-forward-tests/hh2/published-2026-10-24-26.json`. It is reported beside every arm and is not a claim.
3. **direction_dk's don't-know target is the October wave's published right-track don't know, 10.0.** The rule is
   HH2's: solve the shrink *s* on the unrounded aggregate so the don't-know share equals the previous wave's printed
   number. October printed 10 (the Oct 26 point of the p.4 trend chart), as September did.
4. **The ballot arms are kept and scored against the House question the poll prints.** The November poll comes after
   the November 3 election. It may print a recalled House vote, an intention for a later election, or no House
   question. Chirag decided for FT13 on 2026-11-09 to keep the ballot arms, score them against the House question
   printed, disclose that, and report them as not scorable if none prints. HH3 applies the same decision through
   the ballot scoring rule below, fixed before emission so that no choice is left once the answers are known.
5. **Everything else is HH2's frozen method, unchanged**: engine, frame, instruments, Platt maps, bars, head-to-head,
   the don't-know solve on the unrounded aggregate, the builder's acceptance checks and the retry policy. HH3 adds
   provenance and timing checks around that method (disclosure 11 and the Emission entry); they change no number.

## Ballot scoring rule (registered before emission)

The rule reads the target wave's key-results deck. It reads the
topline document only when the key-results deck prints no qualifying question.

1. **Qualifying question.** A question qualifies when it asks about the U.S. House or Congress and prints a Democratic
   row and a Republican row. Questions about the President, the Senate, governors or named candidates do not qualify.
2. **Question order.** Score the first of: (a) a recalled vote in the November 3, 2026 House or congressional
   election; (b) an intention for a future House or congressional election; (c) none.
3. **Base order.** Within the chosen question, score the base the deck uses for its headline toplines (registered
   voters). When the question is not printed on that base, score the first base the deck prints for it.
4. **Tie-break.** When more than one table qualifies at the same step, score the first in the deck's page order.
5. **Share.** Democrat share = Democratic row ÷ (Democratic row + Republican row) × 100. Our ballot instrument is a
   two-row forced choice, so other rows (other, did not vote, not sure) leave the share. When the two rows sum to 100,
   the share is the Democratic row.
6. **Missing.** When no question qualifies, ballot_raw and ballot_cal are reported as not scorable, and the tally is
   out of 8.

The verdict names the document, page, question and base it scored.

## Registered arms and bars

| Arm | Built as | Bars |
|---|---|---|
| approval_raw | frozen FT-series engine, soft first-token, M3ALT wording | approve ±5 · net ±8 |
| direction_raw | same engine, M1 wording | right track ±5 |
| ballot_raw | same engine, CON2026B two-row forced choice | Democrat share ±4, on the question the ballot scoring rule picks |
| approval_cal | Platt on the conditional approve share, `approval_pooled_2019_2025` (a 3.6133, b 1.3759) | approve ±5 · net ±8 · party MAE ≤ 12 |
| direction_dk | E35-form abstain-shrink, *s* solved so aggregate DK = 10.0 (the October wave's published right-track DK) | right track ±5 |
| ballot_cal | Platt `HOUSE_BALLOT_NS` (a 2.7534, b 0.4401) on the two-row share | Democrat share ±4, on the question the ballot scoring rule picks |

**Head-to-head claim:** approval_cal party MAE < approval_raw party MAE (party = Dem / Ind / Rep approve, as
printed by Harvard-Harris; IND/OTH entered as Ind).

**Tally:** 10 claims (the nine bars above and the head-to-head), or 8 when no question qualifies under the
ballot scoring rule.

**Benchmark, reported beside every arm (not scored as a claim):** "same as last month's poll", fixed now from
the October 24–26 wave: approve 39, net −20, right track 31, Democrat share 52, party approve 9 / 27 / 77.

## Registered expectations (from HH2's verdict)

HH2's verdict (`quorum-forward-tests/hh2/verdict-hh2-2026-10-28.md`) states what the method does on this house. We
register these expectations from it, before any HH3 number exists:

1. approval_cal hits approve (±5) and party (MAE ≤ 12). HH1-B hit with 0.0 and MAE 1.47; HH2 hit with +2.2 and 6.27.
2. The head-to-head is upheld. HH2: calibrated party MAE 6.27 against raw 18.9.
3. approval_cal's net is at risk. HH2 missed it by 8.7, because the engine's don't know (6.4) sat above the poll's (3)
   and pulled disapproval under the poll's. HH3 adds no don't-know repair for approval; that would be a new arm.
4. direction_raw fails. Its don't-know share ran near 30 against a printed 10 in HH1 and HH2.
5. direction_dk hits right track (±5) if the poll prints its don't know near 10. HH2: −4.0. We register no view if
   the printed don't know moves far from 10.
6. On an intention question, ballot_cal hits and ballot_raw misses, as in HH2 (+1.4 and −4.8). On a recalled vote we
   register no view: FT12's YouGov ballot arms missed a recalled vote by 14.6 (calibrated) and 18.6 (raw) points on
   Democrat share (`quorum-forward-tests/verdict-ft12-2026-11-08.md`).
7. We register no view on how far the four-sentence anchor moves the engine's level (FT13 disclosure 56).

## Method (frozen at registration)

- Engine: the frozen FT-series / HH1 / HH2 method, Qwen3-14B at revision 40c069824f4251a91eefaf281ebe4c544efd3e18 +
  the FT adapter (eval-adapters/14b, adapter_model.safetensors sha `4cabea94…59b8e5`, adapter_config.json sha
  `563a0337…3282bb`) served as LoRA, soft first-token. As in HH2, the job loads the snapshot at that revision by path
  and checks the adapter hashes before any prompt. The five inference source files hash the same as in HH2's run
  (`quorum/twin/forecast.py` `38609cbe…`, `predict.py` `d415df3a…`, `instruments.py` `6c66dabf…`, `compression.py`
  `0f5e8bfc…`, `evidence.py` `84938adb…`). The run manifest records revision, adapter hashes, package versions, GPU,
  commit, attempt and these source hashes.
- Frame: the W161 adult frame (all adults in Pew ATP wave 161; no registered-voter filter) reweighted to
  Harvard-Harris's printed standing party composition (Dem 33 / Rep 35 / Ind 28 / Other 3); other margins keep W161's
  weights. `scripts/build_hh_frame.py`, frame sha `6653915b47277578d2170c275c57699fe6538e93d347cd5ba990d112a2bd5743`
  (the same file as `quorum-forward-tests/hh1/frame_hh.csv` and `hh2/frame_hh.csv`; 3,170 profiles). It is an adult
  frame scored against registered-voter, likely-voter or voter bases (disclosure 12).
- Instruments: `hh_approval`, `hh_direction`, `hh_generic_ballot` (wording verbatim from their decks: M3ALT,
  M1, CON2026B), unchanged since HH1.
- Era anchor: FT13's, from the mechanical builder (`quorum.twin.anchor_builder`, protocol v1), date 2026-11-10; facts
  in `data/forward/ft13/anchor-facts.json` (AAA $4.0093 "Price as of 11/9/26", read 2026-11-09 IST; Wikipedia "2026
  in the United States" revision 1384645106; BLS CPI-U September 3.7%, average hourly earnings October 3.1%).
  Conflict clause unchanged from FT8's. No election sentence (rule 4, decision 1). Anchor sha256
  `913c6645db67402d199b023c1d9afaf0b4cb881b54bf1b143acd64084c5e1a26`. `anchor_builder --no-network` rebuilt it from
  the facts file byte for byte on 2026-11-09. No polling numbers.
- Emission: one GPU job (3 instruments × HH frame; HH2's took about 5 minutes per instrument),
  `infra/skypilot/quorum-hh3.exec.yaml`, run as job 2 on FT13's registration box (quorum-ft13, L40S spot).
  **Submission is sequential only.** HH3 is submitted through `scripts/launch_hh3_exec.sh` and nothing else, and only
  after FT13's job 1 has ended as SUCCEEDED with no other job pending or running. `sky exec` copies the laptop's
  workdir to the box at submission, so this order means the copy cannot change files under a running FT13 job.
  The launcher reserves the attempt under a lock in `plan/hh3-attempts.log` (retry policy below). It refuses to
  submit, and releases the reservation, unless all of these hold:
  - nothing the workdir upload carries differs from HEAD (`scripts/hh3_box_tree.py --mode laptop`), and HEAD is
    pushed; that HEAD becomes the emission commit;
  - both staged inputs match the registered shas, and the attempt's S3 folder is empty;
  - the earliest laptop-side deadline for the box (FT13's teardown at +2.5 h or hard termination at +2.75 h, read
    from their armed guard logs) is at least 65 minutes away: a 30-minute model step, three instruments of about
    5 minutes and a 20-minute margin;
  - FT13 was accepted locally first. Its four passes, downloaded through the S3 API, match their box DONE stamps; its
    seven companions exist (`scripts/ft_companions.sh` ran); and its S3 objects match that accepted copy.

  **FT13's registered numbers come from the copy accepted before HH3 ran.** The launcher keeps FT13's S3 listing
  (every key with size, ETag and last-modified time) in `plan/hh3-<attempt>-ft13-before.json`. After HH3,
  `bash scripts/launch_hh3_exec.sh --verify-ft13 <attempt>` lists FT13's folder again and refuses if any object
  changed, vanished or was added. The box role can write anywhere in the bucket, so this check replaces a write lock.

  The launcher passes that deadline to the job. The job refuses before any prompt when any of these happens:
  - an input sha differs from the registered frame or anchor;
  - the box's git head is not the emission commit;
  - the box's workdir fails the FT method (`scripts/hh3_box_tree.py --mode box`): any edited tracked file, any
    untracked file outside `hh3-in/`, `results-hh3-<attempt>/` and FT13's `results/`, or any absent tracked file
    that the upload's ignore rule does not leave out (disclosure 13);
  - fewer than 60 minutes remain at start, or fewer than 30 after the model step, before the earliest of that
    deadline and the box's own power-off timers;
  - the model snapshot at the pinned revision is still incomplete after a fetch of at most 30 minutes;
  - an adapter hash differs, or the attempt's S3 folder already exists.

  Outputs go to `s3://sky-quorum-artifacts-615809814090/runs/hh3-registration/<attempt>/`, each instrument saved
  there as soon as it finishes. After the last instrument the job runs the workdir check again (`box-tree-after.json`,
  hashed with the outputs). It requires the same absences as before, writes `SHA256SUMS.box`, and reads every file
  back through the S3 mount. Only after all of these pass does it write the completion marker `HH3-DONE`: the
  sha256 of `SHA256SUMS.box`, the absent count, 0 edited, 0 untracked outside, the attempt and the commit.
- Monitoring: before submission the launcher starts an HH3 output watcher on the attempt's S3 folder
  (`infra/skypilot/s3_progress_watch.sh`, its own log `plan/s3watch-quorum-ft13-hh3-<attempt>.log`). The watcher
  counts the run complete only when `HH3-DONE` exists. After submission the launcher registers a delegation whose
  probe follows HH3's own job id.
- Calibrated arms are CPU transforms of the same rows: `scripts/build_hh2.py --registration hh3`. Before any
  transform it refuses an emission in which any of these fails (HH2's checks, plus the commit and source checks):
  - frame, anchor, instrument text and raw status match the registration;
  - the manifests match it (model revision, adapter, stub off);
  - the run manifest's commit and the box's git head equal the emission commit given with `--emission-commit`, and
    every instrument manifest's commit is that commit, bare or marked `+dirty`;
  - the box's workdir passed the FT method before and after the emission with the same absences, so a `+dirty`
    mark can come only from absences the upload explains and from the allowed outputs (disclosure 13);
  - `HH3-DONE` exists and names this `SHA256SUMS.box`, this commit and the recorded absent count;
  - the inference source hashes on the box and in the checkout equal the five registered hashes in the Engine entry;
  - every frame profile appears exactly once, with the frame's weight and valid probabilities;
  - each forecast file equals the aggregate recomputed from its rows;
  - no profile gives an option exactly 0.
  A refusal is a failed attempt under the retry policy below.
- **Retry policy (declared before emission).** Attempt `a1`. If the box is lost, the job fails, the job refuses on
  the box, or acceptance fails, HH3 reruns once in full as `a2`. The `a2` box is set up as FT13's (the same setup and
  mounts): FT13's own relaunch if FT13 also needs one, or else the next Quorum box that serves the same base model
  and add-on. `a2` runs only if the November poll has not begun fielding by then. The launcher enforces the order:
  - `a1` first; once its submission has started it stays counted, even if the submission then fails;
  - `a2` only after a line recording `a1`'s failure (`bash scripts/launch_hh3_exec.sh --record-failure a1
    "<reason>"`), and never after an `a1` with no recorded failure;
  - nothing after `a2`: a second failure stops and returns to Chirag.

  `a2` goes through the same launcher (with `--cluster` and `--prior-job` for its box) and the same checks. All three
  instruments run again, never mixing attempts. The registered numbers are those of the first attempt that completes
  all three and passes acceptance. No attempt is chosen by its numbers.
- Don't-know solve: on the unrounded aggregate, *s* recorded at full precision, as in HH2.
- Scoring: a committed scorer written from the bars above (as `scripts/score_hh2.py` for HH2), with the ballot
  scoring rule above.

## Disclosures

1. Frame hybrid, surrogate validation, no publisher microdata: as HH1 disclosures 1, 3 and 4.
1b. **Independents are not the same population on both sides.** Harvard-Harris prints IND/OTH (independents and
   others together); our frame's Ind cell holds independents only (others stay in the topline, out of the party
   cut). HH1 and HH2 compared them the same way; the frozen cut is kept and the mismatch disclosed.
2. direction_dk's *s* is solved on the October wave's published don't know (10%). It is the only October number
   that enters a forecast, and it targets the abstain share, not the right-track level. Disclosed as in-sample for
   don't know.
3. **Run-to-run variation.** This engine, served with the adapter as LoRA, does not repeat bit for bit. On 2026-10-04
   each simulated person's probability moved by about 1 point between identical runs, and group totals by up to
   about 0.3 points (`docs/uq1/determinism-probe-round1.md`). On 2026-10-29, two identical runs on two boxes differed
   by a median 1.3 points calibrated (largest 3.5) and 0.5 raw (largest 1.1), on a 67-cell frame
   (`docs/news-prejudice/design.md`). The cause is vLLM 0.8.5's LoRA kernel; a merged checkpoint removes it. HH3
   keeps the registered engine so HH1, HH2 and HH3 compare directly. HH3 runs on a different box from HH2, so any
   change from HH2's numbers includes this noise. The registered numbers are the ones emitted; no rerun is selected.
4. HH2 verdict context: HH2 scored 7 of 10 on the October 24–26 wave. It missed raw right track (−9.9), raw ballot
   (−4.8) and calibrated net (+8.7). Carrying September's poll forward beat the calibrated approval arm on net and
   party, and beat raw right track and raw ballot (`quorum-forward-tests/hh2/verdict-hh2-2026-10-28.md`). HH1 scored
   5 of 8.
5. **The anchor differs from HH2's in six ways.** (a) The date: October 6 → November 10. (b) The AAA gas price:
   $4.3653 → $4.0093 (the sentence prints $4.37 → $4.01). (c) CPI-U moves from the August vintage (3.4%) to the
   September vintage (3.7%). (d) Average hourly earnings move from the September vintage (3.0%) to the October vintage
   (3.1%). (e) The sentence "The 2026 midterm congressional elections are in November." is gone (rule 4). (f) The
   Wikipedia revision moves from 1378680367 to 1384645106; the conflict clause is unchanged (FT13 disclosure 57). No
   run has measured the effect of removing one sentence, so the size of this change on the level is unknown.
6. **The same anchor serves other registrations.** It is FT13's anchor, and also the anchor for UQ1 slot w1116 (FT13
   disclosure 58). HH3 and FT13 are separate registrations, scored against different polls by different scorers.
7. **The ballot question after the election.** HH3's ballot instrument asks an intention for "the congressional
   election", unchanged since HH1, while the anchor no longer names an election. The November poll can print a
   recalled vote, an intention for a later election, or no House question. HH3 scores whatever House question prints
   (decision 4 and the ballot scoring rule). A recalled vote measures something different from an intention (FT12 verdict, point 4).
8. **The October ballot base.** October printed the generic ballot among likely voters (52 / 48). HH3 forecasts on
   the adult frame (disclosure 12), as HH2 did. The benchmark's Democrat share (52) is that likely-voter number. The
   November ballot is scored on the base the ballot scoring rule picks, and the verdict names it.
9. **Target timing.** Harvard-Harris has fielded soon after past elections (target section above). If November's
   fieldwork begins before HH3's push, the target is the next wave to begin fielding after the push, by rule. No
   November number existed or was read when this draft was written (2026-11-09).
10. **The emission runs on a different box from HH2's.** HH2 ran as job 3 on the UQ1 double-smoke box; HH3 runs as
   job 2 on FT13's box. Both boxes install from `infra/requirements-gpu-stageb.txt` (HH2's run recorded vllm 0.8.5,
   torch 2.6.0, transformers 4.51.3), mount the same adapter folder and load the same snapshot by path. HH3's job sets
   `VLLM_USE_V1=1`, as HH2's job did, and records it in the run manifest. FT13's passes download the snapshot through
   `quorum.twin.forecast_pinned`, so HH3's job checks every snapshot file and fetches any missing file at the pinned
   revision. FT13 and HH3 run one after the other on that box, never at the same time.
11. **The builder is parameterised, not copied.** `scripts/build_hh2.py --registration hh3` applies HH3's constants:
   anchor sha, the anchor's file name in the emission manifests, the don't-know target and its source, and the arm
   names. With the changed script, HH2's six forecasts rebuild byte for byte from the public `hh2/` folder (checked
   2026-11-09; `tests/test_build_hh3.py`). In HH3 mode it also requires the emission commit, the registered
   source hashes, the box workdir records and `HH3-DONE`; HH2's checks are unchanged.
12. **The frame is an adult frame; the printed bases are narrower.** `frame_hh.csv` holds all W161 adults, reweighted
   to Harvard-Harris's party targets; `scripts/build_hh_frame.py` applies no registered-voter filter (HH1 disclosure
   1). Harvard-Harris prints its toplines among registered voters. October printed the ballot among likely voters,
   and a recalled vote covers only people who voted. So every arm forecasts a wider population than the one it is
   scored against, and the gap is widest for the ballot. The frame is frozen since HH1; HH3 keeps it and discloses
   the mismatch.
13. **Tracked files are absent on the box, by the upload's rule.** SkyPilot's workdir upload uses `.gitignore` as an
   rsync exclude list and does not honour its `!` re-include lines. So it leaves out every tracked file matched by
   those patterns with the `!` lines dropped, including `plan/` and some `docs/` and `data-spec/` CSV files that git
   itself does not ignore. FT12's box recorded 268 tracked files absent and 0 edited; this rule names exactly those
   268 (`tests/test_build_hh3.py`). HH3 counts its absences the same way and accepts only absences the rule
   explains. FT12's four passes and HH2's emission ran under the same upload rule, so the emission does not need the
   absent files; the transforms run on the laptop from the full checkout.

## Registration-day checklist

1. Anchor: FT13's (its launcher checks the sha against the manifest). Stage `frame_hh.csv` and `anchor-ft13.txt` to
   `s3://sky-quorum-artifacts-615809814090/context/hh3/`; the job checks both shas on the box.
2. FT13's acceptance first: download FT13's four passes through the S3 API and run `scripts/ft_companions.sh` on them.
3. Codex pre-run review; emission by `bash scripts/launch_hh3_exec.sh a1 --ft13-run <FT13 run name> --ft13-dir
   <FT13 download> --ft13-out <FT13 companions>`, run after FT13's job 1 ends as SUCCEEDED and within FT13's
   20-minute idle autostop (the launcher refuses otherwise); Codex post-run review.
4. After the job: `bash scripts/launch_hh3_exec.sh --verify-ft13 a1` (FT13's objects unchanged). Laptop acceptance:
   fresh S3 download of the attempt folder, `sha256sum -c SHA256SUMS.box`, then `scripts/build_hh2.py --registration
   hh3 --emission-commit <the commit the launcher printed>` (its provenance checks must pass). Stamp that commit
   below. Any failure is recorded with `--record-failure a1 "<reason>"` before `a2`.
5. Stamp every forecast sha below; drop DRAFT.
6. Public repo `hh3/`, committed and pushed before fielding:
   - this doc and the six forecasts (`forecast-hh3-*.json`);
   - the emission rows (`rows.jsonl`), per-instrument manifests, run manifest, `box-tree-after.json`, `HH3-DONE` and
     logs (scanned for secrets first), with `SHA256SUMS.box`;
   - the anchor, its manifest and its facts file (rebuilds offline to the same sha);
   - the frame (the same file as hh1 and hh2);
   - the code at the registration commit that reruns the transforms and checks the emission: `scripts/build_hh2.py`,
     `scripts/build_hh1b.py`, `scripts/dk_shrink.py` and `quorum/twin/` `forecast.py`, `instruments.py`,
     `compression.py`, `evidence.py`, `predict.py`, `anchor_builder.py`, with the package versions from the run manifest;
   - `SHA256SUMS.hh3` entries, and tracking rows with calibrated and raw arms on separate rows.

## Registration stamps — numbers and hashes, stamped after the run

- **Emission: attempt `a2`, job 3 on `quorum-ft13`** (AWS ap-northeast-2b, g6e.xlarge L40S spot), submitted 07:42 IST,
  SUCCEEDED 07:51 IST; code commit `f0a2fbe678e1ef656ca66400ffedbf4a606dd5f9` (box git head the same); revision
  `40c069824f4251a91eefaf281ebe4c544efd3e18`; adapter `4cabea94…` / `563a0337…`; vllm 0.8.5, torch 2.6.0,
  transformers 4.51.3, `VLLM_USE_V1=1`; GPU `NVIDIA L40S, 580.159.04`. It ran after FT13's job 1 (SUCCEEDED 07:29),
  never beside it. FT13's 22 S3 objects matched FT13's laptop acceptance copy before submission and again after the
  job (`--verify-ft13 a2`). The box was terminated at 07:52 IST; box time 07:07–07:52 for FT13 and HH3 together, about
  0.76 h at $1.3788/h, ≈ $1.04.
- **Attempt `a1` failed before any forecast (job 2, 07:37 IST, refused in 3 seconds).** The box tree check found one
  untracked file, `.claude/settings.local.json` (this project's Claude Code permission settings; no forecast input).
  The laptop check had passed because the user-level ignore file `~/.config/git/ignore` hides that file from git on
  the laptop, while SkyPilot's upload reads only `.gitignore` and `.git/info/exclude`. I added
  `**/.claude/settings.local.json` to `.git/info/exclude`, as the repository's other `.claude` entries already are,
  recorded a1's failure in `plan/hh3-attempts.log`, and submitted a2 from the same commit. a1 wrote nothing to S3.
  Disclosure 10 says "job 2"; the accepted emission is job 3. The 45-minute idle stop (not 20) is FT13's launch
  setting, chosen so FT13's acceptance fits before HH3.
- **Box workdir before and after the emission:** 276 tracked files absent, every one left out by the upload rule
  (disclosure 13; FT12 had 268), 0 edited, 0 untracked outside the job's paths; the absence list hashes to
  `6ec336b37b27…` both times. `HH3-DONE`: `sums=dacb3b291b87… absent=276 edited=0 untracked_outside=0 attempt=a2`.
- **Acceptance (laptop, 07:52 IST):** fresh S3 download of `runs/hh3-registration/a2/`; `sha256sum -c SHA256SUMS.box`
  14 of 14 OK; `scripts/build_hh2.py --registration hh3 --emission-commit f0a2fbe678e1ef656ca66400ffedbf4a606dd5f9`
  exit 0 with every provenance check passed (frame, anchor, instrument text, manifests, emission commit, inference
  source hashes on the box and in the checkout, box tree records, HH3-DONE, coverage, weights, probabilities, no
  zeroed options, forecasts recomputed from rows). A second build into a separate folder gave identical files.
- **Public-folder check (laptop, before the push):** from a copy of `hh3/`, the anchor command below rebuilt
  `anchor-ft13.txt` byte for byte, `sha256sum -c SHA256SUMS.box` gave 14 of 14 OK, and `build_hh2.py` from the
  folder's own `code/` (taken from commit `f0a2fbe`) exited 0 and reproduced the six forecasts byte for byte.
- Anchor sha256 `913c6645db67402d199b023c1d9afaf0b4cb881b54bf1b143acd64084c5e1a26` (FT13's); frame sha256
  `6653915b47277578d2170c275c57699fe6538e93d347cd5ba990d112a2bd5743`.
- approval (M3ALT), raw: Strongly approve 16.8, Somewhat approve 18.4, Somewhat disapprove 26.6, Strongly disapprove 30.5, Don't Know/Not Sure 7.6; approve 35.2, net -21.9; party positive Dem 27.6 / Ind 33.4 / Rep 44.2 — sha256 `2f3b9d9fd97d8b459aa7d99838bfe385c81e3d42e459bf645da260a4fd4cd2a2`
- direction (M1), raw: Right track 20.1, Wrong track 49.6, Don't know / Unsure 30.3; net -29.5; party positive Dem 16.0 / Ind 18.4 / Rep 25.4 — sha256 `b914224ac62582f0de67701562a652094986ce46498af3ded2199981b1085d69`
- generic ballot (CON2026B), raw: Democrat 47.7, Republican 52.3; net -4.6; party positive Dem 64.7 / Ind 53.2 / Rep 27.0 — sha256 `622a048d8f810e11f9409dc5082399c6575a9f90c79a0aae03b0fb2715de26f7`
- approval_cal: Strongly approve 18.2, Somewhat approve 19.6, Somewhat disapprove 24.3, Strongly disapprove 30.3, Don't Know/Not Sure 7.6; approve 37.8, net -16.8; party positive Dem 14.8 / Ind 31.3 / Rep 65.1 — sha256 `1c9ed1d55e0e7cb61197a96ca13ce60673b5473c126babade263b4f81e501f5d`
- direction_dk: Right track 25.9, Wrong track 64.1, Don't know / Unsure 10.0; net -38.2; party positive Dem 20.8 / Ind 24.0 / Rep 32.3 — sha256 `614ce8de9ea23d5cd241d77f059ddfcf58998927b8486c40aff2d0fd37469d14`
- ballot_cal: Democrat 54.6, Republican 45.4; net +9.2; party positive Dem 89.0 / Ind 68.3 / Rep 10.2 — sha256 `144dca4468c183c3ca99996097d34cc2d3f069fa1d3cf21e7cf7b9138f44a853`
- direction_dk: s = 0.3305029132752284 (solved on the unrounded aggregate; raw DK 30.3 → 10.0).
- **Change from HH2's registered numbers** (HH2 ran on another box, so each change includes run-to-run noise,
  disclosure 3, and the anchor change, disclosure 5): approval_cal 41.2 → 37.8 (−3.4), approval_raw 36.8 → 35.2
  (−1.6), direction_dk 27.0 → 25.9, ballot_cal 53.4 → 54.6. HH3 does not separate the two causes.
- **Expectations, live in the numbers:** approval_cal 37.8 hits approve (±5) on a print of 33 to 42; HH2's benchmark
  (October, 39) would sit 1.2 above it. Net −16.8 hits ±8 on a printed net of −24.8 to −8.8. direction_dk 25.9 hits
  right track on a print of 21 to 30. ballot_cal 54.6 hits a Democrat share of 50.6 to 58.6 on the question the ballot
  scoring rule picks; ballot_raw 47.7 hits 43.7 to 51.7.

## Reproducing from this folder (public, offline)

- Anchor: `PYTHONPATH=code python3 -m quorum.twin.anchor_builder --date 2026-11-10 --facts anchor-facts.json --no-network --out anchor.txt`
  rebuilds `anchor-ft13.txt` byte for byte (sha256 `913c6645…`).
- Emission check: `cd emission && sha256sum -c SHA256SUMS.box`.
- Calibrated arms: `PYTHONPATH=code python3 code/scripts/build_hh2.py --registration hh3 --emission-commit <stamped
  commit> --src emission --out rebuilt --frame frame_hh.csv --anchor anchor-ft13.txt` reproduces the six
  `forecast-hh3-*.json` files byte for byte.

## Verdict
*(empty at registration)*
