#!/usr/bin/env python3
"""Independent universal verifier for the y=9 two-token residual family.

Family: H(R; (x,9); z), all z >= 0, all x >= 9, all R >= 0.
Claim under test (this item): the closed form cand9 (T/P row tables below)
equals H everywhere; with corollaries
  merge-below-diagonal (y=9 promotion of the y=8 line): x <= z-10
       =>  H == single_token(x+9, z, R)
  tail:                                 R >= x+z+10  =>  H == (x+9) % 2
Universal-proof machine (same trust boundary as K1023/K1099/K1104/K1112/
K1126/K1127/K1131/K1135): option decomposition + closed-form mex identity + finite-type
confluence over the free-coordinate box, anchored to raw engines, to the
published y=8 family (K1135, the B-child), to the x=9 multiset merger
((8,9)==(9,8)), to the published fixed-z y>=9 slices (K0999/K1000 z=8,
K1001 z=9, K1002/K1011 z=10) and to the published fixed-z y>=6 slice
families (K1065 z=15 / K1077 z=16 / K1087 z=17) specialised at y=9.

  C1   raw order-preserving AND descending-canonical engines vs cand9,
       z=0..14, x=9..29, R=0..x+z+46
  C1b  single-token closed form (K0832) raw anchor; published y=8 closed
       form (K1135 transcription) raw anchor; x=9 multiset merger
       (8,9)==(9,8) i.e. A==B child value raw anchor
  C1d  published fixed-z slices specialised at y=9 vs cand9,
       z in {8,9,10,15,16,17}, x=9..159, R=1..x+61; plus the published
       low-R single-token reduction R<=z+6 of the z=15/16/17 slices at
       the y=9 rows
  C2   closed-form identity grid z=0..48, x=9..56, R<=x+z+40 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {9,14,...,59}, odd R <= x+z+30
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window +/-20 sentinel +/-21 (2y+2 for y=9),
       free-coordinate box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep,
       per-type confluence of the (value, sorted-children) effect
  C7   fixed-seed far probes (seed 20261123): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+10
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301, 999..1001,
       2999, 3000}, dx in [-21, 13], tail window [x+z+10, x+z+12]
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=9..70, R<=x+z+12 (both engines; cache
       cleared engine-to-engine), plus merge/tail corollaries
  C12  deep closed grid z=0..120, x=9..120, R<=x+z+16

Published transcriptions inside this file:
  engine + single_token closed form: verbatim from the published
  verify_y5_universal.py chain (K1126 line, SHA-256
  3392a8f150619512f1695ee40a1d4c788cedcfbb69fa8e34d1fec0522610902f), as
  carried through verify_y6_universal.py (K1127), verify_y7_universal.py
  (K1131) and verify_y8_universal.py (K1135, SHA-256
  bcad4148bf8de8bd3dacab9fc1442ad01102c159127d511914d4abd46ffcbf98);
  cand8 (in_T8/band8/in_P8/cand8): verbatim from the published
  verify_y8_universal.py (the B-child of the y=9 identity and the x=9
  merger child value);
  cand9 (in_T9/in_P9): verbatim from the published cand9.py (K1138 fit
  experiment, SHA-256 6c3e9242b5650db01b463545308e4ad9c48d06c52943f9258cb3fe176e6ad093),
  with the published -99 overlap sentinel replaced by a fail-closed
  assert (T^P disjointness is a claim this machine re-checks);
  z=8 anchor: K0999 published slice formula, transcribed from the
  published verify_z8_y_ge9_proof.py (K1000 audit line);
  z=9/10 anchors: K1001/K1002 uniform candidate formulas, transcribed
  from the published verify_z9_y_ge9_proof.py / verify_z10_y_ge9_proof.py;
  z=15/16/17 anchors: K1065/K1077/K1087 report T/P formulas specialised
  at y=9 (Y=2y=18, S=x+9; no transitional cells survive at y=9 since
  2y+d >= 18+d > 17), tail evaluated first as published.
Their correctness is K0832/K1135/K0999/K1000/K1001/K1002/K1011/K1065/
K1077/K1087's claim, not re-proven here. Every transcription was
additionally pre-validated in this experiment's build against the raw
order-preserving engine (see report.md). The cand9 tables were fitted to
the raw engines (K1138) and this whole machine re-run from scratch in a
fresh environment; see report.md.
Determinism: fixed seed, no clock, sorted audit keys, stable hash seeds.
"""
import hashlib
import json
import random
import sys
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
# Raw engines (verbatim from the published census line).
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


