# Registrations

*Moved from the [README](README.md) on 2026-11-09.*

## FT11 scored wave, in full (Oct 23–26; the latest when written on Oct 29)

Published poll: *Economist*/YouGov, fielded October 23–26 2026, **registered-voter base
(n = 1,440)**, approval down 1 on the week
([crosstabs](https://d3nkl3psvxxpe9.cloudfront.net/documents/econTabReport_AdxdJpN.pdf),
table 44). The third wave with the re-weighted arm (ygdk) registered as a public arm — every cell, errors shown:

| Quantity | Published (RV) | 14B calibrated (err) | ygdk, re-weighted (err) | 14B raw (err) |
|---|---|---|---|---|
| **Approve** | **39.0** | 34.2 (−4.8) | 37.3 (−1.7) | 33.4 (−5.6) |
| Disapprove | 58.0 | 55.8 (−2.2) | 57.2 (−0.8) | 56.7 (−1.3) |
| Not sure | 2.0 | 10.0 (+8.0) | 5.5 (+3.5) | 10.0 (+8.0) |
| **Net** | **−19.0** | −21.6 (−2.6) | −19.9 (−0.9) | −23.3 (−4.3) |
| Men | 45 | 40.0 (−5.0) | 43.6 (−1.4) | 35.4 (−9.6) |
| Women | 34 | 28.9 (−5.1) | 31.2 (−2.8) | 31.6 (−2.4) |
| Age 18–29 | 35 | 31.6 (−3.4) | 34.3 (−0.7) | 32.5 (−2.5) |
| Age 30–44 | 33 | 33.4 (+0.4) | 36.5 (+3.5) | 33.1 (+0.1) |
| Age 45–64 | 44 | 35.9 (−8.1) | 39.3 (−4.7) | 33.9 (−10.1) |
| Age 65+ | 42 | 35.7 (−6.3) | 38.3 (−3.7) | 34.0 (−8.0) |
| White | 44 | 39.2 (−4.8) | 42.4 (−1.6) | 35.1 (−8.9) |
| Black | 15 | 18.9 (+3.9) | 18.3 (+3.3) | 28.1 (+13.1) |
| Hispanic | 38 | 29.6 (−8.4) | 31.4 (−6.6) | 31.9 (−6.1) |
| Democrats | 4 | 11.6 (+7.6) | 12.3 (+8.3) | 25.3 (+21.3) |
| Independents | 27 | 29.0 (+2.0) | 30.6 (+3.6) | 32.1 (+5.1) |
| Republicans | 81 | 63.9 (−17.1) | 66.0 (−15.0) | 43.4 (−37.6) |

Bars (declared Oct 21): topline ±5 → calibrated −4.8 passes (by 0.2), raw −5.6 fails, ygdk −1.7 passes · net ±8 →
−2.6, −4.3, −0.9, all pass · 9-cell ≤ 6 → calibrated 5.04 passes, raw 6.76 fails (ygdk 3.14, reported) · party ≤ 12 →
calibrated 8.9 passes (ygdk 9.0, reported). Head-to-head 1 (calibrated party error below raw's) UPHELD; ygdk beat
the calibrated arm on the topline (H2H-Y) by 3.1. The 14B's shape is unchanged: low and flat. Its Republican cell
(63.9, against 64.3 last week) missed by −17.1 after Republican approval fell 6 points in a week, so the miss
shrank because the poll came toward the engine. Disapprove stays short because the engine over-hedges into
"Not sure" (+8.0). Last week's poll carried forward (persistence) missed the topline by +1.0, net by 0.0, party by
3.7 and the 9-cell by 1.89: it beat every engine arm on every quantity. On structure (1.56) no arm beat it
(ygdk 2.51, calibrated 2.69).

Earlier waves in full: [`verdict-ft10-2026-10-25.md`](verdict-ft10-2026-10-25.md) ·
[`verdict-ft9-2026-10-15.md`](verdict-ft9-2026-10-15.md) ·
[`verdict-ft8-2026-10-07.md`](verdict-ft8-2026-10-07.md) ·
[`verdict-ft7-2026-10-01.md`](verdict-ft7-2026-10-01.md) ·
[`verdict-ft6-2026-09-24.md`](verdict-ft6-2026-09-24.md) ·
[`verdict-ft5-2026-09-16.md`](verdict-ft5-2026-09-16.md) ·
[`verdict-ft4-2026-09-10.md`](verdict-ft4-2026-09-10.md) · [`forward-test-3.md`](forward-test-3.md).

---

## Registration record — frozen artifacts

Everything below is the registration history, immutable once committed: hashes live in
`SHA256SUMS`, corrections appear as new dated files, never edits. (This README is the
living front page and is excluded from `SHA256SUMS`.)

**Hash convention, stated plainly (2026-09-06).** The hashes in `SHA256SUMS` are
*registration-time* hashes. For Forward Tests 1–3 the verdict was appended to the
registered protocol file after it scored, so `shasum -c` reports those files (three of them; `forward-test-3.md` has no entry in `SHA256SUMS`) as
changed — the registered content is byte-identical up to the appended `## Verdict`
section, and the registration commit (timestamped by GitHub) holds the original. From
Forward Test 4 onward, verdicts are separate dated files (`verdict-<test>-<date>.md`) and
every registered file verifies cold.

## Forward Test 1 — the registration, as frozen 2026-08-13

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

## Forward Test 2 — registered 2026-08-17 (scored 2026-08-27; the verdict is appended to `forward-test-2.md`)

Same frozen method, same bars, next wave: raw (FT2) and calibrated (FT2-B) forecasts of
the first *Economist*/YouGov poll to begin fielding after the registration push, expected
to field on or about August 21–24, 2026. Fresh dated era anchor
(`anchor-2026-08-17.txt`, no polling numbers), hashes in `SHA256SUMS`. Protocol and
forecasts: `forward-test-2.md`, `forecast-ft2.json`, `forecast-ft2b.json`.
