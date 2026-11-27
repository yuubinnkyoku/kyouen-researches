#!/usr/bin/env python3
"""Stage 3: verify the two 3-cap cone distributions and the corrected identity

    1120 * T_m(g) + 210 * U_m(g) = C(m,3) * N_m(g)

for every size m and Grundy value g.  T is taken over all triangles
(non-collinear triples), U over all collinear triples.

The cone of a 3-cap A is the set of safe sets S with A subset of S.  For a
fixed representative A, T_m(g) counts the cone positions of size m and Grundy
g.  The identity is checked both for every (m,g) and in totals.
"""
from __future__ import annotations

import itertools
import json
import pickle
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
N = 21


def main():
    t0 = time.time()
    with open(HERE / "stage1.pkl", "rb") as f:
        s1 = pickle.load(f)
    with open(HERE / "stage2.json", encoding="utf-8") as f:
        s2 = json.load(f)
    masks_by_size = s1["masks_by_size"]
    lines = [tuple(L) for L in s1["lines"]]
    line_masks = [sum(1 << p for p in L) for L in lines]
    got_g = {int(m): int(g) for m, g in s2["got_g"].items()}
    counts = {m: int(v) for m, v in enumerate(s2["counts"])}
    dist = {int(m): {int(g): int(v) for g, v in d.items()} for m, d in s2["dist"].items()}
    max_size = int(s2["max_size"])

    # --- classify all C(21,3) triples -------------------------------------
    triples = list(itertools.combinations(range(N), 3))
    assert len(triples) == 1330
    tri_index = {}
    for idx, t in enumerate(triples):
        m = 0
        for p in t:
            m |= 1 << p
        tri_index[m] = idx
    is_collinear = []
    for t in triples:
        m = (1 << t[0]) | (1 << t[1]) | (1 << t[2])
        is_collinear.append(any((lm & m) == m for lm in line_masks))
    n_tri = sum(1 for c in is_collinear if not c)
    n_col = sum(1 for c in is_collinear if c)
    print(f"3-subsets: {len(triples)}, triangles (non-collinear): {n_tri}, collinear triples: {n_col}")
    assert n_tri == 1120 and n_col == 210

    # All 3-subsets are safe (s=3 allows exactly 3 on a line).
    assert counts[3] == 1330
    assert dist[3] == {0: 1330}

    # Sanity on the named representatives.
    def tmask(t):
        return (1 << t[0]) | (1 << t[1]) | (1 << t[2])

    rep_tri = (0, 1, 5)
    rep_col = (0, 1, 2)
    assert not any((lm & tmask(rep_tri)) == tmask(rep_tri) for lm in line_masks)
    assert any((lm & tmask(rep_col)) == tmask(rep_col) for lm in line_masks)
    ri_tri = tri_index[tmask(rep_tri)]
    ri_col = tri_index[tmask(rep_col)]

    # --- extension table for every triple ---------------------------------
    # ext[idx][m] = number of safe S of size m with the idx-th triple subset S
    print("building extension table over all 1330 triples ...", flush=True)
    ext = [[0] * (max_size + 1) for _ in range(len(triples))]
    for m in range(3, max_size + 1):
        for mask in masks_by_size[m]:
            bits = []
            x = mask
            while x:
                b = x & -x
                bits.append(b.bit_length() - 1)
                x ^= b
            # each 3-subset of this safe set contributes once to its triple
            for a, b, c in itertools.combinations(bits, 3):
                idx = tri_index[(1 << a) | (1 << b) | (1 << c)]
                ext[idx][m] += 1
    print(f"  done, elapsed {time.time()-t0:.2f}s", flush=True)

    # --- uniformity across all triangles / all collinear triples ----------
    tri_rows = set()
    col_rows = set()
    for idx, c in enumerate(is_collinear):
        row = tuple(ext[idx])
        if c:
            col_rows.add(row)
        else:
            tri_rows.add(row)
    print(f"distinct extension vectors: triangles {len(tri_rows)}, collinear {len(col_rows)}")
    assert len(tri_rows) == 1, "triangles are not all equivalent in extension counts"
    assert len(col_rows) == 1, "collinear triples are not all equivalent in extension counts"
    T_row = next(iter(tri_rows))
    U_row = next(iter(col_rows))
    print(f"T_m (triangle {rep_tri}): {T_row}")
    print(f"U_m (collinear {rep_col}): {U_row}")

    T_total = sum(T_row[3:])
    U_total = sum(U_row[3:])
    print(f"cone sizes: triangle {T_total} (claim 5,038), collinear triple {U_total} (claim 3,809)")
    # one-point cone: 21-3 = 18 for triangle, 21-5 = 16 for collinear triple
    # one-point cone: 18 for a triangle; 16 for a collinear triple
    # (the two further points of its line would create 4 on a line).
    assert T_row[3] == 1 and U_row[3] == 1
    one_step_tri = T_row[4]
    one_step_col = U_row[4]
    print(f"one-point extensions: triangle {one_step_tri} (expect 18), collinear {one_step_col} (expect 16)")
    assert one_step_tri == 18 and one_step_col == 16

    # --- T_m(g), U_m(g) and the identity ----------------------------------
    print("\nCONE TABLES (per fixed representative) AND IDENTITY")
    print(" m |  N_m(g) by g        | T_m(0) T_m(1) | U_m(0) U_m(1) | 1120*T+210*U | C(m,3)*N_m")
    all_ok = True
    detail = []
    for m in range(0, max_size + 1):
        Nmg = {0: 0, 1: 0}
        for g, v in dist[m].items():
            Nmg[g] = v
        # T_m(g): cone positions with each Grundy value
        Tmg = {0: 0, 1: 0}
        Umg = {0: 0, 1: 0}
        for g in (0, 1):
            if got_g[m] == g:
                Tmg[g] = T_row[m]
                Umg[g] = U_row[m]
        rhs = {g: (m * (m - 1) * (m - 2) // 6) * Nmg[g] for g in (0, 1)}
        lhs = {g: 1120 * Tmg[g] + 210 * Umg[g] for g in (0, 1)}
        ok = lhs == rhs
        all_ok &= ok
        detail.append({"m": m, "N": Nmg, "T": Tmg, "U": Umg, "lhs": lhs, "rhs": rhs, "ok": ok})
        print(
            f"{m:2d} | {Nmg} | {Tmg} | {Umg} | {lhs} | {rhs}  {'OK' if ok else 'FAIL'}"
        )
    print(f"identity holds for every (m,g): {all_ok}")

    # Totals: also check g-by-g sums and overall pair counts.
    total_lhs = sum(1120 * d["T"][g] + 210 * d["U"][g] for d in detail for g in (0, 1))
    total_rhs = sum(d["rhs"][g] for d in detail for g in (0, 1))
    pair_total = sum(
        m * (m - 1) * (m - 2) // 6 * counts[m] for m in range(0, max_size + 1)
    )
    print(f"total pairs: LHS={total_lhs} RHS={total_rhs} direct={pair_total}")
    assert total_lhs == total_rhs == pair_total
    assert 1120 * T_total + 210 * U_total == pair_total == 6442450

    # All 3-subsets of a safe set are caps; count of triangles in play.
    assert T_total + U_total == 8847

    payload = {
        "n_triangles": n_tri,
        "n_collinear": n_col,
        "triangle_extension_vector": list(T_row),
        "collinear_extension_vector": list(U_row),
        "T_total": T_total,
        "U_total": U_total,
        "identity_detail": detail,
        "identity_ok": all_ok,
        "total_pairs": pair_total,
        "elapsed_s": time.time() - t0,
    }
    with open(HERE / "stage3.json", "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)
    print(f"wrote stage3.json, elapsed {payload['elapsed_s']:.2f}s")
    print(f"IDENTITY_OK={all_ok}")


if __name__ == "__main__":
    main()
