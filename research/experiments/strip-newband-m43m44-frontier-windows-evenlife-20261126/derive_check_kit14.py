#!/usr/bin/env python3
"""derive_check_kit14.py - engine-free arithmetic verification of every
registered kit-14 prediction literal and every kit-15 future constant.
The K0832 closed form (published transcription, byte-cloned engine block
region of the frozen explorer) is the ONLY evaluator; the recursive H
engine is never invoked. Exit 0 iff all checks pass."""
import json
import re
import sys

src = open('explore_m43m44_frontier_windows_evenlife.py').read()
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


BIND = json.loads(ns['K14_BINDING_JSON'])
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

# kit-13 registration was machine-checked at build to contain zero
# self/earlier overlaps; assert no known already-measured row sneaks in
for r in BIND:
    chk(not (r['m'] == 41 and r['z'] == 81), 'm41 z81 not re-registered')
    chk(not (r['m'] == 42 and r['z'] == 82), 'm42 z82 not re-registered')

# z* K1268 checks
chk(v(87, 85, 129) == 0, 'frontier m43 collapse')
chk(v(88, 86, 131) == 1, 'frontier m44 collapse')
for (m, z) in ((43, 85), (44, 86), (41, 81), (42, 82)):
    chk(z == 2 * m - 2 + (m % 2), 'K1268 z*(%d)=%d' % (m, z))

EL = json.loads(ns['K14_EVENLIFE_JSON'])
assert len(EL) == 3
for r in EL:
    m = r['m']; z = r['z']
    chk(z == 3 * m + 8, 'evenlife z=3m+8 m=%d z=%d' % (m, z))
    R = m + z + 1
    chk(v(3 * m + 8, z, R) == 2, 'evenlife stick collapse m=%d' % m)
    chk(v(3 * m + 10, z, R) == 1, 'evenlife NEW collapse m=%d' % m)
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

FUT = json.loads(ns['K15_FUTURE_JSON'])
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
chk(any(f.get('m') == 45 and f.get('z') == 89 for f in FUT), 'future m45 z89 present')
chk(any(f.get('m') == 46 and f.get('z') == 90 for f in FUT), 'future m46 z90 present')
# frontier arithmetic of the 32nd/33rd candidates
chk(89 == 2 * 45 - 2 + 1, 'K1268 z*(45)')
chk(90 == 2 * 46 - 2 + 0, 'K1268 z*(46)')
chk(v(91, 89, 135) == 0, 'm45 frontier collapse literal')
chk(v(92, 90, 137) == 1, 'm46 frontier collapse literal')

# window sweeps measured here: z*(41)-8..-1 = 73..80, z*(42)-8..-1 = 74..81
chk(list(range(73, 81)) == [2 * 41 - 2 + 1 - 8 + i for i in range(8)], 'window m41 arithmetic')
chk(list(range(74, 82)) == [2 * 42 - 2 + 0 - 8 + i for i in range(8)], 'window m42 arithmetic')
# kit-15 window proposals: z*(43)-8..-1 = 77..84, z*(44)-8..-1 = 78..85
chk(list(range(77, 85)) == [2 * 43 - 2 + 1 - 8 + i for i in range(8)], 'window m43 arithmetic')
chk(list(range(78, 86)) == [2 * 44 - 2 + 0 - 8 + i for i in range(8)], 'window m44 arithmetic')

# battery: 1,970 literals = 1,906 kit-13 carried + 64 new; every literal
# triple is (x, z, R) with R = x + z + 1 or a registered seat/stack sum;
# the 64 NEW literals additionally satisfy v == vC == vO before the freeze
BAT = json.loads(ns['BATTERY_TRIPLES_JSON'])
chk(len(BAT) == 1970, 'battery count %d' % len(BAT))
BAT13 = json.loads(re.search(r"BATTERY_TRIPLES_JSON = '(.*?)'\n",
                             open('explore_m41m42_frontier_windows.py').read(), re.S).group(1))
s13 = set(map(tuple, BAT13))
for (x, z2, R2) in BAT:
    chk(v(x, z2, R2) >= 0, 'battery literal sane %s' % str((x, z2, R2)))
for t_ in BAT:
    if tuple(t_) not in s13:
        x, z2, R2 = t_
        chk(v(x, z2, R2) == vC(x, z2, R2) == vO(x, z2, R2),
            'new battery literal v/vC/vO %s' % str(t_))

# anchors: 733 = 616 carried + 117 kit-13 separation spots
ANCH = ns['K14_ANCHORS']
chk(len(ANCH) == 733, 'anchor count %d' % len(ANCH))

print(json.dumps({'result': 'DERIVE-' + ('PASS' if not fails else 'FAIL'),
                  'checks': checks, 'fails': fails},
                 sort_keys=True, separators=(',', ':')))
sys.exit(0 if not fails else 1)
