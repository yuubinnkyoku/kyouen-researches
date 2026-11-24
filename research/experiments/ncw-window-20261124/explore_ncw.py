#!/usr/bin/env python3
"""explore_ncw: PRE-DECLARATION exploration for the non-congruent window
collapse package (T-NCW-P / T-NCW-B): the transition window rows
1 <= k <= z-1 with k NOT congruent z (mod 2), pairs and beds — the exact
O1'/O2 open registration left by K1309.

Claim under test (discovered in this exploration, then typed-verified):

  T-NCW-P: g* := z-2k.  H(2m+g+k; (m, m+g); z) =
            [g odd]                     if g* <= 0 or g > g* or 2m+g < z
            2                           if (g == g* or g == z-2m) and 1<=g<=g* and 2m+g >= z
            [g even]                    otherwise (the flip wedge: g < g*, 2m+g > z)
  T-NCW-B: g* := z-2k, r := (z-1)//2.  H(2a+k; (a, a); z) =
            0                           if g* < 0 (i.e. 2k > z)
            0 if a <= r else 2          if g* == 0 (z even, k = z/2)
            0 if a <= r else (2 if a == r+1 else 1)   if z even, g* > 0
            0 if a <= r else 1          if z odd (g* > 0)

Deterministic output only. Engine: engine_block.py (published chain sha
582c93c1..., embedded verbatim in verify_k1310.py behind the startup gate).
"""
import engine_block as eb

H = eb.H_canonical
HO = eb.H_ordered


def val(R, X, z):
    return H(R, tuple(sorted(X, reverse=True)), z)


def valO(R, X, z):
    return HO(R, tuple(X), z)


def IND(b):
    return 1 if b else 0


def P(k, z, m, g):
    gs = z - 2 * k
    if gs <= 0 or g > gs or 2 * m + g < z:
        return IND(g % 2 == 1)
    if g == gs or g == z - 2 * m:
        return 2
    return IND(g % 2 == 0)


def Bm(k, z, a):
    gs = z - 2 * k
    if gs < 0:
        return 0
    r = (z - 1) // 2
    if a <= r:
        return 0
    if z % 2 == 1:
        return 1
    if gs == 0:
        return 2
    if a == r + 1:
        return 2
    return 1


def ncw_ks(z):
    return [kk for kk in range(1, z) if (kk % 2) != (z % 2)]


print('=== X1: T-NCW-P pair census vs claim, z3..16, m1..8, g1..32 ===')
tot = bad = 0
import collections
region = collections.Counter()
rmap = {}
for z in range(3, 17):
    ptot = pbad = 0
    for m in range(1, 9):
        for g in range(1, 33):
            for k in ncw_ks(z):
                e = val(2 * m + g + k, (m, m + g), z)
                c = P(k, z, m, g)
                ptot += 1
                gs = z - 2 * k
                if gs <= 0 or g > gs or 2 * m + g < z:
                    rr = 'N'
                elif g == gs or g == z - 2 * m:
                    rr = 'T2'
                else:
                    rr = 'F'
                region[rr] += 1
                if e != c:
                    pbad += 1
                    if pbad < 6:
                        print(f'  BAD z={z} m={m} g={g} k={k} v={e} pred={c}')
    H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'X1 total={tot} bad={bad} regions={dict(region)}')
print()

print('=== X2: T-NCW-B bed census vs claim, z3..18, a1..26 ===')
tot = bad = 0
for z in range(3, 19):
    ptot = pbad = 0
    for a in range(1, 27):
        for k in ncw_ks(z):
            e = val(2 * a + k, (a, a), z)
            c = Bm(k, z, a)
            ptot += 1
            if e != c:
                pbad += 1
                if pbad < 6:
                    print(f'  BAD z={z} a={a} k={k} v={e} pred={c}')
    H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'X2 total={tot} bad={bad}')
print()

print('=== X3: value-2 localization check (all 2s lie on the two bands) ===')
print('    bands: dominant g = z-2k (m >= k implied) and diagonal g = z-2m')
tot = bad = 0
for z in range(3, 17):
    for m in range(1, 9):
        for g in range(1, 33):
            for k in ncw_ks(z):
                e = val(2 * m + g + k, (m, m + g), z)
                tot += 1
                onband = (g == z - 2 * k and 2 * m + g >= z) or (g == z - 2 * m and g >= 1 and 2 * m + g >= z and g <= z - 2 * k)
                if e == 2 and not onband:
                    bad += 1
                    if bad < 8:
                        print(f'  OFFBAND z={z} m={m} g={g} k={k}')
                if e != 2 and onband and P(k, z, m, g) == 2:
                    bad += 1
    H.cache_clear()
