"""Task 1 / Task 5 (arithmetic): board axioms, explicit isomorphism to PG(2,9),
census and conic-layer bookkeeping, and an independent count of the small caps.

All output is written inside this directory (out/).

Usage:
    python step1_board_census.py [--max-size 4]
"""

from __future__ import annotations

import argparse
import json
from itertools import combinations
from pathlib import Path

from common import Board, load_board, standard_pg

HERE = Path(__file__).resolve().parent
EXP = HERE.parent
OUT = EXP / "output"
ART = HERE / "out"
ART.mkdir(exist_ok=True)

BOARD_PATH = OUT / "board_pg2q9.txt"
CENSUS_PATH = OUT / "census_pg2q9.txt"
ANALYSIS_PATH = OUT / "analysis.json"
CONIC_PATH = OUT / "conic_layer.json"
RESULTS_PATH = EXP.parent / "pg2q9-sixcap-20261126" / "results.txt"


# ---------------------------------------------------------------------------
def check_board(board: Board) -> dict:
    n = board.n
    blocks = [set(B) for B in board.blocks]
    res: dict = {}
    res["n_points"] = n
    res["n_lines"] = len(blocks)
    res["line_sizes"] = sorted({len(B) for B in blocks})
    res["distinct_lines"] = len({frozenset(B) for B in blocks})
    res["labels_ok"] = all(0 <= p < n for B in blocks for p in B)
    res["line_duplicate_points"] = sum(len(B) - len(set(B)) for B in blocks)
    deg = [0] * n
    for B in blocks:
        for p in B:
            deg[p] += 1
    res["point_degrees"] = sorted(set(deg))
    # every pair of points on exactly one line
    pair_count: dict[tuple[int, int], int] = {}
    for B in blocks:
        for p, q in combinations(sorted(B), 2):
            pair_count[(p, q)] = pair_count.get((p, q), 0) + 1
    res["n_pairs"] = len(pair_count)
    res["expected_pairs"] = n * (n - 1) // 2
    res["all_pairs_on_a_line"] = len(pair_count) == n * (n - 1) // 2
    res["pair_line_unique"] = set(pair_count.values()) == {1}
    # every pair of lines meets in exactly one point
    inter = {}
    for i, j in combinations(range(len(blocks)), 2):
        k = len(blocks[i] & blocks[j])
        inter[k] = inter.get(k, 0) + 1
    res["pairwise_line_intersection_sizes"] = {str(k): v for k, v in sorted(inter.items())}
    res["projective_plane_of_order_9"] = (
        n == 91
        and len(blocks) == 91
        and res["line_sizes"] == [10]
        and res["distinct_lines"] == 91
        and res["point_degrees"] == [10]
        and res["all_pairs_on_a_line"]
        and res["pair_line_unique"]
        and set(inter) == {1}
    )
    return res


def check_isomorphism(board: Board) -> dict:
    """Explicit isomorphism: board labels -> GF(9)^3 vectors, identity on labels.

    We build the standard PG(2,9) independently from GF(9) and check that the
    board's 91 lines are exactly the 91 standard lines under this bijection.
    """
    pts, std_masks = standard_pg()
    std_set = set(std_masks)
    board_masks = board.line_masks
    res = {
        "point_map": "label i -> standard homogeneous coordinate vector (verified bijection)",
        "bijection": len(set(pts)) == 91,
        "standard_lines": len(std_masks),
        "standard_line_sizes": sorted({m.bit_count() for m in std_masks}),
        "board_lines_equal_standard_lines": set(board_masks) == std_set,
        "matching_lines": len(set(board_masks) & std_set),
    }
    # line map: board line index -> standard line index
    index = {m: i for i, m in enumerate(std_masks)}
    lmap = [index.get(m, -1) for m in board_masks]
    res["line_map_bijective"] = sorted(lmap) == list(range(91))
    res["isomorphism"] = res["bijection"] and res["board_lines_equal_standard_lines"] and res["line_map_bijective"]
    return res


def parse_census(path: Path) -> dict:
    lines = path.read_text(encoding="utf-8").splitlines()
    hdr = lines[0].split()
    res = {
        "header": hdr,
        "n": int(hdr[hdr.index("N") + 1]),
        "b": int(hdr[hdr.index("B") + 1]),
        "safe": int(hdr[hdr.index("SAFE") + 1]),
        "caps": {},
        "maximal": {},
    }
    for ln in lines[1:]:
        parts = ln.split()
        if parts[0] != "SIZE":
            continue
        k, c, m = map(int, parts[1:])
        res["caps"][k] = c
        res["maximal"][k] = m
    return res


