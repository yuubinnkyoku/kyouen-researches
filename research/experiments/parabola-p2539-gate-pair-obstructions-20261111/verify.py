"""Independently reconstruct pair families, replay trees, and check actual integer geometry."""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import itertools
import json
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'parabola-p2539-five-obstructions-20261111'
spec=importlib.util.spec_from_file_location('gate_pair_hitting_verifier',OLD/'verify.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(value,indent=2)+'\n')


def audit(cert):
    sr=checker.SEED.read_bytes();er=gzip.decompress(checker.EDGES.read_bytes())
    assert sha(sr)==checker.SEED_SHA==cert['seed_sha256'] and sha(er)==checker.EDGE_SHA==cert['edge_input_sha256']
    assert cert['p']==2539 and cert['fixed']==[0,6,2533] and cert['max_deletions']==5
    qr=(HERE.parent/'parabola-p2539-empty-gate-probes-20261111/qualification.json').read_bytes();q=json.loads(qr)
    assert sha(qr)==cert['prior_qualification_sha256'] and cert['gate']==q['must_add_one_of']
    assert cert['source_sha256']==sha((HERE/'produce.py').read_bytes()) and cert['hitting_search_source_sha256']==sha((OLD/'produce.py').read_bytes())
    vals=list(map(int,sr.split()));assert vals[:2]==[2539,1258];seed=set(vals[2:]);fixed={0,6,2533};gate=cert['gate'];assert len(seed)==1258 and fixed<=seed
    assert gate==sorted(set(gate)) and len(gate)==18 and not seed&set(gate)
    all_edges=[tuple(map(int,l.split())) for l in er.splitlines()[1:]]
    assert len(all_edges)==38868==len(set(all_edges))
    indexed={}
    for edge in all_edges:
        assert len(edge)==4 and list(edge)==sorted(set(edge)) and all(0<=v<2539 for v in edge)
        key=frozenset(v for v in edge if v not in seed)
        if key and key<=set(gate):indexed.setdefault(key,set()).add(edge)
    expected=list(itertools.combinations(gate,2));assert [tuple(e['pair']) for e in cert['entries']]==expected
    geometry=set();excluded=[];counts=Counter();positive=0
    for e,(u,v) in zip(cert['entries'],expected):
        quads=set().union(indexed.get(frozenset([u]),set()),indexed.get(frozenset([v]),set()),indexed.get(frozenset([u,v]),set()))
        if v==2539-u:quads.add(tuple(sorted([u,v,6,2533])))
        quads=sorted(quads);rows=[set(quad)-fixed-{u,v} for quad in quads]
        assert e['obstructions']==len(rows)
        if e['status']=='EXCLUDED':counts.update(checker.check_tree(rows,5,e['refutation']));excluded.append([u,v])
        else:
            assert e['status']=='HITTING_WITNESS';checker.check_hitting(rows,5,e['deletions'],seed-fixed);positive+=1
        geometry.update(quads)
    assert excluded==cert['excluded_pairs']
    return sorted(geometry),dict(excluded_pairs=excluded,nonmirror_excluded_pairs=[p for p in excluded if sum(p)!=2539],hitting_witness_pairs=positive,refutation_nodes=dict(counts))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    raw=a.certificate.read_bytes();cert=json.loads(raw,object_pairs_hook=checker.no_duplicates);geometry,report=audit(cert)
    gr=(f'2539 {len(geometry)}\n'+''.join(' '.join(map(str,q))+'\n' for q in geometry)).encode('ascii');(a.output/'geometric-input.txt.gz').write_bytes(gzip.compress(gr,mtime=0))
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp';generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    with tempfile.TemporaryDirectory(prefix='p2539-gate-pair-') as temporary:
        td=Path(temporary);exe=td/'geometry.exe';(td/'input.txt').write_bytes(gr)
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(exe)],check=True,timeout=60)
        r=subprocess.run([str(exe),str(td/'input.txt')],capture_output=True,text=True,timeout=60)
        save(a.output/'geometry.json',dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,input_sha256=sha(gr),wrapper_source_sha256=sha(wrapper.read_bytes()),generic_source_sha256=sha(generic.read_bytes())))
        assert r.returncode==0 and r.stdout.strip()==f'VERIFIED_EDGES 2539 {len(geometry)}'
    save(a.output/'summary.json',dict(**report,covered_pairs=len(cert['entries']),geometric_quadruples=len(geometry),certificate_sha256=sha(raw),geometry_input_sha256=sha(gr),
        source_sha256=sha(Path(__file__).read_bytes()),hitting_verifier_source_sha256=sha((OLD/'verify.py').read_bytes()),
        scope='Verified necessary pair exclusions for any safe T retaining {0,6,2533} and losing at most5 points of the fixed seed. Other pairs only have witnesses for the provided obstruction families.'))
    print('VERIFIED',len(report['excluded_pairs']),'excluded pairs;',len(report['nonmirror_excluded_pairs']),'nonmirror;',len(geometry),'integer-zero quadruples;',report['refutation_nodes'])


if __name__=='__main__':main()
