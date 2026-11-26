#!/usr/bin/env python3
"""audit_kit9.py: INDEPENDENT ordered-engine audit of the kit-9 frozen
census. Re-executes every row of explore_m33m34_frontier_ladders.out with
H_ordered (the published ordered product engine) instead of the
canonical-sweep engine, then:
 - re-counts all shapes and separations per row (equality with the
   published .out),
 - re-anchors all 234 published spots with the ordered engine,
 - re-checks the 1,454 battery literals closed==vC==vO,
 - classifies the 34 binding rows against their registered, structured
   candidates (seats / dead-seat / stack-candidates / trackers): FULL
   HIT iff the measured pair-seat set equals the registered set, every
   registered seat keeps its registered (direction, value, collapse),
   every registered stack-candidate is present as an exact numeric
   mimic, every dead-seat conforms, and every registered tracker row
   conforms; unregistered 3-token shadows are reported explicitly,
 - reports the lifecycle rows, the even-mid probes, the window rows
   and the two trio trackers explicitly,
 - machine-checks the CO-SPLIT SHADOW pattern across all 62 rows:
   every 3-token separation is {m}+split(co) of a 2-token separation at
   the same S with an identical (value, collapse, direction) triple,
   and every admissible split of every pair-seat is present (candidate
   generalization of the kit-8 log S5 item-9 rule; NON-BINDING here).
"""
import json, re, ast, hashlib
from functools import lru_cache

EXP = 'explore_m33m34_frontier_ladders.py'
OUT = 'explore_m33m34_frontier_ladders.out'

src = open(EXP).read()
bad = [c for c in src if ord(c) > 127]
assert not bad, 'non-ASCII in explorer source'
i = src.index("ENGINE_BLOCK = '''")
j = src.index("'''\n\nPIN", i)
content = src[i + 18:j]
ns = {'lru_cache': lru_cache}
exec(content, ns)
H_c = ns['H_canonical']
H_o = ns['H_ordered']
v = ns['single_token']
PIN = re.search(r"PIN = '([0-9a-f]{64})'", src).group(1)
assert hashlib.sha256(content.encode('utf-8')).hexdigest() == PIN

def grab(name):
    m = re.search(r'\n' + name + r' = ("(?:[^"\\]|\\.)*")', src)
    return json.loads(ast.literal_eval(m.group(1)))
bind = grab('K9_BINDING_JSON')
life = grab('K9_LIFECYCLE_JSON')
probes = grab('K9_PROBES_JSON')

def parts(s, lo, arity):
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
    rec(s, 0, [])
    return out

def ordered_row(R, z, m, smin, smax):
    H_o.cache_clear()
    sep = []
    scnt = 0
    for S in range(smin, smax + 1):
        for X in parts(S, m, 3):
            if not X or X[0] != m:
                continue
            hv = H_o(R, X, z)
            ev = v(S, z, R)
            scnt += 1
            if hv != ev:
                sep.append({'X': list(X), 'S': S, 'value': hv,
                            'collapse': ev,
                            'direction': 'UP' if hv > ev else 'DOWN'})
    return scnt, sep

pub = json.load(open(OUT))
secs = pub['sections']
rows = [s for s in secs if s['section'].endswith('_row_record')]
rows_by_sec = {r['section']: r for r in rows}
assert pub['result'] == 'EXPLORE-DONE'

print('SECTION A: ordered-engine re-execution of all %d rows' % len(rows))
bad_a = 0
for r in rows:
    m = r['min']; z = r['z']; R = r['R']
    dom = r['s_domain']
    a, b = dom[1:-1].split('..')
    scnt, sep = ordered_row(R, z, m, int(a), int(b))
    ok = (scnt == r['shapes']) and (sep == r['separations'])
    if not ok:
        bad_a += 1
        print('  MISMATCH', r['section'], scnt, r['shapes'], len(sep),
              len(r['separations']))
