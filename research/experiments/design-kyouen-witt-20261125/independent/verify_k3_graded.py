"""Tasks 2 and 3: independent K_3 values and the "graded game" claim.

Task 2: K_3 = max |S| with |S cap B| <= 3 for every block B, computed by
        exhaustive enumeration of all safe sets (increasing-point DFS).
        For W_22 additionally an explicit 7-set witness and a complete
        counting proof that no 8-set exists.
Task 3: enumerate all safe sets (<=3 per block), verify every safe set extends
        to a maximal safe set of size exactly K, and compare size counts with
        the report.

Run: python independent/verify_k3_graded.py
"""
from collections import Counter

from common import (CLAIMED_K3, CLAIMS, TAGS, board_lambdas, enumerate_safe,
                    load_board, load_ks_ilp, load_summary, mask_points,
                    block_intersections, save_json)
from moments import moment_solutions

CLAIMED_SIZE_COUNTS = {
    "ag32": [1, 8, 28, 56, 56],
    "w11": [1, 11, 55, 165],
    "w22": [1, 22, 231, 1540, 6160, 7392, 2464, 352],
}


def k3_report(tag):
    v, blocks = load_board(tag)
    safe = enumerate_safe(v, blocks, 3)
    safe_set = set(safe)
    size_of = {m: m.bit_count() for m in safe}
    by_size = Counter(size_of.values())
    K = max(size_of.values())

    # maximal safe sets: no safe extension by one point
    maximal = []
    for m in safe:
        ext = False
        for p in range(v):
            if not (m >> p & 1) and (m | (1 << p)) in safe_set:
                ext = True
                break
        if not ext:
            maximal.append(m)
    max_by_size = Counter(size_of[m] for m in maximal)

    # extension property: every safe set lies in a size-K safe set
    top = [m for m in safe if size_of[m] == K]
    failed = []
    for m in safe:
        if size_of[m] == K:
            continue
        if not any((m & t) == m for t in top):
            failed.append(m)

    # K+1 existence (should be empty by definition of K, sanity check)
    return {
        "tag": tag,
        "v": v,
        "b": len(blocks),
        "k": len(blocks[0]),
        "num_safe": len(safe),
        "size_counts": [by_size.get(j, 0) for j in range(K + 1)],
        "K3_exhaustive": K,
        "maximal_by_size": {str(j): max_by_size.get(j, 0) for j in sorted(max_by_size)},
        "num_maximal": len(maximal),
        "all_maximal_size_K": len(maximal) == by_size[K] and set(max_by_size) == {K},
        "all_safe_extend_to_K": not failed,
        "num_not_extendable": len(failed),
        "K3_claimed": CLAIMED_K3[tag],
        "K3_match": K == CLAIMED_K3[tag],
        "top_sets": top,
    }


def w22_no8_proof(v, blocks):
    """Counting proof (self-contained) that no 8-set is safe in W_22.

    All design parameters are recomputed from the board file.  A set S of size 8
    with |S cap B| <= 3 would give x_j = #{blocks: |S cap B| = j}, j = 0..3,
    satisfying
        x_0+x_1+x_2+x_3 = b
        x_1+2x_2+3x_3 = 8*r
        x_2+3x_3 = lambda_2*C(8,2)
        x_3 = lambda_3*C(8,3)
    but the last two equations contradict: x_2 = lambda_2*28 - 3*lambda_3*56 < 0.
    """
    lam = board_lambdas(v, blocks, 3)
    status, sols = moment_solutions(v, blocks, 3, 8, lam, 3)
    b = len(blocks)
    per_point = [0] * v
    for B in blocks:
        for p in B:
            per_point[p] += 1
    r = per_point[0]
    x3 = lam[3] * 56
    pair_incidences = lam[2] * 28
    x2 = pair_incidences - 3 * x3
    return {
        "b": b,
        "r": r,
        "lambda2": lam[2],
        "lambda3": lam[3],
        "moment_status_for_s8": status,
        "moment_solutions": sols,
        "explicit_x3": x3,
        "explicit_pair_incidences": pair_incidences,
        "explicit_x2": x2,
        "contradiction": x2 < 0,
        "argument": ("every triple of the 8-set lies in exactly one block, so "
                     "exactly C(8,3)*lambda3=56 blocks meet S in 3 points; those "
                     "blocks already contribute 3*56=168 pair-block incidences, "
                     "but the 8-set has only C(8,2)*lambda2=28*5=140 pair-block "
                     "incidences; 168>140."),
    }


def w22_witness(tag):
    v, blocks = load_board(tag)
    safe = enumerate_safe(v, blocks, 3)
    seven = [m for m in safe if m.bit_count() == 7]
    m = seven[0]
    pts = mask_points(m)
    inter = block_intersections(m, blocks)
    return {
        "points": pts,
        "num_size7_safe_sets": len(seven),
        "max_block_intersection": max(inter),
        "block_intersection_distribution": {str(j): c for j, c in
                                            sorted(Counter(inter).items())},
        "all_blocks_at_most_3": max(inter) <= 3,
        "other_size7_witnesses": [[p for p in mask_points(x)] for x in seven[1:4]],
    }


