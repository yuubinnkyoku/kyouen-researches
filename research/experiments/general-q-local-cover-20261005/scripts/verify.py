#!/usr/bin/env python3
"""Exact independent inversion audit for q-general local blocker bounds."""
from __future__ import annotations
import argparse
from collections import Counter
from itertools import combinations
import json
from math import comb,gcd,lcm
from pathlib import Path
import sys

if not __debug__:
    raise SystemExit('Do not disable exact checks with -O.')

ROOT=Path(__file__).resolve().parents[4]
HERE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research/experiments/fixed-width/scripts'))
from q48_exact_threshold import through_three


def normalize(v):
    g=0
    for x in v:g=gcd(g,x)
    v=tuple(x//g for x in v)
    return tuple(-x for x in v) if next(x for x in v if x)<0 else v


def line(a,b):
    x,y=a;u,v=b
    return normalize((y-v,u-x,x*v-u*y))


def invert_to_integer(points,anchor):
    squared=[(x-anchor[0])**2+(y-anchor[1])**2 for x,y in points]
    assert all(squared)
    scale=lcm(*squared)
    return [(scale*(x-anchor[0])//n,scale*(y-anchor[1])//n)
            for (x,y),n in zip(points,squared)]


def rich_bound(n,r):
    assert n>=r+1 and r>=3
    return (comb(n,2)-3)//(comb(r,2)+r-3)


def curve_masks(board):
    keys={through_three(*ps) for ps in combinations(board,3)}
    return {key:sum(1<<i for i,(x,y) in enumerate(board)
                    if key[0]*(x*x+y*y)+key[1]*x+key[2]*y+key[3]==0)
            for key in keys}


def audit_small_board():
    board=[(x,y) for y in range(3) for x in range(4)]
    original=curve_masks(board)
    anchored={}
    for ai,anchor in enumerate(board):
        ids=[i for i in range(len(board)) if i!=ai]
        inverted=invert_to_integer([board[i] for i in ids],anchor)
        keys={line(*ps) for ps in combinations(inverted,2)}
        inverse_masks={sum(1<<i for i,(x,y) in zip(ids,inverted) if a*x+b*y+c==0)
                       for a,b,c in keys}
        direct_masks={mask^(1<<ai) for mask in original.values() if mask>>ai&1}
        # Inverse two-point lines whose original generalized circle contains
        # only anchor+two points are present too; every 3-point curve is in
        # the independent original catalogue, including those circles.
        assert inverse_masks==direct_masks
        anchored[ai]=sorted(inverse_masks)
    summaries=[]
    for q in range(4,9):
        safe=0;empty_tests=0;occupied_tests=0;empty_max=0;occupied_max=0
        for mask in range(1<<len(board)):
            k=mask.bit_count()
            if any((mask&c).bit_count()>=q for c in original.values()):continue
            safe+=1
            for ai in range(len(board)):
                counts=Counter((mask&c).bit_count() for c in anchored[ai])
                if mask>>ai&1:
                    if q>=5 and k>=q:
                        b=counts[q-2]
                        assert b<=rich_bound(k-1,q-2)
                        occupied_tests+=1;occupied_max=max(occupied_max,b)
                elif k>=q:
                    b=counts[q-1]
                    assert b<=rich_bound(k,q-1)
                    empty_tests+=1;empty_max=max(empty_max,b)
                elif k<q-1:
                    assert counts[q-1]==0
                else:
                    assert counts[q-1]<=1
        summaries.append(dict(q=q,safe_states=safe,empty_anchor_tests=empty_tests,
                              occupied_anchor_tests=occupied_tests,
                              maximum_empty_saturated_curves=empty_max,
                              maximum_occupied_saturated_curves=occupied_max))
    return dict(board=[4,3],subsets=1<<len(board),primitive_curves=len(original),
                original_circle_masks_match_inverted_lines_for_anchors=len(board),q_audits=summaries)


def witness(r,occupied):
    # T comprises r collinear points and one point off their line. Integer
    # inversion gives a q-safe set with exactly one saturated anchor curve.
    points=[(i,1) for i in range(r)]+[(0,2)]
    selected=invert_to_integer(points,(0,0))
    scale=lcm(*(x*x+y*y for x,y in points))
    if occupied:selected.append((0,0))
    q=r+2 if occupied else r+1
    assert len(selected)==q
    curves=curve_masks(selected)
    assert all(c.bit_count()<q for c in curves.values())
    through_anchor=[]
    for key in curves:
        if key[3]==0:
            c=curves[key]
            count=c.bit_count()
            if count==q-1:through_anchor.append(key)
    # In the empty-anchor case anchor is absent from the triple catalogue,
    # but the saturated curve is determined by r>=3 selected circle points.
    assert len(through_anchor)==1
    n=q-1 if occupied else q
    assert rich_bound(n,r)==1
    assert through_anchor[0]==(1,0,-scale,0)
    return dict(q=q,occupied_anchor=occupied,points=selected,anchor=[0,0],
                rich_points=r,saturated_curves=1,bound=1,scale=scale,
                primitive_saturated_circle=through_anchor[0])


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output',type=Path,default=HERE/'output/audit.json')
    args=ap.parse_args()
    out=dict(scope='finite exact audit of universal inversion and Melchior proofs',
             small_board=audit_small_board(),
             sharp_smallest_nontrivial_witnesses=[witness(q-1,False) for q in range(4,11)]
                +[witness(q-2,True) for q in range(5,11)])
    p=args.output
    p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out['small_board']))


if __name__=='__main__':main()
