#!/usr/bin/env python3
"""K0944 deep census (deterministic, byte-stable JSON; run twice and cmp).

Pass A: a=0, u <= 100000: U-set (sigma_E(3;0,3u)==1), tail-in-{0,2} census,
       density buckets.
Pass B: a in {1,2,3}, u <= 50000: census of tail==a+1 (ONE-CHAR witnesses).
Pass C: tail table u <= 25000 (all a): fold4 value-1 set for K <= 100000
       equals the ONE-CHAR prediction; mod-4 census.

Writes output/deep_census.json.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sigmaz3_core as C

UMAX_A = 100000
UMAX_B = 50000
UMAX_C = 25000

def main():
    out = {}

    # Pass A
    U, t0, t2 = [], 0, 0
    for u in range(1, UMAX_A + 1):
        v = C.sigma_E_fast(3, 0, 3 * u)
        if v == 1:
            U.append(u)
        elif v == 0:
            t0 += 1
        elif v == 2:
            t2 += 1
    buckets = {}
    for lo, hi in [(1, 1000), (1000, 2000), (2000, 4000), (4000, 8000),
                   (8000, 16000), (16000, 32000), (32000, 64000), (64000, 100000)]:
        buckets[f"({lo},{hi}]"] = sum(1 for u in U if lo < u <= hi)
    out["A"] = {
        "umax": UMAX_A,
        "U_count": len(U),
        "U_all": U,
        "U_first20": U[:20],
        "U_last10": U[-10:],
        "U_density_buckets": buckets,
        "tail_eq0_count": t0,
        "tail_eq2_count": t2,
    }

    # Pass B
    hitsB = {}
    for a in (1, 2, 3):
        hits = []
        for u in range(1, UMAX_B + 1):
            if C.sigma_E_fast(3, a, 3 * u) == a + 1:
                hits.append(u)
        hitsB[str(a)] = {"umax": UMAX_B, "count": len(hits),
                          "first10": hits[:10]}
    out["B"] = hitsB

    # Pass C
    table = {a: [None] + [C.sigma_E_fast(3, a, 3 * u) for u in range(1, UMAX_C + 1)]
             for a in range(4)}
    KMAX = 4 * UMAX_C
    ones_fold = [K for K in range(4, KMAX + 1)
                 if C.fold4(K, table[K % 4][K // 4]) == 1]
    ones_pred = [4 * u + a for a in range(4) for u in range(1, UMAX_C + 1)
                 if table[a][u] == a + 1]
    mod4 = {str(r): 0 for r in range(4)}
    for K in ones_fold:
        mod4[str(K % 4)] += 1
    out["C"] = {
        "umax": UMAX_C, "Kmax": KMAX,
        "ones_fold_count": len(ones_fold),
        "ones_pred_count": len(ones_pred),
        "sets_equal": ones_fold == ones_pred,
        "mod4": mod4,
    }

    outdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    os.makedirs(outdir, exist_ok=True)
    with open(os.path.join(outdir, "deep_census.json"), "w") as f:
        f.write(json.dumps(out, sort_keys=True, separators=(",", ":")))
    print("deep census written; U_count=%d" % len(U))

if __name__ == "__main__":
    main()
