#!/usr/bin/env python3
"""Audit one complete canonical s6 boundary against saved and local replay evidence."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402

EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
sys.path.insert(0, str(EXP / "scripts"))
from audit_saved_s6_targets import (  # noqa: E402
    points,
    read_saved_exact_s6,
    safe_canonical,
    sha256,
)


def relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def read_parent(path: Path) -> tuple[int, int]:
    rows = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or int(row[2]) != 5 or int(row[6]) != 0 or int(row[7]) != 0:
                raise ValueError(f"expected one s5 AND target at {path}:{line_no}: {row}")
            key = (int(row[3]), int(row[4]))
            if not safe_canonical(key, 5):
                raise ValueError(f"unsafe/noncanonical s5 parent: {key}")
            if int(row[5]) != len(legal_after(set(points(key)))):
                raise ValueError(f"s5 parent legal-count mismatch: {key}")
            rows.append(key)
    if len(rows) != 1:
        raise ValueError(f"expected exactly one s5 target in {path}, got {len(rows)}")
    return rows[0]


def read_s5_cache(path: Path) -> dict[tuple[int, int], int]:
    result: dict[tuple[int, int], int] = {}
    with path.open(encoding="utf-8") as stream:
        for line_no, line in enumerate(stream, 1):
            if not line.strip() or line.lstrip().startswith("#"):
                continue
            fields = line.split(",")
            if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
                raise ValueError(f"invalid exact s5 cache row {path}:{line_no}: {line.rstrip()}")
            key, verdict = (int(fields[1]), int(fields[2])), int(fields[4])
            if verdict not in (1, 2) or not safe_canonical(key, 5):
                raise ValueError(f"invalid/noncanonical exact s5 cache row: {key} {verdict}")
            old = result.get(key)
            if old is not None and old != verdict:
                raise ValueError(f"exact s5 cache conflict for {key}: {old} vs {verdict}")
            result[key] = verdict
    return result


def make_boundary(parent: tuple[int, int]) -> set[tuple[int, int]]:
    parent_points = set(points(parent))
    children: set[tuple[int, int]] = set()
    for move in legal_after(parent_points):
        child_points = tuple(sorted((*parent_points, move)))
        if len(child_points) != 6 or has_forbidden_quad(child_points):
            raise ValueError(f"unsafe legal s6 extension: {parent} + {move}")
        child = tuple(d4_canonical_key(child_points))
        if not safe_canonical(child, 6):
            raise ValueError(f"unsafe/noncanonical s6 child from {parent}: {child}")
        predecessors = {
            tuple(d4_canonical_key([point for point in child_points if point != removed]))
            for removed in child_points
        }
        if parent not in predecessors:
            raise ValueError(f"s6 child fails reverse-incidence check: {parent} -> {child}")
        children.add(child)
    return children


def check_full_detail(path: Path, parent: tuple[int, int], boundary: set[tuple[int, int]]) -> dict:
    payload = json.loads(gzip.decompress(path.read_bytes()))
    parents = payload.get("targets", {}).get("parents", [])
    matches = [row for row in parents if tuple(row.get("key", [])) == parent]
    if len(matches) != 1:
        raise ValueError(f"full saved-s6 detail does not contain exactly one target parent {parent}")
    row = matches[0]
    detail_children = {tuple(child["key"]) for child in row.get("children", [])}
    if len(detail_children) != len(row.get("children", [])) or detail_children != boundary:
        raise ValueError("saved-s6 full-detail boundary differs from independently rebuilt geometry")
    if row.get("child_count") != len(boundary):
        raise ValueError("saved-s6 full-detail child count mismatch")
    return {
        "path": relpath(path),
        "sha256": sha256(path),
        "parent_key": list(parent),
        "child_count": len(detail_children),
        "boundary_key_set_matches_geometry": True,
    }


def scan_local(local_root: Path, boundary: set[tuple[int, int]]) -> tuple[int, dict, list[dict]]:
    observations: dict[tuple[int, int], list[dict]] = defaultdict(list)
    matching_files: dict[Path, list[dict]] = defaultdict(list)
    csv_count = 0
    for path in sorted(local_root.rglob("*.csv")):
        csv_count += 1
        with path.open(newline="", encoding="utf-8-sig") as stream:
            for row_no, row in enumerate(csv.reader(stream), 1):
                if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                    continue
                if len(row) < 3 or not row[2].isdigit() or int(row[2]) != 6:
                    continue
                if len(row) != 11:
                    raise ValueError(f"unexpected s6 replay row width at {path}:{row_no}: {row}")
                stones, legal, is_or, budget, verdict, nodes = map(
                    int, (row[2], row[3], row[4], row[5], row[6], row[7])
                )
                raw_key = (int(row[9]), int(row[10]))
                raw_points = points(raw_key)
                if len(raw_points) != 6 or has_forbidden_quad(raw_points):
                    raise ValueError(f"unsafe local s6 replay at {path}:{row_no}: {raw_key}")
                key = tuple(d4_canonical_key(raw_points))
                if key not in boundary:
                    continue
                if (stones != 6 or is_or != 1 or budget <= 0 or verdict not in (0, 1, 2)
                        or nodes < 0 or legal != len(legal_after(set(raw_points)))
                        or not safe_canonical(key, 6)):
                    raise ValueError(f"invalid local boundary s6 replay at {path}:{row_no}: {row}")
                item = {
                    "path": relpath(path),
                    "row": row_no,
                    "budget": budget,
                    "verdict": verdict,
                    "nodes": nodes,
                    "legal_count": legal,
                    "raw_key": list(raw_key),
                    "canonical_key": list(key),
                    "normalized_noncanonical": raw_key != key,
                }
                observations[key].append(item)
                matching_files[path].append(item)

    file_receipts = []
    for path, rows in sorted(matching_files.items()):
        file_receipts.append({
            "path": relpath(path),
            "sha256": sha256(path),
            "matching_rows": len(rows),
        })
        for row in rows:
            row["source_sha256"] = file_receipts[-1]["sha256"]
    return csv_count, observations, file_receipts


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parent", type=Path, required=True)
    parser.add_argument("--saved-audit", type=Path, required=True)
    parser.add_argument("--saved-full-detail", type=Path, required=True)
    parser.add_argument("--s5-cache", type=Path, required=True)
    parser.add_argument("--local-root", type=Path, required=True)
    parser.add_argument("--budget", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    if args.budget <= 0:
        parser.error("budget must be positive")
    if not args.local_root.is_dir():
        raise SystemExit(f"local replay directory is missing: {args.local_root}")

    parent = read_parent(args.parent)
    boundary = make_boundary(parent)
    full_receipt = check_full_detail(args.saved_full_detail, parent, boundary)
    source_audit = json.loads(args.saved_audit.read_text(encoding="utf-8"))
    if not source_audit.get("s6", {}).get("all_s6_exact_rows_geometry_checked"):
        raise SystemExit("saved s6 source audit lacks geometry/legal attestation")
    saved, validated_sources = read_saved_exact_s6(source_audit)
    if source_audit.get("s6", {}).get("exact_conflict_count") != 0:
        raise SystemExit("saved s6 corpus reports exact conflicts")
    s5_cache = read_s5_cache(args.s5_cache)
    if parent in s5_cache:
        raise SystemExit(f"target s5 parent is already exact in current cache: {parent}")

    csv_count, local_observations, local_files = scan_local(args.local_root.resolve(), boundary)
    local_conflicts = []
    entries = []
    blocked_unknown_keys = []
    saved_verdict_counts: Counter[str] = Counter()
    local_verdict_counts: Counter[str] = Counter()
    ready_keys = []
    for key in sorted(boundary):
        saved_row = saved.get(key)
        saved_verdict = saved_row["verdict"] if saved_row is not None else None
        saved_status = {None: "UNSEEN", 0: "UNKNOWN", 1: "WIN", 2: "LOSS"}[saved_verdict]
        saved_verdict_counts[saved_status] += 1
        observations = local_observations.get(key, [])
        exact_local = {row["verdict"] for row in observations if row["verdict"] in (1, 2)}
        if len(exact_local) > 1:
            local_conflicts.append({"key": list(key), "verdicts": sorted(exact_local), "rows": observations})
        elif exact_local:
            local_verdict = next(iter(exact_local))
            local_verdict_counts["WIN" if local_verdict == 1 else "LOSS"] += 1
            if saved_verdict != local_verdict:
                local_conflicts.append({"key": list(key), "local_exact": local_verdict,
                                        "saved_exact": saved_verdict, "rows": observations})
        elif observations:
            local_verdict_counts["UNKNOWN"] += 1

        high_unknown = [row for row in observations
                        if row["verdict"] == 0 and row["budget"] >= args.budget]
        saved_high_unknown = []
        if saved_row is not None:
            saved_high_unknown = [row for row in saved_row.get("observations", [])
                                  if row["verdict"] == 0 and row["legal"] == len(legal_after(set(points(key))))
                                  and row["budget"] >= args.budget]
        blocked = bool(high_unknown or saved_high_unknown)
        if blocked:
            blocked_unknown_keys.append(key)
        if saved_verdict not in (1, 2) and not blocked:
            ready_keys.append(key)
        entries.append({
            "key": list(key),
            "saved_status": saved_status,
            "saved_observation_count": len(saved_row["observations"]) if saved_row else 0,
            "local_observations": observations,
            "same_or_higher_budget_local_unknowns": high_unknown,
            "same_or_higher_budget_saved_unknowns": saved_high_unknown,
            "direct_dispatch_blocked_by_unknown_history": blocked,
        })
    if local_conflicts:
        raise SystemExit(f"local and hash-validated saved exact s6 evidence conflict: {local_conflicts[:3]}")

    out = {
        "schema": "n11-reply27-local-s6-boundary-history-audit-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "interpretation": "The independently rebuilt full canonical s6 boundary is intersected with hash-validated saved exact results and preserved local replay history. Saved exact results are reusable; same-or-higher-budget UNKNOWN s6 rows are excluded from direct replay. UNKNOWN never propagates.",
        "requested_budget": args.budget,
        "parent": {"path": relpath(args.parent), "sha256": sha256(args.parent), "key": list(parent),
                   "safe_canonical": True, "exact_cache_verdict": None},
        "geometry": {"boundary_child_count": len(boundary),
                     "all_children_safe_legal_canonical": True,
                     "all_children_reverse_incidence_checked": True,
                     "saved_full_detail": full_receipt},
        "saved_source_audit": {"path": relpath(args.saved_audit), "sha256": sha256(args.saved_audit),
                               "source_count": len(validated_sources), "all_source_hashes_validated": True,
                               "unique_canonical_s6_keys": len(saved), "exact_conflicts": 0},
        "s5_cache": {"path": relpath(args.s5_cache), "sha256": sha256(args.s5_cache),
                     "exact_rows": len(s5_cache), "target_parent_absent": True, "conflicts": 0},
        "local_history": {"root": relpath(args.local_root), "csv_files_scanned": csv_count,
                          "matching_source_files": local_files,
                          "boundary_rows": sum(len(rows) for rows in local_observations.values()),
                          "distinct_boundary_keys_observed": len(local_observations),
                          "verdict_counts_by_distinct_key": dict(sorted(local_verdict_counts.items())),
                          "exact_conflicts": 0},
        "boundary_saved_verdict_counts": dict(sorted(saved_verdict_counts.items())),
        "boundary_unknown_or_unseen_keys": [row["key"] for row in entries
                                             if row["saved_status"] in ("UNKNOWN", "UNSEEN")],
        "same_or_higher_budget_unknown_keys": [list(key) for key in sorted(blocked_unknown_keys)],
        "direct_dispatch_ready_keys": [list(key) for key in sorted(ready_keys)],
        "direct_dispatch_ready_count": len(ready_keys),
        "boundary_entries": entries,
        "conflicts": 0,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"parent": list(parent), "boundary_child_count": len(boundary),
                      "saved_verdict_counts": out["boundary_saved_verdict_counts"],
                      "local_boundary_rows": out["local_history"]["boundary_rows"],
                      "blocked_unknown_keys": len(blocked_unknown_keys),
                      "dispatch_ready": len(ready_keys), "conflicts": 0,
                      "out": relpath(args.out), "out_sha256": sha256(args.out)}, indent=2))


if __name__ == "__main__":
    main()
