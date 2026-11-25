"""verify_strip_z11.py -- machine audit for the declared claims of the
single-owner declaration note (K1280 provisional; min>=7 critical-strip
z=11 slice; declaration note:
research/log/2026-11-24-strip-z11-min7-single-owner-note.md):

  Lemma F11: F11(s) := H(13;{1}+Y;11) (Y tokens >=3, arity free, Y=()
             for s=0) is independent of the decomposition of s and
             F11(0)=1, F11(3)=0, F11(4)=1, F11(5)=0, F11(6)=1,
             F11(7)=0, F11(8)=1, F11(9)=0, F11(10)=1, F11(11)=0,
             F11(s>=12)=2 -- the REBIRTH of the F-rank persistent-2
             (dead at z=10 after the s=10 blip; alive again at z=11
             for the whole tail). Vs the Sigma-collapse v(s+1,11,13)
             the deviation is TWO-SIDED: the single s=10 DOWNWARD
             deviant 1<2 over the 5-decomposition family
             {(10,),(3,7),(4,6),(5,5),(3,3,4)}, and the PERMANENT tail
             s>=12 UPWARD 2>0 (the persistent-2 rebirth splitting the
             F table from v at scale; 310/330 census-family deviants).
             Extends the published F-ladder (F z in {1..4} K1272,
             F5 K1273, F6 K1274, F7 K1275, F8 K1276, F9 K1277,
             F10 K1279).
  Lemma G11: G11(s) := H(14;{2}+Y;11) depends only on s and
             G11(0)=0, G11(3)=1, G11(4)=0, G11(5)=1, G11(6)=0,
             G11(7)=1, G11(8)=0, G11(9)=1, G11(10)=0,
             G11(11)=1, G11(s>=12)=1. Vs the R2-form collapse
             v(s+2,11,14) the SINGLE s=10 DOWNWARD deviant 0<1 covers
             {(10,),(3,7),(4,6),(5,5),(3,3,4)} (the census family
             holds 4 of them; (10,) is outside and recorded in D7b).
             The z=10 G10 two-sided co-residence shrinks to the single
             downward deviant at the same s=10 position.
  Lemma E11: E11(s) := H(15;{3}+Y;11) depends only on s and
             E11(0)=1, E11(3)=0, E11(4)=1, E11(5)=0, E11(6)=1,
             E11(7)=0, E11(8)=1, E11(9)=0, E11(10)=2, E11(s>=11)=0 --
             the FIRST TWO-SIDED E-rank deviant pair: s=8 DOWNWARD
             1<2 over {(8,),(3,5),(4,4)} and s=10 UPWARD 2>0 over
             {(10,),(3,7),(4,6),(5,5),(3,3,4)}. The E11 recursion
             stays in the K1276/K1277/K1279 CONDITIONAL form
             {G11(s), 1^E10(s)} plus ({v(s+2,11,14)} iff some Y token
             is >= 4); the UNCONDITIONAL ghost form coincides with the
             conditional form over the full 3,657 family at z=11
             (mismatch 0), the THIRD consecutive agreeing slice
             (z=9, z=10, z=11) after the z=8 break at Y=(3,3).
  Lemma D11: floored single-downward D-rung:
             D11(s) := H(16;{4}+Y;11) with ALL Y tokens >=5 (s in
             {0} u {5,6,...}) depends only on s with table
             {8:0, else v(s+4,11,16)} -- the single s=8 DOWNWARD
             deviant D11(8)=0 != v(12,11,16)=1 (the z=10 D10 pair
             {6,8} shrinks to s=8 only; direction preserved). The
             floor min(Y)>=5 is essential: loosened to tokens >=3
             the decomposition-dependence at s=10 enters (loose
             census record; ALSO a shift from the z=9/z=10 loose
             records at s in {8,10}).
  Lemma C11: C11(s) := H(17;{5}+Y;11) with ALL Y tokens >=6 depends
             only on s with table {0:1, 6:1, 8:2, else
             v(s+5,11,17)} -- the FIRST TWO-SIDED C-rank deviant
             pair: s=6 DOWNWARD 1<2 (the D10/D11-era downward line
             reversing at C for a second slice at the s=6 archetype
             position, the same cell as the m=5 z=11 out-of-band
             witness) and s=8 UPWARD 2>0 (the same cell as the
             SECOND m=5 z=11 out-of-band witness -- the two
             structural lines coincide exactly).
  Lemma B11: B11(s) := H(18;{6}+Y;11) with ALL Y tokens >=7 FULLY
             collapses: B11(s) = v(s+6,11,18). THIRD consecutive
             full-collapse B-rung (B9 z=9, B10 z=10, B11 z=11),
             floor >=7 unchanged.
  Lemma A11: A11(s) := H(19;{7}+Y;11) with ALL Y tokens >=8 FULLY
             collapses: A11(s) = v(s+7,11,19). SECOND consecutive
             full-collapse A-rung; the second slice with TWO
             full-collapse rungs (A+B). The A11 C-hand child
             1^v(s+7,10,18) is the published T-Z10 (K1279) THEOREM
             position H(18;{7}+Y;10) -- the strip-theorem dependency
             of the ladder deepens again (z=10 A10 pulled T-Z9;
             z=11 A11 pulls T-Z10).
  Theorem T-Z11: for ALL m>=7, every nonempty finite multiset X
             with min(X)=m: H(m+12;X;11) = v(sum X, 11, m+12).
             Base m=7 is the SECOND TRIVIAL-ABSORPTION base (a=7
             child = B11t(S-7) = v(S-1,11,18) == the stair option
             EXACTLY, by the B11 full collapse -- the base uses NO
             deviant child; the C-hand child is the published
             T-Z10). m>=8 by option-set identity induction on m
             (a=m child = C(m-1,11) at R=m+11=(m-1)+12, a>m children
             by K1264, C-hand child by published T-Z10) with option
             set {v(S-1,11,m+11), 1^v(S,10,m+11)} exactly.
  Corollary: the z=11 slice is determined for all m>=7 (z*(7)=13 so
             m=7 IS in band at z=11); the m=7 row of K1268
             Conjecture C1 is determined for z in {0..11} leaving
             exactly {12} open; m>=8 rows keep z in {12..z*(m)-1}
             open. Out-of-band records: m=6 z=11 witness (6,6):
             parent 0 vs single 1 (the SIGN FLIP of the z=10
             +1 witness, re-recorded here as claimed sharpness --
             min>=7 is necessary); m=5 z=11 witnesses (5,6): parent
             1 vs single 2 (sign flip of the z=10 1-vs-0) and
             (5,8): parent 2 vs single 0 -- the FIRST double-witness
             m=5 out-of-band slice (the second witness co-resides
             with the C11 s=8 deviant cell).

Declared checks (PUBLISH-THEN-EXECUTE):
  D1  Lemma F11: s in {0} u {3..40}, ALL decompositions into 1..4
      tokens >=3 (3,657)                          (3,657 / 10,971)
  D2  Lemma G11: Y = tokens 3..9 multisets, arity 0..4 (330) vs
      G11 table; +1 arithmetic deviant-set comparison:
      {Y: G11 != v(s+2,11,14)} == {(3,3,4),(3,7),(4,6),(5,5)}
      (the (10,) full-decomposition deviant is OUTSIDE the census
      family; anchored in D7b)                      (330 / 991)
  D3  Lemma E11: same 330 shapes vs E11 table; +1 arithmetic
      deviant set == {(3,3,4),(3,5),(3,7),(4,4),(4,6),(5,5),(8,)};
      +1 E11 unconditional ghost-form mismatch counter == 0 over
      the same family                              (330 / 992)
  D4  Lemma D11: s in {0} u {5..40}, ALL decompositions into 1..4
      tokens >=5 (1,650) vs {8:0, else v(s+4,11,16)}
                                                     (1,650 / 4,950)
  D4b Lemma C11: s in {0} u {6..40}, ALL decompositions into 1..4
      tokens >=6 (1,078) vs {0:1, 6:1, 8:2, else v(s+5,11,17)}
                                                     (1,078 / 3,234)
  D4c Lemma B11: s in {0} u {7..40}, ALL decompositions into 1..4
      tokens >=7 (700) vs full collapse v(s+6,11,18)
                                                       (700 / 2,100)
  D4d Lemma A11: s in {0} u {8..40}, ALL decompositions into 1..4
      tokens >=8 (460) vs full collapse v(s+7,11,19)
                                                       (460 / 1,380)
  D5  Theorem T-Z11 grid: m in {7..12} x z=11 x 222 shapes
      (R=m+12)                                     (1,332 / 3,996)
  D6  fixed-seed (20261131) random deep: m in {7..12} x 15 shapes
      (arity 4..5, tokens in [m,m+15], one token fixed at m)
                                                      (90 / 270)
  D7a published K1264/K1268/K1271-K1276 witness anchors (17; the
      same table as the published machines)         (17 / 85)
  D7b theorem anchors 78 points (25 deviant/witness pair anchors +
      53 standard anchors: the F11 s=10 downward deviants
      {(10,),(3,7),(4,6),(5,5),(3,3,4)}, the s=11 agreement
      anchor, and the persistent-2 REBIRTH anchors (12,),(20,);
      the G11 s=10 downward deviants; the E11 two-sided
      s=8/s=10 deviant families; the D11 s=8 downward deviant; the
      C11 two-sided s=6/s=8 deviants (co-residing with the m=5
      z=11 out-of-band witnesses); the m=6 z=11 out-of-band
      SIGN-FLIP witness (6,6); F11/G11/E11/D11/C11/B11/A11 cells,
      the m=7 single token and bottom parents, the bottom stair /
      a=7 / C-hand children (the trivial-absorption core at face
      value), the published z=10 continuity (K1279 deviant
      positions + B10 cell), and the induction parents)
                                                      (78 / 234)
  D8  cell recursion option-set identity (paper proof secs
      2.1-2.7), 1 comparison per point (ordered child option set
      == arithmetic expectation set):
      F11 3,657 = {v(s,12,12), v(s,11,12), 1^F10(s)};
      G11 3,657 = {F11(s), v(s+1,11,13), 1^G10(s)};
      E11 3,657 = CONDITIONAL {G11(s), 1^E10(s)}
                  + ({v(s+2,11,14)}: some Y token >= 4);
      D11 1,650 = {v(s+3,11,15), E11(s), 1^D10(s)};
      C11 1,078 = {v(s+4,11,16), D11(s), 1^C10(s)};
      B11   700 = {v(s+5,11,17), C11(s), 1^B10(s)};
      A11   460 = {v(s+6,11,18), B11(s), 1^v(s+7,10,18)}
      where the z=10 tables in the recursions are the PUBLISHED
      K1279 closed forms (the A11 C-hand line is the published
      T-Z10 theorem position -- the deepest strip-theorem
      dependency in the ladder).
                                                (14,859 / 14,859)
  D9  parent proof-structure option-set inspection: m in {7..11} x
      33 shapes. m=7: opts subset of {A'=v(S-1,11,18),
      c'=1^v(S,10,18), B11t(S-7)} AND the a=7 child == B11t(S-7)
      (the TRIVIAL ABSORPTION observed at face value: the base
      uses no deviant child); m>=8: opts == {v(S-1,11,m+11),
      1^v(S,10,m+11)} exact; parent mex == v(S,11,m+12) both
      engines                                        (165 / 495)
  TOTAL declared: 24,746 points / 44,557 comparisons / bad 0.
  D6c census (NOT in declared totals; bad gate = engine disagreement
  only; observations are recorded, nothing claimed):
    (a) z=12 next-lane cell tables with the proper per-cell floors:
        F12 H(14;{1}+Y;12), G12 H(15;{2}+Y;12), E12 H(16;{3}+Y;12)
        over the 330 family (tokens 3..9, arity 0..4); D12
        H(17;{4}+Y;12) over the 126 floored family (tokens 5..9)
        and the loose 330 family (decomposition-dependence
        record); C12 H(18;{5}+Y;12) over the 70 family (tokens
        6..9); B12 H(19;{6}+Y;12) over the 35 family (tokens
        7..9); A12 H(20;{7}+Y;12) over the 15 family (tokens
        8..9). s-only tables, decomposition-dependence flags,
        deviant records vs v(s+k,12,R). The z=12 closed forms and
        the z=12 strip stay OPEN (registered open; not claimed;
        the pre-declaration probe observed F12 8 deviants (the
        s=12 1-vs-0 single-point blip -- persistent-2 DEAD again
        at z=12 after its z=11 rebirth), G12 12 (s=10 downward 4 +
        s=12 upward 8), E12 4 (s=10 upward), D12 floored 2 (s=8
        downward + s=10 upward), D12_loose decomposition-dependent,
        C12 1 (s=8), B12 1 (s=8 upward -- the B full-collapse
        series z in {9,10,11} BREAKS at z=12 for the first time),
        A12 0 (A full collapse THIRD consecutive slice)).
    (b) z=12 strip grid: m in {5..12} x shapes (R=m+13; 222
        T-family for m in {5,6,7}, 96 census for m in {8..12}):
        collapse record (m=5 OUT of band: 1 separation (5,8)
        parent 1 vs single 0; m=6 OUT of band: 2 separations
        (6,6) parent 0 vs 2 and (6,8) parent 2 vs 1; m>=7 in
        band 100% collapse observed -- recorded only, not
        claimed; the pre-declaration probe saw m in {7..12} all
        clean).
    (c) m=6 z=11 out-of-band record over the 222 T-family (R=18):
        the single (6,6) separation parent 0 vs single 1 (the
        SIGN-FLIP witness; claimed sharpness re-recorded).
    (d) m=5 z=11 out-of-band record over the 222 T-family (R=17):
        the TWO separations (5,6) parent 1 vs single 2 and
        (5,8) parent 2 vs single 0 (the first double-witness
        m=5 slice; claimed sharpness re-recorded).
    (e) E11 UNCONDITIONAL ghost form observation over the full
        3,657 family: mismatch count vs the conditional form
        (z=8 broke at Y=(3,3); z in {9,10} recorded mismatch 0;
        z=11 declared mismatch 0 and re-recorded -- THIRD
        consecutive agreeing slice; general law open).

Fail-closed: any bad>0 -> rc=1; declared-count mismatch -> rc=1
(honest record requirement). Finite machine audit is NOT the proof:
the universal claims rest on the paper proof in the declaration note
(F11/G11/E11 CONDITIONAL/D10-published-line C11/B11/A11 closed-form
ladder with the + trivial-absorption base m=7 + option-set identity
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
def F11_table(s):
    # Lemma F11 closed form (z=11 cell), s in {0} u {3,4,...}
    # persistent-2 REBIRTH: tail holds at 2 for all s>=12
    # (dead at z=10; alive again at z=11)
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1,
            9: 0, 10: 1, 11: 0}.get(s, 2)

def G11_table(s):
    # Lemma G11 closed form (z=11 cell), s in {0} u {3,4,...}
    # single s=10 downward deviant vs v(s+2,11,14)
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0,
            9: 1, 10: 0, 11: 1}.get(s, 1)

def E11_table(s):
    # Lemma E11 closed form (z=11 cell), s in {0} u {3,4,...}
    # first TWO-SIDED E-rank deviant pair: s=8 DOWN 1<2, s=10 UP 2>0
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1,
            9: 0, 10: 2}.get(s, 0)

def D11_table(s):
    # Lemma D11 (floored family, tokens >=5):
    # {8:0, else collapse v(s+4,11,16)}
    if s == 8:
        return 0
    return single_token(s + 4, 11, 16)

def C11_table(s):
    # Lemma C11 (floored family, tokens >=6):
    # {0:1, 6:1, 8:2, else collapse v(s+5,11,17)}
    # first TWO-SIDED C-rank deviant pair: s=6 DOWN 1<2, s=8 UP 2>0
    if s == 6:
        return 1
    if s == 8:
        return 2
    return single_token(s + 5, 11, 17)

def B11_table(s):
    # Lemma B11 (floored family, tokens >=7): full collapse
    return single_token(s + 6, 11, 18)

def A11_table(s):
    # Lemma A11 (floored family, tokens >=8): full collapse
    return single_token(s + 7, 11, 19)

# published z=10 closed forms (K1279), used by the z=11 recursions
def F10t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1,
            9: 0, 10: 1}.get(s, 0)

def G10t(s):
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0,
            9: 1, 10: 2}.get(s, 1)

def E10t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1}.get(s, 0)

def D10t(s):
    if s == 6:
        return 0
    if s == 8:
        return 2
    return single_token(s + 4, 10, 15)

def C10t(s):
    return 1 if s == 6 else single_token(s + 5, 10, 16)

def B10t(s):
    return single_token(s + 6, 10, 17)

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
    R, z = 13, 11
    for s in [0] + list(range(3, 41)):
        exp = F11_table(s)
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
        exp = G11_table(s)
        hc = H_canonical(14, X, 11)
        ho = H_ordered(14, X, 11)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if G11_table(sum(Y)) != single_token(sum(Y) + 2, 11, 14))
    comps += 1
    if deviants != [(3, 3, 4), (3, 7), (4, 6), (5, 5)]:
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
        exp = E11_table(s)
        hc = H_canonical(15, X, 11)
        ho = H_ordered(15, X, 11)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if E11_table(sum(Y)) != single_token(sum(Y) + 3, 11, 15))
    comps += 1
    if deviants != [(3, 3, 4), (3, 5), (3, 7), (4, 4),
                    (4, 6), (5, 5), (8,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    # E11 unconditional ghost-form mismatch counter (330 family):
    # declared 0 (3rd consecutive agreeing slice after the z=8 break)
    mm = 0
    for Y in fam:
        s = sum(Y)
        opts = child_opts_ordered((3,) + Y, 11, 15)
        expu = {G11_table(s), 1 ^ E10t(s),
                single_token(s + 2, 11, 14)}
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
    R, z = 16, 11
    for s in [0] + list(range(5, 41)):
        exp = D11_table(s)
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
    R, z = 17, 11
    for s in [0] + list(range(6, 41)):
        exp = C11_table(s)
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
    R, z = 18, 11
    for s in [0] + list(range(7, 41)):
        exp = B11_table(s)
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
    R, z = 19, 11
    for s in [0] + list(range(8, 41)):
        exp = A11_table(s)
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
    z = 11
    for m in range(7, 13):
        R = m + 12
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
    rng = random.Random(20261131)
    z = 11
    for m in range(7, 13):
        R = m + 12
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
            # per-shape cache clear (value-transparent: the arity-5
            # deep random shapes at m in {10,11,12} otherwise grow
            # the memo past this host's RAM between the per-m clears)
            clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D7a: published witness anchors (identical table to the published
# K1264/K1268/K1271-K1277/K1279 machines D7a; 17 anchors)
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
# D7b: theorem anchors (78 points: 25 deviant/witness pair anchors
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
    # F11 s=10 DOWNWARD deviants (1 < 2): the single pre-tail blip
    dev_point('F11dev10a', (1, 10), 11, 13, 1, 2)
    dev_point('F11dev10b', (1, 3, 7), 11, 13, 1, 2)
    dev_point('F11dev10c', (1, 4, 6), 11, 13, 1, 2)
    dev_point('F11dev10d', (1, 5, 5), 11, 13, 1, 2)
    dev_point('F11dev10e', (1, 3, 3, 4), 11, 13, 1, 2)
    # F11 s=11 agreement anchor: the last pre-tail agreeing point
    dev_point('F11agree11', (1, 11), 11, 13, 0, 0)
    # F11 persistent-2 REBIRTH anchors: the tail splits from v at 2
    # for every s>=12 (dead at z=10; alive again at z=11)
    dev_point('F11rebirth12', (1, 12), 11, 13, 2, 0)
    dev_point('F11rebirth20', (1, 20), 11, 13, 2, 0)
    # G11 s=10 DOWNWARD deviants (0 < 1): all 5 shapes (the census
    # family holds 4; (10,) is the census-exterior deviant)
    dev_point('G11dev10a', (2, 10), 11, 14, 0, 1)
    dev_point('G11dev10b', (2, 3, 7), 11, 14, 0, 1)
    dev_point('G11dev10c', (2, 4, 6), 11, 14, 0, 1)
    dev_point('G11dev10d', (2, 5, 5), 11, 14, 0, 1)
    dev_point('G11dev10e', (2, 3, 3, 4), 11, 14, 0, 1)
    # E11 first TWO-SIDED E deviant pair: s=8 DOWNWARD (1 < 2) and
    # s=10 UPWARD (2 > 0)
    dev_point('E11dev8a', (3, 8), 11, 15, 1, 2)
    dev_point('E11dev8b', (3, 3, 5), 11, 15, 1, 2)
    dev_point('E11dev8c', (3, 4, 4), 11, 15, 1, 2)
    dev_point('E11dev10a', (3, 10), 11, 15, 2, 0)
    dev_point('E11dev10b', (3, 3, 7), 11, 15, 2, 0)
    dev_point('E11dev10c', (3, 4, 6), 11, 15, 2, 0)
    dev_point('E11dev10d', (3, 5, 5), 11, 15, 2, 0)
    dev_point('E11dev10e', (3, 3, 3, 4), 11, 15, 2, 0)
    # D11 single s=8 DOWNWARD deviant (0 < 1; floored family)
    dev_point('D11dev8', (4, 8), 11, 16, 0, 1)
    # C11 first TWO-SIDED C deviant pair: s=6 DOWNWARD (1 < 2) --
    # same cell as the m=5 z=11 out-of-band witness (5,6); and
    # s=8 UPWARD (2 > 0) -- the same cell as the SECOND m=5 z=11
    # out-of-band witness (5,8): the double-witness co-residence
    dev_point('C11dev6/m5z11oob', (5, 6), 11, 17, 1, 2)
    dev_point('C11dev8/m5z11oob2', (5, 8), 11, 17, 2, 0)
    # m=6 z=11 out-of-band SIGN-FLIP witness: parent 0 vs single 1
    # (the z=10 witness was UPWARD 2 vs 1; min>=7 is necessary)
    dev_point('m6z11oob', (6, 6), 11, 18, 0, 1)
    # F11 cells
    for Y, s in [((3,), 3), ((5,), 5), ((6,), 6), ((9,), 9),
                 ((11,), 11), ((12,), 12), ((20,), 20)]:
        std_point('F11', (1,) + Y, 11, 13, F11_table(s))
    # G11 cells
    std_point('G11', (2,), 11, 14, G11_table(0))
    std_point('G11', (2, 3), 11, 14, G11_table(3))
    std_point('G11', (2, 4), 11, 14, G11_table(4))
    std_point('G11', (2, 5), 11, 14, G11_table(5))
    std_point('G11', (2, 9), 11, 14, G11_table(9))
    std_point('G11', (2, 11), 11, 14, G11_table(11))
    std_point('G11', (2, 12), 11, 14, G11_table(12))
    # E11 cells
    std_point('E11', (3,), 11, 15, E11_table(0))
    std_point('E11', (3, 3), 11, 15, E11_table(3))
    std_point('E11', (3, 4), 11, 15, E11_table(4))
    std_point('E11', (3, 6), 11, 15, E11_table(6))
    std_point('E11', (3, 9), 11, 15, E11_table(9))
    std_point('E11', (3, 12), 11, 15, E11_table(12))
    # D11 cells (floored: tokens >=5)
    std_point('D11', (4,), 11, 16, D11_table(0))
    std_point('D11', (4, 5), 11, 16, D11_table(5))
    std_point('D11', (4, 7), 11, 16, D11_table(7))
    std_point('D11', (4, 9), 11, 16, D11_table(9))
    std_point('D11', (4, 20), 11, 16, D11_table(20))
    # C11 cells (floored: tokens >=6)
    std_point('C11', (5,), 11, 17, C11_table(0))
    std_point('C11', (5, 7), 11, 17, C11_table(7))
    std_point('C11', (5, 9), 11, 17, C11_table(9))
    std_point('C11', (5, 20), 11, 17, C11_table(20))
    # B11 cells (floored: tokens >=7; full collapse)
    std_point('B11', (6,), 11, 18, B11_table(0))
    std_point('B11', (6, 8), 11, 18, B11_table(8))
    std_point('B11', (6, 20), 11, 18, B11_table(20))
    # A11 cells (floored: tokens >=8; full collapse)
    std_point('A11', (7,), 11, 19, A11_table(0))
    std_point('A11', (7, 9), 11, 19, A11_table(9))
    std_point('A11', (7, 20), 11, 19, A11_table(20))
    # m=7 single token (the A11 s=0 single; declared duplicate)
    std_point('m7', (7,), 11, 19, single_token(7, 11, 19))
    # bottom parents at z=11, R=19: the T-Z11 base m=7 positions
    std_point('m7p', (7, 7), 11, 19, single_token(14, 11, 19))
    std_point('m7p', (7, 8), 11, 19, single_token(15, 11, 19))
    std_point('m7p', (7, 7, 7), 11, 19, single_token(21, 11, 19))
    std_point('m7p', (7, 8, 9), 11, 19, single_token(24, 11, 19))
    # bottom children: the trivial-absorption core at face value.
    # (i)  stair child (7,7)@z=11,R=18: window edge, == 1;
    # (ii) a=7 child (6,7)@z=11,R=18: the B11 cell with Y=(7,),
    #      == B11t(7) == v(13,11,18) == the stair option EXACTLY;
    # (iii) C-hand child (7,8)@z=10,R=18: the published T-Z10.
    std_point('m7A', (7, 7), 11, 18, single_token(14, 11, 18))
    std_point('m7a7', (6, 7), 11, 18, B11_table(7))
    std_point('m7c', (7, 8), 10, 18, single_token(15, 10, 18))
    # induction parents (m>=8 option-set identity rungs)
    std_point('ind', (8, 8), 11, 20, single_token(16, 11, 20))
    std_point('ind', (9, 9), 11, 21, single_token(18, 11, 21))
    std_point('ind', (10, 10), 11, 22, single_token(20, 11, 22))
    std_point('ind', (12, 12), 11, 24, single_token(24, 11, 24))
    # published z=10 continuity anchors (K1279 cells at their
    # deviant/theorem positions)
    dev_point('z10F', (1, 10), 10, 12, F10t(10),
              single_token(11, 10, 12))
    dev_point('z10G', (2, 8), 10, 13, G10t(8),
              single_token(10, 10, 13))
    dev_point('z10E', (3, 8), 10, 14, E10t(8),
              single_token(11, 10, 14))
    dev_point('z10D', (4, 6), 10, 15, D10t(6),
              single_token(10, 10, 15))
    dev_point('z10C', (5, 6), 10, 16, C10t(6),
              single_token(11, 10, 16))
    std_point('z10B', (6, 7), 10, 17, single_token(13, 10, 17))
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
    cell_opts(13, (1,), 11,
              lambda Y, s: {single_token(s, 12, 12),
                            single_token(s, 11, 12), 1 ^ F10t(s)},
              famF, 'F11')
    clear_engines()
    cell_opts(14, (2,), 11,
              lambda Y, s: {F11_table(s), single_token(s + 1, 11, 13),
                            1 ^ G10t(s)},
              famF, 'G11')
    clear_engines()
    def e11_exp(Y, s):
        exp = {G11_table(s), 1 ^ E10t(s)}
        if any(t >= 4 for t in Y):
            exp.add(single_token(s + 2, 11, 14))
        return exp
    cell_opts(15, (3,), 11, e11_exp, famF, 'E11')
    clear_engines()
    famD = []
    for s in [0] + list(range(5, 41)):
        famD.extend(decomps(s, 5))
    cell_opts(16, (4,), 11,
              lambda Y, s: {single_token(s + 3, 11, 15), E11_table(s),
                            1 ^ D10t(s)},
              famD, 'D11')
    clear_engines()
    famC = []
    for s in [0] + list(range(6, 41)):
        famC.extend(decomps(s, 6))
    cell_opts(17, (5,), 11,
              lambda Y, s: {single_token(s + 4, 11, 16), D11_table(s),
                            1 ^ C10t(s)},
              famC, 'C11')
    clear_engines()
    famB = []
    for s in [0] + list(range(7, 41)):
        famB.extend(decomps(s, 7))
    cell_opts(18, (6,), 11,
              lambda Y, s: {single_token(s + 5, 11, 17), C11_table(s),
                            1 ^ B10t(s)},
              famB, 'B11')
    clear_engines()
    famA = []
    for s in [0] + list(range(8, 41)):
        famA.extend(decomps(s, 8))
    cell_opts(19, (7,), 11,
              lambda Y, s: {single_token(s + 6, 11, 18), B11_table(s),
                            1 ^ single_token(s + 7, 10, 18)},
              famA, 'A11')
    clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D9: parent proof-structure option-set inspection
# ---------------------------------------------------------------
def check_D9():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 11
    for m in range(7, 12):
        R = m + 12
        for X in D9_shapes(m):
            S = sum(X)
            opts = child_opts_ordered(X, z, R)
            vp = single_token(S, z, R)
            ho = H_ordered(R, X, z)
            hc = H_canonical(R, X, z)
            if m == 7:
                # SECOND TRIVIAL-ABSORPTION BASE: the a=7 child
                # equals B11t(S-7) = v(S-1,11,18) == the stair
                # option exactly (no deviant child in the base)
                Ap = single_token(S - 1, 11, 18)
                cp = 1 ^ single_token(S, 10, 18)
                Dv = B11_table(S - 7)
                a7 = am_child_value(X, 7, z, R)
                rel_ok = (opts <= {Ap, cp, Dv}) and (a7 == Dv)
                rel_tag = 'subset+B11t'
                expected = sorted({Ap, cp, Dv})
            else:
                A = single_token(S - 1, 11, m + 11)
                C = 1 ^ single_token(S, 10, m + 11)
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
# on z=12)
# ---------------------------------------------------------------
def check_D6c():
    res = {}
    pts = comps = bad = 0
    # (a) z=12 next-lane cell tables with proper per-cell floors
    cells = {}
    for tag, pre, R, dvoff, tmin, tmax in [
            ('F12', (1,), 14, 1, 3, 9), ('G12', (2,), 15, 2, 3, 9),
            ('E12', (3,), 16, 3, 3, 9), ('D12', (4,), 17, 4, 5, 9),
            ('C12', (5,), 18, 5, 6, 9), ('B12', (6,), 19, 6, 7, 9),
            ('A12', (7,), 20, 7, 8, 9)]:
        fam = Y_tokens(tmin, tmax)
        tbl = {}
        devs = []
        for Y in fam:
            s = sum(Y)
            X = pre + Y
            hc = H_canonical(R, X, 12)
            ho = H_ordered(R, X, 12)
            comps += 2
            if hc != ho:
                bad += 1
            tbl.setdefault(s, set()).add(hc)
            if hc != single_token(s + dvoff, 12, R):
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
    # (a2) D12 loose family (tokens 3..9): decomposition-dependence
    fam = Y_tokens(3, 9)
    tbl = {}
    devs = []
    for Y in fam:
        s = sum(Y)
        hc = H_canonical(17, (4,) + Y, 12)
        ho = H_ordered(17, (4,) + Y, 12)
        comps += 2
        if hc != ho:
            bad += 1
        tbl.setdefault(s, set()).add(hc)
        if hc != single_token(s + 4, 12, 17):
            devs.append(list(Y))
    dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
    tbl2 = {s: sorted(v) for s, v in sorted(tbl.items()) if s <= 20}
    cells['D12_loose'] = {'R': 17, 'floor': 3, 'family': len(fam),
                         'table_s20': {str(k): v for k, v in tbl2.items()},
                         'decomp_dependent_s': dep,
                         'deviant_count': len(devs),
                         'deviants_vs_collapse': devs[:40]}
    pts += len(fam)
    res['z12_cells'] = cells
    clear_engines()
    # (b) z=12 strip grid: m in {5..12} (222 T-family for
    #     m in {5,6,7}; 96 census shapes for m in {8..12})
    strip = {}
    for m in range(5, 13):
        z, R = 12, m + 13
        coll = engine_bad = total = 0
        seps = []
        for X in (T_shapes(m) if m <= 7 else census_shapes(m)):
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
    res['z12_strip'] = strip
    # (c) m=6 z=11 out-of-band record over the 222 T-family
    neg = []
    mneg = 0
    for X in T_shapes(6):
        S = sum(X)
        hc = H_canonical(18, X, 11)
        ho = H_ordered(18, X, 11)
        comps += 2
        mneg += 1
        if hc != ho:
            bad += 1
        if hc != single_token(S, 11, 18):
            neg.append([list(X), hc, single_token(S, 11, 18)])
    res['m6_z11_out_of_band'] = {'total': mneg, 'separations': neg}
    pts += mneg
    clear_engines()
    # (d) m=5 z=11 out-of-band record over the 222 T-family
    neg10 = []
    mneg10 = 0
    for X in T_shapes(5):
        S = sum(X)
        hc = H_canonical(17, X, 11)
        ho = H_ordered(17, X, 11)
        comps += 2
        mneg10 += 1
        if hc != ho:
            bad += 1
        if hc != single_token(S, 11, 17):
            neg10.append([list(X), hc, single_token(S, 11, 17)])
    res['m5_z11_out_of_band'] = {'total': mneg10, 'separations': neg10}
    pts += mneg10
    clear_engines()
    # (e) E11 UNCONDITIONAL ghost form observation (full family)
    famF = []
    for s in [0] + list(range(3, 41)):
        famF.extend(decomps(s, 3))
    mm = 0
    for i, Y in enumerate(famF):
        s = sum(Y)
        opts = child_opts_ordered((3,) + Y, 11, 15)
        expu = {G11_table(s), 1 ^ E10t(s), single_token(s + 2, 11, 14)}
        if opts != expu:
            mm += 1
        if i % 400 == 399:
            clear_engines()
    clear_engines()
    res['E11_uncond_ghost_mismatch'] = mm
    comps += len(famF)
    pts += len(famF)
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'note': ('census observation only; z=12 strip closed '
                     'forms are NOT claimed (registered open); '
                     'm=6 z=12 and m=5 z=12 are out of band; the '
                     'm=6/m=5 z=11 out-of-band separations are '
                     'claimed sharpness re-records (min>=7 '
                     'necessary: the (6,6) sign-flip witness and '
                     'the m=5 double witness)'),
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

    # B1: F11 mis-claimed as the Sigma-collapse v(s+1,11,13)
    #     (caught at the s=10 downward deviant AND the permanent
    #     s>=12 rebirth tail: 310/330 census-family deviants)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(13, (1,) + Y, 11) != single_token(s + 1, 11, 13):
            bad += 1
    rec('B1 F11 mis-claimed collapse v(s+1,11,13)', bad)
    clear_engines()
    # B2: F11(s>=12) tail corruption (2 -> 0; hides the REBIRTH of
    #     persistent-2 after its z=10 death)
    bad = 0
    for s in range(12, 19):
        for Y in decomps(s, 3):
            if H_canonical(13, (1,) + Y, 11) != 0:
                bad += 1
        clear_engines()
    rec('B2 F11(s>=12) tail corruption (2->0; hides the rebirth)', bad)
    # B3: F11(10) flip (1 -> 2; camouflages the s=10 DOWNWARD
    #     deviant as the collapse value v(11,11,13)=2)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 2 if sum(Y) == 10 else F11_table(sum(Y))
        if H_canonical(13, (1,) + Y, 11) != exp:
            bad += 1
    rec('B3 F11(10) flip (1->2; deviant camouflaged as collapse)', bad)
    clear_engines()
    # B4: G11 mis-claimed as the R2-form collapse v(s+2,11,14)
    #     (caught at the s=10 downward deviant: 4 census shapes)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(14, (2,) + Y, 11) != single_token(s + 2, 11, 14):
            bad += 1
    rec('B4 G11 mis-claimed collapse v(s+2,11,14)', bad)
    # B5: G11(10) flip (0 -> 1; camouflages the downward deviant
    #     as the collapse value v(12,11,14)=1)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 1 if sum(Y) == 10 else G11_table(sum(Y))
        if H_canonical(14, (2,) + Y, 11) != exp:
            bad += 1
    rec('B5 G11(10) flip (0->1; deviant camouflaged as collapse)', bad)
    clear_engines()
    # B6: E11 mis-claimed as collapse v(s+3,11,15) (caught at the
    #     two-sided s=8/s=10 deviant pair: 7 census shapes)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(15, (3,) + Y, 11) != single_token(s + 3, 11, 15):
            bad += 1
    rec('B6 E11 mis-claimed collapse v(s+3,11,15)', bad)
    clear_engines()
    # B7: E11(8) flip (1 -> 2; camouflages the s=8 DOWNWARD deviant
    #     as the collapse value v(11,11,15)=2)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 2 if sum(Y) == 8 else E11_table(sum(Y))
        if H_canonical(15, (3,) + Y, 11) != exp:
            bad += 1
    rec('B7 E11(8) flip (1->2; deviant camouflaged as collapse)', bad)
    # B8: E11(10) flip (2 -> 0; camouflages the s=10 UPWARD deviant
    #     as the collapse value v(13,11,15)=0)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 0 if sum(Y) == 10 else E11_table(sum(Y))
        if H_canonical(15, (3,) + Y, 11) != exp:
            bad += 1
    rec('B8 E11(10) flip (2->0; deviant camouflaged as collapse)', bad)
    clear_engines()
    # B9: D11 mis-claimed as a FULL collapse (falsely D11(8)=1);
    #     the floored sweep catches it at s=8 (self-absorption
    #     disguise)
    bad = 0
    for s in [0] + list(range(5, 21)):
        for Y in decomps(s, 5):
            if H_canonical(16, (4,) + Y, 11) != single_token(s + 4, 11, 16):
                bad += 1
        clear_engines()
    rec('B9 D11 mis-claimed full collapse (s=8)', bad)
    # B10: T-Z11 m=6 extension (the (6,6) SIGN-FLIP witness at z=11)
    bad = 0
    for X in T_shapes(6):
        if H_canonical(18, X, 11) != single_token(sum(X), 11, 18):
            bad += 1
    rec('B10 T-Z11 m=6 extension witness (6,6)', bad)
    clear_engines()
    # B11: ordered engine without the C-move XOR
    bad = 0
    for X in [(3, 3), (3, 4), (3, 3, 3), (2, 3), (4, 5), (2, 6)]:
        for z in (3, 4, 5, 6, 7, 8, 9, 10, 11):
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
    #      core forged: the a=m child value is v(S-1,11,m+11); the
    #      mutation mis-specifies the budget as m+10 and is caught)
    bad = 0
    for m in range(7, 11):
        R = m + 12
        for X in D9_shapes(m):
            S = sum(X)
            a_m = am_child_value(X, m, 11, R)
            exp_mut = single_token(S - 1, 11, m + 10)
            if a_m != exp_mut:
                bad += 1
        clear_engines()
    rec('B13 a=m child identity budget mutation (trivial-absorption '
        'forged)', bad)
    # B14: C11 C-hand child mis-specified as 1^D10t(s) (the z=11
    #      C-rank z=10 dependency forged); the option-set identity
    #      catches it (e.g. at s=0 and s in {6,8})
    bad = 0
    for s in [0] + list(range(6, 21)):
        for Y in decomps(s, 6):
            opts = child_opts_ordered((5,) + Y, 11, 17)
            exp = {single_token(s + 4, 11, 16), D11_table(s),
                   1 ^ D10t(s)}
            if opts != exp:
                bad += 1
        clear_engines()
    rec('B14 C11 C-hand child mis-specified 1^D10t(s)', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed:
        sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
DECLARED_TOTALS = {'points': 24746, 'comparisons': 44557}

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
        'theorem': ('Lemma F11 (persistent-2 REBIRTH: single '
                    's=10 DOWNWARD deviant 1<2 over the 5 shapes, '
                    's=11 agreement, then the permanent s>=12 UP '
                    'tail 2>0 -- persistent-2 dead at z=10 is '
                    'alive again at z=11)/G11 (single s=10 '
                    'DOWNWARD 0<1; the z=10 two-sided pair shrinks '
                    'to one side)/E11 (FIRST two-sided E deviant '
                    'pair: s=8 DOWN 1<2 and s=10 UP 2>0; '
                    'conditional recursion, unconditional ghost '
                    'agrees 3rd consecutive slice)/D11 (floored '
                    'single s=8 DOWNWARD 0<1; loose floor breaks '
                    'at s=10)/C11 (FIRST two-sided C deviant pair: '
                    's=6 DOWN 1<2 and s=8 UP 2>0, the s=6 cell '
                    'co-residing with the m=5 z=11 out-of-band '
                    'witness and the s=8 cell with the SECOND '
                    'witness -- the first double-witness m=5 '
                    'slice)/B11 (full collapse 3rd consecutive '
                    'slice)/A11 (full collapse 2nd consecutive '
                    'slice; C-hand child = published T-Z10) + '
                    'Theorem T-Z11: min>=7 critical-strip z=11 '
                    'slice with the SECOND TRIVIAL-ABSORPTION base '
                    'm=7 (a=7 child == stair option exactly, no '
                    'deviant child) + option-set identity induction. '
                    'z*(7)=13 so m=7 IS in band: the m=7 row of '
                    'K1268 Conjecture C1 is determined for '
                    'z in {0..11} leaving exactly {12} open. '
                    'Universal claims proved on paper in the '
                    'declaration note; this finite audit '
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
