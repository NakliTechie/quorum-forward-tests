# Seats by national margin, US House, 2026 maps

## What this is

This curve answers one question. If Democrats win the national two-party House vote by M points, how many seats do they win on the maps in force for November 2026?

You supply M. The curve does not predict M. I built it as of November 2, 2026, from past votes, district partisanship and candidate lists. I used no polls, race ratings, seat forecasts or prediction markets.

The full curve is in `seats_by_margin.csv`, from M = -2 to M = +16 in steps of 0.5.

## Main readings

| M (Democratic margin) | Mean Democratic seats | 80% range | Chance of 218 or more |
|---|---|---|---|
| 0 | 206.5 | 201 to 212 | 0.7% |
| +2 | 212.3 | 207 to 218 | 12.0% |
| +4 | 218.3 | 212 to 224 | 55.3% |
| +6 | 224.9 | 218 to 232 | 92.9% |
| +8 | 232.3 | 225 to 240 | 99.7% |
| +12 | 250.5 | 241 to 260 | 100.0% |

- **Break-even:** the chance of a Democratic majority reaches 50% at M = +3.8. The sensitivity cases below put this between +3.0 and +4.5.
- **Gap to the median district:** at a tied national vote, the median district has a modelled margin of R+5.2. The national margin and the median district margin therefore differ by 5.2 points. Democratic votes pile up in lopsided seats: the mean lean on these maps is D+1.0 in margin terms, and the median lean is R+4.0.
- **Why break-even is below 5.2:** near the median, more seats sit on the Republican side than on the Democratic side. Random error therefore adds more Democratic wins than it removes.
- **Slope of the curve:** near break-even, 1 point of M moves about 3 seats. At M = +10 to +14, 1 point moves about 5 seats, because the baseline has few seats in the first range and more in the second.

## How I built it

1. **District baseline.** I used the Cook 2026 PVI (Partisan Voting Index) for all 435 districts on the 2026 lines. Cook dated this list July 29, 2026. I read it from the district tables in a Wikipedia snapshot dated November 1, 2026. Baseline margin is twice the PVI, because PVI measures share and this model works in margin.
2. **Who is running.** The same tables give the candidates. I marked each seat as Democratic incumbent (183), Republican incumbent (176), open (75) or independent incumbent (1). I marked 19 seats as uncontested by a major party.
3. **District model.** Each contested seat's margin equals a national shift, plus 0.903 times its baseline, plus or minus 4.74 for an incumbent. I fitted this on 2018 to 2024.
4. **Link to M.** For each M, I find the national shift that makes vote-weighted district margins equal M exactly. Weights are the votes each seat is expected to cast. Because the weights are lower in deep-blue seats and uncontested seats count at full margin, the shift is not equal to M.
5. **Simulation.** For each M, I ran 40,000 draws with three error layers, then counted seats. The same random draws serve every M, so the curve is smooth.

## Which maps are in force

The November 1 snapshot gives this list. New maps are in force in 9 states and 173 seats: Alabama, California, Florida, Louisiana, North Carolina, Ohio, Tennessee, Texas and Utah. The October 20 snapshot lists 11 enacted plans: these 9, plus Missouri and Virginia.

**Missouri is an exception to your brief.** The legislature passed a new map, but the 2022 map stays in place for 2026. The US Supreme Court stayed the last order against it on September 25, 2026. Both snapshots report this. Missouri 5 therefore stays at D+12 with its Democratic incumbent running.

**Virginia also keeps its old map.** Voters approved an amendment in April 2026, and the state Supreme Court invalidated it on May 8, 2026. The November 1 snapshot reports this.

I checked the PVI list two ways:

- In the 262 districts in states with unchanged maps, twice the PVI differs from the 2024 presidential margin by 1.1 points on average, with a spread of 1.3. Those margins come from a public table on the 2024 lines (`downloads/pres2024_by_cd_2024lines.csv`). Missouri and Virginia pass this test, which supports their old maps.
- Only the 9 redrawn states show large gaps against the old lines. For the 20 seats in those states that the snapshot's crossover tables list, twice the PVI sits within -0.2 to +4.4 points of the 2024 presidential margin printed for the new lines.

## Parameters and where they came from

