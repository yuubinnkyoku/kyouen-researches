#!/usr/bin/env python3
"""Machine crosscheck of the two independent published-fold-chain root
audit implementations at all eight endpoint pairs (2026-11-15).

The first implementation (v1 line, audit_published_chain_roots_independent_
20261115.py, published outputs schema v3/v4/v5/v6/v7/v8/v9) and the second
implementation
(v2/v4/v5/v6/v7/v8 line, audit_published_chain_roots_second_independent_20261115.py /
..._v4_20261115.py / ..._v5_20261115.py / ..._v6_20261115.py /
..._v7_20261115.py / ..._v8_20261115.py / ..._v9_20261115.py, published
outputs schema v2/v4/v5/v6/v7/v8/v9)
were developed independently and both pass every control over the same
published corpus. This third script pins that agreement mechanically: it
re-reads the fourteen published audit JSONs (blob-pinned below) and
asserts that every shared control agrees at all eight endpoint pairs:

  75d endpoint pair: v3 (first impl)  vs  v2 (second impl)
  80d endpoint pair: v4 (first impl)  vs  v4 (second impl)
  82c endpoint pair: v5 (first impl)  vs  v5 (second impl)
  83a endpoint pair: v6 (first impl)  vs  v6 (second impl)
  83b/83c endpoint pair: v7 (first impl)  vs  v7 (second impl)
  83d endpoint pair: v8 (first impl)  vs  v8 (second impl)
  84a/62a endpoint pair: v9 (first impl)  vs  v9 (second impl)

Checked per endpoint pair:
  1. cumulative_by_post70e_head: same head sequence and same per-head
     fields (roots_in_head, new_orbits_added, both cumulatives, own-branch
     baseline, published own claim, matches_published)
  2. d4_orbits roots/orbits/twin_pairs
  3. per_record_geometry receipt/group record counts, anomaly counts and
     published hex errata counts
  4. head_arithmetic: head counts, classification counts, quote status
     counts, anomaly/erratum/pointer-differs counts
  5. canonical_line_hex_exactly_once: baseline/endpoint/mim/distinct/multi
  6. convention_external_receipts: full record equality
  7. child_closure: full record equality
  8. base_roots / chain_head_roots / inventory_at_1233: full equality
  9. endpoint head records (75d / 80d / 82c / 83a / 83b / 83c / 83d /
     84a / 62a): full
     numeric record equality
 10. (80d/82c) bit-78 duplicate-root bookkeeping: identical root hex
 11. pins_checked: base and chain pin groups must be equal; the post-70e
     count difference must equal exactly the four v2 pin proposals
     (71c/70f/73g/70g) that only the first implementation pins

The audit asserts; on success it writes the agreement JSON. Running it
twice must produce byte-identical output (deterministic ordering
throughout). Bookkeeping crosscheck only - no sweep, no solved-set
reconstruction, and no game-theoretic claim: 11x11 empty board / two-stone
root {49,60} / S2 {59,60} / class 1 / class 2 / class 4 all remain
UNKNOWN.
"""
import hashlib, json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'


def git_blob_sha(path):
    data = Path(path).read_bytes()
    return hashlib.sha1(b'blob %d\0' % len(data) + data).hexdigest()


