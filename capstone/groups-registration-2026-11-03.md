# Capstone voter groups: how we score them on election night

**Registered 2026-11-03, before any 2026 result exists.** It was pushed first to our private repository at 20:27
IST (commit `aac8a3c`) and published here the same evening. The first polls close at 18:00 US Eastern on Nov 3,
which is 04:30 IST on Nov 4. This file adds a scoring rule only. Every number below was fixed on 2026-09-11, when
we published the capstone forecast and its per-profile rows; it is not a new forecast.

## What this tests

The capstone forecast ([registration](capstone-registration.md)) is scored once, in mid-December, on the national
House margin: D+8.54. That registration also published every simulated voter's answer
([rows](rows-capstone-2026-09-11.jsonl)), so the same computation gives the vote by voter group: women, young
voters, Black voters, college graduates and so on. Quorum's claim is accuracy on group breakdowns, so tonight's
voter surveys are a direct test of it.

[`capstone_groups.py`](capstone_groups.py) `forecast` computes the groups from the published rows with the
registered calibration (`HOUSE_BALLOT_NS`, a 2.7534, b 0.4401) and the registered 2022 turnout weights
([capstone-turnout-2022.json](capstone-turnout-2022.json)). It reads no frame file, because each row carries its
weight. A test in our private repository checks that it reproduces the registered topline and the registered
party, sex, age and race breakdowns to 0.05 points.

    PYTHONPATH=<quorum> python3 capstone/capstone_groups.py forecast \
        --rows capstone/rows-capstone-2026-09-11.jsonl --turnout capstone/capstone-turnout-2022.json --out <json>

| File | sha256 |
|---|---|
| [`rows-capstone-2026-09-11.jsonl`](rows-capstone-2026-09-11.jsonl) (registered 2026-09-11) | `e5228474c36754380df26cb930ed2c537f53b2f593b1f8ef394f082e2b2e28a9` |
| [`forecast-capstone-2026-09-11.json`](forecast-capstone-2026-09-11.json) (registered 2026-09-11) | `e14b3c4888dd221b06163fede555c68d469e072ddf80a1befe8aa782b12756f6` |
| [`capstone-turnout-2022.json`](capstone-turnout-2022.json) (registered 2026-09-11) | `6fba47cdcfc1df7a39b1e1919a1bc314e26871e4247d400e6e84ea477db8fd06` |
| [`groups-forecast-2026-11-03.json`](groups-forecast-2026-11-03.json) (this registration's numbers) | `d0475707ec9d25de91669eacb07b526007975a38230216fc88d74d84c0974c18` |
| [`capstone_groups.py`](capstone_groups.py) (forecast and scorer) | `a0d87204b14b58dc0049bd2df888e89f0372ceb95a30ec3d54453a04323d9ad0` |

## Our numbers (two-party Democratic share of the House vote, %)

How to read it: "lean" is the group's Democratic share minus our national share (54.3). A lean of +4.5 for
women means women vote 4.5 points more Democratic than the electorate as a whole.

| Group | D share | Lean | Share of our electorate |
|---|---|---|---|
| Women | 58.8 | +4.5 | 51.3 |
| Men | 48.9 | -5.4 | 47.7 |
| Age 18-29 | 61.4 | +7.1 | 12.7 |
| Age 65+ | 50.9 | -3.4 | 29.0 |
| White | 46.8 | -7.5 | 68.0 |
| Black | 83.0 | +28.7 | 10.0 |
| Hispanic | 66.8 | +12.5 | 12.5 |
| Asian | 64.5 | +10.3 | 4.8 |
| College graduate | 59.1 | +4.8 | 43.6 |
| No college degree | 50.3 | -4.0 | 56.0 |
| White college graduate | 54.3 | +0.0 | 31.5 |
| White no college degree | 40.1 | -14.2 | 36.4 |
| Income under $50,000 | 58.2 | +3.9 | 30.3 |
| Income $100,000 or more | 53.4 | -0.9 | 31.8 |
| Democrats | 94.2 | +40.0 | 29.9 |
| Republicans | 6.2 | -48.1 | 30.0 |
| Independents | 62.2 | +7.9 | 27.7 |

Gaps, reported for information and not scored: gender (women minus men) +10.0; age (18-29 minus 65+) +10.5;
education (college minus no degree) +8.8; white voters by education +14.2; Black minus White +36.2; Hispanic minus
White +20.0.

## The rule, decided now

1. **Source.** The AP VoteCast national U.S. House vote by group, as AP or its partner Fox News publishes it. We
   capture it once, on Thursday Nov 5 between 12:00 and 18:00 IST, after the overnight reweighting to counted
   votes, with a screenshot and a saved page copy. If VoteCast cannot be reached, the order is the NBC News exit
   poll, then the CNN exit poll. The source used is named in the verdict.
2. **Recording.** For each of the 17 groups, D and R as printed. A group the source does not print is recorded
   as null and left out. Independents means the source's "Independent" row, or "Independent or something else"
   if that is its only row. Only D and R are used, renormalized to two-party, the convention of the capstone.
3. **Level score.** The mean absolute error of our 17 group shares against the source. **Bar: 6.0 points**, the
   9-cell bar of the weekly tests.
4. **Lean score.** The mean absolute error of our leans against the source's leans (each group minus the
   source's own national figure). This removes the error the national level puts into every group. **Bar: 4.0.**
5. **Head-to-head.** Our lean error against persistence: the same source's 2022 midterm leans for the same
   groups, which assume the electorate's shape did not change since 2022. Upheld when ours is smaller. The 2022
   table is history and is fetched at scoring; if the same source's 2022 table cannot be found, the fallback is
   Pew Research Center's 2022 validated-voter study, named in the verdict.
6. **Scoring.** `capstone_groups.py score --forecast groups-forecast-2026-11-03.json --survey <capture>.json
   --baseline <2022>.json --out <verdict>.json`, with the capture saved next to it. The capstone's registered
   test, the national margin against the certified count in mid-December, is unchanged by this file.

## What we expect, written now

These are our predictions about our own score, from the gaps above and the weekly tests. They are inference,
not checks.

- Level error about 4 points (a pass), because our national share sits above the polls and every group carries
  part of that.
- Lean error about 4 points (on the bar). Our race and education gaps look narrower than past midterms: Hispanic
  voters too Democratic, and the gap between college graduates and the rest too small.
- Head-to-head not upheld. Group leans move slowly between midterms, so the 2022 table is a hard bar to beat.

## Disclosures

1. One election, one draw. A pass or a miss is one data point.
2. VoteCast is itself a survey of about 100,000 voters, not a count. Its own error is part of what we measure.
3. Our frame is adult citizens reweighted by 2022 turnout, not a model of the 2026 electorate.
4. The frame's age bands are 30-49 and 50-64; surveys print 30-44 and 45-64. Those two groups are not scored.
5. Our overall share computes to 54.28; the registered file says 54.27, because it rounded D and R first.
6. We picked the 17 groups to match what VoteCast usually prints, before seeing any 2026 table.
