#!/usr/bin/env python3
"""Verify the three-token first family X=(x,1,1) closed-form FIT (2026-11-23).

Declaration (pre-published skeleton note, single owner):
  research/log/2026-11-23-three-token-x11-first-family-skeleton-single-owner-note.md
  at commit df870814d1e2caba878ac63d3affb0f6d013741b.

This machine executes the declared check battery against the sibling
transcription cand_x11.py and the published closed forms, with the declared
comparison-point totals (EXPECTED below, fixed at declaration time; any
mismatch is FAIL-CLOSED). Status of the family: OBSERVED (fitting). No
universal claim is made by this file. The standard 11x11 empty board and all
root/win-loss questions for it remain UNKNOWN and untouched.

Raw recursion engines (mex/H_ordered/H_canonical/single_token) are VERBATIM
from the published K1101 machine verify_merge.py (whole-file blob SHA-1
5c09857abf56258325d8879430eff028b4c4b4fb); BoundedEngine/
BoundedEngineCanonical are iterative FIFO-capped mirrors of the same option
sets. cand_y1/cand0_y1/cand_y1_allz are VERBATIM from the same file (K1023);
U/U0 are VERBATIM from the published all-ones induction proof machine
verify_induction_proof.py (blob SHA-1 c60c0e985c21eeda83f6a29db2898223b172bc99).
The candidate itself is byte-embedded between @CAND_TRANSCRIPTION markers and
byte-pinned at runtime against the sibling cand_x11.py (check t0).

Checks (C1..C9b; every check restarts the relevant engines from scratch and
fails closed against EXPECTED):
  t0     transcription integrity: embedded block == sibling file bytes;
         engine single_token vs candidate single_token spot sweep
  c1     box: z in [0,31), x in [1,z+41), R in [0,x+z+31): raw H_ordered ==
         raw H_canonical == cand   (rows/points fail-closed)
  c2 k   slices of the z>=31 sample S1: k in {0,1,2,3} -> z in
         [31,38),[38,46),{60},{99}, x in the 15-column sample, R to
         min(x+z+30,200): bounded ordered == bounded canonical == cand
  c3     far columns: (z,x) in {15,31,60}x{300,500,1000}, R in [0,121):
         bounded canonical == cand
  c4 k   merge census slices: z in [0,16),[16,31),[31,46), x in [1,z-3),
         R to x+z+30: bounded canonical == single_token(x+2,z,·) == cand ==
         raw single token of S
  c5     x=1 column = all-ones k=3: z in [0,81), R to min(z+40,90):
         bounded canonical == U/U0 (published universal) == cand
  c6fit  three-token recurrence identity on the fit grid: z in [1,61),
         x in [1,z+9), R in [1,x+z+10): mex{cand_y1_allz(z+1,x,R-1)
         [remove a 1], cand(z-1,x,R-1) xor 1 [z-move], cand(z,x-1,R-1)
         [decrement x] if x>=2} == cand(z,x,R)
  c6raw k same recurrence with raw bounded engines instead of closed forms:
         slice k in {0,1} -> z in [1,16),[16,31)
  c7     steady sharpness: z in [0,76), x in [z+5,z+41):
         cand(z,x,x+z+3) != (x+2) mod 2 (last pre-tail point differs)
  c7b    3 deep steady columns (20,25),(31,36),(33,38): pretail differs,
         tail value (x+2) mod 2 constant through R=30000
  c8 k   declared LCG sweep slices (k in {0,1,2,3}, 15000 draws each,
         seed 20261123, z=draw1%201, x=1+draw2%(z+60),
         R=draw3%(min(x+z+12,150)+1)): bounded ordered == cand always,
         bounded canonical == cand on every 13th draw; first3/last3 slice
         anchors fail-closed against the declaration
  c9     all-ones lemma columns: z in [4,81), R in [0,z+41):
         U(3,z,·) == single_token(3,z,·) == raw single token
  c9b    row-structure census: z in [0,76), x in [1,z+40): merge rows None,
         row descriptors have V2^V1 = empty and positive tail start;
         the (0,4) generic d=+4 row equals the (0,4) exception entry
         (double booking, checked by surgery)
  audit  fail-closed master audit: all parts present, totals == 494579
         declared comparison points, all bad == 0, C8 anchors == declaration
  --tamper K   tamper battery: K=0 clean control (rc 0), K in 1..10 =
         declared tamper variants (each must be DETECTED, rc 1);
         rc 2 = fail-open (tamper not detected), rc 3 = clean control broken

Deterministic: fixed iteration order, fixed seeds, sorted JSON keys, no
timestamps, stdlib only.
"""
import hashlib
import json
import os
import sys
from functools import lru_cache

sys.setrecursionlimit(1_000_000)

HERE = os.path.dirname(os.path.abspath(__file__))
CAND_FILE = os.path.join(HERE, "cand_x11.py")
OUTD = os.path.join(HERE, "output")

DECLARED_NOTE_COMMIT = "df870814d1e2caba878ac63d3affb0f6d013741b"
DECLARED_NOTE_PATH = "research/log/2026-11-23-three-token-x11-first-family-skeleton-single-owner-note.md"

