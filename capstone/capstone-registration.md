# Midterm Capstone — national House popular-vote margin (declared 2026-09-10, registered 2026-09-11)

**Status: REGISTERED 2026-09-11 (Chirag "go ahead"); public record = the quorum-forward-tests commit adding `capstone/`.** The marquee registration of the series: one
number, one bar, scored once, against the certified result.

## Registered quantity

**The national House of Representatives popular-vote margin, Democratic minus Republican
share of the two-party vote, in the November 3, 2026 general election** — scored against
the Cook Political Report / FEC national House popular vote once ≥ 99% of the vote is
counted (expected mid-December 2026; verdict appended then, not on election night).

Bar: **|forecast margin − certified margin| ≤ 3.0 points.** Head-to-head: our margin error
< the final pre-election generic-ballot polling average's error. **Named at
registration: the RealClearPolitics "2026 Generic Congressional Vote" average as displayed
on November 2, 2026 (D − R spread), captured by screenshot + archive.org snapshot that day.**
Persistence's analogue for an election: the strongest thing a non-forecaster can do is copy
the polling average, so that is the bar to beat.

## Method (frozen at registration)

- Engine: the frozen FT-series method (Qwen3-14B + adapter; phi-4 challenger as a second
  arm only if FT5's head-to-head 3 is upheld). Instrument `yougov_house_ballot` (generic
  form), frame W161.
- Calibration: `HOUSE_BALLOT_NS` Platt (a 2.7534, b 0.4401), frozen 2026-08-26; validated in
  public on FT4 (calibrated margin error −1.1, party MAE 6.8 on the Sep 4–8 wave).
- **Turnout model, declared here — the load-bearing assumption.** Our frame is adult
  citizens; the electorate is not. We reweight each W161 profile cell by a turnout
  propensity from the **2022 Current Population Survey Voting Supplement** (Census; public),
  by age × race/ethnicity × education, applied multiplicatively to the survey weight.
  No 2026 polling, no partisan turnout adjustment, no enthusiasm term. The table and its
  derivation script are committed with the registration. Disclosed: 2022 was a midterm with
  a documented Democratic-overperformance electorate; using it is a choice, made once, here.
- Abstain handling: the instrument's "Other / Not sure / Will not vote" mass is dropped
  and the two-party share renormalized (the standard two-party convention). Disclosed:
  FT4/FT5 showed the raw instrument putting ~14% on "Other" — the calibrated arm is the
  registered one.
- Anchor: mechanical protocol v1 for the registration date.

## Registered expectations, written now
- The calibrated arm's FT4 margin (+5.9) sat 1.1 under the RV-published +7 on the Sep 4–8
  wave; the generic-ballot polling average in early September reads roughly D+5 to D+7.
  A registered margin in that band, with our turnout reweighting moving it ≤ 2 points,
  is the expectation. Ballot polling historically overstates the eventual margin; we do
  **not** register a house-effect correction (none is validated).
- The raw arm is not registered (it inverts the parties — FT4 disclosure 10).

## Disclosures
1. One number scored once — no series; a hit or a miss is a single draw.
2. Turnout is the whole game and ours is a 2022 lookup, not a model.
3. Ballot calibration is fitted on Nationscape 2019 gold; one public wave (FT4) validates it.
4. The generic ballot and the actual House vote differ (uncontested seats, third parties);
   we score against the two-party popular vote and say so.
5. Scored in December, not on election night; no re-registration after Oct 20.

## Pre-registration work — DONE 2026-09-11 ($0)
1. `scripts/turnout_weights.py` → `docs/capstone-turnout-2022.json`: CPS November 2022
   public-use microdata (nov22pub.csv, Census), reported-voted / citizens 18+, weight
   PWSSWGT. Overall citizen turnout **52.2%** — the Census's published 2022 figure, which
   validates the basis. 60 cells (Age 4 × Ethnicity 5 × Education 3); 2 cells with < 100
   records (Other × College graduate+, ages 18–29 and 65+) fall back to their age × ethnicity
   marginal, declared in the file. Multiplier = cell turnout / overall.
