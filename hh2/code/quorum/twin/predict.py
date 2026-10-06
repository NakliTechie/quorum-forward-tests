"""Twin-2K-500 prediction harness (S4) — drive a model to answer held-out survey questions as each
participant, so `quorum.twin.metrics` can score it against the human test-retest ceiling.

The benchmark (Toubia et al. 2025) is a PROMPTED-model task: put the participant's persona in
context, ask the held-out question, read the answer. The published bar is GPT-4.1-mini at 71.72%
(≈88% of the 0.8172 human ceiling), random floor 59.17%. This harness runs the same task with our
open-model serving path — the tuned-vs-prompted question from the landscape research starts here as
prompted-open-model, and fine-tuned adapters are the follow-up.

Answer coding (confirmed on real bytes 2026-08-02): for MC/Matrix items the CSV code is the 1-based
index into the catalog Options (code N = Options[N-1]); sliders are the raw integer in [code_min,
code_max]. So we present options as a numbered list and constrain the model to emit ONE integer in
range — parsed directly as the code, no off-by-one.

Backends: `StubTwinPredictor` (CPU, deterministic — proves the plumbing without a GPU) and
`VLLMTwinPredictor` (the real run). Both implement `predict(prompts, choices) -> list[int]`.
"""

from __future__ import annotations

import math
import os
import re
from typing import Protocol

import numpy as np

from quorum.twin.loader import TwinEval

PERSONA = "persona"
DEMOGRAPHIC = "demographic"
FULL = "full"
# Grounding char budget that fits max_model_len=8192 (~5k tokens grounding + question + scaffold).
# Personas run ~95k chars (~24k tokens) — 3x the window — so PERSONA mode RETRIEVES the answer-blocks
# most relevant to each held-out question instead of front-truncating. The old blind 12k-char cut fed
# only ~12.6% of the persona (demographics + the earliest scales), so persona lift went NEGATIVE in
# the n=300 pilot (persona 0.624 < demographic 0.642, 2026-08-02). See PersonaIndex.
_PERSONA_CHAR_BUDGET = 20000
# build_prompt safety clamp; >= the longest persona (~100.5k chars) so FULL mode is never truncated
# by the formatter — the real bound in FULL is the server's max_model_len (32768 for the ceiling arm).
_HARD_CHAR_CAP = 110000

_WORD = re.compile(r"[a-z]{3,}")


def _tokenize(s: str) -> list[str]:
    return _WORD.findall(s.lower())


def _split_blocks(text: str) -> list[str]:
    """Persona → answer-blocks. The Twin-2K persona is a blank-line-separated Q&A transcript of the
    person's own prior (non-holdout) answers. Split on blank lines; sub-window any oversized piece so
    a block is ~one question, not ~one wave. Falls back to fixed windows with no blank-line structure.
    """
    raw = [b.strip() for b in re.split(r"\n\s*\n", text) if b.strip()]
    if len(raw) < 2:  # no blank-line structure at all → fall back to fixed windows
        raw = [text[i : i + 1200] for i in range(0, len(text), 1000)] or [text]
    blocks: list[str] = []
    for b in raw:
        if len(b) <= 1500:
            blocks.append(b)
        else:
            blocks.extend(b[i : i + 1200] for i in range(0, len(b), 1000))
    return blocks


