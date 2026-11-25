#!/usr/bin/env python3
"""verify_strip_z5.py -- machine audit for the declared claims of the
single-owner declaration note (K1273 provisional; min>=4 critical-strip
z=5 slice):

  Lemma F5 : F(s,5) := H(7;{1}+Y;5) (Y tokens >=3, arity free, Y=() for
              s=0) is independent of the decomposition of s and
              F5(0)=1, F5(3)=0, F5(4)=1, F5(5)=0, F5(s>=6)=2.
              Extends published Lemma F (K1272) from z in {1..4} to z=5.
  Lemma G  : G(s) := H(8;{2}+Y;5) depends only on s and
              G(0)=0, G(3)=1, G(4)=0, G(s>=5)=1. The R2-form collapse
              fails exactly at Y=(4,): G(4)=0 != v(6,5,8)=1
              (arithmetic consequence of the closed form; z=4's D(4)=2
              deviant points the other way).
  Lemma E  : E(s) := H(9;{3}+Y;5) depends only on s and
              E(0)=1, E(3)=0, E(4)=2, E(s>=5)=0. Deviant exactly at
              Y=(4,): E(4)=2 != v(7,5,9)=0 -- this cell IS the
              published K1268 frontier witness (4,3)@R*=9 (parent 2
              vs single 0), now inside the closed-form ladder.
  Theorem T-Z5: for ALL m>=4, every nonempty finite multiset X with
              min(X)=m:  H(m+6;X;5) = v(sum X, 5, m+6).
              Base m=4 via Lemma E + mex absorption; m>=5 by option-set
              identity induction on m (C-hand child = published
              Theorem T-B at z=4, a=m child = C(m-1,5)).
  Corollary: the m=4 row of K1268 Conjecture C1 is COMPLETE (band
              z<z*(4)=6: z in {0,1} K1270, z in {2,3,4} K1272, z=5
              here), and the critical strip z=5 holds for all m>=4.

Declared checks (PUBLISH-THEN-EXECUTE; note:
research/log/2026-11-23-strip-z5-min4-single-owner-note.md):
  D1  Lemma F5: s in {0} u {3..40}, ALL decompositions into 1..4
      tokens >=3 (3,657)                          (3,657 / 10,971)
  D2  Lemma G: Y = tokens 3..9 multisets, arity 0..4 (330) vs G table;
      +1 arithmetic deviant-set comparison: {Y: G != v(s+2,5,8)} ==
      {(4,)}                                        (330 / 991)
  D3  Lemma E: same 330 shapes vs E table; +1 arithmetic deviant-set:
      {Y: E != v(s+3,5,9)} == {(4,)}                (330 / 991)
  D4  Theorem T-Z5 grid: m in {4..9} x z=5 x 222 shapes
      (1 single + 15 two-token d=0..14 + 81 three-token d<=8
       + 125 four-token d<=4)                      (1,332 / 3,996)
  D5  fixed-seed (20261123) random deep: m in {4..9} x 20 shapes
      (arity 4..6, tokens in [m,m+15], one token fixed at m)
                                                    (120 / 360)
  D6a published K1270/K1268 witness anchors (17)   (17 / 85)
  D6b theorem anchors 25 points: E deviant (3,4)@R=9 -> 2/v=0;
      G deviant (2,4)@R=8 -> 0/v=1; E cells (3,3)/(3,5)/(3,3,3);
      G cells (2,3)/(2,5)/(2,3,3); F5 cells (1,3)/(1,4)/(1,5)/(1,6);
      m=4 parents (4,4)/(4,5)/(4,4,4)@R=10 -> 1; C(4,4) cell (4,4)@z=4
      R=9 -> 1; D anchors (2,3)/(2,4)@z=4 R=7 -> 1/2;
      F(.,4) anchors (1,3)/(1,4)@z=4 R=6 -> 0/1;
      C(3,4) cells (3,4)/(3,3,3)@z=4 R=8 -> 0; E(0)/G(0) single
      tokens (3,)/(2,)@z=5 -> 1/0; m=5 parent (5,5)@R=11 -> 1
                                                   (25 / 75)
  D7  proof-structure option-set inspection: m in {4..7} x 33 shapes
      (2-token d=0..6, 3-token d in [0,4]^2, 5-token ramp).
      m=4: opts subset of {A', c', E(S-4)} AND a=4 child == E(S-4).
      m>=5: opts == {v(S-1,5,m+5), 1^v(S,4,m+5)} exact. Parent mex
      == v(sum,z,R) both engines in both cases.  (132 / 396)
  TOTAL declared: 5,943 points / 17,865 comparisons / bad 0.
  D6c census (NOT in declared totals; bad gate = engine disagreement
  only; observations are recorded, nothing claimed):
    (a) z=6 strip grid: m in {4..8} x 96 census shapes (two-token
        d=0..14 + three-token d<=8), R=m+7; collapse record
        (m=4 is OUT of band: z*(4)=6, witness (4,4)@R=11 expected).
    (b) next-lane cell tables at z=6: F6 := H(8;{1}+Y;6),
        G6 := H(9;{2}+Y;6), E6 := H(10;{3}+Y;6) over the 330 shapes:
        s-only tables, decomposition-dependence flags, deviant sets
        vs v(s+2,6,9) / v(s+3,6,10) recorded for the z=6 lane.
        The z=6 strip for m>=5 stays OPEN.

Fail-closed: any bad>0 -> rc=1; declared-count mismatch -> rc=1
(honest record requirement). Finite machine audit is NOT the proof:
the universal claims rest on the paper proof in the declaration note
(F5/G/E closed-form z-ladder + option-set identity + induction on m).
Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2
{59,60}, classes 1/2/4 and class 5343 remain UNKNOWN at all times.
Determinism: no time, no unseeded randomness; value-transparent
engine cache clears between blocks and inside large blocks.
--tamper runs the 12-mutation battery B1-B12 (each MUST be caught).
"""
import sys, os, json, hashlib, random
from functools import lru_cache
from itertools import combinations_with_replacement

