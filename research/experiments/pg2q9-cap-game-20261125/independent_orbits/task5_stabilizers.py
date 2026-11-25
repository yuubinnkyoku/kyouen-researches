"""Task 5 -- stabilizers of the four start caps in PGL(3,9), and the consistency
of the claimed stabilizer orders with the orbit sizes and |PGL(3,9)|.

For each start cap C (transported to the model plane by the explicit
isomorphism), enumerate ALL g in PGL(3,9) with g(C) = C:

  fix one ordered projective frame f = (f1,f2,f3,f4) inside C and enumerate all
  ordered frames d of C; for each pair solve the 12x13 homogeneous system
  A f_i = lam_i d_i (13 unknowns: 9 entries of A, 4 scalars).  For two frames
  the solution space is exactly 1-dimensional, so A is a well defined element
  of GL(3,9) up to scalar.  Every g with g(C) = C produces exactly one
  d = g(f), so the number of successful d equals |Stab_PGL(C)|.

Reported per cap: |Stab|, comparison with |PGL|/orbit and with the claim,
element-order histogram, abelian/cyclic/perfect, derived subgroup, action
profile on the cap (transitivity degree), explicit matrices.
Identification: k=6 -> A5, k=7 -> C7:C3 (Frobenius 21), k=8 -> one of the five
groups of order 8, k=10 -> PGL(2,9) = S6 acting sharply 3-transitively.

Run:  python task5_stabilizers.py
"""

from __future__ import annotations

import itertools
import json
import time
from collections import Counter

import common
import pgcore as pc


def action_profile(perms, cap):
    """Transitivity data for the action of a permutation group on the cap."""
    out = {"cap_size": len(cap)}
    for k in (1, 2, 3):
        if k > len(cap):
            continue
        tup = tuple(cap[:k])
        images = {tuple(p[x] for x in tup) for p in perms}
        possible = 1
        for i in range(k):
            possible *= len(cap) - i
        out[f"distinct_images_of_ordered_{k}-tuple"] = len(images)
        out[f"possible_ordered_{k}-tuples"] = possible
    p0 = cap[0]
    stab_point = [p for p in perms if p[p0] == p0]
    out["point_stabilizer_order"] = len(stab_point)
    out["point_stabilizer_orbit_sizes"] = sorted({len({p[x] for p in stab_point}) for x in cap})
    out["is_transitive"] = len({p[cap[0]] for p in perms}) == len(cap)
    out["is_2_transitive"] = (len({tuple(p[x] for x in cap[:2]) for p in perms})
                              == len(cap) * (len(cap) - 1))
    out["is_3_transitive"] = (len({tuple(p[x] for x in cap[:3]) for p in perms})
                              == len(cap) * (len(cap) - 1) * (len(cap) - 2))
    out["sharply_3_transitive"] = (out["is_3_transitive"]
                                   and len(perms) == len(cap) * (len(cap) - 1) * (len(cap) - 2))
    out["fixed_point_counts"] = dict(sorted(Counter(
        len([x for x in cap if p[x] == x]) for p in perms).items()))
    return out


def structure(M, cap, perms):
    order = len(perms)
    n = M.n
    idp = pc.identity_perm(n)
    hist = Counter(pc.perm_order(p) for p in perms)
    gens, S = pc.small_generating_set(perms, n, order=order)
    abelian = all(pc.compose(g, h) == pc.compose(h, g) for g in gens for h in gens)
    der = pc.derived_subgroup_order(gens, n)
    prof = action_profile(perms, cap)
    return {
        "order": order,
        "n_distinct_permutations": len({tuple(p) for p in perms}),
        "element_order_histogram": {int(k): v for k, v in sorted(hist.items())},
        "n_involutions": hist.get(2, 0),
        "max_element_order": max(hist),
        "abelian": abelian,
        "cyclic": abelian and order == max(hist),
        "generating_set_size": len(gens),
        "generated_group_order_check": len(S),
        "derived_subgroup_order": der,
        "perfect": der == order,
        "action": prof,
    }


