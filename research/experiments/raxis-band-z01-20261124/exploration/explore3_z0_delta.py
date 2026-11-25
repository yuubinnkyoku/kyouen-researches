#!/usr/bin/env python3
"""explore3_z0_delta.py -- z=0/z=1 beyond-edge (delta = R-2m) structure census.
Observation only. Dumps shape-level values for delta=1..6, m=2..4.
"""
import json, hashlib
from functools import lru_cache

ENGINE_SHA = hashlib.sha256(open('engine_block.py','rb').read()).hexdigest()
assert ENGINE_SHA == 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
exec(open('engine_block.py').read())
v = single_token
from itertools import combinations_with_replacement

def shapes(m, R, amax):
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
    out = {}
    for z in (0, 1):
        for m in range(2, 5):
            for delta in range(1, 7):
                R = 2 * m + delta
                rows = []
                for X in shapes(m, R, 5):
                    hc = H_canonical(R, X, z)
                    rows.append([list(X), sum(X), hc, v(sum(X), z, R)])
                clear()
                # candidate laws
                cand = {}
                def law(name, f):
                    bad = [r for r in rows if f(r) != r[2]]
                    cand[name] = len(bad)
                law('S_mod2', lambda r: r[1] % 2)
                law('S_plus1', lambda r: (r[1] + 1) % 2)
                law('minSR', lambda r: min(r[1], r[0][0] * 0 + R) % 2)
                law('R_mod2', lambda r: R % 2)
                law('S_plus_delta', lambda r: (r[1] + delta) % 2)
                # separate: classify by whether all tokens = m
                allm = [r for r in rows if len(set(r[0])) == 1]
                mix = [r for r in rows if len(set(r[0])) > 1]
                key = 'z%d_m%d_d%d' % (z, m, delta)
                out[key] = {
                    'n': len(rows), 'R': R,
                    'sep_from_v': sum(1 for r in rows if r[2] != r[3]),
                    'hv_hist': {str(h): sum(1 for r in rows if r[2] == h) for h in (0,1,2)},
                    'allm_vals': sorted(set(r[2] for r in allm)),
                    'mix_vals': sorted(set(r[2] for r in mix)),
                    'mix_vs_minSR': sum(1 for r in mix if r[2] != min(r[1], R) % 2),
                    'allm_vs_minSR': sum(1 for r in allm if r[2] != min(r[1], R) % 2),
                    'cand': cand,
                }
                print(key, 'R=%d' % R, 'sep=%d' % out[key]['sep_from_v'],
                      'hv=%s' % out[key]['hv_hist'],
                      'allm=%s' % out[key]['allm_vals'], 'mix=%s' % out[key]['mix_vals'],
                      'mixvsminSR=%d allmvsminSR=%d' % (out[key]['mix_vs_minSR'], out[key]['allm_vs_minSR']))
    json.dump(out, open('explore3_delta.json', 'w'), indent=1)
    print('written')

main()
