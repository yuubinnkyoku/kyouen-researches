"""Task 1: verify the board is the Witt design S(5,8,24).

Checks
  * 759 distinct 8-subsets of {0..23}
  * lambda_t for every t-subset, t = 0..5 (lambda_5 = 1, lambda_4 = 5,
    lambda_3 = 21, lambda_2 = 77, lambda_1 = 253, lambda_0 = 759)
  * pairwise octad intersections lie in {0,2,4} with the counts forced by the
    2- and 4-subset incidence numbers
  * derived counts used later: 6-subsets in an octad, 7-subsets in an octad
"""

from __future__ import annotations

import itertools
import json
import math
import sys

from common import BOARD_PATH, B, N, OUT_DIR, load_board


def expected_lambda(t: int) -> int:
    # lambda_t = C(24-t, 5-t) / C(8-t, 5-t) for t <= 5
    return math.comb(N - t, 5 - t) // math.comb(8 - t, 5 - t)


def main() -> int:
    header, octads = load_board()
    failures = []

    def check(cond, msg):
        if not cond:
            failures.append(msg)

    # ---- basic shape -------------------------------------------------------
    check(len(octads) == B, f"expected {B} octads, got {len(octads)}")
    check(len(set(octads)) == B, "octads are not 759 distinct 8-sets")
    for o in octads:
        check(len(o) == 8 and len(set(o)) == 8, f"bad octad {o}")
        check(all(0 <= p < N for p in o), f"point out of range in {o}")

    # ---- lambda_t for t = 0..5 --------------------------------------------
    lam = {}
    for t in range(0, 6):
        need = math.comb(N, t)
        seen = {}
        for o in octads:
            for T in itertools.combinations(o, t):
                seen[T] = seen.get(T, 0) + 1
        tot = sum(seen.values())
        vals = sorted(set(seen.values()))
        expected = expected_lambda(t)
        lam[t] = {
            "distinct_subsets_covered": len(seen),
            "expected_distinct": need,
            "multiplicity_values": vals,
            "expected_multiplicity": expected,
            "total_incidences": tot,
            "expected_total": B * math.comb(8, t),
        }
        check(len(seen) == need, f"lambda_{t}: covered {len(seen)} of {need} subsets")
        check(vals == [expected], f"lambda_{t}: multiplicities {vals} != [{expected}]")
        check(tot == B * math.comb(8, t), f"lambda_{t}: incidence total {tot}")

    # ---- pairwise intersection distribution --------------------------------
    pair_dist = {0: 0, 2: 0, 4: 0}
    bad_pairs = []
    for i in range(B):
        for j in range(i + 1, B):
            k = len(set(octads[i]) & set(octads[j]))
            if k in pair_dist:
                pair_dist[k] += 1
            else:
                bad_pairs.append((i, j, k))
    # forced values: sum C(|cap|,2) = C(24,2) C(77,2); #cap=4 = C(24,4) C(5,2)
    n4 = math.comb(N, 4) * math.comb(5, 2)
    total_pair_inc = math.comb(N, 2) * math.comb(77, 2)
    n2 = total_pair_inc - 6 * n4
    total_pairs = math.comb(B, 2)
    n0 = total_pairs - n2 - n4
    pair_expected = {0: n0, 2: n2, 4: n4}
    check(not bad_pairs, f"octad intersections outside {{0,2,4}}: {bad_pairs[:5]}")
    check(pair_dist == pair_expected,
          f"pair intersection distribution {pair_dist} != {pair_expected}")

    # ---- derived numbers used by the structural claims ---------------------
    six_in_octad = B * math.comb(8, 6)          # 6-subsets contained in some octad
    seven_in_octad = B * math.comb(8, 7)        # 7-subsets contained in some octad
    # a 6-subset lies in at most one octad (lambda_5 = 1 implies this)
    six_counts = {}
    for o in octads:
        for T in itertools.combinations(o, 6):
            six_counts[T] = six_counts.get(T, 0) + 1
    seven_counts = {}
    for o in octads:
        for T in itertools.combinations(o, 7):
            seven_counts[T] = seven_counts.get(T, 0) + 1
    check(len(six_counts) == six_in_octad, "a 6-subset lies in two octads")
    check(max(six_counts.values()) == 1, "a 6-subset lies in two octads")
    check(len(seven_counts) == seven_in_octad, "a 7-subset lies in two octads")
    check(max(seven_counts.values()) == 1, "a 7-subset lies in two octads")

    result = {
        "board_path": str(BOARD_PATH),
        "header": header,
        "octads": len(octads),
        "distinct_octads": len(set(octads)),
        "lambda": lam,
        "pair_intersection_distribution": pair_dist,
        "pair_intersection_expected": pair_expected,
        "six_subsets_in_octad": len(six_counts),
        "six_subsets_in_octad_expected": six_in_octad,
        "seven_subsets_in_octad": len(seven_counts),
        "seven_subsets_in_octad_expected": seven_in_octad,
        "checks_failed": failures,
        "PASS": not failures,
    }
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "task1_board.json").write_text(json.dumps(result, indent=1), encoding="utf-8")
    print(json.dumps(result, indent=1))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
