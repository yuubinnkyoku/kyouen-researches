#!/usr/bin/env python3
"""explore_upper: PRE-DECLARATION exploration for the upper-half collapse
package (pairs k >= z diagonal-and-above, beds k >= z, single-token tail
readings, C-SUM census, transition-window refutation census).

Deterministic output only (frozen .out published in the kit).
Engine: engine_block.py (published chain sha 582c93c1...), embedded verbatim
in verify_k1308.py behind the startup sha gate.
"""
import engine_block as eb
from functools import lru_cache

H = eb.H_canonical
HO = eb.H_ordered


def val(R, X, z):
    return H(R, tuple(sorted(X, reverse=True)), z)


def valO(R, X, z):
    return HO(R, tuple(X), z)


def IND(b):
    return 1 if b else 0


# ---- the three new claims of the package ---------------------------------
def tail(g):
    """T-UH: pair (m, m+g) at k >= z+1 -> [g odd]."""
    return IND(g % 2 == 1)


def bed0(k, z):
    """T-DU': bed {a,a} at k >= z -> 0."""
    assert k >= z
    return 0


def zdiag(g, z):
    """Z-DIAG: pair (m, m+g) at k = z."""
    if g <= z:
        return IND(g % 2 == 1)
    if g == z + 1:
        return 2
    return IND(g % 2 == 0)


def vform(x, z, R):
    return eb.single_token(x, z, R)


print('=== E1: T-UH pair-tail census z0..8, m1..8, g1..10, k=z+1..z+5 ===')
tot = bad = 0
for z in range(0, 9):
    ptot = pbad = 0
    for m in range(1, 9):
        for g in range(1, 11):
            for k in range(z + 1, z + 6):
                e = val(2 * m + g + k, (m, m + g), z)
                ptot += 1
                if e != tail(g):
                    pbad += 1
                    if pbad < 6:
                        print(f'  BAD z={z} m={m} g={g} k={k} v={e} pred={tail(g)}')
        H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'E1 total={tot} bad={bad}')
print()

print('=== E1b: T-UH far stress z in {10,12,14,16,18,20}, m1..12, g1..12, k=z+1..z+3 ===')
tot = bad = 0
for z in (10, 12, 14, 16, 18, 20):
    ptot = pbad = 0
    for m in range(1, 13):
        for g in range(1, 13):
            for k in range(z + 1, z + 4):
                e = val(2 * m + g + k, (m, m + g), z)
                ptot += 1
                if e != tail(g):
                    pbad += 1
                    if pbad < 6:
                        print(f'  BAD z={z} m={m} g={g} k={k} v={e} pred={tail(g)}')
        H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'E1b total={tot} bad={bad}')
print()

print('=== E2: T-DU-prime bed census z0..8, a1..10, k=z..z+6 ===')
tot = bad = 0
for z in range(0, 9):
    for a in range(1, 11):
        for k in range(z, z + 7):
            e = val(2 * a + k, (a, a), z)
            tot += 1
            if e != 0:
                bad += 1
                if bad < 6:
                    print(f'  BAD z={z} a={a} k={k} v={e}')
        H.cache_clear()
print(f'E2 total={tot} bad={bad}')
print()

print('=== E2b: T-DU-prime far stress z in {10,14,18}, a1..14, k=z..z+4 ===')
tot = bad = 0
for z in (10, 14, 18):
    for a in range(1, 15):
        for k in range(z, z + 5):
            e = val(2 * a + k, (a, a), z)
            tot += 1
            if e != 0:
                bad += 1
                if bad < 6:
                    print(f'  BAD z={z} a={a} k={k} v={e}')
        H.cache_clear()
print(f'E2b total={tot} bad={bad}')
print()

print('=== E3: Z-DIAG census z0..8, m1..8, g1..16 ===')
tot = bad = 0
for z in range(0, 9):
    ptot = pbad = 0
    for m in range(1, 9):
        for g in range(1, 17):
            e = val(2 * m + g + z, (m, m + g), z)
            ptot += 1
            if e != zdiag(g, z):
                pbad += 1
                if pbad < 6:
                    print(f'  BAD z={z} m={m} g={g} v={e} pred={zdiag(g, z)}')
        H.cache_clear()
    tot += ptot
    bad += pbad
    print(f'  z={z}: points={ptot} bad={pbad}')
print(f'E3 total={tot} bad={bad}')
print()

print('=== E3b: Z-DIAG far stress z in {10,12,14}, m1..5, g1..30 ===')
tot = bad = 0
for z in (10, 12, 14):
    for m in range(1, 6):
        for g in range(1, 31):
            e = val(2 * m + g + z, (m, m + g), z)
            tot += 1
            if e != zdiag(g, z):
                bad += 1
                if bad < 6:
                    print(f'  BAD z={z} m={m} g={g} v={e} pred={zdiag(g, z)}')
        H.cache_clear()
