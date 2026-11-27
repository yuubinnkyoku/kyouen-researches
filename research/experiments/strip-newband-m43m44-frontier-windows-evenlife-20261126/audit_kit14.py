#!/usr/bin/env python3
"""audit_kit14.py - fail-closed machine audit of the frozen kit-14 census
output. Data-driven, no hardcoded measured values beyond the pre-registered
candidate structure: every quantity is recomputed from the engine block
embedded in the frozen explorer and compared to the frozen .out. Exit code 0
iff ALL gates pass."""
import hashlib
import json
import re
import sys

OUT = 'explore_m43m44_frontier_windows_evenlife.out'
if len(sys.argv) > 1:
    OUT = sys.argv[1]
EXP = 'explore_m43m44_frontier_windows_evenlife.py'

src = open(EXP).read()
_d = {'lru_cache': __import__('functools').lru_cache}
_i = src.find("ENGINE_BLOCK = '''")
_j = src.find("\n'''\n", _i)
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


sec = {s.get('section'): s for s in d['sections']}
gate('G1_engine_gate_pass', sec['engine_gate']['gate'] == 'PASS' and
     sec['engine_gate']['pin'] == 'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92')

bat = sec['k0832_battery']
gate('G2_battery_all_match', bat['all_match'] is True and bat['bad'] == 0,
     'literals=%d' % bat['literals'])
gate('G2b_battery_count_1970', bat['literals'] == 1970, 'literals=%d' % bat['literals'])
bad = 0
for r in bat['rows']:
    if not (v(r['x'], r['z'], r['R']) == vC(r['x'], r['z'], r['R']) == vO(r['x'], r['z'], r['R']) == r['closed'] == r['vC'] == r['vO']):
        bad += 1
gate('G3_battery_recompute', bad == 0, 'bad=%d' % bad)

