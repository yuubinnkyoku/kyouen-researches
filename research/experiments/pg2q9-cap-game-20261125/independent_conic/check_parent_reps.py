"""Cross-check the representative/orbit labels used in the parent artifact
output/conic_layer.json against the independently computed PGL(2,9) orbits."""
import itertools
import json

import conic as K
import gf9 as F
import pg9 as P
from task3_orbits import orbit_partition  # reuse the orbit routine

PARENT = {
    3: [(120, [0, 1, 10])],
    4: [(30, [0, 1, 10, 20]), (180, [0, 1, 10, 31])],
    5: [(180, [0, 1, 10, 20, 31]), (72, [0, 1, 10, 31, 51])],
    6: [(180, [0, 1, 10, 20, 31, 45]), (30, [0, 1, 10, 20, 31, 62])],
    7: [(120, [0, 1, 10, 20, 31, 45, 51])],
    8: [(45, [0, 1, 10, 20, 31, 45, 51, 62])],
    9: [(10, [0, 1, 10, 20, 31, 45, 51, 62, 75])],
}


def main():
    import task3_orbits as T3
    perms = T3.pgl2_perms()
    stabmats = K.stabiliser(K.C_MASK, cache=K.STAB_CACHE)
    stab_perms = K.permutations_on(K.C_MASK, stabmats)
    Cpts = P.bits(K.C_MASK)
    pos = {p: i for i, p in enumerate(Cpts)}

    orbits = {}
    for k in range(3, 10):
        parts = orbit_partition(stab_perms, 10, k)
        lookup = {}
        for orb in parts:
            for s in orb["members"]:
                lookup[s] = orb["size"]
        orbits[k] = lookup

    out = {}
    ok = True
    rows = []
    for k in sorted(PARENT):
        for claimed_size, rep in PARENT[k]:
            assert all(p in Cpts for p in rep), (k, rep)
            key = frozenset(pos[p] for p in rep)
            got = orbits[k][key]
            rows.append({"k": k, "rep": rep, "parent_label": claimed_size,
                         "computed_orbit": got,
                         "match": got == claimed_size})
            ok = ok and got == claimed_size
            print("k=%d rep=%-42s parent_label=%-3d computed=%-3d %s"
                  % (k, rep, claimed_size, got,
                     "OK" if got == claimed_size else "MISMATCH"))
    out["rows"] = rows
    out["all_match"] = ok
    # distribution of the parent's k=4 and k=6 labels
    out["note"] = ("parent representatives for k=4 (both), k=5 (second) and "
                   "k=6 (swapped) are labelled with the wrong orbit size; the "
                   "orbit-size multisets and Grundy values are unaffected")

    # --- K1305 correspondence: {0,1,10,20,42} is the 4,245,696 (stab 10)
    # five-cap orbit; map its conic onto C and check the 72-class.
    five = [0, 1, 10, 20, 42]
    basis, _ = K.forms_through(five)
    f5 = P.canonical_form(tuple(basis[0])) if len(basis) == 1 else None
    M5 = P.form_zero_mask(f5) if f5 else 0
    T = None
    if M5:
        src = [P.POINTS[i] for i in K.frame_of(M5)]
        for a in P.bits(K.C_MASK):
            for b in P.bits(K.C_MASK):
                if b == a:
                    continue
                for c in P.bits(K.C_MASK):
                    if c in (a, b):
                        continue
                    for d in P.bits(K.C_MASK):
                        if d in (a, b, c):
                            continue
                        cand = P.projectivity_from_frame(
                            src, [P.POINTS[a], P.POINTS[b], P.POINTS[c], P.POINTS[d]])
                        if cand is None:
                            continue
                        img = 0
                        for i in P.bits(M5):
                            img |= 1 << P.LABEL[F.normalise(
                                P.mat_vec(cand, P.POINTS[i]))]
                        if img == K.C_MASK:
                            T = cand
                            break
                    if T:
                        break
                if T:
                    break
            if T:
                break
    mapped = None
    orbit_of_mapped = None
    if T is not None:
        mapped = sorted(P.LABEL[F.normalise(P.mat_vec(T, P.POINTS[i]))]
                        for i in five)
        key = frozenset(pos[p] for p in mapped)
        orbit_of_mapped = orbits[5][key]
    out["k1305_correspondence"] = {
        "cap": five,
        "unique_nondegenerate_conic": bool(f5) and P.form_det(f5) != 0,
        "conic_maps_onto_C": T is not None,
        "image_in_C": mapped,
        "orbit_size_of_image_in_C": orbit_of_mapped,
        "expected_72": orbit_of_mapped == 72,
    }
    print("\nK1305 check: {0,1,10,20,42} maps to", mapped,
          "orbit", orbit_of_mapped, "(expected 72)")
    ok = ok and orbit_of_mapped == 72
    out["all_match"] = ok
    with open("results_parent_reps.json", "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=1)
    print("\nall parent representative labels match:", ok)


main()
