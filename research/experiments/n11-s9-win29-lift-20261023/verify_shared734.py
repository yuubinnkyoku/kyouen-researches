#!/usr/bin/env python3
"""Independent Python 3x3 integer-geometry audit of 734 S10 WIN shared-D4 DAG.

No C++ verdicts, solver caches, or intermediate states are trusted. The 734
roots are regenerated from the 29 S9 WIN positions, not taken from C++ output.
"""
from pathlib import Path
import argparse
import sys
P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'n11-four-s8-shared-tt-20261023'))
sys.path.insert(0, str(P.parent / 'n11-four-s8-joint-terminal52-20261023'))
from itertools import combinations
from terminal_geometry import children, safe
from fastgeom import canonical, legal, forbidden, points


def prep(m):
    # Algebraic three-point circle equation, not C++'s 4x4 determinant.
    if m.bit_count() != 10 or not safe(m) or canonical(m) != m:
        raise ValueError('bad S10 root')
    base = list(points(m))
    moves = legal(m)
    n = len(moves)
    if n > 63:
        raise ValueError('more than 63 legal moves')
    bad = []
    for i, j in combinations(range(n), 2):
        if any((forbidden(a, b, moves[i]) >> moves[j]) & 1 for a, b in combinations(base, 2)):
            bad.append((1 << i) | (1 << j))
    for i, j, k in combinations(range(n), 3):
        mask = (1 << i) | (1 << j) | (1 << k)
        if any(mask & b == b for b in bad):
            continue
        if any((forbidden(a, moves[i], moves[j]) >> moves[k]) & 1 for a in base):
            bad.append(mask)
    for i, j, k, l in combinations(range(n), 4):
        mask = (1 << i) | (1 << j) | (1 << k) | (1 << l)
        if any(mask & b == b for b in bad):
            continue
        if (forbidden(moves[i], moves[j], moves[k]) >> moves[l]) & 1:
            bad.append(mask)
    blockers = [[] for _ in range(n)]
    for b in bad:
        for i in range(n):
            if b >> i & 1:
                blockers[i].append(b ^ (1 << i))
    return moves, blockers, None


def check(condition, message):
    if not condition:
        raise ValueError(message)


def run(keys_path=None):
    s9 = [int(s, 16) for s in (P / 's9-win29.keys').read_text().split()]
    check(len(s9) == len(set(s9)) == 29, 'bad S9 list')
    for m in s9:
        check(m.bit_count() == 9 and safe(m) and canonical(m) == m, 'bad S9 root')
    s10 = sorted(set().union(*(children(m) for m in s9)))
    check(len(s10) == 734, 'wrong S10 boundary')
    if keys_path is not None:
        given = [int(s, 16) for s in Path(keys_path).read_text().split()]
        check(given == s10, 'S10 key file differs from regenerated boundary')
    # Descending hexadecimal order is fixed; move priority uses pairs and triples.
    memo = {}
    lookups = hits = edges = 0
    for m in reversed(s10):
        moves, blockers, _ = prep(m)
        def score(i):
            pair = sum(b.bit_count() == 1 for b in blockers[i])
            triple = sum(b.bit_count() == 2 for b in blockers[i])
            dist = abs(moves[i] % 11 - 5) + abs(moves[i] // 11 - 5)
            return 100000 * pair + 1000 * triple - dist
        order = sorted(range(len(moves)), key=lambda i: (-score(i), moves[i]))

        def solve(mask, board):
            nonlocal lookups, hits, edges
            key = canonical(board)
            lookups += 1
            if key in memo:
                hits += 1
                return memo[key]
            for i in order:
                bit = 1 << i
                if mask & bit or any((mask & b) == b for b in blockers[i]):
                    continue
                edges += 1
                if not solve(mask | bit, board | (1 << moves[i])):
                    memo[key] = True
                    return True
            memo[key] = False
            return False
        check(solve(0, m), f'LOSS contradicts claimed S9 WIN: {m:032x}')
    result = (len(memo), lookups, hits, edges)
    check(result == (55010, 94068, 39058, 93334), f'C++ mismatch {result}')
    print('PASS S9=29 S10=734 WIN=734 states=%d lookups=%d hits=%d edges=%d empty=UNKNOWN' % result)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--keys', type=Path)
    run(parser.parse_args().keys)
