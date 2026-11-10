"""TARGET INSTRUMENTS for the forward-test series.

One registry entry per question we forecast, so that adding a target is a data change
rather than a code change. Each entry records the wording actually put to the simulated
respondents, its provenance, and how the published statistic is computed — because the
thing we are scored against is the *publisher's* number, not ours.

Provenance is explicit and load-bearing:
  "verbatim"      — copied from the publisher's own toplines/questionnaire PDF
  "reconstructed" — assembled from the publisher's description and long-standing trend
                    wording; not confirmed against a questionnaire. Wording effects are a
                    real error source and must be disclosed in any registration using it.

Cadence notes drive registration timing: a forecast only counts if it is published before
the target begins fielding.
"""

from __future__ import annotations

INSTRUMENTS: dict[str, dict] = {
    # ---- The Economist / YouGov, weekly (Fri-Mon field, Wed publication) ----------------
    "yougov_approval": {
        "publisher": "The Economist/YouGov",
        "cadence": "weekly; fields Fri-Mon, publishes the following Wed",
        "question": ("Do you approve or disapprove of the way Donald Trump is handling his "
                     "job as President?"),
        "options": ["Strongly approve", "Somewhat approve", "Somewhat disapprove",
                    "Strongly disapprove", "Not sure"],
        "positive": ["Strongly approve", "Somewhat approve"],
        "negative": ["Somewhat disapprove", "Strongly disapprove"],
        "abstain": ["Not sure"],
        "provenance": "verbatim (Economist/YouGov toplines, June 5-8 2026 PDF)",
        "published_cuts": ["party", "sex", "age", "race"],
    },

    "yougov_direction": {
        "publisher": "The Economist/YouGov",
        "cadence": "weekly; same poll as yougov_approval",
        "question": "Would you say things in this country today are...",
        "options": ["Generally headed in the right direction", "Off on the wrong track",
                    "Not sure"],
        "positive": ["Generally headed in the right direction"],
        "negative": ["Off on the wrong track"],
        "abstain": ["Not sure"],
        "provenance": "verbatim (Economist/YouGov toplines, Aug 14-17 2026 PDF, Q1)",
        "published_cuts": ["party"],
    },
    "yougov_house_ballot": {
        "publisher": "The Economist/YouGov",
        "cadence": ("weekly; same poll; toplines print the ADULT-CITIZEN row (Q9, Aug 21-24 "
                    "2026: D 37 / R 31 / Other 1 / NS 9 / will not vote 22); the tabs add a "
                    "registered-voter cut — FT4 registers against the adult row (frame note)"),
        "question": ("In the elections for U.S. Congress in November, who will you vote "
                     "for in the district where you live?"),
        "options": ["The Democratic candidate", "The Republican candidate", "Other",
                    "Not sure", "I will not vote"],
        "positive": ["The Democratic candidate"],
        "negative": ["The Republican candidate"],
        "abstain": ["Other", "Not sure", "I will not vote"],
        "provenance": "verbatim (Economist/YouGov toplines, Aug 14-17 2026 PDF, Q41)",
        "published_cuts": ["party"],
    },
    "hh_approval": {
        "publisher": "Harvard CAPS / Harris Poll",
        "cadence": "~monthly, irregular (25-57 day gaps); registered voters online",
        "question": ("Do you disapprove or approve of the job Donald J. Trump is doing "
                     "as President of the United States?"),
        "options": ["Strongly approve", "Somewhat approve", "Somewhat disapprove",
                    "Strongly disapprove", "Don't Know/Not Sure"],
        "positive": ["Strongly approve", "Somewhat approve"],
        "negative": ["Somewhat disapprove", "Strongly disapprove"],
        "abstain": ["Don't Know/Not Sure"],
        "provenance": ("verbatim (HH topline decks Apr/May/Jul 2026, question M3ALT, "
                       "Table 14 p.16; disapprove-first question wording as printed; "
                       "docs/harvard-harris-recon.md)"),
        "published_cuts": ["party"],
    },
    "hh_direction": {
        "publisher": "Harvard CAPS / Harris Poll",
        "cadence": "~monthly, irregular; registered voters online",
        "question": ("In general, do you think the country is on the right track or is "
                     "it off on the wrong track?"),
        "options": ["Right track", "Wrong track", "Don't know / Unsure"],
        "positive": ["Right track"],
        "negative": ["Wrong track"],
        "abstain": ["Don't know / Unsure"],
        "provenance": ("verbatim (HH toplines Apr/May/Jul 2026, question M1, Table 10 "
                       "p.12; right-track/wrong-track form, NOT 'right direction'; "
                       "docs/harvard-harris-recon.md)"),
        "published_cuts": [],
    },
    "hh_generic_ballot": {
        "publisher": "Harvard CAPS / Harris Poll",
        "cadence": "~monthly, irregular; registered voters online",
        "question": ("If the congressional election were held today would you be more "
                     "likely to vote for a Democrat or a Republican for Congress?"),
        "options": ["Democrat", "Republican"],
        "positive": ["Democrat"],
        "negative": ["Republican"],
        "abstain": [],
        "provenance": ("verbatim (HH toplines, question CON2026B; two published rows "
                       "summing to 100, no undecided — forced-choice convention "
                       "declared; docs/harvard-harris-recon.md)"),
        "published_cuts": [],
    },
    "pres_vote_2024": {
        "publisher": "The Economist/YouGov",
        "cadence": "2024 pre-election waves; asked of registered voters (frame note)",
        "question": ("In November 2024, who do you plan to vote for in the presidential "
                     "election?"),
        "options": ["Kamala Harris", "Donald Trump", "Jill Stein", "Cornel West",
                    "Other", "Not sure", "I would not vote"],
        "positive": ["Kamala Harris"],
        "negative": ["Donald Trump"],
        "abstain": ["Jill Stein", "Cornel West", "Other", "Not sure", "I would not vote"],
        "provenance": ("verbatim (Economist/YouGov toplines, Oct 26-29 2024 PDF "
                       "econtoplines_xAm5lvg, Q6: '[In November 2024, who do you plan "
                       "to/Who did you] vote for...' — forward form used; E18 retrodiction)"),
        "published_cuts": ["party"],
    },

    # ---- Gallup monthly poll (fields ~1st-19th, publishes late month) -------------------
    # Gallup discontinued presidential approval in Feb 2026; these trackers continue.
    "gallup_econ_conditions": {
        "publisher": "Gallup (Economic Confidence Index, component 1)",
        "cadence": "monthly; fields ~1st-19th, publishes late month",
        "question": ("How would you rate economic conditions in this country today -- as "
                     "excellent, good, only fair, or poor?"),
        "options": ["Excellent", "Good", "Only fair", "Poor"],
        "positive": ["Excellent", "Good"],
        "negative": ["Poor"],          # Gallup's net excludes "only fair" from both sides
        "abstain": [],
        "provenance": "reconstructed (Gallup describes the item; wording not confirmed "
                      "against a questionnaire)",
        "published_cuts": ["party"],
        "reference": "July 2026: Excellent/Good 22%, Poor 44% (field July 1-19, n=1,200)",
    },
    "gallup_econ_direction": {
        "publisher": "Gallup (Economic Confidence Index, component 2)",
        "cadence": "monthly; same poll as component 1",
        "question": ("Right now, do you think that economic conditions in the country as a "
                     "whole are getting better or getting worse?"),
        "options": ["Getting better", "Getting worse"],
        "positive": ["Getting better"],
        "negative": ["Getting worse"],
        "abstain": [],
        "provenance": "reconstructed (as above)",
        "published_cuts": ["party"],
        "reference": "July 2026: Better 28%, Worse 67%",
    },
    "gallup_satisfaction": {
        "publisher": "Gallup (Satisfaction with the way things are going)",
        "cadence": "monthly; same poll",
        "question": ("In general, are you satisfied or dissatisfied with the way things are "
                     "going in the United States at this time?"),
        "options": ["Satisfied", "Dissatisfied"],
        "positive": ["Satisfied"],
        "negative": ["Dissatisfied"],
        "abstain": [],
        "provenance": "reconstructed (wording quoted in Gallup trend pages)",
        "published_cuts": ["party"],
        "reference": "Dec 2025: 24% satisfied; party gap has run as wide as 76 points",
    },
}


