"""Bound the number of removed seed points in a fixed-pair SAT neighborhood."""
import argparse
import gzip
import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import time
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
SNAPSHOT = HERE.parent/'parabola-warm-improvement-20261109/encoding_snapshot.py'
spec = importlib.util.spec_from_file_location('frozen_ternary', SNAPSHOT)
encoding = importlib.util.module_from_spec(spec)
spec.loader.exec_module(encoding)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def removal_counter(point_variables, bound, top_id):
    card = CardEnc.atmost([-v for v in point_variables], bound=bound,
                         top_id=top_id, encoding=EncType.seqcounter)
    return card.clauses, max(top_id, card.nv)


def build(seed, target, max_removed):
    p, d, h = 2647, 1323, 1323
    base = encoding.BASE.read_bytes()
    assert sha(base) == encoding.BASE_SHA
    original = [list(map(int, row.split()[:-1])) for row in base.decode('ascii').splitlines()
                if row and row[0] not in 'cp']
    clauses, empties = encoding.encode(p, d, original)
    card = CardEnc.atmost(empties, bound=h+2-target, top_id=3*h, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    prior_top = max(3*h, card.nv)
    point_vars = [t if t <= h else h+p-t for t in seed if t not in (0, d, p-d)]
    assert len(point_vars) == len(seed)-3 and len(set(point_vars)) == len(point_vars)
    extra, nv = removal_counter(point_vars, max_removed, prior_top)
    assert all(abs(v) <= prior_top or abs(v) > 3*h for c in extra for v in c)
    clauses.extend(extra)
    return clauses, nv, prior_top, point_vars


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=Path, required=True)
    ap.add_argument('--target', type=int, required=True)
    ap.add_argument('--max-removed', type=int, required=True)
    ap.add_argument('--budget', type=int, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    raw = args.seed.read_bytes()
    values = list(map(int, raw.split()))
    seed = values[2:]
    assert values[:2] == [2647, len(seed)] and seed == sorted(set(seed))
    assert {0, 1323, 1324} <= set(seed) and all(0 <= t < 2647 for t in seed)
    assert len(seed) < args.target <= 1325 and 0 <= args.max_removed <= len(seed)-3 and args.budget > 0
    args.output.mkdir(parents=True, exist_ok=False)
    clauses, nv, prior_top, point_vars = build(seed, args.target, args.max_removed)
    cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
    (args.output/'input.cnf.gz').write_bytes(gzip.compress(cnf, compresslevel=1, mtime=0))
    report = dict(p=2647, d=1323, seed_path=args.seed.as_posix(), seed_size=len(seed),
                  seed_sha256=sha(raw), target=args.target, max_removed=args.max_removed,
                  conflict_budget=args.budget, variables=nv, clauses=len(clauses),
                  prior_top_id=prior_top, removal_literals=len(point_vars),
                  input_cnf_sha256=sha(cnf), base_cnf_sha256=encoding.BASE_SHA,
                  encoding_snapshot_sha256=sha(SNAPSHOT.read_bytes()), source_sha256=sha(Path(__file__).read_bytes()),
                  python_sat=importlib.metadata.version('python-sat'), solver='Cadical195',
                  scope='Fixed origin/complete pair, bounded seed deletions. Solver UNSAT needs proof audit; UNKNOWN gives no nonexistence result; positive geometry is separate.')
    save(args.output/'init.json', report)
    print(f'READY target={args.target} max_removed={args.max_removed}', flush=True)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
        solver.set_phases(encoding.phases(2647, 1323, seed))
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        proof = solver.get_proof() if answer is False else None
        statistics = solver.accum_stats()
    report.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',
                  solve_seconds=time.monotonic()-started, statistics=statistics)
    if model is not None:
        assert len(model) == nv and {abs(v) for v in model} == set(range(1, nv+1))
        positive = {v for v in model if v > 0}
        assert all(any((v > 0) == (abs(v) in positive) for v in c) for c in clauses)
        points = encoding.parameters(2647, 1323, positive)
        removed, added = sorted(set(seed)-set(points)), sorted(set(points)-set(seed))
        assert len(points) >= args.target and len(removed) <= args.max_removed
        save(args.output/'model.json', dict(signed_model=model))
        (args.output/'candidate.txt').write_text(f'2647 {len(points)}\n'+' '.join(map(str, points))+'\n', encoding='ascii', newline='\n')
        report.update(size=len(points), removed=removed, added=added, geometry='UNCHECKED')
    if proof is not None:
        proof_raw = ('\n'.join(proof)+'\n').encode('ascii')
        (args.output/'proof.drat.gz').write_bytes(gzip.compress(proof_raw, compresslevel=1, mtime=0))
        report.update(proof_sha256=sha(proof_raw), proof_lines=len(proof), independent_proof_audit='NOT_RUN')
    save(args.output/'result.json', report)
    print(json.dumps(report, indent=2), flush=True)


if __name__ == '__main__':
    main()
