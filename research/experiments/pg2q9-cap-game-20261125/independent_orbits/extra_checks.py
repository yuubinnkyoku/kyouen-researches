"""extra_checks.py -- supplementary independent cross-checks.

 1. Census robustness: run the frame-DSF census for a SECOND, unrelated
    projective frame; the per-frame counts must be identical (frame-transitivity).
 2. Every maximal k-cap through the fixed frame lies in the start cap's orbit
    (explicit projectivity for each; sampled for k=8 because of cost).
 3. Structural identities of the census:
       total 9-caps = 10 * #conics,  non-maximal 8-caps = 45 * #conics,
       total 8-caps = maximal 8-caps + 45 * #conics,
       total maximal caps = sum over sizes.
 4. Every 9-cap through the frame extends to a conic; every non-maximal 8-cap
    through the frame is contained in a conic through the frame.
 5. Group-order arguments:
       |SL(3,9)| = |GL(3,9)|/8 = 42,456,960 = |PGL(3,9)|;
       cubing is a bijection of GF(9)^*, so GL = SL . Z and PGL = PSL = SL;
       gcd(60, 21, 8, 720) = 1, hence a subgroup whose orbits on all four
       families have the full sizes must be all of PGL(3,9).

Run:  python extra_checks.py
"""

from __future__ import annotations

import itertools
import json
import math
import time

import common
import pgcore as pc


def exists_element(M, c1, c2):
    """Is there a projectivity mapping the point set c1 onto c2?  (explicit search)"""
    c1 = sorted(c1)
    c2 = sorted(c2)
    f = next(pc.ordered_frames(c1, M))
    fv = [M.vectors[p] for p in f]
    for d in pc.ordered_frames(c2, M):
        A = pc.solve_frame_map(fv, [M.vectors[p] for p in d])
        if A is None:
            continue
        perm = pc.mat_perm(M, A)
        if sorted(perm[p] for p in c1) == c2:
            return True
    return False


