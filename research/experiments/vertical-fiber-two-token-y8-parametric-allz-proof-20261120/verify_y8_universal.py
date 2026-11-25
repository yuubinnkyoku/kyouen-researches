#!/usr/bin/env python3
"""Independent universal verifier for the y=8 two-token residual family.

Family: H(R; (x,8); z), all z >= 0, all x >= 8, all R >= 0.
Claim under test (this item): the closed form cand8 (T/P row tables below)
equals H everywhere; with corollaries
  merge-below-diagonal (y=8 promotion of the y=7 line): x <= z-9
       =>  H == single_token(x+8, z, R)
  tail:                                 R >= x+z+9  =>  H == (x+8) % 2
Universal-proof machine (same trust boundary as K1023/K1099/K1104/K1112/
K1126/K1127/K1131): option decomposition + closed-form mex identity + finite-type
confluence over the free-coordinate box, anchored to raw engines, to the
published y=7 family (K1131, the B-child) and to the published fixed-z
y>=6 slices (K1065/K1077/K1087) specialised at y=8.

  C1   raw order-preserving AND descending-canonical engines vs cand8,
       z=0..14, x=8..28, R=0..x+z+46
  C1b  single-token closed form (K0832) raw anchor; published y=7 closed
       form (K1131 transcription) raw anchor; x=8 multiset merger
       (7,8)==(8,7) i.e. A==B child value raw anchor
  C1d  published fixed-z y>=6 slice families (K1065 z=15 / K1077 z=16 /
       K1087 z=17), specialised at y=8 (Y=2y=16, S=x+8), vs cand8,
       x=8..159, R=1..x+61; plus the published low-R single-token
       reduction R<=z+6 of those slices at the y=8 rows
  C2   closed-form identity grid z=0..48, x=8..56, R<=x+z+40 (+merge,tail)
  C2b  deep-tail identity rows z in {60,72,84,96,108,120,240,400},
       x in {8,13,...,58}, odd R <= x+z+30
  C3   option-decomposition raw anchor (child sets vs raw recursion)
  C4   type machine, clip window +/-18 sentinel +/-19 (2y+2 for y=8),
       free-coordinate box v0=x-z, v1=R-x, v3=R-x-z in +/-60: full sweep,
       per-type confluence of the (value, sorted-children) effect
  C7   fixed-seed far probes (seed 20261123): 200k points, z,x <= 3000,
       R <= 9000, tail window around x+z+9
  C8   boundary manifolds z in {0..5, 29..31, 59..61, 299..301, 999..1001,
       2999, 3000}, dx in [-19, 11], tail window [x+z+9, x+z+11]
  C9   v-space shell sweeps at radii [61,64], [89,92], [117,120]
  C11  raw census anchor z=0..79, x=8..70, R<=x+z+12 (both engines; cache
       cleared engine-to-engine), plus merge/tail corollaries
  C12  deep closed grid z=0..120, x=8..120, R<=x+z+16

Published transcriptions inside this file:
  engine + single_token closed form: verbatim from the published
  verify_y5_universal.py chain (K1126 line, SHA-256
  3392a8f150619512f1695ee40a1d4c788cedcfbb69fa8e34d1fec0522610902f), as
  carried through verify_y6_universal.py (K1127) and verify_y7_universal.py
  (K1131, SHA-256 9200b591a30adf74dd62015ee11cb31d1bb37d9f1f0c00a626ebce9106d87abb);
  cand7 (in_T7/band7/in_P7/cand7): verbatim from the published
  verify_y7_universal.py (the B-child of the y=8 identity and the x=8
  merger child value);
  z=15/16/17 anchors: K1065/K1077/K1087 report formulas specialised at y=8
  (Y=2y=16, S=x+y=x+8), tail first, priority order as published.
Their correctness is K0832/K1131/K1065/K1077/K1087's claim, not
re-proven here. The cand8 tables below were fitted to the raw engines and
then this whole machine re-run from scratch in a fresh environment; see
report.md.
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
# Published y=7 two-token closed form (K1131, verbatim). cand7 is the
# B-child of the y=8 identity (decrement of the 8-token) and the x=8
# multiset-merger child value ((7,8)==(8,7)).
# ------------------------------------------------------------------
def in_T7(z, x, R):
    if R <= 0:
        return False
    if x <= z - 8:
        return R % 2 == 1 and R <= q_odd(x + 7)
    d = x - z
    if z % 2 == 1:
        if d == -7:
            return R % 2 == 1 and R <= z + 6
        if d in (-5, -1, 3, 7):
            pin = z + 14 + (d - 7) // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == 8:
            return (R % 2 == 1 and R <= z) or \
                (R % 2 == 1 and z + 14 <= R <= x + z + 7)
        if d >= 9:
            return (R % 2 == 1 and R <= z) or R == z + 14
        return R % 2 == 1 and R <= z
    else:
        if d == -7:
            return R % 2 == 1 and R <= z + 7
        if d in (-3, 1, 5):
            pin = z + 14 + (d - 7) // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == 8:
            return (R % 2 == 1 and R <= z - 1) or \
                (R % 2 == 1 and z + 15 <= R <= x + z + 7)
        if d >= 9:
            return (R % 2 == 1 and R <= z - 1) or R == z + 15
        return R % 2 == 1 and R <= z - 1


def band7(z, x, R):
    return z + 16 <= R <= x + z + 7 and R % 2 == z % 2


def in_P7(z, x, R):
    if R <= 0:
        return False
    if x <= z - 8:
        S = x + 7
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    b4 = R in (z + 1, z + 3, z + 5, z + 7)
    b5 = b4 or R == z + 9
    b6 = b5 or R == z + 11
    base7 = b6 or R == z + 13
    if z % 2 == 1:
        if d == -7:
            return b4 or R >= z + 8
        if d in (-6, -4):
            return b4
        if d == -5:
            return b4 or R >= z + 9
        if d == -3:
            return b4 or R >= z + 9
        if d == -2:
            return b5
        if d == -1:
            return b5 or R >= z + 11
        if d == 0:
            return b5
        if d == 1:
            return b5 or R >= z + 11
        if d == 2:
            return b6
        if d == 3:
            return b6 or R >= z + 13
        if d == 4:
            return b6
        if d == 5:
            return base7 or R >= z + 14
        if d == 6:
            return base7
        if d == 7:
            return base7 or R >= z + 15
        if d == 8:
            return base7
        tail = x % 2 == 0 and R >= x + z + 8
        return base7 or band7(z, x, R) or tail
    else:
        if d == -7:
            return False
        if d == -6:
            return b4 or R >= z + 8
        if d == -5:
            return b4
        if d == -4:
            return b5 or R >= z + 10
        if d == -3:
            return b4
        if d == -2:
            return b5 or R >= z + 10
        if d == -1:
            return b5
        if d == 0:
            return b6 or R >= z + 12
        if d == 1:
            return b5
        if d == 2:
            return b6 or R >= z + 12
        if d == 3:
            return b6
        if d == 4:
            return base7 or R >= z + 14
        if d == 5:
            return b6
        if d == 6:
            return base7 or R >= z + 14
        if d == 7:
            return base7
        tail = x % 2 == 0 and R >= x + z + 8
        return base7 or band7(z, x, R) or tail


def cand7(z, x, R):
    t = in_T7(z, x, R)
    pv = in_P7(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0


# ------------------------------------------------------------------
# Candidate under test: y=8 two-token parametric closed form, all z.
# Row-class tables, d = x - z, S = x + 8, BASE8 = {z+1, z+3, ..., z+15}
# (8 base points), band = parity-z part of [z+18, x+z+8], tail value
# (x+8) % 2 for R >= x+z+9 (even y: value-1 infinite band on odd x rows):
# merge rows x <= z-9:  T = O[1, q_odd(S)],  P = I[q_odd(S)+1, inf) if S odd
# z odd:  ladder O[1, z]; diag d=-8: T = O[1, z+8] (lattice
#         r=z+y-[2(z-y)~0 mod 4]); pins d in {-4,0,4,8} -> {z+10, z+12,
#         z+14, z+16} = 16+((x-8)+z)/2 on advance rows (x-8)+z == 2 mod 4;
#         sweep d=9: O[z+16, x+z+8]; steady d>=10: {z+16} (= 2y+z);
#         P rows: d=-8: b5|I[z+10]; d=-7: b4; d=-6: b5|I[z+10];
#         d=-5: b5; d=-4: b6|I[z+12]; d=-3: b5; d=-2: b6|I[z+12];
#         d=-1: b6; d=0: b7|I[z+14]; d=1: b6; d=2: b7|I[z+14];
#         d=3: b7; d=4: BASE8|I[z+16]; d=5: b7; d=6: BASE8|I[z+16];
#         d=7: BASE8; d=8 (pin z+16): BASE8|{z+17}|I[z+18];
#         d=9 (sweep): BASE8;
#         generic d>=10: BASE8 | band | (x odd and R >= x+z+9)
# z even: ladder O[1, z-1]; diag d=-8: T = O[1, z+7] (P empty);
#         pins d in {-6,-2,2,6} -> {z+9, z+11, z+13, z+15} = 16+((x-8)+z)/2,
#         lattice (x-8)+z == 2 mod 4; sweep d=9: O[z+17, x+z+8];
#         steady d>=10: {z+17} (= 2y+z+1);
#         P rows: d=-8: empty; d=-7: b5|I[z+10]; d=-6: b4;
#         d=-5: b5|I[z+10]; d=-4: b5; d=-3: b6|I[z+12];
#         d=-2: b5; d=-1: b6|I[z+12]; d=0: b6; d=1: b7|I[z+14];
#         d=2: b6; d=3: b7|I[z+14]; d=4: b7; d=5: BASE8|I[z+16];
#         d=6: b7; d=7: BASE8|I[z+16]; d=8: BASE8;
#         generic d>=9 (incl. sweep): BASE8 | band | (x odd, R >= x+z+9)
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
# Published fixed-z y>=6 slice families (C1d anchors), specialised at y=8.
# Transcribed from the K1065 (z=15), K1077 (z=16), K1087 (z=17) report
# formulas with Y = 2y = 16, d = x - 8, S = x + 8, tail evaluated first
# (R >= S+z+1-8 = x+z+1-... i.e. R >= x+z+9 => S mod 2), piecewise cases
# in published priority order, degenerate cells specialised at y=8
# (z=16: (8,0) T=O[1,23], P empty; z=17: S=17 row (8,1) O[1,25]).
# Independent of the cand8 tables above.
# ------------------------------------------------------------------


def inO(r, a, b):
    return r % 2 == 1 and a <= r <= b


def inE(r, a, b):
    return r % 2 == 0 and a <= r <= b


def inT15y8(x, r):
    d = x - 8
    Y, S = 16, x + 8
    if inO(r, 1, 15):
        return True
    if d in (3, 7, 11, 15):
        return r == Y + (d + 15) // 2
    if d == 16:           # sweep row
        return inO(r, Y + 15, S + 15)
    if d >= 17:           # steady pin
        return r == Y + 15
    return False


def inP15y8(x, r):
    d = x - 8
    Y, S = 16, x + 8
    if d % 2 == 0 and d <= 14:
        return inE(r, 16, Y + 6 + 2 * ((d + 3) // 4))
    if d % 2 == 1 and d <= 15:
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
    if r >= x + 24:  # tail first (R >= S+16 at z=15)
        return (x + 8) % 2
    if inT15y8(x, r):
        return 2
    if inP15y8(x, r):
        return 1
    return 0


def inT16y8(x, r):
    d = x - 8
    Y, S = 16, x + 8
    if d == 0:            # degenerate cell (8,0)
        return inO(r, 1, Y + 7)
    if inO(r, 1, 15):      # ladder O[1, z-1]
        return True
    if d in (2, 6, 10, 14):
        return r == Y + (d + 16) // 2
    if d == 17:           # sweep row
        return inO(r, Y + 17, S + 16)
    if d >= 18:            # steady pin
        return r == Y + 17
    return False


def inP16y8(x, r):
    d = x - 8
    Y, S = 16, x + 8
    if d == 0:            # degenerate cell (8,0): T covers the P band
        return False
    if d % 2 == 0 and d <= 14:
        return inO(r, 17, Y + 7 + 2 * (d // 4))
    if d % 2 == 1 and d <= 15:
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
    if r >= x + 25:  # tail first (R >= S+17 at z=16)
        return (x + 8) % 2
    if inT16y8(x, r):
        return 2
    if inP16y8(x, r):
        return 1
    return 0


def inT17y8(x, r):
    d = x - 8
    Y, S = 16, x + 8
    if S < 16:            # unreachable for x >= 8
        raise AssertionError(x)
    if S < 17:            # x=8: merge zone cell (S=16 even)
        return inO(r, 1, S - 1)
    if S == 17:           # x=9, d=1: ladder reaches O[1,25]
        return inO(r, 1, Y + (d + 17) // 2)
    if inO(r, 1, 17):      # ladder O[1, z]
        return True
    if d == 18:           # sweep row
        return inO(r, Y + 17, S + 17)
    if d >= 19:           # steady pin
        return r == Y + 17
    if d % 4 == 1:        # advance lattice d in {5,9,13} (d=17 -> steady)
        return r == Y + (d + 17) // 2
    return False


def inP17y8(x, r):
    d = x - 8
    Y, S = 16, x + 8
    if S < 17:            # merge zone cell (S=16 even): P empty
        return False
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
        return inE(r, 18, rt - 1) or r >= rt + 1
    return inE(r, 18, rt - 2) or r >= rt


def A17(x, r):
    if r == 0:
        return 0
    if r >= x + 26:  # tail first (R >= S+18 at z=17)
        return (x + 8) % 2
    if inT17y8(x, r):
        return 2
    if inP17y8(x, r):
        return 1
    return 0


# ------------------------------------------------------------------
# Closed-form identity (option decomposition, no raw recursion).
# ------------------------------------------------------------------


def opts8(z, x, R):
    """Closed-form option values of H(R; (x,8); z). R >= 1."""
    if x == 8:
        A = cand7(z, 8, R - 1)   # both token moves coincide at (7,8)=(8,7)
    else:
        A = cand8(z, x - 1, R - 1)
    B = cand7(z, x, R - 1)
    out = [A, B]
    if z >= 1:
        out.append(1 ^ cand8(z - 1, x, R - 1))
    return out


def identity_ok8(z, x, R):
    got = mex(opts8(z, x, R))
    want = cand8(z, x, R)
    return got == want, got, want


def merge_ok8(z, x, R):
    """Merge corollary: x <= z-9 => single token x+8."""
    if x > z - 9:
        return True
    return cand8(z, x, R) == single_token(x + 8, z, R)


def tail_ok8(z, x, R):
    """Tail corollary: R >= x+z+9 => (x+8) % 2."""
    if R < x + z + 9:
        return True
    return cand8(z, x, R) == (x + 8) % 2


# ------------------------------------------------------------------
# Type machine. y=7's clip window (+/-16 sentinel +/-17) folds y=7
# features; the y=8 features (pins up to z+16, sweep top R-2z = 2y = 16
# class, band bottom R-z = 2y+2 = 18, tail offset R-x-z = 9, base span
# to z+15 and the d=8 isolated P point z+17) need +/-18/19 (= 2y+2),
# which achieves full confluence over the free-coordinate box.
# ------------------------------------------------------------------
CLIP, SENT = 18, 19


def clipw(w):
    if w > CLIP:
        return SENT
    if w < -CLIP:
        return -SENT
    return w


def type_of8(z, x, R):
    return (1 if x == 8 else 0,
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
        for x in range(8, 29):
            for R in range(0, x + z + 47):
                n += 1
                c = cand8(z, x, R)
                if H_ordered(R, (x, 8), z) != c or H_canonical(R, (x, 8), z) != c:
                    bad += 1
    audit['C1'] = {'desc': 'raw both engines vs cand8 z=0..14 x=8..28 R<=x+z+46',
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
    # (ii) published y=7 closed form (K1131 transcription) vs raw engine
    for z in range(0, 25):
        for x in range(7, 25):
            for R in range(0, x + z + 30):
                n += 1
                if H_ordered(R, (x, 7), z) != cand7(z, x, R):
                    bad += 1
    # (iii) x=8 multiset merger: (7,8) == (8,7) raw, and == cand7(z,8,R-1)
    for z in range(0, 31):
        for R in range(1, z + 37):
            n += 1
            a = H_ordered(R - 1, (7, 8), z)
            b = H_ordered(R - 1, (8, 7), z)
            c = H_canonical(R - 1, (7, 8), z)
            if a != b or a != c or a != cand7(z, 8, R - 1):
                bad += 1
    audit['C1b'] = {'desc': 'single_token/y=7-child/x=8 merger raw anchors',
                    'points': n, 'bad': bad}


def check_C1d(audit):
    n = bad = 0
    for x in range(8, 160):
        for r in range(1, x + 62):
            n += 3
            if A15(x, r) != cand8(15, x, r):
                bad += 1
            if A16(x, r) != cand8(16, x, r):
                bad += 1
            if A17(x, r) != cand8(17, x, r):
                bad += 1
    # published low-R single-token reduction of the fixed-z slices
    # (K1065: R<=21, K1077: R<=22, K1087: R<=23; i.e. R<=z+6) at y=8 rows
    n_low = bad_low = 0
    for z0 in (15, 16, 17):
        for x in range(8, 160):
            for R in range(1, z0 + 7):
                n_low += 1
                if cand8(z0, x, R) != single_token(x + 8, z0, R):
                    bad_low += 1
    audit['C1d'] = {'desc': 'published z=15/16/17 y>=6 slices (y=8) vs cand8, x=8..159 R<=x+61; + low-R single-token reduction R<=z+6',
                    'points': n + n_low, 'bad': bad + bad_low,
                    'anchor_bad': bad, 'lowR_bad': bad_low}


def check_C2(audit, corr):
    n = bad = 0
    for z in range(0, 49):
        for x in range(8, 57):
            for R in range(1, x + z + 41):
                n += 1
                ok, _, _ = identity_ok8(z, x, R)
                if not ok:
                    bad += 1
                corollary(z, x, R, corr)
    audit['C2'] = {'desc': 'closed identity grid z=0..48 x=8..56 R<=x+z+40 (+merge,tail)',
                   'points': n, 'bad': bad}


def check_C2b(audit):
    n = bad = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(8, 63, 5):
            for R in range(1, x + z + 31, 2):
                n += 1
                ok, _, _ = identity_ok8(z, x, R)
                if not ok or (R >= x + z + 9 and cand8(z, x, R) != (x + 8) % 2):
                    bad += 1
    audit['C2b'] = {'desc': 'deep tail identity rows z in {60..400}',
                    'points': n, 'bad': bad}


def check_C3(audit):
    n = bad = 0
    for z in range(0, 6):
        for x in range(8, 14):
            for R in range(1, x + z + 22):
                n += 1
                # raw option set by manual child enumeration on the raw engine
                raw_opts = set()
                if x > 8:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 8), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (7, 8), z))
                raw_opts.add(H_ordered(R - 1, (x, 7), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 8), z - 1))
                closed = set(opts8(z, x, R))
                if raw_opts != closed:
                    bad += 1
    audit['C3'] = {'desc': 'option decomposition vs raw child enumeration',
                   'points': n, 'bad': bad}


def conform(z, x, R, types):
    """Return True if this point's type conforms (registry update if new)."""
    t = type_of8(z, x, R)
    e = (cand8(z, x, R), tuple(sorted(opts8(z, x, R))))
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
                if z < 0 or x < 8 or R < 1:
                    continue
                n += 1
                ok, _, _ = identity_ok8(z, x, R)
                if not ok:
                    id_bad += 1
                if not conform(z, x, R, types):
                    conf_bad += 1
    bad = id_bad + conf_bad
    audit['C4'] = {'desc': 'type machine box +/-60, clip 18/sentinel 19, confluence',
                   'points': n, 'bad': bad, 'types': len(types),
                   'identity_bad': id_bad, 'confluence_bad': conf_bad}


