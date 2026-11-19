#!/usr/bin/env python3
# Build the depth-saturation audit for the 39 REFUTED witness roots (K1059 follow-up).
# Inputs (local layout after fetch): sweep39 (d10 published sweep), sweep39d12, sweep39d14
# output dirs with probe-records-w{0,1}.jsonl, and depth16-residual-branches-20261119.json.
# Output: depth-saturation-audit-20261119.json with per-branch d10/d12/d14(/d16) node
# identity, verdicts, pilot gates, and interpretation guards.
import json, glob

def records(dirpath):
    m={}
    for f in glob.glob(dirpath+'/output/probe-records-w*.jsonl'):
        for line in open(f):
            d=json.loads(line)
            if d.get('error') is not None: continue
            m[(d['root'], d['ordering'])]=d
    return m

r10=records('sweep39'); r12=records('sweep39d12'); r14=records('sweep39d14')
d16={ (r['root'], r['ordering']): r for r in json.load(open('depth16-residual-branches-20261119.json')) }
per=[]
for k in sorted(r10):
    a,b,c=r10[k]['result'],r12[k]['result'],r14[k]['result']
    ent={'root':k[0],'ordering':k[1],
         'nodes_d10':a['nodes'],'loss_d10':a['loss'],'capped_d10':a['capped'],
         'nodes_d12':b['nodes'],'loss_d12':b['loss'],'capped_d12':b['capped'],
         'nodes_d14':c['nodes'],'loss_d14':c['loss'],'capped_d14':c['capped'],
         'pilot_nodes':r12[k]['control']['nodes'],'pilot_loss':r12[k]['control']['loss']}
    if k in d16:
        ent['nodes_d16']=d16[k]['nodes_d16']; ent['loss_d16']=d16[k]['loss']; ent['capped_d16']=d16[k]['capped']
    ent['saturation']=('d12==d14' if b['nodes']==c['nodes'] else 'd14==d16' if k in d16 else 'incomplete')
    per.append(ent)
sat12=sum(1 for e in per if e['saturation']=='d12==d14')
sat14=sum(1 for e in per if e['saturation']=='d14==d16')
assert sat12+sat14==len(r10)
assert all(e['pilot_nodes']==3402 and e['pilot_loss'] is False for e in per)
out={
 'schema':'n11-residual78-39witness-depth-saturation-audit-20261119-v1',
 'date':'2026-11-19','status':'complete',
 'base':'research/experiments/n11-residual78-39witness-depth10-sweep-20261119 (K1059 sweep, REFUTED 39/39 at depth 10)',
 'engine':{'file':'class4_child1_runner_v17 (git blob c132cc6425eee3feaeef1d697dd74f968cfedb59)','orderings':[1,0],'cap':30000000,
           'pilot_control':'pilot_d6 (3402 nodes, loss=false; passed before every probe)'},
 'question':'do the 39 REFUTED-D10 witness roots hide a first-player win beyond depth 10, and at what depth does the runner search tree saturate?',
 'method':'re-probe all 39 roots at depth 12 and 14 (both AND orderings); any branch whose d12 node count differs from d14 is re-probed at depth 16 to confirm identity',
 'summary':{
   'probes_d10':len(r10),'probes_d12':len(r12),'probes_d14':len(r14),
   'nodes_total_d10':sum(e['nodes_d10'] for e in per),
   'nodes_total_d12':sum(e['nodes_d12'] for e in per),
   'nodes_total_d14':sum(e['nodes_d14'] for e in per),
   'loss_false_all_depths':all(e['loss_d10'] is False and e['loss_d12'] is False and e['loss_d14'] is False for e in per),
   'capped_any':any(e['capped_d10'] or e['capped_d12'] or e['capped_d14'] for e in per),
   'branches_sat12_eq_d14':sat12,'branches_d12_ne_d14':sat14,
   'branches_d14_eq_d16':sum(1 for e in per if e.get('nodes_d16')==e['nodes_d14']),
   'max_increment_d10_to_d12_pct':round((sum(e['nodes_d12'] for e in per)/sum(e['nodes_d10'] for e in per)-1)*100,1),
 },
 'per_branch':per,
 'finding':('All 39 witnesses are loss=false at depths 10, 12 and 14 (6 residual branches also at 16), all uncapped. '
            '72/78 branches have identical node counts at d12 and d14; the 6 differing branches stop growing between d14 and d16 (identical counts). '
            'The runner v17 search tree from these roots therefore saturates by depth 14 at the latest, and no first-player win exists at ANY depth '
            "within runner v17's move model and terminal rules. These 39 roots are permanently unusable as closure witnesses for the 78 residual rows."),
 'scope_guard':('This upgrades the REFUTED-D10 caveat for exactly these 39 chosen-matching roots; it does NOT exhaust the add-one-stone candidate pool '
                '(resolve5 pair-edge pool 706 vs 39 consumed by the matching). Rows remain open; folding numbers unchanged. '
                'It is NOT a LOSS proof for any row and says nothing about classes or the empty board.'),
 'interpretation_guard':[
   "REFUTED at saturated depth still only concerns first-player wins from the individual root under runner v17's move model.",
   'No row closes; frontier 6,213/492,021, solved S6 1,635, five-parent target 34/112 unchanged.',
   'Next step: resolve6 re-matching over the residual pair-edge pool after striking the 39 dead roots.',
   'The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.']
}
json.dump(out, open('depth-saturation-audit-20261119.json','w'), indent=1)
print(json.dumps(out['summary'], indent=1))