class PersonaIndex:
    """Per-participant retrieval over the persona's answer-blocks. Scores each block by IDF-weighted
    lexical overlap with the held-out question, so ubiquitous format tokens ('question','answer',
    'options') self-cancel (IDF≈0) and content words drive the match. Deterministic, CPU-only, no deps.

    No leakage: the loader already strips the held-out items from persona_text, so retrieval surfaces
    the person's answers to RELATED items (legitimate grounding), never the target answer itself."""

    def __init__(self, persona_text: str):
        self.blocks = _split_blocks(persona_text) if persona_text else []
        self._toks = [set(_tokenize(b)) for b in self.blocks]
        df: dict[str, int] = {}
        for ts in self._toks:
            for t in ts:
                df[t] = df.get(t, 0) + 1
        n = max(1, len(self.blocks))
        self._idf = {t: math.log(1.0 + n / c) for t, c in df.items()}
        # L2 norm of each block's IDF vector → cosine scoring, so a long verbose block cannot win on
        # sheer word count (the defect the real-data inspection exposed, 2026-08-02).
        self._norm = [math.sqrt(sum(self._idf[t] ** 2 for t in ts)) or 1.0 for ts in self._toks]

    def retrieve(self, query: str, budget: int, anchor: str = "") -> str:
        """Top relevant blocks (returned in original order) within `budget` chars, prefixed by
        `anchor` — the always-on demographic line. Scoring is IDF-weighted cosine between the query
        and each block, so relevance (not block length) drives selection. Blocks with zero query
        overlap are never included, so a question with little lexical match degrades toward
        demographics-only rather than padding with the longest block."""
        q = set(_tokenize(query))
        scored = []
        for i, ts in enumerate(self._toks):
            inter = q & ts
            if inter:
                s = sum(self._idf[t] ** 2 for t in inter) / self._norm[i]
                scored.append((s, i))
        scored.sort(key=lambda x: (-x[0], x[1]))
        used = len(anchor) + 2
        chosen: list[int] = []
        for _s, i in scored:
            b = self.blocks[i]
            if used + len(b) + 2 > budget:
                continue
            chosen.append(i)
            used += len(b) + 2
        chosen.sort()
        body = "\n\n".join(self.blocks[i] for i in chosen)
        return (anchor.strip() + "\n\n" + body).strip() if anchor else body


class TwinPredictor(Protocol):
    def predict(self, prompts: list[str], choices: list[list[int]]) -> list[int]:
        """One integer answer code per prompt, each constrained to its choices list."""
        ...


def build_prompt(persona_text: str, qmeta: dict, mode: str = PERSONA) -> tuple[str, list[int]]:
    """Return (prompt, valid_codes) for one (participant, question). `valid_codes` is what the model
    must choose from — used to clamp the parse (and would feed guided decoding).

    Choices ALWAYS come from the code range the loader computed (code_min..code_max), NOT from
    len(options): some MC/Matrix questions carry empty Options in the catalog yet have valid answer
    codes in the data, so deriving choices from options gave an EMPTY set and crashed the parse
    (2026-08-02). Labels are shown when present; otherwise the model just picks a number in range.
    """
    ground = persona_text[:_HARD_CHAR_CAP].strip()
    q = qmeta["text"].strip()
    lo, hi = int(qmeta["code_min"]), int(qmeta["code_max"])
    if hi < lo:
        hi = lo
    choices = list(range(lo, hi + 1))  # never empty: hi >= lo guaranteed
    opts = qmeta.get("options") or []
    if qmeta["kind"] != "numeric" and opts:
        numbered = "\n".join(f"{i + 1}. {o}" for i, o in enumerate(opts))
        ask = f"{q}\n\nOptions:\n{numbered}\n\nAnswer with the number of your choice only."
    else:  # numeric, or a coded item whose option labels aren't in the catalog
        ask = f"{q}\n\nAnswer with a single whole number from {lo} to {hi}."
    header = (
        "You are answering a survey exactly as the following person would, based on who they are. "
        "Respond as them, not as an AI. Output only the number.\n\n"
    )
    who = "PERSON (demographics):\n" + ground if mode == DEMOGRAPHIC else "PERSON:\n" + ground
    return f"{header}{who}\n\nQUESTION:\n{ask}\n\nANSWER:", choices