anch = sec['published_anchor_rechecks']
mismatch = [r for r in anch['rows'] if r['match'] is not True or r['value'] != r['published_value']]
gate('G4_anchor_733_match', len(anch['rows']) == 733 and not mismatch,
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
    H.cache_clear()
    scnt = 0
    for S in range(m, smax + 1):
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

# G8: total separations must equal the data-driven registered count:
# every binding seat + every rule-v2 split of every 2-token seat with
# co >= 2m + the evenlife seats/splits (trio conform) and clean windows
_ns = {'lru_cache': __import__('functools').lru_cache,
       'hashlib': __import__('hashlib'), '__name__': 'notmain'}
exec(src, _ns)
BIND = json.loads(_ns['K14_BINDING_JSON'])
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
EL = json.loads(_ns['K14_EVENLIFE_JSON'])
for r in EL:
    m = r['m']
    exp_total += 2
    for co in (2 * m + 8, 2 * m + 10):
        for x in range(m, co - m + 1):
            y = co - x
            if y >= x and y >= m:
                exp_total += 1
gate('G8_total_separations_registered_count', len(recomputed_seps) == exp_total,
     'total=%d expected=%d' % (len(recomputed_seps), exp_total))

# frontier rows: the 30th/31st parity datums, FIRST-EVER m>42 rows
f43 = sec['frontier_m43_z85_row_record']
f44 = sec['frontier_m44_z86_row_record']
gate('G9_frontier_m43_datum', f43['separations'] ==
     [{'S': 87, 'X': [43, 44], 'collapse': 0, 'direction': 'UP', 'value': 2}])
gate('G10_frontier_m44_datum', f44['separations'] ==
     [{'S': 88, 'X': [44, 44], 'collapse': 1, 'direction': 'UP', 'value': 2}])

# all 16 window rows clean
w41 = [sec['inband_m41_z%d_row_record' % z] for z in range(73, 81)]
w42 = [sec['inband_m42_z%d_row_record' % z] for z in range(74, 82)]
gate('G11_windows_16_clean', all(not s['separations'] for s in w41 + w42))

# even-m next-depth rows (m=14/16/18, z=3m+8): parity-flipped template,
# every stack an exact mimic of its host seat, trio conform (absent)
ok_even = True
for m in (14, 16, 18):
    s = sec['evenlife_m%d_z%d_row_record' % (m, 3 * m + 8)]
    seps = s['separations']
    fam = [p for p in seps if p['S'] == 3 * m + 8 and len(p['X']) == 2 and p['X'] == [m, 2 * m + 8]]
    new = [p for p in seps if p['S'] == 3 * m + 10 and len(p['X']) == 2 and p['X'] == [m, 2 * m + 10]]
    if len(fam) != 1 or (fam[0]['value'], fam[0]['collapse'], fam[0]['direction']) != (0, 2, 'DOWN'):
        ok_even = False
    if len(new) != 1 or (new[0]['value'], new[0]['collapse'], new[0]['direction']) != (2, 1, 'UP'):
        ok_even = False
    shadows = [p for p in seps if len(p['X']) == 3]
    if len(shadows) != 11:
        ok_even = False
    for p in shadows:
        host = [q for q in seps if q['S'] == p['S'] and len(q['X']) == 2]
        if len(host) != 1 or host[0]['value'] != p['value']:
            ok_even = False
    if any(p['X'] == [m, m, m] for p in seps):
        ok_even = False  # trio must conform at z=3m+8
gate('G12_evenlife_next_depth_template', ok_even)


# rule-v2 stack shadows + the early-follow observable: every 3-token
# separation in every row mimics its same-S 2-token host exactly; the
# m19/m20 one-past rows carry the full one-past-side split sets as mimics
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
r1968 = sec['ladder_m19_z68_row_record']['separations']
r2069 = sec['ladder_m20_z69_row_record']['separations']
ok_r2 = (ok_r2 and
         sorted(p['X'] for p in r1968 if len(p['X']) == 3) ==
         [[19, 19, 31], [19, 20, 30], [19, 21, 29], [19, 22, 28], [19, 23, 27], [19, 24, 26], [19, 25, 25]] and
         [p for p in r1968 if len(p['X']) == 2][0]['value'] == 1 and
         sorted(p['X'] for p in r2069 if len(p['X']) == 3) ==
         [[20, 20, 30], [20, 21, 29], [20, 22, 28], [20, 23, 27], [20, 24, 26], [20, 25, 25]] and
         [p for p in r2069 if len(p['X']) == 2][0]['value'] == 0)
gate('G13_rule_v2_early_follow_shadows', ok_r2)

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
gate('G15b_future_frontier_32nd_33rd',
     any(f.get('m') == 45 and f.get('z') == 89 for f in futc) and
     any(f.get('m') == 46 and f.get('z') == 90 for f in futc))

# no already-published row may be re-measured here: the kit-13 measured
# ladder/frontier/window/evenlife rows (full 49-row census of the kit-13
# frozen .out, commit 1a480530)
KIT13_ROWS = ["ladder_m19_z66_row_record", "ladder_m19_z67_row_record", "ladder_m20_z67_row_record", "ladder_m20_z68_row_record", "ladder_m21_z62_row_record", "ladder_m21_z63_row_record", "ladder_m22_z63_row_record", "ladder_m22_z64_row_record", "ladder_m23_z64_row_record", "ladder_m23_z65_row_record", "ladder_m24_z65_row_record", "ladder_m24_z66_row_record", "ladder_m25_z66_row_record", "ladder_m25_z67_row_record", "ladder_m26_z67_row_record", "ladder_m26_z68_row_record", "ladder_m27_z66_row_record", "ladder_m27_z67_row_record", "ladder_m28_z67_row_record", "ladder_m28_z68_row_record", "ladder_m29_z72_row_record", "ladder_m29_z73_row_record", "ladder_m30_z73_row_record", "ladder_m30_z74_row_record", "ladder_m31_z70_row_record", "ladder_m31_z71_row_record", "ladder_m32_z71_row_record", "ladder_m32_z72_row_record", "frontier_m41_z81_row_record", "frontier_m42_z82_row_record", "evenlife_m14_z48_row_record", "evenlife_m16_z54_row_record", "evenlife_m18_z60_row_record", "inband_m39_z69_row_record", "inband_m39_z70_row_record", "inband_m39_z71_row_record", "inband_m39_z72_row_record", "inband_m39_z73_row_record", "inband_m39_z74_row_record", "inband_m39_z75_row_record", "inband_m39_z76_row_record", "inband_m40_z70_row_record", "inband_m40_z71_row_record", "inband_m40_z72_row_record", "inband_m40_z73_row_record", "inband_m40_z74_row_record", "inband_m40_z75_row_record", "inband_m40_z76_row_record", "inband_m40_z77_row_record"]
gate('G16_duplicates_not_remeasured',
     all(name not in sec for name in KIT13_ROWS),
     'present=%s' % [name for name in KIT13_ROWS if name in sec][:5])

res = {'result': 'AUDIT-' + ('PASS' if all(g['pass'] for g in gates) else 'FAIL'),
       'gates': gates}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(0 if all(g['pass'] for g in gates) else 1)
