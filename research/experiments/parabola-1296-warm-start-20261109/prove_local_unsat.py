#!/usr/bin/env python3
"""Produce a DRAT proof for a saved local-search CNF, without overwriting it."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import time
from pysat.solvers import Cadical195


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('directory',type=Path)
    args=ap.parse_args()
    folder=args.directory
    out=folder/'local-proof.drat.gz'
    if out.exists(): raise ValueError('proof already exists')
    raw=gzip.decompress((folder/'input.cnf.gz').read_bytes())
    init=json.loads((folder/'init.json').read_text())
    assert hashlib.sha256(raw).hexdigest()==init['encoded_cnf_sha256']
    lines=raw.decode('ascii').splitlines()
    assert lines[0].split()==['p','cnf',str(init['variables']),str(init['clauses'])]
    clauses=[]
    for line in lines[1:]:
        row=list(map(int,line.split()))
        assert row[-1]==0
        clauses.append(row[:-1])
    assert len(clauses)==init['clauses']
    start=time.monotonic()
    with Cadical195(bootstrap_with=clauses,with_proof=True) as solver:
        answer=solver.solve()
        proof=solver.get_proof() if answer is False else None
        stats=solver.accum_stats()
    assert answer is False and proof
    proof_bytes=('\n'.join(proof)+'\n').encode('ascii')
    with out.open('wb') as f:
        with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:
            z.write(proof_bytes)
    summary={'status':'SOLVER_UNSAT','cnf_sha256':hashlib.sha256(raw).hexdigest(),
             'proof_sha256':hashlib.sha256(proof_bytes).hexdigest(),
             'proof_lines':len(proof),'solve_seconds':time.monotonic()-start,'statistics':stats,
             'scope':f"fixed d=1323, at most {init['max_deletions']} seed deletions; independent proof checking required"}
    (folder/'proof-generation.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))


if __name__=='__main__': main()
