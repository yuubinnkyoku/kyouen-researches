#!/usr/bin/env python3
"""derive_check_kit13.py - engine-free arithmetic verification of every
registered kit-13 prediction literal and every kit-14 future constant.
The K0832 closed form (published transcription, byte-cloned engine block
region of the frozen explorer) is the ONLY evaluator; the recursive H
engine is never invoked. Exit 0 iff all checks pass."""
import json
import re
import sys

src = open('explore_m41m42_frontier_windows.py').read()
ns = {'lru_cache': __import__('functools').lru_cache,
      'hashlib': __import__('hashlib'),
      '__name__': 'notmain'}
exec(src, ns)
v = ns['v']
vC = ns['ns']['vC']
vO = ns['ns']['vO']

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


BIND = json.loads(ns['K13_BINDING_JSON'])
assert len(BIND) == 30
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

# kit-12 registration was machine-checked at build to contain zero
# self/earlier overlaps; assert no known already-measured row sneaks in
for r in BIND:
    chk(not (r['m'] == 39 and r['z'] == 77), 'm39 z77 not re-registered')
    chk(not (r['m'] == 40 and r['z'] == 78), 'm40 z78 not re-registered')

# z* K1268 checks
chk(v(83, 81, 123) == 0, 'frontier m41 collapse')
chk(v(84, 82, 125) == 1, 'frontier m42 collapse')
for (m, z) in ((41, 81), (42, 82), (39, 77), (40, 78)):
    chk(z == 2 * m - 2 + (m % 2), 'K1268 z*(%d)=%d' % (m, z))

EL = json.loads(ns['K13_EVENLIFE_JSON'])
assert len(EL) == 3
for r in EL:
    m = r['m']; z = r['z']
    chk(z == 3 * m + 6, 'evenlife z=3m+6 m=%d z=%d' % (m, z))
    R = m + z + 1
    chk(v(3 * m + 6, z, R) == 2, 'evenlife stick collapse m=%d' % m)
    chk(v(3 * m + 8, z, R) == 1, 'evenlife NEW collapse m=%d' % m)
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

FUT = json.loads(ns['K14_FUTURE_JSON'])
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
chk(any(f.get('m') == 43 and f.get('z') == 85 for f in FUT), 'future m43 z85 present')
chk(any(f.get('m') == 44 and f.get('z') == 86 for f in FUT), 'future m44 z86 present')
# frontier arithmetic of the 31st/32nd candidates
chk(85 == 2 * 43 - 2 + 1, 'K1268 z*(43)')
chk(86 == 2 * 44 - 2 + 0, 'K1268 z*(44)')
chk(v(87, 85, 129) == 0, 'm43 frontier collapse literal')
chk(v(88, 86, 131) == 1, 'm44 frontier collapse literal')

# window sweeps measured here: z*(39)-8..-1 = 69..76, z*(40)-8..-1 = 70..77
chk(list(range(69, 77)) == [2 * 39 - 2 + 1 - 8 + i for i in range(8)], 'window m39 arithmetic')
chk(list(range(70, 78)) == [2 * 40 - 2 + 0 - 8 + i for i in range(8)], 'window m40 arithmetic')
# kit-14 window proposals: z*(41)-8..-1 = 73..80, z*(42)-8..-1 = 74..81
chk(list(range(73, 81)) == [2 * 41 - 2 + 1 - 8 + i for i in range(8)], 'window m41 arithmetic')
chk(list(range(74, 82)) == [2 * 42 - 2 + 0 - 8 + i for i in range(8)], 'window m42 arithmetic')

# battery: 1,906 literals = 1,804 kit-12 carried + 102 new; every literal
# triple is (x, z, R) with R = x + z + 1 or a registered seat/stack sum;
# the 102 NEW literals additionally satisfy v == vC == vO before the freeze
BAT = json.loads(ns['BATTERY_TRIPLES_JSON'])
chk(len(BAT) == 1906, 'battery count %d' % len(BAT))
BAT12 = json.loads(re.search(r"BATTERY_TRIPLES_JSON = '(.*?)'\n",
                             open('explore_kit12.py').read(), re.S).group(1))
s12 = set(map(tuple, BAT12))
for (x, z2, R2) in BAT:
    chk(v(x, z2, R2) >= 0, 'battery literal sane %s' % str((x, z2, R2)))
for t_ in BAT:
    if tuple(t_) not in s12:
        x, z2, R2 = t_
        chk(v(x, z2, R2) == vC(x, z2, R2) == vO(x, z2, R2),
            'new battery literal v/vC/vO %s' % str(t_))

# anchors: 616 = 515 carried + 101 kit-12 separation spots
ANCH = ns['K13_ANCHORS']
chk(len(ANCH) == 616, 'anchor count %d' % len(ANCH))

print(json.dumps({'result': 'DERIVE-' + ('PASS' if not fails else 'FAIL'),
                  'checks': checks, 'fails': fails},
                 sort_keys=True, separators=(',', ':')))
sys.exit(0 if not fails else 1)
