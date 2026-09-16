# Quorum — Forward Tests

Public, timestamped forecasts of public opinion surveys, **registered before the survey is
fielded**, scored against the published result, and reported whether they pass or fail.

Quorum is a simulated-population engine: it estimates how a population would answer a
question, using an open-weight language model conditioned on real demographic frames. The
only way to know whether such a thing works is to make it commit in advance, in public.
That is what this repository is for.

**Running tally: 35 of 40 core registered claims hit across five scored waves
(FT1 8/8 · FT2 8/8 · FT3 7/8 · FT4 7/8 · FT5 5/8).** Misses: the raw engine's 9-cell bar
three weeks running, and — on the Sep 11–14 wave, when approval rose 3 points in a week —
both engines' toplines (raw −6.4, calibrated −5.4 against ±5): the first calibrated miss.
The same wave was the first public model-vs-model test: the phi-4 challenger won both
registered head-to-heads against the 14B (party MAE 7.2 vs 8.0; topline 4.1 vs 5.4) and beat
last-wave persistence on subgroup structure — the first arm ever to do so — while failing
its own net bar by 13 points. The arithmetic, the registered expectation we got wrong
(we had called head-to-head 4 for the 14B), and the abstention-repair arm's clean pass are
in [`verdict-ft5-2026-09-16.md`](verdict-ft5-2026-09-16.md). One scored wave
is one wave: a quarter of registered forecasts (weekly waves, a second polling house, 40+
scored quantities) runs before any broader claim is made.

**Per-test verdict record: [`TRACK-RECORD.md`](TRACK-RECORD.md)** — one entry per forward test, regenerated from the register, never hand-edited.

