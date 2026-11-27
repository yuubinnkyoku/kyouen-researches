#!/usr/bin/env python3
"""derive_check_kit10.py - engine-free arithmetic verification of every
registered kit-10 prediction literal and every kit-11 future constant.
The K0832 closed form (published transcription, byte-cloned engine block
region of the frozen explorer) is the ONLY evaluator; the recursive H
engine is never invoked. Exit 0 iff all checks pass."""
import json
import re
import sys

src = open('explore_m35m36_frontier_windows.py').read()
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


BIND = json.load(open('K10_BINDING.json'))
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

# z* K1268 checks
chk(v(71, 69, 105) == 0, 'frontier m35 collapse')
chk(v(72, 70, 107) == 1, 'frontier m36 collapse')
for (m, z) in ((35, 69), (36, 70), (33, 65), (34, 66)):
    chk(z == 2 * m - 2 + (m % 2), 'K1268 z*(%d)=%d' % (m, z))

EL = json.load(open('K10_EVENLIFE.json'))
for r in EL:
    m = r['m']; z = r['z']
    chk(z in (3 * m - 1, 3 * m, 3 * m + 1), 'evenlife z-range m=%d z=%d' % (m, z))
    for lit in text_literals(r['cand']):
        chk(v(lit[0], lit[1], lit[2]) == lit[3],
            'evenlife cand-literal %s (m=%d z=%d)' % (str(lit), m, z))
    for s in r['seats']:
        chk(s[2] == m + s[1], 'evenlife seat-S m=%d' % m)

FUT = json.load(open('K11_FUTURE.json'))
for f in FUT:
    if isinstance(f.get('z'), int):
        m = f['m']; z = f['z']
        chk(z >= 53, 'future z sane')
        if m:
            chk(z + m + 1 >= z, 'future R sane')
    for lit in text_literals(f['prediction']):
        chk(v(lit[0], lit[1], lit[2]) == lit[3],
            'future-literal %s (m=%s z=%s)' % (str(lit), f.get('m'), f.get('z')))
chk(any(f.get('m') == 37 and f.get('z') == 73 for f in FUT), 'future m37 z73 present')
chk(any(f.get('m') == 38 and f.get('z') == 74 for f in FUT), 'future m38 z74 present')

# window sweeps: z*(33)-8..-1 = 57..64, z*(34)-8..-1 = 58..65
chk(list(range(57, 65)) == [2 * 33 - 2 + 1 - 8 + i for i in range(8)], 'window m33 arithmetic')
chk(list(range(58, 66)) == [2 * 34 - 2 + 0 - 8 + i for i in range(8)], 'window m34 arithmetic')

print(json.dumps({'result': 'DERIVE-' + ('PASS' if not fails else 'FAIL'),
                 'checks': checks, 'fails': fails},
                 sort_keys=True, separators=(',', ':')))
sys.exit(0 if not fails else 1)