print(f'X3 total={tot} offband_or_missing={bad}')
print()

print('=== X4: typed packet closure (children from claims + published laws) ===')
print('    pairs z2..12, m1..6, g1..24; beds z2..12, a1..12 ===')


def q_odd(x):
    return x if x % 2 else x - 1


def st(x, p, R):
    return eb.single_token(x, p, R)


def f0(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 1)
    return IND(d % 2 == 0)


def g1(d):
    if d == 1:
        return 2
    if d <= 0:
        return IND(d % 2 == 0)
    return IND(d % 2 == 1)


def Lw(w):
    return 2 * ((w + 1) // 2)


def sw(w):
    return 2 * (w // 2)


def Tw(w, d):
    return g1(d) if w % 2 else f0(d)


def cpsfG(w, R, d):
    if R < Lw(w):
        return 2 * (R % 2)
    return Tw(w, d - sw(w))


def mexs(vals):
    s = set(vals)
    i = 0
    while i in s:
        i += 1
    return i


def tp_ch(m, g, k, z):
    kids = []
    if m >= 2:
        kids.append(P(k, z, m - 1, g + 1))
    else:
        kids.append(st(g + 1, z + 1, g + k + 1))
    if g >= 2:
        kids.append(P(k, z, m, g - 1))
    else:
        kids.append(Bm(k, z, m))
    if k >= 2:
        kids.append(1 ^ P(k - 1, z - 1, m, g))
    else:
        kids.append(1 ^ cpsfG(z - 1, 2 * m + g, g))
    return kids


def tb_ch(a, k, z):
    kids = []
    if a >= 2:
        kids.append(P(k, z, a - 1, 1))
    else:
        kids.append(st(1, z + 1, k + 1))
    if k >= 2:
        kids.append(1 ^ Bm(k - 1, z - 1, a))
    else:
        kids.append(1 ^ cpsfG(z - 1, 2 * a, 0))
    return kids


tot = badt = bade = 0
for z in range(2, 13):
    pt = bt = be = 0
    for m in range(1, 7):
        for g in range(1, 25):
            for k in ncw_ks(z):
                kids = tp_ch(m, g, k, z)
                mc = mexs(kids)
                e = val(2 * m + g + k, (m, m + g), z)
                pt += 1
                if mc != P(k, z, m, g):
                    bt += 1
                    if bt < 4:
                        print(f'  BADT z={z} m={m} g={g} k={k} mex={mc} claim={P(k,z,m,g)} kids={kids}')
                if e != mc:
                    be += 1
                    if be < 4:
                        print(f'  BADE z={z} m={m} g={g} k={k} eng={e} mex={mc} kids={kids}')
    for a in range(1, 13):
        for k in ncw_ks(z):
            kids = tb_ch(a, k, z)
            mc = mexs(kids)
            e = val(2 * a + k, (a, a), z)
            pt += 1
            if mc != Bm(k, z, a):
                bt += 1
                if bt < 4:
                    print(f'  BADT z={z} a={a} k={k} mex={mc} claim={Bm(k,z,a)} kids={kids}')
            if e != mc:
                be += 1
                if be < 4:
                    print(f'  BADE z={z} a={a} k={k} eng={e} mex={mc} kids={kids}')
    H.cache_clear()
    tot += pt
    badt += bt
    bade += be
    print(f'  z={z}: pts={pt} bad_typed={bt} bad_engine={be}')
print(f'X4 total={tot} bad_typed_mex={badt} bad_typed_vs_engine={bade}')
print()

print('=== X5: cross-engine canonical vs ordered, NCW samples ===')
tot = bad = 0
for z in (3, 4, 7, 11):
    for m in range(1, 4):
        for g in range(1, 9):
            for k in ncw_ks(z):
                c = val(2 * m + g + k, (m, m + g), z)
                o = valO(2 * m + g + k, (m, m + g), z)
                tot += 1
                if c != o:
                    bad += 1
    for a in range(1, 4):
        for k in ncw_ks(z):
            c = val(2 * a + k, (a, a), z)
            o = valO(2 * a + k, (a, a), z)
            tot += 1
            if c != o:
                bad += 1
    H.cache_clear()
print(f'X5 total={tot} bad={bad}')
print()

print('=== X6: OBS-NCW subsumption (K1309 D10 frozen 35-row table) ===')
frozen = {
    '3,2': {0: 18, 1: 18}, '4,1': {0: 17, 1: 16, 2: 3},
    '4,3': {0: 18, 1: 18}, '5,2': {0: 18, 1: 16, 2: 2},
    '5,4': {0: 18, 1: 18}, '6,1': {0: 16, 1: 16, 2: 4},
    '6,3': {0: 18, 1: 18}, '6,5': {0: 18, 1: 18},
    '7,2': {0: 17, 1: 16, 2: 3}, '7,4': {0: 18, 1: 18},
    '7,6': {0: 18, 1: 18}, '8,1': {0: 15, 1: 16, 2: 5},
    '8,3': {0: 17, 1: 18, 2: 1}, '8,5': {0: 18, 1: 18},
    '8,7': {0: 18, 1: 18}, '9,2': {0: 17, 1: 16, 2: 3},
    '9,4': {0: 18, 1: 18}, '9,6': {0: 18, 1: 18},
    '9,8': {0: 18, 1: 18}, '10,1': {0: 15, 1: 16, 2: 5},
    '10,3': {0: 17, 1: 18, 2: 1}, '10,5': {0: 18, 1: 18},
    '10,7': {0: 18, 1: 18}, '10,9': {0: 18, 1: 18},
    '11,2': {0: 17, 1: 16, 2: 3}, '11,4': {0: 18, 1: 18},
    '11,6': {0: 18, 1: 18}, '11,8': {0: 18, 1: 18},
    '11,10': {0: 18, 1: 18}, '12,1': {0: 15, 1: 16, 2: 5},
    '12,3': {0: 17, 1: 18, 2: 1}, '12,5': {0: 18, 1: 18},
    '12,7': {0: 18, 1: 18}, '12,9': {0: 18, 1: 18},
    '12,11': {0: 18, 1: 18},
}
tot = bad = badc = 0
for z in range(3, 13):
    for m in range(1, 4):
        for g in range(1, 13):
            for k in range(1, z):
                if (k % 2) == (z % 2):
                    continue
                e = val(2 * m + g + k, (m, m + g), z)
                tot += 1
                key = f'{z},{k}'
                d = frozen[key]
                d[e] = d.get(e, 0) - 1
                if e != P(k, z, m, g):
                    badc += 1
    H.cache_clear()
for key, d in frozen.items():
    if any(v != 0 for v in d.values()):
        bad += 1
print(f'X6 cells={tot} frozen_mismatch_rows={bad} claim_bad={badc}')
print()

print('=== X7: band k=0 gates (K1303 transcription) w1..12 ===')
tot = bad = 0
for w in range(1, 13):
    for m in range(1, 5):
        for g in range(1, 17):
            e = val(2 * m + g, (m, m + g), w)
            cp = cpsfG(w, 2 * m + g, g)
            tot += 1
            if e != cp:
                bad += 1
                if bad < 6:
                    print(f'  BAD w={w} m={m} g={g} e={e} cp={cp}')
    for a in range(1, 7):
        e = val(2 * a, (a, a), w)
        cp = cpsfG(w, 2 * a, 0)
        tot += 1
        if e != cp:
            bad += 1
            if bad < 6:
                print(f'  BADB w={w} a={a} e={e} cp={cp}')
    H.cache_clear()
print(f'X7 total={tot} bad={bad}')
print()

print('=== X8: far stress z {24, 28}, m1..6, g1..24, a1..20 ===')
tot = bad = 0
for z in (24, 28):
    ptot = pbad = 0
    for m in range(1, 7):
        for g in range(1, 25):
            for k in ncw_ks(z):
                e = val(2 * m + g + k, (m, m + g), z)
                ptot += 1
                if e != P(k, z, m, g):
                    pbad += 1
                    if pbad < 6:
                        print(f'  BAD z={z} m={m} g={g} k={k} v={e} pred={P(k,z,m,g)}')
    H.cache_clear()
    for a in range(1, 21):
        for k in ncw_ks(z):
            e = val(2 * a + k, (a, a), z)
            ptot += 1
            if e != Bm(k, z, a):
                pbad += 1
                if pbad < 6:
                    print(f'  BADB z={z} a={a} k={k} v={e} pred={Bm(k,z,a)}')
    H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'X8 total={tot} bad={bad}')
print()
print('ALL STAGES COMPLETE')
