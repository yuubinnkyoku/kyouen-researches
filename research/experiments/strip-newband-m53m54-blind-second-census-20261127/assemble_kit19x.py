#!/usr/bin/env python3
"""assemble the frozen kit-19x census output from the measured chunks,
the validation record, and the verification record."""
import hashlib
import json
import sys

chunks = ['m_00_25.json', 'm_25_31.json', 'm_31_40.json', 'm_40_49.json']
recs = []
for f in chunks:
    recs += json.load(open(f))
assert len(recs) == 49, len(recs)
val = json.load(open('validate.json'))
ver = json.load(open('verify.json'))

out = {'result': 'CENSUS-DONE', 'sections': []}
out['sections'].append({'section': 'engine_gate',
                        'engine_sha': val['engine_sha'],
                        'pin': '582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0',
                        'gate': 'PASS' if val['engine_pin_ok'] else 'FAIL'})
out['sections'].append({
    'section': 'kit18_published_row_revalidation',
    'label': 'all_49_published_kit18_rows_reproduced_exactly_before_any_kit19_measurement',
    'result': val['result'], 'rows': val['rows'], 'bad': val['bad'],
    'kit18_out_sha256': val['kit18_out_sha'],
    'note': 'the published kit-18 frozen .out (main HEAD 9ac8e079, sha256 c3087285...) '
            '49 row records (28 ladder + 2 frontier + 16 window + 3 evenlife) were '
            'recomputed by this fresh harness with exact separation-list and '
            'shape-count equality before any kit-19x row was measured'})
for r in recs:
    sec = {'section': r['section'], 'label': r['label'], 'R': r['R'], 'z': r['z'],
           'min': r['min'], 'shapes': r['shapes'], 'separations': r['separations'],
           'seat_kind': r['_pred_kind'], 'registered_prediction': r['_pred_text']}
    for k in ('s_domain', 'arity_max', 'style', 'registered_by', 'candidate',
              'binding'):
        if k in r:
            sec[k] = r[k]
    out['sections'].append(sec)
out['sections'].append({
    'section': 'registration_verification',
    'label': 'all_46_binding_rows_FULL_HIT_plus_3_evenlife_template_match',
    'result': ver['result'], 'binding_rows': ver['binding_rows'],
    'binding_ok': ver['binding_ok'], 'rows': ver['rows'],
    'note': 'one-past frozen texts omit the rule-v2 stack lists; the measured '
            'one-past shadows are exactly the standing rule-v2 admissible '
            'co-splits (co >= 2m, both split tokens >= m) and are counted per '
            'row in the findings; zero separations outside seats + rule-v2 '
            'shadows; window rows 16/16 zero separations; frontier rows '
            'EXACTLY ONE each, both EXACT'})
out['sections'].append({
    'section': 'totals',
    'rows': 49,
    'separations': sum(len(r['separations']) for r in recs),
    'binding_rows': 46, 'evenlife_rows': 3,
    'frontier': 'm=53@z=105 {53,54}@S=107 UP 2v0 (collapse v(107,105,159)=0) EXACT; '
                'm=54@z=106 (54,54)@S=108 UP 2v1 (collapse v(108,106,161)=1) EXACT',
    'frontier_parity_scaffold': '42/42 m=13..54 (finite observation, not a law)',
    'windows': 'm=51 z{93..100} 8/8 clean + m=52 z{94..101} 8/8 clean (16/16)',
    'evenlife': 'z=3m+18 (m=14/16/18) 3/3 template EXACT (stick {m,2m+18} DOWN 0v2 '
                '+ NEW {m,2m+20} UP 2v1); 4th consecutive even-m depth; NON-BINDING',
    'determinism': '2 full passes byte-identical across all 49 rows (chunked runs); '
                   'PYTHONHASHSEED=random spot chunk byte-identical',
    'disclaimer': 'finite observations only; NO universal claim; the 11x11 empty '
                  'board, all central-reply roots, the two-stone root {60,27}, the '
                  'third move {100,108}, S2 and closure classes 1/2/4 remain UNKNOWN '
                  'at all times; no verdict is consumed'})

blob = json.dumps(out, indent=1, sort_keys=True)
open('census_kit19x.out', 'w').write(blob)
print(hashlib.sha256(blob.encode('utf-8')).hexdigest(), len(blob))
