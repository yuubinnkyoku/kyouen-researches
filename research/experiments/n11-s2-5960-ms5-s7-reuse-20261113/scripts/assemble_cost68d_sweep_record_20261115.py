#!/usr/bin/env python3
"""Assemble class2-lane-cost68d-sweep-20261115.json from the raw v16 batch JSONLs.

The sweep record is derived strictly from the raw batch files:
output/class2-lane-cost68d-raw-batch{1..9}-20261115.jsonl plus the
node-exact determinism rerun output/class2-lane-cost68d-v16-determinism-rerun-20261115.jsonl.
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
OUT = HERE / 'output'
CHILD = '00000000000000809122000000000000'

records = []
for i in range(1, 10):
    for line in (OUT / f'class2-lane-cost68d-raw-batch{i}-20261115.jsonl').read_text().splitlines():
        records.append(json.loads(line))

pilot = [r for r in records if r.get('control') == 'pilot_d6']
cands = [r for r in records if 'bit' in r]
assert len(pilot) == 9 and len(cands) == 68 and len({r['bit'] for r in cands}) == 68
assert all(p['loss'] is False and p['nodes'] == 3402 and p['capped'] is False
           for p in pilot)

rerun = [json.loads(l) for l in
         (OUT / 'class2-lane-cost68d-v16-determinism-rerun-20261115.jsonl').read_text().splitlines()]
rerun_cands = [r for r in rerun if 'bit' in r]
rerun_pilot = [r for r in rerun if r.get('control') == 'pilot_d6']
assert len(rerun_cands) == 8 and len(rerun_pilot) == 1
b1 = {r['bit']: r for r in cands if r['bit'] in {x['bit'] for x in rerun_cands}}
for r in rerun_cands:
    o = b1[r['bit']]
    assert o['loss'] == r['loss'] and o['nodes'] == r['nodes'] and \
        o['capped'] == r['capped'] and o['terminalStoneRange'] == r['terminalStoneRange']
assert rerun_pilot[0]['nodes'] == 3402 and rerun_pilot[0]['loss'] is False

wins = sorted([r for r in cands if r['loss']], key=lambda r: r['bit'])
refuted = [r for r in cands if not r['loss']]
capped = [r for r in cands if r['capped']]
heaviest = sorted(cands, key=lambda r: -r['nodes'])[:5]

rec = {
    'schema': 'n11-class2-lane-cost68d-sweep-20261115-v1',
    'date': '2026-11-15',
    'session': 'long-term lane execution (2026-11-15 JST), continuing after the '
               'warm multiband frontier recompute (chain head 1109 / 6738 / 531295 / 5008 / 395018, '
               'class-frontier-warm-multiband-recompute-20261115.json) and the cost-68d inflight claim '
               '(commit 6175d233, remote md5 verified)',
    's5_parent_hex': '00000000000000809102000000000000',
    's5_parent_note': 'third class-2 coverable target (best coverable class-2 S5) at the claim',
    's6_child_hex': CHILD,
    's6_s7_edge_cost': 68,
    'demand_classes_at_claim': {'c1': 0, 'c2': 2, 'c4': 0},
    'demand_verification': 'VERIFIED before the claim: the child was the cheapest remaining unswept '
                           'child of the third class-2 target and its demand (c1=0,c2=2,c4=0) was '
                           'simulated to survive both the all-greedy-40 and self-29-only post-batch-2 '
                           'fold scenarios; batch-2 fold does not remove it',
    'candidate_enumeration': 'legal_candidates.py independent Bareiss 4x4 enumeration: 68 legal '
                             'candidates, bit-exact with the published edge cost 68',
    'engine': 'class4_child1_runner_v16.ts (published repo-verbatim v16 runner), depth 10, '
              'andclose=1, cap 1e9, pilot d6 control (loss=false at exactly 3,402 nodes) per batch',
    'engine_gate': 'v16 agreement-gated in cost-56a and used for cost-58b/60b/61d/61e/61f/63e/64b/65g/'
                   '65h/65i/67b/68c/69e/70c/71b/75b/75c',
    'win7_d10': len(wins),
    'win7_bits': [r['bit'] for r in wins],
    'win7_root_nodes': {str(r['bit']): r['nodes'] for r in wins},
    'win7_roots': [hex(int(CHILD, 16) | (1 << r['bit']))[2:].zfill(32) for r in wins],
    'verdict': 'WIN7',
    'refuted_d10': len(refuted),
    'capped': len(capped),
    'total_nodes': sum(r['nodes'] for r in cands),
    'total_nodes_note': 'v16 engine node count over the 68 candidates (single run each); all 7 WIN7 '
                        'candidates have v15 cross-engine anchors and fully verified extracted '
                        'certificates (class2-lane-cost68d-win7-certificates-20261115.json)',
    'pilot_d6_controls': 'loss=false at exactly 3,402 nodes in all 9 batch invocations (identical '
                         'control lines); the determinism rerun invocation adds a 10th identical '
                         'control line',
    'determinism_rerun': 'batch1 8 candidates fully re-run (originally mislabeled batch2, repaired): '
                         'loss/nodes/capped/terminalStoneRange byte-identical, only wall-clock ms '
                         'differs (class2-lane-cost68d-v16-determinism-rerun-20261115.jsonl)',
    'batch_numbering_repair': 'the accidental duplicate invocation of the batch1 bits was originally '
                              'written as raw-batch2; renamed to v16-determinism-rerun and the '
                              'original raw-batch3..10 renumbered to raw-batch2..9 (no data loss, '
                              'per-line JSON unchanged)',
    'terminal_stone_range_all': [r['terminalStoneRange'] for r in cands if
                                 r['terminalStoneRange'] != [13, 17]] or [[13, 17]],
    'heaviest_bits': [
        {'bit': r['bit'], 'nodes': r['nodes'],
         'verdict': 'WIN7' if r['loss'] else 'REFUTED'} for r in heaviest],
    'raw_batches': [f'class2-lane-cost68d-raw-batch{i}-20261115.jsonl' for i in range(1, 10)]
                   + ['class2-lane-cost68d-v16-determinism-rerun-20261115.jsonl'],
}
assert rec['win7_d10'] == 7 and rec['refuted_d10'] == 61 and rec['capped'] == 0
assert rec['total_nodes'] == 61325518
(OUT / 'class2-lane-cost68d-sweep-20261115.json').write_text(json.dumps(rec, indent=1) + '\n')
print('written class2-lane-cost68d-sweep-20261115.json; win7 bits',
      rec['win7_bits'], 'total_nodes', rec['total_nodes'])
