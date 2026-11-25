#!/usr/bin/env python3
"""Independent geometry audit and complete lower-bound witness validation."""
from __future__ import annotations
import argparse
import hashlib
from itertools import combinations
import json
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit('Independent validation requires assertions; do not run Python with -O.')

from q58_sat import circles, chord_profiles

HERE=Path(__file__).resolve().parents[1]
ROOT=Path(__file__).resolve().parents[4]
sys.path.insert(0,str(ROOT/'research/experiments/fixed-width/scripts'))
from q48_exact_threshold import through_three
from curve_packing_fixed_width import bound


def witness_check():
    m=15
    rows=[[1,3,6,7,9,11], [1,3,4,6,8,11,13], [1,2,4,8,10,11,13],
          [2,3,5,7,9,10,12], [2,4,5,7,8,9,10]]
    board=[(x,y) for y in range(5) for x in range(m)]
    coefficients={through_three(*ps) for ps in combinations(board,3)}
    forbidden=[]
    for key in coefficients:
        a,b,c,d=key
        curve={k for k,(x,y) in enumerate(board) if a*(x*x+y*y)+b*x+c*y+d==0}
        if len(curve)>=8: forbidden.append((key,curve))
    occupied={y*m+x for y,row in enumerate(rows) for x in row}
    assert len(occupied)==34
    assert all(len(occupied & curve)<8 for _,curve in forbidden)
    blockers=[]
    for k,p in enumerate(board):
        if k in occupied:continue
        used=[(key, sorted(occupied & curve)) for key,curve in forbidden
              if k in curve and len(occupied & curve)==7]
        assert used,(k,p)
        key,ids=used[0]
        blockers.append({'point':p,'curve_coefficients':key,
                         'seven_existing_points':[board[i] for i in ids]})
    circle_sets={tuple(sorted(curve)) for key,curve in forbidden if key[0]}
    assert circle_sets==set(circles(m))
    assert sum(key[0]==0 for key,_ in forbidden)==5
    return dict(m=m,q=8,rows=rows,stones=34,row_counts=list(map(len,rows)),
                safe=True,maximal=True,independent_method='all board triples and primitive integer circle/line coefficients',
                triple_count=len(board)*(len(board)-1)*(len(board)-2)//6,
                distinct_curves=len(coefficients),eight_point_circles=len(circle_sets),
                horizontal_lines=5,blocked_blanks=len(blockers),blockers=blockers)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--independent-circles',type=Path,required=True)
    ap.add_argument('--output',type=Path,default=HERE/'output/q58_independent_audit.json')
    args=ap.parse_args()
    external={tuple(map(int,line.split())) for line in args.independent_circles.read_text().splitlines()}
    actual=set(circles(185))
    assert external==actual
    assert len(actual)==2655
    # Every smaller board is an induced geometric subset of the maximum board.
    # Verify all retained curves directly in integer arithmetic and record counts.
    subboards=[]
    for m in range(16,186):
        retained={tuple(y*m+x for y,x in [(p//185,p%185) for p in curve])
                  for curve in external if all(p%185<m for p in curve)}
        assert retained==set(circles(m)), m
        subboards.append({'m':m,'eight_point_circles':len(retained),
                          'complete_circle_sets_match':True})
    profiles=chord_profiles(184)
    assert len(profiles)==19
    tail=bound(5,8)
    assert tail['packing_U']==186
    square_residues={z*z % 9 for z in range(9)}
    mod9_max=max(sum((n-(2*y+c)**2) % 9 in square_residues for y in range(5))
                 for n in range(9) for c in range(9))
    assert mod9_max==4
    result=dict(schema=1,independent_max_board={'m':185,'circle_count':2655,
                    'generation':'C++ equal-sum pair products on adjacent rows; exact quadratic roots',
                    'circle_file_sha256':hashlib.sha256(args.independent_circles.read_bytes()).hexdigest(),
                    'python_circles_match':True},
                circle_profiles_through_span_184=profiles,induced_subboards=subboards,
                lower_bound_witness=witness_check(),universal_tail=tail,
                mod9_five_row_audit={'coefficient_residue_cases':81,
                                    'square_residues':sorted(square_residues),
                                    'maximum_occupied_rows':mod9_max})
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'geometry_match':len(actual),'witness':'34 stones safe maximal',
                      'universal_tail':186,'output':str(args.output)}))


if __name__=='__main__':main()
