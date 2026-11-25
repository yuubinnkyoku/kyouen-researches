#!/usr/bin/env python3
# Assemble the 43-witness depth-10 sweep classification record.
import json, glob, hashlib
D='/home/user/work/sweep43'
W='/home/user/work'
roots={x['root']: x for x in json.load(open(f'{D}/roots.json'))}
recs=[]
for f in sorted(glob.glob(f'{D}/output/probe-records-w*.jsonl')):
    for line in open(f):
        recs.append(json.loads(line))
by_root={}
for x in recs:
    by_root.setdefault(x['root'], []).append(x)
NEED=43
def need(ok,m):
    if not ok:
        print('GATE FAILED:',m); raise SystemExit(1)
need(len(roots)==NEED,'43 roots')
need(len(by_root)==NEED,'43 roots probed, got %d'%len(by_root))
wins=[];refs=[];capped=[];conflicts=[]
per_root={}
for root,item in roots.items():
    rs=by_root.get(root,[])
    probes=[x for x in rs if 'result' in x and x.get('error') is None]
    need(len(probes)==2,'both orderings: '+root)
    ctrl_ok=all(x.get('control',{}).get('nodes')==3402 and x['control']['loss'] is False for x in rs)
    need(ctrl_ok,'pilot control: '+root)
    unc=[x for x in probes if not x['result']['capped']]
    need(len(unc)==2,'uncapped both orderings: '+root)
    ords=sorted(x['ordering'] for x in unc)
    need(ords==['andclose0','andclose1'],'ordering keys: '+root)
    losses={x['ordering']:x['result']['loss'] for x in unc}
    if losses['andclose0']!=losses['andclose1']:
        conflicts.append(root); continue
    rec={
      'root':root,'added_bit':item['bit'],'child_hex':item['child'],
      'covered_stranded_rows':sorted(item['rows']),
      'probe_runs':[
        {'ordering':x['ordering'],'cap':x['cap'],'loss':x['result']['loss'],
         'capped':x['result']['capped'],'nodes':x['result']['nodes'],
         'terminal_stone_range':x['result'].get('terminalStoneRange'),
         'wall_s':x.get('wall'),'worker':x.get('worker'),'seq':x.get('seq')}
        for x in sorted(probes,key=lambda z:z['ordering'])],
      'pilot_control':{ 'control':'pilot_d6','nodes':3402,'loss':False,'all_pass':True},
    }
    rec['nodes_total']=sum(p['nodes'] for p in rec['probe_runs'])
    if losses['andclose1']:
        wins.append(root)
    else:
        refs.append(root)
    per_root[root]=rec
need(len(wins)+len(refs)+len(capped)+len(conflicts)==NEED,'partition')
out={
 'schema':'n11-stranded86-add-one-stone-witness-43-root-depth10-sweep-20261119-v1',
 'date':'2026-11-19',
 'status':'sweep-complete',
 'base_record':'post-eighth-receipt-cover-resolve4-20261119.json residual 86 stranded rows (add-one-stone expansion census: 43 pair witnesses cover all 86 rows)',
 'engine':{'file':'class4_child1_runner_v17 (git blob c132cc6425eee3feaeef1d697dd74f968cfedb59)','depth':10,'cap':30000000,
           'andclose_orderings':[1,0],'pilot_control':'pilot_d6 (3402 nodes, loss=false, must pass before each probe)',
           'child_convention':'RAW maxbit child (canon_hex(child) is forbidden; epoch-1 loss cause)'},
 'classification_rule':'WIN7-D10 = uncapped loss=true in both orderings; REFUTED-D10 = uncapped loss=false in both orderings; conflict otherwise',
 'classification':{
   'counted_roots':NEED,
   'win7_d10':{'count':len(wins),'roots':sorted(wins)},
   'refuted_d10':{'count':len(refs),'roots':sorted(refs)},
   'capped':{'count':len(capped),'roots':sorted(capped)},
   'ordering_conflicts':{'count':len(conflicts),'roots':sorted(conflicts)}
 },
 'witness_records':[per_root[k] for k in sorted(per_root)],
 'controls':{
   'both_andclose_orderings_uncapped_all_roots':True,
   'pilot_controls_all_pass':True,
   'nodes_total_all_probes':sum(p['nodes'] for r in per_root.values() for p in r['probe_runs']),
   'probe_wall_total_s_rounded':round(sum(p.get('wall_s') or 0 for r in per_root.values() for p in r['probe_runs']),1),
   'verdict_counts':{'WIN':len(wins),'REFUTED':len(refs),'CAPPED':len(capped),'CONFLICT':len(conflicts)}
 },
 'interpretation_guard':[
  'WIN7-D10 proves a first-player win within depth 10 only from the individual seven-stone root.',
  'REFUTED-D10 is NOT a LOSS proof; it bounds first-player wins within depth 10 from that exact root only.',
  'These 43 witnesses are add-one-stone expansions of the 86 stranded five-parent target rows; a WIN witness closes exactly its covered stranded rows (subject to certificate extraction and fold gates).',
  'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.'
 ]
}
with open(f'{D}/output/witness-43-root-depth10-sweep-20261119.json','w') as f:
    json.dump(out,f,indent=1); f.write('\n')
print(json.dumps({k:v for k,v in out['classification'].items() if k!='refuted_d10'},indent=1))
print('total nodes',out['controls']['nodes_total_all_probes'])
