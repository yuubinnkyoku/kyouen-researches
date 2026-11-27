#!/usr/bin/env python3
"""audit_kit17.py - fail-closed machine audit of the frozen kit-17 census
output. Data-driven, no hardcoded measured values beyond the pre-registered
candidate structure: every quantity is recomputed from the engine block
embedded in the frozen explorer and compared to the frozen .out. Exit code 0
iff ALL gates pass."""
import hashlib
import json
import re
import sys

OUT = 'explore_m49m50_frontier_windows_evenlife.out'
if len(sys.argv) > 1:
    OUT = sys.argv[1]
EXP = 'explore_m49m50_frontier_windows_evenlife.py'

src = open(EXP).read()
_d = {'lru_cache': __import__('functools').lru_cache}
_i = src.find("ENGINE_BLOCK = '''")
_j = src.find("\n'''", _i)
eng = src[_i + len("ENGINE_BLOCK = '''"):_j + 1]
assert hashlib.sha256(eng.encode()).hexdigest() == \
    'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
exec(eng, _d)
H = _d['H_canonical']
v = _d['single_token']
vC = _d['vC']
vO = _d['vO']

d = json.load(open(OUT))
gates = []


def gate(name, ok, detail=''):
    gates.append({'gate': name, 'pass': bool(ok), 'detail': detail})


def splits(co, m):
    out = []
    for x in range(m, co - m + 1):
        y = co - x
        if y >= x and y >= m:
            out.append([m, x, y])
    return out


