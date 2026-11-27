#!/usr/bin/env python3
"""compare_z20: cross-run comparison of this lane's independent z=20
measurements (scratch z20_run1.out, from explore_z20f15.py sha d4df9769...)
against the published z20-min15 kit frozen output (commit 2cc16d34,
sha256 09e9026a...f789). The published kit's identity sections extend
one s-step beyond this lane's z20 script's domains (12..57 vs 12..56);
the comparison covers the shared range."""
import json, sys

mine = json.load(open(sys.argv[1] if len(sys.argv) > 1 else 'z20_crossrun/z20_run1.out'))
theirs = json.load(open(sys.argv[2] if len(sys.argv) > 2 else 'research/experiments/strip-z20-min15-20261125/explore_z20f15.out'))

msec = {}
for s in mine['sections']:
    msec.setdefault(s['section'], []).append(s)
tsec = {}
for s in theirs['sections']:
    tsec.setdefault(s['section'], []).append(s)

mismatch = []
cmp_rows = 0
cmp_fields = 0


def eq(a, b, where):
    global cmp_fields
    cmp_fields += 1
    if a != b:
        mismatch.append(f'{where}: {a!r} != {b!r}')


mg = msec['engine_gate'][0]
tg = tsec['engine_gate'][0]
eq(mg['pin'], tg['pin'], 'engine_gate.pin')

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
        eq(d1, d2, w + '.deviant')
        cmp_rows += 1
    eq(a['multivalue_rows'], b['multivalue_rows'], w + '.multivalue_rows')

mt = msec['tail_spots_s46_53'][0]['rows']
tt = tsec['tail_spots_s46_53'][0]['rows']
eq(len(mt), len(tt), 'tail_spots.count')
for r1, r2 in zip(mt, tt):
    cmp_rows += 1
    eq({k: r1[k] for k in ('cell', 's', 'shape', 'value', 'collapse', 'match')},
       {k: r2[k] for k in ('cell', 's', 'shape', 'value', 'collapse', 'match')},
       f'tail_spots[{r2["cell"]}:{r2["s"]}]')

ms = msec['strip_z20_m15_19'][0]
ts = tsec['strip_z20_m15_19'][0]
eq(ms['per_m'], ts['per_m'], 'strip.per_m')
eq(ms['total_shapes'], ts['total_shapes'], 'strip.total_shapes')
eq(ms['violations'], ts['violations'], 'strip.violations')

for name in ('inband_m14_z20_row_record', 'inband_m14_z20_row_record_ext_arity4',
             'inband_m13_z20_row_record', 'inband_m12_z20_row_record'):
    a = msec[name][0]
    b = tsec[name][0]
    cmp_rows += 1
    for k in ('R', 'z', 'min', 'shapes', 'separations', 'arity_max', 's_domain'):
        eq(a[k], b[k], f'{name}.{k}')

msp = msec['strip_spots_m20_23'][0]['rows']
tsp = tsec['strip_spots_m20_23'][0]['rows']
eq(len(msp), len(tsp), 'strip_spots.count')
for r1, r2 in zip(msp, tsp):
    cmp_rows += 1
    eq({k: r1[k] for k in ('m', 'X', 'value', 'collapse', 'match')},
       {k: r2[k] for k in ('m', 'X', 'value', 'collapse', 'match')},
       f'strip_spots[{r2["m"]}:{r2["X"]}]')

mb = msec['m15_base_spot'][0]
tb = tsec['m15_base_spot'][0]
for k in ('X', 'R', 'z', 'value', 'collapse_single', 'match'):
    eq(mb[k], tb[k], f'm15_base_spot.{k}')

mbb = msec['belowband_j1_child_H21_21'][0]
tbb = tsec['belowband_j1_child_H21_21'][0]
for k in ('R', 'z', 'floor', 'shapes', 'deviants', 'multivalue_rows',
          's_domain', 'arity'):
    eq(mbb[k], tbb[k], f'belowband.{k}')

for myname, theirname in (
        ('eleventh_tail_supply_identity_recheck',
         'eleventh_tail_supply_identity_recheck'),
        ('twelfth_tail_supply_identity_precalc',
         'twelfth_tail_supply_identity_recheck')):
    a = msec[myname][0]
    b = tsec[theirname][0]
    eq(a['identity'], b['identity'], f'{myname}.identity')
    for key in ('hold_rows', 'break_rows'):
        arows = [r for r in a[key] if r['s'] <= 56]
        brows = [r for r in b[key] if r['s'] <= 56]
        eq(len(arows), len(brows), f'{name}.{key}.shared_count')
        for r1, r2 in zip(arows, brows):
            cmp_rows += 1
            eq(r1, r2, f'{myname}.{key}[{r2["s"]}]')

print('COMPARE rows=%d field_checks=%d mismatches=%d' %
      (cmp_rows, cmp_fields, len(mismatch)))
for m in mismatch[:20]:
    print('MISMATCH', m)
sys.exit(0 if not mismatch else 1)
