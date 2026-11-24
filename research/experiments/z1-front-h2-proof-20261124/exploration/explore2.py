#!/usr/bin/env python3
"""explore2: z1-delta-4 arm-1 census (C-IIz1-2 / C-LS2 fall-child region)
+ z1-delta-3 allm census (open registration data)."""
import json
from functools import lru_cache
from itertools import combinations_with_replacement
import importlib.util
spec = importlib.util.spec_from_file_location("eb", "engine_block.py")
eb = importlib.util.module_from_spec(spec); spec.loader.exec_module(eb)
H = eb.H_canonical

def shapes(m, hi, amax, mult=1):
    out = set()
    for k in range(1, amax + 1):
        for c in combinations_with_replacement(range(m, hi + 1), k):
            if c.count(m) != mult:
                continue
            t = tuple(sorted(c, reverse=True))
            if len(t) >= 2 and max(t) > m:
                out.add(t)
    return sorted(out)

res = {}
# E1: z1 delta-4 arm-1 mixed: H(2j+4; Y; 1) histogram + 2-check
d4_hist = {}
n2 = 0; tot = 0
for j in range(1, 7):
    R = 2 * j + 4
    for Y in shapes(j, j + 6, 4):
        h = H(R, Y, 1)
        d4_hist[str(h)] = d4_hist.get(str(h), 0) + 1
        tot += 1
        if h == 2: n2 += 1
res["E1_d4_arm1"] = [tot, n2, dict(sorted(d4_hist.items(), key=lambda x: int(x[0])))]
# E2: L-S fall shapes (j-1, j+2)@2j+2 exactly
ls_fall = {}
for j in range(1, 9):
    Y = (j - 1, j + 2) if j >= 2 else (2,)
    h = H(2 * j + 2, Y, 1)
    ls_fall[str(j)] = h
res["E2_LS_fall"] = ls_fall
# E3: class-E fall shapes (m-1, m^{q-1}) and with D remains @ z1-d4(m-1)
ce_fall_hist = {}
tot3 = 0; n2_3 = 0
for m in range(2, 7):
    j = m - 1
    R = 2 * j + 4
    for a in range(2, 7):
        for extra in [(), (m + 2,), (m + 3,), (m + 2, m + 2)]:
            Y = tuple(sorted((j,) + (m,) * (a - 1) + extra, reverse=True))
            if max(Y) <= j: continue
            h = H(R, Y, 1)
            ce_fall_hist[str(h)] = ce_fall_hist.get(str(h), 0) + 1
            tot3 += 1
            if h == 2: n2_3 += 1
res["E3_CE_fall"] = [tot3, n2_3, dict(sorted(ce_fall_hist.items(), key=lambda x: int(x[0])))]
# E4: z1 delta-3 allm census: H(2m+3; (m^a); 1)
d3_allm = {}
for m in range(1, 7):
    for a in range(2, 7):
        h = H(2 * m + 3, tuple([m] * a), 1)
        d3_allm[f"{m}^{a}"] = h
res["E4_d3_allm"] = d3_allm
print(json.dumps(res, indent=1, sort_keys=True))