sec = {s.get('section'): s for s in d['sections']}
gate('G1_engine_gate_pass', sec['engine_gate']['gate'] == 'PASS' and
     sec['engine_gate']['pin'] == 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92')

bat = sec['k0832_battery']
gate('G2_battery_all_match', bat['all_match'] is True and bat['bad'] == 0,
     'literals=%d' % bat['literals'])
gate('G2b_battery_count_2162', bat['literals'] == 2162, 'literals=%d' % bat['literals'])
bad = 0
for r in bat['rows']:
    if not (v(r['x'], r['z'], r['R']) == vC(r['x'], r['z'], r['R']) == vO(r['x'], r['z'], r['R']) == r['closed'] == r['vC'] == r['vO']):
        bad += 1
gate('G3_battery_recompute', bad == 0, 'bad=%d' % bad)

anch = sec['published_anchor_rechecks']
mismatch = [r for r in anch['rows'] if r['match'] is not True or r['value'] != r['published_value']]
gate('G4_anchor_1210_match', len(anch['rows']) == 1210 and not mismatch,
     'rows=%d mismatch=%d' % (len(anch['rows']), len(mismatch)))
bad2 = 0
for r in anch['rows']:
    X = tuple(sorted(r['X'], reverse=True))
    if H(r['R'], X, r['z']) != r['value'] or v(sum(X), r['z'], r['R']) != r['collapse']:
        bad2 += 1
gate('G5_anchor_recompute', bad2 == 0, 'bad=%d' % bad2)

# recompute every row record sweep and compare separation multisets
rows = [s for s in d['sections'] if s.get('section', '').endswith('_row_record')]
gate('G6_row_count_49', len(rows) == 49, 'rows=%d' % len(rows))
bad_rows = []
recomputed_seps = []
for s in rows:
    m = s['min']; z = s['z']; R = s['R']
    smax = max(m + 38, z + 2)
    from_parts = []

    def parts(s_, lo, arity):
        out = []

        def rec(rem, k, cur):
            if rem == 0:
                if 1 <= len(cur) <= arity:
                    out.append(tuple(cur))
                return
            if k == arity:
                return
            for t in range(lo, rem + 1):
                if cur and t < cur[-1]:
                    continue
                cur.append(t)
                rec(rem - t, k + 1, cur)
                cur.pop()
        rec(s_, 0, [])
        return out
    scnt = 0
    for S in range(m, smax + 1):
        H.cache_clear()
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                from_parts.append((S, tuple(X), hv, ev))
    frozen = [(p['S'], tuple(p['X']), p['value'], p['collapse']) for p in s['separations']]
    if sorted(from_parts) != sorted(frozen) or scnt != s['shapes']:
        bad_rows.append(s['section'])
    recomputed_seps.extend(from_parts)
gate('G7_row_sweeps_recompute', not bad_rows, 'bad=%s' % bad_rows[:5])

# G8: total separations must equal the data-driven registered count
_ns = {'lru_cache': __import__('functools').lru_cache,
       'hashlib': __import__('hashlib'), '__name__': 'notmain'}
exec(src, _ns)
BIND = json.loads(_ns['K17_BINDING_JSON'])
exp_total = 0
for r in BIND:
    exp_total += len(r['seats'])
    if r['kind'] != 'frontier':
        for s in r['seats']:
            co = s[1]
            if co >= 2 * r['m']:
                for x in range(r['m'], co - r['m'] + 1):
                    y = co - x
                    if y >= x and y >= r['m']:
                        exp_total += 1
EL = json.loads(_ns['K17_EVENLIFE_JSON'])
for r in EL:
    m = r['m']
    exp_total += 2
    for co in (2 * m + 14, 2 * m + 16):
        for x in range(m, co - m + 1):
            y = co - x
            if y >= x and y >= m:
                exp_total += 1
gate('G8_total_separations_registered_count', len(recomputed_seps) == exp_total,
     'total=%d expected=%d' % (len(recomputed_seps), exp_total))

# frontier rows: the 36th/37th parity datums, FIRST-EVER m>48 rows
f49 = sec['frontier_m49_z97_row_record']
f50 = sec['frontier_m50_z98_row_record']
gate('G9_frontier_m49_datum', f49['separations'] ==
     [{'S': 99, 'X': [49, 50], 'collapse': 0, 'direction': 'UP', 'value': 2}])
gate('G10_frontier_m50_datum', f50['separations'] ==
     [{'S': 100, 'X': [50, 50], 'collapse': 1, 'direction': 'UP', 'value': 2}])

# all 16 window rows clean
w47 = [sec['inband_m47_z%d_row_record' % z] for z in range(85, 93)]
w48 = [sec['inband_m48_z%d_row_record' % z] for z in range(86, 94)]
gate('G11_windows_16_clean', all(not s['separations'] for s in w47 + w48))

# even-m next-depth rows (m=14/16/18, z=3m+14): parity-flipped template,
# every stack an exact mimic of its host seat, trio conform (absent)
ok_even = True
for m in (14, 16, 18):
    s = sec['evenlife_m%d_z%d_row_record' % (m, 3 * m + 14)]
    seps = s['separations']
    fam = [p for p in seps if p['S'] == 3 * m + 14 and len(p['X']) == 2 and p['X'] == [m, 2 * m + 14]]
    new = [p for p in seps if p['S'] == 3 * m + 16 and len(p['X']) == 2 and p['X'] == [m, 2 * m + 16]]
    if len(fam) != 1 or (fam[0]['value'], fam[0]['collapse'], fam[0]['direction']) != (0, 2, 'DOWN'):
        ok_even = False
    if len(new) != 1 or (new[0]['value'], new[0]['collapse'], new[0]['direction']) != (2, 1, 'UP'):
        ok_even = False
    shadows = [p for p in seps if len(p['X']) == 3]
    want_shadows = len(splits(2 * m + 14, m)) + len(splits(2 * m + 16, m))
    if len(shadows) != want_shadows:
        ok_even = False
    for p in shadows:
        host = [q for q in seps if q['S'] == p['S'] and len(q['X']) == 2]
        if len(host) != 1 or host[0]['value'] != p['value']:
            ok_even = False
    if any(p['X'] == [m, m, m] for p in seps):
        ok_even = False  # trio must conform at z=3m+14
gate('G12_evenlife_next_depth_template', ok_even)


# rule-v2 stack shadows + the early-follow observable + the m=25 boundary
# equistack: every 3-token separation in every row mimics its same-S
# 2-token host exactly; the m19/m20 one-past rows carry the full split
# sets as mimics; at m=25 (co=50=2m boundary) the equistack {25,25,25}
# separates as an exact mimic of the one-past seat {25,50} (3rd boundary
# observation; kit-16 saw the 2nd at m=24 one-past co=48, kit-15 the 1st)
def row_mimics(seps):
    for p in seps:
        if len(p['X']) == 3:
            host = [q for q in seps if q['S'] == p['S'] and len(q['X']) == 2 and q['X'][0] == p['X'][0]]
            if len(host) != 1 or any(q['value'] != p['value'] for q in host):
                return False
    return True


ok_r2 = True
for s in rows:
    if not row_mimics(s['separations']):
        ok_r2 = False
r1974 = sec['ladder_m19_z74_row_record']['separations']
r2075 = sec['ladder_m20_z75_row_record']['separations']
# expected early-follow split sets, machine-derived (co=56 both sides)
exp19 = sorted(splits(56, 19))
exp20 = sorted(splits(56, 20))
b19 = [p for p in r1974 if len(p['X']) == 2]
b20 = [p for p in r2075 if len(p['X']) == 2]
ok_r2 = (ok_r2 and
         sorted(p['X'] for p in r1974 if len(p['X']) == 3) == exp19 and
         len(b19) == 1 and (b19[0]['value'], b19[0]['collapse']) == (1, 0) and
         sorted(p['X'] for p in r2075 if len(p['X']) == 3) == exp20 and
         len(b20) == 1 and (b20[0]['value'], b20[0]['collapse']) == (0, 1))
# m=25 boundary equistack: one-past seat {25,50}@S=75 has co=50=2m exactly
r2574 = sec['ladder_m25_z74_row_record']['separations']
eq = [p for p in r2574 if p['X'] == [25, 25, 25]]
host25 = [q for q in r2574 if q['S'] == 75 and q['X'] == [25, 50]]
ok_r2 = ok_r2 and len(eq) == 1 and len(host25) == 1 and \
    eq[0]['value'] == host25[0]['value']
gate('G13_rule_v2_early_follow_boundary_equistack', ok_r2)

# binding rows: all registered seats present with exact values, zero
# unregistered separations beyond the rule-v2 shadow track
fut = BIND
unregistered = []
seatmiss = []
for r in fut:
    m = r['m']; z = r['z']
    key = ('frontier_m%d_z%d' if r['kind'] == 'frontier' else 'ladder_m%d_z%d') % (m, z) + '_row_record'
    if key not in sec:
        seatmiss.append(key)
        continue
    seps = sec[key]['separations']
    for s_ in seps:
        X = tuple(s_['X']); S = s_['S']
        seatish = any(tuple(sr[:2]) == (m, X[-1]) and sr[2] == S and len(X) == 2
                      for sr in r['seats'])
        shadow = len(X) == 3 and X[0] == m and sum(X) == S and X[1] + X[2] == S - m
        if not (seatish or shadow):
            unregistered.append((key, s_))
    # every registered seat separates with the registered ud
    for sr in r['seats']:
        a, co, S, lab = sr
        found = [p for p in seps if p['S'] == S and p['X'] == [m, co]]
        mm = re.search(r'(UP|DOWN) (\d+)v(\d+)', lab)
        if r['kind'] == 'frontier':
            if not found or found[0]['value'] != 2 or found[0]['direction'] != 'UP':
                seatmiss.append((key, lab))
        elif not found:
            seatmiss.append((key, lab))
        elif mm:
            p = found[0]
            got = ('UP' if p['value'] > p['collapse'] else 'DOWN', p['value'], p['collapse'])
            if got != (mm.group(1), int(mm.group(2)), int(mm.group(3))):
                seatmiss.append((key, lab, p))
gate('G14_no_unregistered_ladder_separations',
     not unregistered and not seatmiss,
     'unregistered=%s seatmiss=%s' % (unregistered[:3], seatmiss[:3]))

# future registration constants present and 34 items
futc = sec['future_slice_registration_constants']['registered_for_next_execution_kit_log_S5'][0][0]
gate('G15_future_constants_34', len(futc) == 34, 'items=%d' % len(futc))
gate('G15b_future_frontier_38th_39th',
     any(f.get('m') == 51 and f.get('z') == 101 for f in futc) and
     any(f.get('m') == 52 and f.get('z') == 102 for f in futc))
# kit-18 window proposals: z*(49)-8..-1 = 89..96, z*(50)-8..-1 = 90..97
w49 = [f for f in futc if f.get('m') == 49 and f['kind'].startswith('in-band window')]
w50 = [f for f in futc if f.get('m') == 50 and f['kind'].startswith('in-band window')]
gate('G15c_future_windows_arithmetic',
     len(w49) == 1 and len(w50) == 1 and w49[0]['z'] == '89..96' and w50[0]['z'] == '90..97')

# no already-published row may be re-measured here: the kit-16 measured
# ladder/frontier/window/evenlife rows (full 49-row census of the kit-16
# frozen .out, commit f997daca)
KIT16_ROWS = ["evenlife_m14_z54_row_record", "evenlife_m16_z60_row_record", "evenlife_m18_z66_row_record", "frontier_m47_z93_row_record", "frontier_m48_z94_row_record", "inband_m45_z81_row_record", "inband_m45_z82_row_record", "inband_m45_z83_row_record", "inband_m45_z84_row_record", "inband_m45_z85_row_record", "inband_m45_z86_row_record", "inband_m45_z87_row_record", "inband_m45_z88_row_record", "inband_m46_z82_row_record", "inband_m46_z83_row_record", "inband_m46_z84_row_record", "inband_m46_z85_row_record", "inband_m46_z86_row_record", "inband_m46_z87_row_record", "inband_m46_z88_row_record", "inband_m46_z89_row_record", "ladder_m19_z72_row_record", "ladder_m19_z73_row_record", "ladder_m20_z73_row_record", "ladder_m20_z74_row_record", "ladder_m21_z68_row_record", "ladder_m21_z69_row_record", "ladder_m22_z69_row_record", "ladder_m22_z70_row_record", "ladder_m23_z70_row_record", "ladder_m23_z71_row_record", "ladder_m24_z71_row_record", "ladder_m24_z72_row_record", "ladder_m25_z72_row_record", "ladder_m25_z73_row_record", "ladder_m26_z73_row_record", "ladder_m26_z74_row_record", "ladder_m27_z72_row_record", "ladder_m27_z73_row_record", "ladder_m28_z73_row_record", "ladder_m28_z74_row_record", "ladder_m29_z78_row_record", "ladder_m29_z79_row_record", "ladder_m30_z79_row_record", "ladder_m30_z80_row_record", "ladder_m31_z76_row_record", "ladder_m31_z77_row_record", "ladder_m32_z77_row_record", "ladder_m32_z78_row_record"]
assert len(KIT16_ROWS) == 49
gate('G16_duplicates_not_remeasured',
     all(name not in sec for name in KIT16_ROWS),
     'present=%s' % [name for name in KIT16_ROWS if name in sec][:5])

# dead seats: every registered dead seat CONFORMS (is absent) at z=S-1
dead_ok = True
for r in BIND:
    ds = r.get('expect_dead_seat') or r.get('dead_seat')
    if not ds:
        continue
    m, co, z = ds
    key = 'ladder_m%d_z%d_row_record' % (m, z)
    for p in sec[key]['separations']:
        if p['X'] == [m, co] and p['S'] == z - 1:
            dead_ok = False
gate('G17_dead_seats_conform', dead_ok)

res = {'result': 'AUDIT-' + ('PASS' if all(g['pass'] for g in gates) else 'FAIL'),
       'gates': gates}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(0 if all(g['pass'] for g in gates) else 1)
