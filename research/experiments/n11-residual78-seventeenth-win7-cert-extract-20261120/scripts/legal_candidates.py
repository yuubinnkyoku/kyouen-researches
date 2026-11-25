#!/usr/bin/env python3
"""Independent non-degenerate candidate enumerator for an 11x11 S6 child / S7 root.

A candidate cell p is legal iff placing the new stone on p keeps the stone set
free of 4-concyclic subsets (exact integer Bareiss 4x4 determinants of
[x^2+y^2, x, y, 1] rows; zero determinant = concyclic or collinear quadruple).
Validated bit-exact against the published candidate lists of the class2-lane
cost-58 (58), cost-61-c (61) and cost-63 (63) sweeps and the class4-lane
cost-74a/b sweeps (74/74) on 2026-11-14, and against the engine loser-mobility
of the six cost-74b 7-stone WIN7 roots (50/55/57/58/63/64) on 2026-11-14.

2026-11-14 bugfix: the triple enumeration was hardcoded to
itertools.combinations(range(6), 3), so on a 7-stone root it never inspected
triples containing the last occupied stone and over-reported legal candidates
(e.g. 74 instead of the true 57 for root 00000000020000003821000080000000).
It is now combinations(range(len(st)), 3), correct for any stone count.
6-stone child enumerations are unchanged by this fix.
"""
import itertools
import sys


def cells(hexstr):
    v = int(hexstr, 16)
    return [i for i in range(121) if (v >> i) & 1]


def det4(m):
    a = [row[:] for row in m]
    prev = 1
    for k in range(3):
        if a[k][k] == 0:
            for r in range(k + 1, 4):
                if a[r][k] != 0:
                    a[k], a[r] = a[r], a[k]
                    break
            else:
                return 0
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                a[i][j] = (a[i][j] * a[k][k] - a[i][k] * a[k][j]) // prev
        prev = a[k][k]
    return a[3][3]


def legal_candidates(hexstr):
    st = cells(hexstr)
    rows = []
    for i in st:
        x, y = i % 11, i // 11
        rows.append([x * x + y * y, x, y, 1])
    out = []
    for p in range(121):
        if p in st:
            continue
        px, py = p % 11, p // 11
        prow = [px * px + py * py, px, py, 1]
        unsafe = False
        for (i, j, k) in itertools.combinations(range(len(st)), 3):
            if det4([rows[i], rows[j], rows[k], prow]) == 0:
                unsafe = True
                break
        if not unsafe:
            out.append(p)
    return st, out


if __name__ == '__main__':
    for hexstr in sys.argv[1:]:
        st, cand = legal_candidates(hexstr)
        print(hexstr, 'occupied', len(st), 'legal', len(cand))
        print(','.join(map(str, cand)))
