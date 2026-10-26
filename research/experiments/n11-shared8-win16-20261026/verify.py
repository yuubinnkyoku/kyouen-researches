#!/usr/bin/env python3
"""Independent 4x4 Bareiss integer geometry and terminal minimax."""
from functools import lru_cache
from itertools import combinations
from pathlib import Path

ROOT = '00020000000000821090200000000020'
S9 = '00020000000000821090200000400020'
HERE = Path(__file__).resolve().parent
S10 = (HERE / 's10-win16.keys').read_text('ascii').split()
PARENTS = (
    '00000000000000821090200000000020',
    '00020000000000821080200000000020',
)
XY = [(p % 11, p // 11) for p in range(121)]


def det4(p):
    m = [[XY[x][0], XY[x][1], XY[x][0]**2 + XY[x][1]**2, 1] for x in p]
    sign = 1
    prev = 1
    for k in range(3):
        if m[k][k] == 0:
            for j in range(k + 1, 4):
                if m[j][k]:
                    m[k], m[j] = m[j], m[k]
                    sign = -sign
                    break
            else:
                return 0
        pivot = m[k][k]
        for i in range(k + 1, 4):
            for j in range(k + 1, 4):
                q = m[i][j] * pivot - m[i][k] * m[k][j]
                assert q % prev == 0
                m[i][j] = q // prev
        for i in range(k + 1, 4):
            m[i][k] = 0
        prev = pivot
    return sign * m[3][3]


@lru_cache(maxsize=None)
def forbidden(p):
    return det4(p) == 0


def points(b):
    return tuple(i for i in range(121) if (b >> i) & 1)


def safe(b):
    return all(not forbidden(t) for t in combinations(points(b), 4))


def legal(b):
    pp = points(b)
    tri = list(combinations(pp, 3))
    return tuple(x for x in range(121) if not (b >> x) & 1
                 and all(not forbidden(tuple(sorted(t + (x,)))) for t in tri))


def canonical(b):
    pp = points(b)
    best = None
    for k in range(8):
        n = 0
        for p in pp:
            x, y = XY[p]
            q = [(x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                 (10-x, y), (10-y, 10-x), (x, 10-y), (y, x)][k]
            n |= 1 << (q[0] + 11 * q[1])
        if best is None or n < best:
            best = n
    return best


def children(b):
    return {canonical(b | (1 << p)) for p in legal(b)}


def solve10(b):
    base = points(b)
    moves = legal(b)
    n = len(moves)
    assert n <= 31
    bans = [[] for _ in range(n)]
    existing = []
    for count in (2, 3, 4):
        for comb in combinations(range(n), count):
            mask = sum(1 << i for i in comb)
            if any((mask & x) == x for x in existing):
                continue
            pp = tuple(moves[i] for i in comb)
            if any(forbidden(tuple(sorted(quad)))
                   for quad in combinations(base + pp, 4)
                   if sum(p in pp for p in quad) >= 2):
                existing.append(mask)
                for i in comb:
                    bans[i].append(mask ^ (1 << i))
    memo = {}

    def win(s):
        if s in memo:
            return memo[s]
        for i in range(n):
            if (s >> i) & 1 or any((s & v) == v for v in bans[i]):
                continue
            if not win(s | (1 << i)):
                memo[s] = True
                return True
        memo[s] = False
        return False

    return win(0), len(memo), n


def verify(leaves, root=ROOT, witness=S9, terminal=True):
    assert len(leaves) == len(set(leaves)) == 16
    assert all(len(h) == 32 for h in leaves)
    a = int(root, 16)
    w = int(witness, 16)
    assert len(points(a)) == 8 and len(points(w)) == 9
    assert safe(a) and safe(w)
    assert canonical(a) == a and canonical(w) == w and w in children(a)
    assert {int(h, 16) for h in leaves} == children(w)
    assert len(children(w)) == 16
    for p in PARENTS:
        b = int(p, 16)
        assert len(points(b)) == 7 and safe(b) and canonical(b) == b
        assert a in children(b)
    states = 0
    for h in leaves:
        b = int(h, 16)
        assert len(points(b)) == 10 and canonical(b) == b and safe(b)
        if terminal:
            ans, s, _ = solve10(b)
            assert ans, 'false S10 WIN: ' + h
            states += s
    if terminal:
        assert states == 914
    return {'s8': root, 's9': witness, 's10_leaves': len(leaves),
            'states': states if terminal else None, 'empty_board': 'UNKNOWN'}


if __name__ == '__main__':
    import sys
    print(verify(S10))
    if '--negative' in sys.argv:
        for bad, root, w in [
            (S10[1:], ROOT, S9),
            ([S10[0]] + S10[:-1], ROOT, S9),
            ([ROOT] + S10[1:], ROOT, S9),
            (S10, ROOT, ROOT),
        ]:
            try:
                verify(bad, root, w, terminal=False)
            except (AssertionError, ValueError):
                continue
            raise AssertionError('altered 4x4 certificate accepted')
        print('PASS four independent mutation rejections')
