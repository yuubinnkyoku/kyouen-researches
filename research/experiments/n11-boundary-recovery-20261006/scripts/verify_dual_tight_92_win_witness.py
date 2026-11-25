#!/usr/bin/env python3
"""Verify the dual-tight s4 WIN class from one fully WIN s5 child boundary.

This checks geometry, canonical boundaries, replay identity, and cache
consistency. It treats exact solver verdicts as inputs and does not re-prove
the game outcomes reported by the solver.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = ROOT / "research/experiments/n11-boundary-recovery-20261006"
OUT = EXP / "output"
sys.path.insert(0, str(ROOT / "research/experiments/n11-search-methods/scripts"))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402

CLASS_KEY = (10452854735126921216, 0)
WIN_S5_KEY = (10452925103871098880, 0)
CLASS_AUDIT = OUT / "post-next17-dual-tight-92-boundary-audit.json"
CLASS_TARGETS = OUT / "post-next17-dual-tight-92-targets.csv"
CACHE = OUT / "post-next17-dual-tight-92-final-merged-s5.cache"
S6_META = OUT / "post-next17-dual-tight-92-s6-unresolved-boundary-meta.json"
S6_RAW = OUT / "raw/post-next17-dual-tight-92-s6-unresolved-out.csv"
S6_AUDIT = OUT / "post-next17-dual-tight-92-s6-unresolved-final-audit.json"
S6_SOURCES = OUT / "post-next17-dual-tight-92-s6-unresolved-sources.json"
AUDIT_OUT = OUT / "post-next17-dual-tight-92-win-witness-geometry-audit.json"


import sys as _policy_sys
from pathlib import Path as _PolicyPath
_policy_sys.path.insert(0, str(_PolicyPath(__file__).resolve().parents[4] / 'research/experiments/n11-frontier-selection-20261005/scripts'))
from s5_evidence_policy import quarantined_cache_keys

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    if not (0 <= lo < (1 << 64) and 0 <= hi < (1 << 57)):
        raise ValueError(f"key outside n=11 board: {key}")
    return tuple([i for i in range(64) if lo >> i & 1] + [64 + i for i in range(57) if hi >> i & 1])


def checked_key(key: tuple[int, int], stones: int) -> tuple[int, int]:
    board = points(key)
    if len(board) != stones or has_forbidden_quad(board):
        raise ValueError(f"unsafe s{stones} key: {key}")
    canonical = tuple(d4_canonical_key(board))
    if canonical != key:
        raise ValueError(f"noncanonical s{stones} key: {key} -> {canonical}")
    return canonical


def read_cache(path: Path) -> dict[tuple[int, int], int]:
    _s5_quarantine = quarantined_cache_keys()
    verdicts: dict[tuple[int, int], int] = {}
    with path.open(newline="", encoding="utf-8") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict" or int(row[3]) != 5:
                raise ValueError(f"invalid s5 cache row at {path}:{line_no}: {row}")
            key = checked_key((int(row[1]), int(row[2])), 5)
            if key in _s5_quarantine:
                continue
            value = int(row[4])
            if value not in (1, 2):
                raise ValueError(f"non-exact cache value at {path}:{line_no}: {row}")
            old = verdicts.get(key)
            if old is not None and old != value:
                raise ValueError(f"s5 cache conflict for {key}: {old} vs {value}")
            verdicts[key] = value
    return verdicts


def main() -> int:
    class_audit = json.loads(CLASS_AUDIT.read_text(encoding="utf-8"))
    if tuple(map(int, class_audit["class_key"])) != CLASS_KEY:
        raise ValueError("stored boundary audit names a different class")
    class_points = tuple(map(int, class_audit["class_points"]))
    if len(class_points) != 4 or has_forbidden_quad(class_points):
        raise ValueError(f"unsafe s4 class points: {class_points}")
    if tuple(d4_canonical_key(class_points)) != CLASS_KEY:
        raise ValueError("s4 points do not canonicalize to the target class key")

    geometric_children: set[tuple[int, int]] = set()
    for move in legal_after(set(class_points)):
        child_points = tuple(sorted((*class_points, move)))
        if len(child_points) != 5 or has_forbidden_quad(child_points):
            raise ValueError(f"unsafe legal s5 extension: {class_points} + {move}")
        child = tuple(d4_canonical_key(child_points))
        checked_key(child, 5)
        geometric_children.add(child)
    if len(geometric_children) != 95:
        raise ValueError(f"expected 95 canonical s5 children, got {len(geometric_children)}")

    target_keys: set[tuple[int, int]] = set()
    with CLASS_TARGETS.open(newline="", encoding="utf-8") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].startswith("#"):
                continue
            key = checked_key((int(row[3]), int(row[4])), 5)
            if key in target_keys:
                raise ValueError(f"duplicate s5 target at line {line_no}: {key}")
            target_keys.add(key)
    known_loss = {tuple(map(int, key)) for key in class_audit["known_exact_children"]["keys"]}
    if len(target_keys) != 92 or len(known_loss) != 3 or target_keys & known_loss:
        raise ValueError("stored 92-target/3-known-loss partition is malformed")
    if target_keys | known_loss != geometric_children:
        raise ValueError("stored class boundary does not match geometry-generated 95-child set")

    cache = read_cache(CACHE)
    class_statuses = Counter({"WIN": 0, "LOSS": 0, "UNKNOWN": 0})
    child_rows = []
    for key in sorted(geometric_children):
        value = cache.get(key)
        status = {1: "WIN", 2: "LOSS", None: "UNKNOWN"}[value]
        class_statuses[status] += 1
        child_rows.append({"key": list(key), "status": status})
    if cache.get(WIN_S5_KEY) != 1 or WIN_S5_KEY not in geometric_children:
        raise ValueError("the exact s5 WIN witness is absent from the class boundary/cache")

    witness_points = points(WIN_S5_KEY)
    if len(witness_points) != 5 or has_forbidden_quad(witness_points):
        raise ValueError("s5 WIN witness is unsafe")
    if tuple(d4_canonical_key(witness_points)) != WIN_S5_KEY:
        raise ValueError("s5 WIN witness is not canonical")
    deletion_parents = {
        tuple(d4_canonical_key([p for p in witness_points if p != removed]))
        for removed in witness_points
    }
    if CLASS_KEY not in deletion_parents:
        raise ValueError("s5 WIN witness is not a child of the target s4 class")

    meta = json.loads(S6_META.read_text(encoding="utf-8"))
    parents = [tuple(map(int, key)) for key in meta["parent_keys"]]
    if WIN_S5_KEY not in parents:
        raise ValueError("s5 WIN parent is absent from the generated s6 boundary metadata")
    win_parent_index = parents.index(WIN_S5_KEY)
    witness_s6 = [row for row in meta["canonical_children"] if win_parent_index in row["parent_indices"]]
    if len(witness_s6) != 80:
        raise ValueError(f"expected full 80-child s6 boundary, got {len(witness_s6)}")
    s6_rows: dict[tuple[int, int], list[str]] = {}
    with S6_RAW.open(newline="", encoding="utf-8") as stream:
        for line_no, row in enumerate(csv.reader(stream), 1):
            if not row or row[0].startswith("#"):
                continue
            if len(row) != 11 or row[0] != "replay" or int(row[2]) != 6 or int(row[4]) != 1:
                raise ValueError(f"invalid s6 replay row at {S6_RAW}:{line_no}: {row}")
            key = checked_key((int(row[9]), int(row[10])), 6)
            if key in s6_rows:
                raise ValueError(f"duplicate s6 replay key: {key}")
            s6_rows[key] = row
    for child in witness_s6:
        key = tuple(map(int, child["key"]))
        checked_key(key, 6)
        row = s6_rows.get(key)
        if row is None:
            raise ValueError(f"missing exact s6 row for witness child {key}")
        if int(row[3]) != int(child["legal_count"]):
            raise ValueError(f"s6 legal count mismatch for {key}: {row[3]} != {child['legal_count']}")
        if int(row[6]) != 1:
            raise ValueError(f"s5 WIN witness has non-WIN s6 child {key}: {row[6]}")

    saved_audit = json.loads(S6_AUDIT.read_text(encoding="utf-8"))
    audit_parent = next(
        row for row in saved_audit["targets"]["parents"]
        if tuple(map(int, row["key"])) == WIN_S5_KEY
    )
    if (audit_parent["outcome"] != "WIN" or audit_parent["child_count"] != 80
            or audit_parent["counts"].get("WIN") != 80
            or audit_parent["counts"].get("LOSS", 0) != 0
            or audit_parent["counts"].get("UNKNOWN", 0) != 0
            or audit_parent["counts"].get("UNSEEN", 0) != 0):
        raise ValueError(f"independent full s6 audit does not certify the s5 WIN parent: {audit_parent}")

    if not any(value == 1 for key, value in cache.items() if key in geometric_children):
        raise ValueError("s4 class has no exact s5 WIN child")
    class_status = "WIN"
    sources = [CLASS_AUDIT, CLASS_TARGETS, CACHE, S6_META, S6_RAW, S6_AUDIT, S6_SOURCES]
    report = {
        "schema": "n11-dual-tight-92-win-witness-geometry-audit-v1",
        "scope": "Exact solver values are trusted. This audit verifies canonical safe geometry, complete parent boundaries, s5/s6 incidence, and cache consistency.",
        "root": [60, 27],
        "s4_class": {"key": list(CLASS_KEY), "points": list(class_points), "status": class_status},
        "complete_canonical_s5_boundary": {
            "children": len(geometric_children),
            "partition": {"previous_exact_loss": len(known_loss), "previous_unknown_targets": len(target_keys)},
            "current_cache_status_counts": dict(sorted(class_statuses.items())),
            "children_status": child_rows,
            "geometry_generation": "Enumerate every legal safe s5 extension of the canonical s4 class, D4-canonicalize, and compare the complete set to the stored 3 LOSS + 92 UNKNOWN partition.",
        },
        "s5_win_witness": {
            "key": list(WIN_S5_KEY),
            "safe_canonical": True,
            "s4_parent_incidence": True,
            "cache_verdict": "WIN",
            "complete_canonical_s6_children": len(witness_s6),
            "s6_verdict_counts": {"WIN": len(witness_s6), "LOSS": 0, "UNKNOWN": 0, "UNSEEN": 0},
            "children": [{"key": child["key"], "legal_count": child["legal_count"], "verdict": 1}
                         for child in witness_s6],
        },
        "consequence": "The s4 class is exact WIN because one canonical s5 child is exact WIN; no further child search is required for this class.",
        "status": {"class_10452854735126921216_0": "WIN", "root_60_27": "UNKNOWN", "empty_board": "UNKNOWN"},
        "sources": [{"path": p.relative_to(ROOT).as_posix(), "sha256": sha256(p)} for p in sources],
    }
    AUDIT_OUT.write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")
    print(f"REPLY27_WIN_WITNESS_GEOMETRY_OK class={CLASS_KEY} s5={WIN_S5_KEY} s6=80/80")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
