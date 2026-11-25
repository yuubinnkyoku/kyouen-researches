#!/usr/bin/env python3
"""Check minimum-union bounds against independently enumerated exact optima."""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import hashlib
from itertools import combinations_with_replacement
import json
from pathlib import Path
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/scripts/optimize_s5_selection.py"
sys.path.insert(0, str(SOURCE.parent))
from optimize_s5_selection import Instance, _group_pool_packing, lower_bounds  # noqa: E402
from historical_option_packing import _lp_relaxation_dual as historical_bound  # noqa: E402

VALID_FIELDS = (
    "per_group_min_max", "threshold_cover_max_of_min_option",
    "element_only_fractional_dual", "grouped_fractional_dual_alternating_packing",
    "lp_relaxation_dual_fractional_packing", "best_valid_lower_bound",
)


def subsets(n: int) -> list[set[int]]:
    return [{e for e in range(n) if mask & (1 << e)} for mask in range(1 << n)]


def exact_optimum(inst: Instance) -> tuple[int, set[int]]:
    """Enumerate candidate unions, without using any planner implementation."""
    universe = sorted({e for c in inst.cost for e in c})
    candidates = sorted(range(1 << len(universe)), key=int.bit_count)
    for mask in candidates:
        union = {e for j, e in enumerate(universe) if mask & (1 << j)}
        if all(any(inst.cost[s] <= union for s in opts) for opts in inst.groups):
            return len(union), union
    raise AssertionError("nonempty option groups must admit a union")


def check_instance(inst: Instance) -> dict:
    optimum, union = exact_optimum(inst)
    bounds = lower_bounds(inst)
    for field in VALID_FIELDS:
        assert bounds[field] <= optimum, (field, bounds, optimum, inst.groups, inst.cost)
    weight, denominator = _group_pool_packing(inst)
    load: Counter[int] = Counter()
    for i, numerator in weight.items():
        assert isinstance(numerator, int) and numerator >= 0
        for e in inst.pool[i]:
            load[e] += numerator
    assert all(n <= denominator for n in load.values()), (weight, denominator, load)
    numerator = sum(min(len(inst.cost[s]) for s in inst.groups[i]) * weight[i]
                    for i in inst.paid)
    exact_bound = Fraction(numerator, denominator)
    assert exact_bound <= optimum
    return {"optimum": optimum, "feasible_union": sorted(union), "bounds": bounds,
            "pool_bound_exact": [exact_bound.numerator, exact_bound.denominator],
            "pool_weights_numerator": weight, "pool_denominator": denominator,
            "maximum_capacity_numerator": max(load.values(), default=0)}


def make_instance(groups: tuple | list, cost: list[set[int]]) -> Instance:
    return Instance([list(g) for g in groups], [(i, 0, 0) for i in range(len(groups))], cost)


def all_families(option_count: int) -> list[tuple[int, ...]]:
    return [tuple(i for i in range(option_count) if mask & (1 << i))
            for mask in range(1, 1 << option_count)]


def run_audit() -> dict:
    started = time.time()
    counterexample = make_instance([[0, 1]], [{0}, {1}])
    counterexample_result = check_instance(counterexample)
    counterexample_result["historical_invalid_bound"] = historical_bound(counterexample)
    assert counterexample_result["historical_invalid_bound"] == 2
    assert counterexample_result["optimum"] == 1
    triangle = make_instance([[0, 1], [0, 2], [1, 2]], [{0}, {1}, {2}])
    triangle_result = check_instance(triangle)
    assert triangle_result["pool_bound_exact"] == [3, 2]
    assert triangle_result["optimum"] == 2
    exhaustive = []
    total = 0
    # Families contain the empty cost option too; this exercises free groups.
    # Permuting groups changes no optimum, so test unordered multisets of them.
    for n, group_count in ((3, 2), (2, 3)):
        cost = subsets(n)
        families = all_families(len(cost))
        count = 0
        for groups in combinations_with_replacement(families, group_count):
            check_instance(make_instance(groups, cost))
            count += 1
        exhaustive.append({"universe_elements": n, "groups": group_count,
                           "distinct_nonempty_option_families": len(families),
                           "group_multisets_checked": count})
        total += count
    rng = random.Random(20261013)
    random_count = 1000
    for _ in range(random_count):
        n = rng.choice((4, 5, 6))
        cost = [c for c in subsets(n) if c]
        groups = [rng.sample(range(len(cost)), rng.randint(1, min(len(cost), 8)))
                  for _ in range(rng.randint(1, 7))]
        # Repeated cost sets with distinct option IDs also remain sound.
        if rng.random() < 0.25:
            cost.append(set(cost[0]))
            groups[0].append(len(cost) - 1)
        check_instance(make_instance(groups, cost))
    total += random_count
    return {"schema": "minimum-union-lower-bound-audit-v1", "passed": True,
            "source": str(SOURCE.relative_to(ROOT)),
            "source_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "counterexample": counterexample_result, "fractional_triangle": triangle_result,
            "exhaustive": exhaustive, "seeded_random_instances": random_count,
            "random_seed": 20261013, "total_finite_instances_checked": total + 2,
            "checks": ["Every reported valid lower bound <= independently enumerated exact optimum",
                       "All new group-pool capacities checked with exact integer arithmetic",
                       "Group-pool objective checked with Fraction",
                       "Empty cost options, repeated groups, and duplicated option costs included"],
            "seconds": round(time.time() - started, 3)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=EXP / "output/finite-instance-audit.json")
    args = parser.parse_args()
    result = run_audit()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in ("counterexample", "fractional_triangle")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
