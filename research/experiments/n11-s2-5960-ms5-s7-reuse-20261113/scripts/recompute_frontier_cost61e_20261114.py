#!/usr/bin/env python3
"""Full manifest-level class-2/4 frontier recomputation over ALL published (cost-61e
extension) WIN7 receipts as of main (class2-lane cost-61e session 12, 2026-11-14).

Direct extension of recompute_frontier_cost61d_20261114.py via runpy: after
reproducing every published staged control through after-cost-61d (solved 951 /
unique remaining 6896 / sum 542952 / open 5166/406675), the completed cost-61e
sweep (session 12, S6 child 00000000000000803202000040000000 of the second
class-2 target S5 00000000000000803202000000000000: 61 candidates, run on the
v16 runner: 13 WIN7-D10, 48 REFUTED, 0 capped, 32,935,423 v16 nodes) is
asserted and its three fully verified receipts (bits 109/17/40; 43/47/44
sub-roots PASS, union 0/0 each) are added. CORRECTION discovered during
integration: the claim described this child as the cheapest remaining unswept
child with demand c1=0,c2=2,c4=0, but the child was already solved in the
published after-cost-60b baseline (demand empty since); the claim line was
inherited from the cost-61d claim without re-verification and is recorded as a
bookkeeping error here. WIN7 bit 1's root is the identical 7-stone position as
the published cost-61d bit-30 receipt (already solved in the frontier through
that receipt; the fresh extraction reproduced its certificate bit-exact, md5
93bc0a6a..., and is not re-pushed), so it adds nothing here.
The 9 remaining WIN7-D10 bits stay warm certificate-rebuild candidates and
change no frontier number.
"""
import csv, json, runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-61d frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost61d_20261114.py'))
covers = ns['covers']
summary_state = ns['summary_state']
manifest = ns['manifest']
classes = ns['classes']
s41 = ns['s32']
st41 = ns['st32']
rem41 = ns['rem32']
dem41 = ns['dem32']
assert st41['solved_s6_in_manifest'] == 951 and st41['unique_remaining_s6'] == 6896
assert st41['sum_remaining_cost'] == 542952
assert st41['s6_needed_by_open_classes'] == 5166 and st41['cost_needed_by_open_classes'] == 406675
print('CONTROL after-cost61d published frontier reproduced: OK')

# ---------- 2. assert the completed cost-61e sweep record ----------
j61e = json.loads((OUT / 'class2-lane-cost61e-sweep-20261114.json').read_text())
assert j61e['s6_child_hex'] == '00000000000000803202000040000000'
assert j61e['s5_parent_hex'] == '00000000000000803202000000000000'
assert j61e['s6_s7_edge_cost'] == 61 and j61e['capped'] == 0
assert j61e['win7_d10'] == 13 and j61e['refuted_d10'] == 48
assert j61e['total_nodes'] == 32935423
assert j61e['demand_classes'].startswith('CORRECTION') and 'demand_classes_correction' in j61e
child = int(j61e['s6_child_hex'], 16)
for b, r in zip(j61e['win7_bits'], j61e['win7_roots']):
    assert int(r, 16) == child | (1 << b), (b, r)
print('CONTROL completed cost-61e sweep record: OK (13 WIN7, 48 REFUTED, 0 capped, roots asserted)')

# WIN7 bit 1 is a duplicate of the published cost-61d bit-30 receipt (identical
# 7-stone position); the sweep record documents this and keeps it out of the
# unverified list. Its root must already be solved in the after-cost-61d state.
assert 'duplicate_root_note' in j61e and '00000000000000803202000040000002' in j61e['duplicate_root_note']
assert 1 in j61e['win7_bits'] and 1 not in j61e['unverified_win7_bits']
dup_root = child | (1 << 1)
dup_cov = covers(dup_root)
assert dup_cov <= s41 and len(dup_cov) > 0, \
    'duplicate WIN7 bit-1 root coverage must already be solved via the cost-61d bit-30 receipt'
print('CONTROL cost-61e bit 1 duplicate-root note: OK (covers already in baseline, marginal empty)')

# the 61 candidate bits are bit-exact with the independent enumeration
claim = json.loads((OUT / 'class2-lane-cost61e-inflight-20261114.json').read_text())
assert claim['legal_candidates_total'] == 61 and claim['status'].startswith('completed')
assert claim['result']['win7_d10'] == 13 and claim['result']['capped'] == 0
print('CONTROL cost-61e claim updated to completed: OK')

# the claim's stated demand (c1=0,c2=2,c4=0) does NOT hold in the after-cost-61d
# frontier: the S6 child was already solved there (indeed already in the
# after-cost-60b baseline), so its open-class demand is empty. The claim text
# inherited the cost-61d claim's demand line without re-verification; this
# recompute records the correction explicitly.
assert j61e['s6_child_hex'] not in dem41, \
    'expected the cost-61e child to have empty demand in the after-cost-61d state'
