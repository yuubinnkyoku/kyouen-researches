#!/usr/bin/env python3
"""Independent audit of the cost-70c raw sweep and its current frontier context.

Uses only Python's standard library and exact Bareiss determinants. It does not
import the search engine, its verdict cache, or the repository certificate verifier.
"""
from __future__ import annotations

import csv
import hashlib
import json
import re
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / "output"
SOURCE_MAIN_HEAD = "7cec3e7e8960e2099d53d306a4ca0eafd6f284e4"
CHILD_HEX = "00000000000000803242000000000000"
PARENT_HEX = "00000000000000803202000000000000"
EXPECTED_BATCH_COUNTS = [8, 8, 8, 8, 8, 8, 8, 8, 6]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def det4(points: tuple[int, int, int, int]) -> int:
    """Exact Bareiss determinant of rows [x²+y²,x,y,1]."""
    matrix = []
    for point in points:
        x, y = point % 11, point // 11
        matrix.append([x * x + y * y, x, y, 1])
    sign, previous = 1, 1
    for k in range(3):
        if matrix[k][k] == 0:
            pivot_row = next((r for r in range(k + 1, 4) if matrix[r][k] != 0), None)
            if pivot_row is None:
                return 0
            matrix[k], matrix[pivot_row] = matrix[pivot_row], matrix[k]
            sign *= -1
        pivot = matrix[k][k]
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                numerator = matrix[i][j] * pivot - matrix[i][k] * matrix[k][j]
                if numerator % previous:
                    raise ArithmeticError("Bareiss division was not exact")
                matrix[i][j] = numerator // previous
        for i in range(k + 1, 4):
            matrix[i][k] = 0
        previous = pivot
    return sign * matrix[3][3]


def points_of(mask: int) -> list[int]:
    return [bit for bit in range(121) if (mask >> bit) & 1]


def is_safe(points: list[int]) -> bool:
    return all(det4(q) != 0 for q in combinations(points, 4))


def legal_moves(points: list[int]) -> list[int]:
    occupied = set(points)
    triples = list(combinations(points, 3))
    return [
        bit for bit in range(121)
        if bit not in occupied and all(det4((*triple, bit)) != 0 for triple in triples)
    ]


def csv_rows(path: Path) -> list[dict]:
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip() or line.startswith("#") or line.startswith('"#'):
            continue
        fields = next(csv.reader([line]))
        if len(fields) != 4 or fields[0] == "s5_hex":
            continue
        if not re.fullmatch(r"[0-9a-f]{32}", fields[0]):
            continue
        rows.append({
            "s5_hex": fields[0],
            "s6_hex": fields[1],
            "cost": int(fields[2]),
            "demand": fields[3],
        })
    return rows


