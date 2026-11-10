"""FORWARD TEST 1 — registered pre-field forecast of an Economist/YouGov approval wave.

The investor question in its plainest form: can we predict the presidential approval
survey? This module produces a REGISTERED answer: a frozen, sha-stamped forecast of the
next Economist/YouGov wave's presidential-approval question — topline plus the published
crosstab cuts — computed BEFORE the poll fields, from inputs that contain no 2026 polling
data.

Design (each piece validated earlier in this program):
- Population frame: Pew ATP W161 microdata with survey weights (Pew's census weighting is
  inherited; real joint distributions of age x sex x race x education x party). Research
  use per the ATP license; cite "Pew Research Center's American Trends Panel" in outputs.
- Per-profile prompt: the pew_atp demographic+party profile line + a one-sentence era
  anchor (sha-pinned; contains NO polling numbers) + the target poll's EXACT question
  wording and options (Economist/YouGov toplines, verified against the June 5-8 2026 PDF).
- Elicitation: FT-adapter soft first-token distribution over the 5 option digits — the
  method that recovered the W161 gold approval topline within +-5 points (frozen there;
  no 2026 calibration).
- Aggregation: distinct profiles dedupe (weights summed); topline = weight-averaged soft
  distribution; crosstabs by party / sex / age / race from the same per-profile softs.

Output: forecast JSON (+ manifest, + sha256) — the registrable artifact.
"""

from __future__ import annotations

import hashlib
import json
import os

# The target instrument, VERBATIM from the Economist/YouGov toplines PDF (June 5-8, 2026
# wave, econtoplines_vxERiPy.pdf; identical wording in the July 31-Aug 3 tab report).
# Kept as module constants for the frozen FT1/FT2 record; the CLI now draws wording from
# the instruments registry (quorum.twin.instruments), of which this is the default entry.
YOUGOV_QUESTION = ("Do you approve or disapprove of the way Donald Trump is handling "
                   "his job as President?")
YOUGOV_OPTIONS = ["Strongly approve", "Somewhat approve", "Somewhat disapprove",
                  "Strongly disapprove", "Not sure"]

# Crosstab cuts as published in Economist/YouGov tab reports (verified July 31-Aug 3 PDF).
AGE_BANDS = [("18-29", 18, 29), ("30-44", 30, 44), ("45-64", 45, 64), ("65+", 65, 200)]


def build_prompt(profile_line: str, anchor: str, instrument: str = "yougov_approval") -> str:
    from quorum.twin.instruments import prompt_for

    return prompt_for(instrument, profile_line, anchor)


def calibrate_soft(dist: dict[int, float], spec: dict, a: float, b: float) -> dict[int, float]:
    """Apply Platt calibration to the CONDITIONAL positive share among opinion-holders,
    carrying any abstain mass through untouched — the same semantics validated for the
    FT1-B companion. Per-digit structure within each side is preserved proportionally."""
    from quorum.twin.compression import platt

    opts = spec["options"]
    pos_d = [i + 1 for i, o in enumerate(opts) if o in spec["positive"]]
    neg_d = [i + 1 for i, o in enumerate(opts) if o in spec["negative"]]
    pos = sum(dist.get(d, 0.0) for d in pos_d)
    neg = sum(dist.get(d, 0.0) for d in neg_d)
    held = pos + neg
    if pos <= 0 or neg <= 0:
        return dict(dist)  # degenerate cell: nothing to remap without inventing mass
    cond = platt(pos / held, a, b)
    out = dict(dist)
    for d in pos_d:
        out[d] = dist.get(d, 0.0) * (cond * held / pos)
    for d in neg_d:
        out[d] = dist.get(d, 0.0) * ((1.0 - cond) * held / neg)
    return out


def _agecat_to_band(agecat: str) -> str | None:
    # F_AGECAT labels: "18-29", "30-49", "50-64", "65+" — ATP bands differ from YouGov's
    # (30-44/45-64). Map 30-49 -> "30-44" and 50-64 -> "45-64": each ATP band is assigned
    # to the YouGov band containing most of its span. Declared approximation; the frame's
    # ages are banded at source, so exact YouGov bands are not recoverable.
    m = {"18-29": "18-29", "30-49": "30-44", "50-64": "45-64", "65+": "65+"}
    return m.get(str(agecat).strip())


def _race_group(eth: str) -> str:
    # ATP labels are e.g. "White non-Hispanic" — test the non-Hispanic qualifier FIRST or
    # every such label matches the "hispanic" substring (the bug the first frozen-candidate
    # run surfaced: White/Black vanished into the Hispanic bucket).
    e = str(eth).lower()
    if "non-hispanic" in e or "non hispanic" in e:
        if "black" in e:
            return "Black"
        if "white" in e:
            return "White"
        return "Other"
    if "hispanic" in e:
        return "Hispanic"
    if "black" in e:
        return "Black"
    if "white" in e:
        return "White"
    return "Other"


def _party_group(party: str) -> str | None:
    p = str(party).strip().lower()
    if p.startswith("democrat"):
        return "Dem"
    if p.startswith("republican"):
        return "Rep"
    if p.startswith("independent"):
        return "Ind"
    return None  # "Something else" / refused stay in the topline, out of the party cut


