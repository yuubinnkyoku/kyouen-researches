#!/usr/bin/env python3
"""Audit the q=7,w=5,m=18 lower-bound witness with all board triples."""
import argparse
from itertools import combinations
import json
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit('Independent validation requires assertions; do not use -O.')

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research/experiments/fixed-width/scripts'))
from q48_exact_threshold import through_three
from curve_packing_fixed_width import bound

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--maximum-circles',type=Path,required=True)
    ap.add_argument('--output',type=Path,default=HERE/'output/q57_independent_witness.json')
    args=ap.parse_args()
    m=18
    rows=[[5,8,12,14,17], [1,3,6,7,8,10], [1,3,6,7,10,12],
          [2,4,7,9,11,14], [4,6,7,9,11,12]]
    board=[(x,y) for y in range(5) for x in range(m)]
    keys={through_three(*ps) for ps in combinations(board,3)}
    occupied={y*m+x for y,row in enumerate(rows) for x in row}
    forbidden=[]
    for key in keys:
        a,b,c,d=key
        curve={k for k,(x,y) in enumerate(board) if a*(x*x+y*y)+b*x+c*y+d==0}
        if len(curve)>=7:forbidden.append((key,curve))
    assert len(occupied)==29
    assert all(len(curve & occupied)<=6 for _,curve in forbidden)
    blockers=[]
    for k,p in enumerate(board):
        if k in occupied:continue
        options=[(key,curve) for key,curve in forbidden if k in curve and len(curve & occupied)==6]
        assert options,(k,p)
        key,curve=options[0]
        blockers.append({'point':p,'primitive_curve':key,
                         'six_existing_points':[board[v] for v in sorted(curve & occupied)]})
    # Geometry from maximum-board pair products must contain the exact same
    # seven/eight-point circles, including circles clipped to seven points.
    maximum=[tuple(map(int,line.split())) for line in args.maximum_circles.read_text().splitlines()]
    induced={tuple(sorted(p//200*m+p%200 for p in c if p%200<m)) for c in maximum
             if sum(p%200<m for p in c)>=7}
    direct={tuple(sorted(curve)) for key,curve in forbidden if key[0]}
    assert direct==induced
    tail=bound(5,7)
    assert tail['packing_U']==200
    out=dict(statement='19 <= M_{5,7} <= 200; exact value unresolved',
             lower_bound_witness=dict(m=m,q=7,rows=rows,stones=29,row_counts=list(map(len,rows)),
                  safe=True,maximal=True,blocked_blanks=len(blockers),blockers=blockers),
             independent_audit=dict(method='all board triples, integer primitive coefficients',
                  triples=len(board)*(len(board)-1)*(len(board)-2)//6,
                  distinct_curves=len(keys),seven_eight_point_circles=len(direct),
                  pair_product_geometry_matches=True),
             universal_tail=tail,
             unresolved='Finite UNKNOWN probes do not exclude deficient maximal configurations')
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'witness':'29 stones safe maximal on 5x18','bound':[19,200],
                      'independent_curves':len(direct)}))

if __name__=='__main__':main()
