#!/usr/bin/env python3
"""explore1_z0_raw.py -- z=0 (and z=1 comparison) R-axis raw census.
Engine block machine-cut from the published z11 predecl kit
(sha256 bd5f22e415a78368c9b798296bc84948d5...). Observation only; no claims.

Usage: python3 explore1_z0_raw.py
"""
import json, hashlib
from itertools import combinations_with_replacement
from functools import lru_cache

ENGINE_SHA = hashlib.sha256(open('engine_block.py', 'rb').read()).hexdigest()
assert ENGINE_SHA == 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'

exec(open('engine_block.py').read())

v = single_token

# published cap lemma (K0838/K0832 artifact line): token values >= R+1 can be
# replaced by R+1 without changing H (machine check below anyway in-sweep uses
# explicit shapes; cap applied for state-space boundedness in exploration).
def capX(X, R):
    return tuple(sorted((min(t, R + 1) for t in X), reverse=True))

def shapes(m, R, amax):
    """all canonical multisets with min exactly m, tokens capped at R+1,
    arity 1..amax, S unbounded (all tokens in [m, R+1])."""
    out = []
    hi = R + 1
    for k in range(1, amax + 1):
        for c in combinations_with_replacement(range(m, hi + 1), k):
            if c[0] == m:
                out.append(tuple(reversed(c)))
    return out

def clear():
    H_ordered.cache_clear(); H_canonical.cache_clear()

def main():
    out = {'engine_sha256': ENGINE_SHA}
    # E0: engine sanity vs published single-token closed form
    bad0 = 0
    for z in range(0, 4):
        for x in range(1, 11):
            for R in range(0, 26):
                hc = H_canonical(R, (x,), z)
                if hc != v(x, z, R):
                    bad0 += 1
    out['E0_single_vs_closed'] = {'bad': bad0}
    clear()

    # C1: z=0 collapse census: m=2..8, k=1..m  (R=m+k<=2m)
    coll = {}
    for m in range(2, 9):
        for k in range(1, m + 1):
            R = m + k
            bad = 0; n = 0; det = []
            for X in shapes(m, R, 5):
                hc = H_canonical(R, X, 0)
                exp = v(sum(X), 0, R)
                n += 1
                if hc != exp:
                    bad += 1
                    if len(det) < 5: det.append([list(X), hc, exp])
            clear()
            coll['m%d_k%d' % (m, k)] = {'n': n, 'bad': bad, 'det': det}
            print('z0 collapse m=%d k=%d R=%d n=%d bad=%d' % (m, k, R, n, bad))
    out['z0_collapse'] = coll

    # C2: z=0 just-beyond census: k=m+1, m+2 (R=2m+1, 2m+2)
    beyond = {}
    for m in range(2, 8):
        for k in range(m + 1, m + 3):
            R = m + k
            bad = 0; n = 0; vals = {}; hvs = {}
            for X in shapes(m, R, 5):
                hc = H_canonical(R, X, 0)
                exp = v(sum(X), 0, R)
                n += 1
                if hc != exp:
                    bad += 1
                hvs.setdefault(tuple(sorted(hc for _ in [0])), None)
                key = hc
                vals.setdefault(key, []).append(list(X)[:3])
            clear()
            beyond['m%d_k%d' % (m, k)] = {'n': n, 'sep': bad, 'hv_hist': {str(a): len(b) for a, b in vals.items()}}
            print('z0 beyond m=%d k=%d R=%d n=%d separated=%d hv_hist=%s' % (m, k, R, n, bad, {str(a): len(b) for a, b in vals.items()}))
    out['z0_beyond'] = beyond

    # C3: z=1 collapse census: m=2..8, k=1..m+1
    coll1 = {}
    for m in range(2, 8):
        for k in range(1, m + 2):
            R = m + k
            bad = 0; n = 0; det = []
            for X in shapes(m, R, 5):
                hc = H_canonical(R, X, 1)
                exp = v(sum(X), 1, R)
                n += 1
                if hc != exp:
                    bad += 1
                    if len(det) < 5: det.append([list(X), hc, exp])
            clear()
            coll1['m%d_k%d' % (m, k)] = {'n': n, 'bad': bad, 'det': det}
            print('z1 m=%d k=%d R=%d n=%d bad=%d' % (m, k, R, n, bad))
    out['z1_census'] = coll1

    json.dump(out, open('explore1_z0_raw.json', 'w'), indent=1)
    print('written')

main()
