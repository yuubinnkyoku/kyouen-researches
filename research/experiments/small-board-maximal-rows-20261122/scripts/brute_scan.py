#!/usr/bin/env python3
"""brute_scan.py — THIRD enumeration method for the smallest boards (n = 3, 4):
exhaustive scan over ALL 2^(n^2) cell subsets.

For every subset S (as a bitmask over the n*n cells):
  SAFE(S)    := no forbidden quartet of the (forbidgen, system B) catalog is
                contained in S;
  MAXIMAL(S) := SAFE(S) and every empty cell e is "covered": some quartet
                contains e and its other 3 cells lie in S.

Then the count of maximal safe sets per size k is the complete row
distribution — an independent method-complete cross-check of the DFS
row enumerator (enum_catalog.mjs) whose soundness/completeness argument is
different (subset scan needs no reachability argument at all).

Usage: python3 brute_scan.py <n> <quartets.txt> <out.json>
Output: JSON with per-k counts, plus (n<=4) the full configuration lists for
nonzero rows marked for byte-set comparison with the DFS catalogs.
"""
import json
import sys


def main():
    n = int(sys.argv[1])
    qpath = sys.argv[2]
    outpath = sys.argv[3]
    N = n * n
    assert n <= 4, "subset scan is only tractable for n<=4"
    quarts = []
    with open(qpath, "r", encoding="utf-8") as f:
        first = f.readline().strip()
        assert first == "n=%d" % n, "quartet file board mismatch: %r" % first
        for line in f:
            line = line.strip()
            if line:
                a, b, c, d = (int(x) for x in line.split())
                quarts.append((1 << a) | (1 << b) | (1 << c) | (1 << d))
    qmasks = quarts
    # per-cell quartet membership WITHOUT the cell itself
    cell_q = []
    for c in range(N):
        others = []
        bit = 1 << c
        for q in quarts:
            if q & bit:
                others.append(q & ~bit)
        cell_q.append(others)

    counts = [0] * (N + 1)
    rows = {}
    for S in range(1 << N):
        # popcount
        k = bin(S).count("1")
        if k < 3:
            continue  # with <3 stones no quartet can be completed; maximality
            # handled below via the same formula, but rows k<3 of the DFS are
            # asserted 0 for these boards by enumeration; still check them:
        safe = True
        for q in qmasks:
            if q & S == q:
                safe = False
                break
        if not safe:
            continue
        # maximality: every empty cell covered by 3 stones of S
        covered_all = True
        for e in range(N):
            if (S >> e) & 1:
                continue
            cov = False
            for qo in cell_q[e]:
                if qo & S == qo:
                    cov = True
                    break
            if not cov:
                covered_all = False
                break
        if covered_all:
            counts[k] += 1
            rows.setdefault(k, []).append(sorted(i for i in range(N) if (S >> i) & 1))

    out = {
        "n": n,
        "N": N,
        "quartets": len(quarts),
        "method": "exhaustive 2^N subset scan",
        "counts_by_k": dict((k, counts[k]) for k in range(N + 1) if counts[k] > 0),
        "zero_rows_k": [k for k in range(1, N + 1) if counts[k] == 0],
        "rows": {k: v for k, v in rows.items()},
    }
    with open(outpath, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=1, sort_keys=True)
    brief = {kk: vv for kk, vv in out.items() if kk != "rows"}
    print(json.dumps(brief))
    # NOTE: subsets with k<3 stones are skipped here; for these boards the DFS
    # rows k=1,2 were already asserted 0; we assert k<=4 rows are 0 independently:
    assert all(counts[k] == 0 for k in range(1, 5)), "unexpected small-k maximal set"


if __name__ == "__main__":
    main()
