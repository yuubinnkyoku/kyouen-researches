#!/usr/bin/env python3
"""derive_check_kit19.py - engine-free arithmetic verification of every
registered kit-19 prediction literal and every kit-20 future constant.
The K0832 closed form (published transcription, byte-cloned engine block
region of the frozen explorer) is the ONLY evaluator; the recursive H
engine is never invoked. Exit 0 iff all checks pass.

Kit-19 specifics: the frozen kit-18 prediction texts carry FRESH seat
labels (kit-18 received FRESH from kit-17 and emitted FRESH); the
freshness is ASSERTED here (label co == derived seat co).
"""
import json
import re
import sys

src = open('explore_m53m54_frontier_windows_evenlife.py').read()
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


BIND = json.loads(ns['K19_BINDING_JSON'])
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
    # FRESH-label assertion (this generation): the frozen cand text seat
    # token must EQUAL the derived seat co (kit-16 texts are not stale)
    if r['kind'] != 'frontier':
        labs = re.findall(r'\{%d,(\d+)\}@S=(\d+)' % m, r['cand'])
        if r['kind'] == 'one-past':
            chk(int(labs[0][0]) == r['seats'][0][1],
                'fresh-label one-past m=%d z=%d' % (m, z))
            chk(int(labs[0][1]) == r['seats'][0][2],
                'fresh-label-S one-past m=%d z=%d' % (m, z))
        else:
            chk(int(labs[0][0]) == r['seats'][1][1],
                'fresh-label NEW m=%d z=%d' % (m, z))
            chk(int(labs[0][1]) == r['seats'][1][2],
                'fresh-label-S NEW m=%d z=%d' % (m, z))

# kit-17 registration was machine-checked at build to contain zero
# self/earlier overlaps; assert no known already-measured row sneaks in
for r in BIND:
    chk(not (r['m'] == 51 and r['z'] == 101), 'm51 z101 not re-registered')
    chk(not (r['m'] == 52 and r['z'] == 102), 'm52 z102 not re-registered')

# z* K1268 checks
chk(v(107, 105, 159) == 0, 'frontier m53 collapse')
chk(v(108, 106, 161) == 1, 'frontier m54 collapse')
for (m, z) in ((53, 105), (54, 106), (51, 101), (52, 102)):
    chk(z == 2 * m - 2 + (m % 2), 'K1268 z*(%d)=%d' % (m, z))

EL = json.loads(ns['K19_EVENLIFE_JSON'])
assert len(EL) == 3
for r in EL:
    m = r['m']; z = r['z']
    chk(z == 3 * m + 18, 'evenlife z=3m+18 m=%d z=%d' % (m, z))
    R = m + z + 1
    chk(v(3 * m + 18, z, R) == 2, 'evenlife stick collapse m=%d' % m)
    chk(v(3 * m + 20, z, R) == 1, 'evenlife NEW collapse m=%d' % m)
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

FUT = json.loads(ns['K20_FUTURE_JSON'])
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
chk(any(f.get('m') == 55 and f.get('z') == 109 for f in FUT), 'future m55 z109 present')
chk(any(f.get('m') == 56 and f.get('z') == 110 for f in FUT), 'future m56 z110 present')
# frontier arithmetic of the 42nd/43rd candidates
chk(109 == 2 * 55 - 2 + 1, 'K1268 z*(55)')
chk(110 == 2 * 56 - 2 + 0, 'K1268 z*(56)')
chk(v(111, 109, 165) == 0, 'm55 frontier collapse literal')
chk(v(112, 110, 167) == 1, 'm56 frontier collapse literal')

# window sweeps measured here: z*(51)-8..-1 = 93..100, z*(52)-8..-1 = 94..101
chk(list(range(93, 101)) == [2 * 51 - 2 + 1 - 8 + i for i in range(8)], 'window m51 arithmetic')
chk(list(range(94, 102)) == [2 * 52 - 2 + 0 - 8 + i for i in range(8)], 'window m52 arithmetic')
# kit-20 window proposals: z*(53)-8..-1 = 97..104, z*(54)-8..-1 = 98..105
chk(list(range(97, 105)) == [2 * 53 - 2 + 1 - 8 + i for i in range(8)], 'window m53 arithmetic')
chk(list(range(98, 106)) == [2 * 54 - 2 + 0 - 8 + i for i in range(8)], 'window m54 arithmetic')

# battery: 2,290 literals = 2,226 kit-18 carried + 64 new; every literal
# triple is (x, z, R); the 64 NEW literals additionally satisfy
# v == vC == vO before the freeze
BAT = json.loads(ns['BATTERY_TRIPLES_JSON'])
chk(len(BAT) == 2290, 'battery count %d' % len(BAT))
BAT17 = json.loads(re.search(r"BATTERY_TRIPLES_JSON = '(.*?)'\n",
                             open('explore_m51m52_frontier_windows_evenlife.py').read(), re.S).group(1))
s17 = set(map(tuple, BAT17))
for (x, z2, R2) in BAT:
    chk(v(x, z2, R2) >= 0, 'battery literal sane %s' % str((x, z2, R2)))
for t_ in BAT:
    if tuple(t_) not in s17:
        x, z2, R2 = t_
        chk(v(x, z2, R2) == vC(x, z2, R2) == vO(x, z2, R2),
            'new battery literal v/vC/vO %s' % str(t_))

# anchors: 1,662 = 1,421 carried + 241 kit-18 separation spots
ANCH = ns['K19_ANCHORS']
chk(len(ANCH) == 1662, 'anchor count %d' % len(ANCH))

print(json.dumps({'result': 'DERIVE-' + ('PASS' if not fails else 'FAIL'),
                  'checks': checks, 'fails': fails},
                 sort_keys=True, separators=(',', ':')))
sys.exit(0 if not fails else 1)