| Parameter | Value | Source |
|---|---|---|
| Slope on baseline | 0.903 (standard error 0.008) | Fitted on 1,600 contested seat-elections, 2018 to 2024 |
| Incumbency | 4.74 margin points (standard error 0.26) | Same fit |
| District error, standard deviation | 5.49 points | Residuals of that fit, after removing state effects |
| State error, standard deviation | 2.95 points | Same residuals; shared by all seats in a state |
| Shared error, standard deviation | 0.96 points | Size of the gap between competitive seats and the calibration in 2018 to 2024: +1.33, +1.19, -0.11, +0.70 |
| Turnout against lean | -0.00217 per lean point and -0.00275 per lean point squared over 100, on log votes | Same elections, within state |
| State turnout level | The 2022 level for each state | The last midterm |
| Votes in an uncontested seat | 0.77 of a contested seat with the same lean and state | Median, 2018 to 2024 |
| Votes in an unopposed seat in Florida, Oklahoma, Louisiana | Zero | Those states record no vote for an unopposed candidate |

You asked for a district error and a shared error. I added the state layer because the data show it: seats in one state miss together. Total error per seat is 6.3 points.

Past elections come from the MIT Election Lab returns, 1976 to 2024. Past Cook PVI and incumbents come from archived Wikipedia tables for 2014 to 2024. I cross-checked past PVI against FiveThirtyEight's partisan lean: correlation is 0.996 or higher in 2018, 2020 and 2022.

## Uncontested seats

- **Seats with a known winner:** 17 seats have no Republican and 1 seat has no Democrat. Of the 17, 8 are in California, where two Democrats reached the general election. California 40 has two Republicans.
- **Effect on the national vote:** these seats count at a full 100-point margin with their expected votes. They hold 2.65% of the two-party vote for Democrats and 0.16% for Republicans. Together they add about 2.5 points to M without moving any competitive seat.
- **California 6 is treated separately.** Kevin Kiley, elected as a Republican, runs as an independent against a Democrat. He has no Republican votes, so the seat counts as uncontested in the national vote. The seat itself is simulated as a real race, with Kiley treated as a Republican incumbent.

## Backtest

I ran the same method on four past elections. Parameters came only from elections before the test year, up to the four most recent back to 2014. PVI, who was running and which seats were contested were all known before each election. The actual national margin was the input, as you asked.

| Election | Trained on | Actual M | Predicted mean | 80% range | Actual Democratic seats | Error |
|---|---|---|---|---|---|---|
| 2018 | 2014 to 2016 | +8.72 | 228.1 | 213 to 245 | 235 | -6.9 |
| 2020 | 2014 to 2018 | +3.03 | 224.6 | 214 to 235 | 222 | +2.6 |
| 2022 | 2014 to 2020 | -2.88 | 210.3 | 202 to 219 | 213 | -2.7 |
| 2024 | 2016 to 2022 | -2.78 | 205.8 | 198 to 213 | 215 | -9.2 |

- **Average miss:** 5.35 seats.
- **Direction:** the model under-counted Democrats in 3 of 4 tests, and its mean error was -4.05 seats. Four tests are too few to call that a settled bias, so I report it and do not correct it. The +0.78 row in the sensitivity table shows the effect of a correction: 2 to 3 more Democratic seats at each M, and a break-even near +3.0.
- **Range:** the actual count fell inside the 80% range in 3 of 4 tests. These ranges used the wider shared error of those training windows, 1.69 to 3.18 points.
- **The 2018 miss** traces to old parameters. Incumbency measured from 2014 and 2016 was 10.2 points, about twice the later value. With later parameters the 2018 error is -2.3 (see the second check below).
- **The 2024 miss** is the warning. Competitive seats ran 1.2 points better for Democrats than the calibration said. That accounts for part of the 9-seat miss, and I did not separate the rest.

A second check uses each of 2018 to 2024 as the test and the other three as training. This is a diagnostic, not a backtest, because it uses later elections. Errors were -2.3, -0.7, -3.5 and -9.4, an average miss of 4.0 seats. The 80% range held 3 of 4.

## Variants I tried

I chose the base model before I first computed the 2026 curve. After that first run I corrected one data error: Florida 25 in 2020 carried a vote count of -1. The correction moved the 2020 backtest by 1 seat. The base row of the sensitivity table stayed the same to one decimal place.

| Variant | Average backtest miss | Decision |
|---|---|---|
| Straight line, four elections | 5.35 | Used |
| Straight line, two elections | 5.18 | Not used: the difference is under 0.2 seats, and two elections would drop 2018 from the fit |
| Bent line at lean of +/-30, four elections | 5.88 | Not used |
| Bent line, two elections | 5.22 | Not used |
| Add the average training-year offset to the shift | 7.82 | Rejected |

