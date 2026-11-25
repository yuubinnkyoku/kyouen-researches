#!/usr/bin/env python3
"""explore_z15f8pre: FROZEN PRE-DECLARATION census for the z=15
floor-8 cell ladder (min(Y)>=8, TWO FLOORS BELOW the published z-5 floor-10
and one below the published floor-9 census) — the NECESSITY side continuation
of the general-floor question (K1319 section 5 "is min(Y)>=z-5 necessary and
sufficient?"; the published floor-9 z=15 kit observed the s-only collapse
surviving at floor 9). NO K slot is claimed by this file;
publish-then-execute.

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..8 the floor-8 cell
      Cell_j(s) := H(j+16; {j} U Y; 15), Y tokens >= 8, s = sum(Y) in
      {0} U {8..40}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138 recursion,
      embedded block byte-identical to the K1282..K1320 chain, pin
      bd5f22e4...). Reported per cell: deviants from the Sigma-collapse
      v(s+j,15,j+16) (K0832 closed form) and any multivalue
      (decomposition-dependence) rows. Labels F,G,E,D,C,B,A,A2 with suffix
      15f8. THE CENSUS TARGET: whether the s-only collapse (true at floors
      9 and 10 on this slice) BREAKS at floor 8 — the s=8 rows that were
      outside the floor-9/10 sweep domains are live here for the first time
      at z=15, and the published z=13->z=14 death-point mechanism (s=8
      supply sources cut off by the floor) suggests the deep-floor regime
      REINTRODUCES structure. Multivalue rows would be the first
      decomposition-dependence signal of the strip series on this slice
      family (K1317 section 6 recorded the z=13-floor-8 cells as s-only).
  (b) tail spots: s in {41..48}, single-token shape Y=(s,), all 8 cells.
  (c) below-band bottom-rung child census (floor-8 instance; observational
      only): H(16; Y; 16) vs v(s,16,16), s in {0} U {8..40}, Y tokens
      >= 8, arity 0..4. Published floor-9/10 instances both collapsed
      fully (312/221 shapes, 0 deviants, 0 multivalue); the floor-8 sweep
      adds the s=8 rows and min(Y)=8 shapes.
  (d) m=8 beyond-frontier z=16 record (observational only, NOT a claim
      position; one slice beyond the beyond: z*(8)=14, published frontier
      z=14 (1 separation (8,8) UP), published beyond-frontier z=15
      (1 separation (8,8) DOWN — strip-z16-min9-20261125 kit section (g))),
      swept in the published frontier-record parameter style:
      S in {8..47}, mandatory 8 token, extra parts >= 8, arity <= 3:
      H(25; X; 16) vs v(S,16,25), every separation recorded. This records
      whether the lone (8,8) separation persists a SECOND slice beyond the
      frontier.

Everything is a pure function of the pinned engine bytes; no randomness,
no hash-seed dependence, no wall-clock in the output. stdout is the
frozen artifact (explore_z15f8pre.out).
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
    """sweep floor-8 cell_j over s in {0} U {8..smax}; (dev, multi, total)"""
    R = j + 16
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(8, smax + 1)):
        ys = [()] if s == 0 else parts(s, 8, 4)
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
    for j in range(1, 9):
        name = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2'][j - 1]
        dev, multi, total = cell_sweep(j, 40)
        out.append({'section': 'cell_census', 'cell': f'{name}15f8',
                    'j': j, 'R': j + 16, 'z': 15, 'floor': 8,
                    's_domain': '{0} U {8..40}', 'arity': '0..4 (0 at s=0)',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 9):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2'][j - 1]
        for s in range(41, 49):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 16, X, 15)
            exp = v(s + j, 15, j + 16)
            tail.append({'cell': f'{nm}15f8', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s41_48', 'rows': tail})
    # (c) below-band bottom-rung child census (floor 8): H(16;Y;16) vs v(s,16,16)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(8, 41)):
        ys = [()] if s == 0 else parts(s, 8, 4)
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
    out.append({'section': 'belowband_j1_child_H16_16_floor8',
                'label': 'observational_only_floor8_instance',
                'R': 16, 'z': 16, 'floor': 8,
                's_domain': '{0} U {8..40}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (d) m=8 beyond-beyond frontier record: m=8 at z=16 (z*(8)=14 + 2; observational)
    H.cache_clear()
    gsep = []
    gcnt = 0
    for S in range(8, 48):
        for X in parts(max(S - 8, 0), 8, 3):
            XX = tuple(sorted((8,) + X, reverse=True))
            if sum(XX) != S:
                continue
            hv = H(25, XX, 16)
            ev = v(S, 16, 25)
            gcnt += 1
            if hv != ev:
                gsep.append({'X': list(XX), 'S': S, 'value': hv,
                             'collapse': ev,
                             'direction': 'UP' if hv > ev else 'DOWN'})
    out.append({'section': 'm8_row_z16_beyondfrontier_record',
                'label': 'observational_only_beyond_frontier_second_slice_zstar8_14_plus_2',
                'R': 25, 'z': 16, 'min': 8,
                'S_domain': '{8..47}', 'arity_max': 4,
                'published_anchors': 'z=14 frontier (8,8) UP 2v1 via z14pre; z=15 beyond (8,8) DOWN 0v1 via strip-z16-min9 kit section (g)',
                'shapes': gcnt, 'separations': gsep})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
