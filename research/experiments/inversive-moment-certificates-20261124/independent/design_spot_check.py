#!/usr/bin/env python3
"""Supplementary, independent check of the design context and moment identities.

This script does NOT verify the parent's builder.  It takes an already
generated block list for q=9 (the smallest q in Theorems B and C) and checks
the 3-design axioms directly from the list.  Any 3-(q^2+1,q+1,1) design
satisfies the four moment identities, so this is a concrete sanity check of
the context used by the certificates.

It also loads the published arc witnesses for q=9 and checks from scratch
that they really are s-arcs (every block meets them in at most s points),
then evaluates the moment functional on their true t_r vectors.

Read-only inputs (sibling experiment):
  ../inversive-spectrum-20261124/output/board_q9.json
  ../inversive-spectrum-20261124/output/witness_q9_s4_n16.json
  ../inversive-spectrum-20261124/output/witness_q9_s9_n57.json

Output: output/design_spot_check.json
"""

from __future__ import annotations

import json
from collections import Counter
from itertools import combinations
from math import comb
from pathlib import Path

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
SPECTRUM = HERE.parent.parent / "inversive-spectrum-20261124" / "output"


def coeffs_s(s):
    return (
        s * (s - 3) * (s - 2),
        -(s - 3) * (3 * s - 4),
        2 * (3 * s - 8),
        -6,
    )


def Y_int(coeffs, n, q):
    a0, a1, a2, a3 = coeffs
    return (
        a0 * q * (q * q + 1)
        + a1 * n * q * (q + 1)
        + a2 * comb(n, 2) * (q + 1)
        + a3 * comb(n, 3)
    )


def P_eval(s, r):
    return -((r - (s - 3)) * (r - (s - 2)) * (r - s))


