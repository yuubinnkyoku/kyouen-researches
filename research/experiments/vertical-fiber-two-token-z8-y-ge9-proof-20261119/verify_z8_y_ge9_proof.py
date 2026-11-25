#!/usr/bin/env python3
"""Independent audit for the uniform z=8, y>=9 two-token full Grundy classification (K1000).

Theorem under audit (proved by double induction, this file is the finite independent audit):
  For every x>=y>=9 and R>=0, H(R;(x,y);8) in {0,1,2} with
  value 2 positions T(x,y), value 1 positions P(x,y), and tail H=(x+y) mod 2 for R>=x+y+9.

Anchors: K0996 (z=8,y=8 full slice, used as the B child of the y=9 row),
K0999 (z=8,y=9 full slice, independently proved by the parallel lane; reproduced here),
K0976 (z=7,y>=4 uniform formula, used as every C child), K0832 (recursion, Theorem T, tails).
"""
from __future__ import annotations
import hashlib
import json
from functools import lru_cache
from pathlib import Path


def mex(values):
    s = set(values)
    n = 0
    while n in s:
        n += 1
    return n


def odd(r, a, b):
    return r % 2 == 1 and a <= r <= b


def even(r, a, b):
    return r % 2 == 0 and a <= r <= b


def at_least(r, a):
    return r >= a


# ---------------------------------------------------------------- anchors
def z8_y8(x, r):
    """K0996 published closed form: H(R;(x,8);8), all x>=8, R>=0."""
    if r == 0:
        return 0
    t = (r in (1, 3, 5, 7) or (x == 10 and r == 21) or
         (x == 14 and r == 23) or
         (x == 17 and odd(r, 25, 33)) or
         (x >= 18 and r == 25))
    if x == 8:
        p = odd(r, 9, 19)
    elif x in (9, 11):
        p = odd(r, 9, 19) or at_least(r, 21)
    elif x == 10:
        p = odd(r, 9, 19)
    elif x == 12:
        p = odd(r, 9, 21)
    elif x in (13, 15):
        p = odd(r, 9, 21) or at_least(r, 23)
    elif x == 14:
        p = odd(r, 9, 21)
    elif x == 16:
        p = odd(r, 9, 23)
    elif x == 17:
        p = odd(r, 9, 23) or even(r, 26, 32) or at_least(r, 34)
    elif x == 18:
        p = odd(r, 9, 23) or even(r, 26, 34)
    else:
        p = odd(r, 9, 23) or even(r, 26, x + 16) or (x % 2 == 1 and at_least(r, x + 17))
    return 2 if t else 1 if p else 0


def z7_ge4(x, y, r):
    """K0976 published uniform closed form: H(R;(x,y);7), all x>=y>=4, R>=0."""
    if r == 0:
        return 0
    d = x - y
    s = x + y
    t = (r in (1, 3, 5, 7) or (d == 3 and r == 2 * y + 5) or
         (d == 7 and r == 2 * y + 7) or
         (d == 8 and r in (2 * y + 7, 2 * y + 9, 2 * y + 11, 2 * y + 13, 2 * y + 15)) or
         (d >= 9 and r == 2 * y + 7))
    p = ((d == 0 and even(r, 8, 2 * y + 2)) or
         (d == 1 and (even(r, 8, 2 * y + 8) or odd(r, 2 * y + 5, 2 * y + 7))) or
         (d == 2 and even(r, 8, 2 * y + 4)) or
         (d == 3 and (even(r, 8, 2 * y + 10) or odd(r, 2 * y + 7, 2 * y + 9))) or
         (d == 4 and even(r, 8, 2 * y + 4)) or
         (d == 5 and (even(r, 8, 2 * y + 12) or odd(r, 2 * y + 7, 2 * y + 11))) or
         (d == 6 and even(r, 8, 2 * y + 6)) or
         (d == 7 and (even(r, 8, 2 * y + 14) or odd(r, 2 * y + 9, 2 * y + 13))) or
         (d == 8 and even(r, 8, 2 * y + 6)) or
         (d >= 9 and (even(r, 8, 2 * y + 6) or odd(r, 2 * y + 9, min(2 * y + 2 * d - 3, s + 7)))))
    if t:
        return 2
    if p:
        return 1
    if r >= s + 8:
        return s % 2
    return 0


