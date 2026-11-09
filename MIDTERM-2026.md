# Our 2026 midterm projections

Quorum is an experiment in predicting public opinion and elections with a language model and simulated voters. We give a
fine-tuned open model (Qwen3-14B) about 3,170 voter profiles built from real survey demographics. We ask each profile how it
would vote, then weight and add up the answers. This page lists what we said, when we said it, and how to check it.

*Last updated 2026-11-08, 21:30 IST (the date follow-up and the weekly tally). The voter-group test is scored. The seat and margin read below is early and will change as votes are counted.*

![Our projections for the 2026 US House](capstone/images/projections-card.png)

## Read this first: the date in the prompt moved our number

We found this on Nov 5, after the election. The words "September 11" in the prompt lift our national number by about 2.6 points. The same setup with any other date we tried says about D +6, and that is what the engine said in every other run this season. The registered D +8.54 stands and is scored in December. If it lands close, part of that closeness comes from the date, not from skill. At D +6 the seat table gives about 225, not 234. A follow-up on Nov 7 found that the lift does not need the text's sentence about the war, by a narrow margin, and that January 6 and December 7 did not lift the number. [The evidence is here](capstone/date-sensitivity/README.md).

## What we projected

| Projection | Number | Fixed when | Scored against |
|---|---|---|---|
| National House vote, two-party | **Democrats +8.54** (54.27 to 45.73) | Sep 11, before the election | Certified count, mid-December. Must land within 3 points and beat the polling average (RealClearPolitics, Democrats +8.9). |
| Vote in 17 voter groups | Women 58.8, men 48.9, ages 18-29 61.4, ages 65+ 50.9, White 46.8, Black 83.0, Hispanic 66.8, college graduates 59.1, no degree 50.3, and more | Numbers Sep 11; scoring rule Nov 3, before the polls closed | AP Voter Poll, Nov 5. Group error 6 points or less, lean error 4 or less, and compare with the 2022 pattern. **Scored Nov 5: 2 of 3 hit.** |
| Democratic House seats | **About 234** (80% range 227 to 242) | **After the polls closed**, Nov 4 | Final seat count. This is a conversion of the national number, not an advance forecast. |

We made no Senate or governor projections, and no state-level vote projections.

![Seats by state](capstone/images/seats-by-state-card.png)

## How the seat number was made

A separate AI agent built a district-level table for all 435 seats. Each seat starts from its own Cook 2026 PVI, adjusted for
the incumbent. One national shift then moves every contested seat, set so that the seats add up to the national margin.
40,000 simulated elections add national, state and district error. We read the table at D +8.54. The state card is the same
simulations grouped by state. Quorum's only input is the national number, so these are not state forecasts by Quorum.

The agent saw no 2026 seat count or vote total, but its start-up context did show D +8.54 and one early voter-poll comparison.
That was our error, and [its log](capstone/seats/exposure.md) records it.

## What we know so far

**Voter groups: scored on Nov 5.** Two of three tests hit. [Full verdict](capstone/groups-verdict-2026-11-05.md).

| Test | Bar | Result | Verdict |
|---|---|---|---|
| Group error, 17 groups | 6.0 or less | **3.46** | Hit |
| Lean error, 17 groups | 4.0 or less | **3.25** | Hit |
| Head-to-head against the 2022 pattern, 9 groups | Beat it | 3.07 against 2.65 | Lost, as we said it would be |

- **Biggest misses:** ages 18-29 (61.4 against 74.5), Black voters (83.0 against 90.9), Asian voters (64.5 against 71.7). The age gap is far too narrow: 10.5 against 24.5.
- **Closest:** women (58.8 against 59.6) and Republicans. The gender gap is close: 10.0 against 8.6.
- The source is a survey, not a count, and one election is one data point.

**Seats and the national margin: an early read on Nov 7, not a score.** The count is not final, and the national score comes in mid-December. [Full read](capstone/seats/results-read-2026-11-07.md).

