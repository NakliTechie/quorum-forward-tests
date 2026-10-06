# HH2 — Harvard CAPS/Harris Registration, October 2026

**Status: STAMPED 2026-10-06 (registered when pushed to quorum-forward-tests); drafted 2026-10-06 (Chirag 2026-10-04: "First thing Tomorow is to lock Harris along with the Oct 6
one."). It becomes a registration when pushed to the public repository (quorum-forward-tests) with its
forecasts and hashes, BEFORE the target begins fielding.**
Target: **the first Harvard CAPS/Harris poll to begin fielding after HH2's public push** (order-based; the
last wave fielded September 26–28, 2026; their gaps run 25–57 days, so the next wave is expected late October
to mid-November). On 2026-10-06 09:50 IST harvardharrispoll.com lists September 2026 as the latest poll.

## What changed since HH1 / HH1-B (decided before any HH2 number exists)

- **No house-shift arm.** HH1-B's verdict: approval_cal hit approval (0.0) and its party cuts (MAE 1.47);
  adding the +7.2 house offset on top missed by +7.2, counting the same gap twice. HH2 drops both house arms.
- Everything else is HH1 / HH1-B's frozen method, unchanged: same engine, frame, instruments, Platt maps and
  DK rule, on a fresh mechanical anchor.

## Registered arms and bars

