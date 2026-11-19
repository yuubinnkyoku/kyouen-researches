"""Independent verifier for the two-token boundary slice z=11, y=5 (K1036).

Published claim (universal theorem, proof by x-induction plus complete
A/B/C signature-band table): for H(R;(x,5);11), all x>=5, all R>=0:

  T(x) (value 2):
    x=5:  O[1,9]                          (diagonal x=y row)
    x=6:  O[1,15]                         (h=z row; top 15 = 2y+(d+z)/2 - 1,
                                          d=1, d+z=12 == 0 (mod 4))
    x=7:  O[1,11]
    x=8:  O[1,11] + {17}                  (d=3 lattice point 2y+7)
    x in {9,10,11}: O[1,11]
    x=12: O[1,11] + {19}                  (d=7 lattice point 2y+9)
    x in {13,14,15}: O[1,11]
    x=16: O[1,11] + {21}                  (d=11 lattice = pin 2y+z; pin
                                          appears at row x = pin - y)
    x=17: O[1,11] + O[21,33]              (sweep row x=z+y+1; band O[pin,x+y+z])
    x>=18: O[1,11] + {21}
  P(x) (value 1):
    x=5:  empty
    x=6:  {12,14,16} + I[17,inf)
    x=7:  {12,14,16}
    x=8:  {12,14,16} + I[18,inf)
    x=9:  {12,14,16}
    x=10: {12,14,16} + I[18,inf)
    x=11: {12,14,16,18}
    x=12: {12,14,16,18,20} + I[21,inf)
    x=13: {12,14,16,18}
    x=14: {12,14,16,18} + I[20,inf)
    x=15: {12,14,16,18,20}
    x=16: {12,14,16,18,20} + I[22,inf)
    x=17: {12,14,16,18,20}
    x even >=18: {12,14,16,18,20} + O[23,x+17] + I[x+18,inf)
    x odd  >=19: {12,14,16,18,20} + O[23,x+16]
  everything else value 0; R=0 value 0.
  Height-only: R<=12 implies H = v_single(x+5,11,R) (K0832).
  Tail: R>=x+17 implies H = (x+5) mod 2.

Value-1 base points {12,14,16,18,20} = {z+1,z+3,z+5,z+7,z+9}: fifth
instance of the y-points hypothesis (exactly y points).  Band start
z+2y+2=23, odd band (z parity), sweep row x=z+y+1=17, sweep band
O[21,33]=O[pin,x+y+z], pin=2y+z=21 (odd z ladder O[1,z]).

Audit method: two direct mex recurrences (order-preserving and
descending-multiset canonical) evaluate every child; no published child
closed form is used for the value engine checks.  B/C children are
additionally cross-checked against transcriptions of the published
K1015 (z=11,y=4) and K1007 (z=10,y=5) closed forms.  Coverage of the
band table, exact signature values against the engines, mex against the
closed form, Theorem T parity bound, height-only reduction, tail,
formula-only wide grid, and fixed-seed scatter are all checked.

Deterministic: fixed seeds, no timestamps.  Writes output/audit.json.
Long-running environments can interrupt and resume: progress is
checkpointed in output/state.json after each phase; audit.json is
byte-identical regardless of where execution pauses.
"""

from functools import lru_cache
import hashlib
import json
import random
import sys
import time
from pathlib import Path

sys.setrecursionlimit(300000)

Z = 11
Y = 5
XMIN = 5
TAIL_START = 17        # tail: R >= x+17, H = (x+5) mod 2
HEIGHT_ONLY_MAX = 12   # R <= 12 height-only reduction
SEED_SCATTER = 20261122


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


def _clear_caches():
    H_ordered.cache_clear()
    H_canonical.cache_clear()


def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
    """K0832 single-token closed form."""
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


def _odd_le(R, hi):
    return R % 2 == 1 and 1 <= R <= hi


def in_T(x, R):
    if x == 5:
        return _odd_le(R, 9)
    if x == 6:
        return _odd_le(R, 15)
    if not _odd_le(R, 11):
        if x == 8:
            return R == 17
        if x == 12:
            return R == 19
        if x == 16:
            return R == 21
        if x == 17:
            return 21 <= R <= 33 and R % 2 == 1
        if x >= 18:
            return R == 21
        return False
    return True


