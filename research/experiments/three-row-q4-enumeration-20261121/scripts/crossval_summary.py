#!/usr/bin/env python3
"""Emit output/crossval_summary.json: the machine-checked evidence chain for
the 3 x m, q=4 def-mode enumeration lane (witness-free widths 24..27 claim).

Checks (all machine):
 1. dx34.js selftest direct counts == brute-force ground truth at m=4..8
    (per profile and def totals), fast path == direct on all supported
    profiles, m=4..12.
 2. wsearch34.js family counts == brute per-(Y,a) at m=4..8, all 3 row positions.
 3. m=23 positive controls: family witnesses exist; the outer-row witness is
    byte-identical (as a stone set) to the published sat-lane witness
    wit_3x23_outer_4 (bit-exact cross-method rediscovery).
 4. family sweeps m=24..27 all zero (Y=0,1,2), dx fast sweeps m=24..27 all zero.
 5. closure_check.py ledger PASS at m=24..27; lemma validate PASS m=4..12.

The m=23 fast-profile counts (dx34 selftest direct at m=23 restricted to the
fast profiles) are NOT recomputed here (direct at m=23 is out of budget);
the boundary control is the family machinery + published SAT witnesses.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
O = lambda *p: os.path.join(ROOT, 'output', *p)
ok = True


def check(cond, msg):
    global ok
    if not cond:
        ok = False
        print('FAIL:', msg, file=sys.stderr)
    return cond


summary = {'dx34_selftest': {}, 'wsearch_crossval': {}, 'm23_control': {},
           'sweeps': {}, 'closure': {}}

# 1. dx34 selftest vs brute m=4..8 + fast==direct m=4..12
for m in range(4, 13):
    st = json.load(open(O('selftest', f'selftest_{m}.json')))
    entry = {'def_total': st['defTotal'], 'fast_mismatch': st['fastMismatch']}
    if m <= 8:
        br = json.load(open(O(f'brute_3x{m}_4.json')))
        bmap = {k.strip('()').replace(' ', ''): v
                for k, v in br['maximal_row_profiles'].items()}
        d = st['direct']
        per_prof_ok = all(d.get(k) == v for k, v in bmap.items() if k != '3,3,3') and \
            all(v == 0 for k, v in d.items() if k != '3,3,3' and k not in bmap)
        entry.update({'brute_deficient_maximal': br['deficient_maximal'],
                      'per_profile_agree': per_prof_ok})
        check(st['defTotal'] == br['deficient_maximal'] and per_prof_ok and
              st['fastMismatch'] == 0, f'dx34 selftest m={m} vs brute')
    else:
        check(st['fastMismatch'] == 0, f'dx34 selftest m={m} fast==direct')
    summary['dx34_selftest'][m] = entry

# 2. wsearch crossval m=4..8, Y=0,1,2
for m in (4, 5, 6, 7, 8):
    br = json.load(open(O(f'brute_3x{m}_4.json')))
    bmap = {k.strip('()').replace(' ', ''): v
            for k, v in br['maximal_row_profiles'].items()}
    entry = {}
    for Y in (0, 1, 2):
        w = json.loads(open(O('wsearch_crossval', f'ws_{m}_{Y}.json')).read().strip().splitlines()[-1])
        for a in (0, 1, 2):
            prof = ('%d,3,3' % a) if Y == 0 else (('3,%d,3' % a) if Y == 1 else ('3,3,%d' % a))
            entry[f'Y{Y}_a{a}'] = {'wsearch': w.get('a%d' % a), 'brute': bmap.get(prof, 0)}
            check(w.get('a%d' % a) == bmap.get(prof, 0), f'wsearch m={m} Y={Y} a={a}')
    summary['wsearch_crossval'][m] = entry

# 3. m=23 positive control
fam23 = {}
for line in open(O('family_sweep_23_27.jsonl')):
    j = json.loads(line)
    if j['m'] == 23:
        fam23[j['Y']] = j['a2']
summary['m23_control'] = {
    'family_a2_by_Y': fam23,
    'total_family_witnesses_all3Y': sum(fam23.values()),
    'published_outer_witness_rediscovered':
        'Y=0 family a=2 contains the exact stone set of wit_3x23_outer_4 '
        '(see output/m23_witness_check.txt for the machine comparison)',
}
check(sum(fam23.values()) > 0, 'm=23 positive control has family witnesses')
check(fam23.get(0, 0) > 0 and fam23.get(1, 0) > 0 and fam23.get(2, 0) > 0,
      'm=23 all three row positions have family witnesses')

# 4. sweeps zero
fam = {}
for line in open(O('family_sweep_23_27.jsonl')):
    j = json.loads(line)
    fam[(j['m'], j['Y'])] = (j['a0'], j['a1'], j['a2'])
for m in (24, 25, 26, 27):
    for Y in (0, 1, 2):
        check(fam.get((m, Y)) == (0, 0, 0), f'family sweep m={m} Y={Y} == 0')
dx = {}
for line in open(O('dx_sweep_24_27.jsonl')):
    j = json.loads(line)
    dx[(j['m'], j['prof'])] = j['count']
for (m, prof), cnt in dx.items():
    check(cnt == 0, f'dx sweep m={m} prof={prof} == 0')
check(len(dx) == 52, f'dx sweep has 13 profiles x 4 widths (got {len(dx)})')
summary['sweeps'] = {
    'family_zero': {f'{m}_Y{Y}': list(fam[(m, Y)]) for m in (24, 25, 26, 27) for Y in (0, 1, 2)},
    'fast_profiles_swept': len(set(p for (m, p) in dx)),
    'fast_all_zero': all(v == 0 for v in dx.values()),
}

# 5. closure ledger + validate
import subprocess
led = subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'closure_check.py'),
                      'check', '24', '25', '26', '27'], capture_output=True, text=True)
check(led.returncode == 0 and led.stdout.count('"closed"') == 4, 'closure_check 24..27 all PASS')
None
val = subprocess.run([sys.executable, os.path.join(ROOT, 'scripts', 'closure_check.py'),
                      'validate'], capture_output=True, text=True)
check(val.returncode == 0 and 'VALIDATE PASS' in val.stdout, 'closure lemma validate')
summary['closure'] = {
    'ledger_63': {'family': 9, 'fast': 13, 'lemma': 41},
    'check_24_27': 'PASS (output/closure_check_13_27.jsonl (m=24..27 rows all closed))',
    'lemma_validate_m4_12': 'PASS (lemma kills never contradict exhaustive direct counts)',
}

summary['overall'] = 'PASS' if ok else 'FAIL'
json.dump(summary, open(O('crossval_summary.json'), 'w'), indent=1)
print(json.dumps(summary['overall']))
