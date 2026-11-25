"""Independent bounded hitting-tree replay and real integer geometry; no search-code import."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
SEED=HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt'
EDGES=HERE.parent/'parabola-p2539-pair-pilot-20261110/output/edges.txt.gz'
SEED_SHA='454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'
EDGE_SHA='30e5d500f658a7a245fdff3e5c7830dc62b376632f2a6c1e75dea08552671dff'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def no_duplicates(pairs):
    d={}
    for k,v in pairs:
        assert k not in d;d[k]=v
    return d


def check_tree(rows,budget,node):
    rows=list(map(frozenset,rows));counts=Counter()
    def visit(active,k,n):
        assert type(k) is int and k>=0 and type(n) is dict
        kind=n['type'];counts[kind]+=1
        def edge(i):
            assert type(i) is int and i in active;return rows[i]
        if kind=='empty':
            assert set(n)=={'type','edge'} and not edge(n['edge']);return
        if kind=='packing':
            assert set(n)=={'type','edges'} and type(n['edges']) is list and len(n['edges'])==k+1
            used=set()
            for i in n['edges']:
                r=edge(i);assert r and used.isdisjoint(r);used.update(r)
            return
        assert kind=='branch' and set(n)=={'type','edge','children'} and k>0
        r=edge(n['edge']);assert r and type(n['children']) is dict and set(n['children'])=={str(v) for v in r}
        for v in r:visit(frozenset(i for i in active if v not in rows[i]),k-1,n['children'][str(v)])
    visit(frozenset(range(len(rows))),budget,node)
    return dict(counts)


def check_hitting(rows,budget,witness,allowed):
    assert type(witness) is list and all(type(v) is int for v in witness)
    chosen=set(witness);assert len(chosen)==len(witness)<=budget and chosen<=set(allowed)
    assert all(chosen.intersection(row) for row in rows)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    cert_raw=a.certificate.read_bytes();cert=json.loads(cert_raw,object_pairs_hook=no_duplicates)
    assert (cert['p'],cert['seed_size'],cert['fixed'],cert['max_deletions'])==(2539,1258,[0,6,2533],5)
    seed_raw=SEED.read_bytes();eraw=gzip.decompress(EDGES.read_bytes());assert sha(seed_raw)==SEED_SHA==cert['seed_sha256'] and sha(eraw)==EDGE_SHA==cert['edge_input_sha256']
    vals=list(map(int,seed_raw.split()));assert vals[:2]==[2539,1258];seed=set(vals[2:]);fixed={0,6,2533};assert len(seed)==1258 and fixed<=seed
    assert cert['source_sha256']==sha((HERE/'produce.py').read_bytes())
    lines=eraw.splitlines();assert list(map(int,lines[0].split()))==[2539,len(lines)-1]
    quads=[tuple(map(int,l.split())) for l in lines[1:]];assert len(quads)==len(set(quads))
    families={u:[] for u in sorted(set(range(2539))-seed)}
    for q in sorted(quads):
        assert len(q)==4 and list(q)==sorted(set(q)) and all(0<=t<2539 for t in q)
        outside=[t for t in q if t not in seed]
        if len(outside)==1:families[outside[0]].append(q)
    assert [r['point'] for r in cert['entries']]==list(families)
    excluded=[];counts=Counter();geo=[];witness_count=0
    for entry in cert['entries']:
        u=entry['point'];qs=families[u];rows=[set(q)-fixed-{u} for q in qs];assert entry['obstructions']==len(rows)
        if entry['status']=='EXCLUDED':
            counts.update(check_tree(rows,5,entry['refutation']));excluded.append(u)
        else:
            assert entry['status']=='HITTING_WITNESS';check_hitting(rows,5,entry['deletions'],seed-fixed);witness_count+=1
        geo.extend(qs)
    assert excluded==cert['excluded'] and len(geo)==cert['total_obstructions'] and len(geo)==len(set(geo))
    raw=(f'2539 {len(geo)}\n'+''.join(' '.join(map(str,q))+'\n' for q in geo)).encode('ascii')
    (a.output/'geometric-input.txt.gz').write_bytes(gzip.compress(raw,mtime=0))
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp';generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    with tempfile.TemporaryDirectory(prefix='p2539-obstructions-') as temporary:
        td=Path(temporary);exe=td/'geometry.exe';(td/'edges.txt').write_bytes(raw)
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(exe)],check=True,timeout=60)
        r=subprocess.run([str(exe),str(td/'edges.txt')],capture_output=True,text=True,timeout=60)
        geometry=dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,wrapper_source_sha256=sha(wrapper.read_bytes()),generic_source_sha256=sha(generic.read_bytes()),input_sha256=sha(raw))
        save(a.output/'geometry.json',geometry);assert r.returncode==0 and r.stdout.strip()==f'VERIFIED_EDGES 2539 {len(geo)}'
    save(a.output/'summary.json',dict(p=2539,seed_sha256=SEED_SHA,edge_input_sha256=EDGE_SHA,fixed=sorted(fixed),max_deletions=5,all_outside_points=len(families),
        excluded=excluded,excluded_count=len(excluded),provided_obstructions=len(geo),hitting_witness_count=witness_count,refutation_nodes=dict(counts),
        certificate_sha256=sha(cert_raw),verifier_source_sha256=sha(Path(__file__).read_bytes()),geometry_input_sha256=sha(raw),
        scope='Every listed point is impossible in any safe T containing {0,6,2533} and losing at most5 points of this seed. Other points only have hitting witnesses for provided one-added-point obstructions, not safe extensions or geometric completeness.'))
    print('VERIFIED',len(excluded),'excluded points,',witness_count,'necessary-constraint witnesses,',len(geo),'integer-zero quadruples',dict(counts),flush=True)


if __name__=='__main__':main()
