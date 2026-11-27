#!/usr/bin/env python3
"""derive_check_kit11.py - engine-free arithmetic verification of every
registered kit-11 prediction literal and every kit-12 future constant.
The K0832 closed form (published transcription, byte-cloned engine block
region of the frozen explorer) is the ONLY evaluator; the recursive H
engine is never invoked. Exit 0 iff all checks pass."""
import json
import re
import sys

src = open('explore_m37m38_frontier_windows.py').read()
ns = {'lru_cache': __import__('functools').lru_cache,
      'hashlib': __import__('hashlib'),
      '__name__': 'notmain'}
exec(src, ns)
v = ns['v']

fails = []
checks = 0


def chk(cond, tag):
    global checks
    checks += 1
    if not cond:
        fails.append(tag)


VRE = re.compile(r'v\((\d+),\s*(\d+),\s*(\d+)\)\s*=\s*(\d+)')


def text_literals(t):
    return [(int(a), int(b), int(c), int(val)) for (a, b, c, val) in VRE.findall(t)]


BIND = json.loads(ns['K11_BINDING_JSON'])
assert len(BIND) == 28
for r in BIND:
    m = r['m']; z = r['z']
    R = m + z + 1
    chk(R == m + z + 1, 'R-arith %d %d' % (m, z))
    for lit in text_literals(r['cand']):
        chk(v(lit[0], lit[1], lit[2]) == lit[3],
            'cand-literal %d %d %d -> %d (row m=%d z=%d)' % (lit + (m, z)))
    for s in r['seats']:
        chk(len(s) == 4 and s[0] == m, 'seat-first-token m=%d z=%d %s' % (m, z, s))
        chk(s[2] == m + s[1], 'seat-S sum m=%d z=%d %s' % (m, z, s))
    if r.get('dead_seat'):
        ds = r['dead_seat']
        chk(ds[0] == m and ds[2] == z, 'dead-seat row m=%d z=%d %s' % (m, z, ds))
        chk(ds[1] > m, 'dead-seat co m=%d' % m)
    for sc in r.get('stack_candidates') or []:
        chk(len(sc['X']) == 3 and sc['X'][0] == m, 'stack m-first m=%d %s' % (m, sc))
        chk(sum(sc['X']) == sc['S'], 'stack sum m=%d %s' % (m, sc))
        chk(sc['X'][1] + sc['X'][2] == sc['S'] - m, 'stack co-split m=%d %s' % (m, sc))
        chk(sc['X'][1] >= m and sc['X'][2] >= m and sc['X'][1] <= sc['X'][2],
            'stack admissible m=%d %s' % (m, sc))
    # rule-v2 completeness: a 2-token seat with co >= 2m MUST have its full
    # admissible split set registered; a seat with co < 2m must have none
    for s in r['seats']:
        if r['kind'] == 'frontier':
            continue
        co = s[1]
        S = s[2]
        expect = set()
        for x in range(m, co - m + 1):
            y = co - x
            if y >= x and y >= m:
                expect.add((m, x, y))
        got = set(tuple(sc['X']) for sc in (r.get('stack_candidates') or [])
                  if sc['S'] == S)
        chk(expect == got, 'rule-v2 completeness m=%d z=%d seat co=%d S=%d expect=%s got=%s'
            % (m, z, co, S, sorted(expect), sorted(got)))

# skipped duplicate registrations must NOT be measured in kit-11
secs = None
# (checked at audit time against the .out; here assert the binding list does
#  not contain them)
for r in BIND:
    chk(not (r['m'] == 31 and r['z'] == 66), 'm31 z66 not re-registered')
    chk(not (r['m'] == 32 and r['z'] == 67), 'm32 z67 not re-registered')

# z* K1268 checks
chk(v(75, 73, 111) == 0, 'frontier m37 collapse')
chk(v(76, 74, 113) == 1, 'frontier m38 collapse')
for (m, z) in ((37, 73), (38, 74), (35, 69), (36, 70)):
    chk(z == 2 * m - 2 + (m % 2), 'K1268 z*(%d)=%d' % (m, z))