# ---------------------------------------------------------- uniform candidate
def candidate(x, y, r):
    """Uniform closed form: H(R;(x,y);8) for all x>=y>=9, R>=0 (K0999)."""
    if r == 0:
        return 0
    if r >= x + y + 9:
        return (x + y) % 2
    d = x - y
    t = (r in (1, 3, 5, 7) or
         (d == 2 and r == 2 * y + 5) or
         (d == 6 and r == 2 * y + 7) or
         (d == 9 and odd(r, 2 * y + 9, 2 * y + 17)) or
         (d >= 10 and r == 2 * y + 9))
    if t:
        return 2
    if d == 0:
        p = odd(r, 9, 2 * y + 3)
    elif d == 1:
        p = odd(r, 9, 2 * y + 9) or even(r, 2 * y + 6, 2 * y + 9)
    elif d == 2:
        p = odd(r, 9, 2 * y + 3)
    elif d == 3:
        p = odd(r, 9, 2 * y + 11) or even(r, 2 * y + 6, 2 * y + 11)
    elif d == 4:
        p = odd(r, 9, 2 * y + 5)
    elif d == 5:
        p = odd(r, 9, 2 * y + 13) or even(r, 2 * y + 8, 2 * y + 13)
    elif d == 6:
        p = odd(r, 9, 2 * y + 5)
    elif d == 7:
        p = odd(r, 9, 2 * y + 15) or even(r, 2 * y + 8, 2 * y + 15)
    elif d == 8:
        p = odd(r, 9, 2 * y + 7)
    elif d == 9:
        p = odd(r, 9, 2 * y + 7) or even(r, 2 * y + 10, 2 * y + 16)
    else:
        p = odd(r, 9, 2 * y + 7) or even(r, 2 * y + 10, x + y + 8)
    return 1 if p else 0


# ------------------------------------------------------------ signature bands
def bands_for(y, d, X):
    """Parametric A/B/C signature bands covering 1<=R<=X with X=x+y+8, d=x-y>=0, y>=9."""
    if d == 0:
        return [(1, 1, 7, "01"), (1, 9, 2 * y + 3, "0"), (1, 2 * y + 5, X, "1"),
                (0, 2, 8, "23"), (0, 10, X, "1")]
    if d == 1:
        return [(1, 1, 7, "01"), (1, 9, X, "0"),
                (0, 2, 8, "23"), (0, 10, 2 * y + 2, "1"),
                (0, 2 * y + 4, 2 * y + 4, "12"), (0, 2 * y + 6, X, "0")]
    if d == 2:
        return [(1, 1, 7, "01"), (1, 9, 2 * y + 3, "0"), (1, 2 * y + 5, 2 * y + 5, "01"),
                (1, 2 * y + 7, X, "1"),
                (0, 2, 8, "23"), (0, 10, X, "1")]
    if d == 3:
        return [(1, 1, 7, "01"), (1, 9, X, "0"),
                (0, 2, 8, "23"), (0, 10, 2 * y + 4, "1"),
                (0, 2 * y + 6, 2 * y + 6, "023"), (0, 2 * y + 8, X, "0")]
    if d == 4:
        return [(1, 1, 7, "01"), (1, 9, 2 * y + 5, "0"), (1, 2 * y + 7, X, "1"),
                (0, 2, 8, "23"), (0, 10, X, "1")]
    if d == 5:
        return [(1, 1, 7, "01"), (1, 9, X, "0"),
                (0, 2, 8, "23"), (0, 10, 2 * y + 4, "1"),
                (0, 2 * y + 6, 2 * y + 6, "12"), (0, 2 * y + 8, X, "0")]
    if d == 6:
        return [(1, 1, 7, "01"), (1, 9, 2 * y + 5, "0"), (1, 2 * y + 7, 2 * y + 7, "01"),
                (1, 2 * y + 9, X, "1"),
                (0, 2, 8, "23"), (0, 10, X, "1")]
    if d == 7:
        return [(1, 1, 7, "01"), (1, 9, X, "0"),
                (0, 2, 8, "23"), (0, 10, 2 * y + 6, "1"),
                (0, 2 * y + 8, 2 * y + 8, "023"), (0, 2 * y + 10, X, "0")]
    if d == 8:
        return [(1, 1, 7, "01"), (1, 9, 2 * y + 7, "0"), (1, 2 * y + 9, X, "1"),
                (0, 2, 8, "23"), (0, 10, 2 * y + 6, "1"), (0, 2 * y + 8, X, "123")]
    if d == 9:
        return [(1, 1, 7, "01"), (1, 9, 2 * y + 7, "0"), (1, 2 * y + 9, X, "01"),
                (0, 2, 8, "23"), (0, 10, 2 * y + 6, "1"),
                (0, 2 * y + 8, 2 * y + 8, "123"), (0, 2 * y + 10, X, "0")]
    out = [(1, 1, 7, "01"), (1, 9, 2 * y + 7, "0"), (1, 2 * y + 9, 2 * y + 9, "01"),
           (1, 2 * y + 11, X, "1"),
           (0, 2, 8, "23"), (0, 10, 2 * y + 6, "1"), (0, 2 * y + 8, 2 * y + 8, "123")]
    if d == 10:
        out.append((0, 2 * y + 10, 2 * y + 18, "02"))
        if 2 * y + 20 <= X:
            out.append((0, 2 * y + 20, X, "0"))
    else:
        out.append((0, 2 * y + 10, 2 * y + 10, "02"))
        if 2 * y + 12 <= X:
            out.append((0, 2 * y + 12, X, "0"))
    return out


