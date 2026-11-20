#!/usr/bin/env python3
"""Machine pre-flight for the y=10 two-token residual family H(R; (x,10); z).

Purpose (reliability gates only, NOT a universal proof):
  Before building the full universal-proof verifier verify_y10_universal.py
  (12 checks, both raw engines, fixed-z anchors, type machine with clip
  window +/-22 sentinel +/-23, census, 3x byte-identical runs, K1141
  observed->proved promotion), this pre-flight tests that the two
  closed-form ingredients of the future machine are mutually consistent and
  anchored to the raw recursion on a meaningful region:
    (1) cand10 (the K1141 published fit, kept at status "observed") satisfies
        the option-decomposition mex identity cand10 == mex(opts) with
        B-child = cand9 (the K1138 published, PROVED y=9 family),
        on a main grid + deep windows + the x=10 edge;
    (2) the option decomposition itself is raw-anchored (closed child sets
        equal raw-engine child sets);
    (3) the x=10 seam rows' child value cand9(z,10,R-1) equals the raw
        two-token engine on the (9,10)/(10,9) multiset;
    (4) the cand9 transcription used here (verbatim from the published K1138
        fit cand9.py, with module-level renames Y->Y9, q_odd->q_odd9) is
        semantically identical to the cand9 tables as published inside the
        K1138 universal verifier verify_y9_universal.py (the two published
        copies differ textually on two P-row prefixes that the row-tail
        condition absorbs, and on the overlap sentinel; check C1c here
        machine-verifies semantic identity against the raw region);
    (5) the merge and tail corollaries of cand10 hold on the visited region.

Status of this experiment: pre-flight / observed-support only. It proves
nothing universally; surviving all gates is a necessary, not sufficient
condition for starting the verify_y10_universal.py build.

Published transcriptions inside this file (all constants and tables kept
verbatim, only the module-level renames listed below applied):
  cand10 block: verbatim from the K1141 published cand10.py (SHA-256
  7c08e065d1278e9e90e4f748a2f7a8a6406318618ac06d259659233387427163),
  tables q_odd / single_token_val / in_T10 / _bk / in_P10 / cand10;
  the fit self-check driver (probe_rows.txt reader) is intentionally not
  carried over;
  cand9 block: verbatim from the K1138 published cand9.py (fit experiment,
  SHA-256 6c3e9242b5650db01b463545308e4ad9c48d06c52943f9258cb3fe176e6ad093)
  with module-level renames Y -> Y9, q_odd -> q_odd9 (name collision with
  the cand10 block; bodies unchanged); the published -99 overlap sentinel
  is kept and is fail-visible here (any -99 child is counted as bad);
  cand9V tables: the cand9 tables exactly as published inside the K1138
  published verifier verify_y9_universal.py (SHA-256
  299acb6a70b9625310a3397a10f809879ba4a10a97e965115615d83f46c9171b), with
  renames Y9 -> Y9V, in_T9 -> in_T9V, in_P9 -> in_P9V (bodies unchanged,
  the fail-closed assert variant of the sentinel is not needed here because
  C1c compares Boolean tables);
  raw engines H_ordered / H_canonical: verbatim from the same K1138
  verifier (the published census-line engine transcription).
Their correctness is K0832/K1138/K1141's claim, not re-proven here.

Identity construction (option decomposition of the (x,10) multiset):
  x >= 11: opts = { cand10(z, x-1, R-1), cand9(z, x, R-1) }
           (+ { 1 ^ cand10(z-1, x, R-1) } if z >= 1)
           A-child: decrement of the x-token -> (x-1, 10) = y=10 family;
           B-child: decrement of the 10-token -> (x, 9) = y=9 family (K1138);
  x == 10: A-child (9,10) and B-child (10,9) coincide as multisets, both are
           the y=9 family at x=10: opts = { cand9(z, 10, R-1) }
           (+ C-child if z >= 1).
Corollaries tested:
  merge below diagonal (y=10 promotion of the y=9 line): x <= z-11
       => cand10 == single_token_val(x+10, R)  (z-independent, z >= S+1)
  tail: R >= x+z+11 => cand10 == (x+10) % 2

Checks (all deterministic, no clock, fixed iteration order):
  C2a  main identity grid: z=0..40, x=10..56, R=1..x+z+36 (+merge,tail,overlap)
  C2b  deep-z identity windows: z in {60,72,84,96,108,120,240,400},
       x=10..80, R in [x+z+1, x+z+40] (+tail)
  C2c  deep-x identity windows: x in {70,80,100,150,240,400}, z=0..40,
       R in [x+z+1, x+z+40] (+tail)
  C2d  x=10 edge rows: z=0..60, R in [x+z+1, x+z+70] (+merge,tail)
  C3   raw option anchor: closed child SET equals raw-engine child set,
       z=0..12, x=10..22, R=1..30
  C1b  seam child raw anchor: H(R,(9,10),z) == H(R,(10,9),z) ==
       H_canonical(...) == cand9(z,10,R), z=0..30, R=1..55
  C1c  cand9 transcription equivalence (fit cand9.py copy vs verifier copy):
       in_T9 == in_T9V and in_P9 == in_P9V (and both overlap flags equal),
       z=0..40, x=9..80, R=1..x+z+40

Expected output for THIS exact file is recorded in output/preflight_output.txt;
"overall: PASS" requires every bad counter and overlap counter to be zero.
"""
import sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


