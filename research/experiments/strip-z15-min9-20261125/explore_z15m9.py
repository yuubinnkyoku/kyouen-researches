#!/usr/bin/env python3
"""explore_z15m9: FROZEN PRE-DECLARATION census for the z=15 min>=9
(floor-9) cell ladder F15f9..A315f9, the prospective m=9-row z=15 line
(K1320 declaration note section 7 registered next slice; NO K slot is
claimed by this file; publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..9 the floor-9 cell
      Cell_j(s) := H(j+16; {j} U Y; 15), Y tokens >= 9, s = sum(Y) in
      {0} U {9..40}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138 recursion,
      embedded block byte-identical to the K1282..K1317 chain, pin
      bd5f22e4...). Reported per cell: deviants from the Sigma-collapse
      v(s+j,15,j+16) (K0832 closed form) and any multivalue
      (decomposition-dependence) rows STRUCTURAL NOTE for the declaration
      lane: the floor-9 domain is z-6 (one rank below the z-5 floors of
      T-Z13/T-Z14/T-Z15), and it SWALLOWS the co-token-9 shapes that were
      outside the floor-10 claim (K1320 section 5: the m=9-row line
      statement H(25;X;15)=v(S,15,25) is OPEN; the A3 rung j=9 census here
      IS the m=9-row claim position, swept as a PROVISIONAL census label
      -- no line statement is claimed by this file). The prospective proof
      skeleton mirrors K1320: base m=9 with the a=9 child = the j=8 rung
      A215f9, stair children at R=24=z+min exactly (K1264), C children on
      the published z=14 lines (F14f9..A214f9 cells for j=1..8, floor 9
      domain, and T-Z14(9) at j=9), bottom B child below-band. Key
      measured question: does A215f9 collapse (trivial-absorption base
      again), and does the j=1 F rung keep a tail (its below-band supply
      now allows min(Y)=9 pieces).
  (b) tail spots: s in {41..48}, single-token shape Y=(s,), all 9 cells.
  (c) strip sweep m in {9..14} (the m=9 rows are the NEW prospective
      claim positions H(m+16;X;15) vs v(S,15,m+16); m in {10..14}
      re-measure the published T-Z15 claim positions):
      S in {m..m+39}, Y parts tokens >= m, arity(Y) <= 3.
      EXHAUSTIVE in-sweep.
  (d) m=9-row in-band record at the claim position (25; X; 15), all
      parts >= 9 (co-token 9 allowed), arity <= 3, S in {9..47}:
      the continuity re-measurement of the published predecl kit's
      section (d) (152 shapes, separation 0 there) by this machine.
      z=15 is IN BAND for min=9 (z*(9)=17 > 15; K1268 formula).
      Observational only: the m=9-row line statement is NOT claimed here.
  (e) strip spots: m in {15..18}, X in {(m,m+1),(m,m+2),(m,m,m+1)},
      plus the m=10 base spot X=(10,10) at the T-Z15 base position
      (published continuity anchor).
  (f) below-band bottom-rung child census at the FLOOR-9 domain (NEW
      supply-source measurement; observational only): the j=1 rung's
      B-move child is the BELOW-BAND position (16; Y; 16), and under
      floor 9 the pieces Y can now be as small as 9 (at floor 10 the
      published kit measured min(Y) >= 10 and the published lemma BB
      collapsed it to v(s,16,16) = (B3) stair + (B2); the absorption
      identity v(s,16,16)=v(s,15,16) held for s in {0} U {10..15} and
      broke at s>=16, supplying the F15f10 constant-2 tail). This
      section measures H(16;Y;16) vs v(s,16,16) over the EXTENDED
      domain s in {0} U {9..40}, arity(Y) in 0..4 (first time min(Y)=9
      and single-piece shapes like (9,) enter): deviants, multivalue
      rows recorded. The proof belongs to the declaration lane; this
      section only measures.

Everything is a pure function of the pinned engine bytes; no randomness,
no hash-seed dependence, no wall-clock in the output. stdout is the
frozen artifact (explore_z15m9.out).
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
    """sweep cell_j over s in {0} U {9..smax}; returns (dev, multi, total)"""
    R = j + 16
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(9, smax + 1)):
        ys = [()] if s == 0 else parts(s, 9, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 15)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 15, R)
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
    for j in range(1, 10):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3'][j - 1]
        dev, multi, total = cell_sweep(j, 40)
        cells[f'cell{j}_{name}15f9'] = {
            'z': 15, 'min': j, 'R': j + 16, 'floor': 9,
            's_domain': '{0} U {9..40}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}15f9',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 10):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3'][j - 1]
        for s in range(41, 49):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 16, X, 15)
            exp = v(s + j, 15, j + 16)
            tail.append({'cell': f'{nm}15f9', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s41_48', 'rows': tail})
    # (c) strip sweep m in 10..14 (T-Z15 claim position)
    sv = []
    viol = []
    cnt = 0
    for m in range(9, 15):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 16, XX, 15)
                ev = v(S, 15, m + 16)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z15_m9_14', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) IN-BAND base-child / m=9-row record at the z=15 m=9 claim position
    #     (25; X; 15), all parts >= 9 (co-token 9 allowed), arity <= 3.
    #     Observational only: NOT a T-Z15 claim position.
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(9, 48):
        for X in parts(S, 9, 3):
            if not X or X[0] != 9 or sum(X) != S:
                continue
            hv = H(25, X, 15)
            ev = v(S, 15, 25)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    out.append({'section': 'inband_m9_z15_row_record',
                'label': 'observational_only_base_child_in_band_zstar9_17_gt_15',
                'R': 25, 'z': 15, 'min': 9,
                'co_token_9_allowed': True,
                'shapes': scnt, 'separations': sep})
    # (e) strip spots m in 15..18
    spots = []
    for m in range(15, 19):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 16, X, 15)
            ev = v(S, 15, m + 16)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m15_18', 'rows': spots})
    # m=10 base spot (S=20, both 10-tokens) at the T-Z15 base position
    w = H(26, (10, 10), 15)
    wv = v(20, 15, 26)
    out.append({'section': 'm10_base_spot', 'X': [10, 10], 'R': 26,
                'z': 15, 'value': w, 'collapse_single': wv,
                'match': w == wv})
    # m=9 named claim-position spots (prospective m=9-row line; continuity
    # witnesses for a future declaration battery)
    m9spots = []
    for shp in [(9,), (9, 9), (9, 10), (9, 11), (9, 9, 9), (9, 9, 10)]:
        X = tuple(sorted(shp, reverse=True))
        S = sum(X)
        hv = H(25, X, 15)
        ev = v(S, 15, 25)
        m9spots.append({'X': list(X), 'S': S, 'value': hv,
                        'collapse': ev, 'match': hv == ev})
    out.append({'section': 'm9_claim_position_spots', 'rows': m9spots})
    # (f) below-band bottom-rung child census: H(16; Y; 16) vs v(s,16,16)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(9, 41)):
        ys = [()] if s == 0 else parts(s, 9, 4)
        vals = {}
        for y in ys:
            h = H(16, y, 16)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 16, 16)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H16_16',
                'label': 'observational_only_belowband_floor9_domain_supply_source',
                'R': 16, 'z': 16, 'floor': 9,
                's_domain': '{0} U {9..40}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
