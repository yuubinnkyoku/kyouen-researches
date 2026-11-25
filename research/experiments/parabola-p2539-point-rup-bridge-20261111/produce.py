"""Produce bounded refutations of the frozen retained CNF under one forbidden-point assumption."""
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195

HERE=Path(__file__).resolve().parent
PARENT=HERE.parent/'parabola-p2539-five-pair-split-20261111/output/retained/input.cnf.gz'
PARENT_SHA='64496e29f631e4f4090c103e571490f7959a30558462d9b4992ec668633f561b'
OBSTRUCTIONS=HERE.parent/'parabola-p2539-five-obstructions-20261111/output/certificate.json'


def sha(raw):return hashlib.sha256(raw).hexdigest()


def save(path,obj):
    with path.open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(obj,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=int,required=True);ap.add_argument('--budget',type=int,default=10000);ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();cert=json.loads(OBSTRUCTIONS.read_bytes());assert a.point in cert['excluded'] and a.budget>0
    raw=gzip.decompress(PARENT.read_bytes());assert sha(raw)==PARENT_SHA
    lines=raw.decode('ascii').splitlines();assert lines[0]=='p cnf 51570 144546'
    clauses=[list(map(int,l.split()))[:-1] for l in lines[1:]];lit=36512+a.point;clauses.append([lit])
    child=('p cnf 51570 144547\n'+'\n'.join(lines[1:])+f'\n{lit} 0\n').encode('ascii')
    a.output.mkdir(parents=True,exist_ok=False)
    r=dict(point=a.point,assumption=lit,parent_input_sha256=PARENT_SHA,child_input_sha256=sha(child),conflict_budget=a.budget,proof_enabled=True,
        source_sha256=sha(Path(__file__).read_bytes()),python_sat=importlib.metadata.version('python-sat'),scope='Solver refutation under one positive point unit. Not yet a parent-only derivation of its negative.')
    save(a.output/'init.json',r);start=time.monotonic()
    with Cadical195(bootstrap_with=clauses,with_proof=True) as solver:
        solver.conf_budget(a.budget);answer=solver.solve_limited();stats=solver.accum_stats();proof=solver.get_proof() if answer is False else None
    r.update(status='SOLVER_UNSAT' if answer is False else 'SAT' if answer is True else 'UNKNOWN',proof_complete=answer is False,statistics=stats,solve_seconds=time.monotonic()-start)
    if proof:
        body=('\n'.join(proof)+'\n').encode('ascii');(a.output/'child-proof.drat.gz').write_bytes(gzip.compress(body,mtime=0));r.update(proof_sha256=sha(body),proof_lines=len(proof))
    save(a.output/'result.json',r);print(a.point,r['status'],r.get('proof_lines'),r['solve_seconds'],flush=True)


if __name__=='__main__':main()
