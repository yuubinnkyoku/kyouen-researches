#!/usr/bin/env python3
"""Audit incremental class2-lane WIN7 reuse into the S2{59,60} S6 worklist.

The certificate bodies are not re-run here. This script combines the baseline
verified receipts used by audit_win7_reuse.py with four later class2-lane
WIN7 manifests, then independently checks exact geometry and D4 parent lifts.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
EXP = HERE.parent
SOURCE = EXP / "n11-central-19-cover-20261031" / "output"
MANIFEST = EXP / "n11-s2-5960-milestone5-20261112" / "output"
OUTPUT = HERE / "output"

BASELINE_FILES = (
    SOURCE / "s6sweep" / "verified.json",
    SOURCE / "focus2154_62certs" / "verified.json",
    SOURCE / "frontier2140" / "verified.json",
)
NEW_MANIFESTS = (
    OUTPUT / "class2-lane-cost69c-win7-certificates-20261114.json",
    OUTPUT / "class2-lane-cost70b-win7-certificates-20261114.json",
    OUTPUT / "class2-lane-cost71-win7-certificates-20261114.json",
    OUTPUT / "class2-lane-cost75-win7-certificates-20261114.json",
)
EXPECTED_SOURCE_COUNTS = {
    "class2-lane-cost69c-win7-certificates-20261114.json": 1,
    "class2-lane-cost70b-win7-certificates-20261114.json": 1,
    "class2-lane-cost71-win7-certificates-20261114.json": 2,
    "class2-lane-cost75-win7-certificates-20261114.json": 19,
}


def images(mask: int) -> list[int]:
    result = [0] * 8
    for p in range(121):
        if not (mask >> p) & 1:
            continue
        x, y = p % 11, p // 11
        coords = (
            (x, y), (y, 10 - x), (10 - x, 10 - y), (10 - y, x),
            (10 - x, y), (x, 10 - y), (y, x), (10 - y, 10 - x),
        )
        for i, (a, b) in enumerate(coords):
            result[i] |= 1 << (11 * b + a)
    return result


def canonical(mask: int) -> int:
    return min(images(mask))


def safe(mask: int) -> bool:
    """Exact integer test: no four collinear or cocircular points."""
    points = [(p % 11, p // 11) for p in range(121) if (mask >> p) & 1]
    for a, b, c, d in combinations(points, 4):
        (x1, y1), (x2, y2), (x3, y3), (x4, y4) = a, b, c, d
        cross = lambda x, y: (x2 - x1) * (y - y1) - (y2 - y1) * (x - x1)
        area = cross(x3, y3)
        if area == 0:
            if cross(x4, y4) == 0:
                return False
            continue
        q1, q2, q3 = (x * x + y * y for x, y in (a, b, c))
        den = 2 * area
        ux = q1 * (y2 - y3) + q2 * (y3 - y1) + q3 * (y1 - y2)
        uy = q1 * (x3 - x2) + q2 * (x1 - x3) + q3 * (x2 - x1)
        if ((den * x4 - ux) ** 2 + (den * y4 - uy) ** 2
                == (den * x1 - ux) ** 2 + (den * y1 - uy) ** 2):
            return False
    return True


def load_worklist() -> dict[int, dict]:
    rows: dict[int, dict] = {}
    for path in sorted(MANIFEST.glob("ms5_s6_manifest_part*.csv")):
        with path.open(newline="") as source:
            for row in csv.DictReader(source):
                mask = int(row["hex"], 16)
                assert mask.bit_count() == 6 and canonical(mask) == mask
                assert mask not in rows
                rows[mask] = {
                    "hex": f"{mask:032x}",
                    "cost": int(row["cost"]),
                    "classes": int(row["classes"]),
                }
    assert len(rows) == 7867
    assert sum(row["cost"] for row in rows.values()) == 615497
    return rows


def load_baseline() -> tuple[set[str], set[str]]:
    wins: set[str] = set()
    losses: set[str] = set()
    for path in BASELINE_FILES:
        data = json.loads(path.read_text())
        assert not data.get("fails")
        for raw, entry in data["verified"].items():
            mask = int(raw, 16)
            assert mask.bit_count() == 7 and canonical(mask) == mask
            if entry["type"] == "WIN7":
                wins.add(raw)
            elif entry["type"] == "LOSS7":
                losses.add(raw)
            else:
                raise ValueError(f"unknown verdict in {path}: {entry['type']}")
    assert len(wins) == 4052
    assert len(losses) == 2699
    assert not wins & losses
    return wins, losses


def load_new_roots() -> tuple[dict[str, dict], dict[str, int]]:
    roots: dict[str, dict] = {}
    source_counts: dict[str, int] = {}
    for path in NEW_MANIFESTS:
        data = json.loads(path.read_text())
        certificates = data.get("certificates", [])
        source_counts[path.name] = len(certificates)
        for entry in certificates:
            raw = entry.get("root_hex") or entry.get("root")
            if not raw:
                raise ValueError(f"missing root in {path}")
            mask = int(raw, 16)
            assert mask.bit_count() == 7
            key = f"{canonical(mask):032x}"
            assert safe(int(key, 16)), f"unsafe WIN7 root: {key}"
            if entry.get("verdict") not in (None, "WIN7"):
                raise ValueError(f"non-WIN7 entry in {path}: {entry['verdict']}")
            assert key not in roots, f"duplicate new root: {key}"
            roots[key] = {
                "source_manifest": path.name,
                "sha256": entry.get("sha256"),
                "md5": entry.get("md5"),
            }
    assert source_counts == EXPECTED_SOURCE_COUNTS
    assert len(roots) == 23
    return roots, source_counts


def parent_hits(child_hex: str, worklist: dict[int, dict]):
    child = int(child_hex, 16)
    for bit in range(121):
        if (child >> bit) & 1:
            parent = canonical(child ^ (1 << bit))
            if parent in worklist:
                yield parent, bit


def class_histogram(parents: set[int], worklist: dict[int, dict]) -> dict[str, int]:
    counts: dict[str, int] = defaultdict(int)
    for parent in parents:
        counts[str(worklist[parent]["classes"])] += 1
    return dict(sorted(counts.items(), key=lambda item: int(item[0])))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source-commit",
        default="b8e0427e8d7e8a460ac6fe55bde1ce6cac0f9d58",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=OUTPUT / "class2-win7-reuse-incremental-20261114.json",
    )
    args = parser.parse_args()

    worklist = load_worklist()
    baseline_wins, baseline_losses = load_baseline()
    new_roots, source_counts = load_new_roots()

    new_keys = set(new_roots)
    assert not new_keys & baseline_wins
    assert not new_keys & baseline_losses

    baseline_parents: set[int] = set()
    for child in baseline_wins:
        for parent, _ in parent_hits(child, worklist):
            baseline_parents.add(parent)

    hits: dict[int, dict[str, set[int]]] = defaultdict(lambda: defaultdict(set))
    for child in new_roots:
        for parent, bit in parent_hits(child, worklist):
            hits[parent][child].add(bit)

    new_parents = set(hits)
    incremental = new_parents - baseline_parents
    all_parents = baseline_parents | new_parents
    total_cost = sum(row["cost"] for row in worklist.values())
    baseline_removed_cost = sum(worklist[p]["cost"] for p in baseline_parents)
    incremental_removed_cost = sum(worklist[p]["cost"] for p in incremental)
    total_removed_cost = sum(worklist[p]["cost"] for p in all_parents)

    parent_records = []
    for parent in sorted(hits):
        row = worklist[parent]
        children = []
        for child in sorted(hits[parent]):
            children.append({
                "s7_hex": child,
                "removed_bits_in_canonical_s7": sorted(hits[parent][child]),
                "source_manifest": new_roots[child]["source_manifest"],
            })
        parent_records.append({
            "s6_hex": row["hex"],
            "cost": row["cost"],
            "classes": row["classes"],
            "already_covered_by_baseline": parent in baseline_parents,
            "new_win7_children": children,
        })

    result = {
        "schema": "n11-s2-5960-incremental-win7-reuse-audit-v1",
        "date": "2026-11-14",
        "source_main_commit": args.source_commit,
        "inputs": {
            "s6_worklist_parts": [
                str(path.relative_to(EXP.parent.parent))
                for path in sorted(MANIFEST.glob("ms5_s6_manifest_part*.csv"))
            ],
            "baseline_receipt_files": [
                str(path.relative_to(EXP.parent.parent)) for path in BASELINE_FILES
            ],
            "new_win7_manifests": [
                str(path.relative_to(EXP.parent.parent)) for path in NEW_MANIFESTS
            ],
        },
        "checks": {
            "worklist_rows": len(worklist),
            "total_legal_child_cost": total_cost,
            "baseline_win7_roots": len(baseline_wins),
            "baseline_loss7_roots": len(baseline_losses),
            "baseline_win_loss_conflicts": 0,
            "new_win7_roots": len(new_roots),
            "new_win7_roots_exact_safe_geometry": len(new_roots),
            "new_roots_already_in_baseline_win7": 0,
            "new_roots_conflicting_with_baseline_loss7": 0,
            "new_parent_child_pairs": sum(len(children) for children in hits.values()),
            "new_unique_worklist_parents": len(new_parents),
            "new_parents_already_covered_by_baseline": len(new_parents & baseline_parents),
            "baseline_worklist_parent_hits": len(baseline_parents),
            "incremental_new_worklist_parents": len(incremental),
            "total_worklist_parent_hits_after_union": len(all_parents),
            "remaining_worklist_parents_not_closed_by_win7_reuse": len(worklist) - len(all_parents),
            "baseline_remaining_legal_child_cost": total_cost - baseline_removed_cost,
            "incremental_legal_child_cost_removed": incremental_removed_cost,
            "remaining_legal_child_cost_after_union": total_cost - total_removed_cost,
            "incremental_class_histogram": class_histogram(incremental, worklist),
            "total_class_histogram_after_union": class_histogram(all_parents, worklist),
        },
        "source_manifest_counts": source_counts,
        "new_roots": [
            {"s7_hex": key, **new_roots[key]} for key in sorted(new_roots)
        ],
        "new_parent_records": parent_records,
        "incremental_parent_hex": [
            worklist[parent]["hex"] for parent in sorted(incremental)
        ],
        "interpretation": (
            "WIN7 is original-first-player WIN. Restoring any removed point as "
            "the seventh move gives a winning move from that six-stone parent. "
            "This closes only those S6 worklist rows; it does not decide S2 or "
            "the empty root."
        ),
        "limitations": (
            "Certificate bodies were not re-run. This audit independently checks "
            "the new roots' exact geometric safety, D4 normalization, worklist "
            "parent incidence, and conflicts against the baseline LOSS7 receipts."
        ),
    }

    assert result["checks"]["baseline_worklist_parent_hits"] == 498
    assert result["checks"]["new_parent_child_pairs"] == 70
    assert result["checks"]["new_unique_worklist_parents"] == 48
    assert result["checks"]["new_parents_already_covered_by_baseline"] == 5
    assert result["checks"]["incremental_new_worklist_parents"] == 43
    assert result["checks"]["total_worklist_parent_hits_after_union"] == 541
    assert result["checks"]["remaining_worklist_parents_not_closed_by_win7_reuse"] == 7326
    assert result["checks"]["baseline_remaining_legal_child_cost"] == 577110
    assert result["checks"]["incremental_legal_child_cost_removed"] == 3275
    assert result["checks"]["remaining_legal_child_cost_after_union"] == 573835

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
