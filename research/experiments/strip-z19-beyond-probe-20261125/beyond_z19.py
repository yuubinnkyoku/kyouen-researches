#!/usr/bin/env python3
"""
beyond_z19: FROZEN spot-probe for the z=19 BEYOND/frontier series
(the direct continuation of three active observation series measured
by the published z18-min13 census kit; NO K slot claimed; no claim
made; observational only).

Scope (measures and reports; proves nothing):
  (a) m=10-row z=19 record (R=30; z=19 = z*(10)+1 = the FIRST beyond
      slice for min=10; the published z=18 frontier record measured
      EXACTLY 1 separation X=(10,10) UP 2v1 at the boundary slice).
      Enumeration IDENTICAL to the published z=18 record (S in
      {10..48}, X=(10,) u parts(S-10,10,3), arity<=3) for
      position-by-position cross-slice comparison. PREDECLARED
      candidate outcomes (from the z18 kit handoff): (i) the (8,8)
      analog flipped UP->DOWN one slice beyond the frontier
      (z=14 -> z=15) and persisted; measured (10,10) data decides
      whether the even-m frontier separations flip at +1 or vanish.
  (b) m=9-row z=19 record (R=29; z=19 = z*(9)+2 = the second odd-m
      beyond slice; published arc: z=17 FRONTIER {(9,10) UP 2v0};
      z=18 beyond {(9,10) UP 1v0} - persistence WITHOUT reabsorption
      with value decay 2->1, already DIFFERENT from the (8,8) arc
      which flipped direction at +1). Enumeration IDENTICAL to the
      published z=17/z=18 records (S in {9..47},
      X=(9,) u parts(S-9,9,3), 234 shapes). PREDECLARED candidates:
      (9,10) reabsorbs (first odd-m reabsorption), persists at 1v0,
      or decays to 0v0 (= collapse, i.e. reabsorption of the UP
      class).
  (c) m=8-row z=19 record (R=27; z=19 = z*(8)+5 = the fifth
      consecutive beyond slice; published arc: z14 {(8,8)UP} ->
      z15 {(8,8)DOWN} -> z16 {(8,8)DOWN,(8,10)UP} -> z17 {(8,10)DOWN}
      -> z18 {} (first EMPTY beyond record)). The z=19 entry tests
      whether the EMPTY beyond set is a stable terminal state or a
      new separation re-emerges (the z16 SHRINK->z17->z18 sequence
      suggests stability; no re-emergence has ever been observed
      after a position reabsorbs). Enumeration identical (S in
      {8..47}, X=(8,) u parts(S-8,8,3), 362 shapes).
  (d) TENTH-TAIL SUPPLY PRE-COMPUTATION (pure published K0832 closed
      form, engine-free): the z=19 analog of the published supply
      identities. The typology alternation observed through z=18
      (single point @ even z / hole+tail @ odd z, 4 consecutive data
      points) predicts the TENTH F-tail form at z=19 (odd) has a
      HOLE+TAIL profile. This section measures the closed-form pair
      v(s,20,20) vs v(s,19,20) over s in {0} u {12..57} and rechecks
      the z=18 identity v(s,19,19)=v(s,18,19) (published by the
      z18-min13 kit: hold {0} u {12..17}, break at s=18 as 0v2,
      uniform 2v1 for s>=19). NO prediction is asserted here; the
      raw break structure is recorded for the z=19 census/declaration
      lanes.
  (e) strip spots at the z=19 provisional claim positions for rows
      m in {13..17} (R=m+20, the T-Z19 claim positions for the
      in-band rows), X in {(m,m+1),(m,m+2),(m,m,m+1)}: 15 spot
      checks ahead of the z=19 census, plus the m=14 base spot
      X=(14,14) at R=34 (the T-Z19 base position analog of the
      published 0/1/0 base-spot alternation 0@z16, 1@z17, 0@z18).

Everything is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (beyond_z19.out).
"""

import hashlib, json
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


