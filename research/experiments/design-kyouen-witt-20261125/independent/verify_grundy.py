"""Task 4: independent normal-play and misere Grundy computation.

For every board, enumerate all safe sets (<=3 points per block), build the game
graph (moves = add one point keeping safety), and compute
  * normal-play Grundy values by mex (descending by size),
  * misere win/loss (terminal position is a win for the player to move).
Compare with output/summary.json and verify the graded-parity formula
  Grundy(S) = (K - |S|) mod 2,   misere(S) = (K - |S| + 1) mod 2.

Run: python independent/verify_grundy.py
"""
from collections import Counter

from common import (TAGS, block_masks, enumerate_safe, load_board,
                    load_summary, mask_points, save_json)

NAMES = {"ag32": "AG(3,2)", "ag42": "AG(4,2)", "w11": "W_11", "w12": "W_12",
         "w22": "W_22", "w23": "W_23", "w24": "W_24"}


def compute(tag, v, blocks):
    safe = enumerate_safe(v, blocks, 3)
    safe_set = set(safe)
    by_size = {}
    for m in safe:
        by_size.setdefault(m.bit_count(), []).append(m)
    K = max(by_size)
    grundy = {}
    win = {}
    for size in range(K, -1, -1):
        for m in by_size[size]:
            opts = [m | (1 << p) for p in range(v)
                    if not (m >> p & 1) and (m | (1 << p)) in safe_set]
            vals = {grundy[o] for o in opts}
            g = 0
            while g in vals:
                g += 1
            grundy[m] = g
            win[m] = True if not opts else any(not win[o] for o in opts)
    return safe, K, grundy, win


def main():
    summary = {d["name"]: d for d in load_summary()["designs"]}
    results = []
    for tag in TAGS:
        v, blocks = load_board(tag)
        safe, K, grundy, win = compute(tag, v, blocks)
        dist = Counter(grundy.values())
        root = grundy[0]
        root_misere = 1 if win[0] else 0
        g0_by_size = {}
        for m, g in grundy.items():
            if g == 0:
                g0_by_size[m.bit_count()] = g0_by_size.get(m.bit_count(), 0) + 1
        parity_ok = all(grundy[m] == ((K - m.bit_count()) % 2) for m in safe)
        misere_parity_ok = all(win[m] == bool(((K - m.bit_count() + 1) % 2))
                               for m in safe)
        rep = summary[NAMES[tag]]
        report_dist = {int(k): c for k, c in rep["grundy_distribution"].items()}
        report_g0 = {int(j): rep["size_counts"][str(j)]["grundy0"]
                     for j in rep["size_counts"]}
        r = {
            "tag": tag,
            "v": v,
            "b": len(blocks),
            "num_safe": len(safe),
            "K": K,
            "grundy_distribution": {str(k): c for k, c in sorted(dist.items())},
            "grundy0_by_size": {str(j): g0_by_size.get(j, 0) for j in sorted(g0_by_size)},
            "root_grundy": root,
            "root_normal_P": root == 0,
            "root_misere": root_misere,
            "only_0_1": set(dist) <= {0, 1},
            "graded_parity_formula_holds": parity_ok,
            "misere_parity_formula_holds": misere_parity_ok,
            "report_grundy_distribution": {str(k): c for k, c in sorted(report_dist.items())},
            "report_grundy_distribution_match": dict(dist) == report_dist,
            "report_root_grundy": rep["root_grundy"],
            "report_root_grundy_match": rep["root_grundy"] == root,
            "report_root_misere": rep["root_misere"],
            "report_root_misere_match": rep["root_misere"] == root_misere,
            "report_grundy0_by_size": {str(j): c for j, c in sorted(report_g0.items())},
            "report_grundy0_by_size_match": all(
                g0_by_size.get(j, 0) == c for j, c in report_g0.items()),
        }
        results.append(r)

    save_json("task4_grundy.json", results)
    print("%-5s %3s %4s %6s %-14s %-12s %-9s %-9s %s" %
          ("tag", "v", "K", "safe", "grundy dist", "report dist", "G(0)", "misere(0)", "checks"))
    for r in results:
        print("%-5s %3d %4d %6d %-14s %-12s %-9s %-9s %s" %
              (r["tag"], r["v"], r["K"], r["num_safe"],
               r["grundy_distribution"], r["report_grundy_distribution"],
               r["root_grundy"], r["root_misere"],
               "OK" if (r["report_grundy_distribution_match"] and
                        r["report_root_grundy_match"] and
                        r["report_root_misere_match"] and
                        r["report_grundy0_by_size_match"] and
                        r["only_0_1"] and r["graded_parity_formula_holds"] and
                        r["misere_parity_formula_holds"]) else "FAIL"))
        print("      parity Grundy=(K-|S|)%%2: %s ; misere=(K-|S|+1)%%2: %s ; "
              "G(0)=K%%2: %s ; empty board: %s" %
              (r["graded_parity_formula_holds"], r["misere_parity_formula_holds"],
               r["root_grundy"] == r["K"] % 2,
               "P (second player wins)" if r["root_normal_P"] else "N (first player wins)"))
    checks = [r["report_grundy_distribution_match"] and r["report_root_grundy_match"]
              and r["report_root_misere_match"] and r["report_grundy0_by_size_match"]
              and r["only_0_1"] and r["graded_parity_formula_holds"]
              and r["misere_parity_formula_holds"] for r in results]
    outcomes = {r["tag"]: ("P" if r["root_normal_P"] else "N") for r in results}
    claimed = {"ag32": "P", "ag42": "P", "w11": "N", "w12": "N", "w22": "N",
               "w23": "N", "w24": "N"}
    print()
    print("outcomes:", outcomes)
    print("claimed :", claimed)
    print("TASK 4:", "PASS" if all(checks) and outcomes == claimed else "FAIL")


if __name__ == "__main__":
    main()
