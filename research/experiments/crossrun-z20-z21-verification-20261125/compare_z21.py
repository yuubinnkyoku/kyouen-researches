#!/usr/bin/env python3
"""compare_z21: structured comparison of this run's independent z=21
verification output against the published z21-min16 kit frozen output
(explore_z21f16.out, commit 8a106233, sha256 10f94100...f643)."""
import json, sys

mine = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'verify_z21_indep.out'))
theirs = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'research/experiments/strip-z21-min16-20261125/explore_z21f16.out'))

msec = {}
for s in mine['sections']:
    msec.setdefault(s['section'], []).append(s)
tsec = {}
for s in theirs['sections']:
    tsec.setdefault(s['section'], []).append(s)

mismatch = []
cmp_rows = 0
cmp_fields = 0


def note(msg):
    mismatch.append(msg)


def eq(a, b, where):
    global cmp_rows, cmp_fields
    cmp_fields += 1
    if a != b:
        note(f'{where}: {a!r} != {b!r}')


# engine_gate
mg = msec['engine_gate'][0]
tg = tsec['engine_gate'][0]
eq(mg['pin'], tg['pin'], 'engine_gate.pin')
eq(mg['gate'], tg['gate'], 'engine_gate.gate')

# cell census (15 cells, order-sensitive)
mc = msec['cell_census']
tc = tsec['cell_census']
eq(len(mc), len(tc), 'cell_census.count')
for i, (a, b) in enumerate(zip(mc, tc)):
    w = f'cell_census[{i}:{b.get("cell")}]'
    cmp_rows += 1
    eq(a['cell'], b['cell'], w + '.cell')
    eq(a['shapes'], b['shapes'], w + '.shapes')
    eq(len(a['deviants']), len(b['deviants']), w + '.deviants.len')
    for d1, d2 in zip(a['deviants'], b['deviants']):
        eq(d1, d2, w + '.deviant')  # full dict equality (s,value,collapse,direction,shapes)
        cmp_rows += 1
    eq(a['multivalue_rows'], b['multivalue_rows'], w + '.multivalue_rows')

# tail spots
mt = msec['tail_spots_s47_54'][0]['rows']
tt = tsec['tail_spots_s47_54'][0]['rows']
eq(len(mt), len(tt), 'tail_spots.count')
for r1, r2 in zip(mt, tt):
    cmp_rows += 1
    eq({k: r1[k] for k in ('cell', 's', 'shape', 'value', 'collapse', 'match')},
       {k: r2[k] for k in ('cell', 's', 'shape', 'value', 'collapse', 'match')},
       f'tail_spots[{r2["cell"]}:{r2["s"]}]')

# strip sweep
ms = msec['strip_z21_m16_20'][0]
ts = tsec['strip_z21_m16_20'][0]
eq(ms['per_m'], ts['per_m'], 'strip.per_m')
eq(ms['total_shapes'], ts['total_shapes'], 'strip.total_shapes')
eq(ms['violations'], ts['violations'], 'strip.violations')

# row records (shared numeric fields)
for name in ('inband_m15_z21_row_record', 'inband_m15_z21_row_record_ext_arity4',
             'inband_m14_z21_row_record', 'inband_m13_z21_row_record',
             'inband_m12_z21_row_record'):
    a = msec[name][0]
    b = tsec[name][0]
    cmp_rows += 1
    for k in ('R', 'z', 'min', 'shapes', 'separations', 'arity_max', 's_domain'):
        eq(a[k], b[k], f'{name}.{k}')

# strip spots
msp = msec['strip_spots_m21_24'][0]['rows']
tsp = tsec['strip_spots_m21_24'][0]['rows']
eq(len(msp), len(tsp), 'strip_spots.count')
for r1, r2 in zip(msp, tsp):
    cmp_rows += 1
    eq({k: r1[k] for k in ('m', 'X', 'value', 'collapse', 'match')},
       {k: r2[k] for k in ('m', 'X', 'value', 'collapse', 'match')},
       f'strip_spots[{r2["m"]}:{r2["X"]}]')

# base spot
mb = msec['m16_base_spot'][0]
tb = tsec['m16_base_spot'][0]
for k in ('X', 'R', 'z', 'value', 'collapse_single', 'match'):
    eq(mb[k], tb[k], f'm16_base_spot.{k}')

# below-band
mbb = msec['belowband_j1_child_H22_22'][0]
tbb = tsec['belowband_j1_child_H22_22'][0]
for k in ('R', 'z', 'floor', 'shapes', 'deviants', 'multivalue_rows',
          's_domain', 'arity'):
    eq(mbb[k], tbb[k], f'belowband.{k}')

# identities (full hold/break rows with values)
for name in ('twelfth_tail_supply_identity_recheck',
             'thirteenth_tail_supply_identity_recheck',
             'fourteenth_tail_supply_identity_precalc'):
    a = msec[name][0]
    b = tsec[name][0]
    eq(a['identity'], b['identity'], f'{name}.identity')
    eq(len(a['hold_rows']), len(b['hold_rows']), f'{name}.hold.count')
    for r1, r2 in zip(a['hold_rows'], b['hold_rows']):
        cmp_rows += 1
        eq(r1, r2, f'{name}.hold[{r2["s"]}]')
    eq(len(a['break_rows']), len(b['break_rows']), f'{name}.break.count')
    for r1, r2 in zip(a['break_rows'], b['break_rows']):
        cmp_rows += 1
        eq(r1, r2, f'{name}.break[{r2["s"]}]')

# parity section: summary (mine only)
pl = msec['base_spot_lattice_parity_closed_form'][0]
print('PARITY rows_checked=%d mismatches=%r' % (pl['rows_checked'],
                                                pl['mismatches']))
print('PARITY six data points:',
      [(d['z'], d['collapse_v']) for d in pl['six_published_base_spot_data_points_z16_21']])
print('COMPARE rows=%d field_checks=%d mismatches=%d' %
      (cmp_rows, cmp_fields, len(mismatch)))
for m in mismatch[:20]:
    print('MISMATCH', m)
sys.exit(0 if not mismatch else 1)
