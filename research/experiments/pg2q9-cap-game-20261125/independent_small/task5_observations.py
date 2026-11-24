"""Task 5: the observations/samples.

  * cap {0,1,10,20,32,39}: is it a cap?  Grundy (claim: 2)
  * cap {4,9,20,32,69,84}: is it a cap, is it maximal?  Grundy (claim: 0)
  * 5-caps containing {0,1,10,20}: Grundy values (claim: all 1)
  * extra: random 3-caps / 4-caps to confirm the Grundy is orbit-invariant in practice
"""
import json
import random
import time

import core
import task4_grundy as G

CAP6A = (0, 1, 10, 20, 32, 39)
CAP6B = (4, 9, 20, 32, 69, 84)


def info(points):
    mask = core.cap_mask(points)
    allowed = core.allowed_points(mask)
    return {
        "cap": list(points),
        "is_cap": core.is_cap(points),
        "size": len(points),
        "n_extensions": bin(allowed).count("1"),
        "maximal": allowed == 0,
        "extensions": core.mask_points(allowed),
    }


def main():
    res = {}

    # ---- 6-cap A ----
    a = info(CAP6A)
    gA, memoA = G.grundy_dp(CAP6A)
    a["grundy"] = gA
    a["upset_sizes"] = {}
    for m in memoA:
        k = bin(m).count("1")
        a["upset_sizes"][k] = a["upset_sizes"].get(k, 0) + 1
    a["upset_sizes"] = dict(sorted(a["upset_sizes"].items()))
    a["claim_grundy_2"] = gA == 2
    res["cap6A"] = a
    print("6-cap A", CAP6A, "-> cap:", a["is_cap"], "grundy:", gA,
          "extensions:", a["n_extensions"], "upset:", a["upset_sizes"])

    # ---- 6-cap B (claimed maximal) ----
    b = info(CAP6B)
    gB, memoB = G.grundy_dp(CAP6B)
    b["grundy"] = gB
    b["claim_grundy_0"] = gB == 0
    b["claim_maximal"] = b["maximal"]
    res["cap6B"] = b
    print("6-cap B", CAP6B, "-> cap:", b["is_cap"], "maximal:", b["maximal"],
          "grundy:", gB)

    # ---- all 5-caps containing {0,1,10,20} ----
    t = time.time()
    base = core.cap_mask((0, 1, 10, 20))
    five = []
    allowed = core.allowed_points(base)
    while allowed:
        bit = allowed & -allowed
        allowed ^= bit
        p = bit.bit_length() - 1
        five.append(tuple(sorted(core.mask_points(base) + [p])))
    vals = {}
    for cap in five:
        g, _ = G.grundy_dp(cap)
        vals[cap] = g
    dist = {}
    for v in vals.values():
        dist[v] = dist.get(v, 0) + 1
    rng = random.Random(20261125)
    sample = rng.sample(sorted(vals), 5)
    res["five_caps_containing_4cap"] = {
        "count": len(five),
        "grundy_distribution": {str(k): v for k, v in sorted(dist.items())},
        "random_sample_of_5": {str(c): vals[c] for c in sample},
        "all_grundy_1": set(vals.values()) == {1},
        "seconds": round(time.time() - t, 1),
    }
    print("5-caps containing {0,1,10,20}:", len(five),
          "grundy distribution:", dist)
    print("  random sample of 5:", [(c, vals[c]) for c in sample])

    # ---- extra: random 3-caps and 4-caps ----
    t = time.time()
    rng2 = random.Random(7)
    caps3 = []
    while len(caps3) < 3:
        c = tuple(sorted(rng2.sample(range(91), 3)))
        if core.is_cap(c):
            caps3.append(c)
    g3 = {}
    for c in caps3:
        g3[c] = G.grundy_dp(c)[0]
    caps4 = []
    while len(caps4) < 3:
        c = tuple(sorted(rng2.sample(range(91), 4)))
        if core.is_cap(c):
            caps4.append(c)
    g4 = {}
    for c in caps4:
        g4[c] = G.grundy_dp(c)[0]
    res["random_caps"] = {
        "random_3caps": {str(c): v for c, v in g3.items()},
        "random_4caps": {str(c): v for c, v in g4.items()},
        "all_3caps_grundy_1": set(g3.values()) == {1},
        "all_4caps_grundy_0": set(g4.values()) == {0},
        "seconds": round(time.time() - t, 1),
    }
    print("random 3-caps:", g3)
    print("random 4-caps:", g4)

    with open("out_task5.json", "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, default=str)


if __name__ == "__main__":
    main()
