#!/usr/bin/env python3
"""explore7_lawc.py -- verify LAW-C on z=0 d=2 mixed:
H = 1  iff  mult(m)==1 or (no token >= m+2 and mult(m+1)==1); else 0.
Observation only. Engine sha-gated.
"""
import json, hashlib, time
from functools import lru_cache
from itertools import combinations_with_replacement

ENGINE_SHA = hashlib.sha256(open('engine_block.py','rb').read()).hexdigest()
assert ENGINE_SHA == 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
exec(open('engine_block.py').read())

def shapes(m, hi, amax, lo_m=1):
    for k in range(2, amax + 1):
        for c in combinations_with_replacement(range(1, hi + 1), k):
            if c[0] == 1 and max(c) > 1:
                yield tuple(reversed(c))
            elif c[0] > 1 and c[0] == m - 1 and False:
                pass

def mixed_min_m(m, hi, amax):
    # shapes with min exactly m (all tokens >= m), mixed
    for k in range(2, amax + 1):
        for c in combinations_with_replacement(range(max(m,1), hi + 1), k):
            if c[0] == m and max(c) > m:
                yield tuple(reversed(c))

t0 = time.time()
out = {'engine_sha': ENGINE_SHA, 'law': 'mult(m)==1 or (max<=m+1 and mult(m+1)==1) -> 1 else 0'}
for m in range(1, 9):
    R = 2 * m + 2
    hi = R + 2
    n = bad = 0
    badex = []
    for X in mixed_min_m(m, hi, 6):
        h = H_canonical(R, X, 0)
        mult0 = X.count(m)
        mult1 = X.count(m + 1)
        hasD = max(X) >= m + 2
        pred = 1 if (mult0 == 1 or (not hasD and mult1 == 1)) else 0
        n += 1
        if h != pred:
            bad += 1
            if len(badex) < 6: badex.append([list(X), sum(X), h, pred])
        H_canonical.cache_clear(); H_ordered.cache_clear()
    # samples with min m but including token m-... done
    out['m%d' % m] = {'n': n, 'bad': bad, 'badex': badex}
    print('m=%d R=%d n=%d bad=%d badex=%s' % (m, R, n, bad, badex[:4]), flush=True)
# m=1 special: min 1 shapes (1-tokens) - covered above with m=1 (tokens>=1, mixed)
out['elapsed_s'] = round(time.time() - t0, 1)
json.dump(out, open('explore7_lawc.json', 'w'), indent=1)
print('done %.1fs' % out['elapsed_s'])
