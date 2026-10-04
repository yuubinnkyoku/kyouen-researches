#!/usr/bin/env python3
"""Check the all-rank sharpness recurrence by two exact formulations."""
from itertools import combinations
import json
from pathlib import Path

from independent_count_audit import count_game
from module_core import bits
from twin_core import grundy_occupied


def predicted(n, d):
    if d == 1:
        return 2 if n == 0 else (0 if n % 2 else 3)
    if d == 2:
        return 0 if n == 0 else (3 if n == 1 else 1 + n % 2)
    return n % 2 if n <= d - 2 else (3 - d % 2 if n == d - 1 else 3 - n % 2)


def main():
    rows = []
    direct = 0
    for rank in range(2, 65):
        d = rank - 1
        values = []
        for n in range(rank + 3):
            orbits = tuple((t, b) for t, b in ((d, 2), (d - 1, 5), (0, 6)) if t <= n)
            value, _ = count_game(n, 3, orbits)
            assert value == predicted(n, d)
            if rank <= 7:
                edges = [sum(1 << v for v in subset) | (b << n)
                         for t, b in orbits for subset in combinations(range(n), t)]
                independent = grundy_occupied((1 << (n + 3)) - 1, tuple(edges))["grundy"]
                assert independent == value
                direct += 1
            values.append(value)
        assert values[rank] not in values[:rank]
        rows.append({"rank": rank, "class_sizes": list(range(rank + 3)), "grundy": values,
                     "all_induced_smaller_classes_have_different_grundy": True})
    output = Path(__file__).resolve().parents[1] / "output/rank-sharpness-audit.json"
    output.write_text(json.dumps({"status": "VERIFIED", "all_rank_formula_cases": rows,
                                 "independent_occupied_subset_cases": direct}, indent=2) + "\n")
    print("Sharpness formula:", len(rows), "ranks;", direct, "independent subset cases.")


if __name__ == "__main__":
    main()