def main():
    t00 = time.time()
    out = {}
    M, B, phi = common.setup()
    inv = [0] * M.n
    for b, m in enumerate(phi):
        inv[m] = b

    orbit_sizes = dict(common.CLAIM_ORBIT)
    src = "claimed values (results/task3_orbits.json not found)"
    p3 = pc.RESULTS / "task3_orbits.json"
    if p3.exists():
        d3 = json.loads(p3.read_text(encoding="utf-8"))
        try:
            orbit_sizes = {int(k): v["orbit_size"] for k, v in d3["orbits"].items()}
            src = "own BFS (results/task3_orbits.json)"
        except Exception:
            pass
    out["orbit_sizes_source"] = src
    out["orbit_sizes"] = orbit_sizes
    pgl = 24 * 1769040
    out["pgl_order"] = pgl
    print(f"orbit sizes from: {src} -> {orbit_sizes}")
    print(f"|PGL(3,9)| = {pgl:,d}")

    out["caps"] = {}
    for k in (6, 7, 8, 10):
        cap = common.model_cap(phi, common.STARTS[k])
        t0 = time.time()
        stab = pc.stabilizer_elements(M, cap)
        dt = time.time() - t0
        perms = [p for (A, p) in stab]
        order = len({tuple(p) for p in perms})
        st = structure(M, cap, perms)
        rec = {
            "start_cap_board": common.STARTS[k],
            "start_cap_model": cap,
            "stabilizer_order": order,
            "claimed_stabilizer_order": common.CLAIM_STAB[k],
            "matches_claim": order == common.CLAIM_STAB[k],
            "orbit_size": orbit_sizes[k],
            "pgl_div_orbit": pgl // orbit_sizes[k],
            "pgl_div_stab": pgl // order if order else None,
            "orbit_stabilizer_product": order * orbit_sizes[k],
            "orbit_stabilizer_equals_pgl": order * orbit_sizes[k] == pgl,
            "enumeration_seconds": round(dt, 1),
        }
        rec.update(st)
        rec["examples"] = [
            {"matrix": A, "det": pc.det3(A),
             "order": pc.perm_order(p),
             "cycle_type_on_cap": pc.cycle_type_restricted(p, cap),
             "cycle_type_on_plane_moved": pc.cycle_type(p)[:6]}
            for (A, p) in stab[:6]]
        out["caps"][k] = rec
        print(f"  k={k:2d}: |Stab| = {order:4d} (claim {common.CLAIM_STAB[k]:4d}, match="
              f"{rec['matches_claim']}); |Stab|*orbit = {order * orbit_sizes[k]:,d} = |PGL|: "
              f"{rec['orbit_stabilizer_equals_pgl']}; element orders "
              f"{rec['element_order_histogram']}; abelian={rec['abelian']} "
              f"cyclic={rec['cyclic']} derived={rec['derived_subgroup_order']} "
              f"({dt:.1f}s)", flush=True)

    # ---- identification of the four stabilizers -------------------------
    ident = {}
    s6, s7, s8, s10 = (out["caps"][k] for k in (6, 7, 8, 10))
    if s6["order"] == 60:
        ident["k=6"] = (
            "A5 = PSL(2,5) (the simple group of order 60). Element orders "
            f"{s6['element_order_histogram']} = 1,15,20,24; perfect = {s6['perfect']}; "
            f"action on the 6 cap points transitive = {s6['action']['is_transitive']}, "
            f"2-transitive = {s6['action']['is_2_transitive']} "
            "(so the 6 points are P^1(5) with A5 acting as PSL(2,5)).")
    else:
        ident["k=6"] = f"order {s6['order']}"
    h7 = s7["element_order_histogram"]
    if s7["order"] == 21 and not s7["abelian"]:
        ident["k=7"] = (
            "Non-abelian group of order 21 = Frobenius group C7 : C3. "
            f"Element orders {h7}: {h7.get(7, 0)} elements of order 7 "
            "(a normal Sylow 7-subgroup) and "
            f"{h7.get(3, 0)} elements of order 3; abelian = False, "
            f"cyclic = {s7['cyclic']}, derived subgroup order {s7['derived_subgroup_order']}.")
    elif s7["order"] == 21:
        ident["k=7"] = f"abelian group of order 21, element orders {h7}"
    else:
        ident["k=7"] = f"order {s7['order']}"
    h8 = s8["element_order_histogram"]
    table8 = {
        (1, 1, 2, 4): "C8 (cyclic of order 8)",
        (1, 3, 4, 0): "C4 x C2",
        (1, 7, 0, 0): "C2 x C2 x C2",
        (1, 5, 2, 0): "D4 (dihedral of order 8)",
        (1, 1, 6, 0): "Q8 (quaternion group of order 8)",
    }
    key = (1,) + tuple(h8.get(o, 0) for o in (2, 4, 8))
    ident["k=8"] = (
        f"order 8, element orders {h8}, abelian = {s8['abelian']}, cyclic = "
        f"{s8['cyclic']} -> {table8.get(key, 'unrecognised order-8 pattern')}")
    h10 = s10["element_order_histogram"]
    ident["k=10"] = (
        "PGL(2,9), order 720, acting on the 10 points of the conic sharply "
        f"3-transitively ({s10['action']['sharply_3_transitive']}). Element orders "
        f"{h10}; derived subgroup order {s10['derived_subgroup_order']} (an index-2 "
        "subgroup, so not perfect).  NB: this group is NOT S6 even though |S6| = 720: "
        "S6 has no elements of order 8 or 10, while this group has "
        f"{h10.get(8, 0)} of order 8 and {h10.get(10, 0)} of order 10.  The "
        "distribution coincides with a direct computation from 2x2 matrices over "
        "GF(9) (extra_checks.py) and with the classical PGL(2,9) = M10."
        if s10["order"] == 720 else f"order {s10['order']}")
    out["identification"] = ident
    for k in (6, 7, 8, 10):
        print(f"  identification k={k:2d}: {ident[f'k={k}']}")

    out["all_match_claim"] = all(out["caps"][k]["matches_claim"] for k in (6, 7, 8, 10))
    out["all_orbit_stabilizer"] = all(out["caps"][k]["orbit_stabilizer_equals_pgl"]
                                      for k in (6, 7, 8, 10))
    ok = out["all_match_claim"] and out["all_orbit_stabilizer"]
    out["PASS"] = ok
    out["elapsed_s"] = round(time.time() - t00, 1)
    pc.RESULTS.mkdir(parents=True, exist_ok=True)
    (pc.RESULTS / "task5_stabilizers.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nTASK 5: {'PASS' if ok else 'FAIL'}   ({out['elapsed_s']} s)")
    return out


if __name__ == "__main__":
    main()
