#!/usr/bin/env python3
"""Independent audit for the z=14, y=4 two-token residual-game slice.

Theorem (census-derived, anchored on published child theorems):
  * value-2 positions T(x): x=4: O[1,7]; x in (5,6): O[1,9]; x in (7,8):
    O[1,11]; x=9: O[1,13]; x=10 (h=z row, x+y<z with d-grid top):
    O[1,17] (top 17 = q_odd(2y+(d+z)/2) with d=x-y=6, d+z=20 == 0 mod 4,
    the even-z q_odd-type isolated h=z-row top);
    x in (11,13,14,15,17,18): O[1,13]; x=12: O[1,13] u {19} (d-grid point
    2y+(d+z)/2 = 19, d=8, d+z=22 == 2 mod 4); x=16: O[1,13] u {21}
    (d-grid point 21, d=12, d+z=26 == 2 mod 4);
    x=19 (sweep row x=z+y+1): O[1,13] u O[23,37] = O[1,z-1] u O[pin,x+y+z]
    with pin=23=z+2y+1; x>=20: O[1,13] u {23} (even-z ladder O[1,z-1] u
    pin=z+2y+1=23).
  * value-1 positions P(x): x even <=10: empty; x odd in (5,7,9):
    I[x+5,inf); x in (11,13): {15,17} u I[19,inf); x=12: {15,17};
    x=14: {15,17,19}; x in (15,17): {15,17,19} u I[21,inf); x=16:
    {15,17,19}; x=18: {15,17,19,21}; x odd >=19: {15,17,19,21} u
    E[24,x+17] u I[x+19,inf); x even >=20: {15,17,19,21} u E[24,x+18]
    (finite: even rows carry no infinite band because the tail is 0).
    Value-1 base points {15,17,19,21} = {z+1,z+3,z+5,z+7} (y-point
    hypothesis 4-point instance, first for even z); band start z+2y+2=24
    (even band following the parity of z).
  * tail: R >= x+19 => H = (x+4) mod 2. Height-only: R <= 15 =>
    H = single_token(x+4, 14, R).
Children: A = H(R-1;(x-1,4);14) (x-outer induction, same-slice row x-1),
B = H(R-1;(x,3);14) = K1030 published universal slice,
C = 1 xor H(R-1;(x,4);13) = 1 xor K1027 published universal slice.
At x=4 the two token-decrement moves coincide in the (3,4);14 == (4,3);14
multiset child (K1030 row x'=4 induction base).
The universal argument is x-induction with the complete A/B/C signature
band table below (static rows x=4..20, closed forms for x>=21 odd and
x>=22 even covering R=1..x+18), plus the K0832 general tail (R>=x+19) and
height-only (R <= z+1 = 15) reductions. The two direct mex engines and
finite grids audit transcription; they are not a substitute for the
all-x proof.
"""
from __future__ import annotations

import hashlib
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
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)


def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
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


# K1030, z=14, y=3 (published universal slice; verbatim transcription).
def z14_y3_T(x, r):
    if x == 3:
        return r in (1, 3, 5)
    if x in (4, 5):
        return r in (1, 3, 5, 7)
    if x in (6, 7):
        return r in (1, 3, 5, 7, 9)
    if x in (8, 9):
        return r in (1, 3, 5, 7, 9, 11)
    if x == 10:
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x == 11:
        return r in (1, 3, 5, 7, 9, 11, 13, 15, 17)
    if x in (12, 13, 14, 16, 17):
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x == 15:
        return r in (1, 3, 5, 7, 9, 11, 13) or r == 19
    if x == 18:
        return (r in (1, 3, 5, 7, 9, 11, 13)
                or (21 <= r <= 35 and r % 2 == 1))
    return r in (1, 3, 5, 7, 9, 11, 13) or r == 21


def z14_y3_P(x, r):
    if x % 2 == 1 and x <= 11:
        return False
    if x % 2 == 0 and x <= 10:
        return r >= x + 4
    if x == 12:
        return r == 15 or r >= 17
    if x in (13, 15):
        return r in (15, 17)
    if x in (14, 16):
        return r in (15, 17) or r >= 19
    if x == 17:
        return r in (15, 17, 19)
    if x == 18:
        return (r in (15, 17, 19)
                or (r % 2 == 0 and 22 <= r <= 34)
                or r >= 36)
    if x % 2 == 1:
        return (r in (15, 17, 19)
                or (r % 2 == 0 and 22 <= r <= x + 17))
    return (r in (15, 17, 19)
            or (r % 2 == 0 and 22 <= r <= x + 18)
            or r >= x + 19)


def z14_y3(x, R):
    if R == 0:
        return 0
    if z14_y3_T(x, R):
        return 2
    return 1 if z14_y3_P(x, R) else 0