| Arm | Built as | Bars |
|---|---|---|
| approval_raw | frozen FT-series engine, soft first-token, M3ALT wording | approve ±5 · net ±8 |
| direction_raw | same engine, M1 wording | right track ±5 |
| ballot_raw | same engine, CON2026B two-row forced choice | Democrat share ±4 |
| approval_cal | Platt on the conditional approve share, `approval_pooled_2019_2025` (a 3.6133, b 1.3759) | approve ±5 · net ±8 · party MAE ≤ 12 |
| direction_dk | E35-form abstain-shrink, *s* solved so aggregate DK = 10.0 (the September wave's published right-track DK) | right track ±5 |
| ballot_cal | Platt `HOUSE_BALLOT_NS` (a 2.7534, b 0.4401) on the two-row share | Democrat share ±4 |

**Head-to-head claim:** approval_cal party MAE < approval_raw party MAE (party = Dem / Ind / Rep approve, as
printed by Harvard-Harris; IND/OTH entered as Ind).

**Benchmark, reported beside every arm (not scored as a claim):** "same as last month's poll", fixed now from
the September 26–28 wave: approve 42, net −13, right track 35, Democrat share 50, party approve 15 / 32 / 75.

## Method (frozen at registration)

- Engine: the frozen FT-series / HH1 method, Qwen3-14B at revision 40c069824f4251a91eefaf281ebe4c544efd3e18 +
  the FT adapter (eval-adapters/14b, adapter_model.safetensors sha `4cabea94…59b8e5`, adapter_config.json sha
  `563a0337…3282bb`) served as LoRA, soft first-token. HH1 did not pin the revision; Hugging Face's history shows
  `40c06982…` has been Qwen3-14B's main since 2025-07-26, so HH1 ran the same weights. HH2 pins it by loading the
  snapshot at that revision by path, and the job checks the adapter hashes before any prompt. Each instrument's
  run manifest records revision, adapter hashes, package versions and GPU.
- Frame: W161 recomposed to Harvard-Harris's printed standing composition (party Dem 33 / Rep 35 / Ind 28 /
  Other 3), `scripts/build_hh_frame.py`, frame sha `6653915b47277578d2170c275c57699fe6538e93d347cd5ba990d112a2bd5743`
  (identical to HH1's `quorum-forward-tests/hh1/frame_hh.csv`).
- Instruments: `hh_approval`, `hh_direction`, `hh_generic_ballot` (wording verbatim from their decks: M3ALT,
  M1, CON2026B), unchanged since HH1.
- Era anchor: mechanical builder (`quorum.twin.anchor_builder`, protocol v1), date 2026-10-06; facts in
  `data/forward/hh2/anchor-facts.json` (AAA $4.3653 read 2026-10-06; Wikipedia "2026 in the United States"
  revision 1378680367; BLS CPI Aug 3.4%, average hourly earnings Sep 3.0%). Conflict clause unchanged from
  FT8's (the revision still describes the war, stalled talks and continuing strikes). Anchor sha256
  `df3caf8a224ed80ac347f11bcdb2f6fcc446554c1dc3c49b583e00b7a40c80b0`. No polling numbers.
- Emission: one GPU job (3 instruments × HH frame, ~20 min), run as job 3 on the UQ1 double-smoke box after its
  two smoke jobs; outputs to `s3://sky-quorum-artifacts-615809814090/runs/hh2-registration/<attempt>/`, each
  instrument saved there as soon as it finishes. Calibrated arms are CPU transforms of the same rows
  (`scripts/build_hh2.py`), which first refuses any emission whose frame, anchor, instrument text, raw
  status, manifests (model revision, adapter, stub off, inference-source hashes, code commit), profile coverage
  (every frame profile exactly once), weights or probabilities do not check out, whose forecast files differ from
  the aggregate recomputed from their rows, or in which any profile gives an option exactly 0 (the top-20
  truncation found in UQ1's bare-model arm; adapter arms showed none there). A refusal is a failed attempt under
  the retry policy below.
- **Retry policy (declared before emission).** Attempt `a1`. If the box is lost or the job fails, one full rerun
  as `a2` on a new box: all three instruments again, never mixing attempts. The registered numbers are those of
  the first attempt that completes all three. A second failure stops and returns to Chirag. No attempt is
  chosen by its numbers.
- **One numerical change from HH1-B, declared before emission:** HH1-B solved the DK shrink on the rounded
  aggregate, which can land a tenth off (its solve on HH1 rows gives 9.9 for a 10.0 target). HH2 solves on the
  unrounded aggregate and records *s* at full precision (on HH1 rows: exactly 10.0).

## Disclosures

1. Frame hybrid, surrogate validation, no publisher microdata: as HH1 disclosures 1, 3 and 4.
1b. **Independents are not the same population on both sides.** Harvard-Harris prints IND/OTH (independents and
   others together); our frame's Ind cell holds independents only (others stay in the topline, out of the party
   cut). HH1 compared them the same way; the frozen cut is kept and the mismatch disclosed.
2. direction_dk's *s* is solved on the September wave's published DK (10%), the only post-HH1 published number
   used; it targets the abstain share, not the right-track level. Disclosed as in-sample for DK.
3. **Run-to-run variation.** On 2026-10-04 we found that this engine, served with the adapter as LoRA, does
   not repeat bit for bit: each simulated person's probability moves by about 1 point between identical runs,
   and group totals by up to about 0.3 points (`docs/uq1/determinism-probe-round1.md`). The cause is vLLM
   0.8.5's LoRA kernel. A merged checkpoint removes it, but HH2 keeps the registered engine so HH1 and HH2
   compare directly. The registered numbers are the ones emitted; no rerun is selected.
4. HH1 verdict context: HH1-B approval_cal hit approval exactly and passed 3/3; last month's poll beat every
   other arm (`quorum-forward-tests/hh1/verdict-hh1-2026-10-01.md`).

## Registration-day checklist
1. Anchor built (done, sha above); frame and anchor staged to `s3://…/context/hh2/` with shas checked on the box.
2. Codex pre-run review; emission job; Codex post-run review.
3. `scripts/build_hh2.py` → calibrated arms; stamp every forecast sha here; drop DRAFT.
4. Laptop acceptance: fresh S3 download of the attempt folder, `sha256sum -c SHA256SUMS.box`, then
   `scripts/build_hh2.py` (its provenance checks must pass).
5. Public repo `hh2/`: this doc; the six forecasts; the emission rows (`rows.jsonl`), per-instrument manifests and
   run manifest; the anchor, its manifest and its facts file (rebuilds offline to the same sha); the frame (same
   file as hh1); the code at the registration commit needed to rerun the transforms and check the emission
   (`scripts/build_hh2.py`, `scripts/build_hh1b.py`, `scripts/dk_shrink.py`, `quorum/twin/forecast.py`,
   `quorum/twin/instruments.py`, `quorum/twin/compression.py`, `quorum/twin/evidence.py`,
   `quorum/twin/predict.py`) with the package versions from the run manifest; SHA256SUMS entries; tracking rows.
   Commit and push before fielding.

## Registration stamps (2026-10-06)

- Emission: attempt `a1`, job 3 on quorum-uq1-smoke (AWS ap-northeast-2b, L40S), finished 12:39 IST; code commit
  `442973722876d7af8067d8d91f04e96be46655f7`; revision `40c069824f4251a91eefaf281ebe4c544efd3e18`; vllm 0.8.5, torch 2.6.0,
  transformers 4.51.3; GPU `NVIDIA L40S, 580.159.04`. Fresh-download `sha256sum -c` 13/13 OK; every
  `scripts/build_hh2.py` provenance check passed (frame, anchor, instrument text, raw, manifests, source hashes,
  coverage, weights, probabilities, no zeroed options, forecasts recomputed from rows).
- Anchor sha256 `df3caf8a224ed80ac347f11bcdb2f6fcc446554c1dc3c49b583e00b7a40c80b0`; frame sha256
  `6653915b47277578d2170c275c57699fe6538e93d347cd5ba990d112a2bd5743`.
- approval (M3ALT), raw: Strongly approve 17.7, Somewhat approve 19.1, Somewhat disapprove 26.5, Strongly disapprove 30.3, Don't Know/Not Sure 6.4; net -20.0; party positive Dem 28.6 / Ind 34.2 / Rep 47.1 — sha256 `ff6618ddfbc6095d3004a84c0156bfe7bb9f6dfbe4d7f16e112e39681838aa85`
- direction (M1), raw: Right track 21.1, Wrong track 49.0, Don't know / Unsure 30.0; net -27.9; party positive Dem 16.5 / Ind 19.2 / Rep 27.0 — sha256 `e71a2568b6de1a48434cef05f33b8722e401b75f4dc53b9a2dd0b2883a6b1e6d`
- generic ballot (CON2026B), raw: Democrat 47.2, Republican 52.8; net -5.6; party positive Dem 64.7 / Ind 52.1 / Rep 26.6 — sha256 `1b3698de1554301c6980ecb6cfd3c6ed4bf8174a270ca94a8b10f8c4c1e2042a`
- approval_cal: Strongly approve 20.0, Somewhat approve 21.2, Somewhat disapprove 23.1, Strongly disapprove 29.4, Don't Know/Not Sure 6.4; net -11.3; party positive Dem 16.1 / Ind 33.3 / Rep 71.6 — sha256 `c31c44f0210b26e7e83416f68af70b8c88ff7cd706cc80903557f92e2ac62b50`
- direction_dk: Right track 27.0, Wrong track 63.0, Don't know / Unsure 10.0; net -36.0; party positive Dem 21.4 / Ind 24.9 / Rep 34.1 — sha256 `39c41bd99ff0af41242c0b750b814c0b0263185c0f9ec7cd29c60af71edbf345`
- ballot_cal: Democrat 53.4, Republican 46.6; net +6.8; party positive Dem 89.1 / Ind 65.6 / Rep 9.4 — sha256 `f776d154236f7ae9bec75d5dab0c2e59b29ed49da52bf045b0f142d83fef762a`
- direction_dk: s = 0.3338555085787559 (solved on the unrounded aggregate; raw DK 30.0).
- Benchmark (reported, not a claim), September 26–28 wave: approve 42, net −13, right track 35, Democrat share 50,
  party approve 15 / 32 / 75.

## Reproducing from this folder (public, offline)

- Anchor: `PYTHONPATH=code python3 -m quorum.twin.anchor_builder --date 2026-10-06 --facts anchor-facts.json --no-network --out anchor.txt`
  rebuilds `anchor-2026-10-06.txt` byte for byte (sha256 `df3caf8a…`).
- Emission check: `cd emission && sha256sum -c SHA256SUMS.box` (13 files: rows, manifests, forecasts, run manifest, logs).
- Calibrated arms: `PYTHONPATH=code python3 code/scripts/build_hh2.py --src emission --out rebuilt --frame frame_hh.csv
  --anchor anchor-2026-10-06.txt` reproduces the six `forecast-hh2-*.json` files byte for byte.

## Verdict
*(empty at registration)*
