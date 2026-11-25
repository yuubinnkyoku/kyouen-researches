"""Task 3 (and part of task 4): independent Golay-code / dodecad identification.

* builds the F2-span of the 759 octads, verifies it is the [24,12,8] doubly-even
  self-dual binary Golay code with weight enumerator
  0^1 8^759 12^2576 16^759 24^1
* recomputes the 2576 weight-12 words (dodecads) two independent ways:
  (a) weight-12 code words, (b) symmetric differences of octad pairs meeting
  in exactly 2 points; verifies the two families coincide
* per dodecad: |D cap B| is even and in {2,4,6} for every octad, with the
  distribution 2:132, 4:495, 6:132; D is safe and maximal for s=6; D^c is a
  dodecad
* exact count of the 12-sets that contain at least one octad (needed for the
  analytic s=7 safe-12-set count) via pair/triple inclusion-exclusion
"""

from __future__ import annotations

import itertools
import json
import math
import sys
from collections import Counter

from common import (
    B,
    N,
    OUT_DIR,
    all_codewords,
    dodecads_from_octad_pairs,
    golay_basis,
    load_board,
    octad_masks,
)

FULL = (1 << N) - 1


def main() -> int:
    header, octads = load_board()
    oct_masks = octad_masks(octads)
    oct_index = {m: i for i, m in enumerate(oct_masks)}
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)

    # ------------------------------------------------------------------ code
    rank, rows = golay_basis(octads)
    check(rank == 12, f"octad span rank {rank} != 12")
    words = all_codewords(rows)
    check(len(set(words)) == 1 << rank, "codeword enumeration incomplete")
    weight_dist = Counter(w.bit_count() for w in words)
    expected_weight_dist = {0: 1, 8: 759, 12: 2576, 16: 759, 24: 1}
    check(dict(weight_dist) == expected_weight_dist,
          f"weight distribution {dict(weight_dist)} != {expected_weight_dist}")
    check(all(w.bit_count() % 4 == 0 for w in words), "code is not doubly even")
    # self-orthogonality of the basis (hence of the whole code)
    self_orth = all(((r1 & r2).bit_count() % 2) == 0 for r1 in rows for r2 in rows)
    check(self_orth, "code is not self-orthogonal")
    weight8 = {w for w in words if w.bit_count() == 8}
    check(weight8 == set(oct_masks), "weight-8 words are not exactly the octads")

    # -------------------------------------------------------------- dodecads
    code12 = {w for w in words if w.bit_count() == 12}
    pair12 = dodecads_from_octad_pairs(octads)
    check(len(code12) == 2576, f"weight-12 code words: {len(code12)} != 2576")
    check(len(pair12) == 2576, f"octad-pair symmetric differences: {len(pair12)} != 2576")
    check(code12 == pair12, "weight-12 words differ from octad-pair differences")

    # each dodecad is the symmetric difference of exactly 66 octad pairs
    # (octads meeting it in 6 points come in pairs, 132 of them)
    pair_mult = Counter()
    for i in range(B):
        for j in range(i + 1, B):
            if (oct_masks[i] & oct_masks[j]).bit_count() == 2:
                pair_mult[oct_masks[i] ^ oct_masks[j]] += 1
    check(len(pair_mult) == 2576, f"pair-xor family has {len(pair_mult)} dodecads")
    check(set(pair_mult.values()) == {66},
          f"pair multiplicity values {sorted(set(pair_mult.values()))} != [66]")

    # octad intersection spectrum of a dodecad
    spectrum = Counter()
    maximal_fail = []
    non_safe = []
    complement_fail = []
    profiles = Counter()
    for D in code12:
        inters = Counter((D & b).bit_count() for b in oct_masks)
        spectrum.update(inters.keys())
        if any(k not in (2, 4, 6) for k in inters):
            non_safe.append((D, dict(inters)))
        profiles[tuple(sorted(inters.items()))] += 1
        # maximality for s=6: every outside point must lie in an octad with
        # |D cap B| = 6 (adding it would then make 7 > 6)
        cover = 0
        for b in oct_masks:
            if (D & b).bit_count() == 6:
                cover |= b
        if ((FULL ^ D) & ~cover) != 0:
            maximal_fail.append(D)
        if (FULL ^ D) not in code12:
            complement_fail.append(D)
    check(not non_safe, f"{len(non_safe)} dodecads meet some octad outside {{2,4,6}}")
    check(not maximal_fail, f"{len(maximal_fail)} dodecads are not maximal for s=6")
    check(not complement_fail, "some dodecad complement is not a dodecad")
    expected_profile = ((2, 132), (4, 495), (6, 132))
    profile_ok = all(k == expected_profile for k in profiles)
    check(profile_ok, f"per-dodecad octad-intersection profile: {dict(profiles)}")

    # ---------------------- exact counting of 12-sets containing an octad ----
    # every 12-set containing >= 2 octads is A u B for a pair with |A cap B| = 4
    pair_masks = [oct_masks[i] | oct_masks[j]
                  for i in range(B) for j in range(i + 1, B)
                  if (oct_masks[i] & oct_masks[j]).bit_count() == 4]
    check(len(pair_masks) == 106260, f"pairs with intersection 4: {len(pair_masks)}")
    distinct12 = set(pair_masks)
    k_profile = Counter()
    for X in distinct12:
        pts = [p for p in range(N) if (X >> p) & 1]
        k = 0
        for T in itertools.combinations(pts, 8):
            m = 0
            for p in T:
                m |= 1 << p
            if m in oct_index:
                k += 1
        k_profile[k] += 1
    # sum C(k,2) over distinct 12-sets with >=2 octads must equal 106260
    sum_pairs = sum(k * (k - 1) // 2 * c for k, c in k_profile.items())
    check(sum_pairs == 106260, f"sum C(k,2) = {sum_pairs} != 106260")
    # inclusion-exclusion: |union E_B| = sum_j (-1)^(j+1) * sum_X C(k_X, j)
    union = 0
    j = 1
    while True:
        term = 0
        if j == 1:
            term = B * math.comb(N - 8, 12 - 8)
        else:
            term = sum(math.comb(k, j) * c for k, c in k_profile.items() if k >= j)
        if term == 0:
            break
        union += term if j % 2 == 1 else -term
        j += 1
    total12 = math.comb(N, 12)
    safe12_s7 = total12 - union
    check(safe12_s7 == 1393616, f"s=7 safe 12-sets via inclusion-exclusion: {safe12_s7}")
    # s=7 safe 10/11-set formulas (no two octads fit, so no correction needed)
    safe10_s7 = math.comb(N, 10) - B * math.comb(16, 2)
    safe11_s7 = math.comb(N, 11) - B * math.comb(16, 3)
    check(safe10_s7 == 1870176, f"s=7 safe 10-sets: {safe10_s7}")
    check(safe11_s7 == 2071104, f"s=7 safe 11-sets: {safe11_s7}")

    # ------------------------------------------ dodecad-subset safe-set sides
    # for s=6, every k-subset of a dodecad (k=9,10,11) is safe and, by the
    # minimum distance 8, lies in exactly one dodecad
    sub_counts = {}
    for k in (9, 10, 11, 12):
        subs = set()
        for D in code12:
            pts = [p for p in range(N) if (D >> p) & 1]
            for T in itertools.combinations(pts, k):
                m = 0
                for p in T:
                    m |= 1 << p
                subs.add(m)
        sub_counts[k] = {
            "distinct": len(subs),
            "upper_bound": 2576 * math.comb(12, k),
        }
        check(len(subs) == 2576 * math.comb(12, k),
              f"dodecad {k}-subsets not injective: {len(subs)} != {2576 * math.comb(12, k)}")
    # safety of the dodecad k-subsets is automatic (subsets of safe sets are
    # safe); spot-check a random sample anyway with a direct octad scan.
    import random
    rng = random.Random(20261125)
    sample = rng.sample(sorted(subs), 500)
    check(all(all(((m & b).bit_count() <= 6) for b in oct_masks) for m in sample),
          "a sampled dodecad 12-subset is not safe for s=6")

    result = {
        "rank": rank,
        "codewords": len(words),
        "weight_distribution": dict(sorted(weight_dist.items())),
        "doubly_even": True,
        "self_orthogonal": self_orth,
        "weight8_is_octads": weight8 == set(oct_masks),
        "dodecads_from_code": len(code12),
        "dodecads_from_octad_pairs": len(pair12),
        "dodecad_families_equal": code12 == pair12,
        "dodecad_pair_multiplicities": sorted(set(pair_mult.values())),
        "dodecad_octad_intersection_profile": {str(k): v for k, v in profiles.items()},
        "dodecads_non_safe": len(non_safe),
        "dodecads_not_maximal_s6": len(maximal_fail),
        "dodecad_complement_failures": len(complement_fail),
        "twelve_sets_with_two_octads": len(distinct12),
        "twelve_sets_octad_count_profile": dict(sorted(k_profile.items())),
        "sum_choose_k_2": sum_pairs,
        "twelve_sets_containing_an_octad": union,
        "safe_12_sets_s7": safe12_s7,
        "safe_10_sets_s7": safe10_s7,
        "safe_11_sets_s7": safe11_s7,
        "dodecad_subset_counts": sub_counts,
        "checks_failed": failures,
        "PASS": not failures,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "task3_golay.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
