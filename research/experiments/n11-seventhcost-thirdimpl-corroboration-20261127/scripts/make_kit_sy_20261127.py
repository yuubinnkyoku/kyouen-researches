#!/usr/bin/env python3
"""Part SY kit maker: seventh-cost full-batch third-impl corroboration rows.

Fresh maker (not a byte transform of any previous maker; Part SS/SX
precedent). Inputs are the published Part SW and Part SX kit
gate-rows.json files plus the published kit input CSVs; every pin is
machine-derived, no hand-typed pins (standing rule).

Gates (fail-closed, rc 1 on any failure):
  G1  schema/part of both source gate-rows files
  G2  canonical head block of both sources identical to the pinned
      record of record 42dbb58f (6832 rows WIN 201 / LOSS 6631)
  G3  every per-row input CSV byte-verifies against its source sha256
      pin (41 SW rows + k05)
  G4  target set is exactly k01..k42 minus k05 (SW) plus k05 (SX)
  G5  expected results derived from source expected quadruples
      (field 3 of legal,budget,result,nodes) and replica_verdict agree
  G6  output is deterministic: caller runs the maker twice and the
      audit compares bytes (handled by caller + audit)
  G7  third-impl pins present and hex-sha well-formed
  G8  k05 WIN row is carried with result 1 exactly once
"""
import hashlib, json, sys, pathlib

SW = pathlib.Path('/home/user/work/sw/kit/input/gate-rows.json')
SX = pathlib.Path('/home/user/work/sw/sx/kit/input/gate-rows.json')
SW_IN = pathlib.Path('/home/user/work/sw/kit/input')
SX_IN = pathlib.Path('/home/user/work/sw/sx/kit/input')
THIRD = pathlib.Path('/home/user/work/sy/inv/third_impl.js')
VTBL = pathlib.Path('/home/user/work/sy/pristine/verify_tbl.js')
JSREP = pathlib.Path('/home/user/work/sy/inv/jsreplay_lane.js')
OUT = pathlib.Path('/home/user/work/sy/kit/input/gate-rows.json')

HEXPIN = '08ea958ff59c3234ec5ac55c5c40689bd0999a34e101a88ea0546800cc4a1998'
VTBLPIN = 'c8c52528f70b3a9b438edc3feb4e432fbe705d6be21650383d3955efc6790251'
JSREP_PIN = '845856175d3c793a7eb4306f5902ecda3f1c046a8a53e8f34ed375e51febc3df'
DECL_HEAD = '47ae14ea8455a4bf115f27e9bbbc2a3e8c9b4e9e'

