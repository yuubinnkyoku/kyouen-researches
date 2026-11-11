"""Audit every new pair independently and combine all18 negatives with a prior positive gate."""
import argparse
from collections import Counter
import gzip
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
PAIRS=HERE.parent/'parabola-p2539-pair-obstructions-20261111'
spec=importlib.util.spec_from_file_location('gate_cover_single_families',PAIRS/'verify.py');single=importlib.util.module_from_spec(spec);spec.loader.exec_module(single)
checker=single.checker


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(value,indent=2)+'\n')


def inputs(cert):
    sr=checker.SEED.read_bytes();er=gzip.decompress(checker.EDGES.read_bytes());assert sha(sr)==checker.SEED_SHA==cert['seed_sha256'] and sha(er)==checker.EDGE_SHA==cert['edge_input_sha256']
    qr=(HERE.parent/'parabola-p2539-empty-gate-probes-20261111/qualification.json').read_bytes();q=json.loads(qr)
    assert sha(qr)==cert['prior_qualification_sha256'] and cert['gate']==q['must_add_one_of'] and cert['prior_excluded']==q['excluded_points']
    assert cert['p']==2539 and cert['fixed']==[0,6,2533] and cert['max_deletions']==5
    assert q['max_removed']==5 and q['improvement_size_at_least']==1259 and q['necessary_origin']==1 and q['necessary_complete_pair']==[6,2533]
    assert cert['source_sha256']==sha((HERE/'produce.py').read_bytes()) and cert['hitting_search_source_sha256']==sha((single.OLD/'produce.py').read_bytes())
    vals=list(map(int,sr.split()));assert vals[:2]==[2539,1258];seed=set(vals[2:]);assert len(seed)==1258 and {0,6,2533}<=seed
    gate=cert['gate'];excluded=cert['prior_excluded'];assert len(gate)==18 and len(excluded)==124 and set(gate).isdisjoint(seed|set(excluded))
    candidates=sorted(set(range(2539))-seed-set(gate)-set(excluded));assert len(candidates)==1139 and cert['candidates']==candidates
    edges=[tuple(map(int,line.split())) for line in er.splitlines()[1:]];assert len(edges)==len(set(edges))==38868
    fs,_=single.families(seed,edges);two={}
    for edge in edges:
        assert len(edge)==4 and list(edge)==sorted(set(edge)) and all(0<=v<2539 for v in edge)
        outside=tuple(v for v in edge if v not in seed)
        if len(outside)==2:two.setdefault(outside,[]).append(edge)
    return seed,fs,two,q


def case_quads(u,v,fs,two):return sorted(set(fs[u])|set(fs[v])|set(two.get(tuple(sorted((u,v))),[])))


def audit(cert):
    seed,fs,two,prior=inputs(cert);assert [e['point'] for e in cert['entries']]==cert['candidates']
    geometry=set();counts=Counter();closed=[];negative=0;positive=0
    for entry in cert['entries']:
        u=entry['point'];assert [r['gate_point'] for r in entry['cases']]==cert['gate'];all_negative=True
        for case in entry['cases']:
            v=case['gate_point'];qs=case_quads(u,v,fs,two);rows=[set(q)-{0,6,2533,u,v} for q in qs];assert case['obstructions']==len(rows)
            if case['status']=='EXCLUDED':counts.update(checker.check_tree(rows,5,case['refutation']));negative+=1
            else:
                assert case['status']=='HITTING_WITNESS';checker.check_hitting(rows,5,case['deletions'],seed-{0,6,2533});positive+=1;all_negative=False
            geometry.update(qs)
        if all_negative:closed.append(u)
    assert closed==cert['newly_excluded'] and negative==cert['negative_pairs'] and positive==cert['hitting_witness_pairs'] and negative+positive==20502
    return sorted(geometry),dict(newly_excluded=closed,all_excluded=sorted(set(prior['excluded_points'])|set(closed)),remaining_gate=cert['gate'],covered_non_gate_points=len(cert['entries']),covered_pairs=20502,
        negative_pairs=negative,hitting_witness_pairs=positive,refutation_nodes=dict(counts))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    cr=gzip.decompress(a.certificate.read_bytes());cert=json.loads(cr,object_pairs_hook=checker.no_duplicates);geometry,report=audit(cert)
    gr=(f'2539 {len(geometry)}\n'+''.join(' '.join(map(str,q))+'\n' for q in geometry)).encode('ascii');(a.output/'geometric-input.txt.gz').write_bytes(gzip.compress(gr,mtime=0))
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp';generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    with tempfile.TemporaryDirectory(prefix='p2539-gate-cover-') as temporary:
        td=Path(temporary);exe=td/'geometry.exe';(td/'input.txt').write_bytes(gr)
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(exe)],check=True,timeout=60)
        r=subprocess.run([str(exe),str(td/'input.txt')],capture_output=True,text=True,timeout=60)
        save(a.output/'geometry.json',dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,input_sha256=sha(gr),wrapper_source_sha256=sha(wrapper.read_bytes()),generic_source_sha256=sha(generic.read_bytes())))
        assert r.returncode==0 and r.stdout.strip()==f'VERIFIED_EDGES 2539 {len(geometry)}'
    save(a.output/'summary.json',dict(**report,geometric_quadruples=len(geometry),certificate_sha256=sha(cr),geometry_input_sha256=sha(gr),source_sha256=sha(Path(__file__).read_bytes()),
        single_family_source_sha256=sha((PAIRS/'verify.py').read_bytes()),hitting_verifier_source_sha256=sha((single.OLD/'verify.py').read_bytes()),prior_qualification_sha256=cert['prior_qualification_sha256'],
        scope='Every new point has all18 pair cases independently excluded. Together with the prior necessary positive gate, safe improvements with at most5 seed losses avoid the new points. Other pair witnesses are not safe improvements; no new native RUP claim.'))
    print('VERIFIED',len(report['newly_excluded']),'new exclusions;',len(report['all_excluded']),'total;',len(geometry),'integer-zero quadruples;',dict(counts) if False else report['refutation_nodes'],flush=True)


if __name__=='__main__':main()