# K1027, z=13, y=4 (published universal slice; verbatim transcription).
def z13_y4_T(x, r):
    if x == 4:
        return 1 <= r <= 7 and r % 2 == 1
    if x in (5, 6):
        return 1 <= r <= 9 and r % 2 == 1
    if x in (7, 8):
        return 1 <= r <= 11 and r % 2 == 1
    if x == 9:
        return 1 <= r <= 17 and r % 2 == 1
    if x in (10, 11, 12, 14, 15, 16):
        return 1 <= r <= 13 and r % 2 == 1
    if x == 13:
        return (1 <= r <= 13 and r % 2 == 1) or r == 19
    if x == 17:
        return (1 <= r <= 13 and r % 2 == 1) or r == 21
    if x == 18:
        return ((1 <= r <= 13 and r % 2 == 1)
                or (21 <= r <= 35 and r % 2 == 1))
    return (1 <= r <= 13 and r % 2 == 1) or r == 21


def z13_y4_P(x, r):
    if x in (4, 6, 8):
        return False
    if x == 5:
        return r >= 10
    if x == 7:
        return r >= 12
    if x in (9, 11):
        return r in (14, 16, 18) or r >= 19
    if x == 10:
        return r in (14, 16)
    if x in (12, 14):
        return r in (14, 16, 18)
    if x in (13, 15):
        return r in (14, 16, 18, 20) or r >= 21
    if x in (16, 18):
        return r in (14, 16, 18, 20)
    if x == 17:
        return r in (14, 16, 18, 20) or r >= 22
    if x % 2 == 1:
        return (r in (14, 16, 18, 20)
                or (r % 2 == 1 and 23 <= r <= x + 16)
                or r >= x + 18)
    return (r in (14, 16, 18, 20)
            or (r % 2 == 1 and 23 <= r <= x + 17))


def z13_y4(x, R):
    if R == 0:
        return 0
    if z13_y4_T(x, R):
        return 2
    return 1 if z13_y4_P(x, R) else 0


# Candidate theorem: z=14, y=4 (this slice).
def candidate_T(x, r):
    if x == 4:
        return r in (1, 3, 5, 7)
    if x in (5, 6):
        return 1 <= r <= 9 and r % 2 == 1
    if x in (7, 8):
        return 1 <= r <= 11 and r % 2 == 1
    if x == 9:
        return 1 <= r <= 13 and r % 2 == 1
    if x == 10:
        return 1 <= r <= 17 and r % 2 == 1
    if x in (11, 13, 14, 15, 17, 18):
        return 1 <= r <= 13 and r % 2 == 1
    if x == 12:
        return (1 <= r <= 13 and r % 2 == 1) or r == 19
    if x == 16:
        return (1 <= r <= 13 and r % 2 == 1) or r == 21
    if x == 19:
        return ((1 <= r <= 13 and r % 2 == 1)
                or (23 <= r <= 37 and r % 2 == 1))
    return (1 <= r <= 13 and r % 2 == 1) or r == 23


def candidate_P(x, r):
    if x % 2 == 0 and x <= 10:
        return False
    if x % 2 == 1 and x <= 9:
        return r >= x + 5
    if x in (11, 13):
        return r in (15, 17) or r >= 19
    if x == 12:
        return r in (15, 17)
    if x == 14:
        return r in (15, 17, 19)
    if x in (15, 17):
        return r in (15, 17, 19) or r >= 21
    if x == 16:
        return r in (15, 17, 19)
    if x == 18:
        return r in (15, 17, 19, 21)
    if x % 2 == 1:
        return (r in (15, 17, 19, 21)
                or (r % 2 == 0 and 24 <= r <= x + 17)
                or r >= x + 19)
    return (r in (15, 17, 19, 21)
            or (r % 2 == 0 and 24 <= r <= x + 18))


def candidate(x, R):
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0