canon = covers.__globals__['canon']
assert canon(child) in s41, \
    'expected the cost-61e child to already be solved in the after-cost-61d state'
print('CONTROL cost-61e child demand: EMPTY in the after-cost-61d frontier (child already solved); '
      'claim demand_classes c2=2 recorded as a stale bookkeeping error (correction documented)')

# ---------- 3. add the cost-61e receipts (three fully verified certificates) ----------
w61e = json.loads((OUT / 'class2-lane-cost61e-win7-certificates-20261114.json').read_text())
certs = [c for c in w61e['certificates'] if c.get('verdict') == 'WIN7']
assert len(certs) == 3
assert [c['bit'] for c in certs] == [109, 17, 40]
rows_map = {109: 15534, 17: 22590, 40: 25428}
subs_map = {109: 43, 17: 47, 40: 44}
mob_map = {109: 43, 17: 47, 40: 44}
for c in certs:
    assert c['rows'] == rows_map[c['bit']]
    assert c['sub_roots_pass'] == subs_map[c['bit']]
    assert c['root_check']['loser_mobility'] == mob_map[c['bit']]
    assert c['union_missing'] == 0 and c['union_extra'] == 0
    assert int(c['root_hex'], 16) == child | (1 << c['bit'])
print('CONTROL cost-61e receipts verified: OK (rows/sub-roots/union asserted for bits 109/17/40)')

per_bits = {}
marg_union = set()
for c in certs:
    root = int(c['root_hex'], 16)
    cov = covers(root)
    marg = cov - s41
    marg_m = marg & manifest
    per_bits[c['bit']] = {
        'root_hex': c['root_hex'],
        'covers': len(cov), 'marginal': len(marg),
        'marginal_in_manifest': len(marg_m),
        'marginal_manifest_hexes': sorted(f'{k:032x}' for k in marg_m),
    }
    marg_union |= marg
s42 = s41 | marg_union
st42, rem42, uniq42, dem42 = summary_state(s42)
print('AFTER cost61e:', json.dumps(st42, indent=1))

