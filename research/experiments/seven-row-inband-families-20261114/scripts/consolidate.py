#!/usr/bin/env python3
"""Consolidate verified witnesses from results.jsonl into output/witnesses.json."""
import json, collections
wit = collections.defaultdict(list)
for line in open('results/results.jsonl'):
    r = json.loads(line)
    if r.get('status') == 'SAT' and r.get('jsVerify', {}).get('ok') and r.get('pyVerify', {}).get('ok') and r.get('rowY') is None:
        assert r['rows'] == r['pyVerify']['rows'], (r['w'], r['m'], r['q'])
        wit[(r['w'], r['q'])].append({
            'm': r['m'], 'n': r['nStones'], 'rows': r['rows'], 'lex': r.get('lex'),
            'stones': r['stones'], 'conflicts': r['conflicts'],
            'deficientRows': [y for _, y in r['deficientRows']],
            'jsVerify': r['jsVerify'], 'pyVerify': r['pyVerify']})
out = {}
for (w, q), ws in wit.items():
    seen = {}
    for x in ws: seen[x['m']] = x  # dedup: keep last run per m
    ws = [seen[m] for m in sorted(seen)]
    out[f'w{w}q{q}'] = ws
json.dump({'schema': 1, 'note': 'all witnesses dual-verified (sat.js verifyConfig census-free JS + verify_witness.py Python Fraction); stones are [x,y] pairs; deficientRows have <= q-2 stones; lex means the witness is the {H,V,HV}-orbit lex-leader', 'families': out}, open('output/witnesses.json', 'w'), indent=1)
print(json.dumps({k: {'count': len(v), 'm_range': [v[0]['m'], v[-1]['m']], 'n': [x['n'] for x in v]} for k, v in out.items()}, separators=(',', ':')))
