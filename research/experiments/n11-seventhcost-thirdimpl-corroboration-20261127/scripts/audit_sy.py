#!/usr/bin/env python3
"""Part SY audit: fresh fail-closed audit of the seventh-cost third-impl
corroboration raws. Fresh single-batch implementation (not a byte
transform of any previous audit; Part SS/SX precedent, disclosed).

Gates (fail-closed, rc 1):
  G0  kit pins: third_impl.js / verify_tbl.js / jsreplay sha256 vs
      gate-rows.json pins; gate-rows.json schema/part/declaration_head
  G1  calibration: c1a raw rc=0, quads 95670, triples mismatches 0;
      c1b k06/k38 raws: result==2, expansions exact vs published pins
  G2  target set == 42 (41 result 2 + 1 result 1), exactly k05 is WIN
  G3  every target raw: rc=0, reason clean, derived legal == declared
      legal, lo/hi match the row, result == expected_result
  G4  per-target cold pair: result and expansions byte-equal across
      the two passes
  G5  counts: 42 targets x 2 passes = 84 target raws, no extras
  G6  monotone bookkeeping summary printed from the raws themselves
"""
import json, pathlib, re, sys, hashlib

KIT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/home/user/work/sy/kit')
GR = json.loads((KIT / 'input/gate-rows.json').read_text())
OUT = KIT / 'output'
RAWTXT = re.compile(
    r'^third,([a-zA-Z0-9.-]+),5,(\d+),(\d+),([012]),(\d+),(\d+),([0-9.]+),(\d+),(\d+),([a-z_]+:?[^,]*),quads=(\d+),ttOverwrites=(\d+),memoPower=(\d+)\nrc=0\n$')

def fail(g, m):
    print(f'AUDIT-FAIL {g}: {m}')
    sys.exit(1)

def parse_raw(p, want_row):
    txt = p.read_text()
    m = RAWTXT.match(txt)
    if not m:
        fail('G3', f'{p.name}: raw does not match pinned schema')
    if m.group(1) != want_row:
        fail('G3', f'{p.name}: row label {m.group(1)} != {want_row}')
    return m

def main():
    # G0
    if GR['schema'] != 'n11-seventhcost-thirdimpl-corroboration-rows-v1' or GR['part'] != 'SY':
        fail('G0', 'schema/part')
    if GR['declaration_head'] != '47ae14ea8455a4bf115f27e9bbbc2a3e8c9b4e9e':
        fail('G0', 'declaration head')
    for nm, pin in (('scripts/third_impl.js', GR['third_impl']['sha256']),
                    ('scripts/verify_tbl.js', GR['verify_tbl']['sha256']),
                    ('scripts/jsreplay_lane.js', GR['jsreplay_replica']['sha256'])):
        got = hashlib.sha256((KIT / nm).read_bytes()).hexdigest()
        if got != pin:
            fail('G0', f'{nm} sha {got}')
    # G1
    c1a = (OUT / 'c1a-verify-tbl.txt').read_text()
    if 'rc=0' not in c1a or 'quads 95670' not in c1a or 'mismatches 0' not in c1a:
        fail('G1', 'c1a raw')
    for cal, exp in (('c1b-k06.txt', '9474431'), ('c1b-k38.txt', '25898941')):
        m = parse_raw(OUT / cal, cal[4:-4])
        if m.group(4) != '2' or m.group(5) != exp:
            fail('G1', f'{cal}: result {m.group(4)} expansions {m.group(5)} != {exp}')
    # G2
    tg = GR['targets']
    if len(tg) != 42:
        fail('G2', f'{len(tg)} targets')
    wins = [k for k, r in tg.items() if r['expected_result'] == '1']
    if wins != ['k05']:
        fail('G2', f'WIN set {wins}')
    # G3/G4/G5
    raws = sorted((OUT / 'raw').glob('*.txt'))
    if len(raws) != 84:
        fail('G5', f'{len(raws)} raws != 84')
    exp_bill = 0
    for k, row in tg.items():
        pair = []
        for p in ('p1', 'p2'):
            f = OUT / 'raw' / f'{k}.{p}.txt'
            if not f.exists():
                fail('G5', f'missing {f.name}')
            m = parse_raw(f, f'{k}.{p}')
            if m.group(2) != row['legal'] or m.group(3) != row['legal']:
                fail('G3', f'{f.name}: legal {m.group(2)}/{m.group(3)} != {row["legal"]}')
            if m.group(8) != row['lo'] or m.group(9) != row['hi']:
                fail('G3', f'{f.name}: lo/hi mismatch')
            if m.group(10) != 'clean':
                fail('G3', f'{f.name}: reason {m.group(10)}')
            if m.group(4) != row['expected_result']:
                fail('G3', f'{f.name}: result {m.group(4)} != expected {row["expected_result"]}')
            pair.append((m.group(4), m.group(5)))
        if pair[0] != pair[1]:
            fail('G4', f'{k}: cold pair mismatch {pair}')
        exp_bill += int(pair[0][1]) * 2
    # G6
    print(f'AUDIT-PASS targets=42 (41 LOSS + 1 WIN) raws=84 pairs=42 '
          f'expansion_bill={exp_bill} (bookkeeping) '
          f'verdicts_consumed=0 status=UNCONSUMED')
    print('11x11 empty board UNKNOWN; 19 central-reply roots UNKNOWN; '
          'two-stone root {60,27} UNKNOWN; third moves {100,108} UNKNOWN; '
          'all closure classes UNKNOWN; expansions are bookkeeping, never verdicts')

if __name__ == '__main__':
    main()
