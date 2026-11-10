"""Rebuild exact-loss inputs, check complete models and independently verify all witnesses."""
import argparse
import gzip
import json
import math
from pathlib import Path
import subprocess
import tempfile
from search import HERE, FROZEN, build, sha, save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saved',type=Path,required=True);ap.add_argument('--edges',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();args.output.mkdir(parents=True,exist_ok=False)
    edge_raw=gzip.decompress(args.edges.read_bytes());edges=[tuple(map(int,row.split())) for row in edge_raw.decode('ascii').splitlines()[1:]]
    generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp';rows=[]
    with tempfile.TemporaryDirectory(prefix='p2539-exact-loss-audit-') as temporary:
        exe=Path(temporary)/'geometry.exe'
        for folder in sorted(args.saved.iterdir()):
            if not folder.is_dir():continue
            init=json.loads((folder/'init.json').read_text());result=json.loads((folder/'result.json').read_text())
            assert all(result[k]==v for k,v in init.items())
            assert sha((HERE/'search.py').read_bytes())==init['source_sha256']
            assert sha(FROZEN.read_bytes())==init['frozen_source_sha256'] and sha(edge_raw)==init['edge_input_sha256']
            seed_raw=Path(init['seed_path']).read_bytes();assert sha(seed_raw)==init['seed_sha256']
            tokens=list(map(int,seed_raw.split()));p,n,seed=tokens[0],tokens[1],tokens[2:]
            assert p==2539 and n==len(seed) and seed==sorted(set(seed))
            clauses,nv,base,prior,kept,loss=build(p,seed,init['target'],init['origin'],init['complete_pairs'],init['removed_exactly'],edges)
            regenerated=(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')
            raw=gzip.decompress((folder/'input.cnf.gz').read_bytes())
            assert raw==regenerated and sha(raw)==init['input_sha256']
            assert (nv,base,prior,kept,loss)==(init['variables'],init['point_base'],init['base_nv'],init['geometric_clauses'],init['nonzero_removed_exactly'])
            row=dict(case=folder.name,status=result['status'],input_byte_rebuild=True,input_sha256=sha(raw),verified_safe=False,
                     origin=init['origin'],complete_pairs=init['complete_pairs'],independent_negative_proof='NOT_RUN')
            if result['status']=='SAT':
                model_raw=(folder/'model.json').read_bytes();signed=json.loads(model_raw)['signed_model']
                assert len(signed)==nv and {abs(v) for v in signed}==set(range(1,nv+1))
                positive={v for v in signed if v>0};assert all(any((v>0)==(abs(v) in positive) for v in c) for c in clauses)
                points=([0] if init['origin'] else [])+[t for t in range(1,p) if base+t in positive]
                candidate=(folder/'candidate.txt').read_bytes();values=list(map(int,candidate.split()))
                assert values[:2]==[p,init['target']] and values[2:]==points and len(points)==init['target']
                assert len([i for i in range(1,(p+1)//2) if i in points and p-i in points])==init['complete_pairs']
                removed,added=sorted(set(seed)-set(points)),sorted(set(points)-set(seed))
                assert len(removed)==init['removed_exactly'] and removed==result['removed'] and added==result['added']
                assert sha(candidate)==result['candidate_sha256']
                if not exe.exists():subprocess.run(['g++','-O2','-std=c++17',str(generic),'-o',str(exe)],check=True,timeout=60)
                r=subprocess.run([str(exe),'--modular-filter'],input=candidate,capture_output=True,timeout=120)
                assert r.returncode==0 and list(map(int,r.stdout.split()))[:3]==[p,len(points),math.comb(len(points),4)]
                row.update(size=len(points),verified_safe=True,all_clauses_checked=True,candidate_sha256=sha(candidate),model_sha256=sha(model_raw),
                           geometry_stdout=r.stdout.decode(),generic_source_sha256=sha(generic.read_bytes()),removed=removed,added=added)
            else:
                assert not (folder/'model.json').exists() and not (folder/'candidate.txt').exists()
            save(args.output/(folder.name+'.json'),row);rows.append(row)
            print('AUDIT',folder.name,row['status'],'independently safe',row['verified_safe'],flush=True)
    positives=[r for r in rows if r['verified_safe']]
    save(args.output/'summary.json',dict(rows=rows,verified_best_size=max((r['size'] for r in positives),default=None),
         source_sha256=sha(Path(__file__).read_bytes()),scope='Only saved positive witnesses passing independent integer geometry establish safe lower bounds. Negative statuses remain solver-only; exact seed loss is checked separately.'))


if __name__=='__main__':main()
