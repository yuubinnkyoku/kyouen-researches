#!/usr/bin/env python3
"""
explore_sixthwave_z35_z39: FROZEN PRE-DECLARATION micro-census executing
the REGISTERED HANDOFFS of the fifth-wave micro-kit log section 5
(commit `c66b9022`, kit strip-fifthwave-z33-z37): item #1 the six
TWO-PAST + NEW-WAVE rows, item #2 the six ONE-PAST ladder rows
(measuring SIX birth+3 deaths, datums 16-21, including the DEFERRED
(14,20) death at z=35), item #3 the m=18/m=17 base-spot z=32 touch,
item #4 the k=43/k=44 tail supply pre-computations. NO K slot is
claimed by this file; the constants below were frozen into this
docstring BEFORE the first run of this file, and the file has not
been edited after any of its runs.

SLOT CHECK (performed at kit-build time): latest main head `c66b9022`
(the fifth-wave kit publication itself; no other fast-lane or heavy
lane commit overlaps any position here). No published engine value
exists for any position measured here (the fifth-wave kit published
m=13 at z<=34, m=14 at z<=34, m=15 at z<=36, m=16 at z<=37, m=17 at
z<=36, m=18 at z<=37, and the four z=31 touches; rows below are m=13
at z=35/36, m=14 at z=35/36, m=15 at z=37/38, m=16 at z=38/39, m=17
at z=37/38, m=18 at z=38/39, and the four z=32 touch spots — all
beyond every published value). Every position below is touched by the
engine for the FIRST time at the frozen first run of this file,
except the 22 recheck anchors of section (E). All constants were
re-derived from the PUBLISHED K0832 closed form (pin `bd5f22e4`) under
the published row convention R = m+z+1 BEFORE the freeze; NO engine
recursion ran on any new position before the freeze.

REGISTERED PREDICTIONS, frozen before the first run (x0 style,
R = m+z+1, parts >= m, co-token allowed, arity <= 3, S in {m..m+38};
derived shape counts m=13: 76, m=14: 62, m=15: 50, m=16: 40,
m=17: 32, m=18: 26):

(A) TWO-PAST + NEW-WAVE rows (registered item #1, predicted EXACTLY
    TWO separations each = the previous birth stuck + the newborn):
    (A1) m=13 @ z=35 (ten past, ODD): {13,22}@S=35 DOWN 1v2 (stick 1
         vs collapse v(35,35,49)=2) + new birth {13,24}@S=37 UP 2v0
         (collapse v(37,35,49)=0) — the d=5 (sixth-wave) seat, gap 11.
         Older shapes conform-dead: {13,20} v(33,35,49)=1, {13,18}
         v(31,35,49)=1, {13,16} v(29,35,49)=1, {13,14} v(27,35,49)=1.
    (A2) m=15 @ z=37 (eight past, ODD): {15,22}@S=37 DOWN 1v2 (stick 1
         vs collapse v(37,37,53)=2) + new birth {15,24}@S=39 UP 2v0
         (collapse v(39,37,53)=0) — the d=4 seat, gap 9. Older:
         {15,20} v(35,37,53)=1, {15,18} v(33,37,53)=1, {15,16}
         v(31,37,53)=1.
    (A3) m=14 @ z=36 (ten past, EVEN): (14,22)@S=36 DOWN 0v2 (stick 0
         vs collapse v(36,36,51)=2) + new birth (14,24)@S=38 UP 2v1
         (collapse v(38,36,51)=1) — the d=5 seat, gap 10. Older:
         (14,20) v(34,36,51)=0, (14,18) v(32,36,51)=0, (14,16)
         v(30,36,51)=0, (14,14) v(28,36,51)=0.
    (A4) m=16 @ z=38 (eight past, EVEN): (16,22)@S=38 DOWN 0v2 (stick 0
         vs collapse v(38,38,55)=2) + new birth (16,24)@S=40 UP 2v1
         (collapse v(40,38,55)=1) — the d=4 seat, gap 8. Older:
         (16,20) v(36,38,55)=0, (16,18) v(34,38,55)=0, (16,16)
         v(32,38,55)=0.
    (A5) m=17 @ z=37 (four past, ODD): {17,20}@S=37 DOWN 1v2 (stick 1
         vs collapse v(37,37,55)=2) + new birth {17,22}@S=39 UP 2v0
         (collapse v(39,37,55)=0) — the d=2 seat, gap 5 ({17,22} =
         17+2d+1 with d=2). Older: {17,18} v(35,37,55)=1.
    (A6) m=18 @ z=38 (four past, EVEN): (18,20)@S=38 DOWN 0v2 (stick 0
         vs collapse v(38,38,57)=2) + new birth (18,22)@S=40 UP 2v1
         (collapse v(40,38,57)=1) — the d=2 seat, gap 4 ((18,22) =
         18+2d with d=2). Older: (18,18) v(36,38,57)=0.
(B) ONE-PAST ladder rows (registered item #2, predicted EXACTLY ONE
    separation each = the newest birth in decay); these rows also
    measure SIX birth+3 DEATHS in one kit (datums 16-21, taking the
    death curve from 15/15 to 21/21 across ALL SIX bands m in
    {13..18}, shapes d in {0..4}):
    (B1) m=13 @ z=36: {13,24}@S=37 UP 1v0 (collapse v(37,36,50)=0);
         {13,22} conform-DEAD at birth+3 (collapse v(35,36,50)=1;
         born z=33) — death datum 16, the FIRST d=4-shape death.
    (B2) m=14 @ z=35 (odd offset 9 = NO birth slice): (14,22)@S=36
         DOWN 0v1 (collapse v(36,35,50)=1); (14,20) conform-DEAD at
         birth+3 (collapse v(34,35,50)=0; born z=32) — death datum 17,
         the DEFERRED (14,20) death noted in the fifth-wave log S3.
    (B3) m=15 @ z=38: {15,24}@S=39 UP 1v0 (collapse v(39,38,54)=0);
         {15,22} conform-DEAD at birth+3 (collapse v(37,38,54)=1;
         born z=35) — death datum 18.
    (B4) m=16 @ z=39: (16,24)@S=40 DOWN 0v1 (collapse v(40,39,56)=1);
         (16,22) conform-DEAD at birth+3 (collapse v(38,39,56)=0;
         born z=36) — death datum 19.
    (B5) m=17 @ z=38: {17,22}@S=39 UP 1v0 (collapse v(39,38,56)=0);
         {17,20} conform-DEAD at birth+3 (collapse v(37,38,56)=1;
         born z=35) — death datum 20.
    (B6) m=18 @ z=39: (18,22)@S=40 DOWN 0v1 (collapse v(40,39,58)=1);
         (18,20) conform-DEAD at birth+3 (collapse v(38,39,58)=0;
         born z=36) — death datum 21.
(C) BASE-SPOT z=32 TOUCH (four FIRST-EVER z=32 engine touches, option
    tables frozen BEFORE the run; C-child inputs PUBLISHED by the
    fifth-wave kit as x3/x4):
      (C1) x1 = H(50;{17,18};32) [m=17-row z=32 first co-token, R=50,
           BLIND]: candidate collapse-CONFORM 0 (= v(35,32,50)=0).
      (C2) y1 = H(49;{16,17};32) [m=16-row z=32 first co-token, R=49,
           BLIND]: candidate collapse-CONFORM 1 (= v(33,32,49)=1).
      (C3) x3 = H(51;(18,18);32) [m=18 base-spot on-line, R=51]:
           frozen table {B-child = x1 (in-kit premise disclosed),
           C-child 1^H(51;(18,18);31) = 1^1 = 0 PUBLISHED (fifth-wave
           kit x3)} -> candidate mex{x1,0} = 1 = v(36,32,51)=1
           CONFORMING iff x1 conforms 0 (would extend the m=18
           z-sequence to 17 members).
      (C4) x4 = H(50;(17,17);32) [m=17 base-spot on-line, R=50]:
           frozen table {B-child = y1 (in-kit premise disclosed),
           C-child 1^H(50;(17,17);31) = 1^0 = 1 PUBLISHED (fifth-wave
           kit x4)} -> candidate mex{y1,1} = 0 = v(34,32,50)=0
           CONFORMING iff y1 conforms 1.
(D) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed form,
    NO engine recursion), FROZEN AS REGISTERED in the fifth-wave log
    S5 item #4 (scan domain ends at s=k+34):
      (D1) k=43 THIRTY-FOURTH tail (ODD form, odd-z supply chain
           candidate 13/13): v(s,44,44) =? v(s,43,44) over s in
           {0} U {12..77}: hold {0} U {12..43}, then UNIFORM 0v1 for
           ALL s in {44..77}.
      (D2) k=44 THIRTY-FIFTH tail (EVEN form, even-z supply chain
           candidate 13/13): v(s,45,45) =? v(s,44,45) over s in
           {0} U {12..78}: hold {0} U {12..43}, break 0v2 at s=44,
           then UNIFORM 2v1 for ALL s in {45..78}.
(E) RECHECK ANCHORS (published engine values only): the four z=31
    fifth-wave touches x1..x4 (0,1,1,0) and the EIGHTEEN published
    fifth-wave row separation values (12 two-past-row + 6 one-past-row
    separations). The `match` field is the collapse-CONFORM criterion,
    False BY DESIGN for separation anchors; the operative criterion is
    value_matches_published.
(F) K0832 battery: every single-token literal used by this file,
    checked closed form vs canonical engine vs ordered engine.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_sixthwave_z35_z39.out).
FINITE observations only; no universal statement; NO K slot
claimed; 11x11 empty board and all standard roots UNKNOWN,
unchanged; no verdict consumed.
"""

