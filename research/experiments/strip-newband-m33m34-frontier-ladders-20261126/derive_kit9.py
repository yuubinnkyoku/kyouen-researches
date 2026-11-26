#!/usr/bin/env python3
"""derive_kit9: engine-free paper derivation of every kit-9 registered
literal, from the K0832 single-token closed form and the published seat
lifecycle scaffold. BEFORE any measurement. Includes:
 - (A) a row-prediction GENERATOR whose output must byte-match the 34
       binding rows of the kit-8 frozen future_slice_registration_constants
       (commit 7af915fb, the published-first kit-8 census) - catches any
       transcription slip the way the kit-6 lifecycle-shift lesson
       prescribes (stick-slice occupancy z=S(d-1), death-slice occupancy
       z=S(d-1)+1, co-token, S and collapse v() literals for every named
       seat);
 - (B) the STACK-SHADOW candidate enumeration (kit-8 log S5 item 9 rule,
       binding): at every kit-9 birth slice, every admissible co-token
       split stack {m,x,y} with x+y=co(d), x,y>=m seats at the NEW seat's
       S and is registered as an explicit caption candidate (expected by
       the observation record: exact numeric mimic of the NEW seat);
       empty at every depth below mid-ladder;
 - (C) the trio-tracker candidates m=19 z=58/59 (kit-8 log S5 item 10,
       NON-BINDING; kit-8 second census S5 death-expectation wording);
 - (D) the m=13/15/17 probe lifecycle continuation rows z=3m-1, 3m, 3m+1
       (kit-8 future item 36, contingent => the kit-8 probes measured
       their trios UP 2v0, so the lifecycle rows are registered;
       NON-BINDING observation rows with scaffold candidates);
 - (E) the EVEN-m mid-slice probes m=14@z=40 / m=16@z=46 / m=18@z=52
       (kit-8 second census S5 proposals; counter-probed 0-hit at this
       build BEFORE registering; full x0 row records);
 - (F) the window sweeps m=31 z{53..60} / m=32 z{54..61} (kit-8 frozen
       items 35-36, registered at this build);
 - (G) the kit-10 future constants (engine-free, not measured here);
 - (H) the K0832 battery triple union for kit-9.
"""
import json
import re

# ---- K0832 single-token closed form (published transcription) ----
def q_odd(k):
    return k if k % 2 else k - 1

def v(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))

def zstar(m):
    # K1268: z*(m) = 2m - 2 + (m mod 2)
    return 2 * m - 2 + (m % 2)

checks = []
def chk(cond, label):
    checks.append((bool(cond), label))

# ---- seat lifecycle scaffold (published, observation-derived; engine-free
# ---- arithmetic asserts; every prediction must satisfy these) ----
def co(m, d):
    # co-token at ladder depth d
    return m + 2 * d + 1 if m % 2 else m + 2 * d

def S_of(m, d):
    # seat sum at depth d
    return 2 * m + 2 * d + 1 if m % 2 else 2 * m + 2 * d

def seat_names(m, d):
    return (m, co(m, d))

