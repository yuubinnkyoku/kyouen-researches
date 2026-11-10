"""Bounded hitting-set certificates for single added-point obstructions, without a SAT solver."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
SEED=HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt'
EDGES=HERE.parent/'parabola-p2539-pair-pilot-20261110/output/edges.txt.gz'
SEED_SHA='454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'
EDGE_SHA='30e5d500f658a7a245fdff3e5c7830dc62b376632f2a6c1e75dea08552671dff'
FIXED={0,6,2533}


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def solve(rows,budget):
    rows=list(map(frozenset,rows));calls=0
    def visit(active,k):
        nonlocal calls;calls+=1
        if not active:return True,[]
        for i in active:
            if not rows[i]:return False,dict(type='empty',edge=i)
        degree=Counter(v for i in active for v in rows[i])
        ordered=sorted(active,key=lambda i:(len(rows[i]),sum(degree[v] for v in rows[i]),i))
        used=set();packing=[]
        for i in ordered:
            if used.isdisjoint(rows[i]):
                used.update(rows[i]);packing.append(i)
                if len(packing)>k:return False,dict(type='packing',edges=packing)
        selected=min(active,key=lambda i:(len(rows[i]),-sum(degree[v] for v in rows[i]),i))
        children={}
        for v in sorted(rows[selected]):
            ok,data=visit(tuple(i for i in active if v not in rows[i]),k-1)
            if ok:return True,sorted(set(data)|{v})
            children[str(v)]=data
        return False,dict(type='branch',edge=selected,children=children)
    ok,data=visit(tuple(range(len(rows))),budget)
    return ok,data,calls


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    seed_raw=SEED.read_bytes();edge_raw=gzip.decompress(EDGES.read_bytes());assert sha(seed_raw)==SEED_SHA and sha(edge_raw)==EDGE_SHA
    vals=list(map(int,seed_raw.split()));assert vals[:2]==[2539,1258];seed=set(vals[2:]);assert len(seed)==1258 and FIXED<=seed
    edges=sorted(set(tuple(map(int,l.split())) for l in edge_raw.splitlines()[1:]))
    families={u:[] for u in range(2539) if u not in seed}
    for q in edges:
        outside=set(q)-seed
        if len(outside)==1:families[next(iter(outside))].append(q)
    entries=[];started=time.monotonic()
    for u,quads in families.items():
        rows=[set(q)-{u}-FIXED for q in quads];ok,data,calls=solve(rows,5)
        entry=dict(point=u,obstructions=len(rows),status='HITTING_WITNESS' if ok else 'EXCLUDED',calls=calls)
        entry['deletions' if ok else 'refutation']=data;entries.append(entry)
    excluded=[r['point'] for r in entries if r['status']=='EXCLUDED']
    result=dict(p=2539,seed_size=1258,fixed=sorted(FIXED),max_deletions=5,seed_sha256=SEED_SHA,edge_input_sha256=EDGE_SHA,
        source_sha256=sha(Path(__file__).read_bytes()),entries=entries,excluded=excluded,total_obstructions=sum(len(v) for v in families.values()),elapsed_seconds=time.monotonic()-started,
        scope='Necessary one-added-point hitting constraints from provided real geometric edges. Negative certificates need independent tree/geometry audit; hitting witnesses do not establish safe improvements or completeness of geometric edges.')
    save(a.output/'certificate.json',result)
    print('PRODUCED',len(entries),'points,',len(excluded),'excluded,',result['total_obstructions'],'obstructions,',sum(r['calls'] for r in entries),'nodes',flush=True)
    print('EXCLUDED',excluded,flush=True)


if __name__=='__main__':main()
