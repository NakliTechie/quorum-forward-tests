# The date in the prompt moved our national number

**Found 2026-11-05, after the election.** This does not change the registered forecast, which stays D +8.54 and is scored once against the certified count.

Our Sep 11 forecast was about 2.3 points above the nine other weekly ballot runs of that season, which gave D +5.9 to +6.7 ([all ten](weekly-runs-through-capstone-method.json)). Their setup was the same and their news text almost the same, so we re-ran them. Each pass below is a fresh run of all 3,170 profiles through the registered capstone computation, on one GPU box, on today's software.

| News text | Date in the prompt | Petrol | First run | Re-run |
|---|---|---|---|---|
| Sep 11 | September 11 | $4.28 | D +8.56 unrounded | **D +8.66**, and **D +8.66** again |
| Sep 11 | September 12 | $4.28 | not run before | **D +6.10** |
| Sep 6 | September 11 | $4.15 | not run before | **D +8.76** |
| Sep 6 | September 6 | $4.15 | D +5.96 | D +6.10 |
| Sep 24 | September 24 | | D +6.12 | D +6.42 |
| Oct 14 | October 14 | | D +6.46 | D +6.48 |
| Oct 28 | October 28 | | D +6.08 | D +6.08 |

Changing only the date moved the margin 2.56 and 2.66 points. The two swap prompts are [here](anchor-swap-a.txt) and [here](anchor-swap-b.txt). We wrote the rule for reading this before the run ([repeat margins](repeat-margins.json), [swap margins](swap-margins.json)).

**What we can say.** The Sep 11 number repeats, ordinary weeks repeat, and the words "September 11" lift the margin on today's software.

**What we cannot say.** Why the model reacts this way, whether other dates do the same, or exactly how much the date added to the original run, since the software has changed since September. We expected the Sep 11 number not to repeat, and that prediction was wrong.
