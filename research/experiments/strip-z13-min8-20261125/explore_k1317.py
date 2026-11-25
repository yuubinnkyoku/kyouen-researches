#!/usr/bin/env python3
"""explore_k1317: frozen pre-declaration / declaration-machine census for the
z=13 min>=8 (floor-8) cell ladder and the T-Z13 strip.

Scope (this file measures and reports; it proves nothing by itself):
  (a) cell census: for each j in 1..7 the floor-8 cell
      Cell_j(s) := H(j+14; {j} U Y; 13), Y tokens >= 8, s = sum(Y) in
      {0} U {8..40}, arity(Y) in 0..4 (0 only at s=0),
      swept EXHAUSTIVELY against the published raw engine (K1138 recursion,
      embedded block byte-identical to the K1282..K1315 chain, pin
      bd5f22e4...). Reported per cell: deviants from the Sigma-collapse
      v(s+j,13,j+14) (K0832 closed form) and any multivalue (decomposition
      dependence) rows.
  (b) tail spots: s in {41..48}, single-token shape Y=(s,), all 7 cells.
  (c) strip sweep: m in {8..12}, S in {m..m+39}, Y parts tokens >= m,
      arity(Y) <= 3: H(m+14; X; 13) vs v(S,13,m+14). EXHAUSTIVE in-sweep.
  (d) strip spots: m in {13..16}, X in {(m,m+1),(m,m+2),(m,m,m+1)}.

Everything is a pure function of the pinned engine bytes; no randomness,
no hash-seed dependence, no wall-clock in the output. stdout is the frozen
artifact (explore_k1317.out).
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
    """sweep cell_j over s in {0} U {8..smax}; returns (rows, shape_total)"""
    R = j + 14
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(8, smax + 1)):
        ys = [()] if s == 0 else parts(s, 8, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 13)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 13, R)
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
    for j in range(1, 8):
        name = 'FGE DCBA'[0:0] or ['F', 'G', 'E', 'D', 'C', 'B', 'A'][j - 1]
        dev, multi, total = cell_sweep(j, 40)
        cells[f'cell{j}_{name}13f8'] = {
            'z': 13, 'min': j, 'R': j + 14, 'floor': 8,
            's_domain': '{0} U {8..40}', 'arity': '0..4 (0 at s=0)',
            'shapes': total, 'deviants': dev, 'multivalue_rows': multi}
        out.append({'section': 'cell_census', 'cell': f'{name}13f8',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots
    tail = []
    for j in range(1, 8):
        nm = ['F', 'G', 'E', 'D', 'C', 'B', 'A'][j - 1]
        for s in range(41, 49):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 14, X, 13)
            exp = v(s + j, 13, j + 14)
            tail.append({'cell': f'{nm}13f8', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp,
                         'match': h == exp})
    out.append({'section': 'tail_spots_s41_48', 'rows': tail})
    # (c) strip sweep m in 8..12
    sv = []
    viol = []
    cnt = 0
    for m in range(8, 13):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 14, XX, 13)
                ev = v(S, 13, m + 14)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z13_m8_12', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) strip spots m in 13..16
    spots = []
    for m in range(13, 17):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 14, X, 13)
            ev = v(S, 13, m + 14)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m13_16', 'rows': spots})
    # m=8 TOLERANT-ABSORPTION witness spot (S=16, both 8-tokens)
    w = H(22, (8, 8), 13)
    wv = v(16, 13, 22)
    out.append({'section': 'm8_base_absorption_spot', 'X': [8, 8], 'R': 22,
                'z': 13, 'value': w, 'collapse_single': wv,
                'match': w == wv})
    res = {'result': 'EXPLORE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
