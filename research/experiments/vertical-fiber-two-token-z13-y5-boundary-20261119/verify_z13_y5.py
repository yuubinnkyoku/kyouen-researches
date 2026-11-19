#!/usr/bin/env python3
"""Independent verifier for the z=13, y=5 two-token residual Grundy slice.

Universal claim: all x>=5 and R>=0 are classified by candidate(). The proof
is the outer x-induction plus the complete A/B/C signature-band table in
report.md. This program audits the transcription and the published child
anchors K1027 (z=13,y=4), K1043 (z=12,y=5); it is not itself the source of
universality. Standard library only. Deterministic output: output/audit.json.
"""
from functools import lru_cache
import hashlib
import json
import random
import sys
from pathlib import Path

sys.setrecursionlimit(500000)


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


def clear_caches():
    H_ordered.cache_clear()
    H_canonical.cache_clear()


def odd(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi


# K1027: z=13, y=4.
def B_T(x, r):
    if x == 4: return odd(r, 1, 7)
    if x in (5, 6): return odd(r, 1, 9)
    if x in (7, 8): return odd(r, 1, 11)
    if x == 9: return odd(r, 1, 17)
    if x in (10, 11, 12): return odd(r, 1, 13)
    if x == 13: return odd(r, 1, 13) or r == 19
    if x in (14, 15, 16): return odd(r, 1, 13)
    if x == 17: return odd(r, 1, 13) or r == 21
    if x == 18: return odd(r, 1, 13) or odd(r, 21, 35)
    return odd(r, 1, 13) or r == 21


def B_P(x, r):
    if x in (4, 6, 8): return False
    if x == 5: return r >= 10
    if x == 7: return r >= 12
    if x in (9, 11): return r in (14, 16, 18) or r >= 19
    if x == 10: return r in (14, 16)
    if x in (12, 14): return r in (14, 16, 18)
    if x in (13, 15): return r in (14, 16, 18, 20) or r >= 21
    if x in (16, 18): return r in (14, 16, 18, 20)
    if x == 17: return r in (14, 16, 18, 20) or r >= 22
    if x % 2 == 0:
        return r in (14, 16, 18, 20) or (r % 2 == 1 and 23 <= r <= x + 17)
    return (r in (14, 16, 18, 20)
            or (r % 2 == 1 and 23 <= r <= x + 16)
            or r >= x + 18)


def B(x, r):
    if r == 0: return 0
    if B_T(x, r): return 2
    return 1 if B_P(x, r) else 0


# K1043: z=12, y=5.
def C_T(x, r):
    if x == 5: return odd(r, 1, 9)
    if x == 6: return odd(r, 1, 11)
    if x == 7: return odd(r, 1, 17)
    if x in (8, 9, 10): return odd(r, 1, 11)
    if x == 11: return odd(r, 1, 11) or r == 19
    if x in (12, 13, 14): return odd(r, 1, 11)
    if x == 15: return odd(r, 1, 11) or r == 21
    if x in (16, 17): return odd(r, 1, 11)
    if x == 18: return odd(r, 1, 11) or odd(r, 23, 35)
    return odd(r, 1, 11) or r == 23


def C_P(x, r):
    if x == 5: return False
    if x == 6: return r >= 12
    if x == 7: return False
    if x == 8: return r in (13, 15, 17) or r >= 18
    if x == 9: return r in (13, 15, 17)
    if x == 10: return r in (13, 15, 17, 19) or r >= 20
    if x == 11: return r in (13, 15, 17)
    if x == 12: return r in (13, 15, 17, 19) or r >= 20
    if x == 13: return r in (13, 15, 17, 19)
    if x == 14: return r in (13, 15, 17, 19, 21) or r >= 22
    if x == 15: return r in (13, 15, 17, 19)
    if x == 16: return r in (13, 15, 17, 19, 21) or r >= 22
    if x == 17: return r in (13, 15, 17, 19, 21)
    if x % 2 == 0:
        return (r in (13, 15, 17, 19, 21)
                or (r % 2 == 0 and 24 <= r <= x + 18)
                or r >= x + 19)
    return r in (13, 15, 17, 19, 21) or (r % 2 == 0 and 24 <= r <= x + 17)


def C(x, r):
    if r == 0: return 0
    if C_T(x, r): return 2
    return 1 if C_P(x, r) else 0


# Candidate theorem: T is Grundy 2, P is Grundy 1, all other R are 0.
def T(x, r):
    if x == 5: return odd(r, 1, 9)
    if x in (6, 7): return odd(r, 1, 11)
    if x == 8: return odd(r, 1, 17)
    if x == 9: return odd(r, 1, 13)
    if x == 10: return odd(r, 1, 13) or r == 19
    if x in (11, 12, 13, 15, 16, 17): return odd(r, 1, 13)
    if x == 14: return odd(r, 1, 13) or r == 21
    if x == 18: return odd(r, 1, 13) or r == 23
    if x == 19: return odd(r, 1, 13) or odd(r, 23, 37)
    return odd(r, 1, 13) or r == 23


def P(x, r):
    if x == 5: return False
    if x == 6: return r >= 12
    if x == 7: return False
    if x == 8: return r in (14, 16, 18) or r >= 19
    if x == 9: return r in (14, 16, 18)
    if x == 10: return r in (14, 16, 18, 20) or r >= 21
    if x == 11: return r in (14, 16, 18)
    if x == 12: return r in (14, 16, 18, 20) or r >= 21
    if x == 13: return r in (14, 16, 18, 20)
    if x == 14: return r in (14, 16, 18, 20, 22) or r >= 23
    if x == 15: return r in (14, 16, 18, 20)
    if x == 16: return r in (14, 16, 18, 20, 22) or r >= 23
    if x == 17: return r in (14, 16, 18, 20, 22)
    if x == 18: return r in (14, 16, 18, 20, 22) or r >= 24
    if x == 19: return r in (14, 16, 18, 20, 22)
    if x % 2 == 0:
        return (r in (14, 16, 18, 20, 22)
                or (r % 2 == 1 and 25 <= r <= x + 17)
                or r >= x + 19)
    return r in (14, 16, 18, 20, 22) or (r % 2 == 1 and 25 <= r <= x + 18)


def candidate(x, r):
    if r == 0: return 0
    if T(x, r): return 2
    return 1 if P(x, r) else 0


# (parity, lo, hi, signature), where parity 1 is odd and 0 is even.
FIXED_BANDS = {
 5: [(1,1,9,'01'),(1,11,23,'1'),(0,2,10,'23'),(0,12,22,'1')],
 6: [(1,1,11,'01'),(1,13,23,'0'),(0,2,10,'23'),(0,12,12,'03'),(0,14,24,'0')],
 7: [(1,1,11,'01'),(1,13,25,'1'),(0,2,12,'23'),(0,14,18,'13'),(0,20,24,'1')],
 8: [(1,1,17,'01'),(1,19,25,'0'),(0,2,12,'23'),(0,14,26,'0')],
 9: [(1,1,13,'01'),(1,15,27,'1'),(0,2,12,'23'),(0,14,18,'02'),(0,20,26,'1')],
 10:[(1,1,13,'01'),(1,15,17,'1'),(1,19,19,'01'),(1,21,27,'0'),(0,2,12,'23'),(0,14,14,'02'),(0,16,28,'0')],
 11:[(1,1,13,'01'),(1,15,29,'1'),(0,2,12,'23'),(0,14,14,'02'),(0,16,18,'0'),(0,20,20,'123'),(0,22,28,'1')],
 12:[(1,1,13,'01'),(1,15,19,'1'),(1,21,29,'0'),(0,2,12,'23'),(0,14,14,'02'),(0,16,30,'0')],
 13:[(1,1,13,'01'),(1,15,31,'1'),(0,2,12,'23'),(0,14,14,'02'),(0,16,18,'0'),(0,20,20,'02'),(0,22,30,'1')],
 14:[(1,1,13,'01'),(1,15,19,'1'),(1,21,21,'01'),(1,23,31,'0'),(0,2,12,'23'),(0,14,14,'02'),(0,16,32,'0')],
 15:[(1,1,13,'01'),(1,15,33,'1'),(0,2,12,'23'),(0,14,14,'02'),(0,16,20,'0'),(0,22,22,'123'),(0,24,32,'1')],
 16:[(1,1,13,'01'),(1,15,21,'1'),(1,23,33,'0'),(0,2,12,'23'),(0,14,14,'02'),(0,16,34,'0')],
 17:[(1,1,13,'01'),(1,15,35,'1'),(0,2,12,'23'),(0,14,14,'02'),(0,16,20,'0'),(0,22,22,'02'),(0,24,34,'1')],
 18:[(1,1,13,'01'),(1,15,21,'1'),(1,23,23,'01'),(1,25,35,'0'),(0,2,12,'23'),(0,14,14,'02'),(0,16,20,'0'),(0,22,22,'02'),(0,24,36,'023')],
 19:[(1,1,13,'01'),(1,15,21,'1'),(1,23,37,'01'),(0,2,12,'23'),(0,14,14,'02'),(0,16,20,'0'),(0,22,22,'02'),(0,24,24,'123'),(0,26,36,'1')],
 20:[(1,1,13,'01'),(1,15,21,'1'),(1,23,23,'01'),(1,25,37,'0'),(0,2,12,'23'),(0,14,14,'02'),(0,16,20,'0'),(0,22,22,'02'),(0,24,24,'123'),(0,26,38,'12')],
}


def bands(x):
    if x in FIXED_BANDS:
        return FIXED_BANDS[x]
    if x >= 22 and x % 2 == 0:
        return [(1,1,13,'01'),(1,15,21,'1'),(1,23,23,'01'),(1,25,x+17,'0'),
                (0,2,12,'23'),(0,14,14,'02'),(0,16,20,'0'),(0,22,22,'02'),
                (0,24,24,'123'),(0,26,x+18,'1')]
    if x >= 21 and x % 2 == 1:
        return [(1,1,13,'01'),(1,15,21,'1'),(1,23,23,'01'),(1,25,x+18,'0'),
                (0,2,12,'23'),(0,14,14,'02'),(0,16,20,'0'),(0,22,22,'02'),
                (0,24,24,'123'),(0,26,x+17,'1')]
    raise ValueError(x)


def signature_from_children(x, R):
    r = R - 1
    values = {B(x, r), 1 ^ C(x, r)}
    if x > 5:
        values.add(candidate(x - 1, r))
    return ''.join(str(v) for v in sorted(values))


def single_token(x, z, R):
    if R == 0 or x <= 0: return 0
    if z == 0: return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2*x - 1: return 2
        if R % 2 == 0 and R <= x - 1: return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = z if z % 2 else z - 1
        if R <= m: return 2 if R % 2 else 0
        if m < R < x + z: return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = x if x % 2 else x - 1
        if R <= m: return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x,z,R))


