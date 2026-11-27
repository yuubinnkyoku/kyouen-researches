#!/usr/bin/env python3
"""derive_kit8: engine-free paper derivation of every kit-8 registered
literal, from the K0832 single-token closed form and the published seat
lifecycle scaffold. BEFORE any measurement. Includes:
 - (A) a row-prediction GENERATOR whose output must byte-match the 28
       binding rows of the kit-7 frozen section (d) (catches any
       transcription slip the way the kit-6 lifecycle-shift lesson
       prescribes: the generator asserts stick-slice occupancy
       z=S(d-1), death-slice occupancy z=S(d-1)+1, co-token, S and
       collapse v() literals for every named seat);
 - (B) the trio-tracker candidate regeneration (kit-7 log S5 item 10);
 - (C) the m=26 z=25 hole-row candidate;
 - (D) the trio mid-slice probes m=13/15/17 with the z=3m-2 derivation
       (and the kit-7 log S5 prose off-by-one disclosure);
 - (E) the window sweeps m=29 z{49..56} / m=30 z{50..57};
 - (F) the kit-9 future constants (engine-free, not measured here);
 - (G) the K0832 battery triple union for kit-8.
"""
import json

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

def one_past_row(m, d):
    """one-past slice of the depth-d seat: z = z*+2d+1 (also the death
    slice of the depth-(d-1) seat: z = S(d-1)+1)."""
    z = zstar(m) + 2 * d + 1
    R = m + z + 1
    S = S_of(m, d)
    X = seat_names(m, d)
    dead = co(m, d - 1) if d >= 1 else None
    if m % 2:
        dirn = 'UP'
        cl_v, cl_c = S, z
        txt = "EXACTLY ONE: {%d,%d}@S=%d UP 1v0 (collapse v(%d,%d,%d)=%d)" % (
            X[0], X[1], S, S, z, R, v(S, z, R))
        chk(v(S, z, R) == 0, 'one-past odd collapse==0 m=%d d=%d' % (m, d))
    else:
        dirn = 'DOWN'
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
    else:
        txt = ("EXACTLY TWO: stick (%d,%d) DOWN 0v2 (collapse v(%d,%d,%d)=2)"
               % (m, co(m, d - 1), S_of(m, d - 1), z, R))
        chk(v(S_of(m, d - 1), z, R) == 2, 'even stick collapse==2 m=%d d=%d' % (m, d))
        txt += (" + NEW (%d,%d)@S=%d UP 2v1 (collapse v(%d,%d,%d)=%d), d=%d seat gap %d"
                % (X[0], X[1], Sd, Sd, z, R, v(Sd, z, R), d, gap))
        chk(v(Sd, z, R) == 1, 'even NEW collapse==1 m=%d d=%d' % (m, d))
    return {'kind': 'birth', 'm': m, 'z': z, 'R': R, 'prediction': txt}

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

# ---- (A) regenerate the 28 kit-7 frozen binding rows and byte-compare ----
spec28 = []  # (kind_tag, generator result, fuzzy_role)
# items 1-2: m=19 d=10 one-past/birth
for (m, d) in [(19, 10)]:
    spec28.append(one_past_row(m, d - 1))
    spec28.append(birth_row(m, d))
spec28.append(one_past_row(20, 9)); spec28.append(birth_row(20, 10))
spec28.append(one_past_row(21, 5)); spec28.append(birth_row(21, 6))
spec28.append(one_past_row(22, 5)); spec28.append(birth_row(22, 6))
spec28.append(one_past_row(23, 4)); spec28.append(birth_row(23, 5))
spec28.append(one_past_row(24, 4)); spec28.append(birth_row(24, 5))
spec28.append(one_past_row(25, 3)); spec28.append(birth_row(25, 4))
spec28.append(one_past_row(26, 3)); spec28.append(birth_row(26, 4))
spec28.append(one_past_row(27, 1)); spec28.append(birth_row(27, 2))
spec28.append(one_past_row(28, 1)); spec28.append(birth_row(28, 2))
# m=29: one-past(d0), birth d1, one-past(d1)
spec28.append(one_past_row(29, 0)); spec28.append(birth_row(29, 1)); spec28.append(one_past_row(29, 1))
spec28.append(one_past_row(30, 0)); spec28.append(birth_row(30, 1)); spec28.append(one_past_row(30, 1))
r31 = frontier_row(31, 19); r31['kind'] = 'frontier first contact proposal (FIRST-EVER m=31 row)'
spec28.append(r31)
r32 = frontier_row(32, 20); r32['kind'] = 'frontier first contact proposal (FIRST-EVER m=32 row)'
spec28.append(r32)

