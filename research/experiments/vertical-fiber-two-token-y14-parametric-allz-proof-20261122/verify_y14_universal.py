#!/usr/bin/env python3
"""Universal verifier for the y=14 two-token residual family (PART 2).

Family: H(R; (x,14); z), all z >= 0, all x >= 14, all R >= 0.
Claim under test (K1233, currently status "observed"; this machine is the
promotion-stage part 1): the closed form cand14 (T/P row tables below)
equals H everywhere; with corollaries
  merge-below-diagonal (y=14 promotion of the y=13 line): x <= z-15
       =>  H == single_token(x+14, z, R)
  tail:                                 R >= x+z+15  =>  H == (x+14) % 2

STAGE: part 2 (C1d published fixed-z slice anchors at the y=14 rows and
the independent census_rows.py census.txt consumer are incorporated; on
overall PASS with 3 byte-identical audit runs K1233 is promoted
observed -> proved), per the procedure that promoted
y=5..y=13 (K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/
K1143/K1152/K1231).

Checks implemented and run here: C1, C1b, C1d, C2, C2b, C3, C4 (clip window
2y+2 = 30, sentinel 31), C4t (clip tightness probe 29/30), C7, C8, C9,
C11, C11r, C12.

Run modes:
  python3 verify_y14_universal.py                 # all checks except C11, C11r
  python3 verify_y14_universal.py C11ordered      # census part 1 (slow)
  python3 verify_y14_universal.py C11canonical   # census part 2 (slow)
  python3 verify_y14_universal.py C11             # merge census parts, then
                                                # run all checks incl. C11
  python3 verify_y14_universal.py C1 C2 ...       # explicit check list

  C1   raw order-preserving AND descending-canonical engines vs cand14,
       z=0..14, x=14..32, R=0..x+z+47
  C1b  single-token closed form (K0832) raw anchor; published y=13 closed
       form (K1231 transcription, the B-child of every y=14 point and the
       x=14 A-child) raw anchor; x=14 multiset merger (13,14)==(14,13)
       i.e. A==B child value raw anchor
  C1d  published fixed-z slice anchors (z=8/9/10/15/16/17,
       K0999/K1000/K1001/K1011/K1065/K1077/K1087) evaluated at the y=14
       row vs cand14, x=14..159, R<=x+61; + published low-R single-token
       reduction R<=z+6 (z=15..17). Pre-flighted fail-closed against both
       raw engines and cand14 (scripts/preflight_c1d_y14.py) before
       incorporation
  C2   closed-form identity grid z=0..48, x=14..58, R<=x+z+41 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {14,19,...,64}, R <= x+z+31
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window 2y+2 = 30 sentinel 31, free-coordinate
       box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep, per-type
       confluence of the (value, sorted-children) effect
  C4t  tightness probe: the same box at clip 29 counts confluence
       violations (informational, not part of the bad total) -- tests
       the 10-family continuation candidate of the tight 2y+2 clip
       pattern (y=5..13: 12/14/16/18/20/22/24/26/28; 2y+2 for y=14 is 30)
  C7   fixed-seed far probes (seed 20261142): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+15
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301,
       999..1001, 2999, 3000}, dx in [-30, 17], tail window
       [x+z+15, x+z+17]
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=14..70, R<=x+z+15, both engines,
       plus merge/tail corollaries. Because this execution host is
       memory-capped, the census runs each raw engine in its own command
       (C11ordered / C11canonical) through a BOUNDED-MEMOIZATION twin
       of the verbatim engine (identical recursive definition,
       existing LRU-capped cache; memoization of a deterministic pure
       function is transparent, and LRU eviction is deterministic under
       the fixed visit order). Each part writes output/census-<engine>.json;
       the C11 mode validates both parts (engine name, census geometry
       point counts, corollary counts recomputed from formulas, bad == 0
       fail-closed) and merges them. The unbounded verbatim engines
       still anchor C1, C1b, C3.
  C11r independent census ledger consumer: every row of the raw
       double-recursion census.txt (census_rows.py third implementation,
       z=0..79, x=14..70, R=0..x+z+16) is re-derived from cand14 here
       (T/P sets, Thue-Morse index, tail), fail-closed on a missing,
       duplicate or misaligned ledger (rows must be 80*57 = 4,560)
  C12  deep closed grid z=0..120, x=14..120, R<=x+z+17

Trust boundary (same machine class as the y=5..y=13 promotion machines
K1023/K1099/K1104/K1112/K1126/K1127/K1131/K1135/K1138/K1141/K1143-part1/
K1162/K1231-part1): option decomposition + closed-form mex identity +
finite-type confluence over the free-coordinate box, anchored to raw
engines, to the published y=13 family (K1231 proved, the B-child), to
the x=14 multiset merger ((13,14)==(14,13)) and (C1d) to the published
z=8/9/10/15/16/17 slice closed forms
(K0999/K1000/K1001/K1011/K1065/K1077/K1087) at the y=14 rows. The family law shifts
carried from y=13 to y=14 (even-y type, same as y=10/y=12: value-1
infinite band and tail on x odd rows; pin lattice (d+42)%4==0 at z odd
with o_pin=(d+42)/2 in [15,28], z-odd 7 rows d in
{-10,-6,-2,2,6,10,14} / z-even 7 rows d in {-12,-8,-4,0,4,8,12} -- the
first even-y family with 7 pin rows in BOTH parities and the mod-4
class rotation (y=12 d==0 -> y=14 d==2) inside the same unified
lattice; z-odd I rows k(d)=floor((d+3y+2)/4) with the mixed th rule
th=2k+[d==y mod 4] sweeping 15..29, pin slot = th-1 (4th consecutive
family); sweep row d=15; steady pins z+28/z+29; band bottom 2y+2=30;
tail x+z+15; merge x<=z-15; even-z diagonal without value 1 (7th
consecutive candidate family); base rows k(d)=floor((d+3y+1)/4)) are
all inside the audited tables, not assumed separately.

Published transcriptions inside this file:
  engines + K0832 single_token (raw engines H_ordered/H_canonical, the
  K0832 single-token closed form and its helpers): verbatim from the
  published verify_y13_universal.py part1 (K1231 promotion machine,
  commit ee3b6f73, SHA-256 b73d9aaa94f04f1f4922d84808ac7afe6f5bfb55631b4c990cae29734279141f;
  the engine section is identical in the part2 publication, SHA-256
  079b49ad...), whose own provenance chain is the published
  verify_y12_universal.py (K1162/K1152 promotion machine), verify_y11_
  universal.py (K1143 part 1), verify_y10_universal.py (K1141) and
  verify_y09_universal.py (K1138);
  cand13 (the B-child of every y=14 point and the x=14 merger child):
  verbatim from the published verify_y13_universal.py's cand13 block
  (block-local Y renamed to Y13 so the cand14 block can carry Y = 14;
  that block is itself the published cand13.py transcription minus the
  fit driver; its universal proof is K1231);
  cand14: verbatim from the published cand14.py (K1233 fit experiment,
  commit b6f74dfc, SHA-256 61782b6e0a6dde7717dff9ac672299c918e6400bf18dad47ea419a9f081b961e),
  fit driver omitted (its probe self-check is K1233's own evidence,
  re-runnable there; an independent second verification of that fit --
  including a 2,241,162-point verdict-equivalence of two independently
  derived cand14s -- was published 2026-11-22 in
  vertical-fiber-two-token-y14-parametric-fit-second-verification-20261122);
  the re-defined q_odd/single_token_val copies inside the cand13/cand14
  blocks are semantically identical to the shared body (last definition
  wins at call time, as in the published y=10..y=13 verifiers);
  published fixed-z slice anchors A8u..A17u (C1d): verbatim block from
  the published verify_y13_universal.py part2's anchor section (itself the
  y=10 part2 verifier's transcription of the published slice verifiers,
  K0999/K1000/K1001/K1011/K1065/K1077/K1087), evaluated at the y=14 row
  only after the fail-closed pre-flight (scripts/preflight_c1d_y14.py);
Their correctness is K0832/K1231/K1233's claim, not re-proven here; every
transcription is additionally re-anchored against the raw
order-preserving engine by this machine's C1/C1b, and cand13's y=14-scope
usage is inside its published universal domain (x >= 13 ... x >= 14,
all z, all R, of the K1231 universal proof).
Determinism: fixed seed, no clock, sorted audit keys, census parts
deterministic under the fixed visit order and LRU cap.
"""