# ---------- 4. new ranking ----------
def best(rem, bit):
    return sorted(
        ({'s5_hex': k, 'classes': classes.get(k, 0),
          'remaining_s6_orbits': len(rows),
          'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
         for k, rows in rem.items() if classes.get(k, 0) & bit),
        key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

class2 = best(rem42, 2)
class4 = best(rem42, 4)
print('best class2:', class2[0])
print('next class2:', class2[1:4])
print('best class4:', class4[0])
print('next class4:', class4[1:4])

result = {
    'schema': 'n11-class-frontier-cost61e-recompute-20261114-v1',
    'date': '2026-11-14',
    'baseline_main': 'class-frontier-cost61d-recompute-20261114 (solved 951 / unique remaining 6896 / sum 542952 / open 5166/406675)',
    'method': 'direct extension of recompute_frontier_cost61d_20261114.py: every staged control reproduces the published after-cost-61d frontier exactly (asserted: 951/6896/542952/5166/406675), the completed cost-61e sweep (13 WIN7-D10, 48 REFUTED, 0 capped, 32,935,423 v16 nodes; v15 cross-engine anchors on WIN7 bits 102/4/109 plus REFUTED bit 3, v16 determinism re-run node-exact on bits 102/3/4) is asserted and its three fully verified receipts (bits 109/17/40; rows 15,534/22,590/25,428; sub-roots 43/47/44 PASS; union 0/0 each) are added. CORRECTION discovered during integration: the claim described the S6 child as the cheapest remaining unswept child with demand c1=0,c2=2,c4=0, but the child was already solved in the published after-cost-60b baseline (demand empty in every frontier state since); the claim line was inherited from the cost-61d claim without re-verification. The sweep itself remains valid research on never-solved 7-stone positions: bit 109 adds no new coverage, bit 17 adds 5 covered positions (1 in manifest), bit 40 adds 6 (2 in manifest, one of which is a remaining child of the second class-2 target); WIN7 bit 1 is the identical 7-stone position as the published cost-61d bit-30 receipt (fresh extraction reproduced md5 93bc0a6a bit-exact; not re-pushed); the 9 remaining WIN7-D10 bits stay warm certificate-rebuild candidates and change no frontier number',
    'controls': {
        'after_cost61d': {'solved_in_manifest': 951, 'unique_remaining': 6896,
                          'sum_cost': 542952, 'open_s6': 5166, 'open_cost': 406675,
                          'reproduced': True},
        'cost61e_sweep': {'win7_d10': 13, 'capped': 0, 'refuted_d10': 48,
                          'roots_asserted': True, 'engine': 'v16 (agreement-gated in cost-56a)'},
        'cost61e_duplicate_bit1': {'root_hex': '00000000000000803202000040000002',
                                   'duplicate_of': 'cost-61d bit-30 receipt (md5 93bc0a6a reproduced bit-exact)',
                                   'already_solved_in_baseline': True},
        'cost61e_claim': {'status': 'completed', 'reproduced': True},
        'cost61e_demand': {'claim_stated': {'c1': 0, 'c2': 2, 'c4': 0},
                           'after_cost61d_actual': 'empty (child already solved; not in the open-class demand map)',
                           'verdict': 'claim bookkeeping error: the demand line was inherited from the '
                                      'cost-61d claim without re-verification; the child was already solved '
                                      'in the after-cost-60b baseline (its canon is covered by the '
                                      'cost-61d bit-30 receipt and by earlier coverage); the sweep itself '
                                      'and all certificates remain valid',
                           'reproduced': True},
        'cost61e_receipts': {'rows': rows_map, 'sub_roots_pass': subs_map,
                             'union_missing': 0, 'union_extra': 0, 'reproduced': True},
    },
    'cost61e_addition': per_bits,
    'frontier_after_cost61e': {
        'solved_s6_in_manifest': st42['solved_s6_in_manifest'],
        'remaining_s5_orbits': st42['remaining_s5_orbits'],
        'unique_remaining_s6': st42['unique_remaining_s6'],
        'sum_remaining_cost': st42['sum_remaining_cost'],
        's6_needed_by_open_classes': st42['s6_needed_by_open_classes'],
        'cost_needed_by_open_classes': st42['cost_needed_by_open_classes'],
        'demand_histogram_open_only': st42['hist'],
        'best_class2': class2[0],
        'best_class2_note': 'receipt-unclosable per class-frontier-uncoverability-audit-20261114.json (all 10 remaining children sterile-swept); shown for reference only',
        'best_coverable_class2': next(c for c in class2 if c['s5_hex'] != '00000000000000809082000000000000'),
        'next_class2': class2[1:4],
        'best_class4': class4[0],
        'next_class4': class4[1:4],
    },
    'interpretation_guard': 'bookkeeping over published receipts; REFUTED-D10 sweeps prove only absence of WIN7-D10; WIN7 certificates prove a win within depth 10 from the 7-stone root only; 11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4 remain UNKNOWN',
}
(OUT / 'class-frontier-cost61e-recompute-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-cost61e-recompute-20261114.json')

ranking = sorted(
    ({'s5_hex': k, 'classes': classes.get(k, 0),
      'remaining_s6_orbits': len(rows),
      'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows)}
     for k, rows in rem42.items()),
    key=lambda r: (0 if r['classes'] & 6 else 1, r['remaining_s6_orbits'],
                   r['remaining_s7_edge_cost'], r['s5_hex']))
with (OUT / 'class-frontier-s5-ranking-after-cost61e-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    w.writerow(('s5_hex', 'classes', 'remaining_s6_orbits', 'remaining_s7_edge_cost'))
    for r in ranking:
        w.writerow((r['s5_hex'], r['classes'], r['remaining_s6_orbits'],
                    r['remaining_s7_edge_cost']))

b2 = '00000000000000809082000000000000'
with (OUT / 'class-frontier-top-candidates-s6-after-cost61e-20261114.csv').open('w', newline='') as f:
    w = csv.writer(f, lineterminator=chr(10))
    for label, cand in (('best class-4 blocker-candidate S5', class4[0]),
                        ('best class-2 blocker-candidate S5 (receipt-unclosable, audit-blocked)',
                         {'s5_hex': b2, 'classes': classes.get(b2, 0),
                          'remaining_s6_orbits': len(rem42.get(b2, [])),
                          'remaining_s7_edge_cost':
                              sum(int(r['s6_s7_edge_cost']) for r in rem42.get(b2, []))}),
                        ('best coverable class-2 blocker-candidate S5',
                         next(c for c in class2 if c['s5_hex'] != b2)),
                        ('cost-61e parent S5 (second class-2 target)',
                         next(c for c in class2 if c['s5_hex'] == '00000000000000803202000000000000'))):
        w.writerow([f"# {label}: s5={cand['s5_hex']} classes={cand['classes']} "
                    f"remaining={cand['remaining_s6_orbits']} cost={cand['remaining_s7_edge_cost']}"])
        w.writerow(('s5_hex', 's6_hex', 's6_s7_edge_cost', 'demand'))
        for row in sorted(rem42[cand['s5_hex']], key=lambda r: int(r['s6_s7_edge_cost'])):
            d = dem42[row['s6_hex']]
            w.writerow((cand['s5_hex'], row['s6_hex'], row['s6_s7_edge_cost'],
                        f"c1={d['c1']},c2={d['c2']},c4={d['c4']}"))
print('written ranking + top-candidates CSVs (after-cost61e)')
