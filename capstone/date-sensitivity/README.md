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

## Follow-up, Nov 7: the war sentence and two other dates

We asked two more questions. Does the lift need the Sep 11 text's sentence about the war with Iran? Do two other charged dates, January 6 and December 7, lift the margin too? We wrote the reading rule on Nov 5, before any pass ran, and tightened it on Nov 6 after a review, still before any pass. Four passes ran on one GPU box on Nov 7, 23:07 to 23:25 IST.

| News text | Date in the prompt | Margin |
|---|---|---|
| Sep 11, war sentence removed ([prompt](anchor-nowar-sep11.txt)) | September 11 | **D +9.66** |
| Sep 11, war sentence removed ([prompt](anchor-nowar-sep12.txt)) | September 12 | **D +7.52** |
| Sep 11, full text ([prompt](anchor-jan6.txt)) | January 6, 2026 | **D +5.60** |
| Sep 11, full text ([prompt](anchor-dec7.txt)) | December 7, 2026 | **D +5.38** |

All four numbers are in [date-probe-margins.json](date-probe-margins.json).

**The rule, set before the run.** The war sentence is not needed if the gap between the two war-free passes is +2.0 or more. It is needed if the gap is between −1.0 and +1.0. A date counts as lifting the margin if it reaches D +7.1, which is 1.0 above the D +6.10 reference. We predicted that the war sentence was needed and that neither other date would lift the margin.

**What we found.**
- The gap is +2.14, so by the rule the war sentence is not needed. That half of our prediction was wrong.
- The gap clears its line by only 0.14, on one pass each, so a repeat could land below it.
- Removing the war sentence raised both war-free passes by about 1 point or more.
- Neither January 6 (D +5.60) nor December 7 (D +5.38) reached D +7.1, so neither lifted the margin. That half of our prediction held.

**Limits.** In the January 6 and December 7 prompts only the date changed, so the rest of the text does not fit those dates. That result holds only for these exact prompts. The passes ran on today's software, with the add-on served on top of the base model, so they do not give the Sep 11 run's exact counterfactual. Why the model reacts to "September 11" is still untested.
