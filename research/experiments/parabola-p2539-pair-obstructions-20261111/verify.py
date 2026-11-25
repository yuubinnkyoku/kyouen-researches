"""Reconstruct geometric families independently, replay hitting trees and check real determinants."""
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
OLD=HERE.parent/'parabola-p2539-five-obstructions-20261111'
spec=importlib.util.spec_from_file_location('pair_obstruction_verifier',OLD/'verify.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def families(seed,edges,p=2539,fixed_pair=(6,2533)):
    seed=set(seed);a,b=fixed_pair;assert a+b==p and {0,a,b}<=seed
    result={u:set() for u in range(p) if u not in seed};added=set()
    for q in edges:
        outside=[v for v in q if v not in seed]
        if len(outside)==1:result[outside[0]].add(tuple(q))
    for u in result:
        mirror=p-u
        if mirror in seed:
            q=tuple(sorted((a,b,u,mirror)));assert len(set(q))==4 and 0<=q[0]<q[-1]<p
            result[u].add(q);added.add(q)
    return {u:sorted(v) for u,v in result.items()},sorted(added)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--certificate',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    cr=a.certificate.read_bytes();cert=json.loads(cr,object_pairs_hook=checker.no_duplicates)
    assert (cert['p'],cert['seed_size'],cert['fixed'],cert['max_deletions'])==(2539,1258,[0,6,2533],5)
    seed_raw=checker.SEED.read_bytes();eraw=gzip.decompress(checker.EDGES.read_bytes());assert sha(seed_raw)==checker.SEED_SHA==cert['seed_sha256'] and sha(eraw)==checker.EDGE_SHA==cert['edge_input_sha256']
    vals=list(map(int,seed_raw.split()));assert vals[:2]==[2539,1258];seed=set(vals[2:]);assert len(seed)==1258
    edges=[tuple(map(int,l.split())) for l in eraw.splitlines()[1:]];fs,added=families(seed,edges)
    assert [r['point'] for r in cert['entries']]==list(fs) and len(added)==cert['added_pair_quadruples']
    old=json.loads((OLD/'output/certificate.json').read_bytes())['excluded'];excluded=[];counts=Counter();geometry=[];positive=0
    for entry in cert['entries']:
        u=entry['point'];qs=fs[u];rows=[set(q)-{u,0,6,2533} for q in qs];assert entry['obstructions']==len(qs)
        if entry['status']=='EXCLUDED':counts.update(checker.check_tree(rows,5,entry['refutation']));excluded.append(u)
        else:
            assert entry['status']=='HITTING_WITNESS';checker.check_hitting(rows,5,entry['deletions'],seed-{0,6,2533});positive+=1
        geometry.extend(qs)
    assert excluded==cert['excluded'] and set(old)<=set(excluded) and cert['newly_excluded']==sorted(set(excluded)-set(old))
    assert len(geometry)==len(set(geometry))==cert['total_obstructions']
    raw=(f'2539 {len(geometry)}\n'+''.join(' '.join(map(str,q))+'\n' for q in geometry)).encode('ascii');(a.output/'geometric-input.txt.gz').write_bytes(gzip.compress(raw,mtime=0))
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp';generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    with tempfile.TemporaryDirectory(prefix='p2539-pair-obstructions-') as temporary:
        td=Path(temporary);exe=td/'geometry.exe';(td/'edges.txt').write_bytes(raw)
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(exe)],check=True,timeout=60)
        r=subprocess.run([str(exe),str(td/'edges.txt')],capture_output=True,text=True,timeout=60)
        save(a.output/'geometry.json',dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,input_sha256=sha(raw),wrapper_source_sha256=sha(wrapper.read_bytes()),generic_source_sha256=sha(generic.read_bytes())))
        assert r.returncode==0 and r.stdout.strip()==f'VERIFIED_EDGES 2539 {len(geometry)}'
    save(a.output/'summary.json',dict(p=2539,seed_sha256=checker.SEED_SHA,fixed=[0,6,2533],max_deletions=5,all_outside_points=len(fs),excluded=excluded,
        newly_excluded=cert['newly_excluded'],excluded_count=len(excluded),hitting_witness_count=positive,added_pair_quadruples=len(added),geometric_quadruples=len(geometry),refutation_nodes=dict(counts),
        certificate_sha256=sha(cr),source_sha256=sha(Path(__file__).read_bytes()),hitting_verifier_source_sha256=sha((OLD/'verify.py').read_bytes()),geometry_input_sha256=sha(raw),
        scope='Any safe T retaining {0,6,2533} and losing at most5 seed points avoids all listed points. Remaining witnesses only hit the provided necessary obstruction families. New exclusions have geometric/hitting evidence, not new native RUP proofs.'))
    print('VERIFIED',len(excluded),'excluded,',len(cert['newly_excluded']),'new,',len(geometry),'integer-zero quadruples;',dict(counts))


if __name__=='__main__':main()
