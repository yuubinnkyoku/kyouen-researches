#!/usr/bin/env python3
"""Independent audit for the z=18, y=3 two-token residual-game theorem.

The universal proof is R-strong induction and the complete symbolic
A/B/C signature partition in report.md.  This verifier independently checks
the transcription with ordered and canonical direct recursions, both child
anchors, every listed signature band, the low-R single-token coincidence,
the general tail, and deterministic deep/random samples.
"""
from functools import lru_cache
import hashlib
import json
import random
from pathlib import Path
import sys

sys.setrecursionlimit(100000)


def mex(values):
    m = 0
    while m in values:
        m += 1
    return m


@lru_cache(None)
def g_ordered(R, xs, z):
    if R == 0:
        return 0
    opts = set()
    for i, a in enumerate(xs):
        if a > 1:
            child = xs[:i] + (a - 1,) + xs[i + 1:]
            zz = z
        else:
            child = xs[:i] + xs[i + 1:]
            zz = z + 1
        opts.add(g_ordered(R - 1, child, zz))
    if z:
        opts.add(1 ^ g_ordered(R - 1, xs, z - 1))
    return mex(opts)


@lru_cache(None)
def g_canon(R, xs, z):
    xs = tuple(sorted(xs, reverse=True))
    if R == 0:
        return 0
    opts = set()
    for i, a in enumerate(xs):
        if a > 1:
            child = xs[:i] + (a - 1,) + xs[i + 1:]
            zz = z
        else:
            child = xs[:i] + xs[i + 1:]
            zz = z + 1
        opts.add(g_canon(R - 1, child, zz))
    if z:
        opts.add(1 ^ g_canon(R - 1, xs, z - 1))
    return mex(opts)


def odd(r, a, b):
    return r % 2 == 1 and a <= r <= b


def even(r, a, b):
    return r % 2 == 0 and a <= r <= b


