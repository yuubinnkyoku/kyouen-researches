"""Task 2 -- build PG(2,9) from GF(9)=GF(3)[x]/(x^2+1), match it to the board,
and build our own generating set of PGL(3,9) acting on the 91 points.

Steps
  1. field axioms for GF(9) (all verify_* flags, printed);
  2. own model: 91 canonical nonzero vectors of GF(9)^3, 91 lines = kernels of
     the nonzero covectors; projective-plane axioms checked;
  3. board: parse output/board_pg2q9.txt and check the same axioms;
  4. explicit line-preserving bijection board -> model found by constraint
     propagation + backtracking (NOT by trusting the build script's ordering),
     then verified on all 91 lines;
  5. |PGL(3,9)| = 42,456,960 two ways:
       (a) |GL| = (9^3-1)(9^3-9)(9^3-9^2) = 728*720*648, divided by |Z| = 8;
       (b) count of ordered projective frames by brute force over all
           C(91,4)=2,672,670 4-subsets, times 24;
     plus a check that PGL acts sharply transitively on frames (unique
     projectivity for random frame pairs, via a 12x13 linear system over GF(9));
  6. our generators: the 12 elementary transvections E_ij(1), E_ij(i) plus
     diag(i,1,1) and the 3-cycle (012), as permutations of the 91 points.

Run:  python task2_model_iso.py
"""

from __future__ import annotations

import itertools
import json
import random
import time

import common
import pgcore as pc


def count_frames(P):
    """Brute-force count of 4-subsets with no three collinear."""
    n = P.n
    frames = 0
    nonframes = 0
    for quad in itertools.combinations(range(n), 4):
        ok = True
        for a, b, c in itertools.combinations(quad, 3):
            if c in P.line_sets[P.line_through(a, b)]:
                ok = False
                break
        if ok:
            frames += 1
        else:
            nonframes += 1
    return frames, nonframes


