"""Task 2: PGL(3,9) generators, orders, transitivity on 1/2/3/4-caps."""

from __future__ import annotations

import itertools
import json
import math
import random
import time

import game
import group
import pg


def mat_inv(A):
    M = [
        [A[3 * i], A[3 * i + 1], A[3 * i + 2], 1 if i == 0 else 0,
         1 if i == 1 else 0, 1 if i == 2 else 0]
        for i in range(3)
    ]
    for col in range(3):
        piv = None
        for r in range(col, 3):
            if M[r][col]:
                piv = r
                break
        assert piv is not None
        M[col], M[piv] = M[piv], M[col]
        inv = pg.GF_INV[M[col][col]]
        M[col] = [pg.GF_MUL[inv][x] for x in M[col]]
        for r in range(3):
            if r == col:
                continue
            f = M[r][col]
            if f:
                M[r] = [
                    pg.GF_ADD[M[r][c]][
                        pg.GF_MUL[pg.GF_MUL[2][f]][M[col][c]]
                    ]
                    for c in range(6)
                ]
    B = tuple(M[i][3 + j] for i in range(3) for j in range(3))
    # check
    I = group.mat_mul(A, B)
    assert I == group.mat_identity(), I
    return B


def frame_projectivity(f, d):
    """Return the unique M with M f_i projectively equal to d_i.

    f, d are ordered frames (4 vectors each).
    """
    # matrices have the frame vectors as COLUMNS (row-major storage)
    F = tuple(f[j][i] for i in range(3) for j in range(3))
    Dm = tuple(d[j][i] for i in range(3) for j in range(3))
    Finv = mat_inv(F)
    Dinv = mat_inv(Dm)
    alpha = group.mat_vec(Finv, f[3])
    beta = group.mat_vec(Dinv, d[3])
    assert all(x != 0 for x in alpha), alpha
    assert all(x != 0 for x in beta), beta
    cols = []
    for i in range(3):
        lam = pg.GF_MUL[beta[i]][pg.GF_INV[alpha[i]]]
        cols.append(tuple(pg.GF_MUL[lam][x] for x in d[i]))
    # Dcols has columns lambda_i*d_i: entry (row j, column i) = cols[i][j]
    Dcols = tuple(cols[i][j] for j in range(3) for i in range(3))
    M = group.mat_mul(Dcols, Finv)
    # verify
    for i in range(3):
        img = group.mat_vec(M, f[i])
        lam = pg.GF_MUL[beta[i]][pg.GF_INV[alpha[i]]]
        expect = tuple(pg.GF_MUL[lam][x] for x in d[i])
        assert img == expect, (i, img, expect)
    img4 = group.mat_vec(M, f[3])
    assert img4 == d[3], (img4, d[3])
    return M


def main():
    t0 = time.time()
    n, b, blocks = pg.load_board()
    m_points, m_index, m_lines = pg.build_model()
    phi, _, _, _ = pg.find_isomorphism(n, blocks, m_points, m_lines)

    mats, model_perms, board_perms = group.board_generators(
        m_points, m_index, phi
    )
    gen_check = []
    for i, (M, pm, pb) in enumerate(zip(mats, model_perms, board_perms)):
        gen_check.append(
            {
                "index": i,
                "matrix": list(M),
                "det": group.mat_det(M),
                "invertible": group.mat_det(M) != 0,
                "model_perm_ok": sorted(pm) == list(range(91)),
                "board_lines_preserved": group.is_line_permutation(pb, blocks),
            }
        )
    print("generators:", len(mats))
    print("all generators are collineations:",
          all(x["board_lines_preserved"] for x in gen_check))

    # group orders
    gl_order = (9 ** 3 - 1) * (9 ** 3 - 9) * (9 ** 3 - 9 ** 2)
    pgl_order = gl_order // 8
    frame_count_formula = 91 * 90 * 81 * 64
    print("|GL(3,9)| =", gl_order)
    print("|PGL(3,9)| =", pgl_order)
    print("91*90*81*64 =", frame_count_formula)
    assert pgl_order == frame_count_formula == 42456960

    # ordered frames: every 3-cap has exactly 64 extensions
    t1 = time.time()
    tot3, counts, tot_frames = group.count_ordered_triples_extensions(n, blocks)
    print("ordered 3-caps:", tot3, "extension histogram:", counts,
          "ordered frames:", tot_frames, "seconds:", round(time.time() - t1, 2))
    assert tot3 == 91 * 90 * 81 == 663390
    assert counts == {64: 663390}
    assert tot_frames == 42456960

    # sharp transitivity: random frame pairs mapped by a unique projectivity
    rng = random.Random(20261128)
    game_ = game.CapGame(n, blocks)
    # use model points as vectors for linear algebra, and model frame list
    frame_tests = 0
    for _ in range(30):
        f = None
        d = None
        while f is None:
            cand = rng.sample(range(91), 4)
            if game_.is_cap(sum(1 << p for p in cand)):
                f = cand
        while d is None:
            cand = rng.sample(range(91), 4)
            if game_.is_cap(sum(1 << p for p in cand)):
                d = cand
        fv = [m_points[phi[p]] for p in f]
        dv = [m_points[phi[p]] for p in d]
        M = frame_projectivity(fv, dv)
        assert group.mat_det(M) != 0
        # unique: the solution matrix is determined; check its induced map
        pm = group.matrix_perm(M, m_points, m_index)
        for i in range(4):
            assert pm[phi[f[i]]] == phi[d[i]], (f, d, i)
        frame_tests += 1
    print("random frame pairs mapped by projectivity:", frame_tests)

    # orbit BFS
    orbit_start = {
        1: (0,),
        2: (0, 1),
        3: (0, 1, 10),
        4: (0, 1, 10, 20),
    }
    expected = {1: 91, 2: 4095, 3: 110565, 4: 1769040}
    orbits = {}
    for k in (1, 2, 3, 4):
        t1 = time.time()
        st = orbit_start[k]
        assert game_.is_cap(sum(1 << p for p in st))
        sz = group.orbit_size(st, board_perms, k)
        dt = time.time() - t1
        print(f"orbit k={k}: {sz} (expected {expected[k]}) {dt:.1f}s")
        orbits[str(k)] = {"start": list(st), "size": sz,
                          "expected": expected[k], "seconds": round(dt, 2)}
        assert sz == expected[k]

    out = {
        "generators": gen_check,
        "group_orders": {
            "GL": gl_order,
            "PGL": pgl_order,
            "ordered_frames_formula": frame_count_formula,
        },
        "ordered_triples": {
            "count": tot3,
            "extension_histogram": {str(k): v for k, v in counts.items()},
            "ordered_frames": tot_frames,
        },
        "sharp_transitivity_random_pairs": frame_tests,
        "orbits": orbits,
        "seconds": round(time.time() - t0, 3),
    }
    (pg.HERE / "out").mkdir(exist_ok=True)
    (pg.HERE / "out" / "t3_group.json").write_text(
        json.dumps(out, indent=1), encoding="utf-8"
    )
    print("total seconds:", out["seconds"])


if __name__ == "__main__":
    main()
