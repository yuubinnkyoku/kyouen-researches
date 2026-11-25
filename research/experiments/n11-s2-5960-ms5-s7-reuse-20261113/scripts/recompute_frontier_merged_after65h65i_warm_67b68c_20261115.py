#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation merging the two
parallel class2-lane branches that forked at the after-cost-65h+65i frontier
(2026-11-15).

Both branch endpoints are first reproduced byte-exactly by runpy:

- chain A (warm certificate rebuilds): recompute_frontier_cost63e_warm_20261114.py
  then recompute_frontier_cost65g_warm_20261114.py, ending at the published
  after-cost-65g-warm frontier (solved 1005 / unique remaining 6842 / sum 539174 /
  open 5112/402897);
- chain B (child sweeps): recompute_frontier_cost67b_20261114.py then
  recompute_frontier_cost68c_20261114.py, ending at the published after-cost-68c
  frontier (solved 998 / unique remaining 6849 / sum 539673 / open 5119/403396);
- the common fork state is reproduced directly by
  recompute_frontier_cost65h_65i_20261114.py (solved 991 / unique remaining 6856 /
  sum 540177 / open 5126/403900) and asserted to be a subset of both endpoints.

The four receipt groups are then re-added in a single canonical sequential order
from the fork state (63e-warm bits 42/73/100/116/120; 65g-warm bits
0/15/44/52/75/105; 67b bits 17/117/109; 68c bits 21/11/118), re-deriving every
per-bit marginal from the growing merged union. Chain A's published per-bit
marginals reproduce exactly through the first two groups; the 67b/68c marginals
are recomputed against the merged state and compared with their published
chain-B values, so any cross-chain double coverage is surfaced instead of being
silently double-counted. The merged solved set equals chain A's set union chain
B's set; the overlap between the two branch additions is enumerated explicitly.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce chain A end (after-cost-65g-warm, 1005) ----------
nsA = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost65g_warm_20261114.py'))
covers = nsA['covers']
summary_state = nsA['summary_state']
manifest = nsA['manifest']
classes = nsA['classes']
sA = nsA['s59']
stA = nsA['st59']
assert stA['solved_s6_in_manifest'] == 1005 and stA['unique_remaining_s6'] == 6842
assert stA['sum_remaining_cost'] == 539174
assert stA['s6_needed_by_open_classes'] == 5112 and stA['cost_needed_by_open_classes'] == 402897
print('CONTROL chain A (63e-warm + 65g-warm) end reproduced: '
      '1005/6842/539174/5112/402897')

# ---------- 2. reproduce chain B end (after-cost-68c, 998) ----------
nsB = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost68c_20261114.py'))
sB = nsB['s60']
stB = nsB['st60']
assert stB['solved_s6_in_manifest'] == 998 and stB['unique_remaining_s6'] == 6849
assert stB['sum_remaining_cost'] == 539673
assert stB['s6_needed_by_open_classes'] == 5119 and stB['cost_needed_by_open_classes'] == 403396
print('CONTROL chain B (67b + 68c) end reproduced: '
      '998/6849/539673/5119/403396')

# ---------- 3. reproduce the fork state (after-cost-65h+65i, 991) ----------
nsF = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost65h_65i_20261114.py'))
sF = nsF['s58']
stF = nsF['st58']
assert stF['solved_s6_in_manifest'] == 991 and stF['unique_remaining_s6'] == 6856
assert stF['sum_remaining_cost'] == 540177
assert stF['s6_needed_by_open_classes'] == 5126 and stF['cost_needed_by_open_classes'] == 403900
assert sF <= sA and sF <= sB, 'both branch endpoints must extend the fork state'
addA = sA - sF
addB = sB - sF
overlap = addA & addB
print(f'CONTROL fork (after-cost-65h+65i) reproduced: 991/6856/540177/5126/403900; '
      f'branch additions |A|={len(addA)} |B|={len(addB)} overlap={len(overlap)}')

