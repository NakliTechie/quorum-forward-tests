# Early results read, 2026-11-07 about 10:20 to 10:35 IST

**This is a directional read, not a verdict.** The registered national score waits for the certified count (mid-December). The seat figures
below are a conversion made after the polls closed, not a registered forecast. No model parameter changed: `seats_by_state_at_13.0.csv` is the
frozen `seats_by_state.py` read at a new margin, with the same seed and draws.

| Measure | Ours | Latest | Read |
|---|---|---|---|
| National two-party margin | D +8.54 | D +13.00 (Cook, not final) | 4.46 off; the bar is 3.0 |
| Polling average, D +8.9 | Must be beaten | D +13.00 | 4.10 off, 0.36 closer than ours |
| Democratic seats at D +8.54 | 234.5 (227 to 242) | AP 254 called; NBC 252 called, estimate 259 | Called seats are 12 above our top |
| Democratic seats at D +13.0 | 255.8 (246 to 266) | NBC estimate 259 | 3.2 short, inside the range |
| Ohio at D +8.54 | 5.4 of 15 (4 to 7) | 8 of 15, all called | Above the range |
| State card at D +8.54 | 50 states | 42 inside, 4 open, 4 above, 0 below | Above: TX, OH, NC, IN |
| State card at D +13.0 | 50 states | 46 inside, 3 open, 1 above, 0 below | Above: NC |

**Seat gap.** NBC's estimate of 259 less our 234.5 is 24.5 seats. Reading the table at D +13.0 instead of D +8.54 adds 21.3 seats (87% of the gap). The remaining
3.2 seats (13%) lie between the table and NBC's estimate. The backtest under-counted Democrats by about 4 seats on average, so 3.2 is the size that record would suggest.
NBC's 259 is an estimate, and the margin can still move, so both parts can change.

**What the score needs.** A hit needs a certified margin of +11.54 or lower. If 10 million two-party votes remained, they would have to split about R +4.8 to reach it. I have no
reliable figure for the votes left: Wikipedia's turnout of 124 million is marked "citation needed". We beat the polling average only if the certified margin is below +8.72.

**Ohio.** Democrats won three Republican-held districts and kept district 9, so the result beat the model in Ohio. At D +13.0 the frozen model reads Ohio at 6.6 (5 to 8), so 8 sits at the top of that range.

| District | Chance at D +8.54 | Expected margin | Result (NBC, about 97% to 98% in) |
|---|---|---|---|
| 7 | 20% | R +5.4 | D +9.8, flip (Poindexter over Miller) |
| 10 | 28% | R +3.6 | D +1.6, flip (Knickerbocker over Turner) |
| 15 | 20% | R +5.4 | D +6.6, flip (Leonard over Carey) |
| 9 | 74% | D +4.1 | D +5.4, held (Kaptur) |

## Sources, read directly

- **NBC** https://www.nbcnews.com/politics/2026-elections/house-results : 252 D, 162 R, 21 uncalled; estimate 259 to 176, an 83-seat majority; flipped 43 for a net gain of 41; "Last update 11:33 PM ET". State counts are in `results_by_state_2026-11-07.csv`. South Carolina's page shows district 1 flipped, already inside its 2 Democratic seats.
- **AP** https://apnews.com/projects/elections-2026/us-house-results/ : 254 D, 162 R. AP is two seats ahead of NBC on Democratic calls, so the state card uses NBC's table and can trail AP.
- **Cook vote tracker**, table at https://datawrapper.dwcdn.net/7R9TV/3/ : Democrats 63,306,236 (55.66%), Republicans 48,742,701 (42.86%), total 113,736,670. Two-party margin 14,563,535 / 112,048,937 = 13.00. Its seat widget showed 253 to 161.
- **Wikipedia** repeats the same vote totals, cites Cook, and shows 254 to 162.
- **Ohio** https://www.nbcnews.com/politics/2026-elections/ohio-house-results

Not read: CBS (two URLs returned 404). Cook's own page blocked the built-in browser and froze in Chrome, so I read its embedded table directly.

A state counts as "inside" when its called seats plus every uncalled seat stay within the 80% range, "above" when called seats alone exceed the range, and "open" when the uncalled seats decide it.
