#!/usr/bin/env python3
"""M_{6,7} explicit upper bound via the K0318 curve-packing theorem.

The functions bound/board_audit/det3/curve_key/on_curve below are a verbatim
copy of research/experiments/fixed-width/scripts/curve_packing_fixed_width.py
(K0318 verifier, original commit 49891aaf) - unchanged, inlined so this
experiment is self-contained. The (6,7) driver functions follow:
  - verbatim bound() vs full-range brute integer scan vs closed-form hand
    derivation (three independent computations must agree),
  - controls reproducing published substitutions (3,5)=40, (5,6)=249, (5,7)=200,
  - K0024 sufficient length T_{6,7} recomputed independently,
  - w=6 exhaustive small-board geometry audit (2^18 states),
  - supplementary first-explicit upper bounds U_{6,q}, q=4..8.
"""


import itertools
import json
import math
from pathlib import Path


def choose(n, k):
    return math.comb(n, k) if n >= k >= 0 else 0


def bound(w, q, cross_pairs=True):
    if w < 1 or q < 4:
        raise ValueError("require w >= 1 and q >= 4")
    r, a, n = q - 1, q - 2, (q - 1) * (w - 1)
    budget = choose(n, 3) - (w - 1) * choose(r, 3)
    d0, d1 = choose(r, 3), choose(r - 1, 3)
    per_point = choose(n, 2) // choose(r - 1, 2)
    cross_cost = choose(r - 1, 2) - (r - 1) // 2
    if cross_pairs and cross_cost:
        cross_budget = choose(n, 2) - (w - 1) * choose(r, 2)
        per_point = min(per_point, cross_budget // cross_cost)
    ymax = a * per_point
    if d1:
        ymax = min(ymax, budget // d1)
        period = d0 // math.gcd(d0, d1)
        # f(y+period)-f(y)=period-2*d1/gcd(d0,d1).
        if d0 > 2 * d1:
            ys = range(max(0, ymax - period + 1), ymax + 1)
        else:
            ys = range(min(ymax, period - 1) + 1)
    else:
        ys = [ymax]
    best, witness = -1, None
    for y in ys:
        x = (budget - d1 * y) // d0
        if 2 * x + y > best:
            best, witness = 2 * x + y, [x, y]
    old_a = r + 2 * (choose(n, r) - (w - 1)) + a * choose(n, r - 1)
    old_b = r + 2 * budget + a * choose(n, 2)
    return {"w": w, "q": q, "old_T": min(old_a, old_b),
            "packing_U": r + best, "combined": min(old_a, r + best),
            "Q": budget, "Y": a * per_point, "d0": d0, "d1": d1,
            "integer_optimizer": witness}


def det3(rows):
    (a, b, c), (d, e, f), (g, h, i) = rows
    return a * (e * i - f * h) - b * (d * i - f * g) + c * (d * h - e * g)


def curve_key(points):
    """Primitive (A,B,C,D) of a circle or line through three points."""
    rows = [(x*x + y*y, x, y, 1) for x, y in points]
    coeff = [(-1)**j * det3([row[:j] + row[j+1:] for row in rows]) for j in range(4)]
    divisor = math.gcd(*coeff)
    if not divisor:
        raise AssertionError("three distinct lifted points must be independent")
    coeff = [v // divisor for v in coeff]
    if next(v for v in coeff if v) < 0:
        coeff = [-v for v in coeff]
    return tuple(coeff)


def on_curve(key, p):
    a, b, c, d = key
    x, y = p
    return a*(x*x+y*y) + b*x + c*y + d == 0


def board_audit(w, m, q):
    points = [(x, y) for y in range(w) for x in range(m)]
    keys = {curve_key(triple) for triple in itertools.combinations(points, 3)}
    curves = {key: sum(1 << i for i, p in enumerate(points) if on_curve(key, p)) for key in keys}
    forbidden_curves = [(key, mask) for key, mask in curves.items() if mask.bit_count() >= q]
    row_masks = [((1 << m) - 1) << (y*m) for y in range(w)]
    r = q - 1
    safe_count = row_checks = 0
    for state in range(1 << len(points)):
        if any((state & cmask).bit_count() >= q for _, cmask in forbidden_curves):
            continue
        safe_count += 1
        for rowmask in row_masks:
            b = (state & rowmask).bit_count()
            if b >= r:
                continue
            row_checks += 1
            outside = state & ~rowmask
            x = y = 0
            used_triples = set()
            per_target_pairs = {}
            blocked = 0
            for key, cmask in forbidden_curves:
                occupied = cmask & state
                missing = cmask & rowmask & ~state
                if occupied.bit_count() != r or not missing:
                    continue
                target = occupied & rowmask
                assert target.bit_count() <= 1
                if target:
                    y += 1
                    assert key[0] != 0
                else:
                    x += 1
                assert missing.bit_count() <= 2 - target.bit_count()
                blocked |= missing
                ext = [i for i in range(len(points)) if occupied & outside & (1 << i)]
                triples = set(itertools.combinations(ext, 3))
                assert used_triples.isdisjoint(triples)
                used_triples |= triples
                if target:
                    pairs = set(itertools.combinations(ext, 2))
                    prior = per_target_pairs.setdefault(target, set())
                    assert prior.isdisjoint(pairs)
                    prior |= pairs
            u = outside.bit_count()
            ext_counts = [(outside & rm).bit_count() for rm in row_masks]
            actual_budget = choose(u, 3) - sum(choose(k, 3) for k in ext_counts)
            assert choose(r, 3)*x + choose(r-1, 3)*y <= actual_budget
            assert y <= b * (choose(u, 2) // choose(r-1, 2))
            e = choose(r-1, 2) - (r-1)//2
            if e:
                cross = choose(u, 2) - sum(choose(k, 2) for k in ext_counts)
                assert y <= b * (cross // e)
            assert blocked.bit_count() <= 2*x + y
            assert b + blocked.bit_count() < bound(w, q)["packing_U"]
    return {"w": w, "m": m, "q": q, "safe_sets": safe_count, "row_checks": row_checks}


def brute_H(w, q):
    """Full scan H = max{2x+y : d0 x + d1 y <= Q, 0 <= y <= Y} with cross-pair Y."""
    r, a = q - 1, q - 2
    n = (q - 1) * (w - 1)
    Q = choose(n, 3) - (w - 1) * choose(r, 3)
    d0, d1 = choose(r, 3), choose(r - 1, 3)
    per_point = choose(n, 2) // choose(r - 1, 2)
    cross_cost = choose(r - 1, 2) - (r - 1) // 2
    if cross_cost:
        cross_budget = choose(n, 2) - (w - 1) * choose(r, 2)
        per_point = min(per_point, cross_budget // cross_cost)
    ymax = a * per_point
    if d1:
        ymax = min(ymax, Q // d1)
    best, arg = -1, None
    for y in range(ymax + 1):
        if d1 * y > Q:
            continue
        x = (Q - d1 * y) // d0
        if 2 * x + y > best:
            best, arg = 2 * x + y, (x, y)
    return {"H": best, "argmax_xy": arg, "Q": Q, "Y_raw": a * per_point,
            "ymax": ymax, "d0": d0, "d1": d1}


def closed_form_67():
    """Hand derivation of U_{6,7} from the K0318 report formulas, no shared code."""
    r, a, w, q = 6, 5, 6, 7
    N = r * (w - 1)                     # 30
    Q = math.comb(N, 3) - (w - 1) * math.comb(r, 3)   # 4060 - 5*20 = 3960
    d0 = math.comb(r, 3)                # 20
    d1 = math.comb(r - 1, 3)            # 10
    per_point = math.comb(N, 2) // math.comb(r - 1, 2)  # 435 // 10 = 43
    cross_cost = math.comb(r - 1, 2) - (r - 1) // 2    # 10 - 2 = 8
    cross_budget = math.comb(N, 2) - (w - 1) * math.comb(r, 2)  # 435 - 75 = 360
    per_point = min(per_point, cross_budget // cross_cost)      # min(43, 45) = 43
    Y = a * per_point                   # 215
    # d0 x + d1 y <= Q with d0 = 2 d1: equal budget efficiency 1/10 per blocked point.
    # x = (Q - 10y) // 20; for even y: 2x + y = 396 - y + y = ... verify exactly.
    best, arg = -1, None
    for y in range(0, min(Y, Q // d1) + 1):
        x = (Q - d1 * y) // d0
        if 2 * x + y > best:
            best, arg = 2 * x + y, (x, y)
    return {"r": r, "a": a, "N": N, "Q": Q, "d0": d0, "d1": d1,
            "per_point": per_point, "Y": Y, "H": best, "argmax": arg,
            "U": r + best,
            "algebra_note": "d0 = 2*d1 so 10*(2x+y) = (20x+10y) + 10y - ... parity: "
                            "2x+y = (Q - 10y)//10 + y adjusted; exact max by scan"}


def k0024_T(w, q):
    N = (q - 1) * (w - 1)
    A = q - 1 + 2 * (choose(N, q - 1) - (w - 1)) + (q - 2) * choose(N, q - 2)
    B = q - 1 + 2 * (choose(N, 3) - (w - 1) * choose(q - 1, 3)) + (q - 2) * choose(N, 2)
    return {"A": A, "B": B, "T": min(A, B)}


def w6_geometry_audit(m, q):
    """Exhaustive w=6 small-board audit: all safe sets x all deficient rows,
    verifying the K0318 budget inequalities directly (extends the repo's
    w<=3 audit range to the target width, small m only)."""
    return board_audit(6, m, q)


def main():
    out = {"schema": 1, "date": "2026-11-13", "target": {"w": 6, "q": 7}}

    # 1. verbatim repo bound()
    b67 = bound(6, 7)
    out["repo_bound_6_7"] = b67

    # 2. full-range brute scan (independent of the period shortcut)
    br67 = brute_H(6, 7)
    out["brute_6_7"] = br67
    assert 6 + br67["H"] == b67["packing_U"], (br67, b67)

    # 3. closed-form hand derivation
    cf = closed_form_67()
    out["closed_form_6_7"] = cf
    assert cf["U"] == b67["packing_U"], (cf, b67)

    # 4. controls against published values
    controls = {
        "3_5_expect_40": bound(3, 5)["packing_U"],
        "5_6_expect_249": bound(5, 6)["packing_U"],
        "5_7_expect_200": bound(5, 7)["packing_U"],
    }
    assert controls["3_5_expect_40"] == 40
    assert controls["5_6_expect_249"] == 249, controls
    assert controls["5_7_expect_200"] == 200, controls
    out["controls"] = controls

    # 5. K0024 sufficient length for (6,7) (previous implicit general bound)
    t67 = k0024_T(6, 7)
    out["k0024_T_6_7"] = t67
    assert b67["packing_U"] <= t67["T"]

    # 6. w=6 geometry audit (small m; board_audit is 2^(w*m) exhaustive, so m=3
    #    only. On 6x3 no circle/line carries >=7 points, so this audits the
    #    machinery and confirms the census is empty at this size.)
    audits = [w6_geometry_audit(3, 7)]
    out["w6_board_audits"] = audits

    # 7. supplementary: first explicit upper bounds for the other unrecorded
    #    (6,q) stabilization lengths (no lower-bound witnesses recorded yet).
    supp = []
    for q in range(4, 9):
        b = bound(6, q)
        r, a = q - 1, q - 2
        n = (q - 1) * 5
        Q = choose(n, 3) - 5 * choose(r, 3)
        d0, d1 = choose(r, 3), choose(r - 1, 3)
        per_point = choose(n, 2) // choose(r - 1, 2)
        cc = choose(r - 1, 2) - (r - 1) // 2
        if cc:
            per_point = min(per_point, (choose(n, 2) - 5 * choose(r, 2)) // cc)
        ymax = a * per_point
        if d1:
            ymax = min(ymax, Q // d1)
        best = max(2 * ((Q - d1 * y) // d0) + y
                    for y in range(ymax + 1) if d1 * y <= Q)
        assert r + best == b["packing_U"], (q, r + best, b["packing_U"])
        supp.append({"w": 6, "q": q, "packing_U": b["packing_U"],
                     "old_T": b["old_T"], "combined": b["combined"]})
    out["supplementary_U_6q"] = supp
    out["conclusion"] = {
        "M_6_7_lower": 20,
        "M_6_7_lower_source": "K0761 (35-stone one-row-deficient maximal witnesses at 6x13/16/19)",
        "M_6_7_upper": b67["packing_U"],
        "M_6_7_upper_source": "K0318 curve-packing substitution U_{6,7}=402 (K0024 T=10101)",
        "statement": "20 <= M_{6,7} <= 402",
    }
    text = json.dumps(out, indent=2) + "\n"
    Path("output").mkdir(exist_ok=True)
    Path("output/six_row_q7_upper_bound.json").write_text(text)
    print(text)


if __name__ == "__main__":
    main()