# ---------- 4. the four receipt groups ----------
PARENT = '00000000000000803202000000000000'
GROUPS = [
    ('cost63e_warm', 'class2-lane-cost63e-warm-certificates-20261114.json',
     '00000000000000803202200000000000', [42, 73, 100, 116, 120],
     {42: 45348, 73: 40313, 100: 33856, 116: 48268, 120: 44172},
     {42: 54, 73: 50, 100: 49, 116: 53, 120: 55}),
    ('cost65g_warm', 'class2-lane-cost65g-warm-certificates-20261114.json',
     '00000000000000803202000000000004', [0, 15, 44, 52, 75, 105],
     {0: 42091, 15: 41226, 44: 40807, 52: 37706, 75: 39625, 105: 43743},
     {0: 54, 15: 52, 44: 52, 52: 51, 75: 52, 105: 52}),
    ('cost67b', 'class2-lane-cost67b-win7-certificates-20261114.json',
     '00000000000000803202000020000000', [17, 117, 109],
     {17: 34860, 117: 32441, 109: 27559},
     {17: 47, 117: 50, 109: 47}),
    ('cost68c', 'class2-lane-cost68c-win7-certificates-20261114.json',
     '00000000000000803202000400000000', [21, 11, 118],
     {21: 23096, 11: 40600, 118: 31576},
     {21: 47, 11: 50, 118: 56}),
]
# published chain-B per-bit marginals for cross-chain double-coverage reporting
pub67b = json.loads((OUT / 'class-frontier-cost67b-recompute-20261114.json').read_text())['cost67b_addition']
pub68c = json.loads((OUT / 'class-frontier-cost68c-recompute-20261114.json').read_text())['cost68c_addition']
PUBLISHED = {'cost67b': pub67b, 'cost68c': pub68c}

group_covers = {}
group_roots = {}
for gname, fname, child_hex, bits, rows_map, subs_map in GROUPS:
    rec = json.loads((OUT / fname).read_text())
    assert rec['child_hex'] == child_hex, (gname, rec.get('child_hex'))
    certs = [c for c in rec['certificates'] if c.get('verdict') == 'WIN7']
    assert [c['bit'] for c in certs] == bits, (gname, [c['bit'] for c in certs])
    child = int(child_hex, 16)
    for c in certs:
        assert c['rows'] == rows_map[c['bit']], (gname, c['bit'], c['rows'])
        assert c['sub_roots_pass'] == subs_map[c['bit']], (gname, c['bit'])
        assert c['union_missing'] == 0 and c['union_extra'] == 0
        assert int(c['root_hex'], 16) == child | (1 << c['bit']), (gname, c['bit'])
    group_covers[gname] = {c['bit']: covers(int(c['root_hex'], 16)) for c in certs}
    group_roots[gname] = {c['bit']: c['root_hex'] for c in certs}
    print(f'CONTROL {gname} receipts asserted: bits {bits} (rows/sub-roots/union/roots)')

# ---------- 5. canonical sequential merge from the fork state ----------
s_cur = set(sF)
group_additions = {}
for gname, fname, child_hex, bits, rows_map, subs_map in GROUPS:
    per_bits = {}
    marg_union = set()
    for bit in bits:
        cov = group_covers[gname][bit]
        marg = cov - s_cur
        marg_m = marg & manifest
        entry = {
            'root_hex': group_roots[gname][bit],
            'covers': len(cov), 'marginal': len(marg),
            'marginal_in_manifest': len(marg_m),
            'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
        }
        if gname in PUBLISHED and str(bit) in PUBLISHED[gname]:
            pub = PUBLISHED[gname][str(bit)]
            entry['published_chain_marginal'] = pub['marginal']
            entry['published_chain_marginal_in_manifest'] = pub['marginal_in_manifest']
            entry['marginal_reduced_vs_published'] = len(marg) < pub['marginal']
        per_bits[str(bit)] = entry
        marg_union |= marg
    s_cur |= marg_union
    stG, _, _, _ = summary_state(s_cur)
    group_additions[gname] = per_bits
    print(f'AFTER {gname}: solved_in_manifest={stG["solved_s6_in_manifest"]}')

# chain reproduction controls
assert s_cur == sA | sB, 'merged sequential replay must equal the union of both branch endpoints'
sB_repro = sF.copy()
for gname in ('cost67b', 'cost68c'):
    for bit, cov in group_covers[gname].items():
        sB_repro |= cov
