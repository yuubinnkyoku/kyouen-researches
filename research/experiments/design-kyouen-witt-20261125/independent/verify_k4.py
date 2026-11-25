"""Task 5: independent K_4 verification (max |S| with |S cap B| <= 4).

Two independent routes per board:
  (a) exhaustive increasing-point DFS enumerating every 4-safe set;
  (b) an exact counting (moment) upper bound: if a safe set of size K+1 existed,
      the block-intersection profile x_j would have to satisfy the moment
      identities; infeasibility of that integer system proves |S| <= K.
A witness of size K then pins the value.

Run: python independent/verify_k4.py
"""
from collections import Counter
import itertools

from common import (CLAIMS, TAGS, binomial, board_lambdas, enumerate_safe,
                    load_board, load_ks_ilp, mask_points, save_json)
from moments import moment_solutions

CLAIMED_K4 = {"ag32": 8, "ag42": 16, "w11": 6, "w12": 4, "w22": 10,
              "w23": 8, "w24": 4}
NAMES = {"ag32": "AG(3,2)", "ag42": "AG(4,2)", "w11": "W_11", "w12": "W_12",
         "w22": "W_22", "w23": "W_23", "w24": "W_24"}


def k4_report(tag):
    v, blocks = load_board(tag)
    k = len(blocks[0])
    claimed = CLAIMED_K4[tag]
    safe = enumerate_safe(v, blocks, 4)
    size_of = {m: m.bit_count() for m in safe}
    by_size = Counter(size_of.values())
    K = max(by_size)
    top = [m for m in safe if size_of[m] == K]
    design_t = CLAIMS[tag]["t"]
    lam = board_lambdas(v, blocks, design_t)

    # moment upper bound at K+1 (only meaningful when K+1 <= v)
    s = K + 1
    if s <= v:
        status, sols = moment_solutions(v, blocks, 4, s, lam, design_t)
    else:
        status, sols = "trivial(v)", []

    # why the structural cases are trivial
    structural = None
    if k <= 4:
        structural = ("every block has k=%d <= 4 points, so the whole point set "
                      "is 4-safe; K_4 = v = %d" % (k, v))
    elif design_t >= 5:
        structural = ("5-design: every 5-subset lies in a block, so every 5-set "
                      "is unsafe; every 4-set is safe; K_4 = 4")

    r = {
        "tag": tag,
        "name": NAMES[tag],
        "v": v,
        "b": len(blocks),
        "k": k,
        "K4_exhaustive": K,
        "K4_claimed": claimed,
        "K4_match": K == claimed,
        "num_4safe_sets": len(safe),
        "size_counts": {str(j): by_size.get(j, 0) for j in sorted(by_size)},
        "num_size_K_sets": len(top),
        "witness": mask_points(top[0]),
        "all_witness_blocks_at_most_4": max(
            sum(1 for p in B if top[0] >> p & 1) for B in blocks) <= 4,
        "moment_K_plus_1_s": s,
        "moment_K_plus_1_status": status,
        "moment_K_plus_1_solutions": sols if isinstance(sols, list) else [],
        "lambdas_from_board": {str(t): lam[t] for t in sorted(lam)},
        "structural_reason": structural,
    }
    return r


def main():
    ilp = {d["name"]: d for d in load_ks_ilp()["designs"]}
    results = [k4_report(tag) for tag in TAGS]
    for r in results:
        r["ilp_K4"] = ilp[r["name"]]["K4"]
        r["ilp_K4_match"] = r["ilp_K4"] == r["K4_exhaustive"]
    save_json("task5_k4.json", results)

    for r in results:
        print("=" * 78)
        print("%s (%s) v=%d b=%d k=%d" % (r["tag"], r["name"], r["v"], r["b"], r["k"]))
        print("  exhaustive 4-safe enumeration: %d sets, size counts %s" %
              (r["num_4safe_sets"], r["size_counts"]))
        print("  K_4 = %d (claimed %d) -> %s ; %d sets of size K" %
              (r["K4_exhaustive"], r["K4_claimed"],
               "OK" if r["K4_match"] else "FAIL", r["num_size_K_sets"]))
        print("  witness:", r["witness"],
              "| block intersections <=4:", r["all_witness_blocks_at_most_4"])
        if r["structural_reason"]:
            print("  structural:", r["structural_reason"])
        print("  moment system for s=K+1=%d: %s" %
              (r["moment_K_plus_1_s"], r["moment_K_plus_1_status"]))
        print("  ILP K4 = %d -> %s" % (r["ilp_K4"],
                                       "OK" if r["ilp_K4_match"] else "FAIL"))
    print("=" * 78)
    ok = all(r["K4_match"] and r["ilp_K4_match"] and
             r["all_witness_blocks_at_most_4"] and
             r["moment_K_plus_1_status"] in ("infeasible", "trivial(v)")
             for r in results)
    print("TASK 5:", "PASS" if ok else "FAIL")


if __name__ == "__main__":
    main()
