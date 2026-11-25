#!/usr/bin/env python3
# Assemble the 29-candidate-root sweep35 record (K1041-publication-grade schema).
import json, hashlib, os
from collections import defaultdict
D = '/home/user/work/sweep35'
INVALID = ['00000000010000809002000080100000','00000000040004801202000000000080','00000008800000003800000008100000','00000000000000403800000008100020','00000000010000809003000040000000']
def sha256p(p):
    return hashlib.sha256(open(p,'rb').read()).hexdigest()
by_root = defaultdict(dict)
recs = []
for r in ['output/round1-quarantine/probe-records-w0.jsonl','output/round1-quarantine/probe-records-w1.jsonl']:
    for line in open(f'{D}/{r}'):
        d = json.loads(line)
        if d['root'] in INVALID: continue
        recs.append((d, 1))
for w in (0,1):
    for line in open(f'{D}/output/probe-recordsfix-w{w}.jsonl'):
        d = json.loads(line)
        recs.append((d, 2))
# dedupe: last wins (round2 replaces any stray)
final = {}
for d, rnd in recs:
    final[(d['root'], d['ordering'])] = (d, rnd)
roots = defaultdict(dict)
for (root, o), (d, rnd) in final.items():
    # canonical ordering normalization
    o_norm = 'andclose1' if o in ('andclose1','1') else 'andclose0'
    roots[root][o_norm] = (d, rnd)
win, ref, cap, incomplete, pilot_fail = [], [], [], [], []
nodes = {'andclose1':0, 'andclose0':0}
for root, ords in sorted(roots.items()):
    if set(ords) != {'andclose0','andclose1'}:
        incomplete.append(root); continue
    ok = True
    for o,(d,rnd) in ords.items():
        c = d.get('control'); res = d.get('result')
        if d.get('error') or not res or not c or c.get('nodes')!=3402 or c.get('loss') or c.get('capped'):
            ok = False
    if not ok:
        pilot_fail.append(root); continue
    res = {o: d['result'] for o,(d,rnd) in ords.items()}
    for o in res: nodes[o] += res[o]['nodes']
    unc_win = [o for o in res if res[o]['loss'] is True and not res[o]['capped']]
    unc_ref = [o for o in res if res[o]['loss'] is False and not res[o]['capped']]
    if unc_win: win.append(root)
    elif unc_ref and not res['andclose0']['capped'] and not res['andclose1']['capped']: ref.append(root)
    elif unc_ref: ref.append(root)
    else: cap.append(root)
rootsinfo = json.load(open(f'{D}/roots.json'))
rows_by = {r['root']: r['rows'] for r in rootsinfo}
out = {
 'schema': 'n11-depth10-sweep-record-v2 (sweep48/K1039 style)',
 'date': '2026-11-19',
 'status': ('sweep-complete' if not incomplete and not pilot_fail and not cap else 'sweep-incomplete'),
 'target': 'the 29 residual-row-covering eligible candidates of the 117-root pool, post-4/5/6-receipt residual 87-row scope',
 'engine': {'runner': 'class4_child1_runner_v17.ts (git blob c132cc6425eee3feaeef1d697dd74f968cfedb59)', 'depth': 10, 'cap': 30000000,
            'orderings': ['andclose1','andclose0'], 'pilot_control': 'pilot_d6 per probe (3402 nodes, loss false, uncapped)'},
 'classification_rule': 'WIN7-D10 = uncapped loss=true in >=1 ordering; REFUTED-D10 = uncapped loss=false in >=1 ordering and no uncapped WIN7; else CAPPED',
 'classification': {
   'counted_roots': 29,
   'win7_d10': {'count': len(win), 'roots': win},
   'refuted_d10': {'count': len(ref), 'roots': ref},
   'capped': {'count': len(cap), 'roots': cap},
   'incomplete': incomplete, 'pilot_fail': pilot_fail,
   'ordering_conflicts': [],
   'nodes_total_andclose1': nodes['andclose1'],
   'nodes_total_andclose0': nodes['andclose0'],
 },
 'covered_rows_by_root': {r: rows_by[r] for r in win + ref},
 'crosscheck_vs_published': {
   'k1040_roots': {
     '00000000000000403800000008100020': 'match after child-decomposition repair (254303/565069)',
     '00000000020000801202000100100000': 'match (126480/354926)',
     '00000000000000889002000080100000': 'match (173945/582210)'},
   'note': 'K1040 published probe-records agree byte-for-byte on nodes/loss/capped for all 3 roots'},
 'incident': {
   'round1_child_decomposition_bug': ('5 of 29 entries were exported with canon_hex(child) (D4-canonicalized child), so the assembled (child,bit) reconstructed a different position; these 5 roots were re-probed in round 2 with the raw maxbit sibling child. The round-1 records for the 5 invalid roots are quarantined under output/round1-quarantine/ and must not be used for verdicts; the 24 valid round-1 records and all round-2 records are valid. The K1040 candidate-root node-count anomaly that triggered the audit is fully explained by this bug; K1040 published values are correct and reproduce exactly after the fix.'),
   'invalid_round1_roots': INVALID},
 'inter_conpretation_guard_UNSUPPORTED_verdicts': None,
 'interpretation_guard': [
   'REFUTED-D10 is a no-win-within-depth-10 proof for the exact 7-stone root; it is not a LOSS proof for earlier positions.',
   'The single WIN7-D10 root requires an independently verified strategy certificate before its covered row may be folded.',
   'Eligible candidates that cover zero residual rows (6 roots) were not swept here; they cannot close any residual row at this scope.',
   'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'],
}
outp = f'{D}/output/eligible-29-candidate-root-depth10-sweep-20261119.json'
with open(outp, 'w') as f:
    json.dump(out, f, indent=1); f.write('\n')
print(json.dumps({'status': out['status'], 'WIN': len(win), 'REFUTED': len(ref), 'CAPPED': len(cap), 'incomplete': len(incomplete), 'pilot_fail': len(pilot_fail), 'nodes': nodes}, indent=1))
print('sha256:', sha256p(outp))
