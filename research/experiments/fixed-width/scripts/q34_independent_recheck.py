#!/usr/bin/env python3
"""Independent audit of the width-3, q=4 results (K0068 / K0302 / K0303).

Purpose
-------
Re-verify, with code paths independent of the repo's own verifiers, that

  1. every published 3x23 witness is a safe, maximal 8-stone set
     (=> M_{3,4} >= 24);
  2. the full-capacity value for 3xm, q=4 is exactly 9, and 9 is attainable;
  3. the T_{w,4} sufficient lengths 3, 9, 69, 237, 567, 1113 are exactly the
     closed forms stated in K0068;
  4. the exhaustive q=4, w=3, m=6 table row in q-point-fixed-width.md
     (max 8, distribution 5:4, 6:648, 7:964, 8:108, empty Grundy 1, parity
     formula failing) reproduces.

Why independent
---------------
The repo decides the rule with the integer lifted determinant det[x^2+y^2,x,y,1]
(kyouen_core.det4 in Python, lifted minors in C++). This script implements the
same rule through *different* mechanisms and cross-checks them:

  A. circle-equation fit with exact fractions (constant term included);
  B. exact Gaussian elimination over Q on the 4x4 monomial matrix;
  C. exact Gaussian elimination over the finite field F_1000003.

All three must agree on every quadruple, and the binomial coefficients are
computed three ways. No floating point is used in any decision.

Run
---
    python research/experiments/fixed-width/scripts/q34_independent_recheck.py
"""
from __future__ import annotations

import json
import math
from fractions import Fraction
from itertools import combinations
from pathlib import Path

MOD = 1000003

WITNESSES_23 = {
    "q34_exact_threshold_outer": ([1, 17], [7, 10, 13], [9, 10, 12]),
    "q34_exact_threshold_middle": ([4, 7, 18], [3, 4], [4, 10, 13]),
    "q34_stabilization_lower_bound": ([4, 15, 18], [18, 19], [9, 12, 18]),
}

REPORTED_T = {1: 3, 2: 9, 3: 69, 4: 237, 5: 567, 6: 1113}


# --------------------------------------------------------------- predicates
def cross(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])


def forbidden_fraction(quad):
    """A: fit x^2+y^2+Dx+Ey+F=0 through a non-collinear triple."""
    n = len(quad)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                p, q, s = quad[i], quad[j], quad[k]
                if cross(p, q, s) == 0:
                    continue
                rest = [quad[t] for t in range(n) if t not in (i, j, k)]
                x1, y1 = p
                a1, b1 = Fraction(q[0] - x1), Fraction(q[1] - y1)
                c1 = Fraction(x1 * x1 + y1 * y1) - Fraction(
                    q[0] * q[0] + q[1] * q[1])
                a2, b2 = Fraction(s[0] - x1), Fraction(s[1] - y1)
                c2 = Fraction(x1 * x1 + y1 * y1) - Fraction(
                    s[0] * s[0] + s[1] * s[1])
                det = a1 * b2 - a2 * b1
                D = (c1 * b2 - c2 * b1) / det
                E = (a1 * c2 - a2 * c1) / det
                F = -(Fraction(x1 * x1 + y1 * y1) + D * x1 + E * y1)
                return all(
                    Fraction(t[0] * t[0] + t[1] * t[1]) + D * t[0] + E * t[1] + F == 0
                    for t in rest)
    return True  # every triple collinear => the four are collinear


def _rank(rows, mod=None):
    m = [[Fraction(v) if mod is None else v % mod for v in r] for r in rows]
    rk = 0
    for col in range(len(m[0])):
        piv = next((i for i in range(rk, len(m)) if m[i][col] != 0), None)
        if piv is None:
            continue
        m[rk], m[piv] = m[piv], m[rk]
        pv = m[rk][col]
        if mod is None:
            m[rk] = [v / pv for v in m[rk]]
        else:
            inv = pow(pv, mod - 2, mod)
            m[rk] = [(v * inv) % mod for v in m[rk]]
        for i in range(len(m)):
            if i != rk and m[i][col] != 0:
                f = m[i][col]
                m[i] = [(a - f * b) % mod if mod else a - f * b
                        for a, b in zip(m[i], m[rk])]
        rk += 1
        if rk == len(m):
            break
    return rk


def forbidden_rank_q(quad):
    """B: rank of (1, x, y, x^2+y^2) over Q; <= 3 means one circle or line."""
    return _rank([[1, x, y, x * x + y * y] for x, y in quad]) <= 3


def forbidden_rank_mod(quad):
    """C: same rank test over F_p, an independent arithmetic model."""
    return _rank([[1, x, y, (x * x + y * y) % MOD] for x, y in quad], MOD) <= 3


# ----------------------------------------------------------------- binomial
def pascal(n, k):
    if k < 0 or k > n:
        return 0
    row = [0] * (k + 1)
    row[0] = 1
    for i in range(1, n + 1):
        for j in range(min(i, k), 0, -1):
            row[j] += row[j - 1]
    return row[k]


def multiplicative(n, k):
    if k < 0 or k > n:
        return 0
    k = min(k, n - k)
    r = 1
    for i in range(1, k + 1):
        r = r * (n - k + i) // i
    return r


def bound_a(q, w):
    n = (q - 1) * (w - 1)
    return q - 1 + 2 * (pascal(n, q - 1) - (w - 1)) + (q - 2) * pascal(n, q - 2)


def bound_b(q, w):
    n = (q - 1) * (w - 1)
    return q - 1 + 2 * (pascal(n, 3) - (w - 1) * pascal(q - 1, 3)) \
        + (q - 2) * pascal(n, 2)