AUDIT_PINS = {
    'class2-lane-published-chain-roots-independent-audit-20261115.json':
        '9ae579545b463e30dfa54bc44cd1fbc41b31e670',
    'class2-lane-published-chain-roots-independent-audit-v2-20261115.json':
        'db0916c0ecb64a475537bc0ac9028c73dd3f5294',
    'class2-lane-published-chain-roots-independent-audit-v4-20261115.json':
        'c3df2d1e5d4a4c698b9c8bcc401182524d93f218',
    'class2-lane-published-chain-roots-second-independent-audit-v4-20261115.json':
        'e3a0b7da0a7b1e59137bc4bf5f82ce3e8892a59d',
    'class2-lane-published-chain-roots-independent-audit-v5-20261115.json':
        'd648ed70e8ccafea0ab3cdafe8a3e9cb494f85c7',
    'class2-lane-published-chain-roots-second-independent-audit-v5-20261115.json':
        'af86251aa390c4835e56d2948f69b5504d9921a8',
    'class2-lane-published-chain-roots-independent-audit-v6-20261115.json':
        'e231b79a037ce1b66b4501a241ce12b8c4f24a04',
    'class2-lane-published-chain-roots-second-independent-audit-v6-20261115.json':
        '075723e594af4744d1fe7b4b09a9b2bb8ec7d449',
    'class2-lane-published-chain-roots-independent-audit-v7-20261115.json':
        '76d42c03436016c89e34cf263412894cb0508a71',
    'class2-lane-published-chain-roots-second-independent-audit-v7-20261115.json':
        'cc8301f4936572b23f051737679f0d30ae05465b',
    'class2-lane-published-chain-roots-independent-audit-v8-20261115.json':
        '232e9d6b930e300402e8191aaf20ac1c40a70e45',
    'class2-lane-published-chain-roots-second-independent-audit-v8-20261115.json':
        'ad1261bd563f7f524553a8d07fcb8b7f6da92722',
    'class2-lane-published-chain-roots-independent-audit-v9-20261115.json':
        'c199accf70737250c1484a328eee6e6b51bf0196',
    'class2-lane-published-chain-roots-second-independent-audit-v9-20261115.json':
        'c9c1eb07359510eed083de3f7271fe2319c9ebc9',
}
for name, want in sorted(AUDIT_PINS.items()):
    s = git_blob_sha(OUT / name)
    assert s == want, ('audit pin', name, s, want)


def load(name):
    return json.loads((OUT / name).read_text())


v3 = load('class2-lane-published-chain-roots-independent-audit-20261115.json')
v2 = load('class2-lane-published-chain-roots-independent-audit-v2-20261115.json')
v4f = load('class2-lane-published-chain-roots-independent-audit-v4-20261115.json')
v4s = load('class2-lane-published-chain-roots-second-independent-audit-v4-20261115.json')
v5f = load('class2-lane-published-chain-roots-independent-audit-v5-20261115.json')
v5s = load('class2-lane-published-chain-roots-second-independent-audit-v5-20261115.json')
v6f = load('class2-lane-published-chain-roots-independent-audit-v6-20261115.json')
v6s = load('class2-lane-published-chain-roots-second-independent-audit-v6-20261115.json')
v7f = load('class2-lane-published-chain-roots-independent-audit-v7-20261115.json')
v7s = load('class2-lane-published-chain-roots-second-independent-audit-v7-20261115.json')
v8f = load('class2-lane-published-chain-roots-independent-audit-v8-20261115.json')
v8s = load('class2-lane-published-chain-roots-second-independent-audit-v8-20261115.json')
v9f = load('class2-lane-published-chain-roots-independent-audit-v9-20261115.json')
v9s = load('class2-lane-published-chain-roots-second-independent-audit-v9-20261115.json')

assert v3['schema'] == 'n11-class2-lane-published-chain-roots-independent-audit-20261115-v3'
assert v2['schema'] == 'n11-class2-lane-published-chain-roots-independent-audit-20261115-v2'
assert v4f['schema'] == 'n11-class2-lane-published-chain-roots-independent-audit-20261115-v4'
assert v4s['schema'] == 'n11-class2-lane-published-chain-roots-second-independent-audit-20261115-v4'
assert v5f['schema'] == 'n11-class2-lane-published-chain-roots-independent-audit-20261115-v5'
assert v5s['schema'] == 'n11-class2-lane-published-chain-roots-second-independent-audit-20261115-v5'
assert v6f['schema'] == 'n11-class2-lane-published-chain-roots-independent-audit-20261115-v6'
assert v6s['schema'] == 'n11-class2-lane-published-chain-roots-second-independent-audit-20261115-v6'
assert v7f['schema'] == 'n11-class2-lane-published-chain-roots-independent-audit-20261115-v7'
assert v7s['schema'] == 'n11-class2-lane-published-chain-roots-second-independent-audit-20261115-v7'
assert v8f['schema'] == 'n11-class2-lane-published-chain-roots-independent-audit-20261115-v8'
assert v8s['schema'] == 'n11-class2-lane-published-chain-roots-second-independent-audit-20261115-v8'
assert v9f['schema'] == 'n11-class2-lane-published-chain-roots-independent-audit-20261115-v9'
assert v9s['schema'] == 'n11-class2-lane-published-chain-roots-second-independent-audit-20261115-v9'
for d in (v3, v2, v4f, v4s, v5f, v5s, v6f, v6s, v7f, v7s, v8f, v8s,
          v9f, v9s):
    assert d['verdict'] == 'AUDIT PASSED', d['schema']