sys.setrecursionlimit(1_000_000)

# === ENGINE BLOCK (machine-assembled; see build_engine_from_published.py) ===
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
# declared closed forms (transcription of the declaration note)
# ---------------------------------------------------------------
def F5_table(s):
    # Lemma F5 closed form, s in {0} u {3,4,...}
    if s == 0:
        return 1
    if s == 3:
        return 0
    if s == 4:
        return 1
    if s == 5:
        return 0
    return 2

def G_val(s):
    # Lemma G closed form (z=5 cell), s in {0} u {3,4,...}
    if s == 0:
        return 0
    if s == 3:
        return 1
    if s == 4:
        return 0
    return 1

def E_val(s):
    # Lemma E closed form (z=5 cell), s in {0} u {3,4,...}
    if s == 0:
        return 1
    if s == 3:
        return 0
    if s == 4:
        return 2
    return 0

# ---------------------------------------------------------------
# shape families (declared protocol)
# ---------------------------------------------------------------
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

def Y_tokens_hi():
    # tokens 3..9, arity 0..4 (330 shapes; same family as published)
    out = []
    for k in range(0, 5):
        out.extend(combinations_with_replacement(range(3, 10), k))
    return out

def T_shapes(m):
    # 222 shapes per m for D4 (same family as published)
    out = [(m,)]
    out.extend((m, m + d) for d in range(15))
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    out.extend((m, m + a, m + b, m + c)
               for a in range(5) for b in range(5) for c in range(5))
    return out

def D7_shapes(m):
    # 33 shapes per m for D7 (same family as published)
    out = [(m, m + d) for d in range(7)]
    out.extend((m, m + a, m + b) for a in range(5) for b in range(5))
    out.append(tuple(m + i for i in range(5)))
    return out

def census_shapes(m):
    # 96 shapes per m for D6c (same family as published)
    out = [(m, m + d) for d in range(15)]
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    return out

def child_opts_ordered(X, z, R):
    # child option values of (R,X,z) under the ordered-engine rules
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
    # value of the A-child that decrements a token equal to m
    for i, v in enumerate(X):
        if v == m:
            return H_ordered(R - 1, X[:i] + (m - 1,) + X[i + 1:], z)
    raise ValueError('no token == m')