def check_C7(audit, types, corr):
    rng = random.Random(20261123)
    n = bad = 0
    for _ in range(200000):
        z = rng.randrange(0, 3001)
        x = rng.randrange(8, 3001)
        mode = rng.randrange(4)
        if mode == 0:
            R = rng.randrange(1, x + z + 9)
        elif mode == 1:
            R = x + z + 9 + rng.randrange(-3, 4)
        elif mode == 2:
            x = max(8, z + rng.randrange(-19, 11))
            R = rng.randrange(1, 9001)
        else:
            R = rng.randrange(1, 9001)
        if R < 1 or x < 8:
            continue
        n += 1
        ok, _, _ = identity_ok8(z, x, R)
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
        for dx in range(-19, 12):
            x = z + dx
            if x < 8:
                continue
            for R in range(1, x + z + 28):
                n += 1
                ok, _, _ = identity_ok8(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
            for R in (x + z + 9, x + z + 10, x + z + 11):
                n += 1
                if cand8(z, x, R) != (x + 8) % 2:
                    bad += 1
    audit['C8'] = {'desc': 'boundary manifolds z<=3000, dx in [-19,11], tail window',
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
                    if z < 0 or x < 8 or R < 1:
                        continue
                    n += 1
                    ok, _, _ = identity_ok8(z, x, R)
                    if not ok or not conform(z, x, R, types):
                        bad += 1
    audit['C9'] = {'desc': 'v-space shell sweeps [61,64],[89,92],[117,120]',
                   'points': n, 'bad': bad}


def check_C11(audit, corr):
    n = bad = 0
    for engine in (H_ordered, H_canonical):
        for z in range(0, 80):
            for x in range(8, 71):
                for R in range(0, x + z + 13):
                    c = cand8(z, x, R)
                    if engine(R, (x, 8), z) != c:
                        bad += 1
                    corollary(z, x, R, corr)
                    n += 1
        engine.cache_clear()
    audit['C11'] = {'desc': 'raw census anchor z=0..79 x=8..70 R<=x+z+12, both engines',
                    'points': n, 'bad': bad}


def check_C12(audit, types, corr):
    n = bad = 0
    for z in range(0, 121):
        for x in range(8, 121):
            for R in range(1, x + z + 17):
                n += 1
                ok, _, _ = identity_ok8(z, x, R)
                if not ok or not conform(z, x, R, types):
                    bad += 1
                corollary(z, x, R, corr)
    audit['C12'] = {'desc': 'deep closed grid z=0..120 x=8..120 R<=x+z+16',
                    'points': n, 'bad': bad}


def corollary(z, x, R, corr):
    if x <= z - 9:
        corr['merge']['points'] += 1
        if cand8(z, x, R) != single_token(x + 8, z, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 9:
        corr['tail']['points'] += 1
        if cand8(z, x, R) != (x + 8) % 2:
            corr['tail']['bad'] += 1


def main():
    audit = {'experiment': 'vertical-fiber-two-token-y8-parametric-allz-proof-20261120',
             'family': 'H(R;(x,8);z), z>=0, x>=8, R>=0',
             'checks': {},
             'corollaries': {
                 'merge_below_diagonal': {'claim': 'x<=z-9 => H == single_token(x+8,z,R)'},
                 'tail': {'claim': 'R>=x+z+9 => H == (x+8)%2'}}}
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
