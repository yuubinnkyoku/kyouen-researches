#!/usr/bin/env python3
"""Independent verifier for the z=12, y=2 two-token residual-game slice.

The universal proof is x-induction with the complete A/B/C signature bands
below. Finite audits check the transcription, mex table, anchors, and boundary
reductions; they are not the source of the universal quantifier.
"""
from __future__ import annotations

import json
import random
import sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


@lru_cache(None)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)


@lru_cache(None)
def H_canonical(R, X, z):
    X = tuple(sorted(X))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:]))
            opts.add(H_canonical(R - 1, child, z))
        else:
            opts.add(H_canonical(R - 1, X[:i] + X[i + 1:], z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)


def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
    """K0832 single-token closed form."""
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))


# Published child K1016: z=12, y=1.
def z12_y1_T(x, r):
    if x == 1:
        return r == 1
    if x <= 10:
        top = x + 1 if x % 2 == 0 else x
        return 1 <= r <= top and r % 2 == 1
    if x == 11:
        return 1 <= r <= 13 and r % 2 == 1
    if x in (12, 13):
        return 1 <= r <= 11 and r % 2 == 1
    if x == 14:
        return (1 <= r <= 11 or 15 <= r <= 27) and r % 2 == 1
    return r in (1, 3, 5, 7, 9, 11, 15)


def z12_y1_P(x, r):
    if x % 2 == 1:
        if x <= 11:
            return False
        if x == 13:
            return r == 13
        return r == 13 or (r % 2 == 0 and 16 <= r <= x + 13)
    if x <= 10:
        return r >= x + 2
    if x == 12:
        return r >= 13
    return (r == 13 or (r % 2 == 0 and 16 <= r <= x + 12)
            or r >= x + 14)


def z12_y1(x, r):
    if r == 0:
        return 0
    if z12_y1_T(x, r):
        return 2
    return 1 if z12_y1_P(x, r) else 0


# Published child K1013: z=11, y=2.
def z11_y2_T(x, r):
    if x == 2:
        return r in (1, 3)
    if x in (3, 4):
        return r in (1, 3, 5)
    if x in (5, 6):
        return r in (1, 3, 5, 7)
    if x in (7, 8):
        return r in (1, 3, 5, 7, 9)
    if x == 9:
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x in (10, 11, 12):
        return r in (1, 3, 5, 7, 9, 11)
    if x == 13:
        return r in (1, 3, 5, 7, 9, 11, 15)
    if x == 14:
        return r in (1, 3, 5, 7, 9, 11) or (15 <= r <= 27 and r % 2 == 1)
    return r in (1, 3, 5, 7, 9, 11, 15)


def z11_y2_P(x, r):
    if x in (2, 4, 6, 8):
        return False
    if x == 3:
        return r >= 6
    if x == 5:
        return r >= 8
    if x == 7:
        return r >= 10
    if x in (9, 11):
        return r in (12, 14) or r >= 15
    if x == 10:
        return r == 12
    if x == 12:
        return r in (12, 14)
    if x == 13:
        return r in (12, 14) or r >= 16
    if x == 14:
        return r in (12, 14)
    if x >= 16 and x % 2 == 0:
        return r in (12, 14) or (r % 2 == 1 and 17 <= r <= x + 13)
    return (r in (12, 14) or (r % 2 == 1 and 17 <= r <= x + 12)
            or r >= x + 14)


def z11_y2(x, r):
    if r == 0:
        return 0
    if z11_y2_T(x, r):
        return 2
    return 1 if z11_y2_P(x, r) else 0


# Candidate theorem: z=12, y=2.
def candidate_T(x, r):
    if x == 2:
        return r in (1, 3)
    if x in (3, 4):
        return r in (1, 3, 5)
    if x in (5, 6):
        return r in (1, 3, 5, 7)
    if x in (7, 8):
        return r in (1, 3, 5, 7, 9)
    if x == 9:
        return r in (1, 3, 5, 7, 9, 11)
    if x == 10:
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x in (11, 13, 14):
        return r in (1, 3, 5, 7, 9, 11)
    if x == 12:
        return r in (1, 3, 5, 7, 9, 11, 15)
    if x == 15:
        return (r in (1, 3, 5, 7, 9, 11)
                or (17 <= r <= 29 and r % 2 == 1))
    return r in (1, 3, 5, 7, 9, 11, 17)


def candidate_P(x, r):
    if x % 2 == 0 and x <= 10:
        return False
    if x in (3, 5, 7, 9):
        return r >= x + 3
    if x == 11:
        return r == 13 or r >= 15
    if x == 12:
        return r == 13
    if x == 13:
        return r == 13 or r >= 15
    if x == 14:
        return r in (13, 15)
    if x >= 15 and x % 2 == 1:
        return (r in (13, 15) or (r % 2 == 0 and 18 <= r <= x + 13)
                or r >= x + 15)
    if x >= 16 and x % 2 == 0:
        return r in (13, 15) or (r % 2 == 0 and 18 <= r <= x + 14)
    raise ValueError(x)