def z8_y9(x, R):
    """K0999 published closed form (parallel lane): H(R;(x,9);8), all x>=9, R>=0."""
    if R == 0:
        return 0
    t = R in (1, 3, 5, 7)
    if x == 11:
        t = t or R == 23
    elif x == 15:
        t = t or R == 25
    elif x == 18:
        t = t or odd(R, 27, 35)
    elif x >= 19:
        t = t or R == 27

    if x == 9:
        p = odd(R, 9, 21)
    elif x == 10:
        p = odd(R, 9, 27) or even(R, 24, 26) or at_least(R, 28)
    elif x == 11:
        p = odd(R, 9, 21)
    elif x == 12:
        p = odd(R, 9, 29) or R == 24 or even(R, 26, 28) or at_least(R, 30)
    elif x == 13:
        p = odd(R, 9, 23)
    elif x == 14:
        p = odd(R, 9, 31) or even(R, 26, 30) or at_least(R, 32)
    elif x == 15:
        p = odd(R, 9, 23)
    elif x == 16:
        p = odd(R, 9, 33) or R == 26 or even(R, 28, 32) or at_least(R, 34)
    elif x == 17:
        p = odd(R, 9, 25)
    else:
        p = odd(R, 9, 25) or even(R, 28, x + 17) or (x % 2 == 0 and at_least(R, x + 18))
    return 2 if t else 1 if p else 0


# ---------------------------------------------------------------- engines
def z8_y7(x, r):
    """K0995 published closed form: H(R;(x,7);8), all x>=7, R>=0 (corroboration anchor)."""
    if r == 0:
        return 0
    t = (r in (1, 3, 5, 7) or (x == 9 and r == 19) or
         (x == 13 and r == 21) or
         (x == 16 and odd(r, 23, 31)) or
         (x >= 17 and r == 23))
    if x in (7, 9):
        p = odd(r, 9, 17)
    elif x in (8, 10):
        p = odd(r, 9, 17) or at_least(r, 19)
    elif x in (11, 13):
        p = odd(r, 9, 19)
    elif x in (12, 14):
        p = odd(r, 9, 19) or at_least(r, 21)
    elif x == 15:
        p = odd(r, 9, 21)
    elif x == 16:
        p = odd(r, 9, 21) or even(r, 24, 32) or at_least(r, 33)
    elif x % 2:
        p = odd(r, 9, 21) or even(r, 24, x + 15)
    else:
        p = odd(r, 9, 21) or even(r, 24, x + 14) or at_least(r, x + 16)
    return 2 if t else 1 if p else 0


def make_engines():
    @lru_cache(None)
    def ordered(r, tokens, z):
        if r == 0:
            return 0
        opts = set()
        for i, v in enumerate(tokens):
            if v > 1:
                opts.add(ordered(r - 1, tokens[:i] + (v - 1,) + tokens[i + 1:], z))
            else:
                opts.add(ordered(r - 1, tokens[:i] + tokens[i + 1:], z + 1))
        if z:
            opts.add(1 ^ ordered(r - 1, tokens, z - 1))
        return mex(opts)

    @lru_cache(None)
    def canonical(r, tokens, z):
        if r == 0:
            return 0
        opts = set()
        seen = set()
        for i, v in enumerate(tokens):
            if v in seen:
                continue
            seen.add(v)
            if v > 1:
                child = tuple(sorted(tokens[:i] + (v - 1,) + tokens[i + 1:], reverse=True))
                opts.add(canonical(r - 1, child, z))
            else:
                child = tuple(sorted(tokens[:i] + tokens[i + 1:], reverse=True))
                opts.add(canonical(r - 1, child, z + 1))
        if z:
            opts.add(1 ^ canonical(r - 1, tokens, z - 1))
        return mex(opts)

    return ordered, canonical


