#!/usr/bin/env python3
"""
explore_z17f11: FROZEN PRE-DECLARATION census for the z=17 min>=11
(floor-11) cell ladder — the K1322-system m=11-row z=17 residual
edition (NO K slot is claimed by this file; publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..11 the floor-11 cell
      Cell_j(s) := H(j+18; {j} U Y; 17), Y tokens >= 11, s = sum(Y) in
      {0} U {11..41}, arity(Y) in 0..4 (0 only at s=0), swept
      EXHAUSTIVELY against the published raw engine (K1138 recursion,
      embedded block byte-identical to the K1282..K1322 chain, pin
      bd5f22e4...). Reported per cell: deviants from the Sigma-collapse
      v(s+j,17,j+18) (K0832 closed form) and any multivalue
      (decomposition-dependence) rows.
      STRUCTURAL CONTEXT for the declaration lane: this is the same
      rung budget (R=j+18) and floor as the published z=16 floor-11
      kit domain shape s in {0} U {11..41}; for s >= 12 the shapes are
      SHARED with the published z17-min12 floor-12 census, so the
      s>=12 deviant classes measured there must reappear here
      cell-by-cell (automatic engine cross-check). THE NEW DOMAIN
      CONTENT is s=11: every previous census in this series swept
      only even-s deviant classes ({8,10,12,14,16}); s=11 entering a
      domain is the FIRST odd-s domain entry and probes whether an
      odd-s deviant class exists at all.
      The j=11 rung (label A517f11, PROVISIONAL final naming belongs
      to the declaration lane) at R=29 is EXACTLY the FULL m=11-row
      z=17 domain: min(X)=11 strictly, co-token 11 shapes included,
      arity<=4, s in {11..41} — the K1322 published residual band
      m=11 z in {17..20} FIRST entry, whose arity<=3 S in {11..49}
      record was published by the z17-min12 kit section (d): 110
      shapes, 0 separations. Observational only.
  (b) tail spots: s in {42..49}, single-token shape Y=(s,), all 11
      cells (the A517f11 rows extend the m=11-row z=17 record beyond
      the census cap; observational only).
  (c) below-band bottom-rung child census at FLOOR 11 (the z=17
      floor-11 analog of the K1320 lemma-BB family census;
      observational only): the j=1 rung's B-move child is the
      BELOW-BAND position (18; Y; 18) (min(Y) >= 11 so R=18 lies
      below z+min(Y) >= 28). The published floor-12 child
      H(18;Y;18) collapsed over 155 shapes (z17-min12 kit) and the
      floor-10 z=16 analog H(17;Y;17) collapsed over 221 shapes
      (z16-min10 kit). This section measures the FLOOR-11 z=17
      child: s in {0} U {11..41}, arity(Y) in 0..4, value vs
      v(s,18,18), multivalue rows and deviants recorded. The proof
      belongs to the declaration lane.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z17f11.out).
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
    R = j + 18
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(11, smax + 1)):
        ys = [()] if s == 0 else parts(s, 11, 4)
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
        dev, multi, total = cell_sweep(j, 41)
        cells[f'cell{j}_{name}17f11'] = {
            'z': 17, 'min': j, 'R': j + 18, 'floor': 11,
            's_domain': '{0} U {11..41}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}17f11',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots s in 42..49
    tail = []
    for j in range(1, 12):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5'][j - 1]
        for s in range(42, 50):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 18, X, 17)
            exp = v(s + j, 17, j + 18)
            tail.append({'cell': f'{nm}17f11', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s42_49', 'rows': tail})
    # (c) below-band bottom-rung child census at FLOOR 11:
    #     H(18; Y; 18) vs v(s,18,18), min(Y) >= 11
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(11, 42)):
        ys = [()] if s == 0 else parts(s, 11, 4)
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
    out.append({'section': 'belowband_j1_child_H18_18_floor11',
                'label': 'observational_only_belowband_supply_source_at_z17_floor11',
                'R': 18, 'z': 18, 'floor': 11,
                's_domain': '{0} U {11..41}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
