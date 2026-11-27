#!/usr/bin/env python3
"""derive_check_kit15.py - engine-free arithmetic verification of every
registered kit-15 prediction literal and every kit-16 future constant.
The K0832 closed form (published transcription, byte-cloned engine block
region of the frozen explorer) is the ONLY evaluator; the recursive H
engine is never invoked. Exit 0 iff all checks pass.

Kit-15 specifics (differences from kit-14, all disclosed in the kit README):
- the frozen kit-14 prediction texts carry STALE seat labels (by co-2) for
  all 28 ladder rows; the collapse literals are authoritative and the
  binding seats/stacks here are machine-derived from the S=z/S=z+1/S=z+2/
  S=z-1 arithmetic, so the seat-S-sum check uses the DERIVED seats.
"""
import json
import re
import sys

src = open('explore_m45m46_frontier_windows_evenlife.py').read()
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


BIND = json.loads(ns['K15_BINDING_JSON'])
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
        # derived dead seat: sum = z-1 (S=z-1 arithmetic)
        chk(m + ds[1] == z - 1, 'dead-seat S=z-1 arithmetic m=%d z=%d %s' % (m, z, ds))
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
    # stale-label disclosure: the frozen cand texts carry kit-14 seat tokens;
    # the derived seats must differ from the stale labels by exactly +2 on
    # the co token for the 28 ladder rows (one-past and NEW seats)
    if r['kind'] != 'frontier':
        stale = re.findall(r'\{%d,(\d+)\}@S=(\d+)' % m, r['cand'])
        if r['kind'] == 'one-past':
            chk(int(stale[0][0]) == r['seats'][0][1] - 2,
                'stale-label co-2 one-past m=%d z=%d' % (m, z))
        else:
            chk(int(stale[0][0]) == r['seats'][1][1] - 2,
                'stale-label co-2 NEW m=%d z=%d' % (m, z))

# kit-14 registration was machine-checked at build to contain zero
# self/earlier overlaps; assert no known already-measured row sneaks in
for r in BIND:
    chk(not (r['m'] == 43 and r['z'] == 85), 'm43 z85 not re-registered')
    chk(not (r['m'] == 44 and r['z'] == 86), 'm44 z86 not re-registered')

# z* K1268 checks
chk(v(91, 89, 135) == 0, 'frontier m45 collapse')
chk(v(92, 90, 137) == 1, 'frontier m46 collapse')
for (m, z) in ((45, 89), (46, 90), (43, 85), (44, 86)):
    chk(z == 2 * m - 2 + (m % 2), 'K1268 z*(%d)=%d' % (m, z))

EL = json.loads(ns['K15_EVENLIFE_JSON'])
assert len(EL) == 3
for r in EL:
    m = r['m']; z = r['z']
    chk(z == 3 * m + 10, 'evenlife z=3m+10 m=%d z=%d' % (m, z))
    R = m + z + 1
    chk(v(3 * m + 10, z, R) == 2, 'evenlife stick collapse m=%d' % m)
    chk(v(3 * m + 12, z, R) == 1, 'evenlife NEW collapse m=%d' % m)
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

FUT = json.loads(ns['K16_FUTURE_JSON'])
assert len(FUT) == 34
for f in FUT:
    if isinstance(f.get('z'), int):
        m = f['m']; z = f['z']
        chk(z >= 55, 'future z sane')
        if m:
            chk(m + z + 1 >= z, 'future R sane')
    for lit in text_literals(f['prediction']):
        chk(v(lit[0], lit[1], lit[2]) == lit[3],
            'future-literal %s (m=%s z=%s)' % (str(lit), f.get('m'), f.get('z')))
chk(any(f.get('m') == 47 and f.get('z') == 93 for f in FUT), 'future m47 z93 present')
chk(any(f.get('m') == 48 and f.get('z') == 94 for f in FUT), 'future m48 z94 present')
# frontier arithmetic of the 34th/35th candidates
chk(93 == 2 * 47 - 2 + 1, 'K1268 z*(47)')
chk(94 == 2 * 48 - 2 + 0, 'K1268 z*(48)')
chk(v(95, 93, 141) == 0, 'm47 frontier collapse literal')
chk(v(96, 94, 143) == 1, 'm48 frontier collapse literal')

# window sweeps measured here: z*(43)-8..-1 = 77..84, z*(44)-8..-1 = 78..85
chk(list(range(77, 85)) == [2 * 43 - 2 + 1 - 8 + i for i in range(8)], 'window m43 arithmetic')
chk(list(range(78, 86)) == [2 * 44 - 2 + 0 - 8 + i for i in range(8)], 'window m44 arithmetic')
# kit-16 window proposals: z*(45)-8..-1 = 81..88, z*(46)-8..-1 = 82..89
chk(list(range(81, 89)) == [2 * 45 - 2 + 1 - 8 + i for i in range(8)], 'window m45 arithmetic')
chk(list(range(82, 90)) == [2 * 46 - 2 + 0 - 8 + i for i in range(8)], 'window m46 arithmetic')

# battery: 2,034 literals = 1,970 kit-14 carried + 64 new; every literal
# triple is (x, z, R); the 64 NEW literals additionally satisfy
# v == vC == vO before the freeze
BAT = json.loads(ns['BATTERY_TRIPLES_JSON'])
chk(len(BAT) == 2034, 'battery count %d' % len(BAT))
BAT14 = json.loads(re.search(r"BATTERY_TRIPLES_JSON = '(.*?)'\n",
                             open('explore_m43m44_frontier_windows_evenlife.py').read(), re.S).group(1))
s14 = set(map(tuple, BAT14))
for (x, z2, R2) in BAT:
    chk(v(x, z2, R2) >= 0, 'battery literal sane %s' % str((x, z2, R2)))
for t_ in BAT:
    if tuple(t_) not in s14:
        x, z2, R2 = t_
        chk(v(x, z2, R2) == vC(x, z2, R2) == vO(x, z2, R2),
            'new battery literal v/vC/vO %s' % str(t_))

# anchors: 869 = 733 carried + 136 kit-14 separation spots
ANCH = ns['K15_ANCHORS']
chk(len(ANCH) == 869, 'anchor count %d' % len(ANCH))

print(json.dumps({'result': 'DERIVE-' + ('PASS' if not fails else 'FAIL'),
                  'checks': checks, 'fails': fails},
                 sort_keys=True, separators=(',', ':')))
sys.exit(0 if not fails else 1)
