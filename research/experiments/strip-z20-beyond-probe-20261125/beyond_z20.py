#!/usr/bin/env python3
"""
beyond_z20: FROZEN z=20 beyond/frontier spot-probe kit. The discriminating
z=20 data points for the observation series opened by the z18-min13
census and the z19 beyond/frontier probe kit. NO K slot, NO universal
claim: everything is finite machine observation against the pinned
engine, plus engine-free closed-form pre-computations. Publish-then-
execute.

PREDECLARED CANDIDATE OUTCOMES (written BEFORE the first run):

  (1) m=10-row z=20 (+2 beyond; the diagonal (10,10) arc: UP 2v1 @z18
      frontier -> DOWN 0v1 @z19): candidates (a) REABSORB (the (8,8)
      diagonal arc died at +3: UP@z14 -> DOWN@z15 -> DOWN@z16 -> gone
      @z17; (10,10) is one slice behind, so gone@z20 is the analogy
      candidate), (b) persist DOWN (2-slice-per-position lag of the
      published flip/reabsorb alternation), (c) flip back UP. A new
      even-m gap+2 birth (10,12) is a further candidate (the (8,10)
      arc was born at gap+2 at z=16).
  (2) m=9-row z=20 (+3 beyond; (9,10) UP 2v0 @z17 frontier -> UP 1v0
      @z18 (decay, no reabsorb) -> DOWN 1v2 @z19; NEW (9,12) UP 2v0
      born @z19 at gap +3): candidates: (9,10) reabsorb @z20 (the
      published odd-m beyond separations persist at fixed position but
      the (8,*) arcs show 2-slice reabsorption), (9,12) persist/flip/
      reabsorb. Predictions NOT fixed: both directions recorded.
  (3) m=8-row z=20 (+6 beyond): the beyond set was EMPTY at z=18
      (first empty) and z=19; candidate: remains empty (no re-emergence
      has ever been observed in the series after total reabsorption).
  (4) m=11-row z=20 record: the FOURTH AND FINAL published-entry slot
      of the K1322 residual band m=11 z in {17..20} (z=17/z=18/z=19
      entries all 110 shapes, 0 separations); candidate 0 separations,
      110 shapes (identical enumeration, machine-checked).
  (5) m=12-row z=20 record: THIRD entry of the K1325 residual band m=12
      z in {18..21} (92/92 @z18/z=19); candidate 92 shapes 0 seps.
  (6) m=13-row z=20 record: SECOND entry of the K1328 residual band
      m=13 z in {19..24} (76/75 @z19); candidates 76 (arity<=3
      published residual-band style) and 75 (arity<=4 co-token
      extension) shapes, 0 seps.
  (7) strip spots m in {14..18} at the z=20 slice claim positions
      R=m+21: candidate all-match (15/15 at z=19 published).
  (8) m=15 base spot H(36;(15,15);20): the cross-floor base-spot
      sequence is 0 (z16), 1 (z17), 0 (z18), 1 (z19) -> z-parity
      candidate 0 at z=20.
  (9) ELEVENTH-tail supply identity RECHECK (engine-free): the z19
      census kit pre-computed v(s,21,21)=v(s,20,21) holding on
      {0} U {12..19} with break at s=20 as 0v2 then uniform 2v1 for
      all s>=21 (the exact z=18 even-z identity shape); rechecked
      here over the same domain, frozen cross-artifact consistency.
  (10) TWELFTH-tail supply identity PRE-COMPUTATION (engine-free, NEW):
      v(s,22,22) vs v(s,21,22) over s in {0} U {12..57}. PREDECLARED
      candidate: z=21 is odd, and the odd-z supply identities measured
      so far break uniformly 0v1 from s=z+1 (z=17: hold {0}U{12..17},
      uniform 0v1 from s=18; z=19: hold {0}U{12..19}, uniform 0v1 from
      s=20; 2/2), so the candidate is hold {0} U {12..21} with uniform
      0v1 break for all s>=22. Constants recorded whatever they are.

Everything is a pure function of the pinned engine bytes; no randomness,
no hash-seed dependence, no wall-clock in the output. stdout is the
frozen artifact (beyond_z20.out).
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
    z16-min9 section (e) / z18-min13 sections (d3)-(d5) / beyond_z19:
    arity up to 4 total tokens, co-token m possible)."""
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