EXPECTED = {
    "C1": {"rows": 1705, "points": 129890},
    "C2S": [[105, 10178], [120, 13252], [15, 2156], [15, 2808]],
    "C2_TOTAL_ROWS_POINTS": [255, 28394],
    "C3": {"points": 1089},
    "C4S": [[78, 3666], [300, 19770], [525, 46095]],
    "C5": {"points": 6096},
    "C6": {"fit_points": 163860, "raw_points": 26460},
    "C6RAW": [5580, 20880],
    "C7": {"rows": 2736},
    "C7b": {"columns": 3, "points": 132},
    "C8": {"points": 60000,
           "first3": [[75, 1, 5], [129, 7, 42], [16, 72, 15]],
           "last3": [[182, 39, 108], [149, 37, 62], [146, 121, 106]]},
    "C9": {"lemma_points": 6391},
    "C9b": {"rows": 5890},
    "total": 494579,
}
def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


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
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            opts.add(H_canonical(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_canonical(R - 1, X[:i] + X[i + 1:], z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)


def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
    """Published single-token closed form (K0832 machinery, as transcribed in
    the z17-y2 census)."""
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


_engine_single_token = single_token


# ---------------------------------------------------- bounded memo engines


class _BoundedEngine:
    """Iterative FIFO-capped memo mirror of H_ordered (CANONICAL=False) /
    H_canonical (CANONICAL=True): exactly the same option sets, evaluated
    bottom-up with an explicit stack. Values are pure, so eviction only
    costs recomputation, never correctness."""

    CANONICAL = False
    CAP = 2_000_000

    def __init__(self):
        from collections import deque
        self._deque = deque
        self.cache = {}
        self.fifo = deque()

    def clear(self):
        self.cache = {}
        self.fifo = self._deque()

    def _store(self, key, val):
        self.cache[key] = val
        self.fifo.append(key)
        while len(self.cache) > self.CAP:
            self.cache.pop(self.fifo.popleft(), None)

    def _children(self, r, X, z):
        out = []
        if not self.CANONICAL:
            for i, v in enumerate(X):
                if v > 1:
                    out.append((r - 1, X[:i] + (v - 1,) + X[i + 1:], z))
                else:
                    out.append((r - 1, X[:i] + X[i + 1:], z + 1))
        else:
            i = 0
            n = len(X)
            while i < n:
                v = X[i]
                if v > 1:
                    out.append((r - 1, X[:i] + (v - 1,) + X[i + 1:], z))
                else:
                    out.append((r - 1, X[:i] + X[i + 1:], z + 1))
                while i + 1 < n and X[i + 1] == v:
                    i += 1
                i += 1
        return out

    def H(self, R, X, z):
        key = (R, X, z)
        if key in self.cache:
            return self.cache[key]
        stack = [key]
        while stack:
            k = stack[-1]
            if k in self.cache:
                stack.pop()
                continue
            r, Xk, zk = k
            if r == 0:
                self._store(k, 0)
                stack.pop()
                continue
            opts = []
            missing = []
            cache_get = self.cache.get
            for ch in self._children(r, Xk, zk):
                v = cache_get(ch)
                if v is None:
                    missing.append(ch)
                else:
                    opts.append(v)
            if missing:
                stack.extend(missing)
                continue
            if zk >= 1:
                ck = (r - 1, Xk, zk - 1)
                v = cache_get(ck)
                if v is None:
                    stack.append(ck)
                    continue
                opts.append(1 ^ v)
            self._store(k, mex(opts))
            stack.pop()
        return self.cache[key]


class BoundedEngine(_BoundedEngine):
    CANONICAL = False


class BoundedEngineCanonical(_BoundedEngine):
    CANONICAL = True

# @@CAND_TRANSCRIPTION_START@@
#!/usr/bin/env python3
"""Three-token residual game, first family X=(x,1,1), kappa=1.

Closed-form candidate cand_x11(z, x, R) == H(R; (x, 1, 1); z) for the
K0832 residual game (abstract, kappa=1; no claim about the 2D board).

Regions (d = x - z, S = x + 2):
  merge    x <= z-3          : single_token(x+2, z, R)   (K0832 published
                              single-token closed form, transcribed verbatim)
  transient d in [-2, +4]    : 14 parametric row types (z parity x d), see
                              cand_x11 docstring in verify file / report.md
  steady   x >= z+5          : V2 = odds<=z-1 u {z+3}   (z even, z=0: {3})
                               V2 = odds<=z+4           (z odd)
                               V1 = {z+1} u parity band [z+5, x+z+3]
                               tail R>=x+z+4: (x+2) mod 2  (sharp)
  exceptions (z,x) in {(2,1),(1,1),(1,2),(0,1),(0,2),(0,3),(0,4)}:
                              explicit rows; the x=1 rows (0,1),(1,1),(2,1)
                              are exactly the published all-ones slice
                              U0(3,.) / U(3,1,.) / U(3,2,.) (universal
                              theorem, vertical-fiber-all-ones-induction-proof).

Status: observed (fitting). No universal claim.
Deterministic, stdlib only.
"""


def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
    """Published single-token closed form (K0832). Transcribed VERBATIM from
    research/experiments/vertical-fiber-two-token-merge-below-diagonal-20261120/
    verify_merge.py (GitHub blob SHA 5c09857abf56258325d8879430eff028b4c4b4fb).
    """
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


# Exception rows (z, x) -> (V2 tuple, V1F tuple, tail_R, tail_val).
# Verified against the published all-ones slice U/U0 for the x=1 rows.
_EXC = {
    (2, 1): ((1, 5), (3, 4), 6, 1),
    (1, 1): ((1, 3), (2,), 5, 1),
    (1, 2): ((1, 3, 5), (2,), 6, 0),
    (0, 1): ((), (1,), 4, 1),
    (0, 2): ((3,), (1, 4), 5, 0),
    (0, 3): ((3, 5), (1,), 6, 1),
    (0, 4): ((3, 7), (1, 5), 8, 0),
}


def _odds(lo, hi):
    """Odd integers in [lo, hi] (list)."""
    if lo % 2 == 0:
        lo += 1
    return list(range(lo, hi + 1, 2))


def _band(lo, hi, parity):
    """Integers in [lo, hi] congruent to parity (mod 2) (list)."""
    if lo % 2 != parity:
        lo += 1
    return list(range(lo, hi + 1, 2))


def _ev(z, x, R, V2, V1F, t, tv):
    """Evaluate a row (V2 set, V1F set, tail start t, tail value tv)."""
    if R in V2:
        return 2
    if R in V1F:
        return 1
    if R >= t:
        return tv
    return 0


def _row(z, x):
    """Row descriptor (V2 set, V1F set, t, tv) for cand_x11 at (z, x)."""
    if (z, x) in _EXC:
        V2, V1F, t, tv = _EXC[(z, x)]
        return set(V2), set(V1F), t, tv
    d = x - z
    if d <= -3:
        return None  # merge branch: single_token path, no row sets
    par = z & 1
    if d >= 5:
        # steady
        if par == 0:
            V2 = set(_odds(1, max(z - 1, 0))) | {z + 3}
        else:
            V2 = set(_odds(1, z + 4))
        V1F = {z + 1} | set(_band(z + 5, x + z + 3, (z + 1) & 1))
        t = x + z + 4
        tv = (x + 2) & 1
        return V2, V1F, t, tv
    # transient d in [-2, 4]
    if d == -2:
        if par == 0:
            return set(_odds(1, z + 1)), set(), z + 2, 0
        return set(_odds(1, z)), set(), z + 1, 1
    if d == -1:
        if par == 0:
            return set(_odds(1, max(z - 1, 0))), set(), z + 1, 1
        return set(_odds(1, z)), {z + 1}, z + 2, 0
    if d == 0:
        if par == 0:
            return set(_odds(1, max(z - 1, 0))), {z + 1}, z + 2, 0
        return set(_odds(1, z + 2)), {z + 1}, z + 3, 1
    if d == 1:
        if par == 0:
            return set(_odds(1, max(z - 1, 0))) | {z + 3}, {z + 1}, z + 4, 1
        return set(_odds(1, z + 2)), {z + 1}, z + 3, 0
    if d == 2:
        if par == 0:
            V2 = set(_odds(1, max(z - 1, 0))) | {z + 3} | set(_odds(z + 5, 2 * z + 3))
            return V2, {z + 1}, 2 * z + 4, 0
        V2 = set(_odds(1, 2 * z + 3))
        V1F = {z + 1} | set(_band(z + 5, 2 * z + 3, (z + 1) & 1))
        return V2, V1F, 2 * z + 4, 1
    if d == 3:
        if par == 0:
            V2 = set(_odds(1, max(z - 1, 0))) | {z + 3}
            V1F = {z + 1} | set(_band(z + 5, 2 * z + 3, (z + 1) & 1))
            return V2, V1F, 2 * z + 5, 1
        V2 = set(_odds(1, z + 4))
        V1F = {z + 1} | set(_band(z + 5, 2 * z + 4, (z + 1) & 1))
        return V2, V1F, 2 * z + 5, 0
    if d == 4:
        # x = z + 4; diag pin at 2x-1 = 2z+7 collides with the band top on
        # even z (V2 wins) and sits above the band on odd z.
        if par == 0:
            V2 = set(_odds(1, max(z - 1, 0))) | {z + 3} | {2 * x - 1}
            V1F = {z + 1} | set(_band(z + 5, 2 * z + 5, (z + 1) & 1))
            return V2, V1F, x + z + 4, (x + 2) & 1
        V2 = set(_odds(1, z + 4)) | {2 * x - 1}
        V1F = {z + 1} | set(_band(z + 5, 2 * z + 6, (z + 1) & 1))
        return V2, V1F, x + z + 4, (x + 2) & 1
    raise ValueError((z, x, d))


def cand_x11(z, x, R):
    """Closed-form candidate for H(R; (x,1,1); z), kappa=1 residual game.

    Domains: z >= 0, x >= 1, R >= 0. Status: observed (fit).
    """
    if R == 0:
        return 0
    d = x - z
    if d <= -3:
        # merge below the S=x+2 diagonal: x <= z-3 (z >= 4)
        return single_token(x + 2, z, R)
    V2, V1F, t, tv = _row(z, x)
    if not (V2 & V1F):  # T/P disjointness (structural assert)
        pass
    else:
        raise AssertionError(("T/P overlap", z, x, sorted(V2 & V1F)))
    if R in V2:
        return 2
    if R in V1F:
        return 1
    if R >= t:
        return tv
    return 0
# @@CAND_TRANSCRIPTION_END@@

def cand_y1(z, x, R):
    """Published y=1 parametric closed form (K1023, verbatim cand())."""
    if R == 0:
        return 0
    if x < 1:
        return 0
    S = x + 1 + z
    if z % 2 == 0:
        if x % 2 == 0 and 2 <= x <= z - 2:
            T = (R % 2 == 1 and R <= x + 1)
        elif x % 2 == 1 and x <= z - 3:
            T = (R % 2 == 1 and R <= x)
        elif x == z - 1:
            T = (R % 2 == 1 and R <= z + 1)
        elif x in (z, z + 1):
            T = (R % 2 == 1 and R <= z - 1)
        elif x == z + 2:
            T = (R % 2 == 1 and (R <= z - 1 or z + 3 <= R <= 2 * z + 3))
        else:
            T = (R == z + 3 or (R % 2 == 1 and R <= z - 1))
        if x % 2 == 1 and x <= z - 1:
            P = False
        elif x % 2 == 0 and x <= z - 2:
            P = (R >= x + 2)
        elif x == z:
            P = (R >= z + 1)
        elif x == z + 1:
            P = (R == z + 1)
        elif x % 2 == 0:
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S - 1) or R >= S + 1)
        else:
            P = (R == z + 1 or (R % 2 == 0 and z + 4 <= R <= S))
    else:
        if x % 2 == 0 and x <= z - 1:
            T = (R % 2 == 1 and R <= x + 1)
        elif x % 2 == 1 and x <= z:
            T = (R % 2 == 1 and R <= x)
        elif x == z + 1:
            T = (R % 2 == 1 and R <= z + 2)
        elif x == z + 2:
            T = (R % 2 == 1 and R <= 2 * z + 3)
        else:
            T = (R == z + 2 or (R % 2 == 1 and R <= z))
        if x % 2 == 1 and x <= z - 2:
            P = False
        elif x % 2 == 0 and x <= z - 1:
            P = (R >= x + 2)
        elif x == z:
            P = (R == z + 1)
        elif x == z + 1:
            P = (R == z + 1 or R >= z + 3)
        elif x == z + 2:
            P = (R == z + 1)
        elif x % 2 == 1:
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S))
        else:
            P = (R == z + 1 or (R % 2 == 1 and z + 4 <= R <= S) or R >= S + 1)
    assert not (T and P), (z, x, R)
    return 2 if T else (1 if P else 0)


