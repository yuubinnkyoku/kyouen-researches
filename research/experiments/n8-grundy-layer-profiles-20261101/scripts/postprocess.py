#!/usr/bin/env python3
"""Post-process Grundy-only streaming DP results for a square board.

Reads (from the spill dir):
  level_1.occ, level_2.occ, level_3.occ   sorted u64 occupancy masks per layer
  dp_1.bin, dp_2.bin, dp_3.bin            int8 Grundy value per state, index-aligned
  <solve_json>                            summary from grundy_only_stream_solve.cpp

Produces:
  * one-stone layer analysis (K0113 parity, K0182 distinct kinds)
  * J_n graph on board points, edge iff g({p,q})=0 (K0119 connectivity),
    connectivity by union-find AND BFS (two methods)
  * per-layer max M_n(k), ceiling attainment, saturation onset sigma_n
  * holes at the saturation-start layer (K0183 non-consecutive, K0184 powers of two)
  * D_n(k) = K_n - k - M_n(k) monotonicity and M_n(k) <= K_n - k invariant (K0041)
  * mex-recomputation cross-check of levels 1 and 2 from the dp files
    (independent Python geometry, validates C++ DP index alignment)
  * ceiling witness g recomputation at layer sigma_n
  * forbidden-quad count cross-check (Python determinant enumeration vs C++)

Usage: python3 postprocess.py <n> <spill_dir> <solve_json> <out_json> [edges_file]
"""
import bisect
import itertools
import json
import random
import struct
import sys
from collections import deque


