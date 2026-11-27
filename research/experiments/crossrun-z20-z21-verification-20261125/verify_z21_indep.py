#!/usr/bin/env python3
"""
verify_z21_indep: INDEPENDENT cross-run verification of the published
z=21 min>=16 (floor-16) census kit (commit 8a106233, frozen output
sha256 10f94100eb6240a807a32ac5d0e91f532800f86320a64d40e3ae47891dd2f643)
and, in the same session, a post-hoc cross-run check of the published
z=20 min>=15 census (commit 2cc16d34; the z=20 cross-run numbers are in
this run's log, the z=20 out is the earlier same-lane scratch artifact).
No K slot is claimed by this file. This is a DIFFERENT session and a
DIFFERENT code derivation (adapted from the same-lane z20 explorer,
itself derived from the published z19 kit), executed against the same
pinned raw engine block (sha 582c93c1...; startup pin bd5f22e4...).

Scope (post-publication re-measurement; it proves nothing new by
itself; its value is cross-run / cross-machine reproducibility):
  (a) cell census: j in 1..15, Cell_j(s) := H(j+22; {j} U Y; 21),
      Y tokens >= 16, s in {0} U {16..46}, arity(Y) in 0..4,
      vs the Sigma-collapse v(s+j,21,j+22) (K0832 closed form).
  (b) tail spots s in {47..54}, single token, all 15 cells.
  (c) strip sweep m in {16..20} (provisional T-Z21 claim position),
      S in {m..m+39}, parts >= m, arity <= 3.
  (d) row records, published residual-band style: m=15-row z=21
      (R=37, S in {15..53}, x0 style) + arity<=4 cotoken extension;
      m=14-row (R=36, S in {14..52}); m=13-row (R=35, S in {13..51});
      m=12-row (R=34, S in {12..50}).
  (e) strip spots m in {21..24} + the m=16 base spot
      H(38;(16,16);21) vs v(32,21,38).
  (f) below-band child census H(22; Y; 22) vs v(s,22,22).
  (g) tail supply identities (pure K0832 closed form, no H):
      twelfth v(s,22,22) vs v(s,21,22); thirteenth v(s,23,23) vs
      v(s,22,23); fourteenth v(s,24,24) vs v(s,23,24); each over
      s in {0} U {12..58}.
  (h) BASE-SPOT LATTICE PARITY (closed form, engine-free):
      for every z >= 11, v(2z-10; z; 2z-4) = z (mod 2) by the K0832
      middle branch: z <= x-1 = 2z-11 holds; q_odd(z) <= z < 2z-4 = R;
      R < x+z = 3z-10 iff z > 6; so the value is (R+z)%2 = (3z-4)%2
      which is congruent to z mod 2. Machine-checked over z in
      {11..200} here; the published base-spot observations
      z = 16..21 (values 0/1/0/1/0/1) all sit exactly on this
      collapse parity, and for every PROVED slice (T-Z16..T-Z19,
      whose universal domains contain the base-spot position) the
      identity base-spot = z mod 2 is a corollary rather than a
      fresh observation. For z=20, 21 the base-spot = collapse
      agreement is a census observation (this run re-measures it).

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (verify_z21_indep.out).
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

CELL_NAMES = ['F', 'G', 'E', 'D', 'C', 'B', 'A', 'A2', 'A3', 'A4',
              'A5', 'A6', 'A7', 'A8', 'A9']


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
    """sweep cell_j over s in {0} U {16..smax}; returns (dev, multi, total)"""
    R = j + 22
    dev = []
    multi = []
    total = 0
    for s in [0] + list(range(16, smax + 1)):
        ys = [()] if s == 0 else parts(s, 16, 4)
        vals = {}
        for y in ys:
            X = tuple(sorted((j,) + y, reverse=True))
            h = H(R, X, 21)
            vals.setdefault(h, []).append(y)
            total += 1
        if len(vals) > 1:
            multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s + j, 21, R)
            if val != exp:
                dev.append({'s': s, 'value': val, 'collapse': exp,
                            'direction': 'UP' if val > exp else 'DOWN',
                            'shapes': len(vals[val])})
    H.cache_clear()
    return dev, multi, total


def row_record(sec, rlabel, extra, R, z, m, smin, smax, min_tok):
    """cotoken-style sweep: X = (m,) U parts >= min_tok, arity up to 4 total."""
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
    """published residual-band record style: X[0] == m, all parts >= m,
    arity <= 3 TOTAL."""
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
    # (a) cell census, 15 rungs
    for j in range(1, 16):
        name = CELL_NAMES[j - 1]
        dev, multi, total = cell_sweep(j, 46)
        out.append({'section': 'cell_census', 'cell': f'{name}21f16',
                    'z': 21, 'min': j, 'R': j + 22, 'floor': 16,
                    's_domain': '{0} U {16..46}',
                    'arity': '0..4 (0 at s=0)',
                    'shapes': total, 'deviants': dev,
                    'multivalue_rows': multi})
    # (b) tail spots s in {47..54}, all 15 cells
    tail = []
    for j in range(1, 16):
        nm = CELL_NAMES[j - 1]
        for s in range(47, 55):
            X = tuple(sorted((j, s), reverse=True))
            h = H(j + 22, X, 21)
            exp = v(s + j, 21, j + 22)
            tail.append({'cell': f'{nm}21f16', 's': s, 'shape': [j, s],
                         'value': h, 'collapse': exp, 'match': h == exp})
    H.cache_clear()
    out.append({'section': 'tail_spots_s47_54', 'rows': tail})
    # (c) strip sweep m in 16..20 (provisional T-Z21 claim position)
    sv = []
    viol = []
    cnt = 0
    for m in range(16, 21):
        H.cache_clear()
        for S in range(m, m + 40):
            for X in parts(max(S - m, 0), m, 3):
                XX = tuple(sorted((m,) + X, reverse=True))
                if sum(XX) != S:
                    continue
                hv = H(m + 22, XX, 21)
                ev = v(S, 21, m + 22)
                cnt += 1
                if hv != ev:
                    viol.append({'m': m, 'X': list(XX), 'S': S,
                                 'value': hv, 'collapse': ev})
        sv.append({'m': m, 'cumulative_shapes': cnt,
                   'cumulative_violations': len(viol)})
    out.append({'section': 'strip_z21_m16_20', 'per_m': sv,
                'total_shapes': cnt, 'violations': viol})
    # (d) row records, published residual-band style
    out.append(row_record_x0(
        'inband_m15_z21_row_record',
        'independent_remeasurement_m15_row_z21_candidate_first_t20_residual_entry',
        {'co_token_15_allowed': True,
         's_domain': '{15..53}', 'arity_max': 3,
         'style': 'x0 published residual-band style'},
        37, 21, 15, 15, 53))
    out.append(row_record(
        'inband_m15_z21_row_record_ext_arity4',
        'independent_remeasurement_arity_le4_extension_m15_z21_cotoken_style',
        {'co_token_15_allowed': True,
         's_domain': '{15..53}', 'arity_max': 4},
        37, 21, 15, 15, 53, 15))
    out.append(row_record_x0(
        'inband_m14_z21_row_record',
        'independent_remeasurement_k1330_residual_m14_z21_second_entry',
        {'co_token_14_allowed': True,
         's_domain': '{14..52}', 'arity_max': 3,
         'style': 'x0 published residual-band style'},
        36, 21, 14, 14, 52))
    out.append(row_record_x0(
        'inband_m13_z21_row_record',
        'independent_remeasurement_k1328_residual_m13_z21_third_entry',
        {'co_token_13_allowed': True,
         's_domain': '{13..51}', 'arity_max': 3,
         'style': 'x0 published residual-band style'},
        35, 21, 13, 13, 51))
    out.append(row_record_x0(
        'inband_m12_z21_row_record',
        'independent_remeasurement_k1325_residual_m12_z21_fourth_final_entry',
        {'co_token_12_allowed': True,
         's_domain': '{12..50}', 'arity_max': 3,
         'style': 'x0 published residual-band style'},
        34, 21, 12, 12, 50))
    # (e) strip spots m in {21..24}
    spots = []
    for m in range(21, 25):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 22, X, 21)
            ev = v(S, 21, m + 22)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    H.cache_clear()
    out.append({'section': 'strip_spots_m21_24', 'rows': spots})
    # m=16 base spot
    w = H(38, (16, 16), 21)
    wv = v(32, 21, 38)
    out.append({'section': 'm16_base_spot', 'X': [16, 16], 'R': 38,
                 'z': 21, 'value': w, 'collapse_single': wv,
                 'match': w == wv})
    # (f) below-band child census H(22; Y; 22) vs v(s,22,22)
    H.cache_clear()
    bb_dev = []
    bb_multi = []
    bb_total = 0
    for s in [0] + list(range(16, 47)):
        ys = [()] if s == 0 else parts(s, 16, 4)
        vals = {}
        for y in ys:
            h = H(22, y, 22)
            vals.setdefault(h, []).append(y)
            bb_total += 1
        if len(vals) > 1:
            bb_multi.append({'s': s, 'values': sorted(vals.items())})
        else:
            val = next(iter(vals))
            exp = v(s, 22, 22)
            if val != exp:
                bb_dev.append({'s': s, 'value': val, 'collapse': exp,
                               'direction': 'UP' if val > exp else 'DOWN',
                               'shapes': len(vals[val])})
    out.append({'section': 'belowband_j1_child_H22_22',
                'label': 'independent_remeasurement_belowband_supply_source_at_z21',
                'R': 22, 'z': 22, 'floor': 16,
                's_domain': '{0} U {16..46}', 'arity': '0..4 (0 at s=0)',
                'shapes': bb_total, 'deviants': bb_dev,
                'multivalue_rows': bb_multi})
    # (g) tail supply identities (pure closed form, no H recursion)
    id_defs = [
        ('twelfth_tail_supply_identity_recheck', 'v(s,22,22) =? v(s,21,22)',
         lambda s: (v(s, 22, 22), v(s, 21, 22)), 'v_22_22', 'v_21_22'),
        ('thirteenth_tail_supply_identity_recheck',
         'v(s,23,23) =? v(s,22,23)',
         lambda s: (v(s, 23, 23), v(s, 22, 23)), 'v_23_23', 'v_22_23'),
        ('fourteenth_tail_supply_identity_precalc',
         'v(s,24,24) =? v(s,23,24)',
         lambda s: (v(s, 24, 24), v(s, 23, 24)), 'v_24_24', 'v_23_24'),
    ]
    for sec_name, ident, fn, ka, kb in id_defs:
        holds = []
        breaks = []
        for s in [0] + list(range(12, 59)):
            a, b = fn(s)
            row = {'s': s, ka: a, kb: b, 'equal': a == b}
            (holds if a == b else breaks).append(row)
        out.append({'section': sec_name, 'identity': ident,
                    's_domain': '{0} U {12..58}',
                    'engine_free': 'pure published K0832 single-token '
                                   'closed form, no H recursion',
                    'hold_rows': holds, 'break_rows': breaks})
    # (h) BASE-SPOT LATTICE PARITY (pure closed form, engine-free)
    pl_rows = []
    pl_bad = []
    for zz in range(11, 201):
        x = 2 * zz - 10
        R = 2 * zz - 4
        m = zz if zz % 2 else zz - 1  # q_odd(zz), engine-block helper
        val = v(x, zz, R)
        invars = {'z_le_x_minus_1': zz <= x - 1,
                  'z_ge_1': zz >= 1,
                  'm_lt_R': m < R,
                  'R_lt_x_plus_z': R < x + zz}
        ok = (val == zz % 2) and all(invars.values())
        pl_rows.append({'z': zz, 'x': x, 'R': R, 'q_odd': m,
                        'value': val, 'z_mod_2': zz % 2,
                        'branch_invariants': invars, 'consistent': ok})
        if not ok:
            pl_bad.append(zz)
    six = []
    for zz in range(16, 22):
        x = 2 * zz - 10
        R = 2 * zz - 4
        six.append({'z': zz, 'x': x, 'R': R, 'collapse_v': v(x, zz, R),
                    'z_mod_2': zz % 2})
    out.append({'section': 'base_spot_lattice_parity_closed_form',
                'label': 'engine_free: for all z>=11, v(2z-10;z;2z-4)=(z mod 2) '
                         'by the K0832 middle branch (1<=z<=x-1; q_odd(z)<=z<R=2z-4; '
                         'R<x+z=3z-10 iff z>6); value=(R+z)%2=(3z-4)%2=z mod 2. '
                         'Machine-checked over z in {11..200} with branch '
                         'invariants recorded per row; the published base-spot '
                         'observations z=16..21 (0/1/0/1/0/1) sit exactly on this '
                         'collapse parity; for proved slices T-Z16..T-Z19 the '
                         'identity base-spot=z mod 2 is a corollary.',
                'domain': 'z in {11..200}',
                'rows_checked': len(pl_rows), 'mismatches': pl_bad,
                'first_12_rows': pl_rows[:12],
                'six_published_base_spot_data_points_z16_21': six})
    res = {'result': 'VERIFY-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