print('  rows=%d mismatches=%d' % (len(rows), bad_a))

print('SECTION B: ordered-engine anchors (234 expected)')
anch = next(s for s in secs if s['section'] == 'published_anchor_rechecks')['rows']
bad_b = 0
H_o.cache_clear()
for a in anch:
    XX = tuple(sorted(a['X'], reverse=True))
    if H_o(a['R'], XX, a['z']) != a['value']:
        bad_b += 1
print('  anchors=%d exact=%d' % (len(anch), len(anch) - bad_b))

print('SECTION C: battery literals (1454 expected)')
bat = next(s for s in secs if s['section'] == 'k0832_battery')
bad_c = 0
for b in bat['rows']:
    if not (v(b['x'], b['z'], b['R']) == ns['vO'](b['x'], b['z'], b['R'])
            == ns['vC'](b['x'], b['z'], b['R']) == b['closed']):
        bad_c += 1
print('  literals=%d bad=%d' % (len(bat['rows']), bad_c))

print('SECTION D: classification of the %d binding rows' % len(bind))
seat_re = r'[\{\(](%d), ?(%d)[\}\)]@S=(%d) (UP|DOWN) (\d+)v(\d+)'
def parse_seats(cand, seats):
    named = {}
    for (a, b, S, role) in seats:
        mm = re.search(seat_re % (a, b, S), cand)
        if mm is None:
            mm = re.search(r'[\{\(](%d), ?(%d)[\}\)] ?(UP|DOWN) (\d+)v(\d+)'
                           % (a, b), cand)
            assert mm, (a, b, S, cand[:120])
            # stick-format seat: S comes from the structured field
            named[tuple(sorted((a, b), reverse=True))] = (S, mm.group(3),
                int(mm.group(4)), int(mm.group(5)))
            continue
        named[tuple(sorted((a, b), reverse=True))] = (S, mm.group(4),
            int(mm.group(5)), int(mm.group(6)))
    return named

def classify(r, reg, tag):
    m, z, R = reg['m'], reg['z'], r['R']
    seps = r['separations']
    named = parse_seats(reg['cand'], reg['seats'])
    measured_pairs = {}
    for sp in seps:
        if len(sp['X']) == 2:
            key = tuple(sorted(sp['X'], reverse=True))
            measured_pairs[key] = (sp['S'], sp['direction'],
                sp['value'], sp['collapse'])
    lines = []
    verdict = 'HIT'
    if set(named) != set(measured_pairs):
        verdict = 'DEVIATION'
        lines.append('seat-set mismatch: measured %s named %s' % (
            sorted(measured_pairs), sorted(named)))
    else:
        for key, exp in named.items():
            got = measured_pairs[key]
            if got != exp:
                verdict = 'DEVIATION'
                lines.append('seat %s exp %s got %s' % (key, exp, got))
    # dead-seat conform
    ds = reg.get('dead_seat')
    if ds:
        a, b, dz = ds
        key = tuple(sorted((a, b), reverse=True))
        H_o.cache_clear()
        ev = v(a + b, z, R)
        hv = H_o(R, key, z)
        if hv != ev:
            verdict = 'DEVIATION'
            lines.append('dead-seat %s NOT conforming at z=%d: %s vs %s'
                         % (key, z, hv, ev))
    # registered stack candidates (exact mimic of their seat)
    stack_reg = reg.get('stack_candidates') or []
    reg_stack_keys = set()
    for sc in stack_reg:
        key = tuple(sc['X'])
        reg_stack_keys.add(key)
        sp = next((x for x in seps if tuple(x['X']) == key
                   and x['S'] == sc['S']), None)
        if sp is None:
            verdict = 'DEVIATION'
            lines.append('missing registered stack %s' % (key,))
    # trio trackers: expected CONFORM
    for t in reg.get('tracker') or []:
        H_o.cache_clear()
        key = tuple(t['X'])
        hv = H_o(R, key, z)
        ev = v(t['S'], z, R)
        if hv != ev:
            verdict = 'DEVIATION'
            lines.append('tracker %s NOT conforming at z=%d: %s vs %s'
                         % (key, z, hv, ev))
    measured_stacks = [sp for sp in seps if len(sp['X']) == 3]
    unreg = [sp for sp in measured_stacks
             if tuple(sp['X']) not in reg_stack_keys]
    return verdict, lines, named, measured_pairs, unreg

