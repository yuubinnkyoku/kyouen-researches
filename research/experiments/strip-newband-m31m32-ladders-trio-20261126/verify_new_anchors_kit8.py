#!/usr/bin/env python3
"""verify_new_anchors_kit8.py: PRE-FREEZE anchor verification, run BEFORE
the first run of explore_m31m32_ladders_trio.py.
 - Recomputes the 39 kit-7 separation spots (38 named seats + the
   stacked-trio deviation seat) with the published canonical engine
   (ENGINE_BLOCK byte-pinned bd5f22e4) and asserts value equality with
   the kit-7 published frozen .out values (extracted machine-side).
 - Asserts the anchor_spec table embedded in the kit-8 explorer is a
   byte-superset of the kit-7 explorer's 141-entry anchor_spec block
   (the first 141 entries byte-identical, plus exactly 39 new entries).
"""
import json, hashlib
from functools import lru_cache

src_k8 = open('explore_m31m32_ladders_trio.py').read()
src_k7 = open('explore_kit7.py').read()

def block(src, start_marker, end_marker):
    i = src.index(start_marker)
    j = src.index(end_marker, i)
    return src[i:j]

# 1) anchor table byte-fidelity
blk7 = block(src_k7, '    anchor_spec = [', '    # (a) K0832 battery')
blk8 = block(src_k8, '    anchor_spec = [', '    # (a) K0832 battery')
entries7 = blk7[blk7.index('[') + 1:blk7.rindex(']')]
entries8 = blk8[blk8.index('[') + 1:blk8.rindex(']')]
lines7 = [l for l in entries7.splitlines() if l.strip().startswith('(')]
lines8 = [l for l in entries8.splitlines() if l.strip().startswith('(')]
assert len(lines7) == 141, len(lines7)
assert lines8[:141] == lines7, 'first 141 anchor entries not byte-identical'
assert len(lines8) == 180, len(lines8)
print('anchor table: 141 byte-identical inherited + 39 new =', len(lines8))

# 2) engine re-measurement of the 39 kit-7 spots
ENG = block(src_k8, "ENGINE_BLOCK = '''", "'''\n")
content = ENG[18:]
assert hashlib.sha256(content.encode()).hexdigest() == \
    'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
ns = {'lru_cache': lru_cache}
exec(content, ns)
H = ns['H_canonical']

seps = json.load(open('kit7_seps.json'))
assert len(seps) == 39
bad = 0
for s in seps:
    XX = tuple(sorted(s['X'], reverse=True))
    hv = H(s['R'], XX, s['z'])
    ok = hv == s['value']
    if not ok:
        bad += 1
        print('MISMATCH', s)
print('kit-7 separation spots re-measured: %d/%d exact' % (39 - bad, 39))
assert bad == 0

# 3) the new 39 anchors embedded in the explorer reproduce the same values
import re
newblock = '\n'.join(lines8[141:])
embedded = re.findall(r'\((\d+), \(([\d, ]+)\), (\d+), (\d+),', newblock)
assert len(embedded) == 39, len(embedded)
bad2 = 0
pub = {(s['R'], tuple(sorted(s['X'], reverse=True)), s['z']): s['value'] for s in seps}
for (R, Xs, z, val) in embedded:
    XX = tuple(int(t) for t in Xs.split(','))
    key = (int(R), XX, int(z))
    if pub.get(key) != int(val):
        bad2 += 1
        print('EMBED MISMATCH', key, val, pub.get(key))
print('new-anchor table transcription: %d/%d exact' % (39 - bad2, 39))
assert bad2 == 0
print('PRE-FREEZE ANCHOR VERIFICATION: ALL PASS')
