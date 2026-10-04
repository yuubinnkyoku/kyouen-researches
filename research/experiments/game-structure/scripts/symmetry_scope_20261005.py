#!/usr/bin/env python3
"""Reproduce odd-uniform counterexamples and the high-D4-stabilizer census.

The mathematical results are proved in the accompanying report.  This
script checks the counterexamples by two recurrences, and checks the square
classification by subgroup-orbit enumeration using the shared geometry
core, independently of the formula-based candidate generator.
"""
from collections import Counter
from functools import cache
from itertools import combinations
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts/research"))
from kyouen_core import is_forbidden_quad


def bits(mask):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def counterexample(q):
    v = q + 1
    full = (1 << v) - 1
    forbidden = [full ^ (1 << p) for p in (2, 3)]
    symmetric = full ^ 3

    @cache
    def grundy(s):
        seen = set()
        for p in bits(full ^ s):
            child = s | (1 << p)
            if not any(child & e == e for e in forbidden):
                seen.add(grundy(child))
        g = 0
        while g in seen:
            g += 1
        return g

    # Independent level-wise P/N recurrence, using occupied ID sets rather
    # than bitmask edges or mex.  It also checks all safe states of this game.
    edges = [frozenset(bits(e)) for e in forbidden]
    safe = []
    for k in range(v, -1, -1):
        safe.extend(frozenset(s) for s in combinations(range(v), k)
                    if not any(e <= frozenset(s) for e in edges))
    pn = {}
    for s in safe:
        children = [s | {p} for p in range(v) if p not in s
                    and not any(e <= s | {p} for e in edges)]
        pn[s] = any(not pn[c] for c in children)
        assert pn[s] == bool(grundy(sum(1 << p for p in s)))
    assert grundy(0) == grundy(symmetric) == 1
    assert all(grundy(symmetric | (1 << p)) == 0 for p in (0, 1))
    assert not any(symmetric & e == e for e in forbidden)
    return {"q": q, "vertices": v, "involution": [p ^ 1 for p in range(v)],
            "forbidden_edges": [list(bits(e)) for e in forbidden],
            "symmetric_position": list(bits(symmetric)),
            "root_grundy": grundy(0), "position_grundy": grundy(symmetric),
            "independent_safe_states_checked": len(safe),
            "first_move": 0, "mirror_reply": 1,
            "first_safe": True, "reply_safe": False}


def permutations(n):
    out = []
    for swap in (False, True):
        for flip_x in (False, True):
            for flip_y in (False, True):
                perm = []
                for p in range(n * n):
                    x, y = p % n, p // n
                    if swap:
                        x, y = y, x
                    if flip_x:
                        x = n - 1 - x
                    if flip_y:
                        y = n - 1 - y
                    perm.append(x + n * y)
                out.append(perm)
    return out


def transform(s, perm):
    return sum(1 << perm[p] for p in bits(s))


def candidate_formula(n):
    """Use the proved axes classification, with doubled centered coordinates."""
    index = {(2*x-(n-1), 2*y-(n-1)): x+n*y
             for y in range(n) for x in range(n)}
    result = set()
    orientations = [((1, 0), (0, 1)), ((1, 1), (1, -1))]
    center_choices = [0, 1 << index[(0, 0)]] if n % 2 else [0]
    for u, v in orientations:
        pairs = []
        for dx, dy in (u, v):
            axis = [(0, 0)]
            for a in range(1, n):
                pos, neg = (a*dx, a*dy), (-a*dx, -a*dy)
                if pos in index and neg in index:
                    axis.append((a, (1 << index[pos]) | (1 << index[neg])))
            pairs.append(axis)
        for a, x in pairs[0]:
            for b, y in pairs[1]:
                if a and b and a == b:
                    continue
                for center in center_choices:
                    result.add(x | y | center)
    return result


def subgroup_census(n):
    points = [(x, y) for y in range(n) for x in range(n)]
    perms = permutations(n)

    def safe(s):
        return not any(is_forbidden_quad([points[p] for p in ids])
                       for ids in combinations(bits(s), 4))

    # Derive all subgroups of D4 of order >=4 from closure of permutations.
    # n=1 collapses the permutation representation; use n=3 to identify the
    # abstract multiplication table, preserving all eight group elements.
    abstract = permutations(3)
    composition = [[abstract.index([b[a[p]] for p in range(9)])
                    for b in abstract] for a in abstract]
    subgroups = []
    for mask in range(256):
        members = list(bits(mask))
        if len(members) >= 4 and 0 in members and all(
                composition[a][b] in members for a in members for b in members):
            subgroups.append(members)
    assert len(subgroups) == 4

    found = set()
    for group in subgroups:
        remaining = set(range(n*n))
        safe_orbits = []
        while remaining:
            p = min(remaining)
            orbit = {perms[g][p] for g in group}
            remaining -= orbit
            mask = sum(1 << p for p in orbit)
            if safe(mask):
                safe_orbits.append(mask)
        # Every unsafe orbit is excluded by hereditary safety.  Enumerate
        # all subsets of the remaining orbits, with safety pruning.
        def visit(i, s):
            if i == len(safe_orbits):
                found.add(s)
                return
            visit(i+1, s)
            child = s | safe_orbits[i]
            if safe(child):
                visit(i+1, child)
        visit(0, 0)
    formula = candidate_formula(n)
    assert found == formula
    expected = n*n+1 if n % 2 else n*n//4+n//2+1
    assert len(found) == expected
    sizes, stabilizers = Counter(), Counter()
    five_without_small_legal = 0
    for s in found:
        group = [p for p in perms if transform(s, p) == s]
        assert len(group) >= 4
        sizes[s.bit_count()] += 1
        stabilizers[len(group)] += 1
        if s.bit_count() == 5:
            for p in range(n*n):
                if (s >> p) & 1 or not safe(s | (1 << p)):
                    continue
                assert len({g[p] for g in group}) == 4
            five_without_small_legal += 1
    return {"n": n, "all_high_stabilizer_safe_states": len(found),
            "formula_count": expected, "size_distribution": dict(sorted(sizes.items())),
            "stabilizer_distribution": dict(sorted(stabilizers.items())),
            "five_stone_states_with_no_small_legal_orbit": five_without_small_legal,
            "independent_subgroup_enumeration_matches_formula": True}


def main():
    if not __debug__:
        raise SystemExit("Assertions must remain enabled.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=11)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "research/experiments/game-structure/output/symmetry_scope_20261005.json")
    args = parser.parse_args()
    assert 1 <= args.max_n <= 15
    result = {"odd_uniform_counterexamples": [counterexample(q) for q in (3, 5, 7, 9)],
              "square_high_stabilizer_census": [subgroup_census(n)
                                               for n in range(1, args.max_n+1)],
              "limits": "No new full-square Grundy census; K0186 remains open. General proofs are in the report."}
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps({"counterexample_q": [3, 5, 7, 9],
                      "squares_checked": args.max_n,
                      "output": str(args.output)}))


if __name__ == "__main__":
    main()