def net(dist: dict[str, float], key: str) -> float:
    """Publisher-style net score: %positive - %negative, in points."""
    spec = INSTRUMENTS[key]
    pos = sum(dist.get(o, 0.0) for o in spec["positive"])
    neg = sum(dist.get(o, 0.0) for o in spec["negative"])
    return round(pos - neg, 1)


def economic_confidence_index(conditions: dict[str, float],
                              direction: dict[str, float]) -> float:
    """Gallup's ECI: the mean of the two component net scores, range [-100, +100].

    Verified against the published July 2026 release: conditions net 22-44 = -22,
    direction net 28-67 = -39, mean -30.5, published as -31.
    """
    return round((net(conditions, "gallup_econ_conditions")
                  + net(direction, "gallup_econ_direction")) / 2, 1)


def prompt_for(key: str, profile: str, anchor: str) -> str:
    """The prompt put to one simulated respondent — same shape across all instruments so
    that calibration measured on one is applicable to another."""
    return prompt_for_spec(INSTRUMENTS[key], profile, anchor)


def prompt_for_spec(spec: dict, profile: str, anchor: str) -> str:
    """The same prompt for any {question, options} spec, registered or not (UQ1 generic items)."""
    opts = "\n".join(f"{i + 1}. {o}" for i, o in enumerate(spec["options"]))
    return (f"{profile}\n\n{anchor}\n\nQuestion: {spec['question']}\n{opts}\n"
            f"Answer with the single digit of your choice.\nANSWER: <<")
