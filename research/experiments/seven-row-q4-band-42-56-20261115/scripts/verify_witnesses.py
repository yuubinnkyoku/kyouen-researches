#!/usr/bin/env python3
"""Exact integer-arithmetic verifier for the 7xm, q=4 witness band m=42..56."""
from itertools import combinations
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output"
WITNESSES = json.loads((OUT / "witnesses.json").read_text())
WIDTH_TO_BASE = {}
for base, end in ((42,43),(44,44),(45,46),(47,49),(50,52),(53,56)):
    for m in range(base, end + 1):
        WIDTH_TO_BASE[m] = str(base)

def line(p, q):
    x1,y1=p; x2,y2=q
    a,b,c=y2-y1,x1-x2,x2*y1-x1*y2
    g=math.gcd(math.gcd(abs(a),abs(b)),abs(c))
    if g: a,b,c=a//g,b//g,c//g
    if a<0 or (a==0 and b<0): a,b,c=-a,-b,-c
    return a,b,c

def circle(p, q, r):
    x1,y1=p; x2,y2=q; x3,y3=r
    s1=x1*x1+y1*y1; s2=x2*x2+y2*y2; s3=x3*x3+y3*y3
    det=x1*(y2-y3)-y1*(x2-x3)+(x2*y3-x3*y2)
    if det==0: return None
    B=s1*(y2-y3)-y1*(s2-s3)+(s2*y3-s3*y2)
    C=x1*(s2-s3)-s1*(x2-x3)+(x2*s3-x3*s2)
    D=x1*(y2*s3-y3*s2)-y1*(x2*s3-x3*s2)+s1*(x2*y3-x3*y2)
    a,b,c,d=det,-B,-C,-D
    g=math.gcd(math.gcd(math.gcd(abs(a),abs(b)),abs(c)),abs(d))
    if g: a,b,c,d=a//g,b//g,c//g,d//g
    if a<0: a,b,c,d=-a,-b,-c,-d
    return a,b,c,d

def on_line(co,p):
    a,b,c=co; x,y=p
    return a*x+b*y+c==0

def on_circle(co,p):
    a,b,c,d=co; x,y=p
    return a*(x*x+y*y)+b*x+c*y+d==0

def audit(m, stones):
    stones=[tuple(p) for p in stones]
    assert len(stones)==20 and len(set(stones))==20
    assert all(0<=x<m and 0<=y<7 for x,y in stones)
    lines={}
    for p,q in combinations(stones,2):
        co=line(p,q)
        if co not in lines:
            lines[co]=[s for s in stones if on_line(co,s)]
    circles={}
    for p,q,r in combinations(stones,3):
        co=circle(p,q,r)
        if co is not None and co not in circles:
            circles[co]=[s for s in stones if on_circle(co,s)]
    max_line=max(map(len,lines.values()),default=0)
    max_circle=max(map(len,circles.values()),default=0)
    assert max_line<=3 and max_circle<=3, (m,max_line,max_circle)
    occupied=set(stones)
    uncovered=[]
    for y in range(7):
        for x in range(m):
            p=(x,y)
            if p in occupied: continue
            blocked=any(len(ps)>=3 and on_line(co,p) for co,ps in lines.items())
            if not blocked:
                blocked=any(len(ps)>=3 and on_circle(co,p) for co,ps in circles.items())
            if not blocked: uncovered.append(p)
    assert not uncovered, (m,uncovered[:10])
    rows=[sum(y==yy for x,y in stones) for yy in range(7)]
    assert min(rows)<=2 and max(rows)<=3 and sum(rows)==20
    return {"w":7,"m":m,"q":4,"base_witness_width":int(WIDTH_TO_BASE[m]),
      "safe":True,"maximal":True,"stones":20,"rows":rows,
      "max_line_points":max_line,"max_circle_points":max_circle,
      "distinct_stone_lines":len(lines),"distinct_stone_circles":len(circles),
      "empty_cells":7*m-20,"unblocked_cells":0}

results=[]
for m in range(42,57):
    results.append(audit(m,WITNESSES[WIDTH_TO_BASE[m]]))
out={"status":"PASS","widths":results}
(OUT / "verification.json").write_text(json.dumps(out,indent=2)+"\n")
print("PASS: 15/15 widths, exact integer arithmetic, safe + maximal + row-deficient")
