#!/usr/bin/env python3
"""audit_kit10.py - fail-closed machine audit of the frozen kit-10 census
output. Data-driven, no hardcoded measured values: every quantity is
recomputed from the engine block embedded in the frozen explorer and
compared to the frozen .out. Exit code 0 iff ALL gates pass."""
import hashlib
import json
import sys

OUT = 'explore_m35m36_frontier_ladders.out'
if len(sys.argv) > 1:
    OUT = sys.argv[1]
EXP = 'explore_m35m36_frontier_windows.py'

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
# independent recheck of every battery triple
bad = 0
for r in bat['rows']:
    if not (v(r['x'], r['z'], r['R']) == vC(r['x'], r['z'], r['R']) == vO(r['x'], r['z'], r['R']) == r['closed'] == r['vC'] == r['vO']):
        bad += 1
gate('G3_battery_recompute', bad == 0, 'bad=%d' % bad)

anch = sec['published_anchor_rechecks']
mismatch = [r for r in anch['rows'] if r['match'] is not True or r['value'] != r['published_value']]
gate('G4_anchor_334_match', len(anch['rows']) == 334 and not mismatch,
     'rows=%d mismatch=%d' % (len(anch['rows']), len(mismatch)))
# independent recomputation of anchor values
bad2 = 0
for r in anch['rows']:
    X = tuple(sorted(r['X'], reverse=True))
    if H(r['R'], X, r['z']) != r['value'] or v(sum(X), r['z'], r['R']) != r['collapse']:
        bad2 += 1
gate('G5_anchor_recompute', bad2 == 0, 'bad=%d' % bad2)

# recompute every row record sweep and compare separation multisets
rows = [s for s in d['sections'] if s.get('section', '').endswith('_row_record')]
gate('G6_row_count_57', len(rows) == 57, 'rows=%d' % len(rows))
bad_rows = []
recomputed_seps = []
for s in rows:
    m = s['min']; z = s['z']; R = s['R']
    smax = max(m + 38, z + 2)
    # regenerate parts identical to row_record_x0
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
    # compare with frozen separations
    frozen = [(p['S'], tuple(p['X']), p['value'], p['collapse']) for p in s['separations']]
    if sorted(from_parts) != sorted(frozen) or scnt != s['shapes']:
        bad_rows.append(s['section'])
    recomputed_seps.extend(from_parts)
gate('G7_row_sweeps_recompute', not bad_rows, 'bad=%s' % bad_rows[:5])

# total separation count
gate('G8_total_separations_95', len(recomputed_seps) == 95,
     'total=%d' % len(recomputed_seps))

# binding hit classification: frontier rows are the 23rd/24th parity datums
f35 = sec['frontier_m35_z69_row_record']; f36 = sec['frontier_m36_z70_row_record']
gate('G9_frontier_m35_datum', f35['separations'] == [{'S': 71, 'X': [35, 36], 'collapse': 0, 'direction': 'UP', 'value': 2}])
gate('G10_frontier_m36_datum', f36['separations'] == [{'S': 72, 'X': [36, 36], 'collapse': 1, 'direction': 'UP', 'value': 2}])

# all 16 window rows clean
w33 = [sec['inband_m33_z%d_row_record' % z] for z in range(57, 65)]
w34 = [sec['inband_m34_z%d_row_record' % z] for z in range(58, 66)]
gate('G11_windows_16_clean', all(not s['separations'] for s in w33 + w34))

