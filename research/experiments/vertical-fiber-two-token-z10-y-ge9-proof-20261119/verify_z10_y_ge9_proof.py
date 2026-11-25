#!/usr/bin/env python3
"""Independent audit for the uniform z=10, y>=9 two-token full Grundy classification (K1011).

Theorem under audit (proved by strong induction on y with an outer induction on x;
the candidate formula is the K1002 uniform formula restricted to y>=9):
  For every x>=y>=9 and R>=0, H(R;(x,y);10) takes values in {0,1,2} with
  value 2 locus T(x,y), value 1 locus P(x,y) as in the K1002 closed form, and
  tail H(R;(x,y);10) = (x+y) mod 2 for R >= x+y+11.

Children of (x,y;z=10) at heap R>=1:
  A = H(R-1;(x-1,y);10)  (x-induction within the row; merges with B at d=0)
  B = H(R-1;(x,y-1);10)  (base row y=9: published K1010 y=8 slice; y>=10: y-induction)
  C = 1 xor H(R-1;(x,y);9)  (published K1001 uniform z=9, y>=9 formula)

Anchors re-audited here against direct engines and dual transcriptions:
K1010 (z=10,y=8, both the d-parametric report form and the published
piecewise verifier form), K1001 (z=9,y>=9 uniform), and the census
transcription of the K1002 candidate (y>=6).
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


# ------------------------------------------------- anchor: K1001 (z=9, y>=9 uniform)
def z9_cand(x, y, r):
    """K1001 published uniform closed form: H(R;(x,y);9), all x>=y>=9, R>=0."""
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


# ------------------------------------------------- anchor: K1010 (z=10, y=8), d-form
def z10_y8(x, r):
    """K1010 published closed form (report theorem, d=x-8 form): H(R;(x,8);10)."""
    if r == 0:
        return 0
    S = x + 8
    d = x - 8
    t = r in (1, 3, 5, 7, 9)
    if not t:
        if d in (0, 4, 8) and r == 21 + d // 2:
            t = True
        elif d == 11 and odd(r, 27, S + 10):
            t = True
        elif d >= 12 and r == 27:
            t = True
    if t:
        return 2
    if d % 2 == 0 and d <= 10:
        p = odd(r, 11, 19 + 2 * ((d + 3) // 4))
    elif d % 2 == 0:
        p = odd(r, 11, 25) or even(r, 28, S + 10)
    elif d <= 9:
        p = odd(r, 11, S + 10) or even(r, 22 + 2 * ((d + 1) // 4), S + 9)
    else:
        p = odd(r, 11, 25) or even(r, 28, S + 9)
    if p:
        return 1
    if r >= S + 11:
        return S % 2
    return 0


def k1010_piecewise(x, r):
    """K1010 published verifier transcription (piecewise in x): H(R;(x,8);10)."""
    if r == 0:
        return 0
    S = x + 8
    if r >= S + 11:
        return S % 2
    t = r in (1, 3, 5, 7, 9)
    if x == 8:
        t = t or r == 21
    elif x == 12:
        t = t or r == 23
    elif x == 16:
        t = t or r == 25
    elif x == 19:
        t = t or odd(r, 27, 37)
    elif x >= 20:
        t = t or r == 27
    if x == 8:
        p = odd(r, 11, 19)
    elif x == 9:
        p = odd(r, 11, 27) or even(r, 22, 26)
    elif x == 10:
        p = odd(r, 11, 21)
    elif x == 11:
        p = odd(r, 11, 29) or even(r, 24, 28)
    elif x == 12:
        p = odd(r, 11, 21)
    elif x == 13:
        p = odd(r, 11, 31) or even(r, 24, 30)
    elif x == 14:
        p = odd(r, 11, 23)
    elif x == 15:
        p = odd(r, 11, 33) or even(r, 26, 32)
    elif x == 16:
        p = odd(r, 11, 23)
    elif x == 17:
        p = odd(r, 11, 35) or even(r, 26, 34)
    elif x == 18:
        p = odd(r, 11, 25)
    elif x == 19:
        p = odd(r, 11, 25) or even(r, 28, 36)
    elif x == 20:
        p = odd(r, 11, 25) or even(r, 28, 38)
    elif x % 2 == 0:
        p = odd(r, 11, 25) or even(r, 28, S + 10)
    else:
        p = odd(r, 11, 25) or even(r, 28, S + 9)
    return 2 if t else 1 if p else 0


# ------------------------------------- candidate: K1002 uniform formula (z=10, y>=6)
def candidate(x, y, r):
    """K1002 uniform closed form: H(R;(x,y);10) for all x>=y>=6 (here used y>=9)."""
    if r == 0:
        return 0
    S = x + y
    if r >= S + 11:
        return S % 2
    d = x - y
    t = (r in (1, 3, 5, 7, 9) or
         (d in (0, 4, 8) and r == 2 * y + 5 + d // 2) or
         (d == 11 and odd(r, 2 * y + 11, S + 10)) or
         (d >= 12 and r == 2 * y + 11))
    if t:
        return 2
    if d % 2 == 0 and d <= 10:
        p = odd(r, 11, 2 * y + 3 + 2 * ((d + 3) // 4))
    elif d % 2 == 0:
        p = odd(r, 11, 2 * y + 9) or even(r, 2 * y + 12, S + 10)
    elif d <= 9:
        p = odd(r, 11, S + 10) or even(r, 2 * y + 6 + 2 * ((d + 1) // 4), S + 9)
    else:
        p = odd(r, 11, 2 * y + 9) or even(r, 2 * y + 12, S + 9)
    return 1 if p else 0


def k1002_census(x, y, r):
    """Census experiment transcription of the K1002 candidate (y>=6), verbatim logic."""
    d = x - y
    S = x + y
    tail = S + 11
    if r == 0:
        return 0
    if r >= tail:
        return S % 2
    in_t = r in (1, 3, 5, 7, 9)
    if d in (0, 4, 8):
        in_t = in_t or r == 2 * y + 5 + d // 2
    elif d == 11:
        in_t = in_t or odd(r, 2 * y + 11, S + 10)
    elif d >= 12:
        in_t = in_t or r == 2 * y + 11
    if in_t:
        return 2
    if d % 2 == 0:
        if d <= 10:
            upper = 2 * y + 3 + 2 * ((d + 3) // 4)
            in_p = odd(r, 11, upper)
        else:
            in_p = odd(r, 11, 2 * y + 9) or even(r, 2 * y + 12, S + 10)
    elif d <= 9:
        lower = 2 * y + 6 + 2 * ((d + 1) // 4)
        in_p = odd(r, 11, S + 10) or even(r, lower, S + 9)
    else:
        in_p = odd(r, 11, 2 * y + 9) or even(r, 2 * y + 12, S + 9)
    return 1 if in_p else 0


# ------------------------------------------------------------ signature bands
def bands_for(y, d, X):
    """Parametric A/B/C signature bands covering 1<=R<=X with X=x+y+10, d=x-y>=0, y>=9.

    Entries are (parity, lo, hi, sig) with parity 1=odd, 0=even; O/E run in
    steps of 2 inside [lo, hi]."""
    oh = [(1, 1, 9, "01")]
    eh = [(0, 2, 10, "23")]
    if d == 0:
        return oh + [(1, 11, 2 * y + 3, "0"), (1, 2 * y + 5, 2 * y + 5, "01"),
                     (1, 2 * y + 7, X, "1")] + eh + [(0, 12, X, "1")]
    if d == 1:
        return oh + [(1, 11, X, "0")] + eh + \
            [(0, 12, 2 * y + 4, "1"), (0, 2 * y + 6, 2 * y + 6, "023"), (0, 2 * y + 8, X, "0")]
    if d == 2:
        return oh + [(1, 11, 2 * y + 5, "0"), (1, 2 * y + 7, X, "1")] + eh + [(0, 12, X, "1")]
    if d == 3:
        return oh + [(1, 11, X, "0")] + eh + \
            [(0, 12, 2 * y + 4, "1"), (0, 2 * y + 6, 2 * y + 6, "12"), (0, 2 * y + 8, X, "0")]
    if d == 4:
        return oh + [(1, 11, 2 * y + 5, "0"), (1, 2 * y + 7, 2 * y + 7, "01"),
                     (1, 2 * y + 9, X, "1")] + eh + [(0, 12, X, "1")]
    if d == 5:
        return oh + [(1, 11, X, "0")] + eh + \
            [(0, 12, 2 * y + 6, "1"), (0, 2 * y + 8, 2 * y + 8, "023"), (0, 2 * y + 10, X, "0")]
    if d == 6:
        return oh + [(1, 11, 2 * y + 7, "0"), (1, 2 * y + 9, X, "1")] + eh + [(0, 12, X, "1")]
    if d == 7:
        return oh + [(1, 11, X, "0")] + eh + \
            [(0, 12, 2 * y + 6, "1"), (0, 2 * y + 8, 2 * y + 8, "12"), (0, 2 * y + 10, X, "0")]
    if d == 8:
        return oh + [(1, 11, 2 * y + 7, "0"), (1, 2 * y + 9, 2 * y + 9, "01"),
                     (1, 2 * y + 11, X, "1")] + eh + [(0, 12, X, "1")]
    if d == 9:
        return oh + [(1, 11, X, "0")] + eh + \
            [(0, 12, 2 * y + 8, "1"), (0, 2 * y + 10, 2 * y + 10, "023"), (0, 2 * y + 12, X, "0")]
    if d == 10:
        return oh + [(1, 11, 2 * y + 9, "0"), (1, 2 * y + 11, X, "1")] + eh + \
            [(0, 12, 2 * y + 8, "1"), (0, 2 * y + 10, X, "123")]
    if d == 11:
        return oh + [(1, 11, 2 * y + 9, "0"), (1, 2 * y + 11, X, "01")] + eh + \
            [(0, 12, 2 * y + 8, "1"), (0, 2 * y + 10, 2 * y + 10, "123"), (0, 2 * y + 12, X, "0")]
    if d == 12:
        return oh + [(1, 11, 2 * y + 9, "0"), (1, 2 * y + 11, 2 * y + 11, "01"),
                     (1, 2 * y + 13, X, "1")] + eh + \
            [(0, 12, 2 * y + 8, "1"), (0, 2 * y + 10, 2 * y + 10, "123"), (0, 2 * y + 12, X, "02")]
    return oh + [(1, 11, 2 * y + 9, "0"), (1, 2 * y + 11, 2 * y + 11, "01"),
                 (1, 2 * y + 13, X, "1")] + eh + \
        [(0, 12, 2 * y + 8, "1"), (0, 2 * y + 10, 2 * y + 10, "123"),
         (0, 2 * y + 12, 2 * y + 12, "02"), (0, 2 * y + 14, X, "0")]


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
    """Child-value set of position (x,y;z=10) at heap R>=1 reconstructed from
    anchors/induction hypotheses: A = row y, x-1 (coincides with B at d=0),
    B = row y-1 (K1010 when y=9, candidate by y-induction when y>=10),
    C = 1 XOR (K1001 z=9,y>=9 uniform formula)."""
    d = x - y
    cr = r - 1
    b = z10_y8(x, cr) if y == 9 else candidate(x, y - 1, cr)
    c = 1 ^ z9_cand(x, y, cr)
    if d == 0:
        vals = {b, c}
    else:
        vals = {candidate(x - 1, y, cr), b, c}
    return "".join(map(str, sorted(vals)))


def audit_once():
    failures = []
    ordered, canonical = make_engines()
    # 1) two independent direct engines vs candidate, moderate grid
    direct = 0
    for y in list(range(9, 13)) + [15, 20]:
        dmax = 15 if y <= 12 else 8
        for d in range(0, dmax + 1):
            x = y + d
            for r in range(0, x + y + 12):
                exp = candidate(x, y, r)
                a = ordered(r, (x, y), 10)
                b = canonical(r, (x, y), 10)
                direct += 2
                if a != exp or b != exp:
                    failures.append(("target", x, y, r, a, b, exp))
    # 2) published anchors vs direct engines (K1010 row y=8, K1001 rows y>=9)
    anchor = 0
    for x in range(8, 41):
        for r in range(0, x + 41):
            a = ordered(r, (x, 8), 10)
            b = canonical(r, (x, 8), 10)
            anchor += 2
            if a != z10_y8(x, r) or b != z10_y8(x, r):
                failures.append(("B-anchor-K1010", x, r))
    for y in range(9, 13):
        for d in range(0, 16):
            x = y + d
            for r in range(0, x + y + 11):
                a = ordered(r, (x, y), 9)
                b = canonical(r, (x, y), 9)
                anchor += 2
                if a != z9_cand(x, y, r) or b != z9_cand(x, y, r):
                    failures.append(("C-anchor-K1001", x, y, r))
    # 3) dual transcriptions: K1010 d-form vs published piecewise form;
    #    candidate (used at y>=9) vs census transcription of the K1002 candidate (y>=6)
    dual = 0
    for x in range(8, 301):
        for r in range(0, x + 41):
            dual += 1
            if z10_y8(x, r) != k1010_piecewise(x, r):
                failures.append(("K1010-dual-transcription", x, r))
    census = 0
    for y in range(6, 21):
        for d in range(0, 51):
            x = y + d
            for r in range(0, x + y + 20):
                census += 1
                if candidate(x, y, r) != k1002_census(x, y, r):
                    failures.append(("K1002-census-identity", x, y, r))
    # 4) finite bridging: uniform formula extrapolates to the published y=8 row,
    #    and matches direct engines on the boundary rows y=6,7,8 (proved slices)
    y8agree = 0
    for x in range(8, 301):
        for r in range(0, x + 36):
            if candidate(x, 8, r) == z10_y8(x, r):
                y8agree += 1
            else:
                failures.append(("y8-reproduction-K1010", x, r))
    smally = 0
    for y in (6, 7, 8):
        for x in range(y, 31):
            for r in range(0, x + y + 12):
                smally += 1
                a = ordered(r, (x, y), 10)
                b = canonical(r, (x, y), 10)
                if a != candidate(x, y, r) or b != candidate(x, y, r):
                    failures.append(("boundary-y-slice-engine", x, y, r, a, b, candidate(x, y, r)))
    # 5) induction reconstruction: band coverage, signature identity, mex, Theorem T
    sig = mexn = oddn = evenn = 0

    def band_pass(y, d):
        nonlocal sig, mexn, oddn, evenn
        x = y + d
        X = x + y + 10
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
    # 6) tail formula and tail signature
    tail = tailsig = 0
    for y in range(9, 220):
        for d in range(0, 41):
            x = y + d
            for off in range(4):
                r = x + y + 11 + off
                tail += 1
                if candidate(x, y, r) != (x + y) % 2:
                    failures.append(("tail", x, y, r, candidate(x, y, r), (x + y) % 2))
    for y in range(9, 151):
        for d in range(0, 51):
            x = y + d
            expected = str((x + y + 1) % 2)
            for off in range(4):
                r = x + y + 11 + off
                tailsig += 1
                got = reconstruct(x, y, r)
                if got != expected:
                    failures.append(("tail-signature", x, y, r, got, expected))
    # 7) direct-engine tails beyond the band region for small y
    engtail = 0
    for y in range(9, 12):
        for d in range(0, 16):
            x = y + d
            for off in range(4):
                r = x + y + 11 + off
                engtail += 1
                a = ordered(r, (x, y), 10)
                b = canonical(r, (x, y), 10)
                if a != (x + y) % 2 or b != (x + y) % 2:
                    failures.append(("engine-tail", x, y, r, a, b))
    counts = {"direct_formula_two_engines": direct,
              "independent_anchor_direct": anchor,
              "k1010_dual_transcription": dual,
              "k1002_census_identity": census,
              "y8_slice_reproduction": y8agree,
              "boundary_slice_engine_corroboration": smally,
              "signature_coverage_and_identity": sig,
              "mex_identity": mexn,
              "odd_parent_bound": oddn,
              "even_parent_bound": evenn,
              "tail_formula": tail,
              "tail_signature": tailsig,
              "engine_tail": engtail}
    return {"all_pass": not failures,
            "classification": ("universal proof by strong induction on y with an outer induction on x, "
                                "explicit parametric A/B/C signature bands in (y,d), K1010, K1001, "
                                "K0832 Theorem T and the general tail; finite checks are independent audits only"),
            "counts": counts, "failures": failures,
            "scope": {"direct_y": [9, 12, 15, 20], "direct_R": "0 <= R <= x+y+11",
                      "anchor_K1010_x": [8, 40], "anchor_K1001_y": [9, 12],
                      "k1010_dual_x": [8, 300], "k1002_census_y": [6, 20], "k1002_census_d": [0, 50],
                      "y8_reproduction_x": [8, 300], "y8_reproduction_R": "0 <= R <= x+35",
                      "boundary_slice_engine": "y in (6,7,8), y<=x<=30, R <= x+y+11",
                      "bands_y": "all y in 9..150 plus 9..40 deep-d, samples at 200,500,1000",
                      "bands_d": [0, 200],
                      "signature_R": "1 <= R <= x+y+10",
                      "tail_y": [9, 219], "tail_signature_y": [9, 150]},
            "target": "H(R;(x,y);10), all x>=y>=9, R>=0 (K1002 formula restricted to y>=9)",
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
