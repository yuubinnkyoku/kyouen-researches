"""Try a strictly larger fixed-pair witness using a committed safe warm start."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import importlib.metadata
import json
from pathlib import Path
import time
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195
from encoding_snapshot import BASE, BASE_SHA, encode, parameters, phases


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+'\n', encoding='utf-8', newline='\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', type=int, required=True)
    ap.add_argument('--budget', type=int, required=True)
    ap.add_argument('--warm', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    p, d, h = 2647, 1323, 1323
    warm_raw = args.warm.read_bytes()
    warm = list(map(int, warm_raw.split()))
    assert warm[0] == p and warm[1] == len(warm)-2
    assert warm[2:] == sorted(set(warm[2:])) and {0, d, p-d} <= set(warm[2:])
    assert warm[1] < args.target <= h+2 and args.budget > 0
    args.output.mkdir(parents=True, exist_ok=False)
    base = BASE.read_bytes()
    assert sha(base) == BASE_SHA
    original = [list(map(int, row.split()[:-1])) for row in base.decode('ascii').splitlines() if row and row[0] not in 'cp']
    clauses, empties = encode(p, d, original)
    card = CardEnc.atmost(empties, bound=h+2-args.target, top_id=3*h, encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    nv = max(3*h, card.nv)
    cnf = (f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str, c))+' 0\n' for c in clauses)).encode('ascii')
    (args.output/'input.cnf.gz').write_bytes(gzip.compress(cnf, compresslevel=1, mtime=0))
    report = dict(p=p, d=d, target=args.target, empty_bound=h+2-args.target, conflict_budget=args.budget,
                  variables=nv, clauses=len(clauses), encoded_cnf_sha256=sha(cnf), base_cnf_sha256=BASE_SHA,
                  warm_size=warm[1], warm_input_sha256=sha(warm_raw), warm_source=args.warm.as_posix(),
                  worker_source_sha256=sha(Path(__file__).read_bytes()),
                  encoding_snapshot_sha256=sha(Path(__file__).with_name('encoding_snapshot.py').read_bytes()),
                  python_sat=importlib.metadata.version('python-sat'), solver='Cadical195',
                  scope='0 and complete pair d fixed; UNKNOWN is no nonexistence result; SAT geometry is checked separately.')
    save(args.output/'init.json', report)
    print(f'READY target={args.target} warm={warm[1]}', flush=True)
    start = time.monotonic()
    with Cadical195(bootstrap_with=clauses) as solver:
        solver.set_phases(phases(p, d, warm[2:]))
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        stats = solver.accum_stats()
    report.update(status='SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',
                  solve_seconds=time.monotonic()-start, statistics=stats)
    if model is not None:
        positive = {v for v in model if v > 0}
        assert len(model) == nv and {abs(v) for v in model} == set(range(1, nv+1))
        assert all(any((v > 0) == (abs(v) in positive) for v in c) for c in clauses)
        points = parameters(p, d, positive)
        empty_pairs = [i for i in range(1, h+1) if i != d and 2*h+i in positive]
        assert len(points) >= args.target and len(points) == h+2-len(empty_pairs)
        save(args.output/'model.json', dict(signed_model=model))
        (args.output/'candidate.txt').write_text(f'{p} {len(points)}\n'+' '.join(map(str, points))+'\n', encoding='ascii', newline='\n')
        report.update(size=len(points), empty_pairs=empty_pairs, direct_encoded_clause_violations=0, geometry='UNCHECKED')
    save(args.output/'result.json', report)
    print(json.dumps({key: report.get(key) for key in ('status', 'size', 'solve_seconds')}), flush=True)


if __name__ == '__main__':
    main()
