#!/usr/bin/env python3
"""Independent audit for the uniform two-token z=14, y>=6 theorem.

The universal proof is the symbolic A/B/C signature-band table in report.md.
This verifier checks the table, its mex, the two published child anchors, and
independent order-preserving / sorted direct recurrences on finite grids.
Finite checks are not used as a substitute for the universal induction.
"""
from functools import lru_cache
from pathlib import Path
import hashlib
import json
import random


def mex(values):
    m = 0
    while m in values:
        m += 1
    return m


@lru_cache(None)
def h_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            child = X[:i] + (v - 1,) + X[i + 1:]
            opts.add(h_ordered(R - 1, child, z))
        else:
            child = X[:i] + X[i + 1:]
            opts.add(h_ordered(R - 1, child, z + 1))
    if z >= 1:
        opts.add(1 ^ h_ordered(R - 1, X, z - 1))
    return mex(opts)


@lru_cache(None)
def h_sorted(R, X, z):
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(h_sorted(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(h_sorted(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ h_sorted(R - 1, X, z - 1))
    return mex(opts)


def in_odd(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi


def in_even(r, lo, hi):
    return r % 2 == 0 and lo <= r <= hi


def value14_T(x, y, r):
    d, Y = x - y, 2 * y
    if (y, d) == (6, 0):
        return in_odd(r, 1, 11)
    if (y, d) == (7, 0):
        return in_odd(r, 1, 21)
    if (y, d) == (6, 2):
        return in_odd(r, 1, 19)
    if in_odd(r, 1, 13):
        return True
    if d in (0, 4, 8, 12):
        return r == Y + 7 + d // 2
    if d == 15:
        return in_odd(r, Y + 15, x + y + 14)
    if d >= 16:
        return r == Y + 15
    return False


def value14_P(x, y, r):
    d, Y, S = x - y, 2 * y, x + y
    if (y, d) in ((6, 0), (7, 0), (6, 2)):
        return False
    if (y, d) == (6, 1):
        return r >= 14
    if d % 2 == 0 and d <= 14:
        return in_odd(r, 15, Y + 5 + 2 * ((d + 3) // 4))
    if d % 2 == 1 and d <= 13:
        return (in_odd(r, 15, S + 14)
                or in_even(r, Y + 8 + 2 * ((d + 2) // 4), S + 13)
                or r >= S + 15)
    if d % 2 == 0 and d >= 16:
        return (in_odd(r, 15, Y + 13)
                or in_even(r, Y + 16, S + 14))
    if d % 2 == 1 and d >= 15:
        return (in_odd(r, 15, Y + 13)
                or in_even(r, Y + 16, S + 13)
                or r >= S + 15)
    return False


def value14(x, y, r):
    if r == 0:
        return 0
    S = x + y
    if r >= S + 15:
        return S % 2
    if value14_T(x, y, r):
        return 2
    if value14_P(x, y, r):
        return 1
    return 0


def q_odd(n):
    return n if n % 2 else n - 1


def single_token(x, z, r):
    """K0832 single-token closed form."""
    if r == 0 or x <= 0:
        return 0
    if z == 0:
        return min(r, x) % 2
    if z == x:
        if r % 2 and r <= 2 * x - 1:
            return 2
        if r % 2 == 0 and r <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if r <= m:
            return 2 if r % 2 else 0
        if m < r < x + z:
            return (r + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if r <= m:
            return 2 if r % 2 else 0
        return x % 2
    raise ValueError((x, z, r))


# K1047: z=14, y=5 child used at the y=6 induction base.
def k1047_T(x, r):
    if x == 5:
        return in_odd(r, 1, 9)
    if x in (6, 7):
        return in_odd(r, 1, 11)
    if x == 8:
        return in_odd(r, 1, 13)
    if x == 9:
        return in_odd(r, 1, 19)
    if 10 <= x <= 12:
        return in_odd(r, 1, 13)
    if x == 13:
        return in_odd(r, 1, 13) or r == 21
    if 14 <= x <= 16:
        return in_odd(r, 1, 13)
    if x == 17:
        return in_odd(r, 1, 13) or r == 23
    if x in (18, 19):
        return in_odd(r, 1, 13)
    if x == 20:
        return in_odd(r, 1, 13) or in_odd(r, 25, 39)
    return in_odd(r, 1, 13) or r == 25


def k1047_P(x, r):
    if x == 5:
        return False
    if x == 6:
        return r >= 12
    if x == 7:
        return False
    if x == 8:
        return r >= 14
    if x == 9:
        return False
    if x == 10:
        return r in (15, 17, 19) or r >= 20
    if x == 11:
        return r in (15, 17, 19)
    if x == 12:
        return r in (15, 17, 19) or r >= 21
    if x == 13:
        return r in (15, 17, 19)
    if x == 14:
        return r in (15, 17, 19) or r >= 21
    if x == 15:
        return r in (15, 17, 19, 21)
    if x == 16:
        return r in (15, 17, 19, 21) or r >= 23
    if x == 17:
        return r in (15, 17, 19, 21)
    if x == 18:
        return r in (15, 17, 19, 21) or r >= 23
    if x == 19:
        return r in (15, 17, 19, 21, 23)
    if x % 2 == 0:
        return (r in (15, 17, 19, 21, 23)
                or in_even(r, 26, x + 18) or r >= x + 20)
    return r in (15, 17, 19, 21, 23) or in_even(r, 26, x + 19)


def k1047(x, r):
    if r == 0:
        return 0
    if k1047_T(x, r):
        return 2
    return 1 if k1047_P(x, r) else 0


# K1061: z=13, all x>=y>=6 child used as C.
def z13_T(x, y, r):
    d, S, Y = x - y, x + y, 2 * y
    if y == 6 and d == 0:
        return in_odd(r, 1, 11)
    if y == 6 and d == 1:
        return in_odd(r, 1, 19)
    if in_odd(r, 1, 13):
        return True
    if d % 2 == 1 and 1 <= d <= 13 and (d + 13) % 4 == 2:
        return r == Y + (d + 13) // 2
    if d == 14:
        return in_odd(r, Y + 13, S + 13)
    if d >= 15:
        return r == Y + 13
    return False


def z13_P(x, y, r):
    d, S, Y = x - y, x + y, 2 * y
    if y == 6 and d == 0:
        return False
    if d % 2 == 0:
        if d <= 12:
            return in_even(r, 14, Y + 4 + 2 * ((d + 5) // 4))
        if d == 14:
            return in_even(r, 14, Y + 12)
        return in_even(r, 14, Y + 12) or in_odd(r, Y + 15, S + 13)
    if d <= 13:
        return (in_even(r, 14, S + 13)
                or in_odd(r, Y + 7 + 2 * ((d + 3) // 4), S + 12))
    return in_even(r, 14, Y + 12) or in_odd(r, Y + 15, S + 12)


def value13(x, y, r):
    if r == 0:
        return 0
    S = x + y
    if r >= S + 14:
        return S % 2
    if z13_T(x, y, r):
        return 2
    if z13_P(x, y, r):
        return 1
    return 0


def signature_bands(y, d):
    """Exact A/B/C signature bands for 1<=R<=S+14."""
    Y, S = 2 * y, 2 * y + d
    if (y, d) == (6, 0):
        return ([(1, 11, "01"), (13, Y + 13, "1")],
                [(2, 12, "23"), (14, Y + 14, "1")])
    if (y, d) == (7, 0):
        return ([(1, Y + 7, "01"), (Y + 9, Y + 13, "1")],
                [(2, 14, "23"), (Y + 2, Y + 14, "1")])
    if (y, d) == (6, 1):
        return ([(1, 13, "01"), (15, Y + 15, "0")],
                [(2, 12, "23"), (14, Y + 8, "03"), (Y + 10, Y + 14, "0")])
    if (y, d) == (6, 2):
        return ([(1, Y + 7, "01"), (Y + 9, Y + 15, "1")],
                [(2, 14, "23"), (Y + 4, Y + 16, "1")])
    if (y, d) == (6, 3):
        return ([(1, 13, "01"), (15, Y + 17, "0")],
                [(2, 14, "23"), (Y + 4, Y + 8, "12"), (Y + 10, Y + 16, "0")])
    if (y, d) == (7, 1):
        return ([(1, 13, "01"), (15, Y + 15, "0")],
                [(2, 14, "23"), (Y + 2, Y + 6, "12"),
                 (Y + 8, Y + 8, "023"), (Y + 10, Y + 14, "0")])
    if (y, d) == (7, 3):
        return ([(1, 13, "01"), (15, Y + 17, "0")],
                [(2, 14, "23"), (Y + 2, Y + 6, "1"),
                 (Y + 8, Y + 8, "12"), (Y + 10, Y + 16, "0")])
    if d == 0:
        return ([(1, 13, "01"), (15, Y + 5, "0"),
                 (Y + 7, Y + 7, "01"), (Y + 9, Y + 13, "1")],
                [(2, 14, "23"), (16, Y + 14, "1")])
    if d % 2 == 0 and 2 <= d <= 12:
        st = Y + 7 + 2 * ((d + 3) // 4)
        O = [(1, 13, "01"), (15, st - 2, "0")]
        if d % 4 == 0:
            O += [(st, st, "01"), (st + 2, Y + 13 + d, "1")]
        else:
            O += [(st, Y + 13 + d, "1")]
        return O, [(2, 14, "23"), (16, Y + 14 + d, "1")]
    if d % 2 == 1 and d <= 13:
        c = Y + 6 + 2 * ((d - 1) // 4)
        O = [(1, 13, "01"), (15, S + 14, "0")]
        special = "023" if d % 4 == 1 else "12"
        return O, [(2, 14, "23"), (16, c, "1"),
                   (c + 2, c + 2, special), (c + 4, S + 13, "0")]
    if d == 14:
        return ([(1, 13, "01"), (15, Y + 13, "0"), (Y + 15, Y + 27, "1")],
                [(2, 14, "23"), (16, Y + 12, "1"), (Y + 14, Y + 28, "123")])
    if d == 15:
        return ([(1, 13, "01"), (15, Y + 13, "0"), (Y + 15, S + 14, "01")],
                [(2, 14, "23"), (16, Y + 12, "1"),
                 (Y + 14, Y + 14, "123"), (Y + 16, S + 13, "0")])
    if d == 16:
        return ([(1, 13, "01"), (15, Y + 13, "0"),
                 (Y + 15, Y + 15, "01"), (Y + 17, S + 13, "1")],
                [(2, 14, "23"), (16, Y + 12, "1"),
                 (Y + 14, Y + 14, "123"), (Y + 16, S + 14, "02")])
    if d >= 17:
        o_hi = S + 14 if d % 2 else S + 13
        e_hi = S + 13 if d % 2 else S + 14
        return ([(1, 13, "01"), (15, Y + 13, "0"),
                 (Y + 15, Y + 15, "01"), (Y + 17, o_hi, "1")],
                [(2, 14, "23"), (16, Y + 12, "1"),
                 (Y + 14, Y + 14, "123"), (Y + 16, Y + 16, "02"),
                 (Y + 18, e_hi, "0")])
    raise ValueError((y, d))


def child_signature(x, y, r):
    d = x - y
    opts = {k1047(x, r) if y == 6 else value14(x, y - 1, r)}
    if d > 0:
        opts.add(value14(x - 1, y, r))
    opts.add(1 ^ value13(x, y, r))
    return "".join(str(v) for v in sorted(opts))


def run_audit():
    counts = {}
    failures = []

    n = 0
    for y in range(6, 13):
        for d in range(31):
            x, S = y + d, 2 * y + d
            for r in range(S + 16):
                n += 1
                a = h_ordered(r, (x, y), 14)
                b = h_sorted(r, (x, y), 14)
                c = value14(x, y, r)
                if a != b or a != c:
                    failures.append(("direct", y, d, r, a, b, c))
                    break
            if failures:
                break
        if failures:
            break
    counts["dual_direct_engine_vs_closed_form"] = n

    n = 0
    for x in range(6, 41):
        for r in range(x + 21):
            n += 1
            a = h_ordered(r, (x, 5), 14)
            b = h_sorted(r, (x, 5), 14)
            c = k1047(x, r)
            if a != b or a != c:
                failures.append(("B-anchor", x, r, a, b, c))
                break
        if failures:
            break
    counts["K1047_B_child_anchor"] = n

    n = 0
    for y in range(6, 13):
        for d in range(21):
            x, S = y + d, 2 * y + d
            for r in range(S + 15):
                n += 1
                a = h_ordered(r, (x, y), 13)
                b = h_sorted(r, (x, y), 13)
                c = value13(x, y, r)
                if a != b or a != c:
                    failures.append(("C-anchor", y, d, r, a, b, c))
                    break
            if failures:
                break
        if failures:
            break
    counts["K1061_C_child_anchor"] = n

    n = 0
    for y in range(6, 101):
        for d in range(101):
            x, S = y + d, 2 * y + d
            O, E = signature_bands(y, d)
            for r in range(1, S + 15):
                n += 1
                bands = O if r % 2 else E
                hits = [sig for lo, hi, sig in bands if lo <= r <= hi]
                if len(hits) != 1:
                    failures.append(("coverage", y, d, r, hits))
                    break
                sig = hits[0]
                derived = child_signature(x, y, r - 1)
                if sig != derived:
                    failures.append(("signature", y, d, r, sig, derived))
                    break
                if mex({int(ch) for ch in sig}) != value14(x, y, r):
                    failures.append(("mex", y, d, r, sig))
                    break
            if failures:
                break
        if failures:
            break
    counts["symbolic_band_coverage_signature_mex"] = n

    n = 0
    for y in range(6, 101):
        for d in range(101):
            S = 2 * y + d
            for r in range(21):
                n += 1
                if value14(y + d, y, r) != single_token(S, 14, r):
                    failures.append(("lowR", y, d, r))
                    break
            if failures:
                break
        if failures:
            break
    counts["lowR_single_token_corollary"] = n

    n = 0
    for y in range(6, 11):
        for d in range(16):
            x, S = y + d, 2 * y + d
            for r in range(S + 15, S + 21):
                n += 1
                a = h_ordered(r, (x, y), 14)
                b = h_sorted(r, (x, y), 14)
                if a != b or a != S % 2:
                    failures.append(("tail", y, d, r, a, b, S % 2))
                    break
            if failures:
                break
        if failures:
            break
    counts["tail_direct_engine"] = n

    rng = random.Random(20261120)
    n = 0
    for _ in range(1000):
        y = rng.randint(6, 35)
        d = rng.randint(0, 80)
        x, S = y + d, 2 * y + d
        r = rng.randint(0, S + 25)
        n += 1
        a = h_ordered(r, (x, y), 14)
        b = h_sorted(r, (x, y), 14)
        c = value14(x, y, r)
        if a != b or a != c:
            failures.append(("scatter", y, d, r, a, b, c))
            break
    counts["fixed_seed_scatter"] = n

    payload = {
        "theorem": "H(R;(x,y);14), x>=y>=6, R>=0: full Grundy classification",
        "finite_audit_only": True,
        "counts": counts,
        "total_checks": sum(counts.values()),
        "mismatch_count": len(failures),
        "first_failure": list(failures[0]) if failures else None,
        "seed": 20261120,
        "proof_boundary": "Universal claim rests on y-strong induction, x-outer induction, and the complete symbolic A/B/C signature-band table; finite checks are cross-validation only.",
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    payload["sha256_without_self"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return payload


if __name__ == "__main__":
    result = run_audit()
    here = Path(__file__).resolve().parent
    out = here / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"total_checks": result["total_checks"],
                      "mismatch_count": result["mismatch_count"],
                      "counts": result["counts"],
                      "sha256_without_self": result["sha256_without_self"]},
                     ensure_ascii=False, sort_keys=True))
    if result["mismatch_count"]:
        raise SystemExit(1)
