#!/usr/bin/env python3
"""Stage 2: brute-force safety over all 2^21 subsets, then full Grundy DP.

Independent of stage 1's DFS: here safety is decided mask-by-mask by dynamic
programming on the subset lattice, then the Grundy values are computed by
processing the safe sets in decreasing size.  Both results are cross-checked
against the stage-1 DFS enumeration.

Python standard library only.
"""
from __future__ import annotations

import json
import pickle
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 21
FULL = (1 << N) - 1

CLAIM_COUNTS = {
    0: 1,
    1: 21,
    2: 210,
    3: 1330,
    4: 5880,
    5: 18648,
    6: 41328,
    7: 58320,
    8: 42840,
    9: 11480,
}
CLAIM_TOTAL = 180058
CLAIM_G0 = 89799
CLAIM_G1 = 90259
CLAIM_G = {0: 1, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1, 9: 0}


def mex_from_bits(bits: int) -> int:
    g = 0
    while (bits >> g) & 1:
        g += 1
    return g


def main():
    t0 = time.time()
    with open(HERE / "stage1.pkl", "rb") as f:
        s1 = pickle.load(f)
    lines = [tuple(L) for L in s1["lines"]]
    through = s1["through"]
    line_masks = [sum(1 << p for p in L) for L in lines]
    # masks of the 5 lines through each point
    through_masks = [[line_masks[li] for li in through[p]] for p in range(N)]

    print("[1/4] brute-force safety DP over all 2^21 masks ...", flush=True)
    safe = bytearray(1 << N)
    safe[0] = 1
    cnt = [0] * (N + 1)
    cnt[0] = 1
    for mask in range(1, 1 << N):
        low = mask & -mask
        p = low.bit_length() - 1
        rest = mask ^ low
        if safe[rest]:
            ok = True
            for lm in through_masks[p]:
                if (rest & lm).bit_count() == 3:
                    ok = False
                    break
            if ok:
                safe[mask] = 1
                cnt[mask.bit_count()] += 1
    t_scan = time.time() - t0
    print(f"      safe masks: {sum(cnt)}  elapsed {t_scan:.2f}s", flush=True)
    total = sum(cnt)
    max_size = max(m for m in range(N + 1) if cnt[m])
    print(f"      per-size: { {m: cnt[m] for m in range(N + 1) if cnt[m]} }")
    print(f"      total={total} max_size={max_size}")

    counts_ok = total == CLAIM_TOTAL and all(cnt[m] == CLAIM_COUNTS.get(m, 0) for m in range(N + 1))

    print("[2/4] bucket safe masks by size ...", flush=True)
    by_size = [[] for _ in range(N + 1)]
    for mask in range(1 << N):
        if safe[mask]:
            by_size[mask.bit_count()].append(mask)
    for m in range(N + 1):
        assert len(by_size[m]) == cnt[m]

    # Cross-check against stage-1 DFS enumeration (same universe of safe sets).
    dfs_sets = s1["masks_by_size"]
    same_as_dfs = True
    for m in range(N + 1):
        if sorted(by_size[m]) != sorted(dfs_sets[m]):
            same_as_dfs = False
            print(f"      DFS mismatch at size {m}: {len(by_size[m])} vs {len(dfs_sets[m])}")
    print(f"      brute-force universe == DFS universe: {same_as_dfs}")

    print("[3/4] Grundy DP in decreasing size ...", flush=True)
    grundy = bytearray(1 << N)  # values 0..; only small values expected
    dist = {m: {} for m in range(max_size + 1)}
    ext_min = {m: 10**9 for m in range(max_size + 1)}
    ext_max = {m: -1 for m in range(max_size + 1)}
    stuck = []  # safe sets with no extension but size < max
    for m in range(max_size, -1, -1):
        for mask in by_size[m]:
            seen = 0
            n_ext = 0
            rem = FULL ^ mask
            while rem:
                b = rem & -rem
                rem ^= b
                child = mask | b
                if safe[child]:
                    n_ext += 1
                    seen |= 1 << grundy[child]
            g = mex_from_bits(seen)
            grundy[mask] = g
            dist[m][g] = dist[m].get(g, 0) + 1
            if n_ext < ext_min[m]:
                ext_min[m] = n_ext
            if n_ext > ext_max[m]:
                ext_max[m] = n_ext
            if n_ext == 0 and m < max_size:
                stuck.append(mask)
    t_dp = time.time() - t0
    print(f"      DP elapsed {t_dp - t_scan:.2f}s", flush=True)

    print("\nPER-SIZE GRUNDY DISTRIBUTION (exhaustive)")
    for m in range(max_size + 1):
        d = dict(sorted(dist[m].items()))
        print(f"  k={m:2d}: n={cnt[m]:6d}  dist={d}  extensions per set: [{ext_min[m]}, {ext_max[m]}]")
    print(f"  stuck safe sets with 0 extensions and size < {max_size}: {len(stuck)}")

    uniform = all(len(dist[m]) == 1 for m in range(max_size + 1))
    got_g = {m: next(iter(dist[m])) for m in range(max_size + 1)}
    grundy_ok = uniform and all(got_g.get(m) == CLAIM_G.get(m) for m in range(max_size + 1))

    g0 = sum(v for m in range(max_size + 1) for g, v in dist[m].items() if g == 0)
    g1 = sum(v for m in range(max_size + 1) for g, v in dist[m].items() if g == 1)
    other = total - g0 - g1
    print(f"\nG0={g0} G1={g1} other={other}  (claim G0={CLAIM_G0} G1={CLAIM_G1})")

    # Verify the mex chain from the layer values alone.
    mex_chain_ok = True
    chain = []
    for m in range(max_size, -1, -1):
        if m == max_size:
            chain.append((m, 0))
            continue
        # all children of any size-m set are size-(m+1) and (if uniform) have one value
        child_vals = set(dist[m + 1].keys())
        expect = mex_from_bits(sum(1 << g for g in child_vals))
        chain.append((m, expect))
        if expect != got_g[m]:
            mex_chain_ok = False
    chain.reverse()
    print(f"mex chain (from child layer values): {chain}  ok={mex_chain_ok}")
    # Also without assuming uniformity: children seen in the DP must match.
    # (uniformity itself is the empirical result above.)

    payload = {
        "counts": cnt,
        "total": total,
        "max_size": max_size,
        "counts_ok": counts_ok,
        "same_as_dfs": same_as_dfs,
        "dist": {m: dict(dist[m]) for m in range(max_size + 1)},
        "got_g": got_g,
        "uniform": uniform,
        "grundy_ok": grundy_ok,
        "g0": g0,
        "g1": g1,
        "other": other,
        "stuck": len(stuck),
        "ext_min": {m: ext_min[m] for m in range(max_size + 1)},
        "ext_max": {m: ext_max[m] for m in range(max_size + 1)},
        "mex_chain": chain,
        "mex_chain_ok": mex_chain_ok,
        "elapsed_s": time.time() - t0,
    }
    with open(HERE / "stage2.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    with open(HERE / "safe_bytearray.bin", "wb") as f:
        f.write(safe)
    with open(HERE / "grundy_bytearray.bin", "wb") as f:
        f.write(grundy)
    print(f"\nwrote stage2.json (+ safe/grundy bytearrays), total elapsed {payload['elapsed_s']:.2f}s")
    print(f"COUNTS_OK={counts_ok} UNIVERSES_MATCH={same_as_dfs} UNIFORM={uniform} GRUNDY_OK={grundy_ok}")


if __name__ == "__main__":
    sys.exit(main())