def load_frame_csv(path: str):
    """Cells from a pre-built frame CSV (profile_line, weight, party, sex, age, race) —
    the state_frames.py output format. Same cell shape as load_frame."""
    import csv

    cells: dict[str, dict] = {}
    with open(path, newline="") as f:
        for r in csv.DictReader(f):
            c = cells.setdefault(r["profile_line"], {
                "w": 0.0, "party": r["party"] or None, "sex": r["sex"] or None,
                "age": r["age"] or None, "race": r["race"] or None})
            c["w"] += float(r["weight"])
    return cells


REGISTERED = ("You are ABSOLUTELY CERTAIN", "You are PROBABLY registered")  # W161 F_REG


def load_frame(sav_path: str, minimal: bool = False, registered_only: bool = False):
    """Distinct (profile_line, party, sex, age_band, race) cells with summed ATP weights.
    minimal=True (E43): profile carries Age+Gender+Party only; race is excluded from
    the cut attribution too (it is not in the prompt, so a race cut would misattribute
    shared minimal-cell softs) — declared out of scope in the E43 register row.
    registered_only=True (E53): weights summed over respondents certain or probably
    registered (F_REG) — the registered-voter base YouGov prints from Sep 4 2026."""
    import pyreadstat

    df, _ = pyreadstat.read_sav(sav_path, apply_value_formats=True)
    wcol = next(c for c in df.columns if c.upper().startswith("WEIGHT"))
    from quorum.twin.pew_atp import build_profile  # the validated line builder

    cells: dict[str, dict] = {}
    for _, row in df.iterrows():
        w = float(row[wcol]) if row[wcol] == row[wcol] else 0.0
        if w <= 0:
            continue
        if registered_only and not str(row.get("F_REG", "")).startswith(REGISTERED):
            continue
        line = build_profile(row, party_fields=("party",),
                             fields=[("F_AGECAT", "Age"), ("F_GENDER", "Gender")]
                             if minimal else None)
        c = cells.setdefault(line, {
            "w": 0.0,
            "party": _party_group(row.get("F_PARTY_FINAL")),
            "sex": {"A man": "Male", "A woman": "Female"}.get(
                str(row.get("F_GENDER", "")).strip()),  # YouGov publishes Male/Female only
            "age": _agecat_to_band(row.get("F_AGECAT")),
            "race": None if minimal else _race_group(row.get("F_RACETHNMOD")),
        })
        c["w"] += w
    return cells


def aggregate(cells: dict[str, dict], softs: dict[str, dict[int, float]],
              instrument: str = "yougov_approval") -> dict:
    """Weight-average per-cell soft distributions into topline + published crosstab cuts."""
    from quorum.twin.instruments import INSTRUMENTS

    spec = INSTRUMENTS[instrument]
    options = spec["options"]

    def wavg(sub: list[str]) -> dict:
        tw = sum(cells[k]["w"] for k in sub)
        if tw <= 0:
            return {}
        probs = [sum(cells[k]["w"] * softs[k].get(i + 1, 0.0) for k in sub) / tw
                 for i in range(len(options))]
        out = {o: round(100 * p, 1) for o, p in zip(options, probs)}
        out["Positive"] = round(sum(out[o] for o in spec["positive"]), 1)
        out["Negative"] = round(sum(out[o] for o in spec["negative"]), 1)
        out["Net"] = round(out["Positive"] - out["Negative"], 1)
        if instrument == "yougov_approval":  # legacy keys the committed scorer reads
            out["Approve"] = out["Positive"]
            out["Disapprove"] = out["Negative"]
        out["_n_cells"] = len(sub)
        out["_weight_share"] = round(tw / sum(c["w"] for c in cells.values()), 4)
        return out

    keys = list(cells)
    res = {"topline": wavg(keys), "by": {}}
    for dim, valfn in (("party", lambda c: c["party"]), ("sex", lambda c: c["sex"]),
                       ("age", lambda c: c["age"]), ("race", lambda c: c["race"])):
        groups: dict[str, list[str]] = {}
        for k in keys:
            v = valfn(cells[k])
            if v:
                groups.setdefault(v, []).append(k)
        res["by"][dim] = {g: wavg(ks) for g, ks in sorted(groups.items())}
    return res


def _adapter(v: str | None):
    """'none' selects the bare base model — the era-sweep control arm."""
    return None if v in ("", "none", None) else v


