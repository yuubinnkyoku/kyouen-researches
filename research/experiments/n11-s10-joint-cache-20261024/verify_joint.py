#!/usr/bin/env python3
"""Independent integer-circle check of the joint 52 LOSS + 734 WIN terminal DAG.

Reconstruct WIN leaves from 29 S9 boundaries, check 52 LOSS leaf keys,
and recompute both shared transposition-table traversal orders from scratch.
No C++ output, cached verdicts, or stored terminal states are read.
"""
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
EXPERIMENTS = HERE.parent
S9 = EXPERIMENTS / 'n11-s9-win29-lift-20261023'
S52 = EXPERIMENTS / 'n11-four-s8-shared-tt-20261023'
CERT = EXPERIMENTS / 'n11-four-s8-joint-terminal52-20261023'
sys.path[:0] = [str(S9), str(S52), str(CERT)]
from verify_adaptive734 import prep, require
from fastgeom import canonical, children
from terminal_geometry import safe

MENU = (
    (100000, 1000, 0, -1), (100000, 1000, 0, 1),
    (100000, 1000, 0, -10), (100000, 1000, 0, 10),
    (100000, 1000, 1, -1), (100000, 1000, -1, -1),
    (100000, 100, 0, -1), (100000, 10000, 0, -1),
    (24, 8, -31, 9), (100000, 0, 0, 0),
    (100000, 1000, 0, -100), (100000, 1000, 0, 100),
    (100000, 1000, 10, -1), (100000, 1000, -10, -1),
    (100000, 1000, 0, 0), (100000, 1000, 0, -3),
    (100000, 1000, 0, 3), (100000, 1000, 0, -30),
    (100000, 1000, 0, 30), (100000, 1000, 0, -300),
)
EXPECTED = ((55289, 92730, 37441, 91944),
            (55289, 92728, 37439, 91942))


def inputs():
    s9 = [int(x, 16) for x in (S9 / 's9-win29.keys').read_text().split()]
    require(len(s9) == len(set(s9)) == 29, 'invalid S9 roots')
    for root in s9:
        require(root.bit_count() == 9 and safe(root) and canonical(root) == root,
                'invalid S9 root')
    win = sorted(set().union(*(children(root) for root in s9)), reverse=True)
    require(len(win) == 734, 'invalid S10 WIN boundary')
    sched = ''.join((S9 / 'schedule734-compact.txt').read_text().split())
    require(len(sched) == 1468 and all(c in '0123456789abcdef' for c in sched),
            'invalid WIN schedule')
    win_weights = []
    for i in range(734):
        index = int(sched[2*i:2*i+2], 16)
        require(index < len(MENU), 'invalid WIN schedule index')
        win_weights.append(MENU[index])

    selected = [int(x, 16) for x in (CERT / 'selected52.keys').read_text().split()]
    require(len(selected) == len(set(selected)) == 52, 'invalid LOSS keys')
    loss = []
    for line in (S52 / 'adaptive52-schedule.tsv').read_text().splitlines():
        key, *weights = line.split()
        require(len(weights) == 4, 'invalid LOSS weights')
        loss.append((int(key, 16), tuple(map(int, weights))))
    require(len(loss) == 52 and [key for key, _ in loss] == selected[::-1],
            'LOSS schedule does not match selected52')
    require(not set(win).intersection(selected), 'opposite-verdict root conflict')
    for key in list(win) + selected:
        require(key.bit_count() == 10 and safe(key) and canonical(key) == key,
                'invalid S10 leaf')
    return [(key, weight, True) for key, weight in zip(win, win_weights)], [
        (key, weight, False) for key, weight in loss]


def run(mode, win, loss):
    memo = {}
    lookups = hits = edges = 0
    blocks = (loss, win) if mode == 0 else (win, loss)
    for block in blocks:
        for board, weights, expected in block:
            moves, blockers = prep(board)
            def score(i):
                pair = sum(sub.bit_count() == 1 for sub in blockers[i])
                triple = sum(sub.bit_count() == 2 for sub in blockers[i])
                quad = sum(sub.bit_count() == 3 for sub in blockers[i])
                dist = abs(moves[i] % 11 - 5) + abs(moves[i] // 11 - 5)
                return sum(w*x for w, x in zip(weights, (pair, triple, quad, dist)))
            order = sorted(range(len(moves)), key=lambda i: (-score(i), moves[i]))

            def solve(mask, current):
                nonlocal lookups, hits, edges
                key = canonical(current)
                lookups += 1
                if key in memo:
                    hits += 1
                    return memo[key]
                for i in order:
                    bit = 1 << i
                    if mask & bit or any(mask & sub == sub for sub in blockers[i]):
                        continue
                    edges += 1
                    if not solve(mask | bit, current | (1 << moves[i])):
                        memo[key] = True
                        return True
                memo[key] = False
                return False
            require(solve(0, board) == expected,
                    f'S10 verdict conflict at {board:032x}')
    result = (len(memo), lookups, hits, edges)
    require(result == EXPECTED[mode], f'mode {mode} metrics mismatch: {result}')
    print(f'PASS mode={mode} leaves=786 states={result[0]} lookups={result[1]} '
          f'hits={result[2]} edges={result[3]} conflicts=0 empty=UNKNOWN')


if __name__ == '__main__':
    win, loss = inputs()
    for mode in (0, 1):
        run(mode, win, loss)
