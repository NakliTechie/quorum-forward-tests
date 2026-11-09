# The main test (UQ1): group breakdowns on questions nobody polls weekly

**What it tests.** Given only a question's wording and answer options, the engine predicts how each demographic and
party group answers relative to the whole sample. It must beat a wording-blind baseline built from past crosstabs by
a practical margin. The questions come from 12 weekly Economist/YouGov polls (slots Oct 5 to Dec 21, 2026). For each
poll we take its new questions from the published report, forecast them from the wording alone before any result
cell is read, push the forecast, and only then score it. Each scored week is sealed unread; the verdict reads every week once, after the
last one. The forecasts and seals sit in our private repository until then.

## The frozen protocol

The study's protocol and frozen inputs were fixed in `uq1/freeze.json` on 2026-10-06 at 12:42 IST (private commit
`56b902b`). Its sha256:

```
a329dc217c157e0c44abfe561b57d15612c178f7ca7157b988ec92972375d2b9  uq1/freeze.json
```

**What this proves.** We published this hash on 2026-11-09, after five of the twelve weeks were sealed. So it shows
that the protocol does not change between this commit and the verdict. It does not show anything about Oct 6 to
Nov 9. The private commit date says the file was frozen on Oct 6; that date is set by us, not by a third party. At the
verdict we publish `uq1/freeze.json` itself, so anyone can check it against this hash.

**Where the study stands (Nov 9).** Five weekly slots are sealed (Oct 5, Oct 12, Oct 19, Oct 26, Nov 9; the Nov 9 slot
holds the Nov 4–6 post-election poll). One is excluded, because no Oct 30–Nov 2 poll fielded. Six remain, Nov 16 to
Dec 21. Two questions the frozen extractor admitted are personal-profile items (home ownership; whether the respondent
voted in 2026). The protocol excludes profile items, so both leave the primary analysis, recorded before their weeks'
forecasts; their scores are kept for a sensitivity report.

## A repeat test of our own engine: not repeated

**What we did.** Part of the study (S1) asks older poll questions again. On Nov 7 we ran one week's S1 inputs a second
time, unchanged: the same 74 questions and 92 answer rows, the same anchor text, code and settings, on different
GPU boxes from the first run. Before the second run, we wrote down how to read it: it "repeated" only if every one of
the four engine versions stayed within 0.01 on every saved probability and within 0.2 points on every group share.
We predicted it would repeat.

**What we found.** It did not repeat, so the prediction was wrong.

| Engine version | Rows exactly equal | Largest probability difference | Largest group-share difference (points) |
|---|---|---|---|
| E1 | 91 of 92 | 0.031 | 0.14 |
| E0 | 87 of 92 | 0.056 | 0.76 |
| E2 | 91 of 92 | 0.031 | 0.15 |
| E2b | 91 of 92 | 0.030 | 0.2003, just over 0.2 |

Across the four versions, 360 of 368 rows came back exactly equal, and the median group-share difference is 0 in every
version. The differences sit in 8 rows, and inside those rows only some simulated people changed. Our pre-set rule
names no cause. A check outside the rule rejected one explanation (that the changed rows sit where an interrupted run
resumed): one version ran without any resume and still changed one row.

**What it means for our numbers.** Rerunning the same forecast does not always give the same answer. On this test the
largest change to a group's share was 0.76 points, and almost all rows were identical. Our weekly approval tests use
another serving setup, which varies more: about 1.3 points on party figures in an Oct 29 check. Read small differences
between our forecasts with that in mind.
