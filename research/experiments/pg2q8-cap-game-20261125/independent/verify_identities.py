#!/usr/bin/env python3
"""Cross-check the three independent censuses and the extension-graph identities.

  * SIZE / TOTAL / maximal-count lines of cap_census.exe, cap_census_alt.exe and
    python_census.py must agree.
  * For every size k:  sum_a a * ADDHIST[k][a] == (k+1) * cnt[k+1]
    (counting the edges of the "one point extension" graph in two ways) and
    sum_a ADDHIST[k][a] == cnt[k].
"""
import sys


def read_log(path):
    sizes, maxs, hist, total, maxsizes = {}, {}, {}, None, None
    with open(path, encoding="utf-8") as f:
        for ln in f:
            t = ln.split()
            if not t:
                continue
            if t[0] == "SIZE":
                sizes[int(t[1])] = int(t[2])
                if len(t) > 3:
                    maxs[int(t[1])] = int(t[3])
            elif t[0] == "TOTAL":
                total = int(t[1])
            elif t[0] == "ADDHIST":
                hist[(int(t[1]), int(t[2]))] = int(t[3])
            elif t[0] == "MAXSIZES":
                maxsizes = ln.strip()
    return sizes, maxs, hist, total, maxsizes


def main():
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    boards = {
        "PG": {"main": "census_pg_main.log",
               "alt": "census_pg_alt.log",
               "py": "python_census_pg.log"},
        "AG": {"main": "census_ag_main.log",
               "alt": "census_ag_alt.log",
               "py": "python_census_ag.log"},
    }
    failures = 0
    for tag, logs in boards.items():
        print("=" * 78)
        print(f"{tag}: census cross-checks and extension identities")
        print("=" * 78)
        data = {k: read_log(v) for k, v in logs.items()}
        ref_sizes, _, hist, ref_total, _ = data["main"]
        ref_maxs = data["main"][1]
        for which in ("alt", "py"):
            sizes, maxs, _, total, _ = data[which]
            ok = (sizes == ref_sizes and total == ref_total
                  and (not maxs or maxs == ref_maxs))
            if not ok:
                for k in sorted(set(sizes) | set(ref_sizes)):
                    if sizes.get(k) != ref_sizes.get(k):
                        print(f"  FAIL {which}: size {k}: {sizes.get(k)} != {ref_sizes.get(k)}")
                if total != ref_total:
                    print(f"  FAIL {which}: total {total} != {ref_total}")
                if maxs and maxs != ref_maxs:
                    for k in sorted(set(maxs) | set(ref_maxs)):
                        if maxs.get(k) != ref_maxs.get(k):
                            print(f"  FAIL {which}: maximal {k}: {maxs.get(k)} != {ref_maxs.get(k)}")
                failures += 1
            print(f"  {'PASS' if ok else 'FAIL'}  {which} census agrees with main census"
                  f"   (total={total})")
        # maxsize from main
        maxsize = max(ref_sizes)
        # consistency of ADDHIST with sizes and extension graph
        for k in range(maxsize + 1):
            hsum = sum(v for (kk, a), v in hist.items() if kk == k)
            hval = sum(a * v for (kk, a), v in hist.items() if kk == k)
            ok1 = hsum == ref_sizes.get(k, 0)
            ok2 = hval == (k + 1) * ref_sizes.get(k + 1, 0) if k < maxsize else (hval == 0)
            if not (ok1 and ok2):
                failures += 1
            print(f"  size {k:2d}: caps={ref_sizes.get(k,0):>9}  "
                  f"addhist-sum={hsum:>9} {'ok' if ok1 else 'MISMATCH'}  "
                  f"sum(addable)={hval:>11} vs (k+1)*caps[k+1]="
                  f"{(k+1)*ref_sizes.get(k+1,0):>11} {'ok' if ok2 else 'MISMATCH'}")
        # maximal-cap containment identities:
        # every k-subset of a maximal m-cap is a k-cap; if the counts match
        # exactly, all caps of those sizes are subsets of maximal caps.
        import math
        if tag == "PG":
            m6 = ref_maxs[6]
            m10 = ref_maxs[10]
            idents = [
                (6, m6 + m10 * math.comb(10, 6)),
                (7, m10 * math.comb(10, 7)),
                (8, m10 * math.comb(10, 8)),
                (9, m10 * math.comb(10, 9)),
                (10, m10),
            ]
            desc = f"max6={m6}, max10={m10}"
        else:
            m6 = ref_maxs[6]
            m8 = ref_maxs[8]
            m10 = ref_maxs[10]
            idents = [
                (6, m6 + m8 * math.comb(8, 6) + m10 * math.comb(10, 6)),
                (7, m8 * math.comb(8, 7) + m10 * math.comb(10, 7)),
                (8, m8 + m10 * math.comb(10, 8)),
                (9, m10 * math.comb(10, 9)),
                (10, m10),
            ]
            desc = f"max6={m6}, max8={m8}, max10={m10}"
        print(f"  maximal caps: {desc}")
        for k, expect in idents:
            ok = ref_sizes.get(k, 0) == expect
            if not ok:
                failures += 1
            print(f"  containment identity for size {k}: caps={ref_sizes.get(k,0)} "
                  f"vs subsets-of-maximal-caps={expect}  {'ok' if ok else 'MISMATCH'}")
        print()
    print("=" * 78)
    print(f"RESULT: {'PASS' if failures == 0 else f'FAIL ({failures})'}")
    print("=" * 78)
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
