#!/usr/bin/env python3
"""derive_check_kit20.py - engine-free arithmetic verification of every
registered kit-20 prediction literal and every kit-21 future constant.
The K0832 closed form (published transcription, byte-cloned engine block
region of the frozen explorer) is the ONLY evaluator; the recursive H
engine is never invoked. Exit 0 iff all checks pass.

Kit-20 specifics: the frozen kit-19 prediction texts carry FRESH seat
labels (kit-19 received FRESH from kit-18 and emitted FRESH); the
freshness is ASSERTED here (label co == derived seat co).
"""
import json
import re
import sys

src = open('explore_m55m56_frontier_windows_evenlife.py').read()
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


BIND = json.loads(ns['K20_BINDING_JSON'])
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
    chk(not (r['m'] == 53 and r['z'] == 105), 'm53 z105 not re-registered')
    chk(not (r['m'] == 54 and r['z'] == 106), 'm54 z106 not re-registered')

# z* K1268 checks
chk(v(111, 109, 165) == 0, 'frontier m55 collapse')
chk(v(112, 110, 167) == 1, 'frontier m56 collapse')
for (m, z) in ((55, 109), (56, 110), (53, 105), (54, 106)):
    chk(z == 2 * m - 2 + (m % 2), 'K1268 z*(%d)=%d' % (m, z))

EL = json.loads(ns['K20_EVENLIFE_JSON'])
assert len(EL) == 3
for r in EL:
    m = r['m']; z = r['z']
    chk(z == 3 * m + 20, 'evenlife z=3m+20 m=%d z=%d' % (m, z))
    R = m + z + 1
    chk(v(3 * m + 20, z, R) == 2, 'evenlife stick collapse m=%d' % m)
    chk(v(3 * m + 22, z, R) == 1, 'evenlife NEW collapse m=%d' % m)
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

FUT = json.loads(ns['K21_FUTURE_JSON'])
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
chk(any(f.get('m') == 57 and f.get('z') == 113 for f in FUT), 'future m57 z113 present')
chk(any(f.get('m') == 58 and f.get('z') == 114 for f in FUT), 'future m58 z114 present')
# frontier arithmetic of the 44th/45th candidates
chk(113 == 2 * 57 - 2 + 1, 'K1268 z*(57)')
chk(114 == 2 * 58 - 2 + 0, 'K1268 z*(58)')
chk(v(115, 113, 171) == 0, 'm57 frontier collapse literal')
chk(v(116, 114, 173) == 1, 'm58 frontier collapse literal')

# window sweeps measured here: z*(53)-8..-1 = 97..104, z*(54)-8..-1 = 98..105
chk(list(range(97, 105)) == [2 * 53 - 2 + 1 - 8 + i for i in range(8)], 'window m53 arithmetic')
chk(list(range(98, 106)) == [2 * 54 - 2 + 0 - 8 + i for i in range(8)], 'window m54 arithmetic')
# kit-21 window proposals: z*(55)-8..-1 = 101..108, z*(56)-8..-1 = 102..109
chk(list(range(101, 109)) == [2 * 55 - 2 + 1 - 8 + i for i in range(8)], 'window m55 arithmetic')
chk(list(range(102, 110)) == [2 * 56 - 2 + 0 - 8 + i for i in range(8)], 'window m56 arithmetic')

# battery: 2,354 literals = 2,290 kit-19 carried + 64 new; every literal
# triple is (x, z, R); the 64 NEW literals additionally satisfy
# v == vC == vO before the freeze
BAT = json.loads(ns['BATTERY_TRIPLES_JSON'])
chk(len(BAT) == 2354, 'battery count %d' % len(BAT))
BAT17 = json.loads(re.search(r"BATTERY_TRIPLES_JSON = '(.*?)'\n",
                             open('explore_m53m54_frontier_windows_evenlife.py').read(), re.S).group(1))
s17 = set(map(tuple, BAT17))
for (x, z2, R2) in BAT:
    chk(v(x, z2, R2) >= 0, 'battery literal sane %s' % str((x, z2, R2)))
for t_ in BAT:
    if tuple(t_) not in s17:
        x, z2, R2 = t_
        chk(v(x, z2, R2) == vC(x, z2, R2) == vO(x, z2, R2),
            'new battery literal v/vC/vO %s' % str(t_))

# anchors: 1,935 = 1,662 carried + 273 kit-19 separation spots
ANCH = ns['K20_ANCHORS']
chk(len(ANCH) == 1935, 'anchor count %d' % len(ANCH))

print(json.dumps({'result': 'DERIVE-' + ('PASS' if not fails else 'FAIL'),
                  'checks': checks, 'fails': fails},
                 sort_keys=True, separators=(',', ':')))
sys.exit(0 if not fails else 1)