def controls(d):
    return d['controls']


def crosscheck(tag, a, b):
    """Assert that every shared control agrees between the two
    implementation outputs a (first impl) and b (second impl)."""
    ca, cb = controls(a), controls(b)
    report = {}

    # 1. cumulative bookkeeping: identical head sequence and per-head rows
    cum_a = ca['cumulative_by_post70e_head']
    cum_b = cb['cumulative_by_post70e_head']
    assert [e['head'] for e in cum_a] == [e['head'] for e in cum_b], tag
    for ea, eb in zip(cum_a, cum_b):
        assert ea == eb, (tag, ea['head'])
    report['cumulative_heads'] = len(cum_a)
    report['cumulative_final_document_order'] = cum_a[-1]['audit_document_order_cumulative']
    report['cumulative_final_own_branch'] = cum_a[-1]['fold_own_branch_cumulative']

    # 2. D4 orbit structure
    for key in ('roots', 'orbits', 'twin_pairs'):
        assert ca['d4_orbits'][key] == cb['d4_orbits'][key], (tag, key)
    report['d4'] = {k: ca['d4_orbits'][k] for k in ('roots', 'orbits', 'twin_pairs')}

    # 3. per-record geometry
    ga, gb = ca['per_record_geometry'], cb['per_record_geometry']
    assert ga['receipt_records'] == gb['receipt_records'], tag
    assert ga['group_records'] == gb['group_records'], tag
    assert len(ga['anomalies']) == len(gb['anomalies']) == 0, tag
    assert ga['published_hex_errata'] == gb['published_hex_errata'], tag
    report['geometry'] = {'receipt_records': ga['receipt_records'],
                          'group_records': ga['group_records'],
                          'anomalies': 0,
                          'published_hex_errata': ga['published_hex_errata']}

    # 4. head arithmetic
    ha, hb = ca['head_arithmetic'], cb['head_arithmetic']
    assert len(ha['heads']) == len(hb['heads']), tag
    assert ha['classification_counts'] == hb['classification_counts'], tag
    assert ha['quote_status_counts'] == hb['quote_status_counts'], tag
    assert len(ha['anomalies']) == len(hb['anomalies']) == 0, tag
    assert ha['quote_errata'] == hb['quote_errata'], tag
    assert ha['pointer_name_differs_cases'] == hb['pointer_name_differs_cases'], tag
    report['arith'] = {'heads': len(ha['heads']),
                       'classification_counts': ha['classification_counts'],
                       'quote_status_counts': ha['quote_status_counts'],
                       'anomalies': 0,
                       'quote_errata': ha['quote_errata'],
                       'pointer_name_differs_cases': ha['pointer_name_differs_cases']}

    # 5. canonical line exactly-once
    na, nb = ca['canonical_line_hex_exactly_once'], cb['canonical_line_hex_exactly_once']
    for key in ('baseline_solved', 'endpoint_solved', 'total_mim',
                'distinct_marginal_hexes', 'multi_claims'):
        assert na[key] == nb[key], (tag, key)
    report['canonical_line'] = {k: na[k] for k in
                                ('baseline_solved', 'endpoint_solved',
                                 'total_mim', 'distinct_marginal_hexes',
                                 'multi_claims')}

    # 6. convention-external receipts: full record equality
    ext_a = ca['convention_external_receipts']
    ext_b = cb['convention_external_receipts']
    assert ext_a == ext_b, (tag, ext_a, ext_b)
    report['convention_external_receipts'] = ext_a

    # 7. child-closure bookkeeping: full record equality
    ch_a = ca['child_closure']
    ch_b = cb['child_closure']
    assert ch_a == ch_b, tag
    report['child_closure_heads'] = len(ch_a)

    # 8. base / chain / baseline inventory
    assert ca['base_roots'] == cb['base_roots'], tag
    assert ca['chain_head_roots'] == cb['chain_head_roots'], tag
    assert ca['inventory_at_1233'] == cb['inventory_at_1233'], tag
    report['base_roots_distinct'] = ca['base_roots']['distinct']
    report['chain_head_roots_distinct'] = ca['chain_head_roots']['distinct']
    report['inventory_at_1233'] = ca['inventory_at_1233']

    # 11. pins: base/chain groups equal; post-70e delta == the four
    #     v2 pin proposals (71c/70f/73g/70g) that only the first
    #     implementation pins
    pa, pb = ca['pin_groups'], cb['pin_groups']
    assert pa['base'] == pb['base'] == 26, (tag, pa, pb)
    assert pa['chain'] == pb['chain'] == 52, (tag, pa, pb)
    assert pa['post70e'] - pb['post70e'] == 4, (tag, pa, pb)
    report['pins'] = {
        'first_implementation': ca['pins_checked'], 'pin_groups': pa,
        'second_implementation': cb['pins_checked'], 'pin_groups_2': pb,
        'post70e_delta': 'exactly the four v2 pin proposals '
                         '(71c/70f/73g/70g) pinned only by the first '
                         'implementation; the audited corpus endpoints '
                         'agree',
    }
    return report