# Complete A/B/C signature bands: (R parity, lower, upper, signature).
# Static rows x=4..20; closed forms for odd x>=21 and even x>=22. Each row
# covers R=1..x+18 (= tail-1, S=x+4, general tail starts x+19) disjointly.
def bands_for(x):
    table = {
        4: [(1, 1, 7, "01"), (1, 9, 21, "1"), (0, 2, 8, "23"), (0, 10, 22, "1")],
        5: [(1, 1, 9, "01"), (1, 11, 23, "0"), (0, 2, 8, "23"), (0, 10, 10, "03"), (0, 12, 22, "0")],
        6: [(1, 1, 9, "01"), (1, 11, 23, "1"), (0, 2, 10, "23"), (0, 12, 24, "1")],
        7: [(1, 1, 11, "01"), (1, 13, 25, "0"), (0, 2, 10, "23"), (0, 12, 12, "03"), (0, 14, 24, "0")],
        8: [(1, 1, 11, "01"), (1, 13, 25, "1"), (0, 2, 12, "23"), (0, 14, 26, "1")],
        9: [(1, 1, 13, "01"), (1, 15, 27, "0"), (0, 2, 12, "23"), (0, 14, 18, "03"), (0, 20, 26, "0")],
        10: [(1, 1, 17, "01"), (1, 19, 27, "1"), (0, 2, 14, "23"), (0, 16, 28, "1")],
        11: [(1, 1, 13, "01"), (1, 15, 29, "0"), (0, 2, 14, "23"), (0, 16, 18, "12"), (0, 20, 28, "0")],
        12: [(1, 1, 13, "01"), (1, 15, 17, "0"), (1, 19, 19, "01"), (1, 21, 29, "1"), (0, 2, 14, "23"), (0, 16, 30, "1")],
        13: [(1, 1, 13, "01"), (1, 15, 31, "0"), (0, 2, 14, "23"), (0, 16, 18, "1"), (0, 20, 20, "023"), (0, 22, 30, "0")],
        14: [(1, 1, 13, "01"), (1, 15, 19, "0"), (1, 21, 31, "1"), (0, 2, 14, "23"), (0, 16, 32, "1")],
        15: [(1, 1, 13, "01"), (1, 15, 33, "0"), (0, 2, 14, "23"), (0, 16, 18, "1"), (0, 20, 20, "12"), (0, 22, 32, "0")],
        16: [(1, 1, 13, "01"), (1, 15, 19, "0"), (1, 21, 21, "01"), (1, 23, 33, "1"), (0, 2, 14, "23"), (0, 16, 34, "1")],
        17: [(1, 1, 13, "01"), (1, 15, 35, "0"), (0, 2, 14, "23"), (0, 16, 20, "1"), (0, 22, 22, "023"), (0, 24, 34, "0")],
        18: [(1, 1, 13, "01"), (1, 15, 21, "0"), (1, 23, 35, "1"), (0, 2, 14, "23"), (0, 16, 20, "1"), (0, 22, 36, "123")],
        19: [(1, 1, 13, "01"), (1, 15, 21, "0"), (1, 23, 37, "01"), (0, 2, 14, "23"), (0, 16, 20, "1"), (0, 22, 22, "123"), (0, 24, 36, "0")],
        20: [(1, 1, 13, "01"), (1, 15, 21, "0"), (1, 23, 23, "01"), (1, 25, 37, "1"), (0, 2, 14, "23"), (0, 16, 20, "1"), (0, 22, 22, "123"), (0, 24, 38, "02")],
    }
    if x in table:
        return table[x]
    if x >= 21 and x % 2 == 1:
        return [(1, 1, 13, "01"), (1, 15, 21, "0"), (1, 23, 23, "01"),
                (1, 25, x + 18, "1"),
                (0, 2, 14, "23"), (0, 16, 20, "1"), (0, 22, 22, "123"),
                (0, 24, 24, "02"), (0, 26, x + 17, "0")]
    if x >= 22 and x % 2 == 0:
        return [(1, 1, 13, "01"), (1, 15, 21, "0"), (1, 23, 23, "01"),
                (1, 25, x + 17, "1"),
                (0, 2, 14, "23"), (0, 16, 20, "1"), (0, 22, 22, "123"),
                (0, 24, 24, "02"), (0, 26, x + 18, "0")]
    raise ValueError(x)


def band_signatures(x, R):
    return [sig for parity, lo, hi, sig in bands_for(x)
            if R % 2 == parity and lo <= R and (hi is None or R <= hi)]


def abc_options(x, R):
    r = R - 1
    opts = set()
    if x == 4:
        # The two token-decrement moves coincide in the (4,3);14 multiset.
        opts.add(z14_y3(4, r))
    else:
        opts.add(candidate(x - 1, r))
        opts.add(z14_y3(x, r))
    opts.add(1 ^ z13_y4(x, r))
    return opts


def child_signature(x, R):
    return "".join(str(v) for v in sorted(abc_options(x, R)))


