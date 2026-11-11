"""Exhaust the153 pairs in the residual gate using necessary geometric hitting constraints."""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'parabola-p2539-five-obstructions-20261111'
spec=importlib.util.spec_from_file_location('gate_pair_hitting_search',OLD/'produce.py')
search=importlib.util.module_from_spec(spec);spec.loader.exec_module(search)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(value,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    sr=search.SEED.read_bytes();er=gzip.decompress(search.EDGES.read_bytes());assert sha(sr)==search.SEED_SHA and sha(er)==search.EDGE_SHA
    seed=set(map(int,sr.split()[2:]));fixed={0,6,2533};edges=[tuple(map(int,l.split())) for l in er.splitlines()[1:]]
    qr=(HERE.parent/'parabola-p2539-empty-gate-probes-20261111/qualification.json').read_bytes();qualification=json.loads(qr);gate=qualification['must_add_one_of'];assert len(gate)==18 and not set(gate)&seed
    rows=[]
    for u,v in itertools.combinations(gate,2):
        pair={u,v};qs={q for q in edges if set(q)-seed and set(q)-seed<=pair}
        if u+v==2539:qs.add(tuple(sorted((6,2533,u,v))))
        qs=sorted(qs);ok,data,calls=search.solve([set(q)-pair-fixed for q in qs],5)
        item=dict(pair=[u,v],obstructions=len(qs),status='HITTING_WITNESS' if ok else 'EXCLUDED',calls=calls)
        item['deletions' if ok else 'refutation']=data;rows.append(item)
    excluded=[r['pair'] for r in rows if r['status']=='EXCLUDED'];print('PRODUCED',len(rows),'pairs;',len(excluded),'excluded;',sum(r['calls'] for r in rows),'calls',flush=True)
    save(a.output/'certificate.json',dict(p=2539,seed_sha256=sha(sr),edge_input_sha256=sha(er),prior_qualification_sha256=sha(qr),gate=gate,fixed=sorted(fixed),max_deletions=5,
        entries=rows,excluded_pairs=excluded,source_sha256=sha(Path(__file__).read_bytes()),hitting_search_source_sha256=sha((OLD/'produce.py').read_bytes()),
        scope='Pair incompatibility from provided geometric quadruples only; positive hitting witnesses do not establish safe extensions.'))
    print('EXCLUDED',excluded,flush=True)


if __name__=='__main__':main()
