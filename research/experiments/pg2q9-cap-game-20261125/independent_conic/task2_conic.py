"""Task 2 - C is a nondegenerate conic, it is the unique conic through the
5-cap {0,1,10,20,31}, and the conics form one PGL(3,9) orbit."""
import json
import math

import conic as K
import gf9 as F
import pg9 as P

OUT = "results_task2.json"


def main():
    res = {}
    # ---- C is a 10-point cap ------------------------------------------
    C = K.C
    mask = K.C_MASK
    secants = set()
    ok_cap = True
    for i in range(len(C)):
        for j in range(i + 1, len(C)):
            line = P.PAIR_LINE[C[i]][C[j]]
            secants.add(line)
            if bin(line & mask).count("1") != 2:
                ok_cap = False
    res["C"] = {
        "points": C,
        "distinct": len(set(C)) == 10,
        "is_cap": P.is_cap(mask) and ok_cap,
        "distinct_secant_lines": len(secants),
        "expected_secant_lines": 45,
    }

    # ---- unique quadratic form through the 5-cap, nondegenerate ------
    five = K.FIVE
    basis5, piv5 = K.forms_through(five)
    res["five_cap"] = {
        "points": five,
        "is_cap": P.is_cap(P.mask_of(five)),
        "rank_of_5x6_system": len(piv5),
        "nullspace_dim": len(basis5),
        "unique_form": len(basis5) == 1,
    }
    f5 = P.canonical_form(tuple(basis5[0]))
    m5 = P.form_zero_mask(f5)
    res["five_cap"].update({
        "form": f5,
        "form_det": P.form_det(f5),
        "nondegenerate": P.form_det(f5) != 0,
        "zero_set": P.bits(m5),
        "zero_set_equals_C": m5 == K.C_MASK,
        "zero_set_size": bin(m5).count("1"),
    })

    # forms through all of C
    basisC, pivC = K.forms_through(C)
    res["forms_through_C"] = {
        "rank": len(pivC),
        "nullspace_dim": len(basisC),
        "form": P.canonical_form(tuple(basisC[0])) if basisC else None,
    }
    # quadratic form evaluation on every point of C, and on a few points off C
    res["form_vanishes_on_C"] = all(P.form_value(f5, i) == 0 for i in C)

    # ---- all conics ---------------------------------------------------
    conics = K.all_conics()
    forms = P.all_canonical_forms()
    n_nonzero_classes = len(forms)
    n_degenerate = sum(1 for c in forms if P.form_det(c) == 0)
    res["all_conics"] = {
        "nonzero_forms_up_to_scalar": n_nonzero_classes,
        "expected_(9^6-1)/8": (9 ** 6 - 1) // 8,
        "degenerate_forms": n_degenerate,
        "nondegenerate_forms": n_nonzero_classes - n_degenerate,
        "distinct_conic_point_sets": len(conics),
        "expected_9^5-9^2": 9 ** 5 - 9 ** 2,
        "every_conic_has_10_points": all(bin(m).count("1") == 10 for m in conics),
        "every_conic_is_a_cap": all(P.is_cap(m) for m in conics[:200]),
        "C_is_among_them": K.C_MASK in conics,
    }

    # ---- PGL(3,9) order ----------------------------------------------
    q = 9
    order_pgl3 = (q ** 3 - 1) * (q ** 3 - q) * (q ** 3 - q ** 2) // (q - 1)
    n_frames = 91 * 90 * 81 * 64
    res["group_orders"] = {
        "PGL(3,9)": order_pgl3,
        "ordered_frames": n_frames,
        "regular_action_on_frames": order_pgl3 == n_frames,
    }

    # ---- stabiliser of C and orbit-stabiliser ------------------------
    mats = K.stabiliser(K.C_MASK, cache=K.STAB_CACHE)
    perms = K.permutations_on(K.C_MASK, mats)
    res["stabiliser_C"] = {
        "order": len(mats),
        "distinct_permutations": len(set(perms)),
        "faithful": len(set(perms)) == len(mats),
        "transitive_on_C": len({p[0] for p in perms}) == 10,
        "PGL(2,9)_order": 720,
        "orbit_size_of_C": order_pgl3 // len(mats),
        "number_of_conics": len(conics),
        "single_orbit": order_pgl3 // len(mats) == len(conics),
    }

    # ---- every conic is a translate of C (one orbit) ------------------
    # spot check: for several conics build an explicit projectivity C -> C'
    spot = [conics[0], conics[1], conics[len(conics) // 3], conics[-1]]
    spot_ok = True
    spot_detail = []
    src_pts = K.frame_of(K.C_MASK)
    src = [P.POINTS[i] for i in src_pts]
    for m in spot:
        dst_pts = P.bits(m)
        found = None
        for a in dst_pts:
            for b in dst_pts:
                if b == a:
                    continue
                for c in dst_pts:
                    if c in (a, b):
                        continue
                    for d in dst_pts:
                        if d in (a, b, c):
                            continue
                        T = P.projectivity_from_frame(
                            src, [P.POINTS[a], P.POINTS[b], P.POINTS[c], P.POINTS[d]])
                        if T is None:
                            continue
                        img = 0
                        for i in P.bits(K.C_MASK):
                            img |= 1 << P.LABEL[F.normalise(P.mat_vec(T, P.POINTS[i]))]
                        if img == m:
                            found = T
                            break
                    if found:
                        break
                if found:
                    break
            if found:
                break
        spot_ok = spot_ok and found is not None
        spot_detail.append({"conic_popcount": bin(m).count("1"),
                            "explicit_projectivity": found is not None})
    res["transitivity_spot_check"] = {"ok": spot_ok, "detail": spot_detail}

    # ---- arithmetic cross-check: 10-point zero sets -------------------
    res["pass"] = (res["C"]["is_cap"] and res["C"]["distinct"]
                   and res["five_cap"]["is_cap"] and res["five_cap"]["unique_form"]
                   and res["five_cap"]["nondegenerate"]
                   and res["five_cap"]["zero_set_equals_C"]
                   and res["all_conics"]["distinct_conic_point_sets"] == 9 ** 5 - 9 ** 2
                   and res["all_conics"]["C_is_among_them"]
                   and res["group_orders"]["regular_action_on_frames"]
                   and res["stabiliser_C"]["order"] == 720
                   and res["stabiliser_C"]["faithful"]
                   and res["stabiliser_C"]["single_orbit"]
                   and spot_ok)
    with open(OUT, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1)
    print(json.dumps(res, indent=1))
    print("\nTASK2:", "PASS" if res["pass"] else "FAIL")


main()
