"""Probe the frozen retained-pair input with sixty independently geometric forbidden additions."""
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'parabola-p2539-five-pair-split-20261111/output/retained'
OBSTRUCTIONS=HERE.parent/'parabola-p2539-five-obstructions-20261111'
SEED=HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt'
PARENT_SHA='64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b'
SEED_SHA='454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--budget',type=int,default=100000);ap.add_argument('--proof',action='store_true')
    a=ap.parse_args();assert a.budget>0
    parent=gzip.decompress((PARENT/'input.cnf.gz').read_bytes());assert sha(parent)==PARENT_SHA
    old=json.loads((PARENT/'init.json').read_bytes());assert old['input_sha256']==PARENT_SHA and old['point_base']==36512
    ob=json.loads((OBSTRUCTIONS/'audit-output/summary.json').read_bytes());cert=(OBSTRUCTIONS/'output/certificate.json').read_bytes()
    assert ob['certificate_sha256']==sha(cert) and ob['seed_sha256']==SEED_SHA and ob['excluded_count']==60
    excluded=ob['excluded'];assert len(excluded)==60 and excluded==sorted(set(excluded))
    lines=parent.decode('ascii').splitlines();assert lines[0]=='p cnf 51570 144546'
    units=[-(36512+u) for u in excluded]
    body=('p cnf 51570 144606\n'+'\n'.join(lines[1:])+'\n'+''.join(f'{v} 0\n' for v in units)).encode('ascii')
    clauses=[list(map(int,l.split()))[:-1] for l in body.decode('ascii').splitlines()[1:]]
    seed_raw=SEED.read_bytes();assert sha(seed_raw)==SEED_SHA;seed=set(map(int,seed_raw.split()[2:]));assert not seed.intersection(excluded)
    phases=[]
    for i in range(1,1270):
        lo,hi=i in seed,2539-i in seed
        phases.extend(4*i-3+j if v else -(4*i-3+j) for j,v in enumerate((lo and hi,not lo and not hi,lo and not hi,hi and not lo)))
    phases.extend(36512+t if t in seed else -(36512+t) for t in range(1,2539))
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'input.cnf.gz').write_bytes(gzip.compress(body,mtime=0))
    report=dict(p=2539,target=1259,origin=1,complete_pair=[6,2533],removed_exactly=5,point_base=36512,variables=51570,clauses=144606,
        parent_input_sha256=PARENT_SHA,input_sha256=sha(body),seed_sha256=SEED_SHA,excluded=excluded,added_units=units,
        obstruction_certificate_sha256=sha(cert),obstruction_audit_sha256=sha((OBSTRUCTIONS/'audit-output/summary.json').read_bytes()),
        source_sha256=sha(Path(__file__).read_bytes()),conflict_budget=a.budget,proof_enabled=a.proof,python_sat=importlib.metadata.version('python-sat'),
        scope='Retained-pair exact-five UNKNOWN input augmented by60 independently geometric point exclusions. These units are not asserted to be RUP consequences of the parent CNF alone.')
    save(a.output/'init.json',report);print('READY pruned60',a.budget,'proof',a.proof,flush=True);started=time.monotonic()
    with Cadical195(bootstrap_with=clauses,with_proof=a.proof) as solver:
        solver.set_phases(phases);solver.conf_budget(a.budget);answer=solver.solve_limited();stats=solver.accum_stats()
        model=solver.get_model() if answer is True else None;proof=solver.get_proof() if a.proof and answer is False else None
    report.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',solve_seconds=time.monotonic()-started,statistics=stats,proof_complete=bool(a.proof and answer is False))
    if proof:
        raw=('\n'.join(proof)+'\n').encode('ascii');(a.output/'proof.drat.gz').write_bytes(gzip.compress(raw,mtime=0));report.update(proof_sha256=sha(raw),proof_lines=len(proof))
    if model is not None:
        assert len(model)==51570 and {abs(v) for v in model}==set(range(1,51571));pos={v for v in model if v>0}
        assert all(any((v>0)==(abs(v) in pos) for v in c) for c in clauses)
        points=[0]+[t for t in range(1,2539) if 36512+t in pos];assert len(points)==1259 and {0,6,2533}<=set(points)
        assert len(seed-set(points))==5 and not set(points).intersection(excluded)
        assert [i for i in range(1,1270) if i in points and 2539-i in points]==[6]
        save(a.output/'model.json',dict(signed_model=model));raw=(f'2539 1259\n'+' '.join(map(str,points))+'\n').encode('ascii');(a.output/'candidate.txt').write_bytes(raw)
        report.update(candidate_sha256=sha(raw),removed=sorted(seed-set(points)),added=sorted(set(points)-seed),geometry='NOT_CHECKED')
    save(a.output/'result.json',report);print('pruned60',report['status'],report['solve_seconds'],flush=True)


if __name__=='__main__':main()