def read_masks(path):
    with open(path, "rb") as f:
        data = f.read()
    return list(struct.unpack("<%dQ" % (len(data) // 8), data))


def read_g(path):
    with open(path, "rb") as f:
        data = f.read()
    return list(struct.unpack("<%db" % len(data), data))


def det(m):
    """Exact integer determinant by Laplace expansion (small matrices only)."""
    n = len(m)
    if n == 1:
        return m[0][0]
    d = 0
    for j in range(n):
        minor = [row[:j] + row[j + 1:] for row in m[1:]]
        d += ((-1) ** j) * m[0][j] * det(minor)
    return d


def build_quads(n):
    """Forbidden 4-point masks: det[x^2+y^2, x, y, 1] == 0 (concyclic/collinear)."""
    pts = [(x, y) for y in range(n) for x in range(n)]
    V = n * n
    rows = [[x * x + y * y, x, y, 1] for (x, y) in pts]
    quads = []
    for a, b, c, d in itertools.combinations(range(V), 4):
        if det([rows[a], rows[b], rows[c], rows[d]]) == 0:
            quads.append((1 << a) | (1 << b) | (1 << c) | (1 << d))
    return quads


def build_triples_by_pt(quads, V):
    """For each point p, the list of 3-subsets t such that t | {p} is forbidden."""
    by_pt = [[] for _ in range(V)]
    for q in quads:
        pts = []
        t = q
        while t:
            pts.append((t & -t).bit_length() - 1)
            t &= t - 1
        for p in pts:
            by_pt[p].append(q & ~(1 << p))
    return by_pt


def legal_mask(triples_by_pt, occ, full):
    """Empty points v that complete no forbidden quad with occ."""
    empty = full & ~occ
    blocked = 0
    e = empty
    while e:
        v = (e & -e).bit_length() - 1
        e &= e - 1
        for t in triples_by_pt[v]:
            if (occ & t) == t:
                blocked |= 1 << v
                break
    return empty & ~blocked


def mex_from_children(child_g_values):
    gm = 0
    for g in child_g_values:
        gm |= 1 << g
    return (~gm & (gm + 1)).bit_length() - 1


def mex_recheck(n, spill, k, sample_indices, masks_k, g_k, masks_k1, g_k1,
                triples_by_pt, full):
    """Recompute g for sampled level-k states from dp_{k+1} via mex over legal children."""
    out = []
    for idx in sample_indices:
        S = masks_k[idx]
        lm = legal_mask(triples_by_pt, S, full)
        child_g = []
        o = lm
        while o:
            v = (o & -o).bit_length() - 1
            o &= o - 1
            child = S | (1 << v)
            pos = bisect.bisect_left(masks_k1, child)
            assert pos < len(masks_k1) and masks_k1[pos] == child, (k, idx, hex(child))
            child_g.append(g_k1[pos])
        g = 0 if not child_g else mex_from_children(child_g)
        out.append({"idx": idx, "mask": S, "g_recomputed": g, "g_dp": g_k[idx]})
    return out


def main():
    n = int(sys.argv[1])
    spill = sys.argv[2]
    solve_json = sys.argv[3]
    out_json = sys.argv[4]
    edges_file = sys.argv[5] if len(sys.argv) > 5 else None
    V = n * n

    with open(solve_json) as f:
        sol = json.load(f)
    K = sol["max_safe_size"]
    lsizes = sol["level_sizes"]

    # ---------------- independent geometry ----------------
    quads = build_quads(n)
    triples_by_pt = build_triples_by_pt(quads, V)
    full = (1 << V) - 1

    # ---------------- one-stone layer ----------------
    m1 = read_masks(spill + "/level_1.occ")
    g1 = read_g(spill + "/dp_1.bin")
    assert len(m1) == len(g1) == V, (len(m1), len(g1), V)
    one_stone = {}
    for i, (mask, g) in enumerate(zip(m1, g1)):
        assert mask == (1 << i), (i, mask)
        one_stone[i] = g
    distinct = sorted(set(one_stone.values()))
    nonzero = [v for v in one_stone.values() if v != 0]
    one_stone_out = {
        "distinct_values": distinct,
        "distinct_count": len(distinct),
        "value_counts": {str(v): sum(1 for x in one_stone.values() if x == v) for v in distinct},
        "nonzero_all_odd": all(v % 2 == 1 for v in nonzero),
        "nonzero_values": sorted(set(nonzero)),
        "points_by_value": {str(v): [i for i in range(V) if one_stone[i] == v] for v in distinct},
    }

    # ---------------- J_n graph ----------------
    m2 = read_masks(spill + "/level_2.occ")
    g2 = read_g(spill + "/dp_2.bin")
    assert len(m2) == len(g2) == lsizes[2]
    edges = []
    deg = [0] * V
    for mask, g in zip(m2, g2):
        if g != 0:
            continue
        p = (mask & -mask).bit_length() - 1
        q = (mask ^ (1 << p)).bit_length() - 1
        edges.append((p, q))
        deg[p] += 1
        deg[q] += 1
    parent = list(range(V))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for p, q in edges:
        rp, rq = find(p), find(q)
        if rp != rq:
            parent[rp] = rq
    isolated = [v for v in range(V) if deg[v] == 0]
    noniso = [v for v in range(V) if deg[v] > 0]
    comps_uf = len({find(v) for v in noniso})
    adj = [[] for _ in range(V)]
    for p, q in edges:
        adj[p].append(q)
        adj[q].append(p)
    seen = [False] * V
    ncomp_bfs = 0
    for s in noniso:
        if seen[s]:
            continue
        ncomp_bfs += 1
        seen[s] = True
        dq = deque([s])
        while dq:
            u = dq.popleft()
            for w in adj[u]:
                if not seen[w]:
                    seen[w] = True
                    dq.append(w)
    jn = {
        "vertices": V,
        "edges": len(edges),
        "isolated_vertices": isolated,
        "isolated_count": len(isolated),
        "nonisolated_components_unionfind": comps_uf,
        "nonisolated_components_bfs": ncomp_bfs,
        "nonisolated_connected": comps_uf == 1 and ncomp_bfs == 1,
        "degree_min": min(deg) if noniso else 0,
        "degree_max": max(deg) if noniso else 0,
        "degree_hist": {str(d): sum(1 for x in deg if x == d) for d in sorted(set(deg))},
    }
    if edges_file:
        with open(edges_file, "w") as f:
            for p, q in edges:
                f.write("%d %d\n" % (p, q))

    # ---------------- saturation / ceilings ----------------
    M = sol["M_n_k"]
    assert len(M) == K + 1
    sigma = None
    for k in range(K + 1):
        if M[k] == K - k:
            sigma = k
            break
    D = [K - k - M[k] for k in range(K + 1)]
    D_monotone = all(D[k] >= D[k + 1] for k in range(K))
    ceiling_invariant = all(M[k] <= K - k for k in range(K + 1))
    hists = {lv["k"]: lv["hist"] for lv in sol["levels"]}

    def realized_at(k):
        h = hists[k]
        return {g for g in range(len(h)) if h[g] > 0}

    sat_out = {
        "K_n": K,
        "M_n_k": M,
        "sigma_n": sigma,
        "D_n_k": D,
        "D_monotone_nonincreasing": D_monotone,
        "ceiling_invariant_M_le_K_minus_k": ceiling_invariant,
    }
    if sigma is not None:
        realized = realized_at(sigma)
        rng = K - sigma
        missing = [j for j in range(rng) if j not in realized]
        sat_out["sigma_layer"] = {
            "k": sigma,
            "realized_nimbers": sorted(realized),
            "range_j_lt_K_minus_sigma": list(range(rng)),
            "missing": missing,
            "missing_consecutive_pair_exists": any((j + 1) in missing for j in missing),
            "missing_positive_all_powers_of_two": all(
                (m & (m - 1)) == 0 for m in missing if m > 0
            ),
        }
    sat_out["holes_by_layer"] = {
        str(k): sorted(set(range(max(M) + 1)) - realized_at(k)) for k in range(K + 1)
    }

    # ---------------- mex rechecks from dp files ----------------
    m3 = read_masks(spill + "/level_3.occ")
    g3 = read_g(spill + "/dp_3.bin")
    recheck1 = mex_recheck(n, spill, 1, list(range(V)), m1, g1, m2, g2,
                           triples_by_pt, full)
    rng = random.Random(20261101)
    sample2 = sorted(rng.sample(range(lsizes[2]), min(300, lsizes[2])))
    recheck2 = mex_recheck(n, spill, 2, sample2, m2, g2, m3, g3,
                           triples_by_pt, full)
    recheck = {
        "level1_sample_size": len(recheck1),
        "level1_mismatches": [r for r in recheck1 if r["g_recomputed"] != r["g_dp"]],
        "level2_sample_size": len(recheck2),
        "level2_mismatches": [r for r in recheck2 if r["g_recomputed"] != r["g_dp"]],
    }

    # ---------------- ceiling witness at sigma ----------------
    witness = None
    if sigma is not None and sigma < K:
        lv = [l for l in sol["levels"] if l["k"] == sigma][0]
        widx = lv["witness_idx"]
        wmask = int(lv["witness_mask"])
        mk = read_masks(spill + ("/level_%d.occ" % sigma))
        gk = read_g(spill + ("/dp_%d.bin" % sigma))
        mk1 = read_masks(spill + ("/level_%d.occ" % (sigma + 1)))
        gk1 = read_g(spill + ("/dp_%d.bin" % (sigma + 1)))
        rc = mex_recheck(n, spill, sigma, [widx], mk, gk, mk1, gk1,
                         triples_by_pt, full)
        witness = {
            "k": sigma, "idx": widx, "mask": wmask,
            "g_dp": gk[widx], "g_recomputed": rc[0]["g_recomputed"],
            "mask_matches": mk[widx] == wmask,
        }

    out = {
        "n": n,
        "V": V,
        "K_n": K,
        "g_root": sol["g_root"],
        "n_P": sol["n_P"],
        "n_N": sol["n_N"],
        "n_safe_subsets": sol["n_safe_subsets"],
        "forbidden_quads_python": len(quads),
        "forbidden_quads_cpp": sol["F"],
        "quad_count_match": len(quads) == sol["F"],
        "one_stone": one_stone_out,
        "J_n": jn,
        "saturation": sat_out,
        "mex_recheck": recheck,
        "sigma_witness": witness,
    }
    with open(out_json, "w") as f:
        json.dump(out, f, indent=1)
    print(json.dumps({k: out[k] for k in
                      ("g_root", "quad_count_match", "one_stone", "J_n",
                       "mex_recheck", "sigma_witness")}, indent=1)[:4000])
    print("sigma:", sigma, "M:", M, "D_monotone:", D_monotone,
          "ceiling_inv:", ceiling_invariant)
    if sigma is not None:
        print("sigma_layer:", json.dumps(sat_out["sigma_layer"]))


if __name__ == "__main__":
    main()