# ------------------------------------------------------------------
# Published y=8 two-token closed form (K1135, verbatim). cand8 is the
# B-child of the y=9 identity (decrement of the 9-token) and the x=9
# multiset-merger child value ((8,9)==(9,8)).
# ------------------------------------------------------------------
def in_T8(z, x, R):
    if R <= 0:
        return False
    if x <= z - 9:
        return R % 2 == 1 and R <= q_odd(x + 8)
    d = x - z
    if z % 2 == 1:
        if d == -8:
            return R % 2 == 1 and R <= z + 8
        if d in (-4, 0, 4, 8):
            pin = z + 10 + (d + 4) // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == 9:
            return (R % 2 == 1 and R <= z) or \
                (R % 2 == 1 and z + 16 <= R <= x + z + 8)
        if d >= 10:
            return (R % 2 == 1 and R <= z) or R == z + 16
        return R % 2 == 1 and R <= z
    else:
        if d == -8:
            return R % 2 == 1 and R <= z + 7
        if d in (-6, -2, 2, 6):
            pin = z + 9 + (d + 6) // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == 9:
            return (R % 2 == 1 and R <= z - 1) or \
                (R % 2 == 1 and z + 17 <= R <= x + z + 8)
        if d >= 10:
            return (R % 2 == 1 and R <= z - 1) or R == z + 17
        return R % 2 == 1 and R <= z - 1


def band8(z, x, R):
    return z + 18 <= R <= x + z + 8 and R % 2 == z % 2


def in_P8(z, x, R):
    if R <= 0:
        return False
    if x <= z - 9:
        S = x + 8
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    b4 = R in (z + 1, z + 3, z + 5, z + 7)
    b5 = b4 or R == z + 9
    b6 = b5 or R == z + 11
    b7 = b6 or R == z + 13
    base8 = b7 or R == z + 15
    if z % 2 == 1:
        if d == -8:
            return b5 or R >= z + 10
        if d == -7:
            return b4
        if d == -6:
            return b5 or R >= z + 10
        if d == -5:
            return b5
        if d == -4:
            return b6 or R >= z + 12
        if d == -3:
            return b5
        if d == -2:
            return b6 or R >= z + 12
        if d == -1:
            return b6
        if d == 0:
            return b7 or R >= z + 14
        if d == 1:
            return b6
        if d == 2:
            return b7 or R >= z + 14
        if d == 3:
            return b7
        if d == 4:
            return base8 or R >= z + 16
        if d == 5:
            return b7
        if d == 6:
            return base8 or R >= z + 16
        if d == 7:
            return base8
        if d == 8:
            return base8 or R == z + 17 or R >= z + 18
        if d == 9:
            return base8
        tail = x % 2 == 1 and R >= x + z + 9
        return base8 or band8(z, x, R) or tail
    else:
        if d == -8:
            return False
        if d == -7:
            return b5 or R >= z + 10
        if d == -6:
            return b4
        if d == -5:
            return b5 or R >= z + 10
        if d == -4:
            return b5
        if d == -3:
            return b6 or R >= z + 12
        if d == -2:
            return b5
        if d == -1:
            return b6 or R >= z + 12
        if d == 0:
            return b6
        if d == 1:
            return b7 or R >= z + 14
        if d == 2:
            return b6
        if d == 3:
            return b7 or R >= z + 14
        if d == 4:
            return b7
        if d == 5:
            return base8 or R >= z + 16
        if d == 6:
            return b7
        if d == 7:
            return base8 or R >= z + 16
        if d == 8:
            return base8
        tail = x % 2 == 1 and R >= x + z + 9
        return base8 or band8(z, x, R) or tail


