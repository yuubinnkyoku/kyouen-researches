"""Add complete-pair obstruction quadruples to the frozen single-added-point hitting search."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'parabola-p2539-five-obstructions-20261111'
spec=importlib.util.spec_from_file_location('pair_obstruction_search',OLD/'produce.py')
search=importlib.util.module_from_spec(spec);spec.loader.exec_module(search)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    seed_raw=search.SEED.read_bytes();eraw=gzip.decompress(search.EDGES.read_bytes());assert sha(seed_raw)==search.SEED_SHA and sha(eraw)==search.EDGE_SHA
    seed=set(map(int,seed_raw.split()[2:]));fixed={0,6,2533};families={u:set() for u in range(2539) if u not in seed}
    for q in (tuple(map(int,l.split())) for l in eraw.splitlines()[1:]):
        outside=set(q)-seed
        if len(outside)==1:families[next(iter(outside))].add(q)
    pair_quads=[]
    for u in families:
        if 2539-u in seed:
            q=tuple(sorted([6,2533,u,2539-u]));assert len(set(q))==4
            families[u].add(q);pair_quads.append(q)
    rows=[]
    for u,qs in families.items():
        qs=sorted(qs);ok,data,n=search.solve([set(q)-{u}-fixed for q in qs],5)
        r=dict(point=u,obstructions=len(qs),status='HITTING_WITNESS' if ok else 'EXCLUDED',calls=n);r['deletions' if ok else 'refutation']=data;rows.append(r)
    excluded=[r['point'] for r in rows if r['status']=='EXCLUDED'];previous=json.loads((OLD/'output/certificate.json').read_bytes())['excluded']
    assert set(previous)<=set(excluded)
    save(a.output/'certificate.json',dict(p=2539,seed_size=1258,fixed=sorted(fixed),max_deletions=5,seed_sha256=search.SEED_SHA,edge_input_sha256=search.EDGE_SHA,
        entries=rows,excluded=excluded,newly_excluded=sorted(set(excluded)-set(previous)),added_pair_quadruples=len(pair_quads),total_obstructions=sum(len(v) for v in families.values()),
        source_sha256=sha(Path(__file__).read_bytes()),hitting_search_source_sha256=sha((OLD/'produce.py').read_bytes()),
        scope='Single-added-point obstructions strengthened by actual quadruples consisting of the retained pair and the added point/mirror pair. Negative trees require independent geometry replay.'))
    print('PRODUCED',len(excluded),'excluded,',len(set(excluded)-set(previous)),'new,',len(pair_quads),'pair quadruples',sum(r['calls'] for r in rows),'nodes')


if __name__=='__main__':main()
