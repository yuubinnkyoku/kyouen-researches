#!/usr/bin/env python3
"""Verify direct geometric blockers for every absent point of a saved candidate."""
import argparse
from pathlib import Path


def det(points):
    # Independent translated 3x3 determinant, with original x²+y² column.
    x0, y0 = points[0]
    rows = [(x-x0, y-y0, x*x+y*y-x0*x0-y0*y0) for x, y in points[1:]]
    (a,b,c),(d,e,f),(g,h,i) = rows
    return a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('candidate',type=Path)
    ap.add_argument('blockers',type=Path)
    args=ap.parse_args()
    p,n,*pts=map(int,args.candidate.read_text().split())
    assert p==2647 and n==len(pts) and pts==sorted(set(pts))
    assert all(0<=x<p for x in pts)
    selected=set(pts)
    lines=args.blockers.read_text().splitlines()
    hdr=lines[0].split()
    assert hdr[0:6]==['p',str(p),'n',str(n),'missing',str(p-n)]
    assert hdr[6]=='blocked' and int(hdr[7])==p-n
    absent=set(range(p))-selected
    seen=set()
    for line in lines[1:]:
        values=line.split()
        assert len(values)==4
        d,a,b,c=map(int,values)
        assert d in absent and d not in seen
        assert a<b<c and {a,b,c}<=selected
        assert det([(t,(t*t)%p) for t in (a,b,c,d)])==0
        seen.add(d)
    assert seen==absent
    print(f'PASS: all {len(seen)} absent points have explicit forbidden quadruple witnesses')


if __name__=='__main__':
    main()
