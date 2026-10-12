#!/usr/bin/env python3
"""Exact independent check of the minimal mod-27 obstruction in F(9)=43.

The nine compressed row indices surviving the earlier moduli for g=2 are
(0,2,4,9,10,11,16,18,20). The original F(9) proof obtains this list
from exhaustive intersections of moduli 9,11,7,49,19,23,43.
"""
from itertools import combinations

P = 27
ROWS = (0, 2, 4, 9, 10, 11, 16, 18, 20)
CORE = (0, 2, 4, 9, 10, 18)
SQUARES = {x*x % P for x in range(P)}


def possible_discriminant(rows):
    return any(all((d-4*a*i-16*i*i) % P in SQUARES for i in rows)
               for a in range(P) for d in range(P))


def possible_center(rows):
    # g=2, a=2c, n=d+c^2: independent completed-square form.
    return any(all((n-(4*i+c)**2) % P in SQUARES for i in rows)
               for c in range(P) for n in range(P))


def main():
    counts = {}
    for size in range(1, len(ROWS)+1):
        bad = 0
        for subset in combinations(ROWS, size):
            direct = possible_discriminant(subset)
            center = possible_center(subset)
            assert direct == center, (subset, direct, center)
            bad += not direct
        counts[size] = bad
    assert counts == {1:0, 2:0, 3:0, 4:0, 5:0,
                      6:18, 7:27, 8:9, 9:1}, counts
    assert not possible_discriminant(CORE)
    assert all(possible_discriminant(s) for s in combinations(CORE, 5))
    print('mod=27 g=2 row_indices=', ROWS)
    print('infeasible_subset_counts_by_size=', counts)
    print('minimal_infeasible_core=', CORE)
    print('PASS: 18 minimal six-row obstructions; none with <=5 rows')


if __name__ == '__main__':
    main()
