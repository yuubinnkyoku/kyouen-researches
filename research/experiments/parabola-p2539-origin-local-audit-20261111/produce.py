"""Generate proofs for two frozen negative CNFs; no builder is imported."""
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
PRIOR = HERE.parent/'parabola-p2539-broader-exchange-20261110/output'
CASES = {'changed-pair': 'change-pair-target1259-remove4', 'no-pair': 'no-pair-target1259-remove4'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, obj):
    with path.open('x', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(obj, indent=2)+'\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--case', choices=CASES, required=True)
    ap.add_argument('--output', type=Path, required=True)
    ap.add_argument('--budget', type=int, default=100000)
    args = ap.parse_args()
    source = PRIOR/CASES[args.case]
    init = json.loads((source/'init.json').read_text())
    raw = gzip.decompress((source/'input.cnf.gz').read_bytes())
    assert sha(raw) == init['input_sha256'] and args.budget > 0
    lines = raw.decode('ascii').splitlines()
    _, _, nv, nc = lines[0].split(); nv, nc = int(nv), int(nc)
    clauses = [list(map(int, line.split()))[:-1] for line in lines[1:]]
    assert len(clauses) == nc and max(abs(v) for c in clauses for v in c) <= nv
    args.output.mkdir(parents=True, exist_ok=False)
    seed_raw = Path(init['seed_path']).read_bytes()
    assert sha(seed_raw) == init['seed_sha256']
    seed = set(map(int, seed_raw.split()[2:]))
    phases = []
    if args.case == 'changed-pair':
        for i in range(1, 1270):
            low, high = i in seed, 2539-i in seed
            states = (low and high, not low and not high, low and not high, high and not low)
            phases.extend(4*i-3+j if v else -(4*i-3+j) for j, v in enumerate(states))
    else:
        phases = [init['point_base']+t if t in seed else -(init['point_base']+t) for t in range(1, 2539)]
    report = dict(case=args.case, input_path=(source/'input.cnf.gz').as_posix(), input_sha256=sha(raw),
                  seed_sha256=sha(seed_raw), variables=nv, clauses=nc, conflict_budget=args.budget,
                  phases_sha256=sha((' '.join(map(str, phases))+'\n').encode('ascii')),
                  source_sha256=sha(Path(__file__).read_bytes()), python_sat=importlib.metadata.version('python-sat'),
                  scope='Proof production from a frozen previously solved CNF. Solver status alone does not establish a geometric exclusion.')
    save(args.output/'init.json', report)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
        solver.set_phases(phases)
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        proof = solver.get_proof()
        stats = solver.accum_stats()
    report.update(status='SOLVER_UNSAT' if answer is False else 'SAT' if answer is True else 'UNKNOWN',
                  elapsed_seconds=time.monotonic()-started, statistics=stats, proof_complete=answer is False)
    if proof:
        body = ('\n'.join(proof)+'\n').encode('ascii')
        (args.output/'proof.drat.gz').write_bytes(gzip.compress(body, mtime=0))
        report.update(proof_sha256=sha(body), proof_lines=len(proof))
    save(args.output/'result.json', report)
    print(args.case, report['status'], report.get('proof_lines'), report['elapsed_seconds'], flush=True)


if __name__ == '__main__':
    main()
