"""Partition the frozen UNKNOWN exact-five input by retention of its original complete pair."""
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'parabola-p2539-exact-five-20261111/output/x1-B1-target1259-remove5'
PARENT_SHA='d23890f881d73064f41719de379346d80193fea8ec507a9f7fe0050edf73f40a'
SEED=HERE.parent/'parabola-p2539-exchange-20261110/output/target1258-remove3/candidate.txt'
SEED_SHA='454f0e293fd846aa6616dd45500dbaf9b325834408ec7f69234852e3e35e22fb'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=['retained','changed'],required=True)
    ap.add_argument('--budget',type=int,default=100000);ap.add_argument('--proof',action='store_true');ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();assert a.budget>0
    parent=gzip.decompress((PARENT/'input.cnf.gz').read_bytes());assert sha(parent)==PARENT_SHA
    old=json.loads((PARENT/'init.json').read_text());assert old['input_sha256']==PARENT_SHA and old['seed_sha256']==SEED_SHA
    lines=parent.decode('ascii').splitlines();_,_,nv,nc=lines[0].split();nv,nc=int(nv),int(nc)
    assert (nv,nc)==(51570,144545)
    unit=21 if a.case=='retained' else -21
    body=(f'p cnf {nv} {nc+1}\n'+'\n'.join(lines[1:])+f'\n{unit} 0\n').encode('ascii')
    clauses=[list(map(int,line.split()))[:-1] for line in body.decode('ascii').splitlines()[1:]]
    seed_raw=SEED.read_bytes();assert sha(seed_raw)==SEED_SHA;seed=set(map(int,seed_raw.split()[2:]))
    phases=[]
    for i in range(1,1270):
        lo,hi=i in seed,2539-i in seed
        phases.extend(4*i-3+j if v else -(4*i-3+j) for j,v in enumerate((lo and hi,not lo and not hi,lo and not hi,hi and not lo)))
    phases.extend(old['point_base']+t if t in seed else -(old['point_base']+t) for t in range(1,2539))
    a.output.mkdir(parents=True,exist_ok=False);(a.output/'input.cnf.gz').write_bytes(gzip.compress(body,mtime=0))
    report=dict(case=a.case,parent_input_sha256=PARENT_SHA,input_sha256=sha(body),seed_sha256=SEED_SHA,split_unit=unit,variables=nv,clauses=nc+1,
        origin=1,complete_pairs=1,target=1259,removed_exactly=5,point_base=old['point_base'],conflict_budget=a.budget,proof_enabled=a.proof,
        source_sha256=sha(Path(__file__).read_bytes()),python_sat=importlib.metadata.version('python-sat'),scope='Frozen exact-five UNKNOWN input plus one unit B6 or not B6. Solver claims need independent audit; models need integer geometry.')
    save(a.output/'init.json',report);print('READY',a.case,'budget',a.budget,'proof',a.proof,flush=True);started=time.monotonic()
    with Cadical195(bootstrap_with=clauses,with_proof=a.proof) as solver:
        solver.set_phases(phases);solver.conf_budget(a.budget);answer=solver.solve_limited();model=solver.get_model() if answer is True else None
        proof=solver.get_proof() if a.proof and answer is False else None;stats=solver.accum_stats()
    report.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',solve_seconds=time.monotonic()-started,statistics=stats,proof_complete=bool(a.proof and answer is False))
    if proof:
        raw=('\n'.join(proof)+'\n').encode('ascii');(a.output/'proof.drat.gz').write_bytes(gzip.compress(raw,mtime=0));report.update(proof_sha256=sha(raw),proof_lines=len(proof))
    if model is not None:
        assert len(model)==nv and {abs(v) for v in model}==set(range(1,nv+1));positive={v for v in model if v>0}
        assert all(any((v>0)==(abs(v) in positive) for v in c) for c in clauses)
        points=[0]+[t for t in range(1,2539) if old['point_base']+t in positive]
        assert len(points)==1259 and len(seed-set(points))==5
        pairs=[i for i in range(1,1270) if i in points and 2539-i in points]
        assert len(pairs)==1 and (pairs[0]==6)==(a.case=='retained')
        save(a.output/'model.json',dict(signed_model=model));raw=(f'2539 1259\n'+' '.join(map(str,points))+'\n').encode('ascii');(a.output/'candidate.txt').write_bytes(raw)
        report.update(candidate_sha256=sha(raw),removed=sorted(seed-set(points)),added=sorted(set(points)-seed),complete_pair=pairs[0],geometry='NOT_CHECKED')
    save(a.output/'result.json',report);print(a.case,report['status'],report['solve_seconds'],flush=True)


if __name__=='__main__':main()
