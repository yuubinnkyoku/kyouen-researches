#!/usr/bin/env python3
"""kit-19x verification: check every measured kit-19x row against its
registered prediction (byte-verbatim from the public kit-18 .out future
constants). FULL HIT = every predicted seat separation present with exact
(X, S, direction, value, collapse); every predicted dead seat conforms;
every registered stack candidate present as an exact mimic; and ZERO
unregistered separations in the row (window rows: zero separations)."""
import json
import re
import sys

reg = json.load(open(sys.argv[1]))
chunks = sys.argv[2:-1]
outp = sys.argv[-1]
recs = []
for f in chunks:
    recs += json.load(open(f))
assert len(recs) == 49

results = []
all_ok = True


def row_by_sec(sec):
    for r in recs:
        if r['section'] == sec:
            return r
    raise KeyError(sec)


def find(seps, X, S):
    for sp in seps:
        if tuple(sp['X']) == tuple(sorted(X)) and sp['S'] == S:
            return sp
    return None


for item in reg:
    kind = item['kind']
    m = item.get('m')
    if kind in ('one-past', 'birth'):
        z = item['z']
        sec = 'ladder_m%d_z%d_row_record' % (m, z)
        r = row_by_sec(sec)
        seps = r['separations']
        t = item['prediction']
        ok = True
        findings = []
        used = set()
        # seats
        for pat, grp in [
            (r'\{(\d+),\s*(\d+)\}@S=(\d+)\s+(UP|DOWN)\s+(\d+)v(\d+)',
             lambda a: ([int(a[0]), int(a[1])], int(a[2]), a[3], int(a[4]), int(a[5]))),
        ]:
            for mo in re.finditer(pat, t):
                X, S, ud, hv, ev = grp(mo.groups())
                sp = find(seps, X, S)
                if sp is None:
                    ok = False
                    findings.append('MISSING seat %s@%d' % (X, S))
                elif not (sp['direction'] == ud and sp['value'] == hv and sp['collapse'] == ev):
                    ok = False
                    findings.append('seat %s@%d wrong: %s vs pred %s %dv%d' % (X, S, sp, ud, hv, ev))
                else:
                    used.add((tuple(sp['X']), sp['S']))
        # stick seat: "stick {m,c} DOWN a vb (collapse v(S,z,R)=ev)"
        mo = re.search(r'stick\s+\{(\d+),\s*(\d+)\}\s+DOWN\s+(\d+)v(\d+)', t)
        if mo:
            a, b, hv, ev = map(int, mo.groups())
            S = a + b
            sp = find(seps, [a, b], S)
            if sp is None or sp['direction'] != 'DOWN' or sp['value'] != hv or sp['collapse'] != ev:
                ok = False
                findings.append('stick seat mismatch %s,%s: %s' % (a, b, sp))
            else:
                used.add((tuple(sp['X']), sp['S']))
        # dead seat
        mo = re.search(r'\{(\d+),\s*(\d+)\}\s+conform-DEAD', t)
        if mo:
            a, b = map(int, mo.groups())
            sp = find(seps, [a, b], a + b)
            if sp is not None:
                ok = False
                findings.append('DEAD seat %s,%s separated' % (a, b))
        # stack candidates: every {a,b,c} triple and the seats already used;
        # stacks must mimic their target seat (same direction and value).
        stack_triples = re.findall(r'\{(\d+),\s*(\d+),\s*(\d+)\}', t)
        # figure the two target (direction, value) levels from seats
        levels = set((sp['direction'], sp['value']) for (X, S) in used
                      for sp in [find(seps, list(X), S)] if sp)
        for (a, b, c) in stack_triples:
            X = sorted([int(a), int(b), int(c)])
            S = sum(X)
            sp = find(seps, X, S)
            if sp is None:
                ok = False
                findings.append('MISSING stack shadow %s@%d' % (X, S))
            elif (sp['direction'], sp['value']) not in levels:
                ok = False
                findings.append('stack shadow %s@%d not a mimic: %s' % (X, S, sp))
            else:
                used.add((tuple(sp['X']), sp['S']))
        # zero unregistered separations; the frozen one-past texts omit the
        # rule-v2 stack lists, so accept exactly the admissible rule-v2
        # co-splits of the one-past seat (standing rule v2: co >= 2m,
        # both split tokens >= m, exact mimic of the seat) and count them.
        seat = None
        if kind == 'one-past':
            mo2 = re.search(r'\{(%d),\s*(\d+)\}@S=(\d+)' % m, t)
            if mo2:
                co = int(mo2.group(2))
                Sz = int(mo2.group(3))
                sp_seat = find(seps, [m, co], Sz)
                if sp_seat:
                    seat = sp_seat
                    r2 = set()
                    for a in range(m, co // 2 + 1):
                        b = co - a
                        if b >= a >= m:
                            r2.add((tuple(sorted([m, a, b])), Sz))
                    for key in r2:
                        if key in used:
                            continue
                        spx = find(seps, list(key[0]), key[1])
                        if spx is None:
                            ok = False
                            findings.append('MISSING rule-v2 shadow %s@%d' % (list(key[0]), key[1]))
                        elif not (spx['direction'] == seat['direction'] and spx['value'] == seat['value'] and spx['collapse'] == seat['collapse']):
                            ok = False
                            findings.append('rule-v2 shadow not exact mimic: %s' % spx)
                        else:
                            used.add(key)
                            findings.append('rule-v2 shadow (not listed in frozen one-past text): %s' % spx)
        for sp in seps:
            if (tuple(sp['X']), sp['S']) not in used:
                ok = False
                findings.append('UNREGISTERED separation %s' % sp)
        results.append({'section': sec, 'ok': ok, 'n_seps': len(seps),
                        'findings': findings})
        all_ok = all_ok and ok
    elif kind.startswith('frontier'):
        z = item['z']
        sec = 'frontier_m%d_z%d_row_record' % (m, z)
        r = row_by_sec(sec)
        seps = r['separations']
        t = item['prediction']
        mo = re.search(r'[{(]?(\d+),\s*(\d+)[)}]?@S=(\d+)\s+(UP|DOWN)\s+(\d+)v(\d+)', t)
        a, b, S, ud, hv, ev = int(mo.group(1)), int(mo.group(2)), int(mo.group(3)), mo.group(4), int(mo.group(5)), int(mo.group(6))
        ok = True
        findings = []
        if len(seps) != 1:
            ok = False
            findings.append('row has %d separations, EXACTLY ONE registered' % len(seps))
        sp = find(seps, [a, b], S)
        if sp is None or sp['direction'] != ud or sp['value'] != hv or sp['collapse'] != ev:
            ok = False
            findings.append('frontier seat mismatch: %s vs %s %dv%d' % (sp, ud, hv, ev))
        results.append({'section': sec, 'ok': ok, 'n_seps': len(seps),
                        'findings': findings})
        all_ok = all_ok and ok
    elif kind.startswith('in-band window'):
        zlo, zhi = item['z'].split('..')
        for z in range(int(zlo), int(zhi) + 1):
            sec = 'inband_m%d_z%d_row_record' % (m, z)
            r = row_by_sec(sec)
            ok = len(r['separations']) == 0
            findings = [] if ok else ['%d separations' % len(r['separations'])]
            results.append({'section': sec, 'ok': ok, 'n_seps': len(r['separations']),
                            'findings': findings})
            all_ok = all_ok and ok

# evenlife rows: NON-BINDING template check (any deviation is the datum)
for m in (14, 16, 18):
    z = 3 * m + 18
    sec = 'evenlife_m%d_z%d_row_record' % (m, z)
    r = row_by_sec(sec)
    seps = r['separations']
    findings = []
    stick = find(seps, [m, 2 * m + 18], z + 3 * 0 + 0)  # S = m + (2m+18) = 3m+18 = z
    new = find(seps, [m, 2 * m + 20], z + 2)
    tmpl_stick = stick is not None and stick['direction'] == 'DOWN' and stick['value'] == 0 and stick['collapse'] == 2
    tmpl_new = new is not None and new['direction'] == 'UP' and new['value'] == 2 and new['collapse'] == 1
    findings.append('stick {m,2m+18}@S=z present=%s %s' % (stick is not None, stick))
    findings.append('NEW {m,2m+20}@S=z+2 present=%s %s' % (new is not None, new))
    results.append({'section': sec, 'ok': True, 'n_seps': len(seps),
                    'template_stick_match': tmpl_stick,
                    'template_new_match': tmpl_new,
                    'binding': False, 'findings': findings})

n_ok = sum(1 for x in results if x['ok'])
n_binding = sum(1 for x in results if x['section'].startswith(('ladder_', 'frontier_', 'inband_')))
out = {'result': 'VERIFY-' + ('PASS' if all_ok else 'FAIL'),
       'binding_rows': n_binding, 'binding_ok': n_ok,
       'rows': results,
       'total_seps': sum(len(r['separations']) for r in recs)}
json.dump(out, open(outp, 'w'), indent=1, sort_keys=True)
print(json.dumps({'result': out['result'], 'binding_ok': n_ok,
                  'total_seps': out['total_seps']}))
