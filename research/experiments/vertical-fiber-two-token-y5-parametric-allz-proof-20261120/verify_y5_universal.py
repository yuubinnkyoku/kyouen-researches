#!/usr/bin/env python3
"""Independent universal verifier for the y=5 two-token residual family.

Family: H(R; (x,5); z), all z >= 0, all x >= 5, all R >= 0.
Claim under test (this item): the closed form cand5 (T/P row tables below)
equals H everywhere; with corollaries
  merge-below-diagonal (y=5 promotion of K1101): x <= z-6  =>  H == single_token(x+5, z, R)
  tail:                                R >= x+z+6  =>  H == (x+5) % 2
Universal-proof machine (same trust boundary as K1023/K1099/K1104/K1112):

  C1   raw order-preserving AND descending-canonical engines vs cand5,
       z=0..14, x=5..26, R=0..x+z+45
  C1b  single-token closed form (K0832) raw anchor; published y=4 closed form
       (K1112 transcription) raw anchor; x=5 multiset merger (4,5)==(5,4) raw anchor
  C1d  published fixed-z y=5 slice verifiers (z=16/17/18) vs cand5,
       x=5..120, R=1..x+60
  C2   closed-form identity grid z=0..48, x=5..56, R<=x+z+40 (+ merge, tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400}
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window +/-12 sentinel +/-13 (y=4 machine widened),
       free-coordinate box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep,
       per-type confluence of the (value, sorted-children) effect
  C7   fixed-seed far probes (seed 20261122): 200k points, z,x <= 3000, R <= 9000
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301, 999..1001,
       2999, 3000}, dx in [-13, 6], tail window [x+z+6, x+z+8]
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=5..70, R<=x+z+12 (both engines; cache
       cleared engine-to-engine), plus merge/tail corollaries
  C12  deep closed grid z=0..120, x=5..120, R<=x+z+16

Published transcriptions inside this file (mechanical renames, all validated
by C1d against cand5):
  z=16,y=5 slice: O16/E16/I16/z16y5_T/z16y5_P/z16y5_cand (set-based, published)
  z=17,y=5 slice: BASEP/z17y5_T/z17y5_P/z17y5 (O(1) predicates, published)
  z=18,y=5 slice: q18o/q18e/O18/E18/z18y5_T/z18y5_P/z18y5 (predicates, published)
The z=16 set helper I16 caps at 20000, so C1d probes R <= x+60 << 20000.
The z=16 adapters add lru_cache (performance only, set semantics unchanged).
Determinism: fixed seed, no clock, sorted audit keys, stable hd.

H(R; X; z) definition, single-token closed form, and the y=4 closed form are
verbatim transcriptions of the published verify_y4_universal.py (K1112,
SHA-256 2d5ce3734698ea2a2ac752fb6179a6f6f73c1593b53b5a20858c6d4ae2107d85);
their correctness is K0832/K1104/K1099/K1112's claim, not re-proven here.
"""
import hashlib
import json
import random
import sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)

# ------------------------------------------------------------------
# Published engine + single-token closed form (K0832 line, verbatim
# from verify_y4_universal.py).
# ------------------------------------------------------------------

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
# Published y=4 two-token closed form (K1112, verbatim). cand4 is the
# B-child of the y=5 identity (decrement of the 5-token) and the x=5
# multiset-merger child value.
# ------------------------------------------------------------------