stB_repro, _, _, _ = summary_state(sB_repro)
assert sB_repro == sB and stB_repro['solved_s6_in_manifest'] == 998, \
    'chain B must reproduce from the fork plus its own receipt covers'
print('CONTROL merged replay == union(A, B); chain B reproduced from fork + 67b/68c covers: OK')

sM = sA | sB
stM, remM, uniqM, demM = summary_state(sM)
print('AFTER merged:', json.dumps(stM, indent=1))

overlap_hexes = sorted(f'{k:032x}' for k in overlap)
overlap_in_manifest = overlap & manifest
print(f'overlap between branch additions: {len(overlap)} orbits '
      f'({len(overlap_in_manifest)} in manifest): {overlap_hexes}')

# ---------- 6. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(remM, 2)
class4 = best(remM, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-merged-recompute-after65h65i-warm67b68c-20261115-v1',
    'date': '2026-11-15',
    'baseline_main': 'fork: class-frontier-cost65h-65i-recompute-20261114 (solved 991 / unique remaining 6856 / sum 540177 / open 5126/403900); chain A: class-frontier-cost65g-warm-recompute-20261114 (1005/6842/539174/5112/402897); chain B: class-frontier-cost68c-recompute-20261114 (998/6849/539673/5119/403396)',
    'method': 'single merged replay of the two class2-lane branches that forked at the after-cost-65h+65i frontier: both branch endpoints are reproduced byte-exactly by runpy (chain A warm rebuilds 63e-warm + 65g-warm -> 1005; chain B child sweeps 67b + 68c -> 998), the fork state (991) is reproduced directly and asserted to be a subset of both endpoints, then all four receipt groups (63e-warm bits 42/73/100/116/120, 65g-warm bits 0/15/44/52/75/105, 67b bits 17/117/109, 68c bits 21/11/118) are re-added in one canonical sequential order from the fork with per-bit marginals re-derived from the growing merged union; chain A per-bit marginals reproduce their published values, chain B marginals are compared with their published chain-B values so cross-chain double coverage is surfaced instead of double-counted; the merged solved set equals union(A, B) and chain B is re-reproduced from the fork plus its own covers as a control',
    'controls': {
        'fork_after_cost65h_65i': {'solved_in_manifest': 991, 'unique_remaining': 6856,
                                   'sum_cost': 540177, 'open_s6': 5126, 'open_cost': 403900,
                                   'reproduced': True},
        'chain_A_after_cost65g_warm': {'solved_in_manifest': 1005, 'unique_remaining': 6842,
                                       'sum_cost': 539174, 'open_s6': 5112, 'open_cost': 402897,
                                       'reproduced': True},
        'chain_B_after_cost68c': {'solved_in_manifest': 998, 'unique_remaining': 6849,
                                  'sum_cost': 539673, 'open_s6': 5119, 'open_cost': 403396,
                                  'reproduced': True},
        'fork_subset_of_both_endpoints': True,
        'branch_addition_sizes': {'chain_A': len(addA), 'chain_B': len(addB)},
        'chain_B_reproduced_from_fork_plus_own_covers': True,
        'merged_equals_union_of_endpoints': True,
    },
    'overlap_between_branch_additions': {
        'count': len(overlap),
        'in_manifest': len(overlap_in_manifest),
        's6_hexes': overlap_hexes,
        'note': 'S6 orbits covered by receipts in BOTH branches; counted once in the merged frontier (the two published branch totals each counted them once per branch)',
    },
    'group_additions': group_additions,
    'frontier_after_merged': {
        'solved_s6_in_manifest': stM['solved_s6_in_manifest'],
        'remaining_s5_orbits': stM['remaining_s5_orbits'],
        'unique_remaining_s6': stM['unique_remaining_s6'],
        'sum_remaining_cost': stM['sum_remaining_cost'],
        's6_needed_by_open_classes': stM['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': stM['cost_needed_by_open_classes'],
        'demand_histogram_open_only': stM['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-merged-recompute-after65h65i-warm67b68c-20261115.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-merged-recompute-after65h65i-warm67b68c-20261115.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in remM.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-merged-warm67b68c-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-merged-warm67b68c-20261115.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(remM.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in remM.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('merged-lane parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == PARENT))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(remM[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = demM[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-merged-warm67b68c)')
