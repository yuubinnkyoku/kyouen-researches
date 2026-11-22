#!/usr/bin/env python3
"""Placement census over the (6,5) published-config pool (complete modulo board isometries).

For each unique full-iso config in pool.json, enumerate ALL x-offsets 0..(MAXW-span)
and call append_criterion.py (published Fraction semantics, sha-pinned) on the shifted
stones with scan_limit = MAXW+2. A placement (offset s) witnesses board widths
s+span .. min(reach_s, MAXW) when old_uncovered==0 (K0853: blockedness depends only on
(S,c); safety is width-independent). Per-config checkpoint census/<cfg_id>.json,
resume-safe (existing outputs skipped). Extras: appended cfg 'x' from argv files
(raw stones JSON) are censused the same way (used for any surgery seeds).
Usage: census_pool.py MAXW [extra_stones.json ...]
"""
import json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
KIT = os.path.dirname(HERE)
MAXW = int(sys.argv[1])
extra = sys.argv[2:]

def crit(stones):
    r = subprocess.run(['python3', os.path.join(HERE, 'append_criterion.py'), '6', str(MAXW + 2), '5'],
                       input=json.dumps(stones), capture_output=True, text=True, check=True)
    return json.loads(r.stdout.strip())

def census(cfg_id, stones, span, prov):
    outp = os.path.join(KIT, 'census', cfg_id + '.json')
    if os.path.exists(outp):
        return json.load(open(outp))
    table = []
    for s in range(0, MAXW - span + 1):
        shifted = [[x + s, y] for x, y in stones]
        j = crit(shifted)
        table.append({'offset': s, 'old_uncovered': j['old_uncovered_count'],
                      'reach': j['free_append_reach'], 'first_unblocked': j.get('first_unblocked'),
                      'safe': j['safe']})
    cov = []
    for t in table:
        if t['old_uncovered'] == 0:
            hi = min(t['reach'], MAXW)
            lo = t['offset'] + span
            if hi >= lo:
                cov.append([lo, hi, t['offset']])
    band_top = (max(c[1] for c in cov) if cov else span - 1)
    out = {'cfg_id': cfg_id, 'provenance': prov, 'span': span, 'maxw': MAXW,
           'placements': table, 'covered_ranges': cov, 'band_top': band_top}
    with open(outp, 'w') as f:
        json.dump(out, f, indent=1)
    return out

pool = json.load(open(os.path.join(KIT, 'pool.json')))
for c in pool['configs']:
    r = census(c['cfg_id'], c['stones'], c['span'], c['provenance'])
    print(f"{c['cfg_id']} span {c['span']} band_top {r['band_top']} ranges {r['covered_ranges']}", flush=True)
for i, p in enumerate(extra):
    S = json.load(open(p))
    if isinstance(S, dict):
        S = S.get('stones') or S.get('cells')
    span = max(x for x, y in S) + 1
    cid = 'x%02d' % i
    r = census(cid, [list(t) for t in S], span, [p])
    print(f"{cid} {p} span {span} band_top {r['band_top']} ranges {r['covered_ranges']}", flush=True)