print(f'E3b total={tot} bad={bad}')
print()

print('=== E4: transition-window (1<=k<=z-1) alternation REFUTATION census ===')
print('    refuted conjecture: rows k not congruent z (mod 2) in the window')
print('    have the tail value [g odd].  z3..8, m1..3, g1..12, k=1..z-1.')
tot = cnt = 0
counters = []
for z in range(3, 9):
    for m in range(1, 4):
        for g in range(1, 13):
            for k in range(1, z):
                if (k % 2) == (z % 2):
                    continue
                e = val(2 * m + g + k, (m, m + g), z)
                tot += 1
                if e != tail(g):
                    cnt += 1
                    counters.append((z, k, m, g, e, tail(g)))
        H.cache_clear()
print(f'    window-k-noncongruent rows = {tot}, mismatches vs [g odd] = {cnt}')
for c in counters:
    print('    COUNTER z=%d k=%d m=%d g=%d v=%d pred=%d' % c)
print()

print('=== E4b: transition-window rows k congruent z (mod 2): Z-DIAG hold check ===')
print('    (observation only: do rows k=z-2, z-4, ... agree with ZDIAG(g,z)?)')
tot = cnt = 0
countersB = []
for z in range(3, 14):
    for m in range(1, 4):
        for g in range(1, 13):
            for k in range(1, z):
                if (k % 2) != (z % 2):
                    continue
                e = val(2 * m + g + k, (m, m + g), z)
                tot += 1
                if e != zdiag(g, z):
                    cnt += 1
                    if len(countersB) < 6:
                        countersB.append((z, k, m, g, e, zdiag(g, z)))
        H.cache_clear()
print(f'    congruent rows = {tot}, mismatches vs ZDIAG = {cnt}')
for c in countersB:
    print('    COUNTER-B z=%d k=%d m=%d g=%d v=%d pred=%d' % c)
print()

print('=== E5: L-SB closed-form reading v(x,p,x+j) = x%2, j>=p, both engines ===')
print('    x1..20, p1..14, j=p..p+8')
tot = bad = 0
for x in range(1, 21):
    for p in range(1, 15):
        for j in range(p, p + 9):
            R = x + j
            a = vform(x, p, R)
            b = val(R, (x,), p)
            c = valO(R, (x,), p)
            tot += 1
            if not (a == b == c == x % 2):
                bad += 1
                if bad < 8:
                    print(f'  BAD x={x} p={p} j={j} form={a} can={b} ord={c} want={x%2}')
    H.cache_clear(); HO.cache_clear()
print(f'E5 total={tot} bad={bad}')
print()

print('=== E5b: B-exit special readings (both engines, x<=22) ===')
tot = bad = 0
for z in range(0, 11):
    a1 = vform(z + 2, z + 1, 2 * z + 2)
    a2 = val(2 * z + 2, (z + 2,), z + 1)
    a3 = valO(2 * z + 2, (z + 2,), z + 1)
    tot += 1
    if not (a1 == a2 == a3 == (z + 1) % 2):
        bad += 1
        print(f'  BAD-S1 z={z}: {a1} {a2} {a3} want={(z+1)%2}')
for z in range(0, 11):
    a1 = vform(z + 1, z + 1, 2 * z + 1)
    a2 = val(2 * z + 1, (z + 1,), z + 1)
    a3 = valO(2 * z + 1, (z + 1,), z + 1)
    tot += 1
    if not (a1 == a2 == a3 == 2):
        bad += 1
        print(f'  BAD-S2 z={z}: {a1} {a2} {a3} want=2')
for p in range(0, 9):
    for R in range(2, 11):
        a1 = vform(1, p, R)
        a2 = val(R, (1,), p)
        a3 = valO(R, (1,), p)
        tot += 1
        if not (a1 == a2 == a3 == 1):
            bad += 1
            print(f'  BAD-S3 p={p} R={R}: {a1} {a2} {a3} want=1')
    H.cache_clear(); HO.cache_clear()
print(f'E5b total={tot} bad={bad}')
print()

print('=== E6: C-SUM census (CONJECTURE, no universal claim): tail = [S odd] ===')
print('    single-copy triples a<b<c<=8, z0..5, k=z+2..z+5')
tot = bad = 0
for a in range(1, 9):
    for b in range(a + 1, 9):
        for c in range(b + 1, 9):
            S = a + b + c
            for z in range(0, 6):
                ptot = pbad = 0
                for k in range(z + 2, z + 6):
                    e = val(S + k, (a, b, c), z)
                    ptot += 1
                    if e != S % 2:
                        pbad += 1
                        if pbad < 4:
                            print(f'  TRIPLE BAD {a},{b},{c} z={z} k={k} v={e} S%2={S%2}')
                H.cache_clear()
                tot += ptot
                bad += pbad
