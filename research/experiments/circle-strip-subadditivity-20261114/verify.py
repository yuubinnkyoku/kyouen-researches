#!/usr/bin/env python3
"""Finite consistency checks for the certified P(w) table.

This script does not prove subadditivity for all widths. The all-width
statement is proved by splitting every (a+b)-row window in report.md.
"""
from csv import DictReader
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
TABLE = ROOT / "results/fixed-width/pw_circle_point_max.csv"


def main() -> None:
    with TABLE.open(encoding="utf-8", newline="") as stream:
        rows = list(DictReader(stream))

    values = {int(row["w"]): int(row["P(w)"]) for row in rows}
    assert set(values) == set(range(2, 83))
    assert all(row["status"] == "proved-exact" for row in rows)

    p = {0: 0, 1: 2, **values}
    assert p[82] == 32

    checks = 0
    for a in range(83):
        for b in range(83 - a):
            assert p[a + b] <= p[a] + p[b], (a, b)
            checks += 1
    assert checks == 3486

    best_ratio, best_width = min(
        (Fraction(p[w], w), w) for w in range(1, 83)
    )
    assert (best_ratio, best_width) == (Fraction(16, 41), 82)

    for w in range(83):
        k, r = divmod(w, 82)
        assert p[w] <= 32 * k + 2 * r

    print(
        "PASS: rows=81, P(82)=32, "
        f"subadditivity_table_pairs={checks}, "
        f"minimum_known_ratio={best_ratio} at w={best_width}"
    )


if __name__ == "__main__":
    main()