def main() -> None:  # pragma: no cover - CLI/GPU entry
    import argparse

    from quorum.twin.evidence import manifest, write_run

    from quorum.twin.instruments import INSTRUMENTS

    ap = argparse.ArgumentParser()
    ap.add_argument("--sav", default="data/pew/atp/w161/W161_Feb25/ATP W161.sav")
    ap.add_argument("--minimal-profile", action="store_true",
                    help="E43 arm: Age+Gender+Party profile only")
    ap.add_argument("--frame-csv", default=None,
                    help="pre-built frame CSV (state_frames.py output); overrides --sav")
    ap.add_argument("--anchor", required=True, help="era-anchor text file (sha-pinned; "
                                                    "must contain no polling numbers)")
    ap.add_argument("--instrument", default="yougov_approval", choices=list(INSTRUMENTS))
    ap.add_argument("--platt", default=None, metavar="A,B",
                    help="emit the CALIBRATED companion: apply p'=sigma(a*logit(p)+b) to "
                         "the conditional positive share (family-fit params; the family "
                         "must have passed the AUC + sign diagnostic)")
    ap.add_argument("--platt-family", default=None,
                    help="label of the gold family the (a,b) were fitted on, for the record")
    ap.add_argument("--hf-id", default="Qwen/Qwen3-14B")
    ap.add_argument("--adapter", default="/adapters/14b",
                    help="LoRA path, or 'none' for the bare base (era-sweep control)")
    ap.add_argument("--max-model-len", type=int, default=4096)
    ap.add_argument("--tp", type=int, default=1, help="tensor parallel (32B needs 2x L40S)")
    ap.add_argument("--backend", default="vllm", choices=["vllm", "jev"],
                    help="'jev' sends the same profiles/anchor/question to TypeSafe's hosted "
                         "Jev (E50); --hf-id/--adapter are then unused")
    ap.add_argument("--jev-model", default=None, help="Jev model ID (default: the pinned one)")
    ap.add_argument("--jev-workers", type=int, default=8)
    ap.add_argument("--stub", action="store_true")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    spec = INSTRUMENTS[a.instrument]
    n_opts = len(spec["options"])
    anchor = open(a.anchor).read().strip()
    cells = (load_frame_csv(a.frame_csv) if a.frame_csv
             else load_frame(a.sav, minimal=a.minimal_profile))
    keys = list(cells)
    prompts = [build_prompt(k, anchor, a.instrument) for k in keys]
    print(f"frame: {len(keys)} distinct profiles · total weight "
          f"{sum(c['w'] for c in cells.values()):.1f} · instrument {a.instrument}",
          flush=True)

    choices = [list(range(1, n_opts + 1))] * len(prompts)
    jev_meta = None
    if a.stub:
        soft_list = [{c: 1.0 / len(ch) for c in ch} for ch in choices]
    elif a.backend == "jev":
        from quorum.twin.jev import MODEL, JevPredictor

        jp = JevPredictor(a.out, model=a.jev_model or MODEL, workers=a.jev_workers)
        soft_list, jev_meta = jp.distribution_for(keys, anchor, spec)
        print(f"jev: {jev_meta['answered_models']} · {jev_meta['input_tokens']:,} input tokens"
              f" · ${jev_meta['cost_usd']}", flush=True)
    else:
        from quorum.twin.predict import VLLMTwinPredictor

        pred = VLLMTwinPredictor(a.hf_id, max_model_len=a.max_model_len,
                                 adapter_path=_adapter(a.adapter),
                                 tensor_parallel=a.tp)
        soft_list = pred.distribution(prompts, choices)
    if a.platt:
        pa, pb = (float(x) for x in a.platt.split(","))
        soft_list = [calibrate_soft(d, spec, pa, pb) for d in soft_list]
    softs = dict(zip(keys, soft_list))

    res = aggregate(cells, softs, a.instrument)
    res["instrument"] = {"key": a.instrument, "question": spec["question"],
                         "options": spec["options"], "provenance": spec["provenance"]}
    res["calibration"] = ({"a": pa, "b": pb, "family": a.platt_family}
                          if a.platt else "raw")
    res["anchor_sha256"] = hashlib.sha256(anchor.encode()).hexdigest()
    res["anchor_text"] = anchor
    res["frame"] = {"source": "Pew Research Center's American Trends Panel, Wave 161 "
                              "(Feb 2025) demographic microdata with survey weights",
                    "n_profiles": len(keys)}
    print(json.dumps({k: res[k] for k in ("topline", "by")}, indent=1), flush=True)

    engine = ({"backend": "jev", **jev_meta} if jev_meta else
              {"hf_id": a.hf_id, "adapter": _adapter(a.adapter)})
    if jev_meta:
        res["engine"] = engine
    man = manifest(params={"harness": "forecast_v1", "instrument": a.instrument,
                           "anchor_sha256": res["anchor_sha256"], **engine,
                           "stub": a.stub, "platt": a.platt,
                           "platt_family": a.platt_family, "n_profiles": len(keys)},
                   dataset_paths=[a.frame_csv if a.frame_csv else a.sav, a.anchor])
    rows = [{"profile": k, "w": cells[k]["w"], **{f"p{i}": softs[k].get(i, 0.0)
             for i in range(1, n_opts + 1)}} for k in keys]
    write_run(a.out, man, rows)
    json.dump(res, open(os.path.join(a.out, "forecast.json"), "w"), indent=2)
    fsha = hashlib.sha256(open(os.path.join(a.out, "forecast.json"), "rb").read()).hexdigest()
    print(f"\nFORECAST WRITTEN {a.out}/forecast.json sha256={fsha}", flush=True)


if __name__ == "__main__":
    main()