def main():
    t0 = time.time()
    out = {}
    print("== 1. GF(9) ==")
    ax = pc.gf_axioms()
    out["gf_axioms"] = ax
    print(json.dumps(ax, sort_keys=True))

    print("\n== 2. own model of PG(2,9) ==")
    M = pc.build_model()
    cm = pc.check_plane(M, "model")
    out["model"] = cm
    print(f"91 canonical vectors, 91 lines of 10; axioms ok = {cm['all_ok']} "
          f"(pairs={cm['n_pairs']})")

    print("\n== 3. board file ==")
    B = pc.read_board()
    cb = pc.check_plane(B, "board")
    out["board"] = cb
    print(f"board axioms ok = {cb['all_ok']}")

    print("\n== 4. explicit bijection board -> model ==")
    phi = pc.find_isomorphism(B, M, verbose=True)
    out["iso_verified"] = pc.verify_isomorphism(B, M, phi)
    print(f"verified on all 91 lines: {out['iso_verified']}")
    print(f"phi(board 0..9) = {phi[:10]}")
    # every board line maps to a model line (explicit witness)
    wit = []
    for lid in (0, 1, 45, 90):
        wit.append({"board_line": lid, "board_points": list(B.lines[lid]),
                    "model_line": sorted(phi[p] for p in B.lines[lid])})
    out["line_witnesses"] = wit
    for w in wit:
        print(f"  line {w['board_line']:2d} -> {w['model_line']}")
    out["phi"] = phi

    print("\n== 5. |PGL(3,9)| ==")
    q = 9
    gl = (q ** 3 - 1) * (q ** 3 - q) * (q ** 3 - q ** 2)
    out["gl_order"] = gl
    out["pgl_order_gl_over_8"] = gl // (q - 1)
    print(f"|GL(3,9)| = 728*720*648 = {gl}; |PGL| = |GL|/8 = {gl // 8}")

    frames, nonframes = count_frames(M)
    out["frames_4subset"] = frames
    out["nonframes_4subset"] = nonframes
    out["total_4subsets"] = frames + nonframes
    out["pgl_order_frame_count"] = 24 * frames
    print(f"4-subsets: {frames + nonframes} = {frames} frames + {nonframes} with a collinear triple")
    print(f"ordered frames = 24 * {frames} = {24 * frames}")
    out["pgl_order_frame_count_formula"] = 91 * 90 * 81 * 64
    print(f"91*90*81*64 = {91 * 90 * 81 * 64} (p1 != p0, p2 off a line, p3 off 3 sides)")
    out["pgl_order_agrees"] = (gl // 8 == 24 * frames == 91 * 90 * 81 * 64)
    print(f"all three counts agree: {out['pgl_order_agrees']}")

    # sharp transitivity on frames + uniqueness of the projectivity
    rng = random.Random(20261125)
    def rand_frame(P):
        while True:
            q4 = rng.sample(range(P.n), 4)
            lines = {P.line_through(a, b) for a, b in itertools.combinations(q4, 2)}
            if len(lines) == 6:
                return q4
    trans = 0
    trials = 60
    for _ in range(trials):
        f = rand_frame(M)
        d = rand_frame(M)
        fv = [M.vectors[p] for p in f]
        dv = [M.vectors[p] for p in d]
        rows = []
        for i in range(4):
            for r in range(3):
                row = [0] * 13
                for c in range(3):
                    row[3 * r + c] = fv[i][c]
                row[9 + i] = pc.NEG[dv[i][r]]
                rows.append(row)
        basis = pc.nullspace(rows, 13)
        A = pc.solve_frame_map(fv, dv)
        if A is not None and pc.det3(A) != 0 and len(basis) == 1:
            trans += 1
    out["frame_map_trials"] = trials
    out["frame_map_unique_invertible_solutions"] = trans
    print(f"random frame pairs: {trans}/{trials} unique invertible projectivities (sharp transitivity)")
    # a non-frame target must not admit an invertible solution
    f = rand_frame(M)
    bad = 0
    nonframe_trials = 0
    fv = [M.vectors[p] for p in f]
    for _ in range(200):
        q4 = rng.sample(range(M.n), 4)
        lines = {M.line_through(a, b) for a, b in itertools.combinations(q4, 2)}
        if len(lines) == 6:
            continue
        nonframe_trials += 1
        if pc.frame_map_has_invertible(fv, [M.vectors[p] for p in q4]):
            bad += 1
    out["nonframe_trials"] = nonframe_trials
    out["nonframe_invertible_solutions"] = bad
    print(f"non-frame 4-tuples: {bad}/{nonframe_trials} admit an invertible map (must be 0)")

    print("\n== 6. own generators (permutations of the 91 points) ==")
    mats, labels = pc.generator_matrices()
    gens = []
    for A, lab in zip(mats, labels):
        perm = pc.mat_perm(M, A)
        assert pc.det3(A) != 0
        assert sorted(perm) == list(range(M.n))
        gens.append({"label": lab, "matrix": A, "perm": list(perm),
                     "order_as_permutation": pc.perm_order(perm)})
        print(f"  {lab:12s} det={pc.det3(A)} order={pc.perm_order(perm)}")
    out["generators"] = gens
    # scalar multiples induce the same permutation (PGL, not GL, acts)
    A = mats[0]
    scal = [[pc.MUL[5][A[i][j]] for j in range(3)] for i in range(3)]
    out["scalar_multiple_same_permutation"] = (pc.mat_perm(M, scal) == tuple(gens[0]["perm"]))
    print(f"scalar multiple gives the same point permutation: {out['scalar_multiple_same_permutation']}")

    out["elapsed_s"] = round(time.time() - t0, 2)
    pc.RESULTS.mkdir(parents=True, exist_ok=True)
    (pc.RESULTS / "task2_model_iso.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    ok = (cm["all_ok"] and cb["all_ok"] and out["iso_verified"] and out["pgl_order_agrees"]
          and trans == trials and bad == 0 and out["scalar_multiple_same_permutation"])
    out["PASS"] = ok
    print(f"\nTASK 2: {'PASS' if ok else 'FAIL'}   ({out['elapsed_s']} s)")
    return out


if __name__ == "__main__":
    main()