def cand0_y1(x, R):
    """Published y=1 z=0 base closed form (K1023, cand0)."""
    if R == 0 or x < 1:
        return 0
    if x == 1:
        return 1 if R == 1 else 0
    if R == 3:
        return 2
    if x % 2 == 1:
        return 1 if (R == 1 or (R % 2 == 0 and 4 <= R <= x + 1)) else 0
    return 1 if (R == 1 or (R % 2 == 0 and 4 <= R <= x) or R >= x + 2) else 0


def cand_y1_allz(z, x, R):
    if R == 0:
        return 0
    if z == 0:
        return cand0_y1(x, R)
    return cand_y1(z, x, R)


def q(n):
    return n if n % 2 == 1 else n - 1


def U(k, z, R):  # published unified slice closed form (verbatim)
    if z < 1:
        raise ValueError
    if z % 2 == 1:
        if R % 2 == 1:
            return 2 if R <= q(k) else (1 if k % 2 == 1 else 0)
        if k % 2 == 1:
            if R <= min(z - 3, k - 1):
                return 0
            if R % 4 == (z - 1) % 4 and z - 1 <= R <= 2 * k - z - 1:
                return 0
            return 1
        else:
            if R % 4 == (z + 1) % 4 and z + 1 <= R <= 2 * k - z - 1:
                return 1
            return 0
    else:
        twos = set(range(1, q(min(k, z)) + 1, 2))
        far = 2 * k - z + 1
        if far >= 1:
            twos.add(far)
        if R in twos:
            return 2
        if R % 4 == (z + 1) % 4 and z + 1 <= R <= 2 * k - z - 1 and R != far:
            return 1
        if k % 2 == 1:
            if (R % 2 == 0 and R <= k - 1) or (R % 4 == (z - 1) % 4 and z + 3 <= R <= 2 * k - z - 3):
                return 0
            return 1
        return 0

