#!/usr/bin/env python3
"""Worklist analysis of the second coverable class-2 candidate S5
00000000000000801202000040000000 at the canonical head 1326 (2026-11-15).

Pure bookkeeping on the fold-chain namespace: re-runs the published
cost-62a fold script (which itself reproduces the whole chain head
byte-identically) and analyses the 34 remaining child rows of the second
candidate S5 after the 62a receipts:

- per-row S7 edge cost, demand (c1/c2/c4), and sharing with the class-2
  co-parent S5 00000000000000003800000008001000;
- the cost histogram of the remaining rows and the cheapest next sweep
  targets, with the cost-58 row (IN FLIGHT claim 908716e1, cost-58c)
  explicitly marked do-not-touch;
- no sweep is run and no candidate enumeration is performed.

Bookkeeping only - no game-theoretic claim: 11x11 empty board / two-stone
root {49,60} / S2 {59,60} / class 1 / class 2 / class 4 all UNKNOWN.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ns = __import__('runpy').run_path(str(HERE / 'scripts' / 'recompute_frontier_cost62a_receipts_20261116.py'))
remF2 = ns['remF2']
demF2 = ns['demF2']
classes = ns['classes']
stF2 = ns['stF2']

PARENT1 = '00000000000000801202000040000000'
PARENT2 = '00000000000000003800000008001000'
INFLIGHT_58C = '00000000000000801206000040000000'

assert stF2['solved_s6_in_manifest'] == 1326, stF2
rows1 = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remF2.get(PARENT1, [])}
rows2 = {r['s6_hex']: int(r['s6_s7_edge_cost']) for r in remF2.get(PARENT2, [])}
assert (len(rows1), sum(rows1.values())) == (34, 2368), (len(rows1), sum(rows1.values()))
assert (len(rows2), sum(rows2.values())) == (48, 3582), (len(rows2), sum(rows2.values()))

shared = sorted(set(rows1) & set(rows2))
entries = []
for h in sorted(rows1, key=lambda h: (rows1[h], h)):
    d = demF2.get(h, {})
    entries.append({
        's6_hex': h,
        'edge_cost': rows1[h],
        'demand': {'c1': d.get('c1'), 'c2': d.get('c2'), 'c4': d.get('c4')},
        'in_parent2_worklist': h in rows2,
        'inflight_claim': h == INFLIGHT_58C,
    })

hist = {}
for h, c in rows1.items():
    hist[c] = hist.get(c, 0) + 1
hist_s = {str(k): v for k, v in sorted(hist.items())}

nonflight = [e for e in entries if not e['inflight_claim']]

out = {
    'schema': 'n11-class2-lane-second-candidate-worklist-head1326-20261115-v1',
    'date': '2026-11-15',
    'baseline_head': '1326/6522/515251/4792/378974 (class-frontier-cost62a-receipts-recompute-20261116.json, reproduced by the published fold script)',
    'parent1': {
        's5_hex': PARENT1,
        'classes': classes.get(PARENT1),
        'remaining_rows': len(rows1),
        'remaining_edge_cost': sum(rows1.values()),
    },
    'parent2': {
        's5_hex': PARENT2,
        'classes': classes.get(PARENT2),
        'remaining_rows': len(rows2),
        'remaining_edge_cost': sum(rows2.values()),
    },
    'rows_shared_with_parent2': len(shared),
    'shared_edge_cost_p1_view': sum(rows1[h] for h in shared),
    'cost_histogram': hist_s,
    'inflight_58c_row': {
        's6_hex': INFLIGHT_58C,
        'status': 'IN FLIGHT claim 908716e1 (cost-58c, second candidate S5 cost-58 row) - do not touch',
        'edge_cost': rows1.get(INFLIGHT_58C),
        'in_worklist': INFLIGHT_58C in rows1,
    },
    'rows_sorted_by_cost': entries,
    'cheapest_next_rows_excluding_inflight': [
        {k: e[k] for k in ('s6_hex', 'edge_cost', 'demand', 'in_parent2_worklist')}
        for e in nonflight[:12]
    ],
    'interpretation_guard': (
        'bookkeeping only: remaining-row counts and edge costs are manifest '
        'coverage bookkeeping, not game-theoretic verdicts; REFUTED-D10 is '
        'not a LOSS proof; 11x11 empty board / two-stone root {49,60} / '
        'S2 {59,60} / class 1 / class 2 / class 4 all UNKNOWN'),
}
dest = HERE / 'output' / 'class2-lane-second-candidate-worklist-head1326-20261115.json'
dest.write_text(json.dumps(out, indent=1) + '\n')
print('parent1 (second candidate) 34 rows / 2368; parent2 48 rows / 3582; shared rows:', len(shared))
print('cost histogram:', hist_s)
print('cheapest non-IN-FLIGHT rows:')
for e in nonflight[:12]:
    print(' ', e['edge_cost'], e['s6_hex'], e['demand'], 'shared' if e['in_parent2_worklist'] else '')
print('IN FLIGHT row present in worklist:', INFLIGHT_58C in rows1, rows1.get(INFLIGHT_58C))