# =====================================================================
# cand10: verbatim transcription from the published K1141 fit cand10.py
# (tables only; module constant q_odd/single_token_val/in_T10/_bk/
#  in_P10/cand10 unchanged, fit driver omitted).
# =====================================================================
Y = 10

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

def in_T10(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        return R % 2 == 1 and R <= q_odd(x + Y)
    d = x - z
    if d == -Y:
        return R % 2 == 1 and R <= (z + Y if z % 2 == 1 else z + Y - 1)
    if z % 2 == 1:
        if d in (-7, -3, 1, 5, 9):
            # not a y=10 pin class; plain ladder (keep template explicit)
            return R % 2 == 1 and R <= z
        if d in (-6, -2, 2, 6, 10):
            pin = z + (d + 3 * Y) // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == Y + 1:
            return (R % 2 == 1 and R <= z) or ((R - z) % 2 == 0 and z + 2 * Y <= R <= x + z + Y)
        if d >= Y + 2:
            return (R % 2 == 1 and R <= z) or R == z + 2 * Y
        return R % 2 == 1 and R <= z
    else:
        if d in (-9, -7, -5, -3, -1, 1, 3, 5, 7, 9):
            return R % 2 == 1 and R <= z - 1
        if d in (-8, -4, 0, 4, 8):
            pin = z + (d + 3 * Y) // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == -Y:  # handled above
            return R % 2 == 1 and R <= z + Y - 1
        if d == 10:
            return R % 2 == 1 and R <= z - 1
        if d == Y + 1:
            return (R % 2 == 1 and R <= z - 1) or (R % 2 == 1 and z + 2 * Y + 1 <= R <= x + z + Y)
        if d >= Y + 2:
            return (R % 2 == 1 and R <= z - 1) or R == z + 2 * Y + 1
        return R % 2 == 1 and R <= z - 1

def _bk(off, k):
    return 1 <= off <= 2 * k - 1 and off % 2 == 1

def in_P10(z, x, R):
    if R <= 0:
        return False
    if x <= z - Y - 1:
        S = x + Y
        return S % 2 == 1 and R >= q_odd(S) + 1
    d = x - z
    off = R - z
    base10 = _bk(off, 10)
    band = (2 * Y + 2 <= off <= x + Y) and off % 2 == 0
    tail = x % 2 == 1 and R >= x + z + Y + 1
    if z % 2 == 1:
        # interval rows: d even; base th(d) zigzag
        if d == -10: return _bk(off, 6) or R >= z + 12
        if d == -9: return _bk(off, 5)
        if d == -8: return _bk(off, 6) or R >= z + 12
        if d == -7: return _bk(off, 6)
        if d == -6: return _bk(off, 7) or R >= z + 14
        if d == -5: return _bk(off, 6)
        if d == -4: return _bk(off, 7) or R >= z + 14
        if d == -3: return _bk(off, 7)
        if d == -2: return _bk(off, 8) or R >= z + 16
        if d == -1: return _bk(off, 7)
        if d == 0: return _bk(off, 8) or R >= z + 16
        if d == 1: return _bk(off, 8)
        if d == 2: return _bk(off, 9) or R >= z + 18
        if d == 3: return _bk(off, 8)
        if d == 4: return _bk(off, 9) or R >= z + 18
        if d == 5: return _bk(off, 9)
        if d == 6: return _bk(off, 10) or R >= z + 20
        if d == 7: return _bk(off, 9)
        if d == 8: return _bk(off, 10) or R >= z + 20
        if d == 9: return _bk(off, 10)
        if d == 10: return _bk(off, 10) or R >= z + 21  # pin offset 20 is value 2
        if d == 11: return base10  # sweep row: no value-1 beyond base
        return base10 or band or tail
    else:
        if d == -10: return False  # even-z diagonal: no value-1 at all
        if d == -9: return _bk(off, 6) or R >= z + 12
        if d == -8: return _bk(off, 5)
        if d == -7: return _bk(off, 6) or R >= z + 12
        if d == -6: return _bk(off, 6)
        if d == -5: return _bk(off, 7) or R >= z + 14
        if d == -4: return _bk(off, 6)
        if d == -3: return _bk(off, 7) or R >= z + 14
        if d == -2: return _bk(off, 7)
        if d == -1: return _bk(off, 8) or R >= z + 16
        if d == 0: return _bk(off, 7)
        if d == 1: return _bk(off, 8) or R >= z + 16
        if d == 2: return _bk(off, 8)
        if d == 3: return _bk(off, 9) or R >= z + 18
        if d == 4: return _bk(off, 8)
        if d == 5: return _bk(off, 9) or R >= z + 18
        if d == 6: return _bk(off, 9)
        if d == 7: return _bk(off, 10) or R >= z + 20
        if d == 8: return _bk(off, 9)
        if d == 9: return _bk(off, 10) or R >= z + 20
        if d == 10: return _bk(off, 10)
        return base10 or band or tail  # d >= 11 (sweep included)

def cand10(z, x, R):
    if R <= 0:
        return 0
    if in_T10(z, x, R):
        return 2
    if in_P10(z, x, R):
        return 1
    return 0


# =====================================================================
# cand9: verbatim transcription from the published K1138 fit cand9.py
# (module-level renames only: Y -> Y9, q_odd -> q_odd9; bodies unchanged;
#  the published -99 overlap sentinel kept and fail-visible here).
# =====================================================================
Y9 = 9

def q_odd9(k):
    return k if k % 2 else k - 1

# ---------- T (value 2), verified mismatch=0 on 73811 probe points ----------
def in_T9(z, x, R):
    if R <= 0: return False
    if x <= z - Y9 - 1:
        return R % 2 == 1 and R <= q_odd9(x + Y9)
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

# ---------- P (value 1), fitted from probe ----------
def in_P9(z, x, R):
    if R <= 0: return False
    if x <= z - Y9 - 1:
        S = x + Y9
        return S % 2 == 1 and R >= q_odd9(S) + 1
    d = x - z
    b4 = 1 <= R - z <= 9 and (R - z) % 2 == 1
    b5 = b4 or (R - z == 11)
    b6 = b5 or (R - z == 13)
    b7 = b6 or (R - z == 15)
    base9 = b7 or (R - z == 17)
    if z % 2 == 1:
        if d == -9: return b4 or R >= z + 10
        if d == -8: return b4
        if d == -7: return b4 or R >= z + 11
        if d == -6: return b4
        if d == -5: return b5 or R >= z + 12
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
    p = in_P9(z, x, R)
    if t and p:
        return -99
    if t: return 2
    return 1 if p else 0


# =====================================================================
# cand9V tables: the cand9 tables exactly as published inside the K1138
# published verifier verify_y9_universal.py (renames only:
# Y9 -> Y9V, in_T9 -> in_T9V, in_P9 -> in_P9V; bodies unchanged).
# Twofold purpose: independent second copy for the semantic-equivalence
# check C1c, and the citation-faithful form the future y=10 verifier's
# cand9 transcription must be diffed against.
# =====================================================================
Y9V = 9


def in_T9V(z, x, R):
    if R <= 0: return False
    if x <= z - Y9V - 1:
        return R % 2 == 1 and R <= q_odd(x + Y9V)
    d = x - z
    if z % 2 == 1:
        if d == -Y9V: return R % 2 == 1 and R <= z + Y9V - 1
        if d in (-7, -3, 1, 5, 9):
            pin = z + 2*Y9V + (d - Y9V) // 2
            return (R % 2 == 1 and R <= z) or R == pin
        if d == Y9V + 1:
            return (R % 2 == 1 and R <= z) or (R % 2 == 1 and z + 2*Y9V <= R <= x + z + Y9V)
        if d >= Y9V + 2:
            return (R % 2 == 1 and R <= z) or R == z + 2*Y9V
        return R % 2 == 1 and R <= z
    else:
        if d == -Y9V: return R % 2 == 1 and R <= z + Y9V
        if d in (-5, -1, 3, 7, 11):
            pin = z + (d + 3*Y9V) // 2
            return (R % 2 == 1 and R <= z - 1) or R == pin
        if d == Y9V + 1:
            return (R % 2 == 1 and R <= z - 1) or (R % 2 == 1 and z + 2*Y9V + 1 <= R <= x + z + Y9V)
        if d >= Y9V + 2:
            return (R % 2 == 1 and R <= z - 1) or R == z + 2*Y9V + 1
        return R % 2 == 1 and R <= z - 1


def in_P9V(z, x, R):
    if R <= 0: return False
    if x <= z - Y9V - 1:
        S = x + Y9V
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
        band = (z + 18 <= R <= x + z + Y9V) and R % 2 == z % 2 and R != z + 2*Y9V
        tail = x % 2 == 0 and R >= x + z + Y9V + 1
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
            band = (z + 2*Y9V + 2 <= R <= x + z + Y9V) and R % 2 == z % 2
            tail = x % 2 == 0 and R >= x + z + Y9V + 1
            return base9 or band or tail
        band = (z + 2*Y9V + 2 <= R <= x + z + Y9V) and R % 2 == z % 2
        tail = x % 2 == 0 and R >= x + z + Y9V + 1
        return base9 or band or tail


# =====================================================================
# Raw engines: verbatim from the published K1138 verifier
# verify_y9_universal.py (published census-line engine transcription).
# =====================================================================
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


# =====================================================================
# Closed-form option decomposition of H(R; (x, 10); z), R >= 1.
# =====================================================================

def opts_closed(z, x, R):
    """Closed-form child values of the (x,10) multiset at (R, z). R >= 1.

    Returns (opts_list, sentinel) where sentinel is nonzero if any child
    evaluation hit a transcription sentinel (cand9's -99 overlap marker):
    the identity check treats that as bad immediately.
    """
    sentinel = 0
    if x == 10:
        A = cand9(z, 10, R - 1)          # (9,10) and (10,9) coincide
        if A == -99:
            sentinel += 1
        out = [A]
    else:
        A = cand10(z, x - 1, R - 1)
        B = cand9(z, x, R - 1)
        if B == -99:
            sentinel += 1
        out = [A, B]
    if z >= 1:
        out.append(1 ^ cand10(z - 1, x, R - 1))
    return out, sentinel


def _corollary_counters(z, x, R, corr):
    if x <= z - 11:
        corr['merge']['points'] += 1
        if cand10(z, x, R) != single_token_val(x + 10, R):
            corr['merge']['bad'] += 1
    if R >= x + z + 11:
        corr['tail']['points'] += 1
        if cand10(z, x, R) != (x + 10) % 2:
            corr['tail']['bad'] += 1


# =====================================================================
# Checks.
# =====================================================================

def check_C2a(res, corr):
    n = bad = ov = sent = 0
    for z in range(0, 41):
        for x in range(10, 57):
            for R in range(1, x + z + 37):
                n += 1
                if in_T10(z, x, R) and in_P10(z, x, R):
                    ov += 1
                opts, s = opts_closed(z, x, R)
                sent += s
                if s == 0 and mex(opts) != cand10(z, x, R):
                    bad += 1
                _corollary_counters(z, x, R, corr)
    res['C2a'] = {'desc': 'identity grid z=0..40 x=10..56 R<=x+z+36 (+merge,tail)',
                  'points': n, 'bad': bad, 'overlap': ov, 'sentinel': sent}


def check_C2b(res, corr):
    n = bad = ov = sent = 0
    for z in (60, 72, 84, 96, 108, 120, 240, 400):
        for x in range(10, 81):
            for R in range(x + z + 1, x + z + 41):
                n += 1
                if in_T10(z, x, R) and in_P10(z, x, R):
                    ov += 1
                opts, s = opts_closed(z, x, R)
                sent += s
                if s == 0 and mex(opts) != cand10(z, x, R):
                    bad += 1
                _corollary_counters(z, x, R, corr)
    res['C2b'] = {'desc': 'deep-z windows z in {60,..,400} x=10..80 R=[x+z+1,x+z+40]',
                  'points': n, 'bad': bad, 'overlap': ov, 'sentinel': sent}


def check_C2c(res, corr):
    n = bad = ov = sent = 0
    for x in (70, 80, 100, 150, 240, 400):
        for z in range(0, 41):
            for R in range(x + z + 1, x + z + 41):
                n += 1
                if in_T10(z, x, R) and in_P10(z, x, R):
                    ov += 1
                opts, s = opts_closed(z, x, R)
                sent += s
                if s == 0 and mex(opts) != cand10(z, x, R):
                    bad += 1
                _corollary_counters(z, x, R, corr)
    res['C2c'] = {'desc': 'deep-x windows x in {70,..,400} z=0..40 R=[x+z+1,x+z+40]',
                  'points': n, 'bad': bad, 'overlap': ov, 'sentinel': sent}


def check_C2d(res, corr):
    n = bad = ov = sent = 0
    for z in range(0, 61):
        x = 10
        for R in range(x + z + 1, x + z + 71):
            n += 1
            if in_T10(z, x, R) and in_P10(z, x, R):
                ov += 1
            opts, s = opts_closed(z, x, R)
            sent += s
            if s == 0 and mex(opts) != cand10(z, x, R):
                bad += 1
            _corollary_counters(z, x, R, corr)
    res['C2d'] = {'desc': 'x=10 edge z=0..60 R=[x+z+1,x+z+70] (+merge,tail)',
                  'points': n, 'bad': bad, 'overlap': ov, 'sentinel': sent}


def check_C3(res):
    n = bad = sent = 0
    for z in range(0, 13):
        for x in range(10, 23):
            for R in range(1, 31):
                n += 1
                # raw child set, enumerated by hand on the raw engine
                raw_opts = set()
                if x > 10:
                    raw_opts.add(H_ordered(R - 1, (x - 1, 10), z))
                else:
                    raw_opts.add(H_ordered(R - 1, (9, 10), z))
                raw_opts.add(H_ordered(R - 1, (x, 9), z))
                if z >= 1:
                    raw_opts.add(1 ^ H_ordered(R - 1, (x, 10), z - 1))
                opts, s = opts_closed(z, x, R)
                sent += s
                if s == 0 and set(opts) != raw_opts:
                    bad += 1
    res['C3'] = {'desc': 'closed child set vs raw child enumeration z=0..12 x=10..22 R<=30',
                 'points': n, 'bad': bad, 'sentinel': sent}


def check_C1b(res):
    n = bad = sent = 0
    for z in range(0, 31):
        for R in range(1, 56):
            n += 1
            a = H_ordered(R, (9, 10), z)
            b = H_ordered(R, (10, 9), z)
            c = H_canonical(R, (10, 9), z)
            w = cand9(z, 10, R)
            if w == -99:
                sent += 1
            elif not (a == b == c == w):
                bad += 1
    res['C1b'] = {'desc': 'raw (9,10)==(10,9)==canonical vs cand9(z,10,R) z=0..30 R<=55',
                  'points': n, 'bad': bad, 'sentinel': sent}


def check_C1c(res):
    n = bad = ov = 0
    for z in range(0, 41):
        for x in range(9, 81):
            for R in range(1, x + z + 41):
                n += 1
                t1 = in_T9(z, x, R)
                p1 = in_P9(z, x, R)
                t2 = in_T9V(z, x, R)
                p2 = in_P9V(z, x, R)
                if t1 != t2 or p1 != p2 or (t1 and p1) != (t2 and p2):
                    bad += 1
                if t1 and p1:
                    ov += 1
    res['C1c'] = {'desc': 'cand9 fit-copy vs verifier-copy tables z=0..40 x=9..80 R<=x+z+40',
                  'points': n, 'bad': bad, 'overlap_both': ov}


def main():
    res = {}
    corr = {'merge': {'points': 0, 'bad': 0}, 'tail': {'points': 0, 'bad': 0}}
    check_C2a(res, corr)
    check_C2b(res, corr)
    check_C2c(res, corr)
    check_C2d(res, corr)
    check_C3(res)
    check_C1b(res)
    check_C1c(res)
    total_bad = 0
    print('y=10 universal-machine pre-flight (y10-universal-machine-preflight-20261120)')
    for k in ('C2a', 'C2b', 'C2c', 'C2d', 'C3', 'C1b', 'C1c'):
        c = res[k]
        total_bad += c['bad'] + c.get('overlap', 0) + c.get('sentinel', 0) + c.get('overlap_both', 0)
        print(f"{k}: points={c['points']} bad={c['bad']}", end='')
        for extra in ('overlap', 'sentinel', 'overlap_both'):
            if extra in c:
                print(f' {extra}={c[extra]}', end='')
        print()
        print(f"    {c['desc']}")
    print(f"corollary merge (x<=z-11): points={corr['merge']['points']} bad={corr['merge']['bad']}")
    print(f"corollary tail (R>=x+z+11): points={corr['tail']['points']} bad={corr['tail']['bad']}")
    total_bad += corr['merge']['bad'] + corr['tail']['bad']
    print('overall:', 'PASS' if total_bad == 0 else 'FAIL', 'total_bad =', total_bad)
    return 0 if total_bad == 0 else 1


if __name__ == '__main__':
    sys.exit(main())