full = 0
shadow_rows = []
for reg in bind:
    r = rows_by_sec[('frontier_m%d_z%d_row_record' % (reg['m'], reg['z']))
                    if reg.get('frontier')
                    else ('lifecycle_m%d_z%d_row_record' % (reg['m'], reg['z'])
                          if reg.get('lifecycle_kind')
                          else 'ladder_m%d_z%d_row_record' % (reg['m'], reg['z']))]
    verdict, lines, named, mp, unreg = classify(r, reg, 'bind')
    if unreg:
        shadow_rows.append((reg['item'], reg['m'], reg['z'], unreg))
    if verdict == 'HIT' and not unreg and not lines:
        full += 1
        print('  item%-3d m=%-2d z=%-2d %-4s %s' % (
            reg['item'], reg['m'], reg['z'], verdict,
            'FULL' if not unreg else ''))
    else:
        print('  item%-3d m=%-2d z=%-2d %s %s' % (
            reg['item'], reg['m'], reg['z'], verdict, '; '.join(lines)))
        for sp in unreg:
            print('      unregistered 3-token: %s %dv%d %s S=%d' % (
                sp['X'], sp['value'], sp['collapse'], sp['direction'],
                sp['S']))
print('  binding FULL HIT (seats+stacks+tracker, no unregistered '
      'shadows): %d/%d' % (full, len(bind)))

print('SECTION E: lifecycle rows (9, NON-BINDING scaffold)')
for reg in life:
    r = rows_by_sec['lifecycle_m%d_z%d_row_record' % (reg['m'], reg['z'])]
    seps = r['separations']
    named = parse_seats(reg['cand'], reg['seats'])
    mp = {}
    trios = []
    for sp in seps:
        if len(sp['X']) == 2:
            mp[tuple(sorted(sp['X'], reverse=True))] = (
                sp['S'], sp['direction'], sp['value'], sp['collapse'])
        elif len(sp['X']) == 3:
            trios.append(sp)
    ok = set(named) == set(mp) and all(mp[k] == named[k] for k in named)
    tm = [sp for sp in trios if len(set(sp['X'])) == 1]
    print('  m=%-2d z=%-2d seats %s | trio %s | other stacks %s' % (
        reg['m'], reg['z'], 'HIT' if ok else 'MISMATCH',
        ('%s %dv%d %s' % (tm[0]['X'], tm[0]['value'], tm[0]['collapse'],
                          tm[0]['direction'])) if tm else 'CONFORM',
        [('%s %dv%d' % (sp['X'], sp['value'], sp['collapse']))
         for sp in trios if len(set(sp['X'])) > 1]))

print('SECTION F: even-mid probes (3)')
for reg in probes:
    r = rows_by_sec['evenmid_m%d_z%d_row_record' % (reg['m'], reg['z'])]
    verdict, lines, named, mp, unreg = classify(r, reg, 'probe')
    news = tuple(sorted((reg['m'], reg['seats'][-1][1]), reverse=True))
    trio = [sp for sp in r['separations'] if len(set(sp['X'])) == 1]
    if trio:
        t = trio[0]
        mimic = (news in mp and t['value'] == mp[news][2]
                 and t['collapse'] == mp[news][3])
        ttxt = '%s %dv%d %s -> mimic of NEW seat: %s' % (
            t['X'], t['value'], t['collapse'], t['direction'], mimic)
    else:
        ttxt = 'not measured'
    print('  m=%d z=%d seats %s %s | trio: %s | unreg stacks: %s' % (
        reg['m'], reg['z'], verdict, '; '.join(lines), ttxt,
        [sp['X'] for sp in unreg]))

