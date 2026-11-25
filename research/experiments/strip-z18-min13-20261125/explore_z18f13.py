#!/usr/bin/env python3
"""
explore_z18f13: FROZEN PRE-DECLARATION census for the z=18 min>=13
(floor-13) cell ladder and the T-Z18 strip (the K1325 declaration
continuation; NO K slot is claimed by this file;
publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..12 the floor-13 cell
      Cell_j(s) := H(j+19; {j} U Y; 18), Y tokens >= 13, s = sum(Y) in
      {0} U {13..43}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1325
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,18,j+19) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The j=12 rung (small
      token 12, one rank beyond the published z=17 A5-cell A517f12) is
      prefixed A6 as a PROVISIONAL census label; final naming belongs
      to the declaration lane. STRUCTURAL NOTE for the declaration
      lane: the published z=17 (K1325) deviant positions form the set
      {12, 14, 16, 18+} (A17f12/A2 at 12; C17/D at 12; C/E at 14;
      E/G at 14,16; B/D/G at 12,14,16 tails at s>=18). Under the new
      floor 13 EVERY published source position except s=12 survives
      (>= 13), so the FIRST death-point event of the +1-floor-shift
      series is EXPECTED here (the s=12 classes A17f12/C17f12/D17f12/
      B17f12 all fall below the new floor) -- this census probes
      (i) which of the s=12/14/16/18+ classes persist at z=18 with
      which positions/directions/values, (ii) whether a NEW
      above-floor deviant class appears (at z=15/16/17 the new class
      appeared at s = 2z/2z/2z-2...; the ninth-tail supply
      pre-computation (g) measures the candidate supply source), and
      (iii) whether the A-family collapse run restarts / extends
      (A18f13 .. A618f13), which is exactly the T-Z18 base-m=13
      trivial-absorption case: the a=13 child of the T-Z18 base
      position H(32;{13} U Y;18) is precisely the cell-12 domain
      H(31; {12} U Y;18) -- the FOURTH consecutive in-band base child
      (after K1320 min=9, K1322 min=10, K1325 min=11; z*(12)=22>18).
  (b) tail spots: s in {44..51}, single-token shape Y=(s,), all 12
      cells.
  (c) strip sweep (T-Z18 claim position, PROVISIONAL label): m in
      {13..17}, S in {m..m+39}, Y parts tokens >= m, arity(Y) <= 3:
      H(m+19; X; 18) vs v(S,18,m+19). EXHAUSTIVE in-sweep.
  (d) IN-BAND base-child / m=12-row record (the structurally decisive
      section; observational only, NOT a T-Z18 claim position): the
      T-Z18 base m=13 a=13 child lands at (31; {12} U Y; 18) = the
      m=12-row claim position H(31; X; 18), and z=18 is IN BAND for
      min=12 (z*(12) = 22 > 18, published K1325), the FOURTH
      consecutive slice whose base child is in-band. Swept: S in
      {12..50}, all parts >= 12 (co-token 12 shapes INCLUDED, X[0]=12),
      arity <= 3, recorded against the Sigma-collapse v(S,18,31) with
      every separation listed, PLUS an arity<=4 co-token-style
      extension sweep (section inband_m12_z18_row_record_ext_arity4).
      This is simultaneously the FIRST entry
      of the K1325 published residual band m=12 z in {18..21}.
  (d2) IN-BAND m=11-row z=18 record: the SECOND entry of the K1322
      published residual band m=11 z in {17..20} (the z=17 entry was
      measured by the published z17-min12 kit, 110 shapes,
      separation 0). R = 30, all parts >= 11 (co-token 11 allowed,
      X[0]=11), arity <= 3, S in {11..49}, recorded against
      v(S,18,30). z=18 is in band for min=11 (z*(11) = 21 > 18).
  (d4) m=10-row z=18 FRONTIER record (NEW data; observational only):
      z=18 = z*(10) (published: z*(10) = 18, K1320/K1322 era), i.e.
      this is the m=10 FRONTIER slice, the boundary entry of the
      m=10 row. The m=10 rows at z in {16,17} were measured 0
      separations (130 shapes each, published z16-min11 /
      z17-min12 kits) and the floor-10 z=16 full-domain closure
      A416f10 (221 shapes, 0 deviants). The first odd-m frontier data
      point (m=9, z=17 = z*(9)) was published by the z16-min9 kit:
      234 shapes, exactly one separation X=(9,10) UP. This section
      records the even-m m=10 frontier in the published
      frontier-record parameter style: R = 29, S in {10..48},
      X = (10,) U parts(S-10, 10, 3), arity <= 3, against
      v(S,18,29).
  (d3) m=9-row z=18 BEYOND-frontier record (observational only): the
      published series (z=17 FRONTIER 234 shapes, single separation
      (9,10) UP 2>0) extended one slice beyond. Enumeration form
      IDENTICAL to the published z=17 frontier record (S in {9..47},
      X = (9,) U parts(S-9, 9, 3), R = 28) so the separation sets
      compare position-by-position. Second odd-m beyond-frontier
      data point of the strip series.
  (d5) m=8-row z=18 BEYOND record: the FOURTH consecutive beyond-
      frontier data point of the growth-rule series (published: z=15
      beyond 1 separation (8,8) DOWN; z=16 beyond-beyond 2
      separations ((8,8) DOWN persisting + (8,10) UP new); z=17
      beyond SHRINK to exactly {(8,10) DOWN @S=18} -- the first
      SHRINK event, UP/DOWN alternation). R = 26, domain EXACTLY the
      published z=16/z=17 section-(d) form (S in {8..47}, X = (8,) U
      parts(S-8, 8, 3), 362 shapes) so the separation sets compare
      across slices position-by-position. Observational only.
  (e) strip spots: m in {18..21}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=13 base spot X=(13,13) at the T-Z18 base position.
  (f) below-band bottom-rung child census (the z=18 analog of the
      K1320/K1322/K1325 section-(f) census; observational only): the
      j=1 rung's B-move child is the BELOW-BAND position (19; Y; 19)
      (min(Y) >= 13 so R=19 lies deep below z+min(Y) >= 31). At z=17
      the analogous child H(18;Y;18) collapsed over the full floor-12
      census against v(s,18,18) with the published absorption
      identity v(s,18,18)=v(s,17,18) holding on {0} U {12..17} and
      breaking uniformly for s >= 18 (1 vs 0), the F17f12 supply
      source. This section measures the z=18 child directly
      (H(19;Y;19) vs v(s,19,19), s in {0} U {13..43}, arity(Y)
      in 0..4); the proof belongs to the declaration lane.
  (g) NINTH-TAIL SUPPLY PRE-COMPUTATION (NEW section; pure published
      K0832 closed form, NO engine recursion; the key pre-computation
      flagged by the K1325 resume note): the F-family ninth tail form
      prediction question. The +2-shift extrapolation of the z=15
      (sixth form) -> z=17 (eighth form) profile suggests the supply
      identity v(s,19,19)=v(s,18,19) holding on {0} U {13..19} and
      breaking with constant 1-vs-0 tail for s >= 20. PRE-COMPUTED
      REALITY (measured here from the closed form, s in
      {0} U {12..55}): the identity HOLDS exactly on {0} U {12..17},
      BREAKS at s=18 (v=0 vs v=2), and for ALL s >= 19 breaks
      UNIFORMLY as 2 vs 1 -- i.e. the naive +2-shift prediction
      (break start s >= 20, 1-vs-0 tail) is CONTRADICTED by the
      closed form on both counts; the break starts two positions
      EARLIER (s=18, one below even the z=17 break position) and the
      break constants are 0v2 / 2v1 pairs, never 1v0. The deviant
      profile of the F18f13 cell (section a) is the direct resolution
      of what the ninth form actually is; this section is the supply
      data, not a claim.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z18f13.out).
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


def cell_sweep(j, smax):
    """sweep cell_j over s in {0} U {13..smax}; returns (dev, multi, total)"""
    R = j + 19
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(13, smax + 1)):
        ys = [()] if s == 0 else parts(s, 13, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 18)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 18, R)
            if val != exp:
                dev.append({'s': s, 'value': val, 'collapse': exp,
                            'direction': 'UP' if val > exp else 'DOWN',
                            'shapes': len(vals[val])})
    H.cache_clear()
    return dev, multi, total


def row_record(sec, rlabel, extra, R, z, m, smin, smax, min_tok):
    """frontier/beyond parameter style sweep: X = (m,) U parts >= min_tok.

    This is the published frontier-record enumeration form (z14pre
    section (d) / z16-min9 section (e): arity up to 4 total tokens,
    co-token m possible).
    """
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
    """published residual-band record style (z17-min12 kit sections
    (d)/(d2)): position X = parts(S, m, 3) with X[0] == m, i.e. all
    parts >= m with co-token m allowed, arity <= 3 TOTAL. Shape-
    for-shape comparable with the published z=17 m=11/m=10 records."""
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
    cells = {}
    for j in range(1, 13):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5', 'A6'][j - 1]
        dev, multi, total = cell_sweep(j, 43)
        cells[f'cell{j}_{name}18f13'] = {
            'z': 18, 'min': j, 'R': j + 19, 'floor': 13,
            's_domain': '{0} U {13..43}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}18f13',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 13):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6'][j - 1]
        for s in range(44, 52):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 19, X, 18)
            exp = v(s + j, 18, j + 19)
            tail.append({'cell': f'{nm}18f13', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s44_51', 'rows': tail})
    # (c) strip sweep m in 13..17 (T-Z18 claim position, provisional)
    sv = []
    viol = []
    cnt = 0
    for m in range(13, 18):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 19, XX, 18)
                ev = v(S, 18, m + 19)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z18_m13_17', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=12-row record at the z=18 m=12 claim
    #     position (31; X; 18), all parts >= 12 (co-token 12 allowed),
    #     arity <= 3 TOTAL. Observational only: NOT a T-Z18 claim
    #     position. Published residual-band record style.
    out.append(row_record_x0(
        'inband_m12_z18_row_record',
        'observational_only_base_child_in_band_zstar12_22_gt_18_fourth_consecutive',
        {'co_token_12_allowed': True,
         'residual_band': 'K1325 published m=12 z in {18..21}; FIRST entry',
         's_domain': '{12..50}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        31, 18, 12, 12, 50))
    out.append(row_record(
        'inband_m12_z18_row_record_ext_arity4',
        'observational_only_arity_le4_extension_of_the_m12_z18_record_cotoken_style',
        {'co_token_12_allowed': True,
         's_domain': '{12..50}', 'arity_max': 4},
        31, 18, 12, 12, 50, 12))
    # (d2) IN-BAND m=11-row z=18 record: SECOND entry of the K1322
    #      published residual m=11 z in {17..20}, published record
    #      style (the z=17 entry measured 110 shapes, separation 0).
    out.append(row_record_x0(
        'inband_m11_z18_row_record',
        'observational_only_k1322_residual_m11_z18_second_entry_zstar11_21_gt_18',
        {'co_token_11_allowed': True,
         'residual_band': 'K1322 published m=11 z in {17..20}; z=17 entry measured 110 shapes separation 0 (same enumeration -> same 110 shapes here)',
         's_domain': '{11..49}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        30, 18, 11, 11, 49))
    # (d4) m=10-row z=18 FRONTIER record: z=18 = z*(10) boundary slice.
    out.append(row_record(
        'm10_row_z18_frontier_record',
        'observational_only_frontier_slice_zstar10_equals_18_first_even_m10_frontier',
        {'co_token_10_allowed': True,
         'published_anchors': 'm=9 z=17 frontier (z16-min9 kit): 234 shapes exactly 1 separation X=(9,10) UP 2v0; m=10 z=16/17 records: 130/130 shapes 0 separations; A416f10 full-domain closure 221 shapes 0 deviants',
         's_domain': '{10..48}', 'arity_max': 4},
        29, 18, 10, 10, 48, 10))
    # (d3) m=9-row z=18 BEYOND-frontier record: enumeration form
    #      identical to the published z=17 m=9 frontier record.
    out.append(row_record(
        'm9_row_z18_beyondfrontier_record',
        'observational_only_beyond_frontier_zstar9_17_lt_18_second_odd_m_beyond',
        {'published_anchors': 'm=9 z=17 frontier (z16-min9 kit): 234 shapes exactly 1 separation X=(9,10) UP 2v0',
         's_domain': '{9..47}', 'arity_max': 4},
        28, 18, 9, 9, 47, 9))
    # (d5) m=8-row z=18 BEYOND record: fourth consecutive beyond data
    #      point; enumeration form identical to the published z=16/z=17
    #      section-(d) records.
    out.append(row_record(
        'm8_row_z18_beyondfrontier_record',
        'observational_only_beyond_frontier_fourth_slice_zstar8_14_plus_4',
        {'published_anchors': 'z=14 frontier (8,8) UP; z=15 beyond (8,8) DOWN; z=16 beyond-beyond {(8,8) DOWN, (8,10) UP}; z=17 beyond SHRINK {(8,10) DOWN @S=18}',
         's_domain': '{8..47}', 'arity_max': 4},
        26, 18, 8, 8, 47, 8))
    # (e) strip spots m in 18..21
    spots = []
    for m in range(18, 22):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 19, X, 18)
            ev = v(S, 18, m + 19)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m18_21', 'rows': spots})
    # m=13 base spot (S=26, both 13-tokens) at the T-Z18 base position
    w = H(32, (13, 13), 18)
    wv = v(26, 18, 32)
    out.append({'section': 'm13_base_spot', 'X': [13, 13], 'R': 32,
                'z': 18, 'value': w, 'collapse_single': wv,
                'match': w == wv})
    # (f) below-band bottom-rung child census: H(19; Y; 19) vs v(s,19,19)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(13, 44)):
        ys = [()] if s == 0 else parts(s, 13, 4)
        vals = {}
        for y in ys:
            h = H(19, y, 19)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 19, 19)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H19_19',
                'label': 'observational_only_belowband_supply_source_at_z18',
                'R': 19, 'z': 19, 'floor': 13,
                's_domain': '{0} U {13..43}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g) NINTH-TAIL SUPPLY PRE-COMPUTATION (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 56)):
        a = v(s, 19, 19)
        b = v(s, 18, 19)
        row = {'s': s, 'v_19_19': a, 'v_18_19': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'ninth_tail_supply_identity_precalc',
                'label': 'observational_only_closed_form_precalc_supply_identity_k0832',
                'identity': 'v(s,19,19) =? v(s,18,19)',
                's_domain': '{0} U {12..55}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'naive_plus2_shift_prediction': 'hold on {0} U {13..19}, uniform 1-vs-0 break for s>=20',
                'measured': 'hold exactly on {0} U {12..17}; BREAK at s=18 as 0-vs-2; ALL s>=19 break uniformly as 2-vs-1; naive prediction CONTRADICTED on break start (+2 predicted s=20, measured s=18) and on constants (1v0 predicted, 0v2/2v1 measured)',
                'hold_rows': holds, 'break_rows': breaks,
                'published_partner_anchor': 'z=17 analog v(s,18,18)=v(s,17,18) holds {0} U {12..17}, breaks 1-vs-0 for all s>=18 (K1325 lemma BB-prime supply, re-verified by this pre-computation loop over s in {12..55})'})
    z17_holds = []
    z17_breaks = []
    for s in [0] + list(range(12, 56)):
        a = v(s, 18, 18)
        b = v(s, 17, 18)
        (z17_holds if a == b else z17_breaks).append(
            {'s': s, 'v_18_18': a, 'v_17_18': b})
    out.append({'section': 'z17_partner_identity_precalc_recheck',
                'label': 'observational_only_recheck_of_published_K1325_supply_identity',
                'identity': 'v(s,18,18) =? v(s,17,18)',
                's_domain': '{0} U {12..55}',
                'hold_rows': z17_holds, 'break_rows': z17_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
