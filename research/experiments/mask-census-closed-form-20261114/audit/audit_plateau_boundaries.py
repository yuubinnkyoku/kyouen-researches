#!/usr/bin/env python3
"""Independently count distinct passing residue masks at plateau boundaries.

For each modulus enumerate subsets directly, then reconstruct periodic masks
as integer bitsets. This audits the claimed unique-count boundaries only.
"""
from itertools import product
import json


def residue_sets(modulus):
    squares = {x*x % modulus for x in range(modulus)}
    return [{i for i in range(modulus) if (a-4*i*i-u*i) % modulus in squares}
            for a,u in product(range(modulus),repeat=2)]


def count_unique(patterns, width):
    cycles, remainder = divmod(width,99)
    prefix = (1 << remainder)-1
    passed = set()
    for pattern in patterns:
        size = cycles*pattern.bit_count() + (pattern & prefix).bit_count()
        if size >= 17:
            # A full first period uniquely determines each longer mask. Before
            # one period, deduplicate actual prefixes, not full patterns.
            passed.add(pattern if width >= 99 else pattern & prefix)
    return len(passed)


def main():
    nines, elevens = residue_sets(9), residue_sets(11)
    patterns = {sum(1 << i for i in range(99) if i % 9 in a and i % 11 in b)
                for a in nines for b in elevens}
    assert len(patterns)==3994
    counts = {str(w):count_unique(patterns,w) for w in (95,96,197,198,264,265)}
    assert counts == {'95':3615,'96':3630,'197':3630,'198':3630,'264':3630,'265':3632}
    print(json.dumps({'period_patterns':len(patterns),'unique_counts':counts,
                      'scope':'level 17, mod 9 and mod 11; unique masks only'},indent=2))


if __name__ == '__main__':
    main()