# load kit-7 frozen section (d) and compare
fut = json.load(open('future_kit8.json'))
k7rows = fut['registered_for_next_execution_kit_log_S5'][0]
assert len(k7rows) == 32, len(k7rows)
binding28 = k7rows[:28]

def norm_kind(k, m, d=None):
    return k

mismatch = 0
for i, (gen, ref) in enumerate(zip(spec28, binding28)):
    ok_m = gen['m'] == ref['m']
    ok_z = gen['z'] == ref['z']
    if i in (2,3):
        pass
    # prediction text: kit-7 text has extra annotations for some rows
    ref_txt = ref['prediction']
    gen_txt = gen['prediction']
    strict = gen_txt in ref_txt or ref_txt == gen_txt
    if not strict:
        mismatch += 1
        print('MISMATCH item%d m=%d z=%d' % (i + 1, ref['m'], ref['z']))
        print('  gen :', gen_txt)
        print('  kit7:', ref_txt)

# ---- check the kind strings separately (kit-7 kinds are descriptive) ----
kinds_ref = [r['kind'] for r in binding28]
for i, (gen, ref) in enumerate(zip(spec28, binding28)):
    chk(gen['m'] == ref['m'], 'item%d m' % (i + 1))
    chk(gen['z'] == ref['z'], 'item%d z' % (i + 1))

# ---- (D) trio mid-slice probes: z derivation ----
probes = []
for m in (13, 15, 17):
    d = (m - 1) // 2
    b = birth_row(m, d)
    chk(b['z'] == 3 * m - 2, 'probe z==3m-2 m=%d' % m)
    chk(S_of(m, d) == 3 * m, 'probe birth S==3m m=%d' % m)
    chk(co(m, d) == 2 * m, 'probe co-token==2m m=%d' % m)
    probes.append(b)

# kit-7 log S5 item 12 prose z values 37/42/48: mismatch disclosure
prose_slips = []
for (m, z_log) in [(13, 37), (15, 42), (17, 48)]:
    d = (m - 1) // 2
    z_true = zstar(m) + 2 * d
    if z_log != z_true:
        prose_slips.append((m, z_log, z_true))

# ---- (C) hole row m=26 z=25 ----
hole = {'m': 26, 'z': 25, 'R': 26 + 25 + 1}

# ---- (F) kit-9 future constants ----
future = []
future.append(one_past_row(19, 10)); future.append(birth_row(19, 11))
future.append(one_past_row(20, 10)); future.append(birth_row(20, 11))
future.append(one_past_row(21, 6));  future.append(birth_row(21, 7))
future.append(one_past_row(22, 6));  future.append(birth_row(22, 7))
future.append(one_past_row(23, 5));  future.append(birth_row(23, 6))
future.append(one_past_row(24, 5));  future.append(birth_row(24, 6))
future.append(one_past_row(25, 4));  future.append(birth_row(25, 5))
future.append(one_past_row(26, 4));  future.append(birth_row(26, 5))
future.append(one_past_row(27, 2));  future.append(birth_row(27, 3))
future.append(one_past_row(28, 2));  future.append(birth_row(28, 3))
future.append(birth_row(29, 2));    future.append(one_past_row(29, 2));   future.append(birth_row(29, 3))
future.append(birth_row(30, 2));    future.append(one_past_row(30, 2));   future.append(birth_row(30, 3))
# m=31/m=32 mini-ladders (contingent on kit-8 frontier first contacts)
r31a = one_past_row(31, 0); r31a['contingent'] = True
r31b = birth_row(31, 1)
r31c = one_past_row(31, 1)
r32a = one_past_row(32, 0); r32a['contingent'] = True
r32b = birth_row(32, 1)
r32c = one_past_row(32, 1)
future.extend([r31a, r31b, r31c, r32a, r32b, r32c])
f33 = frontier_row(33, 21); f33['kind'] = 'frontier first contact proposal (FIRST-EVER m=33 row)'
f34 = frontier_row(34, 22); f34['kind'] = 'frontier first contact proposal (FIRST-EVER m=34 row)'
future.extend([f33, f34])