2. `scripts/capstone_forecast.py` — Platt `HOUSE_BALLOT_NS`, weight × multiplier, two-party
   renormalization. **Identity test PASSED**: with multipliers = 1 it reproduces FT5 arm
   F-cal exactly (D 37.3 / R 32.1). 78 of 3,170 profiles lack an Age/Ethnicity/Education
   line and keep multiplier 1 (disclosed; ~1% of weight).
3. **Dry run on FT5's ballot rows (Sep 6 anchor):** identity two-party **D+7.50** → CPS-2022
   reweighted **D+6.00**. The reweight moves the electorate older (65+ 22→29% of weight),
   whiter (60→68%), more educated (College+ 34→44%) — the documented 2022 midterm shape —
   and the margin −1.5 toward R, inside the "≤ 2 points" expectation written above. The
   registered number will be the same computation on a fresh ballot emission under the
   registration-date anchor; the dry run is not the forecast.
4. Verdict scorer: one subtraction; a dated verdict file `verdict-capstone-<date>.md`.

## Registration (2026-09-11) — forecast and hashes

**Registered forecast: national two-party House popular-vote margin D − R = +8.54
(D 54.27 / R 45.73).** Bar ±3.0. Head-to-head vs the RealClearPolitics generic-ballot
average as displayed Nov 2.

| Quantity | Value |
|---|---|
| Raw calibrated shares (adult frame, before reweight) | D 38.4 / R 31.3 / other-NS-WNV 30.3 → two-party D+10.18 |
| **CPS-2022 reweighted (registered)** | D 38.1 / R 32.1 / 29.8 → **two-party D+8.54** |
| Party D-share (registered arm) | Dem 69.7 / Ind 40.5 / Rep 4.5 |
| Emission | `quorum-capstone` (ap-northeast-2, L40S:1 spot), one pass, 3,170 profiles, 2026-09-11; ~$0.5 |
| Anchor | mechanical protocol v1, 2026-09-11 — sha256 `9c631a19fbb4d74e…`, revid 1374181145, AAA $4.2770 (09-10), CPI-U July 3.4, AHE Aug 3.1 |
| Calibration | `HOUSE_BALLOT_NS` a 2.7534 b 0.4401 (frozen 2026-08-26; validated in public FT4) |
| Turnout table | `capstone-turnout-2022.json` (CPS Nov 2022, 60 cells, overall 52.2%) |
| Forecast file | `capstone/forecast-capstone-2026-09-11.json` sha256 `e14b3c4888dd221b…`; rows `capstone/rows-capstone-2026-09-11.jsonl` sha256 `e5228474c3675438…` (published for full reproducibility) |

**Disclosures added at registration:**
6. **Anchor-date sensitivity.** The identical instrument, frame and calibration emitted
   under the Sep 6 anchor (FT5's) gave two-party D+7.50 before reweight and D+6.00 after;
   under today's anchor D+10.18 / D+8.54. The only anchor inputs that changed are the date,
   the gasoline price ($4.15 → $4.28) and the wage vintage. A 2.5-point swing from that is
   the news-valence steering §4 of the paper measures, live in the marquee number. We
   register today's computation as run — no re-emission, no averaging across dates — and
   state that the forecast carries roughly ±1.5 points of anchor-date noise on top of its
   registered bar.
7. **Position vs the polls today.** Public generic-ballot averages on 2026-09-11 read
   roughly D+5 to D+7; our registered D+8.5 sits 1.5–3.5 above them. If the polls are
   right, we miss by about that; the ±3 bar makes the head-to-head a genuine contest, not
   a formality. Generic-ballot averages have tracked the final two-party House vote within
   ~1.5 points in 2018 and 2022.


## Verdict
*(empty; appended when the national two-party House vote is ≥ 99% counted)*
