#!/usr/bin/env python3
"""Select low-legal-count S5 probes only from the audited dispatch-ready set."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[4]


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def record(path: Path) -> dict[str, Any]:
    return {"path": rel(path), "bytes": path.stat().st_size, "sha256": sha(path)}


def read_cache(path: Path) -> set[tuple[int, int]]:
    keys: set[tuple[int, int]] = set()
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise SystemExit(f"invalid exact cache row {line_no}: {row}")
            key, verdict = (int(row[1]), int(row[2])), int(row[4])
            if verdict not in (1, 2) or key in keys:
                raise SystemExit(f"non-exact or duplicate cache key: {key}")
            keys.add(key)
    return keys


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all-targets", type=Path, required=True)
    parser.add_argument("--raw-audit", type=Path, required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--solver", type=Path, required=True)
    parser.add_argument("--solver-source", type=Path, required=True)
    parser.add_argument("--runner", type=Path, required=True)
    parser.add_argument("--dispatch-main", required=True)
    parser.add_argument("--targets-out", type=Path, required=True)
    parser.add_argument("--manifest-out", type=Path, required=True)
    parser.add_argument("--count", type=int, default=8)
    parser.add_argument("--budget", type=int, default=15_000_000)
    args = parser.parse_args()
    if args.count < 1 or args.budget < 1:
        raise SystemExit("count and budget must be positive")
    for path in (args.targets_out, args.manifest_out):
        if path.exists():
            raise SystemExit(f"refusing to overwrite schedule artifact: {path}")

    audit = json.loads(args.raw_audit.read_text(encoding="utf-8"))
    if audit["targets"]["sha256"] != sha(args.all_targets):
        raise SystemExit("full raw-history audit is for a different geometry target CSV")
    if audit["current_cache"]["sha256"] != sha(args.cache):
        raise SystemExit("full raw-history audit is for a different exact cache")
    if audit["requested_budget"] != args.budget or audit["exact_verdict_conflicts"]:
        raise SystemExit("full raw-history audit has a budget mismatch or verdict conflict")

    rows: dict[tuple[int, int], list[str]] = {}
    with args.all_targets.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
                raise SystemExit(f"invalid S5 target row {line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            if key in rows:
                raise SystemExit(f"duplicate canonical target: {key}")
            rows[key] = row

    cache_keys = read_cache(args.cache)
    ready = {tuple(map(int, key)) for key in audit["dispatch_ready_keys"]}
    blocked = {tuple(map(int, item.get("canonical_key", item["key"])))
               for item in audit.get("prior_unknown_same_budget_or_higher", [])}
    if not ready or not ready <= rows.keys() or ready & cache_keys or ready & blocked:
        raise SystemExit("raw-history dispatch-ready set conflicts with geometry/cache/blocked history")
    selected = sorted(ready, key=lambda key: (int(rows[key][5]), key))[:args.count]
    if len(selected) != min(args.count, len(ready)):
        raise SystemExit("selected target count mismatch")

    args.targets_out.parent.mkdir(parents=True, exist_ok=True)
    with args.targets_out.open("w", newline="", encoding="utf-8") as stream:
        stream.write("# low-legal-count exact S5 probes; ordering is scheduling only\n")
        writer = csv.writer(stream, lineterminator="\n")
        for sequence, key in enumerate(selected, 1):
            row = list(rows[key])
            row[1] = str(sequence)
            writer.writerow(row)

    source_paths = [args.all_targets, args.raw_audit, args.cache, Path(__file__).resolve(),
                    args.solver, args.solver_source, args.runner]
    manifest = {
        "schema": "n11-reply27-next-s5-probe-selection-v1",
        "dispatch_main_commit": args.dispatch_main,
        "class_key": [1152921504741065728, 68719476736],
        "claim": "Scheduling only. The selected S5 positions remain UNKNOWN until an exact solver verdict or valid S6 witness is obtained.",
        "selection_rule": "full current raw-history dispatch-ready keys sorted by legal count ascending, then canonical key",
        "budget": args.budget, "budget_per_target": args.budget,
        "count_requested": args.count, "probe_count": len(selected),
        "canonical_class_children": len(rows), "cache_exact_children": audit["current_cache"]["target_exact_intersection"],
        "dispatch_ready_count": len(ready), "blocked_same_or_higher_budget_unknown_keys": [list(key) for key in sorted(blocked)],
        "probe_target_sha256": sha(args.targets_out), "probe_targets": [list(key) for key in selected],
        "selected": [{"rank": i, "key": list(key), "legal_count": int(rows[key][5])}
                     for i, key in enumerate(selected, 1)],
        "sources": [record(path) for path in source_paths],
        "targets_out": record(args.targets_out),
    }
    args.manifest_out.parent.mkdir(parents=True, exist_ok=True)
    args.manifest_out.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n",
                                 encoding="utf-8", newline="\n")
    print(json.dumps({"selected": len(selected), "dispatch_ready": len(ready),
                      "blocked_same_budget_unknowns_excluded": len(blocked),
                      "keys": [list(key) for key in selected]}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