def predict_frame(
    predictor: TwinPredictor, ev: TwinEval, *, mode: str = PERSONA, batch: int = 512,
    ckpt_path: str | None = None,
) -> np.ndarray:
    """Predicted answer code per row of `ev.frame`, aligned to it. Three grounding modes:
      - PERSONA (default): demographic anchor + the persona answer-blocks RETRIEVED as most relevant
        to each held-out question (PersonaIndex) — the scalable design.
      - FULL: the entire persona (~24k tokens) fed verbatim — the rich ceiling. Requires the server's
        max_model_len to hold it (32768 for Qwen3-8B). Prefix caching is IDEAL here: a person's whole
        persona is identical across their ~93 questions, so it prefills once and is reused.
      - DEMOGRAPHIC: the short demographic line alone — the Argyle-style floor.

    CRITICAL: process rows in PERSON order, not frame order. The frame is question-major (all people
    for Q1, then Q2…), so consecutive rows have DIFFERENT personas and prefix caching never hits.
    Grouping a person's questions consecutively lets the shared prefix prefill once. NOTE: in PERSONA
    mode the retrieved BODY differs per question, so the cache hits on the anchor/header prefix, not
    the full persona — a deliberate throughput cost for per-question relevance. We predict in person
    order, build each PersonaIndex once (person-major → on pid change), then scatter back to frame rows.
    """
    frame = ev.frame
    order = frame["pid"].argsort(kind="stable").to_numpy()  # person-major; stable keeps Q order within

    prompts: list[str] = []
    choices: list[list[int]] = []
    index_cache: dict[int, PersonaIndex] = {}
    for pos in order:
        row = frame.iloc[pos]
        pid = int(row["pid"])
        qmeta = ev.questions[row["col"]]
        if mode == PERSONA:
            idx = index_cache.get(pid)
            if idx is None:
                idx = index_cache[pid] = PersonaIndex(ev.grounding.get(pid, ""))
            ground = idx.retrieve(
                qmeta["text"], _PERSONA_CHAR_BUDGET, anchor=ev.demographics.get(pid, "")
            )
        elif mode == FULL:
            ground = ev.grounding.get(pid, "")
        else:  # DEMOGRAPHIC
            ground = ev.demographics.get(pid, "")
        p, ch = build_prompt(ground, qmeta, mode)
        prompts.append(p)
        choices.append(ch)

    # Checkpointed: NaN marks not-yet-predicted. On restart we reload the checkpoint and skip any
    # batch already fully filled, so a preempted run RESUMES instead of recomputing. Paired with the
    # yaml's 60s S3 mirror + resume-pull, no GPU work is lost to an eviction.
    out = np.full(len(frame), np.nan)
    if ckpt_path and os.path.exists(ckpt_path):
        try:
            prev = np.load(ckpt_path)
            if prev.shape == out.shape:
                out = prev  # resume
        except Exception:
            pass  # corrupt/partial checkpoint (e.g. eviction mid-write) → recompute from scratch
    for i in range(0, len(prompts), batch):
        seg = order[i : i + batch]
        if not np.isnan(out[seg]).any():
            continue  # whole batch already done (resumed) — skip the GPU work
        preds = predictor.predict(prompts[i : i + batch], choices[i : i + batch])
        for j, pred in enumerate(preds):
            out[order[i + j]] = pred  # scatter back to the original frame row
        if ckpt_path:
            np.save(ckpt_path, out)  # checkpoint after every batch
    return out


