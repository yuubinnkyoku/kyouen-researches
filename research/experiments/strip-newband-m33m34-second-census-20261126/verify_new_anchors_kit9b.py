#!/usr/bin/env python3
"""verify_new_anchors_kit9b.py: PRE-FREEZE engine re-measurement of the
232 anchor spots embedded in explore_m33m34_second_census.py, run
BEFORE the frozen census execution. Asserts:
 - the embedded ENGINE_BLOCK is byte-pinned to the published chain
   startup pin bd5f22e4...,
 - all 180 inherited spots re-measure to their PUBLISHED values
   (kit-4..kit-7 chain, as embedded in the original kit-8 explorer),
 - all 52 kit-8 separation spots re-measure to the kit-8 published
   .out measured values (the kit-8b second census agreed 54/54).
No census row is measured here (no spoiler of the kit-9b rows).
"""
import json, re, ast, hashlib, os, sys
from functools import lru_cache

CAND = ['explore_m33m34_second_census.py', 'kit9b/explore_m33m34_second_census.py']

def find(names):
    for n in names:
        if os.path.exists(n):
            return n
    raise FileNotFoundError(names)

EXPLORER = find(CAND)
K8_EXPLORER = find(['explore_m31m32_ladders_trio.py',
                    'kit9b/explore_m31m32_ladders_trio.py',
                    'research_experiments_strip-newband-m31m32-'
                    'ladders-trio-20261126_explore_m31m32_ladders_trio.py'])
K8_OUT = find([K8_EXPLORER[:-3] + '.out'])

src = open(EXPLORER).read()
i = src.index("ENGINE_BLOCK = '''")
j = src.index("'''", i + 20)
blk = src[i + 18:j]
pin = hashlib.sha256(blk.encode()).hexdigest()
assert pin == ('bd5f22e415a78368c9b798296bc84948d5637decbf3c2'
               '1a92404d45fb12e3a92'), pin
ns = {'lru_cache': lru_cache}
exec(blk, ns)
H = ns['H_canonical']

m = re.search(r'ANCHOR_SPEC_JSON = \'(.*?)\'\n', src, re.S)
ANCHORS = json.loads(ast.literal_eval("'" + m.group(1) + "'"))
assert len(ANCHORS) == 232

bad = 0
H.cache_clear()
for (R, X, z, pub, role) in ANCHORS:
    val = H(R, tuple(sorted(X, reverse=True)), z)
    if val != pub:
        bad += 1
        print('MISMATCH (R=%s, X=%s, z=%s): engine %s != published %s'
              % (R, X, z, val, pub))
print('embedded 232 anchors re-measured: %d/%d exact' % (232 - bad, 232))
assert bad == 0

# cross-check the 52 new spots against the kit-8 published .out directly
kout = json.loads(open(K8_OUT).read())
seps8 = {}
for sec in kout['sections']:
    for s in sec.get('separations') or []:
        key = (sec['R'], tuple(sorted(s['X'], reverse=True)), sec['z'])
        seps8[key] = s['value']
assert len(seps8) == 54, len(seps8)
k8src = open(K8_EXPLORER).read()
i2 = k8src.index('    anchor_spec = [')
k2 = k8src.index('[', i2)
depth = 0
for p in range(k2, len(k8src)):
    if k8src[p] == '[':
        depth += 1
    elif k8src[p] == ']':
        depth -= 1
        if depth == 0:
            break
k8spec = ast.literal_eval(k8src[k2:p + 1])
have = set((a[0], tuple(sorted(a[1], reverse=True)), a[2]) for a in k8spec)
new = [a for a in ANCHORS if (a[0], tuple(sorted(a[1], reverse=True)), a[2])
       not in have]
assert len(new) == 52, len(new)
bad2 = 0
for (R, X, z, pub, role) in new:
    key = (R, tuple(sorted(X, reverse=True)), z)
    if seps8.get(key) != pub:
        bad2 += 1
        print('KIT8-OUT MISMATCH', key, pub, seps8.get(key))
print('52 new spots vs kit-8 published .out: %d/52 exact' % (52 - bad2))
assert bad2 == 0
print('PRE-FREEZE ANCHOR VERIFICATION kit-9b: ALL PASS')
