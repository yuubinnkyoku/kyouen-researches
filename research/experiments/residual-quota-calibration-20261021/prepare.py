#!/usr/bin/env python3
"""Freeze strata without looking at solver timings or outcomes."""
import argparse,hashlib,itertools,json,pathlib,sys
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=HERE.parent/'residual-gate-calibration-20261021'
SOURCE=ROOT/'research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json'
sys.path.insert(0,str(ROOT/'research/experiments/n11-search-methods/scripts'))
from dfpn_edge_classes import forbidden,d4_canonical_key
sys.path.insert(0,str(HERE.parent/'residual-outcome-search-20261021'))
from oracle import evaluate

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def geometry(occupied):
    occ=sorted(occupied);used=set(occ)
    assert len(used)==len(occ) and all(0<=v<121 for v in occ)
    assert not any(forbidden(*q) for q in itertools.combinations(occ,4))
    triples=list(itertools.combinations(occ,3))
    legal=[v for v in range(121) if v not in used and not any(forbidden(*t,v) for t in triples)]
    edges=[]
    for rank in (2,3,4):
        old=list(itertools.combinations(occ,4-rank))
        for candidate in itertools.combinations(legal,rank):
            if any(forbidden(*candidate,*rest) for rest in old):edges.append(frozenset(candidate))
    edges.sort(key=lambda e:(len(e),sorted(e)))
    minimal=[]
    for edge in edges:
        if not any(other<=edge for other in minimal):minimal.append(edge)
    return dict(occupied=occ,legal=legal,minimal_residual_edges=[sorted(e) for e in minimal])

def choose(pool,old):
    assert pool['seed']==2026102107 and pool['trials']==512 and pool['n']==11
    excluded={d4_canonical_key(s['occupied']) for s in old}
    selected=[];strata=set();trials=set();keys=set()
    for i,s in enumerate(pool['snapshots']):
        group=(len(s['legal']),len(s['occupied'])%2)
        key=d4_canonical_key(s['occupied'])
        if group in strata or s['trial'] in trials or key in excluded or key in keys:continue
        assert 6<=group[0]<=18
        strata.add(group);trials.add(s['trial']);keys.add(key)
        selected.append(dict(pool_index=i,**s))
        if len(selected)==26:break
    assert strata=={(n,p) for n in range(6,19) for p in (0,1)}
    return sorted(selected,key=lambda s:(len(s['legal']),len(s['occupied'])%2))

def rows(fixtures):
    return ''.join(f"fixture,{i},{len(e['occupied'])},{sum(1<<v for v in e['occupied'] if v<64)},{sum(1<<(v-64) for v in e['occupied'] if v>=64)},{len(e['legal'])},0,0,0,0,0\n" for i,e in enumerate(fixtures))

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);args=p.parse_args()
    pool=json.loads((HERE/'candidate-pool.json').read_text())
    original=json.loads(SOURCE.read_text())['snapshots']
    train=[e for e in json.loads((OLD/'fixtures.json').read_text()) if e['split']=='train'];assert len(train)==26
    holdout=[]
    for i,s in enumerate(choose(pool,original)):
        checked=geometry(s['occupied'])
        assert checked['legal']==s['legal']
        assert {frozenset(e) for e in checked['minimal_residual_edges']}=={frozenset(e) for e in s['minimal_residual_edges']}
        g=evaluate(checked);stones=len(s['occupied'])
        holdout.append(dict(id=i,split='new',**s,grundy=g['g'],oracle_states=g['states'],
            result=1 if (g['g']!=0)==(stones%2==0) else 2))
        print(f'new stratum legal={len(s["legal"])} parity={stones%2} independently checked',flush=True)
    (HERE/'fixtures.json').write_text(json.dumps(dict(train=train,new=holdout),indent=2)+'\n')
    for name,data in [('train',train),('new',holdout)]: (HERE/f'{name}-input.csv').write_text(rows(data))
    old_protocol=json.loads((HERE.parent/'residual-outcome-search-20261021/protocol.json').read_text())
    assert digest(pathlib.Path(args.solver))==old_protocol['solver_sha256']
    protocol=dict(seed=2026102107,trials=512,quotas=[128,512,2048],gates=[6,12],repeats=3,board_budget=5000,
        training_roots=26,new_roots=26,stress_roots=3,source_commit=old_protocol['source_commit'],solver_sha256=old_protocol['solver_sha256'],
        hashes={name:digest(HERE/name) for name in ('candidate-pool.json','fixtures.json','train-input.csv','new-input.csv')},
        source_sha256=digest(SOURCE),old_fixtures_sha256=digest(OLD/'fixtures.json'),stress_sha256=digest(OLD/'stress-input.csv'),
        fixture_selection='trial order then chronological first unused stratum; one root per trial; exclude all 826 old roots modulo D4',
        candidate_selection='minimum training UNKNOWN count, sum of per-root solve_us medians, quota, gate; PN candidates only',
        confirmation='OFF versus committed selection on new 26 and stress 3; no reselection',
        adoption='no wrong verdicts, no more UNKNOWN, new solve_us < OFF, stress solve_us <= OFF and no more UNKNOWN',
        default_if_failed='handoff OFF and Grundy evaluator unchanged')
    (HERE/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    print(f'FROZEN train=26 new=26 oracle_states={sum(e["oracle_states"] for e in holdout)} pool={len(pool["snapshots"])}')
if __name__=='__main__':main()
