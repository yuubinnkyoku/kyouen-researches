#!/usr/bin/env python3
"""
verify_dshift_theorem: frozen corroboration audit for the D-SHIFT
TWO-SUPPLY FAMILY closed-form theorem (universal case analysis over
the published single-token closed form, pin bd5f22e4, strip-kit series
engine). The theorem was PROVEN BEFORE this audit (case analysis
published in the kit README and log); this script is a mechanical
corroboration audit, NOT the proof. The finite grids here only
corroborate the written case analysis and are NOT the basis of
universality.

THEOREM (d-shift two-supply family; published closed form v(x,z,R)):
for every integer k >= 1, every shift d >= 1 and every s >= 1, with

    A = v(s, k+d, k+d)      (advance seat: both z and R advanced by d)
    B = v(s, k,   k+d)      (lagging seat: z stays at k, R advanced)

  A-PART (hold then k+d-parity constant, no s cap):
    (A1) 1 <= s <= k+d-1:      A = s mod 2                    (HOLD)
    (A2) s >= k+d, k+d odd:    A = 2                          (uniform)
    (A3) s >= k+d, k+d even:   A = 0                          (uniform)

  B-PART (four pieces, no s cap):
    (B1) 1 <= s <= k-1:        B = s mod 2                    (HOLD)
    (B2) s = k, k+d odd and d <= k-1:   B = 2                 (lag break)
    (B3) s = k otherwise:      B = k mod 2                    (HOLD of A)
    (B4) k+1 <= s <= d (nonempty iff d >= k+1): B = s mod 2   (HOLD tail)
    (B5) s >= max(k+1, d+1):   B = d mod 2                    (uniform)

  IDENTITY REGION A = B (the two-supply identity):
  the hold set is exactly the union of
    (I1) [1..k-1]                                        (always)
    (I2) {k} iff k+d is even OR d >= k                   (else lag break)
    (I3) [k+1..d]                                        (iff d >= k+1)
    (I4) {s in [max(k+1,d+1) .. k+d-1] : s = d (mod 2)}  (striped zone)
    (I5) [k+d..infinity) iff k even AND d even           (uniform tail)
  and the break pairs are
    s = k (iff k+d odd and d <= k-1):                    (k%2, 2)
    striped zone s = d+1 (mod 2):                        ((d+1)%2, d%2)
    uniform tail k,d both odd:                           (0, 1)
    uniform tail k+d odd, d even:                        (2, 0)
    uniform tail k+d odd, d odd:                         (2, 1)

d = 1 INSTANTIATION: (A1) with d=1 gives A = s%2 on [1..k], (A2)/(A3)
at k+1 give 2/0 by k parity; (B1)-(B5) give s%2 on [1..k-1], the
k-even (0,2) lag break at s=k, and the uniform 1 tail — i.e. EXACTLY
the published single-token tail supply identity theorem
(single-token-tail-supply-identity-theorem-20261126) and K1334
Theorem A. Section (f) of this audit machine-checks that
instantiation point-by-point against that published case analysis.

d = 2 INSTANTIATION (the "two-supply family v(s,k+2,k+2) vs
v(s,k,k+2)" registered as open structural question (a) by the
single-token theorem log):
  k even: holds [1..k] (union the isolated k+1 SKIP broken pair
  (1,0)), then holds [k+2..infinity) as (0,0);
  k odd, k >= 3: holds [1..k-1] and the ISOLATED point s = k+1
  (both (0,0)), breaks (1,2) at s = k and (2,0) from s = k+2 on;
  k = 1: holds [1..2], breaks (2,0) from s = 3 on.

DEGENERATE BOUNDARY NOTE (inherited convention, recorded here for the
d-family): at the meaningless input s = 0 the engines return
H(R,(0,),z) = 1 on BOTH seats (the identity A = B still holds
engine-side) while the closed form returns 0 by its x <= 0
convention. No strip-kit measurement involves x = 0. Recorded in
section (g).

This file is a pure function of the pinned engine bytes; no
randomness, no hash-seed dependence, no wall-clock in the output.
stdout is the frozen artifact (verify_dshift_theorem.out).
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


def dshift_pair(s, k, d):
    """Independent implementation of the PROVEN case analysis (the
    written d-shift theorem): returns (A, B) with
    A = v(s,k+d,k+d), B = v(s,k,k+d) for s >= 1, k >= 1, d >= 1."""
    # A-part
    if s <= k + d - 1:
        A = s % 2
    else:
        A = 2 if (k + d) % 2 else 0
    # B-part
    if s <= k - 1:
        B = s % 2
    elif s == k:
        B = 2 if ((k + d) % 2 and d <= k - 1) else k % 2
    elif s <= d:  # k+1 <= s <= d, nonempty iff d >= k+1
        B = s % 2
    else:         # s >= max(k+1, d+1)
        B = d % 2
    return (A, B)


def zone_label(s, k, d):
    """Independent region-classification of the written identity-region
    theorem (derived from the region claims I1-I5, NOT from the pair
    formula): returns (label, expected_pair)."""
    if s <= k - 1:
        p = s % 2
        return ('I1_hold_low', (p, p))
    if s == k:
        if (k + d) % 2 and d <= k - 1:
            return ('lag_break', (k % 2, 2))
        p = k % 2
        return ('I2_hold_k', (p, p))
    if s <= d:  # k+1 <= s <= d
        p = s % 2
        return ('I3_hold_mid', (p, p))
    if s <= k + d - 1:  # striped zone max(k+1,d+1) .. k+d-1
        return ('I4_striped_hold' if s % 2 == d % 2
                else 'I4_striped_break', ((s) % 2, d % 2))
    # uniform tail s >= k+d
    pair = (2, d % 2) if (k + d) % 2 else (0, d % 2)
    if k % 2 == 0 and d % 2 == 0:
        return ('I5_uniform_hold', pair)
    lbl = ('I5_uniform_break_oddodd' if (k + d) % 2 == 0
           else ('I5_uniform_break_deven' if d % 2 == 0
                 else 'I5_uniform_break_dodd'))
    return (lbl, pair)


def published_d1(s, k):
    """Verbatim re-transcription (provenance: the published frozen audit
    supply_identity_theorem_audit.py of
    single-token-tail-supply-identity-theorem-20261126, function
    derived(s,k)): the PUBLISHED single-token tail supply identity case
    analysis, returns (A, B) = (v(s,k+1,k+1), v(s,k,k+1))."""
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
    #     k in 1..400, d in 1..12, s in 1..k+d+45 (pure closed form,
    #     engine-free)
    grid_bad = []
    grid_total = 0
    zone_bad = []
    zone_counts = {}
    for d in range(1, 13):
        for k in range(1, 401):
            for s in range(1, k + d + 46):
                A = v(s, k + d, k + d)
                B = v(s, k, k + d)
                dA, dB = dshift_pair(s, k, d)
                grid_total += 1
                if (A, B) != (dA, dB):
                    grid_bad.append({'k': k, 'd': d, 's': s,
                                     'measured': [A, B],
                                     'derived': [dA, dB]})
                lbl, exp = zone_label(s, k, d)
                zone_counts[lbl] = zone_counts.get(lbl, 0) + 1
                if exp != (A, B):
                    zone_bad.append({'k': k, 'd': d, 's': s, 'label': lbl,
                                     'measured': [A, B], 'expected': list(exp)})
    out.append({'section': 'closed_form_grid_audit',
                'k_domain': '{1..400}', 'd_domain': '{1..12}',
                's_policy': '1..k+d+45', 'points': grid_total,
                'mismatches': len(grid_bad),
                'all_match': len(grid_bad) == 0,
                'bad_rows_sample': grid_bad[:20]})
    out.append({'section': 'identity_region_audit',
                'note': 'independent region classification (zone_label '
                        'from the I1-I5 claims) vs measured pairs on the '
                        'same grid',
                'zone_label_counts': {k: zone_counts[k]
                                      for k in sorted(zone_counts)},
                'mismatches': len(zone_bad),
                'all_match': len(zone_bad) == 0,
                'bad_rows_sample': zone_bad[:20]})
    # (2) large-s extension (pure closed form, engine-free): far beyond
    #     every kit scan cap
    ext_bad = []
    ext_total = 0
    for d in [2, 3, 4, 5, 8, 13, 21]:
        for k in [1, 2, 3, 44, 45, 99, 100, 101, 199, 200]:
            for s in list(range(k + d + 46, k + d + 300, 7)) + [k + d + 5000]:
                A = v(s, k + d, k + d)
                B = v(s, k, k + d)
                dA, dB = dshift_pair(s, k, d)
                ext_total += 1
                if (A, B) != (dA, dB):
                    ext_bad.append({'k': k, 'd': d, 's': s,
                                    'measured': [A, B], 'derived': [dA, dB]})
    out.append({'section': 'large_s_extension_audit',
                'd_sample': [2, 3, 4, 5, 8, 13, 21],
                'k_sample': [1, 2, 3, 44, 45, 99, 100, 101, 199, 200],
                's_policy': 'k+d+46..k+d+300 step 7, plus k+d+5000',
                'points': ext_total, 'mismatches': len(ext_bad),
                'all_match': len(ext_bad) == 0})
    # (3) ENGINE spot audit: canonical AND ordered engines vs the derived
    #     case analysis on both seats (independent corroboration of the
    #     closed-form == engine equivalence on d-shift positions)
    spot_bad = []
    spot_total = 0
    spots = set()
    for k in range(1, 9):          # complete small grid
        for d in [1, 2, 3, 5]:
            for s in range(1, k + d + 7):
                spots.add((s, k, d))
    for k in [10, 12, 15, 20, 25, 31, 44]:   # sampled boundary rows
        for d in [2, 3, 4, 5, 9]:
            for s in [k - 1, k, k + 1, d - 1, d, d + 1, k + d - 1,
                      k + d, k + d + 1, 2 * k]:
                if s >= 1:
                    spots.add((s, k, d))
    for (s, k, d) in sorted(spots):
        R = k + d
        aC, aO = H(R, (s,), k + d), Ho(R, (s,), k + d)
        bC, bO = H(R, (s,), k), Ho(R, (s,), k)
        dA, dB = dshift_pair(s, k, d)
        spot_total += 1
        if (aC, aO, bC, bO) != (dA, dA, dB, dB):
            spot_bad.append({'k': k, 'd': d, 's': s,
                             'measured': [aC, aO, bC, bO],
                             'derived': [dA, dA, dB, dB]})
    out.append({'section': 'engine_spot_audit',
                'policy': 'complete k in 1..8 x d in {1,2,3,5} x s in 1..k+d+6, plus sampled k in {10,12,15,20,25,31,44} x d in {2,3,4,5,9} x s in {k-1,k,k+1,d-1,d,d+1,k+d-1,k+d,k+d+1,2k}',
                'points': spot_total, 'mismatches': len(spot_bad),
                'all_match': len(spot_bad) == 0,
                'bad_rows_sample': spot_bad[:20]})
    # (4) d=1 INSTANTIATION audit: the general-d formulas at d=1 must
    #     reproduce the PUBLISHED single-token theorem case analysis
    #     verbatim (published audit derived(s,k)), k in 1..400,
    #     s in 1..k+45
    d1_bad = []
    d1_total = 0
    for k in range(1, 401):
        for s in range(1, k + 46):
            dA, dB = dshift_pair(s, k, 1)
            pA, pB = published_d1(s, k)
            d1_total += 1
            if (dA, dB) != (pA, pB):
                d1_bad.append({'k': k, 's': s, 'general_d1': [dA, dB],
                               'published': [pA, pB]})
    out.append({'section': 'd1_instantiation_audit',
                'note': 'general-d case analysis instantiated at d=1 vs '
                        'the published single-token tail supply identity '
                        'case analysis (verbatim transcription from '
                        'supply_identity_theorem_audit.py of '
                        'single-token-tail-supply-identity-theorem-20261126)',
                'k_domain': '{1..400}', 's_policy': '1..k+45',
                'points': d1_total, 'mismatches': len(d1_bad),
                'all_match': len(d1_bad) == 0,
                'bad_rows_sample': d1_bad[:20]})
    # (5) degenerate s=0 boundary record: closed form vs engines
    s0 = []
    for (k, d) in [(1, 1), (2, 2), (12, 3), (31, 4), (44, 5)]:
        R = k + d
        cfA, cfB = v(0, k + d, R), v(0, k, R)
        aC, aO = H(R, (0,), k + d), Ho(R, (0,), k + d)
        bC, bO = H(R, (0,), k), Ho(R, (0,), k)
        s0.append({'k': k, 'd': d, 'closed_form': [cfA, cfB],
                   'canonical_engine': [aC, bC],
                   'ordered_engine': [aO, bO],
                   'note': 'degenerate zero-size token: engines give 1 at '
                           'both d-shift seats (hold A=B engine-side), '
                           'closed form uses its x<=0 -> 0 convention '
                           '(inherited degenerate convention, first '
                           'recorded by the single-token theorem audit); '
                           'NO strip-kit measurement involves x=0'})
    out.append({'section': 'degenerate_s0_boundary_record', 'rows': s0})
    # (6) corollary echo: d=2 family (open question (a) of the
    #     single-token theorem log) — the explicit structure
    cor = []
    for k in [1, 2, 3, 4, 5, 10, 15, 30, 44]:
        d = 2
        holds = []
        breaks = []
        for s in range(1, k + 10):
            A = v(s, k + d, k + d)
            B = v(s, k, k + d)
            (holds if A == B else breaks).append(
                {'s': s, 'AB': [A, B]})
        cor.append({'k': k, 'd': 2, 'scan': 's in 1..k+9',
                    'hold_rows': holds, 'break_rows': breaks})
    out.append({'section': 'd2_family_record',
                'note': 'the d=2 two-supply family (open structural '
                        'question (a) of '
                        '2026-11-26-single-token-tail-supply-identity-'
                        'theorem.md): k even -> holds [1..k] then [k+2..inf) '
                        'as (0,0) with the single striped break (1,0) at '
                        's=k+1; k odd k>=3 -> holds [1..k-1] and the '
                        'ISOLATED point k+1 as (0,0), breaks (1,2) at s=k '
                        'and (2,0) from s=k+2; k=1 -> holds [1..2], breaks '
                        '(2,0) from s=3. The rows below are drawn from the '
                        'measured closed form, not from the theorem.',
                'rows': cor})
    res = {'result': 'AUDIT-DONE', 'sections': out}
    print(json.dumps(res, sort_keys=True, separators=(',', ':')))


if __name__ == '__main__':
    main()