pair_75d = crosscheck('75d', v3, v2)

# 9. 75d endpoint record
ep75_a = controls(v3)['endpoint_heads']['endpoint_cost75d']
ep75_b = controls(v2)['endpoint_75d']
assert ep75_a == ep75_b, '75d endpoint record'
pair_75d['endpoint_75d'] = ep75_a

# 80d pair
pair_80d = crosscheck('80d', v4f, v4s)
ep80_a = controls(v4f)['endpoint_heads']['endpoint_cost80d']
ep80_b = controls(v4s)['endpoint_80d']
assert ep80_a == ep80_b, '80d endpoint record'
pair_80d['endpoint_80d'] = ep80_a

# 10. bit-78 duplicate-root bookkeeping: identical root hex
b78_a = controls(v4f)['bit78_duplicate_root_bookkeeping']['root_hex']
b78_b = controls(v4s)['bit78_duplicate_root_bookkeeping']['root_hex']
assert b78_a == b78_b, (b78_a, b78_b)
pair_80d['bit78_root_hex'] = b78_a

# 82c pair
pair_82c = crosscheck('82c', v5f, v5s)
ep82_a = controls(v5f)['endpoint_heads']['endpoint_cost82c']
ep82_b = controls(v5s)['endpoint_82c']
assert ep82_a == ep82_b, '82c endpoint record'
pair_82c['endpoint_82c'] = ep82_a
b78_a5 = controls(v5f)['bit78_duplicate_root_bookkeeping']['root_hex']
b78_b5 = controls(v5s)['bit78_duplicate_root_bookkeeping']['root_hex']
assert b78_a5 == b78_b5 == b78_a, (b78_a5, b78_b5, b78_a)
pair_82c['bit78_root_hex'] = b78_a5

# 83a pair (v3)
pair_83a = crosscheck('83a', v6f, v6s)
ep83_a = controls(v6f)['endpoint_heads']['endpoint_cost83a']
ep83_b = controls(v6s)['endpoint_83a']
assert ep83_a == ep83_b, '83a endpoint record'
pair_83a['endpoint_83a'] = ep83_a
b78_a6 = controls(v6f)['bit78_duplicate_root_bookkeeping']['root_hex']
b78_b6 = controls(v6s)['bit78_duplicate_root_bookkeeping']['root_hex']
assert b78_a6 == b78_b6 == b78_a, (b78_a6, b78_b6, b78_a)
pair_83a['bit78_root_hex'] = b78_a6