def U0(k, R):
    if k >= 1 and R >= 1:
        return 1 if U(k - 1, 1, R - 1) == 0 else 0
    return 0


_band_orig = _band


# ------------------------------------------------------------------ checks

CAND_OVERRIDE = None


def CAND(z, x, R):
    if CAND_OVERRIDE is not None:
        return CAND_OVERRIDE(z, x, R)
    return cand_x11(z, x, R)


def dump(name, obj):
    os.makedirs(OUTD, exist_ok=True)
    p = os.path.join(OUTD, "part-%s.json" % name)
    with open(p, "w") as f:
        json.dump(obj, f, indent=1, sort_keys=True)
        f.write("\n")
    print("wrote", p)


def fail_closed(msg):
    print("FAIL-CLOSED:", msg)
    sys.exit(1)


def check_counts(name, got, want):
    for k, v in want.items():
        if got.get(k) != v:
            fail_closed("CHECK-COUNT-MISMATCH %s.%s got %r want %r" % (name, k, got.get(k), v))


def run_t0():
    src = open(os.path.join(HERE, "verify_x11.py"), "rb").read().decode()
    m1 = "# @@CAND" + "_TRANSCRIPTION_START@@\n"
    m2 = "# @@CAND" + "_TRANSCRIPTION_END@@\n"
    if src.count(m1) != 1 or src.count(m2) != 1:
        fail_closed("T0 marker uniqueness violated")
    block = src.split(m1)[1].split(m2)[0]
    cand_text = open(CAND_FILE, "rb").read().decode()
    byte_equal = block == cand_text
    # engine-block single_token vs cand-block single_token spot equality
    bad = 0
    n = 0
    spot_bad = []
    for x in range(1, 41):
        for z in range(0, 41):
            for R in range(0, min(x + z, 60) + 1):
                n += 1
                a = single_token(x, z, R)  # cand-block copy (defined later, wins)
                b = _engine_single_token(x, z, R)
                if a != b:
                    bad += 1
                    if len(spot_bad) < 5:
                        spot_bad.append([x, z, R, a, b])
    doc = {
        "cand_transcription_byte_equal": bool(byte_equal),
        "single_token_spot_points": n,
        "single_token_spot_bad": bad,
        "single_token_spot_bad_first": spot_bad,
        "cand_sha256": hashlib.sha256(cand_text.encode()).hexdigest(),
        "markers": "1x1",
    }
    if not byte_equal:
        fail_closed("T0: transcription is not byte-equal to sibling cand_x11.py")
    if bad:
        fail_closed("T0: engine/cand single_token spot mismatch")
    dump("t0", doc)
    print("T0 PASS")


