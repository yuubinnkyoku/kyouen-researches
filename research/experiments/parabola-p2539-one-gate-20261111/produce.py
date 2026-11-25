"""One bounded proof-enabled probe of the new exactly-one-empty-gate shape."""
import argparse
import gzip
import hashlib
import importlib.metadata
import itertools
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'parabola-p2539-five-pair-split-20261111/output/retained/input.cnf.gz'
PARENT_SHA='64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b'
PRIOR=HERE.parent/'parabola-p2539-gate-cover-20261111/qualification.json'
SEED=HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,value):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(value,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--budget',type=int,default=100000);a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    parent=gzip.decompress(PARENT.read_bytes());assert sha(parent)==PARENT_SHA
    qr=PRIOR.read_bytes();prior=json.loads(qr);gate=prior['must_add_one_of'];excluded=prior['excluded_points'];assert len(gate)==18 and len(excluded)==221 and a.budget>0
    sr=SEED.read_bytes();assert sha(sr)==prior['seed_sha256'];seed=set(map(int,sr.split()[2:]));base=36512
    extra=[[-base-u] for u in excluded]+[[base+u for u in gate]]+[[-base-u,-base-v] for u,v in itertools.combinations(gate,2)]
    assert len(extra)==375;body=('p cnf 51570 144921\n'+'\n'.join(parent.decode('ascii').splitlines()[1:])+'\n'+''.join(' '.join(map(str,c))+' 0\n' for c in extra)).encode('ascii')
    (a.output/'input.cnf.gz').write_bytes(gzip.compress(body,mtime=0));clauses=[list(map(int,l.split()))[:-1] for l in body.decode('ascii').splitlines()[1:]]
    meta=dict(p=2539,variables=51570,clauses=144921,parent_input_sha256=PARENT_SHA,input_sha256=sha(body),prior_qualification_sha256=sha(qr),seed_sha256=sha(sr),gate=gate,excluded_points=excluded,
        conflict_budget=a.budget,python_sat=importlib.metadata.version('python-sat'),proof_enabled=True,source_sha256=sha(Path(__file__).read_bytes()),scope='Exactly one of the18 residual empty-pair points is added, with exact1259 target and exact5 seed losses; a new restricted shape, not a repeat of the unrestricted18 assumptions.')
    save(a.output/'init.json',meta);print('READY exactly-one-gate',flush=True)
    phases=[]
    for i in range(1,1270):
        lo,hi=i in seed,2539-i in seed;phases.extend(4*i-3+j if v else -(4*i-3+j) for j,v in enumerate((lo and hi,not lo and not hi,lo and not hi,hi and not lo)))
    phases.extend(base+t if t in seed else -(base+t) for t in range(1,2539));started=time.monotonic()
    with Cadical195(bootstrap_with=clauses,with_proof=True) as solver:
        solver.set_phases(phases);solver.conf_budget(a.budget);answer=solver.solve_limited();stats=solver.accum_stats()
        model=solver.get_model() if answer is True else None;proof=solver.get_proof() if answer is False else None
    result=dict(**meta,status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',statistics=stats,elapsed_seconds=time.monotonic()-started,proof_complete=answer is False)
    if proof is not None:
        raw=('\n'.join(proof)+'\n').encode('ascii');(a.output/'proof.drat.gz').write_bytes(gzip.compress(raw,mtime=0));result.update(proof_sha256=sha(raw),proof_lines=len(proof))
    if model is not None:
        assert len(model)==51570 and {abs(v) for v in model}==set(range(1,51571));pos={v for v in model if v>0};assert all(any((v>0)==(abs(v) in pos) for v in c) for c in clauses)
        points=[0]+[t for t in range(1,2539) if base+t in pos];assert len(points)==1259 and len(seed-set(points))==5 and len(set(points)&set(gate))==1 and not set(points)&set(excluded)
        save(a.output/'model.json',dict(signed_model=model));raw=(f'2539 1259\n'+' '.join(map(str,points))+'\n').encode('ascii');(a.output/'candidate.txt').write_bytes(raw);result['candidate_sha256']=sha(raw);result['geometry']='NOT_CHECKED'
    save(a.output/'result.json',result);print(result['status'],stats,result['elapsed_seconds'],flush=True)


if __name__=='__main__':main()