# per-row value-1 point sets below the intermediate band, from the
# raw census: base points appear progressively (3 points at x=6..10,
# 4 at x in {11,13}, 5 from x=12 on the even pioneer rows and x>=15).
ROW_P = {
    5: (), 6: (12, 14, 16), 7: (12, 14, 16), 8: (12, 14, 16),
    9: (12, 14, 16), 10: (12, 14, 16), 11: (12, 14, 16, 18),
    12: (12, 14, 16, 18, 20), 13: (12, 14, 16, 18),
    14: (12, 14, 16, 18, 20), 15: (12, 14, 16, 18, 20),
    16: (12, 14, 16, 18, 20), 17: (12, 14, 16, 18, 20),
}
BASE_P = (12, 14, 16, 18, 20)
# pioneer I-bands on rows 6..16 (start value included in ROW_P rows)
PIONEER_LO = {6: 17, 8: 18, 10: 18, 12: 21, 14: 20, 16: 22}


def in_P(x, R):
    if x <= 17:
        if R in ROW_P[x]:
            return True
        if x in PIONEER_LO:
            return R >= PIONEER_LO[x]
        return False
    if R in BASE_P:
        return True
    if x % 2 == 0:
        return (23 <= R <= x + 17 and R % 2 == 1) or R >= x + 18
    return 23 <= R <= x + 16 and R % 2 == 1


def candidate(x, R):
    if R == 0:
        return 0
    if in_T(x, R):
        return 2
    if in_P(x, R):
        return 1
    return 0


def cand_B(x, r):
    """Transcription of the published K1015 (z=11,y=4) closed form.

    Value of H(r;(x,4);11) for x>=4, r>=0, per the K1015 report tables.
    """
    # value-2 sets (T_B)
    if x == 4:
        if _odd_le(r, 7):
            return 2
    elif x in (5, 6):
        if _odd_le(r, 9):
            return 2
    elif x == 7:
        if _odd_le(r, 15):
            return 2
    elif x in (8, 9, 10):
        if _odd_le(r, 11):
            return 2
    elif x == 11:
        if _odd_le(r, 11) or r == 17:
            return 2
    elif x in (12, 13, 14):
        if _odd_le(r, 11):
            return 2
    elif x == 15:
        if _odd_le(r, 11) or r == 19:
            return 2
    elif x == 16:
        if _odd_le(r, 11) or (19 <= r <= 31 and r % 2 == 1):
            return 2
    else:  # x >= 17
        if _odd_le(r, 11) or r == 19:
            return 2
    # value-1 sets (P_B), exactly per the K1015 report table
    if x == 5:
        return 1 if r >= 10 else 0
    if x in (4, 6):
        return 0
    if x == 8:
        return 1 if r in (12, 14) else 0
    if x in (7, 9):
        return 1 if r in (12, 14) or r >= 16 else 0
    if x == 10:
        return 1 if r in (12, 14, 16) else 0
    if x == 11:
        return 1 if r in (12, 14, 16) or r >= 18 else 0
    if x == 12:
        return 1 if r in (12, 14, 16) else 0
    if x == 13:
        return 1 if r in (12, 14, 16) or r >= 18 else 0
    if x in (14, 16):
        return 1 if r in (12, 14, 16, 18) else 0
    if x == 15:
        return 1 if r in (12, 14, 16, 18) or r >= 20 else 0
    if x % 2 == 0:  # x >= 18 even
        return 1 if r in (12, 14, 16, 18) or (21 <= r <= x + 15 and r % 2 == 1) else 0
    # x >= 17 odd
    return 1 if (r in (12, 14, 16, 18) or (21 <= r <= x + 14 and r % 2 == 1)
                 or r >= x + 16) else 0


