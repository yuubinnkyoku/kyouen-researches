#!/usr/bin/env python3
"""Independent audit of the cost-74d raw sweep (class2 lane, third target S5).

Uses only Python's standard library and exact Bareiss determinants. It does not
import the search engine, its verdict cache, or the repository certificate verifier.
Adapted from audit_cost70c_raw_sweep.py; the d4 canonicalization is additionally
cross-validated against the published class2-lane-cost69f-sweep-audit win roots.
"""
from __future__ import annotations

import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parents[0]
_repo_out = HERE.parent / "output"
OUT = _repo_out if _repo_out.is_dir() else HERE.parent / "out"
CHILD_HEX = "00000000000000809102020000000000"
PARENT_HEX = "00000000000000809102000000000000"
EXPECTED_BATCH_COUNTS = [8, 8, 8, 8, 8, 8, 8, 8, 8, 2]
BATCH_BLOB_SHAS = [
    "d387b6d62cc7001143e66764d20c118688eb863c",
    "90b4e3429f3fb1e7e7aa80d6bac13e30260adf7f",
    "c3f028669ec09e4627d7ec438eb6b4bbe014a1cd",
    "2d92dd60f6625185764f6e70d1ce3c81aba28826",
    "abcfb584b60e6add1f1fa733219bc2d84431c0e5",
    "b48d1aacefcb623629ed7d791a3a3a51f873d5bb",
    "27f459954758e22a5fd0125ae5672a8e6005ca98",
    "40c5e861052f8acc709423dfb4a7d2196c568d3d",
    "55b54a1a73b3c4c149067e3c1d3536c45f630718",
    "7d8b63882ed57e82008a8bc7ad96f9021946faee",
]
CLAIM_BLOB_SHA = "dbc347f65866aab07a6f6b98166b516841770e78"
# Published d4 canonical forms from class2-lane-cost69f-sweep-audit-20261115.json
# (blob sha ba8a2ecaa76ce938636bd0d239c3c11602d3ff23), used to validate this
# script's independent d4 canonicalization before it is applied to 74d roots.
D4_VALIDATION_69F = [
    ("0000000000000080910200000000000c", "0000000000000080910200000000000c"),
    ("00000000000000809102000000100008", "00000000000000809102000000100008"),
    ("00000000000000809102100000000008", "00000000000000809102100000000008"),
    ("00000000000000909102000000000008", "00000000000000909102000000000008"),
    ("00000000000000a09102000000000008", "00000000000000a09102000000000008"),
    ("00000000400000809102000000000008", "00000000100000811202000000000080"),
    ("00002000000000809102000000000008", "00000008000000811202000000000080"),
    ("00400000000000809102000000000008", "00000000210000003800080000010000"),
    ("00800000000000809102000000000008", "00000008200000003800080000010000"),
]


def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def det4(points: tuple[int, int, int, int]) -> int:
    """Exact Bareiss determinant of rows [x^2+y^2, x, y, 1]."""
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


D4_TRANSFORMS = [
    lambda x, y: (x, y),
    lambda x, y: (10 - x, y),
    lambda x, y: (x, 10 - y),
    lambda x, y: (10 - x, 10 - y),
    lambda x, y: (y, x),
    lambda x, y: (10 - y, x),
    lambda x, y: (y, 10 - x),
    lambda x, y: (10 - y, 10 - x),
]


def d4_canonical_hex(mask: int) -> str:
    best = None
    for t in D4_TRANSFORMS:
        transformed = 0
        for bit in points_of(mask):
            x, y = bit % 11, bit // 11
            nx, ny = t(x, y)
            transformed |= 1 << (ny * 11 + nx)
        cand = f"{transformed:032x}"
        if best is None or cand < best:
            best = cand
    return best