def cand8(z, x, R):
    t = in_T8(z, x, R)
    pv = in_P8(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0


# ------------------------------------------------------------------
# Candidate under test: y=9 two-token parametric closed form, all z.
# in_T9/in_P9 are the published cand9.py (K1138 fit experiment) with
# its Y=9 module constant kept verbatim (nothing folded); row-class
# tables, d = x - z, S = x + 9, BASE9 = R-z in {1,3,...,17} (9 base
# points), band = parity-z part of [z+18, x+z+9] minus the steady pin
# (odd z) / [z+20, x+z+9] (even z), tail value (x+9)%2 for
# R >= x+z+10 on even x rows (odd y); merge rows x <= z-10:
# T = O[1, q_odd(S)], P = I[q_odd(S)+1, inf) if S odd.
# The published -99 overlap sentinel is replaced by a fail-closed
# assert; T^P disjointness is itself a claim this machine re-checks.
# ------------------------------------------------------------------
Y9 = 9


def in_T9(z, x, R):
    if R <= 0: return False
    if x <= z - Y9 - 1:
        return R % 2 == 1 and R <= q_odd(x + Y9)
    d = x - z
    if z % 2 == 1:
        if d == -Y9: return R % 2 == 1 and R <= z + Y9 - 1
        if d in (-7, -3, 1, 5, 9):
            pin = z + 2*Y9 + (d - Y9) // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == Y9 + 1:
            return (R % 2 == 1 and R <= z) or (R % 2 == 1 and z + 2*Y9 <= R <= x + z + Y9)
        if d >= Y9 + 2:
            return (R % 2 == 1 and R <= z) or R == z + 2*Y9
        return R % 2 == 1 and R <= z
    else:
        if d == -Y9: return R % 2 == 1 and R <= z + Y9
        if d in (-5, -1, 3, 7, 11):
            pin = z + (d + 3*Y9) // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == Y9 + 1:
            return (R % 2 == 1 and R <= z - 1) or (R % 2 == 1 and z + 2*Y9 + 1 <= R <= x + z + Y9)
        if d >= Y9 + 2:
            return (R % 2 == 1 and R <= z - 1) or R == z + 2*Y9 + 1
        return R % 2 == 1 and R <= z - 1


def in_P9(z, x, R):
    if R <= 0: return False
    if x <= z - Y9 - 1:
        S = x + Y9
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    b4 = 1 <= R - z <= 9 and (R - z) % 2 == 1
    b5 = b4 or (R - z == 11)
    b6 = b5 or (R - z == 13)
    b7 = b6 or (R - z == 15)
    base9 = b7 or (R - z == 17)
    if z % 2 == 1:
        if d == -9: return b4 or R >= z + 10
        if d == -8: return b4
        if d == -7: return b5 or R >= z + 11
        if d == -6: return b4
        if d == -5: return b6 or R >= z + 12
        if d == -4: return b5
        if d == -3: return b6 or R >= z + 14
        if d == -2: return b5
        if d == -1: return b6 or R >= z + 14
        if d == 0:  return b6
        if d == 1:  return b7 or R >= z + 16
        if d == 2:  return b6
        if d == 3:  return b7 or R >= z + 16
        if d == 4:  return b7
        if d == 5:  return base9 or R >= z + 18
        if d == 6:  return b7
        if d == 7:  return base9 or R >= z + 18
        if d == 8:  return base9
        if d == 9:  return base9 or R == z + 19 or R >= z + 20
        if d == 10: return base9
        band = (z + 18 <= R <= x + z + Y9) and R % 2 == z % 2 and R != z + 2*Y9
        tail = x % 2 == 0 and R >= x + z + Y9 + 1
        return base9 or band or tail
    else:
        if d == -9: return False
        if d == -8: return b4 or R >= z + 9
        if d == -7: return b4
        if d == -6: return b5 or R >= z + 12
        if d == -5: return b4
        if d == -4: return b5 or R >= z + 12
        if d == -3: return b5
        if d == -2: return b6 or R >= z + 14
        if d == -1: return b5
        if d == 0:  return b6 or R >= z + 14
        if d == 1:  return b6
        if d == 2:  return b7 or R >= z + 16
        if d == 3:  return b6
        if d == 4:  return b7 or R >= z + 16
        if d == 5:  return b7
        if d == 6:  return base9 or R >= z + 18
        if d == 7:  return b7
        if d == 8:  return base9 or R >= z + 18
        if d == 9:  return base9
        if d == 10:
            band = (z + 2*Y9 + 2 <= R <= x + z + Y9) and R % 2 == z % 2
            tail = x % 2 == 0 and R >= x + z + Y9 + 1
            return base9 or band or tail
        band = (z + 2*Y9 + 2 <= R <= x + z + Y9) and R % 2 == z % 2
        tail = x % 2 == 0 and R >= x + z + Y9 + 1
        return base9 or band or tail


def cand9(z, x, R):
    t = in_T9(z, x, R)
    pv = in_P9(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0


# ------------------------------------------------------------------
# Published fixed-z slice anchors specialised at y=9 (C1d). Independent
# of the cand9 tables above. z=8: K0999 slice formula as published in
# the K1000 audit verifier; z=9/10: K1001/K1002 uniform candidates;
# z=15/16/17: K1065/K1077/K1087 report formulas at Y=2y=18, S=x+9,
# tail first (no transitional cells survive at y=9: 2y+d >= 18+d > 17).
# ------------------------------------------------------------------


def inO(r, a, b):
    return r % 2 == 1 and a <= r <= b


def inE(r, a, b):
    return r % 2 == 0 and a <= r <= b


def A8y9(x, R):
    """K0999 published closed form: H(R;(x,9);8), all x>=9, R>=0."""
    if R == 0:
        return 0
    t = R in (1, 3, 5, 7)
    if x == 11:
        t = t or R == 23
    elif x == 15:
        t = t or R == 25
    elif x == 18:
        t = t or inO(R, 27, 35)
    elif x >= 19:
        t = t or R == 27
    if x == 9:
        p = inO(R, 9, 21)
    elif x == 10:
        p = inO(R, 9, 27) or inE(R, 24, 26) or R >= 28
    elif x == 11:
        p = inO(R, 9, 21)
    elif x == 12:
        p = inO(R, 9, 29) or R == 24 or inE(R, 26, 28) or R >= 30
    elif x == 13:
        p = inO(R, 9, 23)
    elif x == 14:
        p = inO(R, 9, 31) or inE(R, 26, 30) or R >= 32
    elif x == 15:
        p = inO(R, 9, 23)
    elif x == 16:
        p = inO(R, 9, 33) or R == 26 or inE(R, 28, 32) or R >= 34
    elif x == 17:
        p = inO(R, 9, 25)
    else:
        p = inO(R, 9, 25) or inE(R, 28, x + 17) or (x % 2 == 0 and R >= x + 18)
    return 2 if t else 1 if p else 0


def A9y9(x, r):
    """K1001 published uniform candidate: H(R;(x,y);9), y=9 row."""
    y = 9
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
         (d == 10 and inO(r, 2 * y + 9, 2 * y + 19)) or
         (d >= 11 and r == 2 * y + 9))
    if t:
        return 2
    if d == 10:
        p = inE(r, 10, 2 * y + 8)
    elif d % 2 == 1:
        if d <= 3:
            p = inE(r, 10, 2 * y + 6) or r >= 2 * y + 7
        elif d <= 7:
            p = inE(r, 10, 2 * y + 8) or r >= 2 * y + 9
        elif d == 9:
            p = inE(r, 10, 2 * y + 8) or r >= 2 * y + 10
        else:
            p = inE(r, 10, 2 * y + 8) or (inO(r, 2 * y + 11, top))
    else:
        if d <= 2:
            ht = 2 * y + 4
        elif d <= 6:
            ht = 2 * y + 6
        else:
            ht = 2 * y + 8
        if d >= 12:
            p = inE(r, 10, ht) or inO(r, 2 * y + 11, top)
        else:
            p = inE(r, 10, ht)
    return 1 if p else 0


def A10y9(x, r):
    """K1002 published uniform candidate: H(R;(x,y);10), y=9 row
    (independent crosscheck lineage K1011)."""
    y = 9
    if r == 0:
        return 0
    S = x + y
    if r >= S + 11:
        return S % 2
    d = x - y
    t = (r in (1, 3, 5, 7, 9) or
         (d in (0, 4, 8) and r == 2 * y + 5 + d // 2) or
         (d == 11 and inO(r, 2 * y + 11, S + 10)) or
         (d >= 12 and r == 2 * y + 11))
    if t:
        return 2
    if d % 2 == 0 and d <= 10:
        p = inO(r, 11, 2 * y + 3 + 2 * ((d + 3) // 4))
    elif d % 2 == 0:
        p = inO(r, 11, 2 * y + 9) or inE(r, 2 * y + 12, S + 10)
    elif d <= 9:
        p = inO(r, 11, S + 10) or inE(r, 2 * y + 6 + 2 * ((d + 1) // 4), S + 9)
    else:
        p = inO(r, 11, 2 * y + 9) or inE(r, 2 * y + 12, S + 9)
    return 1 if p else 0


def A15y9(x, r):
    """K1065 (z=15, y>=6) report formula at y=9; tail R>=S+16 first."""
    d = x - 9
    Y, S = 18, x + 9
    if r == 0:
        return 0
    if r >= x + 25:
        return (x + 9) % 2
    if inO(r, 1, 15):
        return 2
    if d in (3, 7, 11, 15):
        if r == Y + (d + 15) // 2:
            return 2
    elif d == 16:
        if inO(r, Y + 15, S + 15):
            return 2
    elif d >= 17:
        if r == Y + 15:
            return 2
    if d % 2 == 0 and d <= 14:
        if inE(r, 16, Y + 6 + 2 * ((d + 3) // 4)):
            return 1
    elif d % 2 == 1 and d <= 15:
        if (inE(r, 16, S + 15)
                or inO(r, Y + 7 + 2 * ((d + 5) // 4), S + 14)
                or r >= S + 16):
            return 1
    elif d == 16:
        if inE(r, 16, Y + 14):
            return 1
    elif d % 2 == 1 and d >= 17:
        if (inE(r, 16, Y + 14)
                or inO(r, Y + 17, S + 14)
                or r >= S + 16):
            return 1
    else:  # d even, d >= 18
        if inE(r, 16, Y + 14) or inO(r, Y + 17, S + 15):
            return 1
    return 0


def A16y9(x, r):
    """K1077 (z=16, y>=6) report formula at y=9; tail R>=S+17 first."""
    d = x - 9
    Y, S = 18, x + 9
    if r == 0:
        return 0
    if r >= x + 26:
        return (x + 9) % 2
    if inO(r, 1, 15):
        return 2
    if d in (2, 6, 10, 14):
        if r == Y + (d + 16) // 2:
            return 2
    elif d == 17:
        if inO(r, Y + 17, S + 16):
            return 2
    elif d >= 18:
        if r == Y + 17:
            return 2
    if d % 2 == 0 and d <= 14:
        if inO(r, 17, Y + 7 + 2 * (d // 4)):
            return 1
    elif d % 2 == 1 and d <= 15:
        if (inO(r, 17, S + 16)
                or inE(r, Y + 10 + 2 * ((d - 1) // 4), S + 15)
                or r >= S + 17):
            return 1
    elif d == 16:
        if inO(r, 17, Y + 15):
            return 1
    elif d % 2 == 1 and d >= 17:
        if (inO(r, 17, Y + 15)
                or inE(r, Y + 18, S + 15)
                or r >= S + 17):
            return 1
    else:  # d even, d >= 18
        if inO(r, 17, Y + 15) or inE(r, Y + 18, S + 16):
            return 1
    return 0


def A17y9(x, r):
    """K1087 (z=17, y>=6) report formula at y=9; tail R>=S+18 first."""
    d = x - 9
    Y, S = 18, x + 9
    if r == 0:
        return 0
    if r >= x + 27:
        return (x + 9) % 2
    if inO(r, 1, 17):
        return 2
    if d == 18:
        if inO(r, Y + 17, S + 17):
            return 2
    elif d >= 19:
        if r == Y + 17:
            return 2
    elif d % 4 == 1:
        if r == Y + (d + 17) // 2:
            return 2
    if d >= 19:
        if (inE(r, 18, Y + 16)
                or inO(r, Y + 19, S + 17)
                or r >= S + 18):
            return 1
    elif d == 18:
        if inE(r, 18, Y + 16):
            return 1
    elif d % 2 == 0:
        if inE(r, 18, Y + 8 + 2 * (d // 4)):
            return 1
    else:
        rt = Y + (d + 17) // 2
        if d % 4 == 1:
            if inE(r, 18, rt - 1) or r >= rt + 1:
                return 1
        else:
            if inE(r, 18, rt - 2) or r >= rt:
                return 1
    return 0


# ------------------------------------------------------------------
# Closed-form identity (option decomposition, no raw recursion).
# ------------------------------------------------------------------


def opts9(z, x, R):
    """Closed-form option values of H(R; (x,9); z). R >= 1."""
    if x == 9:
        A = cand8(z, 9, R - 1)   # both token moves coincide at (8,9)=(9,8)
    else:
        A = cand9(z, x - 1, R - 1)
    B = cand8(z, x, R - 1)
    out = [A, B]
    if z >= 1:
        out.append(1 ^ cand9(z - 1, x, R - 1))
    return out


def identity_ok9(z, x, R):
    got = mex(opts9(z, x, R))
    want = cand9(z, x, R)
    return got == want, got, want


def merge_ok9(z, x, R):
    """Merge corollary: x <= z-10 => single token x+9."""
    if x > z - 10:
        return True
    return cand9(z, x, R) == single_token(x + 9, z, R)


def tail_ok9(z, x, R):
    """Tail corollary: R >= x+z+10 => (x+9) % 2."""
    if R < x + z + 10:
        return True
    return cand9(z, x, R) == (x + 9) % 2


# ------------------------------------------------------------------
# Type machine. y=8's clip window (+/-18 sentinel +/-19) folds y=8
# features; the y=9 features (pins up to z+18, sweep top R-2z = 2y = 18
# class, band bottom R-z = 2y+2 = 20, tail offset R-x-z = 10, base span
# to z+17 and the d=9 isolated P point z+19) need +/-20/21 (= 2y+2),
# which achieves full confluence over the free-coordinate box.
# ------------------------------------------------------------------
CLIP, SENT = 20, 21


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of9(z, x, R):
    return (1 if x == 9 else 0,
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
        for x in range(9, 30):
            for R in range(0, x + z + 47):
                n += 1
                c = cand9(z, x, R)
                if H_ordered(R, (x, 9), z) != c or H_canonical(R, (x, 9), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand9 z=0..14 x=9..29 R<=x+z+46',
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
    # (ii) published y=8 closed form (K1135 transcription) vs raw engine
    for z in range(0, 25):
        for x in range(8, 25):
            for R in range(0, x + z + 30):
                n += 1
                if H_ordered(R, (x, 8), z) != cand8(z, x, R):
                    bad += 1
    # (iii) x=9 multiset merger: (8,9) == (9,8) raw, and == cand8(z,9,R-1)
    for z in range(0, 31):
        for R in range(1, z + 38):
            n += 1
            a = H_ordered(R - 1, (8, 9), z)
            b = H_ordered(R - 1, (9, 8), z)
            c = H_canonical(R - 1, (8, 9), z)
            if a != b or a != c or a != cand8(z, 9, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=8-child/x=9 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C1d(audit):
    n = bad = 0
    anchors = (8, A8y9), (9, A9y9), (10, A10y9), (15, A15y9), (16, A16y9), (17, A17y9)
    for z0, fn in anchors:
        for x in range(9, 160):
            for r in range(1, x + 62):
                n += 1
                if fn(x, r) != cand9(z0, x, r):
                    bad += 1
    # published low-R single-token reduction of the fixed-z y>=6 slices
    # (K1065: R<=21, K1077: R<=22, K1087: R<=23; i.e. R<=z+6) at y=9 rows
    n_low = bad_low = 0
    for z0 in (15, 16, 17):
        for x in range(9, 160):
            for R in range(1, z0 + 7):
                n_low += 1
                if cand9(z0, x, R) != single_token(x + 9, z0, R):
                    bad_low += 1
    audit['C1d'] = {'desc': 'published z=8/9/10/15/16/17 slices (y=9) vs cand9, x=9..159 R<=x+61; + low-R single-token reduction R<=z+6 (z=15..17)',
                    'points': n + n_low, 'bad': bad + bad_low,
                    'anchor_bad': bad, 'lowR_bad': bad_low}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(9, 57):
            for R in range(1, x + z + 41):
                n += 1
                ok, _, _ = identity_ok9(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=9..56 R<=x+z+40 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(9, 63, 5):
            for R in range(1, x + z + 31, 2):
                n += 1
                ok, _, _ = identity_ok9(z, x, R)
                if not ok or (R >= x + z + 10 and cand9(z, x, R) != (x + 9) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400}',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(9, 14):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 9:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 9), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (8, 9), z))
                raw_opts.add(H_ordered(R - 1, (x, 8), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 9), z - 1))
                closed = set(opts9(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of9(z, x, R)
    e = (cand9(z, x, R), tuple(sorted(opts9(z, x, R))))
    if t not in types:
        types[t] = e
        return True
    return types[t] == e


def check_C4(audit, types):
    n = bad = conf_bad = id_bad = 0
    B = 60
    for v0 in range(-B, B + 1):
        for v1 in range(-B, B + 1):
            for v3 in range(-B, B + 1):
                z, x, R = vpoint(v0, v1, v3)
                if z < 0 or x < 9 or R < 1:
                    continue
                n += 1
                ok, _, _ = identity_ok9(z, x, R)
                if not ok:
                    id_bad += 1
                if not conform(z, x, R, types):
                    conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 20/sentinel 21, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C7(audit, types, corr):
    rng = random.Random(20261123)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(9, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 10)
        elif mode == 1:
            R = x + z + 10 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(9, z + rng.randrange(-21, 14))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 9:
            continue
        n += 1
        ok, _, _ = identity_ok9(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261123, z,x<=3000',
                   'points': n, 'bad': bad}


def check_C8(audit, types, corr):
    n = bad = 0
    zs = list(range(0, 6)) + list(range(29, 32)) + list(range(59, 62)) + \
        list(range(299, 302)) + list(range(999, 1002)) + [2999, 3000]
    for z in zs:
        for dx in range(-21, 14):
            x = z + dx
            if x < 9:
                continue
            for R in range(1, x + z + 29):
                n += 1
                ok, _, _ = identity_ok9(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 10, x + z + 11, x + z + 12):
                n += 1
                if cand9(z, x, R) != (x + 9) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-21,13], tail window',
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
                    if z < 0 or x < 9 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok9(z, x, R)
                    if not ok or not conform(z, x, R, types):
                        bad += 1
    audit['C9'] = {'desc': 'v-space shell sweeps [61,64],[89,92],[117,120]',
                   'points': n, 'bad': bad}


def check_C11(audit, corr):
    n = bad = 0
    for engine in (H_ordered, H_canonical):
        for z in range(0, 80):
            for x in range(9, 71):
                for R in range(0, x + z + 13):
                    c = cand9(z, x, R)
                    if engine(R, (x, 9), z) != c:
                        bad += 1
                    corollary(z, x, R, corr)
                    n += 1
        engine.cache_clear()
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=9..70 R<=x+z+12, both engines',
                    'points': n, 'bad': bad}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(9, 121):
            for R in range(1, x + z + 17):
                n += 1
                ok, _, _ = identity_ok9(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=9..120 R<=x+z+16',
                    'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 10:
        corr['merge']['points'] += 1
        if cand9(z, x, R) != single_token(x + 9, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 10:
        corr['tail']['points'] += 1
        if cand9(z, x, R) != (x + 9) % 2:
            corr['tail']['bad'] += 1


def main():
    audit = {'experiment': 'vertical-fiber-two-token-y9-parametric-allz-proof-20261120',
             'family': 'H(R;(x,9);z), z>=0, x>=9, R>=0',
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-10 => H == single_token(x+9,z,R)'},
                 'tail': {'claim': 'R>=x+z+10 => H == (x+9)%2'}}}
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    types = {}

    check_C1(audit['checks'])
    check_C1b(audit['checks'])
    check_C1d(audit['checks'])
    check_C2(audit['checks'], corr)
    check_C2b(audit['checks'])
    check_C3(audit['checks'])
    check_C4(audit['checks'], types)
    check_C7(audit['checks'], types, corr)
    check_C8(audit['checks'], types, corr)
    check_C9(audit['checks'], types)
    check_C11(audit['checks'], corr)
    check_C12(audit['checks'], types, corr)

    audit['corollaries']['merge_below_diagonal'].update(corr['merge'])
    audit['corollaries']['tail'].update(corr['tail'])
    total = sum(c['points'] for c in audit['checks'].values())
    allbad = sum(c['bad'] for c in audit['checks'].values())
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
          'types:', len(types))
    for k in sorted(audit['checks']):
        c = audit['checks'][k]
        print(f"  {k}: pts={c['points']} bad={c['bad']}")
    print('  merge:', corr['merge'])
    print('  tail:', corr['tail'])
    return audit


if __name__ == '__main__':
    sys.exit(0 if main()['overall'] == 'PASS' else 1)
