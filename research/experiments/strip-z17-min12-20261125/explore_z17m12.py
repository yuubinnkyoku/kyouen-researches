#!/usr/bin/env python3
"""
explore_z17m12: FROZEN PRE-DECLARATION census for the z=17 min>=12
(floor-12) cell ladder and the T-Z17 strip (the K1322 declaration
continuation; NO K slot is claimed by this file;
publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..11 the floor-12 cell
      Cell_j(s) := H(j+18; {j} U Y; 17), Y tokens >= 12, s = sum(Y) in
      {0} U {12..42}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138
      recursion, embedded block byte-identical to the K1282..K1322
      chain, pin bd5f22e4...). Reported per cell: deviants from the
      Sigma-collapse v(s+j,17,j+18) (K0832 closed form) and any
      multivalue (decomposition-dependence) rows. The j=11 rung (small
      token 11, one rank beyond the published z=16 A4-cell A416f11) is
      prefixed A5 as a PROVISIONAL census label; final naming belongs
      to the declaration lane. STRUCTURAL NOTE for the declaration
      lane: the published z=16 (K1322) deviant positions form the set
      {12, 14, 16} (cells C16f11/B16f11/D16f11 at 12; E16f11/D16f11/
      G16f11 at 14; F16f11/G16f11 at 16; A..A4 fully collapsed). Under
      the new floor 12 ALL THREE source positions survive (>= 12), so
      NO death-point event is expected -- instead this census probes
      (i) whether the three classes persist at z=17 with the same
      positions/directions/values, (ii) whether a NEW above-floor
      deviant class appears (at z=16 the new class was s=16, supplied
      by the absorption-identity break; the z=17 analog supply
      analysis belongs to the declaration lane), and (iii) whether the
      A-family collapse run extends to 5 consecutive rungs (A17f12 ..
      A517f12), which is exactly the T-Z17 base-m=12 trivial-absorption
      case: the a=12 child of the T-Z17 base position H(30;{12} U Y;17)
      is precisely the cell-11 domain H(29;{11} U Y;17).
  (b) tail spots: s in {43..50}, single-token shape Y=(s,), all 11
      cells.
  (c) strip sweep (T-Z17 claim position, PROVISIONAL label): m in
      {12..16}, S in {m..m+39}, Y parts tokens >= m, arity(Y) <= 3:
      H(m+18; X; 17) vs v(S,17,m+18). EXHAUSTIVE in-sweep.
  (d) IN-BAND base-child / m=11-row record (the structurally decisive
      section; observational only, NOT a T-Z17 claim position): the
      T-Z17 base m=12 a=12 child lands at (29; {11} U Y; 17) = the
      m=11-row claim position H(29; X; 17), and z=17 is IN BAND for
      min=11 (z*(11) = 2*11-2+1 = 21 > 17; K1268 formula), the THIRD
      consecutive slice whose base child is in-band (after z=15 min=9
      K1320 and z=16 min=10 K1322). Swept: S in {11..49}, all parts
      >= 11, arity <= 3, i.e. the full min=11 domain INCLUDING
      co-token 11 shapes (X=(11,11,...)), recorded against the
      Sigma-collapse v(S,17,29) with every separation listed. The
      restricted subset with second token >= 12 is exactly the A5-rung
      cell domain; the m=11 row at z=17 is the FIRST entry of the
      K1322 published residual band m=11 z in {17..20}.
  (d2) IN-BAND m=10-row z=17 record: the second and last entry of the
      K1320 published residual band m=10 z in {16,17} (the z=16 entry
      was measured by the published z16-min11 kit, 130 shapes,
      separation 0). R = 28, all parts >= 10 (co-token 10 allowed),
      arity <= 3, S in {10..48}, recorded against v(S,17,28). z=17 is
      in band for min=10 (z*(10) = 18 > 17).
  (d3) m=8-row z=17 BEYOND record: the third consecutive beyond-
      frontier data point of the growth-rule series (published: z=15
      beyond 1 separation (8,8) UP->DOWN flip; z=16 beyond-beyond 2
      separations ((8,8) DOWN persisting + (8,10) UP new)). R = 26,
      domain EXACTLY the published z=16 section-(d) form (S in
      {8..47}, X = (8,) U parts(S-8, 8, 3), 362 shapes) so the
      separation sets compare across slices position-by-position.
      Observational only. The m=9 z=17 frontier record is NOT repeated
      here (already published by the z16-min9 lane kit: 234 shapes,
      single separation (9,10)).
  (e) strip spots: m in {17..20}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=12 base spot X=(12,12) at the T-Z17 base position.
  (f) below-band bottom-rung child census (the z=17 analog of the
      K1320/K1322 section-(f) census; observational only): the j=1
      rung's B-move child is the BELOW-BAND position (18; Y; 18)
      (min(Y) >= 12 so R=18 lies deep below z+min(Y) >= 29). At z=15
      the analogous bottom child collapsed over the full floor-9
      census (H(16;Y;16) = v(s,16,16), K1320 D8 lemma BB); at z=16 the
      analogous child H(17;Y;17) collapsed over the full floor-11
      census against v(s,17,17) (published z16-min11 kit, 183 shapes,
      deviant 0), and the z=16 F-cell tail was supplied through the
      related absorption-identity break. This section measures the
      z=17 child directly: s in {0} U {12..42}, arity(Y) in 0..4,
      value vs v(s,18,18), multivalue rows and deviants recorded. The
      proof belongs to the declaration lane; this section only
      measures.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z17m12.out).
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
    """sweep cell_j over s in {0} U {12..smax}; returns (dev, multi, total)"""
    R = j + 18
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(12, smax + 1)):
        ys = [()] if s == 0 else parts(s, 12, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 17)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 17, R)
            if val != exp:
                dev.append({'s': s, 'value': val, 'collapse': exp,
                            'direction': 'UP' if val > exp else 'DOWN',
                            'shapes': len(vals[val])})
    H.cache_clear()
    return dev, multi, total


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    cells = {}
    for j in range(1, 12):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
                'A5'][j - 1]
        dev, multi, total = cell_sweep(j, 42)
        cells[f'cell{j}_{name}17f12'] = {
            'z': 17, 'min': j, 'R': j + 18, 'floor': 12,
            's_domain': '{0} U {12..42}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}17f12',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 12):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5'][j - 1]
        for s in range(43, 51):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 18, X, 17)
            exp = v(s + j, 17, j + 18)
            tail.append({'cell': f'{nm}17f12', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s43_50', 'rows': tail})
    # (c) strip sweep m in 12..16 (T-Z17 claim position, provisional)
    sv = []
    viol = []
    cnt = 0
    for m in range(12, 17):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 18, XX, 17)
                ev = v(S, 17, m + 18)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z17_m12_16', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=11-row record at the z=17 m=11 claim
    #     position (29; X; 17), all parts >= 11 (co-token 11 allowed),
    #     arity <= 3. Observational only: NOT a T-Z17 claim position.
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(11, 50):
        for X in parts(S, 11, 3):
            if not X or X[0] != 11 or sum(X) != S:
                continue
            hv = H(29, X, 17)
            ev = v(S, 17, 29)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    out.append({'section': 'inband_m11_z17_row_record',
                'label': 'observational_only_base_child_in_band_zstar11_21_gt_17_third_consecutive',
                'R': 29, 'z': 17, 'min': 11,
                'co_token_11_allowed': True,
                'shapes': scnt, 'separations': sep})
    # (d2) IN-BAND m=10-row z=17 record: second and last entry of the
    #      K1320 published residual m=10 z in {16,17}.
    H.cache_clear()
    sep2 = []
    scnt2 = 0
    for S in range(10, 49):
        for X in parts(S, 10, 3):
            if not X or X[0] != 10 or sum(X) != S:
                continue
            hv = H(28, X, 17)
            ev = v(S, 17, 28)
            scnt2 += 1
            if hv != ev:
                sep2.append({'X': list(X), 'S': S, 'value': hv,
                             'collapse': ev,
                             'direction': 'UP' if hv > ev else 'DOWN'})
    out.append({'section': 'inband_m10_z17_row_record',
                'label': 'observational_only_k1320_residual_m10_z17_in_band_zstar10_18_gt_17',
                'R': 28, 'z': 17, 'min': 10,
                'co_token_10_allowed': True,
                'shapes': scnt2, 'separations': sep2})
    # (d3) m=8-row z=17 BEYOND record: third consecutive beyond data
    #      point of the growth-rule series; enumeration form identical
    #      to the published z=16 section-(d) record (S in {8..47},
    #      (8,) U parts(S-8, 8, 3), 362 shapes) for cross-slice
    #      comparability.
    H.cache_clear()
    sep3 = []
    scnt3 = 0
    for S in range(8, 48):
        for X in parts(max(S - 8, 0), 8, 3):
            XX = tuple(sorted((8,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(26, XX, 17)
            ev = v(S, 17, 26)
            scnt3 += 1
            if hv != ev:
                sep3.append({'X': list(XX), 'S': S, 'value': hv,
                             'collapse': ev,
                             'direction': 'UP' if hv > ev else 'DOWN'})
    out.append({'section': 'm8_row_z17_beyondfrontier_record',
                'label': 'observational_only_beyond_frontier_third_slice_zstar8_14_plus_3',
                'R': 26, 'z': 17, 'min': 8,
                'S_domain': '{8..47}', 'arity_max': 4,
                'published_anchors': 'z=14 frontier (8,8) UP 2v1 via z14pre; z=15 beyond (8,8) DOWN 0v1 via strip-z16-min9 kit section (g); z=16 beyond-beyond (8,8) DOWN 0v2 + (8,10) UP 2v1 via strip-z15-min8 kit section (d)',
                'shapes': scnt3, 'separations': sep3})
    # (e) strip spots m in 17..20
    spots = []
    for m in range(17, 21):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 18, X, 17)
            ev = v(S, 17, m + 18)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m17_20', 'rows': spots})
    # m=12 base spot (S=24, both 12-tokens) at the T-Z17 base position
    w = H(30, (12, 12), 17)
    wv = v(24, 17, 30)
    out.append({'section': 'm12_base_spot', 'X': [12, 12], 'R': 30,
                'z': 17, 'value': w, 'collapse_single': wv,
                'match': w == wv})
    # (f) below-band bottom-rung child census: H(18; Y; 18) vs v(s,18,18)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(12, 43)):
        ys = [()] if s == 0 else parts(s, 12, 4)
        vals = {}
        for y in ys:
            h = H(18, y, 18)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 18, 18)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H18_18',
                'label': 'observational_only_belowband_supply_source_at_z17',
                'R': 18, 'z': 18, 'floor': 12,
                's_domain': '{0} U {12..42}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
