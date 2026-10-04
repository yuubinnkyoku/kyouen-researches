#!/usr/bin/env python3
"""Compare every physical SAT model with independent all-maximal census.

On 5x4 there are exactly two eight-point circles. Their union has 14 points;
the other six points must all be occupied in any maximal set. This permits
an exhaustive whole-board maximal census without enumerating SAT auxiliaries.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit('Exact validation requires assertions; do not use -O.')

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research/experiments/fixed-width-frontier-20261005/scripts'))
sys.path.insert(0,'/workspace/research-tools/python-sat')
from q57_sat import geometry_from_maximum
from maximal_probe import encode
from verify_packing import curves_from_triples
from pysat.solvers import Cadical195


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=HERE/'output/maximal-encoding-audit.json')
    args=ap.parse_args()
    m=4;board,independent=curves_from_triples(m)
    curves=[tuple(sorted(pts)) for _,pts in independent]
    active=sorted(set().union(*(set(c) for c in curves)))
    fixed=set(range(5*m))-set(active)
    assert len(curves)==2 and len(active)==14 and len(fixed)==6
    expected=set()
    for mask in range(1<<len(active)):
        occupied=fixed|{p for i,p in enumerate(active) if mask>>i&1}
        if any(sum(p in occupied for p in c)>=7 for c in curves):
            continue
        if all(any(p in c and sum(v in occupied for v in c)==6 for c in curves)
               for p in range(5*m) if p not in occupied):
            expected.add(tuple(sorted(occupied)))
    source=ROOT/'research/experiments/fixed-width-frontier-20261005/output/q57_circles_200.txt'
    maximum=[tuple(map(int,line.split())) for line in source.read_text().splitlines()]
    induced=geometry_from_maximum(m,maximum,200)
    assert set(induced)==set(curves)
    audits=[]
    for target in range(5):
        clauses,nv=encode(m,target,induced)
        observed=set()
        with Cadical195(bootstrap_with=clauses) as solver:
            while solver.solve():
                model=set(solver.get_model())
                selected=tuple(p for p in range(5*m) if p+1 in model)
                assert selected not in observed
                observed.add(selected)
                solver.add_clause([-(p+1) if p in selected else p+1 for p in range(5*m)])
        assert observed==expected
        audits.append(dict(target=target,physical_models=len(observed),variables=nv,clauses=len(clauses)))
    out=dict(board=[5,m],circle_union=len(active),forced_outside_points=len(fixed),
             brute_force_subsets=1<<len(active),maximal_states=len(expected),
             maximal_size_distribution={str(size):sum(len(s)==size for s in expected)
                                       for size in sorted({len(s) for s in expected})},
             sat_model_projection_matches_for_all_targets=audits,
             scope='complete maximal census for 5x4 q7; not a stabilization proof')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':
    main()
