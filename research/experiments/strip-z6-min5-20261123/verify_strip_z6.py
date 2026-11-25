#!/usr/bin/env python3
"""verify_strip_z6.py -- machine audit for the declared claims of the
single-owner declaration note (K1274 provisional; min>=5 critical-strip
z=6 slice):

  Lemma F6 : F6(s) := H(8;{1}+Y;6) (Y tokens >=3, arity free, Y=() for
              s=0) is independent of the decomposition of s and
              F6(0)=1, F6(3)=0, F6(4)=1, F6(5)=0, F6(6)=1, F6(7)=0,
              F6(s>=8)=0. Extends published Lemma F (K1272, z in {1..4})
              and Lemma F5 (K1273, z=5) to z=6. The z=5-only "2-family
              transition" of the F-cell disappears at z=6.
  Lemma G6 : G6(s) := H(9;{2}+Y;6) depends only on s and
              G6(0)=0, G6(3)=1, G6(4)=0, G6(5)=1, G6(6)=2, G6(s>=7)=1.
              The R2-form collapse v(s+2,6,9) fails exactly at
              s in {4,6}: G6(4)=0 != v(6,6,9)=2 (downward) and
              G6(6)=2 != v(8,6,9)=1 (upward; first ladder deviant with
              s>4, and both directions coexist in one cell).
  Lemma E6 : E6(s) := H(10;{3}+Y;6) depends only on s and
              E6(0)=1, E6(3)=0, E6(4)=1, E6(5)=0, E6(s>=6)=0.
              Deviant exactly at s=4: E6(4)=1 != v(7,6,10)=0 (upward).
  Lemma D6 : NEW rung. D6(s) := H(11;{4}+Y;6) with ALL Y tokens >=5
              (s in {0} u {5,6,...}) satisfies the FULL collapse
              D6(s) = v(s+4,6,11) with zero deviants -- the first
              fully collapsing ladder cell. The floor min(Y)>=5 is
              essential: with the floor relaxed the m=4 frontier
              witness (4,4)@R=11 refutes it (parent 2 vs single 1).
  Theorem T-Z6: for ALL m>=5, every nonempty finite multiset X with
              min(X)=m: H(m+7;X;6) = v(sum X, 6, m+7).
              Base m=5 via Lemma D6 (all three parent options equal 1,
              mex{1}=0 = single side) ; m>=6 by option-set identity
              induction on m (a=m child = C(m-1,6), C-hand child =
              published T-Z5 of K1273 at z=5).
  Corollary: the z=6 row of the critical strip is determined for all
              m>=5; the (z=6, m>=5) column of K1268 Conjecture C1 is
              resolved incl. m=5 (z* (5)=9: z in {7,8} stay open).

Declared checks (PUBLISH-THEN-EXECUTE; note:
research/log/2026-11-23-strip-z6-min5-single-owner-note.md,
commit 7018151):
  D1  Lemma F6: s in {0} u {3..40}, ALL decompositions into 1..4
      tokens >=3 (3,657)                          (3,657 / 10,971)
  D2  Lemma G6: Y = tokens 3..9 multisets, arity 0..4 (330) vs G6
      table; +1 arithmetic deviant-set comparison:
      {Y: G6 != v(s+2,6,9)} == {(3,3),(4,),(6,)}   (330 / 991)
  D3  Lemma E6: same 330 shapes vs E6 table; +1 arithmetic deviant
      set == {(4,)}                                (330 / 991)
  D4  Lemma D6: s in {0} u {5..40}, ALL decompositions into 1..4
      tokens >=5 (1,650) vs full collapse v(s+4,6,11)
                                                    (1,650 / 4,950)
  D5  Theorem T-Z6 grid: m in {5..10} x z=6 x 222 shapes
      (1 single + 15 two-token d=0..14 + 81 three-token d<=8
       + 125 four-token d<=4)                      (1,332 / 3,996)
  D6  fixed-seed (20261124) random deep: m in {5..10} x 15 shapes
      (arity 4..5, tokens in [m,m+15], one token fixed at m)
                                                    (90 / 270)
  D7a published K1270/K1268 witness anchors (17)   (17 / 85)
  D7b theorem anchors 39 points (5 deviant/witness pair anchors +
      34 standard anchors: F6/G6/E6/D6 cells, m=5 single+parents,
      base children incl. D6 C-hand children, published z=5
      continuity, induction parents, frontier negative (4,4))
                                                    (39 / 117)
  D8  cell recursion option-set identity (paper proof sec 2.1-2.4):
      child option set == arithmetic expectation for
      F6 3,657 = {v(s,7,7), v(s,6,7), 1^F5(s)};
      G6 330 = {v(s+1,6,8), F6(s), 1^G5(s)};
      E6 330 = {v(s+2,6,9), G6(s), 1^E5(s)};
      D6 1,650 = {v(s+3,6,10), E6(s), 1^v(s+4,5,10)}
                                                   (5,967 / 5,967)
  D9  parent proof-structure option-set inspection: m in {5..9} x
      33 shapes. m=5: opts subset of {A', c', D6(S-5)} AND a=5
      child == D6(S-5); m>=6: opts == {v(S-1,6,m+6), 1^v(S,5,m+6)}
      exact; parent mex == v both engines. (165 / 495)
  TOTAL declared: 13,577 points / 28,833 comparisons / bad 0.
  D6c census (NOT in declared totals; bad gate = engine disagreement
  only; observations are recorded, nothing claimed):
    (a) next-lane (z=7) cell tables with the proper per-cell floors:
        F7 H(9;{1}+Y;7), G7 H(10;{2}+Y;7), E7 H(11;{3}+Y;7) over the
        330 family (tokens 3..9, arity 0..4); D7 H(12;{4}+Y;7) over
        the 126 family (tokens 5..9); C7 H(13;{5}+Y;7) over the 70
        family (tokens 6..9). s-only tables, decomposition-dependence
        flags, deviant sets vs v(s+k,7,R) recorded. The z=7 strip and
        the F7/G7/E7/D7/C7 closed forms stay OPEN (not claimed).
    (b) z=7 strip grid: m in {5..10} x 96 census shapes (R=m+8):
        collapse record (m=5 is IN band: z*(5)=9; records the C1
        (m=5,z=7) observation).
    (c) m=4 negative record at z=6 over the 222 T-family (only the
        frontier witness (4,4) expected to separate).

Fail-closed: any bad>0 -> rc=1; declared-count mismatch -> rc=1
(honest record requirement). Finite machine audit is NOT the proof:
the universal claims rest on the paper proof in the declaration note
(F6/G6/E6/D6 z=6 closed-form ladder + mex base m=5 + option-set
identity induction on m). Standard 11x11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4 and class 5343 remain
UNKNOWN at all times. Determinism: no time, no unseeded randomness;
value-transparent engine cache clears between blocks and inside
large blocks. --tamper runs the 12-mutation battery B1-B12 (each
MUST be caught).
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
def F6_table(s):
    # Lemma F6 closed form, s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0}.get(s, 0)

def G6_table(s):
    # Lemma G6 closed form (z=6 cell), s in {0} u {3,4,...}
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 2}.get(s, 1)

def E6_table(s):
    # Lemma E6 closed form (z=6 cell), s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0}.get(s, 0)

def D6_table(s):
    # Lemma D6 (floored family, tokens >=5): full collapse
    return single_token(s + 4, 6, 11)

# published z=5 closed forms (K1273), used by the D8 recursions
def F5t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0}.get(s, 2)

def G5t(s):
    return {0: 0, 3: 1, 4: 0}.get(s, 1)

def E5t(s):
    return {0: 1, 3: 0, 4: 2}.get(s, 0)

# ---------------------------------------------------------------
# shape families (declared protocol)
# ---------------------------------------------------------------
def decomps(s, tmin, amax=4):
    # all multisets of 1..amax tokens >=tmin summing to s; Y=() if s==0
    if s == 0:
        return [()]
    out = []
    for k in range(1, amax + 1):
        for c in combinations_with_replacement(range(tmin, s + 1), k):
            if sum(c) == s:
                out.append(c)
    return out

def Y_tokens(tmin, tmax):
    # multisets of tokens in [tmin, tmax], arity 0..4
    out = []
    for k in range(0, 5):
        out.extend(combinations_with_replacement(range(tmin, tmax + 1), k))
    return out

def T_shapes(m):
    # 222 shapes per m for D5 (same family as published)
    out = [(m,)]
    out.extend((m, m + d) for d in range(15))
    out.extend((m, m + a, m + b) for a in range(9) for b in range(9))
    out.extend((m, m + a, m + b, m + c)
               for a in range(5) for b in range(5) for c in range(5))
    return out

def D9_shapes(m):
    # 33 shapes per m for D9 (same family as published)
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
    opts = set()
    for i, w in enumerate(X):
        if w > 1:
            opts.add(H_ordered(R - 1, X[:i] + (w - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return opts

def am_child_value(X, m, z, R):
    # value of the A-child that decrements a token equal to m
    for i, w in enumerate(X):
        if w == m:
            return H_ordered(R - 1, X[:i] + (m - 1,) + X[i + 1:], z)
    raise ValueError('no token == m')

# ---------------------------------------------------------------
# D1: Lemma F6 full-decomposition sweep
# ---------------------------------------------------------------
def check_D1():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 8, 6
    for s in [0] + list(range(3, 41)):
        exp = F6_table(s)
        for Y in decomps(s, 3):
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
# D2: Lemma G6 sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D2():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (2,) + Y
        exp = G6_table(s)
        hc = H_canonical(9, X, 6)
        ho = H_ordered(9, X, 6)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if G6_table(sum(Y)) != single_token(sum(Y) + 2, 6, 9))
    comps += 1
    if deviants != [(3, 3), (4,), (6,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D3: Lemma E6 sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D3():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (3,) + Y
        exp = E6_table(s)
        hc = H_canonical(10, X, 6)
        ho = H_ordered(10, X, 6)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if E6_table(sum(Y)) != single_token(sum(Y) + 3, 6, 10))
    comps += 1
    if deviants != [(4,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D4: Lemma D6 sweep (floored family), full collapse
# ---------------------------------------------------------------
def check_D4():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 11, 6
    for s in [0] + list(range(5, 41)):
        exp = D6_table(s)
        for Y in decomps(s, 5):
            X = (4,) + Y
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
# D5: Theorem T-Z6 grid
# ---------------------------------------------------------------
def check_D5():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 6
    for m in range(5, 11):
        R = m + 7
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
# D6: fixed-seed random deep
# ---------------------------------------------------------------
def check_D6():
    pts, comps, bad = 0, 0, 0
    details = []
    rng = random.Random(20261124)
    z = 6
    for m in range(5, 11):
        R = m + 7
        for _ in range(15):
            n = rng.randint(4, 5)
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
# D7a: published witness anchors (identical table to the published
# K1272/K1273 machines D6a; 17 anchors)
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

def check_D7a():
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
# D7b: theorem anchors (39 points)
# ---------------------------------------------------------------
def check_D7b():
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
    # G6 deviant witnesses: parent vs single (both directions)
    dev_point('G6dev4', (2, 4), 6, 9, 0, 2)
    dev_point('G6dev6a', (2, 6), 6, 9, 2, 1)
    dev_point('G6dev6b', (2, 3, 3), 6, 9, 2, 1)
    # E6 deviant witness
    dev_point('E6dev4', (3, 4), 6, 10, 1, 0)
    # F6 cells
    for Y, s in [((3,), 3), ((4,), 4), ((5,), 5), ((6,), 6),
                 ((7,), 7), ((8,), 8)]:
        std_point('F6', (1,) + Y, 6, 8, F6_table(s))
    # G6 cells
    std_point('G6', (2, 3), 6, 9, G6_table(3))
    std_point('G6', (2, 5), 6, 9, G6_table(5))
    std_point('G6', (2, 7), 6, 9, G6_table(7))
    std_point('G6', (2, 5, 5), 6, 9, G6_table(10))
    # E6 cells
    std_point('E6', (3,), 6, 10, E6_table(0))
    std_point('E6', (3, 3), 6, 10, E6_table(3))
    std_point('E6', (3, 5), 6, 10, E6_table(5))
    std_point('E6', (3, 3, 3), 6, 10, E6_table(6))
    # D6 cells (floored: tokens >=5)
    std_point('D6', (4,), 6, 11, D6_table(0))
    std_point('D6', (4, 5), 6, 11, D6_table(5))
    std_point('D6', (4, 6), 6, 11, D6_table(6))
    std_point('D6', (4, 5, 5), 6, 11, D6_table(10))
    std_point('D6', (4, 6, 8), 6, 11, D6_table(14))
    # m=5 single token + parents at z=6, R=12
    std_point('m5', (5,), 6, 12, single_token(5, 6, 12))
    for X in [(5, 5), (5, 6), (5, 5, 5), (5, 7)]:
        std_point('m5p', X, 6, 12, single_token(sum(X), 6, 12))
    # base m=5 children: (i) A-on->6 stair child; (iii) z=5 C-hand child;
    # D6 C-hand children at z=5
    std_point('m5A', (5, 6), 6, 11, single_token(11, 6, 11))
    std_point('m5C', (5, 6), 5, 11, single_token(11, 5, 11))
    std_point('D6C', (4, 5), 5, 10, single_token(9, 5, 10))
    std_point('D6C', (4, 6), 5, 10, single_token(10, 5, 10))
    # published z=5 continuity anchors (K1273)
    std_point('z5', (3, 4), 5, 9, 2)
    std_point('z5', (2, 4), 5, 8, 0)
    std_point('z5', (1, 6), 5, 7, 2)
    # induction parents
    std_point('ind', (6, 6), 6, 13, single_token(12, 6, 13))
    std_point('ind', (8, 8), 6, 15, single_token(16, 6, 15))
    std_point('ind', (7, 7, 9), 6, 14, single_token(23, 6, 14))
    # frontier negative: m=4 at z=6 (the floor-essentiality witness)
    dev_point('front', (4, 4), 6, 11, 2, 1)
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D8: cell recursion option-set identity (proof secs 2.1-2.4)
# ---------------------------------------------------------------
def check_D8():
    pts, comps, bad = 0, 0, 0
    details = []
    def cell_opts(R, pre, z, expfun, fam, tag):
        nonlocal pts, comps, bad
        n = 0
        for Y in fam:
            s = sum(Y)
            opts = child_opts_ordered(pre + Y, z, R)
            exp = expfun(s)
            comps += 1
            if opts != exp:
                bad += 1
                if len(details) < 20:
                    details.append((tag, Y, sorted(opts), sorted(exp)))
            n += 1
            if n % 400 == 0:
                clear_engines()
        pts += n
    famF = []
    for s in [0] + list(range(3, 41)):
        famF.extend(decomps(s, 3))
    cell_opts(8, (1,), 6,
              lambda s: {single_token(s, 7, 7), single_token(s, 6, 7),
                         1 ^ F5t(s)}, famF, 'F6')
    clear_engines()
    fam330 = Y_tokens(3, 9)
    cell_opts(9, (2,), 6,
              lambda s: {single_token(s + 1, 6, 8), F6_table(s),
                         1 ^ G5t(s)}, fam330, 'G6')
    clear_engines()
    cell_opts(10, (3,), 6,
              lambda s: {single_token(s + 2, 6, 9), G6_table(s),
                         1 ^ E5t(s)}, fam330, 'E6')
    clear_engines()
    famD = []
    for s in [0] + list(range(5, 41)):
        famD.extend(decomps(s, 5))
    cell_opts(11, (4,), 6,
              lambda s: {single_token(s + 3, 6, 10), E6_table(s),
                         1 ^ single_token(s + 4, 5, 10)}, famD, 'D6')
    clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D9: parent proof-structure option-set inspection
# ---------------------------------------------------------------
def check_D9():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 6
    for m in range(5, 10):
        R = m + 7
        for X in D9_shapes(m):
            S = sum(X)
            opts = child_opts_ordered(X, z, R)
            vp = single_token(S, z, R)
            ho = H_ordered(R, X, z)
            hc = H_canonical(R, X, z)
            if m == 5:
                Ap = single_token(S - 1, 6, 11)
                cp = 1 ^ single_token(S, 5, 11)
                Dv = D6_table(S - 5)
                a5 = am_child_value(X, 5, z, R)
                rel_ok = (opts <= {Ap, cp, Dv}) and (a5 == Dv)
                rel_tag = 'subset+D6'
                expected = sorted({Ap, cp, Dv})
            else:
                A = single_token(S - 1, 6, m + 6)
                C = 1 ^ single_token(S, 5, m + 6)
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
    pts = comps = bad = 0
    # (a) z=7 next-lane cell tables with proper per-cell floors
    cells = {}
    for tag, pre, R, dvoff, tmin, tmax in [
            ('F7', (1,), 9, 1, 3, 9), ('G7', (2,), 10, 2, 3, 9),
            ('E7', (3,), 11, 3, 3, 9), ('D7', (4,), 12, 4, 5, 9),
            ('C7', (5,), 13, 5, 6, 9)]:
        fam = Y_tokens(tmin, tmax)
        tbl = {}
        devs = []
        for Y in fam:
            s = sum(Y)
            X = pre + Y
            hc = H_canonical(R, X, 7)
            ho = H_ordered(R, X, 7)
            comps += 2
            if hc != ho:
                bad += 1
            tbl.setdefault(s, set()).add(hc)
            if hc != single_token(s + dvoff, 7, R):
                devs.append(list(Y))
        tbl2 = {s: sorted(v) for s, v in sorted(tbl.items()) if s <= 20}
        dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
        cells[tag] = {'R': R, 'floor': tmin, 'family': len(fam),
                      'table_s20': {str(k): v for k, v in tbl2.items()},
                      'decomp_dependent_s': dep,
                      'deviant_count': len(devs),
                      'deviants_vs_collapse': devs[:40]}
        pts += len(fam)
        clear_engines()
    res['z7_cells'] = cells
    # (b) z=7 strip grid: m in {5..10} x 96 census shapes
    strip = {}
    for m in range(5, 11):
        z, R = 7, m + 8
        coll = engine_bad = total = 0
        seps = []
        for X in census_shapes(m):
            S = sum(X)
            hc = H_canonical(R, X, z)
            ho = H_ordered(R, X, z)
            comps += 2
            if hc != ho:
                engine_bad += 1
            if hc != single_token(S, z, R):
                coll += 1
                if len(seps) < 5:
                    seps.append([list(X), hc, single_token(S, z, R)])
            total += 1
        strip[m] = {'total': total, 'collapse': total - coll,
                    'separations': seps}
        bad += engine_bad
        pts += total
        clear_engines()
    res['z7_strip'] = strip
    # (c) m=4 negative record at z=6 over the 222 T-family
    neg = []
    mneg = 0
    for X in T_shapes(4):
        S = sum(X)
        hc = H_canonical(11, X, 6)
        ho = H_ordered(11, X, 6)
        comps += 2
        mneg += 1
        if hc != ho:
            bad += 1
        if hc != single_token(S, 6, 11):
            neg.append([list(X), hc, single_token(S, 6, 11)])
    res['m4_z6_negative'] = {'total': mneg, 'separations': neg}
    pts += mneg
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'note': ('census observation only; z=7 strip for m>=6 and '
                     'the F7/G7/E7/D7/C7 closed forms are NOT claimed '
                     '(open)'),
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
    # B10: C-move without the 1^ (nimber) flip
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

def F6_mut(s, mutant):
    base = F6_table(s)
    if mutant == 'B1' and s >= 8:
        return 2
    if mutant == 'B2' and s == 6:
        return 0
    return base

def q_odd_mut(k):
    return k if k % 2 else k + 1

def single_token_qmut(x, z, R):
    # B11: corrupted q_odd
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

def tamper():
    results = []

    def rec(name, bad):
        results.append({'mutation': name, 'bad': bad})
        print(('CAUGHT' if bad > 0 else 'TAMPER-MISSED') + ': ' + name +
              ' bad=' + str(bad))
        return bad

    # B1/B2: F6 table corruptions (restricted families that must
    #        contain decisive mismatches)
    for (tag, s_list) in [('B1 F6(s>=8): 0->2', list(range(8, 17))),
                          ('B2 F6(6): 1->0', list(range(3, 9)))]:
        mutant = tag[:2]
        bad = 0
        for s in s_list:
            exp = F6_mut(s, mutant)
            for Y in decomps(s, 3):
                if H_canonical(8, (1,) + Y, 6) != exp:
                    bad += 1
            clear_engines()
        rec(tag, bad)
    # B3: G6(4) flip (0 -> 1; hides the s=4 deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 1 if sum(Y) == 4 else G6_table(sum(Y))
        if H_canonical(9, (2,) + Y, 6) != exp:
            bad += 1
    rec('B3 G6(4) flip (0->1)', bad)
    # B4: G6 mis-claimed as R2-form collapse
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(9, (2,) + Y, 6) != single_token(s + 2, 6, 9):
            bad += 1
    rec('B4 G6 mis-claimed collapse v(s+2,6,9)', bad)
    # B5: G6(6) flip (2 -> 1; hides the s=6 deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 1 if sum(Y) == 6 else G6_table(sum(Y))
        if H_canonical(9, (2,) + Y, 6) != exp:
            bad += 1
    rec('B5 G6(6) flip (2->1)', bad)
    clear_engines()
    # B6: E6(4) flip (1 -> 0; hides the deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 0 if sum(Y) == 4 else E6_table(sum(Y))
        if H_canonical(10, (3,) + Y, 6) != exp:
            bad += 1
    rec('B6 E6(4) flip (1->0)', bad)
    # B7: E6 mis-claimed as collapse
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(10, (3,) + Y, 6) != single_token(s + 3, 6, 10):
            bad += 1
    rec('B7 E6 mis-claimed collapse v(s+3,6,10)', bad)
    clear_engines()
    # B8: D6 with the floor relaxed to tokens >= 3 (m=4 frontier
    #     witness (4,4)@R=11 refutes the loosened claim)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(11, (4,) + Y, 6) != single_token(s + 4, 6, 11):
            bad += 1
    rec('B8 D6 floor relaxed to tokens>=3', bad)
    # B9: T-Z6 min=4 extension (frontier witness (4,4)@z=6, R=11)
    bad = 0
    for X in T_shapes(4):
        if H_canonical(11, X, 6) != single_token(sum(X), 6, 11):
            bad += 1
    rec('B9 T-Z6 min=4 extension witness (4,4)@z=6', bad)
    clear_engines()
    # B10: ordered engine without the C-move XOR
    bad = 0
    for X in [(3, 3), (3, 4), (3, 3, 3), (2, 3), (4, 5), (2, 6)]:
        for z in (3, 4, 5, 6):
            for R in range(1, 10):
                if H_ordered_noXOR(R, X, z) != H_canonical(R, X, z):
                    bad += 1
    rec('B10 ordered engine C-move XOR removed', bad)
    # B11: corrupted q_odd closed form
    bad = 0
    for x in range(2, 41):
        for z in range(1, 31):
            for R in range(0, min(x + z, 31) + 1):
                if single_token_qmut(x, z, R) != vC(x, z, R): bad += 1
    rec('B11 q_odd corruption', bad)
    # B12: D9 child-identity mutations (m=5: E6-cell instead of the
    #      D6-cell; m>=6: budget m+5 instead of m+6)
    bad = 0
    for m in range(5, 9):
        R = m + 7
        for X in D9_shapes(m):
            S = sum(X)
            a_m = am_child_value(X, m, 6, R)
            if m == 5:
                exp_mut = E6_table(S - 5)
            else:
                exp_mut = single_token(S - 1, 6, m + 5)
            if a_m != exp_mut:
                bad += 1
        clear_engines()
    rec('B12 D9 a=m child identity mutation (E6-cell/budget-off)', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed:
        sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
DECLARED_TOTALS = {'points': 13577, 'comparisons': 28833}

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
    res['D6'] = check_D6()
    clear_engines()
    res['D7a'] = check_D7a()
    clear_engines()
    res['D7b'] = check_D7b()
    clear_engines()
    res['D8'] = check_D8()
    clear_engines()
    res['D9'] = check_D9()
    clear_engines()
    res['D6c_census'] = check_D6c()
    gated = ('D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7a', 'D7b', 'D8', 'D9')
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
        'theorem': ('Lemma F6/G6/E6/D6 + Theorem T-Z6: min>=5 '
                    'critical-strip z=6 slice; resolves the (z=6, '
                    'm>=5) column of K1268 Conjecture C1 incl. the '
                    'm=5 row through z=6 first fully collapsing ladder '
                    'cell D6 (floored) + mex base m=5 + option-set '
                    'identity induction. Universal claims proved on '
                    'paper in the declaration note; this finite audit '
                    'corroborates.'),
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
