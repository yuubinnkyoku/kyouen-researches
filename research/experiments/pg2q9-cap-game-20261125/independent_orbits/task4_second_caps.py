"""Task 4 -- cross-check transitivity: for each cap size construct a SECOND
maximal cap by a method independent of the group, then exhibit an explicit
element of PGL(3,9) mapping the start cap onto it.

Second caps are built independently of any group action:
  (i)  incidence DFS: all maximal k-caps containing a fixed projective frame
       (a pure incidence construction in the model plane, no group action);
  (ii) random greedy growth in the board plane (pure incidence, no coordinates);
  (iii) for k = 10 additionally the conic x^2 + y^2 + z^2 = 0.

Explicit group element: fix an ordered projective frame f inside the start cap
and enumerate ordered frames d of the second cap; for each pair solve the
12x13 homogeneous linear system A f_i = lam_i d_i over GF(9) (13 unknowns:
9 entries of A and 4 scalars).  Every solution A is a genuine element of
PGL(3,9) = GL(3,9)/scalars; keep the ones with A(start cap) = second cap.
The number of such A is |Stab(start cap)|, an independent handle on task 5.

Run:  python task4_second_caps.py
"""

from __future__ import annotations

import itertools
import json
import random
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


def greedy_cap(P, rng):
    """Random greedy maximal cap in the plane P (incidence only)."""
    order = list(range(P.n))
    rng.shuffle(order)
    cap = []
    cs = set()
    for q in order:
        if all(len(cs & set(P.lines[l])) <= 1 for l in P.point_lines[q]):
            cap.append(q)
            cs.add(q)
    return sorted(cap)


def find_group_elements(M, c1, c2):
    """All A in GL(3,9) (up to scalar) with A(c1) = c2 as point sets."""
    c1 = sorted(c1)
    c2 = sorted(c2)
    f = next(pc.ordered_frames(c1, M))
    fv = [M.vectors[p] for p in f]
    hits = []
    for d in pc.ordered_frames(c2, M):
        dv = [M.vectors[p] for p in d]
        A = pc.solve_frame_map(fv, dv)
        if A is None:
            continue
        perm = pc.mat_perm(M, A)
        if sorted(perm[p] for p in c1) == c2:
            hits.append((A, perm, d))
    return hits


