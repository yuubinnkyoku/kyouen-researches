#!/usr/bin/env python3
"""
explore_z19f14: FROZEN PRE-DECLARATION census for the z=19 min>=14
(floor-14) cell ladder and the T-Z19 strip (the K1328 declaration
continuation; NO K slot is claimed by this file;
publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..13 the floor-14 cell
      Cell_j(s) := H(j+20; {j} U Y; 19), Y tokens >= 14, s = sum(Y) in
      {0} U {14..44}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1328
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,19,j+20) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The j=13 rung (small
      token 13, one rank beyond the published z=18 A6-cell A618f13) is
      prefixed A7 as a PROVISIONAL census label; final naming belongs
      to the declaration lane. STRUCTURAL NOTE for the declaration
      lane: the published z=18 (K1328 census) deviant position set is
      {14, 16, 18} (C/B/D at 14; E/G/D at 16; F/G at 18). Under the
      new floor 14 EVERY published source position survives
      (>= 14), so NO definition-domain-exclusion event is expected
      here (contrast the z=17 -> z=18 shift where the s=12 classes
      fell below floor 13) -- this census probes (i) which of the
      14/16/18 classes persist at z=19 with which positions/
      directions/values, (ii) whether a NEW above-floor deviant class
      appears: the typology alternation predicts hole+tail at odd z
      (z=19), with the hole at s=19 and a persistent tail from s>=20;
      the supply datum is the published z19 probe kit TENTH-tail
      identity v(s,20,20)=v(s,19,20) holding on {0} U {12..19} and
      breaking uniformly 0v1 for s>=20 (naive +2 shift of the z=17
      break constants is NOT assumed: it was already counterexampled
      at z=18), and (iii) whether the A-family collapse run extends
      to SEVEN rungs (A19f14 .. A719f14), which is exactly the T-Z19
      base-m=14 trivial-absorption case: the a=14 child of the T-Z19
      base position H(34;{14} U Y;19) is precisely the cell-13 domain
      H(33; {13} U Y;19) -- the FIFTH consecutive in-band base child
      (after K1320 min=9, K1322 min=10, K1325 min=11, K1328 min=12;
      z*(13)=25 > 19).
  (b) tail spots: s in {45..52}, single-token shape Y=(s,), all 13
      cells.
  (c) strip sweep (T-Z19 claim position, PROVISIONAL label): m in
      {14..18}, S in {m..m+39}, Y parts tokens >= m, arity(Y) <= 3:
      H(m+20; X; 19) vs v(S,19,m+20). EXHAUSTIVE in-sweep.
  (d) IN-BAND base-child / m=13-row record (the structurally decisive
      section; observational only, NOT a T-Z19 claim position): the
      T-Z19 base m=14 a=14 child lands at (33; {13} U Y; 19) = the
      m=13-row claim position H(33; X; 19), and z=19 is IN BAND for
      min=13 (z*(13) = 25 > 19, K1268 formula z*(m)=2m-2+(m mod 2)),
      the FIFTH consecutive slice whose base child is in-band. Swept:
      S in {13..51}, all parts >= 13 (co-token 13 shapes INCLUDED,
      X[0]=13), arity <= 3, recorded against the Sigma-collapse
      v(S,19,33) with every separation listed, PLUS an arity<=4
      co-token-style extension sweep (published style lesson of the
      z18 kit: the base record itself is kept in the published
      residual-band style, the arity<=4 version as a labelled
      extension). This is simultaneously the FIRST entry of the K1328
      published residual band m=13 z in {19..24} (frontier z=25).
  (d2) IN-BAND m=12-row z=19 record: the SECOND entry of the K1325
      published residual band m=12 z in {18..21} (the z=18 entry was
      measured by the published z18 kit, 92 shapes, separation 0).
      R = 32, all parts >= 12 (co-token 12 allowed, X[0]=12), arity
      <= 3, S in {12..50}, recorded against v(S,19,32); SAME
      enumeration as the published z=18 entry -> same 92 shapes,
      shape-for-shape cross-slice comparability machine-checked.
  (d3) IN-BAND m=11-row z=19 record: the THIRD entry of the K1322
      published residual band m=11 z in {17..20} (the z=17 and z=18
      entries were measured by the published z17/z18 kits, 110 shapes
      each, separations 0). R = 31, all parts >= 11 (co-token 11
      allowed, X[0]=11), arity <= 3, S in {11..49}, recorded against
      v(S,19,31); SAME enumeration as the published z=17/z=18 entries
      -> same 110 shapes.
  (e) strip spots: m in {19..22}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=14 base spot X=(14,14) at the T-Z19 base position
      H(34;(14,14);19) -- already measured by the published z19 probe
      kit (=1=v(28,19,34)); rechecked here as the census-internal
      cross-check of the frozen chain value.
  (f) below-band bottom-rung child census (the z=19 analog of the
      K1320/K1322/K1325/K1328 section-(f) census; observational only):
      the j=1 rung's B-move child is the BELOW-BAND position
      (20; Y; 20) (min(Y) >= 14 so R=20 lies deep below z'+min(Y)
      >= 34). At z=18 the analogous child H(19;Y;19) collapsed over
      the full floor-13 census against v(s,19,19) (fourth consecutive
      full collapse; published K1328 lemma BB''). This section measures
      the z=19 child directly (H(20;Y;20) vs v(s,20,20), s in
      {0} U {14..44}, arity(Y) in 0..4); the proof belongs to the
      declaration lane.
  (g) TAIL SUPPLY PRE-COMPUTATIONS (pure published K0832 closed form,
      NO engine recursion):
      (g1) TENTH-tail identity RECHECK: the published z19 probe kit
      measured v(s,20,20)=v(s,19,20) holding on {0} U {12..19} and
      breaking uniformly 0v1 for all s>=20 over s in {0} U {12..55}.
      Rechecked here over the extended domain s in {0} U {12..56}
      (the F19f14 supply datum; the naive +2-shift of the z=17 break
      constants is not assumed anywhere).
      (g2) ELEVENTH-tail identity PRE-COMPUTATION (NEW): the z=20
      slice supply identity v(s,21,21) vs v(s,20,21) over s in
      {0} U {12..56}. PREDECLARED candidate (written before the first
      run): the even-z identities break AT s=z (z=16: break at s=16;
      z=18: break at s=18 as 0v2 then uniform 2v1), so the candidate
      break start is s=20; the break constants are NOT predeclared
      (published even-z constants alternate shapes: z=16 uniform
      1-vs-0, z=18 0v2@18 then 2v1@>=19 -- z=20 discriminates the
      even-z constant pattern).

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z19f14.out).
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
    """sweep cell_j over s in {0} U {14..smax}; returns (dev, multi, total)"""
    R = j + 20
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(14, smax + 1)):
        ys = [()] if s == 0 else parts(s, 14, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 19)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 19, R)
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
    """published residual-band record style (z17-min12 / z18-min13 kit
    sections (d)/(d2)): position X = parts(S, m, 3) with X[0] == m, i.e.
    all parts >= m with co-token m allowed, arity <= 3 TOTAL. Shape-
    for-shape comparable with the published z=18 entries."""
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
    for j in range(1, 14):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5', 'A6', 'A7'][j - 1]
        dev, multi, total = cell_sweep(j, 44)
        cells[f'cell{j}_{name}19f14'] = {
            'z': 19, 'min': j, 'R': j + 20, 'floor': 14,
            's_domain': '{0} U {14..44}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}19f14',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 14):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6', 'A7'][j - 1]
        for s in range(45, 53):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 20, X, 19)
            exp = v(s + j, 19, j + 20)
            tail.append({'cell': f'{nm}19f14', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s45_52', 'rows': tail})
    # (c) strip sweep m in 14..18 (T-Z19 claim position, provisional)
    sv = []
    viol = []
    cnt = 0
    for m in range(14, 19):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 20, XX, 19)
                ev = v(S, 19, m + 20)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z19_m14_18', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=13-row record at the z=19 m=13 claim
    #     position (33; X; 19), all parts >= 13 (co-token 13 allowed),
    #     arity <= 3 TOTAL. Observational only: NOT a T-Z19 claim
    #     position. Published residual-band record style.
    out.append(row_record_x0(
        'inband_m13_z19_row_record',
        'observational_only_base_child_in_band_zstar13_25_gt_19_fifth_consecutive',
        {'co_token_13_allowed': True,
         'residual_band': 'K1328 published m=13 z in {19..24}; frontier z=25; FIRST entry',
         's_domain': '{13..51}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        33, 19, 13, 13, 51))
    out.append(row_record(
        'inband_m13_z19_row_record_ext_arity4',
        'observational_only_arity_le4_extension_of_the_m13_z19_record_cotoken_style',
        {'co_token_13_allowed': True,
         's_domain': '{13..51}', 'arity_max': 4},
        33, 19, 13, 13, 51, 13))
    # (d2) IN-BAND m=12-row z=19 record: SECOND entry of the K1325
    #      published residual m=12 z in {18..21}, published record
    #      style (the z=18 entry measured 92 shapes, separation 0).
    out.append(row_record_x0(
        'inband_m12_z19_row_record',
        'observational_only_k1325_residual_m12_z19_second_entry_zstar12_22_gt_19',
        {'co_token_12_allowed': True,
         'residual_band': 'K1325 published m=12 z in {18..21}; z=18 entry measured 92 shapes separation 0 (same enumeration -> same 92 shapes here)',
         's_domain': '{12..50}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        32, 19, 12, 12, 50))
    # (d3) IN-BAND m=11-row z=19 record: THIRD entry of the K1322
    #      published residual m=11 z in {17..20}, published record
    #      style (the z=17/z=18 entries measured 110 shapes each,
    #      separations 0).
    out.append(row_record_x0(
        'inband_m11_z19_row_record',
        'observational_only_k1322_residual_m11_z19_third_entry_zstar11_21_gt_19',
        {'co_token_11_allowed': True,
         'residual_band': 'K1322 published m=11 z in {17..20}; z=17 and z=18 entries measured 110 shapes each, separations 0 (same enumeration -> same 110 shapes here)',
         's_domain': '{11..49}', 'arity_max': 3, 'style': 'x0 published residual-band style'},
        31, 19, 11, 11, 49))
    # (e) strip spots m in 19..22
    spots = []
    for m in range(19, 23):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 20, X, 19)
            ev = v(S, 19, m + 20)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m19_22', 'rows': spots})
    # m=14 base spot (S=28, both 14-tokens) at the T-Z19 base position
    w = H(34, (14, 14), 19)
    wv = v(28, 19, 34)
    out.append({'section': 'm14_base_spot', 'X': [14, 14], 'R': 34,
                'z': 19, 'value': w, 'collapse_single': wv,
                'match': w == wv,
                'published_probe_crossref': 'beyond_z19 kit (9e955243) measured H(34;(14,14);19)=1=v(28,19,34); rechecked here'})
    # (f) below-band bottom-rung child census: H(20; Y; 20) vs v(s,20,20)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(14, 45)):
        ys = [()] if s == 0 else parts(s, 14, 4)
        vals = {}
        for y in ys:
            h = H(20, y, 20)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 20, 20)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H20_20',
                'label': 'observational_only_belowband_supply_source_at_z19',
                'R': 20, 'z': 20, 'floor': 14,
                's_domain': '{0} U {14..44}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g1) TENTH-TAIL SUPPLY IDENTITY RECHECK (pure K0832 closed form)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 57)):
        a = v(s, 20, 20)
        b = v(s, 19, 20)
        row = {'s': s, 'v_20_20': a, 'v_19_20': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'tenth_tail_supply_identity_recheck',
                'label': 'observational_only_closed_form_recheck_supply_identity_k0832',
                'identity': 'v(s,20,20) =? v(s,19,20)',
                's_domain': '{0} U {12..56}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'published_anchor': 'beyond_z19 kit (commit 9e955243): holds {0} U {12..19}, breaks UNIFORMLY 0v1 for all s>=20 over s in {0} U {12..55}; rechecked and extended here over s in {0} U {12..56}',
                'hold_rows': holds, 'break_rows': breaks})
    # (g2) ELEVENTH-TAIL SUPPLY PRE-COMPUTATION (NEW, pure K0832)
    e_holds = []
    e_breaks = []
    for s in [0] + list(range(12, 57)):
        a = v(s, 21, 21)
        b = v(s, 20, 21)
        row = {'s': s, 'v_21_21': a, 'v_20_21': b, 'equal': a == b}
        (e_holds if a == b else e_breaks).append(row)
    out.append({'section': 'eleventh_tail_supply_identity_precalc',
                'label': 'observational_only_new_closed_form_precalc_z20_slice_supply_k0832',
                'identity': 'v(s,21,21) =? v(s,20,21)',
                's_domain': '{0} U {12..56}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'predeclared_candidate': 'break starts AT s=20 (even-z identities break at s=z: z=16 break at s=16, z=18 break at s=18 as 0v2 then uniform 2v1); break constants NOT predeclared (published even-z constants do not repeat a single form: z=16 uniform 1-vs-0, z=18 0v2@18 + 2v1@>=19); z=20 discriminates the even-z constant pattern',
                'hold_rows': e_holds, 'break_rows': e_breaks})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