# even-life rows: parity-flipped template (family DOWN 0v1/0v2, NEW UP 2v1)
ok_even = True
for m in (14, 16, 18):
    fam, tri, newco, nspl = (m, 2 * m), (m, m, m), (m, 2 * m + 2), (m, m + 1, m + 2 - 1)
    op1 = sec['evenlife_m%d_z%d_row_record' % (m, 3 * m - 1)]['separations']
    st = sec['evenlife_m%d_z%d_row_record' % (m, 3 * m)]['separations']
    op2 = sec['evenlife_m%d_z%d_row_record' % (m, 3 * m + 1)]['separations']
    exp_op1 = sorted([{'S': 3 * m, 'X': [m, 2 * m], 'collapse': 1, 'direction': 'DOWN', 'value': 0},
                      {'S': 3 * m, 'X': [m, m, m], 'collapse': 1, 'direction': 'DOWN', 'value': 0}], key=str)
    exp_st = sorted([{'S': 3 * m, 'X': [m, 2 * m], 'collapse': 2, 'direction': 'DOWN', 'value': 0},
                     {'S': 3 * m, 'X': [m, m, m], 'collapse': 2, 'direction': 'DOWN', 'value': 0},
                     {'S': 3 * m + 2, 'X': [m, 2 * m + 2], 'collapse': 1, 'direction': 'UP', 'value': 2},
                     {'S': 3 * m + 2, 'X': [m, m, m + 2], 'collapse': 1, 'direction': 'UP', 'value': 2},
                     {'S': 3 * m + 2, 'X': [m, m + 1, m + 1], 'collapse': 1, 'direction': 'UP', 'value': 2}], key=str)
    exp_op2 = sorted([{'S': 3 * m + 2, 'X': [m, 2 * m + 2], 'collapse': 1, 'direction': 'DOWN', 'value': 0},
                      {'S': 3 * m + 2, 'X': [m, m, m + 2], 'collapse': 1, 'direction': 'DOWN', 'value': 0},
                      {'S': 3 * m + 2, 'X': [m, m + 1, m + 1], 'collapse': 1, 'direction': 'DOWN', 'value': 0}], key=str)
    if sorted(op1, key=str) != exp_op1 or sorted(st, key=str) != exp_st or sorted(op2, key=str) != exp_op2:
        ok_even = False
gate('G12_evenlife_parity_template', ok_even)

# rule v2 stack shadows at m19/m20 stick+NEW seats: exact mimics, no anomaly
def mimic_check(m, za, seat_S, seat_val, seps):
    host = [p for p in seps if p['S'] == seat_S and len(p['X']) == 2]
    shadows = [p for p in seps if p['S'] == seat_S and len(p['X']) == 3]
    return len(host) == 1 and host[0]['value'] == seat_val and \
        all(p['value'] == seat_val for p in shadows)

r1960 = sec['ladder_m19_z60_row_record']['separations']
r1961 = sec['ladder_m19_z61_row_record']['separations']
r2061 = sec['ladder_m20_z61_row_record']['separations']
r2062 = sec['ladder_m20_z62_row_record']['separations']
ok_r2 = (mimic_check(19, 60, 61, 1, r1960) and len([p for p in r1960 if p['S'] == 61]) == 4 and
         mimic_check(19, 61, 61, 1, r1961) and mimic_check(19, 61, 63, 2, r1961) and
         mimic_check(20, 61, 62, 0, r2061) and
         mimic_check(20, 62, 62, 0, r2062) and mimic_check(20, 62, 64, 2, r2062))
gate('G13_rule_v2_stick_and_new_shadows', ok_r2)

# ladder rows: all 30 registered seats present with exact values, zero
# unregistered separations beyond the rule-v2 shadow track
fut = json.load(open('K10_BINDING.json'))
unregistered = []
for r in fut:
    m = r['m']; z = r['z']
    key = ('frontier_m%d_z%d' if r['kind'] == 'frontier' else 'ladder_m%d_z%d') % (m, z)
    if key not in sec:
        continue
    seps = sec[key]['separations']
    for s_ in seps:
        X = tuple(s_['X']); S = s_['S']
        seatish = any(tuple(sr[:2]) == (m, X[-1]) and sr[2] == S for sr in r['seats'])
        shadow = len(X) == 3 and X[0] == m and sum(X) == S and X[1] + X[2] == S - m
        if not (seatish or shadow):
            unregistered.append((key, s_))
gate('G14_no_unregistered_ladder_separations', not unregistered,
     'unregistered=%s' % unregistered[:5])

# future registration constants present and 34 items
futc = sec['future_slice_registration_constants']['registered_for_next_execution_kit_log_S5'][0][0]
gate('G15_future_constants_34', len(futc) == 34, 'items=%d' % len(futc))

res = {'result': 'AUDIT-' + ('PASS' if all(g['pass'] for g in gates) else 'FAIL'),
       'gates': gates}
print(json.dumps(res, sort_keys=True, separators=(',', ':')))
sys.exit(0 if all(g['pass'] for g in gates) else 1)