def main():
    summary = {d["name"]: d for d in load_summary()["designs"]}
    ilp = {d["name"]: d for d in load_ks_ilp()["designs"]}
    names = {"ag32": "AG(3,2)", "ag42": "AG(4,2)", "w11": "W_11", "w12": "W_12",
             "w22": "W_22", "w23": "W_23", "w24": "W_24"}
    results = []
    for tag in TAGS:
        r = k3_report(tag)
        rep = summary[names[tag]]
        # independent counting (moment) upper bound at K3+1
        vv, bb = load_board(tag)
        lam = board_lambdas(vv, bb, CLAIMS[tag]["t"])
        st, sols = moment_solutions(vv, bb, 3, r["K3_exhaustive"] + 1,
                                    lam, CLAIMS[tag]["t"])
        r["moment_K3_plus_1_s"] = r["K3_exhaustive"] + 1
        r["moment_K3_plus_1_status"] = st
        r["moment_K3_plus_1_solutions"] = sols[:3]
        r["report_size_counts"] = [rep["size_counts"][str(j)]["count"]
                                   if str(j) in rep["size_counts"] else 0
                                   for j in range(len(r["size_counts"]))]
        r["report_size_counts_match"] = r["size_counts"] == r["report_size_counts"]
        r["report_safe_match"] = r["num_safe"] == rep["safe"]
        r["report_maximal_match"] = (
            r["maximal_by_size"].get(str(r["K3_exhaustive"]), 0)
            == rep["size_counts"].get(str(r["K3_exhaustive"]), {}).get("maximal", -1))
        r["ks_ilp_K3"] = ilp[names[tag]]["K3"]
        r["ks_ilp_K3_match"] = r["ks_ilp_K3"] == r["K3_exhaustive"]
        # free the big lists before json
        r["top_sets"] = [mask_points(m) for m in r["top_sets"]][:5]
        results.append(r)

    w22 = w22_no8_proof(*load_board("w22"))
    w22w = w22_witness("w22")

    out = {"boards": results, "w22_no8_proof": w22, "w22_witness": w22w}
    save_json("task2_3_k3_graded.json", out)

    print("%-5s %3s %4s %6s %-28s %-10s %-6s %-6s %s" %
          ("tag", "v", "K3", "safe", "size_counts", "maximal", "claim", "counts", "extend"))
    for r in results:
        print("%-5s %3d %4d %6d %-28s %-10s %-6s %-6s %s" %
              (r["tag"], r["v"], r["K3_exhaustive"], r["num_safe"],
               ",".join(map(str, r["size_counts"])),
               ",".join("%s:%d" % (j, r["maximal_by_size"].get(str(j), 0))
                        for j in sorted(r["maximal_by_size"], key=int)),
               "OK" if r["K3_match"] else "FAIL",
               "OK" if r["report_size_counts_match"] else "FAIL",
               "OK" if r["all_safe_extend_to_K"] else "FAIL"))
        print("      all maximal sets have size K: %s ; maximal count %d ; "
              "report safe %d -> %s ; ILP K3 %d -> %s" %
              (r["all_maximal_size_K"], r["num_maximal"], r["report_safe_match"],
               "OK" if r["report_safe_match"] else "FAIL",
               r["ks_ilp_K3"], "OK" if r["ks_ilp_K3_match"] else "FAIL"))
        print("      moment counting bound at s=K3+1=%d: %s" %
              (r["moment_K3_plus_1_s"], r["moment_K3_plus_1_status"]))
    print()
    print("W_22 explicit 7-set witness:", w22w["points"])
    print("  block intersection distribution:", w22w["block_intersection_distribution"])
    print("  max intersection:", w22w["max_block_intersection"], "->",
          "SAFE" if w22w["all_blocks_at_most_3"] else "UNSAFE")
    print("W_22 no-8-set counting proof:", w22["moment_status_for_s8"],
          "| x3 =", w22["explicit_x3"], ", x2 =", w22["explicit_x2"],
          "-> contradiction:", w22["contradiction"])
    print()
    print("CLAIMED_SIZE_COUNTS check:")
    for tag, claimed in CLAIMED_SIZE_COUNTS.items():
        r = next(x for x in results if x["tag"] == tag)
        print("  %-4s claimed %-30s computed %-30s %s" %
              (tag, claimed, r["size_counts"],
               "OK" if claimed == r["size_counts"] else "FAIL"))
    ok = all(r["K3_match"] and r["report_size_counts_match"] and
             r["all_safe_extend_to_K"] and r["all_maximal_size_K"] and
             r["report_safe_match"] and r["ks_ilp_K3_match"] for r in results)
    print()
    print("TASK 2+3:", "PASS" if ok and w22["contradiction"] else "FAIL")


if __name__ == "__main__":
    main()
