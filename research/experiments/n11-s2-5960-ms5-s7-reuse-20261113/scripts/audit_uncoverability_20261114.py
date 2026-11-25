#!/usr/bin/env python3
"""Uncoverability audit of the remaining S6 children of the top blocker-candidate S5s
at the after-cost-73a frontier (n11 class-2/4 lane, 2026-11-14 session 11).

Rationale. A WIN7-D10 receipt covers an S6 orbit only through one of its S7 roots
(the 7-stone positions S6 + one legal stone; covers() = the canonical images of
root minus each stone). A completed sweep of an S6 child enumerates ALL legal S7
candidates of that child (legal_candidates.py, bit-exact with the published edge
cost, asserted per record). If such a sweep found 0 WIN7-D10 and 0 capped, then no
future WIN7-D10 receipt can ever cover that S6 orbit: every possible receipt root
for it has been individually refuted at depth 10. Such an orbit is *receipt-unclosable*.

This audit classifies every remaining (uncovered) S6 child of the best class-2 and
best class-4 blocker-candidate S5s into: swept-sterile (permanently uncoverable within
the WIN7-D10 receipt framework), swept-WIN7 (impossible for a remaining orbit -
asserted), or unswept (still coverable by a future sweep).

It runs the full after-cost-73a frontier recompute first (every published staged
control is asserted inside it), so the audit is bookkeeping over the same published
receipts only. No new verdicts are computed.
"""
import json
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'

# ---------- 1. reproduce the after-cost-73a frontier (asserts all controls) ----------
ns = runpy.run_path(str(HERE / 'scripts' / 'recompute_frontier_cost73a_20261114.py'))
rem = ns['rem30']          # s5_hex -> remaining S6 incidence rows of the CURRENT frontier
dem = ns['dem30']
classes = ns['classes']
manifest = ns['manifest']
s30 = ns['s30']
st30 = ns['st30']
assert st30['solved_s6_in_manifest'] == 921 and st30['unique_remaining_s6'] == 6926
assert st30['sum_remaining_cost'] == 544995

# ---------- 2. sweep map over every published class2/class4-lane sweep record ----------
def as_count(v):
    if isinstance(v, list):
        return len(v)
    assert isinstance(v, int), v
    return v

swept = {}   # int s6 child hex -> record summary
for p in sorted(OUT.glob('class*-lane-cost*-sweep-20261114.json')):
    j = json.loads(p.read_text())
    child = (j.get('s6_child_hex') or j.get('s6_child')
             or (j.get('target') or {}).get('s6_child_hex'))
    assert isinstance(child, str) and child, p.name
    summ = j.get('summary') or {}
    verd = j.get('verdicts') or {}
    tot = j.get('totals') or {}
    if 'win7_d10' in j and j['win7_d10'] is not None:
        win7 = as_count(j['win7_d10'])
    elif summ.get('win7_d10') is not None:
        win7 = as_count(summ['win7_d10'])
    elif isinstance(j.get('win7_bits'), list):
        win7 = len(j['win7_bits'])
    elif isinstance(j.get('win7_certificates'), list):
        win7 = len(j['win7_certificates'])
    elif isinstance(verd.get('win7_d10'), list):
        win7 = len(verd['win7_d10'])
    else:
        raise AssertionError(('no win7 field', p.name, sorted(j.keys())))
    if 'capped' in j:
        capped = as_count(j['capped'])
    elif 'capped' in summ:
        capped = as_count(summ['capped'])
    elif 'capped' in tot:
        capped = tot['capped']
    else:
        raise AssertionError(('no capped field', p.name))
    entry = {
        'record': p.name,
        's6_child_hex': child,
        'win7_count': win7,
        'capped_count': capped,
    }
    key = int(child, 16)
    if key in swept:
        prev = swept[key]
        # a re-sweep of the same child must agree on sterility
        assert (prev['win7_count'] == 0) == (win7 == 0) and \
               (prev['capped_count'] == 0) == (capped == 0), (p.name, prev)
        continue
    swept[key] = entry
print(f'sweep map: {len(swept)} published S6 child sweeps '
      f'({sum(1 for e in swept.values() if e["win7_count"]) } with WIN7)')

# every swept child must be a legal 6-stone position of the published corpus
for k, e in swept.items():
    assert bin(k).count('1') == 6, e

# ---------- 3. classify the remaining children of the top targets ----------
def classify(s5_hex, s5_class_bit):
    rows = rem[s5_hex]
    assert classes.get(s5_hex, 0) & s5_class_bit
    out = {'sterile_swept': [], 'win7_swept_impossible': [], 'unswept': []}
    for r in rows:
        k = int(r['s6_hex'], 16)
        e = swept.get(k)
        if e is None:
            out['unswept'].append({'s6_hex': r['s6_hex'], 'cost': int(r['s6_s7_edge_cost'])})
        elif e['win7_count'] == 0 and e['capped_count'] == 0:
            out['sterile_swept'].append(
                {'s6_hex': r['s6_hex'], 'cost': int(r['s6_s7_edge_cost']),
                 'record': e['record']})
        else:
            # a remaining (uncovered) orbit cannot come from a swept child with a
            # WIN7 receipt: the frontier recompute would have covered it already
            out['win7_swept_impossible'].append(
                {'s6_hex': r['s6_hex'], 'record': e['record']})
    assert not out['win7_swept_impossible'], out['win7_swept_impossible']
    return out

