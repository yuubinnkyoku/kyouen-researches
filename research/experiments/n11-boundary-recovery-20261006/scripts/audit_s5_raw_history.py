#!/usr/bin/env python3
"""Find prior raw exact-replay evidence for a fixed set of canonical s5 keys."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"key outside n=11 board: {key}")
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def safe_canonical(key: tuple[int, int], stones: int) -> bool:
    pts = points(key)
    return len(pts) == stones and not has_forbidden_quad(pts) \
        and tuple(d4_canonical_key(pts)) == key


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def relative(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def read_targets(path: Path) -> dict[tuple[int, int], dict]:
    result = {}
    for line_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
            raise SystemExit(f"not an s5 AND target: {path}:{line_no}: {row}")
        key = (int(row[3]), int(row[4]))
        if not safe_canonical(key, 5) or key in result:
            raise SystemExit(f"unsafe, noncanonical or duplicate s5 target: {path}:{line_no}: {key}")
        legal = len(legal_after(set(points(key))))
        if int(row[5]) != legal:
            raise SystemExit(f"target legal-count mismatch: {path}:{line_no}: {key}")
        result[key] = {"legal_count": legal, "target_row": line_no}
    if not result:
        raise SystemExit(f"no s5 targets in {path}")
    return result


def read_cache(path: Path | None) -> dict[tuple[int, int], int]:
    if path is None:
        return {}
    result = {}
    for line_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid exact cache row: {path}:{line_no}: {row}")
        key, value = (int(row[1]), int(row[2])), int(row[4])
        if not safe_canonical(key, 5) or value not in (1, 2):
            raise SystemExit(f"invalid exact cache evidence: {path}:{line_no}: {row}")
        old = result.get(key)
        if old is not None and old != value:
            raise SystemExit(f"cache verdict conflict for {key}: {old} vs {value}")
        result[key] = value
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--targets", type=Path, required=True)
    parser.add_argument("--root", type=Path, action="append", required=True,
                        help="directory recursively searched for CSV replay outputs; repeatable")
    parser.add_argument("--current-cache", type=Path)
    parser.add_argument("--budget", type=int, default=15_000_000)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.budget < 1:
        parser.error("budget must be positive")

    targets = read_targets(args.targets)
    cache = read_cache(args.current_cache)
    cache_hits = {key: value for key, value in cache.items() if key in targets}
    observations: dict[tuple[int, int], list[dict]] = defaultdict(list)
    examined = 0
    replay_rows = 0
    matching_paths: dict[Path, list[dict]] = defaultdict(list)
    scanned_files = []
    root_receipts = []

    for root in args.root:
        if not root.is_dir():
            raise SystemExit(f"search root does not exist: {root}")
        files = sorted(root.rglob("*.csv"))
        root_rows = 0
        for path in files:
            examined += 1
            found_in_file = []
            file_replay_rows = 0
            with path.open(newline="", encoding="utf-8-sig") as stream:
                for row_no, row in enumerate(csv.reader(stream), 1):
                    if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                        continue
                    if len(row) != 11:
                        raise SystemExit(f"malformed replay row: {path}:{row_no}: {row}")
                    if int(row[2]) != 5 or int(row[4]) != 0:
                        continue
                    replay_rows += 1
                    root_rows += 1
                    file_replay_rows += 1
                    raw_key = (int(row[9]), int(row[10]))
                    pts = points(raw_key)
                    if len(pts) != 5 or has_forbidden_quad(pts):
                        raise SystemExit(f"unsafe s5 replay row: {path}:{row_no}: {raw_key}")
                    key = tuple(d4_canonical_key(pts))
                    if key not in targets:
                        continue
                    if not safe_canonical(key, 5):
                        raise SystemExit(f"canonical s5 replay key is unsafe: {path}:{row_no}: {key}")
                    legal, budget, verdict, nodes = map(int, (row[3], row[5], row[6], row[7]))
                    if legal != targets[key]["legal_count"] or verdict not in (0, 1, 2) or nodes < 0:
                        raise SystemExit(f"target replay geometry/result fields mismatch: {path}:{row_no}: {row}")
                    item = {"path": relative(path), "row": row_no, "sha256": None,
                            "raw_key": list(raw_key), "canonical_key": list(key),
                            "normalized_noncanonical": raw_key != key,
                            "budget": budget, "verdict": verdict, "nodes": nodes,
                            "legal_count": legal}
                    observations[key].append(item)
                    found_in_file.append(item)
            if found_in_file:
                matching_paths[path] = found_in_file
            scanned_files.append({"path": relative(path), "sha256": digest(path),
                                  "bytes": path.stat().st_size,
                                  "s5_replay_rows": file_replay_rows})
        root_receipts.append({"path": relative(root), "csv_files_examined": len(files),
                              "s5_replay_rows_examined": root_rows})

    for path, rows in matching_paths.items():
        file_hash = digest(path)
        for item in rows:
            item["sha256"] = file_hash

    conflicts = []
    exact = {}
    same_budget_unknown = []
    lower_budget_unknown = []
    for key, rows in sorted(observations.items()):
        exact_values = sorted({row["verdict"] for row in rows if row["verdict"] in (1, 2)})
        if len(exact_values) > 1:
            conflicts.append({"key": list(key), "verdicts": exact_values, "rows": rows})
        elif exact_values:
            exact[key] = exact_values[0]
        for row in rows:
            if row["verdict"] == 0:
                if row["budget"] >= args.budget:
                    same_budget_unknown.append({"key": list(key), **row})
                else:
                    lower_budget_unknown.append({"key": list(key), **row})
            elif key in cache_hits and row["verdict"] in (1, 2) and cache_hits[key] != row["verdict"]:
                conflicts.append({"key": list(key), "cache_verdict": cache_hits[key], "row": row})

    result = {
        "schema": "n11-s5-raw-history-audit-v1",
        "requested_budget": args.budget,
        "targets": {"path": relative(args.targets), "sha256": digest(args.targets),
                    "count": len(targets),
                    "keys": [list(key) for key in sorted(targets)]},
        "search_roots": root_receipts,
        "csv_files_examined": examined,
        "s5_replay_rows_examined": replay_rows,
        "scanned_csv_sources": scanned_files,
        "matching_replay_rows": sum(map(len, observations.values())),
        "matching_source_files": [{"path": relative(path), "sha256": digest(path),
                                    "matching_rows": len(rows)}
                                   for path, rows in sorted(matching_paths.items())],
        "observations": {f"{key[0]},{key[1]}": rows for key, rows in sorted(observations.items())},
        "prior_exact": {f"{key[0]},{key[1]}": value for key, value in sorted(exact.items())},
        "prior_unknown_same_budget_or_higher": same_budget_unknown,
        "prior_unknown_below_budget": lower_budget_unknown,
        "current_cache": {"path": relative(args.current_cache) if args.current_cache else None,
                          "sha256": digest(args.current_cache) if args.current_cache else None,
                          "entries": len(cache), "target_exact_intersection": len(cache_hits),
                          "hits": {f"{key[0]},{key[1]}": value for key, value in sorted(cache_hits.items())}},
        "exact_verdict_conflicts": conflicts,
        "audit_script": {"path": relative(Path(__file__).resolve()),
                         "sha256": digest(Path(__file__).resolve())},
        "dispatch_ready_keys": [list(key) for key in sorted(targets)
                                if key not in exact and key not in cache_hits
                                and key not in {tuple(row["key"]) for row in same_budget_unknown}],
        "interpretation": "Only exact replay rows and validated cache rows provide verdicts. UNKNOWN rows remain UNKNOWN; a same-or-higher-budget UNKNOWN is excluded from direct s5 replay.",
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"targets": len(targets), "csv_files_examined": examined,
                      "matching_rows": result["matching_replay_rows"],
                      "prior_exact": len(exact), "same_budget_unknown": len(same_budget_unknown),
                      "lower_budget_unknown": len(lower_budget_unknown),
                      "cache_hits": len(cache_hits), "conflicts": len(conflicts),
                      "dispatch_ready": len(result["dispatch_ready_keys"])}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
