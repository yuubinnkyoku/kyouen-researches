#!/usr/bin/env python3
"""Independent audit for the z=12, y=3 two-token residual-game slice (K1021).

Backfill provenance: the K1021 publication landed its report, item and CI
audit step, but never landed verify_z12_y3.py and output/audit.json, so
the CI step failed on a missing file. This verifier was reconstructed
from the published report tables (T/P closed forms, complete A/B/C
signature bands, tail and height-only reductions, all re-derived here
from the published universal claim) and the published child theorems.
No theorem is changed: it restores the missing finite-audit artifact of
the already-proven slice.

Theorem (published, K1021 census/induction-derived):
  * value-2 positions T(x):  x=3: O[1,5]; x in (4,5): O[1,7];
    x in (6,7): O[1,9]; x=8: O[1,11];
    x=9 (h=z row, x+y=z): O[1,15] (isolated top 15 = 2y+(d+z)/2 with
    d=x-y=6, d+z=18 == 2 mod 4);
    x in (10,11,12): O[1,11]; x=13: O[1,11] u {17} (advance lattice
    point 17 = 2y+(d+z)/2, d=10=x-y, d+z=22 == 2 mod 4);
    x in (14,15): O[1,11];
    x=16 (sweep row x=z+y+1): O[1,11] u O[19,31] = O[1,z-1] u O[pin,x+y+z]
    with pin=19=2y+z+1;
    x>=17: O[1,11] u {19}.
  * value-1 positions P(x): x odd <=9: empty; x in (4,6,8): I[x+4,inf);
    x=10: {13,15} u I[16,inf); x in (11,13): {13,15};
    x in (12,14): {13,15} u I[17,inf); x=15: {13,15,17};
    x=16: {13,15,17} u E[20,32] u I[33,inf);
    x odd >=17: {13,15,17} u E[20,x+15];
    x even >=18: {13,15,17} u E[20,x+16] u I[x+17,inf).
    Base points {13,15,17} = {z+1,z+3,z+5}, band start 20 = z+2y+2.
  * tail: R >= x+16 => H = (x+3) mod 2. Height-only: R <= 13 =>
    H = single_token(x+3, 12, R).
Children: A = H(R-1;(x-1,3);12) (x-outer induction, same-slice row x-1),
B = H(R-1;(x,2);12) = K1019 published universal slice,
C = 1 xor H(R-1;(x,3);11) = 1 xor K1014 published universal slice.
At x=3 the two token-decrement moves coincide in the (2,3);12 == (3,2);12
child, the x=3 row of K1019.
The universal argument is x-induction with the complete A/B/C signature
band table below (static rows x=3..17, closed forms for x>=19 odd /
x>=18 even, each row covering all R>=1 disjointly) plus the K0832
general tail (R>=x+16) and height-only (R<=13) reductions. The two direct
mex engines and finite grids audit transcription; they are not a
substitute for the all-x proof.
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


# Published child K1019: z=12, y=2 (verbatim closed form from
# verify_z12_y2.py).
def z12_y2_T(x, r):
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


def z12_y2_P(x, r):
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


def z12_y2(x, R):
    if R == 0:
        return 0
    if z12_y2_T(x, R):
        return 2
    return 1 if z12_y2_P(x, R) else 0


# Published child K1014: z=11, y=3 (verbatim closed form from
# verify_z11_y3.py).
def z11_y3(x, r):
    if x == 3:
        T, p = {1, 3, 5}, False
    elif x == 4:
        T, p = {1, 3, 5, 7}, r >= 8
    elif x == 5:
        T, p = {1, 3, 5, 7}, False
    elif x == 6:
        T, p = {1, 3, 5, 7, 9}, r >= 10
    elif x == 7:
        T, p = {1, 3, 5, 7, 9}, False
    elif x == 8:
        T, p = {1, 3, 5, 7, 9, 11, 13}, r == 12 or r >= 14
    elif x == 9:
        T, p = {1, 3, 5, 7, 9, 11}, r in {12, 14}
    elif x == 10:
        T, p = {1, 3, 5, 7, 9, 11, 15}, r in {12, 14} or r >= 16
    elif x == 11:
        T, p = {1, 3, 5, 7, 9, 11}, r in {12, 14}
    elif x == 12:
        T, p = {1, 3, 5, 7, 9, 11}, r in {12, 14} or r >= 16
    elif x == 13:
        T, p = {1, 3, 5, 7, 9, 11}, r in {12, 14, 16}
    elif x == 14:
        T, p = {1, 3, 5, 7, 9, 11, 17}, r in {12, 14, 16} or r >= 18
    elif x == 15:
        T, p = {1, 3, 5, 7, 9, 11} | set(range(17, 30, 2)), r in {12, 14, 16}
    elif x % 2 == 0:
        T = {1, 3, 5, 7, 9, 11, 17}
        p = (r in {12, 14, 16} or (19 <= r <= x + 13 and r % 2 == 1)
             or r >= x + 15)
    else:
        T = {1, 3, 5, 7, 9, 11, 17}
        p = r in {12, 14, 16} or (19 <= r <= x + 14 and r % 2 == 1)
    return 2 if r in T else 1 if p else 0


# Published candidate theorem: z=12, y=3 (K1021).
def candidate_T(x, r):
    if x == 3:
        return r in (1, 3, 5)
    if x in (4, 5):
        return r in (1, 3, 5, 7)
    if x in (6, 7):
        return r in (1, 3, 5, 7, 9)
    if x == 8:
        return r in (1, 3, 5, 7, 9, 11)
    if x == 9:
        return 1 <= r <= 15 and r % 2 == 1
    if x in (10, 11, 12):
        return r in (1, 3, 5, 7, 9, 11)
    if x == 13:
        return r in (1, 3, 5, 7, 9, 11) or r == 17
    if x in (14, 15):
        return r in (1, 3, 5, 7, 9, 11)
    if x == 16:
        return (r in (1, 3, 5, 7, 9, 11)
                or (19 <= r <= 31 and r % 2 == 1))
    return r in (1, 3, 5, 7, 9, 11, 19)


def candidate_P(x, r):
    if x % 2 == 1 and x <= 9:
        return False
    if x in (4, 6, 8):
        return r >= x + 4
    if x == 10:
        return r in (13, 15) or r >= 16
    if x in (11, 13):
        return r in (13, 15)
    if x in (12, 14):
        return r in (13, 15) or r >= 17
    if x == 15:
        return r in (13, 15, 17)
    if x == 16:
        return (r in (13, 15, 17)
                or (r % 2 == 0 and 20 <= r <= 32)
                or r >= 33)
    if x % 2 == 1:
        return r in (13, 15, 17) or (r % 2 == 0 and 20 <= r <= x + 15)
    return (r in (13, 15, 17)
            or (r % 2 == 0 and 20 <= r <= x + 16)
            or r >= x + 17)


def candidate(x, R):
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0


# Complete A/B/C signature bands: (R parity, lower, upper, signature),
# upper None means infinity. Static rows x=3..17; closed forms for
# x>=19 odd / x>=18 even. Each row covers all R>=1 disjointly.
def bands_for(x):
    table = {
        3: [(1, 1, 5, "01"), (1, 7, None, "1"), (0, 2, 6, "23"), (0, 8, None, "1")],
        4: [(1, 1, 7, "01"), (1, 9, None, "0"), (0, 2, 6, "23"), (0, 8, 8, "03"), (0, 10, None, "0")],
        5: [(1, 1, 7, "01"), (1, 9, None, "1"), (0, 2, 8, "23"), (0, 10, None, "1")],
        6: [(1, 1, 9, "01"), (1, 11, None, "0"), (0, 2, 8, "23"), (0, 10, 10, "03"), (0, 12, None, "0")],
        7: [(1, 1, 9, "01"), (1, 11, None, "1"), (0, 2, 10, "23"), (0, 12, None, "1")],
        8: [(1, 1, 11, "01"), (1, 13, None, "0"), (0, 2, 10, "23"), (0, 12, 14, "03"), (0, 16, None, "0")],
        9: [(1, 1, 15, "01"), (1, 17, None, "1"), (0, 2, 12, "23"), (0, 14, None, "1")],
        10: [(1, 1, 11, "01"), (1, 13, None, "0"), (0, 2, 12, "23"), (0, 14, 14, "12"), (0, 16, 16, "023"), (0, 18, None, "0")],
        11: [(1, 1, 11, "01"), (1, 13, 15, "0"), (1, 17, None, "1"), (0, 2, 12, "23"), (0, 14, None, "1")],
        12: [(1, 1, 11, "01"), (1, 13, None, "0"), (0, 2, 12, "23"), (0, 14, 14, "1"), (0, 16, 16, "12"), (0, 18, None, "0")],
        13: [(1, 1, 11, "01"), (1, 13, 15, "0"), (1, 17, 17, "01"), (1, 19, None, "1"), (0, 2, 12, "23"), (0, 14, None, "1")],
        14: [(1, 1, 11, "01"), (1, 13, None, "0"), (0, 2, 12, "23"), (0, 14, 16, "1"), (0, 18, 18, "023"), (0, 20, None, "0")],
        15: [(1, 1, 11, "01"), (1, 13, 17, "0"), (1, 19, None, "1"), (0, 2, 12, "23"), (0, 14, 16, "1"), (0, 18, 30, "123"), (0, 32, None, "1")],
        16: [(1, 1, 11, "01"), (1, 13, 17, "0"), (1, 19, 31, "01"), (1, 33, None, "0"), (0, 2, 12, "23"), (0, 14, 16, "1"), (0, 18, 18, "123"), (0, 20, None, "0")],
        # x=17 is a transitional row: its A child is the sweep row x=16,
        # so even R in [20,32] carry the extra child value 2 (sig "02",
        # mex unchanged at 1). The report lists this as E[20,32]:02.
        17: [(1, 1, 11, "01"), (1, 13, 17, "0"), (1, 19, 19, "01"), (1, 21, None, "1"),
             (0, 2, 12, "23"), (0, 14, 16, "1"), (0, 18, 18, "123"), (0, 20, 32, "02"), (0, 34, None, "1")],
    }
    if x in table:
        return table[x]
    if x >= 18 and x % 2 == 0:
        return [(1, 1, 11, "01"), (1, 13, 17, "0"), (1, 19, 19, "01"),
                (1, 21, x + 15, "1"), (1, x + 17, None, "0"),
                (0, 2, 12, "23"), (0, 14, 16, "1"), (0, 18, 18, "123"),
                (0, 20, 20, "02"), (0, 22, None, "0")]
    if x >= 19 and x % 2 == 1:
        return [(1, 1, 11, "01"), (1, 13, 17, "0"), (1, 19, 19, "01"),
                (1, 21, None, "1"),
                (0, 2, 12, "23"), (0, 14, 16, "1"), (0, 18, 18, "123"),
                (0, 20, 20, "02"), (0, 22, x + 15, "0"), (0, x + 17, None, "1")]
    raise ValueError(x)


def band_signatures(x, R):
    return [sig for parity, lo, hi, sig in bands_for(x)
            if R % 2 == parity and lo <= R and (hi is None or R <= hi)]


def abc_options(x, R):
    r = R - 1
    opts = set()
    if x == 3:
        # The two token-decrement moves coincide: (2,3);12 == (3,2);12,
        # the x=3 row of the published K1019 slice.
        opts.add(z12_y2(3, r))
    else:
        opts.add(candidate(x - 1, r))
        opts.add(z12_y2(x, r))
    opts.add(1 ^ z11_y3(x, r))
    return opts


def child_signature(x, R):
    return "".join(str(v) for v in sorted(abc_options(x, R)))


def audit_once():
    failures = []

    counts = {}

    # Two independent direct mex recurrences vs the closed form.
    direct = 0
    for x in range(3, 81):
        for R in range(0, x + 42):
            expected = candidate(x, R)
            a = H_ordered(R, (x, 3), 12)
            b = H_canonical(R, (x, 3), 12)
            direct += 2
            if a != expected or b != expected or a != b:
                failures.append(("direct", x, R, a, b, expected))
    counts["ordered_and_canonical_direct_vs_formula"] = direct

    # Published B/C child anchors, checked by both direct engines.
    anchors = 0
    for x in range(3, 81):
        for R in range(0, x + 42):
            for engine in (H_ordered, H_canonical):
                b = engine(R, (x, 2), 12)
                c = engine(R, (x, 3), 11)
                anchors += 2
                if b != z12_y2(x, R):
                    failures.append(("B-anchor", x, R, b, z12_y2(x, R)))
                if c != z11_y3(x, R):
                    failures.append(("C-anchor", x, R, c, z11_y3(x, R)))
    counts["B_C_child_anchor_direct_checks"] = anchors

    # Complete A/B/C signature-band table: exact band coverage,
    # signature identity, mex, and Theorem T parity bounds.
    # Bands extend to infinity (closed-form rows are complete R tables),
    # so the checked window 1..x+40 straddles the tail boundary.
    signature_checks = parity_checks = 0
    for x in range(3, 3001):
        for R in range(1, x + 41):
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

    # K0832 height-only reduction for R <= z+1 = 13.
    low = 0
    for x in range(3, 1001):
        for R in range(0, 14):
            low += 1
            if candidate(x, R) != single_token(x + 3, 12, R):
                failures.append(("height-only", x, R, candidate(x, R),
                                 single_token(x + 3, 12, R)))
    counts["height_only_reduction_R_le_13"] = low

    # General high-R tail: S=x+3, z=12, threshold S+z+1=x+16.
    tail = 0
    for x in range(3, 10001):
        for offset in range(4):
            R = x + 16 + offset
            tail += 1
            expected = (x + 3) % 2
            if candidate(x, R) != expected:
                failures.append(("tail", x, R, candidate(x, R), expected))
    counts["general_tail"] = tail

    # Theorem T on a wider formula grid.
    theorem_grid = 0
    for x in range(3, 3001):
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
        x = rng.randint(3, 3000)
        R = rng.randint(0, x + 110)
        scatter += 1
        actual = 0 if R == 0 else mex(abc_options(x, R))
        expected = candidate(x, R)
        if actual != expected:
            failures.append(("scatter", x, R, actual, expected))
    counts["fixed_seed_ABC_scatter"] = scatter

    return {
        "all_pass": not failures,
        "theorem": "z=12 y=3 two-token residual Grundy slice (K1021)",
        "classification": "universal proof by x-induction and complete A/B/C signature bands",
        "backfill_note": ("restores the missing verifier/audit artifact of the published "
                          "K1021 slice; reconstructed from the published report tables and "
                          "the published child closed forms K1019/K1014"),
        "finite_audit_role": ("independent ordered/canonical recursion, child anchors, band "
                              "coverage/signature/mex, low-R reduction, tail, parity, and "
                              "fixed-seed scatter checks only"),
        "scope": {
            "target": "H(R;(x,3);12), x>=3, R>=0",
            "anchor_R": "0 <= R <= x+41",
            "anchor_x": [3, 80],
            "direct_R": "0 <= R <= x+41",
            "direct_x": [3, 80],
            "low_R": "0 <= R <= 13",
            "low_x": [3, 1000],
            "scatter_points": 25000,
            "scatter_seed": 20261123,
            "signature_R": "1 <= R <= x+40",
            "signature_x": [3, 3000],
            "tail_R": "x+16 <= R <= x+19",
            "tail_x": [3, 10000],
            "theorem_grid_R": "0 <= R <= x+30",
            "theorem_grid_x": [3, 3000],
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
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
