#!/usr/bin/env python3
"""Full-upset DP cross-check of sampled safe positions.

For each sampled safe position S, computes grundy(S) by recursively expanding
the entire upset of S (all safe supersets) with memoisation.  This is a
completely different implementation from both C programs (Python integers,
set-based legality, recursive mex) and is used to spot-check their values.

Usage:
  python sample_dp.py --sizes 0,1,2,3,4,5,6,7,8,9,10,11 --counts 3,3,3,3,20,3,2,2,3,3,3,3
Writes out/samples.json and out/probe.txt (for indep_verify probe mode).
"""
import argparse
import json
import os
import random
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.abspath(os.path.join(
    HERE, "..", "..", "projective-blocking-kyouen-20261125",
    "output", "board_pg2q5.txt"))
N = 31

lmask = []
point_lines = [[] for _ in range(N)]


def load():
    with open(BOARD, encoding="utf-8") as f:
        tok = f.read().split()
    it = iter(tok)
    n = int(next(it)); b = int(next(it))
    assert n == N and b == 31
    for _ in range(b):
        ln = int(next(it))
        pts = [int(next(it)) for _ in range(ln)]
        m = 0
        for p in pts:
            m |= 1 << p
            point_lines[p].append(len(lmask))
        lmask.append(m)


def legal(mask, p):
    for c in point_lines[p]:
        if (mask & lmask[c]).bit_count() >= 3:
            return False
    return True


FULL = (1 << N) - 1


def random_safe(k, rng, tries=20000):
    for _ in range(tries):
        s = 0
        ok = True
        for _ in range(k):
            cand = [p for p in range(N)
                    if not (s >> p) & 1 and legal(s, p)]
            if not cand:
                ok = False
                break
            s |= 1 << rng.choice(cand)
        if ok and s.bit_count() == k:
            return s
    return None


def grundy_with_nodes(mask):
    memo = {}
    stack_limit = 100000

    def g(m):
        v = memo.get(m)
        if v is not None:
            return v
        if len(memo) > 20_000_000:
            raise RuntimeError("memo too large")
        seen = 0
        rest = FULL ^ m
        while rest:
            bit = rest & -rest
            p = bit.bit_length() - 1
            if legal(m, p):
                seen |= 1 << g(m | bit)
            rest ^= bit
        v = 0
        while (seen >> v) & 1:
            v += 1
        memo[m] = v
        return v

    t0 = time.time()
    val = g(mask)
    return val, len(memo), time.time() - t0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sizes", default="0,1,2,3,4,5,6,7,8,9,10,11")
    ap.add_argument("--counts", default="3,3,3,3,20,3,2,2,3,3,3,3")
    ap.add_argument("--seed", type=int, default=20261128)
    ap.add_argument("--out", default=os.path.join(HERE, "out", "samples.json"))
    args = ap.parse_args()
    sizes = [int(x) for x in args.sizes.split(",")]
    counts = [int(x) for x in args.counts.split(",")]
    assert len(sizes) == len(counts)

    load()
    rng = random.Random(args.seed)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    results = []
    probe_masks = []
    for k, c in zip(sizes, counts):
        seen_pos = set()
        got = 0
        attempts = 0
        while got < c and attempts < 2000:
            attempts += 1
            m = random_safe(k, rng)
            if m is None or m in seen_pos:
                continue
            seen_pos.add(m)
            val, nodes, secs = grundy_with_nodes(m)
            results.append({"size": k, "mask": m, "grundy": val,
                            "upset_nodes": nodes, "seconds": round(secs, 3)})
            probe_masks.append(m)
            got += 1
            print(f"size {k:2d} mask {m:011d} g={val} nodes={nodes} "
                  f"{secs:.2f}s", flush=True)
        if got < c:
            print(f"WARNING: only {got}/{c} samples for size {k}",
                  file=sys.stderr)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=1)
    probe_path = os.path.join(HERE, "out", "probe.txt")
    with open(probe_path, "w", encoding="ascii") as f:
        f.write(f"{len(probe_masks)}\n")
        for m in probe_masks:
            f.write(f"{m}\n")
    print(f"wrote {args.out} and {probe_path}")


if __name__ == "__main__":
    main()
