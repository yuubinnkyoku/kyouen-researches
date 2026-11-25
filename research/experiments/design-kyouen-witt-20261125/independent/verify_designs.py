"""Task 1: verify from the board files alone that each board is the claimed
Steiner t-design.  For every t-subset count the blocks containing it.

Run:
    python independent/verify_designs.py
"""
import itertools
import json
from collections import Counter

from common import CLAIMS, TAGS, binomial, load_board, save_json


def lambda_counts(v, blocks, t):
    """Return Counter {t-subset-tuple: number of blocks containing it}."""
    cnt = Counter()
    for B in blocks:
        for sub in itertools.combinations(sorted(B), t):
            cnt[sub] += 1
    return cnt


def check_design(tag):
    cl = CLAIMS[tag]
    v, blocks = load_board(tag)
    k = len(blocks[0])
    res = {
        "tag": tag,
        "name": cl["name"],
        "v": v,
        "b": len(blocks),
        "k_distinct": sorted(set(len(B) for B in blocks)),
        "k": k,
        "claimed_t": cl["t"],
        "claimed_lambda": {str(t): cl["lam"][t] for t in cl["lam"]},
    }
    ok = True
    ok &= v == cl["v"]
    ok &= len(blocks) == cl["b"]
    ok &= k == cl["k"]
    # each block is a set of k distinct points in range
    for B in blocks:
        ok &= len(set(B)) == k and len(B) == k
        ok &= all(0 <= p < v for p in B)
    # no repeated blocks
    ok &= len(set(frozenset(B) for B in blocks)) == len(blocks)
    # every point is used
    used = set()
    for B in blocks:
        used.update(B)
    ok &= used == set(range(v))
    res["point_union"] = sorted(used)
    res["basic_ok"] = bool(ok)

    # t-range: claimed design t plus one extra (to see whether it happens to be
    # a (t+1)-design as well); for 5-designs no 6-design is claimed.
    t_max = cl["t"]
    for t in range(2, t_max + 1):
        cnt = lambda_counts(v, blocks, t)
        total = binomial(v, t)
        vals = Counter(cnt.values())
        lam = None
        if len(vals) == 1:
            (lam,) = vals
        uniform = lam is not None and len(cnt) == total
        # double counting: b*C(k,t) = lambda*C(v,t) if uniform
        double = len(blocks) * binomial(k, t)
        res["lambda_%d" % t] = {
            "num_subsets": total,
            "covered_subsets": len(cnt),
            "value_distribution": {str(x): c for x, c in sorted(vals.items())},
            "uniform": uniform,
            "lambda": lam,
            "claimed": cl["lam"][t],
            "matches_claim": uniform and lam == cl["lam"][t],
            "double_count_b_times_Ckt": double,
            "double_count_matches": double == (lam or -1) * total,
        }
        ok &= uniform and lam == cl["lam"][t]

    # extra: lambda_4 range for the 3-designs (report claims 0..1), and lambda_5
    # range where cheap enough.
    extra_t = t_max + 1
    if binomial(v, extra_t) * 1 <= 2_000_000:
        cnt = lambda_counts(v, blocks, extra_t)
        vals = Counter(cnt.values())
        total = binomial(v, extra_t)
        zeros = total - len(cnt)
        dist = {str(x): c for x, c in sorted(vals.items())}
        if zeros:
            dist["0"] = zeros
        res["lambda_%d_extra" % extra_t] = {
            "num_subsets": total,
            "covered_subsets": len(cnt),
            "value_distribution": dist,
            "range": [min(cnt.values(), default=0) if zeros == 0 else 0,
                      max(cnt.values()) if cnt else 0],
            "max": max(cnt.values()) if cnt else 0,
        }
    res["ok"] = bool(ok)
    return res


def main():
    results = [check_design(tag) for tag in TAGS]
    save_json("task1_designs.json", results)
    for r in results:
        print("=" * 78)
        print("%s (%s)  v=%d b=%d k=%d  t=%d" %
              (r["tag"], r["name"], r["v"], r["b"], r["k"], r["claimed_t"]))
        print("  basic board sanity:", "OK" if r["basic_ok"] else "FAIL")
        for t in range(2, r["claimed_t"] + 1):
            d = r["lambda_%d" % t]
            print("  t=%d: %6d subsets, all covered=%s, lambda=%s (claimed %s) "
                  "double-count %d = %d*%d -> %s" %
                  (t, d["num_subsets"], len(d["value_distribution"]) == 1 and
                   d["covered_subsets"] == d["num_subsets"], d["lambda"],
                   d["claimed"], d["double_count_b_times_Ckt"], d["lambda"],
                   d["num_subsets"], "OK" if d["double_count_matches"] else "FAIL"))
            print("       value distribution:", d["value_distribution"],
                  "->", "OK" if d["matches_claim"] else "FAIL")
        et = r["claimed_t"] + 1
        key = "lambda_%d_extra" % et
        if key in r:
            d = r[key]
            print("  t=%d (not claimed): %d subsets, value distribution %s, max %d" %
                  (et, d["num_subsets"], d["value_distribution"], d["max"]))
        print("  RESULT:", "PASS" if r["ok"] else "FAIL")
    print("=" * 78)
    print("all designs:", "PASS" if all(r["ok"] for r in results) else "FAIL")


if __name__ == "__main__":
    main()