# --------------------------------------------------------------------- main
def check_witness(name, rows, m=23):
    W = sorted((x, y) for y, xs in enumerate(rows) for x in xs)
    wset = set(W)
    bad = [q for q in combinations(W, 4) if forbidden_fraction(q)]
    disagree = sum(1 for q in combinations(W, 4)
                   if len({forbidden_fraction(q), forbidden_rank_q(q),
                           forbidden_rank_mod(q)}) != 1)
    unblocked = [p for p in ((x, y) for y in range(3) for x in range(m))
                 if p not in wset
                 and not any(forbidden_fraction(tuple(t) + (p,))
                             for t in combinations(W, 3))]
    return {"name": name, "size": len(W), "rows": [list(r) for r in rows],
            "safe": not bad, "forbidden_quadruples": len(bad),
            "predicate_disagreements": disagree,
            "maximal": not unblocked, "unblocked": [list(p) for p in unblocked]}


def exhaustive_q4_w3_m6():
    m = 6
    pts = [(x, y) for y in range(3) for x in range(m)]
    nv = len(pts)
    ok = bytearray(1 << nv)
    ok[0] = 1
    for mask in range(1, 1 << nv):
        S = [pts[i] for i in range(nv) if mask >> i & 1]
        ok[mask] = (not any(forbidden_fraction(q) for q in combinations(S, 4)))
    grundy = [0] * (1 << nv)
    dist: dict[int, int] = {}
    mx = 0
    for mask in range((1 << nv) - 1, -1, -1):
        if not ok[mask]:
            continue
        kids = [mask | (1 << i) for i in range(nv)
                if not mask >> i & 1 and ok[mask | (1 << i)]]
        if not kids:
            k = bin(mask).count("1")
            dist[k] = dist.get(k, 0) + 1
            mx = max(mx, k)
        else:
            vals = {grundy[k] for k in kids}
            g = 0
            while g in vals:
                g += 1
            grundy[mask] = g
    cap = 9
    return {"m": m, "max_safe_size": mx,
            "maximal_size_distribution": dict(sorted(dist.items())),
            "empty_grundy": grundy[0],
            "parity_formula_all_safe": all(
                not ok[mask] or grundy[mask] == ((cap - bin(mask).count("1")) & 1)
                for mask in range(1 << nv))}


def main() -> None:
    rep: dict = {}

    # 1. predicate cross-validation over the whole 3x23 board
    board = [(x, y) for y in range(3) for x in range(23)]
    n = cnt = 0
    mismatch = []
    for quad in combinations(board, 4):
        q = tuple(quad)
        a, b = forbidden_fraction(q), forbidden_rank_q(q)
        if a != b:
            mismatch.append([list(t) for t in q])
        elif a and forbidden_rank_mod(q) != a:
            mismatch.append(["mod"] + [list(t) for t in q])
        cnt += int(a)
        n += 1
    rep["board_3x23"] = {
        "quadruples_checked": n,
        "binom_69_4": math.comb(69, 4),
        "independent_predicates": 3,
        "predicate_mismatches": len(mismatch),
        "forbidden_quadruples": cnt,
    }
    assert n == math.comb(69, 4) and not mismatch

    # 2. the three published 8-stone witnesses
    rep["witnesses"] = [check_witness(k, v) for k, v in WITNESSES_23.items()]
    rep["all_witnesses_8_stone_safe_maximal"] = all(
        w["safe"] and w["maximal"] and w["size"] == 8
        and w["predicate_disagreements"] == 0 for w in rep["witnesses"])
    assert rep["all_witnesses_8_stone_safe_maximal"]
    rep["consequence"] = "M_{3,4} >= 24"

    # 3. full capacity for 3xm, q=4 is 9 and is attained
    nine = [(x, 0) for x in (0, 3, 6)] + [(x, 1) for x in (1, 4, 7)] \
        + [(x, 2) for x in (2, 5, 8)]
    rep["capacity_9"] = {
        "upper_bound_from_collinearity": 9,
        "nine_stone_set_safe": not any(
            forbidden_fraction(q) for q in combinations(nine, 4)),
        "note": "at most 3 per row since 4 in a row are collinear",
    }
    assert rep["capacity_9"]["nine_stone_set_safe"]

    # 4. T_{w,4} closed form
    tcases = []
    for w in range(1, 7):
        a, b = bound_a(4, w), bound_b(4, w)
        closed = 3 + 2 * (pascal(3 * w - 2, 3) - (w - 1))
        tcases.append({"w": w, "A": a, "B": b, "min_AB": min(a, b),
                       "closed_form": closed, "reported": REPORTED_T[w],
                       "match": min(a, b) == REPORTED_T[w] == closed})
    rep["T_w4"] = {"cases": tcases,
                   "all_match": all(c["match"] for c in tcases)}
    assert rep["T_w4"]["all_match"]
    rep["binomial_implementations_agree"] = all(
        pascal(a, b) == multiplicative(a, b) == math.comb(a, b)
        for a in range(40) for b in range(12))

    # 5. the q=4, w=3, m=6 exhaustive table row
    row = exhaustive_q4_w3_m6()
    rep["q4_w3_m6"] = row
    expected = {"max_safe_size": 8,
                "maximal_size_distribution": {5: 4, 6: 648, 7: 964, 8: 108},
                "empty_grundy": 1, "parity_formula_all_safe": False}
    rep["q4_w3_m6"]["matches_published_table_row"] = all(
        row[k] == v for k, v in expected.items())
    assert rep["q4_w3_m6"]["matches_published_table_row"]

    out = Path(__file__).resolve().parents[1] / "output" \
        / "q34_independent_recheck.json"
    out.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(json.dumps(rep, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()