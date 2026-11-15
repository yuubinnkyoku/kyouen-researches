#!/usr/bin/env python3
"""Exact Fraction audit of the 7x29 q=6 seed's <=2-removal/<=2-addition repairs."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations as C
from math import gcd
from pathlib import Path
import json

S = [
    (9,0),(14,0),(19,0),(20,0),(21,0),
    (2,1),(8,1),(10,1),(13,1),(22,1),
    (7,2),(10,2),(13,2),(19,2),(22,2),
    (3,3),(8,3),(11,3),(27,3),
    (1,4),(5,4),(7,4),(8,4),(14,4),
    (4,5),(6,5),(19,5),(20,5),(25,5),
    (7,6),(8,6),(11,6),(17,6),(22,6),
]
W,H,Q,T = 30,7,6,(29,3)
CELLS = [(x,y) for y in range(H) for x in range(W)]
CI, SI = {p:i for i,p in enumerate(CELLS)}, {p:i for i,p in enumerate(S)}
SSET = set(S)
EMPTY = [p for p in CELLS if p not in SSET]

def line(p,q):
    x,y=p; X,Y=q
    a,b,c=Y-y,x-X,-(Y-y)*x-(x-X)*y
    g=gcd(gcd(abs(a),abs(b)),abs(c)) or 1
    a,b,c=a//g,b//g,c//g
    if a<0 or (a==0 and b<0): a,b,c=-a,-b,-c
    return ("L",a,b,c)

def circle(p,q,r):
    x,y=p; X,Y=q; U,V=r
    A,B,C0=2*(X-x),2*(Y-y),X*X+Y*Y-x*x-y*y
    D,E,G=2*(U-x),2*(V-y),U*U+V*V-x*x-y*y
    det=A*E-B*D
    if det==0: return None
    ux=F(C0*E-B*G,det); uy=F(A*G-C0*D,det)
    return ("C",ux,uy,(F(x)-ux)**2+(F(y)-uy)**2)

def c3(p,q,r):
    c=circle(p,q,r)
    return c if c is not None else line(p,q)

def on(c,p):
    x,y=p
    if c[0]=="L": return c[1]*x+c[2]*y+c[3]==0
    return (F(x)-c[1])**2+(F(y)-c[2])**2==c[3]

CURVE_SET={c3(S[i],S[j],S[k]) for i,j,k in C(range(len(S)),3)}
CURVES=[]
for c in sorted(CURVE_SET,key=repr):
    sm=sum(1<<i for i,p in enumerate(S) if on(c,p))
    pm=sum(1<<j for j,p in enumerate(CELLS) if on(c,p))
    CURVES.append((sm.bit_count(),sm,pm,c))

LINE_EMPTY=[p for p in EMPTY if p[1]==3]
LINE_EMPTY_NOT_T=[p for p in LINE_EMPTY if p!=T]
OFF_EMPTY=[p for p in EMPTY if p[1]!=3]
LINE_STONES=[p for p in S if p[1]==3]
OFF_STONES=[p for p in S if p[1]!=3]

def prepare(removed,k):
    rm=sum(1<<SI[p] for p in removed)
    sf=0; df=[]
    auto=[False]*len(CELLS); sc=[0]*len(CELLS); dc=[[] for _ in CELLS]
    for n,sm,pm,_ in CURVES:
        residual=n-(sm&rm).bit_count()
        if n>=4:
            if residual>=5: sf |= pm
            elif k==2 and residual==4: df.append(pm)
        if n>=3:
            bits=pm
            while bits:
                low=bits&-bits; j=low.bit_length()-1; bits-=low
                if residual>=5: auto[j]=True
                elif residual==4: sc[j] |= pm
                elif k==2 and residual==3: dc[j].append(pm)
    return rm,sf,df,auto,sc,dc,[j for j,v in enumerate(auto) if not v]

def safe(adds,prep):
    _rm,sf,df=prep[:3]
    am=sum(1<<CI[p] for p in adds)
    if sf&am: return False
    if len(adds)==2:
        a,b=(1<<CI[p] for p in adds)
        if any((m&a) and (m&b) for m in df): return False
    return True

def maximal(adds,prep):
    rm,_,_,auto,sc,dc,vul=prep
    am=sum(1<<CI[p] for p in adds)
    if len(adds)==2: a,b=(1<<CI[p] for p in adds)
    for j in vul:
        p=CELLS[j]
        if am>>j&1: continue
        old=SI.get(p)
        if old is not None and not (rm>>old&1): continue
        if sc[j]&am: continue
        if len(adds)==2 and any((m&a) and (m&b) for m in dc[j]): continue
        return False
    return True

def family(name,removals,additions):
    nc=ns=nm=0
    for rem in removals:
        prep=prepare(rem,len(additions[0]))
        for adds in additions:
            nc+=1
            if not safe(adds,prep): continue
            ns+=1
            if maximal(adds,prep): nm+=1
    return {"name":name,"candidates":nc,"safe":ns,"safe_and_maximal":nm}

def main():
    rows=[sum(y==r for _,y in S) for r in range(H)]
    hist=Counter(n for n,_,_,_ in CURVES)
    covered=set()
    for n,_,pm,_ in CURVES:
        if n>=Q-1:
            bits=pm
            while bits:
                low=bits&-bits; covered.add(CELLS[low.bit_length()-1]); bits-=low
    unc29=[[x,y] for x,y in CELLS if x<29 and (x,y) not in SSET and (x,y) not in covered]
    unc30=[[x,y] for x,y in CELLS if (x,y) not in SSET and (x,y) not in covered]

    tcurves={c3(T,S[i],S[j]) for i,j in C(range(len(S)),2)}
    thist=Counter(sum(on(c,p) for p in S) for c in tcurves)
    tpairs=set()
    for n,_,_,c in CURVES:
        if n==3 and on(c,T):
            ps=[p for p in EMPTY if on(c,p)]
            for a,b in C(ps,2): tpairs.add(tuple(sorted((a,b))))
    tpairs=sorted(tpairs)

    assert rows==[5,5,5,4,5,5,5] and max(hist)==5
    assert unc29==[] and unc30==[[29,3]]
    assert dict(thist)=={2:531,3:8,4:1}
    assert tpairs==[((1,3),(5,5)),((1,3),T),((5,5),T),((15,3),T)]

    case_b=((1,3),(5,5))
    line_touch=[p for p in C(S,2) if p[0][1]==3 or p[1][1]==3]
    families=[
        family("T-occupancy",list(C(S,2)),[(T,p) for p in EMPTY if p!=T]),
        family("one-swap",[(p,) for p in S],[(p,) for p in LINE_EMPTY]),
        family("two-remove-one-add",list(C(S,2)),[(p,) for p in LINE_EMPTY]),
        family("three-stone-T-curve-extra",line_touch,[case_b]),
        family("four-stone-line-gap-A",list(C(OFF_STONES,2)),
               [(a,b) for a in LINE_EMPTY_NOT_T for b in OFF_EMPTY]),
        family("four-stone-line-gap-B",
               [(a,b) for a in LINE_STONES for b in OFF_STONES],
               list(C(LINE_EMPTY_NOT_T,2))),
    ]
    totals={k:sum(f[k] for f in families) for k in ("candidates","safe","safe_and_maximal")}
    expected={
        "T-occupancy":(98175,18342,0),"one-swap":(884,154,0),
        "two-remove-one-add":(14586,4306,0),
        "three-stone-T-curve-extra":(126,5,0),
        "four-stone-line-gap-A":(1631250,101439,0),
        "four-stone-line-gap-B":(36000,2484,0),
    }
    for f in families:
        assert (f["candidates"],f["safe"],f["safe_and_maximal"])==expected[f["name"]]
    assert totals=={"candidates":1781021,"safe":126730,"safe_and_maximal":0}

    result={
        "experiment":"seven-row-q6-m30-surgery-completion-20261115",
        "method":"exact Fraction circumcentres; no SAT, census cache, or repository code",
        "board":{"width":W,"height":H,"q":Q,"seed_stones":len(S),
                 "seed_row_counts":rows,"target":list(T)},
        "seed_audit":{
            "distinct_seed_defined_curves":len(CURVES),
            "seed_curve_size_histogram":{str(k):hist[k] for k in sorted(hist)},
            "maximum_seed_curve_size":max(hist),
            "uncovered_empty_cells_on_7x29":unc29,
            "uncovered_empty_cells_on_7x30":unc30,
            "target_curve_size_histogram":{str(k):thist[k] for k in sorted(thist)},
            "three_seed_point_T_curve_empty_pairs":[[list(a),list(b)] for a,b in tpairs],
            "four_seed_point_T_curve":"y=3",
            "unique_three_seed_point_T_curve_pair_avoiding_T":[[1,3],[5,5]],
        },
        "families":families,
        "totals":totals,
        "classification_scope":"All repairs from this seed with at most two removals and at most two additions, final stone count <=34, and T occupied or blocked. The six disjoint families exhaust the T-blocking possibilities.",
        "completeness_lemmas":{
            "safety":"A forbidden six-point line/circle after at most two additions contains at least four seed stones, so it appears in the exact seed-triple curve census.",
            "maximality":"A curve blocking an empty cell after at most two additions contains at least three seed stones, so it appears in the exact seed-triple curve census; all 210 board cells are checked.",
            "family_disjointness":"The 435 case-b configurations with two off-line removals are already in gap-A; the remaining 126 case-b configurations are separated as three-stone-T-curve-extra."
        }
    }
    out=Path(__file__).resolve().parents[1]/"output"/"audit.json"
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=="__main__": main()