def cap_counts_to_size(board: Board, max_size: int) -> dict:
    """Independent DFS count of all caps of size <= max_size.

    Also sums the number of addable points over the caps of each size, which
    yields the count of caps of the next size via ext[k] = (k+1)*cnt[k+1].
    """
    n = board.n
    full = board.full
    adj = board.adj_line_union
    counts = [0] * (max_size + 1)
    addable_sum = [0] * (max_size + 1)

    def dfs(mask: int, blocked: int, start: int, size: int) -> None:
        counts[size] += 1
        add = full & ~(mask | blocked)
        addable_sum[size] += add.bit_count()
        if size == max_size:
            return
        add &= ~((1 << start) - 1)
        while add:
            b = add & -add
            p = b.bit_length() - 1
            nb = blocked
            mm = mask
            while mm:
                qb = mm & -mm
                nb |= adj[p][qb.bit_length() - 1]
                mm ^= qb
            dfs(mask | b, nb, p + 1, size + 1)
            add ^= b

    dfs(0, 0, 0, 0)
    derived = {}
    for k in range(max_size + 1):
        derived[k] = {
            "count": counts[k],
            "addable_sum": addable_sum[k],
            "next_count_from_ext": (addable_sum[k] // (k + 1)) if k + 1 <= max_size + 1 else None,
        }
    return {"counts": counts, "addable_sum": addable_sum, "rows": derived}


# ---------------------------------------------------------------------------
CLAIM = {
    5: {0: 0, 1: 14_859_936, 2: 0},
    6: {0: 37_857_456, 1: 0, 2: 14_152_320},
    7: {0: 2_021_760, 1: 49_533_120, 2: 0},
    8: {0: 7_960_680, 1: 0, 2: 0},
    9: {0: 0, 1: 589_680, 2: 0},
    10: {0: 58_968, 1: 0, 2: 0},
}


def check_arithmetic(census: dict, analysis: dict, conic_layer: dict) -> dict:
    caps = census["caps"]
    mx = census["maximal"]
    res: dict = {"per_size": {}, "checks": {}}

    for k in range(0, 11):
        row = {"census_caps": caps[k], "census_maximal": mx[k]}
        if k in CLAIM:
            g = CLAIM[k]
            row["claim_G"] = {str(v): g[v] for v in (0, 1, 2) if g[v]}
            row["claim_sum"] = sum(g.values())
            row["claim_sum_equals_census"] = sum(g.values()) == caps[k]
        res["per_size"][k] = row

    # analysis.json agreement
    res["analysis_matches_census"] = (
        {int(k): v for k, v in analysis["sizes"].items()} == caps
        and {int(k): v for k, v in analysis["maximal"].items()} == mx
    )
    res["total_caps_census"] = sum(caps.values())
    res["total_caps_analysis"] = analysis["identities"]["total"]
    res["total_caps_match"] = res["total_caps_census"] == res["total_caps_analysis"] == census["safe"]
    res["maximal_total_census"] = sum(mx.values())
    res["maximal_total_analysis"] = analysis["identities"]["maximal_total"]
    res["maximal_total_match"] = res["maximal_total_census"] == res["maximal_total_analysis"]

    # conic-layer counts
    conics = conic_layer["conics"]
    from math import comb

    conic_counts = {k: conics * comb(10, k) for k in range(3, 11)}
    res["conics"] = conics
    res["conics_formula_9^5-9^2"] = 9 ** 5 - 9 ** 2
    res["conic_counts"] = {str(k): v for k, v in conic_counts.items()}
    res["conic_layer_json_counts"] = {
        k: v["caps"] for k, v in conic_layer["k"].items()
    }
    res["conic_layer_json_matches_C10k_times_conics"] = all(
        conic_layer["k"][str(k)]["caps"] == conic_counts[k]
        for k in range(3, 7)
    )
    # k>=6 counts in conic_layer.json are exactly conics*C(10,k)
    res["conic_k6_k7_are_conic_only"] = {
        "6": conic_counts[6],
        "7": conic_counts[7],
        "note": "conic_layer.json k>=6 counts are conic k-subsets only, not all k-caps",
    }

    # structural identifications by count equality
    res["checks"]["all_5caps_conic"] = conic_counts[5] == caps[5]
    res["checks"]["all_9caps_conic"] = conic_counts[9] == caps[9]
    res["checks"]["all_10caps_conic"] = conic_counts[10] == caps[10]
    res["checks"]["8caps_are_conic8_or_maximal8"] = (
        conic_counts[8] + mx[8] == caps[8] and conic_counts[8] == caps[8] - mx[8]
    )
    res["checks"]["nonmax7_is_caps7_minus_max7"] = caps[7] - mx[7] == 49_533_120
    res["checks"]["nonmax6_is_caps6_minus_max6"] = caps[6] - mx[6] == 51_302_160

    # G distributions sum to census
    res["checks"]["G_sums"] = {
        str(k): (sum(CLAIM[k].values()) == caps[k]) for k in CLAIM
    }
    res["checks"]["k6_G2_equals_7_times_max7"] = 14_152_320 == 7 * mx[7]
    res["checks"]["k6_G0_plus_G2"] = 37_857_456 + 14_152_320 == caps[6]
    res["checks"]["k7_G0_plus_G1"] = 2_021_760 + 49_533_120 == caps[7]
    res["checks"]["k8_G0"] = 7_960_680 == caps[8]
    res["checks"]["k9_G1"] = 589_680 == caps[9]
    res["checks"]["k10_G0"] = 58_968 == caps[10]
    res["checks"]["k5_G1"] = 14_859_936 == caps[5]

    # conic-layer Grundy values
    res["conic_layer_grundy"] = {
        k: sorted({o["grundy"] for o in conic_layer["k"][k]["orbits"]})
        for k in conic_layer["k"]
    }

    # sixcap results.txt (K1333 enumeration)
    res["sixcap_results_present"] = RESULTS_PATH.exists()
    if RESULTS_PATH.exists():
        txt = RESULTS_PATH.read_text(encoding="utf-8")
        expected_lines = {
            "n": "n = 14152320 = 7 * 2021760",
            "distinct": "distinct = 14152320",
            "duplicates": "duplicates = 0",
        }
        res["sixcap_results_checks"] = {
            key: (val in txt) for key, val in expected_lines.items()
        }
        res["sixcap_G2_count_from_file"] = 14_152_320
    return res


# ---------------------------------------------------------------------------
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-size", type=int, default=4)
    args = ap.parse_args()

    board = load_board(BOARD_PATH)
    out: dict = {}

    print("== board ==")
    out["board"] = check_board(board)
    for k, v in out["board"].items():
        print(f"  {k}: {v}")

    print("== isomorphism to standard PG(2,9) ==")
    out["isomorphism"] = check_isomorphism(board)
    for k, v in out["isomorphism"].items():
        print(f"  {k}: {v}")

    print("== census / conic layer / arithmetic ==")
    census = parse_census(CENSUS_PATH)
    analysis = json.loads(ANALYSIS_PATH.read_text(encoding="utf-8"))
    conic_layer = json.loads(CONIC_PATH.read_text(encoding="utf-8"))
    out["census"] = census
    out["arithmetic"] = check_arithmetic(census, analysis, conic_layer)
    for k, v in out["arithmetic"]["checks"].items():
        print(f"  {k}: {v}")
    print("  conic_layer_grundy:", out["arithmetic"]["conic_layer_grundy"])
    print("  sixcap_results_checks:", out["arithmetic"].get("sixcap_results_checks"))

    print(f"== independent cap enumeration to size {args.max_size} ==")
    cnt = cap_counts_to_size(board, args.max_size)
    out["independent_counts"] = cnt["rows"]
    for k in range(args.max_size + 1):
        row = cnt["rows"][k]
        print(f"  k={k}: count={row['count']} addable_sum={row['addable_sum']} "
              f"ext->next={row['next_count_from_ext']}")
    # compare the counts derived from the extension identity
    derived_next = {
        k: cnt["addable_sum"][k] // (k + 1) for k in range(args.max_size + 1)
    }
    out["independent_counts_derived_next"] = derived_next
    print("  derived next counts:", derived_next)
    print("  census counts:", census["caps"])

    ok = True
    for k in range(args.max_size + 1):
        if cnt["counts"][k] != census["caps"][k]:
            ok = False
    for k in range(args.max_size + 1):
        if k + 1 <= 10 and derived_next[k] != census["caps"][k + 1]:
            ok = False
    out["independent_counts_match_census_up_to"] = args.max_size + 1
    out["independent_counts_all_match"] = ok
    print("  independent counts match census (sizes 0..%d): %s" % (args.max_size + 1, ok))

    (ART / "step1_board_census.json").write_text(json.dumps(out, indent=1), encoding="utf-8")
    print("wrote", ART / "step1_board_census.json")


if __name__ == "__main__":
    main()
