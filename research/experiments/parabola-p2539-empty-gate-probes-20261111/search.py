"""One bounded empty-pair point assumption; preserve full models and proofs separately."""
import argparse
import gzip
import importlib.metadata
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195
from encoding import HERE,SEED,SEED_SHA,build,sha,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--point',type=int,required=True);ap.add_argument('--budget',type=int,default=10000);ap.add_argument('--proof',action='store_true');ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();body,meta=build();assert a.point in meta['gate_points'] and a.budget>0
    lines=body.decode('ascii').splitlines();assumption=36512+a.point
    child=('p cnf 51570 144663\n'+'\n'.join(lines[1:])+f'\n{assumption} 0\n').encode('ascii');clauses=[list(map(int,l.split()))[:-1] for l in child.decode('ascii').splitlines()[1:]]
    seed_raw=SEED.read_bytes();assert sha(seed_raw)==SEED_SHA;seed=set(map(int,seed_raw.split()[2:]));phases=[]
    for i in range(1,1270):
        lo,hi=i in seed,2539-i in seed
        phases.extend(4*i-3+j if v else -(4*i-3+j) for j,v in enumerate((lo and hi,not lo and not hi,lo and not hi,hi and not lo)))
    phases.extend(36512+t if t in seed else -(36512+t) for t in range(1,2539))
    a.output.mkdir(parents=True,exist_ok=False)
    r=dict(**meta,point=a.point,assumption=assumption,child_input_sha256=sha(child),child_clauses=144663,conflict_budget=a.budget,proof_enabled=a.proof,
        python_sat=importlib.metadata.version('python-sat'),source_sha256=sha(Path(__file__).read_bytes()))
    save(a.output/'init.json',r);print('READY',a.point,flush=True);started=time.monotonic()
    with Cadical195(bootstrap_with=clauses,with_proof=a.proof) as solver:
        solver.set_phases(phases);solver.conf_budget(a.budget);answer=solver.solve_limited();stats=solver.accum_stats()
        model=solver.get_model() if answer is True else None;proof=solver.get_proof() if a.proof and answer is False else None
    r.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',solve_seconds=time.monotonic()-started,statistics=stats,proof_complete=bool(a.proof and answer is False))
    if proof:
        raw=('\n'.join(proof)+'\n').encode('ascii');(a.output/'proof.drat.gz').write_bytes(gzip.compress(raw,mtime=0));r.update(proof_sha256=sha(raw),proof_lines=len(proof))
    if model is not None:
        assert len(model)==51570 and {abs(v) for v in model}==set(range(1,51571));pos={v for v in model if v>0}
        assert all(any((v>0)==(abs(v) in pos) for v in c) for c in clauses)
        points=[0]+[t for t in range(1,2539) if 36512+t in pos];assert len(points)==1259 and {0,6,2533,a.point}<=set(points)
        assert len(seed-set(points))==5 and not set(points)&set(meta['excluded'])
        assert [i for i in range(1,1270) if i in points and 2539-i in points]==[6]
        save(a.output/'model.json',dict(signed_model=model));raw=(f'2539 1259\n'+' '.join(map(str,points))+'\n').encode('ascii');(a.output/'candidate.txt').write_bytes(raw)
        r.update(candidate_sha256=sha(raw),removed=sorted(seed-set(points)),added=sorted(set(points)-seed),geometry='NOT_CHECKED')
    save(a.output/'result.json',r);print(a.point,r['status'],r['solve_seconds'],flush=True)


if __name__=='__main__':main()