def main() -> None:
    claim_path = OUT / "class2-lane-cost70c-inflight-20261115.json"
    claim = json.loads(claim_path.read_text())
    child_hex = claim["s6_child"]
    parent_hex = claim["s5_parent"]
    child_mask = int(child_hex, 16)
    child_points = points_of(child_mask)
    legal = legal_moves(child_points)
    claimed_bits = claim["candidate_bits"]
    assert child_hex == CHILD_HEX and parent_hex == PARENT_HEX
    assert len(child_points) == 6 and is_safe(child_points)
    assert legal == claimed_bits
    assert len(legal) == claim["legal_candidates_total"] == 70

    raw_rows = []
    batches = []
    raw_hashes = {}
    for index in range(1, 10):
        path = OUT / f"class2-lane-cost70c-raw-batch{index}-20261115.jsonl"
        records = read_jsonl(path)
        candidates = [row for row in records if "bit" in row]
        pilots = [row for row in records if row.get("control") == "pilot_d6"]
        assert len(pilots) == 1
        pilot = pilots[0]
        assert pilot.get("loss") is False and pilot.get("capped") is False
        assert pilot.get("nodes") == 3402
        batches.append({
            "batch": index,
            "candidate_count": len(candidates),
            "pilot_count": len(pilots),
            "pilot_nodes": pilot["nodes"],
            "pilot_loss": pilot["loss"],
            "pilot_capped": pilot["capped"],
        })
        raw_rows.extend(candidates)
        raw_hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()

    assert [batch["candidate_count"] for batch in batches] == EXPECTED_BATCH_COUNTS
    raw_bits = [row["bit"] for row in raw_rows]
    assert raw_bits == claimed_bits
    assert len(raw_rows) == len(set(raw_bits)) == 70
    wins = [row for row in raw_rows if row.get("loss") is True]
    refuted = [row for row in raw_rows if row.get("loss") is False and not row.get("capped")]
    capped = [row for row in raw_rows if row.get("capped")]
    assert len(wins) == 13 and len(refuted) == 57 and len(capped) == 0
    assert sum(row["nodes"] for row in raw_rows) == 100_935_666
    assert all(row.get("terminalStoneRange") == [13, 17] for row in raw_rows)
    assert all(row.get("andclose") is True for row in raw_rows)

    root_metrics = []
    for row in wins:
        root_mask = child_mask | (1 << row["bit"])
        root_points = points_of(root_mask)
        assert is_safe(root_points)
        root_metrics.append({
            "bit": row["bit"],
            "root_hex": f"{root_mask:032x}",
            "search_nodes": row["nodes"],
            "root_safe": True,
            "opponent_legal_replies": len(legal_moves(root_points)),
        })
    root_metrics.sort(key=lambda row: (row["opponent_legal_replies"], row["search_nodes"]))

    cert_paths = sorted(OUT.glob("class2-lane-cost*-win7-certificates-20261114.json"))
    cert_paths += sorted(OUT.glob("class2-lane-cost*-warm-certificates-20261114.json"))
    cert_matches = {row["root_hex"]: [] for row in root_metrics}
    for path in cert_paths:
        content = path.read_text()
        for root_hex in cert_matches:
            if root_hex in content:
                cert_matches[root_hex].append(path.name)

    sweep_matches = {row["root_hex"]: [] for row in root_metrics}
    for path in sorted(OUT.glob("class2-lane-cost*-sweep-*.json")):
        try:
            sweep = json.loads(path.read_text())
        except json.JSONDecodeError:
            continue
        roots = sweep.get("win7_roots", [])
        bits = sweep.get("win7_bits", [])
        for root_hex, bit in zip(roots, bits):
            if root_hex in sweep_matches:
                sweep_matches[root_hex].append({"file": path.name, "bit": bit})

    frontier = json.loads((OUT / "class-frontier-cost69e-recompute-20261115.json").read_text())
    frontier_after = frontier["frontier_after_cost69e"]
    closed_by_bit76 = child_hex in frontier["cost69e_addition"]["76"]["marginal_manifest_hexes"]
    assert closed_by_bit76

    top_path = OUT / "class-frontier-top-candidates-s6-after-cost69e-20261115.csv"
    top_rows = csv_rows(top_path)
    parent_rows = [row for row in top_rows if row["s5_hex"] == parent_hex]
    unique_parent_rows = {row["s6_hex"]: row for row in parent_rows}
    assert len(unique_parent_rows) == 6
    assert sum(row["cost"] for row in unique_parent_rows.values()) == 443
    assert child_hex not in unique_parent_rows
    next_child = min(unique_parent_rows.values(), key=lambda row: (row["cost"], row["s6_hex"]))
    assert next_child["cost"] == 71

    pending_v15 = not any(OUT.glob("class2-lane-cost70c-v15-crosscheck-*.jsonl"))
    pending_certificates = not any(OUT.glob("class2-lane-cost70c-win7-certificates-*.json"))

    result = {
        "schema": "n11-class2-cost70c-independent-raw-sweep-audit-v1",
        "source_main_head": SOURCE_MAIN_HEAD,
        "independent_method": "Python standard library; exact Bareiss determinant; no floating point",
        "claim": {
            "s5_parent": parent_hex,
            "s6_child": child_hex,
            "s6_s7_edge_cost": claim["s6_s7_edge_cost"],
            "demand_classes": claim["demand_classes"],
        },
        "geometry": {
            "child_stones": len(child_points),
            "child_safe": True,
            "independent_legal_candidate_count": len(legal),
            "candidate_bits_exact_match": True,
        },
        "batches": batches,
        "raw_sweep": {
            "candidate_rows": len(raw_rows),
            "unique_candidate_bits": len(set(raw_bits)),
            "win7_d10_candidates": len(wins),
            "win7_bits": [row["bit"] for row in wins],
            "refuted_d10_candidates": len(refuted),
            "capped_candidates": len(capped),
            "total_search_nodes": sum(row["nodes"] for row in raw_rows),
            "all_terminal_ranges_13_17": True,
            "all_andclose": True,
            "raw_batch_sha256": raw_hashes,
        },
        "win7_roots_by_opponent_mobility": root_metrics,
        "certificate_manifest_scan": {
            "manifest_count": len(cert_paths),
            "candidate_root_matches": cert_matches,
            "all_13_roots_uncertified_in_scanned_manifests": all(not v for v in cert_matches.values()),
        },
        "prior_sweep_scan": {
            "candidate_root_matches": sweep_matches,
            "warm_rebuild_candidate": {
                "bit": 20,
                "root_hex": "00000000000000803242000000100000",
                "prior_file": "class2-lane-cost64b-sweep-20261114.json",
                "prior_bit": 54,
                "prior_verdict": "WIN7-D10, not a certificate",
            },
        },
        "frontier_after_cost69e": {
            "s6_solved_in_manifest": frontier_after["s6_solved_in_manifest"],
            "s6_unique_remaining": frontier_after["s6_unique_remaining"],
            "s6_sum_remaining_s7_edge_cost": frontier_after["s6_sum_remaining_s7_edge_cost"],
            "s6_needed_by_open_classes": frontier_after["s6_needed_by_open_classes"],
            "sum_remaining_s7_edge_cost_needed_by_open_classes": frontier_after["sum_remaining_s7_edge_cost_needed_by_open_classes"],
            "best_coverable_class2": frontier_after["best_coverable_class2"],
        },
        "midflight_closure": {
            "cost70c_child_closed_by_cost69e_bit76": closed_by_bit76,
            "cost70c_child_is_still_open": False,
            "frontier_change_from_cost70c_raw_sweep": "none; raw WIN7-D10 rows are not certificates",
        },
        "current_top_candidates": {
            "parent_unique_remaining_children": len(unique_parent_rows),
            "parent_remaining_cost": sum(row["cost"] for row in unique_parent_rows.values()),
            "next_child": next_child,
            "cost70c_child_absent": True,
        },
        "pending": {
            "v15_crosscheck": pending_v15,
            "certificate_extraction": pending_certificates,
            "overall_lane_status": "raw v16 sweep complete; lane remains in-flight",
        },
        "interpretation": {
            "win7_d10_is_not_a_certificate": True,
            "refuted_d10_is_not_a_loss_proof": True,
            "standard_11x11_empty_board": "UNKNOWN",
            "two_stone_roots_49_60_and_59_60": "UNKNOWN",
            "s2_59_60": "UNKNOWN",
        },
    }
    output = OUT / "class2-lane-cost70c-raw-sweep-audit-20261115.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