def reconstruct(x, y, r):
    """Child-value set of position (x,y,z=8) at heap R>=1 reconstructed from anchors:
    A = row y, x-1 (induction on x; at d=0 the A child coincides with the B child),
    B = row y-1 at the same x (K0996 when y=9, candidate by y-induction when y>=10),
    C = 1 XOR (z=7,y>=4 uniform formula of K0976)."""
    d = x - y
    cr = r - 1
    b = z8_y8(x, cr) if y == 9 else candidate(x, y - 1, cr)
    c = 1 ^ z7_ge4(x, y, cr)
    if d == 0:
        vals = {b, c}
    else:
        vals = {candidate(x - 1, y, cr), b, c}
    return "".join(map(str, sorted(vals)))


def audit_once():
    failures = []
    ordered, canonical = make_engines()
    direct = 0
    # 1) two independent direct engines vs candidate, moderate grid
    for y in list(range(9, 13)) + [15, 20]:
        dmax = 15 if y <= 12 else 8
        for d in range(0, dmax + 1):
            x = y + d
            for r in range(0, x + y + 11):
                exp = candidate(x, y, r)
                a = ordered(r, (x, y), 8)
                b = canonical(r, (x, y), 8)
                direct += 2
                if a != exp or b != exp:
                    failures.append(("target", x, y, r, a, b, exp))
    # 2) published anchors vs direct engines (K0996 row y=8, K0976 rows y>=9)
    anchor = 0
    for x in range(8, 41):
        for r in range(0, x + 41):
            a = ordered(r, (x, 8), 8)
            b = canonical(r, (x, 8), 8)
            anchor += 2
            if a != z8_y8(x, r) or b != z8_y8(x, r):
                failures.append(("B-anchor-K0996", x, r))
    for y in range(9, 13):
        for d in range(0, 16):
            x = y + d
            for r in range(0, x + y + 9):
                a = ordered(r, (x, y), 7)
                b = canonical(r, (x, y), 7)
                anchor += 2
                if a != z7_ge4(x, y, r) or b != z7_ge4(x, y, r):
                    failures.append(("C-anchor-K0976", x, y, r))
    # 3) uniform formula reproduces the published K0996 (y=8) and K0995 (y=7) slices exactly
    repro = 0
    for x in range(8, 301):
        for r in range(0, x + 35):
            repro += 1
            if candidate(x, 8, r) != z8_y8(x, r):
                failures.append(("y8-reproduction", x, r))
    y7repro = 0
    for x in range(7, 301):
        for r in range(0, x + 31):
            y7repro += 1
            if candidate(x, 7, r) != z8_y7(x, r):
                failures.append(("y7-reproduction", x, r))
    y9repro = 0
    for x in range(9, 301):
        for r in range(0, x + 36):
            y9repro += 1
            if candidate(x, 9, r) != z8_y9(x, r):
                failures.append(("y9-reproduction-K0999", x, r))
    # 3b) finite engine corroboration that the same formula already covers y=5,6
    smally = 0
    for y in (5, 6):
        for x in range(y, 31):
            for r in range(0, x + y + 11):
                smally += 1
                a = ordered(r, (x, y), 8)
                b = canonical(r, (x, y), 8)
                if a != candidate(x, y, r) or b != candidate(x, y, r):
                    failures.append(("small-y-engine", x, y, r, a, b, candidate(x, y, r)))
    # 4) induction reconstruction: band coverage, signature identity, mex, Theorem T
    sig = mexn = oddn = evenn = 0

    def band_pass(y, d):
        nonlocal sig, mexn, oddn, evenn
        x = y + d
        X = x + y + 8
        bd = bands_for(y, d, X)
        for r in range(1, X + 1):
            sig += 1
            hits = [s for p, lo, hi, s in bd if r % 2 == p and lo <= r <= hi]
            if len(hits) != 1:
                failures.append(("coverage", x, y, r, hits))
                continue
            actual = reconstruct(x, y, r)
            if actual != hits[0]:
                failures.append(("signature", x, y, r, hits[0], actual))
            v = mex(set(int(ch) for ch in hits[0]))
            mexn += 1
            if v != candidate(x, y, r):
                failures.append(("mex", x, y, r, v, candidate(x, y, r)))
            if r % 2:
                oddn += 1
                if v > 2:
                    failures.append(("odd-bound", x, y, r, v))
            else:
                evenn += 1
                if v > 1:
                    failures.append(("even-bound", x, y, r, v))

    for y in range(9, 151):
        for d in range(0, 51):
            band_pass(y, d)
    for y in range(9, 41):
        for d in range(51, 201):
            band_pass(y, d)
    for y in (200, 500, 1000):
        for d in range(0, 51):
            band_pass(y, d)
    # 5) tail formula and single-value tail signature
    tail = tailsig = 0
    for y in range(9, 220):
        for d in range(0, 41):
            x = y + d
            for off in range(4):
                r = x + y + 9 + off
                tail += 1
                if candidate(x, y, r) != (x + y) % 2:
                    failures.append(("tail", x, y, r, candidate(x, y, r), (x + y) % 2))
    for y in range(9, 151):
        for d in range(0, 51):
            x = y + d
            expected = str((x + y + 1) % 2)
            for off in range(4):
                r = x + y + 9 + off
                tailsig += 1
                if reconstruct(x, y, r) != expected:
                    failures.append(("tail-signature", x, y, r, reconstruct(x, y, r), expected))
    # 6) direct-engine tails beyond the band region for small y
    engtail = 0
    for y in range(9, 12):
        for d in range(0, 16):
            x = y + d
            for off in range(4):
                r = x + y + 9 + off
                engtail += 1
                a = ordered(r, (x, y), 8)
                b = canonical(r, (x, y), 8)
                if a != (x + y) % 2 or b != (x + y) % 2:
                    failures.append(("engine-tail", x, y, r, a, b))
    counts = {"direct_formula_two_engines": direct,
              "independent_anchor_direct": anchor,
              "y8_slice_reproduction": repro,
              "y7_slice_reproduction": y7repro,
              "y9_slice_reproduction_K0999": y9repro,
              "small_y_engine_corroboration": smally,
              "signature_coverage_and_identity": sig,
              "mex_identity": mexn,
              "odd_parent_bound": oddn,
              "even_parent_bound": evenn,
              "tail_formula": tail,
              "tail_signature": tailsig,
              "engine_tail": engtail}
    return {"all_pass": not failures,
            "classification": ("universal proof by strong induction on y with an outer induction on x, "
                                "explicit parametric A/B/C signature bands in (y,d), K0996, K0976, "
                                "K0832 Theorem T and the general tail; finite checks are independent audits only"),
            "counts": counts, "failures": failures,
            "scope": {"direct_y": [9, 12, 15, 20], "direct_R": "0 <= R <= x+y+10",
              "anchor_K0996_x": [8, 40], "anchor_K0976_y": [9, 12],
              "y8_reproduction_x": [8, 300], "y7_reproduction_x": [7, 300],
              "y9_reproduction_K0999_x": [9, 300],
              "small_y_engine": "y in (5,6), y<=x<=30, R <= x+y+10",
              "bands_y": "all y in 9..150 plus 9..40 deep-d, samples at 200,500,1000",
              "bands_d": [0, 200],
              "signature_R": "1 <= R <= x+y+8",
              "tail_y": [9, 219], "tail_signature_y": [9, 150]},
            "target": "H(R;(x,y);8), all x>=y>=9, R>=0",
            "total_checks": sum(counts.values())}


def run():
    first = audit_once()
    second = audit_once()
    same = (json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":")) ==
            json.dumps(second, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    base = dict(first, repeat_runs=2, repeat_byte_identical=same)
    raw = json.dumps(base, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    result = dict(base, sha256_without_hash_field=hashlib.sha256(raw).hexdigest())
    out = Path(__file__).with_name("output")
    out.mkdir(exist_ok=True)
    (out / "audit.json").write_text(json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"all_pass": result["all_pass"], "counts": result["counts"],
                      "failures": len(result["failures"]), "repeat_byte_identical": same,
                      "sha256_without_hash_field": result["sha256_without_hash_field"],
                      "total_checks": result["total_checks"]}, sort_keys=True))
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
