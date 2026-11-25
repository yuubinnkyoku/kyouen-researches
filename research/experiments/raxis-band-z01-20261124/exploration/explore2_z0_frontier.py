#!/usr/bin/env python3
"""explore2_z0_frontier.py -- frontier-row classification exploration at z=0
and z=1: R = 2m+1, all shapes (min=m, tokens capped, arity<=5). Observation only.
"""
import json, hashlib
from functools import lru_cache
from itertools import combinations_with_replacement

ENGINE_SHA = hashlib.sha256(open('engine_block.py','rb').read()).hexdigest()
assert ENGINE_SHA == 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
exec(open('engine_block.py').read())
v = single_token

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
        for m in range(1, 8):
            R = 2 * m + 1
            rows = []
            for X in shapes(m, R, 5):
                hc = H_canonical(R, X, z)
                exp = v(sum(X), z, R)
                rows.append([list(X), hc, exp, hc != exp])
            clear()
            bad = [r for r in rows if r[3]]
            coll = [r for r in rows if not r[3]]
            hk2 = [r for r in bad if r[1] != 2]
            out['z%d_m%d' % (z, m)] = {
                'n': len(rows), 'separated': len(bad), 'collapsed': len(coll),
                'collapsed_shapes': [r[0] for r in coll],
                'collapsed_H': sorted(set(r[1] for r in coll)),
                'sep_not2': [r for r in hk2][:20],
                'hv2_count': sum(1 for r in bad if r[1] == 2),
            }
            d = out['z%d_m%d' % (z, m)]
            print('z=%d m=%d R=%d n=%d sep=%d coll=%d collshapes=%s sepnot2=%d' % (
                z, m, R, len(rows), len(bad), len(coll),
                str(d['collapsed_shapes'][:9]), len(hk2)))
    json.dump(out, open('explore2_frontier.json', 'w'), indent=1)
    print('written')

main()
