"""Task 4: every 9-cap is a conic or in the example's PGL(3,8) orbit.

Cross-checks the independent census (census.py) against
  * the 32,704 conics built from quadratic forms (check_conic.py),
  * the 294,336-element orbit of the example 9-cap (check_group.py).
"""
import json
import os
import pickle

from pg8 import inc

ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")


def mask_of(pts):
    m = 0
    for p in pts:
        m |= 1 << p
    return m


def main():
    I = inc()
    out = {}
    data = pickle.load(open(os.path.join(ART, "caps.pkl"), "rb"))
    caps9 = data["caps9"]
    caps10 = data["caps10"]
    caps9set = set(caps9)

    conics = []
    with open(os.path.join(ART, "conics.txt")) as f:
        for line in f:
            conics.append(mask_of(int(t) for t in line.split()))
    conic_set = set(conics)
    orbit_ex = set(pickle.load(open(os.path.join(ART, "orbit_example.pkl"), "rb")))
    orbit_co = set(pickle.load(open(os.path.join(ART, "orbit_conic.pkl"), "rb")))

    out["census_9cap_count"] = len(caps9)
    out["census_9cap_distinct"] = len(caps9set)
    out["claim_9cap_count"] = 327040
    out["count_9_ok"] = (len(caps9) == len(caps9set) == 327040)

    out["n_conics_from_forms"] = len(conic_set)
    out["claim_conics"] = 32704
    out["conics_are_9caps"] = conic_set <= caps9set
    out["conics_one_orbit_equals_example_orbit"] = (conic_set == orbit_co)
    out["conic_orbit_size"] = len(orbit_co)

    out["example_cap_in_orbit"] = (mask_of((2, 3, 10, 12, 21, 45, 47, 50, 52))
                                   in orbit_ex)
    out["example_orbit_size"] = len(orbit_ex)
    out["claim_nonconic"] = 294336
    out["nonconic_orbit_is_9caps"] = orbit_ex <= caps9set
    out["conics_and_nonconic_orbit_disjoint"] = (conic_set & orbit_ex) == set()
    out["example_not_conic"] = (mask_of((2, 3, 10, 12, 21, 45, 47, 50, 52))
                                not in conic_set)
    out["orbit_sizes"] = [len(orbit_co), len(orbit_ex)]
    out["sum_equals_census"] = (len(conic_set) + len(orbit_ex) == len(caps9set))
    out["every_9cap_is_conic_or_in_orbit"] = (
        (conic_set | orbit_ex) == caps9set)
    out["split_arithmetic_ok"] = (327040 - 32704 == 294336)

    # extra: are all 9-caps contained in some 10-cap (hyperoval)?
    covered = set()
    for m in caps10:
        b = m
        while b:
            q = (b & -b).bit_length() - 1
            covered.add(m & ~(1 << q))
            b &= b - 1
    out["n_10caps"] = len(caps10)
    out["n_10cap_distinct"] = len(set(caps10))
    out["n_9caps_covered_by_10caps"] = len(covered & caps9set)
    out["all_9caps_in_a_10cap"] = (covered & caps9set) == caps9set
    out["each_10cap_has_10_nine_subsets"] = all(
        bin(m).count("1") == 10 for m in caps10)

    print("census 9-caps:", len(caps9), "distinct:", len(caps9set),
          "expected 327040:", out["count_9_ok"])
    print("conics from forms:", len(conic_set), "expected 32704:",
          len(conic_set) == 32704, " all are 9-caps:", out["conics_are_9caps"])
    print("conic orbit == conic set:", out["conics_one_orbit_equals_example_orbit"],
          " size:", len(orbit_co))
    print("example orbit size:", len(orbit_ex), "expected 294336:",
          len(orbit_ex) == 294336)
    print("disjoint:", out["conics_and_nonconic_orbit_disjoint"],
          " sum == census:", out["sum_equals_census"])
    print("EVERY 9-CAP IS CONIC OR IN ORBIT:",
          out["every_9cap_is_conic_or_in_orbit"])
    print("10-caps:", len(caps10), " 9-caps inside some 10-cap:",
          len(covered & caps9set), "all:", out["all_9caps_in_a_10cap"])

    with open(os.path.join(ART, "task4.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nPASS task4:", out["count_9_ok"] and out["conics_are_9caps"]
          and out["every_9cap_is_conic_or_in_orbit"]
          and out["example_not_conic"] and out["split_arithmetic_ok"])


if __name__ == "__main__":
    main()