def in_T4(z, x, R):
    if R <= 0:
        return False
    if x <= z - 5:
        return R % 2 == 1 and R <= q_odd(x + 4)
    if z % 2 == 1:
        if x == z - 4:
            return R % 2 == 1 and R <= z + 4
        if x == z - 3:
            return R % 2 == 1 and R <= z
        if x == z - 2:
            return R % 2 == 1 and R <= z
        if x == z - 1:
            return R % 2 == 1 and R <= z
        if x == z:
            return (R % 2 == 1 and R <= z) or R == z + 6
        if x == z + 1:
            return R % 2 == 1 and R <= z
        if x == z + 2:
            return R % 2 == 1 and R <= z
        if x == z + 3:
            return R % 2 == 1 and R <= z
        if x == z + 4:
            return (R % 2 == 1 and R <= z) or R == z + 8
        if x == z + 5:
            return ((R % 2 == 1 and R <= z)
                    or (R % 2 == 1 and z + 8 <= R <= 2 * z + 9))
        return (R % 2 == 1 and R <= z) or R == z + 8
    else:
        if x == z - 4:
            return R % 2 == 1 and R <= z + 3
        if x == z - 3:
            return R % 2 == 1 and R <= z - 1
        if x == z - 2:
            return (R % 2 == 1 and R <= z - 1) or R == z + 5
        if x == z - 1:
            return R % 2 == 1 and R <= z - 1
        if x == z:
            return R % 2 == 1 and R <= z - 1
        if x == z + 1:
            return R % 2 == 1 and R <= z - 1
        if x == z + 2:
            return (R % 2 == 1 and R <= z - 1) or R == z + 7
        if x == z + 3:
            return R % 2 == 1 and R <= z - 1
        if x == z + 4:
            return R % 2 == 1 and R <= z - 1
        if x == z + 5:
            return ((R % 2 == 1 and R <= z - 1)
                    or (R % 2 == 1 and z + 9 <= R <= 2 * z + 9))
        return (R % 2 == 1 and R <= z - 1) or R == z + 9


def band4(z, x, R):
    """Intermediate value-1 band O_z[2y+z+2, x+z+4] = O_z[z+10, x+z+4]."""
    return z + 10 <= R <= x + z + 4 and R % 2 == z % 2


def in_P4(z, x, R):
    if R <= 0:
        return False
    S = x + 4
    if x <= z - 5:
        return S % 2 == 1 and R >= q_odd(S) + 1
    base4 = R in (z + 1, z + 3, z + 5, z + 7)
    if z % 2 == 1:
        if x == z - 4:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z - 3:
            return R in (z + 1, z + 3)
        if x == z - 2:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z - 1:
            return R in (z + 1, z + 3, z + 5)
        if x == z:
            return R in (z + 1, z + 3, z + 5) or R >= z + 7
        if x == z + 1:
            return R in (z + 1, z + 3, z + 5)
        if x == z + 2:
            return R in (z + 1, z + 3, z + 5) or R >= z + 7
        if x == z + 3:
            return base4
        if x == z + 4:
            return base4 or R >= z + 9
        if x == z + 5:
            return base4
        tail = x % 2 == 1 and R >= x + z + 5
        return base4 or band4(z, x, R) or tail
    else:
        if x == z - 4:
            return False
        if x == z - 3:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z - 2:
            return R in (z + 1, z + 3)
        if x == z - 1:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z:
            return R in (z + 1, z + 3, z + 5)
        if x == z + 1:
            return R in (z + 1, z + 3, z + 5) or R >= z + 7
        if x == z + 2:
            return R in (z + 1, z + 3, z + 5)
        if x == z + 3:
            return R in (z + 1, z + 3, z + 5) or R >= z + 7
        if x == z + 4:
            return base4
        tail = x % 2 == 1 and R >= x + z + 5
        return base4 or band4(z, x, R) or tail


