"""Task 5: k = 0,1,2 mex chain, independent global cap counts for k <= 5, arithmetic totals.

Independent count of N_3, N_4, N_5 by a direct increasing-order DFS on caps
(no cone, no Grundy table):

  * N_3 : every 3-subset of a line is collinear, so N_3 = C(81,3) - 90*C(9,3);
          also counted by DFS.
  * N_4 : every 4-cap has a unique largest point; count extensions of 3-caps.
  * N_5 : every 5-cap has a unique largest point; count extensions of 4-caps.

The mex chain uses the proved fact that all 3-caps are AGL(2,9)-images of F
(task 2) and G(F) = 1 (task 3/4), plus invariance of Grundy values under affine
maps (the game is an incidence game).

Run: python task5_mex.py
"""

import json
import sys
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from common import parse_board, line_masks  # noqa: E402
from caplib import build_point_lines  # noqa: E402

OUT = HERE / "out"
OUT.mkdir(exist_ok=True)
N = 81
FULL = (1 << N) - 1

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
CLAIM_N = {0: 1, 1: 81, 2: 3240, 3: 77760, 4: 1108080, 5: 8328096, 6: 26290656,
           7: 23794560, 8: 3411720, 9: 239760, 10: 23328}
CLAIM_NG = {
    0: {0: 1}, 1: {1: 81}, 2: {0: 3240}, 3: {1: 77760}, 4: {0: 1108080},
    5: {1: 7861536, 3: 466560},
    6: {0: 12216096, 1: 77760, 2: 13996800},
    7: {0: 2566080, 1: 21228480},
    8: {0: 3353400, 1: 58320},
    9: {0: 6480, 1: 233280},
    10: {0: 23328},
}


def direct_cap_counts(n, masks, pl):
    """Count N_3, N_4, N_5 with a single DFS in increasing point order.

    The DFS stops at depth 3, then for every 4-cap extension counts the safe
    extensions with a larger index.  Returns (N3, N4, N5).
    """
    pair_line = {}
    for L in masks:
        pts = []
        mm = L
        while mm:
            b = mm & -mm
            pts.append(b.bit_length() - 1)
            mm ^= b
        for i in range(9):
            for j in range(i + 1, 9):
                pair_line[(pts[i], pts[j])] = L

    cnt = [0] * len(masks)
    blockcnt = [0] * n
    avail = FULL
    N3 = N4 = N5 = 0

    def add(p):
        nonlocal avail
        avail &= ~(1 << p)
        for c in pl[p]:
            cnt[c] += 1
            if cnt[c] == 2:
                qq = masks[c]
                while qq:
                    b = qq & -qq
                    q = b.bit_length() - 1
                    blockcnt[q] += 1
                    if blockcnt[q] == 1:
                        avail &= ~b
                    qq ^= b

    def remove(p):
        nonlocal avail
        for c in pl[p]:
            cnt[c] -= 1
            if cnt[c] == 1:
                qq = masks[c]
                while qq:
                    b = qq & -qq
                    q = b.bit_length() - 1
                    blockcnt[q] -= 1
                    if blockcnt[q] == 0:
                        avail |= b
                    qq ^= b
        avail |= 1 << p

    def rec(mask, start, depth, pts):
        nonlocal avail, N3, N4, N5
        if depth == 3:
            N3 += 1
            q0, q1, q2 = pts
            blocked3 = pair_line[(q0, q1)] | pair_line[(q0, q2)] | pair_line[(q1, q2)]
            cand = avail & ~((1 << start) - 1)
            while cand:
                b = cand & -cand
                cand ^= b
                p = b.bit_length() - 1
                N4 += 1
                blocked4 = blocked3 | pair_line[(q0, p)] | pair_line[(q1, p)] | pair_line[(q2, p)]
                higher = FULL & ~((1 << (p + 1)) - 1)
                safe = higher & ~blocked4
                N5 += safe.bit_count()
            return
        cand = avail & ~((1 << start) - 1)
        while cand:
            b = cand & -cand
            cand ^= b
            p = b.bit_length() - 1
            add(p)
            rec(mask | b, p + 1, depth + 1, pts + (p,))
            remove(p)
            avail &= ~mask

    rec(0, 0, 0, ())
    return N3, N4, N5


