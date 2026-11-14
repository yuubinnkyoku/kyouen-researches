#!/usr/bin/env python3
"""Exact local-neighborhood audit for the 7x57, q=4 deficient-maximal frontier.

Finite local audit only; it is not a nonexistence proof for all 7x57 sets.
All line/circle decisions use normalized integer equations, never floats.
"""
from itertools import combinations
from math import gcd
import json

W, H, Q = 57, 7, 4
WITNESSES = {
    42: [(1,0),(20,0),(24,0),(1,1),(23,1),(33,1),(9,2),(21,2),(36,2),(4,3),(16,3),(32,3),(9,4),(20,4),(30,4),(6,5),(16,5),(4,6),(19,6),(33,6)],
    44: [(15,0),(22,0),(29,0),(8,1),(12,1),(30,1),(3,2),(28,2),(29,2),(16,3),(17,3),(32,3),(12,4),(29,4),(35,4),(9,5),(25,5),(27,5),(9,6),(30,6)],
    45: [(3,0),(32,0),(15,1),(31,1),(33,1),(13,2),(30,2),(31,2),(17,3),(23,3),(24,3),(3,4),(7,4),(35,4),(3,5),(15,5),(42,5),(13,6),(19,6),(20,6)],
    47: [(19,0),(32,0),(46,0),(34,1),(36,1),(12,2),(27,2),(33,2),(17,3),(27,3),(39,3),(15,4),(17,4),(40,4),(16,5),(26,5),(38,5),(18,6),(32,6),(41,6)],
    50: [(7,0),(27,0),(39,0),(12,1),(26,1),(29,1),(16,2),(33,2),(29,3),(30,3),(32,3),(11,4),(14,4),(42,4),(7,5),(28,5),(36,5),(26,6),(28,6),(39,6)],
    53: [(21,0),(23,0),(26,0),(18,1),(27,1),(39,1),(14,2),(28,2),(46,2),(25,3),(30,3),(39,3),(18,4),(36,4),(43,4),(13,5),(27,5),(35,5),(14,6),(42,6)],
}

def norm_line(p, q):
    x1,y1=p; x2,y2=q
    a,b,c=y2-y1,x1-x2,x2*y1-x1*y2
    g=gcd(gcd(abs(a),abs(b)),abs(c))
    if g: a,b,c=a//g,b//g,c//g
    if a<0 or (a==0 and b<0): a,b,c=-a,-b,-c
    return (a,b,c)

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
    return (a,b,c,d)

def on_line(co,p):
    a,b,c=co; x,y=p
    return a*x+b*y+c==0

def on_circle(co,p):
    a,b,c,d=co; x,y=p
    return a*(x*x+y*y)+b*x+c*y+d==0

def analyse(stones, width, deficient_rows):
    stones=list(stones)
    assert len(stones)==20 and len(set(stones))==20
    assert all(0<=x<width and 0<=y<H for x,y in stones)
    line_keys={norm_line(p,q) for p,q in combinations(stones,2)}
    line_members={co:tuple(p for p in stones if on_line(co,p)) for co in line_keys}
    circle_keys={}
    for tri in combinations(stones,3):
        co=norm_circle(*tri)
        if co is not None: circle_keys[co]=None
    circle_members={co:tuple(p for p in stones if on_circle(co,p)) for co in circle_keys}
    max_line=max((len(v) for v in line_members.values()),default=0)
    max_circle=max((len(v) for v in circle_members.values()),default=0)
    safe=max_line<Q and max_circle<Q
    occupied=set(stones)
    uncovered={}
    for y in deficient_rows:
        uncovered[y]=[]
        for x in range(width):
            p=(x,y)
            if p in occupied: continue
            blocked=any(len(ps)>=Q-1 and on_line(co,p) for co,ps in line_members.items())
            if not blocked:
                blocked=any(len(ps)>=Q-1 and on_circle(co,p) for co,ps in circle_members.items())
            if not blocked: uncovered[y].append(x)
    maximal=all(not xs for xs in uncovered.values())
    return {"safe":safe,"maximal_on_deficient_rows":maximal,
            "max_line":max_line,"max_circle":max_circle,"uncovered":uncovered}

def row_counts(stones):
    return [sum(y==r for x,y in stones) for r in range(H)]

