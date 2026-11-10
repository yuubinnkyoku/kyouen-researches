"""Bounded point exchange around a fixed-origin, fixed-complete-pair seed."""
import argparse
import gzip
import hashlib
import importlib.metadata
import importlib.util
import json
from pathlib import Path
import sys
import time
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
TERNARY = HERE.parent/'parabola-ternary-selection-20261109/ternary.py'
PROJECTION = HERE.parent/'structural-lemmas-2026-10-02/checks/parabola_half_bound.py'
spec = importlib.util.spec_from_file_location('exchange_ternary', TERNARY)
encoding = importlib.util.module_from_spec(spec)
spec.loader.exec_module(encoding)
sys.path.insert(0, str(PROJECTION.parent))
from parabola_half_bound import clauses_for_pair


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, obj):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(obj, indent=2)+'\n')


def parse_seed(raw):
    v = list(map(int, raw.split()))
    p, n = v[:2]
    points = v[2:]
    assert p >= 5 and p % 2 and len(points) == n
    assert points == sorted(set(points)) and 0 in points and 0 <= points[0] < points[-1] < p
    pairs = [i for i in range(1, (p+1)//2) if i in points and p-i in points]
    assert len(pairs) == 1
    return p, pairs[0], points


def build(p, d, edges, seed, target, max_removed):
    h = (p-1)//2
    assert 3 <= target <= h+2 and 0 <= max_removed <= len(seed)-3
    assert {0, d, p-d} <= set(seed)
    assert all(not (i in seed and p-i in seed) for i in range(1, h+1) if i != d)
    original = clauses_for_pair(p, edges, d)
    clauses, empties = encoding.encode(p, d, original)
    cap = CardEnc.atmost(empties, bound=h+2-target, top_id=3*h, encoding=EncType.seqcounter)
    clauses.extend(cap.clauses)
    prior_top = max(3*h, cap.nv)
    seed_vars = [t if t <= h else h+p-t for t in seed if t not in (0, d, p-d)]
    assert len(seed_vars) == len(seed)-3 and len(seed_vars) == len(set(seed_vars))
    removal = CardEnc.atmost([-v for v in seed_vars], bound=max_removed,
                             top_id=prior_top, encoding=EncType.seqcounter)
    clauses.extend(removal.clauses)
    nv = max(prior_top, removal.nv)
    assert max(abs(v) for c in clauses for v in c) <= nv
    return clauses, nv, prior_top, seed_vars


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--seed', type=Path, required=True)
    ap.add_argument('--edges', type=Path, required=True)
    ap.add_argument('--target', type=int, required=True)
    ap.add_argument('--max-removed', type=int, default=3)
    ap.add_argument('--budget', type=int, default=100000)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    raw = args.seed.read_bytes()
    p, d, seed = parse_seed(raw)
    assert p == 2539 and len(seed) < args.target and args.budget > 0
    edge_raw = gzip.decompress(args.edges.read_bytes())
    lines = edge_raw.decode('ascii').splitlines()
    assert lines[0] == '2539 38868'
    edges = [tuple(map(int, line.split())) for line in lines[1:]]
    assert len(edges) == 38868 and edges == sorted(set(edges))
    args.output.mkdir(parents=True, exist_ok=False)
    clauses, nv, prior_top, seed_vars = build(p, d, edges, seed, args.target, args.max_removed)
    cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
    (args.output/'input.cnf.gz').write_bytes(gzip.compress(cnf, mtime=0))
    report = dict(p=p, d=d, seed_path=args.seed.as_posix(), seed_size=len(seed), seed_sha256=sha(raw),
                  target=args.target, max_removed=args.max_removed, conflict_budget=args.budget,
                  variables=nv, clauses=len(clauses), prior_top=prior_top, seed_literals=len(seed_vars),
                  input_sha256=sha(cnf), edge_input_sha256=sha(edge_raw),
                  source_sha256=sha(Path(__file__).read_bytes()), ternary_source_sha256=sha(TERNARY.read_bytes()),
                  projection_source_sha256=sha(PROJECTION.read_bytes()), python_sat=importlib.metadata.version('python-sat'),
                  scope='Fixed origin and complete pair; bounded deletions. Negative solver results give no global upper bound. Positive geometry is checked separately.')
    save(args.output/'init.json', report)
    print('READY', args.target, 'd', d, 'vars', nv, 'clauses', len(clauses), flush=True)
    started = time.monotonic()
    with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
        solver.set_phases(encoding.phases(p, d, seed))
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        proof = solver.get_proof() if answer is False else None
        stats = solver.accum_stats()
    report.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',
                  solve_seconds=time.monotonic()-started, statistics=stats)
    if model is not None:
        assert len(model) == nv and {abs(v) for v in model} == set(range(1, nv+1))
        positive = {v for v in model if v > 0}
        assert all(any((v > 0) == (abs(v) in positive) for v in c) for c in clauses)
        points = encoding.parameters(p, d, positive)
        removed, added = sorted(set(seed)-set(points)), sorted(set(points)-set(seed))
        assert len(points) >= args.target and len(removed) <= args.max_removed
        save(args.output/'model.json', dict(signed_model=model))
        candidate = (f'{p} {len(points)}\n'+' '.join(map(str, points))+'\n').encode('ascii')
        (args.output/'candidate.txt').write_bytes(candidate)
        report.update(size=len(points), removed=removed, added=added, candidate_sha256=sha(candidate),
                      all_clauses_checked=True, geometry='NOT_CHECKED')
    if proof is not None:
        proof_raw = ('\n'.join(proof)+'\n').encode('ascii')
        (args.output/'proof.drat.gz').write_bytes(gzip.compress(proof_raw, mtime=0))
        report.update(proof_sha256=sha(proof_raw), proof_lines=len(proof), independent_proof_audit='NOT_RUN')
    save(args.output/'result.json', report)
    print(report['status'], 'size', report.get('size'), 'seconds', report['solve_seconds'], flush=True)


if __name__ == '__main__':
    main()
