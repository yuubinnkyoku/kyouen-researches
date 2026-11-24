#!/usr/bin/env python3
"""explore4_d2_law.py -- mine the delta=2 law at z=0 and z=1.
Candidates: H = 1 - min(S,R)%2  (the 'complement' law), S-parity laws, etc.
Observation only.
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
        for m in range(1, 7):
            R = 2 * m + 2
            rows = []
            for X in shapes(m, R, 6):
                hc = H_canonical(R, X, z)
                S = sum(X)
                rows.append((X, S, hc))
            # all-m family full arity (up to 8 tokens of value m; S=8m; cap lemma)
            allm = []
            for a in range(1, 9):
                X = tuple([m] * a)
                allm.append([a, H_canonical(R, X, z), v(m*a, z, R)])
            clear()
            mix = [r for r in rows if max(r[0]) > m]
            # candidate laws on mixed
            cands = {
                '1minSR': lambda r: 1 - min(r[1], R) % 2,
                'minSR': lambda r: min(r[1], R) % 2,
                'S_mod2': lambda r: r[1] % 2,
                '1_S': lambda r: 1 - r[1] % 2,
            }
            res = {k: sum(1 for r in mix if f(r) != r[2]) for k, f in cands.items()}
            # breakdown: mixed by S vs R
            s_lt = [r for r in mix if r[1] < R]
            s_ge = [r for r in mix if r[1] >= R]
            lt_bad = sum(1 for r in s_lt if r[2] != (1 - r[1] % 2))
            ge_bad = sum(1 for r in s_ge if r[2] != (1 - R % 2))
            key = 'z%d_m%d' % (z, m)
            out[key] = {'R': R, 'nmix': len(mix), 'cand_bad': res,
                        'allm': allm,
                        'SltR_n': len(s_lt), 'SltR_bad_vs_1mSp2': lt_bad,
                        'SgeR_n': len(s_ge), 'SgeR_bad_vs_1Rp2': ge_bad}
            print(key, 'R=%d' % R, 'nmix=%d' % len(mix), 'cand_bad=', res,
                  'S<R: n=%d bad(1-S%%2)=%d' % (len(s_lt), lt_bad),
                  'S>=R: n=%d bad(1-R%%2)=%d' % (len(s_ge), ge_bad),
                  'allm(first6)=', allm[:6])
    json.dump(out, open('explore4_d2.json', 'w'), indent=1)
    print('written')

main()