def main():
    t00 = time.time()
    out = {}
    M, B, phi = common.setup()
    inv = [0] * M.n
    for b, m in enumerate(phi):
        inv[m] = b
    frame = pc.pick_frame(M)
    print(f"setup ok; fixed projective frame = {frame} (model labels)")

    # (i) incidence DFS: all maximal caps containing the frame, by size
    capmap = pc.frame_caps(M, frame, maxk=10)
    maximal_by_size = {k: [sorted(C) for C, fsz in capmap[k] if fsz == M.n]
                       for k in range(5, 11)}
    print("maximal caps through the frame, by size: "
          + ", ".join(f"k={k}:{len(v)}" for k, v in maximal_by_size.items()))

    # (ii) random-greedy pool, board plane (incidence only, no coordinates)
    rng = random.Random(424242)
    pool = {}
    t0 = time.time()
    for _ in range(400):
        c = greedy_cap(B, rng)
        pool.setdefault(len(c), []).append(c)
    print(f"400 random greedy maximal caps on the board plane in {time.time() - t0:.1f}s; sizes: "
          + ", ".join(f"{k}:{len(v)}" for k, v in sorted(pool.items())))

    # (iii) conic x^2+y^2+z^2 = 0 (independent algebraic construction of a 10-cap)
    Acon = pc.quad_form_matrix((1, 1, 1, 0, 0, 0))
    conic10 = pc.conic_point_set(M, Acon)
    conic_rec = {
        "form": "x^2 + y^2 + z^2", "nonsingular": pc.det3(Acon) != 0,
        "size": len(conic10), "is_cap": is_cap(M, conic10),
        "is_maximal": is_maximal(M, conic10),
        "model_points": conic10, "board_points": sorted(inv[p] for p in conic10),
    }
    out["conic_10cap"] = conic_rec
    print(f"conic x^2+y^2+z^2: size={len(conic10)} cap={conic_rec['is_cap']} "
          f"maximal={conic_rec['is_maximal']} nonsingular={conic_rec['nonsingular']}")

    out["caps"] = {}
    for k in (6, 7, 8, 10):
        start_board = common.STARTS[k]
        start_model = common.model_cap(phi, start_board)
        second, source = None, None
        for C in maximal_by_size[k]:
            if C != start_model:
                second, source = C, "incidence DFS through a fixed frame"
                break
        if second is None:
            for C in pool.get(k, []):
                mc = sorted(phi[p] for p in C)
                if mc != start_model:
                    second, source = mc, "random greedy growth on the board plane"
                    break
        if k == 10 and sorted(conic10) != start_model and second is not None:
            # record the conic as an extra, independently built 10-cap
            extras = find_group_elements(M, start_model, conic10)
            out.setdefault("extra_10cap_check", {})["n_solutions"] = len(extras)
            out["extra_10cap_check"]["maps"] = bool(extras)
            print(f"  extra check: conic x^2+y^2+z^2 lies in the start orbit "
                  f"({len(extras)} explicit elements found): {bool(extras)}")

        rec = {"start_board": start_board, "start_model": start_model,
               "second_board": sorted(inv[p] for p in second),
               "second_model": second, "constructed_by": source,
               "different_from_start": second != start_model,
               "second_is_cap": is_cap(M, second),
               "second_is_maximal": is_maximal(M, second),
               "second_size": len(second)}
        t0 = time.time()
        hits = find_group_elements(M, start_model, second)
        dt = time.time() - t0
        rec["n_explicit_elements"] = len(hits)
        rec["n_explicit_elements_equals_claimed_stab"] = (len(hits) == common.CLAIM_STAB[k])
        rec["expected_stabilizer_order"] = common.CLAIM_STAB[k]
        if hits:
            A, perm, d = hits[0]
            rec["explicit_matrix"] = A
            rec["det"] = pc.det3(A)
            rec["maps_start_to_second_model"] = sorted(perm[p] for p in start_model) == second
            board_perm = [inv[perm[phi[b]]] for b in range(B.n)]
            rec["board_permutation"] = board_perm
            rec["maps_start_to_second_board"] = (
                sorted(board_perm[p] for p in start_board) == rec["second_board"])
            rec["board_permutation_is_bijection"] = sorted(board_perm) == list(range(B.n))
            rec["board_perm_preserves_all_lines"] = all(
                tuple(sorted(board_perm[p] for p in L)) in B.line_index for L in B.lines)
        rec["seconds"] = round(dt, 2)
        out["caps"][k] = rec
        print(f"  k={k:2d}: second cap {rec['second_board']} (by {source}); "
              f"cap={rec['second_is_cap']} maximal={rec['second_is_maximal']}; "
              f"{len(hits)} explicit group elements map start -> second "
              f"(claimed |Stab| = {common.CLAIM_STAB[k]}); "
              f"board-line-preserving = {rec.get('board_perm_preserves_all_lines')} "
              f"[{dt:.1f}s]", flush=True)

    ok = (conic_rec["is_cap"] and conic_rec["is_maximal"] and conic_rec["nonsingular"]
          and all(r["different_from_start"] and r["second_is_cap"] and r["second_is_maximal"]
                  and r.get("maps_start_to_second_model")
                  and r.get("maps_start_to_second_board")
                  and r.get("board_perm_preserves_all_lines")
                  and r.get("board_permutation_is_bijection")
                  for r in out["caps"].values()))
    out["PASS"] = ok
    out["elapsed_s"] = round(time.time() - t00, 1)
    pc.RESULTS.mkdir(parents=True, exist_ok=True)
    (pc.RESULTS / "task4_second_caps.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nTASK 4: {'PASS' if ok else 'FAIL'}   ({out['elapsed_s']} s)")
    return out


if __name__ == "__main__":
    main()
