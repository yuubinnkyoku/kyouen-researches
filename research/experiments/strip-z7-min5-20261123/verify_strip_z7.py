#!/usr/bin/env python3
"""verify_strip_z7.py -- machine audit for the declared claims of the
single-owner declaration note (K1275 provisional; min>=5 critical-strip
z=7 slice; declaration note:
research/log/2026-11-23-strip-z7-min5-single-owner-note.md,
commit 4e8229fd):

  Lemma F7 : F7(s) := H(9;{1}+Y;7) (Y tokens >=3, arity free, Y=() for
              s=0) is independent of the decomposition of s and
              F7(0)=1, F7(3)=0, F7(4)=1, F7(5)=0, F7(6)=1, F7(7)=0,
              F7(s>=8)=2. Extends published Lemma F (K1272, z in
              {1..4}), F5 (K1273, z=5), F6 (K1274, z=6) to z=7. The
              F-cell 2-family RETURNS at z=7 (F6 sent it to 0).
  Lemma G7 : G7(s) := H(10;{2}+Y;7) depends only on s and
              G7(0)=0, G7(3)=1, G7(4)=0, G7(5)=1, G7(6)=0, G7(7)=1,
              G7(s>=8)=1. The R2-form collapse v(s+2,7,10) fails
              exactly at s=6: G7(6)=0 != v(8,7,10)=1 (DOWNWARD --
              the direction flip of the z=6 s=6 deviant 2>1). The
              G6 s=4 deviant disappears at z=7.
  Lemma E7 : E7(s) := H(11;{3}+Y;7) depends only on s and
              E7(0)=1, E7(3)=0, E7(4)=1, E7(5)=0, E7(6)=2,
              E7(s>=7)=0. Deviants exactly at s in {4,6}:
              E7(4)=1 != v(7,7,11)=2 (downward; the z=6 E6(4)=1!=0
              upward flips) and E7(6)=2 != v(9,7,11)=0 (upward;
              the first s>4 deviant family continues).
  Lemma D7 : NEW floored rung (second fully collapsing ladder cell
              after D6): D7(s) := H(12;{4}+Y;7) with ALL Y tokens >=5
              (s in {0} u {5,6,...}) satisfies the FULL collapse
              D7(s) = v(s+4,7,12) with zero deviants. The floor
              min(Y)>=5 is essential: loosened to tokens>=3 the m=4
              negative witness (4,4)@R=12 (0 != 1) and the s=6
              decomposition dependence (Y=(3,3): 0 vs (6,): 1) enter.
  Theorem T-Z7: for ALL m>=5, every nonempty finite multiset X with
              min(X)=m: H(m+8;X;7) = v(sum X, 7, m+8).
              Base m=5 via Lemma D7 (all three parent options equal 1,
              mex{1}=0 = single side -- the z=6-type trivial
              absorption base); m>=6 by option-set identity induction
              on m (a=m child = C(m-1,7), C-hand child = published
              T-Z6 of K1274 at z=6).
  Corollary: the z=7 row of the critical strip is determined for all
              m>=5; the (z=7, m>=5) column of K1268 Conjecture C1 is
              resolved incl. m=5 (z*(5)=9: exactly ONE cell z=8 stays
              open on the m=5 row; m>=6: z in {8..z*(m)-1} open).

Declared checks (PUBLISH-THEN-EXECUTE):
  D1  Lemma F7: s in {0} u {3..40}, ALL decompositions into 1..4
      tokens >=3 (3,657)                          (3,657 / 10,971)
  D2  Lemma G7: Y = tokens 3..9 multisets, arity 0..4 (330) vs G7
      table; +1 arithmetic deviant-set comparison:
      {Y: G7 != v(s+2,7,10)} == {(3,3),(6,)}       (330 / 991)
  D3  Lemma E7: same 330 shapes vs E7 table; +1 arithmetic deviant
      set == {(3,3),(4,),(6,)}                      (330 / 991)
  D4  Lemma D7: s in {0} u {5..40}, ALL decompositions into 1..4
      tokens >=5 (1,650) vs full collapse v(s+4,7,12)
                                                     (1,650 / 4,950)
  D5  Theorem T-Z7 grid: m in {5..10} x z=7 x 222 shapes
      (1 single + 15 two-token d=0..14 + 81 three-token d<=8
       + 125 four-token d<=4)                       (1,332 / 3,996)
  D6  fixed-seed (20261125) random deep: m in {5..10} x 15 shapes
      (arity 4..5, tokens in [m,m+15], one token fixed at m)
                                                     (90 / 270)
  D7a published K1270/K1268 witness anchors (17)     (17 / 85)
  D7b theorem anchors 40 points (6 deviant/witness pair anchors incl.
      the m=4 z=7 downward negative + 34 standard anchors:
      F7/G7/E7/D7 cells, m=5 single+parents, base children incl. D7
      C-hand children, published z=6 continuity, induction parents)
                                                     (40 / 120)
  D8  cell recursion option-set identity (paper proof sec 2.1-2.4):
      child option set == arithmetic expectation for
      F7 3,657 = {v(s,8,8), v(s,7,8), 1^F6(s)};
      G7 330 = {v(s+1,7,9), F7(s), 1^G6(s)};
      E7 330 = {v(s+2,7,10), G7(s), 1^E6(s)};
      D7 1,650 = {v(s+3,7,11), E7(s), 1^v(s+4,6,11)}
                                                    (5,967 / 5,967)
  D9  parent proof-structure option-set inspection: m in {5..9} x
      33 shapes. m=5: opts subset of {A', c', D7(S-5)} AND a=5
      child == D7(S-5); m>=6: opts == {v(S-1,7,m+7), 1^v(S,6,m+7)}
      exact; parent mex == v both engines. (165 / 495)
  TOTAL declared: 13,578 points / 28,836 comparisons / bad 0.
  D6c census (NOT in declared totals; bad gate = engine disagreement
  only; observations are recorded, nothing claimed):
    (a) next-lane (z=8) cell tables with the proper per-cell floors:
        F8 H(10;{1}+Y;8), G8 H(11;{2}+Y;8), E8 H(12;{3}+Y;8) over the
        330 family (tokens 3..9, arity 0..4); D8 H(13;{4}+Y;8) over
        the 126 family (tokens 5..9) and the loose 330 family
        (tokens 3..9; decomposition-dependence record); C8
        H(14;{5}+Y;8) over the 70 family (tokens 6..9). s-only
        tables, decomposition-dependence flags, deviant sets vs
        v(s+k,8,R) recorded. The z=8 strip and the F8/G8/E8/D8/C8
        closed forms stay OPEN (not claimed).
    (b) z=8 strip grid: m in {5..10} x 96 census shapes (R=m+9):
        collapse record (m=5 is IN band: z*(5)=9; the LAST band cell
        of the m=5 row; records the C1 (m=5,z=8) observation).
    (c) m=4 negative record at z=7 over the 222 T-family (only the
        downward frontier witness (4,4)@R=12 expected to separate:
        parent 0 vs single 1 -- the front direction flip).

Fail-closed: any bad>0 -> rc=1; declared-count mismatch -> rc=1
(honest record requirement). Finite machine audit is NOT the proof:
the universal claims rest on the paper proof in the declaration note
(F7/G7/E7/D7 z=7 closed-form ladder + mex base m=5 + option-set
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
def F7_table(s):
    # Lemma F7 closed form (z=7 cell), s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0}.get(s, 2)

def G7_table(s):
    # Lemma G7 closed form (z=7 cell), s in {0} u {3,4,...}
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0}.get(s, 1)

def E7_table(s):
    # Lemma E7 closed form (z=7 cell), s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 2}.get(s, 0)

def D7_table(s):
    # Lemma D7 (floored family, tokens >=5): full collapse
    return single_token(s + 4, 7, 12)

# published z=6 closed forms (K1274), used by the D8 recursions
def F6t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0}.get(s, 0)

def G6t(s):
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 2}.get(s, 1)

def E6t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0}.get(s, 0)

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
# D1: Lemma F7 full-decomposition sweep
# ---------------------------------------------------------------
def check_D1():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 9, 7
    for s in [0] + list(range(3, 41)):
        exp = F7_table(s)
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
# D2: Lemma G7 sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D2():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (2,) + Y
        exp = G7_table(s)
        hc = H_canonical(10, X, 7)
        ho = H_ordered(10, X, 7)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if G7_table(sum(Y)) != single_token(sum(Y) + 2, 7, 10))
    comps += 1
    if deviants != [(3, 3), (6,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D3: Lemma E7 sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D3():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (3,) + Y
        exp = E7_table(s)
        hc = H_canonical(11, X, 7)
        ho = H_ordered(11, X, 7)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if E7_table(sum(Y)) != single_token(sum(Y) + 3, 7, 11))
    comps += 1
    if deviants != [(3, 3), (4,), (6,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D4: Lemma D7 sweep (floored family), full collapse
# ---------------------------------------------------------------
def check_D4():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 12, 7
    for s in [0] + list(range(5, 41)):
        exp = D7_table(s)
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
# D5: Theorem T-Z7 grid
# ---------------------------------------------------------------
def check_D5():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 7
    for m in range(5, 11):
        R = m + 8
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
    rng = random.Random(20261125)
    z = 7
    for m in range(5, 11):
        R = m + 8
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
# K1272/K1273/K1274 machines D7a; 17 anchors)
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
# D7b: theorem anchors (40 points)
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
    # G7 deviant witnesses at s=6 (downward direction flip)
    dev_point('G7dev6a', (2, 6), 7, 10, 0, 1)
    dev_point('G7dev6b', (2, 3, 3), 7, 10, 0, 1)
    # E7 deviant witnesses at s in {4,6}
    dev_point('E7dev4', (3, 4), 7, 11, 1, 2)
    dev_point('E7dev6a', (3, 6), 7, 11, 2, 0)
    dev_point('E7dev6b', (3, 3, 3), 7, 11, 2, 0)
    # m=4 z=7 negative: the downward frontier witness (direction flip)
    dev_point('front', (4, 4), 7, 12, 0, 1)
    # F7 cells
    for Y, s in [((3,), 3), ((4,), 4), ((5,), 5), ((6,), 6),
                 ((7,), 7), ((8,), 8)]:
        std_point('F7', (1,) + Y, 7, 9, F7_table(s))
    # G7 cells
    std_point('G7', (2, 3), 7, 10, G7_table(3))
    std_point('G7', (2, 5), 7, 10, G7_table(5))
    std_point('G7', (2, 7), 7, 10, G7_table(7))
    std_point('G7', (2, 5, 5), 7, 10, G7_table(10))
    # E7 cells
    std_point('E7', (3,), 7, 11, E7_table(0))
    std_point('E7', (3, 3), 7, 11, E7_table(3))
    std_point('E7', (3, 5), 7, 11, E7_table(5))
    std_point('E7', (3, 3, 3), 7, 11, E7_table(6))
    # D7 cells (floored: tokens >=5)
    std_point('D7', (4,), 7, 12, D7_table(0))
    std_point('D7', (4, 5), 7, 12, D7_table(5))
    std_point('D7', (4, 6), 7, 12, D7_table(6))
    std_point('D7', (4, 5, 5), 7, 12, D7_table(10))
    std_point('D7', (4, 6, 8), 7, 12, D7_table(14))
    # m=5 single token + parents at z=7, R=13
    std_point('m5', (5,), 7, 13, single_token(5, 7, 13))
    for X in [(5, 5), (5, 6), (5, 5, 5), (5, 7)]:
        std_point('m5p', X, 7, 13, single_token(sum(X), 7, 13))
    # base m=5 children: (i) A-on->6 stair child; (iii) z=6 C-hand child;
    # D7 C-hand children at z=6
    std_point('m5A', (5, 6), 7, 12, single_token(11, 7, 12))
    std_point('m5C', (5, 6), 6, 12, single_token(11, 6, 12))
    std_point('D7C', (4, 5), 6, 11, single_token(9, 6, 11))
    std_point('D7C', (4, 6), 6, 11, single_token(10, 6, 11))
    # published z=6 continuity anchors (K1274)
    std_point('z6', (3, 4), 6, 10, 1)
    std_point('z6', (2, 4), 6, 9, 0)
    std_point('z6', (1, 6), 6, 8, 1)
    # induction parents
    std_point('ind', (6, 6), 7, 14, single_token(12, 7, 14))
    std_point('ind', (8, 8), 7, 16, single_token(16, 7, 16))
    std_point('ind', (7, 7, 9), 7, 15, single_token(23, 7, 15))
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
    cell_opts(9, (1,), 7,
              lambda s: {single_token(s, 8, 8), single_token(s, 7, 8),
                         1 ^ F6t(s)}, famF, 'F7')
    clear_engines()
    fam330 = Y_tokens(3, 9)
    cell_opts(10, (2,), 7,
              lambda s: {single_token(s + 1, 7, 9), F7_table(s),
                         1 ^ G6t(s)}, fam330, 'G7')
    clear_engines()
    cell_opts(11, (3,), 7,
              lambda s: {single_token(s + 2, 7, 10), G7_table(s),
                         1 ^ E6t(s)}, fam330, 'E7')
    clear_engines()
    famD = []
    for s in [0] + list(range(5, 41)):
        famD.extend(decomps(s, 5))
    cell_opts(12, (4,), 7,
              lambda s: {single_token(s + 3, 7, 11), E7_table(s),
                         1 ^ single_token(s + 4, 6, 11)}, famD, 'D7')
    clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D9: parent proof-structure option-set inspection
# ---------------------------------------------------------------
def check_D9():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 7
    for m in range(5, 10):
        R = m + 8
        for X in D9_shapes(m):
            S = sum(X)
            opts = child_opts_ordered(X, z, R)
            vp = single_token(S, z, R)
            ho = H_ordered(R, X, z)
            hc = H_canonical(R, X, z)
            if m == 5:
                Ap = single_token(S - 1, 7, 12)
                cp = 1 ^ single_token(S, 6, 12)
                Dv = D7_table(S - 5)
                a5 = am_child_value(X, 5, z, R)
                rel_ok = (opts <= {Ap, cp, Dv}) and (a5 == Dv)
                rel_tag = 'subset+D7'
                expected = sorted({Ap, cp, Dv})
            else:
                A = single_token(S - 1, 7, m + 7)
                C = 1 ^ single_token(S, 6, m + 7)
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
    # (a) z=8 next-lane cell tables with proper per-cell floors
    cells = {}
    for tag, pre, R, dvoff, tmin, tmax in [
            ('F8', (1,), 10, 1, 3, 9), ('G8', (2,), 11, 2, 3, 9),
            ('E8', (3,), 12, 3, 3, 9), ('D8', (4,), 13, 4, 5, 9),
            ('C8', (5,), 14, 5, 6, 9)]:
        fam = Y_tokens(tmin, tmax)
        tbl = {}
        devs = []
        for Y in fam:
            s = sum(Y)
            X = pre + Y
            hc = H_canonical(R, X, 8)
            ho = H_ordered(R, X, 8)
            comps += 2
            if hc != ho:
                bad += 1
            tbl.setdefault(s, set()).add(hc)
            if hc != single_token(s + dvoff, 8, R):
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
    # (a2) D8 loose family (tokens 3..9): decomposition-dependence record
    fam = Y_tokens(3, 9)
    tbl = {}
    devs = []
    for Y in fam:
        s = sum(Y)
        hc = H_canonical(13, (4,) + Y, 8)
        ho = H_ordered(13, (4,) + Y, 8)
        comps += 2
        if hc != ho:
            bad += 1
        tbl.setdefault(s, set()).add(hc)
        if hc != single_token(s + 4, 8, 13):
            devs.append(list(Y))
    dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
    tbl2 = {s: sorted(v) for s, v in sorted(tbl.items()) if s <= 20}
    cells['D8_loose'] = {'R': 13, 'floor': 3, 'family': len(fam),
                         'table_s20': {str(k): v for k, v in tbl2.items()},
                         'decomp_dependent_s': dep,
                         'deviant_count': len(devs),
                         'deviants_vs_collapse': devs[:40]}
    pts += len(fam)
    res['z8_cells'] = cells
    clear_engines()
    # (b) z=8 strip grid: m in {5..10} x 96 census shapes
    strip = {}
    for m in range(5, 11):
        z, R = 8, m + 9
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
    res['z8_strip'] = strip
    # (c) m=4 negative record at z=7 over the 222 T-family
    neg = []
    mneg = 0
    for X in T_shapes(4):
        S = sum(X)
        hc = H_canonical(12, X, 7)
        ho = H_ordered(12, X, 7)
        comps += 2
        mneg += 1
        if hc != ho:
            bad += 1
        if hc != single_token(S, 7, 12):
            neg.append([list(X), hc, single_token(S, 7, 12)])
    res['m4_z7_negative'] = {'total': mneg, 'separations': neg}
    pts += mneg
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'note': ('census observation only; z=8 strip for m>=5 and '
                     'the F8/G8/E8/D8/C8 closed forms are NOT claimed '
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

def F7_mut(s, mutant):
    base = F7_table(s)
    if mutant == 'B1' and s >= 8:
        return 0
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

    # B1/B2: F7 table corruptions (restricted families that must
    #        contain decisive mismatches)
    for (tag, s_list) in [('B1 F7(s>=8): 2->0', list(range(8, 17))),
                          ('B2 F7(6): 1->0', list(range(3, 9)))]:
        mutant = tag[:2]
        bad = 0
        for s in s_list:
            exp = F7_mut(s, mutant)
            for Y in decomps(s, 3):
                if H_canonical(9, (1,) + Y, 7) != exp:
                    bad += 1
            clear_engines()
        rec(tag, bad)
    # B3: G7(6) flip (0 -> 1; hides the s=6 downward deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 1 if sum(Y) == 6 else G7_table(sum(Y))
        if H_canonical(10, (2,) + Y, 7) != exp:
            bad += 1
    rec('B3 G7(6) flip (0->1)', bad)
    # B4: G7 mis-claimed as R2-form collapse
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(10, (2,) + Y, 7) != single_token(s + 2, 7, 10):
            bad += 1
    rec('B4 G7 mis-claimed collapse v(s+2,7,10)', bad)
    # B5: E7(6) flip (2 -> 1; hides the s=6 deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 1 if sum(Y) == 6 else E7_table(sum(Y))
        if H_canonical(11, (3,) + Y, 7) != exp:
            bad += 1
    rec('B5 E7(6) flip (2->1)', bad)
    clear_engines()
    # B6: E7(4) flip (1 -> 0; hides the deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 0 if sum(Y) == 4 else E7_table(sum(Y))
        if H_canonical(11, (3,) + Y, 7) != exp:
            bad += 1
    rec('B6 E7(4) flip (1->0)', bad)
    # B7: E7 mis-claimed as collapse
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(11, (3,) + Y, 7) != single_token(s + 3, 7, 11):
            bad += 1
    rec('B7 E7 mis-claimed collapse v(s+3,7,11)', bad)
    clear_engines()
    # B8: D7 with the floor relaxed to tokens >= 3 (the s=6
    #     decomposition dependence Y=(3,3) and the m=4 negative
    #     witness Y=(4,) i.e. (4,4)@R=12 refute the loosened claim)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(12, (4,) + Y, 7) != single_token(s + 4, 7, 12):
            bad += 1
    rec('B8 D7 floor relaxed to tokens>=3', bad)
    # B9: T-Z7 min=4 extension (negative witness (4,4)@z=7, R=12)
    bad = 0
    for X in T_shapes(4):
        if H_canonical(12, X, 7) != single_token(sum(X), 7, 12):
            bad += 1
    rec('B9 T-Z7 min=4 extension witness (4,4)@z=7', bad)
    clear_engines()
    # B10: ordered engine without the C-move XOR
    bad = 0
    for X in [(3, 3), (3, 4), (3, 3, 3), (2, 3), (4, 5), (2, 6)]:
        for z in (3, 4, 5, 6, 7):
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
    # B12: D9 child-identity mutations (m=5: E7-cell instead of the
    #      D7-cell; m>=6: budget m+6 instead of m+7)
    bad = 0
    for m in range(5, 9):
        R = m + 8
        for X in D9_shapes(m):
            S = sum(X)
            a_m = am_child_value(X, m, 7, R)
            if m == 5:
                exp_mut = E7_table(S - 5)
            else:
                exp_mut = single_token(S - 1, 7, m + 6)
            if a_m != exp_mut:
                bad += 1
        clear_engines()
    rec('B12 D9 a=m child identity mutation (E7-cell/budget-off)', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed:
        sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
DECLARED_TOTALS = {'points': 13578, 'comparisons': 28836}

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
        'theorem': ('Lemma F7/G7/E7/D7 + Theorem T-Z7: min>=5 '
                    'critical-strip z=7 slice; resolves the (z=7, '
                    'm>=5) column of K1268 Conjecture C1 incl. the '
                    'm=5 row through z=7 (remaining m=5 band cell: '
                    'z=8 only) via the second fully collapsing '
                    'floored ladder cell D7 + mex base m=5 + '
                    'option-set identity induction. Universal claims '
                    'proved on paper in the declaration note; this '
                    'finite audit corroborates.'),
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
