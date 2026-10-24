#!/usr/bin/env python3
"""Independent 4x4 integer-determinant and terminal-game verifier for one S9 certificate.

Does not read S10 verdict caches or the JavaScript verifier.
"""
from __future__ import annotations
import argparse
import itertools
from pathlib import Path

ROOT = '00000100110002001042100000000010'
N = 121
XY = [(i % 11, i // 11) for i in range(N)]
TRANSFORMS = [
    [11 * yy + xx for x, y in XY for xx, yy in [f(x, y)]]
    for f in (
        lambda x, y: (x, y), lambda x, y: (10-y, x),
        lambda x, y: (10-x, 10-y), lambda x, y: (y, 10-x),
        lambda x, y: (10-x, y), lambda x, y: (10-y, 10-x),
        lambda x, y: (x, 10-y), lambda x, y: (y, x),
    )
]


def points(b: int) -> list[int]:
    return [i for i in range(N) if b >> i & 1]


def canonical(b: int) -> int:
    ps = points(b)
    return min(sum(1 << tr[p] for p in ps) for tr in TRANSFORMS)


def det4(p: tuple[int, int, int, int]) -> int:
    a = [[XY[q][0], XY[q][1], XY[q][0]**2 + XY[q][1]**2, 1] for q in p]
    sign = 1
    prev = 1
    for k in range(3):
        if a[k][k] == 0:
            pivot = next((r for r in range(k+1, 4) if a[r][k]), None)
            if pivot is None:
                return 0
            a[k], a[pivot] = a[pivot], a[k]
            sign = -sign
        v = a[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                z = a[i][j]*v - a[i][k]*a[k][j]
                assert z % prev == 0
                a[i][j] = z // prev
        for i in range(k+1, 4):
            a[i][k] = 0
        prev = v
    return sign*a[3][3]


def safe(b: int) -> bool:
    return all(det4(t) for t in itertools.combinations(points(b), 4))


def legal(b: int) -> list[int]:
    ps = points(b)
    triples = list(itertools.combinations(ps, 3))
    return [p for p in range(N) if not (b >> p & 1)
            and all(det4((*t, p)) for t in triples)]


def children(b: int) -> set[str]:
    return {f'{canonical(b | (1 << p)):032x}' for p in legal(b)}


def terminal_win(h: str) -> tuple[bool, int, int]:
    b = int(h, 16)
    assert len(points(b)) == 10 and canonical(b) == b and safe(b)
    base = points(b)
    moves = legal(b)
    n = len(moves)
    # A safe 10-stone base makes every forbidden extension contain >=2 new stones.
    forbidden = []
    for i, j in itertools.combinations(range(n), 2):
        if any(det4((a, c, moves[i], moves[j])) == 0
               for a, c in itertools.combinations(base, 2)):
            forbidden.append((1 << i) | (1 << j))
    for i, j, k in itertools.combinations(range(n), 3):
        mask = (1 << i) | (1 << j) | (1 << k)
        if not any(mask & bad == bad for bad in forbidden) and any(
            det4((a, moves[i], moves[j], moves[k])) == 0 for a in base
        ):
            forbidden.append(mask)
    for i, j, k, l in itertools.combinations(range(n), 4):
        mask = (1 << i) | (1 << j) | (1 << k) | (1 << l)
        if not any(mask & bad == bad for bad in forbidden) and det4(
            (moves[i], moves[j], moves[k], moves[l])
        ) == 0:
            forbidden.append(mask)
    bans = [[] for _ in range(n)]
    for mask in forbidden:
        for i in range(n):
            if mask >> i & 1:
                bans[i].append(mask ^ (1 << i))
    memo = {}
    def win(mask: int) -> bool:
        if mask in memo:
            return memo[mask]
        for i in range(n):
            bit = 1 << i
            if mask & bit or any(mask & bad == bad for bad in bans[i]):
                continue
            if not win(mask | bit):
                memo[mask] = True
                return True
        memo[mask] = False
        return False
    return win(0), len(memo), n


def verify(text: str, terminal: bool = True) -> dict:
    lines = text.strip().splitlines()
    assert len(lines) == 21
    assert lines[:4] == ['# n11-S9-WIN-terminal-v1', 'BOARD 11',
                         'S9 '+ROOT, 'S10_WIN_LEAVES 16']
    assert lines[-1] == 'END'
    assert all(line.startswith('LEAF ') and len(line) == 37 for line in lines[4:-1])
    leaves = [line[5:] for line in lines[4:-1]]
    assert len(leaves) == len(set(leaves)) == 16
    b = int(ROOT, 16)
    assert len(points(b)) == 9 and canonical(b) == b and safe(b)
    assert set(leaves) == children(b)
    states = 0
    if terminal:
        for h in leaves:
            result, visited, _ = terminal_win(h)
            assert result, f'false S10 WIN: {h}'
            states += visited
        assert states == 185, states
    return {'s9_win_roots': 1, 's10_win_leaves': len(leaves),
            'terminal_states': states if terminal else None, 'empty_board': 'UNKNOWN'}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path, default=Path(__file__).resolve().parents[1] /
                        f'n11-frontier-5proofs-20261017/input/s9-win-{ROOT}.cert')
    parser.add_argument('--negative', action='store_true')
    args = parser.parse_args()
    raw = args.certificate.read_text(encoding='utf-8')
    print(verify(raw))
    if args.negative:
        lines = raw.strip().splitlines()
        variants = [raw.replace('BOARD 11', 'BOARD 10'),
                    '\n'.join(lines[:4]+lines[5:])+'\n',
                    '\n'.join(lines[:5]+[lines[4]]+lines[6:])+'\n',
                    raw.replace('S9 '+ROOT, 'S9 '+'0'*32)]
        for changed in variants:
            try:
                verify(changed, terminal=False)
            except (AssertionError, ValueError):
                continue
            raise AssertionError('malformed certificate accepted')
        print('PASS 4 negative cases')


if __name__ == '__main__':
    main()
