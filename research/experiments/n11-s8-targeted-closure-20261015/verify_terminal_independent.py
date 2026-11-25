#!/usr/bin/env python3
"""Independent 4x4 integer determinant verification of an S8 LOSS certificate.

Does not read stored verdicts, df-pn values, or any cached terminal outcomes.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations
from pathlib import Path
import sys

N = 11
COORDS = [(i % N, i // N) for i in range(N * N)]
ROWS = [(x, y, x * x + y * y, 1) for x, y in COORDS]


def det4(indices):
    # Fraction-free Bareiss elimination of the 4x4 circle determinant.
    a = [list(ROWS[i]) for i in indices]
    sign, prev = 1, 1
    for k in range(3):
        if a[k][k] == 0:
            r = next((r for r in range(k + 1, 4) if a[r][k]), None)
            if r is None:
                return 0
            a[k], a[r] = a[r], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                num = a[i][j] * pivot - a[i][k] * a[k][j]
                assert num % prev == 0
                a[i][j] = num // prev
            a[i][k] = 0
        prev = pivot
    return sign * a[3][3]


@lru_cache(maxsize=100000)
def forbidden(a, b, c, d):
    return det4((a, b, c, d)) == 0


def points(mask):
    return [i for i in range(N * N) if (mask >> i) & 1]


def transform(i, t):
    x, y = COORDS[i]
    return [(x, y), (10 - y, x), (10 - x, 10 - y), (y, 10 - x),
            (10 - x, y), (10 - y, 10 - x), (x, 10 - y), (y, x)][t]


def canonical(mask):
    pp = points(mask)
    return min(sum(1 << (11 * y + x) for x, y in
                   (transform(p, t) for p in pp)) for t in range(8))


def legal(mask):
    pp = points(mask)
    triples = list(combinations(pp, 3))
    return [i for i in range(N * N) if not (mask >> i) & 1
            and not any(forbidden(*tri, i) for tri in triples)]


def children(mask):
    return {canonical(mask | (1 << p)) for p in legal(mask)}


def solve10(mask):
    base, moves = points(mask), legal(mask)
    n = len(moves)
    assert n <= 31
    bad = []
    for i, j in combinations(range(n), 2):
        if any(forbidden(a, b, moves[i], moves[j])
               for a, b in combinations(base, 2)):
            bad.append((1 << i) | (1 << j))
    for i, j, k in combinations(range(n), 3):
        bits = (1 << i) | (1 << j) | (1 << k)
        if not any((bits & v) == v for v in bad) and any(
                forbidden(a, moves[i], moves[j], moves[k]) for a in base):
            bad.append(bits)
    for i, j, k, l in combinations(range(n), 4):
        bits = (1 << i) | (1 << j) | (1 << k) | (1 << l)
        if not any((bits & v) == v for v in bad) and forbidden(
                moves[i], moves[j], moves[k], moves[l]):
            bad.append(bits)
    bans = [[] for _ in range(n)]
    for bits in bad:
        for i in range(n):
            if bits & (1 << i):
                bans[i].append(bits ^ (1 << i))

    @lru_cache(maxsize=None)
    def win(state):
        for i in range(n):
            bit = 1 << i
            if state & bit or any((state & v) == v for v in bans[i]):
                continue
            if not win(state | bit):
                return True
        return False

    outcome = win(0)
    return outcome, win.cache_info().currsize, n


def verify(text, verbose=True):
    assert text.startswith('# n11-S8-LOSS-global-terminal-v1\n')
    lines = [x for x in text.splitlines() if x and not x.startswith('#')]
    assert len(lines) == 20 and lines[0] == 'BOARD 11' and lines[-1] == 'END'
    assert lines[1].startswith('ROOT ')
    root = int(lines[1][5:], 16)
    assert len(points(root)) == 8 and canonical(root) == root
    assert all(not forbidden(*q) for q in combinations(points(root), 4))
    assert all(x.startswith('LEAF ') and len(x) == 37 for x in lines[2:-1])
    leaf_keys = [x[5:] for x in lines[2:-1]]
    assert len(leaf_keys) == 17 and len(set(leaf_keys)) == 17
    leaves = {int(x, 16) for x in leaf_keys}
    obligations = children(root)
    assert len(obligations) == 31
    boundary = set().union(*(children(s9) for s9 in obligations))
    assert all(x in boundary for x in leaves)
    assert all(any(x in leaves for x in children(s9)) for s9 in obligations)
    total = 0
    for h in leaf_keys:
        b = int(h, 16)
        assert len(points(b)) == 10 and canonical(b) == b
        assert all(not forbidden(*q) for q in combinations(points(b), 4))
        outcome, states, n = solve10(b)
        assert outcome is False, (h, outcome)
        total += states
        if verbose:
            print(h, 'LOSS', n, states)
    assert total == 12241, total
    print('PASS 17 LOSS leaves; 31/31 obligations; states', total)


def negative_tests(text):
    lines = text.splitlines()
    idx = next(i for i, x in enumerate(lines) if x.startswith('LEAF '))
    bad = [
        '\n'.join(lines[:idx] + lines[idx + 1:]) + '\n',
        '\n'.join(lines[:idx + 1] + [lines[idx]] + lines[idx + 2:]) + '\n',
        text.replace('BOARD 11', 'BOARD 10'),
        text.replace('ROOT 00000000000040001000044400830000',
                     'ROOT 00000000000040001000044400830001')
    ]
    for altered in bad:
        try:
            verify(altered, verbose=False)
        except (AssertionError, ValueError):
            continue
        raise AssertionError('mutated certificate accepted')
    print('PASS four certificate mutations rejected')


if __name__ == '__main__':
    path = Path(__file__).with_name('s8-loss-terminal.cert')
    text = path.read_text(encoding='utf-8')
    verify(text)
    if '--negative' in sys.argv:
        negative_tests(text)
