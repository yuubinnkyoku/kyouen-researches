#!/usr/bin/env python3
"""Scratch exploration: load boards, verify design identities, search witnesses.

Later this evolves into the final self-contained verifier.
"""
import json
import random
import time
from itertools import combinations
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "output"


def load_board(q):
    with open(OUT / f"board_q{q}.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data


class Board:
    def __init__(self, data):
        self.q = data["q"]
        self.v = data["v"]
        self.b = data["b"]
        self.blocks = [tuple(sorted(bl)) for bl in data["blocks"]]
        self.masks = [sum(1 << p for p in bl) for bl in self.blocks]
        self.point_blocks = [[] for _ in range(self.v)]
        for bi, bl in enumerate(self.blocks):
            for p in bl:
                self.point_blocks[p].append(bi)


def check_design(board):
    q, v, b = board.q, board.v, board.b
    assert v == q * q + 1, (v, q * q + 1)
    assert b == q * (q * q + 1), (b, q * (q * q + 1))
    assert len(board.blocks) == b
    assert len(set(board.blocks)) == b
    assert all(len(bl) == q + 1 for bl in board.blocks), "block size"
    assert all(0 <= p < v for bl in board.blocks for p in bl)
    # point degrees
    degrees = [len(pb) for pb in board.point_blocks]
    assert all(d == q * (q + 1) for d in degrees), "degree"
    # pair multiplicities
    pair_sets = [set(pb) for pb in board.point_blocks]
    lam2 = None
    for i, j in combinations(range(v), 2):
        m = len(pair_sets[i] & pair_sets[j])
        if lam2 is None:
            lam2 = m
        assert m == lam2, ("pair multiplicity", i, j, m, lam2)
    assert lam2 == q + 1, lam2
    # triple multiplicities
    tri_count = {}
    for bi, bl in enumerate(board.blocks):
        for tri in combinations(bl, 3):
            tri_count[tri] = tri_count.get(tri, 0) + 1
    assert len(tri_count) == comb(v, 3), (len(tri_count), comb(v, 3))
    assert all(c == 1 for c in tri_count.values())
    return dict(v=v, b=b, k=q + 1, degree=q * (q + 1), pair_lambda=lam2,
                triples=len(tri_count), triple_lambda=1)


def moment_check(board, q, trials, seed=12345):
    rng = random.Random(seed)
    maxdiff2 = maxdiff3 = 0
    for _ in range(trials):
        n = rng.randrange(0, board.v + 1)
        S = set(rng.sample(range(board.v), n))
        s2 = s3 = 0
        for bl in board.blocks:
            c = sum(1 for p in bl if p in S)
            s2 += c * (c - 1) // 2
            s3 += c * (c - 1) * (c - 2) // 6
        maxdiff2 = max(maxdiff2, abs(s2 - comb(n, 2) * (q + 1)))
        maxdiff3 = max(maxdiff3, abs(s3 - comb(n, 3)))
    return maxdiff2, maxdiff3


def penalty_of(board, S, s):
    return sum(max(0, sum(1 for p in bl if p in S) - s) for bl in board.blocks)


def check_set(board, S, s):
    worst = 0
    for bl in board.blocks:
        c = sum(1 for p in bl if p in S)
        worst = max(worst, c)
    return worst <= s, worst


# ---------------- local search for witness ----------------

def local_search(board, s, n, seed, iters=20000, restarts=200, verbose=False):
    """Fixed-cardinality min-conflicts on sum max(0,count-s)."""
    rng = random.Random(seed)
    v, b = board.v, board.b
    pb = board.point_blocks
    allpts = list(range(v))
    t0 = time.time()
    best_pen = None
    total_iters = 0
    for r in range(restarts):
        S = set(rng.sample(allpts, n))
        counts = [0] * b
        for p in S:
            for bi in pb[p]:
                counts[bi] += 1
        pen = sum(max(0, c - s) for c in counts)
        if best_pen is None or pen < best_pen:
            best_pen = pen
        for it in range(iters):
            total_iters += 1
            if pen == 0:
                return S, dict(found=True, restarts=r + 1, iters=it, total_iters=total_iters,
                               seconds=time.time() - t0)
            viol = [bi for bi, c in enumerate(counts) if c > s]
            if not viol:
                return S, dict(found=True, restarts=r + 1, iters=it, total_iters=total_iters,
                               seconds=time.time() - t0)
            bi = rng.choice(viol)
            # remove a random point of the violated block that is in S
            cand_u = [p for p in board.blocks[bi] if p in S]
            u = rng.choice(cand_u)
            # evaluate all v outside S, choose minimal resulting penalty
            outside = [p for p in allpts if p not in S]
            best_v = None
            best_delta = None
            for vp in outside:
                delta = 0
                affected = set()
                for bidx in pb[u]:
                    affected.add(bidx)
                for bidx in pb[vp]:
                    affected.add(bidx)
                for bidx in affected:
                    c = counts[bidx]
                    if u in board.blocks[bidx] and vp in board.blocks[bidx]:
                        continue
                    if vp in board.blocks[bidx]:
                        delta += max(0, c + 1 - s) - max(0, c - s)
                    else:
                        delta += max(0, c - 1 - s) - max(0, c - s)
                if best_delta is None or delta < best_delta:
                    best_delta = delta
                    best_v = vp
                elif delta == best_delta and rng.random() < 0.5:
                    best_v = vp
            vp = best_v
            # apply swap
            for bidx in pb[u]:
                counts[bidx] -= 1
            for bidx in pb[vp]:
                counts[bidx] += 1
            S.remove(u)
            S.add(vp)
            pen += best_delta
            if rng.random() < 0.05 and len(viol) > 1:
                # occasional random kick
                u2 = rng.choice(list(S))
                v2 = rng.choice(outside)
                if v2 not in S:
                    for bidx in pb[u2]:
                        counts[bidx] -= 1
                    for bidx in pb[v2]:
                        counts[bidx] += 1
                    S.remove(u2)
                    S.add(v2)
                    pen = sum(max(0, c - s) for c in counts)
        if verbose and (r + 1) % 20 == 0:
            print(f"  restart {r+1}: best_pen={best_pen}", flush=True)
    return None, dict(found=False, restarts=restarts, total_iters=total_iters,
                      seconds=time.time() - t0, best_pen=best_pen)


# ---------------- exhaustive DFS enumeration for small boards ----------------

def exhaustive_count(board, s, n, limit=None):
    """Enumerate all size-n subsets satisfying cap s; returns (count, witness, nodes).

    Simple increasing-order DFS with pruning on block counts.
    """
    v, b = board.v, board.b
    blocks = board.blocks
    pb = board.point_blocks
    counts = [0] * b
    chosen = []
    nodes = 0
    result = dict(count=0, witness=None, nodes=0, seconds=0.0)
    t0 = time.time()

    def dfs(start, need):
        nonlocal nodes
        nodes += 1
        if result["count"] > 0 and limit is not None and result["count"] >= limit:
            return
        if need == 0:
            result["count"] += 1
            if result["witness"] is None:
                result["witness"] = tuple(chosen)
            return
        # simple bound: enough remaining points
        if v - start < need:
            return
        for p in range(start, v - need + 1):
            ok = True
            for bidx in pb[p]:
                if counts[bidx] >= s:
                    ok = False
                    break
            if not ok:
                continue
            chosen.append(p)
            for bidx in pb[p]:
                counts[bidx] += 1
            dfs(p + 1, need - 1)
            for bidx in pb[p]:
                counts[bidx] -= 1
            chosen.pop()
            if result["count"] > 0 and limit is not None and result["count"] >= limit:
                return

    dfs(0, n)
    result["nodes"] = nodes
    result["seconds"] = time.time() - t0
    return result


def main():
    for q, s, expected in ((4, 4, 9), (5, 5, 16), (7, 4, 13)):
        data = load_board(q)
        board = Board(data)
        print(f"=== q={q} s={s} (claimed {expected}) ===", flush=True)
        info = check_design(board)
        print("design:", info, flush=True)
        md2, md3 = moment_check(board, q, 20)
        print("moment maxdiff (20 trials):", md2, md3, flush=True)

        if q == 4:
            for n in (9, 10):
                res = exhaustive_count(board, s, n)
                print(f"exhaustive n={n}: count={res['count']} witness={res['witness']} nodes={res['nodes']} sec={res['seconds']:.3f}", flush=True)
        elif q == 5:
            for n in (16, 17):
                res = exhaustive_count(board, s, n)
                print(f"exhaustive n={n}: count={res['count']} witness={res['witness']} nodes={res['nodes']} sec={res['seconds']:.3f}", flush=True)
        else:
            # try local search for 13
            t0 = time.time()
            S, stats = local_search(board, s, 13, seed=1, iters=4000, restarts=100, verbose=True)
            print("local search:", stats, "S=", sorted(S) if S else None, flush=True)
            if S:
                print("verify:", check_set(board, S, s), flush=True)


if __name__ == "__main__":
    main()