import hashlib
import json
import random
import sys
import types
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


# ------------------------------------------------------------------
# Raw engines (verbatim from the published K1138 verifier).
# ------------------------------------------------------------------
@lru_cache(None)
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


@lru_cache(None)
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




# =====================================================================
# Published y=13 two-token closed form (K1231 proved). This is the
# B-child of every y=14 point and the x=14 merger child value. Code
# block verbatim from the published verify_y13_universal.py cand13
# block (block-local Y renamed to Y13 so the cand14 block can carry
# Y = 14; that block is itself the published cand13.py transcription
# minus the fit driver; its universal proof is K1231).
# =====================================================================

Y13 = 13

def q_odd(k):
    return k if k % 2 == 1 else k - 1

def single_token_val(S, R):
    # K0832 published single-token closed form, z-independent rows (merge region)
    if R == 0:
        return 0
    if R % 2 == 1 and R <= q_odd(S):
        return 2
    if S % 2 == 1 and R >= q_odd(S) + 1:
        return 1
    return 0

def in_T13(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y13 - 1:
        S = x + Y13
        return R % 2 == 1 and R <= q_odd(S)
    d = x - z
    o = R - z
    if d == -Y13:
        cap = (z + Y13 - 1) if z % 2 == 1 else (z + Y13)
        if R % 2 == 1 and R <= (z if z % 2 == 1 else z - 1):
            return True
        if z % 2 == 1:
            return o % 2 == 0 and 2 <= o <= cap - z
        else:
            return o % 2 == 1 and 1 <= o <= cap - z
    if z % 2 == 1:
        ladder = R % 2 == 1 and R <= z
        if (d + 3 * Y13) % 4 == 0:
            o_pin = (d + 3 * Y13) // 2
            if Y13 + 1 <= o_pin <= 2 * Y13 and R == z + o_pin:
                return True
        if d == Y13 + 1:
            return ladder or (o % 2 == 0 and 2 * Y13 <= o <= x + Y13)
        if d >= Y13 + 2:
            return ladder or R == z + 2 * Y13
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if (d + 3 * Y13) % 4 == 2:
            o_pin = (d + 3 * Y13) // 2
            if Y13 + 1 <= o_pin <= 2 * Y13 and R == z + o_pin:
                return True
        if d == Y13 + 1:
            return ladder or (o % 2 == 1 and 2 * Y13 + 1 <= o <= x + Y13)
        if d >= Y13 + 2:
            return ladder or R == z + 2 * Y13 + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P13(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y13 - 1:
        S = x + Y13
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b13 = _bk(off, Y13)
    band_base = off % 2 == 0 and 2 * Y13 + 2 <= off <= x + Y13          # steady base rows
    band_int = off % 2 == 0 and 2 * Y13 + 2 <= off <= x + Y13 - 1       # steady I rows
    tail = x % 2 == 0 and R >= x + z + Y13 + 1                          # S odd rows (y=13: x even)
    if z % 2 == 1:
        if -Y13 <= d <= Y13 and d % 2 == 1:
            k = (d + 40) // 4         # I rows: b_k U I[2k+1)  (diag d=-13 included, k=6)
            return _bk(off, k) or off >= 2 * k + 1
        if d == Y13 + 1:
            return b13                 # sweep row, base type: z odd x odd
        if d >= Y13 + 2:
            if d % 2 == 0:
                return b13 or band_base
            return b13 or band_int or tail
        return _bk(off, (d + 40) // 4)  # base rows d even in [-12,12]
    else:
        if d == -Y13:
            return False                # even-z diagonal: no value-1 at all (fit level, 6th consecutive)
        if d == Y13 + 1:
            return b13 or band_int or tail   # sweep row, I type: z even x even
        if d >= Y13 + 2:
            if d % 2 == 1:
                return b13 or band_base
            return b13 or band_int or tail
        if d % 2 == 0:
            k = (d + 38) // 4          # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        return _bk(off, (d + 40) // 4)  # base rows d odd in [-11,13]

def cand13(z, x, R):
    if R <= 0:
        return 0
    if in_T13(z, x, R):
        return 2
    if in_P13(z, x, R):
        return 1
    return 0


# =====================================================================
# Candidate under test: y=14 two-token closed form (K1233 published fit).
# cand14 tables verbatim from the published cand14.py (K1233 fit
# experiment); fit driver omitted. The y=13 family (cand13 block above)
# is the B-child of this identity and the x=14 merger child value.
# =====================================================================

Y = 14

def q_odd(k):
    return k if k % 2 == 1 else k - 1

def single_token_val(S, R):
    # K0832 published single-token closed form, z-independent rows (merge region)
    if R == 0:
        return 0
    if R % 2 == 1 and R <= q_odd(S):
        return 2
    if S % 2 == 1 and R >= q_odd(S) + 1:
        return 1
    return 0

def in_T14(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return R % 2 == 1 and R <= q_odd(S)
    d = x - z
    o = R - z
    if d == -Y:
        if R % 2 == 1 and R <= (z if z % 2 == 1 else z - 1):
            return True
        if z % 2 == 1:
            return o % 2 == 0 and 2 <= o <= Y
        return o % 2 == 1 and 1 <= o <= Y - 1
    if z % 2 == 1:
        ladder = R % 2 == 1 and R <= z
        if (d + 3 * Y) % 4 == 0 and -Y + 4 <= d <= Y:
            if R == z + (d + 3 * Y) // 2:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 0 and 2 * Y <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y
        return ladder
    else:
        ladder = R % 2 == 1 and R <= z - 1
        if (d + 3 * Y) % 4 == 2 and -Y + 2 <= d <= Y - 2:
            if R == z + (d + 3 * Y) // 2:
                return True
        if d == Y + 1:
            return ladder or (o % 2 == 1 and 2 * Y + 1 <= o <= x + Y)
        if d >= Y + 2:
            return ladder or R == z + 2 * Y + 1
        return ladder

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P14(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    b14 = _bk(off, Y)
    band = off % 2 == 0 and 2 * Y + 2 <= off <= x + Y          # steady/sweep even band
    tail = x % 2 == 1 and R >= x + z + Y + 1                    # S odd rows (y=14: x odd)
    if z % 2 == 1:
        if -Y <= d <= Y and d % 2 == 0:
            k = (d + 3 * Y + 2) // 4          # I rows: b_k U I[th) (diag d=-14 incl., k=7)
            th = 2 * k + (1 if (d + 3 * Y) % 4 == 0 else 0)   # pin rows (d==y mod4): 2k+1; skew: 2k
            return _bk(off, k) or off >= th
        if -Y + 1 <= d <= Y - 1 and d % 2 == 1:
            return _bk(off, (d + 3 * Y + 1) // 4)  # base rows d odd
        if d == Y + 1:
            return b14                          # sweep row, base type: z odd x even
        return b14 or band or tail              # d >= Y+2 steady rows
    else:
        if d == -Y:
            return False                        # even-z diagonal: no value-1 (7th consecutive candidate)
        if -Y + 1 <= d <= Y - 1 and d % 2 == 1:
            k = (d + 3 * Y - 1) // 4           # I rows: b_k U I[2k+1)
            return _bk(off, k) or off >= 2 * k + 1
        if -Y + 2 <= d <= Y and d % 2 == 0:
            return _bk(off, (d + 3 * Y + 1) // 4)  # base rows d even in [-12, 14]
        return b14 or band or tail              # d >= Y+1 (sweep 15 incl.: x odd -> tail active)

def cand14(z, x, R):
    if R <= 0:
        return 0
    if in_T14(z, x, R):
        return 2
    if in_P14(z, x, R):
        return 1
    return 0


# =====================================================================
# Published fixed-z slice anchors (C1d), verbatim block from the y=10
# part2 verifier verify_y10_universal.py (published, SHA-256
# f9169449309dcd25aaba8d6379d4289167f61eb3895b031e45ff9e80c46c05e4), whose
# own provenance chain is the published slice verifiers (z=8: K0999/K1000
# verify_z8_y_ge9_proof.py e88e5ea7...; z=9: K1001 verify_z9_y_ge9_proof.py
# db1d60c6...; z=10: K1011 scope verify_z10_y_ge9_proof.py 42db00b2...;
# z=15: K1065 verify_z15_y_ge6.py 131e1c64...; z=16: K1077
# verify_z16_y_ge6.py d07c3b0e...; z=17: K1087 verify_z17_y_ge6.py
# e49d24d2...). Kept in their published parametric (x, y, r) form and
# evaluated at the y=14 row. Pre-flighted fail-closed at the y=14 rows
# before incorporation (scripts/preflight_c1d_y14.py: 13,824 anchor
# points + 9,636 low-R reduction points, three-way vs raw engines and
# cand14, all clean; the y=10 pre-flight of the same transcriptions
# caught an evaluation-order bug in the K1087 first draft, 170 points).
# =====================================================================

# ------------------------------------------------------------------
# Published fixed-z slice anchors specialised at y=10 (C1d).
# Independent of the cand10 tables above. Uniform closed forms kept in
# their published parametric (x,y,r) form and evaluated at the y=10 row:
#   z=8:  K0999/K1000 uniform candidate, scope x>=y>=9
#         (verify_z8_y_ge9_proof.py, SHA-256 e88e5ea7...)
#   z=9:  K1001 uniform candidate, scope x>=y>=9
#         (verify_z9_y_ge9_proof.py, SHA-256 db1d60c6...)
#   z=10: K1002 uniform candidate restricted to y>=9 = the K1011 proof
#         scope (verify_z10_y_ge9_proof.py, SHA-256 42db00b2...)
#   z=15: K1065 uniform y>=6 family (verify_z15_y_ge6.py,
#         SHA-256 131e1c64...); the small-y transitional cells
#         (y,d) in {(6,0),(6,1),(6,2),(7,0),(6,3),(7,1)} are unreachable
#         at y=10, so the published generic rows apply as-is
#   z=16: K1077 uniform y>=6 family (verify_z16_y_ge6.py,
#         SHA-256 d07c3b0e...); unreachable transitional (y,d) cells
#         at y=10 likewise
#   z=17: K1087 uniform y>=6 family (verify_z17_y_ge6.py,
#         SHA-256 e49d24d2...); the S<17 / S==17 transitional branches
#         are unreachable at y=10 (S=x+10>=20)
# Every anchor was pre-validated against both raw engines at the y=10
# rows before incorporation (pre-flight box: z fixed, x=10..45,
# R<=x+z+30: 15,336 points, mismatch 0, both engines).
# ------------------------------------------------------------------


def _od(r, a, b):
    return r % 2 == 1 and a <= r <= b


def _ev(r, a, b):
    return r % 2 == 0 and a <= r <= b


def A8u(x, y, r):
    """K0999/K1000 published uniform form: H(R;(x,y);8), x>=y>=9."""
    if r == 0:
        return 0
    if r >= x + y + 9:
        return (x + y) % 2
    d = x - y
    t = (r in (1, 3, 5, 7) or
         (d == 2 and r == 2 * y + 5) or
         (d == 6 and r == 2 * y + 7) or
         (d == 9 and _od(r, 2 * y + 9, 2 * y + 17)) or
         (d >= 10 and r == 2 * y + 9))
    if t:
        return 2
    if d == 0:
        p = _od(r, 9, 2 * y + 3)
    elif d == 1:
        p = _od(r, 9, 2 * y + 9) or _ev(r, 2 * y + 6, 2 * y + 9)
    elif d == 2:
        p = _od(r, 9, 2 * y + 3)
    elif d == 3:
        p = _od(r, 9, 2 * y + 11) or _ev(r, 2 * y + 6, 2 * y + 11)
    elif d == 4:
        p = _od(r, 9, 2 * y + 5)
    elif d == 5:
        p = _od(r, 9, 2 * y + 13) or _ev(r, 2 * y + 8, 2 * y + 13)
    elif d == 6:
        p = _od(r, 9, 2 * y + 5)
    elif d == 7:
        p = _od(r, 9, 2 * y + 15) or _ev(r, 2 * y + 8, 2 * y + 15)
    elif d == 8:
        p = _od(r, 9, 2 * y + 7)
    elif d == 9:
        p = _od(r, 9, 2 * y + 7) or _ev(r, 2 * y + 10, 2 * y + 16)
    else:
        p = _od(r, 9, 2 * y + 7) or _ev(r, 2 * y + 10, x + y + 8)
    return 1 if p else 0


def A9u(x, y, r):
    """K1001 published uniform form: H(R;(x,y);9), x>=y>=9."""
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
         (d == 10 and _od(r, 2 * y + 9, 2 * y + 19)) or
         (d >= 11 and r == 2 * y + 9))
    if t:
        return 2
    if d == 10:
        p = _ev(r, 10, 2 * y + 8)
    elif d % 2 == 1:
        if d <= 3:
            p = _ev(r, 10, 2 * y + 6) or r >= 2 * y + 7
        elif d <= 7:
            p = _ev(r, 10, 2 * y + 8) or r >= 2 * y + 9
        elif d == 9:
            p = _ev(r, 10, 2 * y + 8) or r >= 2 * y + 10
        else:
            p = _ev(r, 10, 2 * y + 8) or _od(r, 2 * y + 11, top)
    else:
        if d <= 2:
            ht = 2 * y + 4
        elif d <= 6:
            ht = 2 * y + 6
        else:
            ht = 2 * y + 8
        if d >= 12:
            p = _ev(r, 10, ht) or _od(r, 2 * y + 11, top)
        else:
            p = _ev(r, 10, ht)
    return 1 if p else 0


def A10u(x, y, r):
    """K1002 uniform form restricted to y>=9 (K1011 proof scope):
    H(R;(x,y);10), x>=y>=9."""
    if r == 0:
        return 0
    S = x + y
    if r >= S + 11:
        return S % 2
    d = x - y
    t = (r in (1, 3, 5, 7, 9) or
         (d in (0, 4, 8) and r == 2 * y + 5 + d // 2) or
         (d == 11 and _od(r, 2 * y + 11, S + 10)) or
         (d >= 12 and r == 2 * y + 11))
    if t:
        return 2
    if d % 2 == 0 and d <= 10:
        p = _od(r, 11, 2 * y + 3 + 2 * ((d + 3) // 4))
    elif d % 2 == 0:
        p = _od(r, 11, 2 * y + 9) or _ev(r, 2 * y + 12, S + 10)
    elif d <= 9:
        p = _od(r, 11, S + 10) or _ev(r, 2 * y + 6 + 2 * ((d + 1) // 4), S + 9)
    else:
        p = _od(r, 11, 2 * y + 9) or _ev(r, 2 * y + 12, S + 9)
    return 1 if p else 0


def A15u(x, y, r):
    """K1065 published uniform form: H(R;(x,y);15), x>=y>=6.
    The (y,d) transitional cells are unreachable at y=10."""
    d = x - y
    Y = 2 * y
    S = x + y
    if r == 0:
        return 0
    if r >= S + 16:
        return S % 2
    t = (_od(r, 1, 15) or
         (d in (3, 7, 11, 15) and r == Y + (d + 15) // 2) or
         (d == 16 and _od(r, Y + 15, S + 15)) or
         (d >= 17 and r == Y + 15))
    if t:
        return 2
    if d % 2 == 0 and d <= 14:
        p = _ev(r, 16, Y + 6 + 2 * ((d + 3) // 4))
    elif d % 2 == 1 and d <= 15:
        p = (_ev(r, 16, S + 15) or _od(r, Y + 7 + 2 * ((d + 5) // 4), S + 14)
             or r >= S + 16)
    elif d == 16:
        p = _ev(r, 16, Y + 14)
    else:
        hi = S + (15 if d % 2 == 0 else 14)
        p = (_ev(r, 16, Y + 14) or _od(r, Y + 17, hi)
             or (d % 2 == 1 and r >= S + 16))
    return 1 if p else 0


def A16u(x, y, r):
    """K1077 published uniform form: H(R;(x,y);16), x>=y>=6.
    The (y,d) transitional cells are unreachable at y=10."""
    d = x - y
    Y = 2 * y
    S = x + y
    if r == 0:
        return 0
    if r >= S + 17:
        return S % 2
    t = (_od(r, 1, 15) or
         (d in (2, 6, 10, 14) and r == Y + (d + 16) // 2) or
         (d == 17 and _od(r, Y + 17, S + 16)) or
         (d >= 18 and r == Y + 17))
    if t:
        return 2
    if d % 2 == 0 and d <= 14:
        p = _od(r, 17, Y + 7 + 2 * (d // 4))
    elif d % 2 == 1 and d <= 15:
        p = (_od(r, 17, S + 16) or _ev(r, Y + 10 + 2 * ((d - 1) // 4), S + 15)
             or r >= S + 17)
    elif d == 16:
        p = _od(r, 17, Y + 15)
    elif d % 2 == 1:
        p = (_od(r, 17, Y + 15) or _ev(r, Y + 18, S + 15) or r >= S + 17)
    else:
        p = _od(r, 17, Y + 15) or _ev(r, Y + 18, S + 16)
    return 1 if p else 0


def A17u(x, y, r):
    """K1087 published uniform form: H(R;(x,y);17), x>=y>=6.
    T fully evaluated before P (value17 order); the S<17 and S==17
    transitional branches are unreachable at y=10 (S=x+10>=20)."""
    d = x - y
    Y = 2 * y
    S = x + y
    if r == 0:
        return 0
    if r >= S + 18:
        return S % 2
    if _od(r, 1, 17):
        return 2
    if d == 18 and _od(r, Y + 17, S + 17):
        return 2
    if d >= 19 and r == Y + 17:
        return 2
    if d % 2 == 1 and d % 4 == 1 and d <= 17 and r == Y + (d + 17) // 2:
        return 2
    if d >= 19:
        if _ev(r, 18, Y + 16):
            return 1
        if _od(r, Y + 19, S + 17):
            return 1
        if S % 2 == 1 and r >= S + 18:
            return 1
        return 0
    if d == 18:
        return 1 if _ev(r, 18, Y + 16) else 0
    if d % 2 == 1:
        rt = Y + (d + 17) // 2
        if d % 4 == 1:
            p = _ev(r, 18, rt - 1) or r >= rt + 1
        else:
            p = _ev(r, 18, rt - 2) or r >= rt
        return 1 if p else 0
    U = Y + 8 + 2 * (d // 4)
    return 1 if _ev(r, 18, U) else 0


# =====================================================================
# Option decomposition and the identity under test (y=14 family).
# =====================================================================
def opts14(z, x, R):
    """Closed-form option values of H(R; (x,14); z). R >= 1.

    x == 14: both token-decrement children coincide as multisets:
    (13,14) == (14,13), both are the y=13 family row x=14.
    """
    if x == 14:
        A = cand13(z, 14, R - 1)
    else:
        A = cand14(z, x - 1, R - 1)
    out = [A, cand13(z, x, R - 1)]
    if z >= 1:
        out.append(1 ^ cand14(z - 1, x, R - 1))
    return out


def identity_ok14(z, x, R):
    t = in_T14(z, x, R)
    pv = in_P14(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    got = mex(opts14(z, x, R))
    want = cand14(z, x, R)
    return got == want, got, want


# ------------------------------------------------------------------
# Type machine. y=13's clip window (+/-28 sentinel +/-29) folded the
# y=13 features; the y=14 features (pins up to z+28 odd-z / z+29 even-z,
# sweep band d=15 offsets up to x+14, band bottom R-z = 2y+2 = 30,
# tail offset R-x-z = 15, merge boundary x = z-15, base span to z+27
# and the I-row th(d) excursions up to 29) are tested with +/-30/31
# (= 2y+2 for y=14), the 10-family-continuation candidate of the 2y+2
# tight pattern (y=5..13: 12/14/16/18/20/22/24/26/28). CLIP/SENT are
# re-checked for confluence by check_C4; the tightness probe (CLIP=29)
# is reported separately (check_C4t).
# ------------------------------------------------------------------
CLIP, SENT = 30, 31


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of14(z, x, R):
    return (1 if x == 14 else 0,
            1 if z == 0 else 0,
            z % 2, x % 2, R % 2,
            clipw(x - z), clipw(R - x), clipw(R - z),
            clipw(R - x - z), clipw(R - 2 * x), clipw(R - 2 * z))


def vpoint(v0, v1, v3):
    z = v1 - v3
    x = v0 + v1 - v3
    R = v0 + 2 * v1 - v3
    return z, x, R


# ------------------------------------------------------------------
# Checks.
# ------------------------------------------------------------------
def check_C1(audit):
    n = bad = 0
    for z in range(0, 15):
        for x in range(14, 33):
            for R in range(0, x + z + 48):
                n += 1
                c = cand14(z, x, R)
                if H_ordered(R, (x, 14), z) != c or H_canonical(R, (x, 14), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand14 z=0..14 x=14..32 R<=x+z+47',
                   'points': n, 'bad': bad}


def check_C1b(audit):
    n = bad = 0
    # (i) single-token closed form (K0832) vs raw ordered engine
    for z in range(0, 21):
        for x in range(1, 21):
            for R in range(0, x + z + 21):
                n += 1
                if H_ordered(R, (x,), z) != single_token(x, z, R):
                    bad += 1
    # (ii) published y=13 closed form (K1231, the B-child) raw anchor
    for z in range(0, 25):
        for x in range(13, 28):
            for R in range(0, x + z + 30):
                n += 1
                if H_ordered(R, (x, 13), z) != cand13(z, x, R):
                    bad += 1
    # (iii) x=14 multiset merger: (13,14) == (14,13) raw, and == cand13(z,14,R-1)
    for z in range(0, 31):
        for R in range(1, z + 43):
            n += 1
            a = H_ordered(R - 1, (13, 14), z)
            b = H_ordered(R - 1, (14, 13), z)
            c = H_canonical(R - 1, (13, 14), z)
            if a != b or a != c or a != cand13(z, 14, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=13-child/x=14 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C1d(audit):
    """Published fixed-z slice anchors (z=8/9/10/15/16/17) at the y=14 row
    vs cand14; anchors pre-flighted fail-closed against both raw engines
    and cand14 (scripts/preflight_c1d_y14.py) before incorporation. Anchor
    sweeps mirror the published y=10/y=12/y=13 part2 C1d: x=14..159,
    R<=x+61. Includes the published low-R single-token reduction R<=z+6
    (z=15..17).
    """
    n = bad = 0
    anchors = ((8, A8u), (9, A9u), (10, A10u), (15, A15u), (16, A16u), (17, A17u))
    for z0, fn in anchors:
        for x in range(14, 160):
            for r in range(1, x + 62):
                n += 1
                if fn(x, 14, r) != cand14(z0, x, r):
                    bad += 1
    # published low-R single-token reduction of the fixed-z y>=6 slices
    # (R<=z+6) checked directly on the y=14 rows
    n_low = bad_low = 0
    for z0 in (15, 16, 17):
        for x in range(14, 160):
            for R in range(1, z0 + 7):
                n_low += 1
                if cand14(z0, x, R) != single_token(x + 14, z0, R):
                    bad_low += 1
    audit['C1d'] = {'desc': 'published z=8/9/10/15/16/17 uniform slices (y=14) '
                            'vs cand14, x=14..159 R<=x+61; + low-R '
                            'single-token reduction R<=z+6 (z=15..17)',
                    'points': n + n_low, 'bad': bad + bad_low,
                    'anchor_bad': bad, 'lowR_bad': bad_low}


def check_C11r(audit):
    """Independent census consumer: output/census.txt (produced by the raw
    double-recursion census_rows.py third implementation, published in this
    experiment dir) is validated row by row against cand14 here. Every
    ledger row must reproduce from cand14: the value-2 support (T set),
    value-1 support (P set), Thue-Morse index and tail, over R=0..x+z+16.
    Fail-closed on a missing/partial/unaligned ledger.
    """
    out = Path(__file__).with_name("output")
    p = out / "census.txt"
    if not p.is_file():
        raise SystemExit("FAIL-CLOSED: census.txt is missing; run census_rows.py first")
    text = p.read_text(encoding="utf-8")
    lines = [ln for ln in text.split("\n")]
    if not text.endswith("\n"):
        raise SystemExit("FAIL-CLOSED: census.txt does not end with a newline")
    n = bad = rows = 0
    seen = set()
    for ln in lines:
        if ln == "":
            continue
        parts = dict(tok.split("=", 1) for tok in ln.split(" ") if "=" in tok)
        z = int(parts["z"]); x = int(parts["x"])
        if (z, x) in seen:
            raise SystemExit(f"FAIL-CLOSED: duplicate census row ({z},{x})")
        seen.add((z, x))
        rows += 1
        tset = {int(t) for t in parts["T"][1:-1].split(",") if t != ""}
        pset = {int(t) for t in parts["P"][1:-1].split(",") if t != ""}
        values = [cand14(z, x, R) for R in range(0, x + z + 17)]
        n += len(values)
        recompute_t = {R for R, g in enumerate(values) if g == 2}
        recompute_p = {R for R, g in enumerate(values) if g == 1}
        if recompute_t != tset or recompute_p != pset:
            bad += 1
            continue
        tail = (x + 14) % 2
        if int(parts["tail"]) != tail:
            bad += 1
            continue
        hi = len(values) - 1
        idx = None
        for R0 in range(hi, -1, -1):
            ok = all(values[R] == (tail if (R - R0) % 2 == 0 else 1 - tail)
                     for R in range(R0, hi + 1))
            if ok:
                idx = R0
            elif idx is not None:
                break
        if int(parts["idx"]) != idx:
            bad += 1
    if rows != 80 * 57:
        raise SystemExit(f"FAIL-CLOSED: census rows {rows} != 4560")
    audit['C11r'] = {'desc': 'independent raw-double-recursion census ledger '
                            '(census_rows.py third implementation, census.txt) '
                            're-derived from cand14 row by row, R=0..x+z+16, '
                            'z=0..79, x=14..70 (T/P sets, Thue-Morse index, tail)',
                    'points': n, 'bad': bad, 'rows': rows}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(14, 59):
            for R in range(1, x + z + 42):
                n += 1
                ok, _, _ = identity_ok14(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=14..58 R<=x+z+41 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(14, 65, 5):
            for R in range(1, x + z + 32):
                n += 1
                ok, _, _ = identity_ok14(z, x, R)
                if not ok or (R >= x + z + 15 and cand14(z, x, R) != (x + 14) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400} x=14..64(step5) R<=x+z+31',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(14, 19):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 14:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 14), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (13, 14), z))
                raw_opts.add(H_ordered(R - 1, (x, 13), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 14), z - 1))
                closed = set(opts14(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of14(z, x, R)
    e = (cand14(z, x, R), tuple(sorted(opts14(z, x, R))))
    if t not in types:
        types[t] = e
        return True
    return types[t] == e


def box_points(B):
    for v0 in range(-B, B + 1):
        for v1 in range(-B, B + 1):
            for v3 in range(-B, B + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 14 or R < 1:
                    continue
                yield z, x, R


def check_C4(audit, types):
    n = bad = conf_bad = id_bad = 0
    for z, x, R in box_points(60):
        n += 1
        ok, _, _ = identity_ok14(z, x, R)
        if not ok:
            id_bad += 1
        if not conform(z, x, R, types):
            conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 30/sentinel 31, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C4t(audit):
    """Tightness probe: clip 29 / sentinel 30 over the same box.

    Counts type-confluence violations when the clip window is narrowed
    by one (2y+1 instead of the 10-family candidate 2y+2=30). Not part
    of the PASS/FAIL bad total; reported for the pattern claim.
    """
    global CLIP, SENT
    old_clip, old_sent = CLIP, SENT
    CLIP, SENT = 29, 30
    n = viol = 0
    first = None
    probe_types = {}
    for z, x, R in box_points(60):
        n += 1
        if not conform(z, x, R, probe_types):
            viol += 1
            if first is None:
                first = (z, x, R)
    CLIP, SENT = old_clip, old_sent
    audit['C4t'] = {'desc': 'tightness probe clip 29/sentinel 30 (not in bad total)',
                    'points': n, 'violations_at_clip29': viol,
                    'first_violation': first}


def check_C7(audit, types, corr):
    rng = random.Random(20261142)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(14, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 15)
        elif mode == 1:
            R = x + z + 15 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(14, z + rng.randrange(-30, 19))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 14:
            continue
        n += 1
        ok, _, _ = identity_ok14(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261142, z,x<=3000',
                   'points': n, 'bad': bad}


def check_C8(audit, types, corr):
    n = bad = 0
    zs = list(range(0, 6)) + list(range(29, 32)) + list(range(59, 62)) + \
        list(range(299, 302)) + list(range(999, 1002)) + [2999, 3000]
    for z in zs:
        for dx in range(-30, 18):
            x = z + dx
            if x < 13:
                continue
            for R in range(1, x + z + 30):
                n += 1
                ok, _, _ = identity_ok14(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 15, x + z + 16, x + z + 17):
                n += 1
                if cand13(z, x, R) != (x + 13) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-30,17], tail window',
                   'points': n, 'bad': bad}


def check_C9(audit, types):
    n = bad = 0
    for band in ((61, 64), (89, 92), (117, 120)):
        lo, hi = band
        for v0 in range(-hi, hi + 1):
            for v1 in range(-hi, hi + 1):
                for v3 in range(-hi, hi + 1):
                    m = max(abs(v0), abs(v1), abs(v3))
                    if m < lo:
                        continue
                    z, x, R = vpoint(v0, v1, v3)
                    if z < 0 or x < 14 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok14(z, x, R)
                    if not ok or not conform(z, x, R, types):
                        bad += 1
    audit['C9'] = {'desc': 'v-space shell sweeps [61,64],[89,92],[117,120]',
                   'points': n, 'bad': bad}


# ------------------------------------------------------------------
# C11 census: bounded-memoization twins + separate-command parts.
# ------------------------------------------------------------------
CENSUS_CACHE_MAXSIZE = 1_600_000


def _bounded_twin(raw_engine, name):
    """LRU-capped twin of a published raw engine.

    The recursive definition is byte-identical (the published function's
    own code object re-bound into a shallow copy of the module globals,
    with the recursive name resolving to the capped wrapper instead of the
    unbounded cache). Memoization of a deterministic pure function is
    transparent, and LRU eviction is deterministic under the fixed
    census visit order, so the twin returns exactly the published engine's
    values; the cap only bounds residency on this memory-capped host.
    """
    impl = raw_engine.__wrapped__
    g = dict(impl.__globals__)
    twin = types.FunctionType(impl.__code__, g, impl.__name__)
    capped = lru_cache(CENSUS_CACHE_MAXSIZE)(twin)
    g[name] = capped
    return capped


def _census_part_file(engine_name):
    return f"census-{engine_name}.json"


def _census_expected_counts():
    points = merge = tail = 0
    for z in range(0, 80):
        for x in range(14, 71):
            points += x + z + 16
            if x <= z - 15:
                merge += x + z + 16
            tail += 1  # exactly one R (= x+z+15) is >= x+z+15 within the box
    return points, merge, tail


def run_census(engine_name):
    if engine_name not in ("ordered", "canonical"):
        raise SystemExit(f"FAIL-CLOSED: unknown census engine {engine_name}")
    raw = H_ordered if engine_name == "ordered" else H_canonical
    twin = _bounded_twin(raw, "H_ordered" if engine_name == "ordered" else "H_canonical")
    n = bad = 0
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    for z in range(0, 80):
        for x in range(14, 71):
            for R in range(0, x + z + 16):
                c = cand14(z, x, R)
                if twin(R, (x, 14), z) != c:
                    bad += 1
                corollary(z, x, R, corr)
                n += 1
    payload = {
        'engine': engine_name,
        'box': 'z=0..79, x=14..70, R=0..x+z+15',
        'cache_type': 'bounded-memoization twin of the verbatim raw engine (published code object, LRU-capped cache)',
        'cache_maxsize': CENSUS_CACHE_MAXSIZE,
        'points': n,
        'bad': bad,
        'corollaries': {
            'merge': {'points': corr['merge']['points'], 'bad': corr['merge']['bad'],
                      'claim': 'x<=z-15 => H == single_token(x+14,z,R)'},
            'tail': {'points': corr['tail']['points'], 'bad': corr['tail']['bad'],
                     'claim': 'R>=x+z+15 => H == (x+14)%2'},
        },
    }
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, sort_keys=True, indent=2) + "\n"
    (out / _census_part_file(engine_name)).write_text(text, encoding="utf-8")
    print(f"census[{engine_name}]: points={n} bad={bad} "
          f"merge={corr['merge']} tail={corr['tail']}", flush=True)
    return 0 if bad == 0 and corr['merge']['bad'] == 0 and corr['tail']['bad'] == 0 else 1


def check_C11(audit, corr):
    out = Path(__file__).with_name("output")
    parts = {}
    for engine_name in ("ordered", "canonical"):
        p = out / _census_part_file(engine_name)
        if not p.is_file():
            raise SystemExit(
                f"FAIL-CLOSED: census part file for engine '{engine_name}' is "
                f"missing ({p.name}); run mode C11{engine_name} first")
        parts[engine_name] = json.loads(p.read_text(encoding="utf-8"))
    exp_points, exp_merge, exp_tail = _census_expected_counts()
    for engine_name, part in parts.items():
        if part.get('engine') != engine_name:
            raise SystemExit("FAIL-CLOSED: census part engine field mismatch")
        if part.get('box') != 'z=0..79, x=14..70, R=0..x+z+15':
            raise SystemExit("FAIL-CLOSED: census part box mismatch")
        if part.get('cache_maxsize') != CENSUS_CACHE_MAXSIZE:
            raise SystemExit("FAIL-CLOSED: census cache cap mismatch")
        if part.get('points') != exp_points:
            raise SystemExit(f"FAIL-CLOSED: census points {part.get('points')} != {exp_points}")
        if part.get('bad') != 0:
            raise SystemExit("FAIL-CLOSED: census part reported bad != 0")
        cm, ct = part['corollaries']['merge'], part['corollaries']['tail']
        if cm['points'] != exp_merge or cm['bad'] != 0:
            raise SystemExit("FAIL-CLOSED: census merge corollary mismatch")
        if ct['points'] != exp_tail or ct['bad'] != 0:
            raise SystemExit("FAIL-CLOSED: census tail corollary mismatch")
    ordered, canonical = parts['ordered'], parts['canonical']
    n = ordered['points'] + canonical['points']
    bad = ordered['bad'] + canonical['bad']
    for k in ('merge', 'tail'):
        corr[k]['points'] += ordered['corollaries'][k]['points'] + canonical['corollaries'][k]['points']
        corr[k]['bad'] += ordered['corollaries'][k]['bad'] + canonical['corollaries'][k]['bad']
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=14..70 R<=x+z+15, both engines '
                            '(bounded-memoization twins, LRU cap 1600000, separate commands '
                            'C11ordered/C11canonical on this memory-capped host), parts validated '
                            'and merged here with recomputed expected counts',
                    'points': n, 'bad': bad,
                    'ordered_points': ordered['points'],
                    'canonical_points': canonical['points'],
                    'census_cache_maxsize': CENSUS_CACHE_MAXSIZE,
                    'census_part_files': ['census-ordered.json', 'census-canonical.json']}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(14, 121):
            for R in range(1, x + z + 18):
                n += 1
                ok, _, _ = identity_ok14(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=14..120 R<=x+z+17',
                   'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 15:
        corr['merge']['points'] += 1
        if cand14(z, x, R) != single_token(x + 14, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 15:
        corr['tail']['points'] += 1
        if cand14(z, x, R) != (x + 14) % 2:
            corr['tail']['bad'] += 1


def main():
    args = sys.argv[1:]
    if args and args[0] in ("C11ordered", "C11canonical"):
        rc = run_census(args[0][3:].lower())
        return {'overall': 'PASS' if rc == 0 else 'FAIL'}
    requested = set(args)
    everything = {'C1', 'C1b', 'C1d', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C11r', 'C12'}
    todo = requested & everything if requested else (everything - {'C11', 'C11r'})
    audit = {'experiment': 'vertical-fiber-two-token-y14-parametric-allz-proof-20261122',
             'family': 'H(R;(x,14);z), z>=0, x>=14, R>=0',
             'stage': 'part2 (C1d published-slice anchors at y=14 and the '
                      'independent census.txt consumer incorporated; census parts '
                      're-anchored via bounded-memoization twins on a 1 GiB-cgroup '
                      'host; on overall PASS with 3 byte-identical audit runs K1233 '
                      'is promoted observed->proved)',
             'checks_run': sorted(todo),
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-15 => H == single_token(x+14,z,R)'},
                 'tail': {'claim': 'R>=x+z+15 => H == (x+14)%2'}}}
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    types = {}

    for name in ('C1', 'C1b', 'C1d', 'C2', 'C2b', 'C3', 'C4', 'C4t', 'C7', 'C8', 'C9', 'C11', 'C11r', 'C12'):
        if name not in todo:
            continue
        if name == 'C1':
            check_C1(audit['checks'])
        elif name == 'C1b':
            check_C1b(audit['checks'])
        elif name == 'C1d':
            check_C1d(audit['checks'])
        elif name == 'C2':
            check_C2(audit['checks'], corr)
        elif name == 'C2b':
            check_C2b(audit['checks'])
        elif name == 'C3':
            check_C3(audit['checks'])
        elif name == 'C4':
            check_C4(audit['checks'], types)
        elif name == 'C4t':
            check_C4t(audit['checks'])
        elif name == 'C7':
            check_C7(audit['checks'], types, corr)
        elif name == 'C8':
            check_C8(audit['checks'], types, corr)
        elif name == 'C9':
            check_C9(audit['checks'], types)
        elif name == 'C11':
            check_C11(audit['checks'], corr)
        elif name == 'C11r':
            check_C11r(audit['checks'])
        elif name == 'C12':
            check_C12(audit['checks'], types, corr)
        c = audit['checks'].get(name)
        if c:
            print(f"  {name}: pts={c.get('points')} bad={c.get('bad', 0)}", flush=True)

    audit['corollaries']['merge_below_diagonal'].update(corr['merge'])
    audit['corollaries']['tail'].update(corr['tail'])
    total = sum(c['points'] for c in audit['checks'].values() if 'points' in c)
    allbad = sum(c['bad'] for c in audit['checks'].values() if 'bad' in c)
    audit['total_points'] = total
    audit['total_bad'] = allbad + corr['merge']['bad'] + corr['tail']['bad']
    audit['type_count'] = len(types)
    audit['overall'] = 'PASS' if audit['total_bad'] == 0 else 'FAIL'
    audit['verifier_sha256'] = hashlib.sha256(
        Path(__file__).read_bytes()).hexdigest()
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(audit, sort_keys=True, ensure_ascii=False, indent=2)
    (out / "audit.json").write_text(payload + "\n", encoding="utf-8")
    print('overall:', audit['overall'], 'total_points:', total,
          'types:', len(types), flush=True)
    for k in sorted(audit['checks']):
        c = audit['checks'][k]
        print(f"  {k}: pts={c.get('points')} bad={c.get('bad')}", flush=True)
    print('  merge:', corr['merge'])
    print('  tail:', corr['tail'])
    if 'C4t' in audit['checks']:
        t = audit['checks']['C4t']
        print('  C4t:', t['violations_at_clip29'], 'violations at clip 29, first:', t['first_violation'])
    return audit


if __name__ == '__main__':
    sys.exit(0 if main()['overall'] == 'PASS' else 1)
