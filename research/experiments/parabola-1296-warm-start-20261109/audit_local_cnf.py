#!/usr/bin/env python3
"""Rebuild the fixed-pair two-deletion CNF and exhaustively test small counters."""
import gzip
import argparse
import hashlib
from itertools import product
import json
from pathlib import Path
import sys
from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
EXP=HERE/'output/target1304-seed1303-delete2-budget300000'
sys.path.insert(0,str(HERE.parent/'parabola-ternary-selection-20261109'))
import ternary as t


def sha(data): return hashlib.sha256(data).hexdigest()


def main():
    global EXP
    ap=argparse.ArgumentParser()
    ap.add_argument('directory', nargs='?', type=Path, default=EXP)
    EXP=ap.parse_args().directory
    tests=0
    for n in range(1,8):
        for limit in range(min(n,3)+1):
            encoded=CardEnc.atmost([-i for i in range(1,n+1)],bound=limit,top_id=n,encoding=EncType.seqcounter)
            with Cadical195(bootstrap_with=encoded.clauses) as solver:
                for states in product((False,True),repeat=n):
                    assumptions=[i if bit else -i for i,bit in enumerate(states,1)]
                    assert solver.solve(assumptions=assumptions)==(states.count(False)<=limit)
                    tests+=1
    init=json.loads((EXP/'init.json').read_text())
    result=json.loads((EXP/'result.json').read_text())
    assert all(result[k]==v for k,v in init.items())
    assert (init['p'],init['d'],init['target'])==(2647,1323,1304)
    assert init['max_deletions'] in (2,3)
    assert init['worker_sha256']==sha((HERE/'probe_local_swap.py').read_bytes())
    assert init['encoder_sha256']==sha(Path(t.__file__).read_bytes())
    base=t.BASE.read_bytes()
    assert sha(base)==init['base_cnf_sha256']==t.BASE_SHA
    warm=(ROOT/init['warm_source']).read_bytes()
    assert sha(warm)==init['warm_input_sha256']
    vals=list(map(int,warm.split()));p,n,*points=vals;h=1323;d=1323
    assert p==2647 and n==1303 and points==sorted(set(points)) and {0,d,p-d}<=set(points)
    assert all(not (i in points and p-i in points) for i in range(1,h))
    original=[list(map(int,line.split()[:-1])) for line in base.decode('ascii').splitlines() if line and line[0] not in 'cp']
    clauses,empty=t.encode(p,d,original)
    card=CardEnc.atmost(empty,bound=h+2-init['target'],top_id=3*h,encoding=EncType.seqcounter)
    clauses.extend(card.clauses);nv=max(3*h,card.nv)
    chosen=[i if i<=h else h+(p-i) for i in points if i not in {0,d,p-d}]
    assert len(chosen)==1300 and len(set(chosen))==1300
    retention=CardEnc.atmost([-v for v in chosen],bound=init['max_deletions'],top_id=nv,encoding=EncType.seqcounter)
    clauses.extend(retention.clauses);nv=max(nv,retention.nv)
    raw=(f'p cnf {nv} {len(clauses)}\n'+''.join(' '.join(map(str,c))+' 0\n' for c in clauses)).encode('ascii')
    assert raw==gzip.decompress((EXP/'input.cnf.gz').read_bytes())
    assert sha(raw)==init['encoded_cnf_sha256'] and nv==init['variables'] and len(clauses)==init['clauses']
    assert result['status']=='SOLVER_UNSAT'
    print(f'PASS: {tests} small signed-counter cases; exact CNF {nv} variables, {len(clauses)} clauses, sha256={sha(raw)}')


if __name__=='__main__': main()
