#!/usr/bin/env python3
"""explore_wc: PRE-DECLARATION exploration for the window-congruent collapse
package (T-WC / T-WBC): the transition window rows 1<=k<=z-1 with k congruent
z (mod 2).

Claim under test (K1308 OBS-WC universalization candidate):
  T-WC:  pair  H(2m+g+k; (m, m+g); z) = ZDIAG(g, z)  for ALL window k
         (independent of k and m), where ZDIAG(g,z) = [g odd] (g<=z) /
         2 (g=z+1) / [g even] (g>=z+2)  -- the published K1308 Z-DIAG law.
  T-WBC: bed   H(2a+k; (a, a); z) = 0 for ALL window k.

Deterministic output only. Engine: engine_block.py (published chain sha
582c93c1...), embedded verbatim in verify_k1309.py behind the startup gate.
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


def zdiag(g, z):
    if g <= z:
        return IND(g % 2 == 1)
    if g == z + 1:
        return 2
    return IND(g % 2 == 0)


# K1303 general-w band transcription (T-GEPSF / T-GEBED; same law cpsfG).
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


def q_odd(k):
    return k if k % 2 else k - 1


# L-BE: closed-form B-exit table for window pairs at m=1
# b(k) = v(g+1, z+1, g+k+1).
def bexit_pred(g, z, k):
    x = g + 1
    p = z + 1
    R = x + k
    if p == x:
        # single_token branch z == x
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= p <= x - 1:
        m = q_odd(p)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + p:
            return (R + p) % 2
        return x % 2
    # p >= x + 1
    m = q_odd(x)
    if R <= m:
        return 2 if R % 2 else 0
    return x % 2


def window_ks(z):
    return [k for k in range(1, z) if (k % 2) == (z % 2)]


print('=== X1: T-WC window-congruent pair census z3..16, m1..8, g1..24 ===')
tot = bad = 0
for z in range(3, 17):
    ptot = pbad = 0
    for m in range(1, 9):
        for g in range(1, 25):
            for k in window_ks(z):
                e = val(2 * m + g + k, (m, m + g), z)
                ptot += 1
                if e != zdiag(g, z):
                    pbad += 1
                    if pbad < 6:
                        print(f'  BAD z={z} m={m} g={g} k={k} v={e} pred={zdiag(g, z)}')
    H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'X1 total={tot} bad={bad}')
print()

print('=== X1b: T-WC far stress z in {18,20,22}, m1..4, g1..32 ===')
tot = bad = 0
for z in (18, 20, 22):
    ptot = pbad = 0
    for m in range(1, 5):
        for g in range(1, 33):
            for k in window_ks(z):
                e = val(2 * m + g + k, (m, m + g), z)
                ptot += 1
                if e != zdiag(g, z):
                    pbad += 1
                    if pbad < 6:
                        print(f'  BAD z={z} m={m} g={g} k={k} v={e} pred={zdiag(g, z)}')
    H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'X1b total={tot} bad={bad}')
print()

print('=== X1c: T-WC m-distance stress z in {5,8,11,14}, m1..20, g1..12 ===')
tot = bad = 0
for z in (5, 8, 11, 14):
    ptot = pbad = 0
    for m in range(1, 21):
        for g in range(1, 13):
            for k in window_ks(z):
                e = val(2 * m + g + k, (m, m + g), z)
                ptot += 1
                if e != zdiag(g, z):
                    pbad += 1
                    if pbad < 6:
                        print(f'  BAD z={z} m={m} g={g} k={k} v={e} pred={zdiag(g, z)}')
    H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'X1c total={tot} bad={bad}')
print()

print('=== X2: T-WBC window-congruent bed census z3..16, a1..12 ===')
tot = bad = 0
for z in range(3, 17):
    ptot = pbad = 0
    for a in range(1, 13):
        for k in window_ks(z):
            e = val(2 * a + k, (a, a), z)
            ptot += 1
            if e != 0:
                pbad += 1
                if pbad < 6:
                    print(f'  BAD z={z} a={a} k={k} v={e}')
    H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'X2 total={tot} bad={bad}')
print()

print('=== X2b: T-WBC far stress z in {18,20,22}, a1..8 ===')
tot = bad = 0
for z in (18, 20, 22):
    ptot = pbad = 0
    for a in range(1, 9):
        for k in window_ks(z):
            e = val(2 * a + k, (a, a), z)
            ptot += 1
            if e != 0:
                pbad += 1
                if pbad < 6:
                    print(f'  BAD z={z} a={a} k={k} v={e}')
    H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'X2b total={tot} bad={bad}')
print()

print('=== X3: L-BE B-exit regime table check (closed form vs K1303-transcribed single_token)')
print('    over z3..16, g1..24, all window k ===')
tot = bad = 0
for z in range(3, 17):
    for g in range(1, 25):
        for k in window_ks(z):
            e = eb.single_token(g + 1, z + 1, g + k + 1)
            p = bexit_pred(g, z, k)
            tot += 1
            if e != p:
                bad += 1
                if bad < 8:
                    print(f'  BAD g={g} z={z} k={k} enc={e} pred={p}')
print(f'X3 total={tot} bad={bad}')
print()

print('=== X4: typed packet self-check (children built ONLY from claims +')
print('    published laws, mex must equal claim AND engine) ===')
print('    z3..16, m1..6, g1..24, all window k ===')


def typed_pair_children(m, g, k, z):
    """values of all options of window pair (m, m+g)@(2m+g+k) plane z,
    evaluated ONLY from the packet (claims + published laws)."""
    R = 2 * m + g + k
    out = []
    # A-fall (m>=2): pair (m-1, m+g), g'=g+1, same k -> window claim
    if m >= 2:
        out.append(zdiag(g + 1, z))
    # A-compress (upper token): g>=2 -> pair (m, m+g-1); g==1 -> bed (m,m)
    if g >= 2:
        out.append(zdiag(g - 1, z))
    else:
        out.append(0)  # T-WBC window bed
    # B-exit (m==1): remove the 1 -> single token (g+1)@R-1 plane z+1
    if m == 1:
        out.append(bexit_pred(g, z, k))
    # C (z>=1): pair same, k-1, plane z-1; value 1 XOR child
    if k - 1 >= 1:
        child = zdiag(g, z - 1)          # window congruent row one plane down
    else:
        # k=1 -> band k=0 plane z-1 (K1303 T-GEPSF), delta = g, R' = 2m+g
        Rp = 2 * m + g
        child = cpsfG(z - 1, Rp, g)
    out.append(1 ^ child)
    return out


def typed_bed_children(a, k, z):
    """values of all options of window bed (a,a)@(2a+k) plane z."""
    out = []
    if a >= 2:
        # A: token a -> a-1: pair (a-1, a) with m'=a-1, g'=1, same k -> window
        out.append(zdiag(1, z))
    else:
        # a==1: tokens are 1s: B removes one -> single token (1)@k+1 plane z+1
        out.append(eb.single_token(1, z + 1, k + 1))
    if z >= 1:
        # C: bed at k-1, plane z-1
        if k - 1 >= 1:
            out.append(1 ^ 0)  # window bed claim = 0
        else:
            # k=1 -> bed k=0 plane z-1 (K1303 T-GEBED), j = 0, R' = 2a
            out.append(1 ^ cpsfG(z - 1, 2 * a, 0))
    return out


def mex(vals):
    s = set(vals)
    i = 0
    while i in s:
        i += 1
    return i


tot = bad = bad_eng = 0
for z in range(3, 17):
    ptot = pbad = pbe = 0
    for m in range(1, 7):
        for g in range(1, 25):
            for k in window_ks(z):
                ch = typed_pair_children(m, g, k, z)
                mc = mex(ch)
                if mc != zdiag(g, z):
                    pbad += 1
                    if pbad < 6:
                        print(f'  BADT z={z} m={m} g={g} k={k} mex={mc} claim={zdiag(g, z)} ch={ch}')
                e = val(2 * m + g + k, (m, m + g), z)
                if e != mc:
                    pbe += 1
                    if pbe < 6:
                        print(f'  BADE z={z} m={m} g={g} k={k} eng={e} typed_mex={mc} ch={ch}')
                ptot += 1
    for a in range(1, 13):
        for k in window_ks(z):
            ch = typed_bed_children(a, k, z)
            mc = mex(ch)
            if mc != 0:
                pbad += 1
                if pbad < 6:
                    print(f'  BADT-bed z={z} a={a} k={k} mex={mc} ch={ch}')
            e = val(2 * a + k, (a, a), z)
            if e != mc:
                pbe += 1
                if pbe < 6:
                    print(f'  BADE-bed z={z} a={a} k={k} eng={e} typed={mc} ch={ch}')
            ptot += 1
    H.cache_clear()
    tot += ptot
    bad += pbad
    bad_eng += pbe
    print(f'  z={z}: points={ptot} bad_typed_mex={pbad} bad_typed_vs_engine={pbe}')
print(f'X4 total={tot} bad_typed_mex={bad} bad_typed_vs_engine={bad_eng}')
print()

print('=== X5: cross-engine canonical vs ordered, window samples ===')
tot = bad = 0
for z in (3, 5, 8, 11):
    for m in range(1, 4):
        for g in range(1, 10):
            for k in window_ks(z):
                c = val(2 * m + g + k, (m, m + g), z)
                o = valO(2 * m + g + k, (m, m + g), z)
                tot += 1
                if c != o:
                    bad += 1
    for a in range(1, 5):
        for k in window_ks(z):
            c = val(2 * a + k, (a, a), z)
            o = valO(2 * a + k, (a, a), z)
            tot += 1
            if c != o:
                bad += 1
    H.cache_clear()
    print(f'  z={z}: {tot} bad={bad}')
print(f'X5 total={tot} bad={bad}')
print()

print('=== X6: E4b replication (K1308 box): z3..13, m1..3, g1..12, engine ===')
tot = cnt = 0
for z in range(3, 14):
    for m in range(1, 4):
        for g in range(1, 13):
            for k in window_ks(z):
                e = val(2 * m + g + k, (m, m + g), z)
                tot += 1
                if e != zdiag(g, z):
                    cnt += 1
                    if cnt < 6:
                        print(f'  MISS z={z} k={k} m={m} g={g} v={e} pred={zdiag(g, z)}')
    H.cache_clear()
print(f'X6 total={tot} mismatches={cnt}')
print()

print('=== X7: band-split census for k=1 C-children (informational) ===')
cnt_small = 0
for z in range(3, 17, 2):
    for m in range(1, 9):
        for g in range(1, 25):
            if 2 * m + g < Lw(z - 1):
                cnt_small += 1
print(f'X7 small-band cells (2m+g < L(z-1), k=1 rows, z3..16 odd): {cnt_small}')
print()

print('=== X8: non-congruent window rows census (NO claim, obs only) ===')
print('    z3..12, m1..3, g1..12: distribution of values by (z,k) row ===')
from collections import defaultdict
rows = defaultdict(lambda: defaultdict(int))
for z in range(3, 13):
    for m in range(1, 4):
        for g in range(1, 13):
            for k in range(1, z):
                if (k % 2) == (z % 2):
                    continue
                e = val(2 * m + g + k, (m, m + g), z)
                rows[(z, k)][e] += 1
    H.cache_clear()
for key in sorted(rows):
    print(f'  z={key[0]} k={key[1]}: {dict(rows[key])}')
print('X8 done')
print()
print('ALL STAGES COMPLETE')
