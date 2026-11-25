"""Task 5: the three maximal 6-cap representatives.

Checks per representative:
  * it is a cap with 6 points and is maximal (every outside point lies on a
    secant; equivalently no 0-secant outside point),
  * outside-point secant-count distribution == {1:36, 2:24, 3:7},
  * no 10-cap (hyperoval) contains it.
Also computes the three PGL(3,8) orbits and checks that together they are
exactly the set of all maximal 6-caps (count from the independent census).
"""
import json
import os
import pickle
import time

from pg8 import inc
from group import GENS, orbit_of_mask

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")

REPS = [
    (10, 47, 49, 55, 61, 64),
    (17, 27, 30, 44, 52, 70),
    (8, 48, 50, 51, 58, 61),
]


def mask_of(pts):
    m = 0
    for p in pts:
        m |= 1 << p
    return m


def secant_info(I, S):
    S = sorted(S)
    secants = set()
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            secants.add(I.lof[S[i]][S[j]])
    Sset = set(S)
    outside = [p for p in range(73) if p not in Sset]
    dist = {}
    zero_secant = []
    for p in outside:
        c = 0
        for L in secants:
            if (I.line_masks[L] >> p) & 1:
                c += 1
        dist[c] = dist.get(c, 0) + 1
        if c == 0:
            zero_secant.append(p)
    return dist, len(secants), len(outside), zero_secant


def main():
    I = inc()
    out = {"reps": [list(r) for r in REPS]}
    os.makedirs(ART, exist_ok=True)
    data = pickle.load(open(os.path.join(ART, "caps.pkl"), "rb"))
    caps10 = data["caps10"]
    census = json.load(open(os.path.join(ART, "census.json")))
    n_max6 = census["n_maximal6"]

    t0 = time.time()
    orbit_sets = []
    per_rep = []
    all_ok = True
    for k, S in enumerate(REPS):
        r = {"cap": list(S), "size": len(S)}
        r["is_cap"] = I.is_cap(S)
        blocked = I.blocked_mask(S)
        capmask = mask_of(S)
        r["blocked_count"] = (blocked & I.ALL).bit_count()
        r["is_maximal"] = ((blocked | capmask) == I.ALL)
        dist, nsec, nout, zero = secant_info(I, S)
        r["secant_lines"] = nsec
        r["outside_points"] = nout
        r["distribution"] = {str(k2): v for k2, v in sorted(dist.items())}
        r["zero_secant_outside_points"] = zero
        r["distribution_matches"] = (dist == {1: 36, 2: 24, 3: 7})
        r["no_zero_secants"] = (len(zero) == 0)
        r["self_consistent"] = (sum(dist.values()) == 67
                                and sum(k2 * v for k2, v in dist.items()) == 105)
        # containment in a 10-cap
        contained = [m for m in caps10 if (m & capmask) == capmask]
        r["n_10caps_containing"] = len(contained)
        r["contained_in_10cap"] = len(contained) > 0
        # orbit
        t = time.time()
        orb = orbit_of_mask(capmask, GENS)
        r["orbit_size"] = len(orb)
        r["orbit_seconds"] = round(time.time() - t, 2)
        r["stabilizer_order"] = 16482816 // len(orb)
        orbit_sets.append(orb)
        per_rep.append(r)
        all_ok = all_ok and r["is_cap"] and r["is_maximal"] and \
            r["distribution_matches"] and r["no_zero_secants"] and \
            not r["contained_in_10cap"] and r["self_consistent"]
        print(f"rep {S}: cap={r['is_cap']} maximal={r['is_maximal']} "
              f"dist={r['distribution']} zero-secants={len(zero)} "
              f"10caps-containing={len(contained)} orbit={len(orb)} "
              f"({r['orbit_seconds']}s)")
    out["per_rep"] = per_rep

    # three orbits: disjoint, sizes, cover all maximal 6-caps
    sizes = [len(o) for o in orbit_sets]
    out["orbit_sizes"] = sizes
    out["pairwise_disjoint"] = (sizes[0] + sizes[1] + sizes[2]
                                == len(orbit_sets[0] | orbit_sets[1] | orbit_sets[2]))
    out["union_size"] = len(orbit_sets[0] | orbit_sets[1] | orbit_sets[2])
    out["census_maximal6"] = n_max6
    out["orbits_cover_all_maximal6"] = (out["union_size"] == n_max6)
    out["three_classes_confirmed"] = out["pairwise_disjoint"] and \
        out["orbits_cover_all_maximal6"]
    # all orbit members are 6-point sets; sample-cap check
    import random
    rng = random.Random(20261126)
    sample_ok = True
    for orb in orbit_sets:
        lst = list(orb)
        for m in rng.sample(lst, 300):
            pts = [p for p in range(73) if (m >> p) & 1]
            if len(pts) != 6 or not I.is_cap(pts) or \
                    ((I.blocked_mask(pts) | m) != I.ALL):
                sample_ok = False
                break
        if not sample_ok:
            break
    out["orbit_members_are_maximal_6caps_sampled"] = sample_ok

    # invariance argument data: containment in a 10-cap is collineation
    # invariant, so rep-level check covers the whole orbit.
    out["all_reps_10cap_free"] = all(not r["contained_in_10cap"] for r in per_rep)
    out["conclusion_no_maximal6_in_10cap"] = (
        out["all_reps_10cap_free"] and out["orbits_cover_all_maximal6"]
        and out["three_classes_confirmed"])

    print("orbit sizes:", sizes, " union:", out["union_size"],
          " census maximal 6-caps:", n_max6,
          " cover:", out["orbits_cover_all_maximal6"])
    print("sample orbit members are maximal 6-caps:", sample_ok)
    print("conclusion (no maximal 6-cap in a hyperoval):",
          out["conclusion_no_maximal6_in_10cap"])
    with open(os.path.join(ART, "task5.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nPASS task5:", all_ok and out["conclusion_no_maximal6_in_10cap"])
    print("elapsed", round(time.time() - t0, 1), "s")


if __name__ == "__main__":
    main()
