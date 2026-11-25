#!/usr/bin/env python3
"""Independent audit for the uniform z=9, y>=9 two-token full Grundy classification (K1001).

Theorem under audit (proved by strong induction on y with an outer induction on x,
this file is the finite independent audit):
  For every x>=y>=9 and R>=0, H(R;(x,y);9) in {0,1,2} with
  value 2 positions T(x,y), value 1 positions P(x,y), and tail H=(x+y) mod 2 for R>=x+y+10.

Anchors: K0998 (z=9,y=8 full slice, used as the B child of the y=9 row and re-audited
here against direct engines), K1000 (z=8,y>=9 uniform formula, used as every C child
and re-audited here against direct engines), K0832 (recursion, Theorem T, general tail).
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


# ---------------------------------------------------------------- anchor: K1000
def z8_cand(x, y, r):
    """K1000 published uniform closed form: H(R;(x,y);8), all x>=y>=9, R>=0."""
    if r == 0:
        return 0
    if r >= x + y + 9:
        return (x + y) % 2
    d = x - y
    t = (r in (1, 3, 5, 7) or (d == 2 and r == 2 * y + 5) or (d == 6 and r == 2 * y + 7)
         or (d == 9 and odd(r, 2 * y + 9, 2 * y + 17)) or (d >= 10 and r == 2 * y + 9))
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


# ---------------------------------------------------------------- anchor: K0998
def z9_y8(x, r):
    """K0998 published closed form: H(R;(x,8);9), all x>=8, R>=0."""
    if r == 0:
        return 0
    t = (r in (1, 3, 5, 7, 9) or (x == 9 and r == 21) or (x == 13 and r == 23)
         or (x == 17 and r == 25)
         or (x == 18 and odd(r, 25, 35)) or (x >= 19 and r == 25))
    if x in (8, 10):
        p = even(r, 10, 20)
    elif x in (12, 14):
        p = even(r, 10, 22)
    elif x in (16, 18):
        p = even(r, 10, 24)
    elif x == 9:
        p = even(r, 10, 26) or odd(r, 23, 25) or r >= 27
    elif x == 11:
        p = even(r, 10, 28) or odd(r, 23, 27) or r >= 29
    elif x == 13:
        p = even(r, 10, 30) or odd(r, 25, 29) or r >= 31
    elif x == 15:
        p = even(r, 10, 32) or odd(r, 25, 31) or r >= 33
    elif x == 17:
        p = even(r, 10, 34) or odd(r, 27, 33) or r >= 35
    elif x >= 19 and x % 2 == 1:
        p = even(r, 10, 24) or odd(r, 27, x + 16) or r >= x + 18
    else:
        p = even(r, 10, 24) or odd(r, 27, x + 17)
    return 2 if t else 1 if p else (0 if r < x + 18 else (x + 8) % 2)


# ---------------------------------------------------------- uniform candidate
def candidate(x, y, r):
    """Uniform closed form: H(R;(x,y);9) for all x>=y>=9, R>=0."""
    if r == 0:
        return 0
    if r >= x + y + 10:
        return (x + y) % 2
    d = x - y
    top = x + y + 9
    t = (r in (1, 3, 5, 7, 9) or
         (d == 1 and r == 2 * y + 5) or
         (d == 5 and r == 2 * y + 7) or
         (d == 9 and r == 2 * y + 9) or
         (d == 10 and odd(r, 2 * y + 9, 2 * y + 19)) or
         (d >= 11 and r == 2 * y + 9))
    if t:
        return 2
    if d == 10:
        p = even(r, 10, 2 * y + 8)
    elif d % 2 == 1:
        if d <= 3:
            p = even(r, 10, 2 * y + 6) or r >= 2 * y + 7
        elif d <= 7:
            p = even(r, 10, 2 * y + 8) or r >= 2 * y + 9
        elif d == 9:
            p = even(r, 10, 2 * y + 8) or r >= 2 * y + 10
        else:
            p = even(r, 10, 2 * y + 8) or (odd(r, 2 * y + 11, top))
    else:
        if d <= 2:
            ht = 2 * y + 4
        elif d <= 6:
            ht = 2 * y + 6
        else:
            ht = 2 * y + 8
        if d >= 12:
            p = even(r, 10, ht) or odd(r, 2 * y + 11, top)
        else:
            p = even(r, 10, ht)
    return 1 if p else 0


# ------------------------------------------------------------ signature bands
def bands_for(y, d, X):
    """Parametric A/B/C signature bands covering 1<=R<=X with X=x+y+9, d=x-y>=0, y>=9."""
    odd_head = [(1, 1, 9, "01")]
    even_head = [(0, 2, 8, "23"), (0, 10, 10, "02")]
    if d == 0:
        return odd_head + [(1, 11, X, "1")] + even_head + \
            [(0, 12, 2 * y + 2, "0"), (0, 2 * y + 4, 2 * y + 4, "02"), (0, 2 * y + 6, X, "1")]
    if d == 1:
        return odd_head + [(1, 11, 2 * y + 3, "1"), (1, 2 * y + 5, 2 * y + 5, "01"),
                           (1, 2 * y + 7, X, "0")] + even_head + [(0, 12, X, "0")]
    if d == 2:
        return odd_head + [(1, 11, X, "1")] + even_head + \
            [(0, 12, 2 * y + 4, "0"), (0, 2 * y + 6, 2 * y + 6, "123"), (0, 2 * y + 8, X, "1")]
    if d == 3:
        return odd_head + [(1, 11, 2 * y + 5, "1"), (1, 2 * y + 7, X, "0")] + \
            even_head + [(0, 12, X, "0")]
    if d == 4:
        return odd_head + [(1, 11, X, "1")] + even_head + \
            [(0, 12, 2 * y + 4, "0"), (0, 2 * y + 6, 2 * y + 6, "02"), (0, 2 * y + 8, X, "1")]
    if d == 5:
        return odd_head + [(1, 11, 2 * y + 5, "1"), (1, 2 * y + 7, 2 * y + 7, "01"),
                           (1, 2 * y + 9, X, "0")] + even_head + [(0, 12, X, "0")]
    if d == 6:
        return odd_head + [(1, 11, X, "1")] + even_head + \
            [(0, 12, 2 * y + 6, "0"), (0, 2 * y + 8, 2 * y + 8, "123"), (0, 2 * y + 10, X, "1")]
    if d == 7:
        return odd_head + [(1, 11, 2 * y + 7, "1"), (1, 2 * y + 9, X, "0")] + \
            even_head + [(0, 12, X, "0")]
    if d == 8:
        return odd_head + [(1, 11, X, "1")] + even_head + \
            [(0, 12, 2 * y + 6, "0"), (0, 2 * y + 8, 2 * y + 8, "02"), (0, 2 * y + 10, X, "1")]
    if d == 9:
        return odd_head + [(1, 11, 2 * y + 7, "1"), (1, 2 * y + 9, 2 * y + 9, "01"),
                           (1, 2 * y + 11, X, "0")] + even_head + \
            [(0, 12, 2 * y + 6, "0"), (0, 2 * y + 8, 2 * y + 8, "02"), (0, 2 * y + 10, X, "023")]
    if d == 10:
        return odd_head + [(1, 11, 2 * y + 7, "1"), (1, 2 * y + 9, X, "01")] + \
            even_head + [(0, 12, 2 * y + 6, "0"), (0, 2 * y + 8, 2 * y + 8, "02"),
                         (0, 2 * y + 10, 2 * y + 10, "123"), (0, 2 * y + 12, X, "1")]
    if d == 11:
        return odd_head + [(1, 11, 2 * y + 7, "1"), (1, 2 * y + 9, 2 * y + 9, "01"),
                           (1, 2 * y + 11, X, "0")] + even_head + \
            [(0, 12, 2 * y + 6, "0"), (0, 2 * y + 8, 2 * y + 8, "02"),
             (0, 2 * y + 10, 2 * y + 10, "123"), (0, 2 * y + 12, X, "12")]
    return odd_head + [(1, 11, 2 * y + 7, "1"), (1, 2 * y + 9, 2 * y + 9, "01"),
                       (1, 2 * y + 11, X, "0")] + even_head + \
        [(0, 12, 2 * y + 6, "0"), (0, 2 * y + 8, 2 * y + 8, "02"),
         (0, 2 * y + 10, 2 * y + 10, "123"), (0, 2 * y + 12, X, "1")]


# ---------------------------------------------------------------- engines
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
    """Child-value set of position (x,y,z=9) at heap R>=1 reconstructed from anchors:
    A = row y, x-1 (induction on x; at d=0 the A child coincides with the B child),
    B = row y-1 at the same x (K0998 when y=9, candidate by y-induction when y>=10),
    C = 1 XOR (z=8,y>=9 uniform formula of K1000)."""
    d = x - y
    cr = r - 1
    b = z9_y8(x, cr) if y == 9 else candidate(x, y - 1, cr)
    c = 1 ^ z8_cand(x, y, cr)
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
            for r in range(0, x + y + 12):
                exp = candidate(x, y, r)
                a = ordered(r, (x, y), 9)
                b = canonical(r, (x, y), 9)
                direct += 2
                if a != exp or b != exp:
                    failures.append(("target", x, y, r, a, b, exp))
    # 2) published anchors vs direct engines (K0998 row y=8, K1000 rows y>=9)
    anchor = 0
    for x in range(8, 41):
        for r in range(0, x + 41):
            a = ordered(r, (x, 8), 9)
            b = canonical(r, (x, 8), 9)
            anchor += 2
            if a != z9_y8(x, r) or b != z9_y8(x, r):
                failures.append(("B-anchor-K0998", x, r))
    for y in range(9, 13):
        for d in range(0, 16):
            x = y + d
            for r in range(0, x + y + 10):
                a = ordered(r, (x, y), 8)
                b = canonical(r, (x, y), 8)
                anchor += 2
                if a != z8_cand(x, y, r) or b != z8_cand(x, y, r):
                    failures.append(("C-anchor-K1000", x, y, r))
    # 3) finite censuses: the uniform formula reproduces the published K0998 y=8 row
    #    and matches direct engines on the y=5..8 boundary rows
    y8agree = y8bad = 0
    for x in range(8, 301):
        for r in range(0, x + 36):
            if candidate(x, 8, r) == z9_y8(x, r):
                y8agree += 1
            else:
                y8bad += 1
                failures.append(("y8-reproduction-K0998", x, r))
    smally = 0
    for y in (5, 6, 7, 8):
        for x in range(y, 31):
            for r in range(0, x + y + 11):
                smally += 1
                a = ordered(r, (x, y), 9)
                b = canonical(r, (x, y), 9)
                if a != candidate(x, y, r) or b != candidate(x, y, r):
                    failures.append(("small-y-engine", x, y, r, a, b, candidate(x, y, r)))
    # 4) induction reconstruction: band coverage, signature identity, mex, Theorem T
    sig = mexn = oddn = evenn = 0

    def band_pass(y, d):
        nonlocal sig, mexn, oddn, evenn
        x = y + d
        X = x + y + 9
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
                r = x + y + 10 + off
                tail += 1
                if candidate(x, y, r) != (x + y) % 2:
                    failures.append(("tail", x, y, r, candidate(x, y, r), (x + y) % 2))
    for y in range(9, 151):
        for d in range(0, 51):
            x = y + d
            expected = str((x + y + 1) % 2)
            for off in range(4):
                r = x + y + 10 + off
                tailsig += 1
                got = reconstruct(x, y, r)
                if got != expected:
                    failures.append(("tail-signature", x, y, r, got, expected))
    # 6) direct-engine tails beyond the band region for small y
    engtail = 0
    for y in range(9, 12):
        for d in range(0, 16):
            x = y + d
            for off in range(4):
                r = x + y + 10 + off
                engtail += 1
                a = ordered(r, (x, y), 9)
                b = canonical(r, (x, y), 9)
                if a != (x + y) % 2 or b != (x + y) % 2:
                    failures.append(("engine-tail", x, y, r, a, b))
    counts = {"direct_formula_two_engines": direct,
              "independent_anchor_direct": anchor,
              "y8_slice_reproduction": y8agree,
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
                               "explicit parametric A/B/C signature bands in (y,d), K0998, K1000, "
                               "K0832 Theorem T and the general tail; finite checks are independent audits only"),
            "counts": counts, "failures": failures,
            "scope": {"direct_y": [9, 12, 15, 20], "direct_R": "0 <= R <= x+y+11",
              "anchor_K0998_x": [8, 40], "anchor_K1000_y": [9, 12],
              "y8_reproduction_x": [8, 300], "y8_reproduction_R": "0 <= R <= x+35",
              "small_y_engine": "y in (5,6,7,8), y<=x<=30, R <= x+y+10",
              "bands_y": "all y in 9..150 plus 9..40 deep-d, samples at 200,500,1000",
              "bands_d": [0, 200],
              "signature_R": "1 <= R <= x+y+9",
              "tail_y": [9, 219], "tail_signature_y": [9, 150]},
            "target": "H(R;(x,y);9), all x>=y>=9, R>=0",
            "total_checks": sum(counts.values()) + 0}


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
