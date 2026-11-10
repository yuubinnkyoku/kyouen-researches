#!/usr/bin/env python3
"""Verify certificates excluding every one-delete/two-add improvement."""
import argparse
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from verify_extensions import det


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('candidate',type=Path)
    ap.add_argument('single_blockers',type=Path)
    ap.add_argument('pair_blockers',type=Path)
    args=ap.parse_args()
    p,n,*pts=map(int,args.candidate.read_text().split())
    assert p==2647 and n==1303 and n==len(pts) and pts==sorted(set(pts))
    assert all(0<=x<p for x in pts)
    selected=set(pts); missing=set(range(p))-selected
    lines=args.single_blockers.read_text().splitlines()
    head=lines[0].split()
    assert head[:6]==['p',str(p),'n',str(n),'missing',str(len(missing))]
    seen=set(); groups=defaultdict(set); empty=0
    for line in lines[1:]:
        fields=line.split(); d=int(fields[0]); assert d in missing and d not in seen; seen.add(d)
        if fields[1]=='OPEN':
            separator=fields.index('|')
            reported=set(map(int,fields[2:separator])); rest=fields[separator+1:]
            assert reported and reported<=selected
        else:
            reported=set(); rest=fields[1:]
        assert len(rest)>=3 and len(rest)%3==0
        values=list(map(int,rest)); common=None
        for i in range(0,len(values),3):
            triple=values[i:i+3]
            assert triple==sorted(set(triple)) and set(triple)<=selected
            assert det([(x,(x*x)%p) for x in (*triple,d)])==0
            common=set(triple) if common is None else common & set(triple)
        assert common==reported
        if not reported: empty+=1
        for remove in reported: groups[remove].add(d)
    assert seen==missing
    expected={(remove,a,b) for remove,points in groups.items()
              for a,b in combinations(sorted(points),2)}
    actual=set()
    for line in args.pair_blockers.read_text().splitlines():
        remove,a,b,t,u=map(int,line.split())
        key=(remove,a,b)
        assert key in expected and key not in actual
        assert t<u and {t,u}<=selected and remove not in (t,u)
        assert det([(x,(x*x)%p) for x in (a,b,t,u)])==0
        actual.add(key)
    assert actual==expected
    print(f'PASS: {len(missing)} missing points, {empty} excluded after any one deletion; '
          f'{len(expected)} candidate pairs all blocked')


if __name__=='__main__':
    main()