def candidate(x, R):
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0


# (parity, lower, upper, A/B/C signature); each table covers 1..x+14.
def bands_for(x):
    table = {
        2: [(1, 1, 3, "01"), (0, 2, 4, "23"),
            (1, 5, 15, "1"), (0, 6, 16, "1")],
        3: [(1, 1, 5, "01"), (0, 2, 4, "23"), (0, 6, 6, "03"),
            (1, 7, 17, "0"), (0, 8, 16, "0")],
        4: [(1, 1, 5, "01"), (0, 2, 6, "23"),
            (1, 7, 17, "1"), (0, 8, 18, "1")],
        5: [(1, 1, 7, "01"), (0, 2, 6, "23"), (0, 8, 8, "03"),
            (1, 9, 19, "0"), (0, 10, 18, "0")],
        6: [(1, 1, 7, "01"), (0, 2, 8, "23"),
            (1, 9, 19, "1"), (0, 10, 20, "1")],
        7: [(1, 1, 9, "01"), (0, 2, 8, "23"), (0, 10, 10, "03"),
            (1, 11, 21, "0"), (0, 12, 20, "0")],
        8: [(1, 1, 9, "01"), (0, 2, 10, "23"),
            (1, 11, 21, "1"), (0, 12, 22, "1")],
        9: [(1, 1, 11, "01"), (0, 2, 10, "23"), (0, 12, 14, "03"),
            (1, 13, 23, "0"), (0, 16, 22, "0")],
        10: [(1, 1, 13, "01"), (0, 2, 12, "23"),
             (0, 14, 24, "1"), (1, 15, 23, "1")],
        11: [(1, 1, 11, "01"), (0, 2, 12, "23"), (1, 13, 25, "0"),
             (0, 14, 14, "12"), (0, 16, 24, "0")],
        12: [(1, 1, 11, "01"), (0, 2, 12, "23"), (1, 13, 13, "0"),
             (0, 14, 26, "1"), (1, 15, 15, "01"), (1, 17, 25, "1")],
        13: [(1, 1, 11, "01"), (0, 2, 12, "23"), (1, 13, 27, "0"),
             (0, 14, 14, "1"), (0, 16, 16, "023"), (0, 18, 26, "0")],
        14: [(1, 1, 11, "01"), (0, 2, 12, "23"), (1, 13, 15, "0"),
             (0, 14, 14, "1"), (0, 16, 28, "123"), (1, 17, 27, "1")],
        15: [(1, 1, 11, "01"), (0, 2, 12, "23"), (1, 13, 15, "0"),
             (0, 14, 14, "1"), (0, 16, 16, "123"), (1, 17, 29, "01"),
             (0, 18, 28, "0")],
        16: [(1, 1, 11, "01"), (0, 2, 12, "23"), (1, 13, 15, "0"),
             (0, 14, 14, "1"), (0, 16, 16, "123"), (1, 17, 17, "01"),
             (0, 18, 30, "02"), (1, 19, 29, "1")],
    }
    if x in table:
        return table[x]
    if x >= 17 and x % 2 == 1:
        return [(1, 1, 11, "01"), (0, 2, 12, "23"), (1, 13, 15, "0"),
                (0, 14, 14, "1"), (0, 16, 16, "123"), (1, 17, 17, "01"),
                (0, 18, 18, "02"), (1, 19, x + 14, "1"),
                (0, 20, x + 13, "0")]
    if x >= 18 and x % 2 == 0:
        return [(1, 1, 11, "01"), (0, 2, 12, "23"), (1, 13, 15, "0"),
                (0, 14, 14, "1"), (0, 16, 16, "123"), (1, 17, 17, "01"),
                (0, 18, 18, "02"), (1, 19, x + 13, "1"),
                (0, 20, x + 14, "0")]
    raise ValueError(x)


def abc_options(x, R):
    r = R - 1
    opts = set()
    if x == 2:
        # The two token-decrement moves coincide in (2,1);12.
        opts.add(z12_y1(2, r))
    else:
        opts.add(candidate(x - 1, r))
        opts.add(z12_y1(x, r))
    opts.add(1 ^ z11_y2(x, r))
    return opts


