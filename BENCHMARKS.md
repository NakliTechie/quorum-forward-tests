# The engine against simple poll rules

*Moved from the [README](README.md) on 2026-11-09.*

A forecast is only worth something if it beats the obvious rules that need no model. We
score the 14B calibrated arm (B) against three, all computed from published E/YouGov
toplines by `score_ft.py --benchmark-series` (private repo; numbers reproducible from
`tracking.csv`). **Z1** is the last poll published before the registration push, the
honest same-time competitor. **Z2** is the wave just before the target; it is known only at
scoring, because FT2, FT5, FT8 and FT11 were pushed before that wave published. **Z3** is the mean
of the last four polls published before the push.

| Registration | Target wave | Published | **14B calibrated (B)** | Z1 last poll known at push | Z2 wave before target | Z3 mean of last 4 known |
|---|---|---|---|---|---|---|
| FT1 | Aug 14–17 | 35 | 34.9 (−0.1) | 33 (−2.0) | 33 (−2.0) | 34.75 (−0.25) |
| FT2 | Aug 21–24 | 36 | 34.1 (−1.9) | 33 (−3.0) | 35 (−1.0) | 34.75 (−1.25) |
| FT3 | Aug 28–31 | 36 | 32.6 (−3.4) | 36 (0.0) | 36 (0.0) | 35 (−1.0) |
| FT4 | Sep 4–8 | 37 | 34.1 (−2.9) | 36 (−1.0) | 36 (−1.0) | 35 (−2.0) |
| FT5 | Sep 11–14 | 40 | 34.6 (−5.4) | 36 (−4.0) | 37 (−3.0) | 35 (−5.0) |
| FT6 | Sep 18–21 | 35 | 33.9 (−1.1) | 40 (+5.0) | 40 (+5.0) | 37.25 (+2.25) |
| FT7 | Sep 25–28 | 36 | 34.3 (−1.7) | 35 (−1.0) | 35 (−1.0) | 37 (+1.0) |
| FT8 | Oct 2–5 | 38 | 34.4 (−3.6) | 35 (−3.0) | 36 (−2.0) | 37 (−1.0) |
| FT9 | Oct 10–12 | 38 | 34.7 (−3.3) | 38 (0.0) | 38 (0.0) | 37.25 (−0.75) |
| FT10 | Oct 19–20 | 40 | 34.2 (−5.8) | 38 (−2.0) | 38 (−2.0) | 37.25 (−2.75) |
| FT11 | Oct 23–26 | 39 | 34.2 (−4.8) | 38 (−1.0) | 40 (+1.0) | 36.75 (−2.25) |
| FT12 | Nov 4–6 | 36 | 34.5 (−1.5) | 39 (+3.0) | 39 (+3.0) | 38.75 (+2.75) |
| FT13 | Nov 13–16 (pending) | — | 33.3 | 36 | known at scoring | 38.25 |
| **Mean abs. error, 12 waves** | | | **2.96** | 2.08 | 1.75 | 1.85 |

**Read plainly: on the approval topline the engine does not beat simple poll rules.** It
beat Z1 in 4 of 12 waves and Z2 and Z3 in 3 of 12. Its mean error (2.96) is behind Z1 (2.08),
Z2 (1.75) and Z3 (1.85). On FT8–FT11 all three rules beat it, including FT11, where the engine
passed its own ±5 bar. The engine wins when the poll falls back toward the engine's fixed level
(FT6, and FT12, when approval fell 3 points to 36). It loses when the poll sits above that level
(FT3–FT5, FT8–FT11). A retrodiction over the 22 waves before FT1 (known answers, frozen pipeline; not in
this repository) put the calibrated engine at 1.59 against Z2's 1.77. Forward, the order has
reversed. Z2 also beat the engine on party error in each of FT4–FT12 (verdict files). The
engine's case therefore rests on what these rules cannot do at all: questions with no recent
poll to carry forward.

**Declared 2026-10-01, before FT8's target begins fielding:** every verdict from FT8 on
reports Z1, Z2 and Z3 beside the engine on the approval topline. FT8's Z1 (35) and Z3 (37.0)
are fixed by rule at its push and stated above.

**Measurement companion, published before FT8 fields:** the same FT8 answers re-weighted
to YouGov's own printed targets (party 31 D / 33 R, registered voters only) forecast
**36.2** approve / 54.0 disapprove, against B's 34.4 / 55.6. In retrodiction on FT1–FT7 it
cut the topline miss to 1.43 but pushed net past ±8 on 3 of 7 waves. It is reported, not
counted: [`ft8/ft8-companion-ygframe.md`](ft8/ft8-companion-ygframe.md).
