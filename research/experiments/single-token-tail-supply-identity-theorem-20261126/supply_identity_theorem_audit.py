#!/usr/bin/env python3
"""
supply_identity_theorem_audit: frozen audit for the SINGLE-TOKEN TAIL
SUPPLY IDENTITY theorem (closed-form case analysis over the published
single-token closed form, pin bd5f22e4, strip-kit series engine).
The theorem was PROVEN BEFORE this audit (case analysis published in
the kit README and log); this script is a mechanical corroboration
audit, NOT the proof. The proof is the written case analysis; the
finite grid here only corroborates it and is NOT the basis of
universality.

THEOREM (single-token tail supply identity; published closed form
v(x,z,R), row convention R=m+z+1). For every integer k >= 1 and every
integer s >= 1, with A = v(s,k+1,k+1) and B = v(s,k,k+1):

  (i) 1 <= s <= k-1:          A = B = s mod 2        (HOLD)
  (ii) s = k, k odd:          A = B = 1              (HOLD)
  (iii) s = k, k even:        A = 0, B = 2           (single break)
  (iv) s >= k+1, k even:      A = 2, B = 1           (uniform break)
  (v)  s >= k+1, k odd:       A = 0, B = 1           (uniform break)

Corollaries: every per-k tail supply pre-computation registered by the
strip kits (k=31..46 published, k=45/46 registered) is the restriction
of this theorem to its scan domain {0} U {12..k+34}; the theorem covers
ALL k >= 1 with NO upper cap on s, closing the per-k pre-computation
lane.

DEGENERATE BOUNDARY NOTE (discovered and recorded in this audit): at
the meaningless input s=0 (zero-size token) the engines return
H(R,(0,),z) = A = B = 1 while the closed form returns v(0,z,R) = 0 by
its x<=0 convention; the ENGINES still satisfy the identity A = B at
s=0. The closed form and the engines agree on all s >= 1 positions
sampled here and in every strip-kit battery to date; the divergence is
confined to the degenerate x=0 convention. No strip-kit measurement is
affected (strip row scans use parts >= m >= 13; tail scans are
closed-form only).

This file is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (supply_identity_theorem_audit.out).
FINITE observations only; the universal claim is the written case
analysis, NOT this run; NO K slot claimed; 11x11 empty board and all
standard roots UNKNOWN, unchanged; no verdict consumed.
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
Ho = ns['H_ordered']
v = ns['single_token']


def derived(s, k):
    """Independent implementation of the proven case analysis:
    returns (A, B) = (v(s,k+1,k+1), v(s,k,k+1)) for s >= 1, k >= 1."""
    if s <= k - 1:
        p = s % 2
        return (p, p)
    if s == k:
        return (k % 2, 2) if k % 2 == 0 else (1, 1)
    return (2, 1) if k % 2 == 0 else (0, 1)


def main():
    out = []
    out.append({'section': 'engine_gate', 'engine_sha': sha, 'pin': PIN,
                'gate': 'PASS'})
    # (1) grid audit: closed form vs the derived case analysis,
    #     k in 1..400, s in 1..k+45 (pure closed form, engine-free)
    grid_bad = []
    grid_total = 0
    for k in range(1, 401):
        for s in range(1, k + 46):
            A = v(s, k + 1, k + 1)
            B = v(s, k, k + 1)
            dA, dB = derived(s, k)
            grid_total += 1
            if (A, B) != (dA, dB):
                grid_bad.append({'k': k, 's': s, 'measured': [A, B],
                                 'derived': [dA, dB]})
    out.append({'section': 'closed_form_grid_audit',
                'k_domain': '{1..400}', 's_policy': '1..k+45',
                'points': grid_total, 'mismatches': len(grid_bad),
                'all_match': len(grid_bad) == 0,
                'bad_rows_sample': grid_bad[:20]})
    # (2) large-s extension (pure closed form, engine-free): far
    #     beyond every kit scan cap (k+34)
    ext_bad = []
    ext_total = 0
    for k in [1, 2, 3, 44, 45, 99, 100, 101, 199, 200]:
        for s in list(range(k + 46, k + 300, 7)) + [k + 5000]:
            A = v(s, k + 1, k + 1)
            B = v(s, k, k + 1)
            dA, dB = derived(s, k)
            ext_total += 1
            if (A, B) != (dA, dB):
                ext_bad.append({'k': k, 's': s, 'measured': [A, B],
                                'derived': [dA, dB]})
    out.append({'section': 'large_s_extension_audit',
                'k_sample': [1, 2, 3, 44, 45, 99, 100, 101, 199, 200],
                's_policy': 'k+46..k+300 step 7, plus k+5000',
                'points': ext_total, 'mismatches': len(ext_bad),
                'all_match': len(ext_bad) == 0})
    # (3) ENGINE spot audit: canonical AND ordered engines vs the
    #     derived case analysis (independent corroboration of the
    #     closed-form == engine equivalence on identity positions;
    #     this is the K0832 battery discipline of the strip kits)
    spot_bad = []
    spot_total = 0
    spots = set()
    for k in range(1, 15):  # complete small grid
        for s in range(1, k + 11):
            spots.add((s, k))
    for k in [15, 16, 20, 21, 30, 31, 43, 44, 50, 51, 64, 65]:
        for s in [k - 1, k, k + 1, k + 2, k + 10, 2 * k]:
            if s >= 1:
                spots.add((s, k))
    for (s, k) in sorted(spots):
        R = k + 1
        aC, aO = H(R, (s,), k + 1), Ho(R, (s,), k + 1)
        bC, bO = H(R, (s,), k), Ho(R, (s,), k)
        dA, dB = derived(s, k)
        spot_total += 1
        if (aC, aO, bC, bO) != (dA, dA, dB, dB):
            spot_bad.append({'k': k, 's': s,
                             'measured': [aC, aO, bC, bO],
                             'derived': [dA, dA, dB, dB]})
    out.append({'section': 'engine_spot_audit',
                'policy': 'complete k in 1..14 x s in 1..k+10, plus sampled k in {15,16,20,21,30,31,43,44,50,51,64,65} x s in {k-1,k,k+1,k+2,k+10,2k}',
                'points': spot_total, 'mismatches': len(spot_bad),
                'all_match': len(spot_bad) == 0,
                'bad_rows_sample': spot_bad[:20]})
    # (4) degenerate s=0 boundary record: closed form vs engines
    s0 = []
    for k in [1, 12, 31, 44, 45]:
        R = k + 1
        cfA, cfB = v(0, k + 1, R), v(0, k, R)
        aC, aO = H(R, (0,), k + 1), Ho(R, (0,), k + 1)
        bC, bO = H(R, (0,), k), Ho(R, (0,), k)
        s0.append({'k': k, 'closed_form': [cfA, cfB],
                   'canonical_engine': [aC, bC],
                   'ordered_engine': [aO, bO],
                   'note': 'degenerate zero-size token: engines give 1 at '
                           'both identity seats (hold A=B), closed form '
                           'uses its x<=0 -> 0 convention; NO strip-kit '
                           'measurement involves x=0 (row scans use parts '
                           '>= m >= 13, tail scans are closed-form only)'})
    out.append({'section': 'degenerate_s0_boundary_record', 'rows': s0})
    # (5) corollary echo: the published per-k tail supply pre-computations
    out.append({'section': 'corollary_record',
                'note': 'the strip-kit per-k tail supply identity scans '
                        '(z-tail pre-computations k=31..46 published by the '
                        'decay/wave/fifth/sixth-wave kits, k=45/46 '
                        'registered in the sixth-wave log S5 item 4) are '
                        'the restrictions of the proven theorem to their '
                        'scan domains {0} U {12..k+34}; the theorem holds '
                        'for ALL k >= 1 and ALL s >= 1 with no cap'})
    res = {'result': 'AUDIT-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
