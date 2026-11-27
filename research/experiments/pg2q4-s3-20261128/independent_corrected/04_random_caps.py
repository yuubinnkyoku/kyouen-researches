#!/usr/bin/env python3
"""Stage 4: direct-upset Grundy solver, random caps, mex chain, totals.

The solver here is intentionally independent of the stage-2 DP:

  * safety of a move is checked directly from the five lines through the new
    point (no precomputed safe-set table);
  * Grundy values are produced by memoized recursion on the *upset* of the
    queried position.

Phase A computes G(empty), which reaches every safe set, and compares all
180,058 values with stage 2.  Phase B re-runs the solver from scratch for each
size layer and evaluates 20 uniformly random safe sets of that size.  Phase C
re-derives the mex chain and totals from the fresh values.
"""
from __future__ import annotations

import json
import pickle
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 21
FULL = (1 << N) - 1
SEED = 20261128
SAMPLES_PER_SIZE = 20
CLAIM_G = {0: 1, 1: 0, 2: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1, 9: 0}
CLAIM_COUNTS = {0: 1, 1: 21, 2: 210, 3: 1330, 4: 5880, 5: 18648, 6: 41328, 7: 58320, 8: 42840, 9: 11480}


def main():
    t0 = time.time()
    sys.setrecursionlimit(10000)
    with open(HERE / "stage1.pkl", "rb") as f:
        s1 = pickle.load(f)
    with open(HERE / "stage2.json", encoding="utf-8") as f:
        s2 = json.load(f)
    line_masks = s1["line_masks"]
    through = s1["through"]
    lines_through_masks = [[line_masks[li] for li in through[p]] for p in range(N)]
    masks_by_size = s1["masks_by_size"]
    stage2_g = {int(m): int(g) for m, g in s2["got_g"].items()}
    stage2_dist = {int(m): {int(g): int(v) for g, v in d.items()} for m, d in s2["dist"].items()}
    max_size = int(s2["max_size"])

    def make_solver():
        memo = {}

        def g(S: int) -> int:
            v = memo.get(S)
            if v is not None:
                return v
            seen = 0
            rem = FULL ^ S
            while rem:
                b = rem & -rem
                rem ^= b
                p = b.bit_length() - 1
                ok = True
                for lm in lines_through_masks[p]:
                    if (S & lm).bit_count() > 2:
                        ok = False
                        break
                if ok:
                    seen |= 1 << g(S | b)
            val = 0
            while (seen >> val) & 1:
                val += 1
            memo[S] = val
            return val

        return g, memo

    # ---------------- Phase A: full DP via upset recursion ----------------
    print("Phase A: direct upset recursion from the empty position ...", flush=True)
    g_full, memo_full = make_solver()
    g_empty = g_full(0)
    tA = time.time() - t0
    print(f"  G(empty)={g_empty} (claim 1); memo size={len(memo_full)} (claim 180,058); {tA:.2f}s")
    assert g_empty == 1
    assert len(memo_full) == 180058

    # Compare every safe set's value with the stage-2 DP and the claim.
    mismatch_stage2 = 0
    mismatch_claim = 0
    distA = {m: {} for m in range(max_size + 1)}
    for m in range(max_size + 1):
        for S in masks_by_size[m]:
            v = memo_full[S]
            distA[m][v] = distA[m].get(v, 0) + 1
            if v != stage2_g[m]:
                mismatch_stage2 += 1
            if v != CLAIM_G[m]:
                mismatch_claim += 1
    uniformA = all(len(distA[m]) == 1 for m in range(max_size + 1))
    print(f"  vs stage-2 per-size values: mismatches={mismatch_stage2}")
    print(f"  vs claim per-size values:   mismatches={mismatch_claim}")
    print(f"  uniform per size: {uniformA}; per-size dist: { {m: dict(distA[m]) for m in range(max_size+1)} }")

    # ---------------- Phase B: random caps per size -----------------------
    print(f"\nPhase B: {SAMPLES_PER_SIZE} random caps per size, fresh solver per layer ...", flush=True)
    rng = random.Random(SEED)
    sample_rows = []
    all_samples_ok = True
    total_layer_nodes = 0
    for m in range(max_size, -1, -1):
        g, memo = make_solver()
        pool = masks_by_size[m]
        if len(pool) <= SAMPLES_PER_SIZE:
            samples = [rng.choice(pool) for _ in range(SAMPLES_PER_SIZE)]
        else:
            samples = rng.sample(pool, SAMPLES_PER_SIZE)
        vals = []
        for S in samples:
            vals.append(g(S))
        nodes = len(memo)
        total_layer_nodes += nodes
        ok = all(v == CLAIM_G[m] for v in vals)
        all_samples_ok &= ok
        # safety of each sample checked directly (defensive)
        for S in samples:
            bits = [p for p in range(N) if (S >> p) & 1]
            assert len(bits) == m
            for lm in line_masks:
                assert (S & lm).bit_count() <= 3, "sampled a non-safe set"
        distinct = len(set(vals))
        sample_rows.append(
            {
                "size": m,
                "n_pool": len(pool),
                "n_samples": len(samples),
                "nodes_in_layer_solver": nodes,
                "values": sorted(set(vals)),
                "distinct_values": distinct,
                "ok": ok,
            }
        )
        print(
            f"  k={m:2d}: pool={len(pool):6d} samples={len(samples):2d} "
            f"values={sorted(set(vals))} layer_solver_nodes={nodes:6d} ok={ok}"
        )
    print(f"  total solver nodes across layers: {total_layer_nodes}")
    print(f"  all sampled caps match claim: {all_samples_ok}")

    # ---------------- Phase C: mex chain and totals ----------------------
    # Use the fresh full memo (Phase A) to rebuild the chain from scratch.
    print("\nPhase C: mex chain and totals from fresh values ...", flush=True)
    chain_ok = True
    chain = []
    for m in range(max_size + 1):
        child_vals = set(distA[m + 1].keys()) if m < max_size else set()
        if m == max_size:
            mex = 0
        else:
            mex = 0
            while mex in child_vals:
                mex += 1
        chain.append((m, mex))
        if mex != stage2_g[m]:
            chain_ok = False
    print(f"  child-layer mex chain: {chain}  ok={chain_ok}")
    g0 = sum(v for m in range(max_size + 1) for k, v in distA[m].items() if k == 0)
    g1 = sum(v for m in range(max_size + 1) for k, v in distA[m].items() if k == 1)
    other = sum(v for m in range(max_size + 1) for k, v in distA[m].items() if k not in (0, 1))
    print(f"  totals from fresh values: G0={g0} G1={g1} other={other} sum={g0+g1+other}")
    totals_ok = (g0, g1, other) == (89799, 90259, 0)
    # layer counts from the fresh enumeration lists
    layer_ok = all(len(masks_by_size[m]) == CLAIM_COUNTS.get(m, 0) for m in range(N + 1))
    print(f"  layer counts match claim: {layer_ok}")
    print(f"  max safe size: {max(m for m in range(N + 1) if masks_by_size[m])} (claim 9)")

    payload = {
        "g_empty": g_empty,
        "memo_size": len(memo_full),
        "mismatch_stage2": mismatch_stage2,
        "mismatch_claim": mismatch_claim,
        "uniform": uniformA,
        "distA": {m: dict(distA[m]) for m in range(max_size + 1)},
        "samples": sample_rows,
        "all_samples_ok": all_samples_ok,
        "total_layer_nodes": total_layer_nodes,
        "chain": chain,
        "chain_ok": chain_ok,
        "g0": g0,
        "g1": g1,
        "other": other,
        "totals_ok": totals_ok,
        "layer_ok": layer_ok,
        "seed": SEED,
        "elapsed_s": time.time() - t0,
    }
    with open(HERE / "stage4.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"\nwrote stage4.json, elapsed {payload['elapsed_s']:.2f}s")
    print(
        f"PHASE_A_OK={mismatch_stage2 == 0 and mismatch_claim == 0 and uniformA} "
        f"PHASE_B_OK={all_samples_ok} PHASE_C_OK={chain_ok and totals_ok and layer_ok}"
    )


if __name__ == "__main__":
    main()
