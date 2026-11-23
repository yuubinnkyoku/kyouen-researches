#!/usr/bin/env python3
"""verify_min3_banded_strip.py -- machine audit for the declared claims of
the single-owner declaration note (K1272 provisional; min>=3 banded window
extension to the critical strip z in {2,3,4}):

  Lemma U   : H(2;{1}+Y;0) = 0 for every nonempty Y with min(Y)>=2;
              H(2;{1};0) = 1.
  Lemma F   : F(s,z) := H(z+2;{1}+Y;z) is independent of the decomposition
              of s into 1..4 tokens >=3 (Y=() allowed for s=0), for
              z in {1,2,3,4}, s in {0} u {3,4,...}; table:
              F(s,1)=1/2 (s=0/s>=3), F(s,2)=1/0, F(s,3)=1/0/2 (s=3/s>=4),
              F(s,4)=1 (s=0) /0 (s=3) /1 (s=4) /0 (s>=5).
  Lemma R2  : H(z+3;{2}+Y;z) = v(s+2,z,z+3) for z in {0,1,2,3}
              (z in {0,1} = K1270; z in {2,3} is the new part).
  Lemma D   : D(s) := H(7;{2}+Y;4) obeys D(0)=0, D(3)=1, D(4)=2, D(s>=5)=1;
              collapse fails exactly at Y=(4,): D(4)=2 != v(6,4,7)=1.
  Theorem T-B: for ALL m>=3, z in {2,3,4}, nonempty X with min(X)=m:
              H(z+m+1;X;z) = v(sum X, z, z+m+1).
              Together with K1270 (z in {0,1}) this resolves the entire
              band z<z*(3)=5 for m=3 -- row m=3 of K1268 Conjecture C1.

Declared checks (PUBLISH-THEN-EXECUTE; note:
research/log/2026-11-23-min3-banded-strip-z2z4-single-owner-note.md,
commit 4be51cb6):
  D1  Lemma U sweep: Y = tokens 2..9 multisets, arity 1..4 (494) + {1}
      (495 points / 1,485 comparisons)
  D2  Lemma F: z in {1..4}, s in {0} u {3..40}, ALL decompositions into
      1..4 tokens >=3 (3,657 per z)  (14,628 / 43,884)
  D3  Lemma R2/D: Y = tokens 3..9, arity 0..4 (330 per z); z in {0..3}
      vs v(s+2,z,z+3), z=4 vs D(s); +1 arithmetic deviant-set comparison
      deviants == {(4,)}                        (1,650 / 4,951)
  D4  Theorem T-B grid: m in {3..8} x z in {2,3,4} x 222 shapes
      (1 single + 15 two-token d=0..14 + 81 three-token d<=8
       + 125 four-token d<=4)                    (3,996 / 11,988)
  D5  fixed-seed (20261234) random deep: m in {3..8} x z in {2,3,4} x 20
      shapes (arity 4..6, tokens in [m,m+15], one token fixed at m)
                                                (360 / 1,080)
  D6a published K1270/K1268 witness anchors (17) (17 / 85, 5 per point)
  D6b theorem anchors 23: R2(4) deviant (2,4); D cells (2,3)/(2,5)/(2,3,3);
      C(3,4) spots (3,4)/(3,3)/(3,3,3)@R=8; U cells (1,3)/(1); F-table 14
                                                (23 / 69)
  D7  proof-structure option-set inspection: m in {3..6} x z in {2,3,4} x
      33 shapes (2-token d=0..6, 3-token d in [0,4]^2, 5-token ramp).
      (m,z) != (3,4): child value set == {v(S-1,z,z+m), 1^v(S,z-1,z+m)}
      exact match. (3,4): opts subset of {A',c',D(S-3)} AND a=3 child
      == D(S-3). Parent mex == v both engines in both cases.
                                                (396 / 1,188)
  TOTAL declared: 21,565 points / 64,730 comparisons / bad 0.
  D6c census (NOT in declared totals, NOT gated on collapse): m in {4..7}
      x z=5 x 96 shapes (two-token d=0..14 + three-token d<=8);
      384 points / 768 comparisons; bad gate is engine disagreement only.
      The z>=5 strip for m>=4 stays OPEN (census records observations).

Fail-closed: any bad>0 -> rc=1; declared-count mismatch -> rc=1 (honest
record requirement). Finite machine audit is NOT the proof: the universal
claims rest on the paper proof in the declaration note (finite z-ladder
F/R2/D closed forms + option-set identity + induction on m). Standard
11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, classes
1/2/4 and class 5343 remain UNKNOWN at all times.
Determinism: no time, no unseeded randomness in the audit; value-
transparent engine cache clears between blocks and inside large blocks.
--tamper runs the 12-mutation battery B1-B12 (each MUST be caught).
"""
import sys, os, json, hashlib, random
from functools import lru_cache
from itertools import combinations_with_replacement