def row_record_x0(sec, rlabel, extra, R, z, m, smin, smax):
    """published residual-band record style (z17-min12 / z18-min13 /
    z19-min14 kit sections (d)): X = parts(S, m, 3) with X[0] == m,
    all parts >= m with co-token m allowed, arity <= 3 TOTAL."""
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
    # (1) m=10-row z=20 beyond record (identical published enumeration:
    #     the beyond_z19 m=10 z=19 record measured 170 shapes).
    out.append(row_record(
        'm10_row_z20_beyond_record',
        'observational_only_beyond_frontier_zstar10_18_lt_20_second_even_m10_beyond_slice',
        {'published_anchors': 'm=10 z=18 FRONTIER (z18-min13 kit): 170 shapes 1 separation (10,10) UP 2v1; m=10 z=19 (+1 beyond, beyond_z19 kit): 170 shapes 1 separation (10,10) DOWN 0v1; identical enumeration -> same 170 shapes',
         's_domain': '{10..48}', 'arity_max': 4,
         'predeclared_candidates': 'reabsorb / persist DOWN / flip UP / (10,12) birth at gap+2'},
        31, 20, 10, 10, 48, 10))
    # (2) m=9-row z=20 beyond record (identical published enumeration:
    #     234 shapes at z=17/z=18/z=19).
    out.append(row_record(
        'm9_row_z20_beyond_record',
        'observational_only_beyond_frontier_zstar9_17_lt_20_third_odd_m9_beyond_slice',
        {'published_anchors': 'm=9 z=17 frontier: (9,10) UP 2v0; z=18 beyond: (9,10) UP 1v0 (decay, persist); z=19 beyond (beyond_z19 kit): (9,10) DOWN 1v2 + NEW (9,12) UP 2v0 born at gap+3; identical enumeration -> same 234 shapes',
         's_domain': '{9..47}', 'arity_max': 4,
         'predeclared_candidates': '(9,10) reabsorb-or-persist; (9,12) persist/flip/reabsorb'},
        30, 20, 9, 9, 47, 9))
    # (3) m=8-row z=20 beyond record (identical published enumeration:
    #     362 shapes; z=18/z=19 both measured 0 separations).
    out.append(row_record(
        'm8_row_z20_beyond_record',
        'observational_only_beyond_frontier_zstar8_14_lt_20_sixth_slice_empty_candidate',
        {'published_anchors': 'z=14 frontier (8,8) UP; z=15 (8,8) DOWN; z=16 {(8,8) DOWN, (8,10) UP}; z=17 {(8,10) DOWN}; z=18 EMPTY; z=19 EMPTY; identical enumeration -> same 362 shapes',
         's_domain': '{8..47}', 'arity_max': 4,
         'predeclared_candidates': 'remains empty (no re-emergence ever observed)'},
        29, 20, 8, 8, 47, 8))
    # (4) m=11-row z=20 record: FOURTH AND FINAL entry of the K1322
    #     published residual band m=11 z in {17..20}.
    out.append(row_record_x0(
        'inband_m11_z20_row_record',
        'observational_only_k1322_residual_m11_z20_fourth_final_entry_zstar11_21_gt_20',
        {'co_token_11_allowed': True,
         'residual_band': 'K1322 published m=11 z in {17..20}; z=17/z=18/z=19 entries measured 110 shapes each, separations 0 (same enumeration -> same 110 shapes here); z=21 is the frontier z*(11)=21',
         's_domain': '{11..49}', 'arity_max': 3, 'style': 'x0 published residual-band style',
         'predeclared_candidates': '110 shapes 0 separations'},
        32, 20, 11, 11, 49))
    # (5) m=12-row z=20 record: THIRD entry of the K1325 published
    #     residual band m=12 z in {18..21}.
    out.append(row_record_x0(
        'inband_m12_z20_row_record',
        'observational_only_k1325_residual_m12_z20_third_entry_zstar12_22_gt_20',
        {'co_token_12_allowed': True,
         'residual_band': 'K1325 published m=12 z in {18..21}; z=18/z=19 entries measured 92 shapes each, separations 0 (same enumeration -> same 92 shapes here)',
         's_domain': '{12..50}', 'arity_max': 3, 'style': 'x0 published residual-band style',
         'predeclared_candidates': '92 shapes 0 separations'},
        33, 20, 12, 12, 50))
    # (6) m=13-row z=20 record: SECOND entry of the K1328 published
    #     residual band m=13 z in {19..24} (frontier z=25).
    out.append(row_record_x0(
        'inband_m13_z20_row_record',
        'observational_only_k1328_residual_m13_z20_second_entry_zstar13_25_gt_20',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; z=19 entry (z19-min14 census kit) measured 76 shapes 0 seps + arity<=4 ext 75/0 (same enumeration)',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style',
         'predeclared_candidates': '76 shapes 0 separations'},
        34, 20, 13, 13, 51))
    out.append(row_record(
        'inband_m13_z20_row_record_ext_arity4',
        'observational_only_arity_le4_extension_of_the_m13_z20_record_cotoken_style',
        {'co_token_13_allowed': True,
         's_domain': '{13..51}', 'arity_max': 4,
         'predeclared_candidates': '75 shapes 0 separations'},
        34, 20, 13, 13, 51, 13))
    # (7) strip spots m in {14..18} at the z=20 slice claim positions
    spots = []
    for m in range(14, 19):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 21, X, 20)
            ev = v(S, 20, m + 21)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m14_18_z20', 'rows': spots,
                'predeclared_candidates': 'all match (z=19 published 15/15)'})
    # (8) m=15 base spot at the z=20 slice base position
    w = H(36, (15, 15), 20)
    wv = v(30, 20, 36)
    out.append({'section': 'm15_base_spot', 'X': [15, 15], 'R': 36,
                'z': 20, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'predeclared_candidates': 'z-parity candidate 0 (published sequence 0 z16 / 1 z17 / 0 z18 / 1 z19)'})
    # (9) ELEVENTH-tail supply identity RECHECK (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 57)):
        a = v(s, 21, 21)
        b = v(s, 20, 21)
        row = {'s': s, 'v_21_21': a, 'v_20_21': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'eleventh_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,21,21) =? v(s,20,21)',
                's_domain': '{0} U {12..56}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'z19-min14 census kit section (g2): holds {0} U {12..19}, breaks at s=20 as 0v2, then uniform 2v1 for all s>=21 (the exact z=18 even-z identity shape)',
                'hold_rows': holds, 'break_rows': breaks})
    # (10) TWELFTH-tail supply identity PRE-COMPUTATION (NEW)
    t_holds = []
    t_breaks = []
    for s in [0] + list(range(12, 58)):
        a = v(s, 22, 22)
        b = v(s, 21, 22)
        row = {'s': s, 'v_22_22': a, 'v_21_22': b, 'equal': a == b}
        (t_holds if a == b else t_breaks).append(row)
    out.append({'section': 'twelfth_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z21_slice_supply_k0832',
                'identity': 'v(s,22,22) =? v(s,21,22)',
                's_domain': '{0} U {12..57}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'odd z=21: hold {0} U {12..21} with uniform 0v1 break for all s>=22 (odd-z form 2/2 published: z=17 and z=19 identities hold through s=z then break uniform 0v1)',
                'hold_rows': t_holds, 'break_rows': t_breaks})
    res = {'result': 'PROBE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