# ---------------------------------------------------------------
# D1: Lemma F5 full-decomposition sweep
# ---------------------------------------------------------------
def check_D1():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 7, 5
    for s in [0] + list(range(3, 41)):
        exp = F5_table(s)
        for Y in F_decompositions(s):
            X = (1,) + Y
            hc = H_canonical(R, X, z)
            ho = H_ordered(R, X, z)
            comps += 3
            if hc != exp or ho != exp or hc != ho:
                bad += 1
                if len(details) < 20:
                    details.append((s, Y, hc, ho, exp))
            pts += 1
        clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D2: Lemma G sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D2():
    pts, comps, bad = 0, 0, 0
    details = []
    for Y in Y_tokens_hi():
        s = sum(Y)
        X = (2,) + Y
        exp = G_val(s)
        hc = H_canonical(8, X, 5)
        ho = H_ordered(8, X, 5)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    # arithmetic deviant set (no engine): exactly Y=(4,)
    deviants = sorted(Y for Y in Y_tokens_hi()
                      if G_val(sum(Y)) != single_token(sum(Y) + 2, 5, 8))
    comps += 1
    if deviants != [(4,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D3: Lemma E sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D3():
    pts, comps, bad = 0, 0, 0
    details = []
    for Y in Y_tokens_hi():
        s = sum(Y)
        X = (3,) + Y
        exp = E_val(s)
        hc = H_canonical(9, X, 5)
        ho = H_ordered(9, X, 5)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    # arithmetic deviant set (no engine): exactly Y=(4,)
    deviants = sorted(Y for Y in Y_tokens_hi()
                      if E_val(sum(Y)) != single_token(sum(Y) + 3, 5, 9))
    comps += 1
    if deviants != [(4,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D4: Theorem T-Z5 grid
# ---------------------------------------------------------------
def check_D4():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 5
    for m in range(4, 10):
        R = m + 6
        for X in T_shapes(m):
            S = sum(X)
            exp = single_token(S, z, R)
            hc = H_canonical(R, X, z)
            ho = H_ordered(R, X, z)
            comps += 3
            if hc != exp or ho != exp or hc != ho:
                bad += 1
                if len(details) < 20:
                    details.append((m, X, hc, ho, exp))
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
    rng = random.Random(20261123)
    z = 5
    for m in range(4, 10):
        R = m + 6
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
                    details.append((m, X, hc, ho, exp))
            pts += 1
        clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D6a: published witness anchors (identical table to the published
# K1272 machine D6a; 17 anchors)
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
# D6b: theorem anchors (25 points)
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
    def dev_point(tag, X, z, R, epar, esing):
        nonlocal pts, comps, bad
        hc = H_canonical(R, X, z)
        ho = H_ordered(R, X, z)
        s = single_token(sum(X), z, R)
        comps += 3
        if hc != epar or ho != epar or s != esing:
            bad += 1
            details.append((tag, X, z, R, hc, ho, epar, s, esing))
        pts += 1
    # E deviant witness (published K1268 frontier): parent 2, single 0
    dev_point('Edev', (3, 4), 5, 9, 2, 0)
    # G deviant: parent 0, single v(6,5,8)=1
    dev_point('Gdev', (2, 4), 5, 8, 0, 1)
    # E cells
    std_point('E', (3, 3), 5, 9, E_val(3))
    std_point('E', (3, 5), 5, 9, E_val(5))
    std_point('E', (3, 3, 3), 5, 9, E_val(6))
    # G cells
    std_point('G', (2, 3), 5, 8, G_val(3))
    std_point('G', (2, 5), 5, 8, G_val(5))
    std_point('G', (2, 3, 3), 5, 8, G_val(6))
    # F5 cells
    std_point('F5', (1, 3), 5, 7, F5_table(3))
    std_point('F5', (1, 4), 5, 7, F5_table(4))
    std_point('F5', (1, 5), 5, 7, F5_table(5))
    std_point('F5', (1, 6), 5, 7, F5_table(6))
    # m=4 parents at z=5, R=10: all collapse to 1
    std_point('Tm4', (4, 4), 5, 10, single_token(8, 5, 10))
    std_point('Tm4', (4, 5), 5, 10, single_token(9, 5, 10))
    std_point('Tm4', (4, 4, 4), 5, 10, single_token(12, 5, 10))
    # C(4,4) cell (used as the m=4 base C-hand child)
    std_point('C44', (4, 4), 4, 9, single_token(8, 4, 9))
    # published Lemma D anchors (z=4 C-hand of G)
    std_point('D', (2, 3), 4, 7, 1)
    std_point('D', (2, 4), 4, 7, 2)
    # published Lemma F z=4 anchors (C-hand of F5)
    std_point('F4', (1, 3), 4, 6, 0)
    std_point('F4', (1, 4), 4, 6, 1)
    # published C(3,4) cells (z=4 C-hand of E; K1272 T-B)
    std_point('C34', (3, 4), 4, 8, single_token(7, 4, 8))
    std_point('C34', (3, 3, 3), 4, 8, single_token(9, 4, 8))
    # E(0)/G(0) single tokens at z=5
    std_point('E0', (3,), 5, 9, E_val(0))
    std_point('G0', (2,), 5, 8, G_val(0))
    # m=5 parent
    std_point('Tm5', (5, 5), 5, 11, single_token(10, 5, 11))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D7: proof-structure option-set inspection
# ---------------------------------------------------------------
def check_D7():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 5
    for m in range(4, 8):
        R = m + 6
        for X in D7_shapes(m):
            S = sum(X)
            opts = child_opts_ordered(X, z, R)
            vp = single_token(S, z, R)
            ho = H_ordered(R, X, z)
            hc = H_canonical(R, X, z)
            if m == 4:
                Ap = single_token(S - 1, 5, 9)
                cp = 1 ^ single_token(S, 4, 9)
                Ev = E_val(S - 4)
                a4 = am_child_value(X, 4, z, R)
                rel_ok = (opts <= {Ap, cp, Ev}) and (a4 == Ev)
                rel_tag = 'subset+E'
                expected = sorted({Ap, cp, Ev})
            else:
                A = single_token(S - 1, 5, m + 5)
                C = 1 ^ single_token(S, 4, m + 5)
                rel_ok = (opts == {A, C})
                rel_tag = 'set_eq'
                expected = sorted({A, C})
            comps += 3
            if (not rel_ok) or (ho != vp) or (hc != vp):
                bad += 1
                if len(details) < 20:
                    details.append((m, X, sorted(opts), expected,
                                    rel_tag, ho, hc, vp))
            pts += 1
        clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D6c census (NOT in declared totals; bad gate = engine disagreement;
# observations only, no collapse claims beyond the theorem band)
# ---------------------------------------------------------------
def check_D6c():
    res = {}
    # (a) z=6 strip grid: m in {4..8}, census shapes
    strip = {}
    pts = comps = bad = 0
    for m in range(4, 9):
        z, R = 6, m + 7
        coll = engine_bad = total = 0
        seps = []
        for X in census_shapes(m):
            S = sum(X)
            hc = H_canonical(R, X, z)
            ho = H_ordered(R, X, z)
            v = single_token(S, z, R)
            comps += 2
            if hc != ho:
                engine_bad += 1
            if hc != v:
                coll += 1
                seps.append([ list(X), hc, v ])
            total += 1
        strip[m] = {'total': total, 'collapse': total - coll, 'separations': seps}
        bad += engine_bad
        pts += total
        clear_engines()
    res['z6_strip'] = strip
    # (b) next-lane cell tables at z=6
    cells = {}
    for tag, pre, R, dv in [('F6', (1,), 8, None),
                            ('G6', (2,), 9, 2), ('E6', (3,), 10, 3)]:
        tbl = {}
        dep = []
        devs = []
        for Y in Y_tokens_hi():
            s = sum(Y)
            X = pre + Y
            hc = H_canonical(R, X, 6)
            ho = H_ordered(R, X, 6)
            comps += 1 if dv is None else 2
            if hc != ho:
                bad += 1
            tbl.setdefault(s, set()).add(hc)
            if dv is not None and hc != single_token(s + dv, 6, R):
                devs.append(list(Y))
        tbl = {s: sorted(v) for s, v in sorted(tbl.items())}
        dep = [s for s, v in tbl.items() if len(v) > 1]
        cells[tag] = {'table': tbl, 'decomp_dependent_s': dep,
                      'deviants_vs_collapse': devs}
        pts += 330
        clear_engines()
    res['z6_cells'] = cells
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'note': ('census observation only; z=6 strip for m>=5 and '
                     'the F6/G6/E6 closed forms are NOT claimed (open)'),
            'census': res}

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

def F5_mut(s, mutant):
    base = F5_table(s)
    if mutant == 'B1' and s >= 6:
        return 0
    if mutant == 'B2' and s == 4:
        return 0
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

    # B1/B2: F5 table corruptions
    for (tag, smin, smax) in [('B1 F5(s>=6): 2->0', 6, 40),
                              ('B2 F5(4): 1->0', 3, 8)]:
        mutant = tag[:2]
        bad = 0
        for s in [0] + list(range(smin if smin > 3 else 3, smax + 1)):
            exp = F5_mut(s, mutant)
            for Y in F_decompositions(s):
                if H_canonical(7, (1,) + Y, 5) != exp:
                    bad += 1
        rec(tag, bad)
        clear_engines()
    # B3: G(4) flip (0 -> 1; hides the deviant)
    bad = 0
    for Y in Y_tokens_hi():
        exp = 1 if sum(Y) == 4 else G_val(sum(Y))
        if H_canonical(8, (2,) + Y, 5) != exp:
            bad += 1
    rec('B3 G(4) flip (0->1)', bad)
    # B4: G mis-claimed as R2-form collapse
    bad = 0
    for Y in Y_tokens_hi():
        s = sum(Y)
        if H_canonical(8, (2,) + Y, 5) != single_token(s + 2, 5, 8):
            bad += 1
    rec('B4 G mis-claimed collapse v(s+2,5,8)', bad)
    # B5: E(4) flip (2 -> 0; hides the K1268 frontier witness)
    bad = 0
    for Y in Y_tokens_hi():
        exp = 0 if sum(Y) == 4 else E_val(sum(Y))
        if H_canonical(9, (3,) + Y, 5) != exp:
            bad += 1
    rec('B5 E(4) flip (2->0)', bad)
    # B6: E mis-claimed as collapse
    bad = 0
    for Y in Y_tokens_hi():
        s = sum(Y)
        if H_canonical(9, (3,) + Y, 5) != single_token(s + 3, 5, 9):
            bad += 1
    rec('B6 E mis-claimed collapse v(s+3,5,9)', bad)
    clear_engines()
    # B7: T-Z5 min=3 extension (witness (4,3)@z=5, R=9)
    bad = 0
    for X in T_shapes(3):
        if H_canonical(9, X, 5) != single_token(sum(X), 5, 9):
            bad += 1
    rec('B7 T-Z5 min=3 extension witness (4,3)@z=5', bad)
    # B8: T-Z5 z=6 m=4 extension (frontier witness (4,4)@z=6, R=11)
    bad = 0
    for X in T_shapes(4):
        if H_canonical(11, X, 6) != single_token(sum(X), 6, 11):
            bad += 1
    rec('B8 T-Z5 z=6 m=4 extension witness (4,4)@z=6', bad)
    # B9: ordered engine without the C-move XOR
    bad = 0
    for X in [(3, 3), (3, 4), (3, 3, 3), (2, 3), (4, 5)]:
        for z in (3, 4, 5):
            for R in range(1, 10):
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
    # B12: D7 child-identity mutations (m=4: D-cell instead of E-cell;
    #      m>=5: budget m+4 instead of m+5)
    bad = 0
    for m in range(4, 7):
        R = m + 6
        for X in D7_shapes(m):
            S = sum(X)
            a_m = am_child_value(X, m, 5, R)
            if m == 4:
                # D-cell of K1272: D(0)=0, D(3)=1, D(4)=2, D(s>=5)=1
                if S - 4 == 0:
                    exp_mut = 0
                elif S - 4 == 3:
                    exp_mut = 1
                elif S - 4 == 4:
                    exp_mut = 2
                else:
                    exp_mut = 1
            else:
                exp_mut = single_token(S - 1, 5, m + 4)
            if a_m != exp_mut:
                bad += 1
    rec('B12 D7 a=m child identity mutation (D-cell/budget-off)', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed:
        sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
DECLARED_TOTALS = {'points': 5943, 'comparisons': 17865}

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
        'theorem': ('Lemma F5/G/E + Theorem T-Z5: min>=4 critical-strip '
                    'z=5 slice; completes the m=4 row of K1268 Conjecture '
                    'C1 (band z<z*(4)=6) and proves the strip z=5 for '
                    'all m>=4. Universal claims proved on paper in the '
                    'declaration note; this finite audit corroborates.'),
        'declared_totals': DECLARED_TOTALS,
        'observed_totals': {'points': pts, 'comparisons': comps},
        'census': {'points': res['D6c_census']['points'],
                   'comparisons': res['D6c_census']['comparisons'],
                   'bad_engine': census_bad},
        'unknown_statement': ('standard 11x11 empty board, two-stone '
                              'roots {49,60}/{59,60}, S2 {59,60}, classes '
                              '1/2/4, class 5343: UNKNOWN at all times'),
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
