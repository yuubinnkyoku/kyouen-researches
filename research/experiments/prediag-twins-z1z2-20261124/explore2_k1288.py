#!/usr/bin/env python3
"""quick z3/z4 pre-diag band census (observation only, for open registration)
+ claim-check of the z1/z2 band laws on a wide box."""
from engine_block import H_canonical as H, H_ordered as HO


def IND(b):
    return 1 if b else 0


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


def claim_z1(m, g, k):
    R = 2 * m + g + k
    if R < 0:
        return None
    if R == 0:
        return 0
    if R == 1:
        return 2
    return g1(R - 2 * m)


def claim_z2(m, g, k):
    R = 2 * m + g + k
    if R < 0:
        return None
    if R == 1:
        return 2
    return f0(R - 2 * m - 2)


def bed_claim_z1(m, j):
    R = 2 * m + j
    if R < 0:
        return None
    if R == 0:
        return 0
    if R == 1:
        return 2
    return g1(j)


def bed_claim_z2(m, j):
    R = 2 * m + j
    if R < 0:
        return None
    if R == 1:
        return 2
    return f0(j - 2)


# --- wide-box claim checks (canonical engine) ---
n = bad = 0
badex = []
for m in range(1, 21):
    for g in range(1, 45):
        for k in range(-2 * m - g, 1):
            v = claim_z1(m, g, k)
            if v is None:
                continue
            e = H(2 * m + g + k, (m, m + g), 1)
            n += 1
            if v != e:
                bad += 1
                if len(badex) < 6:
                    badex.append(('z1s', m, g, k, v, e))
print("z1 slices wide box: cells=%d bad=%d %s" % (n, bad, badex))

n = bad = 0
badex = []
for m in range(1, 21):
    for g in range(1, 45):
        for k in range(-2 * m - g, 1):
            v = claim_z2(m, g, k)
            if v is None:
                continue
            e = H(2 * m + g + k, (m, m + g), 2)
            n += 1
            if v != e:
                bad += 1
                if len(badex) < 6:
                    badex.append(('z2s', m, g, k, v, e))
print("z2 slices wide box: cells=%d bad=%d %s" % (n, bad, badex))

n = bad = 0
badex = []
for z, cf in [(1, bed_claim_z1), (2, bed_claim_z2)]:
    for m in range(1, 26):
        for j in range(-52, 1):
            v = cf(m, j)
            if v is None:
                continue
            e = H(2 * m + j, (m, m), z)
            n += 1
            if v != e:
                bad += 1
                if len(badex) < 6:
                    badex.append(('bed%d' % z, m, j, v, e))
print("beds wide box: cells=%d bad=%d %s" % (n, bad, badex))

# ordered engine cross-check on a subsample
n = bad = 0
for m in range(1, 9):
    for g in range(1, 20):
        for k in range(-2 * m - g, 1):
            for z, cf in [(1, claim_z1), (2, claim_z2)]:
                v = cf(m, g, k)
                if v is None:
                    continue
                e = HO(2 * m + g + k, (m, m + g), z)
                n += 1
                if v != e:
                    bad += 1
print("ordered-engine cross: cells=%d bad=%d" % (n, bad))

# --- z3/z4 pre-diag far-row census (observation) ---
print()
print("z3 slices, representative row m=12, k in [-12..-1], g 1..18:")
for z in (3, 4):
    for k in range(-12, 0):
        vals = []
        for g in range(1, 19):
            R = 24 + g + k
            vals.append('.' if R < 0 else H(R, (12, 12 + g), z))
        print("z%d k=%d %s" % (z, k, vals))
print()
# delta-collapse question for z3/z4: check value depends only on R-2m for far region
print("z3 delta-collapse check (k<=0, R>=2, m 3..12, g<=25):")
bad = tot = 0
ex = []
for m in range(3, 13):
    for g in range(1, 26):
        for k in range(-2 * m - g, 1):
            R = 2 * m + g + k
            if R < 2:
                continue
            tot += 1
            key = (z, R - 2 * m)
