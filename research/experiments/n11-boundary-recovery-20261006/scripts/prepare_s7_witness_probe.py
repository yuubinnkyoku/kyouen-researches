#!/usr/bin/env python3
"""Audit a small complete s7 boundary and prepare exact-loss witness probes for s6 OR parents."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from itertools import combinations
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
sys.path.insert(0, str(ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"))
from audit_saved_s6_targets import points, safe_canonical, sha256  # noqa: E402


def relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def scan_files(roots: list[Path]) -> list[Path]:
    found = set()
    for root in roots:
        root = root.resolve()
        if not root.exists():
            raise SystemExit(f"raw-history scan root does not exist: {root}")
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in {".csv", ".out", ".txt", ".cache"}:
                found.add(path.resolve())
    return sorted(found)


def read_s7_row(row: list[str], path: Path, row_no: int) -> dict | None:
    if not row or row[0].lstrip().startswith("#"):
        return None
    if row[0] != "replay" or len(row) < 3:
        return None
    if not row[2].isdigit() or int(row[2]) != 7:
        return None
    if len(row) != 11 or int(row[4]) != 0:
        raise ValueError(f"invalid s7 AND replay at {path}:{row_no}: {row}")
    raw_key = (int(row[9]), int(row[10]))
    raw_points = points(raw_key)
    if len(raw_points) != 7 or has_forbidden_quad(raw_points):
        raise ValueError(f"unsafe s7 raw replay at {path}:{row_no}: {raw_key}")
    key = tuple(d4_canonical_key(raw_points))
    verdict, budget, nodes, legal = int(row[6]), int(row[5]), int(row[7]), int(row[3])
    if verdict not in (0, 1, 2) or budget <= 0 or nodes < 0:
        raise ValueError(f"invalid s7 replay result at {path}:{row_no}: {row}")
    if not safe_canonical(key, 7):
        raise ValueError(f"canonical s7 replay is unsafe: {key}")
    actual_legal = len(legal_after(set(points(key))))
    if legal != actual_legal:
        raise ValueError(f"s7 legal-count mismatch at {path}:{row_no}: {legal} != {actual_legal}")
    return {"key": key, "raw_key": raw_key, "verdict": verdict, "budget": budget,
            "nodes": nodes, "legal": legal, "path": relpath(path), "row": row_no}


def read_s7_cache_line(line: str, path: Path, line_no: int) -> dict | None:
    if not line.startswith("s7verdict,"):
        return None
    fields = line.split(",")
    if len(fields) != 6 or fields[0] != "s7verdict" or int(fields[3]) != 7:
        raise ValueError(f"invalid s7 cache row at {path}:{line_no}: {line}")
    key = (int(fields[1]), int(fields[2]))
    verdict = int(fields[4])
    if verdict not in (1, 2) or not safe_canonical(key, 7):
        raise ValueError(f"invalid/noncanonical exact s7 cache row at {path}:{line_no}: {line}")
    return {"key": key, "raw_key": key, "verdict": verdict, "budget": None,
            "nodes": None, "legal": None, "path": relpath(path), "row": line_no,
            "source_kind": "s7verdict_cache"}


def choose_cover(parents: list[tuple[int, int]], eligible: dict[tuple[int, int], set[tuple[int, int]]],
                 legal_counts: dict[tuple[int, int], int]) -> list[tuple[int, int]]:
    """Minimize distinct S7 probes needed to place a LOSS witness opportunity on every s6 parent."""
    parent_index = {key: i for i, key in enumerate(parents)}
    masks: dict[int, list[tuple[int, int]]] = defaultdict(list)
    for child, child_parents in eligible.items():
        mask = 0
        for parent in child_parents:
            if parent in parent_index:
                mask |= 1 << parent_index[parent]
        if mask:
            masks[mask].append(child)
    choices = []
    for mask, children in masks.items():
        choices.append(min(children, key=lambda key: (legal_counts[key], key)))
    full = (1 << len(parents)) - 1
    best = None
    for size in range(1, len(parents) + 1):
        for combo in combinations(choices, size):
            mask = 0
            for key in combo:
                for parent in eligible[key]:
                    mask |= 1 << parent_index[parent]
            if mask != full:
                continue
            ordered = tuple(sorted(combo))
            score = (len(ordered), sum(legal_counts[key] for key in ordered), ordered)
            if best is None or score < best[0]:
                best = (score, list(ordered))
        if best is not None:
            break
    return best[1] if best else []


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s6-boundary-json", type=Path, required=True)
    parser.add_argument("--s6-boundary-full-gzip", type=Path, required=True)
    parser.add_argument("--scan-root", type=Path, action="append", required=True)
    parser.add_argument("--budget", type=int, default=1_000_000)
    parser.add_argument("--targets-out", type=Path, required=True)
    parser.add_argument("--audit-out", type=Path, required=True)
    args = parser.parse_args()
    if args.budget < 1:
        parser.error("--budget must be positive")

    boundary = json.loads(args.s6_boundary_json.read_text(encoding="utf-8"))
    full_doc = json.loads(gzip.decompress(args.s6_boundary_full_gzip.read_bytes()))
    parents_full = full_doc.get("targets", {}).get("parents", [])
    if len(parents_full) != 1 or len(parents_full[0].get("children", [])) != 90:
        raise SystemExit("expected one fully audited 90-child s5 parent boundary")
    parent_row = boundary["targets"]["parents"][0]
    if parent_row["outcome"] != "UNKNOWN" or parent_row["child_count"] != 90 or parent_row["counts"].get("UNKNOWN") != 3:
        raise SystemExit("s5 boundary no longer has exactly three unresolved s6 children")
    unknown_children = sorted(tuple(item["key"]) for item in parents_full[0]["children"]
                              if item["status"] == "UNKNOWN")
    if len(unknown_children) != 3:
        raise SystemExit(f"expected three exact-UNKNOWN s6 children, found {len(unknown_children)}")
    if any(not safe_canonical(key, 6) for key in unknown_children):
        raise SystemExit("unresolved s6 child is unsafe/noncanonical")

    parent_children: dict[tuple[int, int], set[tuple[int, int]]] = {}
    child_parents: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    child_legal: dict[tuple[int, int], int] = {}
    geometry_rows = []
    for parent in unknown_children:
        parent_points = set(points(parent))
        children = set()
        legal_moves = legal_after(parent_points)
        for move in legal_moves:
            child_points = tuple(sorted((*parent_points, move)))
            if len(child_points) != 7 or has_forbidden_quad(child_points):
                raise SystemExit(f"unsafe legal s7 extension: {parent} + {move}")
            child = tuple(d4_canonical_key(child_points))
            if not safe_canonical(child, 7):
                raise SystemExit(f"unsafe canonical s7 child: {child}")
            predecessors = {tuple(d4_canonical_key([p for p in child_points if p != removed]))
                            for removed in child_points}
            if parent not in predecessors:
                raise SystemExit(f"reverse incidence failure {parent} -> {child}")
            children.add(child)
            child_parents[child].add(parent)
            actual_legal = len(legal_after(set(child_points)))
            if child in child_legal and child_legal[child] != actual_legal:
                raise SystemExit(f"inconsistent s7 legal count for shared child {child}")
            child_legal[child] = actual_legal
        parent_children[parent] = children
        geometry_rows.append({"parent_s6": list(parent), "legal_extension_moves": len(legal_moves),
                              "canonical_s7_children": len(children)})

    boundary_s7 = set(child_parents)
    scanned = scan_files(args.scan_root)
    all_rows: dict[tuple[int, int], list[dict]] = defaultdict(list)
    source_files = []
    replay_rows = 0
    for path in scanned:
        matches = []
        if path.suffix.lower() == ".cache":
            for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                record = read_s7_cache_line(line, path, line_no)
                if record and record["key"] in boundary_s7:
                    all_rows[record["key"]].append(record)
                    matches.append({"row": line_no, "key": list(record["key"]), "verdict": record["verdict"],
                                    "budget": None, "source_kind": "s7verdict_cache"})
                    replay_rows += 1
        else:
            try:
                stream = path.open(newline="", encoding="utf-8-sig")
                for row_no, row in enumerate(csv.reader(stream), 1):
                    record = read_s7_row(row, path, row_no)
                    if record and record["key"] in boundary_s7:
                        all_rows[record["key"]].append(record)
                        matches.append({"row": row_no, "key": list(record["key"]),
                                        "verdict": record["verdict"], "budget": record["budget"],
                                        "raw_key": list(record["raw_key"])})
                        replay_rows += 1
            finally:
                stream.close()
        source_files.append({"path": relpath(path), "sha256": sha256(path), "bytes": path.stat().st_size,
                             "matching_s7_rows": matches})

    exact: dict[tuple[int, int], int] = {}
    same_or_higher_unknown: dict[tuple[int, int], list[dict]] = defaultdict(list)
    internal_conflicts = []
    for key, observations in all_rows.items():
        exact_values = {r["verdict"] for r in observations if r["verdict"] in (1, 2)}
        if len(exact_values) > 1:
            internal_conflicts.append({"key": list(key), "verdicts": sorted(exact_values),
                                       "observations": observations})
        elif exact_values:
            exact[key] = next(iter(exact_values))
        for record in observations:
            if record["verdict"] == 0 and record["budget"] is not None and record["budget"] >= args.budget:
                same_or_higher_unknown[key].append(record)
    if internal_conflicts:
        raise SystemExit(f"saved s7 exact verdict conflicts: {len(internal_conflicts)}")

    parent_outcomes = {}
    unresolved_parents = []
    for parent, children in parent_children.items():
        if any(exact.get(child) == 1 for child in children):
            outcome = "WIN"
        elif all(exact.get(child) == 2 for child in children):
            outcome = "LOSS"
        else:
            outcome = "UNKNOWN"
        parent_outcomes[parent] = outcome
        if outcome == "UNKNOWN":
            unresolved_parents.append(parent)

    eligible: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    for child, parents in child_parents.items():
        if child in exact or child in same_or_higher_unknown:
            continue
        for parent in parents:
            if parent_outcomes[parent] == "UNKNOWN":
                eligible[child].add(parent)
    schedule = choose_cover(unresolved_parents, eligible, child_legal) if unresolved_parents else []
    schedule_rows = []
    for index, key in enumerate(schedule):
        schedule_rows.append(["target", index, 7, key[0], key[1], child_legal[key], 0, 0, 0, 0, 0])
    args.targets_out.parent.mkdir(parents=True, exist_ok=True)
    args.audit_out.parent.mkdir(parents=True, exist_ok=True)
    for path in (args.targets_out, args.audit_out):
        if path.exists():
            raise SystemExit(f"refusing to overwrite existing artifact: {path}")
    with args.targets_out.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["# exact s7 WIN-witness probe; ordering/budget are scheduling only"])
        writer.writerows(schedule_rows)

    parent_reports = []
    for parent, children in sorted(parent_children.items()):
        counts = Counter("WIN" if exact.get(k) == 1 else "LOSS" if exact.get(k) == 2
                         else "BLOCKED_UNKNOWN" if k in same_or_higher_unknown else "UNSEEN"
                         for k in children)
        parent_reports.append({
            "parent_s6": list(parent),
            "canonical_s7_children": len(children),
            "counts": dict(sorted(counts.items())),
            "saved_exact_loss_witnesses": [list(k) for k in sorted(children) if exact.get(k) == 2],
            "same_or_higher_budget_unknown_keys": [list(k) for k in sorted(children) if k in same_or_higher_unknown],
            "s6_outcome_from_saved_s7": parent_outcomes[parent],
        })
    selected_reports = []
    for key in schedule:
        selected_reports.append({"key": list(key), "legal_s7_children": child_legal[key],
                                 "affected_s6_parents": [list(p) for p in sorted(eligible[key])],
                                 "selection_reason": "minimum-size cover of unresolved s6 parents; then minimum total legal count; key order tie-break"})

    audit = {
        "schema": "n11-s7-witness-probe-preflight-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": "complete canonical s7 boundaries of the exact-UNKNOWN s6 children of one s5 parent; saved solver outcomes are inputs, not inferred from scores",
        "inputs": {
            "s6_boundary_json": {"path": relpath(args.s6_boundary_json), "sha256": sha256(args.s6_boundary_json)},
            "s6_boundary_full_gzip": {"path": relpath(args.s6_boundary_full_gzip), "sha256": sha256(args.s6_boundary_full_gzip)},
            "scan_roots": [relpath(p) for p in args.scan_root],
            "scan_file_count": len(scanned),
            "scan_files": source_files,
            "scan_s7_replay_rows_in_target_boundaries": replay_rows,
            "budget_for_proposed_probe": args.budget,
        },
        "boundary_geometry": {
            "s6_parent_count": len(parent_children),
            "unique_canonical_s7_keys": len(boundary_s7),
            "shared_s7_children": sum(len(v) > 1 for v in child_parents.values()),
            "parents": geometry_rows,
            "parent_results_from_saved_s7": parent_reports,
        },
        "schedule": {
            "ready_target_count": len(schedule),
            "unresolved_s6_parent_count": len(unresolved_parents),
            "covers_every_unresolved_s6_parent": bool(unresolved_parents) and all(
                any(parent in eligible[key] for key in schedule) for parent in unresolved_parents),
            "targets_csv": relpath(args.targets_out),
            "targets_sha256": sha256(args.targets_out),
            "selected_targets": selected_reports,
            "target_rows": schedule_rows,
            "exact_verdict_conflicts": 0,
            "same_or_higher_budget_unknown_key_count": len(same_or_higher_unknown),
            "unknowns_used_as_verdicts": False,
        },
        "claim": "a scheduled exact s7 WIN child would prove its s6 OR parent WIN; no scheduled or unknown result is treated as a verdict",
    }
    args.audit_out.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"s6_parents": len(parent_children), "canonical_s7_keys": len(boundary_s7),
                      "s7_rows_in_history": replay_rows, "ready_targets": len(schedule),
                      "covers_all_unresolved_s6": audit["schedule"]["covers_every_unresolved_s6_parent"],
                      "s6_status_from_saved_s7": dict(Counter(parent_outcomes.values())),
                      "audit_sha256": sha256(args.audit_out), "targets_sha256": sha256(args.targets_out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
