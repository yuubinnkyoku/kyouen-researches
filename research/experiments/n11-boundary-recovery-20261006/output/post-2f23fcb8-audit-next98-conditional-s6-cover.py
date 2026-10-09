#!/usr/bin/env python3
"""Independently verify the latest-main conditional 49-S6 cover for next98."""
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OUT = ROOT / "research/experiments/n11-boundary-recovery-20261006/output"
TARGETS = OUT / "post-034a26a4-after-class-win-ranking-targets.csv"
RANKING = OUT / "post-034a26a4-after-class-win-ranking.json"
CACHE = OUT / "post-034a26a4-next-class-10376293541461626880-67108864-probe8-early-win-merged-s5.cache"
AUDIT = OUT / "post-b4d9b6a9-next98-conditional-s6-cover-audit.json"
WITNESSES = OUT / "post-b4d9b6a9-next98-conditional-s6-cover.csv"
PRECISION = OUT / "post-b4d9b6a9-next98-key-precision-correction.md"
OUTPUT = OUT / "post-2f23fcb8-next98-conditional-s6-geometry-audit.json"
DFPN_GEOMETRY = ROOT / "research/experiments/n11-search-methods/scripts/dfpn_edge_classes.py"
INDEPENDENT_GEOMETRY = ROOT / "research/experiments/n11-boundary-recovery-20261006/scripts/n11_integer_circle_geometry.py"

import sys
sys.path.insert(0, str(DFPN_GEOMETRY.parent))
sys.path.insert(0, str(INDEPENDENT_GEOMETRY.parent))
from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after  # noqa: E402
from n11_integer_circle_geometry import legal_points  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def points(key: tuple[int, int]) -> tuple[int, ...]:
    lo, hi = key
    return tuple([i for i in range(64) if (lo >> i) & 1]
                 + [64 + i for i in range(57) if (hi >> i) & 1])


def load_targets() -> dict[tuple[int, int], int]:
    targets: dict[tuple[int, int], int] = {}
    for line_no, row in enumerate(csv.reader(TARGETS.open(newline="", encoding="utf-8-sig")), 1):
        if not row or row[0].lstrip().startswith("#"):
            continue
        key = (int(row[3]), int(row[4]))
        pts = points(key)
        if len(pts) != 5 or has_forbidden_quad(pts) or tuple(d4_canonical_key(pts)) != key:
            raise SystemExit(f"unsafe/noncanonical target at row {line_no}: {key}")
        if key in targets:
            raise SystemExit(f"duplicate target: {key}")
        moves = legal_after(set(pts))
        if len(moves) != int(row[5]):
            raise SystemExit(f"target legal-count mismatch: {key}")
        targets[key] = len(moves)
    if len(targets) != 98:
        raise SystemExit(f"expected 98 canonical s5 parents, got {len(targets)}")
    return targets