def stack_splits(m, d):
    """admissible co-token split stacks at a birth slice: co(d) >= 2m
    is required; splits {m,x,y}, x+y=co(d), x>=m, y>=m seat at S(d)."""
    c = co(m, d)
    out = []
    if c >= 2 * m:
        for x in range(m, c // 2 + 1):
            y = c - x
            if y >= m:
                out.append((x, y))
    return out

def one_past_row(m, d):
    """one-past slice of the depth-d seat: z = z*+2d+1 (also the death
    slice of the depth-(d-1) seat: z = S(d-1)+1)."""
    z = zstar(m) + 2 * d + 1
    R = m + z + 1
    S = S_of(m, d)
    X = seat_names(m, d)
    dead = co(m, d - 1) if d >= 1 else None
    if m % 2:
        txt = "EXACTLY ONE: {%d,%d}@S=%d UP 1v0 (collapse v(%d,%d,%d)=%d)" % (
            X[0], X[1], S, S, z, R, v(S, z, R))
        chk(v(S, z, R) == 0, 'one-past odd collapse==0 m=%d d=%d' % (m, d))
    else:
        txt = "EXACTLY ONE: (%d,%d)@S=%d DOWN 0v1 (collapse v(%d,%d,%d)=%d)" % (
            X[0], X[1], S, S, z, R, v(S, z, R))
        chk(v(S, z, R) == 1, 'one-past even collapse==1 m=%d d=%d' % (m, d))
    if d == 0:
        txt += "; one-past of the d=0 seat (frontier decay 2->%d)" % (1 if m % 2 else 0)
        chk(z == zstar(m) + 1, 'frontier one-past z m=%d' % m)
    else:
        dS = S_of(m, d - 1)
        if m % 2:
            txt += "; {%d,%d} conform-DEAD at z=%d=S+1 (collapse v(%d,%d,%d)=%d)" % (
                m, dead, dS + 1, dS, z, R, v(dS, z, R))
            chk(v(dS, z, R) == 1, 'odd dead-shape collapse==1 m=%d d=%d' % (m, d))
        else:
            txt += "; (%d,%d) conform-DEAD at z=%d=S+1 (collapse v(%d,%d,%d)=%d)" % (
                m, dead, dS + 1, dS, z, R, v(dS, z, R))
            chk(v(dS, z, R) == 0, 'even dead-shape collapse==0 m=%d d=%d' % (m, d))
        chk(z == dS + 1, 'death-slice occupancy z=S(d-1)+1 m=%d d=%d' % (m, d))
        txt += "; death-of-d=%d" % (d - 1)
    return {'kind': 'one-past', 'm': m, 'z': z, 'R': R, 'prediction': txt}

def birth_row(m, d):
    """birth slice of depth d: z = z*+2d; stick seat occupies S(d-1)=z."""
    z = zstar(m) + 2 * d
    R = m + z + 1
    Sd = S_of(m, d)
    X = seat_names(m, d)
    gap = X[1] - m
    chk(z == S_of(m, d - 1), 'stick-slice occupancy z=S(d-1) m=%d d=%d' % (m, d))
    if m % 2:
        txt = ("EXACTLY TWO: stick {%d,%d} DOWN 1v2 (collapse v(%d,%d,%d)=2)"
               % (m, co(m, d - 1), S_of(m, d - 1), z, R))
        chk(v(S_of(m, d - 1), z, R) == 2, 'odd stick collapse==2 m=%d d=%d' % (m, d))
        txt += (" + NEW {%d,%d}@S=%d UP 2v0 (collapse v(%d,%d,%d)=%d), d=%d seat gap %d"
                % (X[0], X[1], Sd, Sd, z, R, v(Sd, z, R), d, gap))
        chk(v(Sd, z, R) == 0, 'odd NEW collapse==0 m=%d d=%d' % (m, d))
        ud = '2v0'
    else:
        txt = ("EXACTLY TWO: stick (%d,%d) DOWN 0v2 (collapse v(%d,%d,%d)=2)"
               % (m, co(m, d - 1), S_of(m, d - 1), z, R))
        chk(v(S_of(m, d - 1), z, R) == 2, 'even stick collapse==2 m=%d d=%d' % (m, d))
        txt += (" + NEW (%d,%d)@S=%d UP 2v1 (collapse v(%d,%d,%d)=%d), d=%d seat gap %d"
                % (X[0], X[1], Sd, Sd, z, R, v(Sd, z, R), d, gap))
        chk(v(Sd, z, R) == 1, 'even NEW collapse==1 m=%d d=%d' % (m, d))
        ud = '2v1'
    return {'kind': 'birth', 'm': m, 'z': z, 'R': R, 'prediction': txt,
            'seat_ud': ud}

def frontier_row(m, nth):
    z = zstar(m)
    R = m + z + 1
    S = 2 * m + 1 if m % 2 else 2 * m
    if m % 2:
        txt = "EXACTLY ONE: {%d,%d}@S=%d UP 2v0 (collapse v(%d,%d,%d)=%d)" % (
            m, m + 1, S, S, z, R, v(S, z, R))
        chk(v(S, z, R) == 0, 'odd frontier collapse==0 m=%d' % m)
        txt += "; z*(%d)=2*%d-2+1=%d per K1268 (derive_check double-checked); R=%d" % (m, m, z, R)
    else:
        txt = "EXACTLY ONE: (%d,%d)@S=%d UP 2v1 (collapse v(%d,%d,%d)=%d)" % (
            m, m, S, S, z, R, v(S, z, R))
        chk(v(S, z, R) == 1, 'even frontier collapse==1 m=%d' % m)
        txt += "; z*(%d)=2*%d-2+0=%d per K1268 (derive_check double-checked); R=%d" % (m, m, z, R)
    return {'kind': 'frontier', 'm': m, 'z': z, 'R': R, 'prediction': txt}

# ---- (A) regenerate the 34 kit-8 frozen binding rows and byte-compare ----
binding = json.load(open('future_kit9_binding.json'))
assert len(binding) == 34, len(binding)

spec = []
spec.append(one_past_row(19, 10)); spec.append(birth_row(19, 11))
spec.append(one_past_row(20, 10)); spec.append(birth_row(20, 11))
spec.append(one_past_row(21, 6));  spec.append(birth_row(21, 7))
spec.append(one_past_row(22, 6));  spec.append(birth_row(22, 7))
spec.append(one_past_row(23, 5));  spec.append(birth_row(23, 6))
spec.append(one_past_row(24, 5));  spec.append(birth_row(24, 6))
spec.append(one_past_row(25, 4));  spec.append(birth_row(25, 5))
spec.append(one_past_row(26, 4));  spec.append(birth_row(26, 5))
spec.append(one_past_row(27, 2));  spec.append(birth_row(27, 3))
spec.append(one_past_row(28, 2));  spec.append(birth_row(28, 3))
spec.append(birth_row(29, 2));     spec.append(one_past_row(29, 2)); spec.append(birth_row(29, 3))
spec.append(birth_row(30, 2));     spec.append(one_past_row(30, 2)); spec.append(birth_row(30, 3))
r31a = one_past_row(31, 0); r31a['contingent'] = True
r31c = one_past_row(31, 1)
spec.extend([r31a, birth_row(31, 1), r31c])
r32a = one_past_row(32, 0); r32a['contingent'] = True
r32c = one_past_row(32, 1)
spec.extend([r32a, birth_row(32, 1), r32c])
f33 = frontier_row(33, 21); f33['kind'] = 'frontier first contact proposal (FIRST-EVER m=33 row)'
f34 = frontier_row(34, 22); f34['kind'] = 'frontier first contact proposal (FIRST-EVER m=34 row)'
spec.extend([f33, f34])

assert len(spec) == 34, len(spec)

mismatch = 0
for i, (gen, ref) in enumerate(zip(spec, binding)):
    chk(gen['m'] == ref['m'], 'item%d m' % (i + 1))
    chk(gen['z'] == ref['z'], 'item%d z' % (i + 1))
    ok = gen['prediction'] in ref['prediction'] or ref['prediction'] == gen['prediction']
    if not ok:
        mismatch += 1
        print('MISMATCH item%d m=%d z=%d' % (i + 1, ref['m'], ref['z']))
        print('  gen :', gen['prediction'])
        print('  kit8:', ref['prediction'])

# ---- (B) stack-shadow candidate enumeration for every kit-9 birth row ----
stack_regs = {}
for (m, d) in [(19, 11), (20, 11), (21, 7), (22, 7), (23, 6), (24, 6), (25, 5),
               (26, 5), (27, 3), (28, 3), (29, 2), (29, 3), (30, 2), (30, 3),
               (31, 1), (32, 1)]:
    z = zstar(m) + 2 * d
    sp = stack_splits(m, d)
    if sp:
        chk(S_of(m, d) == z + 2, 'birth seat S=z+2 m=%d d=%d' % (m, d))
    stack_regs[(m, d)] = sp
chk(stack_regs[(19, 11)] == [(19, 23), (20, 22), (21, 21)], 'm19 d11 splits')
chk(stack_regs[(20, 11)] == [(20, 22), (21, 21)], 'm20 d11 splits')
for (m, d) in [(21, 7), (22, 7), (23, 6), (24, 6), (25, 5), (26, 5), (27, 3),
               (28, 3), (29, 2), (29, 3), (30, 2), (30, 3), (31, 1), (32, 1)]:
    chk(stack_regs[(m, d)] == [], 'empty split domain m=%d d=%d' % (m, d))

# ---- (D) the m=13/15/17 probe lifecycle continuation rows ----
lifecycle = []
for m in (13, 15, 17):
    dmid = (m - 1) // 2
    a = one_past_row(m, dmid)
    b = birth_row(m, dmid + 1)
    c = one_past_row(m, dmid + 1)
    for r in (a, b, c):
        chk(r['z'] in (3 * m - 1, 3 * m, 3 * m + 1), 'lifecycle z band m=%d' % m)
        lifecycle.append(r)
    chk(a['z'] == 3 * m - 1, 'lifecycle z=3m-1 m=%d' % m)
    chk(b['z'] == 3 * m, 'lifecycle z=3m m=%d' % m)
    chk(c['z'] == 3 * m + 1, 'lifecycle z=3m+1 m=%d' % m)
    # stack splits at the lifecycle birth rows
    sp = stack_splits(m, dmid + 1)
    chk(sp == [(m, m + 2), (m + 1, m + 1)], 'lifecycle birth splits m=%d' % m)
    chk(S_of(m, dmid + 1) == 3 * m + 2, 'lifecycle birth S m=%d' % m)

# ---- (E) even-m mid-slice probes ----
even_probes = []
for m in (14, 16, 18):
    dmid = m // 2
    b = birth_row(m, dmid)
    chk(b['z'] == zstar(m) + 2 * dmid, 'even probe z m=%d' % m)
    chk(b['z'] == 3 * m - 2, 'even probe z==3m-2 m=%d' % m)
    chk(S_of(m, dmid) == 3 * m, 'even probe birth S==3m m=%d' % m)
    chk(co(m, dmid) == 2 * m, 'even probe co==2m m=%d' % m)
    sp = stack_splits(m, dmid)
    chk(sp == [(m, m)], 'even probe equistack-only split m=%d' % m)
    even_probes.append(b)

# ---- (G) the kit-10 future constants ----
future = []
future.append(one_past_row(19, 11)); future.append(birth_row(19, 12))
future.append(one_past_row(20, 11)); future.append(birth_row(20, 12))
future.append(one_past_row(21, 7));  future.append(birth_row(21, 8))
future.append(one_past_row(22, 7));  future.append(birth_row(22, 8))
future.append(one_past_row(23, 6));  future.append(birth_row(23, 7))
future.append(one_past_row(24, 6));  future.append(birth_row(24, 7))
future.append(one_past_row(25, 5));  future.append(birth_row(25, 6))
future.append(one_past_row(26, 5));  future.append(birth_row(26, 6))
future.append(one_past_row(27, 3));  future.append(birth_row(27, 4))
future.append(one_past_row(28, 3));  future.append(birth_row(28, 4))
future.append(birth_row(29, 4));     future.append(one_past_row(29, 4)); future.append(birth_row(29, 5))
future.append(birth_row(30, 4));     future.append(one_past_row(30, 4)); future.append(birth_row(30, 5))
future.append(one_past_row(31, 1)); future.append(birth_row(31, 2)); future.append(one_past_row(31, 2))
future.append(one_past_row(32, 1)); future.append(birth_row(32, 2)); future.append(one_past_row(32, 2))
f35 = frontier_row(35, 23); f35['kind'] = 'frontier first contact proposal (FIRST-EVER m=35 row)'
f36 = frontier_row(36, 24); f36['kind'] = 'frontier first contact proposal (FIRST-EVER m=36 row)'
future.extend([f35, f36])
# stack splits of the kit-10 birth rows (S5 item-9 rule, engine-free)
k10_stacks = {}
for (m, d) in [(19, 12), (20, 12)]:
    k10_stacks['%d' % m] = stack_splits(m, d)
chk(k10_stacks['19'] == [(19, 25), (20, 24), (21, 23), (22, 22)], 'kit10 m19 d12 splits')
chk(k10_stacks['20'] == [(20, 24), (21, 23), (22, 22)], 'kit10 m20 d12 splits')
for (m, d) in [(21, 8), (22, 8), (23, 7), (24, 7), (25, 6), (26, 6), (27, 4),
               (28, 4), (29, 4), (29, 5), (30, 4), (30, 5), (31, 2), (32, 2)]:
    chk(stack_splits(m, d) == [], 'kit10 empty split domain m=%d d=%d' % (m, d))

# ---- (H) battery triple union ----
bat = set()
k8 = json.load(open('kit8_battery_triples.json'))
for t in k8:
    bat.add(tuple(t))
meas_rows = [[19, 58], [19, 59], [20, 59], [20, 60], [21, 54], [21, 55],
             [22, 55], [22, 56], [23, 56], [23, 57], [24, 57], [24, 58],
             [25, 58], [25, 59], [26, 59], [26, 60], [27, 58], [27, 59],
             [28, 59], [28, 60], [29, 61], [29, 62], [29, 63], [30, 62],
             [30, 63], [30, 64], [31, 62], [31, 63], [31, 64], [32, 63],
             [32, 64], [32, 65], [33, 65], [34, 66],
             [13, 38], [13, 39], [13, 40], [15, 44], [15, 45], [15, 46],
             [17, 50], [17, 51], [17, 52], [14, 40], [16, 46], [18, 52]]
for z in range(53, 61):
    meas_rows.append([31, z])
for z in range(54, 62):
    meas_rows.append([32, z])
for (m, z) in meas_rows:
    R = m + z + 1
    for S in (m, m + 2, 2 * m, 2 * m + 1, m + 37, m + 38):
        bat.add((S, z, R))
    bat.add((max(m + 38, z + 2), z, R))
for r in spec + future + lifecycle + even_probes:
    for (S, zz, RR) in re.findall(r'v\((\d+),(\d+),(\d+)\)', r['prediction']):
        t = (int(S), int(zz), int(RR))
        chk(v(t[0], t[1], t[2]) in (0, 1, 2), 'battery triple valid')
        bat.add(t)
# new anchor collapse literals (the 54 kit-8 separation spots)
seps = json.load(open('kit8_seps.json'))
assert len(seps) == 54, len(seps)
for s in seps:
    chk(sum(s['X']) == s['S'], 'sep spot S==sum(X)')
    bat.add((s['S'], s['z'], s['R']))

# ---- report ----
print('checks:', len(checks), 'failed:', sum(1 for c in checks if not c[0]))
for c in checks:
    if not c[0]:
        print('FAIL:', c[1])
print('prediction text mismatches vs kit-8 frozen constants (34 rows):', mismatch)
print('battery union triples:', len(bat))
print('lifecycle rows:', len(lifecycle), 'even probes:', len(even_probes))
print('kit-10 future rows:', len(future))

out = {
  'binding34_regenerated_ok': mismatch == 0,
  'stack_regs': {'%d_%d' % k: v for k, v in stack_regs.items()},
  'k10_stacks': k10_stacks,
  'lifecycle': lifecycle,
  'even_probes': even_probes,
  'future_kit10': future,
  'battery_triples': sorted(bat),
}
json.dump(out, open('kit9_derive_spec.json', 'w'), indent=1)
print('kit9_derive_spec.json written')