print('SECTION G: window rows (16, expect 0 separations each)')
win = [r for r in rows if r['section'].startswith('inband')]
tot = sum(len(r['separations']) for r in win)
print('  rows=%d total_seps=%d -> %s' % (
    len(win), tot, 'ALL CLEAN' if tot == 0 else 'DIRTY'))
print('  band notes:')
for r in win:
    if r['section'].endswith(('z53_row_record', 'z54_row_record')):
        print('   ', r['section'], '|', r.get('band'))

print('SECTION H: trio trackers (m=19, registered NON-BINDING)')
for reg in bind:
    for t in reg.get('tracker') or []:
        r = rows_by_sec['ladder_m%d_z%d_row_record' % (reg['m'], reg['z'])]
        H_o.cache_clear()
        hv = H_o(r['R'], tuple(t['X']), reg['z'])
        ev = v(t['S'], reg['z'], r['R'])
        print('  m=19 z=%d trio %s: %s (expected CONFORM)' % (
            reg['z'], t['X'], 'CONFORM' if hv == ev
            else 'DEVIATION %d vs %d' % (hv, ev)))

print('SECTION I: CO-SPLIT SHADOW lemma check across all %d rows' % len(rows))
def splits(co, m):
    return [(a, co - a) for a in range(m, co // 2 + 1)]
anom = 0
for r in rows:
    seps2 = {}
    seps3 = {}
    for sp in r['separations']:
        if len(sp['X']) == 2:
            seps2[sp['S']] = [sp]
        elif len(sp['X']) == 3:
            seps3.setdefault(sp['S'], []).append(sp)
    for key in seps2:
        seps2[key] = [sp for sp in r['separations']
                      if len(sp['X']) == 2 and sp['S'] == key]
    allS = set(sp['S'] for sp in r['separations'])
    for S in allS:
        for sp3 in seps3.get(S, []):
            # (i) is it {m}+split(co) of a pair at same S?
            ok = False
            for sp2 in [sp for sp in r['separations']
                        if len(sp['X']) == 2 and sp['S'] == S]:
                co = sp2['X'][1]
                parts3 = tuple(sorted(sp3['X'][1:]))
                if (parts3 in splits(co, sp2['X'][0])
                        and sp3['X'][0] == sp2['X'][0]
                        and (sp3['value'], sp3['collapse'],
                             sp3['direction'])
                        == (sp2['value'], sp2['collapse'],
                            sp2['direction'])):
                    ok = True
                    break
            if not ok:
                anom += 1
                print('  ANOMALY %s: stack %s at S=%d is not an exact '
                      'mimic split of a pair seat' % (r['section'],
                      sp3['X'], S))
        # (ii) every admissible split present
        for sp2 in [sp for sp in r['separations']
                    if len(sp['X']) == 2 and sp['S'] == S]:
            m0, co = sp2['X']
            for (a, b) in splits(co, m0):
                want = tuple(sorted([m0, a, b], reverse=True))
                if not any(tuple(sorted(sp3['X'], reverse=True)) == want
                           for sp3 in seps3.get(S, [])):
                    anom += 1
                    print('  ANOMALY %s: missing split %s of pair %s at '
                          'S=%d' % (r['section'], want, sp2['X'], S))
print('  anomalies=%d (0 = pattern holds on every row of this kit)'
      % anom)

n3 = sum(1 for r in rows for sp in r['separations'] if len(sp['X']) == 3)
n2 = sum(1 for r in rows for sp in r['separations'] if len(sp['X']) == 2)
print('  total pair seats measured: %d, total 3-token shadows: %d'
      % (n2, n3))
print('AUDIT DONE: A=%d B=%d C=%d' % (bad_a, bad_b, bad_c))