def moments(t, n, q):
    """Return the four moment sums and their design-theoretic values."""
    s0 = sum(t.values())
    s1 = sum(r * c for r, c in t.items())
    s2 = sum(comb(r, 2) * c for r, c in t.items())
    s3 = sum(comb(r, 3) * c for r, c in t.items())
    return {
        "sum_t": s0,
        "sum_r_t": s1,
        "sum_C2_t": s2,
        "sum_C3_t": s3,
        "expected_sum_t": q * (q * q + 1),
        "expected_sum_r_t": n * q * (q + 1),
        "expected_sum_C2_t": comb(n, 2) * (q + 1),
        "expected_sum_C3_t": comb(n, 3),
    }


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def main():
    board_path = SPECTRUM / "board_q9.json"
    if not board_path.exists():
        print(f"SKIP: {board_path} not found")
        return

    board = load_json(board_path)
    q = board["q"]
    v = board["v"]
    b = board["b"]
    k = board["block_size"]
    blocks = [tuple(sorted(bl)) for bl in board["blocks"]]
    results = {"q": q, "v": v, "b": b, "k": k, "checks": {}, "witnesses": {}}

    def check(cond, label, detail=None):
        if not cond:
            raise AssertionError(f"{label}: {detail}")
        results["checks"].setdefault("passed", 0)
        results["checks"]["passed"] += 1

    check(q == 9, "board q", q)
    check(v == q * q + 1 == 82, "v", v)
    check(b == q * (q * q + 1) == 738, "b", b)
    check(k == q + 1 == 10, "k", k)
    check(len(blocks) == b, "block count", len(blocks))
    check(len(set(blocks)) == b, "blocks distinct", len(set(blocks)))
    check(all(len(bl) == k for bl in blocks), "all block sizes", {len(bl) for bl in blocks})
    check(all(len(set(bl)) == k for bl in blocks), "no repeated points in block")
    check(all(0 <= x < v for bl in blocks for x in bl), "point labels in range")

    # Pair multiplicities.
    pair = Counter()
    for bl in blocks:
        for x, y in combinations(bl, 2):
            pair[(x, y)] += 1
    check(len(pair) == comb(v, 2), "every pair occurs", len(pair))
    check(set(pair.values()) == {q + 1}, "pair multiplicity q+1", set(pair.values()))

    # Triple multiplicities: all C(v,3) triples exactly once.
    triples = set()
    duplicate = False
    for bl in blocks:
        for tri in combinations(bl, 3):
            if tri in triples:
                duplicate = True
            triples.add(tri)
    check(not duplicate, "no triple on two blocks")
    check(len(triples) == comb(v, 3), "every triple exactly once", len(triples))

    point_degree = Counter(x for bl in blocks for x in bl)
    check(set(point_degree.values()) == {q * (q + 1)}, "point degree q(q+1)",
          set(point_degree.values()))
    results["checks"]["pair_multiplicity"] = q + 1
    results["checks"]["triple_count"] = len(triples)
    results["checks"]["point_degree"] = q * (q + 1)

    # Moment identities on arbitrary subsets.
    subset_sizes = [0, 1, 2, 3, 4, 5, 10, 16, 20, 28, 57, 82]
    subset_rows = []
    for n in subset_sizes:
        S = set(range(n))
        t = Counter(len(S & set(bl)) for bl in blocks)
        m = moments(t, n, q)
        for key in ("sum_t", "sum_r_t", "sum_C2_t", "sum_C3_t"):
            check(m[key] == m["expected_" + key], f"moment {key} for n={n}",
                  (m[key], m["expected_" + key]))
        row = {"n": n, "t": {str(r): c for r, c in sorted(t.items())}}
        # Check the linear functional on P_4, P_5 and P_9 for every subset.
        for s in (4, 5, 9):
            lhs = sum(P_eval(s, r) * c for r, c in t.items())
            rhs = Y_int(coeffs_s(s), n, q)
            check(lhs == rhs, f"Y on actual t_r, s={s}, n={n}", (lhs, rhs))
            row[f"sum_P{s}"] = lhs
            row[f"Y{s}"] = rhs
        subset_rows.append(row)
    results["checks"]["subsets"] = subset_rows

    # Published arc witnesses: verify the arc property from scratch.
    for s, name in ((4, "witness_q9_s4_n16.json"), (9, "witness_q9_s9_n57.json")):
        path = SPECTRUM / name
        if not path.exists():
            results["witnesses"][name] = "missing"
            continue
        w = load_json(path)
        pts = w["points"]
        check(w["q"] == q, f"{name} q", w["q"])
        check(w["s"] == s, f"{name} s", w["s"])
        check(w["n"] == len(pts), f"{name} n", (w["n"], len(pts)))
        check(len(set(pts)) == len(pts), f"{name} distinct")
        check(all(0 <= x < v for x in pts), f"{name} labels")
        S = set(pts)
        t = Counter(len(S & set(bl)) for bl in blocks)
        max_r = max(t)
        check(max_r <= s, f"{name} is an s-arc", (max_r, s))
        check(all(t.get(r, 0) == 0 for r in range(s + 1, k + 1)),
              f"{name} t_r=0 for r>s")
        m = moments(t, len(S), q)
        for key in ("sum_t", "sum_r_t", "sum_C2_t", "sum_C3_t"):
            check(m[key] == m["expected_" + key], f"{name} moment {key}",
                  (m[key], m["expected_" + key]))
        lhs = sum(P_eval(s, r) * c for r, c in t.items())
        rhs = Y_int(coeffs_s(s), len(S), q)
        check(lhs == rhs, f"{name} sum P_s = Y", (lhs, rhs))
        check(lhs >= 0, f"{name} nonnegative certificate value", lhs)
        results["witnesses"][name] = {
            "s": s,
            "n": len(S),
            "max_block_intersection": max_r,
            "t": {str(r): c for r, c in sorted(t.items())},
            "sum_P_s": lhs,
            "Y": rhs,
        }

    # Boundary values at the critical sizes for the q=9 instances.
    crit = {}
    for s in range(5, q):
        n = (s - 2) * q + 1
        y = Y_int(coeffs_s(s), n, q)
        W = q * (s - 1) * (s - 4) - s * (s - 2) * (s - 3) - 2
        check(y == -q * W, f"q=9 critical s={s}", (y, -q * W))
        check(y < 0, f"q=9 critical negative s={s}", y)
        crit[s] = {"n": n, "Y": y, "W": W}
    results["q9_critical_values"] = crit
    y4 = Y_int(coeffs_s(4), 2 * q + 2, q)
    check(y4 == -4 * (q * q - 5 * q - 2), "q=9 theorem A critical", y4)
    check(y4 < 0, "q=9 theorem A negative", y4)
    results["q9_critical_values"]["A_s4"] = {"n": 2 * q + 2, "Y": y4}
    yC = Y_int((-12, 12, -10, 6), 2 * q - 1, q)
    check(yC == -2 * (q - 8) * (q - 1), "q=9 theorem C critical", yC)
    check(yC < 0, "q=9 theorem C negative", yC)
    results["q9_critical_values"]["C_blocking"] = {"m": 2 * q - 1, "Y": yC}

    results["status"] = "PASS"
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "design_spot_check.json").write_text(
        json.dumps(results, indent=1, ensure_ascii=False), encoding="utf-8"
    )
    print(json.dumps(results, indent=1, ensure_ascii=False))


if __name__ == "__main__":
    main()