def main() -> None:
    claim = json.loads((OUT / "class2-lane-cost74d-inflight-20261115.json").read_text())
    child_hex = claim["s6_child"]
    parent_hex = claim["s5"]
    child_mask = int(child_hex, 16)
    child_points = points_of(child_mask)
    assert child_hex == CHILD_HEX and parent_hex == PARENT_HEX
    assert len(child_points) == 6 and is_safe(child_points)

    # 1. Validate the d4 canonicalization against the published 69f audit values.
    for root_hex, expected in D4_VALIDATION_69F:
        got = d4_canonical_hex(int(root_hex, 16))
        assert got == expected, (root_hex, got, expected)

    # 2. Independent geometric re-derivation of the candidate set.
    legal = legal_moves(child_points)
    claimed_bits = claim["legal_candidates"]
    assert legal == claimed_bits, "independent legal-move enumeration differs from claim"
    assert len(legal) == claim["candidate_count"] == 74

    # 3. Parse all ten raw batches.
    raw_rows = []
    batches = []
    for index in range(1, 11):
        path = OUT / f"class2-lane-cost74d-raw-batch{index}-20261115.jsonl"
        records = read_jsonl(path)
        candidates = [row for row in records if "bit" in row]
        pilots = [row for row in records if row.get("control") == "pilot_d6"]
        assert len(pilots) == 1
        pilot = pilots[0]
        assert pilot.get("loss") is False and pilot.get("capped") is False
        assert pilot.get("nodes") == 3402
        repo_path = f"research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/{path.name}"
        batches.append({
            "batch": index,
            "input_path": repo_path,
            "input_blob_sha": BATCH_BLOB_SHAS[index - 1],
            "candidate_bits": [row["bit"] for row in candidates],
            "pilot_nodes": pilot["nodes"],
        })
        raw_rows.extend(candidates)

    assert [len(b["candidate_bits"]) for b in batches] == EXPECTED_BATCH_COUNTS
    raw_bits = [row["bit"] for row in raw_rows]
    assert raw_bits == claimed_bits, "batch bits differ from claim order"
    assert len(raw_rows) == len(set(raw_bits)) == 74

    wins = [row for row in raw_rows if row.get("loss") is True]
    refuted = [row for row in raw_rows if row.get("loss") is False and not row.get("capped")]
    capped = [row for row in raw_rows if row.get("capped")]
    assert len(wins) == 15 and len(refuted) == 59 and len(capped) == 0
    assert sum(row["nodes"] for row in raw_rows) == 101_848_441
    assert all(row.get("terminalStoneRange") == [13, 17] for row in raw_rows)
    assert all(row.get("andclose") is True for row in raw_rows)

    # 4. WIN7 roots: geometry, opponent mobility, d4 canonical orbits.
    win_roots = []
    for row in wins:
        root_mask = child_mask | (1 << row["bit"])
        root_points = points_of(root_mask)
        assert len(root_points) == 7 and is_safe(root_points)
        win_roots.append({
            "bit": row["bit"],
            "nodes": row["nodes"],
            "root_hex": f"{root_mask:032x}",
            "d4_canonical_hex": d4_canonical_hex(root_mask),
            "opponent_legal_replies": len(legal_moves(root_points)),
        })
    win_roots.sort(key=lambda r: r["bit"])
    canonical_forms = [r["d4_canonical_hex"] for r in win_roots]
    assert len(set(canonical_forms)) == 15, "WIN7 roots must have distinct d4 orbits"
    # child | 1<<bit check via integer arithmetic
    for r in win_roots:
        assert int(r["root_hex"], 16) == child_mask | (1 << r["bit"])

    result = {
        "schema": "n11-class2-lane-cost74d-raw-sweep-audit-20261115-v1",
        "date": "2026-11-15",
        "independent_method": "Python standard library; exact Bareiss determinant; no floating point; d4 canonicalization validated against the published cost69f sweep audit",
        "target": {
            "s5_hex": parent_hex,
            "s6_child_hex": child_hex,
            "edge_cost": 74,
            "legal_candidate_count": 74,
        },
        "source_claim": {
            "path": "research/experiments/n11-s2-5960-ms5-s7-reuse-20261113/output/class2-lane-cost74d-inflight-20261115.json",
            "blob_sha": CLAIM_BLOB_SHA,
        },
        "geometry": {
            "child_stones": len(child_points),
            "child_safe": True,
            "independent_legal_candidate_count": len(legal),
            "candidate_bits_exact_match": True,
        },
        "batches": batches,
        "aggregate": {
            "batches": 10,
            "records": len(raw_rows),
            "candidates": 74,
            "win7_d10": 15,
            "win7_d10_bits": [r["bit"] for r in win_roots],
            "refuted_d10": 59,
            "capped": 0,
            "candidate_nodes": sum(row["nodes"] for row in raw_rows),
            "pilot_controls": 10,
            "pilot_nodes": [3402] * 10,
            "win_roots_d4_orbits": len(set(canonical_forms)),
        },
        "win_roots": win_roots,
        "crosschecks": {
            "v15_independent_engine": "class2-lane-cost74d-v15-crosscheck-20261115.jsonl: all 15 WIN7 bits loss=true on v15 (pilot 5949 x5), refuted anchors bits 25,103 loss=false",
            "determinism_rerun": "class2-lane-cost74d-det-rerun-20261115.jsonl: bits 2,102,118 node-exact match vs sweep (1887907/6288355/456245)",
        },
        "checks": {
            "all_74_claim_bits_present_in_order": True,
            "all_74_bits_unique": True,
            "all_batches_have_one_pilot": True,
            "all_pilots_3402": True,
            "all_candidate_verdicts_boolean": True,
            "no_capped_candidates": True,
            "win7_d10_roots_have_distinct_d4_orbits": True,
            "d4_canonicalization_validated_against_69f_audit": True,
        },
        "proof_boundary": {
            "certificate_extraction": "not yet recorded on this main snapshot",
            "independent_certificate_verification": "not yet recorded on this main snapshot",
            "s6_frontier_contribution": 0,
            "note": "WIN7-D10 is a raw depth-limited search verdict for a seven-stone root. It is not a certificate, does not close the six-stone parent by itself, and does not determine the empty-board winner. Fold into the canonical chain requires certificate extraction and independent verification first.",
        },
        "interpretation": {
            "win7_d10_is_not_a_certificate": True,
            "refuted_d10_is_not_a_loss_proof": True,
            "standard_11x11_empty_board": "UNKNOWN",
            "two_stone_roots_49_60_and_59_60": "UNKNOWN",
            "s2_59_60": "UNKNOWN",
            "class_2": "UNKNOWN",
            "class_4": "UNKNOWN",
        },
    }
    output = OUT / "class2-lane-cost74d-sweep-audit-20261115.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({
        "audit_written": str(output),
        "candidates": 74,
        "win7_d10_bits": [r["bit"] for r in win_roots],
        "distinct_d4_orbits": len(set(canonical_forms)),
        "total_nodes": sum(row["nodes"] for row in raw_rows),
    }, indent=2))


if __name__ == "__main__":
    main()
