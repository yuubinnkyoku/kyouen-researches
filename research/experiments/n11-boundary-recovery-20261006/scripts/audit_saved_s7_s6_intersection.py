#!/usr/bin/env python3
"""Audit saved exact s7 rows against unresolved canonical s6 children."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE = ROOT / "research/experiments/n11-search-methods/scripts"
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(EDGE))
sys.path.insert(0, str(HERE))

from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
from audit_saved_s6_targets import points, safe_canonical, sha256  # noqa: E402
from prepare_s7_witness_probe import read_s7_cache_line, read_s7_row, scan_files  # noqa: E402


def relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--s6-runner-summary", type=Path, required=True)
    ap.add_argument("--scan-root", type=Path, action="append", required=True)
    ap.add_argument("--out", type=Path, required=True)
    ap.add_argument("--sources-out", type=Path, required=True)
    args = ap.parse_args()
    if args.out.exists() or args.sources_out.exists():
        raise SystemExit("refusing to overwrite an existing audit output")

    runner = json.loads(args.s6_runner_summary.read_text(encoding="utf-8"))
    parents = runner.get("parents")
    if not isinstance(parents, list) or not parents:
        raise SystemExit("s6 runner summary has no parent boundaries")
    unresolved: set[tuple[int, int]] = set()
    for row in parents:
        if row.get("outcome") != "UNKNOWN":
            raise SystemExit("expected only unresolved s6 parents in this audit")
        for raw in row.get("unresolved_children", []):
            key = tuple(map(int, raw))
            if len(key) != 2 or not safe_canonical(key, 6):
                raise SystemExit(f"unsafe/noncanonical s6 key: {key}")
            unresolved.add(key)
    if not unresolved:
        raise SystemExit("no unresolved s6 keys")

    parent_children: dict[tuple[int, int], set[tuple[int, int]]] = {}
    child_parents: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    legal_counts: dict[tuple[int, int], int] = {}
    for parent in sorted(unresolved):
        occupied = set(points(parent))
        children = set()
        for move in legal_after(occupied):
            raw_points = tuple(sorted((*occupied, move)))
            if len(raw_points) != 7 or has_forbidden_quad(raw_points):
                raise SystemExit(f"unsafe legal s7 extension {parent} + {move}")
            child = tuple(d4_canonical_key(raw_points))
            if not safe_canonical(child, 7):
                raise SystemExit(f"unsafe/noncanonical s7 child: {child}")
            predecessors = {
                tuple(d4_canonical_key([point for point in raw_points if point != removed]))
                for removed in raw_points
            }
            if parent not in predecessors:
                raise SystemExit(f"canonical reverse incidence failed: {parent} -> {child}")
            children.add(child)
            child_parents[child].add(parent)
            legal = len(legal_after(set(raw_points)))
            previous = legal_counts.setdefault(child, legal)
            if previous != legal:
                raise SystemExit(f"inconsistent legal count for shared s7 child {child}")
        parent_children[parent] = children

    boundary = set(child_parents)
    found: dict[tuple[int, int], list[dict]] = defaultdict(list)
    scanned = scan_files(args.scan_root)
    source_files: dict[Path, dict] = {}
    for path in scanned:
        matches = []
        if path.suffix.lower() == ".cache":
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                record = read_s7_cache_line(line, path, line_no)
                if record is not None and record["key"] in boundary:
                    found[record["key"]].append(record)
                    matches.append({"line": line_no, "key": list(record["key"]),
                                    "verdict": record["verdict"], "budget": None})
        else:
            with path.open(newline="", encoding="utf-8-sig") as stream:
                for row_no, row in enumerate(csv.reader(stream), 1):
                    record = read_s7_row(row, path, row_no)
                    if record is not None and record["key"] in boundary:
                        found[record["key"]].append(record)
                        matches.append({"line": row_no, "key": list(record["key"]),
                                        "raw_key": list(record["raw_key"]),
                                        "verdict": record["verdict"], "budget": record["budget"]})
        if matches:
            source_files[path] = {"path": relpath(path), "sha256": sha256(path), "rows": matches}

    exact: dict[tuple[int, int], int] = {}
    conflicts = []
    for key, rows in found.items():
        verdicts = {int(row["verdict"]) for row in rows if int(row["verdict"]) in (1, 2)}
        if len(verdicts) > 1:
            conflicts.append({"key": list(key), "verdicts": sorted(verdicts)})
        elif verdicts:
            exact[key] = next(iter(verdicts))
    if conflicts:
        raise SystemExit(f"saved exact s7 verdict conflict(s): {conflicts[:3]}")

    parent_results = []
    for parent, children in sorted(parent_children.items()):
        wins = sum(exact.get(key) == 1 for key in children)
        losses = sum(exact.get(key) == 2 for key in children)
        unknown = len(children) - wins - losses
        if losses:
            outcome = "WIN"  # an exact s7 LOSS witnesses this s6 OR-parent WIN
        elif wins == len(children):
            outcome = "LOSS"
        else:
            outcome = "UNKNOWN"
        parent_results.append({
            "s6_key": list(parent),
            "canonical_s7_children": len(children),
            "saved_exact_s7": {"WIN": wins, "LOSS": losses, "UNSEEN_OR_UNKNOWN": unknown},
            "saved_exact_loss_witnesses": [list(key) for key in sorted(children) if exact.get(key) == 2],
            "exact_outcome_from_saved_s7": outcome,
        })

    source_entries = [
        {"path": relpath(args.s6_runner_summary), "sha256": sha256(args.s6_runner_summary)},
        {"path": relpath(Path(__file__).resolve()), "sha256": sha256(Path(__file__).resolve())},
        {"path": relpath(HERE / "prepare_s7_witness_probe.py"),
         "sha256": sha256(HERE / "prepare_s7_witness_probe.py")},
        {"path": relpath(HERE / "audit_saved_s6_targets.py"),
         "sha256": sha256(HERE / "audit_saved_s6_targets.py")},
        {"path": relpath(EDGE / "dfpn_edge_classes.py"), "sha256": sha256(EDGE / "dfpn_edge_classes.py")},
        *[{"path": source_files[path]["path"], "sha256": source_files[path]["sha256"]}
          for path in sorted(source_files)],
    ]
    source_doc = {
        "schema": "n11-saved-s7-s6-intersection-sources-v1",
        "sources": source_entries,
        "scan_roots": [relpath(path) for path in args.scan_root],
        "scanned_file_count": len(scanned),
    }
    result = {
        "schema": "n11-saved-s7-s6-intersection-v1",
        "claim": "saved exact s7 intersection only; no solver replay; absent and UNKNOWN rows remain UNKNOWN",
        "input_s6_runner_summary": {"path": relpath(args.s6_runner_summary),
                                     "sha256": sha256(args.s6_runner_summary)},
        "s6_unknown_count": len(unresolved),
        "unique_canonical_s7_boundary_count": len(boundary),
        "saved_exact_s7_key_count": len(exact),
        "saved_exact_s7_sources": len(source_files),
        "conflict_count": 0,
        "s6_outcomes": {name: sum(row["exact_outcome_from_saved_s7"] == name for row in parent_results)
                         for name in ("WIN", "LOSS", "UNKNOWN")},
        "s6_parents": parent_results,
        "source_manifest": source_doc,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    source_doc["generated"] = [{"path": relpath(args.out), "sha256": sha256(args.out)}]
    args.sources_out.parent.mkdir(parents=True, exist_ok=True)
    args.sources_out.write_text(json.dumps(source_doc, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in result.items() if key != "s6_parents"}, indent=2))
    print("SAVED_S7_S6_INTERSECTION_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