- **National margin:** Cook's vote tracker read D +13.00 on Nov 7, not final. At that figure our D +8.54 is 4.46 off, outside its 3-point bar, and the polling average (+8.9) is 4.10 off, slightly closer than we are. We hit only if the certified margin is +11.54 or lower, and we beat the average only if it is below +8.72.
- **Seats:** our 234 was too low. AP had called 254 for Democrats, and NBC estimated 259 to 176.
- **Where the seat miss came from:** the same seat table read at D +13.0 gives about 256 (range 246 to 266). So about 21 of the 24.5-seat gap to NBC's estimate comes from our national margin, and about 3 from the table. Both parts can still move.
- **States:** at D +8.54, 42 of 50 states sit inside their ranges, 4 are still open, 4 are above (Texas, Ohio, North Carolina, Indiana), and none are below. Ohio went 8 of 15 for Democrats against our range of 4 to 7. At D +13.0, 46 are inside, 3 open, and 1 above (North Carolina).

## Check it yourself

| What | Fixed | Links |
|---|---|---|
| National forecast | Sep 11, 2026 | [commit `50d1d42`](https://github.com/NakliTechie/quorum-forward-tests/commit/50d1d42) · [registration](capstone/capstone-registration.md) · [forecast file](capstone/forecast-capstone-2026-09-11.json) · [news context given to the model](capstone/anchor-capstone-2026-09-11.txt) |
| Polling average to beat | Nov 2, 2026 | [commit `84a2091`](https://github.com/NakliTechie/quorum-forward-tests/commit/84a2091) · [captured figures](capstone/rcp-baseline-2026-11-02.json) |
| Voter-group scoring rule | Nov 3, 2026 | [commit `b4dd863`](https://github.com/NakliTechie/quorum-forward-tests/commit/b4dd863) · [rule](capstone/groups-registration-2026-11-03.md) · [numbers](capstone/groups-forecast-2026-11-03.json) |
| Correction to that rule | Nov 4, 2026 | [errata](ERRATA.md): we named the survey wrongly. No number changed. |
| Voter-group verdict | Nov 5, 2026 | [verdict](capstone/groups-verdict-2026-11-05.md) · [survey table](capstone/survey-ap-voter-poll-2026-11-05.json) · [2022 baseline](capstone/baseline-2022.json) · [scores](capstone/groups-verdict-2026-11-05.json) |
| Date finding | Nov 5, 2026 | [evidence](capstone/date-sensitivity/README.md) · [errata](ERRATA.md) |
| Seat conversion | Nov 4, 2026 | [overview](capstone/seats/README.md) · [method and backtest](capstone/seats/method.md) · [what the agent saw](capstone/seats/exposure.md) · [seats by margin](capstone/seats/seats_by_margin.csv) · [seats by state](capstone/seats/seats_by_state_at_8.54.csv) |
| Early seat and margin read | Nov 7, 2026 | [read](capstone/seats/results-read-2026-11-07.md) · [results by state](capstone/seats/results_by_state_2026-11-07.csv) · [seats by state at D +13.0](capstone/seats/seats_by_state_at_13.0.csv) |
| Weekly poll record | Aug to Oct 2026 | [track record](TRACK-RECORD.md) · [every test and verdict](SCOREBOARD.md) · [checksums](SHA256SUMS) |

Files are hashed in `SHA256SUMS`, and corrections go in new dated entries, never edits. Commit dates are set by the author, so
treat them as our record, which the hashes and GitHub's push history support. The seat code runs from this repository. The model
weights and part of the forecast code are private, so the forecasts themselves cannot be rerun from here.

## Caveats

- **One election is one data point.** A hit or a miss on the national number proves little by itself.
- **The date in the prompt mattered.** Our registration put date noise at about ±1.5 points. The real effect was larger and came from one date: see the top of this page.
- **Turnout is a lookup.** We reweighted to 2022 turnout. It is not a model of the 2026 electorate.
- **Simple rules beat us on weekly approval.** We hit 84 of 96 registered claims, but copying recent polls was closer on the headline number over twelve weeks: 1.75 to 2.08 points off, against our 2.96.
- **The engine is noisy.** Rerunning identical cases moved answers by a median of 1.3 points in one test.
- **Seats are after the fact.** The method missed by 5.35 seats on average across four past elections, under-counted Democrats by about 4, and has never been tested above a margin of +8.7.
- **We have no state detail.** The simulated voters carry four regions, not states.

Comments and corrections are welcome: open an issue on this repository.

---

Population frame derived from Pew Research Center's American Trends Panel, Wave 161. Source: "Pew Research Center's American
Trends Panel". Pew Research Center bears no responsibility for the analyses or interpretations presented here. The opinions
expressed herein, including any implications for policy, are those of the author and not of Pew Research Center.