print("  cells=%d (test below)" % tot)
# collect value by delta across (m,g,k)
from collections import defaultdict
by_d = defaultdict(set)
for m in range(3, 13):
    for g in range(1, 26):
        for k in range(-2 * m - g, 1):
            R = 2 * m + g + k
            if R < 2:
                continue
            by_d[R - 2 * m].add(H(R, (m, m + g), 3))
splits = {d: sorted(v) for d, v in by_d.items() if len(v) > 1}
print("  z3 delta-split deltas (R>=2 region): %s" % splits if splits else "  z3 delta-collapse: UNIQUE per delta, R>=2 region, m 3..12 g<=25")
tab = ' '.join(str(sorted(by_d.get(d, []))[0] if len(by_d.get(d, [])) == 1 else -1) for d in range(-30, 20))
print("  z3 value-by-delta map d=-30..19 (-1 = split/absent): %s" % tab)
by_d4 = defaultdict(set)
for m in range(3, 13):
    for g in range(1, 26):
        for k in range(-2 * m - g, 1):
            R = 2 * m + g + k
            if R < 2:
                continue
            by_d4[R - 2 * m].add(H(R, (m, m + g), 4))
splits4 = {d: sorted(v) for d, v in by_d4.items() if len(v) > 1}
if splits4:
    print("  z4 delta-split deltas: %s" % splits4)
else:
    tab4 = ' '.join(str(sorted(by_d4.get(d, []))[0] if len(by_d4.get(d, [])) == 1 else -1) for d in range(-30, 20))
    print("  z4 delta-collapse UNIQUE; value-by-delta d=-30..19 (-1 = absent): %s" % tab4)
# refinement: R>=4 restriction to isolate small-R exception layer (z3: R=2,3 / z4: R<=3?)
for zz in (3, 4):
    tabr = defaultdict(set)
    n_r4 = 0
    for m in range(3, 13):
        for g in range(1, 26):
            for k in range(-2 * m - g, 1):
                R = 2 * m + g + k
                if R < 4:
                    continue
                n_r4 += 1
                tabr[R - 2 * m].add(H(R, (m, m + g), zz))
    sr = {d: sorted(v) for d, v in tabr.items() if len(v) > 1}
    print("  z%d delta-split with R>=4 only (cells=%d): %s" % (zz, n_r4, sr) if sr else "  z%d delta-collapse UNIQUE for R>=4 (cells=%d), m 3..12 g<=25" % (zz, n_r4))
    tabR2 = defaultdict(set)
    n_r6 = 0
    for m in range(3, 13):
        for g in range(1, 26):
            for k in range(-2 * m - g, 1):
                R = 2 * m + g + k
                if R < 6:
                    continue
                n_r6 += 1
                tabR2[R - 2 * m].add(H(R, (m, m + g), zz))
    sr2 = {d: sorted(v) for d, v in tabR2.items() if len(v) > 1}
    print("  z%d delta-split with R>=6 only (cells=%d): %s" % (zz, n_r6, sr2) if sr2 else "  z%d delta-collapse UNIQUE for R>=6 (cells=%d), m 3..12 g<=25" % (zz, n_r6))
print("done")

# LAW check (OBS): does z3 == g1(d-2) / z4 == f0(d-4) hold for ALL R>=4 in the box?
for zz, fn in ((3, lambda d: g1(d - 2)), (4, lambda d: f0(d - 4))):
    bad3 = tot3 = 0
    ex9 = []
    for m in range(3, 13):
        for g in range(1, 26):
            for k in range(-2 * m - g, 1):
                R = 2 * m + g + k
                if R < 4:
                    continue
                tot3 += 1
                e = fn(R - 2 * m)
                h = H(R, (m, m + g), zz)
                if h != e:
                    bad3 += 1
                    if len(ex9) < 6:
                        ex9.append((m, g, k, h, e))
    print("z%d law g1/f0 shift check (R>=4, m 3..12, g<=25, k<=0): cells=%d bad=%d %s" % (zz, tot3, bad3, ex9[:6] if bad3 else "ALL MATCH"))
print("done2")
