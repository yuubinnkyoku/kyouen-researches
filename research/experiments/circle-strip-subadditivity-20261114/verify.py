#!/usr/bin/env python3
"""Finite checks for the certified P(w) table and circle witnesses.

The all-width subadditivity and remainder arguments are in report.md.
This script checks the published finite table, the P(83) witness, and the
sharp remainder constant for slope 16/41.
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

    # The global bound uses only remainders r=0..81 after division by 82.
    remainder_errors = {
        r: 41 * p[r] - 16 * r
        for r in range(82)
    }
    best_error = max(remainder_errors.values())
    best_remainder = min(
        r for r, error in remainder_errors.items() if error == best_error
    )
    assert (best_error, best_remainder, p[best_remainder]) == (568, 26, 24)

    # Finite table values also satisfy the resulting affine inequality.
    for w in range(84):
        assert 41 * p[w] - 16 * w <= 568

    print(
        "PASS: P(82)=32, P(83)=34, witness_points=34, "
        f"subadditivity_table_pairs={checks}, "
        f"minimum_known_ratio={best_ratio} at w={best_width}, "
        "sharp_additive_error=568/41 at remainder=26"
    )


if __name__ == "__main__":
    main()
