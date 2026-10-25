#!/usr/bin/env python3
"""Standalone, cache-free 4x4 integer-geometry audit of six N11 S9 AND roots."""
import argparse
from functools import lru_cache
from itertools import combinations
from pathlib import Path

HERE = Path(__file__).resolve().parent
FULL = (1 << 121) - 1


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def points(s):
    return [p for p in range(121) if s >> p & 1]


def det4(a, b, c, d):
    rows = [[p % 11, p // 11, (p % 11)**2 + (p // 11)**2, 1]
            for p in (a, b, c, d)]
    sign, previous = 1, 1
    for k in range(3):
        if rows[k][k] == 0:
            pivot_row = next((j for j in range(k + 1, 4)
                              if rows[j][k]), None)
            if pivot_row is None:
                return 0
            rows[k], rows[pivot_row] = rows[pivot_row], rows[k]
            sign = -sign
        pivot = rows[k][k]
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                numerator = rows[i][j]*pivot - rows[i][k]*rows[k][j]
                need(numerator % previous == 0, 'non-exact Bareiss division')
                rows[i][j] = numerator // previous
            rows[i][k] = 0
        previous = pivot
    return sign * rows[3][3]


@lru_cache(None)
def forbidden(triple):
    a, b, c = triple
    return sum(1 << p for p in range(121)
               if p not in triple and det4(a, b, c, p) == 0)


def safe(s):
    return not any(det4(*quad) == 0 for quad in combinations(points(s), 4))


def legal(s):
    blocked = s
    for triple in combinations(points(s), 3):
        blocked |= forbidden(triple)
    return FULL & ~blocked


def canonical(s):
    ps = points(s)
    best = FULL
    for swap in (False, True):
        for flip_x in (False, True):
            for flip_y in (False, True):
                image = 0
                for p in ps:
                    x, y = p % 11, p // 11
                    if swap:
                        x, y = y, x
                    if flip_x:
                        x = 10 - x
                    if flip_y:
                        y = 10 - y
                    image |= 1 << (11*y + x)
                best = min(best, image)
    return best


def solve(root):
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
    verdict = visit(root)
    return verdict, len(memo)


def read_keys(filename, expected, stones):
    lines = (HERE / filename).read_text(encoding='utf-8').splitlines()
    need(len(lines) == expected and lines == sorted(set(lines)),
         f'invalid count/order/duplicate: {filename}')
    need(all(len(x) == 32 and set(x) <= set('0123456789abcdef')
             for x in lines), f'invalid key syntax: {filename}')
    values = {int(x, 16) for x in lines}
    need(all(x.bit_count() == stones and safe(x) and canonical(x) == x
             for x in values), f'unsafe/noncanonical: {filename}')
    return values


def check_boundary(roots, leaves, parents):
    actual_leaves = set()
    actual_parents = set()
    for root in roots:
        actual_leaves.update(canonical(root | (1 << p))
                             for p in points(legal(root)))
        actual_parents.update(canonical(root ^ (1 << p))
                              for p in points(root))
    need(actual_leaves == leaves, 'incomplete S9 AND boundary')
    need(actual_parents == parents, 'incorrect S8 OR parent union')
    for parent in parents:
        need(any(canonical(parent | (1 << p)) in roots
                 for p in points(legal(parent))),
             'missing legal S8-to-S9 witness')


def verify(cpp_tsv=None, negative=False):
    roots = read_keys('s9-roots.keys', 6, 9)
    leaves = read_keys('s10-win.keys', 106, 10)
    parents = read_keys('s8-win.keys', 54, 8)
    check_boundary(roots, leaves, parents)
    frozen = HERE.parent / 'n11-targeted-terminal-lift-20261015' / 'data'
    frozen_win8 = set((frozen / 'lifted_s8_win_51571.txt').read_text().split())
    frozen_loss8 = set((frozen / 'all_s8_loss_294.txt').read_text().split())
    frozen_win9 = set((frozen / 'lifted_s9_win_51571.txt').read_text().split())
    need((len(frozen_win8), len(frozen_loss8), len(frozen_win9)) ==
         (13501, 294, 1611), 'frozen comparison baseline changed')
    parent_keys = {f'{x:032x}' for x in parents}
    root_keys = {f'{x:032x}' for x in roots}
    need(not parent_keys & frozen_loss8, 'S8 WIN/LOSS conflict')
    need(not parent_keys & frozen_win8 and not root_keys & frozen_win9,
         'claimed new local class already in frozen baseline')
    if negative:
        for bad_leaves, bad_parents in (
            (leaves - {min(leaves)}, parents),
            (leaves, parents - {min(parents)}),
            (leaves | {min(roots)}, parents),
        ):
            try:
                check_boundary(roots, bad_leaves, bad_parents)
            except ValueError:
                pass
            else:
                raise ValueError('mutated boundary accepted')
    states = 0
    legal_counts = {}
    for leaf in sorted(leaves):
        verdict, visited = solve(leaf)
        need(verdict, f'non-WIN S10 terminal leaf: {leaf:032x}')
        states += visited
        legal_counts[f'{leaf:032x}'] = legal(leaf).bit_count()
    need(states == 12604, 'independent terminal state count changed')
    for root in roots:
        need(not solve(root)[0], f'non-LOSS-to-move S9: {root:032x}')
    if cpp_tsv is not None:
        rows = {}
        for line in cpp_tsv.read_text(encoding='utf-8').splitlines():
            fields = line.split()
            need(len(fields) == 4, 'malformed C++ row')
            key, verdict, visited, moves = fields
            need(key not in rows and verdict == 'WIN' and int(visited) > 0,
                 'duplicate or non-WIN C++ leaf')
            rows[key] = int(moves)
        need(rows == legal_counts, 'C++/Python leaf or legal-move mismatch')
    print('VERIFIED 6 S9 FIRST_WIN, 106 S10 terminal WIN classes, '
          '54 S8 WIN parents, 12604 independent 4x4 Python states; '
          'empty=UNKNOWN')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--cpp-tsv', type=Path)
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    verify(args.cpp_tsv, args.negative)
