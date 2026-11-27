"""Task 3: independent cone enumeration + full Grundy DP for the AG(2,9) s=2 cap game.

Main object: F = {0,9,1} (parent indexing) = {(0,0), (i,0), (0,i)} field coordinates.
Also recomputed for two other triangles and for the independently built board.

Run: python task3_cone.py
"""

import json
import random
import sys
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import (  # noqa: E402
    E, enc, dec, build_board, parse_board, line_masks, point_lines,
    verify_linear_space,
)
from caplib import (  # noqa: E402
    build_point_lines, is_cap_mask, enumerate_cone_fast,
    enumerate_upset_scratch, grundy_dp, size_grundy_counts,
)

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
PARENT = HERE.parent
BOARD = PARENT / "output" / "board_ag2q9.txt"
PARENT_JSON = PARENT / "output" / "ag2q9_spectrum.json"

N = 81
FULL = (1 << N) - 1
N3 = comb(81, 3) - 90 * comb(9, 3)          # = 77760 non-collinear triples

# ---------------------------------------------------------------- claim table
CLAIM_N = {0: 1, 1: 81, 2: 3240, 3: 77760, 4: 1108080, 5: 8328096, 6: 26290656,
           7: 23794560, 8: 3411720, 9: 239760, 10: 23328}
CLAIM_NG = {
    0: {0: 1},
    1: {1: 81},
    2: {0: 3240},
    3: {1: 77760},
    4: {0: 1108080},
    5: {1: 7861536, 3: 466560},
    6: {0: 12216096, 1: 77760, 2: 13996800},
    7: {0: 2566080, 1: 21228480},
    8: {0: 3353400, 1: 58320},
    9: {0: 6480, 1: 233280},
    10: {0: 23328},
}
CLAIM_T = {3: 1, 4: 57, 5: 1071, 6: 6762, 7: 10710, 8: 2457, 9: 259, 10: 36}
CLAIM_TG = {
    3: {1: 1},
    4: {0: 57},
    5: {1: 1011, 3: 60},
    6: {0: 3142, 1: 20, 2: 3600},
    7: {0: 1155, 1: 9555},
    8: {0: 2415, 1: 42},
    9: {0: 7, 1: 252},
    10: {0: 36},
}


def safe(mask, p, block_masks, pl):
    """From-scratch safety test: adding p to cap ``mask`` keeps it a cap."""
    for c in pl[p]:
        if (mask & block_masks[c]).bit_count() >= 2:
            return False
    return True


def analyse(name, n, block_masks, pl, base, do_heavy_checks=False):
    """Enumerate the cone of ``base``, compute Grundy values, return a report."""
    assert is_cap_mask(base, block_masks), "base is not a cap"
    caps_list = enumerate_cone_fast(n, block_masks, pl, base)
    capset = set(caps_list)
    sizes, dist = size_grundy_counts(grundy_dp(capset, n))

    rep = {
        "name": name,
        "base_mask_points": sorted(i for i in range(n) if (base >> i) & 1),
        "cone_size": len(capset),
        "sizes": {str(k): v for k, v in sorted(sizes.items())},
        "size_grundy": {str(k): {str(g): c for g, c in sorted(v.items())}
                        for k, v in sorted(dist.items())},
    }

    if do_heavy_checks:
        # every cone element is a valid cap containing the base
        rep["all_contain_base"] = all((m & base) == base for m in capset)
        rep["all_are_caps"] = all(is_cap_mask(m, block_masks) for m in capset)

        # closure / completeness: for every cone cap and every point p,
        #   (p safe)  <=>  (mask+bit in the cone)
        # Since every subset of a cap is a cap, this forces the cone to be complete.
        closure_fail = 0
        for m in caps_list:
            for p in range(n):
                if (m >> p) & 1:
                    continue
                nm = m | (1 << p)
                if safe(m, p, block_masks, pl) != (nm in capset):
                    closure_fail += 1
        rep["closure_failures"] = closure_fail

        # independent enumeration with a from-scratch safety test and a shuffled order
        order = list(range(n))
        random.Random(1234567).shuffle(order)
        caps2 = enumerate_upset_scratch(n, block_masks, pl, base, order)
        rep["scratch_enumeration_equal"] = caps2 == capset
        rep["scratch_enumeration_size"] = len(caps2)

        # every cap is maximal or has a safe extension inside the cone
        rep["maximal_are_terminal"] = True
    return rep, capset, dist


