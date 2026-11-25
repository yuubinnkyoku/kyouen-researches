#!/usr/bin/env python3
"""Independent geometry + terminal minimax verification for the n11 S6 WIN witness.

No precomputed verdict cache or external libraries.
Usage: python3 verify_s6_terminal.py ../input/s6-win-certificate.txt
Omitting --limit is required for a full proof; --limit is diagnostic only.
"""
import argparse
from functools import lru_cache
from itertools import combinations
from pathlib import Path

N = 11


def check(condition, message="invalid certificate"):
    """Runtime validation that remains active under python -O."""
    if not condition:
        raise ValueError(message)



def points(m):
    return [i for i in range(121) if m >> i & 1]


def circle(a, b, c, d):
    # Four lifted points are coplanar iff the original four are cocircular
    # or collinear. Both are forbidden by the standard complete-call rule.
    def vec(p):
        x, y = p % N, p // N
        return (x, y, x*x+y*y)
    z = vec(d)
    u = [x-y for x, y in zip(vec(a), z)]
    v = [x-y for x, y in zip(vec(b), z)]
    w = [x-y for x, y in zip(vec(c), z)]
    return (u[0]*(v[1]*w[2]-v[2]*w[1])
            -u[1]*(v[0]*w[2]-v[2]*w[0])
            +u[2]*(v[0]*w[1]-v[1]*w[0])) == 0


def safe(m):
    return all(not circle(*q) for q in combinations(points(m), 4))


def legal(m):
    p = points(m)
    triples = list(combinations(p, 3))
    return [x for x in range(121) if not (m >> x & 1)
            and all(not circle(a, b, c, x) for a, b, c in triples)]


def canonical(m):
    best = None
    for t in range(8):
        v = 0
        for p in points(m):
            x, y = p % 11, p // 11
            xx, yy = ((x,y),(10-y,x),(10-x,10-y),(y,10-x),
                      (10-x,y),(10-y,10-x),(x,10-y),(y,x))[t]
            v |= 1 << (11*yy+xx)
        best = v if best is None else min(best, v)
    return best


def children(m):
    return {canonical(m | (1 << p)) for p in legal(m)}


def next_player_wins_at_s10(m):
    check(m.bit_count() == 10 and safe(m))
    base = points(m)
    moves = legal(m)
    n = len(moves)
    check(n <= 31, f'terminal bitmask width exceeded: {n}')
    bad = set()
    for i, j in combinations(range(n), 2):
        if any(circle(a, b, moves[i], moves[j])
               for a, b in combinations(base, 2)):
            bad.add((1 << i) | (1 << j))
    for i, j, k in combinations(range(n), 3):
        e = (1 << i) | (1 << j) | (1 << k)
        if any(e & b == b for b in bad):
            continue
        if any(circle(a, moves[i], moves[j], moves[k]) for a in base):
            bad.add(e)
    for ids in combinations(range(n), 4):
        e = sum(1 << i for i in ids)
        if any(e & b == b for b in bad):
            continue
        if circle(*(moves[i] for i in ids)):
            bad.add(e)
    ban_by = [[] for _ in range(n)]
    for e in bad:
        for i in range(n):
            if e >> i & 1:
                ban_by[i].append(e ^ (1 << i))

    @lru_cache(None)
    def win(state):
        for i in range(n):
            bit = 1 << i
            if state & bit or any(state & b == b for b in ban_by[i]):
                continue
            if not win(state | bit):
                return True
        return False

    return win(0), win.cache_info().currsize


def verify(path, limit=None):
    lines = Path(path).read_text(encoding='utf-8').splitlines()
    check(lines[:2] == ['# n11-S6-WIN-terminal-v1', 'BOARD 11'])
    check(lines[-1] == 'END')
    check(len(lines) >= 6)
    tag, h = lines[2].split()
    check(tag == 'S6' and len(h) == 32)
    s6 = int(h, 16)
    check(s6.bit_count() == 6 and safe(s6) and canonical(s6) == s6)
    tag, num = lines[3].split()
    check(tag == 'S7_WITNESSES' and int(num) >= 1)
    n7 = int(num)
    idx = 4
    witnesses = set()
    all_s10 = set()
    s8_edges = 0
    for _ in range(n7):
        tag, h, count = lines[idx].split()
        idx += 1
        check(tag == 'S7' and len(h) == 32)
        s7 = int(h, 16)
        check(s7.bit_count() == 7 and safe(s7) and canonical(s7) == s7)
        check(s7 in children(s6) and s7 not in witnesses)
        witnesses.add(s7)
        expected = children(s7)
        check(int(count) == len(expected))
        actual = set()
        for _ in range(int(count)):
            tag, a, b = lines[idx].split()
            idx += 1
            check(tag == 'WIN8' and len(a) == len(b) == 32)
            s8, s9 = int(a, 16), int(b, 16)
            check(s8.bit_count() == 8 and s9.bit_count() == 9)
            check(safe(s8) and safe(s9))
            check(canonical(s8) == s8 and canonical(s9) == s9)
            check(s8 in expected and s8 not in actual)
            check(s9 in children(s8))
            actual.add(s8)
            all_s10.update(children(s9))
            s8_edges += 1
        check(actual == expected)
    check(idx == len(lines) - 1)
    targets = sorted(all_s10)
    if limit is not None:
        check(limit >= 0)
        targets = targets[:limit]
    states = 0
    for i, s10 in enumerate(targets, 1):
        win, visited = next_player_wins_at_s10(s10)
        check(win, f'S10 LOSS contradicts WIN witness: {s10:032x}')
        states += visited
        if i % 200 == 0:
            print(f'checked {i}/{len(all_s10)} S10 terminal roots', flush=True)
    label = 'PASS' if limit is None else 'PARTIAL-NOT-A-PROOF'
    print(f'{label} S6={s6:032x} WIN, S7={n7}, S8_edges={s8_edges}, '
          f'checked_S10={len(targets)}/{len(all_s10)}, '
          f'terminal_states={states}, empty=UNKNOWN')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('certificate', type=Path)
    ap.add_argument('--limit', type=int, default=None,
                    help='diagnostic sample only; omit for full proof')
    args = ap.parse_args()
    verify(args.certificate, args.limit)
