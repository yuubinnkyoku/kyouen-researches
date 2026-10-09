#!/usr/bin/env python3
"""Cross-check a rebuilt S5 class boundary against every saved cache/replay CSV."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--boundary", required=True, type=Path)
    parser.add_argument("--class-lo", required=True, type=int)
    parser.add_argument("--class-hi", required=True, type=int)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--root", required=True, type=Path, action="append")
    args = parser.parse_args()

    boundary = json.loads(args.boundary.read_text(encoding="utf-8"))
    child_rows = boundary["boundary"]["children"]
    keys = {tuple(map(int, row["key"])) for row in child_rows}
    if len(keys) != boundary["boundary"]["canonical_children"]:
        raise SystemExit("boundary contains duplicate or malformed canonical keys")
    exact: dict[tuple[int, int], list[dict[str, object]]] = defaultdict(list)
    unknown: dict[tuple[int, int], list[dict[str, object]]] = defaultdict(list)
    conflicts: list[dict[str, object]] = []
    scanned_files = 0
    parsed_rows = 0

    files: set[Path] = set()
    for root in args.root:
        if not root.exists():
            continue
        files.update(path for path in root.rglob("*") if path.is_file() and path.suffix.lower() in {".cache", ".csv"})
    for path in sorted(files):
        scanned_files += 1
        try:
            handle = path.open(newline="", encoding="utf-8-sig")
        except (OSError, UnicodeError):
            continue
        with handle:
            for line_number, row in enumerate(csv.reader(handle), 1):
                if not row:
                    continue
                parsed_rows += 1
                try:
                    if row[0] == "s5verdict" and len(row) >= 6 and int(row[3]) == 5:
                        key = (int(row[1]), int(row[2]))
                        verdict, nodes = int(row[4]), int(row[5])
                        budget = None
                        kind = "cache"
                    elif row[0] == "replay" and len(row) >= 11 and int(row[2]) == 5:
                        key = (int(row[9]), int(row[10]))
                        verdict, nodes = int(row[6]), int(row[7])
                        budget = int(row[5])
                        kind = "replay"
                    else:
                        continue
                except (ValueError, IndexError):
                    continue
                if key not in keys:
                    continue
                evidence = {
                    "path": str(path),
                    "line": line_number,
                    "kind": kind,
                    "verdict": verdict if verdict in (1, 2) else None,
                    "nodes": nodes,
                    "budget": budget,
                }
                if verdict in (1, 2):
                    exact[key].append(evidence)
                elif verdict == 0:
                    unknown[key].append(evidence)

    for key, records in sorted(exact.items()):
        verdicts = sorted({int(record["verdict"]) for record in records})
        if len(verdicts) > 1:
            conflicts.append({"key": list(key), "verdicts": verdicts, "sources": records})

    exact_verdicts = {key: next(iter({int(record["verdict"]) for record in records})) for key, records in exact.items() if records}
    merged: dict[tuple[int, int], int] = {}
    for row in child_rows:
        key = tuple(map(int, row["key"]))
        cache_verdict = row.get("verdict")
        if cache_verdict in (1, 2):
            previous = merged.get(key)
            if previous is not None and previous != cache_verdict:
                conflicts.append({"key": list(key), "verdicts": sorted({previous, cache_verdict}), "sources": ["boundary-audit"]})
            merged[key] = cache_verdict
        if key in exact_verdicts:
            previous = merged.get(key)
            if previous is not None and previous != exact_verdicts[key]:
                conflicts.append({"key": list(key), "verdicts": sorted({previous, exact_verdicts[key]}), "sources": exact[key]})
            merged[key] = exact_verdicts[key]

    result = {
        "schema": "n11-reply27-target-boundary-history-audit-v1",
        "class_key": [args.class_lo, args.class_hi],
        "canonical_children": len(keys),
        "scanned_files": scanned_files,
        "parsed_csv_rows": parsed_rows,
        "exact_child_keys_with_saved_evidence": len(exact),
        "exact_evidence_records": sum(map(len, exact.values())),
        "same_budget_unknown_child_keys": len({k for k, records in unknown.items() if any(r["budget"] == 15_000_000 for r in records)}),
        "verdict_conflict_count": len(conflicts),
        "conflicts": conflicts,
        "exact_children": [
            {"key": list(key), "verdict": exact_verdicts[key], "sources": records}
            for key, records in sorted(exact.items())
        ],
        "unknown_child_records": [
            {"key": list(key), "sources": records}
            for key, records in sorted(unknown.items())
        ],
        "status_counts": {
            "WIN": sum(value == 1 for value in merged.values()),
            "LOSS": sum(value == 2 for value in merged.values()),
            "UNKNOWN": len(keys - set(merged)),
        },
        "roots": [str(root) for root in args.root],
        "boundary_sha256": sha256(args.boundary),
    }
    args.out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: result[k] for k in (
        "class_key", "canonical_children", "scanned_files", "parsed_csv_rows",
        "exact_child_keys_with_saved_evidence", "exact_evidence_records",
        "same_budget_unknown_child_keys", "verdict_conflict_count", "status_counts"
    )}, indent=2))
    if conflicts:
        raise SystemExit("saved exact verdict conflicts found")


if __name__ == "__main__":
    main()