def k1051(x, r):
    """Published K1051: H(r;(x,2);18)."""
    if r == 0:
        return 0
    if r >= x + 21:
        return (x + 2) % 2
    if x == 2:
        t = r in (1, 3)
        p = False
    elif x <= 14:
        top = 2 * ((x - 1) // 2) + 3
        t = odd(r, 1, top)
        p = x % 2 == 1 and r >= x + 3
    elif x == 15:
        t = odd(r, 1, 17)
        p = r >= 18
    elif x == 16:
        t = odd(r, 1, 19)
        p = False
    elif x in (17, 19):
        t = odd(r, 1, 17)
        p = r in (19, 21) or r >= 22
    elif x == 18:
        t = odd(r, 1, 17) or r == 21
        p = r == 19
    elif x == 20:
        t = odd(r, 1, 17)
        p = r in (19, 21)
    elif x == 21:
        t = odd(r, 1, 17) or odd(r, 23, 41)
        p = r in (19, 21) or even(r, 24, 42)
    else:
        t = odd(r, 1, 17) or r == 23
        upper = x + 21 if x % 2 else x + 20
        p = r in (19, 21) or even(r, 24, upper)
    return 2 if t else 1 if p else 0


def k1067(x, r):
    """Published K1067: H(r;(x,3);17)."""
    if r == 0:
        return 0
    if r >= x + 21:
        return (x + 3) % 2
    if x <= 13:
        top = 2 * (x // 2) + 3
        t = odd(r, 1, top)
        p = x % 2 == 0 and r >= x + 4
    elif x == 14:
        t = odd(r, 1, 19)
        p = r == 18 or r >= 20
    elif x == 15:
        t = odd(r, 1, 17)
        p = r in (18, 20)
    elif x == 16:
        t = odd(r, 1, 17) or r == 21
        p = r in (18, 20) or r >= 22
    elif x == 17:
        t = odd(r, 1, 17)
        p = r in (18, 20)
    elif x == 18:
        t = odd(r, 1, 17)
        p = r in (18, 20) or r >= 22
    elif x == 19:
        t = odd(r, 1, 17)
        p = r in (18, 20, 22)
    elif x == 20:
        t = odd(r, 1, 17) or r == 23
        p = r in (18, 20, 22) or r >= 24
    elif x == 21:
        t = odd(r, 1, 17) or odd(r, 23, 41)
        p = r in (18, 20, 22)
    else:
        t = odd(r, 1, 17) or r == 23
        upper = x + 20 if x % 2 else x + 19
        p = r in (18, 20, 22) or odd(r, 25, upper)
    return 2 if t else 1 if p else 0


def z18_y3_T(x, r):
    if r % 2 == 0:
        return False
    if x <= 14:
        return r <= 2 * (x // 2) + 3
    if x == 15:
        return r <= 21
    if 16 <= x <= 18:
        return r <= 17
    if x == 19:
        return r <= 17 or r == 23
    if x in (20, 21):
        return r <= 17
    if x == 22:
        return r <= 17 or 25 <= r <= 43
    return r <= 17 or r == 25


def z18_y3_P(x, r):
    if x <= 15:
        return x >= 4 and x % 2 == 0 and r >= x + 4
    if x == 16:
        return r in (19, 21) or r >= 22
    if x == 17:
        return r in (19, 21)
    if x in (18, 20):
        return r in (19, 21) or r >= 23
    if x == 19:
        return r in (19, 21)
    if x == 21:
        return r in (19, 21, 23)
    if x == 22:
        return (r in (19, 21, 23) or even(r, 26, 42) or r >= 44)
    upper = x + 20 if x % 2 == 0 else x + 21
    return (r in (19, 21, 23) or even(r, 26, upper)
            or (x % 2 == 0 and r >= x + 22))


def z18_y3(x, r):
    """Closed form for H(r;(x,3);18), x>=3."""
    if r == 0:
        return 0
    if r >= x + 22:
        return (x + 3) % 2
    if z18_y3_T(x, r):
        return 2
    if z18_y3_P(x, r):
        return 1
    return 0


def single18(n, r):
    """K0832 single-token formula v(n,18,r)."""
    if r == 0:
        return 0
    if n < 18:
        m = n if n % 2 else n - 1
        if r % 2 and r <= m:
            return 2
        if r % 2 == 0 and r <= m:
            return 0
        return n % 2
    if n == 18:
        if r % 2 and r <= 35:
            return 2
        if r % 2 == 0 and r <= 17:
            return 0
        return 0
    if r % 2 and r <= 17:
        return 2
    if r % 2 == 0 and r <= 17:
        return 0
    if r < n + 18:
        return (r + 18) % 2
    return n % 2


STATIC_BANDS = {
    3:  ([(1, 5, "01"), (7, 23, "1")],
         [(2, 6, "23"), (8, 24, "1")]),
    4:  ([(1, 7, "01"), (9, 25, "0")],
         [(2, 6, "23"), (8, 8, "03"), (10, 24, "0")]),
    5:  ([(1, 7, "01"), (9, 25, "1")],
         [(2, 8, "23"), (10, 26, "1")]),
    6:  ([(1, 9, "01"), (11, 27, "0")],
         [(2, 8, "23"), (10, 10, "03"), (12, 26, "0")]),
    7:  ([(1, 9, "01"), (11, 27, "1")],
         [(2, 10, "23"), (12, 28, "1")]),
    8:  ([(1, 11, "01"), (13, 29, "0")],
         [(2, 10, "23"), (12, 12, "03"), (14, 28, "0")]),
    9:  ([(1, 11, "01"), (13, 29, "1")],
         [(2, 12, "23"), (14, 30, "1")]),
    10: ([(1, 13, "01"), (15, 31, "0")],
         [(2, 12, "23"), (14, 14, "03"), (16, 30, "0")]),
    11: ([(1, 13, "01"), (15, 31, "1")],
         [(2, 14, "23"), (16, 32, "1")]),
    12: ([(1, 15, "01"), (17, 33, "0")],
         [(2, 14, "23"), (16, 16, "03"), (18, 32, "0")]),
    13: ([(1, 15, "01"), (17, 33, "1")],
         [(2, 16, "23"), (18, 34, "1")]),
    14: ([(1, 17, "01"), (19, 35, "0")],
         [(2, 16, "23"), (18, 20, "03"), (22, 34, "0")]),
    15: ([(1, 21, "01"), (23, 35, "1")],
         [(2, 18, "23"), (20, 36, "1")]),
    16: ([(1, 17, "01"), (19, 37, "0")],
         [(2, 18, "23"), (20, 20, "12"), (22, 22, "023"), (24, 36, "0")]),
    17: ([(1, 17, "01"), (19, 21, "0"), (23, 37, "1")],
         [(2, 18, "23"), (20, 38, "1")]),
    18: ([(1, 17, "01"), (19, 39, "0")],
         [(2, 18, "23"), (20, 20, "1"), (22, 22, "12"), (24, 38, "0")]),
    19: ([(1, 17, "01"), (19, 21, "0"), (23, 23, "01"), (25, 39, "1")],
         [(2, 18, "23"), (20, 40, "1")]),
    20: ([(1, 17, "01"), (19, 41, "0")],
         [(2, 18, "23"), (20, 22, "1"), (24, 24, "023"), (26, 40, "0")]),
    21: ([(1, 17, "01"), (19, 23, "0"), (25, 41, "1")],
         [(2, 18, "23"), (20, 22, "1"), (24, 42, "123")]),
    22: ([(1, 17, "01"), (19, 23, "0"), (25, 43, "01")],
         [(2, 18, "23"), (20, 22, "1"), (24, 24, "123"), (26, 42, "0")]),
    23: ([(1, 17, "01"), (19, 23, "0"), (25, 25, "01"), (27, 43, "1")],
         [(2, 18, "23"), (20, 22, "1"), (24, 24, "123"), (26, 44, "02")]),
}


def bands(x):
    if x in STATIC_BANDS:
        return STATIC_BANDS[x]
    odd_end = x + 21 if x % 2 == 0 else x + 20
    even_end = x + 20 if x % 2 == 0 else x + 21
    return (
        [(1, 17, "01"), (19, 23, "0"), (25, 25, "01"), (27, odd_end, "1")],
        [(2, 18, "23"), (20, 22, "1"), (24, 24, "123"),
         (26, 26, "02"), (28, even_end, "0")],
    )


MEX = {"01": 2, "23": 0, "03": 1, "0": 1, "1": 0,
       "12": 0, "023": 1, "123": 0, "02": 1}


def signature(x, R):
    rr = R - 1
    if x == 3:
        a = b = k1051(x, rr)
    else:
        a = z18_y3(x - 1, rr)
        b = k1051(x, rr)
    c = 1 ^ k1067(x, rr)
    return "".join(str(v) for v in sorted({a, b, c}))


def run():
    counts = {}

    n = 0
    for x in range(3, 51):
        for r in range(x + 46):
            a = g_ordered(r, (x, 3), 18)
            b = g_canon(r, (x, 3), 18)
            c = z18_y3(x, r)
            assert a == b == c, ("parent", x, r, a, b, c)
            n += 1
    counts["parent_ordered_canonical_formula"] = n

    n = 0
    for x in range(2, 81):
        for r in range(x + 36):
            a = g_ordered(r, (x, 2), 18)
            b = g_canon(r, (x, 2), 18)
            c = k1051(x, r)
            assert a == b == c, ("K1051", x, r, a, b, c)
            n += 1
    counts["K1051_B_anchor"] = n

    n = 0
    for x in range(3, 81):
        for r in range(x + 36):
            a = g_ordered(r, (x, 3), 17)
            b = g_canon(r, (x, 3), 17)
            c = k1067(x, r)
            assert a == b == c, ("K1067", x, r, a, b, c)
            n += 1
    counts["K1067_C_anchor"] = n

    n = 0
    for x in range(3, 101):
        O, E = bands(x)
        for parity, row, first in ((1, O, 1), (0, E, 2)):
            assert row[0][0] == first
            previous = None
            for lo, hi, sig in row:
                assert lo % 2 == parity and hi % 2 == parity and lo <= hi
                assert sig in MEX
                if previous is not None:
                    assert lo == previous + 2, ("band gap", x, parity, row)
                previous = hi
                for r in range(lo, hi + 1, 2):
                    got = signature(x, r)
                    assert got == sig, ("band identity", x, r, sig, got)
                    value = MEX[sig]
                    assert value == z18_y3(x, r), ("band mex", x, r, sig, value)
                    n += 1
            target = x + 21
            expected_top = target if target % 2 == parity else target - 1
            assert previous == expected_top, ("band top", x, parity, previous, expected_top)
    counts["signature_band_cover_identity_mex"] = n

    n = 0
    for x in range(4, 2001):
        for r in range(1, x + 22):
            s = signature(x, r)
            assert z18_y3(x, r) == MEX[s], ("induction", x, r, s)
            n += 1
    for r in range(1, 25):
        s = signature(3, r)
        assert z18_y3(3, r) == MEX[s], ("base", r, s)
        n += 1
    counts["induction_closure_sweep"] = n

    n = 0
    for x in range(3, 301):
        for r in range(22):
            a = z18_y3(x, r)
            b = single18(x + 3, r)
            assert a == b, ("low-R", x, r, a, b)
            n += 1
    counts["low_R_single_token"] = n

    assert z18_y3(16, 22) == 1
    assert single18(19, 22) == 0
    counts["low_R_sharpness_witness"] = 1

    n = 0
    for x in range(3, 101):
        for r in range(x + 22, x + 32):
            a = g_ordered(r, (x, 3), 18)
            b = g_canon(r, (x, 3), 18)
            c = (x + 3) % 2
            assert a == b == c, ("tail", x, r, a, b, c)
            n += 1
    counts["tail_direct"] = n

    n = 0
    for x in range(24, 200001):
        O, E = bands(x)
        for parity, row in ((1, O), (0, E)):
            for lo, hi, sig in row:
                midpoint = (lo + hi) // 2
                mid = midpoint - midpoint % 2 + parity
                for r in {lo, hi, mid}:
                    if lo <= r <= hi and r % 2 == parity:
                        assert signature(x, r) == sig, ("deep band", x, r, sig, signature(x, r))
                        assert MEX[sig] == z18_y3(x, r)
                        n += 1
        for r in (x + 22, x + 23, x + 30, x + 41):
            assert z18_y3(x, r) == (x + 3) % 2
            n += 1
    counts["deep_affine_samples"] = n

    rng = random.Random(20261120)
    n = 0
    for _ in range(5000):
        x = rng.randint(3, 10000)
        r = rng.randint(0, x + 40)
        v = z18_y3(x, r)
        assert v in (0, 1, 2)
        assert not (z18_y3_T(x, r) and z18_y3_P(x, r))
        if r >= x + 22:
            assert v == (x + 3) % 2
        elif r >= 1:
            s = signature(x, r)
            assert MEX[s] == v
        n += 1
    counts["fixed_seed_scatter"] = n

    counts["total_comparisons"] = sum(counts.values())
    counts["claim"] = "H(R;(x,3);18), all x>=3 and R>=0"
    counts["proof_status"] = "proved_by_R_strong_induction_and_complete_symbolic_signature_bands"
    counts["finite_audit_scope"] = {
        "parent_direct": "3<=x<=50, 0<=R<=x+45",
        "K1051_B_anchor": "2<=x<=80, 0<=R<=x+35",
        "K1067_C_anchor": "3<=x<=80, 0<=R<=x+35",
        "signature_bands": "3<=x<=100, complete 1<=R<=x+21",
        "induction_closure": "4<=x<=2000, 1<=R<=x+21 plus x=3 base R=1..24",
        "low_R": "3<=x<=300, 0<=R<=21",
        "tail_direct": "3<=x<=100, x+22<=R<=x+31",
        "deep_affine": "24<=x<=200000, all band endpoints/midpoints and four tail points",
        "scatter_seed": 20261120,
    }
    counts["ordered_states"] = g_ordered.cache_info().currsize
    counts["canonical_states"] = g_canon.cache_info().currsize
    counts["single_token_sharpness"] = {
        "x": 16, "R": 22, "two_token": z18_y3(16, 22),
        "single_token": single18(19, 22)
    }
    counts["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(counts, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                   encoding="utf-8")
    return counts


if __name__ == "__main__":
    result = run()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2))
