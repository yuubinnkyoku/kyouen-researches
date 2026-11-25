#!/usr/bin/env python3
"""explore_z16f9pre: FROZEN PRE-DECLARATION census for the z=16
floor-9 cell ladder (min(Y)>=9) and the m=9-row z=16/z=17 records
(the K1320 completion log's next tasks 1-2; the z=15 floor-9 census of the
same campaign was published by a parallel run as
research/experiments/strip-z15-min9-20261125 (commit 5ec6c35d) and is
byte-reproduced and value-cross-checked from this lane in the verification
log; NO K slot is claimed by this file; publish-then-execute).

NOT the T-Z16 (floor-11) predecl census: the z=16 strip-series next
slice would use floor 11 = z-5; this kit is instead the m=9-ROW
COMPLETION campaign (in-band z=16 record + the z=17 frontier record).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..9 the floor-9 cell
      Cell_j(s) := H(j+17; {j} U Y; 16), Y tokens >= 9, s = sum(Y) in
      {0} U {9..40}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138 recursion,
      embedded block byte-identical to the K1282..K1320 chain, pin
      bd5f22e4...). Reported per cell: deviants from the Sigma-collapse
      v(s+j,16,j+17) (K0832 closed form) and any multivalue
      (decomposition-dependence) rows. The 9 rungs follow the published
      naming convention F,G,E,D,C,B,A,A2,A3 with suffix 16f9: the j=9 rung
      A316f9 (small token 9 = the floor itself) is the m=9-row z=16 claim
      position measured as a cell, mirroring the published z=15-min9 kit's
      A315f9 rung (provisional census label; final naming belongs to the
      declaration lane). STRUCTURAL NOTES for the declaration lane:
      (i) the C-move children land in the z=15 floor-9 cells F15f9..A315f9
      (published kit strip-z15-min9-20261125; census-to-census anchor at
      floors 9 = 9); (ii) the a-child of the m=9-row z=16 claim position
      (token 9 -> 8) is rung j=8 of this ladder; (iii) the published z=15
      floor-9 kit observed the floor-9 deviant structure IDENTICAL to the
      published floor-10 structure (no new deviant positions from the s=9
      rows, all cells s-only, below-band child H(16;Y;16) fully collapsed
      at floor 9 across 312 shapes) -- the same questions are re-asked one
      slice up at z=16 where the supply sources shift to the newly
      published z=15 cells.
  (b) tail spots: s in {41..48}, single-token shape Y=(s,), all 9 cells.
  (c) m=9-row z=16 record (the LAST IN-BAND slice of the m=9 row,
      z*(9)=17 > 16; the row-statement candidate together with the
      published z=15 records): H(26; X; 16) vs v(S,16,26) over S in
      {9..47}, all parts >= 9 with at least one 9 token (min(X)=9
      exactly, CO-TOKEN 9 SHAPES INCLUDED), arity <= 4 (complementary to
      the rung-census domain of (a) A316f9: that sweep is anchored by a
      guaranteed 9 token with up to 4 extra parts, this sweep allows any
      1..4-token multiset with min exactly 9).
  (c2) m=9-row z=16 tail spots: single extra-token shapes X=(9,t),
      t in {39..51} (S in {48..60}), R=26.
  (d) below-band bottom-rung child census (floor-9 instance at z=16;
      observational only): H(17; Y; 17) vs v(s,17,17), s in {0} U
      {9..40}, Y tokens >= 9, arity 0..4. At z=15/floor-9 the analogous
      child H(16;Y;16) was a measured full collapse (published z15-min9
      kit section, 312 shapes, 0 deviants, 0 multivalue).
  (e) m=9-row z=17 FRONTIER record (observational only, NOT a claim
      position): z=17 = z*(9) (K1268 formula) is the frontier slice
      itself -- the FIRST out-of-band slice of the m=9 row. Published
      even-m frontier observations: m=8 at z=14 = z*(8) (362 shapes,
      exactly 1 separation X=(8,8)) and its beyond-frontier z=15
      continuation (section (g) below: the lone (8,8) separation
      PERSISTS one slice further out, flipping UP -> DOWN). The ODD-m
      frontier structure is UNOBSERVED so far in the strip series; this
      section records the first odd-m frontier data point: H(27; X; 17)
      vs v(S,17,27) over S in {9..47}, mandatory 9 token, extra parts
      >= 9, arity <= 3 (the published frontier-record parameter style).
  (f) m=9 base spot at z=16: X=(9,9) at the floor-9 base position
      (R=26, z=16).
  (g) m=8 beyond-frontier z=15 record (observational only; measured by
      this lane's z=15 census build during the raced window and
      transplanted here so it is published exactly once): m=8 at z=15 is
      one slice beyond the frontier (z*(8)=14 < 15), swept in the
      published frontier-record parameter style (z=14 kit section (d)):
      S in {8..47}, mandatory 8 token, extra parts >= 8, arity <= 3:
      H(24; X; 15) vs v(S,15,24), every separation recorded. The
      published z=14 frontier record observed exactly one separation
      X=(8,8) over 362 shapes; this records what happens ONE FURTHER
      slice out -- the first beyond-frontier data point of the strip
      series.

Everything is a pure function of the pinned engine bytes; no randomness,
no hash-seed dependence, no wall-clock in the output. stdout is the
frozen artifact (explore_z16f9pre.out).
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
    """sweep floor-9 cell_j over s in {0} U {9..smax}; (dev, multi, total)"""
    R = j + 17
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(9, smax + 1)):
        ys = [()] if s == 0 else parts(s, 9, 4)
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
    for j in range(1, 10):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3'][j - 1]
        dev, multi, total = cell_sweep(j, 40)
        out.append({'section': 'cell_census', 'cell': f'{name}16f9',
                    'j': j, 'R': j + 17, 'z': 16, 'floor': 9,
                    's_domain': '{0} U {9..40}', 'arity': '0..4 (0 at s=0)',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 10):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3'][j - 1]
        for s in range(41, 49):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 17, X, 16)
            exp = v(s + j, 16, j + 17)
            tail.append({'cell': f'{nm}16f9', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s41_48', 'rows': tail})
    # (c) m=9-row z=16 record (last in-band slice; observational)
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(9, 48):
        for X in parts(S, 9, 4):
            if not X or X[0] != 9 or sum(X) != S:
                continue
            hv = H(26, X, 16)
            ev = v(S, 16, 26)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    out.append({'section': 'm9_row_z16_record',
                'label': 'observational_last_inband_slice_m9_row_zstar9_17_gt_16',
                'R': 26, 'z': 16, 'min': 9, 'co_token_9_allowed': True,
                'arity_max': 4, 'S_domain': '{9..47}',
                'complementary_to_rung_census_A316f9': True,
                'shapes': scnt, 'separations': sep})
    # (c2) m=9-row z=16 tail spots (S in {48..60})
    rowtail = []
    for t in range(39, 52):
        X = tuple(sorted((9, t), reverse=True))
        S = 9 + t
        hv = H(26, X, 16)
        ev = v(S, 16, 26)
        rowtail.append({'X': list(X), 'S': S, 'value': hv, 'collapse': ev,
                        'match': hv == ev})
    out.append({'section': 'm9_row_z16_tail_spots_s48_60', 'rows': rowtail})
    # (d) below-band bottom-rung child census (floor 9): H(17;Y;17) vs v(s,17,17)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(9, 41)):
        ys = [()] if s == 0 else parts(s, 9, 4)
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
    out.append({'section': 'belowband_j1_child_H17_17_floor9',
                'label': 'observational_only_floor9_instance_z16',
                'R': 17, 'z': 17, 'floor': 9,
                's_domain': '{0} U {9..40}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (e) m=9-row z=17 FRONTIER record (z*(9)=17; first odd-m frontier data)
    H.cache_clear()
    fsep = []
    fcnt = 0
    for S in range(9, 48):
        for X in parts(max(S - 9, 0), 9, 3):
            XX = tuple(sorted((9,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(27, XX, 17)
            ev = v(S, 17, 27)
            fcnt += 1
            if hv != ev:
                fsep.append({'X': list(XX), 'S': S, 'value': hv,
                             'collapse': ev,
                             'direction': 'UP' if hv > ev else 'DOWN'})
    out.append({'section': 'm9_row_z17_frontier_record',
                'label': 'observational_only_frontier_slice_zstar9_equals_17_first_odd_m',
                'R': 27, 'z': 17, 'min': 9,
                'S_domain': '{9..47}', 'arity_max': 4,
                'published_even_m_frontier_anchors': 'm=8 z=14: 362 shapes exactly 1 separation X=(8,8) UP; z=15 beyond (section g): (8,8) DOWN persists',
                'shapes': fcnt, 'separations': fsep})
    # (f) m=9 base spot (S=18, both 9-tokens) at the floor-9 base position
    w = H(26, (9, 9), 16)
    wv = v(18, 16, 26)
    out.append({'section': 'm9_base_spot', 'X': [9, 9], 'R': 26,
                'z': 16, 'value': w, 'collapse_single': wv,
                'match': w == wv})
    # (g) m=8 beyond-frontier z=15 record (transplanted from this lane's
    #     raced z=15 census build; see kit README provenance)
    H.cache_clear()
    gsep = []
    gcnt = 0
    for S in range(8, 48):
        for X in parts(max(S - 8, 0), 8, 3):
            XX = tuple(sorted((8,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(24, XX, 15)
            ev = v(S, 15, 24)
            gcnt += 1
            if hv != ev:
                gsep.append({'X': list(XX), 'S': S, 'value': hv,
                             'collapse': ev,
                             'direction': 'UP' if hv > ev else 'DOWN'})
    out.append({'section': 'm8_row_z15_beyondfrontier_record',
                'label': 'observational_only_beyond_frontier_zstar8_14_lt_15_transplanted',
                'R': 24, 'z': 15, 'min': 8,
                'S_domain': '{8..47}', 'arity_max': 4,
                'published_z14_frontier_record': 'z14pre section (d): 362 shapes, exactly 1 separation X=(8,8)',
                'shapes': gcnt, 'separations': gsep})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
