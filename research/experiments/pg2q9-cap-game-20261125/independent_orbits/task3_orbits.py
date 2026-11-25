"""Task 3 -- orbits of the four start caps under our own generators of PGL(3,9),
plus an independent census of maximal caps to compare the orbit sizes with.

(a) Generators: the 12 elementary transvections E_ij(1), E_ij(i) (i != j), plus
    diag(i,1,1) and the 3-cycle (012), as permutations of the 91 model points.
    BFS over 91-bit point-set masks (chunk-table permutation application).
(b) Independent census: a cap containing a fixed projective frame F is counted
    by DFS.  PGL(3,9) is transitive on frames (task 2), so the number m_k of
    maximal k-caps through a fixed frame is the same for every frame, and
    double counting (maximal k-cap, frame contained in it) gives

        #(maximal k-caps) = #frames * m_k / C(k,4),

    with #frames = 1,769,040 and C(k,4) frames per k-cap.  Same for T_k = the
    number of all k-caps.
(c) 10-caps are conics: count nondegenerate ternary quadratic forms over GF(9)
    up to scalar (q^5-q^2 = 58,968) and check the 10-cap point set is one.

Run:  python task3_orbits.py [k ...]        (default: 6 7 8 10)
"""

from __future__ import annotations

import itertools
import json
import sys
import time

import common
import pgcore as pc


def is_cap(P, pts):
    s = set(pts)
    return all(len(s & set(L)) <= 2 for L in P.lines)


def is_maximal(P, pts):
    s = set(pts)
    on_sec = set()
    for L in P.lines:
        if len(s & set(L)) == 2:
            on_sec |= set(L)
    return all(q in on_sec for q in range(P.n) if q not in s)


def quad_form_matrix(coefs):
    """Symmetric matrix A with q(x) = x^T A x for q = c0 x^2+c1 y^2+c2 z^2+c3 xy+c4 xz+c5 yz."""
    c0, c1, c2, c3, c4, c5 = coefs
    h = 2  # 1/2 in GF(3)
    return [[c0, pc.MUL[h][c3], pc.MUL[h][c4]],
            [pc.MUL[h][c3], c1, pc.MUL[h][c5]],
            [pc.MUL[h][c4], pc.MUL[h][c5], c2]]


