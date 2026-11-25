#!/usr/bin/env python3
"""Independent exact audit using normalized integer line/circle equations."""
from __future__ import annotations
import json
from itertools import combinations
from math import gcd

W, H = 60, 7
BASE53 = [(21,0),(23,0),(26,0),(18,1),(27,1),(39,1),(14,2),(28,2),(46,2),
          (25,3),(30,3),(39,3),(18,4),(36,4),(43,4),(13,5),(27,5),(35,5),(14,6),(42,6)]
FOUNDB = [(21,0),(23,0),(26,0),(18,1),(27,1),(39,1),(14,2),(46,2),(25,3),
          (30,3),(39,3),(18,4),(43,4),(13,5),(27,5),(35,5),(14,6),(42,6),(56,2),(7,4)]

def norm_line(p, q):
    x1,y1=p; x2,y2=q
    a,b,c=y2-y1,x1-x2,x2*y1-x1*y2
    g=gcd(gcd(abs(a),abs(b)),abs(c))
    if g: a,b,c=a//g,b//g,c//g
    if a<0 or (a==0 and b<0): a,b,c=-a,-b,-c
    return a,b,c

def norm_circle(p, q, r):
    x1,y1=p; x2,y2=q; x3,y3=r
    s1=x1*x1+y1*y1; s2=x2*x2+y2*y2; s3=x3*x3+y3*y3
    det=x1*(y2-y3)-y1*(x2-x3)+(x2*y3-x3*y2)
    if det==0: return None
    B=s1*(y2-y3)-y1*(s2-s3)+(s2*y3-s3*y2)
    C=x1*(s2-s3)-s1*(x2-x3)+(x2*s3-x3*s2)
    D=x1*(y2*s3-y3*s2)-y1*(x2*s3-x3*s2)+s1*(x2*y3-x3*y2)
    a,b,c,d=det,-B,-C,-D
    g=gcd(gcd(gcd(abs(a),abs(b)),abs(c)),abs(d))
    if g: a,b,c,d=a//g,b//g,c//g,d//g
    if a<0: a,b,c,d=-a,-b,-c,-d
    return a,b,c,d

def on_line(co,p):
    a,b,c=co; x,y=p
    return a*x+b*y+c==0

def on_circle(co,p):
    a,b,c,d=co; x,y=p
    return a*(x*x+y*y)+b*x+c*y+d==0

def row_counts(stones):
    return tuple(sum(y==r for x,y in stones) for r in range(H))

def geometry(stones):
    lines={norm_line(p,q) for p,q in combinations(stones,2)}
    line_members={co:[p for p in stones if on_line(co,p)] for co in lines}
    circles={co for tri in combinations(stones,3) if (co:=norm_circle(*tri)) is not None}
    circle_members={co:[p for p in stones if on_circle(co,p)] for co in circles}
    safe=not any(len(ps)>=4 for ps in line_members.values()) and not any(len(ps)>=4 for ps in circle_members.values())
    return safe,line_members,circle_members

def maximal_row(stones,width,row,line_members,circle_members):
    occupied=set(stones)
    for x in range(width):
        q=(x,row)
        if q in occupied: continue
        if any(len(ps)>=3 and on_line(co,q) for co,ps in line_members.items()): continue
        if any(len(ps)>=3 and on_circle(co,q) for co,ps in circle_members.items()): continue
        return False
    return True

def audit(seed_name,native_width,seed):
    assert len(seed)==20 and row_counts(seed)==(3,3,3,3,3,3,2)
    seed_safe,seed_lines,seed_circles=geometry(seed)
    assert seed_safe and maximal_row(seed,native_width,6,seed_lines,seed_circles)
    occupied=set(seed)
    counts={"candidates":0,"safe":0,"safe_maximal":0}
    for rem in range(20):
        base=seed[:rem]+seed[rem+1:]
        for y in range(H):
            for x in range(W):
                add=(x,y)
                if add in occupied: continue
                candidate=base+[add]
                if row_counts(candidate)!=(3,3,3,3,3,3,2): continue
                counts["candidates"]+=1
                safe,lines,circles=geometry(candidate)
                if not safe: continue
                counts["safe"]+=1
                deficient=next(r for r,n in enumerate(row_counts(candidate)) if n==2)
                if maximal_row(candidate,W,deficient,lines,circles):
                    counts["safe_maximal"]+=1
    return {"seed":seed_name,"native_width":native_width,**counts}

def main():
    results=[audit("base53",53,BASE53),audit("foundB_7x59",59,FOUNDB)]
    out={"all_safe_maximal_counts_zero":all(r["safe_maximal"]==0 for r in results),
         "method":"normalized integer line/circle equations; no floating point",
         "required_row_profile":[3,3,3,3,3,3,2],"results":results,"target_width":60}
    print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))
if __name__=="__main__": main()
