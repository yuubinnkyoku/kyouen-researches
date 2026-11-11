#!/usr/bin/env python3
"""Search for C4-saturated graphs with every degree at least two."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195
import saturation_sat


def encode(n, size):
    edges, clauses, top = saturation_sat.encode(n,size)
    for vertex in range(n):
        literals = [i for i,e in enumerate(edges,1) if vertex in e]
        card = CardEnc.atleast(literals,bound=2,top_id=top,encoding=EncType.seqcounter)
        clauses.extend(card.clauses)
        top = max(top,card.nv)
    return edges,clauses,top


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--n',type=int,required=True,choices=range(4,14))
    parser.add_argument('--edges',type=int,required=True)
    parser.add_argument('--budget',type=int,default=500000)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    if not 1 <= args.edges < args.n*(args.n-1)//2 or args.budget <= 0:
        parser.error('invalid edge count or budget')
    args.output.mkdir(parents=True,exist_ok=False)
    edges,clauses,top = encode(args.n,args.edges)
    raw = (f'p cnf {top} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode()
    with (args.output/'input.cnf.gz').open('wb') as f:
        with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z: z.write(raw)
    print(f'READY variables={top} clauses={len(clauses)}',flush=True)
    with Cadical195(bootstrap_with=clauses,with_proof=True) as solver:
        solver.conf_budget(args.budget)
        answer = solver.solve_limited()
        model = solver.get_model() if answer is True else None
        proof = solver.get_proof() if answer is False else None
        stats = solver.accum_stats()
    result = {'n':args.n,'edges':args.edges,'variables':top,'clauses':len(clauses),
              'budget':args.budget,'cnf_sha256':hashlib.sha256(raw).hexdigest(),
              'worker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'encoder_sha256':hashlib.sha256(Path(saturation_sat.__file__).read_bytes()).hexdigest(),
              'status':'SAT' if answer is True else 'SOLVER_UNSAT' if answer is False else 'UNKNOWN',
              'statistics':stats,'scope':'fixed edge and min-degree 2; UNSAT requires independent proof checking'}
    if model is not None:
        positive = {v for v in model if v > 0}
        assert all(any((lit > 0) == (abs(lit) in positive) for lit in clause) for clause in clauses)
        saturation_sat.verify_model(args.n,args.edges,edges,positive)
        chosen = [e for i,e in enumerate(edges,1) if i in positive]
        assert all(sum(v in e for e in chosen) >= 2 for v in range(args.n))
        result['selected_edges'] = chosen
    if proof is not None:
        proof_raw = ('\n'.join(proof)+'\n').encode()
        result['proof_sha256'] = hashlib.sha256(proof_raw).hexdigest()
        result['proof_lines'] = len(proof)
        with (args.output/'proof.drat.gz').open('wb') as f:
            with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z: z.write(proof_raw)
    (args.output/'result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)


if __name__ == '__main__':
    main()
