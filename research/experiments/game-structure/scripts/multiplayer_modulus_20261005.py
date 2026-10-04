#!/usr/bin/env python3
"""Finite cross-checks of the all-r terminal-player congruence theorem.

The proof is separate.  Compare maximal-cardinality arithmetic against a
direct continuation DAG for every nonempty complex on <=4 labeled points.
The geometric examples reuse the shared integer geometry core.
"""
from collections import Counter
from functools import cache
from itertools import combinations
from math import gcd
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts/research"))
from kyouen_core import Board, square_points


def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length()-1
        mask ^= b


def modulus(sizes):
    sizes = list(sizes)
    return gcd(*(s-sizes[0] for s in sizes))


def complexes(v):
    masks = list(range(1 << v))
    for chosen in range(1, 1 << len(masks)):
        facets = [masks[i] for i in bits(chosen)]
        if any(a & b == a for a, b in combinations(facets, 2)) or any(
                a & b == b for a, b in combinations(facets, 2)):
            continue
        family = {s for s in masks if any(s & f == s for f in facets)}
        yield family, facets


def verify_family(family, facets, r_values):
    @cache
    def terminal_sizes(s):
        children = [s | (1 << p) for p in range(max(family).bit_length())
                    if not (s >> p) & 1 and s | (1 << p) in family]
        return (frozenset().union(*(terminal_sizes(c) for c in children))
                if children else frozenset({s.bit_count()}))

    delta = modulus(f.bit_count() for f in facets)
    checks = 0
    for r in r_values:
        strategy_independent = True
        for s in family:
            reachable = {f.bit_count() for f in facets if f & s == s}
            assert reachable == terminal_sizes(s)
            d = modulus(reachable)
            losers = {(t-s.bit_count()) % r for t in terminal_sizes(s)}
            assert (len(losers) == 1) == (d % r == 0)
            strategy_independent &= len(losers) == 1
            checks += 1
        assert strategy_independent == (delta % r == 0)
    return delta, checks


def square(n):
    b = Board(square_points(n))
    family = {s for s in range(1 << b.V) if b.is_safe(s)}
    facets = [s for s in family if b.is_maximal(s)]
    delta, checks = verify_family(family, facets, range(2, 9))
    hist = Counter(s.bit_count() for s in facets)
    return {"n": n, "safe_states": len(family), "maximal_size_counts": dict(sorted(hist.items())),
            "terminal_difference_gcd": delta,
            "root_possible_losers_by_r": {r: sorted({t % r for t in hist})
                                          for r in range(2, 9)},
            "direct_dag_state_modulus_checks": checks}


def main():
    if not __debug__:
        raise SystemExit("Assertions must remain enabled.")
    all_facets, rows = [], []
    for v in range(5):
        count, checks = 0, 0
        for family, facets in complexes(v):
            d, c = verify_family(family, facets, range(2, 9))
            count += 1
            checks += c
            all_facets.append(([f.bit_count() for f in facets], d))
        rows.append({"vertices": v, "all_nonempty_downward_closed_families": count,
                     "direct_dag_state_modulus_checks": checks})
    products = 0
    for a, da in all_facets:
        for b, db in all_facets:
            assert modulus(x+y for x in a for y in b) == gcd(da, db)
            products += 1
    result = {"abstract_complete_census": rows, "all_ordered_product_checks": products,
              "square_examples": [square(n) for n in range(1, 5)],
              "limits": "The r-person rule stops at the first player without a legal move. No multiplayer Sprague-Grundy or xor claim."}
    path = ROOT / "research/experiments/game-structure/output/multiplayer_modulus_20261005.json"
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"complexes": sum(r["all_nonempty_downward_closed_families"] for r in rows),
                      "product_checks": products, "squares": 4}))


if __name__ == "__main__":
    main()