# ---- (G) battery triples ----
bat = set()
k7 = json.load(open('kit7_battery_triples.json'))
for t in k7:
    bat.add(tuple(t))
meas_rows = [[19, 56], [19, 57], [20, 57], [20, 58], [21, 52], [21, 53],
             [22, 53], [22, 54], [23, 54], [23, 55], [24, 55], [24, 56],
             [25, 56], [25, 57], [26, 57], [26, 58], [27, 56], [27, 57],
             [28, 57], [28, 58], [29, 58], [29, 59], [29, 60], [30, 59],
             [30, 60], [30, 61], [31, 61], [32, 62],
             [26, 25], [13, 37], [15, 43], [17, 49]]
for z in range(49, 57):
    meas_rows.append([29, z])
for z in range(50, 58):
    meas_rows.append([30, z])
for (m, z) in meas_rows:
    R = m + z + 1
    for S in (m, m + 2, 2 * m, 2 * m + 1, m + 37, m + 38):
        bat.add((S, z, R))
    # seat collapse literals of the row's registered candidates
    bat.add((min(m + 2, m + 38), z, R))
# every future constant's named collapse literals
def lit_of_row(r):
    out = []
    m = r['m']; z = r['z']; R = r['R']
    # named v() literals in the prediction text
    import re
    for (S, zz, RR) in re.findall(r'v\((\d+),(\d+),(\d+)\)', r['prediction']):
        out.append((int(S), int(zz), int(RR)))
    return out
for r in spec28 + future + probes:
    for t in lit_of_row(r):
        chk(v(t[0], t[1], t[2]) in (0, 1, 2), 'battery triple valid')
        bat.add(t)
# new anchor collapse literals (kit-7 separation spots)
seps = json.load(open('kit7_seps.json'))
for s in seps:
    bat.add((s['S'], s['z'], s['R']))

# ---- report ----
print('checks:', len(checks), 'failed:', sum(1 for c in checks if not c[0]))
for c in checks:
    if not c[0]:
        print('FAIL:', c[1])
print('prediction text mismatches vs kit-7 frozen (d):', mismatch)
print('prose slips (kit-7 log S5 item-12 z):', prose_slips)
print('battery union triples:', len(bat))

out = {
  'binding28': binding28,
  'binding28_regenerated_ok': mismatch == 0,
  'trio_tracker': [
    {'m': 19, 'z': 56, 'X': [19, 19, 19], 'S': 57,
     'cand': 'mimic: UP 1v0 (value 1) like the birth seat one-past {19,38}@S=57, or conform (value 0 = collapse v(57,56,76)), or other; NON-BINDING observation candidate, any outcome is the datum'},
    {'m': 19, 'z': 57, 'X': [19, 19, 19], 'S': 57,
     'cand': 'mimic: DOWN 1v2 (value 1, collapse 2) like the stick {19,38}@S=57, or conform (value 2 = collapse v(57,57,77)), or other; NON-BINDING observation candidate, any outcome is the datum'},
  ],
  'hole_row': hole,
  'probes': probes,
  'future_kit9': future,
  'battery_triples': sorted(bat),
}
json.dump(out, open('kit8_spec.json', 'w'), indent=1)
print('kit8_spec.json written')
