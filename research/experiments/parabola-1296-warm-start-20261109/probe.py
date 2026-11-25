#!/usr/bin/env python3
"""Bounded fixed-pair ternary SAT probe seeded by the verified 1296-point witness."""
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import sys
import time
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
sys.path.insert(0, str(HERE.parent / 'parabola-ternary-selection-20261109'))
import ternary as t


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', type=int, required=True)
    ap.add_argument('--budget', type=int, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    p, d, h = 2647, 1323, 1323
    if not 3 <= args.target <= h + 2 or args.budget <= 0:
        raise ValueError('invalid target or budget')
    args.output.mkdir(parents=True, exist_ok=False)
    base = t.BASE.read_bytes()
    if sha(base) != t.BASE_SHA:
        raise ValueError('unexpected direct-projection CNF')
    original = [list(map(int, line.split()[:-1])) for line in base.decode('ascii').splitlines()
                if line and line[0] not in 'cp']
    clauses, empty_vars = t.encode(p, d, original)
    card = CardEnc.atmost(empty_vars, bound=h + 2 - args.target,
                          top_id=3 * h, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    nv = max(3 * h, card.nv)
    dimacs = (f'p cnf {nv} {len(clauses)}\n' + ''.join(
        ' '.join(map(str, c)) + ' 0\n' for c in clauses)).encode('ascii')
    with (args.output / 'input.cnf.gz').open('wb') as stream:
        with gzip.GzipFile(filename='', mode='wb', fileobj=stream, mtime=0) as out:
            out.write(dimacs)
    warm_path = HERE.parent / 'parabola-ternary-selection-20261109/output/target1293-budget100000/candidate.txt'
    warm_bytes = warm_path.read_bytes()
    data = list(map(int, warm_bytes.split()))
    if data[0] != p or data[1] != 1296 or len(data) != 1298 or len(set(data[2:])) != 1296:
        raise ValueError('invalid warm witness')
    report = {'p': p, 'd': d, 'target': args.target, 'empty_bound': h + 2 - args.target,
              'conflict_budget': args.budget, 'variables': nv, 'clauses': len(clauses),
              'base_cnf_sha256': sha(base), 'encoded_cnf_sha256': sha(dimacs),
              'warm_input_sha256': sha(warm_bytes), 'worker_sha256': sha(Path(__file__).read_bytes()),
              'encoder_sha256': sha(Path(t.__file__).read_bytes()),
              'python_sat': importlib.metadata.version('python-sat'), 'solver': 'Cadical195',
              'scope': '0 and pair d fixed; all other pairs low/high/empty; UNSAT is unaudited and applies only to this d'}
    (args.output / 'init.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'READY clauses={len(clauses)} variables={nv}', flush=True)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses) as solver:
        solver.set_phases(t.phases(p, d, data[2:]))
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        stats = solver.accum_stats()
    report.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',
                  solve_seconds=time.monotonic()-started, statistics=stats)
    if model is not None:
        positive = {v for v in model if v > 0}
        if len(model) != nv or {abs(v) for v in model} != set(range(1, nv+1)):
            raise ValueError('invalid SAT model')
        if not all(any((lit > 0) == (abs(lit) in positive) for lit in c) for c in clauses):
            raise ValueError('model violates a clause')
        selected = t.parameters(p, d, positive)
        empties = [i for i in range(1, h+1) if i != d and 2*h+i in positive]
        if len(selected) < args.target or len(selected) != h + 2 - len(empties):
            raise ValueError('invalid candidate size')
        report.update(size=len(selected), empty_pairs=empties, geometry='UNCHECKED')
        (args.output/'model.json').write_text(json.dumps({'signed_model':model})+'\n')
        (args.output/'candidate.txt').write_text(f'{p} {len(selected)}\n'+' '.join(map(str,selected))+'\n', encoding='ascii')
    (args.output / 'result.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({k:report.get(k) for k in ('status','solve_seconds','size','statistics')}), flush=True)


if __name__ == '__main__':
    main()
