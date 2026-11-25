#!/usr/bin/env python3
"""Reconcile every saved exact s5 cache against the reply27 checkpoint cache.

This audits persisted rows only. It invokes the repository's canonical safe-key
validator and does not run the game solver.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "research/experiments/n11-frontier-selection-20261005/scripts"
sys.path.insert(0, str(SCRIPTS))
from merge_exact_s5_evidence import merge  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def is_exact_s5_cache(path: Path) -> bool:
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if row and not row[0].lstrip().startswith("#"):
                return len(row) == 6 and row[0] == "s5verdict" and row[3] == "5"
    return False


def read_cache(path: Path) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.reader(f):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise ValueError(f"invalid exact s5 row in {path}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if key in result and result[key] != verdict:
                raise ValueError(f"in-file verdict conflict in {path}: {key}")
            result[key] = verdict
    return result


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--checkpoint-cache", type=Path, required=True)
    ap.add_argument("--root", type=Path, action="append", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    caches = sorted({p for root in args.root for p in root.rglob("*.cache")
                     if is_exact_s5_cache(p)})
    if not any(p.resolve() == args.checkpoint_cache.resolve() for p in caches):
        raise SystemExit("checkpoint cache was not discovered under the supplied roots")

    union, receipt = merge(caches, [])
    checkpoint = read_cache(args.checkpoint_cache)
    extra = {k: v for k, v in union.items() if k not in checkpoint}
    missing = {k: v for k, v in checkpoint.items() if k not in union}

    origins: dict[tuple[int, int], list[str]] = defaultdict(list)
    for path in caches:
        with path.open(newline="", encoding="utf-8-sig") as f:
            for row in csv.reader(f):
                if row and row[0] == "s5verdict":
                    origins[(int(row[1]), int(row[2]))].append(relative(path))

    counts = {"WIN": sum(v == 1 for v in checkpoint.values()),
              "LOSS": sum(v == 2 for v in checkpoint.values())}
    report = {
        "schema": "n11-reply27-s5-cache-corpus-audit-v1",
        "claim": "Persisted exact s5 cache rows were canonicalized and merged; this audit does not infer verdicts.",
        "cache_files_discovered": len(caches),
        "cache_files": receipt["sources"],
        "corpus_unique_exact_rows": len(union),
        "checkpoint_cache": {
            "path": relative(args.checkpoint_cache),
            "sha256": sha256(args.checkpoint_cache),
            "unique_exact_rows": len(checkpoint),
            "counts": counts,
        },
        "corpus_conflicts": receipt["conflicts"],
        "corpus_vs_checkpoint_extra_rows": [
            {"key": list(k), "verdict": v, "sources": origins[k]}
            for k, v in sorted(extra.items())
        ],
        "checkpoint_rows_missing_from_corpus": [
            {"key": list(k), "verdict": v} for k, v in sorted(missing.items())
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("S5_CACHE_CORPUS_AUDIT_OK " + json.dumps({
        "cache_files": len(caches),
        "corpus_rows": len(union),
        "checkpoint_rows": len(checkpoint),
        "conflicts": receipt["conflicts"],
        "extra": len(extra),
        "missing": len(missing),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
