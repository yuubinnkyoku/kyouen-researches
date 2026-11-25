#!/usr/bin/env python3
"""Audit an exact s5 WIN witness against a complete dual-tight s4 boundary."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EDGE = ROOT / "research/experiments/n11-search-methods/scripts"
sys.path.insert(0, str(EDGE))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402


import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parents[4] / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import quarantined_cache_keys

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < 1 << 64 and 0 <= hi < 1 << 57):
        raise ValueError(f"key outside n=11 board: {key}")
    return tuple([i for i in range(64) if lo >> i & 1]
                 + [64 + i for i in range(57) if hi >> i & 1])


def checked_key(key: tuple[int, int], stones: int) -> tuple[int, int]:
    pts = points(key)
    if len(pts) != stones or has_forbidden_quad(pts):
        raise ValueError(f"unsafe s{stones} position: {key}")
    canonical = tuple(d4_canonical_key(pts))
    if canonical != key:
        raise ValueError(f"noncanonical s{stones} key: {key} -> {canonical}")
    return key


def read_cache(path: Path) -> dict[tuple[int, int], int]:
    _s5_quarantine = quarantined_cache_keys()
    result = {}
    for line_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
            raise SystemExit(f"invalid s5 cache row {path}:{line_no}: {row}")
        key = checked_key((int(row[1]), int(row[2])), 5)
        if key in _s5_quarantine:
            continue
        value = int(row[4])
        if value not in (1, 2):
            raise SystemExit(f"non-exact s5 cache verdict: {path}:{line_no}: {row}")
        old = result.get(key)
        if old is not None and old != value:
            raise SystemExit(f"s5 cache conflict for {key}: {old} vs {value}")
        result[key] = value
    return result


def read_targets(path: Path) -> tuple[set[tuple[int, int]], dict]:
    keys = set()
    legal = {}
    for line_no, row in enumerate(csv.reader(path.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 11 or int(row[2]) != 5 or int(row[7]) != 0:
            raise SystemExit(f"invalid s5 target {path}:{line_no}: {row}")
        key = checked_key((int(row[3]), int(row[4])), 5)
        count = len(legal_after(set(points(key))))
        if int(row[5]) != count or key in keys:
            raise SystemExit(f"target geometry mismatch or duplicate {path}:{line_no}: {key}")
        keys.add(key)
        legal[key] = count
    return keys, legal


def reply27_class_coverage(target: tuple[int, int]) -> set[int]:
    """Rebuild root-to-s4 incidence for one class directly from legal geometry."""
    root = {60, 27}
    vertices = set(legal_after(root))
    if len(vertices) != 119:
        raise SystemExit(f"expected 119 legal third moves, got {len(vertices)}")
    coverage = set()
    for first in vertices:
        for second in legal_after(root | {first}):
            if second <= first:
                continue
            key = tuple(d4_canonical_key([60, 27, first, second]))
            if key == target:
                coverage.update((first, second))
    return coverage


def class_status(cache: dict[tuple[int, int], int], children: set[tuple[int, int]]) -> str:
    values = [cache.get(key) for key in children]
    if 1 in values:
        return "WIN"
    if all(value == 2 for value in values):
        return "LOSS"
    return "UNKNOWN"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--class-lo", type=int, required=True)
    ap.add_argument("--class-hi", type=int, required=True)
    ap.add_argument("--base-cache", type=Path, required=True)
    ap.add_argument("--full-targets", type=Path, required=True)
    ap.add_argument("--probe-targets", type=Path, required=True)
    ap.add_argument("--new-exact-cache", type=Path, required=True)
    ap.add_argument("--raw", type=Path, required=True)
    ap.add_argument("--merged-cache", type=Path, required=True)
    ap.add_argument("--ranking", type=Path, required=True)
    ap.add_argument("--summary", type=Path, required=True)
    ap.add_argument("--sources", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    class_key = (args.class_lo, args.class_hi)
    checked_key(class_key, 4)
    class_points = points(class_key)

    coverage = reply27_class_coverage(class_key)
    if not coverage:
        raise SystemExit("requested s4 class is not reachable after root {60,27}")
    generated_children = set()
    for move in legal_after(set(class_points)):
        child_points = tuple(sorted((*class_points, move)))
        if len(child_points) != 5 or has_forbidden_quad(child_points):
            raise SystemExit(f"unsafe legal s5 extension: {class_points} + {move}")
        generated_children.add(tuple(d4_canonical_key(child_points)))
    if not generated_children:
        raise SystemExit("s4 class has no legal s5 extensions")

    full_targets, _ = read_targets(args.full_targets)
    probe_targets, probe_legal = read_targets(args.probe_targets)
    if not probe_targets <= full_targets:
        raise SystemExit("probe contains s5 keys outside the full UNKNOWN target boundary")
    ranking = json.loads(args.ranking.read_text(encoding="utf-8"))
    rank_item = ranking.get("next_target", {})
    if rank_item.get("key") != list(class_key):
        raise SystemExit("ranking source identifies a different s4 class")
    if rank_item.get("canonical_s5_children") != len(generated_children):
        raise SystemExit("ranking child cardinality disagrees with direct geometry")
    if sorted(rank_item.get("coverage", [])) != sorted(coverage):
        raise SystemExit("ranking coverage vertices disagree with root geometry")

    base = read_cache(args.base_cache)
    base_children = {key: base[key] for key in generated_children if key in base}
    if Counter(base_children.values()) != Counter({2: rank_item["known_loss_s5"]}):
        raise SystemExit("base-cache status partition differs from ranked known-loss boundary")
    if set(base_children) | full_targets != generated_children or set(base_children) & full_targets:
        raise SystemExit("full target CSV is not exactly the unknown part of the complete class boundary")

    exact_delta = read_cache(args.new_exact_cache)
    if set(exact_delta) != probe_targets:
        raise SystemExit("new exact cache keys differ from the scheduled probe targets")
    raw = {}
    for line_no, row in enumerate(csv.reader(args.raw.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        if len(row) != 11 or row[0] != "replay" or int(row[2]) != 5 or int(row[4]) != 0:
            raise SystemExit(f"invalid s5 raw replay row {args.raw}:{line_no}: {row}")
        key = checked_key((int(row[9]), int(row[10])), 5)
        if key not in probe_targets or key in raw:
            raise SystemExit(f"unexpected/duplicate s5 raw replay key: {key}")
        if (int(row[3]) != probe_legal[key] or int(row[5]) != 15_000_000
                or int(row[6]) not in (1, 2) or int(row[7]) < 0):
            raise SystemExit(f"raw replay legal count or exact verdict invalid: {row}")
        raw[key] = {"verdict": int(row[6]), "nodes": int(row[7]), "legal_count": int(row[3])}
    if set(raw) != probe_targets or {key: item["verdict"] for key, item in raw.items()} != exact_delta:
        raise SystemExit("raw exact replay rows and new s5 cache disagree")

    merged = read_cache(args.merged_cache)
    expected = dict(base)
    for key, value in exact_delta.items():
        if key in expected and expected[key] != value:
            raise SystemExit(f"exact s5 verdict conflict: {key}")
        expected[key] = value
    if merged != expected:
        raise SystemExit("merged s5 cache differs from exact base+probe evidence")

    statuses = Counter({"WIN": 0, "LOSS": 0, "UNKNOWN": 0})
    boundary_rows = []
    for key in sorted(generated_children):
        value = merged.get(key)
        status = {1: "WIN", 2: "LOSS", None: "UNKNOWN"}[value]
        statuses[status] += 1
        boundary_rows.append({"key": list(key), "status": status})
    witnesses = [key for key in generated_children if merged.get(key) == 1]
    if not witnesses:
        raise SystemExit("no exact s5 WIN witness in the class boundary/cache")
    witness_parents = {}
    parent_impacts = []
    for witness in witnesses:
        witness_points = points(witness)
        parents = {tuple(d4_canonical_key([p for p in witness_points if p != removed]))
                   for removed in witness_points}
        if class_key not in parents:
            raise SystemExit(f"exact s5 WIN witness is not a legal child of class: {witness}")
        witness_parents[str(witness)] = sorted([list(parent) for parent in parents])
        for parent in sorted(parents):
            parent_coverage = reply27_class_coverage(parent)
            if parent_coverage:
                parent_children = {
                    tuple(d4_canonical_key(tuple(sorted((*points(parent), move)))))
                    for move in legal_after(set(points(parent)))
                }
                if witness not in parent_children:
                    raise SystemExit(f"reverse s4 incidence disagrees with forward geometry: {parent} -> {witness}")
                parent_impacts.append({
                    "key": list(parent),
                    "reachable_from_reply27": True,
                    "coverage_vertices": sorted(parent_coverage),
                    "canonical_s5_children": len(parent_children),
                    "status_before_probe": class_status(base, parent_children),
                    "status_after_probe": class_status(merged, parent_children),
                    "witness_child": list(witness),
                })
            else:
                parent_impacts.append({"key": list(parent), "reachable_from_reply27": False,
                                       "witness_child": list(witness)})

    summary = json.loads(args.summary.read_text(encoding="utf-8"))
    if (summary.get("exact_replay_counts", {}).get("WIN") != sum(v == 1 for v in exact_delta.values())
            or summary.get("exact_replay_counts", {}).get("LOSS") != sum(v == 2 for v in exact_delta.values())
            or summary.get("raw_output", {}).get("sha256") != sha256(args.raw)
            or summary.get("new_exact_cache", {}).get("sha256") != sha256(args.new_exact_cache)):
        raise SystemExit("saved probe summary differs from exact raw/cache artifacts")
    source_manifest = json.loads(args.sources.read_text(encoding="utf-8"))
    target_digest = sha256(args.probe_targets)
    target_is_bound = source_manifest.get("probe_target_sha256") == target_digest
    if not target_is_bound:
        # The v2 collector stores file bindings in `inputs` rather than the
        # older standalone `probe_target_sha256` field. Preserve that manifest
        # verbatim and validate the exact scheduled-target entry here.
        target_rel = args.probe_targets.resolve().relative_to(ROOT.resolve()).as_posix()
        bound_targets = [item for item in source_manifest.get("inputs", [])
                         if item.get("path", "").replace("\\", "/") == target_rel]
        if len(bound_targets) != 1 or bound_targets[0].get("sha256") != target_digest:
            raise SystemExit("probe v2 source manifest does not bind the scheduled input")

    inputs = [args.base_cache, args.full_targets, args.probe_targets, args.new_exact_cache,
              args.raw, args.merged_cache, args.ranking, args.summary, args.sources,
              Path(__file__).resolve()]
    report = {
        "schema": "n11-dual-tight-s4-win-witness-geometry-audit-v1",
        "scope": "Exact solver outcomes are inputs. This audit rebuilds the complete canonical s5 boundary and verifies the exact s5 WIN witness incidence; unknown siblings remain unknown.",
        "root": [60, 27],
        "s4_class": {"key": list(class_key), "points": list(class_points), "status": "WIN",
                     "coverage_vertices": sorted(coverage)},
        "complete_canonical_s5_boundary": {
            "children": len(generated_children),
            "before_probe": {"known_loss": len(base_children), "unknown_targets": len(full_targets), "win": 0},
            "probe_exact": {"LOSS": sum(v == 2 for v in exact_delta.values()),
                            "WIN": sum(v == 1 for v in exact_delta.values())},
            "current_cache_status_counts": dict(sorted(statuses.items())),
            "children_status": boundary_rows,
        },
        "s5_win_witnesses": [{"key": list(key), "safe_canonical": True,
                              "legal_s4_parent_incidence": class_key in [tuple(p) for p in witness_parents[str(key)]],
                              "exact_cache_verdict": "WIN", "source_replay": raw[key]}
                             for key in sorted(witnesses)],
        "s5_witness_parent_classes": witness_parents,
        "reply27_parent_class_impacts_from_witness": parent_impacts,
        "consequence": "One exact WIN s5 child proves this s4 class WIN; all remaining s5 children for the class were left unexplored.",
        "status": {"class": "WIN", "root_60_27": "UNKNOWN", "empty_board": "UNKNOWN"},
        "sources": [{"path": p.resolve().relative_to(ROOT.resolve()).as_posix(), "sha256": sha256(p)}
                    for p in inputs],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n",
                        encoding="utf-8", newline="\n")
    print(f"DUAL_TIGHT_S4_WIN_GEOMETRY_OK class={class_key} children={len(generated_children)} witnesses={len(witnesses)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
