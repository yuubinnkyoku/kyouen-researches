"""Extra structural check: how 9-caps sit inside the 32,704 ten-caps.

Every 9-cap has exactly one point not on any of its secants (its unique
extension point), and 10-caps are exactly the caps so obtained.  In
particular each conic extends uniquely to a 10-cap (the conic plus its
nucleus in characteristic 2), and distinct conics give distinct 10-caps.
"""
import json
import os
import pickle
import random
import time

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
    caps10set = set(caps10)
    caps9set = set(caps9)
    conics = []
    with open(os.path.join(ART, "conics.txt")) as f:
        for line in f:
            conics.append(mask_of(int(t) for t in line.split()))
    conic_set = set(conics)

    def extension_points(m):
        blocked = 0
        pts = [p for p in range(73) if (m >> p) & 1]
        for i in range(len(pts)):
            for j in range(i + 1, len(pts)):
                blocked |= I.line_masks[I.lof[pts[i]][pts[j]]]
        return [p for p in range(73) if not ((blocked | m) >> p) & 1]

    t0 = time.time()
    ext_hist = {}
    hyper = set()
    for m in conic_set:
        e = extension_points(m)
        ext_hist[len(e)] = ext_hist.get(len(e), 0) + 1
        assert len(e) == 1, (m, e)
        hm = m | (1 << e[0])
        assert hm in caps10set
        hyper.add(hm)
    out["conic_extension_count_histogram"] = {str(k): v for k, v in ext_hist.items()}
    out["conics_extend_uniquely"] = (ext_hist == {1: len(conic_set)})
    out["distinct_10caps_from_conics"] = len(hyper)
    out["conic_to_10cap_bijective"] = (len(hyper) == len(caps10set))
    out["all_10caps_are_conic_plus_nucleus"] = (hyper == caps10set)

    # every 9-cap (conic or not) has exactly one extension point, sampled
    nonconic = list(caps9set - conic_set)
    rng = random.Random(20261126)
    sample = rng.sample(nonconic, 3000)
    bad = 0
    samp_hist = {}
    for m in sample:
        e = extension_points(m)
        samp_hist[len(e)] = samp_hist.get(len(e), 0) + 1
        if len(e) != 1 or (m | (1 << e[0])) not in caps10set:
            bad += 1
    out["nonconic_9cap_sample"] = len(sample)
    out["nonconic_sample_extension_histogram"] = {str(k): v for k, v in samp_hist.items()}
    out["nonconic_sample_all_unique_extension"] = (bad == 0)

    # full check: the 9-subsets of the 10-caps are exactly all 9-caps
    n_subsets = 0
    covered = set()
    for m in caps10set:
        b = m
        while b:
            q = (b & -b).bit_length() - 1
            covered.add(m & ~(1 << q))
            n_subsets += 1
            b &= b - 1
    out["n_9subsets_of_10caps"] = n_subsets
    out["9subsets_equal_all_9caps"] = (covered == caps9set)
    out["each_9cap_in_unique_10cap"] = (n_subsets == len(covered) == len(caps9set))

    print("conic extension-point histogram:", out["conic_extension_count_histogram"])
    print("distinct 10-caps from conics:", len(hyper), " census 10-caps:",
          len(caps10set), " bijective:", out["conic_to_10cap_bijective"])
    print("non-conic sample (3000) unique extension:",
          out["nonconic_sample_all_unique_extension"],
          out["nonconic_sample_extension_histogram"])
    print("9-subsets of 10-caps:", n_subsets, " == all 9-caps:",
          out["9subsets_equal_all_9caps"], " unique:",
          out["each_9cap_in_unique_10cap"])
    print("seconds:", round(time.time() - t0, 1))
    with open(os.path.join(ART, "hyperovals.json"), "w") as f:
        json.dump(out, f, indent=1)
    print("\nPASS extra:",
          out["conics_extend_uniquely"] and out["conic_to_10cap_bijective"]
          and out["all_10caps_are_conic_plus_nucleus"]
          and out["nonconic_sample_all_unique_extension"]
          and out["9subsets_equal_all_9caps"])


if __name__ == "__main__":
    main()
