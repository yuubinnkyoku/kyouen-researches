#!/usr/bin/env python3
"""Independent D4 audit of cost-64d receipt-to-frontier marginal coverage.

This is a structural audit only. It does not invoke the game engine or
recompute any WIN7-D10 verdict; it checks D4 deletion identities and the
head-1419 fold-prep projection against the published worklist and audit.
"""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from pathlib import Path

TRANSFORMS = (
    lambda x, y: (x, y),
    lambda x, y: (10 - y, x),
    lambda x, y: (10 - x, 10 - y),
    lambda x, y: (y, 10 - x),
    lambda x, y: (10 - x, y),
    lambda x, y: (10 - y, 10 - x),
    lambda x, y: (x, 10 - y),
    lambda x, y: (y, x),
)


def default_repo_root() -> Path:
    for parent in Path(__file__).resolve().parents:
        if (parent / "research/knowledge/README.md").is_file():
            return parent
    return Path.cwd()


def set_bits(mask: int) -> list[int]:
    out: list[int] = []
    while mask:
        low = mask & -mask
        out.append(low.bit_length() - 1)
        mask ^= low
    return out


def canonical_hex(mask: int) -> str:
    images: list[int] = []
    for transform in TRANSFORMS:
        image = 0
        for bit in set_bits(mask):
            x, y = bit % 11, bit // 11
            X, Y = transform(x, y)
            image |= 1 << (Y * 11 + X)
        images.append(image)
    return f"{min(images):032x}"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=default_repo_root())
    args = parser.parse_args()
    root = args.root.resolve()

    exp = root / "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113"
    worklist_path = (
        root / "research/experiments/n11-class2-lane-closability-ranking-20261116/output"
        / "class-frontier-remaining-s6-worklist-1410-20261116.csv"
    )
    claim_path = exp / "output/class2-lane-cost64d-inflight-20261116.json"
    audit_path = exp / "output/class2-lane-cost64d-raw-sweep-audit-20261116.json"

    with worklist_path.open(encoding="utf-8", newline="") as handle:
        rows = {
            row["s6_canonical_hex"]: {
                "category": row["category"],
                "cost": int(row["own_candidates_s6_s7_edge_cost"]),
                "open_parents": int(row["open_parents"]),
                "open_after": int(row["open_candidates_after_transfers"]),
            }
            for row in csv.DictReader(handle)
        }
    claim = json.loads(claim_path.read_text(encoding="utf-8"))
    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    child = int(claim["s6_child"], 16)
    legal = set(claim["legal_candidates"])
    win_bits = claim["results"]["win7_d10_bits"]
    published = {
        int(receipt["bit"]): sorted(receipt["marginal_in_manifest_1419"])
        for receipt in audit["fold_prep_marginals_at_1419"]["receipts"]
    }

    root_orbits: set[str] = set()
    raw_union: set[str] = set()
    new_union: set[str] = set()
    raw_edges = 0
    new_edges = 0
    histogram: Counter[int] = Counter()
    per_root: list[dict[str, object]] = []
    mismatches: list[dict[str, object]] = []

    for bit in win_bits:
        if bit not in legal:
            raise AssertionError(f"WIN bit {bit} is not a legal candidate")
        win_root = child | (1 << bit)
        if win_root.bit_count() != 7:
            raise AssertionError(f"bit {bit} does not produce a 7-stone root")
        root_key = canonical_hex(win_root)
        if root_key in root_orbits:
            raise AssertionError(f"duplicate D4 WIN-root orbit at bit {bit}")
        root_orbits.add(root_key)

        raw_hits: set[str] = set()
        new_hits: set[str] = set()
        for stone in set_bits(win_root):
            row_key = canonical_hex(win_root ^ (1 << stone))
            row = rows.get(row_key)
            if row is None:
                continue
            raw_hits.add(row_key)
            if row["open_after"] > 0:
                new_hits.add(row_key)

        raw_edges += len(raw_hits)
        new_edges += len(new_hits)
        raw_union.update(raw_hits)
        new_union.update(new_hits)
        histogram[len(new_hits)] += 1
        actual = sorted(new_hits)
        expected = published.get(bit, [])
        if actual != expected:
            mismatches.append({"bit": bit, "actual": actual, "expected": expected})
        per_root.append({"bit": bit, "marginal_rows": actual})

    fold = audit["fold_prep_marginals_at_1419"]
    parent_projection = fold["per_open_parent_projected_row_loss"]
    parent_incidence = sum(rows[key]["open_parents"] for key in new_union)
    projected_parent_rows_lost = sum(
        int(item["rows_lost"]) for item in parent_projection.values()
    )
    projected_parent_cost_delta = sum(
        int(item["projected_cost_delta"]) for item in parent_projection.values()
    )

    result = {
        "schema": "n11-class2-lane-cost64d-marginal-audit-third-20261116-v1",
        "date": "2026-11-16",
        "method": "Independent D4 re-canonicalization of all 23 WIN roots and their seven one-stone deletions; only rows with open_candidates_after_transfers > 0 count as new marginals",
        "worklist_rows": len(rows),
        "legal_candidates": len(legal),
        "win_roots": len(win_bits),
        "distinct_d4_win_root_orbits": len(root_orbits),
        "raw_subset_hits": {
            "unique_rows": len(raw_union),
            "receipt_row_edges": raw_edges,
            "already_scheduled_rows_excluded": len(raw_union - new_union),
            "already_scheduled_edges_excluded": raw_edges - new_edges,
        },
        "new_marginals": {
            "unique_rows": len(new_union),
            "receipt_row_edges": new_edges,
            "receipt_coverage_histogram": {
                str(key): histogram[key] for key in sorted(histogram)
            },
            "parent_row_incidences": parent_incidence,
            "published_parent_rows_lost": projected_parent_rows_lost,
            "sum_projected_parent_cost_delta": projected_parent_cost_delta,
            "projected_head": fold["projected_head_after_fold"],
        },
        "per_root_marginals_match_published_audit": not mismatches,
        "mismatches": mismatches,
        "swept_child_in_new_marginals": claim["s6_child"] in new_union,
        "per_root": per_root,
        "newly_closed_rows": [
            {
                "s6_canonical_hex": key,
                "category": rows[key]["category"],
                "edge_cost": rows[key]["cost"],
                "open_parents": rows[key]["open_parents"],
            }
            for key in sorted(new_union)
        ],
        "interpretation_guard": "Structural fold-prep audit only: it does not independently verify WIN7-D10 engine verdicts, does not apply the fold, and proves no game-theoretic value for any parent or the 11x11 empty board.",
    }

    assert len(rows) == 6438
    assert len(legal) == 64
    assert len(win_bits) == 23
    assert len(root_orbits) == 23
    assert len(raw_union) == 20 and raw_edges == 42
    assert len(new_union) == 16 and new_edges == 38
    assert parent_incidence == projected_parent_rows_lost == 30
    assert projected_parent_cost_delta == -2133
    assert fold["projected_head_after_fold"] == 1435
    assert not mismatches
    assert result["swept_child_in_new_marginals"]

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
