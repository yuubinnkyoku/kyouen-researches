"""Check exact parent+unit partition, independent schema and every saved positive witness."""
import argparse
import gzip
import hashlib
import json
import math
from pathlib import Path
import subprocess
import tempfile
from schema import audit, COUNTER_SOURCE, SEED_SHA

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'parabola-p2539-exact-five-20261111/output/x1-B1-target1259-remove5'
SEED=HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--saved',type=Path,required=True);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    parent=gzip.decompress((PARENT/'input.cnf.gz').read_bytes());assert sha(parent)=='d23890f881d73064f41719de379346d80193fea8ec507a9f7fe0050edf73f40a'
    lines=parent.decode('ascii').splitlines();seed_raw=SEED.read_bytes();assert sha(seed_raw)==SEED_SHA
    tokens=list(map(int,seed_raw.split()));assert tokens[:2]==[2539,1258];seed=tokens[2:];rows=[]
    wrapper=HERE.parent/'parabola-hplus1-drat-20261109/verify_edges.cpp';generic=HERE.parent/'parabola-local-repair-20261109/verify_subset.cpp'
    with tempfile.TemporaryDirectory(prefix='p2539-pair-inputs-') as temporary:
        td=Path(temporary);exe=td/'geometry.exe'
        subprocess.run(['g++','-O2','-std=c++17',str(wrapper),'-o',str(exe)],check=True,timeout=60)
        for case in ['retained','changed']:
            d=a.saved/case;init=json.loads((d/'init.json').read_text());r=json.loads((d/'result.json').read_text());launch=json.loads((d/'launch.json').read_text())
            assert launch['returncode']==0 and not launch['timed_out'];assert all(r[k]==v for k,v in init.items())
            assert sha((HERE/'search.py').read_bytes())==init['source_sha256'] and init['seed_sha256']==SEED_SHA
            unit=21 if case=='retained' else -21
            raw=gzip.decompress((d/'input.cnf.gz').read_bytes())
            expected=('p cnf 51570 144546\n'+'\n'.join(lines[1:])+f'\n{unit} 0\n').encode('ascii')
            assert raw==expected and sha(raw)==init['input_sha256'] and init['parent_input_sha256']==sha(parent)
            edges,report=audit(raw,seed,case)
            eraw=(f'2539 {len(edges)}\n'+''.join(' '.join(map(str,q))+'\n' for q in edges)).encode('ascii');(td/'edges.txt').write_bytes(eraw)
            ge=subprocess.run([str(exe),str(td/'edges.txt')],capture_output=True,text=True,timeout=60)
            assert ge.returncode==0 and ge.stdout.strip()==f'VERIFIED_EDGES 2539 {len(edges)}'
            report.update(input_sha256=sha(raw),seed_sha256=SEED_SHA,schema_source_sha256=sha((HERE/'schema.py').read_bytes()),prefix_source_sha256=sha(COUNTER_SOURCE.read_bytes()),geometry_stdout=ge.stdout,generic_source_sha256=sha(generic.read_bytes()),wrapper_source_sha256=sha(wrapper.read_bytes()))
            save(a.output/(case+'-schema.json'),report)
            row=dict(case=case,status=r['status'],input_sha256=sha(raw),parent_plus_unit_byte_exact=True,independent_schema_geometry=True,verified_safe=False,independent_unsat_proof=False)
            if r['status']=='SAT':
                m=json.loads((d/'model.json').read_bytes())['signed_model'];assert len(m)==51570 and {abs(v) for v in m}==set(range(1,51571));pos={v for v in m if v>0}
                clauses=[list(map(int,line.split()))[:-1] for line in raw.decode('ascii').splitlines()[1:]]
                assert all(any((v>0)==(abs(v) in pos) for v in c) for c in clauses)
                points=[0]+[t for t in range(1,2539) if report['point_base']+t in pos];candidate=(d/'candidate.txt').read_bytes();t=list(map(int,candidate.split()))
                assert t==[2539,1259]+points and len(points)==1259 and len(set(seed)-set(points))==5
                assert sha(candidate)==r['candidate_sha256'];assert ((6 in points and 2533 in points)==(case=='retained'))
                witness=td/'subset.exe';subprocess.run(['g++','-O2','-std=c++17',str(generic),'-o',str(witness)],check=True,timeout=60)
                result=subprocess.run([str(witness),'--modular-filter'],input=candidate,capture_output=True,timeout=180)
                assert result.returncode==0 and list(map(int,result.stdout.split()))[:3]==[2539,1259,math.comb(1259,4)]
                row.update(verified_safe=True,candidate_sha256=sha(candidate),all_clauses_checked=True,geometry_stdout=result.stdout.decode())
            else:assert not (d/'candidate.txt').exists() and not (d/'model.json').exists()
            rows.append(row);print('CHECK',case,r['status'],'safe',row['verified_safe'],flush=True)
    assert {r['case'] for r in rows}=={'retained','changed'}
    save(a.output/'summary.json',dict(cases=rows,exhaustive_partition=True,seed_sha256=SEED_SHA,parent_input_sha256=sha(parent),source_sha256=sha(Path(__file__).read_bytes()),scope='Exhaustive B6/not B6 partition verified by byte comparison, schemas and real geometry. Solver-negative statuses remain unaudited here; only generic-verified positive witnesses establish lower bounds.'))


if __name__=='__main__':main()
