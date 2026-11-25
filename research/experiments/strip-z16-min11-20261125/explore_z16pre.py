#!/usr/bin/env python3
"""
explore_z16pre: FROZEN PRE-DECLARATION census for the z=16 min>=11
(floor-11) cell ladder and the T-Z16 strip (the K1320 declaration-note
observation-series continuation; NO K slot is claimed by this file;
publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..10 the floor-11 cell
      Cell_j(s) := H(j+17; {j} U Y; 16), Y tokens >= 11, s = sum(Y) in
      {0} U {11..41}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138 recursion,
      embedded block byte-identical to the K1282..K1320 chain, pin
      bd5f22e4...). Reported per cell: deviants from the Sigma-collapse
      v(s+j,16,j+17) (K0832 closed form) and any multivalue
      (decomposition-dependence) rows. The j=10 rung (small token 10,
      one rank beyond the published z=15 A3-cell A315f10) is prefixed A4
      as a PROVISIONAL census label; final naming belongs to the
      declaration lane. STRUCTURAL NOTE for the declaration lane: the
      published z=15 deviant positions form the set {10, 12, 14} (cells
      C15f10/B15f10/A15f10 at 10; C15f10/D15f10/E15f10 at 12;
      F15f10/G15f10/E15f10 at 14) plus the F15f10 s>=16 constant-2 tail
      (supplied from below-band). Under the new floor 11 ONLY the s=10
      sources DIE (below floor); the s=12 and s=14 sources survive, and
      the census additionally probes for NEW above-floor deviant
      positions -- the SECOND death-point deactivation event of the
      series (the z=13 -> z=14 transition was the first) is therefore
      partially EXPECTED here (s=10 branch only) and this census
      measures the actual outcome directly.
  (b) tail spots: s in {42..49}, single-token shape Y=(s,), all 10 cells.
  (c) strip sweep (T-Z16 claim position): m in {11..15}, S in {m..m+39},
      Y parts tokens >= m, arity(Y) <= 3:
      H(m+17; X; 16) vs v(S,16,m+17). EXHAUSTIVE in-sweep.
  (d) IN-BAND base-child / m=10-row record (the structurally decisive
      section; observational only, NOT a T-Z16 claim position): the
      T-Z16 base m=11 a=11 child lands at (27; {10} U Y; 16) = the
      m=10-row claim position H(27; X; 16), and z=16 is IN BAND for
      min=10 (z*(10) = 2*10-2+0 = 18 > 16; K1268 formula), the SECOND
      consecutive slice whose base child is in-band (after the z=15
      min=9 base child, K1320).
      Swept: S in {10..48}, all parts >= 10, arity <= 3, i.e. the full
      min=10 domain INCLUDING co-token 10 shapes (X=(10,10,...)),
      recorded against the Sigma-collapse v(S,16,27) with every
      separation listed. The restricted subset with second token >= 11
      is exactly the A4-rung cell domain; the co-token-10 shapes probe
      whether the m=10 row statement H(27;X;16)=v(S,16,27) (the K1320
      section-6 open residual z=16) could hold universally.
  (e) strip spots: m in {16..19}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=11 base spot X=(11,11) at the T-Z16 base position.
  (f) below-band bottom-rung child census (the z=16 analog of the K1320
      section-(f) census; observational only): the j=1 rung's B-move
      child is the BELOW-BAND position (17; Y; 17) (min(Y) >= 11 so R=17
      lies deep below z+min(Y) >= 27). At z=15 the analogous bottom child
      collapsed over the full floor-10 census (H(16;Y;16) = v(s,16,16),
      K1320 D8 lemma BB); the F16f11 tail structure measured in (a) is
      expected to be generated through this child in the same way.
      This section measures that below-band child directly: s in
      {0} U {11..41}, arity(Y) in 0..4, value vs v(s,17,17), multivalue
      rows and deviants recorded. The proof belongs to the declaration
      lane; this section only measures.

Everything is a pure function of the pinned engine bytes; no randomness,
no hash-seed dependence, no wall-clock in the output. stdout is the
frozen artifact (explore_z16pre.out).
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
    """sweep cell_j over s in {0} U {11..smax}; returns (dev, multi, total)"""
    R = j + 17
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(11, smax + 1)):
        ys = [()] if s == 0 else parts(s, 11, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 16)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 16, R)
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
    for j in range(1, 11):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4'][j - 1]
        dev, multi, total = cell_sweep(j, 41)
        cells[f'cell{j}_{name}16f11'] = {
            'z': 16, 'min': j, 'R': j + 17, 'floor': 11,
            's_domain': '{0} U {11..41}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}16f11',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 11):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4'][j - 1]
        for s in range(42, 50):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 17, X, 16)
            exp = v(s + j, 16, j + 17)
            tail.append({'cell': f'{nm}16f11', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s42_49', 'rows': tail})
    # (c) strip sweep m in 11..15 (T-Z16 claim position)
    sv = []
    viol = []
    cnt = 0
    for m in range(11, 16):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 17, XX, 16)
                ev = v(S, 16, m + 17)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z16_m11_15', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=10-row record at the z=16 m=10 claim
    #     position (27; X; 16), all parts >= 10 (co-token 10 allowed),
    #     arity <= 3. Observational only: NOT a T-Z16 claim position.
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(10, 49):
        for X in parts(S, 10, 3):
            if not X or X[0] != 10 or sum(X) != S:
                continue
            hv = H(27, X, 16)
            ev = v(S, 16, 27)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    out.append({'section': 'inband_m10_z16_row_record',
                'label': 'observational_only_base_child_in_band_zstar10_18_gt_16_second_consecutive',
                'R': 27, 'z': 16, 'min': 10,
                'co_token_10_allowed': True,
                'shapes': scnt, 'separations': sep})
    # (e) strip spots m in 16..19
    spots = []
    for m in range(16, 20):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 17, X, 16)
            ev = v(S, 16, m + 17)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m16_19', 'rows': spots})
    # m=11 base spot (S=22, both 11-tokens) at the T-Z16 base position
    w = H(28, (11, 11), 16)
    wv = v(22, 16, 28)
    out.append({'section': 'm11_base_spot', 'X': [11, 11], 'R': 28,
                'z': 16, 'value': w, 'collapse_single': wv,
                'match': w == wv})
    # (f) below-band bottom-rung child census: H(17; Y; 17) vs v(s,17,17)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(11, 42)):
        ys = [()] if s == 0 else parts(s, 11, 4)
        vals = {}
        for y in ys:
            h = H(17, y, 17)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 17, 17)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H17_17',
                'label': 'observational_only_belowband_supply_source_at_z16',
                'R': 17, 'z': 17, 'floor': 11,
                's_domain': '{0} U {11..41}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
