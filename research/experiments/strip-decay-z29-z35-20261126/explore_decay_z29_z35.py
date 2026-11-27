#!/usr/bin/env python3
"""
explore_decay_z29_z35: FROZEN PRE-DECLARATION micro-census executing the
REGISTERED HANDOFFS of the frontier micro-kit log section 5 (commit
`d49b480a`, the strip-frontier-z27-z34 kit): item #1 the one-past
parity-decay candidates at m=17/m=18, item #2 the secondary-birth and
death-curve next slices (m=15@z=31, m=16@z=32 two-past; m=14@z=29
three-past; m=13@z=29 four-past), item #3 the m=18/m=17 base-spot
z=29 touch with blind option tables, item #4 the k=37/k=38 tail supply
pre-computations. NO K slot is claimed by this file; the constants
below were frozen into this docstring BEFORE the first run of this
file and the file has not been edited after any of its runs.

SLOT CHECK (performed at kit-build time): the latest main head is
`d49b480a` (the frontier micro-kit itself). The positions measured
here — the m=17 row at z=34, the m=18 row at z=35, the m=15 row at
z=31, the m=16 row at z=32, the m=14 row at z=29 AND z=30, the m=13
row at z=29 AND z=30, the four z=29 touch spots — have NO published
engine value of any kind (the frontier micro-kit measured the m=15 row
at z=29/30, the m=16 row at z=30/31, the m=17 row at z=33, the m=18
row at z=34, the m=13 row at z=27/28, the m=14 row at z=27/28 and the
four z=28 touches; the published repositories of engine values at
z >= 29 are exactly those rows). Every position below is touched by
the engine for the FIRST time at the frozen first run of this file,
except the recheck anchors of section (G).

HONEST DISCLOSURE (drafting discipline, before the freeze): the
candidates below were formulated from (i) PUBLISHED finite
observations (the frontier kit rows, now on main) and (ii) the PROVED
K0832 single-token closed form v(x,z,R) for every collapse constant,
machine-verified during drafting with closed form only — NO engine
recursion was run on any new position before the freeze (nothing
existed to observe). The one-past parity-decay rule (2 data per
parity) and the secondary-birth rule (1 datum per parity) are
CANDIDATES; the predictions below are falsifiable extrapolations, and
the separation lists are recorded verbatim whatever they are.

REGISTERED CANDIDATES, frozen before the first run:

(A) ONE-PAST PARITY-DECAY rows (registered frontier-kit S5 item #1;
    x0 style, R = m+z+1, parts >= m, co-token allowed, arity <= 3,
    S in {m..m+38}; derived shape counts m=17: 32, m=18: 26):
      (A1) m=17 @ z=34 (one past z*(17)=33, ODD): predicted EXACTLY
           ONE separation: {17,18} @S=35, UP 1v0 (odd decay 2->1,
           collapse v(35,34,52)=0) — decay candidate datum 3/odd.
      (A2) m=18 @ z=35 (one past z*(18)=34, EVEN): predicted EXACTLY
           ONE separation: (18,18) @S=36, DOWN 0v1 (even decay 2->0,
           collapse v(36,35,54)=1) — decay candidate datum 3/even.
(B) TWO-PAST SECONDARY-BIRTH rows (registered S5 item #2; shape
    counts m=15: 50, m=16: 40):
      (B1) m=15 @ z=31 (two past, ODD): predicted EXACTLY TWO
           separations: the original {15,16} @S=31 persists with the
           odd value STUCK at 1 while its collapse jumps to
           v(31,31,47)=2 -> DOWN 1v2, plus the NEW SECONDARY
           {15,18} @S=33 born at value 2 -> UP 2v0 (the gap-3
           secondary-shape rule, collapse v(33,31,47)=0).
      (B2) m=16 @ z=32 (two past, EVEN): predicted EXACTLY TWO
           separations: the original (16,16) @S=32 with the even
           value STUCK at 0, collapse v(32,32,49)=2 -> DOWN 0v2, plus
           the NEW SECONDARY (16,18) @S=34 born at value 2 -> UP 2v1
           (the gap-2 secondary-shape rule, collapse v(34,32,49)=1).
(C) THREE-PAST DEATH row (registered S5 item #2; shape count 62):
      (C1) m=14 @ z=29 (three past, EVEN): predicted ZERO
           separations — the original (14,14) @S=28 DIES conform
           (stuck value 0 = collapse v(28,29,44)=0, the m=13
           precedent at three-past) AND the secondary (14,16) @S=30
           decays 2->1 = conform (collapse v(30,29,44)=1): the whole
           row conforming is the boldest falsifiable prediction this
           kit carries.
(D) FOUR-PAST decay row (registered S5 item #2, no hard value pick;
    shape count 76):
      (D1) m=13 @ z=29 (four past, ODD): NON-BINDING expectation: the
           secondary {13,16} @S=29 persists with value stuck at 1
           against collapse v(29,29,43)=2 -> DOWN 1v2 and is the
           ONLY separation; NO hard value pick is claimed (0 or 2
           would both be new-decay data); recorded verbatim.
(E) KIT-ADDED curve extensions (NO CANDIDATE, first contacts):
      (E1) m=13 @ z=30 (FIVE past; shape count 76).
      (E2) m=14 @ z=30 (FOUR past; shape count 62).
(F) BASE-SPOT z=29 TOUCH (registered S5 item #3; four FIRST-EVER
    z=29 engine touches, option tables frozen BEFORE the run; the
    C-child inputs are the PUBLISHED z=28 values of the frontier
    kit):
      (F1) u1 = H(47;{17,18};29) [m=17-row z=29 first co-token,
           R=47, blind]: candidate collapse-CONFORM 0
           (= collapse v(35,29,47)=0).
      (F2) u2 = H(46;{16,17};29) [m=16-row z=29 first co-token,
           R=46, blind]: candidate collapse-CONFORM 1
           (= collapse v(33,29,46)=1).
      (F3) u3 = H(48;(18,18);29) [m=18 base-spot on-line member,
           R=48]: frozen option table {B-child = u1 (in-kit premise
           disclosed), C-child = 1^H(47;(18,18);28) = 1^1 = 0
           PUBLISHED (frontier kit t3)} -> candidate mex{u1,0} = 1 =
           collapse v(36,29,48)=1 CONFORMING iff u1 conforms 0.
      (F4) u4 = H(47;(17,17);29) [m=17 base-spot on-line member,
           R=47]: frozen option table {B-child = u2 (in-kit premise
           disclosed), C-child = 1^H(46;(17,17);28) = 1^0 = 1
           PUBLISHED (frontier kit t4)} -> candidate mex{u2,1} = 0 =
           collapse v(34,29,47)=0 CONFORMING iff u2 conforms 1.
      On conform, the m=18 base-spot on-line z-sequence extends to
      z=29 (published z in {16..28} = 0,1,0,1,0,1,0,1,1,1,1,1,1) and
      the m=17 z-sequence to z=29 (all zero).
(G) RECHECK ANCHORS (published engine values only): the four z=28
    frontier-kit touches t1..t4 (0,1,1,0) and the eight published
    frontier-kit past-row separation engine values (m13z27 {13,14}=1
    and {13,16}=2; m14z27 (14,14)=0; m15z30 {15,16}=1; m16z31
    (16,16)=0; m13z28 {13,16}=1; m14z28 (14,14)=0 and (14,16)=2).
    The `match` field is the collapse-CONFORM criterion; for the nine
    separation anchors it is False BY DESIGN — the operative recheck
    criterion is value == published_value.
(H) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed form,
    NO engine recursion):
      (H1) k=37 TWENTY-EIGHTH tail (registered S5 item #4, ODD form,
           odd-z supply chain candidate 10/10): identity
           v(s,38,38) =? v(s,37,38) over s in {0} U {12..71}: hold
           {0} U {12..37}, then UNIFORM 0v1 for ALL s in {38..71}.
      (H2) k=38 TWENTY-NINTH tail (registered S5 item #4, EVEN form,
           even-z supply chain candidate 10/10): identity
           v(s,39,39) =? v(s,38,39) over s in {0} U {12..72}: hold
           {0} U {12..37}, break 0v2 at s=38, then UNIFORM 2v1 for
           ALL s in {39..72}.
(I) K0832 battery: every single-token literal used by this file
    (candidate collapses, spot tables, recheck collapses, supply
    samples), checked closed form vs canonical engine vs ordered
    engine. Candidate: all match.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_decay_z29_z35.out).
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

ORDINAL = {37: 'twentyeighth', 38: 'twentyninth'}


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
    # candidate shape collapses (A)(B)(C)(D)
    for (x, z2, R2) in [(35, 34, 52), (36, 35, 54), (31, 31, 47),
                        (33, 31, 47), (32, 32, 49), (34, 32, 49),
                        (28, 29, 44), (30, 29, 44), (29, 29, 43),
                        (32, 29, 44), (35, 34, 52)]:
        battery_lits.append((x, z2, R2))
    # z=29 spot tables: collapses and C-child published literals
    for (x, z2, R2) in [(35, 29, 47), (33, 29, 46), (36, 29, 48),
                        (34, 29, 47), (36, 28, 47), (34, 28, 46)]:
        battery_lits.append((x, z2, R2))
    # recheck anchor collapses (published z=27/28/30/31 separations)
    for (x, z2, R2) in [(28, 27, 42), (29, 27, 41), (31, 30, 46),
                        (32, 31, 48), (27, 28, 42), (30, 28, 43),
                        (35, 28, 46), (33, 28, 45)]:
        battery_lits.append((x, z2, R2))
    # supply identity sample points (k=37 odd form, k=38 even form)
    for (x, z2, R2) in [(12, 38, 38), (37, 38, 38), (38, 38, 38),
                        (37, 37, 38), (38, 37, 38), (71, 38, 38),
                        (71, 37, 38), (12, 39, 39), (38, 39, 39),
                        (38, 38, 39), (39, 39, 39), (72, 39, 39),
                        (72, 38, 39)]:
        battery_lits.append((x, z2, R2))
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
    # (A) ONE-PAST PARITY-DECAY rows
    out.append(row_record_x0(
        'onepast_m17_z34_row_record',
        'one_past_m17_z34_PREDECLARED_PARITY_DECAY_datum3_odd',
        {'co_token_17_allowed': True,
         'law_candidate': 'frontier-kit S5 item #1 one-past parity-decay candidate (2 data/parity: odd m=13@z=26 and m=15@z=30 UP 1v0; even m=14@z=27 and m=16@z=31 DOWN 0v1); prediction frozen BEFORE the run: EXACTLY ONE separation {17,18}@S=35 UP 1v0 (odd decay 2->1, collapse v(35,34,52)=0), other 31 shapes conform; recorded verbatim whatever it is',
         's_domain': '{17..55}', 'arity_max': 3,
         'derived_shape_count': 32,
         'style': 'x0 published residual-band style'},
        52, 34, 17, 17, 55))
    out.append(row_record_x0(
        'onepast_m18_z35_row_record',
        'one_past_m18_z35_PREDECLARED_PARITY_DECAY_datum3_even',
        {'co_token_18_allowed': True,
         'law_candidate': 'prediction frozen BEFORE the run: EXACTLY ONE separation (18,18)@S=36 DOWN 0v1 (even decay 2->0, collapse v(36,35,54)=1), other 25 shapes conform; recorded verbatim whatever it is',
         's_domain': '{18..56}', 'arity_max': 3,
         'derived_shape_count': 26,
         'style': 'x0 published residual-band style'},
        54, 35, 18, 18, 56))
    # (B) TWO-PAST SECONDARY-BIRTH rows
    out.append(row_record_x0(
        'twopast_m15_z31_row_record',
        'two_past_m15_z31_PREDECLARED_SECONDARY_BIRTH_datum2_odd',
        {'co_token_15_allowed': True,
         'law_candidate': 'frontier-kit S5 item #2 candidates; prediction frozen BEFORE the run: EXACTLY TWO separations: original {15,16}@S=31 DOWN 1v2 (odd value stuck at 1, collapse jumps to v(31,31,47)=2) + NEW secondary {15,18}@S=33 born UP 2v0 (gap-3 rule, collapse v(33,31,47)=0); recorded verbatim whatever it is',
         's_domain': '{15..53}', 'arity_max': 3,
         'derived_shape_count': 50,
         'style': 'x0 published residual-band style'},
        47, 31, 15, 15, 53))
    out.append(row_record_x0(
        'twopast_m16_z32_row_record',
        'two_past_m16_z32_PREDECLARED_SECONDARY_BIRTH_datum2_even',
        {'co_token_16_allowed': True,
         'law_candidate': 'prediction frozen BEFORE the run: EXACTLY TWO separations: original (16,16)@S=32 DOWN 0v2 (even value stuck at 0, collapse v(32,32,49)=2) + NEW secondary (16,18)@S=34 born UP 2v1 (gap-2 rule, collapse v(34,32,49)=1); recorded verbatim whatever it is',
         's_domain': '{16..54}', 'arity_max': 3,
         'derived_shape_count': 40,
         'style': 'x0 published residual-band style'},
        49, 32, 16, 16, 54))
    # (C) THREE-PAST DEATH row
    out.append(row_record_x0(
        'threepast_m14_z29_row_record',
        'three_past_m14_z29_PREDECLARED_FULL_DEATH_ZERO_SEPARATIONS',
        {'co_token_14_allowed': True,
         'law_candidate': 'the boldest prediction frozen BEFORE the run: ZERO separations — original (14,14)@S=28 dies conform (even value stuck 0 = collapse v(28,29,44)=0, per the m=13 three-past death precedent) AND secondary (14,16)@S=30 decays 2->1 = conform (collapse v(30,29,44)=1); the whole row conforming would complete the m>=14-side death curve; recorded verbatim whatever it is',
         's_domain': '{14..52}', 'arity_max': 3,
         'derived_shape_count': 62,
         'style': 'x0 published residual-band style'},
        44, 29, 14, 14, 52))
    # (D) FOUR-PAST decay row (no hard value pick)
    out.append(row_record_x0(
        'fourpast_m13_z29_row_record',
        'four_past_m13_z29_NONBINDING_stuck_value_expectation_recorded_verbatim',
        {'co_token_13_allowed': True,
         'law_candidate': 'NON-BINDING expectation frozen BEFORE the run: secondary {13,16}@S=29 persists as the ONLY separation with odd value stuck at 1 vs collapse v(29,29,43)=2 -> DOWN 1v2; NO hard value pick (0 or 2 would be new decay data); recorded verbatim whatever it is',
         's_domain': '{13..51}', 'arity_max': 3,
         'derived_shape_count': 76,
         'style': 'x0 published residual-band style'},
        43, 29, 13, 13, 51))
    # (E) kit-added curve extensions, NO CANDIDATE
    out.append(row_record_x0(
        'fivepast_m13_z30_row_record',
        'five_past_m13_z30_NO_CANDIDATE_kit_added_first_contact',
        {'co_token_13_allowed': True,
         'note': 'z*(13)=25 so z=30 is FIVE past (kit-added, NO CANDIDATE); the full m=13 decay curve now spans z=25..30; recorded verbatim whatever it is',
         's_domain': '{13..51}', 'arity_max': 3,
         'derived_shape_count': 76,
         'style': 'x0 published residual-band style'},
        44, 30, 13, 13, 51))
    out.append(row_record_x0(
        'fourpast_m14_z30_row_record',
        'four_past_m14_z30_NO_CANDIDATE_kit_added_first_contact',
        {'co_token_14_allowed': True,
         'note': 'z*(14)=26 so z=30 is FOUR past (kit-added, NO CANDIDATE); the m=14 decay curve now spans z=26..30; recorded verbatim whatever it is',
         's_domain': '{14..52}', 'arity_max': 3,
         'derived_shape_count': 62,
         'style': 'x0 published residual-band style'},
        45, 30, 14, 14, 52))
    # (F) m=18/m=17 base-spot z=29 touch — four first-ever z=29 engine
    #     touches with option tables frozen before the run
    u1 = H(47, tuple(sorted((17, 18), reverse=True)), 29)
    u2 = H(46, tuple(sorted((16, 17), reverse=True)), 29)
    u3 = H(48, (18, 18), 29)
    u4 = H(47, (17, 17), 29)
    out.append({'section': 'z29_basespot_touch',
                'label': 'frontier_kit_S5_item3_registered_blind_option_tables_first_ever_z29_engine_touches',
                'spots': [
                    {'id': 'u1', 'X': [17, 18], 'R': 47, 'z': 29,
                     'value': u1, 'collapse': v(35, 29, 47),
                     'role': 'm=17-row z=29 first co-token member; BLIND candidate collapse-conform 0 = v(35,29,47)',
                     'match': u1 == v(35, 29, 47)},
                    {'id': 'u2', 'X': [16, 17], 'R': 46, 'z': 29,
                     'value': u2, 'collapse': v(33, 29, 46),
                     'role': 'm=16-row z=29 first co-token member; BLIND candidate collapse-conform 1 = v(33,29,46)',
                     'match': u2 == v(33, 29, 46)},
                    {'id': 'u3', 'X': [18, 18], 'R': 48, 'z': 29,
                     'value': u3, 'collapse': v(36, 29, 48),
                     'role': 'm=18 base-spot on-line member; frozen option table {B-child = u1 (in-kit first-contact premise disclosed), C-child 1^H(47;(18,18);28)=1^1=0 PUBLISHED frontier-kit t3}; candidate mex{u1,0}=1 = collapse v(36,29,48) CONFORMING iff u1 conforms 0',
                     'match': u3 == v(36, 29, 48)},
                    {'id': 'u4', 'X': [17, 17], 'R': 47, 'z': 29,
                     'value': u4, 'collapse': v(34, 29, 47),
                     'role': 'm=17 base-spot on-line member; frozen option table {B-child = u2 (in-kit premise disclosed), C-child 1^H(46;(17,17);28)=1^0=1 PUBLISHED frontier-kit t4}; candidate mex{u2,1}=0 = collapse v(34,29,47) CONFORMING iff u2 conforms 1',
                     'match': u4 == v(34, 29, 47)}],
                'published_anchor': 'm=18 base-spot on-line z-sequence z in {16..28} = 0,1,0,1,0,1,0,1,1,1,1,1,1 (published incl. z=28 by the frontier kit t3); m=17 z-sequence z in {16..28} = all zero; on conform the z=29 members are u3(m=18) and u4(m=17)'})
    # (G) recheck anchors — published engine values only
    rechecks = []
    for (R, X, z2, expected) in [
            (46, (17, 18), 28, 0), (45, (16, 17), 28, 1),
            (47, (18, 18), 28, 1), (46, (17, 17), 28, 0),
            (41, (13, 14), 27, 1), (41, (13, 16), 27, 2),
            (42, (14, 14), 27, 0), (46, (15, 16), 30, 1),
            (48, (16, 16), 31, 0), (42, (13, 16), 28, 1),
            (43, (14, 14), 28, 0), (43, (14, 16), 28, 2)]:
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
                'match_field_note': 'match is the collapse-CONFORM criterion; for the 8 published separation anchors it is False BY DESIGN (the engine value deviates from the collapse); the operative recheck criterion is value_matches_published',
                'rows': rechecks})
    # (H) tail supply pre-computations (pure closed form, engine-free)
    for k in (37, 38):
        dom = [0] + list(range(12, k + 35))
        if k == 37:
            secname = 'twentyeighth_tail_supply_identity_precalc'
            lab = ('registered_candidate_odd_form_10of10_frontier_kit_S5_item4')
            note = ('REGISTERED candidate (frontier kit log S5 item #4, commit d49b480a): hold {0} U {12..37}, then UNIFORM 0v1 for ALL s in {38..71}; odd-z supply chain candidate 10/10; the z=37-slice supply datum precomputed for the future z=37 declaration lane')
        else:
            secname = 'twentyninth_tail_supply_identity_precalc'
            lab = ('registered_candidate_even_form_10of10_frontier_kit_S5_item4')
            note = ('REGISTERED candidate (frontier kit log S5 item #4): hold {0} U {12..37}, break 0v2 at s=38, then UNIFORM 2v1 for ALL s in {39..72}; even-z supply chain candidate 10/10; the z=38-slice supply datum precomputed for the future z=38 declaration lane')
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
