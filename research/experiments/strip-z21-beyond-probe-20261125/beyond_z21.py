#!/usr/bin/env python3
"""
beyond_z21: FROZEN z=21 beyond/frontier spot-probe kit. The discriminating
z=21/z=22 data points for the observation series opened by the z18-min13
census and the z19/z20 beyond/frontier probe kits. NO K slot, NO universal
claim: everything is finite machine observation against the pinned
engine, plus engine-free closed-form pre-computations. Publish-then-
execute.

PREDECLARED CANDIDATE OUTCOMES (written BEFORE the first run):

  (1) m=11-row z=21 FRONTIER record (z=21 = z*(11) by the published K1268
      formula z*(m)=2m-2+(m mod 2): the THIRD frontier slice of the strip
      series after m=9@z=17 and m=10@z=18). The frontier parity rule
      candidate: odd-m frontier carries a SINGLE (m,m+1) UP separation
      (m=9 z=17: (9,10) UP 2v0, 1/1); even-m frontier carries a single
      (m,m) diagonal UP (m=10 z=18: (10,10) UP 2v1). Candidate: exactly
      one separation X=(11,12) UP, direction/value constants recorded
      whatever they are (the z=17 constants are the only published
      odd-m frontier datum).
  (2) m=12-row z=22 FRONTIER record (z=22 = z*(12)): the FOURTH frontier
      slice and the SECOND even-m frontier datum. Candidate: exactly one
      separation X=(12,12) UP 2v1 (the m=10 z=18 form). This is a z=22
      measurement OUTSIDE the published z22-min17 census kit (which
      swept strip m in {17..21} and residual rows m=16/15/14/13 only).
  (3) m=10-row z=21 (+3 beyond; the arc: z=18 FRONTIER (10,10) UP 2v1 ->
      z=19 +1 (10,10) DOWN 0v1 -> z=20 +2 {(10,10) DOWN 0v1 persist +
      (10,12) UP 2v1 BORN}): candidates (a) (10,10) reabsorb (the (8,8)
      diagonal arc died at its +3), (b) persist DOWN a third slice,
      (c) flip; (d) (10,12) persist/flip/reabsorb; (e) new gap+4 birth
      (10,14) - no gap+4 birth has ever been observed (births: gap+2
      even-m (8,10)@z16/(10,12)@z20, gap+3 odd-m (9,12)@z19).
  (4) m=9-row z=21 (+4 beyond; the arc: z=17 FRONTIER (9,10) UP 2v0 ->
      z=18 (9,10) UP 1v0 decay -> z=19 {(9,10) DOWN 1v2 + (9,12) UP 2v0
      born} -> z=20 {(9,12) UP 1v0 singleton, (9,10) reabsorbed}):
      candidates for (9,12): second decay (2->1->0v-? i.e. reabsorb-or-
      collapse-to-value-equality has never been observed mid-arc),
      persist 1v0, flip DOWN; new births at further gap recorded as
      they are.
  (5) m=8-row z=21 (+7 beyond; the arc: z=14 FRONTIER (8,8) UP ->
      z=15 (8,8) DOWN -> z=16 {(8,8) DOWN + (8,10) UP} -> z=17 {(8,10)
      DOWN} SHRINK -> z=18 EMPTY -> z=19 EMPTY -> z=20 RE-EMERGENCE
      {(8,12) DOWN 0v2 + (8,14) UP 2v1}): candidates: the re-emergent
      pair persists / flips / is reabsorbed (a SECOND re-emergence has
      never been observed; the z=20 event was the first); further
      births recorded as they are.
  (6) m=11-row z=22 beyond record (the FIRST beyond slice of the m=11
      arc, one slice after this kit's frontier record (1)): the
      published +1-beyond behaviors are m=9 UP 2v0 -> UP 1v0 (decay,
      persist) and m=10 UP 2v1 -> DOWN 0v1 (flip): candidates
      persist-decay / flip / reabsorb for the frontier separation,
      plus possible new births.
  (7) FIFTEENTH-tail supply identity RECHECK (engine-free): the z22
      census kit pre-computed v(s,25,25)=v(s,24,25) holding on
      {0} U {12..23} with break at s=24 as 0v2 then uniform 2v1 for all
      s>=25 (the K1334 theorem A k=24 even form); rechecked here over
      {0} U {12..60}, frozen cross-artifact consistency.
  (8) SIXTEENTH-tail supply identity PRE-COMPUTATION (engine-free, NEW):
      v(s,26,26) vs v(s,25,26) over s in {0} U {12..61}. PREDECLARED
      candidate (K1334 theorem A k=25 odd-instance, engine-free,
      machine-checked k<=140): hold exactly on {0} U {12..25}, uniform
      0v1 break for all s>=26 - the odd-z supply-identity form is 4/4
      measured so far (z=17, z=19, z=21-supply, z=23-supply published)
      and this is the z=25-supply datum. Constants recorded whatever
      they are.

Everything is a pure function of the pinned engine bytes; no randomness,
no hash-seed dependence, no wall-clock in the output. stdout is the
frozen artifact (beyond_z21.out).
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
Ho = ns['H_ordered']
v = ns['single_token']


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


def row_record(sec, rlabel, extra, R, z, m, smin, smax, min_tok):
    """frontier/beyond parameter style sweep: X = (m,) U parts >= min_tok.
    The published frontier-record enumeration form (z14pre section (d) /
    z16-min9 section (e) / z18-min13 sections (d3)-(d5) / beyond_z19/
    beyond_z20: arity up to 4 total tokens, co-token m possible)."""
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(max(S - m, 0), min_tok, 3):
            XX = tuple(sorted((m,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(R, XX, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(XX), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return {'section': sec, 'label': rlabel, 'R': R, 'z': z, 'min': m,
            **extra, 'shapes': scnt, 'separations': sep}


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    # (1) m=11-row z=21 FRONTIER record (z*(11)=21, the third frontier
    #     slice of the series; identical enumeration form to the
    #     published m=9 z=17 / m=10 z=18 frontier records).
    out.append(row_record(
        'm11_row_z21_frontier_record',
        'observational_only_frontier_slice_zstar11_equals_21_second_odd_frontier',
        {'co_token_11_allowed': True,
         'published_anchors': 'm=9 z=17 frontier (z16-min9 kit): 234 shapes exactly 1 separation X=(9,10) UP 2v0 (odd-m frontier rule 1/1); m=10 z=18 frontier (z18-min13 kit): 170 shapes exactly 1 separation X=(10,10) UP 2v1 (even-m frontier rule 1/1); m=11 rows z in {17..20}: 110 shapes each, 0 separations (residual-band style, K1322 published, band CLOSED at z=20)',
         's_domain': '{11..49}', 'arity_max': 4,
         'predeclared_candidates': 'exactly one separation X=(11,12) UP (odd-m frontier rule 2/2 candidate); constants recorded as measured'},
        33, 21, 11, 11, 49, 11))
    # (2) m=12-row z=22 FRONTIER record (z*(12)=22; fourth frontier slice;
    #     second even-m frontier datum; OUTSIDE the published z22-min17
    #     census kit sweeps).
    out.append(row_record(
        'm12_row_z22_frontier_record',
        'observational_only_frontier_slice_zstar12_equals_22_second_even_frontier',
        {'co_token_12_allowed': True,
         'published_anchors': 'm=10 z=18 frontier: exactly 1 separation X=(10,10) UP 2v1 (even-m frontier rule 1/1); m=12 rows z in {18..21}: 92 shapes each, 0 separations (K1325 published residual band, CLOSED at z=21)',
         's_domain': '{12..50}', 'arity_max': 4,
         'predeclared_candidates': 'exactly one separation X=(12,12) UP 2v1 (even-m frontier rule 2/2 candidate); constants recorded as measured'},
        35, 22, 12, 12, 50, 12))
    # (3) m=10-row z=21 beyond record (identical published enumeration:
    #     170 shapes at z=18/z=19/z=20).
    out.append(row_record(
        'm10_row_z21_beyond_record',
        'observational_only_beyond_frontier_zstar10_18_lt_21_third_even_m10_beyond_slice',
        {'published_anchors': 'm=10 z=18 FRONTIER: (10,10) UP 2v1; z=19 (+1): (10,10) DOWN 0v1; z=20 (+2): {(10,10) DOWN 0v1 persist + (10,12) UP 2v1 born}; identical enumeration -> same 170 shapes',
         's_domain': '{10..48}', 'arity_max': 4,
         'predeclared_candidates': '(10,10) reabsorb (8,8 arc precedent died at +3) / persist DOWN / flip; (10,12) persist/flip/reabsorb; new (10,14) gap+4 birth possible (first ever)'},
        32, 21, 10, 10, 48, 10))
    # (4) m=9-row z=21 beyond record (identical published enumeration:
    #     234 shapes at z=17..z=20).
    out.append(row_record(
        'm9_row_z21_beyond_record',
        'observational_only_beyond_frontier_zstar9_17_lt_21_fourth_odd_m9_beyond_slice',
        {'published_anchors': 'm=9 z=17 frontier: (9,10) UP 2v0; z=18: (9,10) UP 1v0 (decay, persist); z=19: {(9,10) DOWN 1v2 + (9,12) UP 2v0 born}; z=20: {(9,12) UP 1v0 singleton, (9,10) reabsorbed}; identical enumeration -> same 234 shapes',
         's_domain': '{9..47}', 'arity_max': 4,
         'predeclared_candidates': '(9,12) persist 1v0 / decay / flip DOWN / reabsorb; new births recorded as they are'},
        31, 21, 9, 9, 47, 9))
    # (5) m=8-row z=21 beyond record (identical published enumeration:
    #     362 shapes; z=18/z=19 empty, z=20 re-emergence).
    out.append(row_record(
        'm8_row_z21_beyond_record',
        'observational_only_beyond_frontier_zstar8_14_lt_21_seventh_slice_post_reemergence',
        {'published_anchors': 'z=14 frontier (8,8) UP; z=15 (8,8) DOWN; z=16 {(8,8) DOWN, (8,10) UP}; z=17 {(8,10) DOWN}; z=18 EMPTY; z=19 EMPTY; z=20 RE-EMERGENCE {(8,12) DOWN 0v2 + (8,14) UP 2v1} (first re-emergence of the series); identical enumeration -> same 362 shapes',
         's_domain': '{8..47}', 'arity_max': 4,
         'predeclared_candidates': 'the re-emergent pair persists / flips / is reabsorbed; a SECOND re-emergence never observed; further births recorded as they are'},
        30, 21, 8, 8, 47, 8))
    # (6) m=11-row z=22 beyond record: the FIRST beyond slice of the
    #     m=11 arc (one slice after the frontier record (1)).
    out.append(row_record(
        'm11_row_z22_beyond_record',
        'observational_only_beyond_frontier_zstar11_21_lt_22_first_beyond_slice_of_the_m11_arc',
        {'co_token_11_allowed': True,
         'published_anchors': 'published +1-beyond behaviors: m=9 UP 2v0 -> UP 1v0 (decay, persist); m=10 UP 2v1 -> DOWN 0v1 (flip); the m=11 arc opens with this measurement (after the z=21 frontier record in this kit)',
         's_domain': '{11..49}', 'arity_max': 4,
         'predeclared_candidates': 'frontier separation persist-decay / flip / reabsorb; new births recorded as they are'},
        34, 22, 11, 11, 49, 11))
    # (7) FIFTEENTH-tail supply identity RECHECK (pure K0832 closed form)
    f_holds = []
    f_breaks = []
    for s in [0] + list(range(12, 61)):
        a = v(s, 25, 25)
        b = v(s, 24, 25)
        row = {'s': s, 'v_25_25': a, 'v_24_25': b, 'equal': a == b}
        (f_holds if a == b else f_breaks).append(row)
    out.append({'section': 'fifteenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,25,25) =? v(s,24,25)',
                's_domain': '{0} U {12..60}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z22-min17 census kit (115c0bb9): holds {0} U {12..23}, breaks at s=24 as 0v2, then uniformly 2v1 for all s>=25 (K1334 theorem A k=24 even form); rechecked and extended here',
                'hold_rows': f_holds, 'break_rows': f_breaks})
    # (8) SIXTEENTH-tail supply identity PRE-COMPUTATION (NEW)
    s_holds = []
    s_breaks = []
    for s in [0] + list(range(12, 62)):
        a = v(s, 26, 26)
        b = v(s, 25, 26)
        row = {'s': s, 'v_26_26': a, 'v_25_26': b, 'equal': a == b}
        (s_holds if a == b else s_breaks).append(row)
    out.append({'section': 'sixteenth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z25_slice_supply_k0832',
                'identity': 'v(s,26,26) =? v(s,25,26)',
                's_domain': '{0} U {12..61}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'K1334 theorem A k=25 odd-instance (proved, machine-checked k<=140): hold exactly on {0} U {12..25}, uniform 0v1 break for all s>=26 - the odd-z supply-identity form measured 4/4 so far (z=17, z=19, z=21-supply, z=23-supply); this is the z=25-supply datum',
                'hold_rows': s_holds, 'break_rows': s_breaks})
    res = {'result': 'PROBE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