def main() -> int:
    if OUTPUT.exists():
        raise SystemExit(f"refusing to overwrite audit: {OUTPUT}")
    audit = json.loads(AUDIT.read_text(encoding="utf-8"))
    rank = json.loads(RANKING.read_text(encoding="utf-8"))
    precision = PRECISION.read_text(encoding="utf-8")
    correct_key_text = ("1152921504741065728", "68719476736")
    if correct_key_text[0] not in precision or correct_key_text[1] not in precision:
        raise SystemExit("exact decimal key correction is absent")
    key_match = re.search(r"s4_key = \(\"(\d+)\", \"(\d+)\"\)", precision)
    if not key_match or tuple(key_match.groups()) != correct_key_text:
        raise SystemExit("precision correction exact s4 key mismatch")
    s4_key = tuple(map(int, correct_key_text))
    if tuple(rank["next_target"]["key"]) != s4_key:
        raise SystemExit("ranked exact key differs from precision correction")
    if audit.get("schema") != "n11-conditional-s6-cover-audit-v1":
        raise SystemExit("unexpected incoming cover audit schema")
    if (audit.get("source_s5_cache_sha256") != sha(CACHE)
            or audit.get("witnesses_sha256") != sha(WITNESSES)
            or audit.get("s5_children") != 102 or audit.get("known_loss_s5") != 4
            or audit.get("unknown_s5") != 98 or audit.get("known_win_s5") != 0):
        raise SystemExit("incoming audit does not match exact cache / witness / target boundary")

    targets = load_targets()
    children_by_parent: dict[tuple[int, int], set[tuple[int, int]]] = {}
    parents_by_child: dict[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
    raw_incidence = 0
    for parent in targets:
        occupied = set(points(parent))
        legal_moves = legal_after(occupied)
        raw_incidence += len(legal_moves)
        child_keys = {tuple(d4_canonical_key([*occupied, move])) for move in legal_moves}
        children_by_parent[parent] = child_keys
        for child in child_keys:
            parents_by_child[child].add(parent)
    multiplicities = Counter(len(parents) for parents in parents_by_child.values())
    expected_multiplicity = {1: 335, 2: 4334, 3: 43}
    if (raw_incidence != 9179 or len(parents_by_child) != 4712
            or dict(sorted(multiplicities.items())) != expected_multiplicity):
        raise SystemExit(
            "independent complete s6 incidence mismatch: "
            f"edges={raw_incidence}, unique={len(parents_by_child)}, "
            f"multiplicity={dict(sorted(multiplicities.items()))}"
        )

    witness_keys: list[tuple[int, int]] = []
    legal_counts: list[int] = []
    covered: set[tuple[int, int]] = set()
    witness_parent_rows = []
    for line_no, row in enumerate(csv.reader(WITNESSES.open(newline="", encoding="utf-8-sig")), 1):
        if not row:
            continue
        if len(row) != 2:
            raise SystemExit(f"invalid witness CSV row {line_no}: {row}")
        key = (int(row[0]), int(row[1]))
        pts = points(key)
        if len(pts) != 6 or has_forbidden_quad(pts) or tuple(d4_canonical_key(pts)) != key:
            raise SystemExit(f"unsafe/noncanonical S6 witness at row {line_no}: {key}")
        if key in witness_keys:
            raise SystemExit(f"duplicate S6 witness: {key}")
        legal = legal_points(pts)
        parents = parents_by_child.get(key, set())
        if not parents:
            raise SystemExit(f"S6 witness is not a child of a current UNKNOWN S5 parent: {key}")
        witness_keys.append(key)
        legal_counts.append(len(legal))
        covered.update(parents)
        witness_parent_rows.append({"s6_key": list(map(str, key)),
                                    "s5_parents": [list(map(str, p)) for p in sorted(parents)],
                                    "legal_s7_count": len(legal)})
    if len(witness_keys) != 49 or covered != set(targets):
        missing = sorted(set(targets) - covered)
        raise SystemExit(f"49-witness cover does not cover all parents: missing {missing[:5]}")
    if (sum(legal_counts) != 4093 or min(legal_counts) != 66 or max(legal_counts) != 95):
        raise SystemExit("independent S6 legal-child counts differ from incoming audit")

    common_parent = (10376293541595841536, 68719476736)
    if common_parent not in targets:
        raise SystemExit("exact common parent cited in precision correction is not a target")
    weights = {p: (0.0 if p == common_parent else 0.5) for p in targets}
    column_max = max(sum(weights[p] for p in parents)
                     for parents in parents_by_child.values())
    dual_total = sum(weights.values())
    if column_max > 1.0 or dual_total != 48.5:
        raise SystemExit(f"dual lower bound invalid: total={dual_total} max-column={column_max}")

    inputs = [TARGETS, RANKING, CACHE, AUDIT, WITNESSES, PRECISION,
              DFPN_GEOMETRY, INDEPENDENT_GEOMETRY]
    result = {
        "schema": "n11-next98-conditional-s6-geometry-audit-v1",
        "verification_main": "2f23fcb80ae853c93d31ed5d2e0f8d7d25ce757a",
        "incoming_audit_source_main": audit["source_main"],
        "root": [60, 27],
        "s4_key_exact_decimal": list(map(str, s4_key)),
        "s5_parent_count": len(targets),
        "complete_canonical_s6_incidence": {
            "raw_parent_child_edges": raw_incidence,
            "deduplicated_canonical_parent_child_edges": sum(map(len, children_by_parent.values())),
            "unique_s6_children": len(parents_by_child),
            "multiplicity": {str(k): v for k, v in sorted(multiplicities.items())},
        },
        "conditional_cover": {
            "witness_count": len(witness_keys),
            "covered_unknown_s5_parents": len(covered),
            "witness_parent_multiplicity": dict(sorted(Counter(len(r["s5_parents"]) for r in witness_parent_rows).items())),
            "witness_legal_s7_sum": sum(legal_counts),
            "witness_legal_s7_min": min(legal_counts),
            "witness_legal_s7_max": max(legal_counts),
            "exact_s6_keys": [list(map(str, key)) for key in witness_keys],
            "parent_incidence": witness_parent_rows,
        },
        "minimum_cover_dual": {
            "zero_weight_common_s5": list(map(str, common_parent)),
            "weight_other_97": "1/2",
            "dual_total": "97/2",
            "maximum_s6_column_weight": str(column_max),
            "integer_lower_bound": 49,
            "upper_bound_witnesses": 49,
            "minimum_is_49": True,
        },
        "verdicts": {
            "all_49_s6": "UNKNOWN",
            "all_98_s5": "UNKNOWN",
            "conditional_claim": "If all 49 listed exact s6 positions are LOSS, their verified parent incidence proves all 98 listed s5 parents LOSS.",
            "s4_class": "UNKNOWN",
            "reply27_root": "UNKNOWN",
            "empty_board": "UNKNOWN",
        },
        "sources": [{"path": path.resolve().relative_to(ROOT).as_posix(),
                     "bytes": path.stat().st_size, "sha256": sha(path)} for path in inputs],
    }
    OUTPUT.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n",
                      encoding="utf-8", newline="\n")
    print(json.dumps({"out": OUTPUT.resolve().relative_to(ROOT).as_posix(),
                      "s4_key": list(map(str, s4_key)),
                      "complete_s6_incidence": result["complete_canonical_s6_incidence"],
                      "conditional_cover": {k: v for k, v in result["conditional_cover"].items() if k not in {"exact_s6_keys", "parent_incidence"}},
                      "minimum_cover": result["minimum_cover_dual"],
                      "verdicts": result["verdicts"], "output_sha256": sha(OUTPUT)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