def run_c1():
    bad = []
    n = rows = 0
    for z in range(0, 31):
        for x in range(1, z + 41):
            rows += 1
            topR = x + z + 30
            X = (x, 1, 1)
            for R in range(0, topR + 1):
                n += 1
                ho = H_ordered(R, X, z)
                hc = H_canonical(R, X, z)
                c = CAND(z, x, R)
                if not (ho == hc == c):
                    bad.append([z, x, R, ho, hc, c])
                    if len(bad) >= 20:
                        break
            if len(bad) >= 20:
                break
        if len(bad) >= 20:
            break
    doc = {"rows": rows, "points": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C1", doc, EXPECTED["C1"])
    if bad:
        fail_closed("C1 bad %d" % len(bad))
    dump("c1", doc)
    print("C1 PASS")


def _c2_xs(z):
    xs = sorted(set([1, 2, 3] + list(range(max(1, z - 3), z + 7)) + [z + 5, z + 6, z + 10, z + 40]))
    return [t for t in xs if t >= 1]


C2_ZS = [list(range(31, 38)), list(range(38, 46)), [60], [99]]


def run_c2(idx):
    EO = BoundedEngine()
    EC = BoundedEngineCanonical()
    bad = []
    n = rows = 0
    for z in C2_ZS[idx]:
        for x in _c2_xs(z):
            topR = min(x + z + 30, 200)
            rows += 1
            for R in range(0, topR + 1):
                n += 1
                ho = EO.H(R, (x, 1, 1), z)
                hc = EC.H(R, (x, 1, 1), z)
                c = CAND(z, x, R)
                if not (ho == hc == c):
                    bad.append([z, x, R, ho, hc, c])
                    if len(bad) >= 20:
                        break
            if len(bad) >= 20:
                break
        EO.clear()
        EC.clear()
        if len(bad) >= 20:
            break
    doc = {"slice": idx, "rows": rows, "points": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C2s%d" % idx, doc, {"rows": EXPECTED["C2S"][idx][0],
                                     "points": EXPECTED["C2S"][idx][1]})
    if bad:
        fail_closed("C2s%d bad %d" % (idx, len(bad)))
    dump("c2s%d" % idx, doc)
    print("C2s%d PASS" % idx)


def run_c3():
    EC = BoundedEngineCanonical()
    bad = []
    n = 0
    for z in [15, 31, 60]:
        for x in [300, 500, 1000]:
            for R in range(0, 121):
                n += 1
                hc = EC.H(R, (x, 1, 1), z)
                c = CAND(z, x, R)
                if hc != c:
                    bad.append([z, x, R, hc, c])
                    if len(bad) >= 20:
                        break
            EC.clear()
            if len(bad) >= 20:
                break
        if len(bad) >= 20:
            break
    doc = {"points": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C3", doc, EXPECTED["C3"])
    if bad:
        fail_closed("C3 bad %d" % len(bad))
    dump("c3", doc)
    print("C3 PASS")


C4_ZS = [(0, 16), (16, 31), (31, 46)]


def run_c4(idx):
    EC = BoundedEngineCanonical()
    bad = []
    n = rows = 0
    z0, z1 = C4_ZS[idx]
    for z in range(z0, z1):
        for x in range(1, z - 2):
            rows += 1
            topR = x + z + 30
            for R in range(0, topR + 1):
                n += 1
                hc = EC.H(R, (x, 1, 1), z)
                v = single_token(x + 2, z, R)
                raws = EC.H(R, (x + 2,), z)
                c = CAND(z, x, R)
                if not (hc == v == c) or raws != v:
                    bad.append([z, x, R, hc, v, c, raws])
                    if len(bad) >= 20:
                        break
            if len(bad) >= 20:
                break
        EC.clear()
        if len(bad) >= 20:
            break
    doc = {"slice": idx, "rows": rows, "points": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C4s%d" % idx, doc, {"rows": EXPECTED["C4S"][idx][0],
                                     "points": EXPECTED["C4S"][idx][1]})
    if bad:
        fail_closed("C4s%d bad %d" % (idx, len(bad)))
    dump("c4s%d" % idx, doc)
    print("C4s%d PASS" % idx)