def main():
    shift_results={}
    total_shifts=0
    for base, stones in WITNESSES.items():
        counts=row_counts(stones)
        deficient=[i for i,c in enumerate(counts) if c<3]
        assert len(deficient)==1 and counts[deficient[0]]==2 and max(counts)==3
        base_audit=analyse(stones,base,deficient)
        assert base_audit["safe"] and base_audit["maximal_on_deficient_rows"]
        shifts=[]
        for shift in range(-min(x for x,y in stones), W-1-max(x for x,y in stones)+1):
            shifted=[(x+shift,y) for x,y in stones]
            res=analyse(shifted,W,deficient)
            assert res["safe"]
            miss=sum(map(len,res["uncovered"].values()))
            shifts.append({"shift":shift,"uncovered_count":miss,
                           "uncovered":res["uncovered"][deficient[0]]})
        total_shifts+=len(shifts)
        best=min(shifts,key=lambda x:(x["uncovered_count"],abs(x["shift"]),x["shift"]))
        shift_results[str(base)]={"fitting_translations":len(shifts),"best":best,
                                  "any_full_extension":any(x["uncovered_count"]==0 for x in shifts)}

    base=WITNESSES[53]
    deficient=[6]
    candidates=0
    successful=[]
    move_stats={
        "within-row":{"candidates":0,"safe":0,"safe_maximal":0,"best_uncovered":None,"best_uncovered_safe":None},
        "full-to-deficient":{"candidates":0,"safe":0,"safe_maximal":0,"best_uncovered":None,"best_uncovered_safe":None},
    }
    occ=set(base)
    # Same-row moves preserve row counts.
    for i,(x,y) in enumerate(base):
        for xn in range(W):
            if (xn,y) in occ: continue
            cand=base[:i]+base[i+1:]+[(xn,y)]
            candidates+=1
            move_stats["within-row"]["candidates"]+=1
            cc=row_counts(cand)
            if any(c>3 for c in cc): continue
            dr=[r for r,c in enumerate(cc) if c<3]
            res=analyse(cand,W,dr)
            miss=sum(map(len,res["uncovered"].values()))
            old=move_stats["within-row"]["best_uncovered"]
            move_stats["within-row"]["best_uncovered"]=miss if old is None else min(old,miss)
            if res["safe"]:
                move_stats["within-row"]["safe"]+=1
                old_safe=move_stats["within-row"]["best_uncovered_safe"]
                move_stats["within-row"]["best_uncovered_safe"]=miss if old_safe is None else min(old_safe,miss)
                if res["maximal_on_deficient_rows"]:
                    move_stats["within-row"]["safe_maximal"]+=1
                    successful.append({"kind":"within-row","from":[x,y],"to":[xn,y]})
    # Move a stone from a full row to the unique deficient row.
    dy=6
    for i,(x,y) in enumerate(base):
        if y==dy: continue
        for xn in range(W):
            if (xn,dy) in occ: continue
            cand=base[:i]+base[i+1:]+[(xn,dy)]
            candidates+=1
            move_stats["full-to-deficient"]["candidates"]+=1
            cc=row_counts(cand)
            if any(c>3 for c in cc): continue
            dr=[r for r,c in enumerate(cc) if c<3]
            res=analyse(cand,W,dr)
            miss=sum(map(len,res["uncovered"].values()))
            old=move_stats["full-to-deficient"]["best_uncovered"]
            move_stats["full-to-deficient"]["best_uncovered"]=miss if old is None else min(old,miss)
            if res["safe"]:
                move_stats["full-to-deficient"]["safe"]+=1
                old_safe=move_stats["full-to-deficient"]["best_uncovered_safe"]
                move_stats["full-to-deficient"]["best_uncovered_safe"]=miss if old_safe is None else min(old_safe,miss)
                if res["maximal_on_deficient_rows"]:
                    move_stats["full-to-deficient"]["safe_maximal"]+=1
                    successful.append({"kind":"full-to-deficient","from":[x,y],"to":[xn,dy]})

    out={
      "scope":"finite local-neighborhood audit only; not a nonexistence proof for 7x57",
      "board":{"width":W,"height":H,"q":Q},
      "translation_audit":{"base_witnesses":list(WITNESSES),"total_fitting_translations":total_shifts,
                            "results":shift_results},
      "single_relocation_audit":{"base_width":53,"candidate_moves":candidates,
                                  "successful_safe_maximal_row_deficient_moves":successful,
                                  "by_move_type":move_stats,"all_candidates_exhausted":True},
    }
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
