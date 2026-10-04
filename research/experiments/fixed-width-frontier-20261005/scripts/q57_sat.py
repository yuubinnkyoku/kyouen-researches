#!/usr/bin/env python3
"""Finite q=7,w=5 probes using all clipped seven/eight-point circles."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

if not __debug__:
    raise SystemExit('Exact validation requires assertions; do not use -O.')

def geometry_from_maximum(m,source,max_m):
    cs=set()
    for curve in source:
        ps=tuple(p//max_m*m+p%max_m for p in curve if p%max_m<m)
        if len(ps)>=7:cs.add(ps)
    return sorted(cs)

def encode(m,target,curves,encoding='aggregate'):
    from pysat.card import CardEnc,EncType
    from pysat.formula import IDPool
    pool=IDPool(start_from=5*m+1)
    clauses=[]
    for y in range(5):
        clauses += CardEnc.atmost(list(range(y*m+1,(y+1)*m+1)),
                    bound=5 if y==target else 6,vpool=pool,
                    encoding=EncType.seqcounter).clauses
    for curve in curves:
        clauses.extend([-p-1 for p in subset] for subset in combinations(curve,7))
    blockers=[[] for _ in range(m)]
    for curve in curves:
        if encoding=='aggregate':
            b=pool.id()
            # Under the existing <=6 safety constraint, b means exactly six
            # occupied points. Every (k-6+1)-subset must contain one occupied.
            clauses.extend([-b]+[p+1 for p in subset]
                           for subset in combinations(curve,len(curve)-6+1))
            for p in curve:
                if p//m==target:blockers[p%m].append(b)
        else:
            for p in curve:
                if p//m!=target:continue
                for subset in combinations([v for v in curve if v!=p],6):
                    b=pool.id();blockers[p%m].append(b)
                    clauses.extend([[-b,v+1] for v in subset])
    clauses.extend([target*m+x+1]+options for x,options in enumerate(blockers))
    return clauses,pool.top

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pysat-path',default='/workspace/research-tools/python-sat')
    ap.add_argument('--circles',type=Path,required=True)
    ap.add_argument('--max-m',type=int,default=200)
    ap.add_argument('--m',type=int,nargs='+',required=True)
    ap.add_argument('--seconds',type=int,default=10)
    ap.add_argument('--encoding',choices=['aggregate','expanded'],default='aggregate')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args();sys.path.insert(0,args.pysat_path)
    from pysat.solvers import Cadical195
    source=[tuple(map(int,line.split())) for line in args.circles.read_text().splitlines()]
    results=[]
    for m in args.m:
        curves=geometry_from_maximum(m,source,args.max_m)
        for target in range(3):
            clauses,nv=encode(m,target,curves,args.encoding)
            started=time.monotonic();result=None
            with Cadical195(bootstrap_with=clauses) as solver:
                while result is None and time.monotonic()-started<args.seconds:
                    solver.conf_budget(20000);result=solver.solve_limited()
                model=set(solver.get_model()) if result is True else None
                stats=solver.accum_stats()
            rows=[[x for x in range(m) if y*m+x+1 in model] for y in range(5)] if model else None
            if rows is not None:
                occupied={y*m+x for y,row in enumerate(rows) for x in row}
                assert len(rows[target])<=5 and all(len(row)<=6 for row in rows)
                assert all(len(set(curve) & occupied)<=6 for curve in curves)
                assert all(any(p in curve and len(set(curve) & occupied)==6 for curve in curves)
                           for p in range(target*m,(target+1)*m) if p not in occupied)
            record=dict(m=m,target=target,status='SAT' if result is True else 'UNSAT' if result is False else 'UNKNOWN',
                        variables=nv,clauses=len(clauses),curves=len(curves),rows=rows,
                        solver_statistics=stats,wall_seconds=time.monotonic()-started,
                        encoding=args.encoding,
                        proof_kind='Finite SAT probe, no independently checked proof trace yet')
            results.append(record);print(json.dumps(record),flush=True)
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(json.dumps(results,indent=2)+'\n')

if __name__=='__main__':main()