def run_c5():
    EC = BoundedEngineCanonical()
    bad = []
    n = 0
    for z in range(0, 81):
        topR = min(z + 40, 90)
        for R in range(0, topR + 1):
            n += 1
            hc = EC.H(R, (1, 1, 1), z)
            uu = U(3, z, R) if z >= 1 else U0(3, R)
            c = CAND(z, 1, R)
            if not (hc == uu == c):
                bad.append([z, R, hc, uu, c])
                if len(bad) >= 20:
                    break
        EC.clear()
        if len(bad) >= 20:
            break
    doc = {"points": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C5", doc, EXPECTED["C5"])
    if bad:
        fail_closed("C5 bad %d" % len(bad))
    dump("c5", doc)
    print("C5 PASS")


def run_c6fit():
    bad = []
    n = 0
    for z in range(1, 61):
        for x in range(1, z + 9):
            for R in range(1, x + z + 10):
                n += 1
                B = cand_y1_allz(z + 1, x, R - 1)
                opts = {B}
                C = 1 ^ CAND(z - 1, x, R - 1)
                opts.add(C)
                if x >= 2:
                    A = CAND(z, x - 1, R - 1)
                    opts.add(A)
                w = mex(opts)
                c = CAND(z, x, R)
                if w != c:
                    bad.append([z, x, R, w, c])
                    if len(bad) >= 20:
                        break
            if len(bad) >= 20:
                break
        if len(bad) >= 20:
            break
    doc = {"points": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C6fit", doc, {"points": EXPECTED["C6"]["fit_points"]})
    if bad:
        fail_closed("C6fit bad %d" % len(bad))
    dump("c6fit", doc)
    print("C6fit PASS")


C6RAW_ZS = [(1, 16), (16, 31)]


def run_c6raw(idx):
    EC = BoundedEngineCanonical()
    bad = []
    n = 0
    z0, z1 = C6RAW_ZS[idx]
    for z in range(z0, z1):
        for x in range(1, z + 9):
            for R in range(1, x + z + 6):
                n += 1
                B = EC.H(R - 1, (x, 1), z + 1)
                opts = {B}
                C = 1 ^ EC.H(R - 1, (x, 1, 1), z - 1)
                opts.add(C)
                if x >= 2:
                    opts.add(EC.H(R - 1, (x - 1, 1, 1), z))
                w = mex(opts)
                hp = EC.H(R, (x, 1, 1), z)
                if w != hp:
                    bad.append([z, x, R, w, hp])
                    if len(bad) >= 20:
                        break
            if len(bad) >= 20:
                break
        EC.clear()
        if len(bad) >= 20:
            break
    doc = {"slice": idx, "points": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C6raw%d" % idx, doc, {"points": EXPECTED["C6RAW"][idx]})
    if bad:
        fail_closed("C6raw%d bad %d" % (idx, len(bad)))
    dump("c6raw%d" % idx, doc)
    print("C6raw%d PASS" % idx)


def run_c7():
    bad = []
    n = 0
    for z in range(0, 76):
        for x in range(z + 5, z + 41):
            n += 1
            tv = (x + 2) & 1
            v = CAND(z, x, x + z + 3)
            if v == tv:
                bad.append([z, x, v, tv])
                if len(bad) >= 20:
                    break
        if len(bad) >= 20:
            break
    doc = {"rows": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C7", doc, EXPECTED["C7"])
    if bad:
        fail_closed("C7 bad %d" % len(bad))
    dump("c7", doc)
    print("C7 PASS")


def run_c7b():
    EC = BoundedEngineCanonical()
    bad = []
    n = 0
    cols = []
    for z, x in [(20, 25), (31, 36), (33, 38)]:
        t = x + z + 4
        tv = (x + 2) & 1
        okpre = EC.H(x + z + 3, (x, 1, 1), z) != tv
        vals = [EC.H(R, (x, 1, 1), z) for R in range(t, t + 40)]
        deep = [EC.H(R, (x, 1, 1), z) for R in (29997, 29998, 29999, 30000)]
        n += 44
        if not okpre:
            bad.append([z, x, "pretail"])
        if any(v != tv for v in vals) or any(v != tv for v in deep):
            bad.append([z, x, "tailvalue", vals[0], deep[0], tv])
        else:
            cols.append([z, x, t, tv])
        EC.clear()
    doc = {"columns": len(cols), "points": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C7b", doc, EXPECTED["C7b"])
    if bad:
        fail_closed("C7b bad %d" % len(bad))
    dump("c7b", doc)
    print("C7b PASS")


C8_PER = 15000


def _c8_draw(iLow, iHigh, engines=("o", "c13")):
    """Process draws [iLow, iHigh); returns (bad, nfirsts, nlasts)."""
    EO = BoundedEngine()
    EC = BoundedEngineCanonical()
    bad = []
    n = 0
    st = 20261123
    firsts = []
    lasts = []
    for _ in range(3 * iLow):
        st = (6364136223846793005 * st + 1442695040888963407) % (1 << 64)
    for i in range(iLow, iHigh):
        st = (6364136223846793005 * st + 1442695040888963407) % (1 << 64)
        d1 = st
        st = (6364136223846793005 * st + 1442695040888963407) % (1 << 64)
        d2 = st
        st = (6364136223846793005 * st + 1442695040888963407) % (1 << 64)
        d3 = st
        z = d1 % 201
        x = 1 + d2 % (z + 60)
        Rcap = min(x + z + 12, 150)
        R = d3 % (Rcap + 1)
        n += 1
        h_o = EO.H(R, (x, 1, 1), z)
        use_c = (engines == "o" and (i % 13 == 0)) or engines == "c"
        h_c = EC.H(R, (x, 1, 1), z) if use_c else h_o
        c = CAND(z, x, R)
        if not (h_o == h_c == c):
            bad.append([z, x, R, h_o, h_c, c])
            if len(bad) >= 20:
                break
        if i - iLow < 3:
            firsts.append([z, x, R])
        if i >= iHigh - 3:
            lasts.append([z, x, R])
    return bad, n, firsts, lasts


def run_c8(idx):
    iLow = idx * C8_PER
    iHigh = iLow + C8_PER
    bad, n, firsts, lasts = _c8_draw(iLow, iHigh, ("o", "c13"))
    doc = {"slice": idx, "draws_low": iLow, "draws_high": iHigh, "points": n,
           "bad": len(bad), "first": bad[:20],
           "slice_first3": firsts, "slice_last3": lasts,
           "canonical_engine_points": (n + 12) // 13}
    if doc["points"] != C8_PER or doc["bad"] != 0:
        fail_closed("C8s%d points/bad mismatch" % idx)
    dump("c8s%d" % idx, doc)
    print("C8s%d PASS" % idx)


def run_c9():
    EC = BoundedEngineCanonical()
    bad = []
    n = 0
    for z in range(4, 81):
        for R in range(0, z + 41):
            n += 1
            uu = U(3, z, R)
            v = single_token(3, z, R)
            raw = EC.H(R, (3,), z)
            if not (uu == v == raw):
                bad.append([z, R, uu, v, raw])
                if len(bad) >= 20:
                    break
        EC.clear()
        if len(bad) >= 20:
            break
    doc = {"lemma_points": n, "bad": len(bad), "first": bad[:20]}
    check_counts("C9", doc, EXPECTED["C9"])
    if bad:
        fail_closed("C9 bad %d" % len(bad))
    dump("c9", doc)
    print("C9 PASS")


def run_c9b():
    bad = []
    n = 0
    # (0,4) double booking: generic d=+4 row (EXC disabled) == EXC entry
    exc04 = _EXC[(0, 4)]
    del _EXC[(0, 4)]
    try:
        gen04 = _row(0, 4)
    finally:
        _EXC[(0, 4)] = exc04
    if gen04 is None:
        bad.append([(0, 4), "generic row is None"])
    else:
        V2, V1F, t, tv = gen04
        if not (V2 == set(exc04[0]) and V1F == set(exc04[1]) and t == exc04[2] and tv == exc04[3]):
            bad.append([(0, 4), sorted(V2), sorted(V1F), t, tv])
    for z in range(0, 76):
        for x in range(1, z + 41):
            n += 1
            d = x - z
            row = _row(z, x)
            if d <= -3:
                if row is not None:
                    bad.append([z, x, "merge row not None"])
            else:
                if row is None:
                    bad.append([z, x, "row None"])
                    continue
                V2, V1F, t, tv = row
                if V2 & V1F:
                    bad.append([z, x, "T/P overlap", sorted(V2 & V1F)])
                if t <= 0:
                    bad.append([z, x, "nonpositive tail start", t])
            if len(bad) >= 20:
                break
        if len(bad) >= 20:
            break
    doc = {"rows": n, "bad": len(bad), "first": bad[:20],
           "exc04_double_booked_equal": (len(bad) == 0)}
    check_counts("C9b", doc, EXPECTED["C9b"])
    if bad:
        fail_closed("C9b bad %d" % len(bad))
    dump("c9b", doc)
    print("C9b PASS")


def run_audit():
    names = (["t0", "c1"] + ["c2s%d" % i for i in range(4)] + ["c3"]
             + ["c4s%d" % i for i in range(3)]
             + ["c5", "c6fit", "c6raw0", "c6raw1", "c7", "c7b"]
             + ["c8s%d" % i for i in range(4)] + ["c9", "c9b"])
    checks = {}
    total = 0
    for nm in names:
        p = os.path.join(OUTD, "part-%s.json" % nm)
        if not os.path.exists(p):
            fail_closed("audit: missing part %s" % nm)
        with open(p) as f:
            checks[nm] = json.load(f)
    if not checks["t0"]["cand_transcription_byte_equal"]:
        fail_closed("audit: T0 not byte equal")
    if checks["t0"]["single_token_spot_bad"] != 0:
        fail_closed("audit: T0 spot bad")
    pts = {"C1": checks["c1"]["points"]}
    pts["C2"] = sum(checks["c2s%d" % i]["points"] for i in range(4))
    pts["C3"] = checks["c3"]["points"]
    pts["C4"] = sum(checks["c4s%d" % i]["points"] for i in range(3))
    pts["C5"] = checks["c5"]["points"]
    pts["C6"] = checks["c6fit"]["points"] + checks["c6raw0"]["points"] + checks["c6raw1"]["points"]
    pts["C7"] = checks["c7"]["rows"]
    pts["C7b"] = checks["c7b"]["points"]
    pts["C8"] = sum(checks["c8s%d" % i]["points"] for i in range(4))
    pts["C9"] = checks["c9"]["lemma_points"]
    for k, v in pts.items():
        total += v
    if total != EXPECTED["total"]:
        fail_closed("audit: total %d != declared %d" % (total, EXPECTED["total"]))
    # declared pre-registration anchors from the note
    if checks["c8s0"]["slice_first3"] != EXPECTED["C8"]["first3"]:
        fail_closed("audit: C8 first3 anchor mismatch")
    if checks["c8s3"]["slice_last3"] != EXPECTED["C8"]["last3"]:
        fail_closed("audit: C8 last3 anchor mismatch")
    bads = {
        "c1": checks["c1"]["bad"],
        "c2": sum(checks["c2s%d" % i]["bad"] for i in range(4)),
        "c3": checks["c3"]["bad"],
        "c4": sum(checks["c4s%d" % i]["bad"] for i in range(3)),
        "c5": checks["c5"]["bad"],
        "c6": checks["c6fit"]["bad"] + checks["c6raw0"]["bad"] + checks["c6raw1"]["bad"],
        "c7": checks["c7"]["bad"], "c7b": checks["c7b"]["bad"],
        "c8": sum(checks["c8s%d" % i]["bad"] for i in range(4)),
        "c9": checks["c9"]["bad"], "c9b": checks["c9b"]["bad"],
    }
    if any(v != 0 for v in bads.values()):
        fail_closed("audit: bad counts nonzero")
    doc = {
        "family": "three-token-first-family-X=(x,1,1)",
        "stage": "fit",
        "status": "PASS",
        "kind": "master-verifier-audit",
        "declared_note_commit": "df870814d1e2caba878ac63d3affb0f6d013741b",
        "declared_note_path": "research/log/2026-11-23-three-token-x11-first-family-skeleton-single-owner-note.md",
        "provenance": {
            "engines_and_y1": "verify_merge.py (K1101 machine), whole-file blob SHA-1 5c09857abf56258325d8879430eff028b4c4b4fb, refetched byte-compared at declaration HEAD df870814",
            "all_ones_U": "verify_induction_proof.py (vertical-fiber-all-ones-induction-proof-20261116), refetched byte-compared at declaration HEAD df870814",
            "cand": "sibling cand_x11.py, sha256 below, byte-pinned by T0",
        },
        "cand_sha256": checks["t0"]["cand_sha256"],
        "expected": EXPECTED,
        "per_check_points": pts,
        "checks": checks,
        "total_points": total,
        "total_bad": 0,
    }
    p = os.path.join(OUTD, "audit.json")
    with open(p, "w") as f:
        json.dump(doc, f, indent=1, sort_keys=True)
        f.write("\n")
    print("AUDIT PASS total_points=%d" % total)
    print("wrote", p)


# ------------------------------------------------------------------ tamper

_orig_cand_x11 = None


def _get_orig():
    global _orig_cand_x11
    if _orig_cand_x11 is None:
        _orig_cand_x11 = cand_x11
    return _orig_cand_x11


def _t1(z, x, R):
    if (z, x, R) == (0, 1, 1):
        return 1 ^ _get_orig()(z, x, R)
    return _get_orig()(z, x, R)


def _t4(z, x, R):
    if x == z - 3:
        return _get_orig()(z, x, R) ^ 1
    return _get_orig()(z, x, R)


def _t5(z, x, R):
    if x - z >= 5 and R == x + z + 4:
        return 0
    return _get_orig()(z, x, R)


def _t6(z, x, R):
    if x - z >= 5 and R >= x + z + 4:
        return 1 ^ _get_orig()(z, x, R)
    return _get_orig()(z, x, R)


def _t7(z, x, R):
    if z % 2 == 0 and x == z + 2 and R == 2 * z + 3:
        return 0
    return _get_orig()(z, x, R)


def _t8(z, x, R):
    if x == z + 4 and R == 2 * x - 1:
        return 0
    return _get_orig()(z, x, R)


TAMPER_SPECS = {
    1: ("override-point-flip-(0,1,1)",
        lambda: globals().__setitem__("CAND_OVERRIDE", _t1)),
    2: ("exc-row-(2,1)-V2-V1F-swap",
        lambda: _EXC.__setitem__((2, 1), ((3, 4), (1, 5), 6, 1))),
    3: ("steady-band-parity-flip",
        lambda: globals().__setitem__("_band",
               (lambda lo, hi, parity: _band_orig(lo, hi, 1 - parity)))),
    4: ("merge-boundary-x=z-3-xor1",
        lambda: globals().__setitem__("CAND_OVERRIDE", _t4)),
    5: ("tail-start-x+z+4-drop",
        lambda: globals().__setitem__("CAND_OVERRIDE", _t5)),
    6: ("tail-value-flip",
        lambda: globals().__setitem__("CAND_OVERRIDE", _t6)),
    7: ("d=+2-sweep-top-removal",
        lambda: globals().__setitem__("CAND_OVERRIDE", _t7)),
    8: ("d=+4-diag-pin-removal",
        lambda: globals().__setitem__("CAND_OVERRIDE", _t8)),
    9: ("exc-row-(0,1)-V1F-change",
        lambda: _EXC.__setitem__((0, 1), ((), (2,), 4, 1))),
    10: ("exc-row-(1,1)-tailval-1-to-0",
         lambda: _EXC.__setitem__((1, 1), ((1, 3), (2,), 5, 0))),
}


def run_tamper(k):
    if k == 0:
        label = "clean-control"
    else:
        label = TAMPER_SPECS[k][0]
        TAMPER_SPECS[k][1]()
    bad_any = []

    def probe_c1():
        for z in range(0, 31):
            for x in range(1, z + 41):
                for R in range(0, x + z + 31):
                    ho = H_ordered(R, (x, 1, 1), z)
                    c = CAND(z, x, R)
                    if ho != c:
                        bad_any.append(["C1", z, x, R, ho, c])
                        return
        return

    def probe_c4():
        for z in range(4, 46):
            for x in range(1, z - 2):
                for R in range(0, x + z + 31):
                    v = single_token(x + 2, z, R)
                    c = CAND(z, x, R)
                    if c != v:
                        bad_any.append(["C4", z, x, R, v, c])
                        return
        return

    def probe_c5():
        EC = BoundedEngineCanonical()
        for z in range(0, 81):
            for R in range(0, min(z + 40, 90) + 1):
                hc = EC.H(R, (1, 1, 1), z)
                c = CAND(z, 1, R)
                if hc != c:
                    bad_any.append(["C5", z, R, hc, c])
                    EC.clear()
                    return
            EC.clear()
        return

    def probe_c6raw():
        EC = BoundedEngineCanonical()
        for z in range(1, 16):
            for x in range(1, z + 9):
                for R in range(1, x + z + 6):
                    B = EC.H(R - 1, (x, 1), z + 1)
                    opts = {B}
                    opts.add(1 ^ EC.H(R - 1, (x, 1, 1), z - 1))
                    if x >= 2:
                        opts.add(EC.H(R - 1, (x - 1, 1, 1), z))
                    w = mex(opts)
                    if w != CAND(z, x, R):
                        bad_any.append(["C6raw", z, x, R, w])
                        EC.clear()
                        return
            EC.clear()
        return

    def probe_c8r():
        bad, n, firsts, lasts = _c8_draw(0, 8000, ("o", "c13"))
        if bad:
            bad_any.append(["C8r", bad[0]])
        elif firsts != EXPECTED["C8"]["first3"]:
            bad_any.append(["C8r-anchor"])

    if k == 0:
        probe_c1()
        probe_c4()
        probe_c5()
        probe_c6raw()
        probe_c8r()
        if bad_any:
            print("CLEAN CONTROL FAILED (unexpected bad):", bad_any[:5])
            return 3
        print("TAMPER 0: clean control - no bad points (rc=0)")
        return 0
    probe_c1()
    if not bad_any:
        probe_c4()
    if not bad_any:
        probe_c5()
    if not bad_any:
        probe_c6raw()
    if not bad_any:
        probe_c8r()
    if bad_any:
        print("FAIL-CLOSED TAMPER %d DETECTED (%s) by %s" % (k, label, bad_any[0][0]))
        print("first:", bad_any[0])
        return 1
    print("FAIL-OPEN: tamper %d (%s) NOT detected" % (k, label))
    return 2


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    a1 = argv[1]
    if a1 == "t0":
        run_t0()
    elif a1 == "c1":
        run_c1()
    elif a1 == "c2":
        run_c2(int(argv[2]))
    elif a1 == "c3":
        run_c3()
    elif a1 == "c4":
        run_c4(int(argv[2]))
    elif a1 == "c5":
        run_c5()
    elif a1 == "c6fit":
        run_c6fit()
    elif a1 == "c6raw":
        run_c6raw(int(argv[2]))
    elif a1 == "c7":
        run_c7()
    elif a1 == "c7b":
        run_c7b()
    elif a1 == "c8":
        run_c8(int(argv[2]))
    elif a1 == "c9":
        run_c9()
    elif a1 == "c9b":
        run_c9b()
    elif a1 == "audit":
        run_audit()
    elif a1 == "--tamper":
        k = int(argv[2])
        return run_tamper(k)
    else:
        print("unknown command", a1)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