# 83b/83c pair (v4): the v7 outputs extend the pinned chain through the
# cost-83b (1309 -> 1312) and cost-83c (1312 -> 1313) folds
pair_83c = crosscheck('83c', v7f, v7s)
ep83b_a = controls(v7f)['endpoint_heads']['endpoint_cost83b']
ep83b_b = controls(v7s)['endpoint_83b']
assert ep83b_a == ep83b_b, '83b endpoint record'
pair_83c['endpoint_83b'] = ep83b_a
ep83c_a = controls(v7f)['endpoint_heads']['endpoint_cost83c']
ep83c_b = controls(v7s)['endpoint_83c']
assert ep83c_a == ep83c_b, '83c endpoint record'
pair_83c['endpoint_83c'] = ep83c_a
b78_a7 = controls(v7f)['bit78_duplicate_root_bookkeeping']['root_hex']
b78_b7 = controls(v7s)['bit78_duplicate_root_bookkeeping']['root_hex']
assert b78_a7 == b78_b7 == b78_a, (b78_a7, b78_b7, b78_a)
pair_83c['bit78_root_hex'] = b78_a7

# 83d pair (v8): the v8 outputs extend the pinned chain through the
# cost-83d (1313 -> 1314) fold
pair_83d = crosscheck('83d', v8f, v8s)
ep83d_a = controls(v8f)['endpoint_heads']['endpoint_cost83d']
ep83d_b = controls(v8s)['endpoint_83d']
assert ep83d_a == ep83d_b, '83d endpoint record'
pair_83d['endpoint_83d'] = ep83d_a
b78_a8 = controls(v8f)['bit78_duplicate_root_bookkeeping']['root_hex']
b78_b8 = controls(v8s)['bit78_duplicate_root_bookkeeping']['root_hex']
assert b78_a8 == b78_b8 == b78_a, (b78_a8, b78_b8, b78_a)
pair_83d['bit78_root_hex'] = b78_a8

# 84a/62a pair (v9): the v9 outputs extend the pinned chain through the
# cost-84a (1314 -> 1318) and cost-62a (1318 -> 1326) folds
pair_84a62a = crosscheck('84a/62a', v9f, v9s)
ep84a_a = controls(v9f)['endpoint_heads']['endpoint_cost84a']
ep84a_b = controls(v9s)['endpoint_84a']
assert ep84a_a == ep84a_b, '84a endpoint record'
pair_84a62a['endpoint_84a'] = ep84a_a
ep62a_a = controls(v9f)['endpoint_heads']['endpoint_cost62a']
ep62a_b = controls(v9s)['endpoint_62a']
assert ep62a_a == ep62a_b, '62a endpoint record'
pair_84a62a['endpoint_62a'] = ep62a_a
b78_a9 = controls(v9f)['bit78_duplicate_root_bookkeeping']['root_hex']
b78_b9 = controls(v9s)['bit78_duplicate_root_bookkeeping']['root_hex']
assert b78_a9 == b78_b9 == b78_a, (b78_a9, b78_b9, b78_a)
pair_84a62a['bit78_root_hex'] = b78_a9

