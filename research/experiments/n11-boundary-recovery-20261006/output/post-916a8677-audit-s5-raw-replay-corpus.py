#!/usr/bin/env python3
"""Audit saved five-stone raw replay rows against an exact S5 cache."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SEARCH = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(SEARCH))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"key outside n=11 board: {key}")
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def load_cache(path: Path) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8-sig") as f:
        for line_no, row in enumerate(csv.reader(f), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise ValueError(f"invalid current cache row {path}:{line_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2) or len(points(key)) != 5 or has_forbidden_quad(points(key)) \
                    or tuple(d4_canonical_key(points(key))) != key:
                raise ValueError(f"unsafe/noncanonical current cache row {path}:{line_no}: {row}")
            if key in result and result[key] != verdict:
                raise ValueError(f"current cache conflict for {key}")
            result[key] = verdict
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--current-cache", type=Path, required=True)
    ap.add_argument("--root", type=Path, action="append", required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()

    cache = load_cache(args.current_cache)
    observations: dict[tuple[int, int], list[dict]] = defaultdict(list)
    files: list[dict] = []
    roots = []
    for root in args.root:
        paths = sorted(root.rglob("*.csv"))
        s5_rows = 0
        exact_rows = 0
        for path in paths:
            matched = []
            with path.open(newline="", encoding="utf-8-sig") as f:
                for row_no, row in enumerate(csv.reader(f), 1):
                    if not row or row[0] != "replay":
                        continue
                    if len(row) != 11:
                        raise SystemExit(f"malformed replay row {path}:{row_no}: {row}")
                    if int(row[2]) != 5 or int(row[4]) != 0:
                        continue
                    raw_key = (int(row[9]), int(row[10]))
                    pts = points(raw_key)
                    if len(pts) != 5 or has_forbidden_quad(pts):
                        raise SystemExit(f"unsafe s5 replay row {path}:{row_no}: {raw_key}")
                    key = tuple(d4_canonical_key(pts))
                    legal, budget, verdict, nodes = map(int, (row[3], row[5], row[6], row[7]))
                    if legal != len(legal_after(set(pts))) or verdict not in (0, 1, 2) or nodes < 0:
                        raise SystemExit(f"invalid s5 replay geometry/result {path}:{row_no}: {row}")
                    item = {"path": relative(path), "row": row_no,
                            "raw_key": list(raw_key), "canonical_key": list(key),
                            "normalized_noncanonical": raw_key != key, "legal_count": legal,
                            "budget": budget, "verdict": verdict, "nodes": nodes}
                    observations[key].append(item)
                    matched.append(item)
                    s5_rows += 1
                    exact_rows += verdict in (1, 2)
            if matched:
                files.append({"path": relative(path), "sha256": digest(path),
                              "bytes": path.stat().st_size, "s5_replay_rows": len(matched),
                              "exact_s5_replay_rows": sum(r["verdict"] in (1, 2) for r in matched)})
        roots.append({"path": relative(root), "csv_files_examined": len(paths),
                      "s5_replay_rows": s5_rows, "exact_s5_replay_rows": exact_rows})

    exact: dict[tuple[int, int], int] = {}
    conflicts = []
    budget_counts: Counter[int] = Counter()
    verdict_counts: Counter[int] = Counter()
    for key, rows in sorted(observations.items()):
        vals = sorted({r["verdict"] for r in rows if r["verdict"] in (1, 2)})
        if len(vals) > 1:
            conflicts.append({"key": list(key), "verdicts": vals, "rows": rows})
        elif vals:
            exact[key] = vals[0]
        for row in rows:
            verdict_counts[row["verdict"]] += 1
            if row["verdict"] in (1, 2):
                budget_counts[row["budget"]] += 1

    cache_replay_conflicts = [
        {"key": list(k), "cache_verdict": cache[k], "raw_verdict": exact[k]}
        for k in sorted(cache.keys() & exact.keys()) if cache[k] != exact[k]
    ]
    extra = {k: v for k, v in exact.items() if k not in cache}
    cache_only = {k: v for k, v in cache.items() if k not in exact}
    report = {
        "schema": "n11-reply27-s5-raw-replay-corpus-audit-v1",
        "claim": "Saved raw replay rows were geometry-audited and compared to the exact cache; no solver was run.",
        "roots": roots,
        "source_files_with_s5_replay_rows": files,
        "raw_s5_replay_rows": sum(verdict_counts.values()),
        "raw_exact_s5_replay_rows": sum(verdict_counts[v] for v in (1, 2)),
        "raw_verdict_counts": {str(k): verdict_counts[k] for k in sorted(verdict_counts)},
        "exact_replay_budget_counts": {str(k): budget_counts[k] for k in sorted(budget_counts)},
        "raw_unique_exact_s5_keys": len(exact),
        "raw_exact_verdict_conflicts": conflicts,
        "current_cache": {"path": relative(args.current_cache), "sha256": digest(args.current_cache),
                          "entries": len(cache), "WIN": sum(v == 1 for v in cache.values()),
                          "LOSS": sum(v == 2 for v in cache.values())},
        "cache_raw_verdict_conflicts": cache_replay_conflicts,
        "raw_exact_not_in_cache": [
            {"key": list(k), "verdict": v,
             "rows": [r for r in observations[k] if r["verdict"] in (1, 2)]}
            for k, v in sorted(extra.items())
        ],
        "cache_rows_without_raw_s5_replay": [
            {"key": list(k), "verdict": v} for k, v in sorted(cache_only.items())
        ],
        "same_budget_unknown_rows": [
            {"key": list(k), **r} for k, rows in sorted(observations.items()) for r in rows
            if r["verdict"] == 0 and r["budget"] >= 15_000_000
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print("S5_RAW_REPLAY_CORPUS_AUDIT_OK " + json.dumps({
        "s5_rows": report["raw_s5_replay_rows"],
        "raw_exact_keys": len(exact),
        "cache_entries": len(cache),
        "raw_conflicts": len(conflicts),
        "cache_conflicts": len(cache_replay_conflicts),
        "extra_exact": len(extra),
        "cache_only": len(cache_only),
        "same_budget_unknown": len(report["same_budget_unknown_rows"]),
    }, sort_keys=True))


if __name__ == "__main__":
    main()