def audit_once():
    clear_caches()
    checks = {}
    n = 0
    for x in range(5, 27):
        for r in range(x + 26):
            a = H_ordered(r, (x, 5), 13)
            b = H_canonical(r, (x, 5), 13)
            c = candidate(x, r)
            if a != b or a != c:
                raise AssertionError(("root-grid", x, r, a, b, c))
            n += 1
    checks["root_two_engines_vs_closed_form"] = n

    nb = nc = 0
    for x in range(4, 22):
        for r in range(x + 26):
            a = H_ordered(r, (x, 4), 13)
            b = H_canonical(r, (x, 4), 13)
            c = B(x, r)
            if a != b or a != c:
                raise AssertionError(("B-anchor", x, r, a, b, c))
            nb += 1
    for x in range(5, 22):
        for r in range(x + 26):
            a = H_ordered(r, (x, 5), 12)
            b = H_canonical(r, (x, 5), 12)
            c = C(x, r)
            if a != b or a != c:
                raise AssertionError(("C-anchor", x, r, a, b, c))
            nc += 1
    checks["K1027_B_anchor"] = nb
    checks["K1043_C_anchor"] = nc

    ns = 0
    for x in range(5, 1001):
        expected_R = set(range(1, x + 19))
        covered = set()
        for parity, lo, hi, sig in bands(x):
            if not (1 <= lo <= hi <= x + 18):
                raise AssertionError(("bad-band-bounds", x, parity, lo, hi, sig))
            for r in range(lo, hi + 1, 2):
                if r % 2 != parity or r in covered:
                    raise AssertionError(("band-overlap-or-parity", x, r, sig))
                covered.add(r)
                actual = signature_from_children(x, r)
                if actual != sig:
                    raise AssertionError(("signature", x, r, sig, actual))
                if mex(map(int, sig)) != candidate(x, r):
                    raise AssertionError(("mex", x, r, sig, candidate(x,r)))
                ns += 1
        if covered != expected_R:
            raise AssertionError(("coverage", x))
    checks["signature_coverage_and_mex"] = ns

    nl = 0
    for x in range(5, 5001):
        for r in range(15):
            if candidate(x, r) != single_token(x + 5, 13, r):
                raise AssertionError(("height-only", x, r))
            nl += 1
    checks["height_only_formula"] = nl

    nt = 0
    for x in range(5, 5001):
        for r in range(x + 19, x + 23):
            if candidate(x, r) != ((x + 5) % 2):
                raise AssertionError(("tail", x, r))
            nt += 1
    checks["tail_formula"] = nt

    rng = random.Random(20261124)
    nr = 0
    for _ in range(1000):
        x = rng.randint(5, 28)
        r = rng.randint(0, x + 26)
        a = H_ordered(r, (x, 5), 13)
        b = H_canonical(r, (x, 5), 13)
        c = candidate(x, r)
        if a != b or a != c:
            raise AssertionError(("scatter", x, r, a, b, c))
        nr += 1
    checks["fixed_seed_scatter"] = nr

    return {
        "theorem": "H(R;(x,5);13) candidate classification",
        "scope": {"x_min": 5, "R_min": 0, "R_unbounded": True},
        "checks": checks,
        "total_comparisons": sum(checks.values()),
        "mismatches": 0,
        "seed": 20261124,
        "universal_basis": "outer induction on x plus complete symbolic A/B/C signature bands; finite checks are audits only",
    }


def main():
    first = audit_once()
    second = audit_once()
    b1 = json.dumps(first, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    b2 = json.dumps(second, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    if b1 != b2:
        raise AssertionError("two in-process audits are not byte-identical")
    out = Path(__file__).resolve().parent / "output"
    out.mkdir(parents=True, exist_ok=True)
    (out / "audit.json").write_text(b1, encoding="utf-8")
    print(b1, end="")
    print("sha256=" + hashlib.sha256(b1.encode()).hexdigest())


if __name__ == "__main__":
    main()
