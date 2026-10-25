#!/usr/bin/env python3
"""Independent cache-free terminal verifier for one S9 AND certificate."""
import argparse
from functools import lru_cache
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = int('00000000040c00011000010a00001000', 16)
FULL = (1 << 121) - 1

def need(ok, msg):
    if not ok:
        raise ValueError(msg)

def points(s):
    return [p for p in range(121) if s >> p & 1]

def on_circle(a, b, c, d):
    x0, y0 = d % 11, d // 11
    rows = []
    for p in (a, b, c):
        x, y = p % 11, p // 11
        rows.append((x*x + y*y - x0*x0 - y0*y0, x-x0, y-y0))
    a, b, c = rows
    return (a[0]*(b[1]*c[2]-b[2]*c[1])
            - a[1]*(b[0]*c[2]-b[2]*c[0])
            + a[2]*(b[0]*c[1]-b[1]*c[0])) == 0

def safe(s):
    return not any(on_circle(*q) for q in combinations(points(s), 4))

@lru_cache(None)
def forbidden_after_three(triple):
    a, b, c = triple
    return sum(1 << p for p in range(121)
               if p not in triple and on_circle(a, b, c, p))

def legal(s):
    blocked = s
    for triple in combinations(points(s), 3):
        blocked |= forbidden_after_three(triple)
    return FULL & ~blocked

def canonical(s):
    images = []
    for swap in (False, True):
        for flipx in (False, True):
            for flipy in (False, True):
                out = 0
                for p in points(s):
                    x, y = p % 11, p // 11
                    if swap:
                        x, y = y, x
                    if flipx:
                        x = 10 - x
                    if flipy:
                        y = 10 - y
                    out |= 1 << (11*y + x)
                images.append(out)
    return min(images)

def solve(s):
    memo = {}
    def visit(board):
        if board in memo:
            return memo[board]
        moves = legal(board)
        while moves:
            bit = moves & -moves
            moves -= bit
            if not visit(board | bit):
                memo[board] = True
                return True
        memo[board] = False
        return False
    result = visit(s)
    return result, len(memo)

def read_keys(path, n, stones):
    lines = path.read_text(encoding='utf-8').splitlines()
    need(len(lines) == n and lines == sorted(set(lines)),
         'wrong count/order/duplicate in ' + str(path))
    need(all(len(s) == 32 and set(s) <= set('0123456789abcdef')
             for s in lines), 'invalid hexadecimal key')
    vals = {int(s, 16) for s in lines}
    need(all(s.bit_count() == stones and safe(s) and canonical(s) == s
             for s in vals), 'unsafe/noncanonical key')
    return vals

def verify(cpp_tsv=None, negative=False):
    need(ROOT.bit_count() == 9 and safe(ROOT) and canonical(ROOT) == ROOT,
         'invalid nine-stone root')
    leaves = read_keys(HERE / 's10-win18.keys', 18, 10)
    parents = read_keys(HERE / 's8-win9.keys', 9, 8)
    moves = legal(ROOT)
    actual = set()
    while moves:
        bit = moves & -moves
        moves -= bit
        actual.add(canonical(ROOT | bit))
    need(actual == leaves, 'S9 universal boundary incomplete')
    actual_parents = {canonical(ROOT ^ (1 << p)) for p in points(ROOT)}
    need(actual_parents == parents, 'S8 parent list incomplete')
    for p in parents:
        # A canonical S8 parent may be a rotated/reflected version of the
        # actual subset of ROOT.  Enumerate all legal moves of that parent,
        # not merely the coordinates occupied by the untransformed ROOT.
        allowed = legal(p)
        need(any(canonical(p | (1 << v)) == ROOT for v in range(121)
                 if allowed >> v & 1), 'invalid S8-to-S9 witness')
    move_counts = {}
    states = 0
    for s in sorted(leaves):
        verdict, n = solve(s)
        need(verdict, 'S10 not WIN to move: %032x' % s)
        move_counts['%032x' % s] = legal(s).bit_count()
        states += n
    need(not solve(ROOT)[0], 'S9 not LOSS to move')
    need(states == 1192, 'terminal search-state count changed')
    if cpp_tsv is not None:
        rows = {}
        for line in cpp_tsv.read_text(encoding='utf-8').splitlines():
            parts = line.split()
            need(len(parts) == 4, 'malformed C++ result')
            key, verdict, count, moves = parts
            need(key not in rows and verdict == 'WIN' and int(count) > 0,
                 'duplicate or non-WIN C++ result')
            rows[key] = int(moves)
        need(rows == move_counts, 'C++/Python outcome or legal-move mismatch')
        if negative:
            def matches(items):
                return items == move_counts
            need(not matches(dict(list(rows.items())[:-1])),
                 'missing C++ child accepted')
            corrupt = dict(rows)
            first = next(iter(corrupt))
            corrupt[first] += 1
            need(not matches(corrupt), 'tampered C++ move count accepted')
    print('VERIFIED S9 FIRST_WIN, 18/18 terminal S10 WIN, 9 S8 WIN parents, '
          '1192 independent Python leaf states; empty=UNKNOWN')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cpp-tsv', type=Path)
    ap.add_argument('--negative', action='store_true')
    args = ap.parse_args()
    verify(args.cpp_tsv, args.negative)