sys.setrecursionlimit(1_000_000)

# === ENGINE BLOCK (machine-extracted; see build_engine_from_published.py) ===
def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m

# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier block; the same
# transcription is embedded in the published y22 machine K1257).
# ------------------------------------------------------------------
@lru_cache(maxsize=6_000_000)
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

@lru_cache(maxsize=6_000_000)
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

def vC(x, z, R):  # canonical-engine single token
    return H_canonical(R, (x,), z)
def vO(x, z, R):  # ordered-engine single token
    return H_ordered(R, (x,), z)

# ------------------------------------------------------------------
# Published K0832 single-token closed form (transcription of the published
# single_token block in the y22 machine K1257; see report provenance).
# ------------------------------------------------------------------
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
# === END ENGINE BLOCK ===

SELF_SHA = hashlib.sha256(open(__file__, 'rb').read()).hexdigest()

def clear_engines():
    # value-transparent memo reset (bounds live cache entries only)
    H_ordered.cache_clear()
    H_canonical.cache_clear()

# ---------------------------------------------------------------
# declared closed forms (transcription of the declaration note tables)
# ---------------------------------------------------------------
def lemma_U_expected(Y):
    # H(2;{1}+Y;0): 0 for nonempty Y (tokens >=2), 1 for Y=()
    return 0 if len(Y) > 0 else 1

def F_table(s, z):
    # Lemma F closed form, z in {1,2,3,4}, s in {0} u {3,4,...}
    if z == 1:
        return 1 if s == 0 else 2
    if z == 2:
        return 1 if s == 0 else 0
    if z == 3:
        if s == 0:
            return 1
        if s == 3:
            return 0
        return 2
    if z == 4:
        if s == 0:
            return 1
        if s == 3:
            return 0
        if s == 4:
            return 1
        return 0
    raise ValueError((s, z))

def D_val(s):
    # Lemma D closed form (z=4 cell), s in {0} u {3,4,...}
    if s == 0:
        return 0
    if s == 3:
        return 1
    if s == 4:
        return 2
    return 1

# ---------------------------------------------------------------
# shape families (declared protocol)
# ---------------------------------------------------------------
def Y_tokens_lo():   # tokens 2..9, arity 1..4 (494 shapes)
    out = []
    for k in range(1, 5):
        out.extend(combinations_with_replacement(range(2, 10), k))
    return out

def Y_tokens_hi():   # tokens 3..9, arity 0..4 (330 shapes)
    out = []
    for k in range(0, 5):
        out.extend(combinations_with_replacement(range(3, 10), k))
    return out

def F_decompositions(s):
    # all multisets of 1..4 tokens >=3 summing to s; Y=() for s=0
    if s == 0:
        return [()]
    out = []
    for k in range(1, 5):
        for c in combinations_with_replacement(range(3, s + 1), k):
            if sum(c) == s:
                out.append(c)
    return out

def T_shapes(m):
    # 222 shapes per (m,z) for D4
    out = [(m,)]
    out.extend((m, m + d) for d in range(15))
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    out.extend((m, m + a, m + b, m + c)
               for a in range(5) for b in range(5) for c in range(5))
    return out