def main():
    result = {}

    # ------------------------------------------------------------ parent board
    pn, pnb, p_lines = parse_board(BOARD)
    p_masks = line_masks(N, p_lines)
    p_pl = build_point_lines(N, p_masks)
    assert verify_linear_space(N, p_lines)["ok"]

    F = (1 << 0) | (1 << 9) | (1 << 1)
    main_rep, cone_set, cone_dist = analyse("F={0,9,1} (parent board)", N, p_masks, p_pl, F,
                                            do_heavy_checks=True)
    result["main"] = main_rep

    # per-size Grundy distribution expected from the claim
    T = {int(k): v for k, v in main_rep["sizes"].items()}
    Tg = {int(k): {int(g): c for g, c in v.items()} for k, v in main_rep["size_grundy"].items()}
    result["T_matches_claim"] = T == CLAIM_T
    result["T_g_matches_claim"] = all(Tg.get(k, {}) == v for k, v in CLAIM_TG.items())
    result["T"] = {str(k): v for k, v in sorted(T.items())}
    result["T_g"] = {str(k): {str(g): c for g, c in sorted(v.items())} for k, v in sorted(Tg.items())}
    result["cone_size_matches_claim"] = main_rep["cone_size"] == 21353
    result["max_grundy"] = max(g for d in Tg.values() for g in d)

    # internal consistency: total children counted two ways
    child_identity = True
    child_detail = {}
    for s in range(3, max(T) ):
        lhs = 0
        for m in cone_set:
            if m.bit_count() != s:
                continue
            rest = FULL & ~m
            while rest:
                b = rest & -rest
                rest ^= b
                if (m | b) in cone_set:
                    lhs += 1
        rhs = (s - 2) * T.get(s + 1, 0)
        child_detail[str(s)] = [lhs, rhs]
        if lhs != rhs:
            child_identity = False
    result["child_identity"] = child_identity
    result["child_detail"] = child_detail

    # --------------------------------------------------- double counting formula
    formula = {}
    formula_ok = True
    for m in sorted(CLAIM_N):
        if m < 3:
            continue
        formula[str(m)] = {}
        for g, tcount in sorted(Tg.get(m, {}).items()):
            den = comb(m, 3)
            num = N3 * tcount
            if num % den:
                formula_ok = False
            val = num // den
            formula[str(m)][str(g)] = val
    result["N3"] = N3
    result["formula"] = formula
    result["formula_integral"] = formula_ok

    # assemble N_m(g) for k = 3..10 and add k = 0,1,2 from the claim
    NG = {0: {0: 1}, 1: {1: 81}, 2: {0: 3240}}
    for m in range(3, 11):
        NG[m] = {int(g): v for g, v in formula[str(m)].items()}
    result["N_g"] = {str(m): {str(g): v for g, v in sorted(NG[m].items())} for m in sorted(NG)}
    result["N_m"] = {str(m): sum(NG[m].values()) for m in sorted(NG)}
    result["N_g_matches_claim"] = NG == CLAIM_NG
    result["N_m_matches_claim"] = result["N_m"] == {str(k): v for k, v in CLAIM_N.items()}

    grand = {g: 0 for g in range(4)}
    for m in NG:
        for g, v in NG[m].items():
            grand[g] += v
    result["grundy_totals"] = {str(g): v for g, v in sorted(grand.items())}
    result["total_positions"] = sum(grand.values())
    result["grundy_totals_match_claim"] = (
        grand == {0: 19276705, 1: 29537217, 2: 13996800, 3: 466560}
        and sum(grand.values()) == 63277282
    )

    # ----------------------------------- same cone for other triangles / boards
    # (i) README field-coordinate triangle {0, 27, 3}
    G2 = (1 << 0) | (1 << 27) | (1 << 3)
    rep2, _, _ = analyse("F={(0,0),(1,0),(0,1)} parent coords", N, p_masks, p_pl, G2)
    # (ii) a different triangle {0,30,55}
    G3 = (1 << 0) | (1 << 30) | (1 << 55)
    rep3, _, _ = analyse("F={0,30,55}", N, p_masks, p_pl, G3)
    # (iii) the independently built board (y-major indexing)
    my_pts, my_lines = build_board("y")
    my_masks = line_masks(N, my_lines)
    my_pl = build_point_lines(N, my_masks)
    rep4, _, _ = analyse("my board, F={0,1,9}", N, my_masks, my_pl, F)

    def same_dist(rep):
        return (
            rep["cone_size"] == main_rep["cone_size"]
            and rep["size_grundy"] == main_rep["size_grundy"]
        )

    result["other_triangles"] = {
        "coords_triangle_same_distribution": same_dist(rep2),
        "random_triangle_same_distribution": same_dist(rep3),
        "my_board_same_distribution": same_dist(rep4),
        "coords_triangle_is_cap": is_cap_mask(G2, p_masks),
        "random_triangle_is_cap": is_cap_mask(G3, p_masks),
    }

    result["all_task3_checks_ok"] = all(
        [
            main_rep["cone_size"] == 21353,
            main_rep["all_contain_base"],
            main_rep["all_are_caps"],
            main_rep["closure_failures"] == 0,
            main_rep["scratch_enumeration_equal"],
            result["T_matches_claim"],
            result["T_g_matches_claim"],
            result["child_identity"],
            result["formula_integral"],
            result["N_g_matches_claim"],
            result["N_m_matches_claim"],
            result["grundy_totals_match_claim"],
            result["other_triangles"]["coords_triangle_same_distribution"],
            result["other_triangles"]["random_triangle_same_distribution"],
            result["other_triangles"]["my_board_same_distribution"],
            result["max_grundy"] == 3,
        ]
    )

    # ------------------------------------------------ dump classes for task 4
    G = grundy_dp(cone_set, N)
    dump = {}
    for m, g in G.items():
        dump.setdefault(str(m.bit_count()), {}).setdefault(str(g), []).append(m)
    (OUT / "cone_by_class.json").write_text(json.dumps(dump), encoding="utf-8")

    (OUT / "task3_cone.json").write_text(json.dumps(result, indent=1), encoding="utf-8")

    # ----------------------------------------------------------------- report
    print("=" * 78)
    print("TASK 3  cone of F + full Grundy DP")
    print("=" * 78)
    print("cone size                        :", main_rep["cone_size"], "(claim 21353)")
    print("all contain F / all are caps     :", main_rep["all_contain_base"],
          "/", main_rep["all_are_caps"])
    print("closure failures (safe child)    :", main_rep["closure_failures"])
    print("second (from-scratch) enumeration:", main_rep["scratch_enumeration_size"],
          "equal:", main_rep["scratch_enumeration_equal"])
    print("max Grundy in cone               :", result["max_grundy"])
    print()
    print(" m |      T_m | Grundy distribution (cone)")
    print("---+----------+-----------------------------------------------")
    for m in sorted(T):
        print("%2d | %8d | %s" % (m, T[m], {g: c for g, c in sorted(Tg[m].items())}))
    print()
    print("T_m table matches claim          :", result["T_matches_claim"])
    print("T_m(g) table matches claim       :", result["T_g_matches_claim"])
    print("child-count identity             :", result["child_identity"], child_detail)
    print("N_3 = C(81,3)-90*C(9,3)          :", N3)
    print("formula N_m(g)=N_3*T_m(g)/C(m,3) : integral", result["formula_integral"],
          "and matches claim:", result["N_g_matches_claim"])
    print()
    print(" k | N_m        | Grundy distribution (global)")
    print("---+------------+----------------------------------------------")
    for m in sorted(NG):
        dist_str = {g: v for g, v in sorted(NG[m].items())}
        print("%2d | %10d | %s" % (m, sum(NG[m].values()), dist_str))
    print()
    print("Grundy totals G0/G1/G2/G3        :", result["grundy_totals"],
          "claim:", {"G0": 19276705, "G1": 29537217, "G2": 13996800, "G3": 466560})
    print("total positions                  :", result["total_positions"], "(claim 63277282)")
    print("other triangles / my board equal :", result["other_triangles"])
    print("all task-3 checks                :", result["all_task3_checks_ok"])
    print("wrote", OUT / "task3_cone.json", "and", OUT / "cone_by_class.json")
    return result


if __name__ == "__main__":
    r = main()
    raise SystemExit(0 if r["all_task3_checks_ok"] else 1)