def run_audit():
    failures = []
    counts = {}

    # Two independent direct mex recurrences vs the closed form.
    direct = 0
    for x in range(2, 81):
        for R in range(0, x + 41):
            expected = candidate(x, R)
            a = H_ordered(R, (x, 2), 12)
            b = H_canonical(R, (x, 2), 12)
            direct += 2
            if a != expected or b != expected or a != b:
                failures.append(("direct", x, R, a, b, expected))
    counts["ordered_and_canonical_direct_vs_formula"] = direct

    # Published B/C child anchors, checked by both direct engines.
    anchors = 0
    for x in range(2, 81):
        for R in range(0, x + 41):
            for engine in (H_ordered, H_canonical):
                b = engine(R, (x, 1), 12)
                c = engine(R, (x, 2), 11)
                anchors += 2
                if b != z12_y1(x, R):
                    failures.append(("B-anchor", x, R, b, z12_y1(x, R)))
                if c != z11_y2(x, R):
                    failures.append(("C-anchor", x, R, c, z11_y2(x, R)))
    counts["B_C_child_anchor_direct_checks"] = anchors

    # Complete A/B/C signature-band table, exact coverage, signatures, mex,
    # and Theorem T parity bounds.
    signature_checks = 0
    for x in range(2, 3001):
        bands = bands_for(x)
        for R in range(1, x + 15):
            hits = [sig for parity, lo, hi, sig in bands
                    if R % 2 == parity and lo <= R <= hi]
            if len(hits) != 1:
                failures.append(("band-coverage", x, R, hits))
                continue
            actual = "".join(str(v) for v in sorted(abc_options(x, R)))
            if actual != hits[0]:
                failures.append(("band-signature", x, R, hits[0], actual))
                continue
            value = mex({int(ch) for ch in hits[0]})
            expected = candidate(x, R)
            if value != expected:
                failures.append(("band-mex", x, R, hits[0], value, expected))
            values = {int(ch) for ch in hits[0]}
            if R % 2:
                if not values.issubset({0, 1}) or value > 2:
                    failures.append(("Theorem-T-odd", x, R, hits[0], value))
            elif value > 1:
                failures.append(("Theorem-T-even", x, R, hits[0], value))
            signature_checks += 1
    counts["A_B_C_signature_coverage_identity_mex_and_Theorem_T"] = signature_checks

    # K0832 height-only reduction for R <= z+1 = 13.
    low = 0
    for x in range(2, 1001):
        for R in range(0, 14):
            low += 1
            if candidate(x, R) != single_token(x + 2, 12, R):
                failures.append(("height-only", x, R, candidate(x, R),
                                 single_token(x + 2, 12, R)))
    counts["height_only_reduction_R_le_13"] = low

    # General high-R tail: S=x+2, z=12, threshold S+z+1=x+15.
    tail = 0
    for x in range(2, 10001):
        for offset in range(4):
            R = x + 15 + offset
            tail += 1
            expected = (x + 2) % 2
            if candidate(x, R) != expected:
                failures.append(("tail", x, R, candidate(x, R), expected))
    counts["general_tail"] = tail

    # Theorem T on a wider formula grid.
    theorem_grid = 0
    for x in range(2, 3001):
        for R in range(0, x + 25):
            theorem_grid += 1
            value = candidate(x, R)
            if value not in (0, 1, 2):
                failures.append(("range", x, R, value))
            if R % 2 == 0 and value > 1:
                failures.append(("Theorem-T-even-grid", x, R, value))
            if value == 2 and R % 2 == 0:
                failures.append(("even-value-two", x, R))
    counts["Theorem_T_formula_grid"] = theorem_grid

    # Fixed-seed independent A/B/C mex scatter.
    rng = random.Random(20261119)
    scatter = 0
    for _ in range(25000):
        x = rng.randint(2, 3000)
        R = rng.randint(0, x + 100)
        scatter += 1
        actual = 0 if R == 0 else mex(abc_options(x, R))
        expected = candidate(x, R)
        if actual != expected:
            failures.append(("scatter", x, R, actual, expected))
    counts["fixed_seed_ABC_scatter"] = scatter

    return {
        "all_pass": not failures,
        "classification": "universal proof by x-induction and complete A/B/C signature bands",
        "counts": counts,
        "failure_count": len(failures),
        "finite_audit_role": (
            "independent ordered/canonical recursion, child anchors, band coverage/signature/mex, "
            "low-R reduction, tail, parity, and fixed-seed scatter checks only"
        ),
        "first_failures": failures[:20],
        "scope": {
            "anchor_R": "0 <= R <= x+40",
            "anchor_x": [2, 80],
            "direct_R": "0 <= R <= x+40",
            "direct_x": [2, 80],
            "low_R": "0 <= R <= 13",
            "low_x": [2, 1000],
            "scatter_points": 25000,
            "scatter_seed": 20261119,
            "signature_R": "1 <= R <= x+14",
            "signature_x": [2, 3000],
            "tail_R": "x+15 <= R <= x+18",
            "tail_x": [2, 10000],
            "theorem_grid_R": "0 <= R <= x+24",
            "theorem_grid_x": [2, 3000],
        },
        "target": "H(R;(x,2);12), x>=2, R>=0",
        "total_checks": sum(counts.values()),
    }


def main():
    audit = run_audit()
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    (out / "audit.json").write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if audit["all_pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
