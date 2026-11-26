#!/usr/bin/env python3
"""
explore_z27z34_frontier: FROZEN PRE-DECLARATION micro-census executing the
REGISTERED HANDOFFS of the published z26f20 kit log section 5 (commit
`68bc863d`): item #1 next frontier test data (the PARITY-CORRECTED
FRONTIER-RECORD LAW candidate), item #2 one-past datum candidates, item
#3 the TWENTY-SIXTH-tail (k=35) pre-computation, and item #4 the m=18
base-spot z-sequence z=28 touch with the blind option tables registered
there. NO K slot is claimed by this file; the constants below were
frozen into this docstring BEFORE the first run of this file and the
file has not been edited after any of its runs.

SLOT CHECK (performed at kit-build time): the latest main (head
`f5124331`, 2026-11-26T04:48:55Z) contains NO z=27-slice census kit, NO
z=28..34 engine values of any kind (filename:explore_z27 / explore_z28 /
explore_z29 searches return 0 hits; "k=35" hits are only the unrelated
n11-cost16 closure lane), NO frontier-row record at z >= 27, and the
only published z=27 engine values are the four z26f20 handoff spots
h1=H(45;{17,18};27)=0, h2=H(44;{16,17};27)=1, h3=H(46;(18,18);27)=1,
h4=H(45;(17,17);27)=0 (plus its below-band H(27;Y;27) child-slice
census, whose shapes have min(Y) >= 20 and R=27 — disjoint from every
position measured here). The only published z=25/z=26 frontier-record
separations are H(39;{13,14};25)=2, H(40;{13,14};26)=1,
H(41;(14,14);26)=2. Every z in {27..34} position below is touched by
the engine for the FIRST time at the frozen first run of this file,
except the recheck anchors listed in section (r).

HONEST DISCLOSURE (drafting discipline, before the freeze): the
candidate constants below were derived BY CLOSED FORM ONLY — the
published PROVED K0832 single-token form v(x,z,R) (and pure
combinatorial shape counting) — during drafting, BEFORE the freeze.
The drafting scratch used NO engine recursion at all; for the new
z in {27..34} positions no engine value existed on main at freeze
time, so nothing could be drafted from observation. All collapse
constants quoted below were machine-verified against the K0832 closed
form only; the engine cross-check happens for the first time inside
the frozen run (section (b1) battery).

REGISTERED CANDIDATES, frozen before the first run:

(A) FRONTIER-ROW RECORDS at the row's own frontier z = z*(m)
    (K1268: z*(m) = 2m-2+(m mod 2)), x0 published residual-band style
    (R = m+z+1, all parts >= m, co-token m allowed, arity <= 3 TOTAL,
    S in {m..m+38}); derived shape counts (pure combinatorics):
    m=13: 76, m=14: 62, m=15: 50, m=16: 40, m=17: 32, m=18: 26.
    The z26f20 §5-item-#1 PARITY-SPLIT candidate (two data points:
    m=13@z=25, m=14@z=26) predicts at z = z*(m) EXACTLY ONE
    separation per row:
      (A1) m=15 @ z=29 (z*(15)=29, ODD): unique separation
           X={15,16} @S=31, UP 2v0 (collapse v(31,29,45)=0);
           the other 49 shapes conform. PARITY-SPLIT candidate datum 3.
      (A2) m=16 @ z=30 (z*(16)=30, EVEN): unique separation
           X=(16,16) @S=32, UP 2v1 (collapse v(32,30,47)=1);
           the other 39 shapes conform. PARITY-SPLIT candidate datum 4.
      (A3) m=17 @ z=33 (z*(17)=33, ODD): unique separation
           X={17,18} @S=35, UP 2v0 (collapse v(35,33,51)=0);
           the other 31 shapes conform. PARITY-SPLIT candidate datum 5.
      (A4) m=18 @ z=34 (z*(18)=34, EVEN): unique separation
           X=(18,18) @S=36, UP 2v1 (collapse v(36,34,53)=1);
           the other 25 shapes conform. PARITY-SPLIT candidate datum 6.
    On confirmation these would carry the parity-split candidate to
    6/6 (odd m=13/15/17; even m=14/16/18) — still a CANDIDATE
    (finite observations; no universal claim). The separation lists
    are recorded verbatim whatever they are; refutation is itself
    the datum.
(B) ONE-PAST / FARTHER-PAST ROW RECORDS (registered §5 item #2 plus
    kit-added first contacts; x0 style, same S ranges):
    (B1) m=13 @ z=27 [TWO past its frontier z*(13)=25; the z26f20 §5
         item #2 registered it under the one-past item — recorded
         here with the honest label TWO-PAST]: NO CANDIDATE, first
         contact. Published trajectory of the m=13 frontier
         separation shape {13,14} @S=27: z=25 UP 2v0, z=26 UP 1v0;
         its z=27 collapse is v(27,27,41)=2 — recorded verbatim.
    (B2) m=14 @ z=27 [ONE past its frontier z*(14)=26]: NO
         CANDIDATE, first contact. NON-BINDING structural expectation
         (§5 item #2 drop rule candidate): the at-frontier
         separation X=(14,14) @S=28 UP 2v1 (value 2, collapse
         v(28,26,41)=1) persists with value DROP 2->1; at z=27 the
         collapse of (14,14) is v(28,27,42)=1, so a drop to 1 would
         be CONFORM-INVISIBLE (1v1) and the row would show NO
         separation — the expectation is recorded in this falsifiable
         form.
    (B3) m=15 @ z=30 [ONE past, ODD; kit-added first contact]: NO
         CANDIDATE. NON-BINDING drop expectation: {15,16} @S=31
         persists with value 2->1; collapse v(31,30,46)=0, so the
         drop would remain visible as UP 1v0.
    (B4) m=16 @ z=31 [ONE past, EVEN; kit-added first contact]: NO
         CANDIDATE. NON-BINDING drop expectation: (16,16) @S=32
         value 2->1; collapse v(32,31,48)=1, drop = CONFORM-INVISIBLE.
    (B5) m=13 @ z=28 [THREE past; kit-added first contact]: NO
         CANDIDATE.
    (B6) m=14 @ z=28 [TWO past; kit-added first contact]: NO
         CANDIDATE.
(C) m=18 BASE-SPOT z-SEQUENCE z=28 TOUCH (registered §5 item #4;
    four FIRST-EVER z=28 engine touches, option tables frozen here
    BEFORE the run; pattern publishes its inputs from z26f20):
      (C1) t1 = H(46;{17,18};28) [m=17-row z=28 first co-token
           member, R=46, blind]: candidate collapse-CONFORM 0
           (= collapse v(35,28,46)=0).
      (C2) t2 = H(45;{16,17};28) [m=16-row z=28 first co-token
           member, R=45, blind]: candidate collapse-CONFORM 1
           (= collapse v(33,28,45)=1).
      (C3) t3 = H(47;(18,18);28) [m=18 base-spot on-line member,
           R=47]: frozen option table {B-child = t1 (in-kit
           first-contact premise disclosed), C-child = 1^H(46;(18,18);27)
           = 1^1 = 0 PUBLISHED (z26f20 h3)} -> candidate mex{0,0} = 1
           = collapse v(36,28,47)=1 CONFORMING iff t1 conforms 0.
      (C4) t4 = H(46;(17,17);28) [m=17 base-spot on-line member,
           R=46]: frozen option table {B-child = t2 (in-kit premise
           disclosed), C-child = 1^H(45;(17,17);27) = 1^0 = 1
           PUBLISHED (z26f20 h4)} -> candidate mex{1,1} = 0 =
           collapse v(34,28,46)=0 CONFORMING iff t2 conforms 1.
      On conform, the m=18 base-spot on-line z-sequence extends to
      z=28 (published z in {16..27} = 0,1,0,1,0,1,0,1,1,1,1,1) and
      the m=17 sequence to z=28 (published z in {16..27} =
      0,0,0,0,0,0 — all zero).
(D) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed form,
    NO engine recursion):
      (D1) k=35 TWENTY-SIXTH tail (registered §5 item #3, ODD form,
           odd-z supply chain candidate 9/9): identity
           v(s,36,36) =? v(s,35,36) over s in {0} U {12..69}:
           hold {0} U {12..35}, then UNIFORM 0v1 for ALL
           s in {36..69} (closed-form scan during drafting confirmed
           34 break rows, signature constant (0,1)).
      (D2) k=36 TWENTY-SEVENTH tail (kit-added registration, EVEN
           form, even-z supply chain candidate 9/9): identity
           v(s,37,37) =? v(s,36,37) over s in {0} U {12..70}:
           hold {0} U {12..35}, break 0v2 at s=36, then UNIFORM 2v1
           for ALL s in {37..70} (closed-form scan during drafting
           confirmed 35 break rows: the 0v2 point then constant (2,1)).
      The z=35/z=36-slice supply data for the future declaration
      lanes is thereby precomputed.
(E) RECHECK ANCHORS (published engine values only): the four z=27
    z26f20 handoff spots (0,1,1,0) and the three published
    frontier-record separations H(39;{13,14};25)=2,
    H(40;{13,14};26)=1, H(41;(14,14);26)=2.
(F) K0832 battery: every single-token literal used by this file's
    derivations and measured collapses (frontier and past-row first
    co-token shapes, spot-table children, recheck anchors, supply
    identity samples), checked closed-form vs canonical-engine vs
    ordered-engine. Candidate: all match.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z27z34_frontier.out).
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

ORDINAL = {35: 'twentysixth', 36: 'twentyseventh'}


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
    # (F) K0832 battery: every single-token literal used by this file.
    battery_lits = []
    # frontier/past-row first co-token + co-equal shape collapses
    for (x, z2, R2) in [(31, 29, 45), (30, 29, 45), (32, 30, 47),
                        (35, 33, 51), (34, 33, 51), (36, 34, 53),
                        (37, 34, 53), (28, 27, 42), (29, 27, 42),
                        (27, 27, 41), (26, 27, 41), (28, 28, 43),
                        (29, 28, 43), (27, 28, 42), (26, 28, 42),
                        (31, 30, 46), (30, 30, 46), (32, 31, 48),
                        (33, 31, 48)]:
        battery_lits.append((x, z2, R2))
    # z=28 spot tables: collapses and C-child published literals
    for (x, z2, R2) in [(35, 28, 46), (33, 28, 45), (36, 28, 47),
                        (34, 28, 46), (36, 27, 46), (34, 27, 45),
                        (46, 27, 27)]:
        battery_lits.append((x, z2, R2))
    # recheck anchor collapses (z=25/26/27 published)
    for (x, z2, R2) in [(27, 25, 39), (27, 26, 40), (28, 26, 41),
                        (35, 27, 45), (33, 27, 44)]:
        battery_lits.append((x, z2, R2))
    # supply identity sample points (k=35 odd form, k=36 even form)
    for (x, z2, R2) in [(12, 36, 36), (35, 36, 36), (36, 36, 36),
                        (35, 35, 36), (36, 35, 36), (69, 36, 36),
                        (69, 35, 36), (12, 37, 37), (36, 37, 37),
                        (36, 36, 37), (37, 37, 37), (70, 37, 37),
                        (70, 36, 37)]:
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
    # (A) FRONTIER-ROW RECORDS — parity-split candidate datums 3..6
    out.append(row_record_x0(
        'frontier_m15_z29_row_record',
        'frontier_record_m15_z29_at_its_own_frontier_zstar15_equals_29_PREDECLARED_PARITY_SPLIT_datum3',
        {'co_token_15_allowed': True,
         'law_candidate': 'z26f20 S5 item #1 parity-corrected frontier-record law candidate (two published data points: m=13@z=25 {13,14}@S=27 UP 2v0; m=14@z=26 (14,14)@S=28 UP 2v1); prediction frozen BEFORE the run: EXACTLY ONE separation X={15,16} @S=31 UP 2v0 (collapse v(31,29,45)=0), other 49 shapes conform; recorded verbatim whatever it is',
         's_domain': '{15..53}', 'arity_max': 3,
         'derived_shape_count': 50,
         'style': 'x0 published residual-band style'},
        45, 29, 15, 15, 53))
    out.append(row_record_x0(
        'frontier_m16_z30_row_record',
        'frontier_record_m16_z30_at_its_own_frontier_zstar16_equals_30_PREDECLARED_PARITY_SPLIT_datum4',
        {'co_token_16_allowed': True,
         'law_candidate': 'parity-split prediction frozen BEFORE the run: EXACTLY ONE separation X=(16,16) @S=32 UP 2v1 (collapse v(32,30,47)=1), other 39 shapes conform; recorded verbatim whatever it is',
         's_domain': '{16..54}', 'arity_max': 3,
         'derived_shape_count': 40,
         'style': 'x0 published residual-band style'},
        47, 30, 16, 16, 54))
    out.append(row_record_x0(
        'frontier_m17_z33_row_record',
        'frontier_record_m17_z33_at_its_own_frontier_zstar17_equals_33_PREDECLARED_PARITY_SPLIT_datum5',
        {'co_token_17_allowed': True,
         'law_candidate': 'parity-split prediction frozen BEFORE the run: EXACTLY ONE separation X={17,18} @S=35 UP 2v0 (collapse v(35,33,51)=0), other 31 shapes conform; recorded verbatim whatever it is',
         's_domain': '{17..55}', 'arity_max': 3,
         'derived_shape_count': 32,
         'style': 'x0 published residual-band style'},
        51, 33, 17, 17, 55))
    out.append(row_record_x0(
        'frontier_m18_z34_row_record',
        'frontier_record_m18_z34_at_its_own_frontier_zstar18_equals_34_PREDECLARED_PARITY_SPLIT_datum6',
        {'co_token_18_allowed': True,
         'law_candidate': 'parity-split prediction frozen BEFORE the run: EXACTLY ONE separation X=(18,18) @S=36 UP 2v1 (collapse v(36,34,53)=1), other 25 shapes conform; recorded verbatim whatever it is',
         's_domain': '{18..56}', 'arity_max': 3,
         'derived_shape_count': 26,
         'style': 'x0 published residual-band style'},
        53, 34, 18, 18, 56))
    # (B) ONE-PAST / FARTHER-PAST ROW RECORDS — first contacts, NO
    #     CANDIDATE (non-binding expectations frozen in the docstring)
    out.append(row_record_x0(
        'past_m13_z27_row_record_TWO_PAST',
        'two_past_record_m13_z27_NO_CANDIDATE_first_contact_registered_z26f20_S5_item2',
        {'co_token_13_allowed': True,
         'note': 'z*(13)=25 so z=27 is TWO past the frontier (the S5 item #2 registration listed it under the one-past item; honest label here TWO-PAST); published m=13 separation trajectory: z=25 {13,14}@S=27 UP 2v0, z=26 UP 1v0; z=27 collapse of {13,14}@S=27 is v(27,27,41)=2; separation list recorded verbatim whatever it is',
         's_domain': '{13..51}', 'arity_max': 3,
         'derived_shape_count': 76,
         'style': 'x0 published residual-band style'},
        41, 27, 13, 13, 51))
    out.append(row_record_x0(
        'past_m14_z27_row_record_ONE_PAST',
        'one_past_record_m14_z27_NO_CANDIDATE_first_contact_registered_z26f20_S5_item2',
        {'co_token_14_allowed': True,
         'note': 'z*(14)=26 so z=27 is ONE past (the true second one-past datum); NON-BINDING drop-rule expectation frozen BEFORE the run: at-frontier separation (14,14)@S=28 UP 2v1 (collapse v(28,26,41)=1) persists with value drop 2->1, which at z=27 (collapse v(28,27,42)=1) would be CONFORM-INVISIBLE (1v1) i.e. the row would show NO separation; recorded verbatim whatever it is',
         's_domain': '{14..52}', 'arity_max': 3,
         'derived_shape_count': 62,
         'style': 'x0 published residual-band style'},
        42, 27, 14, 14, 52))
    out.append(row_record_x0(
        'past_m15_z30_row_record_ONE_PAST',
        'one_past_record_m15_z30_NO_CANDIDATE_kit_added_first_contact',
        {'co_token_15_allowed': True,
         'note': 'z*(15)=29 so z=30 is ONE past (kit-added section); NON-BINDING drop-rule expectation: {15,16}@S=31 persists with value 2->1 UP 1v0 visible (collapse v(31,30,46)=0); recorded verbatim whatever it is',
         's_domain': '{15..53}', 'arity_max': 3,
         'derived_shape_count': 50,
         'style': 'x0 published residual-band style'},
        46, 30, 15, 15, 53))
    out.append(row_record_x0(
        'past_m16_z31_row_record_ONE_PAST',
        'one_past_record_m16_z31_NO_CANDIDATE_kit_added_first_contact',
        {'co_token_16_allowed': True,
         'note': 'z*(16)=30 so z=31 is ONE past (kit-added section); NON-BINDING drop-rule expectation: (16,16)@S=32 value 2->1 would be CONFORM-INVISIBLE (collapse v(32,31,48)=1); recorded verbatim whatever it is',
         's_domain': '{16..54}', 'arity_max': 3,
         'derived_shape_count': 40,
         'style': 'x0 published residual-band style'},
        48, 31, 16, 16, 54))
    out.append(row_record_x0(
        'past_m13_z28_row_record_THREE_PAST',
        'three_past_record_m13_z28_NO_CANDIDATE_kit_added_first_contact',
        {'co_token_13_allowed': True,
         'note': 'z*(13)=25 so z=28 is THREE past (kit-added section, NO CANDIDATE); recorded verbatim whatever it is',
         's_domain': '{13..51}', 'arity_max': 3,
         'derived_shape_count': 76,
         'style': 'x0 published residual-band style'},
        42, 28, 13, 13, 51))
    out.append(row_record_x0(
        'past_m14_z28_row_record_TWO_PAST',
        'two_past_record_m14_z28_NO_CANDIDATE_kit_added_first_contact',
        {'co_token_14_allowed': True,
         'note': 'z*(14)=26 so z=28 is TWO past (kit-added section, NO CANDIDATE); recorded verbatim whatever it is',
         's_domain': '{14..52}', 'arity_max': 3,
         'derived_shape_count': 62,
         'style': 'x0 published residual-band style'},
        43, 28, 14, 14, 52))
    # (C) m=18 base-spot z-sequence z=28 touch — four first-ever z=28
    #     engine touches with option tables frozen before the run
    t1 = H(46, tuple(sorted((17, 18), reverse=True)), 28)
    t2 = H(45, tuple(sorted((16, 17), reverse=True)), 28)
    t3 = H(47, (18, 18), 28)
    t4 = H(46, (17, 17), 28)
    out.append({'section': 'z28_basespot_touch',
                'label': 'z26f20_S5_item4_registered_blind_option_tables_first_ever_z28_engine_touches',
                'spots': [
                    {'id': 't1', 'X': [17, 18], 'R': 46, 'z': 28,
                     'value': t1, 'collapse': v(35, 28, 46),
                     'role': 'm=17-row z=28 first co-token member; BLIND candidate collapse-conform 0 = v(35,28,46)',
                     'match': t1 == v(35, 28, 46)},
                    {'id': 't2', 'X': [16, 17], 'R': 45, 'z': 28,
                     'value': t2, 'collapse': v(33, 28, 45),
                     'role': 'm=16-row z=28 first co-token member; BLIND candidate collapse-conform 1 = v(33,28,45)',
                     'match': t2 == v(33, 28, 45)},
                    {'id': 't3', 'X': [18, 18], 'R': 47, 'z': 28,
                     'value': t3, 'collapse': v(36, 28, 47),
                     'role': 'm=18 base-spot on-line member; frozen option table {B-child = t1 (in-kit first-contact premise disclosed), C-child 1^H(46;(18,18);27)=1^1=0 PUBLISHED z26f20 h3}; candidate mex{t1,0}=1 = collapse v(36,28,47) CONFORMING iff t1 conforms 0',
                     'match': t3 == v(36, 28, 47)},
                    {'id': 't4', 'X': [17, 17], 'R': 46, 'z': 28,
                     'value': t4, 'collapse': v(34, 28, 46),
                     'role': 'm=17 base-spot on-line member; frozen option table {B-child = t2 (in-kit premise disclosed), C-child 1^H(45;(17,17);27)=1^0=1 PUBLISHED z26f20 h4}; candidate mex{t2,1}=0 = collapse v(34,28,46) CONFORMING iff t2 conforms 1',
                     'match': t4 == v(34, 28, 46)}],
                'published_anchor': 'm=18 base-spot on-line z-sequence z in {16..27} = 0,1,0,1,0,1,0,1,1,1,1,1 (published incl. the z=27 value by the z26f20 h3); m=17 z-sequence z in {16..27} = 0,0,0,0,0,0; on conform the z=28 members are t3(m=18) and t4(m=17)'})
    # (E) recheck anchors — published engine values only
    rechecks = []
    for (R, X, z2, expected) in [
            (45, (17, 18), 27, 0), (44, (16, 17), 27, 1),
            (46, (18, 18), 27, 1), (45, (17, 17), 27, 0),
            (39, (13, 14), 25, 2), (40, (13, 14), 26, 1),
            (41, (14, 14), 26, 2)]:
        XX = tuple(sorted(X, reverse=True))
        hv = H(R, XX, z2)
        S = sum(X)
        ev = v(S, z2, R)
        rechecks.append({'R': R, 'X': list(XX), 'z': z2,
                         'value': hv, 'collapse': ev,
                         'published_value': expected,
                         'match': hv == ev == expected})
    out.append({'section': 'published_recheck_anchors', 'rows': rechecks})
    # (D) tail supply pre-computations (pure closed form, engine-free)
    for k in (35, 36):
        if k == 35:
            dom = [0] + list(range(12, 70))
            secname = 'twentysixth_tail_supply_identity_precalc'
            lab = ('registered_candidate_odd_form_9of9_z26f20_S5_item3')
            note = ('REGISTERED candidate (z26f20 kit log S5 item #3, commit 68bc863d): hold {0} U {12..35}, then UNIFORM 0v1 for ALL s in {36..69}; odd-z supply chain candidate 9/9 (k=19/21/23/25/27/29/31/33 prior closed-form + k=35 here); the z=35-slice supply datum precomputed for the future z=35 declaration lane')
        else:
            dom = [0] + list(range(12, 71))
            secname = 'twentyseventh_tail_supply_identity_precalc'
            lab = ('kit_added_registration_even_form_9of9')
            note = ('NEW registration by this kit: hold {0} U {12..35}, break 0v2 at s=36, then UNIFORM 2v1 for ALL s in {37..70}; even-z supply chain candidate 9/9 (k=20/22/24/26/28/30/32/34 published + k=36 closed-form here); the z=36-slice supply datum precomputed for the future z=36 declaration lane')
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
