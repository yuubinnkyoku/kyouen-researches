#!/usr/bin/env python3
"""kit-19x audit: fail-closed gates over the frozen census_kit19x.out.

Usage: python3 audit_kit19x.py <census_kit19x.out> <kit18_published.out>
Exit 0 + AUDIT-PASS iff every gate passes. Any tamper must fail-closed."""
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CENSUS_PIN = '275faedc80d04e2899c081eb7c56a0bcb80f7cf01b644793c6b846eb3d10a2f4'
KIT18_PIN = 'c3087285fbdbd44d0588132f9c1d4c75fce2913b816ce383a5f0b377154364ba'
ENGINE_PIN = '582c93c17bcd4fa618bfb74c733c3d679e197e8749ec4bbcc8821d3a6610d5c0'

SPOT_ROWS = ['frontier_m53_z105_row_record', 'frontier_m54_z106_row_record',
             'ladder_m27_z78_row_record', 'ladder_m27_z79_row_record',
             'inband_m51_z100_row_record', 'evenlife_m16_z66_row_record']

fails = []


def gate(name, ok, detail=''):
    print('%s %s %s' % ('GATE-PASS' if ok else 'GATE-FAIL', name, detail))
    if not ok:
        fails.append(name)


def main():
    census_path, kit18_path = sys.argv[1], sys.argv[2]
    # G0: engine byte-clone pin
    esha = hashlib.sha256(open(os.path.join(HERE, 'engine_block.py'), 'rb').read()).hexdigest()
    gate('G0_engine_pin', esha == ENGINE_PIN, esha[:16])
    # G1: registration source pin
    ksha = hashlib.sha256(open(kit18_path, 'rb').read()).hexdigest()
    gate('G1_kit18_source_pin', ksha == KIT18_PIN, ksha[:16])
    # G2: frozen census pin
    csha = hashlib.sha256(open(census_path, 'rb').read()).hexdigest()
    gate('G2_census_pin', csha == CENSUS_PIN, csha[:16])
    d = json.load(open(census_path))
    secs = d['sections']
    # G3: registration provenance: byte-verbatim prediction texts
    regflat = json.load(open(os.path.join(HERE, 'kit19_registration_extracted.json')))
    rows = [s for s in secs if s.get('section', '').endswith('_row_record')]
    pred_by_item = [r['prediction'] for r in regflat if r['kind'] in
                    ('one-past', 'birth') or r['kind'].startswith('frontier')]
    got = [s.get('registered_prediction') for s in rows
           if s['section'].startswith(('ladder_', 'frontier_'))]
    gate('G3_registration_provenance',
         len(got) == len(pred_by_item) == 30 and
         all(a == b for a, b in zip(got, pred_by_item)),
         '%d/%d texts verbatim' % (len(got), len(pred_by_item)))
    # G4: live recompute of spot rows, byte compare
    import census_kit19x as cx
    reg = cx.parse_registration(kit18_path)
    built = {r['section']: r for r in cx.build_kit19_rows(reg)}
    ok4 = True
    for secname in SPOT_ROWS:
        b = built[secname]
        live = cx.row_record(b['section'], b['label'], {}, b['R'], b['z'],
                             b['min'], b['smin'], b['smax'])
        frozen = [s for s in rows if s['section'] == secname][0]
        m = (live['separations'] == frozen['separations'] and
             live['shapes'] == frozen['shapes'] and
             live['R'] == frozen['R'] and live['z'] == frozen['z'])
        if not m:
            ok4 = False
    gate('G4_spot_live_recompute', ok4, '%d rows' % len(SPOT_ROWS))
    # G5: structural + outcome gates
    ladder = [s for s in rows if s['section'].startswith('ladder_')]
    frontier = [s for s in rows if s['section'].startswith('frontier_')]
    windows = [s for s in rows if s['section'].startswith('inband_')]
    evenlife = [s for s in rows if s['section'].startswith('evenlife_')]
    gate('G5_structure', len(rows) == 49 and len(ladder) == 28 and
         len(frontier) == 2 and len(windows) == 16 and len(evenlife) == 3,
         '49=28+2+16+3')
    gate('G5a_windows_clean', all(len(s['separations']) == 0 for s in windows),
         '16/16 zero-separation')
    f53 = [s for s in frontier if s['section'] == 'frontier_m53_z105_row_record'][0]
    f54 = [s for s in frontier if s['section'] == 'frontier_m54_z106_row_record'][0]
    gate('G5b_frontier_exact',
         len(f53['separations']) == 1 and f53['separations'][0] == 
         {'S': 107, 'X': [53, 54], 'collapse': 0, 'direction': 'UP', 'value': 2} and
         len(f54['separations']) == 1 and f54['separations'][0] == 
         {'S': 108, 'X': [54, 54], 'collapse': 1, 'direction': 'UP', 'value': 2},
         'm53 {53,54}@107 UP 2v0 / m54 (54,54)@108 UP 2v1')
    tot = [s for s in secs if s['section'] == 'totals'][0]
    gate('G5c_totals', tot['separations'] ==
         sum(len(s['separations']) for s in rows) == 273, '273 separations')
    ver = [s for s in secs if s['section'] == 'registration_verification'][0]
    gate('G6_verification', ver['result'] == 'VERIFY-PASS' and
         ver['binding_ok'] == 49, 'VERIFY-PASS 49')
    val = [s for s in secs if s['section'] == 'kit18_published_row_revalidation'][0]
    gate('G7_revalidation', val['result'] == 'VALIDATE-PASS' and val['bad'] == 0
         and val['rows'] == 49, '49/49 kit-18 rows reproduced')

    print('AUDIT-%s gates=%d fails=%d' % ('PASS' if not fails else 'FAIL',
                                          10, len(fails)))
    return 0 if not fails else 1


if __name__ == '__main__':
    sys.exit(main())