def audit_once():
    failures = []
    counts = {}

    # Two independent direct mex recurrences vs the closed form.
    direct = 0
    for x in range(4, 81):
        for R in range(0, x + 42):
            expected = candidate(x, R)
            a = H_ordered(R, (x, 4), 14)
            b = H_canonical(R, (x, 4), 14)
            direct += 2
            if a != expected or b != expected or a != b:
                failures.append(("direct", x, R, a, b, expected))
    counts["ordered_and_canonical_direct_vs_formula"] = direct

    # Published B/C child anchors, checked by both direct engines.
    anchors = 0
    for x in range(4, 81):
        for R in range(0, x + 42):
            for engine in (H_ordered, H_canonical):
                b = engine(R, (x, 3), 14)
                c = engine(R, (x, 4), 13)
                anchors += 2
                if b != z14_y3(x, R):
                    failures.append(("B-anchor", x, R, b, z14_y3(x, R)))
                if c != z13_y4(x, R):
                    failures.append(("C-anchor", x, R, c, z13_y4(x, R)))
    counts["B_C_child_anchor_direct_checks"] = anchors

    # Complete A/B/C signature-band table: exact coverage of R=1..x+18,
    # signature identity, mex, and Theorem T parity bounds.
    signature_checks = parity_checks = 0
    for x in range(4, 3001):
        for R in range(1, x + 19):
            hits = band_signatures(x, R)
            if len(hits) != 1:
                failures.append(("band-coverage", x, R, hits))
                continue
            actual = child_signature(x, R)
            if hits[0] != actual:
                failures.append(("band-signature", x, R, hits[0], actual))
                continue
            value = mex({int(ch) for ch in hits[0]})
            expected = candidate(x, R)
            signature_checks += 1
            if value != expected:
                failures.append(("band-mex", x, R, hits[0], value, expected))
            values = {int(ch) for ch in hits[0]}
            if R % 2:
                if not values.issubset({0, 1}) or value > 2:
                    failures.append(("Theorem-T-odd", x, R, hits[0], value))
            elif value > 1:
                failures.append(("Theorem-T-even", x, R, hits[0], value))
            parity_checks += 1
    counts["A_B_C_signature_coverage_identity_mex_and_Theorem_T"] = signature_checks
    counts["Theorem_T_parity_bound"] = parity_checks

    # K0832 height-only reduction for R <= z+1 = 15.
    low = 0
    for x in range(4, 1001):
        for R in range(0, 16):
            low += 1
            if candidate(x, R) != single_token(x + 4, 14, R):
                failures.append(("height-only", x, R, candidate(x, R),
                                 single_token(x + 4, 14, R)))
    counts["height_only_reduction_R_le_15"] = low

    # General high-R tail: S=x+4, z=14, threshold S+|X|+z-1 = x+19.
    tail = 0
    for x in range(4, 10001):
        for offset in range(4):
            R = x + 19 + offset
            tail += 1
            expected = (x + 4) % 2
            if candidate(x, R) != expected:
                failures.append(("tail", x, R, candidate(x, R), expected))
    counts["general_tail"] = tail

    # Theorem T on a wider formula grid.
    theorem_grid = 0
    for x in range(4, 3001):
        for R in range(0, x + 31):
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
    rng = random.Random(20261123)
    scatter = 0
    for _ in range(25000):
        x = rng.randint(4, 3000)
        R = rng.randint(0, x + 110)
        scatter += 1
        actual = 0 if R == 0 else mex(abc_options(x, R))
        expected = candidate(x, R)
        if actual != expected:
            failures.append(("scatter", x, R, actual, expected))
    counts["fixed_seed_ABC_scatter"] = scatter

    return {
        "all_pass": not failures,
        "theorem": "z=14 y=4 two-token residual Grundy slice",
        "classification": "universal proof by x-induction and complete A/B/C signature bands",
        "finite_audit_role": "independent ordered/canonical recursion, child anchors, band coverage/signature/mex, low-R reduction, tail, parity, and fixed-seed scatter checks only",
        "scope": {
            "target": "H(R;(x,4);14), x>=4, R>=0",
            "anchor_R": "0 <= R <= x+41",
            "anchor_x": [4, 80],
            "direct_R": "0 <= R <= x+41",
            "direct_x": [4, 80],
            "low_R": "0 <= R <= 15",
            "low_x": [4, 1000],
            "scatter_points": 25000,
            "scatter_seed": 20261123,
            "signature_R": "1 <= R <= x+18",
            "signature_x": [4, 3000],
            "tail_R": "x+19 <= R <= x+22",
            "tail_x": [4, 10000],
            "theorem_grid_R": "0 <= R <= x+30",
            "theorem_grid_x": [4, 3000],
        },
        "counts": counts,
        "total_checks": sum(counts.values()),
        "failure_count": len(failures),
        "first_failures": failures[:20],
    }


def run():
    first = audit_once()
    second = audit_once()
    first_bytes = json.dumps(first, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")).encode()
    second_bytes = json.dumps(second, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")).encode()
    same = first_bytes == second_bytes
    result = {
        **first,
        "repeat_runs": 2,
        "repeat_byte_identical": same,
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "sha256_without_hash_field": hashlib.sha256(first_bytes).hexdigest(),
    }
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True,
                          indent=2) + "\n"
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "audit.json").write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["all_pass"] and same else 1


if __name__ == "__main__":
    sys.exit(run())
