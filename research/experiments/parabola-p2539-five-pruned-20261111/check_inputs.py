"""Check independent parent+geometric units, child status, and any positive model in full geometry."""
import argparse
import gzip
import json
import math
from pathlib import Path
import subprocess
import tempfile
from schema import audit,HERE,sha,SEED_SHA


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saved',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    init=json.loads((a.saved/'init.json').read_bytes());result=json.loads((a.saved/'result.json').read_bytes());launch=json.loads((a.saved/'launch.json').read_bytes())
    assert launch['returncode']==0 and not launch['timed_out'] and all(result[k]==v for k,v in init.items())
    assert sha((HERE/'search.py').read_bytes())==init['source_sha256'] and init['seed_sha256']==SEED_SHA
    raw=gzip.decompress((a.saved/'input.cnf.gz').read_bytes());assert sha(raw)==init['input_sha256']
    seed_raw=(HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt').read_bytes();seed=list(map(int,seed_raw.split()))[2:]
    geometry,obstructions,report=audit(raw,seed);report['schema_source_sha256']=sha((HERE/'schema.py').read_bytes());save(a.output/'schema.json',report)
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp';generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp';checks=[]
    with tempfile.TemporaryDirectory(prefix='p2539-pruned-input-') as temporary:
        td=Path(temporary);exe=td/'geometry.exe';subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(exe)],check=True,timeout=60)
        for name,edges in [('parent',geometry),('hitting-obstructions',obstructions)]:
            eraw=(f'2539 {len(edges)}\n'+''.join(' '.join(map(str,q))+'\n' for q in edges)).encode('ascii');(td/'edges.txt').write_bytes(eraw)
            r=subprocess.run([str(exe),str(td/'edges.txt')],capture_output=True,text=True,timeout=60)
            assert r.returncode==0 and r.stdout.strip()==f'VERIFIED_EDGES 2539 {len(edges)}'
            checks.append(dict(kind=name,quadruples=len(edges),returncode=r.returncode,stdout=r.stdout,input_sha256=sha(eraw)))
        verified_safe=False
        if result['status']=='SAT':
            model=json.loads((a.saved/'model.json').read_bytes())['signed_model'];assert len(model)==51570 and {abs(v) for v in model}==set(range(1,51571));pos={v for v in model if v>0}
            clauses=[list(map(int,l.split()))[:-1] for l in raw.decode('ascii').splitlines()[1:]];assert all(any((v>0)==(abs(v) in pos) for v in c) for c in clauses)
            points=[0]+[t for t in range(1,2539) if 36512+t in pos];candidate=(a.saved/'candidate.txt').read_bytes()
            assert list(map(int,candidate.split()))==[2539,1259]+points and len(points)==1259 and {0,6,2533}<=set(points)
            assert len(set(seed)-set(points))==5 and not set(points).intersection(report['excluded']) and sha(candidate)==result['candidate_sha256']
            subset=td/'subset.exe';subprocess.run(['g++','-O2','-std=c++17',str(generic),'-o',str(subset)],check=True,timeout=60)
            r=subprocess.run([str(subset),'--modular-filter'],input=candidate,capture_output=True,timeout=180)
            assert r.returncode==0 and list(map(int,r.stdout.split()))[:3]==[2539,1259,math.comb(1259,4)];verified_safe=True
            save(a.output/'witness.json',dict(returncode=r.returncode,stdout=r.stdout.decode(),candidate_sha256=sha(candidate)))
        else:assert not (a.saved/'model.json').exists() and not (a.saved/'candidate.txt').exists()
    save(a.output/'summary.json',dict(status=result['status'],verified_safe=verified_safe,independent_unsat_proof=False,input_sha256=sha(raw),seed_sha256=SEED_SHA,
        geometry_checks=checks,generic_source_sha256=sha(generic.read_bytes()),wrapper_source_sha256=sha(wrapper.read_bytes()),
        source_sha256=sha(Path(__file__).read_bytes()),scope='Parent and60 independent geometric units checked. UNKNOWN remains unresolved; negative solver status is not independently certified here.'))
    print('CHECK pruned60',result['status'],'independently safe',verified_safe,'geometry',[(r['kind'],r['quadruples']) for r in checks],flush=True)


if __name__=='__main__':main()
