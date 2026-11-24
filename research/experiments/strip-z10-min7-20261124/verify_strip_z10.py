#!/usr/bin/env python3
"""verify_strip_z10.py -- machine audit for the declared claims of the
single-owner declaration note (K1278 provisional; min>=7 critical-strip
z=10 slice; declaration note:
research/log/2026-11-24-strip-z10-min7-single-owner-note.md):

  Lemma F10: F10(s) := H(12;{1}+Y;10) (Y tokens >=3, arity free, Y=()
             for s=0) is independent of the decomposition of s and
             F10(0)=1, F10(3)=0, F10(4)=1, F10(5)=0, F10(6)=1,
             F10(7)=0, F10(8)=1, F10(9)=0, F10(10)=1, F10(s>=11)=0.
             Vs the Sigma-collapse v(s+1,10,12) the single s=10
             UPWARD deviant 1>0 covers exactly the 5-decomposition
             family {(10,),(3,7),(4,6),(5,5),(3,3,4)} -- the DEATH
             of the F-rank persistent-2 (the z=9 F9 kept every
             s>=10 at 2; z=10 sinks to 0 from s=11 on after one
             last blip at s=10). Extends the published F-ladder
             (F z in {1..4} K1272, F5 K1273, F6 K1274, F7 K1275,
             F8 K1276, F9 K1277).
  Lemma G10: G10(s) := H(13;{2}+Y;10) depends only on s and
             G10(0)=0, G10(3)=1, G10(4)=0, G10(5)=1, G10(6)=0,
             G10(7)=1, G10(8)=0, G10(9)=1, G10(10)=2,
             G10(s>=11)=1. Vs the R2-form collapse v(s+2,10,13)
             the deviation set is TWO-SIDED and co-resident in one
             rung for the first time in the G-rank: s=8 DOWNWARD
             0<2 over {(8,),(3,5),(4,4)} and s=10 UPWARD 2>1 over
             {(3,7),(4,6),(5,5),(3,3,4)} (the census family; the
             full-decomposition family adds (2,10) and the F10
             s=10 deviant realizes as the first F->G deviant chain
             pushing the mex to 2).
  Lemma E10: E10(s) := H(14;{3}+Y;10) depends only on s and
             E10(0)=1, E10(3)=0, E10(4)=1, E10(5)=0, E10(6)=1,
             E10(7)=0, E10(8)=1, E10(s>=9)=0. The single s=8
             UPWARD deviant 1>0 covers exactly {(8,),(3,5),(4,4)}
             (the z=9 E9 had s in {6,8}; z=10 keeps only s=8).
             The E10 recursion expectation is CONDITIONAL:
             {G10(s), 1^E9(s)} plus ({v(s+2,10,13)} iff some Y
             token is >= 4); the UNCONDITIONAL ghost form coincides
             with the conditional form over the full 3,657 family
             at z=10 (mismatch 0), the SECOND consecutive agreeing
             slice (z=9, z=10) after the z=8 break at Y=(3,3).
  Lemma D10: the first TWO-DEVIANT floored D-rung, two-sided:
             D10(s) := H(15;{4}+Y;10) with ALL Y tokens >=5 (s in
             {0} u {5,6,...}) depends only on s with table
             {6:0, 8:2, else v(s+4,10,15)} -- the s=6 DOWNWARD
             deviant D10(6)=0 != v(10,10,15)=2 (second consecutive
             slice, direction stable) PLUS the s=8 UPWARD deviant
             D10(8)=2 != v(12,10,15)=1: the E10 s=8 deviant is NOT
             absorbed by the parent mex and FRUITS as a parent
             deviant (z=9 absorbed E9(8)=2 into the collapse).
             The floor min(Y)>=5 is essential: loosened to tokens
             >=3 the decomposition-dependence at s in {8,10}
             enters (loose census record; same positions as the
             published D8/D9 loose records).
  Lemma C10: C10(s) := H(16;{5}+Y;10) with ALL Y tokens >=6 depends
             only on s with table {0:1, 6:1, else v(s+5,10,16)} --
             the SINGLE s=6 upward deviant C10(6)=1>0 realizes the
             D10 s=6 downward deviant as a child value and the
             parent mex absorbs it with an UPWARD flip for the
             SECOND consecutive slice (z=9: D9(6)=0 -> C9(6)=2;
             z=10: D10(6)=0 -> C10(6)=1; the absorbed value decays
             2 -> 1 but the reversal structure continues). The
             position H(16;{5,6};10) is the same shape as the
             m=5 z=10 out-of-band witness.
  Lemma B10: B10(s) := H(17;{6}+Y;10) with ALL Y tokens >=7 FULLY
             collapses: B10(s) = v(s+6,10,17). SECOND consecutive
             full-collapse B-rung (B9 z=9, B10 z=10), floor >=7
             unchanged.
  Lemma A10: A10(s) := H(18;{7}+Y;10) with ALL Y tokens >=8 FULLY
             collapses: A10(s) = v(s+7,10,18). FIRST full-collapse
             A-rung; the first slice with TWO full-collapse rungs
             (B10+A10). The A10 C-hand child 1^v(s+7,9,17) is the
             published T-Z9 (K1277) THEOREM position H(17;{7}+Y;9)
             -- the deepest strip-theorem dependency chain so far
             (z=9 B9 pulled T-Z8; z=10 B10 pulls the published
             cell table B9; z=10 A10 pulls T-Z9).
  Theorem T-Z10: for ALL m>=7, every nonempty finite multiset X
             with min(X)=m: H(m+11;X;10) = v(sum X, 10, m+11).
             Base m=7 is the FIRST TRIVIAL-ABSORPTION base (a=7
             child = B10t(S-7) = v(S-1,10,17) == the stair option
             EXACTLY, by the B10 full collapse -- the base uses NO
             deviant child, unlike the K1273/K1276/K1277
             deviant-absorption bases; the C-hand child is the
             published T-Z9). m>=8 by option-set identity induction
             on m (a=m child = C(m-1,10) at R=m+10=(m-1)+11,
             a>m children by K1264, C-hand child by published
             T-Z9) with option set {v(S-1,10,m+10),
             1^v(S,9,m+10)} exactly.
  Corollary: the z=10 slice is determined for all m>=7; the m=7
             row of K1268 Conjecture C1 is determined for
             z in {0..10} leaving exactly {11,12} open; m>=8 rows
             keep z in {11..z*(m)-1} open. Out-of-band records:
             m=6 z=10 witness (6,6): parent 2 vs single 1 (K1277
             published, re-recorded); m=5 z=10 witness (5,6):
             parent 1 vs single 0 (amplitude decay from the z=9
             2 vs 0, sign unchanged); m=6 z=11 census witness
             (6,6): parent 0 vs single 1 (SIGN FLIP, registered
             for the next lane).

Declared checks (PUBLISH-THEN-EXECUTE):
  D1  Lemma F10: s in {0} u {3..40}, ALL decompositions into 1..4
      tokens >=3 (3,657)                          (3,657 / 10,971)
  D2  Lemma G10: Y = tokens 3..9 multisets, arity 0..4 (330) vs
      G10 table; +1 arithmetic deviant-set comparison:
      {Y: G10 != v(s+2,10,13)} == {(3,3,4),(3,5),(3,7),(4,4),
      (4,6),(5,5),(8,)} (the (2,10) full-decomposition deviant is
      OUTSIDE the census family; recorded in D7b/D8)
                                                      (330 / 991)
  D3  Lemma E10: same 330 shapes vs E10 table; +1 arithmetic
      deviant set == {(3,5),(4,4),(8,)}; +1 E10 unconditional
      ghost-form mismatch counter == 0 over the same family
                                                      (330 / 992)
  D4  Lemma D10: s in {0} u {5..40}, ALL decompositions into 1..4
      tokens >=5 (1,650) vs {6:0, 8:2, else v(s+4,10,15)}
                                                     (1,650 / 4,950)
  D4b Lemma C10: s in {0} u {6..40}, ALL decompositions into 1..4
      tokens >=6 (1,078) vs {0:1, 6:1, else v(s+5,10,16)}
                                                     (1,078 / 3,234)
  D4c Lemma B10: s in {0} u {7..40}, ALL decompositions into 1..4
      tokens >=7 (700) vs full collapse v(s+6,10,17)
                                                       (700 / 2,100)
  D4d Lemma A10: s in {0} u {8..40}, ALL decompositions into 1..4
      tokens >=8 (460) vs full collapse v(s+7,10,18)
                                                       (460 / 1,380)
  D5  Theorem T-Z10 grid: m in {7..12} x z=10 x 222 shapes
      (R=m+11)                                     (1,332 / 3,996)
  D6  fixed-seed (20261129) random deep: m in {7..12} x 15 shapes
      (arity 4..5, tokens in [m,m+15], one token fixed at m)
                                                      (90 / 270)
  D7a published K1264/K1268/K1271-K1276 witness anchors (17; the
      same table as the published machines)         (17 / 85)
  D7b theorem anchors 75 points (22 deviant/witness pair anchors +
      53 standard anchors: the F10 s=10 upward deviants
      {(10,),(3,7),(4,6),(5,5),(3,3,4)} and the persistent-2 death
      anchor (1,11); the G10 s=8 downward + s=10 upward deviants
      including the census-exterior (2,10); the E10 s=8 upward
      deviants; the D10 s=6 downward + s=8 upward deviants; the
      C10 s=6 upward deviant (same position as the m=5 z=10
      out-of-band witness); the m=6 z=10 out-of-band witness
      (6,6); F10/G10/E10/D10/C10/B10/A10 cells, the m=7 single
      token and bottom parents, the bottom stair / a=7 / C-hand
      children (the trivial-absorption core at face value), the
      published z=9 continuity, and the induction parents)
                                                      (75 / 225)
  D8  cell recursion option-set identity (paper proof secs
      2.1-2.7), 1 comparison per point (ordered child option set
      == arithmetic expectation set):
      F10 3,657 = {v(s,11,11), v(s,10,11), 1^F9(s)};
      G10 3,657 = {F10(s), v(s+1,10,12), 1^G9(s)};
      E10 3,657 = CONDITIONAL {G10(s), 1^E9(s)}
                  + ({v(s+2,10,13)}: some Y token >= 4);
      D10 1,650 = {v(s+3,10,14), E10(s), 1^D9(s)};
      C10 1,078 = {v(s+4,10,15), D10(s), 1^C9(s)};
      B10   700 = {v(s+5,10,16), C10(s), 1^B9(s)};
      A10   460 = {v(s+6,10,17), B10(s), 1^v(s+7,9,17)}
      where the z=9 tables in the recursions are the PUBLISHED
      K1277 closed forms (the A10 C-hand line is the published
      T-Z9 theorem position -- the deepest strip-theorem
      dependency in the ladder).
                                                (14,859 / 14,859)
  D9  parent proof-structure option-set inspection: m in {7..11} x
      33 shapes. m=7: opts subset of {A'=v(S-1,10,17),
      c'=1^v(S,9,17), B10t(S-7)} AND the a=7 child == B10t(S-7)
      (the TRIVIAL ABSORPTION observed at face value: the base
      uses no deviant child); m>=8: opts == {v(S-1,10,m+10),
      1^v(S,9,m+10)} exact; parent mex == v(S,10,m+11) both
      engines                                        (165 / 495)
  TOTAL declared: 24,743 points / 44,548 comparisons / bad 0.
  D6c census (NOT in declared totals; bad gate = engine disagreement
  only; observations are recorded, nothing claimed):
    (a) z=11 next-lane cell tables with the proper per-cell floors:
        F11 H(13;{1}+Y;11), G11 H(14;{2}+Y;11), E11 H(15;{3}+Y;11)
        over the 330 family (tokens 3..9, arity 0..4); D11
        H(16;{4}+Y;11) over the 126 floored family (tokens 5..9)
        and the loose 330 family (decomposition-dependence
        record); C11 H(17;{5}+Y;11) over the 70 family (tokens
        6..9); B11 H(18;{6}+Y;11) over the 35 family (tokens
        7..9); A11 H(19;{7}+Y;11) over the 15 family (tokens
        8..9). s-only tables, decomposition-dependence flags,
        deviant records vs v(s+k,11,R). The z=11 closed forms and
        the z=11 strip stay OPEN (registered open; not claimed;
        the pre-declaration probe observed F11 310/330 deviants
        -- the first large F-rank split from v -- G11 4, E11 7,
        D11 floored 1, C11 2, D11_loose decomposition-dependence
        at s=10, B11/A11 census collapse).
    (b) z=11 strip grid: m in {6..11} x 96 census shapes (R=m+12):
        collapse record (m=6 is OUT of band: z*(6)=10, witness
        (6,6) parent 0 vs single 1 -- the SIGN FLIP of the z=10
        +1 witness; m>=7 in band 96/96 collapse expected from the
        probe but recorded only, not claimed).
    (c) m=6 z=10 out-of-band record over the 222 T-family (R=17):
        the single (6,6) separation (upward 2 vs 1) is expected
        and recorded (the frontier s=6 shape; published K1277
        re-record).
    (d) m=5 z=10 out-of-band record over the 222 T-family (R=16):
        the single (5,6) separation (parent 1 vs single 0;
        amplitude decay from the published z=9 2 vs 0, sign
        unchanged) is expected and recorded.
    (e) E10 UNCONDITIONAL ghost form observation over the full
        3,657 family: mismatch count vs the conditional form
        (z=8 broke at Y=(3,3); z=9 recorded mismatch 0; z=10
        declared mismatch 0 and re-recorded -- SECOND consecutive
        agreeing slice; nothing claimed about z>=11).

Fail-closed: any bad>0 -> rc=1; declared-count mismatch -> rc=1
(honest record requirement). Finite machine audit is NOT the proof:
the universal claims rest on the paper proof in the declaration note
(F10/G10/E10/DTD/C10/B10/A10 closed-form ladder with the CONDITIONAL
E10 recursion + trivial-absorption base m=7 + option-set identity
induction on m). Standard 11x11 empty board, two-stone roots
{49,60}/{59,60}, S2 {59,60}, classes 1/2/4, classes 10968/23964/
2251/5343 remain UNKNOWN at all times; node and point counts are
never read as win/loss statements. Determinism: no time, no unseeded
randomness; engine cache clears between blocks and inside large
blocks. Invoking with `tamper` as the first argument runs the
14-mutation battery B1-B14 (each MUST be caught).
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
def F10_table(s):
    # Lemma F10 closed form (z=10 cell), s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1,
            9: 0, 10: 1}.get(s, 0)

def G10_table(s):
    # Lemma G10 closed form (z=10 cell), s in {0} u {3,4,...}
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0,
            9: 1, 10: 2}.get(s, 1)

def E10_table(s):
    # Lemma E10 closed form (z=10 cell), s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1}.get(s, 0)

def D10_table(s):
    # Lemma D10 (floored family, tokens >=5):
    # {6:0, 8:2, else collapse v(s+4,10,15)}
    if s == 6:
        return 0
    if s == 8:
        return 2
    return single_token(s + 4, 10, 15)

def C10_table(s):
    # Lemma C10 (floored family, tokens >=6):
    # {0:1, 6:1, else collapse v(s+5,10,16)}
    return 1 if s == 6 else single_token(s + 5, 10, 16)

def B10_table(s):
    # Lemma B10 (floored family, tokens >=7): full collapse
    return single_token(s + 6, 10, 17)

def A10_table(s):
    # Lemma A10 (floored family, tokens >=8): full collapse
    return single_token(s + 7, 10, 18)

# published z=9 closed forms (K1277), used by the z=10 recursions
def F9t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1, 9: 0}.get(s, 2)

def G9t(s):
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0, 9: 1}.get(s, 1)

def E9t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 2}.get(s, 0)

def D9t(s):
    return 0 if s == 6 else single_token(s + 4, 9, 14)

def C9t(s):
    return 2 if s == 6 else single_token(s + 5, 9, 15)

def B9t(s):
    return single_token(s + 6, 9, 16)

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
# D1: Lemma F10 full-decomposition sweep
# ---------------------------------------------------------------
def check_D1():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 12, 10
    for s in [0] + list(range(3, 41)):
        exp = F10_table(s)
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
# D2: Lemma G10 sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D2():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (2,) + Y
        exp = G10_table(s)
        hc = H_canonical(13, X, 10)
        ho = H_ordered(13, X, 10)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if G10_table(sum(Y)) != single_token(sum(Y) + 2, 10, 13))
    comps += 1
    if deviants != [(3, 3, 4), (3, 5), (3, 7), (4, 4),
                    (4, 6), (5, 5), (8,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D3: Lemma E10 sweep + arithmetic deviant set + ghost counter
# ---------------------------------------------------------------
def check_D3():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (3,) + Y
        exp = E10_table(s)
        hc = H_canonical(14, X, 10)
        ho = H_ordered(14, X, 10)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if E10_table(sum(Y)) != single_token(sum(Y) + 3, 10, 14))
    comps += 1
    if deviants != [(3, 5), (4, 4), (8,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    # E10 unconditional ghost-form mismatch counter (330 family):
    # declared 0 (2nd consecutive agreeing slice after the z=8 break)
    mm = 0
    for Y in fam:
        s = sum(Y)
        opts = child_opts_ordered((3,) + Y, 10, 14)
        expu = {G10_table(s), 1 ^ E9t(s),
                single_token(s + 2, 10, 13)}
        if opts != expu:
            mm += 1
    comps += 1
    if mm != 0:
        bad += 1
        details.append(('ghost_mismatch', mm))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'uncond_ghost_mismatch_330': mm,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D4: Lemma D10 sweep (floored family) vs
#     {6:0, 8:2, else collapse v(s+4,10,15)}
# ---------------------------------------------------------------
def check_D4():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 15, 10
    for s in [0] + list(range(5, 41)):
        exp = D10_table(s)
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
# D4b: Lemma C10 sweep (floored family, tokens >=6)
#       vs {0:1, 6:1, else collapse v(s+5,10,16)}
# ---------------------------------------------------------------
def check_D4b():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 16, 10
    for s in [0] + list(range(6, 41)):
        exp = C10_table(s)
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
# D4c: Lemma B10 sweep (floored family, tokens >=7)
#       full collapse v(s+6,10,17)
# ---------------------------------------------------------------
def check_D4c():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 17, 10
    for s in [0] + list(range(7, 41)):
        exp = B10_table(s)
        for Y in decomps(s, 7):
            X = (6,) + Y
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
# D4d: Lemma A10 sweep (floored family, tokens >=8)
#       full collapse v(s+7,10,18)
# ---------------------------------------------------------------
def check_D4d():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 18, 10
    for s in [0] + list(range(8, 41)):
        exp = A10_table(s)
        for Y in decomps(s, 8):
            X = (7,) + Y
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
# D5: Theorem T-Z10 grid
# ---------------------------------------------------------------
def check_D5():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 10
    for m in range(7, 13):
        R = m + 11
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
    rng = random.Random(20261129)
    z = 10
    for m in range(7, 13):
        R = m + 11
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
# K1264/K1268/K1271-K1276/K1277 machines D7a; 17 anchors)
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
# D7b: theorem anchors (75 points: 22 deviant/witness pair anchors
#      + 53 standard anchors)
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
    # F10 s=10 upward deviants (1 > 0): the persistent-2 death blip
    dev_point('F10dev10a', (1, 10), 10, 12, 1, 0)
    dev_point('F10dev10b', (1, 3, 7), 10, 12, 1, 0)
    dev_point('F10dev10c', (1, 4, 6), 10, 12, 1, 0)
    dev_point('F10dev10d', (1, 5, 5), 10, 12, 1, 0)
    dev_point('F10dev10e', (1, 3, 3, 4), 10, 12, 1, 0)
    # F10 persistent-2 death anchor: s>=11 sinks to the collapse
    dev_point('F10death11', (1, 11), 10, 12, 0, 0)
    # G10 s=8 downward deviants (0 < 2)
    dev_point('G10dev8a', (2, 8), 10, 13, 0, 2)
    dev_point('G10dev8b', (2, 3, 5), 10, 13, 0, 2)
    dev_point('G10dev8c', (2, 4, 4), 10, 13, 0, 2)
    # G10 s=10 upward deviants (2 > 1): includes the census-exterior
    # (2,10) -- the first F->G deviant chain pushing mex to 2
    dev_point('G10dev10a', (2, 10), 10, 13, 2, 1)
    dev_point('G10dev10b', (2, 3, 7), 10, 13, 2, 1)
    dev_point('G10dev10c', (2, 4, 6), 10, 13, 2, 1)
    dev_point('G10dev10d', (2, 5, 5), 10, 13, 2, 1)
    dev_point('G10dev10e', (2, 3, 3, 4), 10, 13, 2, 1)
    # E10 s=8 upward deviants (1 > 0)
    dev_point('E10dev8a', (3, 8), 10, 14, 1, 0)
    dev_point('E10dev8b', (3, 3, 5), 10, 14, 1, 0)
    dev_point('E10dev8c', (3, 4, 4), 10, 14, 1, 0)
    # D10 two-sided deviants: s=6 downward (0 < 2), s=8 upward
    # (2 > 1; the E10 s=8 deviant fruits at the parent)
    dev_point('D10dev6', (4, 6), 10, 15, 0, 2)
    dev_point('D10dev8', (4, 8), 10, 15, 2, 1)
    # C10 s=6 upward deviant (1 > 0; D10(6)=0 flipped again,
    # 2nd consecutive reversive absorption, absorbed value decays
    # 2 -> 1); same position as the m=5 z=10 out-of-band witness
    dev_point('C10dev6/m5z10oob', (5, 6), 10, 16, 1, 0)
    # m=6 z=10 out-of-band upward witness (frontier s=6 shape)
    dev_point('m6z10oob', (6, 6), 10, 17, 2, 1)
    # m=5 z=10 out-of-band witness (amplitude decay 2 -> 1 vs the
    # published z=9 2-vs-0, sign unchanged)
    dev_point('m5z10oob', (5, 6), 10, 16, 1, 0)
    # F10 cells
    for Y, s in [((3,), 3), ((4,), 4), ((5,), 5), ((6,), 6),
                 ((8,), 8), ((9,), 9), ((12,), 12)]:
        std_point('F10', (1,) + Y, 10, 12, F10_table(s))
    # G10 cells
    std_point('G10', (2,), 10, 13, G10_table(0))
    std_point('G10', (2, 3), 10, 13, G10_table(3))
    std_point('G10', (2, 4), 10, 13, G10_table(4))
    std_point('G10', (2, 5), 10, 13, G10_table(5))
    std_point('G10', (2, 9), 10, 13, G10_table(9))
    std_point('G10', (2, 11), 10, 13, G10_table(11))
    std_point('G10', (2, 12), 10, 13, G10_table(12))
    # E10 cells
    std_point('E10', (3,), 10, 14, E10_table(0))
    std_point('E10', (3, 3), 10, 14, E10_table(3))
    std_point('E10', (3, 4), 10, 14, E10_table(4))
    std_point('E10', (3, 6), 10, 14, E10_table(6))
    std_point('E10', (3, 9), 10, 14, E10_table(9))
    std_point('E10', (3, 12), 10, 14, E10_table(12))
    # D10 cells (floored: tokens >=5)
    std_point('D10', (4,), 10, 15, D10_table(0))
    std_point('D10', (4, 5), 10, 15, D10_table(5))
    std_point('D10', (4, 7), 10, 15, D10_table(7))
    std_point('D10', (4, 9), 10, 15, D10_table(9))
    std_point('D10', (4, 20), 10, 15, D10_table(20))
    # C10 cells (floored: tokens >=6)
    std_point('C10', (5,), 10, 16, C10_table(0))
    std_point('C10', (5, 7), 10, 16, C10_table(7))
    std_point('C10', (5, 8), 10, 16, C10_table(8))
    std_point('C10', (5, 20), 10, 16, C10_table(20))
    # B10 cells (floored: tokens >=7; full collapse)
    std_point('B10', (6,), 10, 17, B10_table(0))
    std_point('B10', (6, 8), 10, 17, B10_table(8))
    std_point('B10', (6, 20), 10, 17, B10_table(20))
    # A10 cells (floored: tokens >=8; full collapse)
    std_point('A10', (7,), 10, 18, A10_table(0))
    std_point('A10', (7, 9), 10, 18, A10_table(9))
    std_point('A10', (7, 20), 10, 18, A10_table(20))
    # m=7 single token (the A10 s=0 single; declared duplicate)
    std_point('m7', (7,), 10, 18, single_token(7, 10, 18))
    # bottom parents at z=10, R=18: the T-Z10 base m=7 positions
    std_point('m7p', (7, 7), 10, 18, single_token(14, 10, 18))
    std_point('m7p', (7, 8), 10, 18, single_token(15, 10, 18))
    std_point('m7p', (7, 7, 7), 10, 18, single_token(21, 10, 18))
    std_point('m7p', (7, 8, 9), 10, 18, single_token(24, 10, 18))
    # bottom children: the trivial-absorption core at face value.
    # (i)  stair child (7,7)@z=10,R=17: window edge, == 1;
    # (ii) a=7 child (6,7)@z=10,R=17: the B10 cell with Y=(7,),
    #      == B10t(7) == v(13,10,17) == the stair option EXACTLY;
    # (iii) C-hand child (7,8)@z=9,R=17: the published T-Z9.
    std_point('m7A', (7, 7), 10, 17, single_token(14, 10, 17))
    std_point('m7a7', (6, 7), 10, 17, B10_table(7))
    std_point('m7c', (7, 8), 9, 17, single_token(15, 9, 17))
    # induction parents (m>=8 option-set identity rungs)
    std_point('ind', (8, 8), 10, 19, single_token(16, 10, 19))
    std_point('ind', (9, 9), 10, 20, single_token(18, 10, 20))
    std_point('ind', (10, 10), 10, 21, single_token(20, 10, 21))
    std_point('ind', (12, 12), 10, 23, single_token(24, 10, 23))
    # published z=9 continuity anchors (K1277 cells at their
    # deviant/theorem positions)
    dev_point('z9F', (1, 10), 9, 11, F9t(10), single_token(11, 9, 11))
    dev_point('z9G', (2, 8), 9, 12, G9t(8), single_token(10, 9, 12))
    dev_point('z9E', (3, 6), 9, 13, E9t(6), single_token(9, 9, 13))
    dev_point('z9D', (4, 6), 9, 14, D9t(6), single_token(10, 9, 14))
    dev_point('z9C', (5, 6), 9, 15, C9t(6), single_token(11, 9, 15))
    std_point('z9B', (6, 7), 9, 16, single_token(13, 9, 16))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D8: cell recursion option-set identity (proof secs 2.1-2.7)
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
    cell_opts(12, (1,), 10,
              lambda Y, s: {single_token(s, 11, 11),
                            single_token(s, 10, 11), 1 ^ F9t(s)},
              famF, 'F10')
    clear_engines()
    cell_opts(13, (2,), 10,
              lambda Y, s: {F10_table(s), single_token(s + 1, 10, 12),
                            1 ^ G9t(s)},
              famF, 'G10')
    clear_engines()
    def e10_exp(Y, s):
        exp = {G10_table(s), 1 ^ E9t(s)}
        if any(t >= 4 for t in Y):
            exp.add(single_token(s + 2, 10, 13))
        return exp
    cell_opts(14, (3,), 10, e10_exp, famF, 'E10')
    clear_engines()
    famD = []
    for s in [0] + list(range(5, 41)):
        famD.extend(decomps(s, 5))
    cell_opts(15, (4,), 10,
              lambda Y, s: {single_token(s + 3, 10, 14), E10_table(s),
                            1 ^ D9t(s)},
              famD, 'D10')
    clear_engines()
    famC = []
    for s in [0] + list(range(6, 41)):
        famC.extend(decomps(s, 6))
    cell_opts(16, (5,), 10,
              lambda Y, s: {single_token(s + 4, 10, 15), D10_table(s),
                            1 ^ C9t(s)},
              famC, 'C10')
    clear_engines()
    famB = []
    for s in [0] + list(range(7, 41)):
        famB.extend(decomps(s, 7))
    cell_opts(17, (6,), 10,
              lambda Y, s: {single_token(s + 5, 10, 16), C10_table(s),
                            1 ^ B9t(s)},
              famB, 'B10')
    clear_engines()
    famA = []
    for s in [0] + list(range(8, 41)):
        famA.extend(decomps(s, 8))
    cell_opts(18, (7,), 10,
              lambda Y, s: {single_token(s + 6, 10, 17), B10_table(s),
                            1 ^ single_token(s + 7, 9, 17)},
              famA, 'A10')
    clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D9: parent proof-structure option-set inspection
# ---------------------------------------------------------------
def check_D9():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 10
    for m in range(7, 12):
        R = m + 11
        for X in D9_shapes(m):
            S = sum(X)
            opts = child_opts_ordered(X, z, R)
            vp = single_token(S, z, R)
            ho = H_ordered(R, X, z)
            hc = H_canonical(R, X, z)
            if m == 7:
                # FIRST TRIVIAL-ABSORPTION BASE: the a=7 child
                # equals B10t(S-7) = v(S-1,10,17) == the stair
                # option exactly (no deviant child in the base)
                Ap = single_token(S - 1, 10, 17)
                cp = 1 ^ single_token(S, 9, 17)
                Dv = B10_table(S - 7)
                a7 = am_child_value(X, 7, z, R)
                rel_ok = (opts <= {Ap, cp, Dv}) and (a7 == Dv)
                rel_tag = 'subset+B10t'
                expected = sorted({Ap, cp, Dv})
            else:
                A = single_token(S - 1, 10, m + 10)
                C = 1 ^ single_token(S, 9, m + 10)
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
# D6c census (NOT in declared totals; bad gate = engine
# disagreement; observations only, no strip/closed-form claims
# on z=11)
# ---------------------------------------------------------------
def check_D6c():
    res = {}
    pts = comps = bad = 0
    # (a) z=11 next-lane cell tables with proper per-cell floors
    cells = {}
    for tag, pre, R, dvoff, tmin, tmax in [
            ('F11', (1,), 13, 1, 3, 9), ('G11', (2,), 14, 2, 3, 9),
            ('E11', (3,), 15, 3, 3, 9), ('D11', (4,), 16, 4, 5, 9),
            ('C11', (5,), 17, 5, 6, 9), ('B11', (6,), 18, 6, 7, 9),
            ('A11', (7,), 19, 7, 8, 9)]:
        fam = Y_tokens(tmin, tmax)
        tbl = {}
        devs = []
        for Y in fam:
            s = sum(Y)
            X = pre + Y
            hc = H_canonical(R, X, 11)
            ho = H_ordered(R, X, 11)
            comps += 2
            if hc != ho:
                bad += 1
            tbl.setdefault(s, set()).add(hc)
            if hc != single_token(s + dvoff, 11, R):
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
    # (a2) D11 loose family (tokens 3..9): decomposition-dependence
    fam = Y_tokens(3, 9)
    tbl = {}
    devs = []
    for Y in fam:
        s = sum(Y)
        hc = H_canonical(16, (4,) + Y, 11)
        ho = H_ordered(16, (4,) + Y, 11)
        comps += 2
        if hc != ho:
            bad += 1
        tbl.setdefault(s, set()).add(hc)
        if hc != single_token(s + 4, 11, 16):
            devs.append(list(Y))
    dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
    tbl2 = {s: sorted(v) for s, v in sorted(tbl.items()) if s <= 20}
    cells['D11_loose'] = {'R': 16, 'floor': 3, 'family': len(fam),
                         'table_s20': {str(k): v for k, v in tbl2.items()},
                         'decomp_dependent_s': dep,
                         'deviant_count': len(devs),
                         'deviants_vs_collapse': devs[:40]}
    pts += len(fam)
    res['z11_cells'] = cells
    clear_engines()
    # (b) z=11 strip grid: m in {6..11} x 96 census shapes
    strip = {}
    for m in range(6, 12):
        z, R = 11, m + 12
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
                if len(seps) < 8:
                    seps.append([list(X), hc, single_token(S, z, R)])
            total += 1
        strip[m] = {'total': total, 'collapse': total - coll,
                    'separations': seps}
        bad += engine_bad
        pts += total
        clear_engines()
    res['z11_strip'] = strip
    # (c) m=6 z=10 out-of-band record over the 222 T-family
    neg = []
    mneg = 0
    for X in T_shapes(6):
        S = sum(X)
        hc = H_canonical(17, X, 10)
        ho = H_ordered(17, X, 10)
        comps += 2
        mneg += 1
        if hc != ho:
            bad += 1
        if hc != single_token(S, 10, 17):
            neg.append([list(X), hc, single_token(S, 10, 17)])
    res['m6_z10_out_of_band'] = {'total': mneg, 'separations': neg}
    pts += mneg
    clear_engines()
    # (d) m=5 z=10 out-of-band record over the 222 T-family
    neg10 = []
    mneg10 = 0
    for X in T_shapes(5):
        S = sum(X)
        hc = H_canonical(16, X, 10)
        ho = H_ordered(16, X, 10)
        comps += 2
        mneg10 += 1
        if hc != ho:
            bad += 1
        if hc != single_token(S, 10, 16):
            neg10.append([list(X), hc, single_token(S, 10, 16)])
    res['m5_z10_out_of_band'] = {'total': mneg10, 'separations': neg10}
    pts += mneg10
    clear_engines()
    # (e) E10 UNCONDITIONAL ghost form observation (full family)
    famF = []
    for s in [0] + list(range(3, 41)):
        famF.extend(decomps(s, 3))
    mm = 0
    for i, Y in enumerate(famF):
        s = sum(Y)
        opts = child_opts_ordered((3,) + Y, 10, 14)
        expu = {G10_table(s), 1 ^ E9t(s), single_token(s + 2, 10, 13)}
        if opts != expu:
            mm += 1
        if i % 400 == 399:
            clear_engines()
    clear_engines()
    res['E10_uncond_ghost_mismatch'] = mm
    comps += len(famF)
    pts += len(famF)
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'note': ('census observation only; z=11 strip closed '
                     'forms are NOT claimed (registered open); '
                     'm=6 z=11 is out of band (z*(6)=10, witness '
                     '(6,6) parent 0 vs single 1: SIGN FLIP of the '
                     'z=10 witness)'),
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
    # B11: C-move without the 1^ (nimber) flip
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
    # B12: corrupted q_odd
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

    # B1: F10 mis-claimed as the Sigma-collapse v(s+1,10,12)
    #     (caught at the s=10 upward deviants)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(12, (1,) + Y, 10) != single_token(s + 1, 10, 12):
            bad += 1
    rec('B1 F10 mis-claimed collapse v(s+1,10,12)', bad)
    clear_engines()
    # B2: F10(s>=11) corruption (0 -> 1; hides the persistent-2 death)
    bad = 0
    for s in range(11, 18):
        for Y in decomps(s, 3):
            if H_canonical(12, (1,) + Y, 10) != 1:
                bad += 1
        clear_engines()
    rec('B2 F10(s>=11) corruption (0->1)', bad)
    # B3: F10(10) flip (1 -> 0; hides the s=10 upward deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 0 if sum(Y) == 10 else F10_table(sum(Y))
        if H_canonical(12, (1,) + Y, 10) != exp:
            bad += 1
    rec('B3 F10(10) flip (1->0)', bad)
    clear_engines()
    # B4: G10 mis-claimed as the R2-form collapse (caught at
    #     s in {8,10}: the two-sided co-resident deviants)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(13, (2,) + Y, 10) != single_token(s + 2, 10, 13):
            bad += 1
    rec('B4 G10 mis-claimed collapse v(s+2,10,13)', bad)
    # B5: G10(8) flip (0 -> 2; disguises the s=8 downward deviant
    #     as the collapse value)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 2 if sum(Y) == 8 else G10_table(sum(Y))
        if H_canonical(13, (2,) + Y, 10) != exp:
            bad += 1
    rec('B5 G10(8) flip (0->2)', bad)
    clear_engines()
    # B6: G10(10) flip (2 -> 1; hides the s=10 upward deviant and
    #     the first F->G deviant chain)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 1 if sum(Y) == 10 else G10_table(sum(Y))
        if H_canonical(13, (2,) + Y, 10) != exp:
            bad += 1
    rec('B6 G10(10) flip (2->1)', bad)
    # B7: E10 mis-claimed as collapse v(s+3,10,14) (caught at s=8)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(14, (3,) + Y, 10) != single_token(s + 3, 10, 14):
            bad += 1
    rec('B7 E10 mis-claimed collapse v(s+3,10,14)', bad)
    clear_engines()
    # B8: E10(8) flip (1 -> 0; hides the s=8 upward deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 0 if sum(Y) == 8 else E10_table(sum(Y))
        if H_canonical(14, (3,) + Y, 10) != exp:
            bad += 1
    rec('B8 E10(8) flip (1->0)', bad)
    # B9: D10 mis-claimed as a FULL collapse (falsely D10(6)=...);
    #     the floored sweep catches it at s in {6,8}: the FIRST
    #     two-sided floored D-rung cannot be disguised as a collapse
    bad = 0
    for s in [0] + list(range(5, 21)):
        for Y in decomps(s, 5):
            if H_canonical(15, (4,) + Y, 10) != single_token(s + 4, 10, 15):
                bad += 1
        clear_engines()
    rec('B9 D10 mis-claimed full collapse (s in {6,8})', bad)
    # B10: T-Z10 m=6 extension (the (6,6) witness at z=10)
    bad = 0
    for X in T_shapes(6):
        if H_canonical(17, X, 10) != single_token(sum(X), 10, 17):
            bad += 1
    rec('B10 T-Z10 m=6 extension witness (6,6)', bad)
    clear_engines()
    # B11: ordered engine without the C-move XOR
    bad = 0
    for X in [(3, 3), (3, 4), (3, 3, 3), (2, 3), (4, 5), (2, 6)]:
        for z in (3, 4, 5, 6, 7, 8, 9, 10):
            for R in range(1, 12):
                if H_ordered_noXOR(R, X, z) != H_canonical(R, X, z):
                    bad += 1
    rec('B11 ordered engine C-move XOR removed', bad)
    H_ordered_noXOR.cache_clear()
    clear_engines()
    # B12: corrupted q_odd closed form
    bad = 0
    for x in range(2, 41):
        for z in range(1, 31):
            for R in range(0, min(x + z, 31) + 1):
                if single_token_qmut(x, z, R) != vC(x, z, R): bad += 1
    rec('B12 q_odd corruption', bad)
    # B13: a=m child identity budget mutation (the trivial-absorption
    #      core forged: the a=m child value is v(S-1,10,m+10); the
    #      mutation mis-specifies the budget as m+9 and is caught)
    bad = 0
    for m in range(7, 11):
        R = m + 11
        for X in D9_shapes(m):
            S = sum(X)
            a_m = am_child_value(X, m, 10, R)
            exp_mut = single_token(S - 1, 10, m + 9)
            if a_m != exp_mut:
                bad += 1
        clear_engines()
    rec('B13 a=m child identity budget mutation (trivial-absorption '
        'forged)', bad)
    # B14: C10 C-hand child mis-specified as 1^D10t(s) (the z=10
    #      C-rank z=9 dependency forged); the option-set identity
    #      catches it (e.g. at s=0 and s=6)
    bad = 0
    for s in [0] + list(range(6, 21)):
        for Y in decomps(s, 6):
            opts = child_opts_ordered((5,) + Y, 10, 16)
            exp = {single_token(s + 4, 10, 15), D10_table(s),
                   1 ^ D10_table(s)}
            if opts != exp:
                bad += 1
        clear_engines()
    rec('B14 C10 C-hand child mis-specified 1^D10t(s)', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed:
        sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
DECLARED_TOTALS = {'points': 24743, 'comparisons': 44548}

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
    res['D4d'] = check_D4d()
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
    gated = ('D1', 'D2', 'D3', 'D4', 'D4b', 'D4c', 'D4d', 'D5',
             'D6', 'D7a', 'D7b', 'D8', 'D9')
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
        'theorem': ('Lemma F10 (persistent-2 DEATH: single s=10 '
                    'upward deviant, 5 shapes; s>=11 sinks)/G10 ('
                    'first two-sided co-resident G deviants s=8 DOWN '
                    '0<2 and s=10 UP 2>1, mex chain from F10(10)=1)/'
                    'E10 (single s=8 upward deviant; conditional '
                    'recursion, unconditional ghost agrees 2nd '
                    'consecutive slice)/D10 (FIRST two-sided floored '
                    'D deviants s=6 DOWN 0<2 and s=8 UP 2>1: the E10 '
                    's=8 deviant fruits at the parent)/C10 (single '
                    's=6 upward 1>0: reversive absorption 2nd '
                    'consecutive slice, absorbed value decays 2->1)/'
                    'B10 (full collapse 2nd consecutive slice)/A10 '
                    '(FIRST full-collapse A rung; two full-collapse '
                    'rungs co-resident; C-hand child = published '
                    'T-Z9) + Theorem T-Z10: min>=7 critical-strip '
                    'z=10 slice with the FIRST TRIVIAL-ABSORPTION '
                    'base m=7 (a=7 child == stair option exactly, '
                    'no deviant child) + option-set identity '
                    'induction. The m=7 row of K1268 Conjecture C1 '
                    'is determined for z in {0..10} leaving exactly '
                    '{11,12} open. Universal claims proved on paper '
                    'in the declaration note; this finite audit '
                    'corroborates.'),
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