I also compared turnout sources by how far they pushed the calibrated shift from its value under actual turnout (`turnout_check.py`). Across the four test years, the root mean square error was 1.17 points with the last same-type election, 0.99 with the election two years before, and 1.06 with their average. I kept the same-type election. The sensitivity table shows the choice has little effect on the 2026 curve.

## Sensitivity

Each row changes one assumption. Full numbers are in `sensitivity.csv`.

| Case | Mean at M = 0 | Mean at M = +4 | Mean at M = +8 | Break-even M |
|---|---|---|---|---|
| Base | 206.5 | 218.3 | 232.3 | 3.79 |
| Fit on 2020 to 2024 | 207.1 | 218.6 | 232.6 | 3.69 |
| Fit on 2014 to 2024 | 208.0 | 219.2 | 232.4 | 3.47 |
| Bent line in lean | 207.3 | 219.2 | 233.5 | 3.51 |
| Incumbents on new maps get half the effect | 205.3 | 217.5 | 232.6 | 4.07 |
| Competitive seats beat the calibration by +0.78 | 208.7 | 220.7 | 235.4 | 3.03 |
| State turnout levels from 2018 | 206.4 | 218.2 | 232.3 | 3.80 |
| State turnout levels from 2024 | 206.9 | 218.8 | 232.9 | 3.64 |
| Turnout gap between blue and red seats as flat as 2018 | 205.1 | 216.8 | 230.4 | 4.28 |
| New-map seats run 2 points more Democratic | 208.5 | 220.8 | 235.9 | 3.02 |
| New-map seats run 2 points more Republican | 204.6 | 216.1 | 229.3 | 4.52 |
| No state error | 206.6 | 217.7 | 231.1 | 3.98 |

In 2018 to 2024 I measured no incumbency discount in redrawn states (-0.07 points), so the half-effect row is a stress case.

## What the curve can say

- It says how many seats a given national margin buys on these maps, and how wide the range is from seat-level, state-level and shared error.
- It says where the majority line sits: near M = +3.8, within a range of about +3.0 to +4.5.

## What the curve cannot say

- It says nothing about what M will be.
- Nothing above M = +8.7 has been tested. The only Democratic wave in the data is 2018, so the top half of the curve is an extension of a straight line.
- It knows nothing of candidate quality, money, scandal or local issues.
- It treats the slope and the incumbency effect as known. Year-to-year movement in them is outside the simulation, so the 80% ranges understate the true uncertainty by an amount I did not measure.
- The shared error rests on four values, which is a thin basis.
- It counts Democratic seats only. A seat won by an independent counts as not Democratic. Independents other than Kiley are not modelled.

**Definition of M.** I add a candidate's minor-party ballot lines to their major-party total, as in New York. This gives M values up to 0.17 points away from party-line tallies. For 2024, mine is -2.78 and the party-line figure is -2.63. When you read a real M against this curve, use the same rule, or allow about half a seat.

## Weakest assumption

The weakest assumption is uniform swing: every contested seat moves by the same amount when M moves. This includes the 173 seats on 9 new maps, which have never held a House election. Their baselines track the 2024 presidential vote closely, so a midterm that moves those voters differently breaks the assumption.

The backtest gives direct evidence of this risk. In 2024 competitive seats ran 1.2 points better for Democrats than the calibration said, in the year of the largest miss. A 2-point error in the new-map seats alone moves break-even by about 0.75 points in either direction. That is the largest single sensitivity I found.

## Departures from your brief

- **MIT file.** Harvard Dataverse requires a guestbook form before download. I did not submit a form. I used a public GitHub copy instead, and its MD5 checksum, `a9566ac393913a1af343284e837c17bb`, equals the one Dataverse publishes. The data are CC0.
- **Past years.** I started the panel at 2014, not 1976, because 2014 is the first year whose PVI table my parser reads. The 2012 table has a different layout, and I did not pursue it.
- **Missouri.** See "Which maps are in force".

## How to rerun

`zsh fetch_data.sh downloads` fetches the inputs. I ran these downloads step by step and did not rerun the script as one block. The archive now redirects a header request for the 2024 House snapshot to a post-election capture, so the script checks the revision date in each file and stops if it finds a later one. `zsh run_all.sh` rebuilds every result from `downloads/`, and it ran with exit code 0. A second run of `run_curve.py` produced a byte-identical `seats_by_margin.csv`. `verify_outputs.py` checks the outputs and exits 0: it recomputes the calibration to within 1e-14 points of M and matches the simulated means to a closed-form sum within 0.15 seats. The core code is `seatmodel.py`. `backtest.py` and `run_curve.py` use it.
