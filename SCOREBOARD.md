# Scoreboard

*Moved from the [README](README.md) on 2026-11-09.*

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
| Sep 11–14, 2026 (RV base; approval +3 on the week) | Sep 6, pre-field (`6855b4b`) | 14B raw | 1/3 bars (**topline −6.4** · net −4.9 · **9-cell 6.59**; the verdict file prints 0/3, corrected in [ERRATA](ERRATA.md) item 2) | **FAIL** | [verdict](verdict-ft5-2026-09-16.md) · [protocol](ft5/ft5-registration.md) |
| Sep 11–14, 2026 | Sep 6, pre-field | 14B calibrated | 3/4 bars (**topline −5.4 > 5** · net −2.8 · 9-cell 4.28 · party 8.0) + head-to-head upheld — first calibrated miss | **FAIL** | [verdict](verdict-ft5-2026-09-16.md) |
| Sep 11–14, 2026 | Sep 6, pre-field | **phi-4 challenger** raw · calibrated | raw 2/3 (topline +2.4 · **net +9.7** · 9-cell 4.23); cal 3/4 (topline +4.1 · **net +13.2** · 9-cell 5.40 · party **7.2**) — **head-to-head 3 UPHELD (7.2 < 8.0), head-to-head 4 UPHELD (4.1 < 5.4)**; beat persistence on structure (1.59 vs 2.78) | **FAIL / FAIL — challenger wins both head-to-heads** | [verdict](verdict-ft5-2026-09-16.md) |
| Sep 11–14, 2026 | Sep 6, pre-field | raw+dk (C) · no-anchor (D) · direction (E) · ballot (F) | **C PASS 3/3, dk head-to-head UPHELD** · D expected FAIL met (−11.4) · E 0/4 (Platt arm retired) · F cal margin +0.2 + party 7.5 hit, D-share −6.7 miss | measurements | [verdict](verdict-ft5-2026-09-16.md) |
| Sep 18–21, 2026 (RV base; approval −5 on the week) | Sep 16, pre-field (`64f8ef2`) | 14B raw | 2/3 bars (topline −1.7 · net +3.7 · **9-cell 6.80 > 6**) | **FAIL** | [verdict](verdict-ft6-2026-09-24.md) · [protocol](ft6/ft6-registration.md) |
| Sep 18–21, 2026 | Sep 16, pre-field | 14B calibrated | 4/4 bars (topline −1.1 · net +4.9 · 9-cell 4.12 · party 9.7) + head-to-head upheld | **PASS** | [verdict](verdict-ft6-2026-09-24.md) |
| Sep 18–21, 2026 | Sep 16, pre-field | phi-4 challenger raw · calibrated | raw 0/3 (**topline +7.3 · net +18.6 · 9-cell 8.90**); cal 1/4 (**topline +9.1 · net +22.1 · 9-cell 10.00** · party 11.3) — **head-to-heads 3, 4 and 5 all NOT upheld** (the 14B won each) | **FAIL / FAIL** | [verdict](verdict-ft6-2026-09-24.md) |
| Sep 18–21, 2026 | Sep 16, pre-field | raw+dk (C) · no-anchor (D) · direction_dk (E) · ballot (F) | C 2/3 (9-cell 6.99), dk head-to-head UPHELD · D expected FAIL met (−6.4) · **E direction_dk PASS −3.1** (first direction pass) · F cal margin −3.1 + party 7.4 hit, D-share −7.3 miss | measurements | [verdict](verdict-ft6-2026-09-24.md) |
| Sep 25–28, 2026 (RV base; approval +1 on the week) | Sep 24, pre-field (`7c3965b`) | 14B raw | 3/3 bars (topline −2.5 · net +2.9 · 9-cell 5.61) — first raw 9-cell pass since FT2 | **PASS** | [verdict](verdict-ft7-2026-10-01.md) · [protocol](ft7/ft7-registration.md) |
| Sep 25–28, 2026 | Sep 24, pre-field | 14B calibrated | 4/4 bars (topline −1.7 · net +4.7 · 9-cell 3.39 · party 8.0) + head-to-head upheld; last week's poll carried forward beat it on every quantity | **PASS** | [verdict](verdict-ft7-2026-10-01.md) |
| Sep 25–28, 2026 | Sep 24, pre-field | phi-4 challenger raw · calibrated | raw 0/3 (**topline +6.3 · net +17.5 · 9-cell 7.19**); cal 1/4 (**topline +8.1 · net +21.1 · 9-cell 8.39** · party 10.9) — **head-to-heads 3, 4 and 5 all NOT upheld** (the 14B won each) | **FAIL / FAIL** | [verdict](verdict-ft7-2026-10-01.md) |
| Sep 25–28, 2026 | Sep 24, pre-field | raw+dk (C) · no-anchor (D) · direction_dk (E) · ballot (F) | **C PASS 3/3**, dk head-to-head UPHELD · D expected FAIL met (−7.5) · **E direction_dk PASS −2.9** (second pass) · F cal margin −2.6 + party 8.3 hit, D-share −7.5 miss | measurements | [verdict](verdict-ft7-2026-10-01.md) |
| Oct 2–5, 2026 (RV base; approval +2 on the week) | Sep 29, pre-field (`ef7aef3`) | 14B raw | 2/3 bars (topline −4.5 · net −1.0 · **9-cell 6.84 > 6**) | **FAIL** | [verdict](verdict-ft8-2026-10-07.md) · [protocol](ft8/ft8-registration.md) |
| Oct 2–5, 2026 | Sep 29, pre-field | 14B calibrated | 4/4 bars (topline −3.6 · net +0.8 · 9-cell 4.97 · party 7.9) + head-to-head upheld; **tracking measure** (first scored): engine +0.1 vs poll +2.0, inside 3 on a quiet week — season slope 0.164, not tracking; Z1, Z2, Z3 and last week's poll all beat it on the topline | **PASS** | [verdict](verdict-ft8-2026-10-07.md) |
| Oct 2–5, 2026 | Sep 29, pre-field | phi-4 challenger raw · calibrated (last wave; retired from FT9) | raw 2/3 (topline +4.3 · **net +13.5** · 9-cell 5.84); cal 1/4 (**topline +6.0 · net +17.0 · 9-cell 7.00** · party 9.5) — **head-to-heads 3, 4 and 5 all NOT upheld**; FT5–FT8: 2 of 11 | **FAIL / FAIL** | [verdict](verdict-ft8-2026-10-07.md) |
| Oct 2–5, 2026 | Sep 29, pre-field | raw+dk (C) · no-anchor (D) · direction_dk (E) · ballot (F) · YouGov-weighted companion | C 2/3 (9-cell 6.18), dk head-to-head UPHELD · D expected FAIL met (−9.4) · **E direction_dk FAIL −5.7** (registered −1 to −5: expectation wrong; direction rose 3) · F cal margin −3.7 + party 10.1 hit, D-share −9.6 miss · companion 36.2 (−1.8), net +4.2 | measurements | [verdict](verdict-ft8-2026-10-07.md) |
| Oct 10–12, 2026 (RV base; approval flat on the week) | Oct 8, pre-field (`f0552aa`) | 14B raw | 3/3 bars (topline −4.4 · net +0.2 · 9-cell 5.93) | **PASS** | [verdict](verdict-ft9-2026-10-15.md) · [protocol](ft9/ft9-registration.md) |
| Oct 10–12, 2026 | Oct 8, pre-field | 14B calibrated | 4/4 bars (topline −3.3 · net +2.5 · 9-cell 3.96 · party 8.8) + head-to-head upheld; tracking: engine +0.3 vs poll 0.0, inside 3 on a flat week — season slope 0.160; Z1, Z2, Z3 and last week's poll all beat it on the topline (H2H-Z not upheld, as registered) | **PASS** | [verdict](verdict-ft9-2026-10-15.md) |
| Oct 10–12, 2026 | Oct 8, pre-field | ygdk (our answers re-weighted to YouGov's party mix + the not-sure fix) · poll-only rules Z1, Z3 | ygdk 2/2 (topline **0.0** · net +4.5), H2H-Y UPHELD (beat B by 3.3) · Z1 38 (0.0) 2/2 · Z3 37.25 (−0.75) 2/2 | **PASS** | [verdict](verdict-ft9-2026-10-15.md) |
| Oct 10–12, 2026 | Oct 8, pre-field | raw+dk (C) · no-anchor (D) · direction_dk (E) · ballot (F, F2) · YouGov-weighted companion | **C PASS 3/3**, dk head-to-head UPHELD · D expected FAIL met (−9.5) · **E direction_dk PASS −3.2** (registered expectation FAIL: wrong; direction fell 3) · F cal margin −1.7 + party 11.2 hit, D-share −8.7 miss · **F2 PASS 3/3** (D-share −2.1 · margin 0.0 · party 5.2), H2H-F2 UPHELD · companion 36.5 (−1.5) | measurements | [verdict](verdict-ft9-2026-10-15.md) |
| Oct 19–20, 2026 (RV base; approval +2 on the week) | Oct 14, pre-field (`07e3d97`) | 14B raw | 1/3 bars (**topline −6.7** · net −4.2 · **9-cell 7.11 > 6**) | **FAIL** | [verdict](verdict-ft10-2026-10-25.md) · [protocol](ft10/ft10-registration.md) |
| Oct 19–20, 2026 | Oct 14, pre-field | 14B calibrated | 3/4 bars (**topline −5.8** · net −2.4 · 9-cell 5.21 · party 11.7) + head-to-head upheld; tracking: engine −0.5 vs poll +2.0, inside 3 — season slope 0.135; Z1, Z2, Z3 and last week's poll all beat it on the topline (H2H-Z not upheld, as registered) | **FAIL** | [verdict](verdict-ft10-2026-10-25.md) |
| Oct 19–20, 2026 | Oct 14, pre-field | ygdk (our answers re-weighted to YouGov's party mix + the not-sure fix) · poll-only rules Z1, Z3 | ygdk 2/2 (topline −2.5 · net −0.4), H2H-Y UPHELD (beat B by 3.3) · Z1 38 (−2.0) 2/2 · Z3 37.25 (−2.75) 2/2 | **PASS** | [verdict](verdict-ft10-2026-10-25.md) |
| Oct 19–20, 2026 | Oct 14, pre-field | raw+dk (C) · no-anchor (D) · direction_dk (E) · ballot (F, F2) · YouGov-weighted companion | C 1/3 (topline −5.1 · 9-cell 6.20), dk head-to-head UPHELD · D expected FAIL met (−11.5) · **E direction_dk PASS −4.1** (registered expectation FAIL: wrong again) · F cal margin +0.6 + party 10.0 hit, D-share −7.5 miss · **F2 PASS 3/3** (D-share −0.8 · margin +2.5 · party 5.0), H2H-F2 UPHELD · companion 36.0 (−4.0) | measurements | [verdict](verdict-ft10-2026-10-25.md) |
| Oct 23–26, 2026 (RV base; approval −1 on the week) | Oct 21, pre-field (`d5ff073`) | 14B raw | 1/3 bars (**topline −5.6** · net −4.3 · **9-cell 6.76 > 6**) | **FAIL** | [verdict](verdict-ft11-2026-10-29.md) · [protocol](ft11/ft11-registration.md) |
| Oct 23–26, 2026 | Oct 21, pre-field | 14B calibrated | 4/4 bars (topline −4.8, inside ±5 by 0.2 · net −2.6 · 9-cell 5.04 · party 8.9) + head-to-head upheld; tracking: engine 0.0 vs poll −1.0, inside 3 — season slope 0.126; Z1, Z2, Z3 and last week's poll all beat it on the topline (H2H-Z not upheld, as registered) | **PASS** | [verdict](verdict-ft11-2026-10-29.md) |
| Oct 23–26, 2026 | Oct 21, pre-field | ygdk (our answers re-weighted to YouGov's party mix + the not-sure fix) · poll-only rules Z1, Z3 | ygdk 2/2 (topline −1.7 · net −0.9), H2H-Y UPHELD (beat B by 3.1) · Z1 38 (−1.0) 2/2 · Z3 36.75 (−2.25) 2/2 | **PASS** | [verdict](verdict-ft11-2026-10-29.md) |
| Oct 23–26, 2026 | Oct 21, pre-field | raw+dk (C) · no-anchor (D) · direction_dk (E) · ballot (F, F2) · YouGov-weighted companion | **C PASS 3/3** (9-cell 5.92), dk head-to-head UPHELD · D expected FAIL met (−10.5) · **E direction_dk FAIL −5.4** (registered expectation about −6 FAIL: met; direction rose 1 to 29) · F cal margin −0.5 + party 10.0 hit, D-share −8.5 miss · **F2 PASS 3/3** (D-share −1.9 · margin +1.3 · party 5.9), H2H-F2 UPHELD · companion 35.9 (−3.1) | measurements | [verdict](verdict-ft11-2026-10-29.md) |
| Nov 4–6, 2026 (RV base, 3,166; first poll after the election; approval −3 over two weeks) | Oct 28, pre-field | 14B raw | 3/3 bars (topline −2.5 · net +3.0 · 9-cell 4.39) | **PASS** | [verdict](verdict-ft12-2026-11-08.md) · [protocol](ft12/ft12-registration.md) |
| Nov 4–6, 2026 | Oct 28, pre-field | 14B calibrated | 4/4 bars (topline −1.5 · net +4.9 · 9-cell 2.42 · party 8.6) + head-to-head upheld; tracking: engine +0.3 vs poll −3.0, **outside 3** — season slope 0.081; beat Z1, Z2 and Z3 on the topline (H2H-Z upheld, as the registration's conditional said) | **PASS** | [verdict](verdict-ft12-2026-11-08.md) |
| Nov 4–6, 2026 | Oct 28, pre-field | ygdk (our answers re-weighted to YouGov's party mix + the not-sure fix) · poll-only rules Z1, Z3 | ygdk 2/2 (topline +1.6 · net +6.8), H2H-Y not upheld (1.6 against B's 1.5) · Z1 39 (+3.0) 2/2 · Z3 38.75 (+2.75) 2/2 | **PASS** | [verdict](verdict-ft12-2026-11-08.md) |
| Nov 4–6, 2026 | Oct 28, pre-field | raw+dk (C) · no-anchor (D) · direction_dk (E) · ballot (F, F2) · YouGov-weighted companion | **C PASS 3/3** (9-cell 4.50), dk head-to-head UPHELD · D expected FAIL met (−7.5) · **E direction_dk PASS +1.7** (direction fell 7 to 22) · ballot scored against a recalled vote, not an intention: F cal margin −5.7, D-share −14.6, party 14.8, all miss · **F2 2/3** (margin −3.9 · party 8.5 · D-share −8.0 miss), H2H-F2 UPHELD · companion 36.2 (+0.2) | measurements | [verdict](verdict-ft12-2026-11-08.md) |

### Gallup — satisfaction with the way things are going · monthly

| Poll (fields) | Registered | Engine | Result | Verdict | Detail |
|---|---|---|---|---|---|
| September 2026 (Sept 1–17) | Aug 29, pre-field (`4881748`) | raw + calibrated | published **21** satisfied: raw 35.7 (**+14.7**), calibrated 48.7 (**+27.7**), bar ±5; last month's poll exact (0.0); party claims pending until Gallup publishes party figures | **FAIL / FAIL** (0 of 2 scored, 2 pending) | [verdict](gs1/verdict-gs1-2026-10-02.md) · [protocol](gs1/gallup-satisfaction-registration.md) |

### Harvard CAPS/Harris — approval, right track, generic ballot · roughly monthly

| Poll (fielded) | Registered | Arms | Result | Verdict | Detail |
|---|---|---|---|---|---|
| September 2026 (Sep 26–28, 2,200 RV) | Aug 29, pre-field (`4881748`) | HH1 raw + house-adjusted | **5 of 8**: approve raw −4.7, adjusted +2.5 · net raw −5.8, **adjusted +8.4 miss** · **right track −10.5 miss** · ballot D −3.4 · **adjusted party MAE 14.2 miss** · head-to-head (adjusted beats raw) upheld | **FAIL** | [verdict](hh1/verdict-hh1-2026-10-01.md) · [protocol](hh1/hh1-registration.md) |
| September 2026 | Sep 3, pre-field (`b35d880`) | HH1-B companions | **approval_cal PASS 3/3** (approve 0.0 · net +3.6 · party 1.47) · cal+house 1/3 (+7.2 · +17.9 · 7.67) · direction_dk −4.2 hit · ballot_cal +2.4 hit · head-to-heads 1 and 3 upheld, 2 not upheld (as registered) | companion, reported | [verdict](hh1/verdict-hh1-2026-10-01.md) · [protocol](hh1/hh1b-registration.md) |
| October 2026 (Oct 24–26, 2,700 RV) | Oct 6, pre-field (`e3ed905`) | HH2 raw + calibrated (house offset dropped) | **7 of 10**: approve raw −2.2, cal +2.2 · net raw 0.0, **cal +8.7 miss** · **right track raw −9.9 miss**, direction_dk −4.0 · **ballot D raw −4.8 miss**, cal +1.4 (ballot printed among likely voters) · cal party MAE 6.27 · head-to-head (cal party beats raw) upheld | **FAIL** | [verdict](hh2/verdict-hh2-2026-10-28.md) · [protocol](hh2/hh2-registration.md) |

### The November 3, 2026 midterm — national House popular-vote margin · the capstone

| Registered | Quantity | Forecast | Bar / head-to-head | Verdict | Detail |
|---|---|---|---|---|---|
| Sep 11, 2026, pre-election | two-party House vote, D − R | **D+8.54** (D 54.27 / R 45.73) | ±3.0 · beats the RealClearPolitics generic-ballot average as of Nov 2, captured Nov 2: **D+8.9** (52.0 / 43.1) | *scored Dec 2026, when ≥ 99% counted* | [registration](capstone/capstone-registration.md) · [forecast](capstone/forecast-capstone-2026-09-11.json) · [rows](capstone/rows-capstone-2026-09-11.jsonl) · [RCP baseline](capstone/rcp-baseline-2026-11-02.json) |
| Nov 4, 2026, **after polls closed** (a conversion, not a forecast) | Democratic House seats at the registered margin | **about 234** (80% range 227 to 242) | none registered | *compared with the final seat count* | [overview](capstone/seats/README.md) · [method](capstone/seats/method.md) · [what the agent saw](capstone/seats/exposure.md) |
| Nov 3, 2026, before polls close (numbers fixed Sep 11) | two-party House vote in 17 voter groups (women, 18-29, Black, college graduates ...) | women 58.8 · men 48.9 · White 46.8 · Black 83.0 · Hispanic 66.8 · college 59.1 · no degree 50.3 (D share) | group error ≤ 6.0 · lean error ≤ 4.0 · beats 2022 leans | *scored Nov 5 against the AP Voter Poll ([errata](ERRATA.md))* | [registration](capstone/groups-registration-2026-11-03.md) · [numbers](capstone/groups-forecast-2026-11-03.json) |

One number, one bar, scored once. Turnout is a declared 2022-CPS reweight (the table and
its script are in `capstone/`). The registration put the anchor-date sensitivity at ±1.5; after the
election we found that the date in the prompt moves the number about 2.6 points ([date sensitivity](capstone/date-sensitivity/README.md), [errata](ERRATA.md)).

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
