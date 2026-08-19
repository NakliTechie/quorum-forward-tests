# Quorum Forward Test 1 — Registered Pre-Field Forecast (Economist/YouGov approval)

**Registered: 2026-08-13, BEFORE the target poll begins fielding.** This document plus the
frozen forecast JSON (sha256 below, added at freeze) constitute the registration. Nothing
in the method is altered after the target poll fields; the verdict is published either way.

## Target

The **next Economist/YouGov weekly poll** to begin fielding after this registration's
timestamp (expected to field on or about **August 14–17, 2026**, publishing the following
week — the series' standing Friday–Monday cadence), specifically its presidential job
approval question:

> "Do you approve or disapprove of the way Donald Trump is handling his job as President?"
> Strongly approve / Somewhat approve / Somewhat disapprove / Strongly disapprove / Not sure

(Wording and options verbatim from the Economist/YouGov June 5–8, 2026 toplines PDF;
unchanged in the July 31–August 3, 2026 tab report.)

## Registered quantities

From the target wave's published toplines and crosstabs, among U.S. adult citizens:

1. **Topline**: Approve, Disapprove, Net (Approve − Disapprove).
2. **Crosstabs**: Approve share by Sex (Male / Female), Age (18-29 / 30-44 / 45-64 /
   65+), and Race (White / Black / Hispanic) — 9 registered subgroup cells.
3. **Party ID cuts (Dem / Ind / Rep) are published in the same forecast file but are
   EXPLORATORY, not registered.** Disclosure: a pre-registration dry run of the frozen
   method showed the model's party-conditional spread is strongly compressed relative to
   any published wave (a known zero-shot conditioning weakness); the party cuts were
   moved out of the registered set BEFORE registration, the bars below never applied to
   them, and they are published unregistered so the weakness is visible rather than
   hidden. Sharpening party conditioning is named future work for Forward Test 2+.

## Scoring rule and success bars (declared now)

- Topline Approve absolute error ≤ **5 points**; Net absolute error ≤ **8 points**
  (bars set from the method's frozen Feb-2025 calibration, W161 ±5).
- Registered-subgroup mean absolute error (9 cells: sex, age, race) ≤ **6 points**.
- All errors computed against the published figures as printed; no adjustments.
- **The result is published whether it passes or fails.** Misses are reported with the
  same prominence as hits.

## Method (frozen at registration)

- **Engine**: Qwen3-14B + the Quorum fine-tuned adapter, soft first-token distribution
  over the five option digits — the elicitation that recovered the Pew ATP W161 (Feb 2025)
  approval topline within ±5 points. **No 2026 polling data enters the model, the prompt,
  or any calibration step.**
- **Population frame**: Pew Research Center's American Trends Panel, Wave 161 (Feb 2025)
  demographic microdata with survey weights (census weighting inherited from Pew).
  Distinct demographic+party profiles, weights summed. Research use; cited per license.
- **Prompt** = profile line + era anchor + the exact target question/options. The era
  anchor is one paragraph of verifiable public facts **containing no polling numbers**;
  its sha256 is pinned in the manifest and below.
- **Aggregation**: weight-averaged soft distributions; crosstabs from the same per-profile
  distributions grouped by the frame's party/sex/age/race.
- Code: `quorum/twin/forecast.py` at the registration commit (sha in the repo tag).

## Declared limitations

- The frame's party composition is Feb-2025; drift since is unmodeled.
- ATP age bands (30-49/50-64) map approximately onto YouGov bands (30-44/45-64).
- "Not sure" is modeled as a first-class option; models typically under-allocate to it.
- Single-wave calibration (W161). This is Forward Test **1**; the point is the series.

## Registration mechanics

- Anchor sha256: `293d2f7cb3574da15b450ebcd5f11bb11c3679007e823c4fc612aa30ca7c4191`
- Forecast JSON sha256: `eec02e1510edfa2cad621fd4bae6a71ee6dabbdc76af647d060435bbef6dfeb1`
- Public timestamp: OSF registration + public post of this document's hash (performed by
  Chirag; Quorum's repo is private, so the hash post is the public commitment).

## Verdict (to be appended when the target wave publishes)

**PASS — scored 2026-08-19 against the Economist/YouGov poll fielded August 14-17, 2026**
(n = 1,611; toplines question 31; tab report table 31, page 45;
[article](https://yougov.com/en-us/articles/55390-democrats-midterms-lead-war-military-iran-cuba-august-14-17-2026-economist-yougov-poll) ·
[toplines PDF](https://d3nkl3psvxxpe9.cloudfront.net/documents/econtoplines_8q3E3LQ.pdf) ·
[tabs PDF](https://d3nkl3psvxxpe9.cloudfront.net/documents/econTabReport_jNjXIL6.pdf)).
This is the first wave that began fielding after this document's public timestamp, i.e.
the registered target. Scored by the scorer committed before publication
(`score_forward_test.py`); inputs and output published beside this file
(`published-2026-08-14-17.json`, `score-ft1-2026-08-19.json`).

| Registered quantity | Forecast | Published | Error | Bar | Result |
|---|---|---|---|---|---|
| Topline Approve | 33.6 | 35.0 | −1.4 | ≤ 5 | **pass** |
| Net (Approve − Disapprove) | −22.2 | −26.0 | +3.8 | ≤ 8 | **pass** |
| Sex/age/race 9-cell MAE | — | — | 4.14 | ≤ 6 | **pass** |

9-cell detail (forecast − published): Male −3.0, Female −0.6; 18-29 +2.3, 30-44 +6.3,
45-64 −5.6, 65+ −8.7; White −3.4, Black +5.2, Hispanic −2.2.

**Party cuts (exploratory, never scored, published as pledged):** forecast 24.1 / 31.4 /
46.3 (Dem/Ind/Rep) vs published 4.0 / 21.0 / 80.0 — MAE 21.4. This is the raw engine's
party compression, disclosed at registration and the reason the calibrated companion
(Forward Test 1-B) exists; its registered party cuts are scored in `forward-test-1b.md`.

### Context: the persistence benchmark (added at scoring, before publication)

Presidential approval is polled weekly, so the cheapest possible "forecast" is last
week's wave. For honesty we state it ourselves: the previous Economist/YouGov wave
(fielded Aug 7-10: 33 approve / 62 disapprove / net −29; party Dem 4 / Rep 79) predicts
this wave with topline error 2.0, net error 3.0, and near-zero party error. On net,
persistence beats both of our forecasts; on topline, ours edge it. Persistence, however,
is not a simulation — it is the fielded poll re-used, and it exists only for questions
already being polled every week. Quorum's engine consumed no 2026 polling data (the
anchor is sha-pinned and number-free; calibration was fitted on 2019 and 2025 gold), and
its product surface is questions with no last-week's-number to copy. Approval is the
proving ground because gold exists to score against; the persistence column is published
so readers can see exactly how informative that proving ground is. A visible imperfection
inside the pass, also stated: the forecast put 10.6% in "Not sure" against a published 3%,
so disapproval came in 5-6 points low and the net bar absorbed it — the engine over-hedges,
and that is now a tracked defect, not a hidden one.

Disclosures carried through: the era anchor's factual error (war onset month) disclosed
in Forward Test 2's registration stands; the test passed with the frozen, erroneous
anchor in place.

