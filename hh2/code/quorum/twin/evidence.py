"""Run provenance for eval harnesses — the evidence-freeze layer (2026-08-07 reviews, Objection 12).

Every eval run persists TWO artifacts next to its report:
  manifest.json — commit SHA, argv, python, params, and sha256 of every dataset file actually read
  rows.jsonl    — one row per scored record (ids, gold, soft prob, grouping fields)

so any table can be rebuilt from disk without a GPU, and any number can be traced to the exact
code + data + sample that produced it. A result without these is not citable."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone


def file_sha256(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def commit_sha() -> str:
    """HEAD sha, suffixed '+dirty' when the tree has uncommitted changes — a clean SHA must mean
    'this exact code ran'."""
    try:
        sha = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True,
                             timeout=5).stdout.strip() or "(unknown)"
        dirty = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True,
                               timeout=5).stdout.strip()
        return sha + ("+dirty" if dirty else "")
    except Exception:
        return "(unknown)"


def manifest(params: dict, dataset_paths: list[str]) -> dict:
    """Assemble the run manifest. `params` = everything that shaped the run (waves, n, seed, model,
    adapter, arms); `dataset_paths` = the files actually read (hashed, so a silently-changed input
    is detectable)."""
    return {
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "argv": sys.argv,
        "commit": commit_sha(),
        "python": sys.version.split()[0],
        "params": params,
        "datasets": [{"path": p, "sha256": file_sha256(p)} for p in sorted(dataset_paths)],
    }


def write_run(out_dir: str, man: dict, rows: list[dict]) -> None:
    os.makedirs(out_dir, exist_ok=True)
    json.dump(man, open(os.path.join(out_dir, "manifest.json"), "w"), indent=2)
    with open(os.path.join(out_dir, "rows.jsonl"), "w") as f:
        for r in rows:
            f.write(json.dumps(r) + "\n")


def read_rows(out_dir: str) -> list[dict]:
    with open(os.path.join(out_dir, "rows.jsonl")) as f:
        return [json.loads(line) for line in f if line.strip()]


def read_manifest(out_dir: str) -> dict:
    p = os.path.join(out_dir, "manifest.json")
    return json.load(open(p)) if os.path.exists(p) else {}
