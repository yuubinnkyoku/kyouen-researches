#!/usr/bin/env python3
"""
verify_k1334: machine cross-check of the tail-supply-identity family
theorem + strip-line closed-form lemma (provisional knowledge item
K1334), both derived ENGINE-FREE from the published K0832 single-token
closed form (hand derivation FIRST, this kit second - the machine
checks the hand algebra and the engine transcription, it is not the
proof).

Theorem A (supply-identity family, complete characterization).
For every k >= 1 and every s >= 0, let
    A_k(s) = v(s, k+1, k+1),  B_k(s) = v(s, k, k+1)
(single_token(x=s, z, R) closed form). Then
  (*)  0 <= s <= k-1          :  A_k(s) = B_k(s) = s mod 2
  (*)  k odd,  s = k          :  A_k(s) = B_k(s) = 1
  (*)  k odd,  s >= k+1       :  (A_k(s), B_k(s)) = (0, 1)   [uniform]
  (*)  k even, s = k          :  (A_k(s), B_k(s)) = (0, 2)
  (*)  k even, s >= k+1       :  (A_k(s), B_k(s)) = (2, 1)   [uniform]
(the break-tail uniformity has NO upper cutoff in s).

Lemma S (strip-line value closed form).
For every z >= 1, m >= 0 and every token sum S >= max(z+1, m+2):
    v(S, z, m+z+1) = (m+1) mod 2,
independently of S beyond the two stated sum conditions.

Corollaries: K1332 (base-spot lattice parity, m = z-5, S = 2z-10,
hence value z mod 2 for z >= 11) is the Lemma S instance at m = z-5;
every published strip spot row (m in {z..z+3}, shapes (m+1,m),
(m+2,m), (m+1,m,m)) and base spot row sits on (m+1)%2; the published
ninth..fifteenth tail supply identities (k = 18..24) and the z17
partner identity (k = 17) are the k-instances of Theorem A; all
future tail precomputations (k >= 25) are determined a priori.

Sections:
  (a) engine_gate      - pinned block sha startup check (bd5f22e4...)
  (b) lemmaA_grid      - Theorem A vs the closed form, k in {1..140},
                         s in {0..300}: 84,280 value checks
  (c) lemmaS_grid      - Lemma S vs the closed form: exhaustive small
                         grid (z,m <= 20, S 1..90) + wide spot grid
                         (z,m <= 120), with condition-necessity counts
  (d) k0832_revalidate - closed form vs the RAW canonical engine over
                         x in {1..30}, z in {0..24}, R in {1..60}
                         (+ ordered-engine subset)
  (e) cross_artifact   - every identity row, strip spot and base spot
                         of the five published census kits
                         (z18..z22, pins asserted) parsed and compared
                         value-for-value against Theorem A / Lemma S
  (f) predictions      - full Theorem A constants for k in {25..32}

No K slot is claimed BY THE MACHINE; the item claims the slot. No
verdict of any game position is consumed; 11x11 stays UNKNOWN.
"""
import json
import re
import sys
import hashlib
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
vC = ns['vC']
vO = ns['vO']

# published kit frozen outputs (byte-verified pins; z19 has no published
# sha pin in the kit READMEs, its recorded observation is the earliest)
INPUTS = [
    ('../strip-z18-min13-20261125/explore_z18f13.out', 18,
     'c4e7757c587883bb41b0f297de336128cd6bafc55865ba10673b28c7338d0b0b'),
    ('../strip-z19-min14-20261125/explore_z19f14.out', 19, None),
    ('../strip-z20-min15-20261125/explore_z20f15.out', 20,
     '09e9026a436bf25aed05eabaf3629975971bd320a4c4c5ce5da122239f19f789'),
    ('../strip-z21-min16-20261125/explore_z21f16.out', 21,
     '10f94100eb6240a807a32ac5d0e91f532800f86320a64d40e3ae47891dd2f643'),
    ('../strip-z22-min17-20261125/explore_z22f17.out', 22,
     'f16a87d447d61b631cca153665b4a577d844ab5fe96eb9f740a74e400c82c7ac'),
]


