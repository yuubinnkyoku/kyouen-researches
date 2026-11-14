#!/usr/bin/env python3
"""Finite checks for the certified P(w) table and the P(83) witness.

The all-width subadditivity proof is in report.md; this script checks the
published finite table and the explicit 34-point lower-bound witness.
"""
from collections import Counter
from csv import DictReader
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TABLE = ROOT / "results/fixed-width/pw_circle_point_max.csv"


def main() -> None:
    with TABLE.open(encoding="utf-8", newline="") as stream:
        rows = list(DictReader(stream))

    values = {int(row["w"]): int(row["P(w)"]) for row in rows}
    assert set(values) == set(range(2, 84))
    assert all(row["status"] == "proved-exact" for row in rows)

    p = {0: 0, 1: 2, **values}
    assert (p[82], p[83]) == (32, 34)

    # Independently enumerate the odd-coordinate solutions of the witness
    # circle (2x-105)^2 + (2y-105)^2 = 11050 in rows 0..82.
    witness_points = set()
    for X in range(-105, 106, 2):
        for Y in range(-105, 106, 2):
            if X * X + Y * Y == 11050:
                x = (X + 105) // 2
                y = (Y + 105) // 2
                if 0 <= y <= 82:
                    witness_points.add((x, y))

    row_counts = Counter(y for _, y in witness_points)
    expected_rows = [0, 1, 5, 6, 9, 12, 19, 23, 28, 30, 42, 50, 55, 63, 75, 77, 82]
    assert len(witness_points) == 34
    assert sorted(row_counts) == expected_rows
    assert set(row_counts.values()) == {2}

    # Check every subadditivity instance a+b <= 83 in the published table.
    checks = 0
    for a in range(84):
        for b in range(84 - a):
            assert p[a + b] <= p[a] + p[b], (a, b)
            checks += 1
    assert checks == 3570

    best_ratio, best_width = min(
        (Fraction(p[w], w), w) for w in range(1, 84)
    )
    assert (best_ratio, best_width) == (Fraction(16, 41), 82)

    for w in range(84):
        k, r = divmod(w, 82)
        assert p[w] <= 32 * k + 2 * r

    print(
        "PASS: rows=82, P(82)=32, P(83)=34, witness_points=34, "
        f"subadditivity_table_pairs={checks}, "
        f"minimum_known_ratio={best_ratio} at w={best_width}"
    )


if __name__ == "__main__":
    main()