def row_record(sec, rlabel, anchors, R, z, m, smin, smax):
    H.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(max(S - m, 0), m, 3):
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
            's_domain': '{%d..%d}' % (smin, smax), 'arity_max': 4,
            'published_anchors': anchors, 'shapes': scnt,
            'separations': sep}


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    # (a) m=10-row z=19 record: first beyond slice for min=10
    out.append(row_record(
        'm10_row_z19_record',
        'observational_only_first_beyond_slice_zstar10_18_plus_1',
        'z=18 frontier (z18-min13 kit): 170 shapes EXACTLY 1 separation X=(10,10) S=20 UP 2v1; even-m arc anchor (8,8): UP@z14 frontier, DOWN@z15 (+1 flip), DOWN persist@z16, reabsorbed@z17',
        30, 19, 10, 10, 48))
    # (b) m=9-row z=19 record: second odd-m beyond slice
    out.append(row_record(
        'm9_row_z19_record',
        'observational_only_second_odd_m_beyond_slice_zstar9_17_plus_2',
        'z=17 frontier (z16-min9 kit): 234 shapes 1 separation (9,10) UP 2v0; z=18 beyond (z18-min13 kit): 234 shapes 1 separation (9,10) S=19 UP 1v0 (value decay, NO direction flip, NO reabsorption)',
        29, 19, 9, 9, 47))
    # (c) m=8-row z=19 record: fifth consecutive beyond slice
    out.append(row_record(
        'm8_row_z19_record',
        'observational_only_fifth_consecutive_beyond_slice_zstar8_14_plus_5',
        'arc: z14 {(8,8)UP} -> z15 {(8,8)DOWN} -> z16 {(8,8)DOWN,(8,10)UP} -> z17 {(8,10)DOWN} -> z18 {} (first EMPTY beyond record, z18-min13 kit)',
        27, 19, 8, 8, 47))
    # (d) TENTH-tail supply pre-computation (engine-free)
    holds = []
    breaks = []
    for s in [0] + list(range(12, 58)):
        a = v(s, 20, 20)
        b = v(s, 19, 20)
        row = {'s': s, 'v_20_20': a, 'v_19_20': b, 'equal': a == b}
        (holds if a == b else breaks).append(row)
    out.append({'section': 'tenth_tail_supply_identity_precalc',
                'label': 'observational_only_closed_form_precalc_z19_supply_identity',
                'identity': 'v(s,20,20) =? v(s,19,20)',
                's_domain': '{0} U {12..57}',
                'engine_free': 'pure published K0832 single-token closed form, no H recursion',
                'typology_note': 'the observed single@even-z / hole+tail@odd-z F-tail alternation (4 consecutive data points through z=18, z18-min13 kit) puts z=19 (odd) in the hole+tail class; NO prediction is asserted',
                'hold_rows': holds, 'break_rows': breaks})
    z18_holds = []
    z18_breaks = []
    for s in [0] + list(range(12, 58)):
        a = v(s, 19, 19)
        b = v(s, 18, 19)
        (z18_holds if a == b else z18_breaks).append(
            {'s': s, 'v_19_19': a, 'v_18_19': b})
    out.append({'section': 'z18_supply_identity_recheck',
                'label': 'observational_only_recheck_of_the_z18min13_published_identity',
                'identity': 'v(s,19,19) =? v(s,18,19)',
                's_domain': '{0} U {12..57}',
                'hold_rows': z18_holds, 'break_rows': z18_breaks})
    # (e) strip spots at the z=19 provisional claim positions
    spots = []
    for m in range(13, 18):
        for shp in [(m, m + 1), (m, m + 2), (m, m, m + 1)]:
            X = tuple(sorted(shp, reverse=True))
            S = sum(X)
            hv = H(m + 20, X, 19)
            ev = v(S, 19, m + 20)
            spots.append({'m': m, 'X': list(X), 'value': hv,
                          'collapse': ev, 'match': hv == ev})
    out.append({'section': 'strip_spots_m13_17_z19', 'rows': spots})
    # m=14 base spot (the T-Z19 floor-14 base position analog)
    w = H(34, (14, 14), 19)
    wv = v(28, 19, 34)
    out.append({'section': 'm14_base_spot', 'X': [14, 14], 'R': 34,
                'z': 19, 'value': w, 'collapse_single': wv,
                'match': w == wv})
    res = {'result': 'PROBE-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