def main():
    t00 = time.time()
    out = {}
    M, B, phi = common.setup()
    inv = [0] * M.n
    for b, m in enumerate(phi):
        inv[m] = b

    # ---------------------------------------------------------------- 1
    print("== 1. census for a second frame ==")
    f1 = pc.pick_frame(M)
    # a second, unrelated frame (first 4-subset different from f1 with no collinear triple)
    f1s = tuple(sorted(f1))
    f2 = None
    for quad in itertools.combinations(range(M.n), 4):
        if quad == f1s:
            continue
        if len({M.line_through(a, b) for a, b in itertools.combinations(quad, 2)}) == 6:
            f2 = quad
            break
    assert f2 is not None
    c1 = pc.frame_caps(M, f1, maxk=10)
    c2 = pc.frame_caps(M, f2, maxk=10)
    same = all(len(c1[k]) == len(c2[k]) for k in range(4, 11))
    maxsame = all(sum(1 for C, f in c1[k] if f == M.n) == sum(1 for C, f in c2[k] if f == M.n)
                  for k in range(4, 11))
    out["framecounts"] = {
        "frame1": {k: len(c1[k]) for k in range(4, 11)},
        "frame2": {k: len(c2[k]) for k in range(4, 11)},
        "maximal_frame1": {k: sum(1 for C, f in c1[k] if f == M.n) for k in range(4, 11)},
        "maximal_frame2": {k: sum(1 for C, f in c2[k] if f == M.n) for k in range(4, 11)},
        "identical": same and maxsame,
    }
    print(f"  frame1 = {f1}: caps/frame {[len(c1[k]) for k in range(4, 11)]}")
    print(f"  frame2 = {f2}: caps/frame {[len(c2[k]) for k in range(4, 11)]}")
    print(f"  identical per-frame counts: {same and maxsame}")

    # ---------------------------------------------------------------- 2
    print("\n== 2. every maximal k-cap through the frame is in the start orbit ==")
    res2 = {}
    for k, take in ((6, None), (7, None), (8, 5), (10, None)):
        start = common.model_cap(phi, common.STARTS[k])
        targets = [sorted(C) for C, fsz in c1[k] if fsz == M.n and sorted(C) != start]
        if take is not None:
            targets = targets[:take]
        t0 = time.time()
        hits = [exists_element(M, start, t) for t in targets]
        res2[k] = {"checked": len(targets), "in_orbit": sum(hits),
                   "seconds": round(time.time() - t0, 1)}
        print(f"  k={k:2d}: {sum(hits)}/{len(targets)} other maximal {k}-caps through the frame "
              f"are projectively equivalent to the start cap [{time.time() - t0:.1f}s]")
    out["other_caps_in_orbit"] = res2

    # ---------------------------------------------------------------- 3
    print("\n== 3. structural identities ==")
    nframes = 1769040
    T = {k: len(c1[k]) for k in range(4, 11)}
    m = {k: sum(1 for C, f in c1[k] if f == M.n) for k in range(4, 11)}
    C4 = {k: math.comb(k, 4) for k in range(4, 11)}
    total = {k: nframes * T[k] // C4[k] for k in range(4, 11)}
    maximal = {k: nframes * m[k] // C4[k] for k in range(4, 11)}
    ncon = 9 ** 5 - 9 ** 2
    ident = {
        "total_caps": total,
        "maximal_caps": maximal,
        "conics": ncon,
        "caps10_eq_conics": total[10] == ncon,
        "caps9_eq_10x_conics": total[9] == 10 * ncon,
        "nonmax8_eq_45x_conics": total[8] - maximal[8] == math.comb(10, 8) * ncon,
        "total8_eq_max8_plus_45conics": total[8] == maximal[8] + 45 * ncon,
        "maximal_total": sum(maximal.values()),
        "parent_maximal_total": 8095464,
        "all_caps_total": sum(total.values()) + (1 + 91 + 4095 + 110565),
        "parent_all_caps_total": 128917712,
    }
    out["identities"] = ident
    for key in ("caps10_eq_conics", "caps9_eq_10x_conics", "nonmax8_eq_45x_conics",
                "total8_eq_max8_plus_45conics"):
        print(f"  {key}: {ident[key]}")
    print(f"  maximal caps total = {ident['maximal_total']:,d} "
          f"(parent analysis.json: {ident['parent_maximal_total']:,d})")
    print(f"  all caps total = {ident['all_caps_total']:,d} "
          f"(parent analysis.json: {ident['parent_all_caps_total']:,d})")

    # ---------------------------------------------------------------- 4
    print("\n== 4. 9-caps and non-maximal 8-caps live in conics ==")
    conics_through_frame = [frozenset(C) for C, fsz in c1[10] if fsz == M.n]
    nine = [frozenset(C) for C, fsz in c1[9]]
    eight_nonmax = [frozenset(C) for C, fsz in c1[8] if fsz != M.n]
    nine_ok = all(any(C <= K for K in conics_through_frame) for C in nine)
    eight_ok = all(any(C <= K for K in conics_through_frame) for C in eight_nonmax)
    out["nine_in_conic"] = {"n": len(nine), "all_in_conic": nine_ok}
    out["nonmax8_in_conic"] = {"n": len(eight_nonmax), "all_in_conic": eight_ok}
    print(f"  {len(nine)} 9-caps through the frame, all inside one of the "
          f"{len(conics_through_frame)} conics through the frame: {nine_ok}")
    print(f"  {len(eight_nonmax)} non-maximal 8-caps through the frame, all inside such a "
          f"conic: {eight_ok}")

    # ---------------------------------------------------------------- 5
    print("\n== 5. group-order arguments ==")
    q = 9
    gl = (q ** 3 - 1) * (q ** 3 - q) * (q ** 3 - q ** 2)
    sl = gl // (q - 1)
    cubes = {pc._pow(a, 3) for a in range(1, 9)}
    gcd4 = math.gcd(math.gcd(60, 21), math.gcd(8, 720))
    arg = {
        "gl": gl, "sl": sl, "pgl_frame_count": 24 * nframes,
        "sl_equals_pgl": sl == 24 * nframes,
        "cubes_of_GF9star": sorted(cubes),
        "cubing_is_bijection": cubes == set(range(1, 9)),
        "gcd_60_21_8_720": gcd4,
        "conclusion": ("|SL(3,9)| = |GL|/8 = |PGL(3,9)|; cubing is a bijection of GF(9)^*, "
                       "so GL = SL.Z and PGL = PSL = SL.  Hence the 12 elementary "
                       "transvections generate all of PGL(3,9); and because "
                       "gcd(60,21,8,720) = 1, any subgroup whose orbits on the four "
                       "families have the full sizes must equal PGL(3,9).")
    }
    out["group_order_argument"] = arg
    print(f"  |GL(3,9)| = {gl:,d}; |SL(3,9)| = {sl:,d}; |PGL| = 24*#frames = {24 * nframes:,d}")
    print(f"  cubing on GF(9)^* is a bijection: {arg['cubing_is_bijection']} ({sorted(cubes)})")
    print(f"  gcd(60,21,8,720) = {gcd4}")

    # ---------------------------------------------------------------- 6
    print("\n== 6. the 720-element stabilizer is PGL(2,9), not S6 ==")
    from collections import Counter

    def mul2(X, Y):
        return ((pc.ADD[pc.MUL[X[0][0]][Y[0][0]]][pc.MUL[X[0][1]][Y[1][0]]],
                 pc.ADD[pc.MUL[X[0][0]][Y[0][1]]][pc.MUL[X[0][1]][Y[1][1]]]),
                (pc.ADD[pc.MUL[X[1][0]][Y[0][0]]][pc.MUL[X[1][1]][Y[1][0]]],
                 pc.ADD[pc.MUL[X[1][0]][Y[0][1]]][pc.MUL[X[1][1]][Y[1][1]]]))

    def is_scalar(X):
        return X[0][1] == 0 and X[1][0] == 0 and X[0][0] == X[1][1]

    hists = Counter()
    ngl = 0
    for a, b, c, d in itertools.product(range(9), repeat=4):
        if pc.ADD[pc.MUL[a][d]][pc.NEG[pc.MUL[b][c]]] == 0:
            continue
        ngl += 1
        X = ((a, b), (c, d))
        k = 1
        while not is_scalar(X):
            X = mul2(X, ((a, b), (c, d)))
            k += 1
        hists[k] += 1
    pgl29 = {k: v // 8 for k, v in sorted(hists.items())}
    # stabilizer histogram from task5's enumeration
    d5 = json.loads((pc.RESULTS / "task5_stabilizers.json").read_text(encoding="utf-8"))
    stab10 = {int(k): v for k, v in d5["caps"]["10"]["element_order_histogram"].items()}
    s6_orders = {1: 1, 2: 75, 3: 80, 4: 180, 5: 144, 6: 240}
    out["pgl29"] = {
        "order": ngl // 8,
        "element_order_histogram": pgl29,
        "stabilizer20_order_histogram": stab10,
        "histograms_agree": pgl29 == stab10,
        "s6_element_order_histogram": s6_orders,
        "stabilizer_is_not_S6": pgl29 != s6_orders,
    }
    print(f"  |PGL(2,9)| = {ngl // 8} from {ngl} 2x2 matrices; element orders {pgl29}")
    print(f"  720-element cap stabilizer element orders: {stab10}; agree = {pgl29 == stab10}")
    print(f"  S6 would have orders {s6_orders}; the stabilizer is NOT S6: {pgl29 != s6_orders}")

    ok = (same and maxsame and all(v["in_orbit"] == v["checked"] for v in res2.values())
          and ident["caps10_eq_conics"] and ident["caps9_eq_10x_conics"]
          and ident["nonmax8_eq_45x_conics"] and nine_ok and eight_ok
          and arg["cubing_is_bijection"] and arg["sl_equals_pgl"] and gcd4 == 1
          and out["pgl29"]["histograms_agree"] and out["pgl29"]["stabilizer_is_not_S6"])
    out["PASS"] = ok
    out["elapsed_s"] = round(time.time() - t00, 1)
    pc.RESULTS.mkdir(parents=True, exist_ok=True)
    (pc.RESULTS / "extra_checks.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nEXTRA CHECKS: {'PASS' if ok else 'FAIL'}   ({out['elapsed_s']} s)")
    return out


if __name__ == "__main__":
    main()