# endpoint progression sanity across the two audits of each implementation
assert pair_75d['d4']['roots'] == 569 and pair_80d['d4']['roots'] == 587
assert pair_82c['d4']['roots'] == 592 and pair_83a['d4']['roots'] == 596
assert pair_83c['d4']['roots'] == 603 and pair_83d['d4']['roots'] == 606
assert pair_84a62a['d4']['roots'] == 616
assert pair_75d['canonical_line']['endpoint_solved'] == 1296
assert pair_80d['canonical_line']['endpoint_solved'] == 1305
assert pair_82c['canonical_line']['endpoint_solved'] == 1306
assert pair_83a['canonical_line']['endpoint_solved'] == 1309
assert pair_83c['canonical_line']['endpoint_solved'] == 1313
assert pair_83d['canonical_line']['endpoint_solved'] == 1314
assert pair_84a62a['canonical_line']['endpoint_solved'] == 1326
assert pair_75d['cumulative_heads'] == 17 and pair_80d['cumulative_heads'] == 21
assert pair_82c['cumulative_heads'] == 22 and pair_83a['cumulative_heads'] == 23
assert pair_83c['cumulative_heads'] == 25 and pair_83d['cumulative_heads'] == 26
assert pair_84a62a['cumulative_heads'] == 28
assert pair_75d['child_closure_heads'] == 24 and pair_80d['child_closure_heads'] == 28
assert pair_82c['child_closure_heads'] == 29 and pair_83a['child_closure_heads'] == 30
assert pair_83c['child_closure_heads'] == 32 and pair_83d['child_closure_heads'] == 33
assert pair_84a62a['child_closure_heads'] == 35
assert pair_80d['d4']['orbits'] == pair_80d['d4']['roots'] - 11
assert pair_82c['d4']['orbits'] == pair_82c['d4']['roots'] - 11
assert pair_83a['d4']['orbits'] == pair_83a['d4']['roots'] - 11
assert pair_83c['d4']['orbits'] == pair_83c['d4']['roots'] - 11
assert pair_83d['d4']['orbits'] == pair_83d['d4']['roots'] - 11
assert pair_84a62a['d4']['orbits'] == pair_84a62a['d4']['roots'] - 11

result = {
    'schema': 'n11-class2-lane-published-fold-chain-dual-implementation-agreement-20261115-v6',
    'date': '2026-11-15',
    'verdict': 'AGREEMENT CONFIRMED',
    'method': 'third, machine crosscheck of the two independently developed '
              'published-fold-chain root audit implementations over their '
              'fourteen published audit JSONs (blob-pinned): at all eight '
              'endpoint pairs (75d, 80d, 82c, 83a, 83b/83c, 83d and '
              '84a/62a), the '
              'cumulative per-head '
              'bookkeeping (sequence and all fields), D4 orbit structure, '
              'per-record geometry counts and errata, head arithmetic '
              'classification/quote/anomaly counts, canonical-line '
              'exactly-once totals, convention-external receipts, '
              'child-closure bookkeeping, base/chain/baseline inventory '
              'and the endpoint head records agree exactly; the pin count '
              'difference is exactly the four v2 pin proposals pinned only '
              'by the first implementation; at the 80d, 82c, 83a, 83b/83c '
              'and 83d endpoints the bit-78 duplicate-root bookkeeping '
              'reports the '
              'identical root',
    'inputs': {
        'audit_json_pins': AUDIT_PINS,
        'first_implementation_schemas': [v3['schema'], v4f['schema'],
                                         v5f['schema'], v6f['schema'],
                                         v7f['schema'], v8f['schema'],
                                         v9f['schema']],
        'second_implementation_schemas': [v2['schema'], v4s['schema'],
                                          v5s['schema'], v6s['schema'],
                                          v7s['schema'], v8s['schema'],
                                          v9s['schema']],
    },
    'pair_75d': pair_75d,
    'pair_80d': pair_80d,
    'pair_82c': pair_82c,
    'pair_83a': pair_83a,
    'pair_83c': pair_83c,
    'pair_83d': pair_83d,
    'pair_84a62a': pair_84a62a,
    'supersedes': 'class2-lane-published-fold-chain-dual-implementation-'
                  'agreement-v5-20261115.json (schema v5, 75d + 80d + 82c + '
                  '83a + 83b/83c + 83d endpoint pairs); this v6 output adds '
                  'the 84a/62a endpoint pair (first-impl v9 vs second-impl '
                  'v9, both extending the pinned chain through the cost-84a '
                  'and cost-62a folds to the 1326 endpoint; 106 vs 102 pins, '
                  '28 post-70e heads each, 616 roots / 605 orbits / 11 twin '
                  'pairs); the v5 file remains published unchanged',
    'interpretation_guard': 'bookkeeping agreement crosscheck over '
                            'published audit outputs only; solved counts '
                            'measure manifest coverage, not the '
                            'game-theoretic value of any position; '
                            'nothing here decides any S5 parent, any '
                            'class, the two-stone root {49,60} or the '
                            '11x11 empty board: 11x11 empty board / '
                            'two-stone root {49,60} / S2 {59,60} / class '
                            '1 / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class2-lane-published-fold-chain-dual-implementation-agreement-v6-20261115.json').write_text(
    json.dumps(result, indent=1, sort_keys=True) + '\n')
