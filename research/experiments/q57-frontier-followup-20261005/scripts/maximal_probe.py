#!/usr/bin/env python3
"""Bounded q57 probes imposing maximality on every row.

Reuse the complete circle geometry and safe-target encoding. Unlike the
previous necessary-condition probes, add saturation clauses to outside rows
too. UNSAT is a probe unless a separate proof checker verifies a trace.
"""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from pathlib import Path
import sys
import time

if not __debug__:
    raise SystemExit('Validation requires assertions; do not use -O.')

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research/experiments/fixed-width-frontier-20261005/scripts'))
from q57_sat import geometry_from_maximum


def encode(m,target,curves):
    from pysat.card import CardEnc,EncType
    from pysat.formula import IDPool
    pool=IDPool(start_from=5*m+1)
    clauses=[]
    row_full={}
    for y in range(5):
        row=list(range(y*m+1,(y+1)*m+1))
        clauses+=CardEnc.atmost(row,bound=5 if y==target else 6,vpool=pool,
                               encoding=EncType.seqcounter).clauses
        if y!=target:
            flag=pool.id();row_full[y]=flag
            if m>=6:
                counter=CardEnc.atleast(row,bound=6,vpool=pool,
                                       encoding=EncType.seqcounter)
                clauses.extend([-flag]+c for c in counter.clauses)
            else:
                clauses.append([-flag])
    covering=[[] for _ in range(5*m)]
    for curve in curves:
        clauses.extend([-p-1 for p in subset] for subset in combinations(curve,7))
        flag=pool.id()
        clauses.extend([-flag]+[p+1 for p in subset]
                       for subset in combinations(curve,len(curve)-5))
        for p in curve:
            covering[p].append(flag)
    for p in range(5*m):
        clauses.append([p+1]+([row_full[p//m]] if p//m!=target else [])+covering[p])
    return clauses,pool.top


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pysat-path',default='/workspace/research-tools/python-sat')
    ap.add_argument('--circles',type=Path,
                    default=ROOT/'research/experiments/fixed-width-frontier-20261005/output/q57_circles_200.txt')
    ap.add_argument('--m',type=int,nargs='+',default=[19,20,24,28])
    ap.add_argument('--target',type=int,nargs='+',default=[0,1,2])
    ap.add_argument('--seconds',type=float,default=8)
    ap.add_argument('--output',type=Path,default=HERE/'output/maximal-probe.json')
    args=ap.parse_args();sys.path.insert(0,args.pysat_path)
    from pysat.solvers import Cadical195
    source=[tuple(map(int,line.split())) for line in args.circles.read_text().splitlines()]
    out=[]
    for m in args.m:
        curves=geometry_from_maximum(m,source,200)
        for target in args.target:
            clauses,nv=encode(m,target,curves)
            started=time.monotonic();status=None
            with Cadical195(bootstrap_with=clauses) as solver:
                while status is None and time.monotonic()-started<args.seconds:
                    solver.conf_budget(20000);status=solver.solve_limited()
                stats=solver.accum_stats()
                selected=set(solver.get_model()) if status is True else None
            rows=None
            if selected is not None:
                rows=[[x for x in range(m) if y*m+x+1 in selected] for y in range(5)]
                occupied={y*m+x for y,row in enumerate(rows) for x in row}
                assert len(rows[target])<=5 and all(len(row)<=6 for row in rows)
                assert all(len(occupied & set(curve))<=6 for curve in curves)
                assert all(len(rows[p//m])==6 or any(p in curve and len(occupied & set(curve))==6
                           for curve in curves) for p in range(5*m) if p not in occupied)
            record=dict(m=m,target=target,status='SAT' if status is True else 'UNSAT' if status is False else 'UNKNOWN',
                        rows=rows,variables=nv,clauses=len(clauses),curves=len(curves),
                        elapsed_seconds=time.monotonic()-started,statistics=stats,
                        evidence='finite bounded probe; UNSAT has no independently checked trace')
            out.append(record)
            print(json.dumps(record),flush=True)
            args.output.parent.mkdir(parents=True,exist_ok=True)
            args.output.write_text(json.dumps(out,indent=2)+'\n')


if __name__=='__main__':
    main()
