#!/usr/bin/env python3
"""Independent 3-point integer-circle terminal verification of adaptive 734-leaf schedule.

Regenerates all 734 S10 leaves from the 29 S9 roots. Does not read C++ results,
search caches, or intermediate verdicts.
"""
from itertools import combinations
from pathlib import Path
import sys

P = Path(__file__).resolve().parent
sys.path.insert(0, str(P.parent / 'n11-four-s8-joint-terminal52-20261023'))
from terminal_geometry import safe
from fastgeom import canonical, children, forbidden as forbidden_mask, legal, points


def require(b, message):
    if not b:
        raise ValueError(message)


def prep(board):
    base = list(points(board))
    moves = legal(board)
    n = len(moves)
    require(n <= 63, 'too many legal moves')
    forbidden = []
    bad_pairs = set()
    bad_triples = set()
    for i, j in combinations(range(n), 2):
        if any((forbidden_mask(a, b, moves[i]) >> moves[j]) & 1
               for a, b in combinations(base, 2)):
            pair = (1 << i) | (1 << j)
            forbidden.append(pair)
            bad_pairs.add(pair)
    for i, j, k in combinations(range(n), 3):
        mask = (1 << i) | (1 << j) | (1 << k)
        if ((1 << i) | (1 << j)) in bad_pairs or ((1 << i) | (1 << k)) in bad_pairs or ((1 << j) | (1 << k)) in bad_pairs:
            continue
        if any((forbidden_mask(a, moves[i], moves[j]) >> moves[k]) & 1 for a in base):
            forbidden.append(mask)
            bad_triples.add(mask)
    for i, j, k, l in combinations(range(n), 4):
        mask = (1 << i) | (1 << j) | (1 << k) | (1 << l)
        if any((mask ^ (1 << t)) in bad_triples for t in (i,j,k,l)):
            continue
        if any((mask ^ (1 << t) ^ (1 << u)) in bad_pairs for t,u in combinations((i,j,k,l),2)):
            continue
        if (forbidden_mask(moves[i], moves[j], moves[k]) >> moves[l]) & 1:
            forbidden.append(mask)
    blockers = [[] for _ in range(n)]
    for mask in forbidden:
        for i in range(n):
            if mask & (1 << i):
                blockers[i].append(mask ^ (1 << i))
    return moves, blockers


def run(schedule):
    s9 = [int(s, 16) for s in (P / 's9-win29.keys').read_text().split()]
    require(len(s9) == len(set(s9)) == 29, 'S9 list invalid')
    for b in s9:
        require(b.bit_count() == 9 and safe(b) and canonical(b) == b, 'bad S9 root')
    leaves = sorted(set().union(*(children(b) for b in s9)), reverse=True)
    require(len(leaves) == 734, 'S10 boundary invalid')
    schedule_hex = ''.join(Path(schedule).read_text().split())
    require(len(schedule_hex) == 1468 and all(c in '0123456789abcdef' for c in schedule_hex), 'schedule shape invalid')
    menu = [(100000,1000,0,-1),(100000,1000,0,1),
            (100000,1000,0,-10),(100000,1000,0,10),
            (100000,1000,1,-1),(100000,1000,-1,-1),
            (100000,100,0,-1),(100000,10000,0,-1),
            (24,8,-31,9),(100000,0,0,0),
            (100000,1000,0,-100),(100000,1000,0,100),
            (100000,1000,10,-1),(100000,1000,-10,-1),
            (100000,1000,0,0),(100000,1000,0,-3),
            (100000,1000,0,3),(100000,1000,0,-30),
            (100000,1000,0,30),(100000,1000,0,-300)]
    memo = {}
    lookups = hits = edges = 0
    for index, board in enumerate(leaves):
        j = int(schedule_hex[2*index:2*index+2], 16)
        require(j < len(menu), 'invalid menu index')
        weights = menu[j]
        require(board.bit_count() == 10 and safe(board) and canonical(board) == board, 'bad S10 root')
        moves, blockers = prep(board)
        def score(i):
            pair = sum(b.bit_count() == 1 for b in blockers[i])
            triple = sum(b.bit_count() == 2 for b in blockers[i])
            quad = sum(b.bit_count() == 3 for b in blockers[i])
            dist = abs(moves[i] % 11 - 5) + abs(moves[i] // 11 - 5)
            return sum(w * x for w, x in zip(weights, (pair, triple, quad, dist)))
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
                if mask & bit or any(mask & f == f for f in blockers[i]):
                    continue
                edges += 1
                if not solve(mask | bit, current | (1 << moves[i])):
                    memo[key] = True
                    return True
            memo[key] = False
            return False
        require(solve(0, board), f'S10 LOSS {board:032x}')
    result = len(memo), lookups, hits, edges
    print('PASS S9=29 S10=734 WIN=734 states=%d lookups=%d hits=%d edges=%d empty=UNKNOWN' % result)
    return result


if __name__ == '__main__':
    require(len(sys.argv) == 2, 'usage: verify_adaptive734.py SCHEDULE')
    require(run(sys.argv[1]) == (48794, 81853, 33059, 81119), 'C++ mismatch')