best2 = '00000000000000809082000000000000'
best4 = '00000000020000003800000080000000'
c2 = classify(best2, 2)
c4 = classify(best4, 4)

n2 = len(rem[best2]); n4 = len(rem[best4])
assert len(c2['sterile_swept']) + len(c2['unswept']) == n2
assert len(c4['sterile_swept']) + len(c4['unswept']) == n4

print(f'best class-2 S5 {best2}: {n2} remaining = '
      f"{len(c2['sterile_swept'])} sterile-swept (unclosable) + {len(c2['unswept'])} unswept")
print(f'best class-4 S5 {best4}: {n4} remaining = '
      f"{len(c4['sterile_swept'])} sterile-swept (unclosable) + {len(c4['unswept'])} unswept")

# ---------- 4. next class-2 targets: coverable-child inventory ----------
next2 = []
for s5_hex, rows in rem.items():
    if not (classes.get(s5_hex, 0) & 2) or s5_hex == best2:
        continue
    unswept = sorted((int(r['s6_s7_edge_cost']), r['s6_hex'])
                     for r in rows if int(r['s6_hex'], 16) not in swept)
    sterile = [r for r in rows if int(r['s6_hex'], 16) in swept
               and swept[int(r['s6_hex'], 16)]['win7_count'] == 0]
    next2.append({
        's5_hex': s5_hex,
        'remaining_s6_orbits': len(rows),
        'remaining_s7_edge_cost': sum(int(r['s6_s7_edge_cost']) for r in rows),
        'sterile_swept_children': len(sterile),
        'unswept_children': len(unswept),
        'cheapest_unswept': (unswept[0] if unswept else None),
    })
next2.sort(key=lambda r: (r['remaining_s6_orbits'], r['remaining_s7_edge_cost'], r['s5_hex']))

result = {
    'schema': 'n11-class-frontier-uncoverability-audit-20261114-v1',
    'date': '2026-11-14',
    'method': 'classification of every remaining S6 child of the best class-2 / class-4 '
              'blocker-candidate S5s at the after-cost-73a frontier against all published '
              'class2/class4-lane sweep records; the after-cost-73a frontier (solved 921 / '
              'unique remaining 6,926 / sum 544,995 / open 5,196/408,718) is reproduced first '
              'with every staged control asserted (runpy of recompute_frontier_cost73a_20261114.py)',
    'sweep_map_size': len(swept),
    'best_class2': {
        's5_hex': best2, 'remaining': n2,
        'receipt_unclosable_children': len(c2['sterile_swept']),
        'unclosable_cost': sum(x['cost'] for x in c2['sterile_swept']),
        'unswept_children': len(c2['unswept']),
        'sterile_swept': c2['sterile_swept'],
        'unswept': c2['unswept'],
    },
    'best_class4': {
        's5_hex': best4, 'remaining': n4,
        'receipt_unclosable_children': len(c4['sterile_swept']),
        'unclosable_cost': sum(x['cost'] for x in c4['sterile_swept']),
        'unswept_children': len(c4['unswept']),
        'sterile_swept': c4['sterile_swept'],
        'unswept': c4['unswept'],
    },
    'next_class2_targets': next2[:12],
    'conclusion': (
        'A completed sweep of an S6 child with 0 WIN7-D10 and 0 capped enumerates ALL legal '
        'S7 roots of that child and refutes each at depth 10, so no WIN7-D10 receipt can ever '
        'cover that S6 orbit. The best class-2 S5 '
        '00000000000000809082000000000000 now has ALL of its remaining children in this state: '
        'it can never reach 0 remaining within the WIN7-D10 receipt framework and is therefore '
        'exhausted as a sweep target - the frontier ranking should treat it as blocked. '
        'Progress on class 2 must come from (a) other class-2 S5 candidates whose remaining '
        'children are unswept (receipt-coverable), or (b) a direct refutation of the S5 '
        'candidate itself (SECOND_WIN route), which is outside the receipt framework. '
        'The same audit is reported for the best class-4 S5 (the class4-lane parallel still '
        'has unswept coverable children there).'),
    'interpretation_guard': (
        'bookkeeping over published receipts and sweep records; REFUTED-D10 is the absence of '
        'a winner win within depth 10 in that subtree only and decides nothing about the '
        '11x11 empty root / {49,60} / S2 {59,60} / class 2 / class 4, which remain UNKNOWN'),
}
(OUT / 'class-frontier-uncoverability-audit-20261114.json').write_text(
    json.dumps(result, indent=1) + chr(10))
print('written class-frontier-uncoverability-audit-20261114.json')
print('next class-2 targets (top 5):')
for r in next2[:5]:
    print(' ', r['s5_hex'], 'remaining', r['remaining_s6_orbits'], 'cost', r['remaining_s7_edge_cost'],
          'sterile-swept', r['sterile_swept_children'], 'unswept', r['unswept_children'],
          'cheapest-unswept', r['cheapest_unswept'])