![Published Economist/YouGov approval vs Quorum's registered pre-field forecasts](tracking.png)

*The series so far: published waves (lines) against every registered forecast (diamonds —
filled = scored, open = wave pending; large = calibrated engine, small = raw). The chart
shows the misses too: our disapprove runs visibly low (the "Not sure" over-hedge named in
the verdict). Data + sources: [`tracking.csv`](tracking.csv); one row appends per wave.*

---

## What we have found out about our own engine (published 19 Aug 2026, before Forward Test 2 scores)

We run diagnostics on our own method and publish what they find, including when the
finding weakens a result we have already reported. This one does.

**The engine's absolute level is a fixed prior. It does not respond to the era.** We put
twelve mechanically-built, date-only context anchors to the frozen engine, spanning
February 2017 to August 2026 — a period over which real presidential approval moved
between 34% and 49%. The engine returned **29.7% to 33.2%** for every one of them. The
slope of our prediction against the published truth is **+0.004** (r = +0.023): about
four hundredths of a point of movement for every point reality moved. It never exceeded
33.2%, even against anchors whose true value was 49%. The flatness holds equally for
dates inside the model's training data and dates after it, so this is not a memory
limitation — it is a fixed prior.

**What that means for Forward Test 1, which passed.** Its topline pass was substantially
a coincidence: the published figure was 35.0%, our engine's constant sits near 32%, and
the context facts plus the calibration lifted it to 34.9%. Had the identical registered
method been aimed at the December 2025 wave, it would have predicted roughly 35% against
a published 41% — a six-point miss and a failed bar. **We do not forecast movement, and
no absolute level from this engine should be trusted without an external anchor.**

**What is not affected.** The party-structure result stands: raw party error of 21.4
points versus 7.23 for the calibrated engine is a *difference between two engines on
identical inputs*, which no shared level prior can manufacture. Per-respondent
discrimination (AUC 0.896 against real individual answers) is likewise independent of
level.

**What we are doing about it.** The registered series continues unchanged — the frozen
method is the record, and altering it after seeing a result would defeat the purpose.
Alongside it we are building a two-stage engine of the kind survey statisticians already
use for this exact problem: the model supplies the conditional structure it is genuinely
good at, and a small amount of real data supplies the level. Future registrations will
also carry a **movement bar** — predicting the change from the previous published wave,
which a fixed prior cannot fake.

Evidence: twelve-anchor sweep, 19 August 2026. We publish this before Forward Test 2 is
scored rather than after, so it cannot be mistaken for an explanation of a result we have
already seen.

---

## Scoreboard

One row per engine per wave; rows are appended as waves register and score, newest last.
Every verdict links to the frozen protocol carrying its arithmetic.

### The Economist/YouGov — presidential approval · weekly

| Wave (fielded) | Registered | Engine | Result | Verdict | Detail |
|---|---|---|---|---|---|
| Aug 14–17, 2026 | Aug 13, pre-field | raw | 3/3 bars (topline −1.4 · net +3.8 · 9-cell 4.14) | **PASS** | [protocol + verdict](forward-test-1.md) |
| Aug 14–17, 2026 | Aug 13, pre-field | calibrated | 4/4 bars (topline −0.1 · party MAE 7.23) + head-to-head upheld | **PASS** | [protocol + verdict](forward-test-1b.md) |
| Aug 21–24, 2026 | Aug 17, pre-field | raw | 3/3 bars (topline −2.7 · net −2.0 · 9-cell 5.2) | **PASS** | [protocol + verdict](forward-test-2.md) |
| Aug 21–24, 2026 | Aug 17, pre-field | calibrated | 4/4 bars (topline −1.9 · party MAE 9.0) + head-to-head upheld | **PASS** | [protocol + verdict](forward-test-2.md) |
| Aug 28–31, 2026 | Aug 26, pre-field | raw | 2/3 bars (topline −3.4 · net +0.1 · **9-cell 6.31 > 6**) | **FAIL** | [protocol + verdict](forward-test-3.md) |
| Aug 28–31, 2026 | Aug 26, pre-field | calibrated | 4/4 bars (topline −3.4 · party MAE 8.8) + head-to-head upheld; structure bar lost to persistence and movement bar failed, both as registered | **PASS** | [protocol + verdict](forward-test-3.md) |
| Sep 4–8, 2026 (RV base — frame change, disclosed) | Sep 2, pre-field (`e4a0bd0`) | raw | 2/3 bars (topline −3.7 · net +0.6 · **9-cell 6.63 > 6**) | **FAIL** | [verdict](verdict-ft4-2026-09-10.md) · [protocol](ft4/ft4-registration.md) |
| Sep 4–8, 2026 | Sep 2, pre-field | calibrated | 4/4 bars (topline −2.9 · 9-cell 4.36 · party MAE 8.9) + head-to-head upheld; movement bar passed | **PASS** | [verdict](verdict-ft4-2026-09-10.md) |
| Sep 4–8, 2026 | Sep 2, pre-field | raw+dk (C) · no-anchor (D) · direction (E) · ballot (F) | C: dk head-to-head UPHELD (NS 8.0→3.6), 9-cell miss · D: expected topline FAIL met (−8.5) · E: 0/4 as disclosed · F: cal margin −1.1 + party 6.8 hit, D-share −4.3 miss | measurements, reported | [verdict](verdict-ft4-2026-09-10.md) |
| Sep 11–14, 2026 (RV base; approval +3 on the week) | Sep 6, pre-field (`6855b4b`) | 14B raw | 0/3 bars (**topline −6.4** · net −4.9 · **9-cell 6.59**) | **FAIL** | [verdict](verdict-ft5-2026-09-16.md) · [protocol](ft5/ft5-registration.md) |
| Sep 11–14, 2026 | Sep 6, pre-field | 14B calibrated | 3/4 bars (**topline −5.4 > 5** · net −2.8 · 9-cell 4.28 · party 8.0) + head-to-head upheld — first calibrated miss | **FAIL** | [verdict](verdict-ft5-2026-09-16.md) |
| Sep 11–14, 2026 | Sep 6, pre-field | **phi-4 challenger** raw · calibrated | raw 2/3 (topline +2.4 · **net +9.7** · 9-cell 4.23); cal 3/4 (topline +4.1 · **net +13.2** · 9-cell 5.40 · party **7.2**) — **head-to-head 3 UPHELD (7.2 < 8.0), head-to-head 4 UPHELD (4.1 < 5.4)**; beat persistence on structure (1.59 vs 2.78) | **FAIL / FAIL — challenger wins both head-to-heads** | [verdict](verdict-ft5-2026-09-16.md) |
| Sep 11–14, 2026 | Sep 6, pre-field | raw+dk (C) · no-anchor (D) · direction (E) · ballot (F) | **C PASS 3/3, dk head-to-head UPHELD** · D expected FAIL met (−11.4) · E 0/4 (Platt arm retired) · F cal margin +0.2 + party 7.5 hit, D-share −6.7 miss | measurements | [verdict](verdict-ft5-2026-09-16.md) |
| first wave to field after Sep 16 (expected Sep 18–21) | Sep 16, pre-field | 14B A–D · **phi-4 P/P-cal (continues; H2H3/4 + NEW H2H5 net)** · direction_dk · ballot | approval 33.3 / 33.9 (third straight); phi-4 42.3 / 44.1; direction_dk 23.9 | *pending* | [protocol](ft6/ft6-registration.md) |

### Gallup — satisfaction with the way things are going · monthly

| Poll (fields) | Registered | Engine | Result | Verdict | Detail |
|---|---|---|---|---|---|
| September 2026 (~Sept 1–19) | Aug 29, pre-field (`4881748`) | raw + calibrated | satisfied 35.7 (raw) / 48.7 (calibrated, cross-survey miss risk disclosed) | *pending* | [protocol](gs1/gallup-satisfaction-registration.md) |

### The November 3, 2026 midterm — national House popular-vote margin · the capstone

| Registered | Quantity | Forecast | Bar / head-to-head | Verdict | Detail |
|---|---|---|---|---|---|
| Sep 11, 2026, pre-election | two-party House vote, D − R | **D+8.54** (D 54.27 / R 45.73) | ±3.0 · beats the RealClearPolitics generic-ballot average as of Nov 2 | *scored Dec 2026, when ≥ 99% counted* | [registration](capstone/capstone-registration.md) · [forecast](capstone/forecast-capstone-2026-09-11.json) · [rows](capstone/rows-capstone-2026-09-11.jsonl) |

One number, one bar, scored once. Turnout is a declared 2022-CPS reweight (the table and
its script are in `capstone/`); the anchor-date sensitivity of the number (±1.5) is
disclosed in the registration, not discovered after.

### Coming next — each gated on the published entry rule

A question family enters this scoreboard only after passing a validation diagnostic on
real per-person data (correct party ordering and adequate discrimination), and the rule
is applied before any forecast is made — families that fail are named, not skipped
silently (economic evaluation currently fails it and is excluded).

- **Direction of country** and the **generic House ballot** (same weekly poll) — entry
  diagnostics passed on Nationscape gold (uAUC 0.765 / 0.950, party ordering correct);
  registered in FT4 as measurement arms, with their registration-day weaknesses disclosed.
- **Trump favorability** — diagnostic passed (uAUC 0.831) and calibration frozen; no weekly
  published target in the E/YouGov toplines, so not yet registrable.
- **Consumer sentiment** — currently excluded (economic family); enters only if a
  published in-family repair passes its own pre-declared test.

---

## Latest scored wave, in full

Published poll: *Economist*/YouGov, fielded September 11–14 2026, **registered-voter base
(n = 1,461)**, approval up 3 on the week
([crosstabs](https://d3nkl3psvxxpe9.cloudfront.net/documents/econTabReport_ZmVljW6.pdf),
table 19). The first wave with two engines registered side by side — every cell for both,
errors shown:

| Quantity | Published (RV) | 14B calibrated (err) | phi-4 calibrated (err) | 14B raw (err) |
|---|---|---|---|---|
| **Approve** | **40.0** | 34.6 (**−5.4**) | 44.1 (**+4.1**) | 33.6 (−6.4) |
| Disapprove | 58.0 | 55.4 (−2.6) | 49.9 (−8.1) | 56.4 (−1.6) |
| Not sure | 2.0 | 10.0 (+8.0) | 6.9 (+4.9) | 10.0 (+8.0) |
| **Net** | **−18** | −20.8 (−2.8) | −5.8 (**+13.2**) | −22.8 (−4.9) |
| Men | 44 | 40.6 (−3.4) | 46.8 (+2.8) | 35.4 (−8.6) |
| Women | 36 | 29.4 (−6.6) | 41.9 (+5.9) | 31.5 (−4.5) |
| Age 18–29 | 31 | 31.7 (+0.7) | 37.9 (+6.9) | 32.3 (+1.3) |
| Age 30–44 | 37 | 33.9 (−3.1) | 42.3 (+5.3) | 33.0 (−4.0) |
| Age 45–64 | 44 | 36.9 (−7.1) | 48.3 (+4.3) | 34.0 (−10.0) |
| Age 65+ | 43 | 36.2 (−6.8) | 48.2 (+5.2) | 33.8 (−9.2) |
| White | 45 | 39.8 (−5.2) | 50.4 (+5.4) | 35.1 (−9.9) |
| Black | 16 | 18.6 (+2.6) | 24.3 (+8.3) | 27.9 (+11.9) |
| Hispanic | 33 | 30.0 (−3.0) | 37.5 (+4.5) | 31.7 (−1.3) |
| Democrats | 4 | 11.0 (+7.0) | 17.9 (+13.9) | 25.1 (+21.1) |
| Independents | 30 | 29.0 (−1.0) | 33.2 (+3.2) | 32.1 (+2.1) |
| Republicans | 82 | 66.1 (**−15.9**) | 86.6 (**+4.6**) | 44.2 (−37.8) |

Bars (declared Sep 6): topline ±5 → 14B **−5.4 FAIL**, phi-4 +4.1 pass · net ±8 → 14B
pass, phi-4 **+13.2 FAIL** · 9-cell ≤ 6 → 4.28 / 5.40 both pass (raw 6.59 fails) · party
≤ 12 → 8.0 / **7.2** both pass. The two registered head-to-heads: **phi-4's party error
beat the 14B's (7.2 < 8.0) and its topline error beat the 14B's (4.1 < 5.4)** — we had
registered the second one for the 14B. phi-4's 9-cell deviations beat last-wave
persistence (1.59 vs 2.78), the first time any arm has. Read the two engines' shapes in
the table: the 14B runs low and flat (Republicans −15.9), phi-4 runs high and sharp
(every demographic cell +3 to +8, net far too positive). The abstention-repair arm passed
3/3 with its head-to-head upheld.

The fine print — the wave's 3-point move that no registered arm could see, the RV frame,
and why the challenger continues to FT6 without becoming the spine — is in
`verdict-ft5-2026-09-16.md`.

---|---|---|---|
| **Approve** | **37.0** | **34.1 (−2.9)** | 33.3 (−3.7) |
| Disapprove | 61.0 | 55.9 (−5.1) | 56.7 (−4.3) |
| Not sure | 2.0 | 10.0 (+8.0) | 10.0 (+8.0) |
| **Net** | **−24** | **−21.8 (+2.2)** | −23.4 (+0.6) |
| Men | 44 | 40.0 (−4.0) | 35.4 (−8.6) |
| Women | 30 | 28.9 (−1.1) | 31.5 (+1.5) |
| Age 18–29 | 26 | 31.4 (+5.4) | 32.3 (+6.3) |
| Age 30–44 | 30 | 33.5 (+3.5) | 33.0 (+3.0) |
| Age 45–64 | 43 | 36.2 (−6.8) | 34.0 (−9.0) |
| Age 65+ | 42 | 35.4 (−6.6) | 33.8 (−8.2) |
| White | 41 | 39.3 (−1.7) | 35.1 (−5.9) |
| Black | 15 | 18.5 (+3.5) | **27.9 (+12.9)** |
| Hispanic | 36 | 29.4 (−6.6) | 31.7 (−4.3) |
| Democrats | 3 | **11.0 (+8.0)** | 25.0 (+22.0) |
| Independents | 25 | **28.7 (+3.7)** | 31.8 (+6.8) |
| Republicans | 80 | **64.9 (−15.1)** | 43.7 (−36.3) |

Bars (declared before fielding; averages, so single cells above may exceed them):
topline ±5 → **2.9 / 3.7**, both pass · net ±8 → **2.2 / 0.6**, both pass ·
sex/age/race 9-cell MAE ≤ 6 → **4.36 pass / 6.63 FAIL** — the raw engine's second
consecutive 9-cell miss, spread across Men, 45–64, 65+ and Black this time · party MAE
≤ 12, registered for the calibrated engine only → **8.9**, pass; head-to-head upheld.
FT4 also carried the abstention-repair arm (head-to-head **upheld**: "Not sure" 8.0 → 3.6
with the topline improving), the no-anchor ablation (**failed its topline by 8.5, as
registered**), and direction / House-ballot measurement arms (direction 0/4 as disclosed;
ballot calibrated hit margin −1.1 and party 6.8, missed the Democratic share by 0.3
beyond its bar on a named-candidate form).

Read the verdict's fine print in `verdict-ft4-2026-09-10.md`, including what we surface
ourselves: the frame change, the persistence column (last wave re-used beat both engines
on every approval quantity — three of four scored waves now), and the calibrated arm
passing a movement bar it was registered to fail — by moving against the real direction
inside a wide bar, which we do not count as tracking.

---|---|---|---|
| **Approve** | **36.0** | **32.6 (−3.4)** | 32.6 (−3.4) |
| Disapprove | 60.0 | 56.6 (−3.4) | 56.5 (−3.5) |
| Not sure | 4.0 | 10.9 (+6.9) | 10.9 (+6.9) |
| **Net** | **−24** | **−24.0 (0.0)** | −23.9 (+0.1) |
| Men | 40 | 38.5 (−1.5) | 34.7 (−5.3) |
| Women | 32 | 27.2 (−4.8) | 30.7 (−1.3) |
| Age 18–29 | 32 | 29.8 (−2.2) | 31.6 (−0.4) |
| Age 30–44 | 27 | 31.8 (+4.8) | 32.4 (+5.4) |
| Age 45–64 | 39 | 34.7 (−4.3) | 33.2 (−5.8) |
| Age 65+ | 43 | 34.1 (−8.9) | 33.2 (−9.8) |
| White | 42 | 37.5 (−4.5) | 34.4 (−7.6) |
| Black | 11 | 17.6 (+6.6) | **27.3 (+16.3)** |
| Hispanic | 36 | 28.0 (−8.0) | 31.1 (−4.9) |
| Democrats | 5 | **10.2 (+5.2)** | 24.3 (+19.3) |
| Independents | 22 | **26.6 (+4.6)** | 31.1 (+9.1) |
| Republicans | 80 | **63.4 (−16.6)** | 43.1 (−36.9) |

Bars (declared before fielding; averages, so single cells above may exceed them):
topline ±5 → **3.4 / 3.4**, both pass · net ±8 → **0.0 / 0.1**, both pass ·
sex/age/race 9-cell MAE ≤ 6 → **5.07 pass / 6.31 FAIL** — the raw engine's first public
miss, carried by the Black cell · party MAE ≤ 12, registered for the calibrated engine
only → **8.8**, pass (raw party published unregistered, missed by 21.8; the head-to-head
claim that calibration fixes it was registered, and upheld). FT3 also carried two new
bars: subgroup *structure* against persistence (lost, 3.87 vs 2.78 — the backtest said
it would) and a *movement* bar (failed, −3.4 forecast vs 0.0 actual — registered in
advance as the bar we expected to fail, because the engine's level does not move).

Read the verdict's fine print in `forward-test-3.md`, including what we surface
ourselves: the engine over-predicts "Not sure" (10.9 vs 4, its widest gap yet — a repair
is registered as a variant arm from FT4), and simply copying the previous week's poll
beat both engines on every quantity this wave (persistence: topline 0.0, net 3.0,
party 2.0, 9-cell 2.78) — a benchmark that exists only for questions already polled
weekly, which is why an already-polled question is the proving ground and not the
product.

---

## Registration record — frozen artifacts

Everything below is the registration history, immutable once committed: hashes live in
`SHA256SUMS`, corrections appear as new dated files, never edits. (This README is the
living front page and is excluded from `SHA256SUMS`.)

**Hash convention, stated plainly (2026-09-06).** The hashes in `SHA256SUMS` are
*registration-time* hashes. For Forward Tests 1–3 the verdict was appended to the
registered protocol file after it scored, so `shasum -c` reports those four files as
changed — the registered content is byte-identical up to the appended `## Verdict`
section, and the registration commit (timestamped by GitHub) holds the original. From
Forward Test 4 onward, verdicts are separate dated files (`verdict-<test>-<date>.md`) and
every registered file verifies cold.

## Forward Test 1 — the registration, as frozen 2026-08-13 2026-08-13

**Target:** the next *Economist*/YouGov weekly poll to begin fielding after the registration
timestamp (expected on or about 14–17 August 2026), presidential job approval question:

> "Do you approve or disapprove of the way Donald Trump is handling his job as President?"

**Registered forecast** (U.S. adult citizens):

| Quantity | Forecast |
|---|---|
| **Approve** | **33.6%** |
| **Disapprove** | **55.8%** |
| **Net** | **−22.2** |
| Not sure | 10.6% |

Registered subgroup approve shares:

| Cut | Forecast |
|---|---|
| Male / Female | 36.0 / 31.4 |
| Age 18–29 / 30–44 / 45–64 / 65+ | 32.3 / 33.3 / 34.4 / 34.3 |
| White / Black / Hispanic | 35.6 / 27.2 / 31.8 |

Also published, **explicitly not registered** (see the protocol's disclosure): party-ID
cuts — Dem 24.1, Ind 31.4, Rep 46.3. A pre-registration dry run showed the method's
party-conditional spread is compressed relative to any published wave; rather than quietly
drop the weakness, we publish it unregistered and name it as the next thing to fix.

**Declared success bars** (set before the result exists): topline approve error ≤ 5 points;
net error ≤ 8 points; mean absolute error across the 9 registered subgroup cells ≤ 6 points.

**Method, in one paragraph:** ~3,200 distinct demographic profiles drawn from Pew Research
Center's American Trends Panel Wave 161 (February 2025) microdata, carrying Pew's survey
weights; each profile is put to the poll's exact question wording by a fine-tuned
open-weight model, which returns a probability distribution over the five answer options;
the distributions are weight-averaged into a topline and crosstabs. The prompt includes one
paragraph of era context (`anchor-2026-08-13.txt`) containing **no polling numbers**. No
2026 polling data enters the model, the prompt, or any calibration step. The method's only
calibration anchor is a February 2025 validation in which it recovered the published Pew
approval topline within ±5 points.

**Files**

| File | What it is |
|---|---|
| `forward-test-1.md` | the full protocol as registered, including limitations |
| `forecast-ft1.json` | the frozen forecast, with the era anchor and its hash inside |
| `anchor-2026-08-13.txt` | the era-context paragraph given to the model |
| `SHA256SUMS` | hashes of all three |

**Registration mechanism.** This repository *is* the registration. The three registered
artifacts — `forward-test-1.md`, `forecast-ft1.json`, `anchor-2026-08-13.txt` — are
immutable once committed: their hashes in `SHA256SUMS` will never change, and any
correction appears as a new dated file rather than an edit. (This README is the living
front page and is excluded from `SHA256SUMS` for that reason.)

**How to verify us:** the commit that added the registered artifacts is timestamped by
GitHub and predates the target poll's field dates. Check `SHA256SUMS` against the files; check the
field dates on the published *Economist*/YouGov toplines; then compare the numbers above to
what the poll actually reported. When it publishes, the verdict — pass or fail, with the
arithmetic — is appended to `forward-test-1.md` in this repository.

---

## Forward Test 1-B — companion, registered the same day (calibrated)

Forward Test 1's protocol disclosed that the engine's party-conditional spread is
compressed. Investigating that — using only 2019 and 2025 gold data, none from 2026 — found
that the engine *ranks* respondents well (AUC 0.896 against real per-person answers) while
its *probabilities* are systematically compressed, and that a two-parameter monotone
calibration corrects it: held-out party error 20.25 → 5.63 points, and the same correction
transports to a different survey from a different era with no refitting.

FT1-B registers that correction as a falsifiable prediction **on the same poll**, so one
published result adjudicates the uncorrected and corrected engine. **Forward Test 1 is
unchanged and will be scored exactly as registered** — its file and hash are untouched.

| Cut | FT1 (raw) | FT1-B (calibrated) |
|---|---|---|
| Approve / Disapprove / Net | 33.6 / 55.8 / −22.2 | **34.9 / 54.5 / −19.7** |
| Party: Dem / Ind / Rep | 24.1 / 31.4 / 46.3 | **9.8 / 27.3 / 70.4** |
| Sex: Male / Female | 36.0 / 31.4 | **41.2 / 29.1** |
| Age: 18-29 / 30-44 / 45-64 / 65+ | 32.3 / 33.3 / 34.4 / 34.3 | **31.3 / 34.0 / 37.3 / 36.9** |
| Race: White / Black / Hispanic | 35.6 / 27.2 / 31.8 | **40.6 / 17.1 / 29.6** |

The registered claim: FT1-B's party error beats FT1's, and lands within 12 points. Details,
bars, and the full disclosure are in `forward-test-1b.md`; the forecast is
`forecast-ft1b.json`.

---

## Forward Test 2 — registered 2026-08-17 (pending)

Same frozen method, same bars, next wave: raw (FT2) and calibrated (FT2-B) forecasts of
the first *Economist*/YouGov poll to begin fielding after the registration push, expected
to field on or about August 21–24, 2026. Fresh dated era anchor
(`anchor-2026-08-17.txt`, no polling numbers), hashes in `SHA256SUMS`. Protocol and
forecasts: `forward-test-2.md`, `forecast-ft2.json`, `forecast-ft2b.json`.

---

## What is not here

The model, adapters, and harness source are not published; the panel microdata is not
redistributed (its licence forbids that). This repository is the *commitment record*: what
we predicted, when we predicted it, and how it scored.

## Attribution

Population frame derived from Pew Research Center's American Trends Panel, Wave 161. Pew
Research Center bears no responsibility for the analyses or interpretations here.
