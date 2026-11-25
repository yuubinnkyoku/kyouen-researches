#!/usr/bin/env python3
"""Independently verify the raw class2-lane cost-73c depth-10 sweep."""
from __future__ import annotations

import csv
import json
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
EXP = HERE.parent
OUTPUT = HERE / "output"
MANIFEST = EXP / "n11-s2-5960-milestone5-20261112" / "output"
CHILD_HEX = "00000000000000809082000000000080"
PARENT_HEX = "00000000000000809082000000000000"
EXPECTED_FRESH = {120: 26_150_087, 32: 19_876_385, 67: 14_451_598}


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


def main() -> None:
    child = int(CHILD_HEX, 16)
    parent = int(PARENT_HEX, 16)
    assert child.bit_count() == 6 and parent.bit_count() == 5
    assert child ^ parent == 1 << 7

    worklist_path = MANIFEST / "ms5_s6_manifest_part2.csv"
    with worklist_path.open(newline="") as source:
        worklist = {int(row["hex"], 16): row for row in csv.DictReader(source)}
    assert child in worklist
    assert int(worklist[child]["cost"]) == 73
    assert int(worklist[child]["classes"]) == 3

    legal_bits = {
        bit for bit in range(121)
        if not ((child >> bit) & 1) and safe(child | (1 << bit))
    }
    assert len(legal_bits) == 73

    all_rows = []
    per_batch = []
    for batch in range(1, 12):
        path = OUTPUT / f"class2-lane-cost73c-raw-batch{batch}-20261114.jsonl"
        rows = [json.loads(line) for line in path.read_text().splitlines() if line]
        controls = [row for row in rows if row.get("control") == "pilot_d6"]
        candidates = [row for row in rows if "bit" in row]
        assert len(controls) == 1
        control = controls[0]
        assert control["loss"] is False
        assert control["capped"] is False
        assert control["nodes"] == 5_949
        assert len(candidates) == (7 if batch <= 10 else 3)
        for row in candidates:
            assert row["loss"] is False
            assert row["capped"] is False
            assert row["andclose"] is True
            assert row["terminalStoneRange"] == [13, 17]
            assert row["nodes"] > 0
        all_rows.extend(candidates)
        per_batch.append(len(candidates))

    bits = [row["bit"] for row in all_rows]
    assert len(bits) == len(set(bits)) == 73
    assert set(bits) == legal_bits

    record = json.loads(
        (OUTPUT / "class2-lane-cost73c-sweep-20261114.json").read_text()
    )
    assert record["s5_parent_hex"] == PARENT_HEX
    assert record["s6_child_hex"] == CHILD_HEX
    assert record["s6_s7_edge_cost"] == 73
    assert record["demand_classes"] == {"c1": 2, "c2": 2, "c4": 0}
    assert record["win7_d10"] == 0 and record["win7_bits"] == []
    assert record["refuted_d10"] == 73 and record["capped"] == 0
    assert sum(row["nodes"] for row in all_rows) == record["total_nodes"] == 388_889_991
    assert record["terminal_stone_range_all"] == [[13, 17]]

    heaviest = sorted(all_rows, key=lambda row: row["nodes"], reverse=True)[:6]
    assert record["heaviest_bits"] == [
        {"bit": row["bit"], "nodes": row["nodes"]} for row in heaviest
    ]
    node_by_bit = {row["bit"]: row["nodes"] for row in all_rows}
    assert {bit: node_by_bit[bit] for bit in EXPECTED_FRESH} == EXPECTED_FRESH

    print(json.dumps({
        "s6_child": CHILD_HEX,
        "worklist_cost": 73,
        "legal_candidates": len(legal_bits),
        "raw_candidate_rows": len(all_rows),
        "unique_candidate_bits": len(set(bits)),
        "batch_candidate_counts": per_batch,
        "pilot_controls": 11,
        "pilot_nodes_each": 5_949,
        "total_nodes": record["total_nodes"],
        "result": "73 REFUTED-D10 / 0 WIN7-D10 / 0 capped",
        "fresh_rerun_nodes_match": EXPECTED_FRESH,
        "frontier_change": False,
    }, indent=2))


if __name__ == "__main__":
    main()