import hashlib, json, sys
from functools import lru_cache

ENGINE_BLOCK = '''def mex(values):
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
'''

PIN = 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
sha = hashlib.sha256(ENGINE_BLOCK.encode('utf-8')).hexdigest()
assert sha == PIN, sha
ns = {'lru_cache': lru_cache}
exec(ENGINE_BLOCK, ns)
H = ns['H_canonical']
v = ns['single_token']

ORDINAL = {43: 'thirtyfourth', 44: 'thirtyfifth'}

def parts(s, lo, arity):
    """all multisets (nondecreasing tuples) of tokens >= lo, sum s, 1..arity tokens"""
    out = []

    def rec(rem, k, cur):
        if rem == 0:
            if 1 <= len(cur) <= arity:
                out.append(tuple(cur))
            return
        if k == arity:
            return
        for t in range(lo, rem + 1):
            if cur and t < cur[-1]:
                continue
            cur.append(t)
            rec(rem - t, k + 1, cur)
            cur.pop()

    rec(s, 0, [])
    return out


def row_record_x0(sec, rlabel, extra, R, z, m, smin, smax):
    """published residual-band record style: X = parts(S, m, 3) with
    X[0] == m, i.e. all parts >= m with co-token m allowed, arity <= 3
    TOTAL. Shape-for-shape comparable with the published entries."""
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return {'section': sec, 'label': rlabel, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    vC = ns['vC']
    vO = ns['vO']
    # (I) K0832 battery: every single-token literal used by this file.
    battery_lits = []
    # row-shape collapses: alive separations (A)(B)
    for (x, z2, R2) in [(35, 35, 49), (37, 35, 49), (37, 37, 53),
                        (39, 37, 53), (36, 36, 51), (38, 36, 51),
                        (38, 38, 55), (40, 38, 55), (37, 37, 55),
                        (39, 37, 55), (38, 38, 57), (40, 38, 57),
                        (37, 36, 50), (36, 35, 50), (39, 38, 54),
                        (40, 39, 56), (39, 38, 56), (40, 39, 58)]:
        battery_lits.append((x, z2, R2))
    # row-shape collapses: death/conform (dead shapes)
    for (x, z2, R2) in [(33, 35, 49), (31, 35, 49), (29, 35, 49),
                        (27, 35, 49), (35, 37, 53), (33, 37, 53),
                        (31, 37, 53), (34, 36, 51), (32, 36, 51),
                        (30, 36, 51), (28, 36, 51), (36, 38, 55),
                        (34, 38, 55), (32, 38, 55), (35, 37, 55),
                        (36, 38, 57), (35, 36, 50), (34, 35, 50),
                        (37, 38, 54), (38, 39, 56), (37, 38, 56),
                        (38, 39, 58)]:
        battery_lits.append((x, z2, R2))
    # z=32 spot collapses
    for (x, z2, R2) in [(35, 32, 50), (33, 32, 49), (36, 32, 51),
                        (34, 32, 50)]:
        battery_lits.append((x, z2, R2))
    # fifthwave kit published separation collapse constants
    for (x, z2, R2) in [(35, 35, 53), (37, 35, 53), (36, 36, 55),
                        (38, 36, 55), (33, 33, 47), (35, 33, 47),
                        (34, 34, 49), (36, 34, 49), (35, 35, 51),
                        (37, 35, 51), (36, 36, 53), (38, 36, 53),
                        (35, 34, 48), (34, 33, 48), (37, 36, 52),
                        (38, 37, 54), (37, 36, 54), (38, 37, 56)]:
        battery_lits.append((x, z2, R2))
    # z=31 published touch anchor collapses
    for (x, z2, R2) in [(35, 31, 49), (33, 31, 48), (36, 31, 50),
                        (34, 31, 49)]:
        battery_lits.append((x, z2, R2))
    # supply identity sample points (k=43 odd form, k=44 even form)
    for (x, z2, R2) in [(12, 44, 44), (43, 44, 44), (44, 44, 44),
                        (44, 43, 44), (77, 44, 44), (77, 43, 44),
                        (12, 45, 45), (44, 45, 45), (45, 45, 45),
                        (45, 44, 45), (78, 45, 45), (78, 44, 45)]:
        battery_lits.append((x, z2, R2))
    battery_lits = list(dict.fromkeys(battery_lits))
    battery = []
    bad_bat = 0
    for (x, z2, R2) in battery_lits:
        cf = v(x, z2, R2)
        cn = vC(x, z2, R2)
        od = vO(x, z2, R2)
        ok = (cf == cn == od)
        if not ok:
            bad_bat += 1
        battery.append({'x': x, 'z': z2, 'R': R2, 'closed': cf,
                        'vC': cn, 'vO': od, 'match': ok})
    out.append({'section': 'k0832_battery', 'literals': len(battery),
                'all_match': bad_bat == 0, 'bad': bad_bat,
                'rows': battery})
    # (A) two-past + new-wave rows (fifthwave log S5 item #1)
    out.append(row_record_x0(
        'twopast_m13_z35_row_record',
        'two_past_m13_z35_PREDECLARED_sixth_wave_d5_seat',
        {'co_token_13_allowed': True,
         'law_candidate': 'registered item #1 (fifthwave log S5, commit c66b9022); prediction frozen BEFORE the run: EXACTLY TWO separations: {13,22}@S=35 DOWN 1v2 (two-past stick 1 vs collapse v(35,35,49)=2) + NEW birth {13,24}@S=37 UP 2v0 (collapse v(37,35,49)=0), the d=5 (sixth-wave) seat gap 11; {13,20}/{13,18}/{13,16}/{13,14} conform-dead (collapses v(33,35,49)=1 / v(31,35,49)=1 / v(29,35,49)=1 / v(27,35,49)=1); all other 74 shapes conform; recorded verbatim whatever it is',
         's_domain': '{13..51}', 'arity_max': 3,
         'derived_shape_count': 76,
         'style': 'x0 published residual-band style'},
        49, 35, 13, 13, 51))
    out.append(row_record_x0(
        'twopast_m15_z37_row_record',
        'two_past_m15_z37_PREDECLARED_fourth_wave_d4_seat',
        {'co_token_15_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: {15,22}@S=37 DOWN 1v2 (two-past stick 1 vs collapse v(37,37,53)=2) + NEW birth {15,24}@S=39 UP 2v0 (collapse v(39,37,53)=0), the d=4 seat gap 9; {15,20}/{15,18}/{15,16} conform-dead (collapses v(35,37,53)=1 / v(33,37,53)=1 / v(31,37,53)=1); all other 48 shapes conform; recorded verbatim whatever it is',
         's_domain': '{15..53}', 'arity_max': 3,
         'derived_shape_count': 50,
         'style': 'x0 published residual-band style'},
        53, 37, 15, 15, 53))
    out.append(row_record_x0(
        'twopast_m14_z36_row_record',
        'two_past_m14_z36_PREDECLARED_sixth_wave_d5_seat',
        {'co_token_14_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: (14,22)@S=36 DOWN 0v2 (two-past stick 0 vs collapse v(36,36,51)=2) + NEW birth (14,24)@S=38 UP 2v1 (collapse v(38,36,51)=1), the d=5 seat gap 10; (14,20)/(14,18)/(14,16)/(14,14) conform-dead (collapses v(34,36,51)=0 / v(32,36,51)=0 / v(30,36,51)=0 / v(28,36,51)=0); all other 60 shapes conform; recorded verbatim whatever it is',
         's_domain': '{14..52}', 'arity_max': 3,
         'derived_shape_count': 62,
         'style': 'x0 published residual-band style'},
        51, 36, 14, 14, 52))
    out.append(row_record_x0(
        'twopast_m16_z38_row_record',
        'two_past_m16_z38_PREDECLARED_fourth_wave_d4_seat',
        {'co_token_16_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: (16,22)@S=38 DOWN 0v2 (two-past stick 0 vs collapse v(38,38,55)=2) + NEW birth (16,24)@S=40 UP 2v1 (collapse v(40,38,55)=1), the d=4 seat gap 8; (16,20)/(16,18)/(16,16) conform-dead (collapses v(36,38,55)=0 / v(34,38,55)=0 / v(32,38,55)=0); all other 38 shapes conform; recorded verbatim whatever it is',
         's_domain': '{16..54}', 'arity_max': 3,
         'derived_shape_count': 40,
         'style': 'x0 published residual-band style'},
        55, 38, 16, 16, 54))
    out.append(row_record_x0(
        'twopast_m17_z37_row_record',
        'two_past_m17_z37_PREDECLARED_third_wave_d2_seat',
        {'co_token_17_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: {17,20}@S=37 DOWN 1v2 (two-past stick 1 vs collapse v(37,37,55)=2) + NEW birth {17,22}@S=39 UP 2v0 (collapse v(39,37,55)=0), the d=2 seat gap 5 ({17,22} = 17+2d+1 with d=2); {17,18} conform-dead (collapse v(35,37,55)=1); all other 30 shapes conform; recorded verbatim whatever it is',
         's_domain': '{17..55}', 'arity_max': 3,
         'derived_shape_count': 32,
         'style': 'x0 published residual-band style'},
        55, 37, 17, 17, 55))
    out.append(row_record_x0(
        'twopast_m18_z38_row_record',
        'two_past_m18_z38_PREDECLARED_third_wave_d2_seat',
        {'co_token_18_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: (18,20)@S=38 DOWN 0v2 (two-past stick 0 vs collapse v(38,38,57)=2) + NEW birth (18,22)@S=40 UP 2v1 (collapse v(40,38,57)=1), the d=2 seat gap 4 ((18,22) = 18+2d with d=2); (18,18) conform-dead (collapse v(36,38,57)=0); all other 24 shapes conform; recorded verbatim whatever it is',
         's_domain': '{18..56}', 'arity_max': 3,
         'derived_shape_count': 26,
         'style': 'x0 published residual-band style'},
        57, 38, 18, 18, 56))
    # (B) one-past ladder rows (fifthwave log S5 item #2); each also
    #     measures a birth+3 death (datums 16-21)
    out.append(row_record_x0(
        'onepast_m13_z36_row_record',
        'one_past_m13_z36_PREDECLARED_death_of_13_22',
        {'co_token_13_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation {13,24}@S=37 UP 1v0 (born z=35, odd one-past decay 2->1, collapse v(37,36,50)=0); {13,22} conform-DEAD at its birth+3 slice (collapsed to 1 = collapse v(35,36,50)=1; born z=33), death datum 16, the FIRST d=4-shape death; all other 75 shapes conform; recorded verbatim whatever it is',
         's_domain': '{13..51}', 'arity_max': 3,
         'derived_shape_count': 76,
         'style': 'x0 published residual-band style'},
        50, 36, 13, 13, 51))
    out.append(row_record_x0(
        'onepast_m14_z35_row_record',
        'one_past_m14_z35_PREDECLARED_death_of_14_20_deferred_datum',
        {'co_token_14_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation (14,22)@S=36 DOWN 0v1 (born z=34, even one-past decay 2->0, collapse v(36,35,50)=1); (14,20) conform-DEAD at its birth+3 slice (collapse v(34,35,50)=0; born z=32), death datum 17 — the DEFERRED (14,20) death noted in the fifthwave log S3; NOTE z=35 is an odd-offset slice for m=14 (z-z*=9), so NO birth and exactly this one separation; (14,18)/(14,16)/(14,14) conform-dead; all other 61 shapes conform; recorded verbatim whatever it is',
         's_domain': '{14..52}', 'arity_max': 3,
         'derived_shape_count': 62,
         'style': 'x0 published residual-band style'},
        50, 35, 14, 14, 52))
    out.append(row_record_x0(
        'onepast_m15_z38_row_record',
        'one_past_m15_z38_PREDECLARED_death_of_15_22',
        {'co_token_15_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation {15,24}@S=39 UP 1v0 (born z=37, odd one-past decay 2->1, collapse v(39,38,54)=0); {15,22} conform-DEAD at its birth+3 slice (collapse v(37,38,54)=1; born z=35), death datum 18; all other 49 shapes conform; recorded verbatim whatever it is',
         's_domain': '{15..53}', 'arity_max': 3,
         'derived_shape_count': 50,
         'style': 'x0 published residual-band style'},
        54, 38, 15, 15, 53))
    out.append(row_record_x0(
        'onepast_m16_z39_row_record',
        'one_past_m16_z39_PREDECLARED_death_of_16_22',
        {'co_token_16_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation (16,24)@S=40 DOWN 0v1 (born z=38, even one-past decay 2->0, collapse v(40,39,56)=1); (16,22) conform-DEAD at its birth+3 slice (collapse v(38,39,56)=0; born z=36), death datum 19; all other 39 shapes conform; recorded verbatim whatever it is',
         's_domain': '{16..54}', 'arity_max': 3,
         'derived_shape_count': 40,
         'style': 'x0 published residual-band style'},
        56, 39, 16, 16, 54))
    out.append(row_record_x0(
        'onepast_m17_z38_row_record',
        'one_past_m17_z38_PREDECLARED_death_of_17_20',
        {'co_token_17_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation {17,22}@S=39 UP 1v0 (born z=37, odd one-past decay 2->1, collapse v(39,38,56)=0); {17,20} conform-DEAD at its birth+3 slice (collapse v(37,38,56)=1; born z=35), death datum 20; all other 31 shapes conform; recorded verbatim whatever it is',
         's_domain': '{17..55}', 'arity_max': 3,
         'derived_shape_count': 32,
         'style': 'x0 published residual-band style'},
        56, 38, 17, 17, 55))
    out.append(row_record_x0(
        'onepast_m18_z39_row_record',
        'one_past_m18_z39_PREDECLARED_death_of_18_20',
        {'co_token_18_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation (18,22)@S=40 DOWN 0v1 (born z=38, even one-past decay 2->0, collapse v(40,39,58)=1); (18,20) conform-DEAD at its birth+3 slice (collapse v(38,39,58)=0; born z=36), death datum 21 — sixth-wave death coverage: the curve would reach 21/21 across ALL SIX bands; all other 25 shapes conform; recorded verbatim whatever it is',
         's_domain': '{18..56}', 'arity_max': 3,
         'derived_shape_count': 26,
         'style': 'x0 published residual-band style'},
        58, 39, 18, 18, 56))
    # (C) m=18/m=17 base-spot z=32 touch
    x1 = H(50, tuple(sorted((17, 18), reverse=True)), 32)
    y1 = H(49, tuple(sorted((16, 17), reverse=True)), 32)
    x3 = H(51, (18, 18), 32)
    x4 = H(50, (17, 17), 32)
    out.append({'section': 'z32_basespot_touch',
                'label': 'fifthwave_log_S5_item3_registered_blind_option_tables_first_ever_z32_engine_touches',
                'spots': [
                    {'id': 'x1', 'X': [17, 18], 'R': 50, 'z': 32,
                     'value': x1, 'collapse': v(35, 32, 50),
                     'role': 'm=17-row z=32 first co-token member; BLIND candidate collapse-conform 0 = v(35,32,50)',
                     'match': x1 == v(35, 32, 50)},
                    {'id': 'y1', 'X': [16, 17], 'R': 49, 'z': 32,
                     'value': y1, 'collapse': v(33, 32, 49),
                     'role': 'm=16-row z=32 first co-token member; BLIND candidate collapse-conform 1 = v(33,32,49)',
                     'match': y1 == v(33, 32, 49)},
                    {'id': 'x3', 'X': [18, 18], 'R': 51, 'z': 32,
                     'value': x3, 'collapse': v(36, 32, 51),
                     'role': 'm=18 base-spot on-line member; frozen option table {B-child = x1 (in-kit first-contact premise disclosed), C-child 1^H(51;(18,18);31)=1^1=0 PUBLISHED fifthwave-kit x3}; candidate mex{x1,0}=1 = collapse v(36,32,51) CONFORMING iff x1 conforms 0 (would extend the m=18 z-sequence to 17 members)',
                     'match': x3 == v(36, 32, 51)},
                    {'id': 'x4', 'X': [17, 17], 'R': 50, 'z': 32,
                     'value': x4, 'collapse': v(34, 32, 50),
                     'role': 'm=17 base-spot on-line member; frozen option table {B-child = y1 (in-kit premise disclosed), C-child 1^H(50;(17,17);31)=1^0=1 PUBLISHED fifthwave-kit x4}; candidate mex{y1,1}=0 = collapse v(34,32,50) CONFORMING iff y1 conforms 1',
                     'match': x4 == v(34, 32, 50)}],
                'published_anchor': 'm=18 base-spot on-line z-sequence published z in {16..31} = 0,1,0,1,0,1,0,1,1,1,1,1,1,1,1,1 (16 members incl. x3 by the fifth-wave kit); m=17 members published all zero through z=31 (incl. x4); on conform the z=32 members are x3 (m=18, 17th member) and x4 (m=17)'})
    # (E) recheck anchors — published engine values only
    rechecks = []
    for (R, X, z2, expected) in [
            (53, (17, 18), 35, 1), (53, (17, 20), 35, 2),
            (55, (18, 18), 36, 0), (55, (18, 20), 36, 2),
            (47, (13, 20), 33, 1), (47, (13, 22), 33, 2),
            (49, (14, 20), 34, 0), (49, (14, 22), 34, 2),
            (51, (15, 20), 35, 1), (51, (15, 22), 35, 2),
            (53, (16, 20), 36, 0), (53, (16, 22), 36, 2),
            (48, (13, 22), 34, 1), (48, (14, 20), 33, 0),
            (52, (15, 22), 36, 1), (54, (16, 22), 37, 0),
            (54, (17, 20), 36, 1), (56, (18, 20), 37, 0),
            (49, (17, 18), 31, 0), (48, (16, 17), 31, 1),
            (50, (18, 18), 31, 1), (49, (17, 17), 31, 0)]:
        XX = tuple(sorted(X, reverse=True))
        hv = H(R, XX, z2)
        S = sum(X)
        ev = v(S, z2, R)
        rechecks.append({'R': R, 'X': list(XX), 'z': z2,
                         'value': hv, 'collapse': ev,
                         'published_value': expected,
                         'value_matches_published': hv == expected,
                         'match': hv == ev == expected})
    out.append({'section': 'published_recheck_anchors',
                'match_field_note': 'match is the collapse-CONFORM criterion; for the 18 published separation anchors it is False BY DESIGN (the engine value deviates from the collapse); the operative recheck criterion is value_matches_published; for the 4 touch anchors x1..x4 conform holds and match is True as published',
                'rows': rechecks})
    # (D) tail supply pre-computations (pure closed form, engine-free)
    for k in (43, 44):
        dom = [0] + list(range(12, k + 35))
        if k == 43:
            secname = 'thirtyfourth_tail_supply_identity_precalc'
            lab = ('registered_candidate_odd_form_13of13_fifthwave_log_S5_item4')
            note = ('REGISTERED (fifthwave log S5 item #4): hold {0} U {12..43}, then UNIFORM 0v1 for ALL s in {44..77}; odd-z supply chain candidate 13/13; the z=43-slice supply datum precomputed for the future z=43 declaration lane')
        else:
            secname = 'thirtyfifth_tail_supply_identity_precalc'
            lab = ('registered_candidate_even_form_13of13_fifthwave_log_S5_item4')
            note = ('REGISTERED (fifthwave log S5 item #4): hold {0} U {12..43}, break 0v2 at s=44, then UNIFORM 2v1 for ALL s in {45..78}; even-z supply chain candidate 13/13; the z=44-slice supply datum precomputed for the future z=44 declaration lane')
        holds = []
        breaks = []
        for s in dom:
            a = v(s, k + 1, k + 1)
            b = v(s, k, k + 1)
            row = {'s': s, f'v_{k+1}_{k+1}': a, f'v_{k}_{k+1}': b,
                   'equal': a == b}
            (holds if a == b else breaks).append(row)
        out.append({'section': secname,
                    'label': lab,
                    'k': k, 'ordinal': ORDINAL[k],
                    'identity': f'v(s,{k+1},{k+1}) =? v(s,{k},{k+1})',
                    's_domain': '{0} U {%d..%d}' % (12, dom[-1]),
                    'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                    'published_anchor': note,
                    'hold_rows': holds, 'break_rows': breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
