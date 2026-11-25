#!/usr/bin/env python3
"""Build the published (6,5) witness config pool with D4 images and global dedup.

Sources (all downloaded from repo main, byte-identical, sha256 in sources/):
  k0808_scan.json   : six-row-deficient-witnesses-20261113 largest-m witness (6,5,19)
  q56_records.jsonl : six-row-q5-q6-frontier-20261120 SAT records m=19..28 (q5 tags)
  extended.json     : witness-extension-kissat-20261114 (6,5) 6x29 column-extension
  w65_30.json       : extend6-deep-removal-20261114 (6,5) 6x30 x2
  L2_c630_def.json  : encoding-symmetry-kissat-20261114 (6,5) 6x30 L2 (in verify/)

Per published witness we emit its <=4 D4 images (span-preserving:
id, H = x -> span-1-x, V = y -> 5-y, HV), each normalized to minx=0,
with a global dedup on the full lattice-isomorphism canonical key
(8 transforms x translation). Output pool.json (deterministic order).
"""
import json, os, sys
from itertools import permutations

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'sources')

def load(name):
    with open(os.path.join(SRC, name)) as f:
        return json.load(f)

def norm(S):
    mn = min(x for x, y in S)
    return sorted((x - mn, y) for x, y in S)

def canon_key(S):
    # full lattice-iso canonical: D4 on the integer lattice (translations free)
    mn_x = min(x for x, y in S); mn_y = min(y for x, y in S)
    mx_x = max(x for x, y in S); mx_y = max(y for x, y in S)
    P = [(x - mn_x, y - mn_y) for x, y in S]
    W, Hh = mx_x - mn_x, mx_y - mn_y
    forms = []
    for fx, fy in [(1,1),(1,-1),(-1,1),(-1,-1)]:
        for swap in (False, True):
            pts = []
            for x, y in P:
                a, b = fx*x, fy*y
                if swap: a, b = b, a
                pts.append((a, b))
            mx_a = max(a for a,b in pts); mx_b = max(b for a,b in pts)
            forms.append(sorted((mx_a - a, mx_b - b) for a, b in pts))
    return min('|'.join(f'{x},{y}' for x, y in f) for f in forms)

published = []  # (label, stones)
k0808 = load('k0808_scan.json')
for e in k0808['witnesses_largest_m']:
    if e['w'] == 6 and e['q'] == 5:
        published.append((f"k0808_6x{e['m']}", [tuple(p) for p in e['cells']]))
recs = []
with open(os.path.join(SRC, 'q56_records.jsonl')) as f:
    for line in f:
        line = line.strip()
        if line:
            recs.append(json.loads(line))
for r in recs:
    if 'q5' in r.get('tag', '') and isinstance(r.get('witness'), dict):
        st = r['witness'].get('stones')
        if st:
            published.append((f"q56_{r['tag']}_6x{r['m']}", [tuple(p) for p in st]))
ext = load('extended.json')
for e in ext:
    if e['w'] == 6 and e['q'] == 5:
        published.append((f"ext_{e['fromM']}to{e['toM']}_6x{e['toM']}", [tuple(p) for p in e['stones']]))
w65 = load('w65_30.json')
for i, e in enumerate(w65):
    published.append((f"ext6_a{i}_6x{e['m']}", [tuple(p) for p in e['stones']]))
l2 = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'verify', 'L2_pub.json')))
published.append(("L2_6x30", [tuple(p) for p in l2['stones']]))

pool = {}
entries = []
for label, S in published:
    span = max(x for x, y in S) + 1
    seen_imgs = set()
    for iname, tf in (('id', None), ('H', 'H'), ('V', 'V'), ('HV', 'HV')):
        if tf is None:
            T = S
        elif tf == 'H':
            T = [(span - 1 - x, y) for x, y in S]
        elif tf == 'V':
            T = [(x, 5 - y) for x, y in S]
        else:
            T = [(span - 1 - x, 5 - y) for x, y in S]
        key = canon_key(T)
        if key in seen_imgs:  # image duplicate within this witness
            continue
        seen_imgs.add(key)
        if key in pool:
            pool[key]['provenance'].append(f"{label}:{iname}")
            continue
        # relative-config identity across full iso class; store normalized id image
        N = norm(T)
        pool[key] = {'stones': N, 'span': max(x for x, y in N) + 1,
                     'provenance': [f"{label}:{iname}"], 'iso_key': key}

entries = [pool[k] for k in sorted(pool)]
out = {'w': 6, 'q': 5, 'configs': []}
cnt = 0
for e in entries:
    e['cfg_id'] = f"c{cnt:03d}"
    out['configs'].append(e)
    cnt += 1
with open(os.path.join(SRC, '..', 'pool.json'), 'w') as f:
    json.dump(out, f, indent=1)
print(f"published witnesses: {len(published)}, unique iso configs (with D4 images): {cnt}")
for e in out['configs']:
    print(e['cfg_id'], 'span', e['span'], ' <- ', '; '.join(e['provenance']))
