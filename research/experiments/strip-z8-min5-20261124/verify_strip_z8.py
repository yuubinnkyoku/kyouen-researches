#!/usr/bin/env python3
"""verify_strip_z8.py -- machine audit for the declared claims of the
single-owner declaration note (K1276 provisional; min>=5 critical-strip
z=8 slice; declaration note:
research/log/2026-11-24-strip-z8-min5-single-owner-note.md,
commit f4dcf92e):

  Lemma F8 : F8(s) := H(10;{1}+Y;8) (Y tokens >=3, arity free, Y=() for
              s=0) is independent of the decomposition of s and
              F8(0)=1, F8(3)=0, F8(4)=1, F8(5)=0, F8(6)=1, F8(7)=0,
              F8(8)=1, F8(s>=9)=0. Extends the published F-ladder
              (F z in {1..4} K1272, F5 K1273, F6 K1274, F7 K1275).
  Lemma G8 : G8(s) := H(11;{2}+Y;8) depends only on s and
              G8(0)=0, G8(3)=1, G8(4)=0, G8(5)=1, G8(6)=0, G8(7)=1,
              G8(8)=2, G8(s>=9)=1. The R2-form collapse v(s+2,8,11)
              fails exactly at s in {6,8}: deviants
              {(6,),(3,3)} downward 0<2 and {(8,),(3,5),(4,4)}
              upward 2>1.
  Lemma E8 : E8(s) := H(12;{3}+Y;8) depends only on s and
              E8(0)=1, E8(3)=0, E8(4)=1, E8(5)=0, E8(6)=1,
              E8(s>=7)=0. Deviants exactly {(6,),(3,3)}, upward
              1>0. The E8 recursion expectation is CONDITIONAL:
              {G8(s), 1^E7(s)} plus ({v(s+2,8,11)} iff some Y token
              is >= 4). The unconditional ghost form breaks at
              Y=(3,3) s=6 (observed set {0,3} vs unconditional
              {0,2,3}) -- pre-registered as probe P12 before the
              declaration. At z=7 the E7 ghost had coincided with
              the option value, so the unconditional form passed
              there by luck.
  Lemma D8 : the first NON-collapsing floored ladder rung:
              D8(s) := H(13;{4}+Y;8) with ALL Y tokens >=5 (s in
              {0} u {5,6,...}) depends only on s with table
              {0:0, 6:2, else v(s+4,8,13)} -- the SINGLE s=6 upward
              deviant D8(6)=2 != v(10,8,13)=1 breaks the full-
              collapse series D6 (K1274), D7 (K1275). The floor
              min(Y)>=5 is essential: loosened to tokens>=3 the
              decomposition-dependence at s in {6,8} enters.
  Lemma C7 : C7(s) := H(13;{5}+Y;7) with ALL Y tokens >=6 (s in
              {0} u {6,6,...}) FULLY collapses:
              C7(s) = v(s+5,7,13), zero deviants, zero decomposition
              dependence (the K1274 D6c census observation extended
              to the full floored decomposition family).
  Lemma C8 : C8(s) := H(14;{5}+Y;8) with ALL Y tokens >=6 FULLY
              collapses: C8(s) = v(s+5,8,14). The D8 s=6 deviant 2
              is absorbed by the mex (verified at all s).
  Theorem T-Z8: for ALL m>=5, every nonempty finite multiset X with
              min(X)=m: H(m+9;X;8) = v(sum X, 8, m+9).
              Base m=5: all three parent option families collapse
              to the value 1 (A'=v(S-1,8,13), c'=1^v(S,7,13),
              D8(S-5)) except the single s=6 deviant child value 2
              (S=11), which the parent mex absorbs -> parent mex
              {1} (resp. {1,2}) = 0 = v(S,8,14). m>=6 by option-set
              identity induction on m (a=m child = induction
              hypothesis C(m-1,8) at R=m+8 = (m-1)+9, a>m children
              by the published K1264 staircase window-edge
              equality, C-hand child = published T-Z7 (K1275) at
              z=7).
  Corollary: the z=8 row of the critical strip is determined for
              all m>=5; the m=5 row of K1268 Conjecture C1 is fully
              resolved including its last band cell z=8 (z*(5)=9);
              m>=6 rows keep z in {9..z*(m)-1} open.

Declared checks (PUBLISH-THEN-EXECUTE):
  D1  Lemma F8: s in {0} u {3..40}, ALL decompositions into 1..4
      tokens >=3 (3,657)                          (3,657 / 10,971)
  D2  Lemma G8: Y = tokens 3..9 multisets, arity 0..4 (330) vs G8
      table; +1 arithmetic deviant-set comparison:
      {Y: G8 != v(s+2,8,11)} == {(6,),(3,3),(8,),(3,5),(4,4)}
                                                     (330 / 991)
  D3  Lemma E8: same 330 shapes vs E8 table; +1 arithmetic deviant
      set == {(6,),(3,3)}                           (330 / 991)
  D4  Lemma D8: s in {0} u {5..40}, ALL decompositions into 1..4
      tokens >=5 (1,650) vs {0:0, 6:2, else v(s+4,8,13)}
                                                     (1,650 / 4,950)
  D4b Lemma C7: s in {0} u {6..40}, ALL decompositions into 1..4
      tokens >=6 (1,078) vs full collapse v(s+5,7,13)
                                                     (1,078 / 3,234)
  D4c Lemma C8: the same 1,078 decompositions vs full collapse
      v(s+5,8,14)                                   (1,078 / 3,234)
  D5  Theorem T-Z8 grid: m in {5..10} x z=8 x 222 shapes (R=m+9)
                                                     (1,332 / 3,996)
  D6  fixed-seed (20261126) random deep: m in {5..10} x 15 shapes
      (arity 4..5, tokens in [m,m+15], one token fixed at m)
                                                      (90 / 270)
  D7a published K1272/K1273/K1274/K1275 witness anchors (17)
                                                      (17 / 85)
  D7b theorem anchors 47 points (13 deviant/witness pair anchors:
      the G8 s=6 / s=8 deviants, the E8 s=6 deviants, the F8 s=8
      deviants, the D8 s=6 deviant (same position as the m=4 z=8
      upward negative), the m=4 z=8 downward negative (4,4), and
      the m=5 z=9 out-of-band upward witness (5,6); + 34 standard
      anchors: F8/G8/E8/D8/C7/C8 cells, the m=5 single token and
      bottom parents, the bottom A' stair and c'-hand children, the
      published z=7 continuity, and the induction parents)
                                                      (47 / 141)
  D8  cell recursion option-set identity (paper proof secs
      2.1-2.6), 1 comparison per point (ordered child option set
      == arithmetic expectation set):
      F8 3,657 = {v(s,9,9), v(s,8,9), 1^F7(s)};
      G8 3,657 = {F8(s), v(s+1,8,10), 1^G7(s)};
      E8 3,657 = CONDITIONAL {G8(s), 1^E7(s)}
                  + ({v(s+2,8,11)}: some Y token >= 4);
      D8 1,650 = {v(s+3,8,12), E8(s), 1^v(s+4,7,12)};
      C7 1,078 = {v(s+4,7,12), 1^v(s+5,6,12)};
      C8 1,078 = {D8(s), v(s+4,8,13), 1^v(s+5,7,13)}
                                                   (14,777 / 14,777)
      where D8(s) in the C8 line is the declared floored table
      (2 at s=6 exactly -- the C8 recursion actually realizes the
      deviant, which the collapse value absorbs).
  D9  parent proof-structure option-set inspection: m in {5..9} x
      33 shapes. m=5: opts subset of {A'=v(S-1,8,13),
      c'=1^v(S,7,13), D8(S-5)} AND the a=5 child == D8(S-5)
      (the s=6 deviant absorption is observed at face value);
      m>=6: opts == {v(S-1,8,m+8), 1^v(S,7,m+8)} exact; parent mex
      == v(S,8,m+9) both engines                    (165 / 495)
  TOTAL declared: 24,551 points / 44,135 comparisons / bad 0.
  D6c census (NOT in declared totals; bad gate = engine disagreement
  only; observations are recorded, nothing claimed):
    (a) z=9 next-lane cell tables with the proper per-cell floors:
        F9 H(11;{1}+Y;9), G9 H(12;{2}+Y;9), E9 H(13;{3}+Y;9) over
        the 330 family (tokens 3..9, arity 0..4); D9 H(14;{4}+Y;9)
        over the 126 floored family (tokens 5..9) and the loose 330
        family (decomposition-dependence record); C9 H(15;{5}+Y;9)
        over the 70 family (tokens 6..9); B9 H(16;{6}+Y;9) over the
        35 family (tokens 7..9). s-only tables, decomposition-
        dependence flags, deviant records vs v(s+k,9,R). The z=9
        strip and the F9/G9/E9/D9/C9/B9 closed forms stay OPEN
        (registered as open; not claimed).
    (b) z=9 strip grid: m in {5..10} x 96 census shapes (R=m+10):
        collapse record (m=5 is OUT of band: z*(5)=9; the (5,6)
        witness recorded; m=6 is the last band cell of its row).
    (c) m=4 negative record at z=8 over the 222 T-family: the two
        separations (4,4) (downward 0 vs 2) and (4,6) (upward 2
        vs 1) are expected and recorded.
    (d) m=5 z=9 out-of-band record over the 222 T-family: the
        single (5,6) separation (upward 2 vs 0) is expected and
        recorded.

Fail-closed: any bad>0 -> rc=1; declared-count mismatch -> rc=1
(honest record requirement). Finite machine audit is NOT the proof:
the universal claims rest on the paper proof in the declaration note
(F8/G8/E8/D8/C7/C8 closed-form ladder with the CONDITIONAL E8
recursion + mex base m=5 + option-set identity induction on m).
Standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2
{59,60}, classes 1/2/4, classes 10968/23964/2251/5343 remain
UNKNOWN at all times; node and point counts are never read as
win/loss statements. Determinism: no time, no unseeded randomness;
engine cache clears between blocks and inside large blocks.
Invoking with `tamper` as the first argument runs the 14-mutation
battery B1-B14 (each MUST be caught).
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
def F8_table(s):
    # Lemma F8 closed form (z=8 cell), s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1}.get(s, 0)

def G8_table(s):
    # Lemma G8 closed form (z=8 cell), s in {0} u {3,4,...}
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 2}.get(s, 1)

def E8_table(s):
    # Lemma E8 closed form (z=8 cell), s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1}.get(s, 0)

def D8_table(s):
    # Lemma D8 (floored family, tokens >=5): {0:0, 6:2, else collapse}
    return 2 if s == 6 else single_token(s + 4, 8, 13)

# published z=7 closed forms (K1275), used by the D8 recursions
def F7t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0}.get(s, 2)

def G7t(s):
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0}.get(s, 1)

def E7t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 2}.get(s, 0)

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
# D1: Lemma F8 full-decomposition sweep
# ---------------------------------------------------------------
def check_D1():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 10, 8
    for s in [0] + list(range(3, 41)):
        exp = F8_table(s)
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
# D2: Lemma G8 sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D2():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (2,) + Y
        exp = G8_table(s)
        hc = H_canonical(11, X, 8)
        ho = H_ordered(11, X, 8)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if G8_table(sum(Y)) != single_token(sum(Y) + 2, 8, 11))
    comps += 1
    if deviants != [(3, 3), (3, 5), (4, 4), (6,), (8,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D3: Lemma E8 sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D3():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (3,) + Y
        exp = E8_table(s)
        hc = H_canonical(12, X, 8)
        ho = H_ordered(12, X, 8)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if E8_table(sum(Y)) != single_token(sum(Y) + 3, 8, 12))
    comps += 1
    if deviants != [(3, 3), (6,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D4: Lemma D8 sweep (floored family) vs {0:0, 6:2, else collapse}
# ---------------------------------------------------------------
def check_D4():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 13, 8
    for s in [0] + list(range(5, 41)):
        exp = D8_table(s)
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
# D4b / D4c: Lemma C7 / C8 sweeps (floored family, tokens >=6)
#             full collapse v(s+5,7,13) / v(s+5,8,14)
# ---------------------------------------------------------------
def check_D4b():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 13, 7
    for s in [0] + list(range(6, 41)):
        exp = single_token(s + 5, 7, 13)
        for Y in decomps(s, 6):
            X = (5,) + Y
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

def check_D4c():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 14, 8
    for s in [0] + list(range(6, 41)):
        exp = single_token(s + 5, 8, 14)
        for Y in decomps(s, 6):
            X = (5,) + Y
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
# D5: Theorem T-Z8 grid
# ---------------------------------------------------------------
def check_D5():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 8
    for m in range(5, 11):
        R = m + 9
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
    rng = random.Random(20261126)
    z = 8
    for m in range(5, 11):
        R = m + 9
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
# K1272/K1273/K1274/K1275 machines D7a; 17 anchors)
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
# D7b: theorem anchors (47 points)
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
    # G8 deviant witnesses at s=6 (downward) and s=8 (upward)
    dev_point('G8dev6a', (2, 6), 8, 11, 0, 2)
    dev_point('G8dev6b', (2, 3, 3), 8, 11, 0, 2)
    dev_point('G8dev8a', (2, 8), 8, 11, 2, 1)
    dev_point('G8dev8b', (2, 3, 5), 8, 11, 2, 1)
    dev_point('G8dev8c', (2, 4, 4), 8, 11, 2, 1)
    # E8 deviant witnesses at s=6 (upward)
    dev_point('E8dev6a', (3, 6), 8, 12, 1, 0)
    dev_point('E8dev6b', (3, 3, 3), 8, 12, 1, 0)
    # F8 deviant witnesses at s=8 (downward)
    dev_point('F8dev8a', (1, 8), 8, 10, 1, 0)
    dev_point('F8dev8b', (1, 3, 5), 8, 10, 1, 0)
    dev_point('F8dev8c', (1, 4, 4), 8, 10, 1, 0)
    # D8 deviant witness at s=6 (upward; same position as the m=4
    # z=8 upward negative)
    dev_point('D8dev6', (4, 6), 8, 13, 2, 1)
    # m=4 z=8 negative: the downward witness
    dev_point('m4neg', (4, 4), 8, 13, 0, 2)
    # m=5 z=9 out-of-band upward witness (frontier s=6 shape joins
    # the front witness -- census observation anchor)
    dev_point('m5z9oob', (5, 6), 9, 15, 2, 0)
    # F8 cells
    for Y, s in [((3,), 3), ((4,), 4), ((5,), 5), ((6,), 6),
                 ((7,), 7)]:
        std_point('F8', (1,) + Y, 8, 10, F8_table(s))
    # G8 cells
    std_point('G8', (2, 3), 8, 11, G8_table(3))
    std_point('G8', (2, 5), 8, 11, G8_table(5))
    std_point('G8', (2, 7), 8, 11, G8_table(7))
    std_point('G8', (2, 5, 5), 8, 11, G8_table(10))
    # E8 cells
    std_point('E8', (3,), 8, 12, E8_table(0))
    std_point('E8', (3, 3), 8, 12, E8_table(3))
    std_point('E8', (3, 5), 8, 12, E8_table(5))
    std_point('E8', (3, 3, 3), 8, 12, E8_table(6))
    # D8 cells (floored: tokens >=5)
    std_point('D8', (4,), 8, 13, D8_table(0))
    std_point('D8', (4, 5), 8, 13, D8_table(5))
    std_point('D8', (4, 5, 5), 8, 13, D8_table(10))
    std_point('D8', (4, 6, 8), 8, 13, D8_table(14))
    # C7 cells (floored: tokens >=6)
    std_point('C7', (5,), 7, 13, single_token(5, 7, 13))
    std_point('C7', (5, 6), 7, 13, single_token(11, 7, 13))
    std_point('C7', (5, 6, 8), 7, 13, single_token(19, 7, 13))
    # C8 cells (floored: tokens >=6)
    std_point('C8', (5,), 8, 14, single_token(5, 8, 14))
    std_point('C8', (5, 6), 8, 14, single_token(11, 8, 14))
    std_point('C8', (5, 6, 8), 8, 14, single_token(19, 8, 14))
    # m=5 single token + bottom parents at z=8, R=14
    std_point('m5', (5,), 8, 14, single_token(5, 8, 14))
    std_point('m5p', (5, 6), 8, 14, single_token(11, 8, 14))
    std_point('m5p', (5, 5, 5), 8, 14, single_token(15, 8, 14))
    # bottom children: (i) A-on-5 stair child (A' ladder rung);
    # (iii) c'-hand child = published T-Z7 position
    std_point('m5A', (5, 5), 8, 13, single_token(10, 8, 13))
    std_point('m5C', (5, 6), 7, 13, single_token(11, 7, 13))
    # published z=7 continuity anchors (K1275 F7/G7/E7 cells)
    std_point('z7', (1, 8), 7, 9, F7t(8))
    std_point('z7', (2, 8), 7, 10, G7t(8))
    std_point('z7', (3, 6), 7, 11, E7t(6))
    # induction parents
    std_point('ind', (6, 6), 8, 15, single_token(12, 8, 15))
    std_point('ind', (8, 8), 8, 17, single_token(16, 8, 17))
    std_point('ind', (7, 7, 9), 8, 16, single_token(23, 8, 16))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D8: cell recursion option-set identity (proof secs 2.1-2.6)
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
            exp = expfun(Y, s)
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
    cell_opts(10, (1,), 8,
              lambda Y, s: {single_token(s, 9, 9), single_token(s, 8, 9),
                            1 ^ F7t(s)}, famF, 'F8')
    clear_engines()
    cell_opts(11, (2,), 8,
              lambda Y, s: {F8_table(s), single_token(s + 1, 8, 10),
                            1 ^ G7t(s)}, famF, 'G8')
    clear_engines()
    def e8_exp(Y, s):
        exp = {G8_table(s), 1 ^ E7t(s)}
        if any(t >= 4 for t in Y):
            exp.add(single_token(s + 2, 8, 11))
        return exp
    cell_opts(12, (3,), 8, e8_exp, famF, 'E8')
    clear_engines()
    famD = []
    for s in [0] + list(range(5, 41)):
        famD.extend(decomps(s, 5))
    cell_opts(13, (4,), 8,
              lambda Y, s: {single_token(s + 3, 8, 12), E8_table(s),
                            1 ^ single_token(s + 4, 7, 12)}, famD, 'D8')
    clear_engines()
    famC = []
    for s in [0] + list(range(6, 41)):
        famC.extend(decomps(s, 6))
    cell_opts(13, (5,), 7,
              lambda Y, s: {single_token(s + 4, 7, 12),
                            1 ^ single_token(s + 5, 6, 12)}, famC, 'C7')
    clear_engines()
    cell_opts(14, (5,), 8,
              lambda Y, s: {D8_table(s), single_token(s + 4, 8, 13),
                            1 ^ single_token(s + 5, 7, 13)}, famC, 'C8')
    clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D9: parent proof-structure option-set inspection
# ---------------------------------------------------------------
def check_D9():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 8
    for m in range(5, 10):
        R = m + 9
        for X in D9_shapes(m):
            S = sum(X)
            opts = child_opts_ordered(X, z, R)
            vp = single_token(S, z, R)
            ho = H_ordered(R, X, z)
            hc = H_canonical(R, X, z)
            if m == 5:
                Ap = single_token(S - 1, 8, 13)
                cp = 1 ^ single_token(S, 7, 13)
                Dv = D8_table(S - 5)
                a5 = am_child_value(X, 5, z, R)
                rel_ok = (opts <= {Ap, cp, Dv}) and (a5 == Dv)
                rel_tag = 'subset+D8'
                expected = sorted({Ap, cp, Dv})
            else:
                A = single_token(S - 1, 8, m + 8)
                C = 1 ^ single_token(S, 7, m + 8)
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
# observations only, no strip/closed-form claims on z=9)
# ---------------------------------------------------------------
def check_D6c():
    res = {}
    pts = comps = bad = 0
    # (a) z=9 next-lane cell tables with proper per-cell floors
    cells = {}
    for tag, pre, R, dvoff, tmin, tmax in [
            ('F9', (1,), 11, 1, 3, 9), ('G9', (2,), 12, 2, 3, 9),
            ('E9', (3,), 13, 3, 3, 9), ('D9', (4,), 14, 4, 5, 9),
            ('C9', (5,), 15, 5, 6, 9), ('B9', (6,), 16, 6, 7, 9)]:
        fam = Y_tokens(tmin, tmax)
        tbl = {}
        devs = []
        for Y in fam:
            s = sum(Y)
            X = pre + Y
            hc = H_canonical(R, X, 9)
            ho = H_ordered(R, X, 9)
            comps += 2
            if hc != ho:
                bad += 1
            tbl.setdefault(s, set()).add(hc)
            if hc != single_token(s + dvoff, 9, R):
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
    # (a2) D9 loose family (tokens 3..9): decomposition-dependence
    fam = Y_tokens(3, 9)
    tbl = {}
    devs = []
    for Y in fam:
        s = sum(Y)
        hc = H_canonical(14, (4,) + Y, 9)
        ho = H_ordered(14, (4,) + Y, 9)
        comps += 2
        if hc != ho:
            bad += 1
        tbl.setdefault(s, set()).add(hc)
        if hc != single_token(s + 4, 9, 14):
            devs.append(list(Y))
    dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
    tbl2 = {s: sorted(v) for s, v in sorted(tbl.items()) if s <= 20}
    cells['D9_loose'] = {'R': 14, 'floor': 3, 'family': len(fam),
                         'table_s20': {str(k): v for k, v in tbl2.items()},
                         'decomp_dependent_s': dep,
                         'deviant_count': len(devs),
                         'deviants_vs_collapse': devs[:40]}
    pts += len(fam)
    res['z9_cells'] = cells
    clear_engines()
    # (b) z=9 strip grid: m in {5..10} x 96 census shapes
    strip = {}
    for m in range(5, 11):
        z, R = 9, m + 10
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
    res['z9_strip'] = strip
    # (c) m=4 negative record at z=8 over the 222 T-family
    neg = []
    mneg = 0
    for X in T_shapes(4):
        S = sum(X)
        hc = H_canonical(13, X, 8)
        ho = H_ordered(13, X, 8)
        comps += 2
        mneg += 1
        if hc != ho:
            bad += 1
        if hc != single_token(S, 8, 13):
            neg.append([list(X), hc, single_token(S, 8, 13)])
    res['m4_z8_negative'] = {'total': mneg, 'separations': neg}
    pts += mneg
    clear_engines()
    # (d) m=5 z=9 out-of-band record over the 222 T-family
    neg9 = []
    mneg9 = 0
    for X in T_shapes(5):
        S = sum(X)
        hc = H_canonical(15, X, 9)
        ho = H_ordered(15, X, 9)
        comps += 2
        mneg9 += 1
        if hc != ho:
            bad += 1
        if hc != single_token(S, 9, 15):
            neg9.append([list(X), hc, single_token(S, 9, 15)])
    res['m5_z9_out_of_band'] = {'total': mneg9, 'separations': neg9}
    pts += mneg9
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'note': ('census observation only; z=9 strip for m>=6 and '
                     'the F9/G9/E9/D9/C9/B9 closed forms are NOT '
                     'claimed (registered open); m=5 z=9 is out of '
                     'band (z*(5)=9)'),
            'census': res}

# =====================================================================
# tamper battery B1-B14 (each mutation MUST be caught; rc=1 otherwise)
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

    # B1: F8 table s=8 corruption (1 -> 0; hides the s=8 deviant)
    bad = 0
    for Y in decomps(8, 3):
        if H_canonical(10, (1,) + Y, 8) != 0:
            bad += 1
    rec('B1 F8(8) corruption (1->0)', bad)
    clear_engines()
    # B2: F8(s>=9) corruption (0 -> 1)
    bad = 0
    for s in range(9, 17):
        for Y in decomps(s, 3):
            if H_canonical(10, (1,) + Y, 8) != 1:
                bad += 1
        clear_engines()
    rec('B2 F8(s>=9) corruption (0->1)', bad)
    # B3: G8(6) flip (0 -> 2; disguises the s=6 downward deviant as
    #     the collapse value)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 2 if sum(Y) == 6 else G8_table(sum(Y))
        if H_canonical(11, (2,) + Y, 8) != exp:
            bad += 1
    rec('B3 G8(6) flip (0->2)', bad)
    clear_engines()
    # B4: G8 mis-claimed as the R2-form collapse (caught at s in {6,8})
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(11, (2,) + Y, 8) != single_token(s + 2, 8, 11):
            bad += 1
    rec('B4 G8 mis-claimed collapse v(s+2,8,11)', bad)
    # B5: G8(8) flip (2 -> 1; hides the s=8 upward deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 1 if sum(Y) == 8 else G8_table(sum(Y))
        if H_canonical(11, (2,) + Y, 8) != exp:
            bad += 1
    rec('B5 G8(8) flip (2->1)', bad)
    clear_engines()
    # B6: E8(6) flip (1 -> 0; hides the s=6 deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 0 if sum(Y) == 6 else E8_table(sum(Y))
        if H_canonical(12, (3,) + Y, 8) != exp:
            bad += 1
    rec('B6 E8(6) flip (1->0)', bad)
    # B7: E8 mis-claimed as collapse v(s+3,8,12)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(12, (3,) + Y, 8) != single_token(s + 3, 8, 12):
            bad += 1
    rec('B7 E8 mis-claimed collapse v(s+3,8,12)', bad)
    clear_engines()
    # B8: D8 mis-claimed as a FULL collapse (falsely D8(6)=1);
    #     the floored sweep catches it at s=6
    bad = 0
    for s in [0] + list(range(5, 21)):
        for Y in decomps(s, 5):
            if H_canonical(13, (4,) + Y, 8) != single_token(s + 4, 8, 13):
                bad += 1
        clear_engines()
    rec('B8 D8 mis-claimed full collapse (D8(6)=1)', bad)
    # B9: T-Z8 min=4 extension (the two separations (4,4)/(4,6))
    bad = 0
    for X in T_shapes(4):
        if H_canonical(13, X, 8) != single_token(sum(X), 8, 13):
            bad += 1
    rec('B9 T-Z8 min=4 extension witnesses (4,4)/(4,6)', bad)
    clear_engines()
    # B10: ordered engine without the C-move XOR
    bad = 0
    for X in [(3, 3), (3, 4), (3, 3, 3), (2, 3), (4, 5), (2, 6)]:
        for z in (3, 4, 5, 6, 7, 8):
            for R in range(1, 10):
                if H_ordered_noXOR(R, X, z) != H_canonical(R, X, z):
                    bad += 1
    rec('B10 ordered engine C-move XOR removed', bad)
    H_ordered_noXOR.cache_clear()
    clear_engines()
    # B11: corrupted q_odd closed form
    bad = 0
    for x in range(2, 41):
        for z in range(1, 31):
            for R in range(0, min(x + z, 31) + 1):
                if single_token_qmut(x, z, R) != vC(x, z, R): bad += 1
    rec('B11 q_odd corruption', bad)
    # B12: D9 a=m child identity mutations (m=5: the E8-cell value
    #      instead of the D8-cell value; m>=6: budget m+7 instead of
    #      m+8)
    bad = 0
    for m in range(5, 9):
        R = m + 9
        for X in D9_shapes(m):
            S = sum(X)
            a_m = am_child_value(X, m, 8, R)
            if m == 5:
                exp_mut = E8_table(S - 5)
            else:
                exp_mut = single_token(S - 1, 8, m + 7)
            if a_m != exp_mut:
                bad += 1
        clear_engines()
    rec('B12 D9 a=m child identity mutation (E8-cell/budget-off)', bad)
    # B13: C7/C8 mis-claimed as constant-0 tables (the D4b/D4c
    #      expectation side destroyed; C7(0)=C8(0)=1)
    bad = 0
    for s in [0] + list(range(6, 21)):
        for Y in decomps(s, 6):
            if H_canonical(13, (5,) + Y, 7) != 0:
                bad += 1
            if H_canonical(14, (5,) + Y, 8) != 0:
                bad += 1
        clear_engines()
    rec('B13 C7/C8 mis-claimed constant-0 tables', bad)
    # B14: C8 C-hand child mis-specified as 1^D7(s)=1^v(s+4,7,12)
    #      (the z=7 dependency of the C8 recursion forged); the
    #      option-set identity check catches it (e.g. at s=6)
    bad = 0
    for s in [0] + list(range(6, 21)):
        for Y in decomps(s, 6):
            opts = child_opts_ordered((5,) + Y, 8, 14)
            exp = {D8_table(s), single_token(s + 4, 8, 13),
                   1 ^ single_token(s + 4, 7, 12)}
            if opts != exp:
                bad += 1
        clear_engines()
    rec('B14 C8 C-hand child mis-specified 1^D7(s)', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed:
        sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
DECLARED_TOTALS = {'points': 24551, 'comparisons': 44135}

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
    res['D4b'] = check_D4b()
    clear_engines()
    res['D4c'] = check_D4c()
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
    gated = ('D1', 'D2', 'D3', 'D4', 'D4b', 'D4c', 'D5', 'D6',
             'D7a', 'D7b', 'D8', 'D9')
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
        'theorem': ('Lemma F8/G8/E8/D8 (floored, first NON-'
                    'collapsing rung with the single s=6 upward '
                    'deviant)/C7/C8 (full collapses) + Theorem '
                    'T-Z8: min>=5 critical-strip z=8 slice; the '
                    'm=5 row of K1268 Conjecture C1 fully resolved '
                    'incl. its last band cell z=8 (z*(5)=9) via the '
                    'conditional-E8 z=8 ladder + the C7/C8 full-'
                    'collapse cells contributed by this note + mex '
                    'base m=5 (D8 s=6 deviant absorbed) + option-set '
                    'identity induction. Universal claims proved on '
                    'paper in the declaration note; this finite '
                    'audit corroborates.'),
        'declared_totals': DECLARED_TOTALS,
        'observed_totals': {'points': pts, 'comparisons': comps},
        'census': {'points': res['D6c_census']['points'],
                   'comparisons': res['D6c_census']['comparisons'],
                   'bad_engine': census_bad},
        'unknown_statement': ('standard 11x11 empty board, two-stone '
                              'roots {49,60}/{59,60}, S2 {59,60}, '
                              'classes 1/2/4, classes 10968/23964/'
                              '2251/5343: UNKNOWN at all times'),
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