def cand_C0(x, r):
    """Transcription of the published K1007 (z=10,y=5) closed form.

    Value of H(r;(x,5);10) for x>=5, r>=0, per the K1007 report tables.
    """
    # value-2 sets (T_10^(5))
    if x == 5:
        if _odd_le(r, 15):
            return 2
    elif x in (6, 7, 8, 10, 11, 12, 14, 15):
        if _odd_le(r, 9):
            return 2
    elif x == 9:
        if _odd_le(r, 9) or r == 17:
            return 2
    elif x == 13:
        if _odd_le(r, 9) or r == 19:
            return 2
    elif x == 16:
        if _odd_le(r, 9) or (21 <= r <= 31 and r % 2 == 1):
            return 2
    else:  # x >= 17
        if _odd_le(r, 9) or r == 21:
            return 2
    # value-1 sets (P_10^(5))
    if x == 5:
        return 0
    if x in (7, 9):
        return 1 if r in (11, 13, 15) else 0
    if x in (11, 13):
        return 1 if r in (11, 13, 15, 17) else 0
    if x == 15:
        return 1 if r in (11, 13, 15, 17, 19) else 0
    if x == 6:
        return 1 if r in (11, 13, 15) or r >= 16 else 0
    if x in (8, 10):
        return 1 if r in (11, 13, 15, 17) or r >= 18 else 0
    if x in (12, 14):
        return 1 if r in (11, 13, 15, 17, 19) or r >= 20 else 0
    if x % 2 == 0:  # x >= 16 even
        return 1 if (r in (11, 13, 15, 17, 19)
                     or (22 <= r <= x + 16 and r % 2 == 0)
                     or r >= x + 17) else 0
    # x >= 17 odd
    return 1 if (r in (11, 13, 15, 17, 19)
                 or (22 <= r <= x + 15 and r % 2 == 0)) else 0


def abc_options(x, R):
    """A/B/C child values via the direct ordered-mex engine.

    Published decomposition for the slice (z=11,y=5):
    A = H(R-1;(x-1,5);11) for x>=6,
    B = H(R-1;(x,4);11), C = 1 xor H(R-1;(x,5);10).
    At x=5 the two token-decrement moves merge into the multiset (4,5),
    handled by B.
    """
    r = R - 1
    opts = set()
    opts.add(H_ordered(r, (x, Y - 1), Z))      # B
    if x > Y:
        opts.add(H_ordered(r, (x - 1, Y), Z))  # A
    opts.add(1 ^ H_ordered(r, (x, Y), Z - 1))  # C
    return opts


def child_signature(x, R):
    return "".join(str(v) for v in sorted(abc_options(x, R)))


def cl_signature(x, R):
    """A/B/C child values via the closed forms: A = own slice closed form
    (induction layer), B = K1015 transcription, C = 1 xor K1007
    transcription.  Used for deep-row signature checks where the raw
    engines do not fit in bounded memory; the transcriptions themselves
    are engine-audited in the V7 anchor phases."""
    r = R - 1
    opts = {cand_B(x, r)}
    if x > Y:
        opts.add(candidate(x - 1, r))
    opts.add(1 ^ cand_C0(x, r))
    return "".join(str(v) for v in sorted(opts))


# --- signature band table ---------------------------------------------
# Band entry: (parity, lo, hi, sig) with parity 0=even, 1=odd, 2=both;
# hi None = unbounded.  Bands are disjoint and cover all R >= 1.

def _both(lo, hi, s):
    return (2, lo, hi, s)


def _odd(lo, hi, s):
    return (1, lo, hi, s)


def _even(lo, hi, s):
    return (0, lo, hi, s)


PREFIX_STEADY = [
    _odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
    _odd(13, 19, "1"), _even(14, 18, "0"), _even(20, 20, "02"),
    _odd(21, 21, "01"), _even(22, 22, "123"),
]

STATIC_BANDS = {
    5: [_odd(1, 9, "01"), _even(2, 10, "23"), _even(12, 16, "13"),
        _odd(11, None, "1"), _even(18, None, "1")],
    6: [_odd(1, 15, "01"), _even(2, 10, "23"), _even(12, 16, "0"),
        _both(17, None, "0")],
    7: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 16, "02"),
        _odd(13, None, "1"), _even(18, None, "1")],
    8: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
        _odd(13, 15, "1"), _even(14, 16, "0"), _odd(17, 17, "01"),
        _both(18, None, "0")],
    9: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
        _odd(13, 17, "1"), _even(14, 16, "0"), _even(18, 18, "123"),
        _both(19, None, "1")],
    10: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
         _odd(13, 17, "1"), _even(14, 16, "0"), _both(18, None, "0")],
    11: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
         _odd(13, 19, "1"), _even(14, 16, "0"), _even(18, 18, "02"),
         _both(20, None, "1")],
    12: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
         _odd(13, 17, "1"), _even(14, 20, "0"), _odd(19, 19, "01"),
         _both(21, None, "0")],
    13: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
         _odd(13, 19, "1"), _even(14, 18, "0"), _even(20, 20, "123"),
         _both(21, None, "1")],
    14: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
         _odd(13, 19, "1"), _even(14, 20, "0"), _both(21, None, "0")],
    15: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
         _odd(13, 19, "1"), _even(14, 18, "0"), _even(20, 20, "02"),
         _both(21, None, "1")],
    16: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
         _odd(13, 19, "1"), _even(14, 18, "0"), _even(20, 20, "02"),
         _odd(21, 21, "01"), _even(22, 32, "023"), _odd(23, 33, "0"),
         _both(34, None, "0")],
    17: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
         _odd(13, 19, "1"), _even(14, 18, "0"), _even(20, 20, "02"),
         _odd(21, 21, "01"), _even(22, 22, "123"), _odd(23, 33, "01"),
         _even(24, 34, "1"), _both(35, None, "1")],
    18: [_odd(1, 11, "01"), _even(2, 10, "23"), _even(12, 12, "02"),
         _odd(13, 19, "1"), _even(14, 18, "0"), _even(20, 20, "02"),
         _odd(21, 21, "01"), _even(22, 22, "123"), _odd(23, 35, "0"),
         _even(24, 34, "12"), _both(36, None, "0")],
}


