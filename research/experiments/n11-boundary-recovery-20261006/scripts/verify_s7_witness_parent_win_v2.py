#!/usr/bin/env python3
"""Verify exact s7 WIN witnesses through complete s6 and s5 boundaries to an s4 WIN."""
from __future__ import annotations

import argparse
import csv
import gzip
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
sys.path.insert(0, str(ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts"))
from audit_saved_s6_targets import points, read_saved_exact_s6, safe_canonical, sha256  # noqa: E402


import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parents[4] / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import quarantined_cache_keys

def relpath(path: Path) -> str:
    try:
        return path.resolve().relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        return str(path.resolve())


def read_s5_cache(path: Path) -> dict[tuple[int, int], int]:
    _s5_quarantine = quarantined_cache_keys()
    out: dict[tuple[int, int], int] = {}
    for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split(",")
        if len(fields) != 6 or fields[0] != "s5verdict" or int(fields[3]) != 5:
            raise ValueError(f"invalid exact s5 cache row {path}:{line_no}: {line}")
        key = (int(fields[1]), int(fields[2]))
        if key in _s5_quarantine:
            continue
        verdict = int(fields[4])
        if verdict not in (1, 2) or not safe_canonical(key, 5):
            raise ValueError(f"invalid/noncanonical exact s5 cache row {path}:{line_no}: {line}")
        old = out.get(key)
        if old is not None and old != verdict:
            raise ValueError(f"exact s5 cache conflict for {key}")
        out[key] = verdict
    return out


def read_one_s5_target(path: Path) -> tuple[int, int]:
    found = []
    with path.open(newline="", encoding="utf-8-sig") as stream:
        for row_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
                raise ValueError(f"expected one s5 AND target at {path}:{row_no}: {row}")
            key = (int(row[3]), int(row[4]))
            if not safe_canonical(key, 5) or int(row[5]) != len(legal_after(set(points(key)))):
                raise ValueError(f"unsafe/noncanonical s5 target: {key}")
            found.append(key)
    if len(found) != 1:
        raise ValueError(f"expected one s5 target, found {len(found)}")
    return found[0]


def legal_canonical_children(key: tuple[int, int], stones: int) -> tuple[set[tuple[int, int]], dict[tuple[int, int], int]]:
    parent_points = set(points(key))
    if len(parent_points) != stones or has_forbidden_quad(parent_points) or tuple(d4_canonical_key(parent_points)) != key:
        raise ValueError(f"invalid canonical s{stones} parent: {key}")
    children = set()
    child_legal = {}
    for move in legal_after(parent_points):
        child_points = tuple(sorted((*parent_points, move)))
        if len(child_points) != stones + 1 or has_forbidden_quad(child_points):
            raise ValueError(f"unsafe legal extension from {key}: {move}")
        child = tuple(d4_canonical_key(child_points))
        if not safe_canonical(child, stones + 1):
            raise ValueError(f"unsafe canonical child: {child}")
        predecessors = {tuple(d4_canonical_key([p for p in child_points if p != removed]))
                        for removed in child_points}
        if key not in predecessors:
            raise ValueError(f"reverse incidence failure {key} -> {child}")
        children.add(child)
        count = len(legal_after(set(child_points)))
        if child in child_legal and child_legal[child] != count:
            raise ValueError(f"inconsistent legal count for shared child {child}")
        child_legal[child] = count
    if len(children) != len(child_legal):
        raise AssertionError("child legal-count table has duplicate/missing key")
    return children, child_legal


def reply27_class_coverage(target: tuple[int, int]) -> set[int]:
    """Rebuild root-to-s4 incidence; canonical keys need not retain literal 60 and 27."""
    root = {60, 27}
    third_moves = set(legal_after(root))
    if len(third_moves) != 119:
        raise ValueError(f"expected 119 legal third moves after {{60,27}}, got {len(third_moves)}")
    coverage = set()
    for first in third_moves:
        for second in legal_after(root | {first}):
            if second <= first:
                continue
            if tuple(d4_canonical_key([60, 27, first, second])) == target:
                coverage.update((first, second))
    return coverage


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--s5-target", type=Path, required=True)
    parser.add_argument("--s5-s6-boundary-full-gzip", type=Path, required=True)
    parser.add_argument("--augmented-s6-source-audit", type=Path, required=True)
    parser.add_argument("--s7-preflight", type=Path, required=True)
    parser.add_argument("--s7-source-manifest", type=Path, required=True)
    parser.add_argument("--base-s5-cache", type=Path, required=True)
    parser.add_argument("--class-lo", type=int, required=True)
    parser.add_argument("--class-hi", type=int, required=True)
    parser.add_argument("--boundary-audit-out", type=Path, required=True)
    parser.add_argument("--derived-cache-out", type=Path, required=True)
    parser.add_argument("--merged-cache-out", type=Path, required=True)
    parser.add_argument("--merge-receipt-out", type=Path, required=True)
    args = parser.parse_args()

    output_paths = [args.boundary_audit_out, args.derived_cache_out, args.merged_cache_out, args.merge_receipt_out]
    if any(path.exists() for path in output_paths):
        raise SystemExit("refusing to overwrite an existing verification artifact")

    s5_key = read_one_s5_target(args.s5_target)
    if not safe_canonical((args.class_lo, args.class_hi), 4):
        raise SystemExit("target s4 class is unsafe/noncanonical")
    class_key = (args.class_lo, args.class_hi)
    class_coverage = reply27_class_coverage(class_key)
    if not class_coverage:
        raise SystemExit("target s4 class is outside the {60,27} reply27 lane")

    source_audit = json.loads(args.augmented_s6_source_audit.read_text(encoding="utf-8"))
    if source_audit.get("run_status") != "ok" or source_audit.get("s6", {}).get("exact_conflict_count") != 0:
        raise SystemExit("augmented s6 source audit is not conflict-free")
    s6_exact, s6_sources = read_saved_exact_s6(source_audit)
    if len(s6_sources) != source_audit.get("source_file_count"):
        raise SystemExit("augmented s6 source count mismatch")

    s6_full = json.loads(gzip.decompress(args.s5_s6_boundary_full_gzip.read_bytes()))
    s5_parent_rows = s6_full.get("targets", {}).get("parents", [])
    if len(s5_parent_rows) != 1 or tuple(s5_parent_rows[0].get("key", [])) != s5_key:
        raise SystemExit("full s6 boundary is not bound to the supplied s5 target")
    s6_rows = s5_parent_rows[0].get("children", [])
    direct_s6_keys = {tuple(item["key"]) for item in s6_rows}
    if len(s6_rows) != 90 or len(direct_s6_keys) != 90:
        raise SystemExit("s5 target does not have a complete 90-child canonical s6 boundary")
    rebuilt_s6, _ = legal_canonical_children(s5_key, 5)
    if rebuilt_s6 != direct_s6_keys:
        raise SystemExit("stored s6 boundary differs from independently rebuilt canonical geometry")
    if Counter(item["status"] for item in s6_rows) != Counter({"WIN": 87, "UNKNOWN": 3}):
        raise SystemExit("unexpected direct s6 boundary status/count before s7 propagation")

    direct_status = {}
    for item in s6_rows:
        key = tuple(item["key"])
        evidence = s6_exact.get(key)
        saved_verdict = item.get("saved_verdict")
        if evidence is None or evidence["verdict"] != saved_verdict:
            raise SystemExit(f"full s6 boundary result does not match hash-validated sources for {key}")
        if saved_verdict == 1:
            direct_status[key] = "WIN"
        elif saved_verdict == 2:
            direct_status[key] = "LOSS"
        elif saved_verdict == 0:
            direct_status[key] = "UNKNOWN"
        else:
            raise SystemExit(f"unexpected saved s6 verdict for {key}: {saved_verdict}")

    s6_unknowns = sorted(key for key, status in direct_status.items() if status == "UNKNOWN")
    if len(s6_unknowns) != 3:
        raise SystemExit("expected three direct-UNKNOWN s6 parents for s7 witness audit")
    s7_children_by_parent = {}
    s7_legal_by_key = {}
    for parent in s6_unknowns:
        children, legal = legal_canonical_children(parent, 6)
        s7_children_by_parent[parent] = children
        for child, count in legal.items():
            old = s7_legal_by_key.get(child)
            if old is not None and old != count:
                raise SystemExit(f"shared s7 child legal-count mismatch {child}")
            s7_legal_by_key[child] = count

    preflight = json.loads(args.s7_preflight.read_text(encoding="utf-8"))
    source_manifest = json.loads(args.s7_source_manifest.read_text(encoding="utf-8"))
    if source_manifest.get("preflight", {}).get("sha256") != sha256(args.s7_preflight):
        raise SystemExit("s7 source manifest preflight hash mismatch")
    if source_manifest.get("targets", {}).get("sha256") != preflight.get("schedule", {}).get("targets_sha256"):
        raise SystemExit("s7 source manifest target hash mismatch")
    if preflight.get("inputs", {}).get("scan_s7_replay_rows_in_target_boundaries") != 0:
        raise SystemExit("s7 preflight did not establish an empty saved replay intersection")
    boundary_parent_rows = preflight.get("boundary_geometry", {}).get("parents", [])
    preflight_s7_counts = {tuple(item["parent_s6"]): item["canonical_s7_children"]
                           for item in boundary_parent_rows}
    if set(preflight_s7_counts) != set(s6_unknowns):
        raise SystemExit("s7 preflight parent keys differ from the three direct-UNKNOWN s6 parents")
    for parent, children in s7_children_by_parent.items():
        if len(children) != preflight_s7_counts[parent]:
            raise SystemExit(f"s7 boundary count differs from preflight for {parent}")

    target_key_set = set()
    s7_exact: dict[tuple[int, int], int] = {}
    witness_rows = []
    for item in source_manifest.get("raw_sources", []):
        key = tuple(item.get("key", []))
        if key in target_key_set:
            raise SystemExit(f"duplicate s7 raw target in source manifest: {key}")
        target_key_set.add(key)
        path = (ROOT / item.get("artifact_path", "")).resolve()
        if not path.is_file() or sha256(path) != item.get("sha256"):
            raise SystemExit(f"s7 raw artifact missing/hash mismatch: {path}")
        parsed = []
        for row_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
            if not row or row[0].lstrip().startswith("#") or row[0] != "replay":
                continue
            if len(row) != 11 or int(row[2]) != 7 or int(row[4]) != 0:
                raise SystemExit(f"invalid s7 AND replay {path}:{row_no}: {row}")
            raw_key = (int(row[9]), int(row[10]))
            canonical = tuple(d4_canonical_key(points(raw_key)))
            verdict, budget, nodes, legal = int(row[6]), int(row[5]), int(row[7]), int(row[3])
            if (canonical != key or not safe_canonical(key, 7) or verdict != 1
                    or budget != source_manifest.get("budget_per_target") or nodes != item.get("nodes")
                    or legal != s7_legal_by_key.get(key)):
                raise SystemExit(f"s7 WIN raw row mismatch/geometry failure {path}:{row_no}: {row}")
            parsed.append(row)
        if len(parsed) != 1 or key not in s7_legal_by_key:
            raise SystemExit(f"s7 raw key is not one legal child row: {path}")
        # Check every reverse parent from geometry and bind to the manifested target incidences.
        child_points = points(key)
        all_parents = {tuple(d4_canonical_key([p for p in child_points if p != removed]))
                       for removed in child_points}
        affected = {parent for parent in s6_unknowns if key in s7_children_by_parent[parent]}
        if affected != {tuple(parent) for parent in item.get("affected_s6_parents", [])}:
            raise SystemExit(f"s7 parent incidence differs from source manifest for {key}")
        if not affected.issubset(all_parents):
            raise SystemExit(f"s7 witness lacks safe canonical s6 incidence for {key}")
        s7_exact[key] = 1
        witness_rows.append({"key": list(key), "verdict": "WIN", "legal": legal,
                             "budget": budget, "nodes": nodes,
                             "source": relpath(path), "sha256": sha256(path),
                             "affected_s6_parents": [list(parent) for parent in sorted(affected)],
                             "all_safe_canonical_s6_parents": [list(parent) for parent in sorted(all_parents)]})

    selected = {tuple(item["key"]) for item in preflight.get("schedule", {}).get("selected_targets", [])}
    if target_key_set != selected or len(target_key_set) != 2:
        raise SystemExit("s7 raw sources do not exactly match the two-row selected schedule")
    if source_manifest.get("runner_summary", {}).get("reported_s5_outcome") != "WIN":
        raise SystemExit("local runner did not report the s5 parent WIN")

    s6_propagated = {}
    s6_rows_by_parent = []
    for parent, children in s7_children_by_parent.items():
        status = "WIN" if any(s7_exact.get(child) == 1 for child in children) else (
            "LOSS" if all(s7_exact.get(child) == 2 for child in children) else "UNKNOWN")
        witness = sorted(child for child in children if s7_exact.get(child) == 1)
        if status != "WIN" or not witness:
            raise SystemExit(f"s7 evidence does not resolve s6 OR parent as WIN: {parent}")
        s6_propagated[parent] = status
        s6_rows_by_parent.append({"s6_parent": list(parent), "complete_canonical_s7_boundary": len(children),
                                  "saved_exact_s7_win_witnesses": [list(key) for key in witness],
                                  "derived_s6_outcome": status})

    final_s6 = dict(direct_status)
    final_s6.update(s6_propagated)
    if len(final_s6) != 90 or any(status != "WIN" for status in final_s6.values()):
        raise SystemExit("complete s5 boundary is not all exact WIN after s7 propagation")
    s5_outcome = "WIN"

    # Rebuild the complete class boundary and use only the one exact s5 WIN witness.
    class_children, _ = legal_canonical_children(class_key, 4)
    if not class_children or s5_key not in class_children:
        raise SystemExit(f"s5 witness is not a child in the independently rebuilt complete s4 boundary: {s5_key}")
    cache = read_s5_cache(args.base_s5_cache)
    if s5_key in cache:
        raise SystemExit(f"s5 witness already exists in base exact cache; reconcile the provenance first: {s5_key}")
    class_values = dict(cache)
    class_values[s5_key] = 1
    class_counts = Counter("WIN" if class_values.get(key) == 1 else "LOSS" if class_values.get(key) == 2 else "UNKNOWN"
                           for key in class_children)
    class_status = "WIN" if class_counts["WIN"] else "LOSS" if class_counts["UNKNOWN"] == 0 else "UNKNOWN"
    if class_status != "WIN":
        raise SystemExit("exact s5 witness failed to classify target s4 class as WIN")

    # Enumerate every safe canonical s4 parent of this exact s5 witness and
    # check reply27 reachability from the root geometry, not literal point ids:
    # D4 canonicalization can rotate/reflect {60,27} in the stored class key.
    s5_points = points(s5_key)
    reverse_s4 = {}
    for removed in s5_points:
        parent_points = tuple(p for p in s5_points if p != removed)
        parent = tuple(d4_canonical_key(parent_points))
        if has_forbidden_quad(parent_points) or not safe_canonical(parent, 4):
            continue
        if removed not in legal_after(set(parent_points)):
            continue
        if tuple(d4_canonical_key((*parent_points, removed))) != s5_key:
            raise SystemExit(f"reverse s4 incidence mismatch for {parent} -> {s5_key}")
        coverage = reply27_class_coverage(parent)
        if coverage:
            reverse_s4[parent] = sorted(coverage)

    delta_text = ("# exact s5 verdicts derived from complete s6 boundaries with exact s7 WIN witnesses\n"
                  f"s5verdict,{s5_key[0]},{s5_key[1]},5,1,0\n")
    merged_values = dict(cache)
    old = merged_values.get(s5_key)
    if old is not None and old != 1:
        raise SystemExit(f"s5 derived WIN conflicts with base exact cache: {s5_key} {old}")
    merged_values[s5_key] = 1
    merged_text = "# s5 verdict cache: n=11 schema=1 (base exact cache plus verified s7-witness-derived s5 WIN)\n"
    merged_text += "".join(f"s5verdict,{lo},{hi},5,{verdict},0\n"
                          for (lo, hi), verdict in sorted(merged_values.items()))

    args.derived_cache_out.parent.mkdir(parents=True, exist_ok=True)
    args.merged_cache_out.parent.mkdir(parents=True, exist_ok=True)
    args.derived_cache_out.write_text(delta_text, encoding="utf-8", newline="\n")
    args.merged_cache_out.write_text(merged_text, encoding="utf-8", newline="\n")
    derived_rows = read_s5_cache(args.derived_cache_out)
    merged_check = read_s5_cache(args.merged_cache_out)
    if derived_rows != {s5_key: 1} or len(merged_check) != len(cache) + 1:
        raise SystemExit("derived/merged cache post-write validation failed")
    if Counter(map(str, merged_check.values())) != Counter(map(str, class_values.values())):
        raise SystemExit("post-write merged cache verdict totals differ")

    audit = {
        "schema": "n11-reply27-s7-witness-to-s5-class-win-geometry-audit-v1",
        "created_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "outcome_provenance": "Exact s7 WIN results are accepted solver outcomes; geometry independently checks each legal canonical child and derives its s6 OR parent WIN. All 90 canonical s6 children of the s5 AND parent are then checked WIN before deriving s5 WIN and its s4 class WIN.",
        "inputs": {
            "s5_target": {"path": relpath(args.s5_target), "sha256": sha256(args.s5_target)},
            "s5_s6_boundary_full_gzip": {"path": relpath(args.s5_s6_boundary_full_gzip), "sha256": sha256(args.s5_s6_boundary_full_gzip)},
            "augmented_s6_source_audit": {"path": relpath(args.augmented_s6_source_audit), "sha256": sha256(args.augmented_s6_source_audit),
                                           "source_files_revalidated": len(s6_sources), "canonical_s6_keys": len(s6_exact),
                                           "exact_conflicts": 0},
            "s7_preflight": {"path": relpath(args.s7_preflight), "sha256": sha256(args.s7_preflight)},
            "s7_source_manifest": {"path": relpath(args.s7_source_manifest), "sha256": sha256(args.s7_source_manifest)},
            "base_s5_cache": {"path": relpath(args.base_s5_cache), "sha256": sha256(args.base_s5_cache),
                              "exact_rows": len(cache), "verdict_counts": dict(sorted(Counter(map(str, cache.values())).items()))},
        },
        "s7_loss_witnesses": witness_rows,
        "s6_parent_win_derivations": s6_rows_by_parent,
        "s5_parent": {
            "key": list(s5_key), "complete_canonical_s6_boundary": len(rebuilt_s6),
            "before_s7_verdict_counts": dict(sorted(Counter(direct_status.values()).items())),
            "after_s7_verdict_counts": dict(sorted(Counter(final_s6.values()).items())),
            "all_children_exact_win": all(status == "WIN" for status in final_s6.values()),
            "outcome": s5_outcome,
        },
        "s4_class": {
            "key": list(class_key), "complete_canonical_s5_boundary": len(class_children),
            "reply27_third_move_coverage": sorted(class_coverage),
            "witness_is_safe_legal_canonical_child": s5_key in class_children,
            "boundary_status_counts_after_merge": dict(sorted(class_counts.items())),
            "outcome": class_status,
            "reply27_s4_parents_of_s5_witness": [
                {"key": list(key), "third_move_coverage": coverage}
                for key, coverage in sorted(reverse_s4.items())],
        },
        "cache_merge": {
            "derived_s5_cache": {"path": relpath(args.derived_cache_out), "sha256": sha256(args.derived_cache_out),
                                 "rows": len(derived_rows), "verdict_counts": {"WIN": 1}},
            "merged_s5_cache": {"path": relpath(args.merged_cache_out), "sha256": sha256(args.merged_cache_out),
                                "rows": len(merged_check), "verdict_counts": dict(sorted(Counter(map(str, merged_check.values())).items()))},
            "conflicts": 0,
        },
        "exact_verdict_conflicts": 0,
        "unknowns_propagated": False,
        "proof_scope": "s4 class WIN from one exact s5 WIN child; no statement is made about {60,27} or the empty board",
    }
    args.boundary_audit_out.parent.mkdir(parents=True, exist_ok=True)
    args.boundary_audit_out.write_text(json.dumps(audit, indent=2, sort_keys=True) + "\n",
                                      encoding="utf-8", newline="\n")
    receipt = {
        "schema": "n11-reply27-s7-derived-s5-cache-merge-v1",
        "base_cache": {"path": relpath(args.base_s5_cache), "sha256": sha256(args.base_s5_cache),
                       "rows": len(cache), "verdict_counts": dict(sorted(Counter(map(str, cache.values())).items()))},
        "delta_cache": {"path": relpath(args.derived_cache_out), "sha256": sha256(args.derived_cache_out),
                        "rows": len(derived_rows), "verdict_counts": {"WIN": 1}},
        "merged_cache": {"path": relpath(args.merged_cache_out), "sha256": sha256(args.merged_cache_out),
                         "rows": len(merged_check), "verdict_counts": dict(sorted(Counter(map(str, merged_check.values())).items()))},
        "duplicate_verdicts": 0,
        "conflicts": 0,
        "boundary_audit": {"path": relpath(args.boundary_audit_out), "sha256": sha256(args.boundary_audit_out)},
        "root": [60, 27],
        "claim": "a single exact s5 WIN witness proves the s4 class WIN; UNKNOWN rows remain raw-only and are not propagated",
    }
    args.merge_receipt_out.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n",
                                      encoding="utf-8", newline="\n")
    print(json.dumps({"s7_loss_witnesses": len(witness_rows), "s6_parents_derived_win": len(s6_propagated),
                      "s5_parent": list(s5_key), "s5_outcome": s5_outcome,
                      "class": list(class_key), "class_outcome": class_status,
                      "s4_boundary": len(class_children), "s4_status_counts": dict(sorted(class_counts.items())),
                      "merged_s5_rows": len(merged_check), "conflicts": 0,
                      "audit_sha256": sha256(args.boundary_audit_out),
                      "merge_receipt_sha256": sha256(args.merge_receipt_out)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