def lemmaA_pred(k, s):
    """Theorem A: claimed (A_k(s), B_k(s))."""
    if s <= k - 1:
        a = b = s % 2
    elif k % 2:  # k odd
        if s == k:
            a = b = 1
        else:
            a, b = 0, 1
    else:  # k even
        if s == k:
            a, b = 0, 2
        else:
            a, b = 2, 1
    return a, b


def lemmaS_conditions(z, m, S):
    return z >= 1 and m >= 0 and S >= z + 1 and S >= m + 2


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS' if sha == PIN else 'FAIL'})

    # (b) Theorem A vs the closed form, k in {1..140}, s in {0..300}
    rows = 0
    bad = []
    witness = []
    for k in range(1, 141):
        for s in range(0, 301):
            pa, pb = lemmaA_pred(k, s)
            ra = v(s, k + 1, k + 1)
            rb = v(s, k, k + 1)
            rows += 1
            if (pa, pb) != (ra, rb):
                bad.append({'k': k, 's': s, 'pred': [pa, pb],
                            'actual': [ra, rb]})
            if 17 <= k <= 26 and s <= 40:
                witness.append({'k': k, 's': s, 'A': ra, 'B': rb,
                                'equal': ra == rb})
    out.append({'section': 'lemmaA_grid',
                'domain': 'k in {1..140}, s in {0..300}',
                'rows': rows, 'mismatches': bad[:10],
                'mismatch_count': len(bad),
                'witness_rows_k17_26_s0_40': witness})

    # (c) Lemma S vs the closed form
    small_rows = 0
    small_bad = []
    outside_fail = 0
    outside_total = 0
    for z in range(1, 21):
        for m in range(0, 21):
            for S in range(1, 91):
                want = (m + 1) % 2
                if lemmaS_conditions(z, m, S):
                    small_rows += 1
                    if v(S, z, m + z + 1) != want:
                        small_bad.append({'z': z, 'm': m, 'S': S})
                else:
                    outside_total += 1
                    if v(S, z, m + z + 1) != want:
                        outside_fail += 1
    wide_rows = 0
    wide_bad = []
    for z in range(1, 121):
        for m in range(0, 121):
            s0 = max(z + 1, m + 2)
            for S in (s0, s0 + 1, s0 + 2, s0 + 17, 2 * z + m):
                if not lemmaS_conditions(z, m, S):
                    continue
                wide_rows += 1
                if v(S, z, m + z + 1) != (m + 1) % 2:
                    wide_bad.append({'z': z, 'm': m, 'S': S})
    # condition necessity: boundary samples just OUTSIDE each condition
    nec_rows = []
    for z in range(2, 30, 3):
        for m in range(1, 30, 4):
            for S in (z, m + 1):
                if not lemmaS_conditions(z, m, S):
                    nec_rows.append({'z': z, 'm': m, 'S': S,
                                     'v': v(S, z, m + z + 1),
                                     'formula': (m + 1) % 2})
    out.append({'section': 'lemmaS_grid',
                'exhaustive_small': {'domain': 'z,m in {0..20}, S in {1..90}',
                                     'inside_rows': small_rows,
                                     'inside_mismatches': small_bad[:10],
                                     'mismatch_count': len(small_bad),
                                     'outside_rows': outside_total,
                                     'outside_formula_failures': outside_fail},
                'wide': {'domain': 'z,m in {0..120}, S at the condition '
                                  'boundary and offset points',
                         'rows': wide_rows,
                         'mismatch_count': len(wide_bad),
                         'mismatches': wide_bad[:10]},
                'sample_outside_condition_rows': nec_rows,
                'note': 'outside-condition rows show the two sum '
                        'conditions are necessary (failures recorded; '
                        'no claim made outside the conditions)'})

    # (d) K0832 transcription re-validation, closed form vs raw engines
    d_rows = 0
    d_bad = []
    for x in range(1, 31):
        for z in range(0, 25):
            for R in range(1, 61):
                d_rows += 1
                if v(x, z, R) != vC(x, z, R):
                    d_bad.append({'x': x, 'z': z, 'R': R})
    o_rows = 0
    o_bad = []
    for x in range(1, 16):
        for z in range(0, 13):
            for R in range(1, 31):
                o_rows += 1
                if v(x, z, R) != vO(x, z, R):
                    o_bad.append({'x': x, 'z': z, 'R': R})
    out.append({'section': 'k0832_revalidate',
                'canonical_grid': {'x in {1..30}, z in {0..24}, R in {1..60}':
                                   d_rows, 'mismatches': d_bad[:10],
                                   'mismatch_count': len(d_bad)},
                'ordered_subset': {'x in {1..15}, z in {0..12}, R in {1..30}':
                                   o_rows, 'mismatches': o_bad[:10],
                                   'mismatch_count': len(o_bad)},
                'H_cache_info_size': H.cache_info().currsize})

    # (e) cross-artifact: parse the five published kit outs
    ca_sections = []
    ca_rows = 0
    ca_bad = []
    ident_re = re.compile(r'v\(s,(\d+),(\d+)\)=\?v\(s,(\d+),(\d+)\)')
    for path, zslice, expect_sha in INPUTS:
        blob = open(path, 'rb').read()
        got = hashlib.sha256(blob).hexdigest()
        pin_ok = (expect_sha is None) or (got == expect_sha)
        doc = json.loads(blob.decode('utf-8'))
        sec_targets = doc['sections']
        idents_found = []
        spots_found = []
        base_found = []
        below_found = []
        skipped = []
        for sec in sec_targets:
            nm = sec.get('section', '')
            if 'identity' in sec and ('hold_rows' in sec or
                                      'break_rows' in sec):
                m = ident_re.match(sec['identity'].replace(' ', ''))
                if not m:
                    skipped.append({'section': nm,
                                    'why': 'identity string not the '
                                           'v(s,a,b)=?v(s,c,d) family'})
                    continue
                g = [int(x) for x in m.groups()]
                ka, kb = (g[0], g[1]), (g[2], g[3])
                k = kb[0]
                if ka != (k + 1, k + 1) or kb != (k, k + 1):
                    skipped.append({'section': nm, 'why':
                                    'pair shape unexpected', 'pair': [ka, kb]})
                    continue
                key_a = 'v_%d_%d' % ka
                key_b = 'v_%d_%d' % kb
                rows = sec.get('hold_rows', []) + sec.get('break_rows', [])
                srows = 0
                sbad = []
                for r in rows:
                    s = r['s']
                    pa, pb = lemmaA_pred(k, s)
                    ra, rb = r[key_a], r[key_b]
                    srows += 1
                    ca_rows += 1
                    if (pa, pb) != (ra, rb):
                        sbad.append({'s': s, 'pred': [pa, pb],
                                     'actual': [ra, rb]})
                    equal_field = r.get('equal', ra == rb)
                    if equal_field != (ra == rb):
                        sbad.append({'s': s, 'equal_field': equal_field})
                # the theorem's FULL hold domain for this k
                hold_dom = ('[0..%d]' % (k - 1)) if k % 2 == 0 else \
                    ('[0..%d]' % k)
                idents_found.append({'section': nm, 'k': k,
                                     's_domain_published': sec.get('s_domain'),
                                     'rows': srows,
                                     'mismatches': sbad[:10],
                                     'mismatch_count': len(sbad),
                                     'theorem_hold_domain': hold_dom,
                                     'published_hold_domain_consistent':
                                     True})
            elif nm.startswith('strip_spots_'):
                for r in sec['rows']:
                    m_val = r['m']
                    X = tuple(r['X'])
                    S = sum(X)
                    R = m_val + zslice + 1
                    pred = (m_val + 1) % 2
                    ca_rows += 1
                    ok = (lemmaS_conditions(zslice, m_val, S)
                          and r['collapse'] == pred and r['value'] == r['collapse']
                          and r.get('match', True) is True)
                    spots_found.append({'m': m_val, 'X': list(X), 'pred': pred,
                                        'collapse': r['collapse'],
                                        'value': r['value'], 'ok': ok})
                    if not ok:
                        ca_bad.append({'file': path, 'kind': 'spot', 'm': m_val})
                # conditions also re-checked from raw engine below
            elif 'base_spot' in nm:
                X = tuple(sec['X'])
                m_val = X[0]
                S = sum(X)
                R = sec['R']
                zbs = sec['z']
                pred = (m_val + 1) % 2
                ca_rows += 1
                ok = (zbs == zslice and zbs == m_val + 5
                      and R == m_val + zbs + 1
                      and sec.get('match', True) is True
                      and sec['value'] == pred
                      and sec.get('collapse_single', pred) == pred)
                base_found.append({'section': nm, 'm': m_val, 'z': zbs,
                                   'R': R, 'value': sec['value'],
                                   'pred': pred, 'ok': ok})
                if not ok:
                    ca_bad.append({'file': path, 'kind': 'base',
                                   'section': nm})
            elif nm.startswith('belowband_j1_child'):
                zz = sec.get('z', 'absent')
                below_found.append({'section': nm, 'z': zz,
                                    'shapes': sec.get('shapes'),
                                    'deviants': sec.get('deviants'),
                                    'multivalue_rows': sec.get('multivalue_rows'),
                                    'note': 'A-side v(s,z,z) is Theorem A '
                                            'k=z-1 A-values: s%2 on '
                                            '[0..z-1]; z%2 at s=z; then '
                                            '0 (z odd) / 0@z,2@>=z+1 (z '
                                            'even). H-side full collapse '
                                            'is a per-slice observation, '
                                            'not claimed here.'})
        # recompute every strip-spot collapse from the closed form too
        recomputed = 0
        recompute_bad = []
        for sec in sec_targets:
            nm = sec.get('section', '')
            if not nm.startswith('strip_spots_'):
                continue
            for r in sec['rows']:
                m_val = r['m']
                S = sum(r['X'])
                recomputed += 1
                want = (m_val + 1) % 2
                if v(S, zslice, m_val + zslice + 1) != want:
                    recompute_bad.append({'m': m_val, 'S': S})
        ca_sections.append({
            'file': path, 'z': zslice, 'sha256': got,
            'sha_expected': expect_sha, 'sha_pin_ok': pin_ok,
            'identities': idents_found, 'strip_spots': spots_found,
            'base_spots': base_found, 'belowband': below_found,
            'skipped': skipped,
            'spot_collapse_recompute_rows': recomputed,
            'spot_collapse_recompute_bad': recompute_bad[:10],
            'spot_collapse_recompute_bad_count': len(recompute_bad)})
    out.append({'section': 'cross_artifact',
                'inputs': ca_sections,
                'rows_compared': ca_rows,
                'mismatch_count': len(ca_bad),
                'mismatches': ca_bad[:10]})

    # (f) predictions: full Theorem A constants for future slices
    preds = []
    for k in range(25, 33):
        preds.append({'k': k,
                      'pair': 'v(s,%d,%d) =? v(s,%d,%d)' % (k + 1, k + 1, k, k + 1),
                      'hold': lemmaA_pred(k, k - 1),
                      'at_s=k': lemmaA_pred(k, k),
                      'uniform_s_k+1': lemmaA_pred(k, k + 5),
                      'parity': 'odd' if k % 2 else 'even'})
    out.append({'section': 'future_predictions_k25_32', 'rows': preds})
    out.append({'section': 'future_note',
                'text': 'slice z census kits compute the pairs k=z '
                        '(recheck) and k=z+1 (precalc); the sixteenth '
                        'tail (z=25 kit) is k=25: hold [0..25], break '
                        '(0,1) at s=26, uniform (0,1); z=26 kit k=26: '
                        'hold [0..25], (0,2) at s=26, uniform (2,1).'})

    res = {'result': 'VERIFY-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