def bands_for(x):
    if x in STATIC_BANDS:
        return STATIC_BANDS[x]
    if x >= 19 and x % 2 == 1:
        return PREFIX_STEADY + [
            _odd(23, x + 16, "0"), _even(24, x + 17, "1"),
            _both(x + 18, None, "1")]
    # x >= 20 even
    return PREFIX_STEADY + [
        _odd(23, x + 17, "0"), _even(24, x + 16, "1"),
        _both(x + 18, None, "0")]


@lru_cache(None)
def _row_bands(x):
    return tuple(bands_for(x))


def band_at(x, R):
    """The unique band covering R in the band table (None if not unique)."""
    hits = [sig for parity, lo, hi, sig in _row_bands(x)
            if (parity == 2 or R % 2 == parity)
            and lo <= R and (hi is None or R <= hi)]
    if len(hits) != 1:
        return None
    return hits[0]


# --- audit phases ------------------------------------------------------

def audit_phases(counts, failures):
    def note(key, inc=1):
        counts[key] = counts.get(key, 0) + inc

    def fail(msg):
        if len(failures) < 25:
            failures.append(msg)

    phases = []

    # V1: two direct recurrences vs the closed form (and each other).
    def v1():
        key = "ordered_and_canonical_direct_vs_formula"
        for x in range(5, 81):
            for R in range(0, x + 41):
                expected = candidate(x, R)
                a = H_ordered(R, (x, Y), Z)
                b = H_canonical(R, (x, Y), Z)
                if a != expected:
                    fail(f"V1 ordered mismatch x={x} R={R}: {a} != {expected}")
                if b != expected:
                    fail(f"V1 canonical mismatch x={x} R={R}: {b} != {expected}")
                if a != b:
                    fail(f"V1 engine disagree x={x} R={R}: {a} != {b}")
                note(key, 3)
            _clear_caches()
    phases.append(("V1_direct_recurrences", v1))

    # V2: band signature values against the A/B/C engine.
    def v2_sig(rows):
        key = "band_signature_vs_abc_engine"
        for x in rows:
            for R in range(1, x + TAIL_START + 1):
                sig = band_at(x, R)
                if sig is None:
                    fail(f"V2 coverage x={x} R={R}: not exactly one band")
                    note(key)
                    continue
                if child_signature(x, R) != sig:
                    fail(f"V2 signature x={x} R={R}: table {sig} != engine")
                note(key)
            _clear_caches()
    phases.append(("V2_signature_rows_x5_150",
                   lambda: v2_sig(range(5, 151))))
    phases.append(("V2_signature_spot_rows",
                   lambda: v2_sig([160, 175])))

    # V2cl: deep-row band signature values via the closed-form child
    # anchors (memory-bounded; engines validate the anchors up to x=45).
    def v2_cl(xlo, xhi):
        key = "band_signature_vs_closed_form_children_grid"
        for x in range(xlo, xhi + 1):
            for R in range(1, x + TAIL_START + 1):
                sig = band_at(x, R)
                if sig is None:
                    fail(f"V2cl coverage x={x} R={R}")
                    note(key)
                    continue
                if cl_signature(x, R) != sig:
                    fail(f"V2cl signature x={x} R={R}: table {sig} != cl "
                         f"{cl_signature(x, R)}")
                note(key)
    phases.append(("V2cl_signature_grid_x5_250", lambda: v2_cl(5, 250)))
    phases.append(("V2cl_signature_grid_x251_700",
                   lambda: v2_cl(251, 700)))

    # V2b: same decomposition with the canonical engine.
    def v2_canonical():
        key = "abc_canonical_engine_agreement"
        for x in range(5, 81):
            for R in range(1, x + TAIL_START + 1):
                r = R - 1
                opts = set()
                opts.add(H_canonical(r, (x, Y - 1), Z))
                if x > Y:
                    opts.add(H_canonical(r, (x - 1, Y), Z))
                opts.add(1 ^ H_canonical(r, (x, Y), Z - 1))
                sig = "".join(str(v) for v in sorted(opts))
                table = band_at(x, R)
                if table is None or sig != table:
                    fail(f"V2b canonical x={x} R={R}: {sig} vs {table}")
                note(key)
            _clear_caches()
    phases.append(("V2b_canonical_agreement", v2_canonical))

    # V2c: band coverage + mex + Theorem T parity bound over a wide grid.
    def v2_cov():
        key = "band_coverage_mex_and_parity_bound_grid"
        for x in range(5, 701):
            for R in range(1, x + TAIL_START + 1):
                sig = band_at(x, R)
                if sig is None:
                    fail(f"V2c coverage x={x} R={R}: not exactly one band")
                    note(key)
                    continue
                m = mex(int(d) for d in sig)
                if m != candidate(x, R):
                    fail(f"V2c mex x={x} R={R}: sig {sig}")
                if R % 2 == 0 and m > 1:
                    fail(f"V2c Theorem T bound x={x} R={R}: {m}")
                if R % 2 == 1 and m > 2:
                    fail(f"V2c Theorem T bound x={x} R={R}: {m}")
                note(key, 2)
    phases.append(("V2c_coverage_grid", v2_cov))

    # V3: height-only reduction R<=12 for all x<=1500, engine spot checks.
    def v3_f():
        key = "height_only_reduction_R_le_12"
        for x in range(5, 1501):
            for R in range(0, HEIGHT_ONLY_MAX + 1):
                if candidate(x, R) != single_token(x + Y, Z, R):
                    fail(f"V3 height-only x={x} R={R}")
                note(key)
    phases.append(("V3_height_only", v3_f))

    def v3_e():
        key = "single_token_vs_engine"
        for x in range(5, 61):
            for R in range(0, HEIGHT_ONLY_MAX + 1):
                st = single_token(x + Y, Z, R)
                if st != H_ordered(R, (x + Y,), Z):
                    fail(f"V3 single-token engine x={x} R={R}: {st}")
                note(key)
            _clear_caches()
    phases.append(("V3_single_token_engine", v3_e))

    # V4: general tail, formula and engine.
    def v4_f():
        key = "general_tail"
        for x in range(5, 6001):
            for R in (x + TAIL_START, x + TAIL_START + 1,
                      x + TAIL_START + 2):
                if candidate(x, R) != (x + Y) % 2:
                    fail(f"V4 tail x={x} R={R}")
                note(key)
    phases.append(("V4_tail_formula", v4_f))

    def v4_e():
        key = "general_tail_vs_engine"
        for x in range(5, 61):
            for R in range(x + TAIL_START, x + TAIL_START + 20):
                if H_ordered(R, (x, Y), Z) != (x + Y) % 2:
                    fail(f"V4 tail engine x={x} R={R}")
                note(key)
            _clear_caches()
    phases.append(("V4_tail_engine", v4_e))

    # V5: wide formula grid: band table vs T/P classifier, x<=3000.
    def v5():
        key = "signature_table_vs_formula_grid"
        for x in range(5, 3001):
            for R in range(1, x + TAIL_START + 1):
                sig = band_at(x, R)
                if sig is None:
                    fail(f"V5 coverage x={x} R={R}")
                    note(key)
                    continue
                if mex(int(d) for d in sig) != candidate(x, R):
                    fail(f"V5 mex x={x} R={R}")
                note(key)
    phases.append(("V5_signature_formula_grid", v5))

    # V6: fixed-seed scatter, ordered engine vs formula.
    def v6(n_points, n_skip):
        key = "fixed_seed_scatter"
        rng = random.Random(SEED_SCATTER)
        for i in range(n_points + n_skip):
            x = rng.randrange(5, 201)
            R = rng.randrange(0, x + 46)
            if i < n_skip:
                continue
            if H_ordered(R, (x, Y), Z) != candidate(x, R):
                fail(f"V6 scatter x={x} R={R}")
            note(key)
            _clear_caches()
    phases.append(("V6_scatter_1", lambda: v6(150, 0)))
    phases.append(("V6_scatter_2", lambda: v6(150, 150)))
    phases.append(("V6_scatter_3", lambda: v6(150, 300)))
    phases.append(("V6_scatter_4", lambda: v6(150, 450)))

    # V7: B/C child anchors vs transcriptions of K1015 / K1007.
    def v7(xlo, xhi):
        keyB = "B_child_anchor_vs_K1015_transcription"
        keyC = "C_child_anchor_vs_K1007_transcription"
        for x in range(xlo, xhi + 1):
            for r in range(0, x + 41):
                bval = H_ordered(r, (x, Y - 1), Z)
                if bval != cand_B(x, r):
                    fail(f"V7 B anchor x={x} r={r}: engine {bval} != K1015 "
                         f"{cand_B(x, r)}")
                note(keyB)
                cval = 1 ^ H_ordered(r, (x, Y), Z - 1)
                if cval != 1 ^ cand_C0(x, r):
                    fail(f"V7 C anchor x={x} r={r}: engine {cval} != 1^K1007 "
                         f"{1 ^ cand_C0(x, r)}")
                note(keyC)
            _clear_caches()
    phases.append(("V7_BC_anchors_x5_25", lambda: v7(5, 25)))
    phases.append(("V7_BC_anchors_x26_45", lambda: v7(26, 45)))

    return phases