print(f'    triples total={tot} bad={bad}')
print('    mixed triples {a,a,b}/{a,b,b} a<b<=7, z0..4, k=z+2..z+5')
fams = []
for a in range(1, 8):
    for b in range(a + 1, 8):
        fams.append((a, a, b))
        fams.append((a, b, b))
tot = bad = 0
for (x, y, w) in fams:
    S = x + y + w
    for z in range(0, 5):
        for k in range(z + 2, z + 6):
            e = val(S + k, (x, y, w), z)
            tot += 1
            if e != S % 2:
                bad += 1
                if bad < 8:
                    print(f'  MIXED BAD {x},{y},{w} z={z} k={k} v={e} pred={S%2}')
        H.cache_clear()
print(f'    mixed total={tot} bad={bad}')
print('    quads a<b<c<d<=6, z0..2, k=z+3..z+6')
tot = bad = 0
for a in range(1, 7):
    for b in range(a + 1, 7):
        for c in range(b + 1, 7):
            for d in range(c + 1, 7):
                S = a + b + c + d
                for z in range(0, 3):
                    for k in range(z + 3, z + 7):
                        e = val(S + k, (a, b, c, d), z)
                        tot += 1
                        if e != S % 2:
                            bad += 1
                            if bad < 8:
                                print(f'  QUAD BAD {a},{b},{c},{d} z={z} k={k} v={e} pred={S%2}')
                    H.cache_clear()
print(f'    quads total={tot} bad={bad}')
print()

print('=== E6b: mixed-triple EARLIER-tail probe (threshold check, obs only) ===')
print('    {a,a,b} at k=z+1: does [S odd] already hold? (bad counted as obs)')
for (x, y, w) in [(1, 1, 2), (1, 1, 3), (2, 2, 3), (1, 2, 2), (1, 3, 3), (2, 3, 3)]:
    S = x + y + w
    row = []
    for z in range(0, 5):
        for k in [z, z + 1]:
            row.append((z, k, val(S + k, (x, y, w), z)))
        H.cache_clear()
    print(f'  {{{x},{y},{w}}} (z,k,v): {row}')
print()

print('=== E7: cross-engine canonical vs ordered, tail/diag/bed samples ===')
tot = bad = 0
for z in (0, 3, 7, 12):
    for m in range(1, 7):
        for g in range(1, 10):
            for k in range(z + 1, z + 4):
                R = 2 * m + g + k
                hc = val(R, (m, m + g), z)
                ho = valO(R, (m, m + g), z)
                tot += 1
                if hc != ho:
                    bad += 1
                    print(f'  BAD-PAIR z={z} m={m} g={g} k={k} can={hc} ord={ho}')
        H.cache_clear(); HO.cache_clear()
for z in (0, 5, 11):
    for a in range(1, 9):
        for k in range(z, z + 3):
            R = 2 * a + k
            hc = val(R, (a, a), z)
            ho = valO(R, (a, a), z)
            tot += 1
            if hc != ho:
                bad += 1
                print(f'  BAD-BED z={z} a={a} k={k} can={hc} ord={ho}')
    H.cache_clear(); HO.cache_clear()
print(f'E7 total={tot} bad={bad}')
print()

print('=== E8: sharpness records (obs only) ===')
print('    bed {a,a} at k=z-1 (one below the T-DU-prime threshold):')
for z in range(1, 7):
    row = []
    for a in range(1, 5):
        row.append(val(2 * a + z - 1, (a, a), z))
        H.cache_clear()
    print(f'  z={z} a=1..4 k=z-1: {row}')
print('    pair diag vs tail mismatch witnesses (k=z value vs [g odd]):')
for z in range(0, 6):
    g0 = z + 1
    w = val(2 + g0 + z, (1, 1 + g0), z)
    H.cache_clear()
    print(f'  z={z} g={g0} k=z diag value = {w} (tail pred would be {tail(g0)})')
print()

print('=== E9: plane 0/1/2 full closure above the band: k=1..6, m1..3, g1..12 ===')
print('    claims: k=z Z-DIAG / k>=z+1 T-UH / z2-k1 [g odd] (K1286 C4)')
tot = bad = 0
for z in (0, 1, 2):
    for m in range(1, 4):
        for g in range(1, 13):
            for k in range(1, 7):
                e = val(2 * m + g + k, (m, m + g), z)
                if z == 2 and k == 1:
                    pred = tail(g)
                elif k == z:
                    pred = zdiag(g, z)
                elif k >= z + 1:
                    pred = tail(g)
                else:
                    continue
                tot += 1
                if e != pred:
                    bad += 1
                    if bad < 8:
                        print(f'  BAD z={z} m={m} g={g} k={k} v={e} pred={pred}')
        H.cache_clear()
print(f'E9 total={tot} bad={bad}')
print()
print('explore_upper done.')
