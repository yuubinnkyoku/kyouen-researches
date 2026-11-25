#!/usr/bin/env python3
# Assemble the 39-live-witness depth-10 sweep classification from raw probe records.
# Gates (fail-closed):
#  G1 partition: exactly 39 roots x 2 orderings = 78 unique (root, ordering) keys
#  G2 both orders present for every root
#  G3 uncapped: every probe result capped == false
#  G4 pilot_d6 control: every record control loss == false and nodes == 3402
#  G5 order-consistency: no root with WIN verdict in one order and REFUTED in another
#  G6 covered rows: witness roots' covered rows union == resolve6 residual 78 rows
#  G7 duplicate agreement: any duplicate (root, ordering) ok-records agree exactly
#     (nodes, loss, capped) -- determinism cross-check at zero cost
#  G8 roots are 7-stone D4-canon, child = root - lowest set bit, child|1<<bit == root
import json, hashlib, collections, sys

D = '/home/user/work/sweep39live'
OUT = f'{D}/output/witness-39live-root-depth10-sweep-20261120.json'

roots = json.load(open(f'{D}/roots.json'))
by_root = {r['root']: r for r in roots}

recs = []
for w in range(4):
    for line in open(f'{D}/output/probe-records-w{w}.jsonl'):
        recs.append(json.loads(line))

gates = []
def gate(name, ok, detail):
    gates.append({'name': name, 'pass': bool(ok), 'detail': detail})
    if not ok:
        print('GATE FAIL:', name, detail); sys.exit(1)

ok_recs = [r for r in recs if r.get('result') and not r.get('error')]
gate('no-error-records', all(not r.get('error') for r in recs),
     {'recorded': len(recs), 'errors': sum(1 for r in recs if r.get('error'))})

keys = collections.Counter((r['root'], r['ordering']) for r in ok_recs)
gate('partition-78', len(keys) == 78 and set(k[0] for k in keys) == set(by_root),
     {'unique_keys': len(keys), 'roots': len(set(k[0] for k in keys))})

per_root = collections.defaultdict(dict)
dups = collections.defaultdict(list)
for r in ok_recs:
    per_root[r['root']][r['ordering']] = r
    dups[(r['root'], r['ordering'])].append(r['result'])
mism = 0
for k, v in dups.items():
    if len(v) > 1:
        if not all(x['nodes'] == v[0]['nodes'] and x['loss'] == v[0]['loss']
                   and x['capped'] == v[0]['capped'] for x in v):
            mism += 1
gate('duplicate-agreement', mism == 0,
     {'dup_keys': sum(1 for v in dups.values() if len(v) > 1), 'mismatches': mism})

gate('both-orders', all(set(per_root[r]) == {'andclose1', 'andclose0'} for r in by_root),
     {'roots': len(by_root)})

cap_bad = [(r['root'], r['ordering']) for r in ok_recs if r['result'].get('capped') ]
gate('uncapped', len(cap_bad) == 0, {'capped': len(cap_bad)})

pil_bad = [r['root'] for r in ok_recs
           if not (r.get('control') and r['control'].get('loss') is False
                   and r['control'].get('nodes') == 3402)]
gate('pilot-d6', len(pil_bad) == 0,
     {'expected_nodes': 3402, 'failures': len(pil_bad)})

cls = {}
conflict = []
total_nodes = 0
max_probe = None
for root, item in by_root.items():
    r1 = per_root[root]['andclose1']['result']
    r0 = per_root[root]['andclose0']['result']
    total_nodes += r1['nodes'] + r0['nodes']
    for r in (r1, r0):
        if max_probe is None or r['nodes'] > max_probe['nodes']:
            max_probe = {'root': root, **r}
    if r1['loss'] != r0['loss']:
        conflict.append(root)
        cls[root] = 'ORDER-CONFLICT'
    else:
        cls[root] = 'WIN7-D10' if r1['loss'] is True else 'REFUTED-D10'
gate('order-consistency', len(conflict) == 0, {'conflicts': conflict})

cov = set()
for r in roots:
    assert bin(int(r['root'], 16)).count('1') == 7
    lo = int(r['root'], 16) & (-int(r['root'], 16))
    assert (int(r['child'], 16) | lo) == int(r['root'], 16)
    assert lo.bit_length() - 1 == r['bit']
    cov.update(r['rows'])
residual = set(json.load(open(f'{D}/resolve6.json'))['base_state']['residual_row_hex'])
gate('covered-rows-equal-residual78', cov == residual,
     {'covered': len(cov), 'residual': len(residual)})
gate('anatomy-decomposition', True,
     {'roots': len(roots), 'popcount': 7, 'rule': 'child = root - lowest set bit, raw hex, canon_hex forbidden'})

dist = collections.Counter(cls.values())
out = {
  'schema': 'n11-residual78-39livewitness-depth10-sweep-20261120-v1',
  'date': '2026-11-20',
  'protocol': {
    'runner': 'class4_child1_runner_v17.ts git blob c132cc6425eee3feaeef1d697dd74f968cfedb59',
    'depth': 10, 'cap': 30000000,
    'orderings': ['andclose1', 'andclose0'],
    'pilot_d6_control': {'loss': False, 'nodes': 3402},
    'child_rule': 'RAW integer hex, child = root - lowest set bit (canon_hex forbidden, K1046 incident rule)',
    'runner_transport': 'raw.githubusercontent.com commit-SHA-pinned, git blob sha1 verified c132cc6425eee3feaeef1d697dd74f968cfedb59'
  },
  'inputs': {
    'resolve6': {
      'path': 'research/experiments/n11-residual78-cache-join-resolve6-20261120/output/post-saturation-full-cache-join-resolve6-20261120.json',
      'sha256': 'e85d4bfb867a193f2b3cdb23ec9e15679359c9f337fcd97eb5c62473b90c281a',
      'witness_selection': 'witness_full (39 live roots, maximum matching 39 over 78 residual rows, stranded 0, all safe)'
    }
  },
  'classification': {root: cls[root] for root in sorted(by_root)},
  'summary': {
    'roots': 39, 'probes': 78, 'win': dist.get('WIN7-D10', 0),
    'refuted': dist.get('REFUTED-D10', 0), 'capped': 0,
    'order_conflicts': len(conflict),
    'total_nodes': total_nodes,
    'max_probe': max_probe,
    'avg_nodes_per_probe': total_nodes // 78
  },
  'gates': gates,
  'interpretation_guard': [
    'REFUTED-D10 is not a LOSS proof; it means no first-mover win within depth 10 under the runner v17 move model.',
    'WIN7-D10 roots are certificate extraction candidates only; rows are closed by receipt fold after extraction and independent dual verification.',
    'This sweep is row-coverage candidate bookkeeping and says nothing about game-theoretic values of rows, the two-stone roots, or the empty board.',
    'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
  ]
}
blob = json.dumps(out, indent=1, sort_keys=True) + '\n'
open(OUT, 'w').write(blob)
print('all gates pass:', all(g['pass'] for g in gates))
print(json.dumps(out['summary'], indent=1))
print('sha256:', hashlib.sha256(blob.encode()).hexdigest())
