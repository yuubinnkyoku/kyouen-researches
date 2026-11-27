#!/usr/bin/env python3
"""verify_new_anchors_kit9.py: PRE-FREEZE anchor verification, run BEFORE
the first run of explore_m33m34_frontier_ladders.py.
 - Recomputes the 54 kit-8 separation spots (the publish-priority kit-8
   census 7af915fb, all 48 rows) with the published canonical engine
   (ENGINE_BLOCK byte-pinned bd5f22e4) and asserts value equality with
   the kit-8 published frozen .out values (extracted machine-side).
 - Asserts the anchor_spec table embedded in the kit-9 explorer is a
   byte-superset of the kit-8 explorer's 180-entry anchor_spec block
   (the first 180 entries byte-identical, plus exactly 54 new entries).
"""
import json, hashlib, re
from functools import lru_cache

src_k9 = open('explore_m33m34_frontier_ladders.py').read()
src_k8 = open('/home/user/tool-results/kit9build/k8pub/explore_m31m32_ladders_trio.py').read()

def block(src, start_marker, end_marker):
    i = src.index(start_marker)
    j = src.index(end_marker, i)
    return src[i:j]

# 1) anchor table byte-fidelity
blk8 = block(src_k8, '    anchor_spec = [', '    # (a) K0832 battery')
blk9 = block(src_k9, '    anchor_spec = [', '    # (a) K0832 battery')
entries8 = blk8[blk8.index('[') + 1:blk8.rindex(']')]
entries9 = blk9[blk9.index('[') + 1:blk9.rindex(']')]
lines8 = [l for l in entries8.splitlines() if l.strip().startswith('(')]
lines9 = [l for l in entries9.splitlines() if l.strip().startswith('(')]
assert len(lines8) == 180, len(lines8)
assert lines9[:180] == lines8, 'first 180 anchor entries not byte-identical'
assert len(lines9) == 234, len(lines9)
print('anchor table: 180 byte-identical inherited + 54 new =', len(lines9))

# 2) engine re-measurement of the 54 kit-8 spots
i = src_k9.index("ENGINE_BLOCK = '''")
j = src_k9.index("'''", i + 18)
content = src_k9[i + 18:j]
assert hashlib.sha256(content.encode()).hexdigest() == \
    'bd5f22e415a78368c9b798296bc84948d5637decbf3c21a92404d45fb12e3a92'
ns = {'lru_cache': lru_cache}
exec(content, ns)
H = ns['H_canonical']

seps = json.load(open('kit8_seps.json'))
assert len(seps) == 54
bad = 0
for s in seps:
    XX = tuple(sorted(s['X'], reverse=True))
    hv = H(s['R'], XX, s['z'])
    ok = hv == s['value']
    if not ok:
        bad += 1
        print('MISMATCH', s)
print('kit-8 separation spots re-measured: %d/%d exact' % (54 - bad, 54))
assert bad == 0

# 3) the new 54 anchors embedded in the explorer reproduce the same values
newblock = '\n'.join(lines9[180:])
embedded = re.findall(r'\((\d+), \(([\d, ]+)\), (\d+), (\d+),', newblock)
assert len(embedded) == 54, len(embedded)
bad2 = 0
pub = {(s['R'], tuple(sorted(s['X'], reverse=True)), s['z']): s['value'] for s in seps}
for (R, Xs, z, val) in embedded:
    XX = tuple(int(t) for t in Xs.split(','))
    key = (int(R), XX, int(z))
    if pub.get(key) != int(val):
        bad2 += 1
        print('EMBED MISMATCH', key, val, pub.get(key))
print('new-anchor table transcription: %d/%d exact' % (54 - bad2, 54))
assert bad2 == 0

# 4) the 54 spots additionally agree with the concurrent second census
#    output (independent blind double census of kit-8; equality where
#    overlap) - fetched output pin eb87a405, machine-side only, no edit.
sec = json.load(open('/home/user/tool-results/kit9build/k8second/explore_m31m32_laddercont_midtrio_windows.out'))
sec_rows = [s for s in sec['sections'] if s['section'].endswith('_row_record')]
secspots = set()
for r in sec_rows:
    for sp in r['separations']:
        secspots.add((r['R'], tuple(sorted(sp['X'], reverse=True)), r['z'], sp['value']))
agree = disagree = 0
for s in seps:
    key = (s['R'], tuple(sorted(s['X'], reverse=True)), s['z'], s['value'])
    if key in secspots:
        agree += 1
    else:
        disagree += 1
print('second-census agreement: %d identical spot-values, %d not found there' % (agree, disagree))
assert disagree == 0, 'second census disagreement'

print('PRE-FREEZE ANCHOR VERIFICATION: ALL PASS')
