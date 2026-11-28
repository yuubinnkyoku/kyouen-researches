#!/usr/bin/env python3
"""Local search for small 2-fold blocking sets (witness finder, not a proof).

Cost = sum over lines of max(0, 2 - |S cap L|). Move = add a point on a
deficient line, drop a random point (mild annealing). A cost-0 set is a
witness; verified by check_blocking before returning. Deterministic per seed.
"""
import json, random, sys, os
sys.path.insert(0, os.path.dirname(__file__))
from sat_min import get_plane, check_blocking

def search(kind, q, k, iters=200000, seed=0, restarts=200):
    n, lines = get_plane(kind, q)
    inc = [[] for _ in range(n)]
    for li, L in enumerate(lines):
        for p in L:
            inc[p].append(li)
    rng = random.Random(seed)
    best_cost = None
    for r in range(restarts):
        S = set(rng.sample(range(n), k))
        cnt = [0] * len(lines)
        for p in S:
            for li in inc[p]:
                cnt[li] += 1
        cost = sum(max(0, 2 - c) for c in cnt)
        if best_cost is None or cost < best_cost:
            best_cost = cost
        for it in range(iters // restarts):
            if cost == 0:
                ok, bad = check_blocking(n, lines, sorted(S))
                assert ok
                return sorted(S), 0
            deficient = [li for li, c in enumerate(cnt) if c < 2]
            li = rng.choice(deficient)
            cands = [p for p in lines[li] if p not in S]
            if not cands:
                continue
            a = rng.choice(cands)
            b = rng.choice(sorted(S))
            S.add(a); S.discard(b)
            for l2 in inc[a]: cnt[l2] += 1
            for l2 in inc[b]: cnt[l2] -= 1
            newcost = sum(max(0, 2 - c) for c in cnt)
            if newcost > cost and rng.random() < 0.3:
                S.discard(a); S.add(b)
                for l2 in inc[a]: cnt[l2] -= 1
                for l2 in inc[b]: cnt[l2] += 1
            else:
                cost = newcost
                if cost < best_cost:
                    best_cost = cost
    return None, best_cost

if __name__ == '__main__':
    kind, q, k = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    seed = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    S, bc = search(kind, q, k, seed=seed)
    if S:
        print(json.dumps({'kind': kind, 'q': q, 'k': k, 'res': 'FOUND',
                          'size': len(S), 'witness': S, 'seed': seed}))
    else:
        print(json.dumps({'kind': kind, 'q': q, 'k': k, 'res': 'none',
                          'best_cost': bc, 'seed': seed}))
