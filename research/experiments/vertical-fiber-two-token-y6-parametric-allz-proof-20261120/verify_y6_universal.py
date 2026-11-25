#!/usr/bin/env python3
"""Independent universal verifier for the y=6 two-token residual family.

Family: H(R; (x,6); z), all z >= 0, all x >= 6, all R >= 0.
Claim under test (this item): the closed form cand6 (T/P row tables below)
equals H everywhere; with corollaries
  merge-below-diagonal (y=6 promotion of K1101/K1126): x <= z-7
       =>  H == single_token(x+6, z, R)
  tail:                                 R >= x+z+7  =>  H == (x+6) % 2
Universal-proof machine (same trust boundary as K1023/K1099/K1104/K1112/
K1126): option decomposition + closed-form mex identity + finite-type
confluence over the free-coordinate box, anchored to raw engines and to the
published fixed-z y>=6 slices.

  C1   raw order-preserving AND descending-canonical engines vs cand6,
       z=0..14, x=6..26, R=0..x+z+46
  C1b  single-token closed form (K0832) raw anchor; published y=5 closed form
       (K1126 transcription) raw anchor; x=6 multiset merger (5,6)==(6,5)
       raw anchor
  C1d  published fixed-z y>=6 slice families (K1065 z=15 / K1077 z=16 /
       K1087 z=17), specialised at y=6, vs cand6, x=6..159, R=1..x+61
  C2   closed-form identity grid z=0..48, x=6..56, R<=x+z+40 (+ merge, tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {6,11,...,56}, odd R <= x+z+30
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window +/-14 sentinel +/-15 (y=5 machine widened),
       free-coordinate box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep,
       per-type confluence of the (value, sorted-children) effect
  C7   fixed-seed far probes (seed 20261122): 200k points, z,x <= 3000,
       R <= 9000
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301, 999..1001,
       2999, 3000}, dx in [-15, 8], tail window [x+z+7, x+z+9]
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=6..70, R<=x+z+12 (both engines; cache
       cleared engine-to-engine), plus merge/tail corollaries
  C12  deep closed grid z=0..120, x=6..120, R<=x+z+16

Published transcriptions inside this file:
  engine + single_token closed form: verbatim from the published
  verify_y5_universal.py (K1126, SHA-256
  3392a8f150619512f1695ee40a1d4c788cedcfbb69fa8e34d1fec0522610902f);
  cand5 (in_T5/band5/in_P5/cand5): verbatim from the same file (the B-child
  of the y=6 identity and the x=6 merger child value);
  z=15/16/17 anchors: K1065/K1077/K1087 item formulas specialised at y=6
  (Y=2y=12, S=x+y=x+6), tail first, priority order as published.
Their correctness is K0832/K1126/K1065/K1077/K1087's claim, not re-proven
here. The cand6 tables below were fitted to the raw engines and then this
whole machine re-run from scratch in a fresh environment; see report.md.
Determinism: fixed seed, no clock, sorted audit keys, stable hash seeds.
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
# Published y=5 two-token closed form (K1126, verbatim). cand5 is the
# B-child of the y=6 identity (decrement of the 6-token) and the x=6
# multiset-merger child value.
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
# Candidate under test: y=6 two-token parametric closed form, all z.
# Row-class tables, d = x - z, S = x + 6, BASE6 = {z+1, z+3, ..., z+11}
# (6 base points), band = parity-z part of [z+14, x+z+6], tail value
# (x+6) % 2 for R >= x+z+7):
# merge rows x <= z-7:  T = O[1, q_odd(S)],  P = I[q_odd(S)+1, inf) if S odd
# z odd:  ladder O[1, z]; diag d=-6: T = O[1, z+6] (advance pin absorbed);
#         pins d in {-2, 2, 6} -> {z+8, z+10, z+12} = {z+9+d/2}, the lattice
#         2y+(x-z... equivalently pin = 2y + ((x-y)+z)/2 on advance rows
#         (x-6)+z == 2 mod 4; sweep d=7: O[z+12, x+z+6]; steady d>=8: {z+12}
#         (= 2y+z); P rows: d=-6: b3|I[z+7]; d=-5: b3; d=-4: b3|I[z+7];
#         d=-3: b4; d=-2: b4|I[z+9]; d=-1: b4; d=0: b4|I[z+9]; d=1: b5;
#         d=2: b5|I[z+11]; d=3: b5; d=4: b5|I[z+11]; d=5: BASE6;
#         d=6: BASE6|I[z+13]; d=7: BASE6; generic d>=8:
#         BASE6 | band | (x odd and R >= x+z+7)
# z even: ladder O[1, z-1]; diag d=-6: T = O[1, z+5] (pin z+6 even, cap-1);
#         pins d in {-4, 0, 4} -> {z+7, z+9, z+11}, lattice (x-6)+z == 0 mod
#         4, pin = 2y + ((x-y)+z+1)/2 = z+9+d/2; sweep d=7: O[z+13, x+z+6];
#         steady d>=8: {z+13} (= 2y+z+1); P rows: d=-6: empty; d=-5: b3|I[z+7];
#         d=-4: b3; d=-3: b3|I[z+7]; d=-2: b4; d=-1: b4|I[z+9]; d=0: b4;
#         d=1: b4|I[z+9]; d=2: b5; d=3: b5|I[z+11]; d=4: b5; d=5: b5|I[z+11];
#         d=6: BASE6; generic d>=7: BASE6 | band | (x odd and R >= x+z+7)
# ------------------------------------------------------------------

def in_T6(z, x, R):
    if R <= 0:
        return False
    if x <= z - 7:
        return R % 2 == 1 and R <= q_odd(x + 6)
    d = x - z
    if z % 2 == 1:
        if d == -6:
            return R % 2 == 1 and R <= z + 6
        if d in (-2, 2, 6):
            pin = z + 9 + d // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == 7:
            return (R % 2 == 1 and R <= z) or \
                (R % 2 == 1 and z + 12 <= R <= x + z + 6)
        if d >= 8:
            return (R % 2 == 1 and R <= z) or R == z + 12
        return R % 2 == 1 and R <= z
    else:
        if d == -6:
            return R % 2 == 1 and R <= z + 5
        if d in (-4, 0, 4):
            pin = z + 9 + d // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == 7:
            return (R % 2 == 1 and R <= z - 1) or \
                (R % 2 == 1 and z + 13 <= R <= x + z + 6)
        if d >= 8:
            return (R % 2 == 1 and R <= z - 1) or R == z + 13
        return R % 2 == 1 and R <= z - 1


def band6(z, x, R):
    """Intermediate value-1 band [z+2y+2, x+z+y] = [z+14, x+z+6], parity z."""
    return z + 14 <= R <= x + z + 6 and R % 2 == z % 2


def in_P6(z, x, R):
    if R <= 0:
        return False
    if x <= z - 7:
        S = x + 6
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    b3 = R in (z + 1, z + 3, z + 5)
    b4 = b3 or R == z + 7
    b5 = b4 or R == z + 9
    base6 = b5 or R == z + 11
    if z % 2 == 0:
        if d == -6:
            return False
        if d == -5:
            return b3 or R >= z + 7
        if d == -4:
            return b3
        if d == -3:
            return b3 or R >= z + 7
        if d == -2:
            return b4
        if d == -1:
            return b4 or R >= z + 9
        if d == 0:
            return b4
        if d == 1:
            return b4 or R >= z + 9
        if d == 2:
            return b5
        if d == 3:
            return b5 or R >= z + 11
        if d == 4:
            return b5
        if d == 5:
            return b5 or R >= z + 11
        if d == 6:
            return base6
        tail = x % 2 == 1 and R >= x + z + 7
        return base6 or band6(z, x, R) or tail
    else:
        if d == -6:
            return b3 or R >= z + 7
        if d == -5:
            return b3
        if d == -4:
            return b3 or R >= z + 7
        if d == -3:
            return b4
        if d == -2:
            return b4 or R >= z + 9
        if d == -1:
            return b4
        if d == 0:
            return b4 or R >= z + 9
        if d == 1:
            return b5
        if d == 2:
            return b5 or R >= z + 11
        if d == 3:
            return b5
        if d == 4:
            return b5 or R >= z + 11
        if d == 5:
            return base6
        if d == 6:
            return base6 or R >= z + 13
        if d == 7:
            return base6
        tail = x % 2 == 1 and R >= x + z + 7
        return base6 or band6(z, x, R) or tail


def cand6(z, x, R):
    t = in_T6(z, x, R)
    pv = in_P6(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0

# ------------------------------------------------------------------
# Published fixed-z y>=6 slice families (C1d anchors), specialised at y=6.
# Transcribed from the K1065 (z=15), K1077 (z=16), K1087 (z=17) report
# formulas with Y = 2y = 12, d' = x - 6, S = x + 6, tail evaluated first
# (R >= S+z-9 = x+z+7 => S mod 2), piecewise cases in published priority
# order. Independent of the cand6 tables above.
# ------------------------------------------------------------------


def inO(r, a, b):
    return r % 2 == 1 and a <= r <= b


def inE(r, a, b):
    return r % 2 == 0 and a <= r <= b


def inT15(x, r):
    d = x - 6
    Y, S = 12, x + 6
    if d == 0:
        return inO(r, 1, 11)
    if d in (1, 2):
        return inO(r, 1, 13)
    if d == 3:
        return inO(r, 1, 21)
    if inO(r, 1, 15):
        return True
    if d in (7, 11, 15):
        return r == Y + (d + 15) // 2
    if d == 16:
        return inO(r, Y + 15, S + 15)
    if d >= 17:
        return r == Y + 15
    return False


def inP15(x, r):
    d = x - 6
    Y, S = 12, x + 6
    if d in (0, 2):
        return False
    if d == 1:
        return r >= 14
    if d == 3:
        return r >= 16
    if d % 2 == 0 and d <= 14:
        return inE(r, 16, Y + 6 + 2 * ((d + 3) // 4))
    if d % 2 == 1 and 4 <= d <= 15:
        return (inE(r, 16, S + 15)
                or inO(r, Y + 7 + 2 * ((d + 5) // 4), S + 14)
                or r >= S + 16)
    if d == 16:
        return inE(r, 16, Y + 14)
    if d % 2 == 1 and d >= 17:
        return (inE(r, 16, Y + 14)
                or inO(r, Y + 17, S + 14)
                or r >= S + 16)
    if d % 2 == 0 and d >= 18:
        return inE(r, 16, Y + 14) or inO(r, Y + 17, S + 15)
    raise AssertionError(x)


def A15(x, r):
    if r == 0:
        return 0
    if r >= x + 22:  # tail first (R >= S+16 at z=15)
        return (x + 6) % 2
    if inT15(x, r):
        return 2
    if inP15(x, r):
        return 1
    return 0


def inT16(x, r):
    d = x - 6
    Y, S = 12, x + 6
    if x <= 9:
        return r % 2 == 1 and r <= q_odd(S)
    if d == 4:
        return inO(r, 1, 21)
    if inO(r, 1, 15):
        return True
    if d in (6, 10, 14):
        return r == Y + (d + 16) // 2
    if d == 17:
        return inO(r, Y + 17, S + 16)
    if d >= 18:
        return r == Y + 17
    return False


def inP16(x, r):
    d = x - 6
    Y, S = 12, x + 6
    if x <= 9:
        return S % 2 == 1 and r >= q_odd(S) + 1
    if d in (0, 2, 4):
        return False
    if d == 1:
        return r >= 14
    if d == 3:
        return r >= 16
    if d % 2 == 0 and d <= 14:
        return inO(r, 17, Y + 7 + 2 * (d // 4))
    if d % 2 == 1 and 5 <= d <= 15:
        return (inO(r, 17, S + 16)
                or inE(r, Y + 10 + 2 * ((d - 1) // 4), S + 15)
                or r >= S + 17)
    if d == 16:
        return inO(r, 17, Y + 15)
    if d % 2 == 1 and d >= 17:
        return (inO(r, 17, Y + 15)
                or inE(r, Y + 18, S + 15)
                or r >= S + 17)
    if d % 2 == 0 and d >= 18:
        return inO(r, 17, Y + 15) or inE(r, Y + 18, S + 16)
    raise AssertionError(x)


def A16(x, r):
    if r == 0:
        return 0
    if r >= x + 23:  # tail first (R >= S+17 at z=16)
        return (x + 6) % 2
    if inT16(x, r):
        return 2
    if inP16(x, r):
        return 1
    return 0


def inT17(x, r):
    d = x - 6
    Y, S = 12, x + 6
    if S < 17:
        return r % 2 == 1 and r <= q_odd(S)
    if S == 17:
        return inO(r, 1, Y + (d + 17) // 2 - (1 if d % 4 == 3 else 0))
    if inO(r, 1, 17):
        return True
    if d == 18:
        return inO(r, Y + 17, S + 17)
    if d >= 19:
        return r == Y + 17
    if d % 4 == 1:
        return r == Y + (d + 17) // 2
    return False


def inP17(x, r):
    d = x - 6
    Y, S = 12, x + 6
    if S < 17:
        return S % 2 == 1 and r >= q_odd(S) + 1
    if d >= 19:
        return (inE(r, 18, Y + 16)
                or inO(r, Y + 19, S + 17)
                or r >= S + 18)
    if d == 18:
        return inE(r, 18, Y + 16)
    if d % 2 == 0:
        return inE(r, 18, Y + 8 + 2 * (d // 4))
    rt = Y + (d + 17) // 2
    if d % 4 == 1:
        if inE(r, 18, rt - 1):
            return True
        return r >= rt + 1
    if inE(r, 18, rt - 2):
        return True
    return r >= rt


def A17(x, r):
    if r == 0:
        return 0
    if r >= x + 24:  # tail first (R >= S+18 at z=17)
        return (x + 6) % 2
    if inT17(x, r):
        return 2
    if inP17(x, r):
        return 1
    return 0

# ------------------------------------------------------------------
# Closed-form identity (option decomposition, no raw recursion).
# ------------------------------------------------------------------


def opts6(z, x, R):
    """Closed-form option values of H(R; (x,6); z). R >= 1."""
    if x == 6:
        A = cand5(z, 6, R - 1)   # both token moves coincide at (5,6)=(6,5)
    else:
        A = cand6(z, x - 1, R - 1)
    B = cand5(z, x, R - 1)
    out = [A, B]
    if z >= 1:
        out.append(1 ^ cand6(z - 1, x, R - 1))
    return out


def identity_ok6(z, x, R):
    got = mex(opts6(z, x, R))
    want = cand6(z, x, R)
    return got == want, got, want


def merge_ok6(z, x, R):
    """Merge corollary: x <= z-7 => single token x+6."""
    if x > z - 7:
        return True
    return cand6(z, x, R) == single_token(x + 6, z, R)


def tail_ok6(z, x, R):
    """Tail corollary: R >= x+z+7 => (x+6) % 2."""
    if R < x + z + 7:
        return True
    return cand6(z, x, R) == (x + 6) % 2


# ------------------------------------------------------------------
# Type machine. y=5's clip window (+/-12/13) folds y=6 features
# (advance pins at z+9+d/2 class, sweep band top R-2z = 13 class);
# +/-14/15 achieves full confluence over the free-coordinate box.
# ------------------------------------------------------------------
CLIP, SENT = 14, 15


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of6(z, x, R):
    return (1 if x == 6 else 0,
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
        for x in range(6, 27):
            for R in range(0, x + z + 47):
                n += 1
                c = cand6(z, x, R)
                if H_ordered(R, (x, 6), z) != c or H_canonical(R, (x, 6), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand6 z=0..14 x=6..26 R<=x+z+46',
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
    # (ii) published y=5 closed form (K1126 transcription) vs raw engine
    for z in range(0, 25):
        for x in range(5, 25):
            for R in range(0, x + z + 30):
                n += 1
                if H_ordered(R, (x, 5), z) != cand5(z, x, R):
                    bad += 1
    # (iii) x=6 multiset merger: (5,6) == (6,5) raw, and == cand5(z,6,R-1)
    for z in range(0, 31):
        for R in range(1, z + 37):
            n += 1
            a = H_ordered(R - 1, (5, 6), z)
            b = H_ordered(R - 1, (6, 5), z)
            c = H_canonical(R - 1, (5, 6), z)
            if a != b or a != c or a != cand5(z, 6, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=5-child/x=6 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C1d(audit):
    n = bad = 0
    for x in range(6, 160):
        for r in range(1, x + 62):
            n += 3
            if A15(x, r) != cand6(15, x, r):
                bad += 1
            if A16(x, r) != cand6(16, x, r):
                bad += 1
            if A17(x, r) != cand6(17, x, r):
                bad += 1
    audit['C1d'] = {'desc': 'published z=15/16/17 y>=6 slices (y=6) vs cand6, x=6..159 R<=x+61',
                    'points': n, 'bad': bad}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(6, 57):
            for R in range(1, x + z + 41):
                n += 1
                ok, _, _ = identity_ok6(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=6..56 R<=x+z+40 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(6, 61, 5):
            for R in range(1, x + z + 31, 2):
                n += 1
                ok, _, _ = identity_ok6(z, x, R)
                if not ok or (R >= x + z + 7 and cand6(z, x, R) != (x + 6) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400}',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(6, 13):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 6:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 6), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (5, 6), z))
                raw_opts.add(H_ordered(R - 1, (x, 5), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 6), z - 1))
                closed = set(opts6(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of6(z, x, R)
    e = (cand6(z, x, R), tuple(sorted(opts6(z, x, R))))
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
                if z < 0 or x < 6 or R < 1:
                    continue
                n += 1
                ok, _, _ = identity_ok6(z, x, R)
                if not ok:
                    id_bad += 1
                if not conform(z, x, R, types):
                    conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 14/sentinel 15, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C7(audit, types, corr):
    rng = random.Random(20261122)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(6, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 7)
        elif mode == 1:
            R = x + z + rng.randrange(-3, 4) if x + z >= 4 else 1
        elif mode == 2:
            x = max(6, z + rng.randrange(-15, 9))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1:
            continue
        n += 1
        ok, _, _ = identity_ok6(z, x, R)
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
        for dx in range(-15, 9):
            x = z + dx
            if x < 6:
                continue
            for R in range(1, x + z + 28):
                n += 1
                ok, _, _ = identity_ok6(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 7, x + z + 8, x + z + 9):
                n += 1
                if cand6(z, x, R) != (x + 6) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-15,8], tail window',
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
                    if z < 0 or x < 6 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok6(z, x, R)
                    if not ok or not conform(z, x, R, types):
                        bad += 1
    audit['C9'] = {'desc': 'v-space shell sweeps [61,64],[89,92],[117,120]',
                   'points': n, 'bad': bad}


def check_C11(audit, corr):
    n = bad = 0
    for engine in (H_ordered, H_canonical):
        for z in range(0, 80):
            for x in range(6, 71):
                for R in range(0, x + z + 13):
                    c = cand6(z, x, R)
                    if engine(R, (x, 6), z) != c:
                        bad += 1
                    corollary(z, x, R, corr)
                    n += 1
        engine.cache_clear()
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=6..70 R<=x+z+12, both engines',
                    'points': n, 'bad': bad}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(6, 121):
            for R in range(1, x + z + 17):
                n += 1
                ok, _, _ = identity_ok6(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=6..120 R<=x+z+16',
                    'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 7:
        corr['merge']['points'] += 1
        if cand6(z, x, R) != single_token(x + 6, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 7:
        corr['tail']['points'] += 1
        if cand6(z, x, R) != (x + 6) % 2:
            corr['tail']['bad'] += 1


def main():
    audit = {'experiment': 'vertical-fiber-two-token-y6-parametric-allz-proof-20261120',
             'family': 'H(R;(x,6);z), z>=0, x>=6, R>=0',
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-7 => H == single_token(x+6,z,R)'},
                 'tail': {'claim': 'R>=x+z+7 => H == (x+6)%2'}}}
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