def run():
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    state_path = out / "state.json"

    counts = {}
    failures = []
    phase_index = 0
    resumed = False
    if state_path.exists():
        state = json.loads(state_path.read_text(encoding="utf-8"))
        counts = state["counts"]
        failures = state["failures"]
        phase_index = state["phase_index"]
        resumed = True

    phases = audit_phases(counts, failures)
    t0 = time.monotonic()
    while phase_index < len(phases):
        if phase_index > 0 and time.monotonic() - t0 > 130:
            break
        fn = phases[phase_index][1]
        fn()
        phase_index += 1
        state_path.write_text(
            json.dumps({"phase_index": phase_index, "counts": counts,
                        "failures": failures}, sort_keys=True),
            encoding="utf-8")

    if phase_index < len(phases):
        import resource
        print(json.dumps({"resumed": resumed, "incomplete": True,
                          "phase_index": phase_index,
                          "total_phases": len(phases),
                          "max_rss_kb": resource.getrusage(
                              resource.RUSAGE_SELF).ru_maxrss}))
        return {"all_pass": False, "incomplete": True}

    audit = {
        "all_pass": not failures,
        "classification": ("universal theorem: x-induction over the slice "
                           "rows plus complete A/B/C signature band table"),
        "counts": counts,
        "failure_count": len(failures),
        "failures": failures,
        "finite_audit_role": ("transcription/implementation audit of the "
                              "published z=11 y=5 slice closed form, band "
                              "table, and B/C child anchors from K1015 and "
                              "K1007; children evaluated by two direct mex "
                              "recurrences (ordered and multiset canonical), "
                              "not by child closed forms; universality rests "
                              "on the x-induction and band-table proof, not "
                              "on this finite audit"),
        "seeds": {"scatter": SEED_SCATTER},
        "slice": "two-token residual game z=11 y=5, all x>=5, all R>=0 (K1036)",
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    }
    audit["total_checks"] = sum(counts.values())
    body = json.dumps(audit, sort_keys=True, indent=2, ensure_ascii=False)

    stable = dict(audit)
    stable.pop("verifier_sha256", None)
    stable.pop("total_checks", None)
    stable["counts"] = dict(sorted(counts.items()))
    stable_bytes = json.dumps(stable, sort_keys=True, indent=2,
                              ensure_ascii=False)
    audit_stable_sha = hashlib.sha256(stable_bytes.encode("utf-8")).hexdigest()

    result = {
        "all_pass": audit["all_pass"],
        "total_checks": audit["total_checks"],
        "audit_sha256_excluding_self_reference": audit_stable_sha,
        "failure_count": len(failures),
    }
    (out / "audit.json").write_bytes(body.encode("utf-8"))
    state_path.unlink()
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return result


if __name__ == "__main__":
    raise SystemExit(0 if run()["all_pass"] else 1)