def D7_shapes(m):
    # 33 shapes per (m,z) for D7
    out = [(m, m + d) for d in range(7)]
    out.extend((m, m + a, m + b) for a in range(5) for b in range(5))
    out.append(tuple(m + i for i in range(5)))
    return out

def census_shapes(m):
    # 96 shapes per (m,z) for D6c (z=5)
    out = [(m, m + d) for d in range(15)]
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    return out

def child_opts_ordered(X, z, R):
    # child option values of (R,X,z) under the ordered-engine move rules
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return opts

def am_child_value(X, m, z, R):
    # value of the A-child that decrements a token equal to m (min(X)=m)
    for i, v in enumerate(X):
        if v == m:
            return H_ordered(R - 1, X[:i] + (m - 1,) + X[i + 1:], z)
    raise ValueError('no token == m')

# ---------------------------------------------------------------
# D1: Lemma U sweep
# ---------------------------------------------------------------
def check_D1():
    pts, comps, bad = 0, 0, 0
    details = []
    shapes = Y_tokens_lo() + [()]
    for Y in shapes:
        X = (1,) + Y
        exp = lemma_U_expected(Y)
        hc = H_canonical(2, X, 0)
        ho = H_ordered(2, X, 0)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D2: Lemma F full-decomposition sweep
# ---------------------------------------------------------------
def check_D2():
    pts, comps, bad = 0, 0, 0
    details = []
    for z in (1, 2, 3, 4):
        R = z + 2
        for s in [0] + list(range(3, 41)):
            exp = F_table(s, z)
            for Y in F_decompositions(s):
                X = (1,) + Y
                hc = H_canonical(R, X, z)
                ho = H_ordered(R, X, z)
                comps += 3
                if hc != exp or ho != exp or hc != ho:
                    bad += 1
                    if len(details) < 20:
                        details.append((z, s, Y, hc, ho, exp))
                pts += 1
        clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D3: Lemma R2 (z=0..3) + Lemma D (z=4) + arithmetic deviant set
# ---------------------------------------------------------------
def check_D3():
    pts, comps, bad = 0, 0, 0
    details = []
    shapes = Y_tokens_hi()
    for z in (0, 1, 2, 3, 4):
        R = z + 3
        for Y in shapes:
            s = sum(Y)
            X = (2,) + Y
            exp = single_token(s + 2, z, z + 3) if z <= 3 else D_val(s)
            hc = H_canonical(R, X, z)
            ho = H_ordered(R, X, z)
            comps += 3
            if hc != exp or ho != exp or hc != ho:
                bad += 1
                if len(details) < 20:
                    details.append((z, Y, hc, ho, exp))
            pts += 1
    # arithmetic deviant set (no engine calls): exactly Y=(4,)
    deviants = sorted(Y for Y in shapes
                      if D_val(sum(Y)) != single_token(sum(Y) + 2, 4, 7))
    comps += 1
    if deviants != [(4,)]:
        bad += 1
        details.append(('deviant_set', deviants))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D4: Theorem T-B grid
# ---------------------------------------------------------------
def check_D4():
    pts, comps, bad = 0, 0, 0
    details = []
    for m in range(3, 9):
        for z in (2, 3, 4):
            R = z + m + 1
            for X in T_shapes(m):
                S = sum(X)
                exp = single_token(S, z, R)
                hc = H_canonical(R, X, z)
                ho = H_ordered(R, X, z)
                comps += 3
                if hc != exp or ho != exp or hc != ho:
                    bad += 1
                    if len(details) < 20:
                        details.append((m, z, X, hc, ho, exp))
                pts += 1
            clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D5: fixed-seed random deep