def sha256(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()

def fail(gate, msg):
    print(f'MAKER-FAIL {gate}: {msg}')
    sys.exit(1)

def main():
    sw = json.loads(SW.read_text())
    sx = json.loads(SX.read_text())
    # G1
    if sw.get('schema') != 'n11-seventhcost-41loss-cppgate-rows-v1':
        fail('G1', f'sw schema {sw.get("schema")}')
    if sx.get('schema') != 'n11-seventhcost-k05-l50m-cppgate-rows-v1':
        fail('G1', f'sx schema {sx.get("schema")}')
    if sw.get('part') != 'SW' or sx.get('part') != 'SX':
        fail('G1', 'part labels')
    # G2
    for src, nm in ((sw, 'sw'), (sx, 'sx')):
        ch = src['canonical_head']
        if ch.get('label') != '42dbb58f' or ch.get('WIN') != 201 or ch.get('LOSS') != 6631:
            fail('G2', f'{nm} canonical head block {ch}')
    # G4 set shape
    tg = dict(sw['targets'])
    ks = sorted(tg)
    want = [f'k{i:02d}' for i in range(1, 43)]
    want.remove('k05')
    if ks != want:
        fail('G4', 'sw target set != k01..k42 minus k05')
    k05 = sx['target']['k05']
    # G3 input pins
    for k, row in list(tg.items()) + [('k05', k05)]:
        base = SX_IN if k == 'k05' else SW_IN
        p = base / f'{k}.input.csv'
        if not p.exists():
            fail('G3', f'missing {p}')
        got = sha256(p)
        pin = row['input_sha256']
        if got != pin:
            fail('G3', f'{k} input sha {got} != pin {pin}')
    # G5 expected result from quad + replica_verdict
    out_targets = {}
    for k, row in list(tg.items()) + [('k05', k05)]:
        quad = row['expected'].split(',')
        result = quad[2]
        if result not in ('1', '2'):
            fail('G5', f'{k} quad result {result}')
        rv = row['replica_verdict']
        if str(rv) != result:
            fail('G5', f'{k} replica_verdict {rv} != quad result {result}')
        out_targets[k] = {
            'lo': row['lo'], 'hi': row['hi'], 'legal': row['legal'],
            'expected_result': result, 'stage_budget': row['budget'],
            'replica_expected_quad': row['expected'],
            'input_sha256': row['input_sha256'],
            'raw_provenance': row['raw_provenance'],
            'second_impl_gate': 'SW 44/44' if k != 'k05' else 'SX 4/4',
        }
    # G8
    if out_targets['k05']['expected_result'] != '1':
        fail('G8', 'k05 not WIN')
    if sum(1 for r in out_targets.values() if r['expected_result'] == '1') != 1:
        fail('G8', 'not exactly one WIN row')
    # G7 pins
    tp = sha256(THIRD)
    if tp != HEXPIN:
        fail('G7', f'third_impl sha {tp}')
    vp = sha256(VTBL)
    if vp != VTBLPIN:
        fail('G7', f'verify_tbl sha {vp}')
    jp = sha256(JSREP)
    if jp != JSREP_PIN:
        fail('G7', f'jsreplay sha {jp}')
    kit = {
        'schema': 'n11-seventhcost-thirdimpl-corroboration-rows-v1',
        'part': 'SY',
        'declaration_head': DECL_HEAD,
        'declaration_log': 'research/log/2026-11-27-n11-seventhcost-thirdimpl-corroboration-declaration.md',
        'canonical_head': sw['canonical_head'],
        'third_impl': {
            'path': 'kit/scripts/third_impl.js',
            'sha256': tp,
            'provenance': 'byte-equal re-publication provenance of the ea73c3e3 publication; byte-verified against the pinned sixth-cost third-impl kit copy on this host',
        },
        'verify_tbl': {'sha256': vp},
        'jsreplay_replica': {'sha256': jp},
        'invocation': 'node third_impl.js --lo=<lo> --hi=<hi> --stones=5 --legal=<legal> --row=<kNN>.pN --cap=400000000 --wallcap=260 --memo-power=22',
        'calibration': {
            'c1a_verify_tbl': {'rc': 0, 'quads': '95670', 'triples_mismatches': '0'},
            'c1b_calib_k06': {'lo': '10376293541462675456', 'hi': '65536', 'legal': '89',
                              'expected_result': '2', 'expected_expansions': '9474431',
                              'provenance': 'published sixth-cost k06-cold-a raw'},
            'c1b_calib_k38': {'lo': '10376293541461626880', 'hi': '66048', 'legal': '100',
                              'expected_result': '2', 'expected_expansions': '25898941',
                              'provenance': 'Part SU publication'},
        },
        'targets': out_targets,
        'protocol': {
            'passes_per_target': 2,
            'cold_pair_fields_equal': ['result', 'expansions'],
            'expansions_compared_only_across_third_impl_runs': True,
            'hard_stop_on': ['result != expected_result', 'cold-pair field mismatch', 'GATE_FAIL', 'crash', 'truncation'],
        },
        'meaning': 'verdict-level corroboration bookkeeping only; NO verdict consumed, no cache increment, no class-status change; adoption stays with a separately declared adoption Part',
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(kit, indent=1, sort_keys=False) + '\n')
    print(f'MAKER-PASS targets={len(out_targets)} (41 LOSS + 1 WIN)')

if __name__ == '__main__':
    main()
