#!/usr/bin/env python3
"""Independent exact lifted-determinant audit; no pair-sum circle generation."""
from itertools import combinations
from fractions import Fraction as F
from collections import Counter
from pathlib import Path


def det4(rows):
    m = [list(row) for row in rows]
    prev, sign = 1, 1
    for k in range(3):
        p = next((p for p in range(k, 4) if m[p][k]), None)
        if p is None:
            return 0
        if p != k:
            m[p], m[k] = m[k], m[p]
            sign = -sign
        pivot = m[k][k]
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                t = m[i][j] * pivot - m[i][k] * m[k][j]
                assert t % prev == 0
                m[i][j] = t // prev
            m[i][k] = 0
        prev = pivot
    return sign * m[3][3]


def audit(U, V):
    u, v = 1 / U, 1 / V
    from math import lcm
    L = lcm(u.denominator, v.denominator)
    z = (0, int(u * L), int((u + v) * L))
    D = int((u + v) * L * L)
    pts = [(D * x * x + z[y] ** 2, x, z[y], 1)
           for y in range(3) for x in range(5)]
    edges = []
    for subset in combinations(range(15), 6):
        if all(det4([pts[i] for i in quad]) == 0
               for quad in combinations(subset, 4)):
            edges.append(sum(1 << i for i in subset))
    safe = [False] * (1 << 15)
    safe[0] = True
    for mask in range(1, 1 << 15):
        safe[mask] = safe[mask & (mask - 1)] and not any(
            mask & edge == edge for edge in edges)
    grundy = [0] * (1 << 15)
    terminal = Counter()
    for mask in range((1 << 15) - 1, -1, -1):
        if not safe[mask]:
            continue
        children = [grundy[mask | (1 << i)] for i in range(15)
                    if not (mask >> i & 1) and safe[mask | (1 << i)]]
        if not children:
            terminal[mask.bit_count()] += 1
        seen = set(children)
        while grundy[mask] in seen:
            grundy[mask] += 1
    return len(edges), sum(safe), grundy[0], max(grundy), ''.join(
        f'{k}:{v},' for k, v in sorted(terminal.items()))


def main():
    cases = Path(__file__).resolve().parent.parent / 'output/q36_real_row_gap_m5_cases.tsv'
    n = 0
    for line in cases.read_text().splitlines():
        name, un, ud, vn, vd, circles, safe, root, maxg, terminal = line.split()
        actual = audit(F(int(un), int(ud)), F(int(vn), int(vd)))
        expected = int(circles), int(safe), int(root), int(maxg), terminal
        assert actual == expected, (name, actual, expected)
        print('PASS', name, actual)
        n += 1
    assert n == 13
    print('PASS all 13 determinant cases')


if __name__ == '__main__':
    main()