def parse_int_in_range(text: str, choices: list[int]) -> int:
    """Pull the first integer from a generation and clamp to the valid choice set. Falls back to the
    middle choice (a neutral guess, not a systematic 0) when nothing parses."""
    import re

    if not choices:  # defensive — build_prompt guarantees non-empty, but never crash on a bad row
        return 0
    m = re.search(r"-?\d+", text)
    if not m:
        return choices[len(choices) // 2]
    v = int(m.group())
    if v in choices:
        return v
    return min(choices, key=lambda c: abs(c - v))  # nearest valid code


class StubTwinPredictor:
    """CPU plumbing stub — deterministic, no model. Returns the median valid code per item so the
    full pipeline (build → predict → score) runs and is testable without a GPU. Its accuracy is
    meaningless by design; it exists to prove alignment, batching, and scoring end to end."""

    def predict(self, prompts: list[str], choices: list[list[int]]) -> list[int]:
        return [ch[len(ch) // 2] for ch in choices]


def _digit_logprobs(top: dict, valid: set[int]) -> dict[int, float]:
    """Best logprob per valid option digit among the returned top tokens."""
    lp: dict[int, float] = {}
    for info in top.values():
        tok = (info.decoded_token or "").strip()
        # isascii guard: str.isdigit() accepts Unicode digit forms ('²', circled digits)
        # that int() rejects — one such token in any top-20 would crash-loop a t=0 resume
        if tok.isascii() and tok.isdigit():
            c = int(tok)
            if c in valid and (c not in lp or info.logprob > lp[c]):
                lp[c] = info.logprob
    return lp


def complete_distribution(top: dict, choices: list[int]) -> dict[int, float] | None:
    """Renormalised option distribution, or None if any option is absent from `top`."""
    lp = _digit_logprobs(top, set(choices))
    if set(lp) != set(choices):
        return None
    probs = {c: math.exp(v) for c, v in lp.items()}
    z = sum(probs.values())
    return {c: probs[c] / z for c in choices}


class VLLMTwinPredictor:  # pragma: no cover - GPU only
    """Real run: an open base model, prompted, measuring the PROMPTED open-model bar (no LoRA in v1).

    v1 uses FREE generation + a robust parse (`parse_int_in_range`), NOT guided decoding. Reason:
    vLLM's default guided backend (xgrammar) supports only JSON/EBNF, not `choice` mode, and the
    incompatibility surfaces at generation time — it crashed the first run mid-predict (2026-08-02).
    The prompt already asks for a bare number and the parser clamps any output to the valid code set,
    so unconstrained decoding gets the same answer without the backend fragility. Guided decoding is
    a later accuracy refinement (JSON-schema enum works with xgrammar), not a v1 requirement.
    """

    def __init__(
        self, hf_id: str, *, max_model_len: int = 8192, gpu_mem_util: float = 0.90,
        adapter_path: str | None = None, enforce_eager: bool = True,
        tensor_parallel: int = 1, kv_fp8: bool = False, revision: str | None = None,
        max_logprobs: int | None = None, enable_prefix_caching: bool = True,
        max_num_seqs: int | None = None, seed: int | None = None,
    ):
        """enforce_eager=False enables CUDA graphs — decode-heavy workloads (paper-format
        whole-survey generation) are 3-4x faster per sequence; eager remains the default for
        the short-generation harnesses that never noticed the difference."""
        from vllm import LLM, SamplingParams

        # prefix caching is the difference between hours and minutes: a participant's persona
        # (~3-4k tokens) is the shared PREFIX of all their questions, so vLLM prefills it once and
        # reuses the KV. Content-hashed → hits regardless of batch order.
        kw = dict(
            model=hf_id, max_model_len=max_model_len, gpu_memory_utilization=gpu_mem_util,
            enforce_eager=enforce_eager, trust_remote_code=True, dtype="bfloat16",
            enable_prefix_caching=enable_prefix_caching, tensor_parallel_size=tensor_parallel,
        )
        if max_num_seqs:  # UQ1 determinism probe: 1 = no batching across prompts
            kw["max_num_seqs"] = max_num_seqs
        if seed is not None:
            kw["seed"] = seed
        if revision:  # E56: an immutable model revision (default None keeps every earlier harness unchanged)
            kw["revision"] = revision
            kw["tokenizer_revision"] = revision
        if max_logprobs:  # UQ1: distribution_complete() may ask for up to this many top tokens
            kw["max_logprobs"] = max_logprobs
        if kv_fp8:  # halves KV bytes/token -> ~2x decode concurrency at long contexts
            kw["kv_cache_dtype"] = "fp8"
        # Stage B: serve the base + the fine-tuned LoRA adapter, so this harness scores the pretrained
        # model unchanged. A light LoRA keeps instruction-following intact, so the existing prompt still
        # reads the answer — the adapter just shifts the answer distribution toward human-like.
        self._lora = None
        if adapter_path:
            from vllm.lora.request import LoRARequest

            kw["enable_lora"] = True
            kw["max_lora_rank"] = 64
            self._lora = LoRARequest("stageb", 1, adapter_path)
        self.llm = LLM(**kw)
        # max_tokens 12: room for a number + a stray token; temp 0 for determinism
        self.sp = SamplingParams(temperature=0.0, max_tokens=12)

    def predict(self, prompts: list[str], choices: list[list[int]]) -> list[int]:
        res = self.llm.generate(prompts, self.sp, lora_request=self._lora)
        return [parse_int_in_range(res[i].outputs[0].text, choices[i]) for i in range(len(prompts))]

    def generate(self, prompts: list[str], max_tokens: int = 2500) -> list[str]:
        """Greedy free-text generation — for whole-survey JSON elicitation (the Mega-Study paper's
        own format), where the model fills a multi-question answer scaffold rather than emitting a
        single option digit."""
        from vllm import SamplingParams

        sp = SamplingParams(temperature=0.0, max_tokens=max_tokens)
        res = self.llm.generate(prompts, sp, lora_request=self._lora)
        return [r.outputs[0].text for r in res]

    def distribution(self, prompts: list[str], choices: list[list[int]]) -> list[dict[int, float]]:
        """First-token probability over each prompt's integer choices — the Argyle/Santurkar
        elicitation. Greedy `predict` collapses to the modal safe code (e.g. a neutral '3' on a 1-5
        approval scale); this reads the model's actual mass on each option-digit token and renormalizes
        over the valid set, so the persona gradient greedy discards is preserved. Returns one
        {code: prob} per prompt. Assumes each choice is a single-digit token (true for 0-9); options
        outside the top-`logprobs` set get 0 mass and the rest are renormalized."""
        from vllm import SamplingParams

        sp = SamplingParams(temperature=0.0, max_tokens=1, logprobs=20)
        res = self.llm.generate(prompts, sp, lora_request=self._lora)
        out: list[dict[int, float]] = []
        for i in range(len(prompts)):
            lp = _digit_logprobs(res[i].outputs[0].logprobs[0], set(choices[i]))
            probs = {c: math.exp(v) for c, v in lp.items()}
            z = sum(probs.values()) or 1.0
            out.append({c: probs.get(c, 0.0) / z for c in choices[i]})
        return out

    def distribution_complete(self, prompts: list[str], choices: list[list[int]],
                              tops: tuple[int, ...] = (20, 200, 1000)) -> list[dict[int, float]]:
        """As `distribution`, but every option must carry its own probability (UQ1; Codex
        uq1-smoke post-run review 1). A prompt whose options are not all in the top-k tokens is
        asked again with a larger k; one still missing an option after the last k raises, never
        scores the option 0. The LLM must be built with max_logprobs >= max(tops)."""
        from vllm import SamplingParams

        out: list[dict[int, float] | None] = [None] * len(prompts)
        todo = list(range(len(prompts)))
        for k in tops:
            if not todo:
                break
            sp = SamplingParams(temperature=0.0, max_tokens=1, logprobs=k)
            res = self.llm.generate([prompts[i] for i in todo], sp, lora_request=self._lora)
            left = []
            for j, i in enumerate(todo):
                d = complete_distribution(res[j].outputs[0].logprobs[0], choices[i])
                if d is None:
                    left.append(i)
                else:
                    out[i] = d
            todo = left
        if todo:
            raise RuntimeError(f"{len(todo)} prompts still miss an option in the top {tops[-1]} tokens")
        return out  # type: ignore[return-value]