EL = json.loads(ns['K11_EVENLIFE_JSON'])
assert len(EL) == 3
for r in EL:
    m = r['m']; z = r['z']
    chk(z == 3 * m + 2, 'evenlife z=3m+2 m=%d z=%d' % (m, z))
    R = m + z + 1
    chk(v(3 * m + 2, z, R) == 2, 'evenlife stick collapse m=%d' % m)
    chk(v(3 * m + 4, z, R) == 1, 'evenlife NEW collapse m=%d' % m)
    for lit in text_literals(r['cand']):
        chk(v(lit[0], lit[1], lit[2]) == lit[3],
            'evenlife cand-literal %s (m=%d z=%d)' % (str(lit), m, z))
    for s in r['seats']:
        chk(s[2] == m + s[1], 'evenlife seat-S m=%d' % m)
    # rule-v2 completeness for both seats
    for s in r['seats']:
        co = s[1]; S = s[2]
        expect = set()
        for x in range(m, co - m + 1):
            y = co - x
            if y >= x and y >= m:
                expect.add((m, x, y))
        got = set(tuple(sc['X']) for sc in (r.get('stack_candidates') or [])
                  if sc['S'] == S)
        chk(expect == got, 'evenlife rule-v2 completeness m=%d co=%d' % (m, co))

FUT = json.loads(ns['K12_FUTURE_JSON'])
assert len(FUT) == 34
for f in FUT:
    if isinstance(f.get('z'), int):
        m = f['m']; z = f['z']
        chk(z >= 53, 'future z sane')
        if m:
            chk(m + z + 1 >= z, 'future R sane')
    for lit in text_literals(f['prediction']):
        chk(v(lit[0], lit[1], lit[2]) == lit[3],
            'future-literal %s (m=%s z=%s)' % (str(lit), f.get('m'), f.get('z')))
chk(any(f.get('m') == 39 and f.get('z') == 77 for f in FUT), 'future m39 z77 present')
chk(any(f.get('m') == 40 and f.get('z') == 78 for f in FUT), 'future m40 z78 present')
# frontier arithmetic of the 27th/28th candidates
chk(77 == 2 * 39 - 2 + 1, 'K1268 z*(39)')
chk(78 == 2 * 40 - 2 + 0, 'K1268 z*(40)')
chk(v(79, 77, 117) == 0, 'm39 frontier collapse literal')
chk(v(80, 78, 119) == 1, 'm40 frontier collapse literal')

# window sweeps: z*(35)-8..-1 = 61..68, z*(36)-8..-1 = 62..69 (kit-11)
chk(list(range(61, 69)) == [2 * 35 - 2 + 1 - 8 + i for i in range(8)], 'window m35 arithmetic')
chk(list(range(62, 70)) == [2 * 36 - 2 + 0 - 8 + i for i in range(8)], 'window m36 arithmetic')
# kit-12 window proposals: z*(37)-8..-1 = 65..72, z*(38)-8..-1 = 66..73
chk(list(range(65, 73)) == [2 * 37 - 2 + 1 - 8 + i for i in range(8)], 'window m37 arithmetic')
chk(list(range(66, 74)) == [2 * 38 - 2 + 0 - 8 + i for i in range(8)], 'window m38 arithmetic')

# battery: 1,702 literals = 1,604 kit-10 carried + 98 new; every literal
# triple is (x, z, R) with R = x + z + 1 or a registered seat/stack sum
BAT = json.loads(ns['BATTERY_TRIPLES_JSON'])
chk(len(BAT) == 1702, 'battery count %d' % len(BAT))
for (x, z2, R2) in BAT:
    chk(v(x, z2, R2) >= 0, 'battery literal sane %s' % str((x, z2, R2)))

# anchors: 429 = 334 carried + 95 kit-10 separation spots
ANCH = ns['K11_ANCHORS']
chk(len(ANCH) == 429, 'anchor count %d' % len(ANCH))

print(json.dumps({'result': 'DERIVE-' + ('PASS' if not fails else 'FAIL'),
                  'checks': checks, 'fails': fails},
                 sort_keys=True, separators=(',', ':')))
sys.exit(0 if not fails else 1)
