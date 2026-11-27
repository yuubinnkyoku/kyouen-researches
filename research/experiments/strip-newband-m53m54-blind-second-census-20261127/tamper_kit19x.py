#!/usr/bin/env python3
"""kit-19x tamper battery (scratch copies only, never published)."""
import json, shutil, subprocess, sys

def run(census):
    r = subprocess.run([sys.executable, 'audit_kit19x.py', census, '/home/user/ky/kit18.out'],
                       capture_output=True, text=True)
    return r.returncode, r.stdout

def mutate(src, dst, fn):
    shutil.copy(src, dst)
    d = json.load(open(dst))
    fn(d)
    json.dump(d, open(dst, 'w'), indent=1, sort_keys=True)

def t1(d):  # flip frontier m53 separation value
    for s in d['sections']:
        if s['section'] == 'frontier_m53_z105_row_record':
            s['separations'][0]['value'] = 1

def t2(d):  # phantom separation in a clean window row
    for s in d['sections']:
        if s['section'] == 'inband_m51_z93_row_record':
            s['separations'].append({'S': 94, 'X': [51, 43], 'collapse': 0,
                                     'direction': 'UP', 'value': 1})

def t3(d):  # corrupt a registered prediction text byte
    for s in d['sections']:
        if s['section'] == 'ladder_m27_z78_row_record':
            s['registered_prediction'] = s['registered_prediction'].replace('UP 1v0', 'UP 1v1')

res = []
for name, fn in [('T1_frontier_value_flip', t1), ('T2_phantom_window_sep', t2),
                 ('T3_prediction_text_flip', t3)]:
    mutate('census_kit19x.out', 'scratch_tamper.json', fn)
    rc, out = run('scratch_tamper.json')
    caught = [l for l in out.splitlines() if 'GATE-FAIL' in l]
    res.append((name, rc, [l.split()[1] for l in caught]))
rc0, out0 = run('census_kit19x.out')
print(json.dumps({'tamper_results': [{'test': n, 'rc': rc, 'caught_gates': g} for n, rc, g in res],
                  'clean_control_rc': rc0,
                  'all_fail_closed': all(rc != 0 for _, rc, _ in res) and rc0 == 0}, indent=1))