print('AGREEMENT CONFIRMED')
print('75d pair: %d heads / %d roots / %d orbits / %d twins / canon %d..%d mim %d'
      % (pair_75d['cumulative_heads'], pair_75d['d4']['roots'],
         pair_75d['d4']['orbits'], pair_75d['d4']['twin_pairs'],
         pair_75d['canonical_line']['baseline_solved'],
         pair_75d['canonical_line']['endpoint_solved'],
         pair_75d['canonical_line']['total_mim']))
print('80d pair: %d heads / %d roots / %d orbits / %d twins / canon %d..%d mim %d / bit78 %s'
      % (pair_80d['cumulative_heads'], pair_80d['d4']['roots'],
         pair_80d['d4']['orbits'], pair_80d['d4']['twin_pairs'],
         pair_80d['canonical_line']['baseline_solved'],
         pair_80d['canonical_line']['endpoint_solved'],
         pair_80d['canonical_line']['total_mim'],
         pair_80d['bit78_root_hex']))
print('82c pair: %d heads / %d roots / %d orbits / %d twins / canon %d..%d mim %d / bit78 %s'
      % (pair_82c['cumulative_heads'], pair_82c['d4']['roots'],
         pair_82c['d4']['orbits'], pair_82c['d4']['twin_pairs'],
         pair_82c['canonical_line']['baseline_solved'],
         pair_82c['canonical_line']['endpoint_solved'],
         pair_82c['canonical_line']['total_mim'],
         pair_82c['bit78_root_hex']))
print('83a pair: %d heads / %d roots / %d orbits / %d twins / canon %d..%d mim %d / bit78 %s'
      % (pair_83a['cumulative_heads'], pair_83a['d4']['roots'],
         pair_83a['d4']['orbits'], pair_83a['d4']['twin_pairs'],
         pair_83a['canonical_line']['baseline_solved'],
         pair_83a['canonical_line']['endpoint_solved'],
         pair_83a['canonical_line']['total_mim'],
         pair_83a['bit78_root_hex']))
print('83c pair (83b+83c folds): %d heads / %d roots / %d orbits / %d twins / canon %d..%d mim %d / bit78 %s'
      % (pair_83c['cumulative_heads'], pair_83c['d4']['roots'],
         pair_83c['d4']['orbits'], pair_83c['d4']['twin_pairs'],
         pair_83c['canonical_line']['baseline_solved'],
         pair_83c['canonical_line']['endpoint_solved'],
         pair_83c['canonical_line']['total_mim'],
         pair_83c['bit78_root_hex']))
print('83d pair (83d fold): %d heads / %d roots / %d orbits / %d twins / canon %d..%d mim %d / bit78 %s'
      % (pair_83d['cumulative_heads'], pair_83d['d4']['roots'],
         pair_83d['d4']['orbits'], pair_83d['d4']['twin_pairs'],
         pair_83d['canonical_line']['baseline_solved'],
         pair_83d['canonical_line']['endpoint_solved'],
         pair_83d['canonical_line']['total_mim'],
         pair_83d['bit78_root_hex']))
print('84a/62a pair (84a + 62a folds): %d heads / %d roots / %d orbits / %d twins / canon %d..%d mim %d / bit78 %s'
      % (pair_84a62a['cumulative_heads'], pair_84a62a['d4']['roots'],
         pair_84a62a['d4']['orbits'], pair_84a62a['d4']['twin_pairs'],
         pair_84a62a['canonical_line']['baseline_solved'],
         pair_84a62a['canonical_line']['endpoint_solved'],
         pair_84a62a['canonical_line']['total_mim'],
         pair_84a62a['bit78_root_hex']))
