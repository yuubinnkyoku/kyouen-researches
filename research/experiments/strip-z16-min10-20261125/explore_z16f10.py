#!/usr/bin/env python3
"""
explore_z16f10: FROZEN PRE-DECLARATION census for the z=16 min>=10
(floor-10) cell ladder — the K1320-system-2 m=10-row z=16 residual
edition (NO K slot is claimed by this file; publish-then-execute).

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..10 the floor-10 cell
      Cell_j(s) := H(j+17; {j} U Y; 16), Y tokens >= 10, s = sum(Y) in
      {0} U {10..40}, arity(Y) in 0..4 (0 only at s=0), swept
      EXHAUSTIVELY against the published raw engine (K1138 recursion,
      embedded block byte-identical to the K1282..K1322 chain, pin
      bd5f22e4...). Reported per cell: deviants from the Sigma-collapse
      v(s+j,16,j+17) (K0832 closed form) and any multivalue
      (decomposition-dependence) rows.
      STRUCTURAL CONTEXT for the declaration lane: this is the
      SAME 221-shape-per-cell domain as the published z=15 floor-10
      kit (F15f10..A315f10, 9 rungs; the z=16 edition extends to the
      10th rung). The j=10 rung (label A416f10, PROVISIONAL final
      naming belongs to the declaration lane) at R=27 is EXACTLY the
      FULL m=10-row z=16 domain: min(X)=10 strictly, co-token 10
      shapes included, the K1320-system-2 published open residual
      (m=10 row, z in {16,17}; the z=16 entry was measured at
      arity<=3, S in {10..48} by the published z16-min11 kit section
      (d): 130 shapes, 0 separations; here it is swept at arity<=4,
      s in {10..40} in the cell form). The m=10-row z=17 entry is
      published by the z17-min12 kit section (d2) (130 shapes, 0
      separations).
      THE DEATH-EVENT QUESTION: the z=15 published (K1320 proven)
      deviant classes sit at s in {10, 12, 14} plus the F15f10
      constant-2 tail s >= 16. At z=16 floor 11 the s=10 branch is
      BELOW FLOOR (the K1322 second death event: domain exclusion,
      not a z-transition). This floor-10 census puts s=10 BACK INSIDE
      the domain and therefore directly measures whether the s=10
      classes REVIVE at z=16 (domain re-entry) or stay dead — and
      whether the published floor-11 structures {12, 14, 16} persist
      unchanged (for s >= 12 the floor-10 and floor-11 sweeps share
      shapes, so shared-row values cross-check automatically against
      the published z16-min11 deviant table).
  (b) tail spots: s in {41..48}, single-token shape Y=(s,), all 10
      cells (the A416f10 rows extend the m=10-row z=16 record beyond
      the census cap; observational only).
  (c) below-band bottom-rung child census at FLOOR 10 (the z=16
      floor-10 analog of the K1320 D8 lemma-BB census; observational
      only): the j=1 rung's B-move child is the BELOW-BAND position
      (17; Y; 17) (min(Y) >= 10 so R=17 lies below z+min(Y) >= 26).
      The published floor-11 child H(17;Y;17) collapsed over 183
      shapes (z16-min11 kit); the K1320 lemma BB proved the floor-10
      z=15 analog H(16;Y;16)=v(s,16,16). This section measures the
      FLOOR-10 z=16 child: s in {0} U {10..40}, arity(Y) in 0..4,
      value vs v(s,17,17), multivalue rows and deviants recorded.
      Whether the collapse holds (and at which s it breaks, if any)
      decides the supply structure for both the floor-10 F rung and
      the m=10-row closure; the proof belongs to the declaration
      lane.

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (explore_z16f10.out).
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
    """sweep cell_j over s in {0} U {10..smax}; returns (dev, multi, total)"""
    R = j + 17
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(10, smax + 1)):
        ys = [()] if s == 0 else parts(s, 10, 4)
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
        dev, multi, total = cell_sweep(j, 40)
        cells[f'cell{j}_{name}16f10'] = {
            'z': 16, 'min': j, 'R': j + 17, 'floor': 10,
            's_domain': '{0} U {10..40}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}16f10',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots s in 41..48
    tail = []
    for j in range(1, 11):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4'][j - 1]
        for s in range(41, 49):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 17, X, 16)
            exp = v(s + j, 16, j + 17)
            tail.append({'cell': f'{nm}16f10', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s41_48', 'rows': tail})
    # (c) below-band bottom-rung child census at FLOOR 10:
    #     H(17; Y; 17) vs v(s,17,17), min(Y) >= 10
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(10, 41)):
        ys = [()] if s == 0 else parts(s, 10, 4)
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
    out.append({'section': 'belowband_j1_child_H17_17_floor10',
                'label': 'observational_only_belowband_supply_source_at_z16_floor10',
                'R': 17, 'z': 17, 'floor': 10,
                's_domain': '{0} U {10..40}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