def cand4(z, x, R):
    t = in_T4(z, x, R)
    pv = in_P4(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0



# ------------------------------------------------------------------
# Candidate under test: y=5 two-token parametric closed form, all z.
# Row-class tables (d = x - z, S = x + 5, BASE5 = {z+1, z+3, z+5, z+7, z+9},
# band = O_z[z+12, x+z+5], tail value (x+5) % 2 for R >= x+z+6):
# merge rows x <= z-6:  T = O[1, q_odd(S)],  P = I[S+1, inf) if S odd else empty
# (single_token(x+5, z, R) re-specialised in the z >= S+1 branch);
# z odd:  diag d=-5: T = O[1, z+4];  pins d=-3->{z+6}, d=+1->{z+8},
#         d=+5->{z+10};  sweep d=+6: T = in-band | O[z+10, 2z+11];
#         d>=+7: in-band | {z+10};
# z even: diag d<=-5: T = O[1, z+5]; pins d=-1->{z+7}, d=+3->{z+9};
#         sweep d=+6: T = in-band | O[z+11, 2z+11];  d>=+7: {z+11};
# P rows: see in_P5 (base points BASE5, half-integer P-bands, integer
#         P-bands into the tail at even x, steady O_z band + tail).
# Grid anchors: 179,300-point two-engine grid (work step, pre-audit) and
# C1/C11 raw grids in this verifier.
# ------------------------------------------------------------------

def in_T5(z, x, R):
    if R <= 0:
        return False
    if x <= z - 6:
        return R % 2 == 1 and R <= q_odd(x + 5)
    d = x - z
    if z % 2 == 1:
        if d <= -5:            # diagonal x=z-5, S=z (may be vacuous for small z via x>=5)
            return R % 2 == 1 and R <= z + 4
        inband = R % 2 == 1 and R <= z
        if d == -3:
            return inband or R == z + 6
        if d == 1:
            return inband or R == z + 8
        if d == 5:
            return inband or R == z + 10
        if d == 6:
            return inband or (R % 2 == 1 and z + 10 <= R <= 2 * z + 11)
        if d >= 7:
            return inband or R == z + 10
        return inband
    else:
        if d <= -5:
            return R % 2 == 1 and R <= z + 5
        inband = R % 2 == 1 and R <= z - 1
        if d == -1:
            return inband or R == z + 7
        if d == 3:
            return inband or R == z + 9
        if d == 6:
            return inband or (R % 2 == 1 and z + 11 <= R <= 2 * z + 11)
        if d >= 7:
            return inband or R == z + 11
        return inband

def band5(z, x, R):
    return z + 12 <= R <= x + z + 5 and R % 2 == z % 2

def in_P5(z, x, R):
    if R <= 0:
        return False
    if x <= z - 6:
        S = x + 5
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    base5 = R in (z+1, z+3, z+5, z+7, z+9)
    b3 = R in (z+1, z+3, z+5)
    b4 = R in (z+1, z+3, z+5, z+7)
    if z % 2 == 1:
        if d == -5:
            return b3 or R >= z + 6
        if d == -4:
            return b3
        if d == -3:
            return b4 or R >= z + 8
        if d == -2:
            return b3
        if d == -1:
            return b4 or R >= z + 8
        if d == 0:
            return b4
        if d == 1:
            return base5 or R >= z + 10
        if d == 2:
            return b4
        if d == 3:
            return base5 or R >= z + 10
        if d == 4:
            return base5
        if d == 5:
            return base5 or R == z + 11 or R >= z + 12
        if d == 6:
            return base5
        tail = x % 2 == 0 and R >= x + z + 6
        return base5 or band5(z, x, R) or tail
    else:
        if d == -5:
            return False
        if d == -4:
            return b3 or R >= z + 6
        if d == -3:
            return b3
        if d == -2:
            return b4 or R >= z + 8
        if d == -1:
            return b3
        if d == 0:
            return b4 or R >= z + 8
        if d == 1:
            return b4
        if d == 2:
            return base5 or R >= z + 10
        if d == 3:
            return b4
        if d == 4:
            return base5 or R >= z + 10
        if d == 5:
            return base5
        tail = x % 2 == 0 and R >= x + z + 6
        return base5 or band5(z, x, R) or tail

def cand5(z, x, R):
    t = in_T5(z, x, R)
    pv = in_P5(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0



# ------------------------------------------------------------------
# Published fixed-z y=5 slice transcriptions (C1d anchors).
# ------------------------------------------------------------------

# --- z=16, y=5 published slice (set-based; renamed helpers) ---

def O16(a,b): return set(range(a+(a%2==0),b+1,2))
def E16(a,b): return set(range(a+(a%2==1),b+1,2))
def I16(a): return set(range(a,20000))

# ---------- parent closed form: z=16, y=5 ----------
BASE5={17,19,21,23,25}
@lru_cache(maxsize=256)
def z16y5_T(x):
    if x==5: return O16(1,9)
    if x in (6,7): return O16(1,11)
    if x in (8,9): return O16(1,13)
    if x==10: return O16(1,15)
    if x==11: return O16(1,21)          # x+y=z row, continuous cap 21=2y+(d+z)/2
    if x==15: return O16(1,15)|{23}     # advance point, d+z=26==2 mod 4
    if x==19: return O16(1,15)|{25}     # advance point, d+z=30==2 mod 4
    if x==22: return O16(1,15)|O16(27,43) # sweep row z+y+1: O[pin,x+y+z]
    if x>=23: return O16(1,15)|{27}     # steady pin 27=2y+z+1
    return O16(1,15)

@lru_cache(maxsize=256)
def z16y5_P(x):
    if x in (5,7,9,11): return set()
    if x==6: return I16(12)
    if x==8: return I16(14)
    if x==10: return I16(16)
    if x==12: return {17,19,21}|I16(22)
    if x in (13,15): return {17,19,21}
    if x==19: return {17,19,21,23}
    if x==14: return {17,19,21,23}|I16(24)
    if x==16: return {17,19,21,23}|I16(24)
    if x==17: return {17,19,21,23}
    if x==18: return BASE5|I16(26)
    if x==20: return BASE5|I16(26)
    if x==21: return BASE5
    if x%2: return BASE5|E16(28,x+21)
    return BASE5|E16(28,x+22)|I16(x+23)



def z16y5_cand(x, r):
    if r==0: return 0
    if r in z16y5_T(x): return 2
    return 1 if r in z16y5_P(x) else 0




# --- z=17, y=5 published slice (O(1) predicates) ---

BASEP = {18, 20, 22, 24, 26}
# ---------- parent closed form: O(1) predicates ----------
def z17y5_T(x, r):
    if x == 5: return r % 2 == 1 and r <= 9
    if x in (6, 7): return r % 2 == 1 and r <= 11
    if x in (8, 9): return r % 2 == 1 and r <= 13
    if x in (10, 11): return r % 2 == 1 and r <= 15
    if x == 12: return r % 2 == 1 and r <= 21
    if x == 14: return (r % 2 == 1 and r <= 17) or r == 23
    if x == 18: return (r % 2 == 1 and r <= 17) or r == 25
    if x == 22: return (r % 2 == 1 and r <= 17) or r == 27
    if x == 23: return (r % 2 == 1 and r <= 17) or (r % 2 == 1 and 27 <= r <= 45)
    if x >= 24: return (r % 2 == 1 and r <= 17) or r == 27
    return r % 2 == 1 and r <= 17

def z17y5_P(x, r):
    if x in (5, 7, 9, 11): return False
    if x == 6: return r >= 12
    if x == 8: return r >= 14
    if x == 10: return r >= 16
    if x == 12: return r in (18, 20, 22) or r >= 23
    if x in (13, 15): return r in (18, 20, 22)
    if x in (14, 16): return r in (18, 20, 22) or r >= 24
    if x in (17, 19): return r in (18, 20, 22, 24)
    if x in (18, 20): return r in (18, 20, 22, 24) or r >= 26
    if x == 21: return r in BASEP
    if x == 22: return r in BASEP or r >= 28
    if x == 23: return r in BASEP
    if x % 2: return r in BASEP or (r % 2 == 1 and 29 <= r <= x + 22)
    return r in BASEP or (r % 2 == 1 and 29 <= r <= x + 23) or r >= x + 24

def z17y5(x, r):
    if r == 0: return 0
    if r >= x + 23: return (x + 5) % 2
    if z17y5_T(x, r): return 2
    if z17y5_P(x, r): return 1
    return 0




# --- z=18, y=5 published slice (predicates; renamed helpers) ---

def q18o(n): return n if n%2 else n-1
def q18e(n): return n if n%2==0 else n-1
def O18(r, a, b): return r%2==1 and a<=r<=b
def E18(r, a, b): return r%2==0 and a<=r<=b

# Target T/P predicates.
def z18y5_T(x, r):
    if 5<=x<=12: return O18(r,1,q18o(x+5))
    if x==13: return O18(r,1,23)
    if 14<=x<=16 or x in (18,19,20,22,23): return O18(r,1,17)
    if x==17: return O18(r,1,17) or r==25
    if x==21: return O18(r,1,17) or r==27
    if x==24: return O18(r,1,17) or O18(r,29,47)
    return O18(r,1,17) or r==29

def z18y5_P(x, r):
    if x in (5,7,9,11,13): return False
    if x in (6,8,10,12): return r>=x+6
    if x==14: return r in (19,21) or r>=23
    if x==15: return r in (19,21,23)
    if x==16: return r in (19,21,23) or r>=25
    if x==17: return r in (19,21,23)
    if x==18: return r in (19,21,23) or r>=25
    if x==19: return r in (19,21,23,25)
    if x==20: return r in (19,21,23,25) or r>=27
    if x==21: return r in (19,21,23,25)
    if x==22: return r in (19,21,23,25) or r>=27
    if x==23: return r in (19,21,23,25,27)
    if x==24: return r in (19,21,23,25,27) or E18(r,30,46) or r>=48
    b=r in (19,21,23,25,27)
    if x%2: return b or E18(r,30,q18e(x+23))
    return b or E18(r,30,q18e(x+23)) or r>=x+24

def z18y5(x, r):
    if r==0: return 0
    t,p=z18y5_T(x, r), z18y5_P(x, r)
    assert not(t and p),(x,r)
    return 2 if t else 1 if p else 0



# ------------------------------------------------------------------
# Closed-form identity (option decomposition, no raw recursion).
# ------------------------------------------------------------------



def opts5(z, x, R):
    """Closed-form option values of H(R; (x,5); z). R >= 1."""
    if x == 5:
        A = cand4(z, 5, R - 1)   # both token moves coincide at (4,5)=(5,4)
    else:
        A = cand5(z, x - 1, R - 1)
    B = cand4(z, x, R - 1)
    out = [A, B]
    if z >= 1:
        out.append(1 ^ cand5(z - 1, x, R - 1))
    return out


def identity_ok5(z, x, R):
    got = mex(opts5(z, x, R))
    want = cand5(z, x, R)
    return got == want, got, want


def merge_ok5(z, x, R):
    """Merge corollary: x <= z-6 => single token x+5."""
    if x > z - 6:
        return True
    return cand5(z, x, R) == single_token(x + 5, z, R)


def tail_ok5(z, x, R):
    """Tail corollary: R >= x+z+6 => (x+5) % 2."""
    if R < x + z + 6:
        return True
    return cand5(z, x, R) == (x + 5) % 2


# ------------------------------------------------------------------
# Type machine. y=4's clip window (+/-9/10) folds y=5 features
# (steady pins at R-z = z+11 class, sweep band top R-2z = 11 class);
# +/-12/13 achieves full confluence over the free-coordinate box.
# ------------------------------------------------------------------
CLIP, SENT = 12, 13


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of5(z, x, R):
    return (1 if x == 5 else 0,
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
        for x in range(5, 27):
            for R in range(0, x + z + 46):
                n += 1
                c = cand5(z, x, R)
                if H_ordered(R, (x, 5), z) != c or H_canonical(R, (x, 5), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand5 z=0..14 x=5..26 R<=x+z+45',
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
    # (ii) published y=4 closed form (K1112 transcription) vs raw ordered engine
    for z in range(0, 25):
        for x in range(4, 25):
            for R in range(0, x + z + 30):
                n += 1
                if H_ordered(R, (x, 4), z) != cand4(z, x, R):
                    bad += 1
    # (iii) x=5 multiset merger: (4,5) == (5,4) raw, and == cand4(z,5,R-1)
    for z in range(0, 31):
        for R in range(1, z + 37):
            n += 1
            a = H_ordered(R - 1, (4, 5), z)
            b = H_ordered(R - 1, (5, 4), z)
            c = H_canonical(R - 1, (4, 5), z)
            if a != b or a != c or a != cand4(z, 5, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=4-child/x=5 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C1d(audit):
    n = bad = 0
    for x in range(5, 121):
        for r in range(1, x + 61):
            n += 3
            if z16y5_cand(x, r) != cand5(16, x, r):
                bad += 1
            if z17y5(x, r) != cand5(17, x, r):
                bad += 1
            if z18y5(x, r) != cand5(18, x, r):
                bad += 1
    audit['C1d'] = {'desc': 'published z=16/17/18 y=5 slices vs cand5, x=5..120 R<=x+60',
                    'points': n, 'bad': bad}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(5, 57):
            for R in range(1, x + z + 41):
                n += 1
                ok, _, _ = identity_ok5(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=5..56 R<=x+z+40 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(5, 61, 5):
            for R in range(1, x + z + 31, 2):
                n += 1
                ok, _, _ = identity_ok5(z, x, R)
                if not ok or (R >= x + z + 6 and cand5(z, x, R) != (x + 5) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400}',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 7):
        for x in range(5, 12):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 5:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 5), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (4, 5), z))
                raw_opts.add(H_ordered(R - 1, (x, 4), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 5), z - 1))
                closed = set(opts5(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of5(z, x, R)
    e = (cand5(z, x, R), tuple(sorted(opts5(z, x, R))))
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
                if z < 0 or x < 5 or R < 1:
                    continue
                n += 1
                ok, _, _ = identity_ok5(z, x, R)
                if not ok:
                    id_bad += 1
                if not conform(z, x, R, types):
                    conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 12/sentinel 13, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C7(audit, types, corr):
    rng = random.Random(20261122)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(5, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 7)
        elif mode == 1:
            R = x + z + rng.randrange(-3, 4) if x + z >= 4 else 1
        elif mode == 2:
            x = max(5, z + rng.randrange(-13, 7))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1:
            continue
        n += 1
        ok, _, _ = identity_ok5(z, x, R)
        if not ok or not conform(z, x, R, types):
            bad += 1
        corollary(z, x, R, corr)
    audit['C7'] = {'desc': 'seeded far probes 200k, seed 20261122, z,x<=3000',
                   'points': n, 'bad': bad}


def check_C8(audit, types, corr):
    n = bad = 0
    zs = list(range(0, 6)) + list(range(29, 32)) + list(range(59, 62)) + \
        list(range(299, 302)) + list(range(999, 1002)) + [2999, 3000]
    for z in zs:
        for dx in range(-13, 7):
            x = z + dx
            if x < 5:
                continue
            for R in range(1, x + z + 28):
                n += 1
                ok, _, _ = identity_ok5(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 6, x + z + 7, x + z + 8):
                n += 1
                if cand5(z, x, R) != (x + 5) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-13,6], tail window',
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
                    if z < 0 or x < 5 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok5(z, x, R)
                    if not ok or not conform(z, x, R, types):
                        bad += 1
    audit['C9'] = {'desc': 'v-space shell sweeps [61,64],[89,92],[117,120]',
                   'points': n, 'bad': bad}


def check_C11(audit, corr):
    n = bad = 0
    for engine in (H_ordered, H_canonical):
        for z in range(0, 80):
            for x in range(5, 71):
                for R in range(0, x + z + 13):
                    c = cand5(z, x, R)
                    if engine(R, (x, 5), z) != c:
                        bad += 1
                    corollary(z, x, R, corr)
                    n += 1
        engine.cache_clear()
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=5..70 R<=x+z+12, both engines',
                    'points': n, 'bad': bad}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(5, 121):
            for R in range(1, x + z + 17):
                n += 1
                ok, _, _ = identity_ok5(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=5..120 R<=x+z+16',
                    'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 6:
        corr['merge']['points'] += 1
        if cand5(z, x, R) != single_token(x + 5, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 6:
        corr['tail']['points'] += 1
        if cand5(z, x, R) != (x + 5) % 2:
            corr['tail']['bad'] += 1


def main():
    audit = {'experiment': 'vertical-fiber-two-token-y5-parametric-allz-proof-20261120',
             'family': 'H(R;(x,5);z), z>=0, x>=5, R>=0',
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-6 => H == single_token(x+5,z,R)'},
                 'tail': {'claim': 'R>=x+z+6 => H == (x+5)%2'}}}
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
    main()
