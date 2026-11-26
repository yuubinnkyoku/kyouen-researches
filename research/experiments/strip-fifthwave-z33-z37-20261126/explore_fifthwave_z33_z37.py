#!/usr/bin/env python3
"""
explore_fifthwave_z33_z37: FROZEN PRE-DECLARATION micro-census executing
the REGISTERED HANDOFFS of the wave-train micro-kit log section 5
(commit `69c4009a`, the tail-range-corrected version; kit
strip-wavetrain-z31-z35): item #1 the six TWO-PAST + NEW-WAVE rows,
item #2 the six ONE-PAST ladder rows, item #3 the m=18/m=17 base-spot
z=31 touch, item #4 the k=41/k=42 tail supply pre-computations. NO
K slot is claimed by this file; the constants below were frozen into
this docstring BEFORE the first run of this file, and the file has not
been edited after any of its runs.

SLOT CHECK (performed at kit-build time): latest main head `69c4009a`
(the wave-train kit's tail-range typo correction itself; the n11 heavy
lane heads `575a58fe`..`730bb3f6` do not overlap any position here).
No published engine value exists for any position measured here (the
wave-train kit published the m=13 row at z=25..32, m=14 at z=26..32,
m=15 at z=29..34, m=16 at z=30..35, m=17 at z=33/34, m=18 at
z=34/35, and the four z=30 touches; rows below are m=13 at z=33/34,
m=14 at z=33/34, m=15 at z=35/36, m=16 at z=36/37, m=17 at z=35/36,
m=18 at z=36/37, and the four z=31 touch spots — all beyond every
published value). Every position below is touched by the engine for
the FIRST time at the frozen first run of this file, except the 18
recheck anchors of section (E). All constants were re-derived from
the PUBLISHED K0832 closed form (pin `bd5f22e4`) under the published
row convention R = m+z+1 BEFORE the freeze; NO engine recursion ran
on any new position before the freeze.

REGISTERED PREDICTIONS, frozen before the first run (x0 style,
R = m+z+1, parts >= m, co-token allowed, arity <= 3, S in {m..m+38};
derived shape counts m=13: 76, m=14: 62, m=15: 50, m=16: 40,
m=17: 32, m=18: 26):

(A) TWO-PAST + NEW-WAVE rows (registered item #1, predicted EXACTLY
    TWO separations each = the previous birth stuck + the newborn):
    (A1) m=17 @ z=35 (two past, ODD): {17,18}@S=35 DOWN 1v2 (stick 1
         vs collapse v(35,35,53)=2) + new birth {17,20}@S=37 UP 2v0
         (collapse v(37,35,53)=0) — the FIRST m=17 second birth, gap-3
         rule datum.
    (A2) m=18 @ z=36 (two past, EVEN): (18,18)@S=36 DOWN 0v2 (stick 0
         vs collapse v(36,36,55)=2) + new birth (18,20)@S=38 UP 2v1
         (collapse v(38,36,55)=1) — the FIRST m=18 second birth, gap-2
         rule datum.
    (A3) m=13 @ z=33 (eight past, ODD): {13,20}@S=33 DOWN 1v2 (stick
         1 vs collapse v(33,33,47)=2) + new birth {13,22}@S=35 UP 2v0
         (collapse v(35,33,47)=0) — the d=3 (fourth-wave) seat, gap 7.
    (A4) m=14 @ z=34 (eight past, EVEN): (14,20)@S=34 DOWN 0v2
         (stick 0 vs collapse v(34,34,49)=2) + new birth (14,22)@S=36
         UP 2v1 (collapse v(36,34,49)=1) — the d=3 seat, gap 6.
    (A5) m=15 @ z=35 (six past, ODD): {15,20}@S=35 DOWN 1v2 (stick 1
         vs collapse v(35,35,51)=2) + new birth {15,22}@S=37 UP 2v0
         (collapse v(37,35,51)=0) — the d=2 seat, gap 5.
    (A6) m=16 @ z=36 (six past, EVEN): (16,20)@S=36 DOWN 0v2 (stick 0
         vs collapse v(36,36,53)=2) + new birth (16,22)@S=38 UP 2v1
         (collapse v(38,36,53)=1) — the d=2 seat, gap 4.
(B) ONE-PAST ladder rows (registered item #2, predicted EXACTLY ONE
    separation each = the newest birth in decay): these rows also
    measure SIX birth+3 DEATHS in one kit (streak: death curve would
    go from 9/9 to 15/15 across ALL SIX bands m in {13..18}):
    (B1) m=13 @ z=34: {13,22}@S=35 UP 1v0 (collapse v(35,34,48)=0);
         {13,20} conform-DEAD at birth+3 (collapse v(33,34,48)=1).
    (B2) m=14 @ z=33: (14,20)@S=34 DOWN 0v1 (collapse
         v(34,33,48)=1); (14,18) conform-DEAD at birth+3 (collapse
         v(32,33,48)=0).
    (B3) m=15 @ z=36: {15,22}@S=37 UP 1v0 (collapse v(37,36,52)=0);
         {15,20} conform-DEAD at birth+3 (collapse v(35,36,52)=1).
    (B4) m=16 @ z=37: (16,22)@S=38 DOWN 0v1 (collapse
         v(38,37,54)=1); (16,20) conform-DEAD at birth+3 (collapse
         v(36,37,54)=0).
    (B5) m=17 @ z=36: {17,20}@S=37 UP 1v0 (collapse v(37,36,54)=0);
         {17,18} conform-DEAD at birth+3 (collapse v(35,36,54)=1) —
         the FIRST m=17 death.
    (B6) m=18 @ z=37: (18,20)@S=38 DOWN 0v1 (collapse
         v(38,37,56)=1); (18,18) conform-DEAD at birth+3 (collapse
         v(36,37,56)=0) — the FIRST m=18 death.
(C) BASE-SPOT z=31 TOUCH (four FIRST-EVER z=31 engine touches, option
    tables frozen BEFORE the run; C-child inputs PUBLISHED by the
    wave-train kit as w3/w4):
      (C1) x1 = H(49;{17,18};31) [m=17-row z=31 first co-token, R=49,
           BLIND]: candidate collapse-CONFORM 0 (= v(35,31,49)=0).
      (C2) y1 = H(48;{16,17};31) [m=16-row z=31 first co-token, R=48,
           BLIND]: candidate collapse-CONFORM 1 (= v(33,31,48)=1).
      (C3) x3 = H(50;(18,18);31) [m=18 base-spot on-line, R=50]:
           frozen table {B-child = x1 (in-kit premise disclosed),
           C-child 1^H(49;(18,18);30) = 1^1 = 0 PUBLISHED (wave-train
           kit w3)} -> candidate mex{x1,0} = 1 = v(36,31,50)=1
           CONFORMING iff x1 conforms 0 (would extend the m=18
           z-sequence to 16 members).
      (C4) x4 = H(49;(17,17);31) [m=17 base-spot on-line, R=49]:
           frozen table {B-child = y1 (in-kit premise disclosed),
           C-child 1^H(48;(17,17);30) = 1^0 = 1 PUBLISHED (wave-train
           kit w4)} -> candidate mex{y1,1} = 0 = v(34,31,49)=0
           CONFORMING iff y1 conforms 1.
(D) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed form,
    NO engine recursion), FROZEN AS REGISTERED in the log's
    tail-range-CORRECTED S5 item #4 (scan domain ends at s=k+34):
      (D1) k=41 THIRTY-SECOND tail (ODD form, odd-z supply chain
           candidate 12/12): v(s,42,42) =? v(s,41,42) over s in
           {0} U {12..75}: hold {0} U {12..41}, then UNIFORM 0v1 for
           ALL s in {42..75}.
      (D2) k=42 THIRTY-THIRD tail (EVEN form, even-z supply chain
           candidate 12/12): v(s,43,43) =? v(s,42,43) over s in
           {0} U {12..76}: hold {0} U {12..41}, break 0v2 at s=42,
           then UNIFORM 2v1 for ALL s in {43..76}.
(E) RECHECK ANCHORS (published engine values only): the four z=30
    wave-train touches w1..w4 (0,1,1,0) and the fourteen published
    wave-train row separation values. The `match` field is the
    collapse-CONFORM criterion, False BY DESIGN for separation
    anchors; the operative criterion is value_matches_published.
(F) K0832 battery: every single-token literal used by this file,
    checked closed form vs canonical engine vs ordered engine.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_fifthwave_z33_z37.out).
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

ORDINAL = {41: 'thirtysecond', 42: 'thirtythird'}

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
    for (x, z2, R2) in [(35, 35, 53), (37, 35, 53), (36, 36, 55),
                        (38, 36, 55), (33, 33, 47), (35, 33, 47),
                        (34, 34, 49), (36, 34, 49), (35, 35, 51),
                        (37, 35, 51), (36, 36, 53), (38, 36, 53),
                        (35, 34, 48), (34, 33, 48), (37, 36, 52),
                        (38, 37, 54), (37, 36, 54), (38, 37, 56)]:
        battery_lits.append((x, z2, R2))
    # row-shape collapses: death/conform (dead shapes)
    for (x, z2, R2) in [(33, 34, 48), (31, 33, 47), (29, 33, 47),
                        (27, 33, 47), (32, 33, 48), (30, 34, 49),
                        (28, 34, 49), (35, 36, 52), (33, 35, 51),
                        (31, 35, 51), (36, 37, 54), (34, 36, 53),
                        (32, 36, 53), (35, 36, 54), (36, 37, 56)]:
        battery_lits.append((x, z2, R2))
    # z=31 spot collapses
    for (x, z2, R2) in [(35, 31, 49), (33, 31, 48), (36, 31, 50),
                        (34, 31, 49)]:
        battery_lits.append((x, z2, R2))
    # wave-train kit published separation collapse constants
    for (x, z2, R2) in [(33, 32, 48), (34, 33, 50), (32, 31, 46),
                        (35, 34, 50), (33, 33, 49), (35, 33, 49),
                        (34, 34, 51), (36, 34, 51), (31, 31, 45),
                        (33, 31, 45), (33, 32, 46), (32, 32, 47),
                        (34, 32, 47), (36, 35, 52)]:
        battery_lits.append((x, z2, R2))
    # z=30 published touch anchor collapses
    for (x, z2, R2) in [(35, 30, 48), (33, 30, 47), (36, 30, 49),
                        (34, 30, 48)]:
        battery_lits.append((x, z2, R2))
    # supply identity sample points (k=41 odd form, k=42 even form)
    for (x, z2, R2) in [(12, 42, 42), (41, 42, 42), (42, 42, 42),
                        (42, 41, 42), (75, 42, 42), (75, 41, 42),
                        (12, 43, 43), (41, 43, 43), (42, 43, 43),
                        (43, 43, 43), (42, 42, 43), (76, 43, 43),
                        (76, 42, 43)]:
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
    # (A) two-past + new-wave rows (log S5 item #1)
    out.append(row_record_x0(
        'twopast_m17_z35_row_record',
        'two_past_m17_z35_PREDECLARED_first_second_birth_gap3',
        {'co_token_17_allowed': True,
         'law_candidate': 'registered item #1 (wavetrain log S5, commit 69c4009a); prediction frozen BEFORE the run: EXACTLY TWO separations: {17,18}@S=35 DOWN 1v2 (two-past stick 1 vs collapse v(35,35,53)=2) + NEW birth {17,20}@S=37 UP 2v0 (gap-3 rule, collapse v(37,35,53)=0), the FIRST m=17 second birth; all other 30 shapes conform; recorded verbatim whatever it is',
         's_domain': '{17..55}', 'arity_max': 3,
         'derived_shape_count': 32,
         'style': 'x0 published residual-band style'},
        53, 35, 17, 17, 55))
    out.append(row_record_x0(
        'twopast_m18_z36_row_record',
        'two_past_m18_z36_PREDECLARED_first_second_birth_gap2',
        {'co_token_18_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: (18,18)@S=36 DOWN 0v2 (two-past stick 0 vs collapse v(36,36,55)=2) + NEW birth (18,20)@S=38 UP 2v1 (gap-2 rule, collapse v(38,36,55)=1), the FIRST m=18 second birth; all other 24 shapes conform; recorded verbatim whatever it is',
         's_domain': '{18..56}', 'arity_max': 3,
         'derived_shape_count': 26,
         'style': 'x0 published residual-band style'},
        55, 36, 18, 18, 56))
    out.append(row_record_x0(
        'twopast_m13_z33_row_record',
        'two_past_m13_z33_PREDECLARED_fourth_wave_d3_seat',
        {'co_token_13_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: {13,20}@S=33 DOWN 1v2 (two-past stick 1 vs collapse v(33,33,47)=2) + NEW birth {13,22}@S=35 UP 2v0 (collapse v(35,33,47)=0), the d=3 (fourth-wave) seat gap 7; {13,18}/{13,16}/{13,14} conform-dead (collapses v(31,33,47)=1 / v(29,33,47)=1 / v(27,33,47)=1); all other 74 shapes conform; recorded verbatim whatever it is',
         's_domain': '{13..51}', 'arity_max': 3,
         'derived_shape_count': 76,
         'style': 'x0 published residual-band style'},
        47, 33, 13, 13, 51))
    out.append(row_record_x0(
        'twopast_m14_z34_row_record',
        'two_past_m14_z34_PREDECLARED_fourth_wave_d3_seat',
        {'co_token_14_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: (14,20)@S=34 DOWN 0v2 (two-past stick 0 vs collapse v(34,34,49)=2) + NEW birth (14,22)@S=36 UP 2v1 (collapse v(36,34,49)=1), the d=3 seat gap 6; (14,18)/(14,16)/(14,14) conform-dead (collapses v(32,34,49)/v(30,34,49)/v(28,34,49) all 0); all other 60 shapes conform; recorded verbatim whatever it is',
         's_domain': '{14..52}', 'arity_max': 3,
         'derived_shape_count': 62,
         'style': 'x0 published residual-band style'},
        49, 34, 14, 14, 52))
    out.append(row_record_x0(
        'twopast_m15_z35_row_record',
        'two_past_m15_z35_PREDECLARED_third_wave_d2_seat',
        {'co_token_15_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: {15,20}@S=35 DOWN 1v2 (two-past stick 1 vs collapse v(35,35,51)=2) + NEW birth {15,22}@S=37 UP 2v0 (collapse v(37,35,51)=0), the d=2 seat gap 5; {15,18}/{15,16} conform-dead (collapses v(33,35,51)=1 / v(31,35,51)=1); all other 48 shapes conform; recorded verbatim whatever it is',
         's_domain': '{15..53}', 'arity_max': 3,
         'derived_shape_count': 50,
         'style': 'x0 published residual-band style'},
        51, 35, 15, 15, 53))
    out.append(row_record_x0(
        'twopast_m16_z36_row_record',
        'two_past_m16_z36_PREDECLARED_third_wave_d2_seat',
        {'co_token_16_allowed': True,
         'law_candidate': 'registered item #1; prediction frozen BEFORE the run: EXACTLY TWO separations: (16,20)@S=36 DOWN 0v2 (two-past stick 0 vs collapse v(36,36,53)=2) + NEW birth (16,22)@S=38 UP 2v1 (collapse v(38,36,53)=1), the d=2 seat gap 4; (16,18)/(16,16) conform-dead (collapses v(34,36,53)=0 / v(32,36,53)=0); all other 38 shapes conform; recorded verbatim whatever it is',
         's_domain': '{16..54}', 'arity_max': 3,
         'derived_shape_count': 40,
         'style': 'x0 published residual-band style'},
        53, 36, 16, 16, 54))
    # (B) one-past ladder rows (log S5 item #2); each also measures a
    #     birth+3 death
    out.append(row_record_x0(
        'onepast_m13_z34_row_record',
        'one_past_m13_z34_PREDECLARED_death_of_13_20',
        {'co_token_13_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation {13,22}@S=35 UP 1v0 (born z=33, odd one-past decay 2->1, collapse v(35,34,48)=0); {13,20} conform-DEAD at its birth+3 slice (collapsed to 1 = collapse v(33,34,48)=1; born z=31), death datum 10; all other 75 shapes conform; recorded verbatim whatever it is',
         's_domain': '{13..51}', 'arity_max': 3,
         'derived_shape_count': 76,
         'style': 'x0 published residual-band style'},
        48, 34, 13, 13, 51))
    out.append(row_record_x0(
        'onepast_m14_z33_row_record',
        'one_past_m14_z33_PREDECLARED_death_of_14_18',
        {'co_token_14_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation (14,20)@S=34 DOWN 0v1 (born z=32, even one-past decay 2->0, collapse v(34,33,48)=1); (14,18) conform-DEAD at its birth+3 slice (collapse v(32,33,48)=0; born z=30), death datum 11; (14,16)/(14,14) conform-dead; all other 61 shapes conform; recorded verbatim whatever it is',
         's_domain': '{14..52}', 'arity_max': 3,
         'derived_shape_count': 62,
         'style': 'x0 published residual-band style'},
        48, 33, 14, 14, 52))
    out.append(row_record_x0(
        'onepast_m15_z36_row_record',
        'one_past_m15_z36_PREDECLARED_death_of_15_20',
        {'co_token_15_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation {15,22}@S=37 UP 1v0 (born z=35, odd one-past decay 2->1, collapse v(37,36,52)=0); {15,20} conform-DEAD at its birth+3 slice (collapse v(35,36,52)=1; born z=33), death datum 12; all other 49 shapes conform; recorded verbatim whatever it is',
         's_domain': '{15..53}', 'arity_max': 3,
         'derived_shape_count': 50,
         'style': 'x0 published residual-band style'},
        52, 36, 15, 15, 53))
    out.append(row_record_x0(
        'onepast_m16_z37_row_record',
        'one_past_m16_z37_PREDECLARED_death_of_16_20',
        {'co_token_16_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation (16,22)@S=38 DOWN 0v1 (born z=36, even one-past decay 2->0, collapse v(38,37,54)=1); (16,20) conform-DEAD at its birth+3 slice (collapse v(36,37,54)=0; born z=34), death datum 13; all other 39 shapes conform; recorded verbatim whatever it is',
         's_domain': '{16..54}', 'arity_max': 3,
         'derived_shape_count': 40,
         'style': 'x0 published residual-band style'},
        54, 37, 16, 16, 54))
    out.append(row_record_x0(
        'onepast_m17_z36_row_record',
        'one_past_m17_z36_PREDECLARED_first_m17_death',
        {'co_token_17_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation {17,20}@S=37 UP 1v0 (born z=35, odd one-past decay 2->1, collapse v(37,36,54)=0); {17,18} conform-DEAD at its birth+3 slice (collapse v(35,36,54)=1; born z=33) — the FIRST m=17 death, completing death coverage for ALL SIX bands m in {13..18}; all other 31 shapes conform; recorded verbatim whatever it is',
         's_domain': '{17..55}', 'arity_max': 3,
         'derived_shape_count': 32,
         'style': 'x0 published residual-band style'},
        54, 36, 17, 17, 55))
    out.append(row_record_x0(
        'onepast_m18_z37_row_record',
        'one_past_m18_z37_PREDECLARED_first_m18_death',
        {'co_token_18_allowed': True,
         'law_candidate': 'registered item #2; prediction frozen BEFORE the run: EXACTLY ONE separation (18,20)@S=38 DOWN 0v1 (born z=36, even one-past decay 2->0, collapse v(38,37,56)=1); (18,18) conform-DEAD at its birth+3 slice (collapse v(36,37,56)=0; born z=34) — the FIRST m=18 death; all other 25 shapes conform; recorded verbatim whatever it is',
         's_domain': '{18..56}', 'arity_max': 3,
         'derived_shape_count': 26,
         'style': 'x0 published residual-band style'},
        56, 37, 18, 18, 56))
    # (C) m=18/m=17 base-spot z=31 touch
    x1 = H(49, tuple(sorted((17, 18), reverse=True)), 31)
    y1 = H(48, tuple(sorted((16, 17), reverse=True)), 31)
    x3 = H(50, (18, 18), 31)
    x4 = H(49, (17, 17), 31)
    out.append({'section': 'z31_basespot_touch',
                'label': 'wavetrain_log_S5_item3_registered_blind_option_tables_first_ever_z31_engine_touches',
                'spots': [
                    {'id': 'x1', 'X': [17, 18], 'R': 49, 'z': 31,
                     'value': x1, 'collapse': v(35, 31, 49),
                     'role': 'm=17-row z=31 first co-token member; BLIND candidate collapse-conform 0 = v(35,31,49)',
                     'match': x1 == v(35, 31, 49)},
                    {'id': 'y1', 'X': [16, 17], 'R': 48, 'z': 31,
                     'value': y1, 'collapse': v(33, 31, 48),
                     'role': 'm=16-row z=31 first co-token member; BLIND candidate collapse-conform 1 = v(33,31,48)',
                     'match': y1 == v(33, 31, 48)},
                    {'id': 'x3', 'X': [18, 18], 'R': 50, 'z': 31,
                     'value': x3, 'collapse': v(36, 31, 50),
                     'role': 'm=18 base-spot on-line member; frozen option table {B-child = x1 (in-kit first-contact premise disclosed), C-child 1^H(49;(18,18);30)=1^1=0 PUBLISHED wavetrain-kit w3}; candidate mex{x1,0}=1 = collapse v(36,31,50) CONFORMING iff x1 conforms 0 (would extend the m=18 z-sequence to 16 members)',
                     'match': x3 == v(36, 31, 50)},
                    {'id': 'x4', 'X': [17, 17], 'R': 49, 'z': 31,
                     'value': x4, 'collapse': v(34, 31, 49),
                     'role': 'm=17 base-spot on-line member; frozen option table {B-child = y1 (in-kit premise disclosed), C-child 1^H(48;(17,17);30)=1^0=1 PUBLISHED wavetrain-kit w4}; candidate mex{y1,1}=0 = collapse v(34,31,49) CONFORMING iff y1 conforms 1',
                     'match': x4 == v(34, 31, 49)}],
                'published_anchor': 'm=18 base-spot on-line z-sequence published z in {16..30} = 0,1,0,1,0,1,0,1,1,1,1,1,1,1,1 (15 members incl. w3 by the wave-train kit); m=17 members published all zero through z=30 (incl. w4); on conform the z=31 members are x3 (m=18) and x4 (m=17)'})
    # (E) recheck anchors — published engine values only
    rechecks = []
    for (R, X, z2, expected) in [
            (48, (15, 18), 32, 1), (50, (16, 18), 33, 0),
            (46, (14, 18), 31, 0), (50, (15, 20), 34, 1),
            (49, (15, 18), 33, 1), (49, (15, 20), 33, 2),
            (51, (16, 18), 34, 0), (51, (16, 20), 34, 2),
            (45, (13, 18), 31, 1), (45, (13, 20), 31, 2),
            (46, (13, 20), 32, 1), (47, (14, 18), 32, 0),
            (47, (14, 20), 32, 2), (52, (16, 20), 35, 0),
            (48, (17, 18), 30, 0), (47, (16, 17), 30, 1),
            (49, (18, 18), 30, 1), (48, (17, 17), 30, 0)]:
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
                'match_field_note': 'match is the collapse-CONFORM criterion; for the 14 published separation anchors it is False BY DESIGN (the engine value deviates from the collapse); the operative recheck criterion is value_matches_published; for the 4 touch anchors w1..w4 conform holds and match is True as published',
                'rows': rechecks})
    # (D) tail supply pre-computations (pure closed form, engine-free)
    for k in (41, 42):
        dom = [0] + list(range(12, k + 35))
        if k == 41:
            secname = 'thirtysecond_tail_supply_identity_precalc'
            lab = ('registered_candidate_odd_form_12of12_wavetrain_log_S5_item4')
            note = ('REGISTERED (wavetrain log S5 item #4, tail-range-corrected, commit 69c4009a): hold {0} U {12..41}, then UNIFORM 0v1 for ALL s in {42..75}; odd-z supply chain candidate 12/12; the z=41-slice supply datum precomputed for the future z=41 declaration lane')
        else:
            secname = 'thirtythird_tail_supply_identity_precalc'
            lab = ('registered_candidate_even_form_12of12_wavetrain_log_S5_item4')
            note = ('REGISTERED (wavetrain log S5 item #4, tail-range-corrected): hold {0} U {12..41}, break 0v2 at s=42, then UNIFORM 2v1 for ALL s in {43..76}; even-z supply chain candidate 12/12; the z=42-slice supply datum precomputed for the future z=42 declaration lane')
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
