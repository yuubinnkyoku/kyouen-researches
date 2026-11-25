#!/usr/bin/env python3
"""verify_strip_z9.py -- machine audit for the declared claims of the
single-owner declaration note (K1277 provisional; min>=6 critical-strip
z=9 slice; declaration note:
research/log/2026-11-24-strip-z9-min6-single-owner-note.md):

  Lemma F9 : F9(s) := H(11;{1}+Y;9) (Y tokens >=3, arity free, Y=() for
              s=0) is independent of the decomposition of s and
              F9(0)=1, F9(3)=0, F9(4)=1, F9(5)=0, F9(6)=1, F9(7)=0,
              F9(8)=1, F9(9)=0, F9(s>=10)=2. Vs the R2-form
              collapse v(s+1,9,11) the table has the s=8
              downward 3-shape deviant set {(8,),(3,5),(4,4)}
              (1<2) PLUS the persistent-2 family: every s>=10
              is an upward deviant 2>0 (e.g. (1,10) and (1,12)
              anchors), the first F-rung whose late table stays
              OFF the collapse for all large s. Extends the
              published F-ladder (F z in {1..4} K1272, F5 K1273,
              F6 K1274, F7 K1275, F8 K1276).
  Lemma G9 : G9(s) := H(12;{2}+Y;9) depends only on s and
              G9(0)=0, G9(3)=1, G9(4)=0, G9(5)=1, G9(6)=0, G9(7)=1,
              G9(8)=0, G9(9)=1, G9(s>=10)=1. The R2-form collapse
              v(s+2,9,12) fails exactly at s=8: deviants
              {(8,),(3,5),(4,4)} downward 0<1 (single deviant s;
              direction FLIPS the published G8 s=8 upward 2>1
              record at z=8).
  Lemma E9 : E9(s) := H(13;{3}+Y;9) depends only on s and
              E9(0)=1, E9(3)=0, E9(4)=1, E9(5)=0, E9(6)=1, E9(7)=0,
              E9(8)=2, E9(s>=9)=0. Deviants exactly
              {(6,),(3,3)} downward 1<2 and {(8,),(3,5),(4,4)}
              upward 2>0. The E9 recursion expectation is CONDITIONAL:
              {G9(s), 1^E8(s)} plus ({v(s+2,9,12)} iff some Y token
              is >= 4). NEW OBSERVATION vs z=8: the UNCONDITIONAL
              ghost form coincides with the conditional form over the
              full 3,657-decomposition family at z=9 (mismatch 0),
              recorded in the census; the z=8 break at Y=(3,3) was
              z-specific. The declared check keeps the CONDITIONAL
              form (the proven one).
  Lemma D9 : the first DOWNWARD floored D-rung:
              D9(s) := H(14;{4}+Y;9) with ALL Y tokens >=5 (s in
              {0} u {5,6,...}) depends only on s with table
              {6:0, else v(s+4,9,14)} -- the SINGLE s=6 downward
              deviant D9(6)=0 != v(10,9,14)=1 breaks the full-
              collapse series and FLIPS the published D8 s=6 upward
              deviant direction (z=8: 2>1). The floor min(Y)>=5 is
              essential: loosened to tokens>=3 the decomposition-
              dependence at s in {8,10} enters.
  Lemma C9 : C9(s) := H(15;{5}+Y;9) with ALL Y tokens >=6 depends
              only on s with table {6:2, else v(s+5,9,15)} -- the
              SINGLE s=6 upward deviant C9(6)=2 (same position as
              the published m=5 z=9 out-of-band witness) realizes
              the D9 s=6 downward deviant as a child value, and the
              parent mex absorbs it (upward flip of the D9 downward
              deviant, K1273/K1276-type absorption).
  Lemma B9 : B9(s) := H(16;{6}+Y;9) with ALL Y tokens >=7 FULLY
              collapses: B9(s) = v(s+6,9,16). Zero deviants, zero
              decomposition dependence (the B-rank full-collapse
              cell at z=9). The B9 recursion is the FIRST strip-
              theorem-dependent rung: its C-hand child value
              1^v(s+6,8,15) is the published T-Z8 (K1276) THEOREM
              position H(15;{6}+Y;8), not a cell table.
  Theorem T-Z9: for ALL m>=6, every nonempty finite multiset X with
              min(X)=m: H(m+10;X;9) = v(sum X, 9, m+10).
              Base m=6: all parent option families collapse
              (i) a>m stair children = v(S-1,9,15)=0 (published
              K1264 staircase window-edge equality),
              (ii) a=6 child = C9(S-6) in {0,2},
              (iii) C-hand child = 1^v(S,8,15) = 0 (published
              T-Z8, K1276) -> parent mex {0} (resp. {0,2}) =
              1 = v(S,9,16) (deviant-absorption base, same shape
              as K1273/K1276). m>=7 by option-set identity
              induction on m (a=m child = C(m-1,9) at
              R=m+9 = (m-1)+10, a>m children by K1264, C-hand
              child = published T-Z8) with option set {v(S-1,9,m+9),
              1^v(S,8,m+9)} exactly.
  Corollary: the z=9 row of the critical strip is determined for
              all m>=6; the m=6 row of K1268 Conjecture C1 is fully
              resolved including its last band cell z=9 (z*(6)=10);
              m>=7 rows keep z in {10..z*(m)-1} open; the z=10
              census is registered open with m=6 z=10 out-of-band
              (witness (6,6): parent 2 vs single 1, the frontier
              s=6 shape).

Declared checks (PUBLISH-THEN-EXECUTE):
  D1  Lemma F9: s in {0} u {3..40}, ALL decompositions into 1..4
      tokens >=3 (3,657)                          (3,657 / 10,971)
  D2  Lemma G9: Y = tokens 3..9 multisets, arity 0..4 (330) vs G9
      table; +1 arithmetic deviant-set comparison:
      {Y: G9 != v(s+2,9,12)} == {(3,5),(4,4),(8,)}
                                                     (330 / 991)
  D3  Lemma E9: same 330 shapes vs E9 table; +1 arithmetic deviant
      set == {(3,3),(3,5),(4,4),(6,),(8,)}            (330 / 991)
      (E9 deviants: s=6 downward + s=8 upward = 5 decompositions)
  D4  Lemma D9: s in {0} u {5..40}, ALL decompositions into 1..4
      tokens >=5 (1,650) vs {6:0, else v(s+4,9,14)}
                                                     (1,650 / 4,950)
  D4b Lemma C9: s in {0} u {6..40}, ALL decompositions into 1..4
      tokens >=6 (1,078) vs {6:2, else v(s+5,9,15)}
                                                     (1,078 / 3,234)
  D4c Lemma B9: s in {0} u {7..40}, ALL decompositions into 1..4
      tokens >=7 (700) vs full collapse v(s+6,9,16)
                                                       (700 / 2,100)
  D5  Theorem T-Z9 grid: m in {6..11} x z=9 x 222 shapes (R=m+10)
                                                     (1,332 / 3,996)
  D6  fixed-seed (20261128) random deep: m in {6..11} x 15 shapes
      (arity 4..5, tokens in [m,m+15], one token fixed at m)
                                                      (90 / 270)
  D7a published K1272/K1273/K1274/K1275 witness anchors (17)
                                                      (17 / 85)
  D7b theorem anchors 60 points (16 deviant/witness pair anchors:
      the F9 s=8 downward deviants {(8,),(3,5),(4,4)} and the
      persistent-2 family anchors (1,10)/(1,12); the G9 s=8
      downward deviants; the E9 s=6 downward + s=8 upward
      deviants; the D9 s=6 downward deviant; the C9 s=6 upward
      deviant (same position as the published m=5 z=9 out-of-band
      witness (5,6)); the m=6 z=10 out-of-band upward witness
      (6,6); + 44 standard anchors: F9/G9/E9/D9/C9/B9 cells, the
      m=6 single token and bottom parents, the bottom stair /
      C-hand / a=6 children, the published z=8 continuity, and
      the induction parents)
                                                      (60 / 180)
  D8  cell recursion option-set identity (paper proof secs
      2.1-2.6), 1 comparison per point (ordered child option set
      == arithmetic expectation set):
      F9 3,657 = {v(s,10,10), v(s,9,10), 1^F8(s)};
      G9 3,657 = {F9(s), v(s+1,9,11), 1^G8(s)};
      E9 3,657 = CONDITIONAL {G9(s), 1^E8(s)}
                  + ({v(s+2,9,12)}: some Y token >= 4);
      D9 1,650 = {v(s+3,9,13), E9(s), 1^D8(s)};
      C9 1,078 = {v(s+4,9,14), D9(s), 1^v(s+5,8,14)};
      B9   700 = {v(s+5,9,15), C9(s), 1^v(s+6,8,15)}
                                                   (14,399 / 14,399)
      where D9(s) in the C9 line and C9(s) in the B9 line are the
      declared floored tables (the C9 recursion realizes the D9
      s=6 deviant 0 as a child value and the parent mex absorbs
      it; the B9 C-hand line is the published T-Z8 theorem
      position, the first strip-theorem-dependent rung).
  D9  parent proof-structure option-set inspection: m in {6..10} x
      33 shapes. m=6: opts subset of {A'=v(S-1,9,15),
      c'=1^v(S,8,15), C9(S-6)} AND the a=6 child == C9(S-6)
      (the s=6 deviant absorption is observed at face value);
      m>=7: opts == {v(S-1,9,m+9), 1^v(S,8,m+9)} exact; parent mex
      == v(S,9,m+10) both engines                    (165 / 495)
  TOTAL declared: 23,808 points / 42,662 comparisons / bad 0.
  D6c census (NOT in declared totals; bad gate = engine disagreement
  only; observations are recorded, nothing claimed):
    (a) z=10 next-lane cell tables with the proper per-cell floors:
        F10 H(12;{1}+Y;10), G10 H(13;{2}+Y;10), E10 H(14;{3}+Y;10)
        over the 330 family (tokens 3..9, arity 0..4); D10
        H(15;{4}+Y;10) over the 126 floored family (tokens 5..9)
        and the loose 330 family (decomposition-dependence
        record); C10 H(16;{5}+Y;10) over the 70 family (tokens
        6..9); B10 H(17;{6}+Y;10) over the 35 family (tokens
        7..9); A10 H(18;{7}+Y;10) over the 15 family (tokens
        8..9). s-only tables, decomposition-dependence flags,
        deviant records vs v(s+k,10,R). The z=10 closed forms and
        the z=10 strip stay OPEN (registered open; not claimed).
    (b) z=10 strip grid: m in {6..11} x 96 census shapes (R=m+11):
        collapse record (m=6 is OUT of band: z*(6)=10; m>=7 in
        band 96/96 collapse expected from the probe but recorded
        only, not claimed).
    (c) m=6 z=10 out-of-band record over the 222 T-family (R=17):
        the single (6,6) separation (upward 2 vs 1) is expected
        and recorded (the frontier s=6 shape).
    (d) m=5 z=9 out-of-band record over the 222 T-family (R=15):
        the single (5,6) separation (upward 2 vs 0) is expected
        and recorded (re-record of the published witness).
    (e) E9 UNCONDITIONAL ghost form observation over the full
        3,657 family: mismatch count vs the conditional form
        (z=8 broke at Y=(3,3); z=9 recorded mismatch 0 from the
        pre-declaration probe -- the official machine re-records
        it; nothing claimed about z>=10).

Fail-closed: any bad>0 -> rc=1; declared-count mismatch -> rc=1
(honest record requirement). Finite machine audit is NOT the proof:
the universal claims rest on the paper proof in the declaration note
(F9/G9/E9/D9/C9/B9 closed-form ladder with the CONDITIONAL E9
recursion + mex base m=6 + option-set identity induction on m).
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
def F9_table(s):
    # Lemma F9 closed form (z=9 cell), s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1, 9: 0}.get(s, 2)

def G9_table(s):
    # Lemma G9 closed form (z=9 cell), s in {0} u {3,4,...}
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 0, 9: 1}.get(s, 1)

def E9_table(s):
    # Lemma E9 closed form (z=9 cell), s in {0} u {3,4,...}
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 2}.get(s, 0)

def D9_table(s):
    # Lemma D9 (floored family, tokens >=5): {6:0, else collapse}
    return 0 if s == 6 else single_token(s + 4, 9, 14)

def C9_table(s):
    # Lemma C9 (floored family, tokens >=6): {6:2, else collapse}
    return 2 if s == 6 else single_token(s + 5, 9, 15)

# published z=8 closed forms (K1276), used by the z=9 recursions
def F8t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1, 7: 0, 8: 1}.get(s, 0)

def G8t(s):
    return {0: 0, 3: 1, 4: 0, 5: 1, 6: 0, 7: 1, 8: 2}.get(s, 1)

def E8t(s):
    return {0: 1, 3: 0, 4: 1, 5: 0, 6: 1}.get(s, 0)

def D8t(s):
    return 2 if s == 6 else single_token(s + 4, 8, 13)

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
# D1: Lemma F9 full-decomposition sweep
# ---------------------------------------------------------------
def check_D1():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 11, 9
    for s in [0] + list(range(3, 41)):
        exp = F9_table(s)
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
# D2: Lemma G9 sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D2():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (2,) + Y
        exp = G9_table(s)
        hc = H_canonical(12, X, 9)
        ho = H_ordered(12, X, 9)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if G9_table(sum(Y)) != single_token(sum(Y) + 2, 9, 12))
    comps += 1
    if deviants != [(3, 5), (4, 4), (8,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D3: Lemma E9 sweep + arithmetic deviant set
# ---------------------------------------------------------------
def check_D3():
    pts, comps, bad = 0, 0, 0
    details = []
    fam = Y_tokens(3, 9)
    for Y in fam:
        s = sum(Y)
        X = (3,) + Y
        exp = E9_table(s)
        hc = H_canonical(13, X, 9)
        ho = H_ordered(13, X, 9)
        comps += 3
        if hc != exp or ho != exp or hc != ho:
            bad += 1
            if len(details) < 20:
                details.append((Y, hc, ho, exp))
        pts += 1
    clear_engines()
    deviants = sorted(Y for Y in fam
                      if E9_table(sum(Y)) != single_token(sum(Y) + 3, 9, 13))
    comps += 1
    if deviants != [(3, 3), (3, 5), (4, 4), (6,), (8,)]:
        bad += 1
        details.append(('deviant_set', [list(y) for y in deviants]))
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'deviants_arithmetic': [list(y) for y in deviants],
            'details_mismatch': details}

# ---------------------------------------------------------------
# D4: Lemma D9 sweep (floored family) vs {6:0, else collapse}
# ---------------------------------------------------------------
def check_D4():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 14, 9
    for s in [0] + list(range(5, 41)):
        exp = D9_table(s)
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
# D4b: Lemma C9 sweep (floored family, tokens >=6)
#       vs {6:2, else collapse v(s+5,9,15)}
# ---------------------------------------------------------------
def check_D4b():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 15, 9
    for s in [0] + list(range(6, 41)):
        exp = C9_table(s)
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
# D4c: Lemma B9 sweep (floored family, tokens >=7)
#       full collapse v(s+6,9,16)
# ---------------------------------------------------------------
def check_D4c():
    pts, comps, bad = 0, 0, 0
    details = []
    R, z = 16, 9
    for s in [0] + list(range(7, 41)):
        exp = single_token(s + 6, 9, 16)
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
# D5: Theorem T-Z9 grid
# ---------------------------------------------------------------
def check_D5():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 9
    for m in range(6, 12):
        R = m + 10
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
    rng = random.Random(20261128)
    z = 9
    for m in range(6, 12):
        R = m + 10
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
# K1272/K1273/K1274/K1275/K1276 machines D7a; 17 anchors)
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
# D7b: theorem anchors (60 points)
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
    # F9 s=8 downward deviants (1 < 2)
    dev_point('F9dev8a', (1, 8), 9, 11, 1, 2)
    dev_point('F9dev8b', (1, 3, 5), 9, 11, 1, 2)
    dev_point('F9dev8c', (1, 4, 4), 9, 11, 1, 2)
    # F9 persistent-2 family anchors (upward 2 > 0)
    dev_point('F9dev10', (1, 10), 9, 11, 2, 0)
    dev_point('F9dev12', (1, 12), 9, 11, 2, 0)
    # G9 s=8 downward deviants (0 < 1)
    dev_point('G9dev8a', (2, 8), 9, 12, 0, 1)
    dev_point('G9dev8b', (2, 3, 5), 9, 12, 0, 1)
    dev_point('G9dev8c', (2, 4, 4), 9, 12, 0, 1)
    # E9 s=6 downward deviants (1 < 2)
    dev_point('E9dev6a', (3, 6), 9, 13, 1, 2)
    dev_point('E9dev6b', (3, 3, 3), 9, 13, 1, 2)
    # E9 s=8 upward deviants (2 > 0)
    dev_point('E9dev8a', (3, 8), 9, 13, 2, 0)
    dev_point('E9dev8b', (3, 3, 5), 9, 13, 2, 0)
    dev_point('E9dev8c', (3, 4, 4), 9, 13, 2, 0)
    # D9 s=6 downward deviant (0 < 1)
    dev_point('D9dev6', (4, 6), 9, 14, 0, 1)
    # C9 s=6 upward deviant (2 > 0); same position as the published
    # m=5 z=9 out-of-band witness
    dev_point('C9dev6/m5z9oob', (5, 6), 9, 15, 2, 0)
    # m=6 z=10 out-of-band upward witness (frontier s=6 shape)
    dev_point('m6z10oob', (6, 6), 10, 17, 2, 1)
    # F9 cells
    for Y, s in [((3,), 3), ((4,), 4), ((5,), 5), ((6,), 6),
                 ((7,), 7), ((9,), 9)]:
        std_point('F9', (1,) + Y, 9, 11, F9_table(s))
    # G9 cells
    std_point('G9', (2, 3), 9, 12, G9_table(3))
    std_point('G9', (2, 5), 9, 12, G9_table(5))
    std_point('G9', (2, 7), 9, 12, G9_table(7))
    std_point('G9', (2, 9), 9, 12, G9_table(9))
    std_point('G9', (2, 5, 5), 9, 12, G9_table(10))
    # E9 cells
    std_point('E9', (3,), 9, 13, E9_table(0))
    std_point('E9', (3, 3), 9, 13, E9_table(3))
    std_point('E9', (3, 5), 9, 13, E9_table(5))
    std_point('E9', (3, 3, 3), 9, 13, E9_table(6))
    std_point('E9', (3, 7), 9, 13, E9_table(7))
    # D9 cells (floored: tokens >=5)
    std_point('D9', (4,), 9, 14, D9_table(0))
    std_point('D9', (4, 5), 9, 14, D9_table(5))
    std_point('D9', (4, 5, 5), 9, 14, D9_table(10))
    std_point('D9', (4, 6, 8), 9, 14, D9_table(14))
    std_point('D9', (4, 7), 9, 14, D9_table(7))
    # C9 cells (floored: tokens >=6)
    std_point('C9', (5,), 9, 15, C9_table(0))
    std_point('C9', (5, 7), 9, 15, C9_table(7))
    std_point('C9', (5, 7, 10), 9, 15, C9_table(17))
    std_point('C9', (5, 6, 10), 9, 15, C9_table(16))
    # B9 cells (floored: tokens >=7; full collapse)
    std_point('B9', (6,), 9, 16, single_token(6, 9, 16))
    std_point('B9', (6, 7), 9, 16, single_token(13, 9, 16))
    std_point('B9', (6, 7, 9), 9, 16, single_token(22, 9, 16))
    std_point('B9', (6, 8, 12), 9, 16, single_token(26, 9, 16))
    # m=6 single token + bottom parents at z=9, R=16
    std_point('m6', (6,), 9, 16, single_token(6, 9, 16))
    std_point('m6p', (6, 6), 9, 16, single_token(12, 9, 16))
    std_point('m6p', (6, 7), 9, 16, single_token(13, 9, 16))
    std_point('m6p', (6, 6, 6), 9, 16, single_token(18, 9, 16))
    # bottom children: (i) stair child of a token > 6;
    # (ii) C-hand child = published T-Z8 position;
    # (iii) a=6 child (C9 cell value)
    std_point('m6A', (6, 6), 9, 15, single_token(12, 9, 15))
    std_point('m6C', (6, 7), 8, 15, single_token(13, 8, 15))
    std_point('m6a6', (5, 7), 9, 15, C9_table(7))
    # published z=8 continuity anchors (K1276 F8/G8/E8/D8 cells
    # and the published z=8 C8 position)
    std_point('z8', (1, 8), 8, 10, F8t(8))
    std_point('z8', (2, 8), 8, 11, G8t(8))
    std_point('z8', (3, 6), 8, 12, E8t(6))
    std_point('z8', (4, 6), 8, 13, D8t(6))
    std_point('z8', (5, 6), 8, 14, single_token(11, 8, 14))
    # induction parents
    std_point('ind', (7, 7), 9, 17, single_token(14, 9, 17))
    std_point('ind', (9, 9), 9, 19, single_token(18, 9, 19))
    std_point('ind', (8, 8, 10), 9, 18, single_token(26, 9, 18))
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
    cell_opts(11, (1,), 9,
              lambda Y, s: {single_token(s, 10, 10), single_token(s, 9, 10),
                            1 ^ F8t(s)}, famF, 'F9')
    clear_engines()
    cell_opts(12, (2,), 9,
              lambda Y, s: {F9_table(s), single_token(s + 1, 9, 11),
                            1 ^ G8t(s)}, famF, 'G9')
    clear_engines()
    def e9_exp(Y, s):
        exp = {G9_table(s), 1 ^ E8t(s)}
        if any(t >= 4 for t in Y):
            exp.add(single_token(s + 2, 9, 12))
        return exp
    cell_opts(13, (3,), 9, e9_exp, famF, 'E9')
    clear_engines()
    famD = []
    for s in [0] + list(range(5, 41)):
        famD.extend(decomps(s, 5))
    cell_opts(14, (4,), 9,
              lambda Y, s: {single_token(s + 3, 9, 13), E9_table(s),
                            1 ^ D8t(s)}, famD, 'D9')
    clear_engines()
    famC = []
    for s in [0] + list(range(6, 41)):
        famC.extend(decomps(s, 6))
    cell_opts(15, (5,), 9,
              lambda Y, s: {single_token(s + 4, 9, 14), D9_table(s),
                            1 ^ single_token(s + 5, 8, 14)}, famC, 'C9')
    clear_engines()
    famB = []
    for s in [0] + list(range(7, 41)):
        famB.extend(decomps(s, 7))
    cell_opts(16, (6,), 9,
              lambda Y, s: {single_token(s + 5, 9, 15), C9_table(s),
                            1 ^ single_token(s + 6, 8, 15)}, famB, 'B9')
    clear_engines()
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'details_mismatch': details}

# ---------------------------------------------------------------
# D9: parent proof-structure option-set inspection
# ---------------------------------------------------------------
def check_D9():
    pts, comps, bad = 0, 0, 0
    details = []
    z = 9
    for m in range(6, 11):
        R = m + 10
        for X in D9_shapes(m):
            S = sum(X)
            opts = child_opts_ordered(X, z, R)
            vp = single_token(S, z, R)
            ho = H_ordered(R, X, z)
            hc = H_canonical(R, X, z)
            if m == 6:
                Ap = single_token(S - 1, 9, 15)
                cp = 1 ^ single_token(S, 8, 15)
                Dv = C9_table(S - 6)
                a6 = am_child_value(X, 6, z, R)
                rel_ok = (opts <= {Ap, cp, Dv}) and (a6 == Dv)
                rel_tag = 'subset+C9'
                expected = sorted({Ap, cp, Dv})
            else:
                A = single_token(S - 1, 9, m + 9)
                C = 1 ^ single_token(S, 8, m + 9)
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
# observations only, no strip/closed-form claims on z=10)
# ---------------------------------------------------------------
def check_D6c():
    res = {}
    pts = comps = bad = 0
    # (a) z=10 next-lane cell tables with proper per-cell floors
    cells = {}
    for tag, pre, R, dvoff, tmin, tmax in [
            ('F10', (1,), 12, 1, 3, 9), ('G10', (2,), 13, 2, 3, 9),
            ('E10', (3,), 14, 3, 3, 9), ('D10', (4,), 15, 4, 5, 9),
            ('C10', (5,), 16, 5, 6, 9), ('B10', (6,), 17, 6, 7, 9),
            ('A10', (7,), 18, 7, 8, 9)]:
        fam = Y_tokens(tmin, tmax)
        tbl = {}
        devs = []
        for Y in fam:
            s = sum(Y)
            X = pre + Y
            hc = H_canonical(R, X, 10)
            ho = H_ordered(R, X, 10)
            comps += 2
            if hc != ho:
                bad += 1
            tbl.setdefault(s, set()).add(hc)
            if hc != single_token(s + dvoff, 10, R):
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
    # (a2) D10 loose family (tokens 3..9): decomposition-dependence
    fam = Y_tokens(3, 9)
    tbl = {}
    devs = []
    for Y in fam:
        s = sum(Y)
        hc = H_canonical(15, (4,) + Y, 10)
        ho = H_ordered(15, (4,) + Y, 10)
        comps += 2
        if hc != ho:
            bad += 1
        tbl.setdefault(s, set()).add(hc)
        if hc != single_token(s + 4, 10, 15):
            devs.append(list(Y))
    dep = [s for s, v in sorted(tbl.items()) if len(v) > 1]
    tbl2 = {s: sorted(v) for s, v in sorted(tbl.items()) if s <= 20}
    cells['D10_loose'] = {'R': 15, 'floor': 3, 'family': len(fam),
                          'table_s20': {str(k): v for k, v in tbl2.items()},
                          'decomp_dependent_s': dep,
                          'deviant_count': len(devs),
                          'deviants_vs_collapse': devs[:40]}
    pts += len(fam)
    res['z10_cells'] = cells
    clear_engines()
    # (b) z=10 strip grid: m in {6..11} x 96 census shapes
    strip = {}
    for m in range(6, 12):
        z, R = 10, m + 11
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
    res['z10_strip'] = strip
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
    clear_engines()
    # (e) E9 UNCONDITIONAL ghost form observation (full family)
    famF = []
    for s in [0] + list(range(3, 41)):
        famF.extend(decomps(s, 3))
    mm = 0
    for i, Y in enumerate(famF):
        s = sum(Y)
        opts = child_opts_ordered((3,) + Y, 9, 13)
        expu = {G9_table(s), 1 ^ E8t(s), single_token(s + 2, 9, 12)}
        if opts != expu:
            mm += 1
        if i % 400 == 399:
            clear_engines()
    clear_engines()
    res['E9_uncond_ghost_mismatch'] = mm
    comps += len(famF)
    pts += len(famF)
    return {'points': pts, 'comparisons': comps, 'bad': bad,
            'note': ('census observation only; z=10 strip closed '
                     'forms are NOT claimed (registered open); '
                     'm=6 z=10 is out of band (z*(6)=10)'),
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

    # B1: F9 mis-claimed as the Sigma-collapse v(s+1,9,11)
    #     (caught at s=8 downward and s>=10 persistent family)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(11, (1,) + Y, 9) != single_token(s + 1, 9, 11):
            bad += 1
    rec('B1 F9 mis-claimed collapse v(s+1,9,11)', bad)
    clear_engines()
    # B2: F9(s>=10) corruption (2 -> 0; hides the persistent family)
    bad = 0
    for s in range(10, 17):
        for Y in decomps(s, 3):
            if H_canonical(11, (1,) + Y, 9) != 0:
                bad += 1
        clear_engines()
    rec('B2 F9(s>=10) corruption (2->0)', bad)
    # B3: G9(8) flip (0 -> 1; disguises the s=8 downward deviant
    #     as the collapse value)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 1 if sum(Y) == 8 else G9_table(sum(Y))
        if H_canonical(12, (2,) + Y, 9) != exp:
            bad += 1
    rec('B3 G9(8) flip (0->1)', bad)
    clear_engines()
    # B4: G9 mis-claimed as the R2-form collapse (caught at s=8)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(12, (2,) + Y, 9) != single_token(s + 2, 9, 12):
            bad += 1
    rec('B4 G9 mis-claimed collapse v(s+2,9,12)', bad)
    # B5: E9(8) flip (2 -> 0; hides the s=8 upward deviant)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 0 if sum(Y) == 8 else E9_table(sum(Y))
        if H_canonical(13, (3,) + Y, 9) != exp:
            bad += 1
    rec('B5 E9(8) flip (2->0)', bad)
    clear_engines()
    # B6: E9(6) flip (1 -> 2; disguises the s=6 downward deviant as
    #     the collapse value)
    bad = 0
    for Y in Y_tokens(3, 9):
        exp = 2 if sum(Y) == 6 else E9_table(sum(Y))
        if H_canonical(13, (3,) + Y, 9) != exp:
            bad += 1
    rec('B6 E9(6) flip (1->2)', bad)
    # B7: E9 mis-claimed as collapse v(s+3,9,13)
    bad = 0
    for Y in Y_tokens(3, 9):
        s = sum(Y)
        if H_canonical(13, (3,) + Y, 9) != single_token(s + 3, 9, 13):
            bad += 1
    rec('B7 E9 mis-claimed collapse v(s+3,9,13)', bad)
    clear_engines()
    # B8: D9 mis-claimed as a FULL collapse (falsely D9(6)=1);
    #     the floored sweep catches it at s=6
    bad = 0
    for s in [0] + list(range(5, 21)):
        for Y in decomps(s, 5):
            if H_canonical(14, (4,) + Y, 9) != single_token(s + 4, 9, 14):
                bad += 1
        clear_engines()
    rec('B8 D9 mis-claimed full collapse (D9(6)=1)', bad)
    # B9: T-Z9 min=5 extension (the (5,6) witness)
    bad = 0
    for X in T_shapes(5):
        if H_canonical(15, X, 9) != single_token(sum(X), 9, 15):
            bad += 1
    rec('B9 T-Z9 min=5 extension witness (5,6)', bad)
    clear_engines()
    # B10: ordered engine without the C-move XOR
    bad = 0
    for X in [(3, 3), (3, 4), (3, 3, 3), (2, 3), (4, 5), (2, 6)]:
        for z in (3, 4, 5, 6, 7, 8, 9):
            for R in range(1, 11):
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
    # B12: D9 a=m child identity mutations (m=6: the parent-side
    #      stair value instead of the C9-cell value, hiding the
    #      s=6 deviant; m>=7: budget m+8 instead of m+9)
    bad = 0
    for m in range(6, 10):
        R = m + 10
        for X in D9_shapes(m):
            S = sum(X)
            a_m = am_child_value(X, m, 9, R)
            if m == 6:
                exp_mut = single_token(S - 1, 9, 15)
            else:
                exp_mut = single_token(S - 1, 9, m + 8)
            if a_m != exp_mut:
                bad += 1
        clear_engines()
    rec('B12 D9 a=m child identity mutation (stair-value/budget-off)',
        bad)
    # B13: C9/B9 mis-claimed as constant-0 tables (the D4b/D4c
    #      expectation side destroyed; C9(0)=v(5,9,15)=1)
    bad = 0
    for s in [0] + list(range(6, 21)):
        for Y in decomps(s, 6):
            if H_canonical(15, (5,) + Y, 9) != 0:
                bad += 1
        clear_engines()
    for s in [0] + list(range(7, 21)):
        for Y in decomps(s, 7):
            if H_canonical(16, (6,) + Y, 9) != 0:
                bad += 1
        clear_engines()
    rec('B13 C9/B9 mis-claimed constant-0 tables', bad)
    # B14: C9 C-hand child mis-specified as 1^D8t(s) (the z=8
    #      D-rank dependency forged); the option-set identity
    #      check catches it (e.g. at s=0 and s=6)
    bad = 0
    for s in [0] + list(range(6, 21)):
        for Y in decomps(s, 6):
            opts = child_opts_ordered((5,) + Y, 9, 15)
            exp = {single_token(s + 4, 9, 14), D9_table(s),
                   1 ^ D8t(s)}
            if opts != exp:
                bad += 1
        clear_engines()
    rec('B14 C9 C-hand child mis-specified 1^D8t(s)', bad)
    missed = [r['mutation'] for r in results if r['bad'] == 0]
    print('TAMPER BATTERY:', 'ALL CAUGHT' if not missed else 'MISSED: ' + str(missed))
    if missed:
        sys.exit(1)
    sys.exit(0)

# ---------------------------------------------------------------
DECLARED_TOTALS = {'points': 23808, 'comparisons': 42662}

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
        'theorem': ('Lemma F9/G9/E9/D9 (floored, single s=6 '
                    'DOWNWARD deviant; direction flip of the D8 '
                    'upward)/C9 (single s=6 UPWARD deviant, same '
                    'position as the m=5 z=9 oob witness; mex-'
                    'absorbed by the base)/B9 (FULL collapse; '
                    'first strip-theorem-dependent rung) + Theorem '
                    'T-Z9: min>=6 critical-strip z=9 slice; the '
                    'm=6 row of K1268 Conjecture C1 fully resolved '
                    'incl. its last band cell z=9 (z*(6)=10) via '
                    'the conditional-E9 z=9 ladder + mex base m=6 '
                    '(deviant-absorption) + option-set identity '
                    'induction. Universal claims proved on paper '
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
