# Errata

Corrections to published text. The original files are unchanged; each entry says what was
wrong, what is right, and where to check it. Verdicts (pass or fail) are unaffected unless an
entry says otherwise.

## 2026-09-29 — from an independent review of the record

An independent model (OpenAI Codex, `gpt-6-astra`) read this repository and the project's
private records without seeing our own summary, and reported inconsistencies. Each item below
was checked against the files before it was listed here.

**1. The movement bar never measured movement (FT3–FT7).** It compared the forecast's change
from the previous poll with the real change from the same previous poll. The previous poll
cancels out, so the bar was the approval-topline error with a ±3 limit. Every "movement bar
passed/failed" line in FT3–FT6 is a statement about the topline, not about tracking. From FT8
it is replaced by a **tracking measure**: our own forecast's change since the previous
registration against the poll's change since the previous poll (bar ≤ 3, registered as a
measurement we expect to fail). FT7 is scored as registered, with the tracking measure
reported beside it.

What the tracking evidence already says, from the scored waves (`score-ft*.json`):

| Waves | Poll change | Our calibrated forecast's change |
|---|---|---|
| FT1 → FT2 | +1.0 | −0.8 |
| FT2 → FT3 | 0.0 | −1.5 |
| FT3 → FT4 | +1.0 | +1.5 |
| FT4 → FT5 | +3.0 | +0.5 |
| FT5 → FT6 | −5.0 | −0.7 |

The slope of our change on the real change is **0.16** (1 would be full tracking, 0 a flat
line). The engine barely moves with opinion. We have said so since FT3; this table measures it
properly.

**2. FT5, arm A (14B raw) tally.** `verdict-ft5-2026-09-16.md` prints "FAIL (0/3)". Its net
error (−4.9) passed the ±8 bar, so it is **1/3**. The series tally (42 of 48) already counted
it correctly.

**3. FT5, phi-4 against persistence.** The same file says persistence "lost the 9-cell to both
phi-4 arms". It did not: persistence's 9-cell error (3.11) beat both phi-4 arms (4.23, 5.40).
phi-4's first win over persistence was on the centered **structure** measure (1.59 vs 2.78),
as the file's headline section states.

**4. FT3, persistence "on every quantity".** `forward-test-3.md` says persistence beat both
engines on every quantity that wave. It lost on net: persistence 3.0 against our 0.0 and +0.1.

**5. FT3 date.** The track record said "Registered 2026-08-24". FT3 was committed privately on
Aug 24 and pushed publicly on **Aug 26**, before its target (Aug 28–31) began fielding, as
`forward-test-3.md`'s registration-mechanism note records. `TRACK-RECORD.md` now says so.

## 2026-11-04 — the survey named in the voter-group scoring rule

**What was wrong.** `capstone/groups-registration-2026-11-03.md` names its source as "AP VoteCast" and
calls it a survey of "about 100,000 voters". We wrote both from earlier years and did not check them
before registering.

**What is right.** AP's 2026 survey is the AP Voter Poll: about 80,000 voters in all 50 states, conducted
by SSRS for The Associated Press, ABC News, CBS News, CNN, FOX News Media, NBC News and Versant
([AP article, Nov 3, via PBS](https://www.pbs.org/newshour/politics/ap-voter-poll-how-key-demographic-groups-voted-in-the-2026-midterms)).

**What changes.** No forecast number, bar or scoring step changes. The rule's source order (AP or Fox
News, then NBC, then CNN) now leads to one shared survey: ABC News and NBC News print the same rows.
AP's article prints only some groups, the Fox News address we tried returned a 404, and CNN is unavailable
from our location. We therefore capture the full table from
[ABC News](https://abcnews.com/Elections/polls-2026-us-house-election-results-analysis) in the registered
window, November 5, 12:00 to 18:00 IST, and name that page in the verdict.

**What we did before this entry.** This entry was written after the polls closed. We read ABC's table as it
stood on November 4 at 09:04 IST and ran it through the registered scorer as an informal early read. The
forecast numbers and the rule were already public, so that read could not change them. The registered score
uses the November 5 capture. The original registration file is unchanged.

## 2026-11-05 — what moved the capstone number

**What was wrong.** `capstone/capstone-registration.md`, disclosure 6, puts a 2.5-point swing between the Sep 6 and Sep 11 runs down to "news-valence steering", and says the forecast carries roughly ±1.5 points of anchor-date noise.

**What is right.** Changing only the date in the prompt moved the margin 2.56 and 2.66 points on today's software, and changing the petrol price did almost nothing. The nine other weekly runs gave D +5.9 to +6.7. Evidence: `capstone/date-sensitivity/README.md`.

**What changes.** The registered forecast, its bar and its December score do not change. The registration file is unchanged.

