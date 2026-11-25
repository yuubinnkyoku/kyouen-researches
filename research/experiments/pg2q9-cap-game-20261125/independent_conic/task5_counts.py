"""Task 5 - incidence / distinct cap counts around the conic layer.

Checks
  * 3-caps: 110,565, each on 64 conics (local computation + PGL(3,9)
    transitivity on non-collinear triples), incidence 58,968*120 = 7,076,160.
  * 4-caps: 1,769,040, each on 7 conics, incidence 58,968*210 = 12,383,280.
  * 5-caps: 14,859,936 (computed without conics), each on exactly one conic,
    so 58,968*252 = 14,859,936 and the PGL(2,9) split 180/72 gives
    58,968*180 = 10,614,240 and 58,968*72 = 4,245,696.
  * k=6,7,8,9: 58,968*C(10,k) = 12,383,280 / 7,076,160 / 2,653,560 / 589,680;
    every 9-cap is conic (4-cap argument gives 589,680 = 58,968*10).
"""
import json
import random

import conic as K
import gf9 as F
import pg9 as P

OUT = "results_task5.json"
FULL = P.FULL
C3 = 110565
C4 = 1769040
C5 = 14859936
NCONIC = 58968


def conics_through_pts(pts):
    """Return (all_forms, nondegenerate_forms, zero_masks_nondegenerate)."""
    basis, piv = K.forms_through(pts)
    forms = []
    for b in basis:
        forms.append(tuple(b))
    return basis, piv


def count_conics_containing(mask, conics):
    return sum(1 for m in conics if (m & mask) == mask)


def all_forms_through(pts):
    """All quadratic forms (canonical) through the points, as coefficient tuples."""
    basis, _ = K.forms_through(pts)
    out = set()
    k = len(basis)
    for code in range(9 ** k):
        coef = []
        t = code
        for _ in range(k):
            coef.append(t % 9)
            t //= 9
        if all(x == 0 for x in coef):
            continue
        v = [0] * 6
        for ci, cv in enumerate(coef):
            if cv:
                for i in range(6):
                    v[i] = F.ADD[v[i]][F.MUL[cv][basis[ci][i]]]
        cf = P.canonical_form(tuple(v))
        if cf is not None:
            out.add(cf)
    return sorted(out)


