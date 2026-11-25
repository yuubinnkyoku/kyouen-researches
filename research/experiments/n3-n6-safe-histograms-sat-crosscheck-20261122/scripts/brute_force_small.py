#!/usr/bin/env python3
"""brute_force_small.py — COMPLETELY independent third system for n=3 and n=4.

Enumerates ALL 2^(n^2) subsets of the board (no DFS pruning, no cov state,
no shared code with either enumerator):

  geometry: own Leibniz determinant routine (4 points are concyclic or
  collinear iff det[[x, y, x^2+y^2, 1]] == 0), computed over ALL
  C(n^2, 4) combinations directly — then cross-checked against the
  catalog text file for identical quartet content.

  safety:     S safe iff no forbidden quartet q satisfies q subset of S.
  maximality: S maximal-safe iff S safe and for every empty cell e there is
  a forbidden quartet q with e in q and (q \\ {e}) subset of S.

Outputs JSON with the maximal spectrum (count per k), the safe-subset
histogram, the full maximal config list, and the own-vs-catalog quartet
cross-check. Exit 1 on any quartet cross-check failure.
"""
import itertools
import json
import sys


def concyclic_or_collinear(pts):
    """det[[x, y, x^2+y^2, 1]] == 0  <=>  the four points are concyclic
    or collinear (the standard kyouen q=4 forbidden test).
    Expansion along the all-ones column: det = -M0 + M1 - M2 + M3 where
    Mi is the 3x3 determinant of [[x, y, x^2+y^2]] rows, deleting row i."""
    def d3(a, b, c):
        return (a[0] * (b[1] * c[2] - b[2] * c[1])
                - a[1] * (b[0] * c[2] - b[2] * c[0])
                + a[2] * (b[0] * c[1] - b[1] * c[0]))
    rows = [(x, y, x * x + y * y) for (x, y) in pts]
    det = (d3(rows[1], rows[2], rows[3])
           - d3(rows[0], rows[2], rows[3])
           + d3(rows[0], rows[1], rows[3])
           - d3(rows[0], rows[1], rows[2]))
    return det == 0


def main():
    n = int(sys.argv[1])
    catalog_path = sys.argv[2]
    out_path = sys.argv[3]
    N = n * n
    coords = [(i % n, i // n) for i in range(N)]
    quarts = sorted(
        tuple(sorted(c))
        for c in itertools.combinations(range(N), 4)
        if concyclic_or_collinear([coords[c] for c in c])
    )
    cat = []
    for line in open(catalog_path, encoding='utf8'):
        line = line.strip()
        if line and not line.startswith('n='):
            cat.append(tuple(int(t) for t in line.split()))
    cat.sort()
    quarts_eq_catalog = (quarts == cat)

    quartet_masks = [sum(1 << c for c in q) for q in quarts]
    cell_quarts = [[] for _ in range(N)]
    for q in quarts:
        for c in q:
            cell_quarts[c].append(q)
    cell_targets = []
    for e in range(N):
        lst = []
        for q in cell_quarts[e]:
            om = 0
            for c in q:
                if c != e:
                    om |= 1 << c
            lst.append(om)
        cell_targets.append(lst)

    configs_by_k = {}
    safe_subsets_by_size = {}
    maximal_cfgs = []
    for S in range(1 << N):
        unsafe = False
        for m in quartet_masks:
            if (S & m) == m:
                unsafe = True
                break
        if unsafe:
            continue
        size = bin(S).count('1')
        safe_subsets_by_size[size] = safe_subsets_by_size.get(size, 0) + 1
        maximal = True
        for e in range(N):
            if S & (1 << e):
                continue
            hit = False
            for om in cell_targets[e]:
                if om & ~S == 0:
                    hit = True
                    break
            if not hit:
                maximal = False
                break
        if maximal:
            configs_by_k[size] = configs_by_k.get(size, 0) + 1
            maximal_cfgs.append(sorted(c for c in range(N) if S & (1 << c)))
    maximal_cfgs.sort()
    out = {
        'n': n,
        'quartets_owned_impl': len(quarts),
        'quartets_equal_to_catalog_file': quarts_eq_catalog,
        'maximal_spectrum': dict(sorted(configs_by_k.items())),
        'maximal_total': sum(configs_by_k.values()),
        'safe_subset_histogram': dict(sorted((k, v) for k, v in
                                             safe_subsets_by_size.items())),
        'safe_total': sum(safe_subsets_by_size.values()),
        'max_safe_size': max(safe_subsets_by_size),
        'num_maximal_cfgs_listed': len(maximal_cfgs),
    }
    with open(out_path, 'w') as f:
        json.dump(out, f, indent=1)
    with open(out_path + '.configs.csv', 'w') as f:
        for s in maximal_cfgs:
            f.write(','.join(map(str, s)) + '\n')
    print(json.dumps(out))
    if not quarts_eq_catalog:
        sys.exit(1)


if __name__ == '__main__':
    main()