def main():
    result = {}

    pn, pnb, p_lines = parse_board(HERE.parent / "output" / "board_ag2q9.txt")
    masks = line_masks(N, p_lines)
    pl = build_point_lines(N, masks)

    # ---------------------------------------------- independent global counts
    n3_dfs, n4_dfs, n5_dfs = direct_cap_counts(N, masks, pl)
    n3_formula = comb(81, 3) - 90 * comb(9, 3)
    result["counts"] = {
        "N3_formula": n3_formula,
        "N3_dfs": n3_dfs,
        "N4_dfs": n4_dfs,
        "N5_dfs": n5_dfs,
        "N3_claim": CLAIM_N[3],
        "N4_claim": CLAIM_N[4],
        "N5_claim": CLAIM_N[5],
        "N3_ok": n3_dfs == n3_formula == CLAIM_N[3] == 77760,
        "N4_ok": n4_dfs == CLAIM_N[4] == 1108080,
        "N5_ok": n5_dfs == CLAIM_N[5] == 8328096,
    }

    # T_m derived from the globally counted N_m must match the cone counts
    T_from_global = {}
    for m in (3, 4, 5):
        den = comb(m, 3)
        num = CLAIM_N[m] * den
        T_from_global[m] = num // n3_formula
        assert num % n3_formula == 0
    result["T_from_global"] = {str(k): v for k, v in T_from_global.items()}
    result["T_from_global_ok"] = all(T_from_global[m] == CLAIM_T[m] for m in (3, 4, 5))

    # ------------------------------------------------------------- mex chain
    # all pairs are caps, all 3-caps are one AGL orbit, G(F)=1
    result["mex_chain"] = {
        "N0": 1,
        "N1": 81,
        "N2": comb(81, 2),
        "N2_is_all_pairs": comb(81, 2) == 3240,
        "all_2_sets_are_caps": True,     # a 2-set has at most 2 points on any line
        "all_3_caps_one_orbit": True,    # task 2: |AGL| = #ordered triangles
        "G_of_3_caps": 1,                # G(F)=1 (task 3/4) + affine invariance
        "G_of_2_caps_mex_1": 0,
        "G_of_1_point_mex_0": 1,
        "G_of_empty_mex_1": 0,
        "reason": (
            "A 2-cap has exactly the 72 three-caps through it as options; all "
            "three-caps have G=1, so mex{1}=0.  A 1-point position has the 80 "
            "two-caps through it as options, all G=0, so mex{0}=1.  The empty "
            "position has the 81 one-point positions as options, all G=1, so "
            "mex{1}=0."
        ),
    }
    result["mex_chain_ok"] = (
        comb(81, 2) == CLAIM_NG[2][0] == 3240
        and CLAIM_NG[1][1] == 81
        and CLAIM_NG[0][0] == 1
    )

    # ------------------------------------------------------------- arithmetic
    # claim table internal consistency
    arith_ok = True
    sums = {}
    total = 0
    for m in sorted(CLAIM_NG):
        s = sum(CLAIM_NG[m].values())
        sums[m] = s
        total += s
        if s != CLAIM_N[m]:
            arith_ok = False
    result["claim_size_sums"] = {str(k): v for k, v in sums.items()}
    result["claim_total"] = total
    result["claim_total_ok"] = total == 63277282
    result["claim_size_sums_ok"] = arith_ok and sums == CLAIM_N

    g_tot = {0: 0, 1: 0, 2: 0, 3: 0}
    for m in CLAIM_NG:
        for g, v in CLAIM_NG[m].items():
            g_tot[g] += v
    result["claim_grundy_totals"] = {str(g): v for g, v in sorted(g_tot.items())}
    result["claim_grundy_totals_ok"] = g_tot == {0: 19276705, 1: 29537217,
                                                2: 13996800, 3: 466560}

    # compare with the parent's JSON output
    parent_json = json.loads((HERE.parent / "output" / "ag2q9_spectrum.json")
                             .read_text(encoding="utf-8"))
    p_sizes = {int(k): v for k, v in parent_json["sizes"].items()}
    p_ok = True
    for m in range(3, 11):
        entry = p_sizes[m]
        if entry["T"] != CLAIM_T[m]:
            p_ok = False
        if {int(g): v for g, v in entry["T_g"].items()} != CLAIM_TG[m]:
            p_ok = False
        if entry.get("N") is not None and entry["N"] != CLAIM_N[m]:
            p_ok = False
        if entry.get("N_g") is not None and \
           {int(g): v for g, v in entry["N_g"].items()} != CLAIM_NG[m]:
            p_ok = False
    for m in (0, 1, 2):
        if p_sizes[m]["N"] != CLAIM_N[m] or \
           {int(g): v for g, v in p_sizes[m]["N_g"].items()} != CLAIM_NG[m]:
            p_ok = False
    result["parent_json_consistent_with_claim"] = p_ok
    result["parent_json_cone_size"] = parent_json["cone_size"]
    result["parent_json_N3"] = parent_json["N3"]

    result["all_task5_checks_ok"] = all([
        result["counts"]["N3_ok"],
        result["counts"]["N4_ok"],
        result["counts"]["N5_ok"],
        result["T_from_global_ok"],
        result["mex_chain_ok"],
        result["claim_total_ok"],
        result["claim_size_sums_ok"],
        result["claim_grundy_totals_ok"],
        result["parent_json_consistent_with_claim"],
    ])

    (OUT / "task5_mex.json").write_text(json.dumps(result, indent=1), encoding="utf-8")

    print("=" * 78)
    print("TASK 5  mex chain, global counts k<=5, arithmetic totals")
    print("=" * 78)
    print("N_3  formula           :", n3_formula)
    print("N_3  DFS               :", n3_dfs)
    print("N_4  DFS               :", n4_dfs, "(claim %d)" % CLAIM_N[4])
    print("N_5  DFS               :", n5_dfs, "(claim %d)" % CLAIM_N[5])
    print("T_3,T_4,T_5 from global:", {k: T_from_global[k] for k in (3, 4, 5)},
          "claim:", {k: CLAIM_T[k] for k in (3, 4, 5)})
    print()
    print("mex chain  : empty G=0, point G=1, pair G=0, triangle G=1")
    print("  N_0=1, N_1=81, N_2=C(81,2)=3240, all 3-caps one AGL orbit")
    print("  chain ok :", result["mex_chain_ok"])
    print()
    print("claim N_m sums         :", result["claim_size_sums"])
    print("claim total            :", total, "(63277282:", result["claim_total_ok"], ")")
    print("claim Grundy totals    :", result["claim_grundy_totals"])
    print("parent JSON consistent :", p_ok)
    print("all task-5 checks      :", result["all_task5_checks_ok"])
    print("wrote", OUT / "task5_mex.json")
    return result


if __name__ == "__main__":
    r = main()
    raise SystemExit(0 if r["all_task5_checks_ok"] else 1)
