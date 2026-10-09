"""A finite shared-S5 rejection probe, not a probabilistic proof."""
import gzip
import json
from collections import defaultdict
from study import ROOT, EXP, A, s5cache, sha, dump, pts, legal_points

def main():
    out=EXP/'output'
    cache=s5cache(out/'current-exact-s5.cache')
    geo=json.loads(gzip.decompress((out/'geometry.json.gz').read_bytes()))
    hist={(h['stones'],*h['key']):h for h in json.loads((out/'history.json').read_text())}
    for f in out.glob('*/summary.json'):
        for r in json.loads(f.read_text()).get('results',[]):
            if r.get('verdict') is None:
                continue
            k=(r['stones'],*r['key'])
            h=hist.setdefault(k,dict(verdict=0,max_unknown_budget=0))
            if r['verdict']:
                h['verdict']=r['verdict']
                if r['stones']==5:
                    cache[tuple(r['key'])]=r['verdict']
            else:
                h['max_unknown_budget']=max(h['max_unknown_budget'],r['budget'])
    incidence=defaultdict(list)
    candidates=[]
    for g in geo:
        if not {100,108}.intersection(g['coverage']):
            continue
        ch={tuple(c) for c in g['children']}
        if any(cache.get(c)==1 for c in ch) or all(cache.get(c)==2 for c in ch):
            continue
        unknown=ch-cache.keys()
        candidates.append(dict(key=g['key'],unknown=len(unknown),coverage=g['coverage']))
        for c in unknown:
            incidence[c].append(g['key'])
    profile=json.loads((out/'historical-cost-profile.json').read_text())['profile']
    rows=[]
    for k,parents in incidence.items():
        h=hist.get((5,*k),{})
        if h.get('verdict') or h.get('max_unknown_budget',0)>=15_000_000:
            continue
        legal=len(legal_points(pts(k)))
        b=profile.get(str(legal//10*10),dict(n=0,verdicts={},mean_truncated_nodes=15_000_000))
        # Empirical WIN frequency is selection-biased. It only prioritizes
        # an experiment; it cannot be a calibrated probability or verdict.
        freq=(b['verdicts'].get('1',0)+.5)/(b['n']+1)
        score=len(parents)*freq/b['mean_truncated_nodes']
        rows.append(dict(key=k,affected_classes=parents,legal=legal,incidence=len(parents),
                         descriptive_priority=score,historical_bucket=b))
    rows.sort(key=lambda r:(-r['descriptive_priority'],r['legal'],r['key']))
    dump(out/'shared-ranking.json',dict(candidates=candidates,ranking=rows,
           caveat='selection-biased historical frequency, capped cost; ranking only, no calibrated probabilities'))
    dump(out/'shared-plan.json',dict(history_sha256=sha(out/'history.json'),
           selection='eight highest empirical WIN-rejection-per-capped-node shared S5 targets',
           targets=[dict(arm='C_shared',stones=5,key=r['key'],budget=15_000_000,
                         affected_classes=r['affected_classes']) for r in rows[:8]]))
    print('live candidates',len(candidates),'selected',[(r['key'],r['legal'],r['incidence']) for r in rows[:8]],flush=True)

if __name__=='__main__':
    main()