def main(ks):
    t00 = time.time()
    out = {}
    M, B, phi = common.setup()
    cm = pc.check_plane(M, "model")
    out["model_ok"] = cm["all_ok"]
    assert cm["all_ok"]

    print("== generators ==")
    mats, labels = pc.generator_matrices()
    perms = [pc.mat_perm(M, A) for A in mats]
    assert all(pc.det3(A) != 0 for A in mats)
    for lab, p in zip(labels, perms):
        assert sorted(p) == list(range(M.n))
    t0 = time.time()
    tabs = [pc.perm_chunk_tables(p, M.n) for p in perms]
    out["n_generators"] = len(tabs)
    out["generator_labels"] = labels
    print(f"{len(tabs)} generators: {labels}")
    print(f"chunk tables built in {time.time() - t0:.2f}s")

    print("\n== (a) BFS orbits of the start caps ==")
    out["orbits"] = {}
    for k in ks:
        cap = common.model_cap(phi, common.STARTS[k])
        assert is_cap(M, cap) and is_maximal(M, cap), f"start {k}-cap not a maximal cap"
        mask = pc.mask_of(cap)
        t0 = time.time()
        seen = {mask}
        frontier = [mask]
        last = 0

        def progress(size):
            nonlocal last
            if size - last >= 500000:
                last = size
                print(f"    ... {size:,d} masks ({time.time() - t0:.1f}s)", flush=True)

        while frontier:
            nxt = []
            for m in frontier:
                for t in tabs:
                    n2 = pc.apply_tables(t, m)
                    if n2 not in seen:
                        seen.add(n2)
                        nxt.append(n2)
            frontier = nxt
            progress(len(seen))
        size = len(seen)
        dt = time.time() - t0
        bad = 0
        sampled = 0
        for m in itertools.islice(iter(seen), 100):
            pts = pc.points_of(m)
            sampled += 1
            if len(pts) != k or not is_cap(M, pts) or not is_maximal(M, pts):
                bad += 1
        rec = {
            "start_cap_board": common.STARTS[k],
            "start_cap_model": cap,
            "orbit_size": size,
            "claim": common.CLAIM_ORBIT[k],
            "matches_claim": size == common.CLAIM_ORBIT[k],
            "seconds": round(dt, 1),
            "sampled_members": sampled,
            "sampled_bad": bad,
        }
        out["orbits"][k] = rec
        print(f"  k={k:2d}: orbit size = {size:>10,d}   claim = {common.CLAIM_ORBIT[k]:>10,d}"
              f"   match = {rec['matches_claim']}   ({dt:.1f}s; {sampled} sampled members all"
              f" maximal {k}-caps: {bad == 0})", flush=True)
        del seen

    print("\n== (b) independent census via one projective frame ==")
    frame = pc.pick_frame(M)
    print(f"frame = {frame} (no three collinear)")
    t0 = time.time()
    capmap = pc.frame_caps(M, frame, maxk=10)
    out["frame_census_seconds"] = round(time.time() - t0, 2)
    nframes = 1769040  # 4-subsets with no collinear triple (brute force, task 2)
    out["n_frames"] = nframes
    out["caps_through_frame"] = {}
    out["maximal_through_frame"] = {}
    out["total_caps_by_size"] = {0: 1, 1: 91, 2: 91 * 90 // 2,
                                 3: 91 * 90 * 89 // 6 - 91 * 120}
    out["maximal_caps_by_size"] = {}
    parent_sizes = {0: 1, 1: 91, 2: 4095, 3: 110565, 4: 1769040, 5: 14859936,
                    6: 52009776, 7: 51554880, 8: 7960680, 9: 589680, 10: 58968}
    parent_max = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 707616, 7: 2021760,
                  8: 5307120, 9: 0, 10: 58968}
    print(f"  {'k':>3} {'T_k':>6} {'all k-caps':>13} {'parent':>13} {'m_k':>5} "
          f"{'maximal k-caps':>15} {'parent':>10}")
    all_ok = True
    for k in range(4, 11):
        Tk = len(capmap[k])
        mk = sum(1 for C, fsz in capmap[k] if fsz == M.n)
        c4 = k * (k - 1) * (k - 2) * (k - 3) // 24
        allk = nframes * Tk // c4
        maxk = nframes * mk // c4
        out["caps_through_frame"][k] = Tk
        out["maximal_through_frame"][k] = mk
        out["total_caps_by_size"][k] = allk
        out["maximal_caps_by_size"][k] = maxk
        ok = (allk == parent_sizes[k] and maxk == parent_max[k])
        all_ok = all_ok and ok
        print(f"  {k:>3} {Tk:>6} {allk:>13,d} {parent_sizes[k]:>13,d} {mk:>5} "
              f"{maxk:>15,d} {parent_max[k]:>10,d}   {'ok' if ok else 'MISMATCH'}")
    for k in range(4, 11):
        c4 = k * (k - 1) * (k - 2) * (k - 3) // 24
        assert (nframes * out["caps_through_frame"][k]) % c4 == 0
        assert (nframes * out["maximal_through_frame"][k]) % c4 == 0
    out["census_matches_parent"] = all_ok
    out["no_maximal_9_caps"] = out["maximal_caps_by_size"][9] == 0
    out["maximal_5_caps"] = out["maximal_caps_by_size"][5]
    print(f"  census matches the claimed counts: {all_ok}")
    print(f"  maximal 9-caps: {out['maximal_caps_by_size'][9]}   "
          f"maximal 5-caps: {out['maximal_caps_by_size'][5]}")

    print("\n== (c) 10-caps = conics ==")
    t0 = time.time()
    n_nondegen = 0
    n_nz = 0
    for coefs in itertools.product(range(9), repeat=6):
        if coefs == (0,) * 6:
            continue
        n_nz += 1
        if pc.det3(quad_form_matrix(coefs)) != 0:
            n_nondegen += 1
    nconics = n_nondegen // 8
    out["nonzero_symmetric_matrices"] = n_nz
    out["nondegenerate_symmetric_matrices"] = n_nondegen
    out["conics_mod_scalars"] = nconics
    out["conics_formula_q5_minus_q2"] = 9 ** 5 - 9 ** 2
    print(f"  symmetric 3x3 forms over GF(9): {n_nz} nonzero, {n_nondegen} nondegenerate "
          f"-> {nconics} conics mod scalars  (q^5-q^2 = {9 ** 5 - 9 ** 2})   [{time.time() - t0:.1f}s]")
    cap10 = common.model_cap(phi, common.STARTS[10])
    rows = []
    for p in cap10:
        x, y, z = M.vectors[p]
        rows.append([pc.MUL[x][x], pc.MUL[y][y], pc.MUL[z][z],
                     pc.MUL[x][y], pc.MUL[x][z], pc.MUL[y][z]])
    basis = pc.nullspace(rows, 6)
    out["quadratic_form_space_dim_through_cap"] = len(basis)
    forms_ok = False
    if len(basis) == 1:
        A = quad_form_matrix(basis[0])
        out["conic_form_matrix"] = A
        out["conic_form_nonsingular"] = pc.det3(A) != 0
        on = []
        for p in range(M.n):
            x, y, z = M.vectors[p]
            val = pc.ADD[pc.ADD[pc.MUL[A[0][0]][pc.MUL[x][x]]][pc.MUL[A[1][1]][pc.MUL[y][y]]]][pc.MUL[A[2][2]][pc.MUL[z][z]]]
            val = pc.ADD[val][pc.MUL[2][pc.MUL[A[0][1]][pc.MUL[x][y]]]]
            val = pc.ADD[val][pc.MUL[2][pc.MUL[A[0][2]][pc.MUL[x][z]]]]
            val = pc.ADD[val][pc.MUL[2][pc.MUL[A[1][2]][pc.MUL[y][z]]]]
            if val == 0:
                on.append(p)
        out["conic_point_set"] = on
        out["cap_is_conic_point_set"] = sorted(on) == sorted(cap10)
        forms_ok = out["conic_form_nonsingular"] and out["cap_is_conic_point_set"]
    print(f"  forms through the start 10-cap: {len(basis)}-dimensional; "
          f"nonsingular = {out.get('conic_form_nonsingular')}; "
          f"zero set equals the cap = {out.get('cap_is_conic_point_set')}")

    out["all_orbits_match_claim"] = all(out["orbits"][k]["matches_claim"] for k in ks)
    out["elapsed_s"] = round(time.time() - t00, 1)
    pc.RESULTS.mkdir(parents=True, exist_ok=True)
    (pc.RESULTS / "task3_orbits.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    ok = out["all_orbits_match_claim"] and all_ok and out["no_maximal_9_caps"] and forms_ok
    out["PASS"] = ok
    print(f"\nTASK 3: {'PASS' if ok else 'FAIL'}   ({out['elapsed_s']} s)")
    return out


if __name__ == "__main__":
    ks = [int(a) for a in sys.argv[1:]] or [6, 7, 8, 10]
    main(ks)
