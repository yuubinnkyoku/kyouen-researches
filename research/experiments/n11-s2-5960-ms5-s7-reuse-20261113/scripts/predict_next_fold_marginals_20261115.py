#!/usr/bin/env python3
"""Forward marginal prediction for the next unified merge, measured against
the published unified chain head 1154
(class-frontier-unified-merge-recompute-20261115.json).

Measured receipt groups (all verdicts already published on main, certificates
pending for the 69f group):
- cost-70c child 00000000000000803242000000000000, WIN7-D10 bits
  3/42/86/103 (uncertified warm rebuild candidates);
- cost-69f child 00000000000000809102000000000008, WIN7-D10 bits
  2/20/44/68/69/94/109/118/119 (sweep complete, certificates being
  published by that lane).

For each root (root == child | 1<<bit asserted) the manifest marginal
covers(root) - s_1154 is re-derived from the chain machinery. This is
bookkeeping arithmetic over published WIN7-D10 verdicts only - it does not
verify the certificates (that stays with the fold) and does not change any
verdict. WIN7-D10 proves only a win within depth 10 from the 7-stone root.
"""
import json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_unified_merge_20261115.py'))
covers = ns['covers']
manifest = ns['manifest']
s_1154 = set(ns['s_cur'])
assert ns['stU']['solved_s6_in_manifest'] == 1154

def measure(child_hex, bits, band):
    child_v = int(child_hex, 16)
    out = []
    for bit in bits:
        root_v = child_v | (1 << bit)
        cov = covers(root_v)
        marg = cov - s_1154
        mim = marg & manifest
        out.append({
            'band': band, 'bit': bit, 'child_hex': child_hex,
            'root_hex': f'{root_v:032x}',
            'covers': len(cov), 'marginal': len(marg),
            'marginal_in_manifest': len(mim),
            'marginal_manifest_hexes': sorted(f'{k:032x}' for k in mim),
        })
    return out

c70 = measure('00000000000000803242000000000000', (3, 42, 86, 103), 'class2-lane-cost70c')
c69 = measure('00000000000000809102000000000008',
              (2, 20, 44, 68, 69, 94, 109, 118, 119), 'class2-lane-cost69f')

# cross-child duplicate scan against all published receipt roots
recon = json.loads((HERE / 'output' / 'class2-lane-unified-fold-reconciliation-20261115.json').read_text())
recdoc2 = json.loads((HERE / 'output' / 'class2-lane-warm-multiband2-certificates-20261115.json').read_text())
certdoc68 = json.loads((HERE / 'output' / 'class2-lane-cost68d-win7-certificates-20261115.json').read_text())
hygdoc = json.loads((HERE / 'output' / 'class2-lane-warm-band-hygiene-certificates-20261115.json').read_text())
published_roots = {c['root_hex'] for c in certdoc68['certificates']}
published_roots |= {r['root_hex'] for r in hygdoc['records']}
published_roots |= {r['root_hex'] for r in recdoc2['records']}
published_roots |= {r['root_hex'] for r in recon['cost70c_warm_batch2_receipts']}
for r in c70 + c69:
    r['root_in_published_receipts'] = r['root_hex'] in published_roots

# ---------- union-based fold prediction (per-record growing-union simulation) ----------
c69_child_hex = '00000000000000809102000000000008'
s_pred = set(s_1154)
c69_growing = []
for r in c69:
    cov = covers(int(r['root_hex'], 16))
    marg = cov - s_pred
    mim = marg & manifest
    c69_growing.append({
        'bit': r['bit'],
        'marginal_in_manifest_at_fold': len(mim),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in mim),
    })
    s_pred |= marg
assert s_pred == s_1154 | set().union(*(covers(int(r['root_hex'], 16)) for r in c69))
distinct_hexes = sorted({h for r in c69_growing for h in r['marginal_manifest_hexes']})
assert len(distinct_hexes) == sum(r['marginal_in_manifest_at_fold'] for r in c69_growing)