def main():
    res = {}
    conics = K.all_conics()
    res["inputs"] = {"conics": len(conics), "3caps": C3, "4caps": C4,
                     "5caps": C5}

    # ---- 3-caps: count and extension distribution ---------------------
    n3 = 0
    ext3 = {}
    sum4 = 0
    for a in range(91):
        for b in range(a + 1, 91):
            lab = P.PAIR_LINE[a][b]
            La, Lb = P.PAIR_LINE[a], P.PAIR_LINE[b]
            for c in range(b + 1, 91):
                if (lab >> c) & 1:
                    continue
                n3 += 1
                f = lab | La[c] | Lb[c]
                allow = FULL & ~f
                k = allow.bit_count()
                ext3[k] = ext3.get(k, 0) + 1
                sum4 += k
    res["three_caps"] = {
        "count": n3,
        "expected_110565": n3 == C3,
        "closed_form": 121485 - 91 * 120,
        "extension_count_distribution": ext3,
        "every_3cap_has_64_extensions": list(ext3) == [64],
        "pairs_(3cap,4th_point)": sum4,
        "4caps_derived": sum4 // 4,
    }

    # ---- 4-caps: extension distribution -------------------------------
    ext4 = {}
    sum5 = 0
    for a in range(91):
        for b in range(a + 1, 91):
            lab = P.PAIR_LINE[a][b]
            La, Lb = P.PAIR_LINE[a], P.PAIR_LINE[b]
            for c in range(b + 1, 91):
                if (lab >> c) & 1:
                    continue
                f = lab | La[c] | Lb[c]
                allow = FULL & ~f
                Lc = P.PAIR_LINE[c]
                x = allow
                while x:
                    bb = x & -x
                    x ^= bb
                    p = bb.bit_length() - 1
                    f4 = f | P.PAIR_LINE[p][a] | P.PAIR_LINE[p][b] | Lc[p]
                    e = (FULL & ~f4).bit_count()
                    ext4[e] = ext4.get(e, 0) + 1
                    sum5 += e
    res["four_caps"] = {
        "extension_count_distribution": ext4,
        "every_4cap_has_42_extensions": list(ext4) == [42],
        "sum_over(4cap,5th_point)": sum5,
        "5caps_derived": sum5 // 20,
        "expected_5caps": C5,
        "match": sum5 // 20 == C5,
    }

    # ---- local conic counts through a 3-cap, 4-cap, 5-cap -------------
    rnd = random.Random(20261125)
    sample3 = []
    while len(sample3) < 8:
        s = tuple(sorted(rnd.sample(range(91), 3)))
        if P.is_cap(P.mask_of(s)):
            sample3.append(s)
    sample3.append((0, 1, 10))
    c3_counts = {s: count_conics_containing(P.mask_of(s), conics) for s in sample3}
    res["three_cap_conic_counts"] = {
        "samples": {"%s" % (s,): c for s, c in c3_counts.items()},
        "all_64": set(c3_counts.values()) == {64},
    }

    sample4 = []
    while len(sample4) < 8:
        s = tuple(sorted(rnd.sample(range(91), 4)))
        if P.is_cap(P.mask_of(s)):
            sample4.append(s)
    sample4 += [(0, 1, 10, 20), (0, 1, 10, 45)]
    c4_counts = {s: count_conics_containing(P.mask_of(s), conics) for s in sample4}
    res["four_cap_conic_counts"] = {
        "samples": {"%s" % (s,): c for s, c in c4_counts.items()},
        "all_7": set(c4_counts.values()) == {7},
    }

    # 4-cap pencil: 10 conics, 7 nondegenerate, covering exactly the 42
    # extension points => every 5-cap lies on a conic.
    four = (0, 1, 10, 20)
    forms4 = all_forms_through(list(four))
    nondeg = [f for f in forms4 if P.form_det(f) != 0]
    deg = [f for f in forms4 if P.form_det(f) == 0]
    allowed4 = P.allowed(P.mask_of(four))
    cover = 0
    cover_conflict = 0
    for f in nondeg:
        m = P.form_zero_mask(f)
        assert (m & P.mask_of(four)) == P.mask_of(four)
        extra = m & ~P.mask_of(four)
        if extra & cover:
            cover_conflict += 1
        cover |= extra
    res["four_cap_pencil"] = {
        "cap": list(four),
        "forms_through": len(forms4),
        "nondegenerate": len(nondeg),
        "degenerate": len(deg),
        "allowed_extension_points": allowed4.bit_count(),
        "covered_by_nondegenerate_conics": (cover & allowed4).bit_count(),
        "cover_equals_allowed": (cover & allowed4) == allowed4,
        "overlaps": cover_conflict,
        "conclusion": "every 5-cap containing this 4-cap lies on a conic",
    }

    # the two 5-cap orbit representatives: unique conic, nondegenerate
    five = []
    for s in ([0, 1, 10, 20, 31], [0, 1, 10, 20, 51]):
        basis, piv = K.forms_through(s)
        f = P.canonical_form(tuple(basis[0])) if len(basis) == 1 else None
        m = P.form_zero_mask(f) if f else 0
        five.append({
            "cap": s, "system_rank": len(piv), "forms": len(basis),
            "unique": len(basis) == 1,
            "nondegenerate": bool(f) and P.form_det(f) != 0,
            "zero_set_is_C": bool(f) and m == K.C_MASK,
            "extension_count": P.allowed(P.mask_of(s)).bit_count(),
        })
    res["five_cap_reps"] = five

    # ---- incidence arithmetic ----------------------------------------
    res["incidence_arithmetic"] = {
        "3": {"incidence": NCONIC * 120, "distinct_times_64": C3 * 64,
              "equal": NCONIC * 120 == C3 * 64 == 7076160},
        "4": {"incidence": NCONIC * 210, "distinct_times_7": C4 * 7,
              "equal": NCONIC * 210 == C4 * 7 == 12383280},
        "5": {"incidence": NCONIC * 252, "equals_5caps": NCONIC * 252 == C5,
              "split_180": NCONIC * 180, "split_72": NCONIC * 72,
              "split_sum": NCONIC * (180 + 72),
              "claim_180": 10614240, "claim_72": 4245696,
              "claim_sum": 10614240 + 4245696},
    }

    # ---- transitivity evidence: explicit projectivities ---------------
    def map_cap(T, cap):
        out = []
        for i in cap:
            out.append(P.LABEL[F.normalise(P.mat_vec(T, P.POINTS[i]))])
        return sorted(out)

    # 3-caps: map (0,1,10) to several random 3-caps (any two non-collinear
    # triples are bases of the 3-space, so the linear map exists)
    tri_ok = 0
    tri_tests = 0
    src3 = [P.POINTS[0], P.POINTS[1], P.POINTS[10]]
    Pm = P.mat_from_columns(*src3)
    for s in sample3:
        if s == (0, 1, 10):
            continue
        dst = [P.POINTS[i] for i in s]
        Qm = P.mat_from_columns(*dst)
        M = P.mat_normalize(P.mat_mul(Qm, P.mat_inv(Pm)))
        tri_tests += 1
        if map_cap(M, (0, 1, 10)) == sorted(s):
            tri_ok += 1
    res["transitivity_3caps"] = {"tests": tri_tests, "ok": tri_ok,
                                 "all": tri_ok == tri_tests}

    # 4-caps: map (0,1,10,20) to random 4-caps (frames)
    quad_tests = 0
    quad_ok = 0
    src4 = [P.POINTS[i] for i in (0, 1, 10, 20)]
    for s in sample4:
        if s == (0, 1, 10, 20):
            continue
        dst = [P.POINTS[i] for i in s]
        T = P.projectivity_from_frame(src4, dst)
        quad_tests += 1
        if T is not None and map_cap(T, (0, 1, 10, 20)) == sorted(s):
            quad_ok += 1
    res["transitivity_4caps"] = {"tests": quad_tests, "ok": quad_ok,
                                 "all": quad_ok == quad_tests}

    # ---- 9-caps: count via the 4-cap extension tree ------------------
    base = P.mask_of((0, 1, 10, 20))
    seen = {base}
    stack = [base]
    by_size = {}
    while stack:
        T = stack.pop()
        by_size[bin(T).count("1")] = by_size.get(bin(T).count("1"), 0) + 1
        a = P.allowed(T)
        while a:
            b = a & -a
            a ^= b
            U = T | b
            if U not in seen:
                seen.add(U)
                stack.append(U)
    n9 = by_size.get(9, 0)
    n10 = by_size.get(10, 0)
    # every 9-cap containing the 4-cap must be inside one of the 7 conics
    nine_sets = [m for m in seen if bin(m).count("1") == 9]
    inside_conic = all(any((m & Cmask) == m for Cmask in
                           [P.form_zero_mask(f) for f in nondeg]) for m in nine_sets)
    res["nine_caps"] = {
        "upset_of_fixed_4cap_by_size": dict(sorted(by_size.items())),
        "9caps_containing_the_4cap": n9,
        "expected_42": n9 == 42,
        "all_inside_one_of_the_7_conics": inside_conic,
        "total_9caps_formula": C4 * n9 // 126,
        "expected_589680": C4 * n9 // 126 == 589680,
        "conic_9_subsets": NCONIC * 10,
        "all_9caps_are_conic": C4 * n9 // 126 == NCONIC * 10,
    }

    # ---- k = 6,7,8,9 numbers -----------------------------------------
    res["k_ge_6_counts"] = {
        "6": {"incidence": NCONIC * 210, "claim": 12383280},
        "7": {"incidence": NCONIC * 120, "claim": 7076160},
        "8": {"incidence": NCONIC * 45, "claim": 2653560},
        "9": {"incidence": NCONIC * 10, "claim": 589680},
    }
    # cross-check: #6-caps = sum over 5-caps of extensions / 6.
    # extensions of a 5-cap are constant on PGL(3,9)-orbits (2 orbits).
    e1 = P.allowed(P.mask_of((0, 1, 10, 20, 31))).bit_count()
    e2 = P.allowed(P.mask_of((0, 1, 10, 20, 51))).bit_count()
    total6 = (10614240 * e1 + 4245696 * e2) // 6
    res["six_caps_cross_check"] = {
        "extensions_180_orbit": e1, "extensions_72_orbit": e2,
        "total_6caps_formula": total6,
        "parent_census_6caps": 52009776,
        "match": total6 == 52009776,
    }

    res["pass"] = (n3 == C3 and list(ext3) == [64] and sum4 // 4 == C4
                   and list(ext4) == [42] and sum5 // 20 == C5
                   and res["three_cap_conic_counts"]["all_64"]
                   and res["four_cap_conic_counts"]["all_7"]
                   and res["four_cap_pencil"]["nondegenerate"] == 7
                   and res["four_cap_pencil"]["cover_equals_allowed"]
                   and all(f["unique"] and f["nondegenerate"] for f in five)
                   and res["incidence_arithmetic"]["3"]["equal"]
                   and res["incidence_arithmetic"]["4"]["equal"]
                   and res["incidence_arithmetic"]["5"]["equals_5caps"]
                   and res["transitivity_3caps"]["all"]
                   and res["transitivity_4caps"]["all"]
                   and res["nine_caps"]["expected_42"]
                   and res["nine_caps"]["all_9caps_are_conic"])
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))
    print("\nTASK5:", "PASS" if res["pass"] else "FAIL")


main()
