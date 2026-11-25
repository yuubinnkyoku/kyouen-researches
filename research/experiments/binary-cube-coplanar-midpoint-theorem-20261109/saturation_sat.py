#!/usr/bin/env python3
"""Encode fixed-edge C4-saturated graphs of a specified exact edge count."""
import argparse
import gzip
import hashlib
from itertools import combinations, permutations
import json
from pathlib import Path

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195


def encode(n, size):
    edges = list(combinations(range(n), 2))
    var = {e: i + 1 for i, e in enumerate(edges)}
    edge = lambda u, v: var[tuple(sorted((u, v)))]
    clauses = [[edge(0, 1)]]
    for a, b, c, d in combinations(range(n), 4):
        for cycle in ((a,b,c,d), (a,b,d,c), (a,c,b,d)):
            clauses.append([-edge(cycle[i],cycle[(i+1)%4]) for i in range(4)])
    counter = CardEnc.equals(list(var.values()), bound=size, top_id=len(edges), encoding=EncType.seqcounter)
    clauses.extend(counter.clauses)
    top = max(len(edges), counter.nv)
    for u, v in edges:
        witnesses = []
        for a, b in permutations((x for x in range(n) if x not in (u,v)), 2):
            top += 1
            witnesses.append(top)
            for lit in (edge(u,a), edge(a,b), edge(b,v)):
                clauses.append([-top, lit])
        clauses.append([edge(u,v)] + witnesses)
    return edges, clauses, top


def verify_model(n, size, edges, model):
    chosen = {e for i, e in enumerate(edges, 1) if i in model}
    assert len(chosen) == size and (0,1) in chosen
    cycles = []
    for a,b,c,d in combinations(range(n),4):
        for q in ((a,b,c,d), (a,b,d,c), (a,c,b,d)):
            cycles.append({tuple(sorted((q[i], q[(i+1)%4]))) for i in range(4)})
    assert all(not c <= chosen for c in cycles)
    assert all(any(c <= chosen | {e} for c in cycles) for e in edges if e not in chosen)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n', type=int, required=True, choices=range(4,12))
    parser.add_argument('--edges', type=int, required=True)
    parser.add_argument('--budget', type=int, default=300000)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not 1 <= args.edges < args.n*(args.n-1)//2 or args.budget <= 0:
        parser.error('invalid edge count or budget')
    args.output.mkdir(parents=True, exist_ok=False)
    edges, clauses, top = encode(args.n, args.edges)
    raw = (f'p cnf {top} {len(clauses)}\n' + ''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()
    with (args.output/'input.cnf.gz').open('wb') as f:
        with gzip.GzipFile(filename='', mode='wb', fileobj=f, mtime=0) as out: out.write(raw)
    print(f'READY variables={top} clauses={len(clauses)}', flush=True)
    with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        proof = solver.get_proof() if answer is False else None
        stats = solver.accum_stats()
    result = {'n':args.n, 'edges':args.edges, 'variables':top, 'clauses':len(clauses),
              'budget':args.budget, 'cnf_sha256':hashlib.sha256(raw).hexdigest(),
              'status':'SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',
              'statistics':stats, 'scope':'fixed edge; UNSAT requires independent proof checking'}
    if model is not None:
        positive = {v for v in model if v > 0}
        assert all(any((lit > 0) == (abs(lit) in positive) for lit in clause) for clause in clauses)
        verify_model(args.n, args.edges, edges, positive)
        result['selected_edges'] = [e for i, e in enumerate(edges, 1) if i in positive]
    if proof is not None:
        proof_raw = ('\n'.join(proof)+'\n').encode()
        result['proof_sha256'] = hashlib.sha256(proof_raw).hexdigest()
        result['proof_lines'] = len(proof)
        with (args.output/'proof.drat.gz').open('wb') as f:
            with gzip.GzipFile(filename='', mode='wb', fileobj=f, mtime=0) as out: out.write(proof_raw)
    (args.output/'result.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2), flush=True)


if __name__ == '__main__':
    main()