summary_state = ns['summary_state']
classes = ns['classes']
stP, remP, uniqP, demP = summary_state(s_pred)
def target(s5_hex):
    rows = remP.get(s5_hex, [])
    return {'s5_hex': s5_hex, 'classes': classes.get(s5_hex, 0),
            'remaining_s6_orbits': len(rows),
            'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
THIRD = '00000000000000809102000000000000'
AUDIT_BLOCKED = '00000000000000809082000000000000'
BEST_CLASS4 = '00000000020000003800000080000000'

result = {
    'schema': 'class2-lane-next-fold-marginal-prediction-20261115-v2',
    'date': '2026-11-15',
    'baseline': 'class-frontier-unified-merge-recompute-20261115 (chain head 1154 / 6693 / 527949 / 4963 / 391672)',
    'method': 'marginal-in-manifest re-derivation from the chain covers() against the '
              'unified 1154 solved set; root identity root == child | 1<<bit asserted; '
              'bookkeeping over published WIN7-D10 verdicts only - certificates for the '
              '69f group are pending with that lane and must pass independent verification '
              'before the fold; the prediction folds the 69f receipts in bit order with '
              'per-record marginals re-derived from the growing union (the fold convention), '
              'so the predicted increment is the DISTINCT union of manifest marginals, not '
              'the per-record sum against the static baseline; root_in_published_receipts '
              'flags cross-child duplicates (positive cross-checks, never re-folded)',
    'cost70c_uncertified_bits': c70,
    'cost70c_finding': 'all four remaining WIN7-D10 bits (3/42/86/103) have marginal 0 '
                       'against the 1154 head (bits 3/103 fully pre-covered, bits 42/86 '
                       'cover only non-manifest orbits): extracting them completes the '
                       'cost-70c band certification (13/13) but advances NO manifest '
                       'orbit - gain-0 warm candidates under the current head',
    'cost69f_swept_bits': c69,
    'cost69f_fold_simulation': {
        'per_record_growing_union_marginals': c69_growing,
        'distinct_manifest_hexes': distinct_hexes,
        'predicted_solved_increment': len(distinct_hexes),
        'predicted_next_head_if_published_and_verified': {
            'solved_s6_in_manifest': stP['solved_s6_in_manifest'],
            'unique_remaining_s6': stP['unique_remaining_s6'],
            'sum_remaining_cost': stP['sum_remaining_cost'],
            's6_needed_by_open_classes': stP['s6_needed_by_open_classes'],
            'cost_needed_by_open_classes': stP['cost_needed_by_open_classes'],
        },
        'third_class2_target_effect': {
            'before': {'s5_hex': THIRD, 'remaining_s6_orbits': 8,
                       'remaining_s7_edge_cost': 588},
            'after_predicted': target(THIRD),
            'note': 'the swept child ' + c69_child_hex + ' leaves remaining membership; '
                    'the cheapest remaining unswept child of the third target becomes '
                    '00000000000000809102000000002000 (cost 69, c1=0,c2=2,c4=2)',
        },
        'audit_blocked_class2_predicted': target(AUDIT_BLOCKED),
        'best_class4_predicted': target(BEST_CLASS4),
    },
    'interpretation_guard': 'solved counts measure manifest coverage, not the '
                            'game-theoretic value of the 11x11 empty board; WIN7-D10 '
                            'proves only a win within depth 10 from the 7-stone root; '
                            'the prediction is conditional on publication and independent '
                            'verification of the pending 69f certificates; 11x11 empty '
                            'root / {49,60} / S2 {59,60} / class 2 / class 4 remain '
                            'UNKNOWN',
}
out = HERE / 'output' / 'class2-lane-next-fold-marginal-prediction-20261115.json'
out.write_text(json.dumps(result, indent=1) + chr(10))
print('cost-70c remaining 4 bits:')
for r in c70:
    print(' bit', r['bit'], 'covers', r['covers'], 'marginal', r['marginal'],
          'in_manifest', r['marginal_in_manifest'],
          'dup' if r['root_in_published_receipts'] else '')
print('cost-69f 9 bits (static 1154 baselines):')
for r in c69:
    print(' bit', r['bit'], 'covers', r['covers'], 'marginal', r['marginal'],
          'in_manifest', r['marginal_in_manifest'],
          'dup' if r['root_in_published_receipts'] else '')
print('cost-69f growing-union fold simulation:')
for r in c69_growing:
    print(' bit', r['bit'], 'in_manifest_at_fold', r['marginal_in_manifest_at_fold'],
          r['marginal_manifest_hexes'])
print('distinct manifest hexes:', len(distinct_hexes), distinct_hexes)
print('predicted next head:', json.dumps(stP))
print('third class2 target predicted:', target(THIRD))
print('audit-blocked predicted:', target(AUDIT_BLOCKED))
print('best class4 predicted:', target(BEST_CLASS4))
print('written', out.name)
