"""Produce proofs only for the three previously negative exact-five CNFs."""
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195

HERE=Path(__file__).resolve().parent
CASES={'x0-B0':(0,0),'x0-B1':(0,1),'x1-B0':(1,0)}


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--case',choices=CASES,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--budget',type=int,default=100000)
    args=ap.parse_args();x,c=CASES[args.case]
    source=HERE/'output'/f'{args.case}-target1259-remove5';init=json.loads((source/'init.json').read_text());original=json.loads((source/'result.json').read_text())
    assert original['status']=='SOLVER_UNSAT'
    body=gzip.decompress((source/'input.cnf.gz').read_bytes());assert sha(body)==init['input_sha256']
    lines=body.decode('ascii').splitlines();_,_,nv,nc=lines[0].split();nv,nc=int(nv),int(nc)
    clauses=[list(map(int,line.split()))[:-1] for line in lines[1:]];assert len(clauses)==nc
    seed_raw=Path(init['seed_path']).read_bytes();assert sha(seed_raw)==init['seed_sha256'];seed=set(map(int,seed_raw.split()[2:]))
    phases=[]
    for i in range(1,1270):
        a,b=i in seed,2539-i in seed
        phases.extend(4*i-3+j if v else -(4*i-3+j) for j,v in enumerate((a and b,not a and not b,a and not b,b and not a)))
    phases.extend(init['point_base']+t if t in seed else -(init['point_base']+t) for t in range(1,2539))
    args.output.mkdir(parents=True,exist_ok=False)
    report=dict(case=args.case,origin=x,complete_pairs=c,input_sha256=sha(body),seed_sha256=sha(seed_raw),conflict_budget=args.budget,
        source_sha256=sha(Path(__file__).read_bytes()),python_sat=importlib.metadata.version('python-sat'),scope='Proof generation for a frozen solver-UNSAT input; not an independent audit. The x1-B1 UNKNOWN case is not rerun.')
    save(args.output/'init.json',report);started=time.monotonic()
    with Cadical195(bootstrap_with=clauses,with_proof=True) as solver:
        solver.set_phases(phases);solver.conf_budget(args.budget);answer=solver.solve_limited();proof=solver.get_proof();stats=solver.accum_stats()
    report.update(status='SOLVER_UNSAT' if answer is False else 'SAT' if answer is True else 'UNKNOWN',proof_complete=answer is False,elapsed_seconds=time.monotonic()-started,statistics=stats)
    if proof:
        raw=('\n'.join(proof)+'\n').encode('ascii');(args.output/'proof.drat.gz').write_bytes(gzip.compress(raw,mtime=0))
        report.update(proof_sha256=sha(raw),proof_lines=len(proof))
    save(args.output/'result.json',report);print(args.case,report['status'],report.get('proof_lines'),report['elapsed_seconds'],flush=True)


if __name__=='__main__':main()