# ---------------------------------------------------------------
def check_D5():
    pts, comps, bad = 0, 0, 0
    details = []
    rng = random.Random(20261234)
    for m in range(3, 9):
        for z in (2, 3, 4):
            R = z + m + 1
            for _ in range(20):
                n = rng.randint(4, 6)
                toks = [m] + [rng.randint(m, m + 15) for _ in range(n - 1)]
                X = tuple(sorted(toks))
                S = sum(X)
                exp = single_token(S, z, R)
                hc = H_canonical(R, X, z)
                ho = H_ordered(R, X, z)
                comps += 3
                if hc != exp or ho != exp or hc != ho:
                    bad += 1
                    if len(details) < 20:
                        details.append((m, z, X, hc, ho, exp))
                pts += 1
            clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D6a: published witness anchors (identical table to the published
# K1270 machine ones-multiset-t2-lowz-banded D0b; 17 anchors)
# spec: (X, z, R, expected_parent, expected_single)
# ---------------------------------------------------------------
ANCHORS = [
    ((12, 6), 17, 24, 0, 1),
    ((12, 6), 18, 25, 0, 2),
    ((14, 6), 19, 26, 0, 1),
    ((16, 6), 20, 27, 2, 1),
    ((2, 1), 1, 3, 2, 0),
    ((1, 1, 1), 1, 3, 2, 0),
    ((2, 2), 2, 5, 2, 1),
    ((4, 3), 5, 9, 2, 0),
    ((4, 4), 6, 11, 2, 1),
    ((6, 5), 9, 15, 2, 0),
    ((6, 6), 10, 17, 2, 1),
    ((1, 1), 0, 1, 1, 1),
    ((1, 1), 0, 2, 0, 0),
    ((1, 1, 1), 0, 3, 0, 1),
    ((1, 1), 1, 3, 0, 0),
    ((2, 1), 0, 3, 2, 1),
    ((2, 1), 1, 3, 2, 0),
]

def check_D6a():
    pts, comps, bad = 0, 0, 0
    details = []
    for (X, z, R, ep, es) in ANCHORS:
        xs = tuple(X)
        hc = H_canonical(R, xs, z)
        ho = H_ordered(R, xs, z)
        s = single_token(sum(xs), z, R)
        Rw = max(z + min(xs), 2)
        cw = single_token(sum(xs), z, Rw)
        hcw = H_canonical(Rw, xs, z)
        how = H_ordered(Rw, xs, z)
        comps += 5
        if (hc != ho) or (hc != ep) or (ho != ep) or (s != es) \
                or ((hcw, how) != (cw, cw)):
            bad += 1
            details.append((xs, z, R, hc, ho, ep, s, es, hcw, how, cw))
        pts += 1
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D6b: theorem anchors (23 points)
# ---------------------------------------------------------------
def check_D6b():
    pts, comps, bad = 0, 0, 0
    details = []
    def std_point(tag, X, z, R, exp):
        nonlocal pts, comps, bad
        hc = H_canonical(R, X, z)
        ho = H_ordered(R, X, z)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            details.append((tag, X, z, R, hc, ho, exp))
        pts += 1
    # R2(4) deviant: parent 2, single v(6,4,7)=1
    X, z, R = (2, 4), 4, 7
    hc = H_canonical(R, X, z); ho = H_ordered(R, X, z)
    s = single_token(sum(X), z, R)
    comps += 3
    if hc != 2 or ho != 2 or s != 1:
        bad += 1
        details.append(('R2dev', X, z, R, hc, ho, 2, s))
    pts += 1
    # D cells (z=4, R=7): D(3)=D(5)=D(6)=1
    for Y in [(3,), (5,), (3, 3)]:
        std_point('D', (2,) + Y, 4, 7, D_val(sum(Y)))
    # C(3,4) spots (z=4, R=8): parent 0, single v(S,4,8)=0
    for X in [(3, 4), (3, 3), (3, 3, 3)]:
        z, R = 4, 8
        hc = H_canonical(R, X, z); ho = H_ordered(R, X, z)
        s = single_token(sum(X), z, R)
        comps += 3
        if hc != 0 or ho != 0 or s != 0:
            bad += 1
            details.append(('C34', X, z, R, hc, ho, 0, s))
        pts += 1
    # U cells
    std_point('U', (1, 3), 0, 2, lemma_U_expected((3,)))
    std_point('U', (1,), 0, 2, lemma_U_expected(()))
    # F-table 14 points
    for (s, z) in [(0, 1), (0, 2), (0, 3), (0, 4), (3, 1), (3, 2),
                   (3, 3), (3, 4), (4, 3), (4, 4), (5, 4), (6, 4),
                   (12, 4), (20, 4)]:
        Y = () if s == 0 else (s,)
        std_point('F', (1,) + Y, z, z + 2, F_table(s, z))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D7: proof-structure option-set inspection
# ---------------------------------------------------------------
def check_D7():
    pts, comps, bad = 0, 0, 0
    details = []
    for m in range(3, 7):
        for z in (2, 3, 4):
            R = z + m + 1
            for X in D7_shapes(m):
                S = sum(X)
                opts = child_opts_ordered(X, z, R)
                vp = single_token(S, z, R)
                ho = H_ordered(R, X, z)
                hc = H_canonical(R, X, z)
                if (m, z) != (3, 4):
                    A = single_token(S - 1, z, z + m)
                    C = 1 ^ single_token(S, z - 1, z + m)
                    rel_ok = (opts == {A, C})
                    rel_tag = 'set_eq'
                    expected = sorted({A, C})
                else:
                    Ap = single_token(S - 1, 4, 7)
                    cp = 1 ^ single_token(S, 3, 7)
                    Dv = D_val(S - 3)
                    a3 = am_child_value(X, 3, z, R)
                    rel_ok = (opts <= {Ap, cp, Dv}) and (a3 == Dv)
                    rel_tag = 'subset+am'
                    expected = sorted({Ap, cp, Dv})
                comps += 3
                if (not rel_ok) or (ho != vp) or (hc != vp):
                    bad += 1
                    if len(details) < 20:
                        details.append((m, z, X, sorted(opts), expected,
                                        rel_tag, ho, hc, vp))
                pts += 1
            clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D6c: z=5 census for m in {4..7} (NOT in declared totals; bad gate is
# engine disagreement only; collapse recorded as observation)
# ---------------------------------------------------------------
def check_D6c():
    pts, comps, bad = 0, 0, 0
    collapse_counts = {}
    for m in range(4, 8):
        z = 5
        R = z + m + 1
        coll = engine_bad = total = 0
        for X in census_shapes(m):
            S = sum(X)
            hc = H_canonical(R, X, z)
            ho = H_ordered(R, X, z)
            v = single_token(S, z, R)
            comps += 2
            if hc != ho:
                engine_bad += 1
            if hc == v:
                coll += 1
            total += 1
        collapse_counts[m] = {'total': total, 'collapse': coll,
                               'engine_bad': engine_bad}
        bad += engine_bad
        pts += total
        clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'note': ('census observation only; z>=5 collapse for m>=4 is '
                     'NOT claimed (open)'),
            'collapse_counts': collapse_counts}

# =====================================================================
# tamper battery B1-B12 (each mutation MUST be caught; rc=1 otherwise)
# =====================================================================
def _mex(vals):
    vals = set(vals); m = 0
    while m in vals: m += 1
    return m

@lru_cache(maxsize=1_000_000)
def H_ordered_noXOR(R, X, z):
    # B9: C-move without the 1^ (nimber) flip
    if R == 0: return 0
    opts = set()
    for i, w in enumerate(X):
        if w > 1:
            opts.add(H_ordered_noXOR(R - 1, X[:i] + (w - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered_noXOR(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(H_ordered_noXOR(R - 1, X, z - 1))
    return _mex(opts)

def F_table_mut(s, z, mutant):
    # B2/B3/B4: one cell of the F table corrupted
    base = F_table(s, z)
    if mutant == 'B2' and z == 2 and s >= 3:
        return 2
    if mutant == 'B3' and z == 3 and s >= 4:
        return 0
    if mutant == 'B4' and z == 4 and s >= 5:
        return 1
    return base

def q_odd_mut(k):
    return k if k % 2 else k + 1

def single_token_qmut(x, z, R):
    # B10: corrupted q_odd
    if R == 0 or x <= 0: return 0
    if z == 0: return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1: return 2
        if R % 2 == 0 and R <= x - 1: return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd_mut(z)
        if R <= m: return 2 if R % 2 else 0
        if m < R < x + z: return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd_mut(x)
        if R <= m: return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

def single_token_midmut(x, z, R):
    # B11: middle-branch parity corrupted: (R+z)%2 -> (R+z+1)%2
    if R == 0 or x <= 0: return 0
    if z == 0: return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1: return 2
        if R % 2 == 0 and R <= x - 1: return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m: return 2 if R % 2 else 0
        if m < R < x + z: return (R + z + 1) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m: return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

def tamper():
    results = []

    def rec(name, bad):
        results.append({'mutation': name, 'bad': bad})
        print(('CAUGHT' if bad > 0 else 'TAMPER-MISSED') + ': ' + name +
              ' bad=' + str(bad))
        return bad

    # B1: Lemma U value flip (0 -> 1 for nonempty Y)
    bad = 0
    for Y in Y_tokens_lo():
        if H_canonical(2, (1,) + Y, 0) != 1:
            bad += 1
    rec('B1 Lemma U flip (0->1)', bad)
    # B2/B3/B4: F-table cell corruptions
    for (tag, z, smin) in [('B2 F(s,2) s>=3: 0->2', 2, 3),
                           ('B3 F(s,3) s>=4: 2->0', 3, 4),
                           ('B4 F(s,4) s>=5: 0->1', 4, 5)]:
        mutant = tag[:2]
        bad = 0
        for s in range(smin, 21):
            for Y in F_decompositions(s):
                if H_canonical(z + 2, (1,) + Y, z) != F_table_mut(s, z, mutant):
                    bad += 1
        rec(tag, bad)
        clear_engines()
    # B5: D(4) flip (2 -> 1)
    bad = 0
    for Y in Y_tokens_hi():
        exp = 1 if sum(Y) == 4 else D_val(sum(Y))
        if H_canonical(7, (2,) + Y, 4) != exp:
            bad += 1
    rec('B5 D(4) flip (2->1)', bad)
    # B6: R2(4) mis-claimed as collapse (D formula -> v formula)
    bad = 0
    for Y in Y_tokens_hi():
        s = sum(Y)
        if H_canonical(7, (2,) + Y, 4) != single_token(s + 2, 4, 7):
            bad += 1
    rec('B6 R2(4) mis-claimed collapse', bad)
    # B7: T-B m=2 extension (witness (2,2)@z=2, R=5)
    bad = 0
    if H_canonical(5, (2, 2), 2) != single_token(4, 2, 5):
        bad += 1
    rec('B7 T-B m=2 extension witness (2,2)@z=2', bad)
    # B8: T-B z=5 extension (witness (4,3)@z=5, R=9)
    bad = 0
    if H_canonical(9, (4, 3), 5) != single_token(7, 5, 9):
        bad += 1
    rec('B8 T-B z=5 extension witness (4,3)@z=5', bad)
    # B9: ordered engine without the C-move XOR
    bad = 0
    for X in [(3, 3), (3, 4), (3, 3, 3), (2, 3), (4, 5)]:
        for z in (2, 3, 4):
            for R in range(1, 9):
                if H_ordered_noXOR(R, X, z) != H_canonical(R, X, z):
                    bad += 1
    rec('B9 ordered engine C-move XOR removed', bad)
    # B10: corrupted q_odd closed form
    bad = 0
    for x in range(2, 41):
        for z in range(1, 31):
            for R in range(0, min(x + z, 31) + 1):
                if single_token_qmut(x, z, R) != vC(x, z, R): bad += 1
    rec('B10 q_odd corruption', bad)
    # B11: middle-branch parity corruption
    bad = 0
    for x in range(2, 41):
        for z in range(1, 31):
            for R in range(0, min(x + z, 31) + 1):
                if single_token_midmut(x, z, R) != vC(x, z, R): bad += 1
    rec('B11 K0832 middle-branch (R+z+1)%2 corruption', bad)
    # B12: D7 expected A-value window-off (v(S-1,z,z+m+1))
    bad = 0
    for m in (3, 4):
        for z in (2, 3, 4):
            R = z + m + 1
            for X in D7_shapes(m):
                S = sum(X)
                opts = child_opts_ordered(X, z, R)
                A_mut = single_token(S - 1, z, z + m + 1)
                C = 1 ^ single_token(S, z - 1, z + m)
                if opts != {A_mut, C}:
                    bad += 1
    rec('B12 D7 expected A-value window-off', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed:
        sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
DECLARED_TOTALS = {'points': 21565, 'comparisons': 64730}

def run_audit():
    res = {}
    res['D1'] = check_D1()
    clear_engines()
    res['D2'] = check_D2()
    clear_engines()
    res['D3'] = check_D3()
    clear_engines()
    res['D4'] = check_D4()
    clear_engines()
    res['D5'] = check_D5()
    clear_engines()
    res['D6a'] = check_D6a()
    clear_engines()
    res['D6b'] = check_D6b()
    clear_engines()
    res['D7'] = check_D7()
    clear_engines()
    res['D6c_census'] = check_D6c()
    gated = ('D1', 'D2', 'D3', 'D4', 'D5', 'D6a', 'D6b', 'D7')
    total_bad = sum(res[k]['bad'] for k in gated)
    pts = sum(res[k]['points'] for k in gated)
    comps = sum(res[k]['comparisons'] for k in gated)
    count_bad = 0
    if pts != DECLARED_TOTALS['points']:
        count_bad += 1
    if comps != DECLARED_TOTALS['comparisons']:
        count_bad += 1
    census_bad = res['D6c_census']['bad']
    res['summary'] = {
        'n_bad': total_bad + count_bad + census_bad,
        'theorem': ('Lemma U/F/R2/D + Theorem T-B: min>=3 banded window '
                    'extension to z in {2,3,4}; with K1270 (z in {0,1}) '
                    'this completes the m=3 row of K1268 Conjecture C1 '
                    '(band z<z*(3)=5). Universal claims proved on paper in '
                    'the declaration note; this finite audit corroborates.'),
        'declared_totals': DECLARED_TOTALS,
        'observed_totals': {'points': pts, 'comparisons': comps},
        'census': {'points': res['D6c_census']['points'],
                   'comparisons': res['D6c_census']['comparisons'],
                   'bad_engine': census_bad},
        'unknown_statement': ('standard 11x11 empty board, two-stone roots '
                              '{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, '
                              'class 5343: UNKNOWN at all times'),
        'meta': {'verifier_sha256': SELF_SHA},
    }
    res['points_totals'] = {k: res[k]['points'] for k in gated}
    res['comparisons_totals'] = {k: res[k]['comparisons'] for k in gated}
    return res, total_bad + count_bad + census_bad, pts, comps

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'audit'
    if mode == 'tamper':
        tamper(); return
    res, bad, pts, comps = run_audit()
    os.makedirs('output', exist_ok=True)
    with open('output/audit.json', 'w') as f:
        f.write(json.dumps(res, indent=1, sort_keys=True,
                           ensure_ascii=True) + '\n')
    print('TOTAL points:', pts, 'comparisons:', comps, 'bad:', bad)
    print('D6c census:', res['summary']['census'])
    if bad:
        print('AUDIT FAIL: bad =', bad); sys.exit(1)
    print('AUDIT PASS'); sys.exit(0)

if __name__ == '__main__':
    main()
