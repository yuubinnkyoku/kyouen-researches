#!/usr/bin/env python3
"""explore (pre-declaration, K1284 candidate)"""
import json, importlib.util
from itertools import combinations_with_replacement
spec = importlib.util.spec_from_file_location("eb", "engine_block.py")
eb = importlib.util.module_from_spec(spec); spec.loader.exec_module(eb)
H = eb.H_canonical

def shapes(m, hi, amax, mult=1):
    out = set()
    for k in range(1, amax + 1):
        for c in combinations_with_replacement(range(m, hi + 1), k):
            if c.count(m) != mult: continue
            t = tuple(sorted(c, reverse=True))
            if len(t) >= 2 and max(t) > m: out.add(t)
    return sorted(out)

res = {}
# E1: T-L4z1: arm-1 @ z1-d4, max >= j+2 -> 0; collect nonzero values found
bad = []; hist = {}; n = 0
for j in range(1, 8):
    R = 2*j + 4
    for Y in shapes(j, j+7, 4):
        if max(Y) < j + 2: continue
        h = H(R, Y, 1); n += 1
        hist[str(h)] = hist.get(str(h), 0) + 1
        if h != 0: bad.append([j, Y, h])
# tall giants: huge tokens
for j in range(1, 5):
    R = 2*j + 4
    for extra in [(), (j+1,), (j+1, j+1)]:
        for big in [10, 15, 25, 40]:
            Y = tuple(sorted((j, big) + extra, reverse=True))
            h = H(R, Y, 1); n += 1
            if h != 0: bad.append([j, Y, h])
res["E1_L4"] = [n, len(bad), dict(sorted(hist.items())), bad[:10]]

# E2: L-Z5F: (m, U) @ 2m+5, U tokens in [m+2, ...], max >= m+3 -> != 0
bad2 = []; n2 = 0
for m in range(1, 7):
    R = 2*m + 5
    for k in range(1, 4):
        for c in combinations_with_replacement(range(m+2, m+8), k):
            U = tuple(sorted(c, reverse=True))
            if max(U) < m + 3: continue
            h = H(R, (m,) + U, 1); n2 += 1
            if h == 0: bad2.append([m, (m,)+U, h])
res["E2_Z5F"] = [n2, len(bad2), bad2[:10]]

# E3: T-LS2: (j, j+2) @ 2j+3 -> 2
bad3 = []; vals = {}
for j in range(1, 12):
    h = H(2*j+3, (j, j+2), 1); vals[str(j)] = h
    if h != 2: bad3.append([j, h])
res["E3_LS2"] = [len(vals), bad3, vals]

# E4: T-IIz1-2: class E @ 2m+3 -> 2
bad4 = []; n4 = 0
for m in range(2, 7):
    R = 2*m + 3
    for q in range(2, 5):
        for k in range(0, 4):
            for c in combinations_with_replacement(range(m+1, m+6), k):
                Y = tuple(sorted((m,)*q + c, reverse=True))
                # class E: mult(m)>=2, mixed, non-arm-2
                if max(Y) == m: continue
                arm2 = (max(Y) <= m+1) and (Y.count(m+1) == 1)
                if arm2: continue
                h = H(R, Y, 1); n4 += 1
                if h != 2: bad4.append([m, Y, h])
res["E4_IIz12"] = [n4, len(bad4), bad4[:10]]

# E5: T-ALPHA: arm-1 @ 2m+3 -> 2 iff (m,m+2) else 1
bad5 = []; n5 = 0; h1 = 0; h2 = 0
for m in range(1, 8):
    R = 2*m + 3
    for Y in shapes(m, m+7, 5):
        h = H(R, Y, 1); n5 += 1
        exp = 2 if Y == (m+2, m) else 1
        if h == 1: h1 += 1
        elif h == 2: h2 += 1
        if h != exp: bad5.append([m, Y, h, exp])
res["E5_ALPHA"] = [n5, len(bad5), {"ones": h1, "twos": h2}, bad5[:10]]

# E6: floors
f = {}
f["G4z2_(2,2)"] = H(4, (2,2), 2)
f["G4z2_(2,3)"] = H(4, (2,3), 2)
f["G4z2_(3,3)"] = H(4, (3,3), 2)
f["G4z2_(2,2,2)"] = H(4, (2,2,2), 2)
f["W411"] = H(4, (1,1), 1)
f["v_3_2_4"] = H(4, (3,), 2)
f["v_2_2_4"] = H(4, (2,), 2)
f["v_5_2_4"] = H(4, (5,), 2)
f["B_12_d5z1"] = H(5, (1,2), 1)
# BC5 singles: v(x,2,5)=1 for x>=3
b = [x for x in range(3, 21) if H(5, (x,), 2) != 1]
f["BC5_single_bad"] = b
# BC5 multi: min>=2 multi @5z2 nonzero
b2 = []
for k in range(2, 5):
    for c in combinations_with_replacement(range(2, 9), k):
        Y = tuple(sorted(c, reverse=True))
        if H(5, Y, 2) == 0: b2.append(Y)
f["BC5_multi_bad"] = b2
res["E6_floors"] = f

# E7 (open data): pure-c1 @ z1-d4 census (j, (j+1)^c)
pc = {}
for j in range(1, 7):
    R = 2*j + 4
    for c in range(1, 6):
        Y = tuple(sorted((j, (j+1)*c), reverse=True))
        pc[f"{j}:{c}"] = H(R, Y, 1)
res["E7_purec1_d4_OPEN"] = pc

# E8 (open data): z0-d4 arm-1 census by shape class
z4 = {}
for m in range(1, 7):
    R = 2*m + 4
    for Y in shapes(m, m+6, 3):
        if max(Y) < m+2: continue  # high-gap-ish only (no (m+1)-token means max>=m+2)
        h = H(R, Y, 0)
        key = "gap2" if max(Y) == m+2 else "gap>=3"
        z4.setdefault(key, {}).setdefault(str(h), 0)
        z4[key][str(h)] += 1
res["E8_z0d4_arm1_OPEN"] = z4

# E9: T-ALPHA row-1 wide (1, U) @5z1 with |U|>=2
bad9 = []; n9 = 0
for k in range(2, 5):
    for c in combinations_with_replacement(range(2, 8), k):
        Y = tuple(sorted((1,) + c, reverse=True))
        h = H(5, Y, 1); n9 += 1
        exp = 2 if Y == (3, 1) else 1
        if h != exp: bad9.append([Y, h, exp])
res["E9_alpha_row1_wide"] = [n9, len(bad9), bad9[:8]]

print(json.dumps(res, indent=1, sort_keys=True, default=str))
