"""Evaluate new gate/non-gate pairs and cover a point by all18 incompatible gate cases."""
import argparse
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'parabola-p2539-five-obstructions-20261111'
spec=importlib.util.spec_from_file_location('gate_cover_hitting_search',OLD/'produce.py');search=importlib.util.module_from_spec(spec);spec.loader.exec_module(search)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(value,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    sr=search.SEED.read_bytes();er=gzip.decompress(search.EDGES.read_bytes());assert sha(sr)==search.SEED_SHA and sha(er)==search.EDGE_SHA
    seed=set(map(int,sr.split()[2:]));fixed={0,6,2533};outside=set(range(2539))-seed
    qr=(HERE.parent/'parabola-p2539-empty-gate-probes-20261111/qualification.json').read_bytes();prior=json.loads(qr);gate=prior['must_add_one_of'];excluded=set(prior['excluded_points'])
    assert len(gate)==18 and len(excluded)==124 and set(gate)<=outside-excluded
    candidates=sorted(outside-excluded-set(gate));assert len(candidates)==1139
    indexed={}
    for line in er.splitlines()[1:]:
        quad=tuple(map(int,line.split()));key=tuple(sorted(set(quad)-seed))
        if 1<=len(key)<=2:indexed.setdefault(key,set()).add(quad)
    for u in outside:
        if 2539-u in seed:indexed.setdefault((u,),set()).add(tuple(sorted([6,2533,u,2539-u])))
    rows=[];closed=[];negative=0;calls=0;started=time.monotonic()
    for u in candidates:
        entries=[]
        for v in gate:
            pair=tuple(sorted((u,v)));qs=sorted(indexed.get((u,),set())|indexed.get((v,),set())|indexed.get(pair,set()))
            ok,data,n=search.solve([set(q)-fixed-{u,v} for q in qs],5);calls+=n;negative+=not ok
            row=dict(gate_point=v,obstructions=len(qs),status='HITTING_WITNESS' if ok else 'EXCLUDED');row['deletions' if ok else 'refutation']=data;entries.append(row)
        if all(r['status']=='EXCLUDED' for r in entries):closed.append(u)
        rows.append(dict(point=u,cases=entries))
        if len(rows)%200==0:print('DONE',len(rows),'points;',len(closed),'closed;',negative,'negative pairs',flush=True)
    result=dict(p=2539,seed_sha256=sha(sr),edge_input_sha256=sha(er),prior_qualification_sha256=sha(qr),fixed=sorted(fixed),max_deletions=5,gate=gate,prior_excluded=sorted(excluded),
        candidates=candidates,entries=rows,newly_excluded=closed,negative_pairs=negative,hitting_witness_pairs=18*len(candidates)-negative,hitting_calls=calls,elapsed_seconds=time.monotonic()-started,
        source_sha256=sha(Path(__file__).read_bytes()),hitting_search_source_sha256=sha((OLD/'produce.py').read_bytes()),scope='New gate/non-gate pairs only. All18 negative cases cover a point using the prior positive gate. Requires independent hitting and integer-geometry audit; other witnesses are not safe extensions.')
    raw=(json.dumps(result,indent=2)+'\n').encode('utf-8');(a.output/'certificate.json.gz').write_bytes(gzip.compress(raw,mtime=0));save(a.output/'manifest.json',dict(certificate_sha256=sha(raw),compressed_sha256=sha((a.output/'certificate.json.gz').read_bytes()),newly_excluded=closed,negative_pairs=negative,hitting_witness_pairs=result['hitting_witness_pairs']))
    print('PRODUCED',len(rows)*18,'new pairs;',len(closed),'new exclusions;',negative,'negative pairs;',calls,'calls',flush=True);print('NEWLY_EXCLUDED',closed,flush=True)


if __name__=='__main__':main()
