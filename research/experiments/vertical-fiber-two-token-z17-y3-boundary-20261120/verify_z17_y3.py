#!/usr/bin/env python3
"""Independent finite audit for the z=17, y=3 two-token slice.

Checks:
- two independent raw recursion engines (order-preserving and
  descending-canonical) against the closed-form candidate
- child anchors: K1044 (z=17,y=2) and K1050 (z=16,y=3) transcriptions
- full-parity signature band table (static rows x=3..23, generic rows
  odd x>=25 / even x>=24), mex mapping, parity claim
- height-only reduction (K0832 proven bound R<=z+1=18; finite observation
  extends to R<=20), general tail R>=x+21, fixed-seed scatter
- closure base (x=3, multiset confluence {2,3}={3,2}, both decrease moves
  lead to the same child) and the induction-step mex sweep itself
- deep band-edge/pin/steady sampling up to x=200,000
"""
from __future__ import annotations
import hashlib, json, random
from functools import lru_cache
from pathlib import Path

def mex(values):
    m=0; values=set(values)
    while m in values: m+=1
    return m

@lru_cache(None)
def H_ordered(R, X, z):
    if R==0: return 0
    opts=set()
    for i,v in enumerate(X):
        if v>1: opts.add(H_ordered(R-1,X[:i]+(v-1,)+X[i+1:],z))
        else: opts.add(H_ordered(R-1,X[:i]+X[i+1:],z+1))
    if z: opts.add(1^H_ordered(R-1,X,z-1))
    return mex(opts)

@lru_cache(None)
def H_canonical(R, X, z):
    X=tuple(sorted(X,reverse=True))
    if R==0: return 0
    opts=set(); i=0
    while i<len(X):
        v=X[i]
        if v>1:
            Y=tuple(sorted(X[:i]+(v-1,)+X[i+1:],reverse=True))
            opts.add(H_canonical(R-1,Y,z))
        else:
            Y=tuple(sorted(X[:i]+X[i+1:],reverse=True))
            opts.add(H_canonical(R-1,Y,z+1))
        while i+1<len(X) and X[i+1]==v: i+=1
        i+=1
    if z: opts.add(1^H_canonical(R-1,X,z-1))
    return mex(opts)

def O(a,b): return set(range(a+(a%2==0),b+1,2))
def E(a,b): return set(range(a+(a%2==1),b+1,2))
def I(a): return set(range(a,20000))

# ---------- parent closed form: z=17, y=3 ----------
def T(x):
    if x==3: return O(1,5)
    if x in (4,5): return O(1,7)
    if x in (6,7): return O(1,9)
    if x in (8,9): return O(1,11)
    if x in (10,11): return O(1,13)
    if x in (12,13): return O(1,15)
    if x==14: return O(1,19)
    if x==15: return O(1,17)
    if x==16: return O(1,17)|{21}
    if 17<=x<=19: return O(1,17)
    if x==20: return O(1,17)|{23}
    if x==21: return O(1,17)|O(23,41)
    return O(1,17)|{23}

def P(x):
    if x%2 and x<=13: return set()
    if x in (4,6,8,10,12): return I(x+4)
    if x==14: return {18}|I(20)
    if x in (15,17): return {18,20}
    if x in (16,18): return {18,20}|I(22)
    if x in (19,21): return {18,20,22}
    if x==20: return {18,20,22}|I(24)
    if x%2: return {18,20,22}|O(25,x+20)
    return {18,20,22}|O(25,x+19)|I(x+21)

def cand(x,r):
    if r==0: return 0
    if r in T(x): return 2
    return 1 if r in P(x) else 0

# ---------- B anchor: K1044 (z=17, y=2) transcription ----------
def child17y2(x,r):
    if r==0: return 0
    if x==2: t={1,3}
    elif x in (3,4): t=O(1,5)
    elif x in (5,6): t=O(1,7)
    elif x in (7,8): t=O(1,9)
    elif x in (9,10): t=O(1,11)
    elif x in (11,12): t=O(1,13)
    elif x in (13,14): t=O(1,15)
    elif x==15: t=O(1,19)
    elif 16<=x<=18: t=O(1,17)
    elif x==19: t=O(1,17)|{21}
    elif x==20: t=O(1,17)|O(21,39)
    else: t=O(1,17)|{21}
    if r in t: return 2
    p=None
    if not x%2 and x<=14: p=set()
    elif x%2 and x<=13: p=I(x+3)
    elif x==15: p={18,20}|I(21)
    elif x==16: p={18}
    elif x==17: p={18,20}|I(21)
    elif x==18: p={18,20}
    elif x==19: p={18,20}|I(22)
    elif x==20: p={18,20}
    elif x%2: p={18,20}|O(23,x+20)|I(x+21)
    else: p={18,20}|O(23,x+19)
    return 1 if r in p else 0

# ---------- C anchor: K1050 (z=16, y=3) transcription ----------
def child16y3(x,r):
    if r==0: return 0
    if x==3: t=O(1,5)
    elif x in (4,5): t=O(1,7)
    elif x in (6,7): t=O(1,9)
    elif x in (8,9): t=O(1,11)
    elif x in (10,11): t=O(1,13)
    elif x==12: t=O(1,15)
    elif x==13: t=O(1,19)
    elif 14<=x<=16: t=O(1,15)
    elif x==17: t=O(1,15)|{21}
    elif x in (18,19): t=O(1,15)
    elif x==20: t=O(1,15)|O(23,39)
    else: t=O(1,15)|{23}
    if r in t: return 2
    p=None
    if x==3 or (x%2 and x<=13): p=set()
    elif x==4: p=I(8)
    elif x in (6,8,10,12): p=I(x+4)
    elif x==14: p={17,19}|I(20)
    elif x in (15,17): p={17,19}
    elif x in (16,18): p={17,19}|I(21)
    elif x==19: p={17,19,21}
    elif x==20: p={17,19,21}|E(24,40)|I(41)
    elif x==21: p={17,19,21}|E(24,40)
    elif x%2: p={17,19,21}|E(24,x+19)
    else: p={17,19,21}|E(24,x+20)|I(x+21)
    return 1 if r in p else 0

# ---------- signature bands ----------
STATIC={
3:  ([(1,5,'01'),(7,23,'1')],[(2,6,'23'),(8,22,'1')]),
4:  ([(1,7,'01'),(9,23,'0')],[(2,6,'23'),(8,8,'03'),(10,24,'0')]),
5:  ([(1,7,'01'),(9,25,'1')],[(2,8,'23'),(10,24,'1')]),
6:  ([(1,9,'01'),(11,25,'0')],[(2,8,'23'),(10,10,'03'),(12,26,'0')]),
7:  ([(1,9,'01'),(11,27,'1')],[(2,10,'23'),(12,26,'1')]),
8:  ([(1,11,'01'),(13,27,'0')],[(2,10,'23'),(12,12,'03'),(14,28,'0')]),
9:  ([(1,11,'01'),(13,29,'1')],[(2,12,'23'),(14,28,'1')]),
10: ([(1,13,'01'),(15,29,'0')],[(2,12,'23'),(14,14,'03'),(16,30,'0')]),
11: ([(1,13,'01'),(15,31,'1')],[(2,14,'23'),(16,30,'1')]),
12: ([(1,15,'01'),(17,31,'0')],[(2,14,'23'),(16,16,'03'),(18,32,'0')]),
13: ([(1,15,'01'),(17,33,'1')],[(2,16,'23'),(18,20,'13'),(22,32,'1')]),
14: ([(1,19,'01'),(21,33,'0')],[(2,16,'23'),(18,34,'0')]),
15: ([(1,17,'01'),(19,35,'1')],[(2,16,'23'),(18,20,'02'),(22,34,'1')]),
16: ([(1,17,'01'),(19,19,'1'),(21,21,'01'),(23,35,'0')],[(2,16,'23'),(18,18,'02'),(20,36,'0')]),
17: ([(1,17,'01'),(19,37,'1')],[(2,16,'23'),(18,18,'02'),(20,20,'0'),(22,22,'123'),(24,36,'1')]),
18: ([(1,17,'01'),(19,21,'1'),(23,37,'0')],[(2,16,'23'),(18,18,'02'),(20,38,'0')]),
19: ([(1,17,'01'),(19,39,'1')],[(2,16,'23'),(18,18,'02'),(20,20,'0'),(22,22,'02'),(24,38,'1')]),
20: ([(1,17,'01'),(19,21,'1'),(23,23,'01'),(25,39,'0')],[(2,16,'23'),(18,18,'02'),(20,20,'0'),(22,22,'02'),(24,40,'023')]),
21: ([(1,17,'01'),(19,21,'1'),(23,41,'01')],[(2,16,'23'),(18,18,'02'),(20,20,'0'),(22,22,'02'),(24,24,'123'),(26,40,'1')]),
22: ([(1,17,'01'),(19,21,'1'),(23,23,'01'),(25,41,'0')],[(2,16,'23'),(18,18,'02'),(20,20,'0'),(22,22,'02'),(24,24,'123'),(26,42,'12')]),
23: ([(1,17,'01'),(19,21,'1'),(23,23,'01'),(25,43,'0')],[(2,16,'23'),(18,18,'02'),(20,20,'0'),(22,22,'02'),(24,24,'123'),(26,42,'1')]),
}
def expected_sig(x,r):
    odd=[(1,17,'01'),(19,21,'1'),(23,23,'01')]
    even=[(2,16,'23'),(18,18,'02'),(20,20,'0'),(22,22,'02'),(24,24,'123')]
    if x<=23: bands=STATIC[x][0 if r%2 else 1]
    elif r%2: bands=odd+[(25,(x+20 if x%2 else x+19),'0')]
    else: bands=even+[(26,(x+19 if x%2 else x+20),'1')]
    for lo,hi,s in bands:
        if lo<=r<=hi: return s
    raise AssertionError((x,r,bands))

def actual_sig(x,r):
    vals={H_ordered(r-1,(x-1,3),17),H_ordered(r-1,(x,2),17),1^H_ordered(r-1,(x,3),16)}
    return ''.join(map(str,sorted(vals)))

@lru_cache(None)
def single(x,z,r):
    if r==0 or (x==0 and z==0): return 0
    opts=set()
    if x>1: opts.add(single(x-1,z,r-1))
    elif x==1: opts.add(single(0,z+1,r-1))
    if z: opts.add(1^single(x,z-1,r-1))
    return mex(opts)

# Logic predicates mirroring the set-based closed forms exactly, O(1) membership.

def cand_pred(x,r):
    if r==0: return 0
    # --- T(x) ---
    if x==3: t=(r%2==1 and r<=5)
    elif x in (4,5): t=(r%2==1 and r<=7)
    elif x in (6,7): t=(r%2==1 and r<=9)
    elif x in (8,9): t=(r%2==1 and r<=11)
    elif x in (10,11): t=(r%2==1 and r<=13)
    elif x in (12,13): t=(r%2==1 and r<=15)
    elif x==14: t=(r%2==1 and r<=19)
    elif x==15: t=(r%2==1 and r<=17)
    elif x==16: t=(r%2==1 and r<=17) or r==21
    elif 17<=x<=19: t=(r%2==1 and r<=17)
    elif x==20: t=(r%2==1 and r<=17) or r==23
    elif x==21: t=(r%2==1 and r<=17) or (r%2==1 and 23<=r<=41)
    else: t=(r%2==1 and r<=17) or r==23
    if t: return 2
    # --- P(x) ---
    if x%2 and x<=13: return 0
    if x in (4,6,8,10,12): return 1 if r>=x+4 else 0
    if x==14: return 1 if (r==18 or r>=20) else 0
    if x in (15,17): return 1 if r in (18,20) else 0
    if x in (16,18): return 1 if (r in (18,20) or r>=22) else 0
    if x in (19,21): return 1 if r in (18,20,22) else 0
    if x==20: return 1 if (r in (18,20,22) or r>=24) else 0
    if x%2: return 1 if (r in (18,20,22) or (r%2==1 and 25<=r<=x+20)) else 0
    return 1 if (r in (18,20,22) or (r%2==1 and 25<=r<=x+19) or r>=x+21) else 0

def child17y2_pred(x,r):
    if r==0: return 0
    if x==2: t=r in (1,3)
    elif x in (3,4): t=(r%2==1 and r<=5)
    elif x in (5,6): t=(r%2==1 and r<=7)
    elif x in (7,8): t=(r%2==1 and r<=9)
    elif x in (9,10): t=(r%2==1 and r<=11)
    elif x in (11,12): t=(r%2==1 and r<=13)
    elif x in (13,14): t=(r%2==1 and r<=15)
    elif x==15: t=(r%2==1 and r<=19)
    elif 16<=x<=18: t=(r%2==1 and r<=17)
    elif x==19: t=(r%2==1 and r<=17) or r==21
    elif x==20: t=(r%2==1 and r<=17) or (r%2==1 and 21<=r<=39)
    else: t=(r%2==1 and r<=17) or r==21
    if t: return 2
    if not x%2 and x<=14: return 0
    if x%2 and x<=13: return 1 if r>=x+3 else 0
    if x==15: return 1 if (r in (18,20) or r>=21) else 0
    if x==16: return 1 if r==18 else 0
    if x==17: return 1 if (r in (18,20) or r>=21) else 0
    if x==18: return 1 if r in (18,20) else 0
    if x==19: return 1 if (r in (18,20) or r>=22) else 0
    if x==20: return 1 if r in (18,20) else 0
    if x%2: return 1 if (r in (18,20) or (r%2==1 and 23<=r<=x+20) or r>=x+21) else 0
    return 1 if (r in (18,20) or (r%2==1 and 23<=r<=x+19)) else 0

def child16y3_pred(x,r):
    if r==0: return 0
    if x==3: t=(r%2==1 and r<=5)
    elif x in (4,5): t=(r%2==1 and r<=7)
    elif x in (6,7): t=(r%2==1 and r<=9)
    elif x in (8,9): t=(r%2==1 and r<=11)
    elif x in (10,11): t=(r%2==1 and r<=13)
    elif x==12: t=(r%2==1 and r<=15)
    elif x==13: t=(r%2==1 and r<=19)
    elif 14<=x<=16: t=(r%2==1 and r<=15)
    elif x==17: t=(r%2==1 and r<=15) or r==21
    elif x in (18,19): t=(r%2==1 and r<=15)
    elif x==20: t=(r%2==1 and r<=15) or (r%2==1 and 23<=r<=39)
    else: t=(r%2==1 and r<=15) or r==23
    if t: return 2
    if x==3 or (x%2==1 and x<=13): return 0
    if x==4: return 1 if r>=8 else 0
    if x in (6,8,10,12): return 1 if r>=x+4 else 0
    if x==14: return 1 if (r in (17,19) or r>=20) else 0
    if x in (15,17): return 1 if r in (17,19) else 0
    if x in (16,18): return 1 if (r in (17,19) or r>=21) else 0
    if x==19: return 1 if r in (17,19,21) else 0
    if x==20: return 1 if (r in (17,19,21) or (r%2==0 and 24<=r<=40) or r>=41) else 0
    if x==21: return 1 if (r in (17,19,21) or (r%2==0 and 24<=r<=40)) else 0
    if x%2: return 1 if (r in (17,19,21) or (r%2==0 and 24<=r<=x+19)) else 0
    return 1 if (r in (17,19,21) or (r%2==0 and 24<=r<=x+20) or r>=x+21) else 0

def run():
    c={'direct_ordered_vs_formula':0,'direct_canonical_vs_formula':0,'ordered_vs_canonical':0,
       'signature_band_and_mex':0,'tail':0,'height_only_proven':0,'height_only_R20':0,
       'random':0,'K1044_child_anchor':0,'K1050_child_anchor':0,
       'closure_base':0,'closure_sweep':0,'formula_deep_consistency':0,'pred_vs_formula':0}
    for x in range(3,61):
        for r in range(x+46):
            v=cand(x,r);a=H_ordered(r,(x,3),17);b=H_canonical(r,(x,3),17)
            assert a==v and b==v and a==b,(x,r,a,b,v)
            c['direct_ordered_vs_formula']+=1;c['direct_canonical_vs_formula']+=1;c['ordered_vs_canonical']+=1
    for x in range(2,61):
        for r in range(x+46):
            v=child17y2(x,r)
            assert H_ordered(r,(x,2),17)==v and H_canonical(r,(x,2),17)==v,(x,r)
            c['K1044_child_anchor']+=2
    for x in range(3,61):
        for r in range(x+46):
            v=child16y3(x,r)
            assert H_ordered(r,(x,3),16)==v and H_canonical(r,(x,3),16)==v,(x,r)
            c['K1050_child_anchor']+=2
    mm={'01':2,'23':0,'03':1,'0':1,'1':0,'12':0,'13':0,'023':1,'123':0,'02':1}
    for x in range(3,96):
        for r in range(1,x+21):
            s=actual_sig(x,r)
            assert s==expected_sig(x,r),(x,r,s,expected_sig(x,r))
            val=mex(set(map(int,s)))
            assert val==mm[s]==cand(x,r),(x,r,s,val,cand(x,r))
            if r%2: assert val<=2
            else: assert val<=1
            c['signature_band_and_mex']+=1
        for r in range(x+21,x+66):
            assert H_ordered(r,(x,3),17)==(x+3)%2;c['tail']+=1
        for r in range(19):
            assert H_ordered(r,(x,3),17)==single(x+3,17,r);c['height_only_proven']+=1
        for r in range(19,21):
            assert H_ordered(r,(x,3),17)==single(x+3,17,r);c['height_only_R20']+=1
    # equi-transcription: logic predicates vs set-based closed forms (engine domain).
    for x in range(3,61):
        for r in range(0,x+47):
            assert cand_pred(x,r)==cand(x,r),(x,r)
            c['pred_vs_formula']+=1
    for x in range(2,61):
        for r in range(0,x+47):
            assert child17y2_pred(x,r)==child17y2(x,r),(x,r)
            c['pred_vs_formula']+=1
    for x in range(3,61):
        for r in range(0,x+47):
            assert child16y3_pred(x,r)==child16y3(x,r),(x,r)
            c['pred_vs_formula']+=1
    # closure identity sweep: the induction step itself on the parameterized forms.
    # base row x=3: the two token-decrease moves lead to the same multiset {2,3},
    # so A=B=K1044's x=3 row; children K1044 (universal) and 1^K1050 (universal).
    for r in range(1,25):
        assert cand_pred(3,r)==mex({child17y2_pred(3,r-1),1^child16y3_pred(3,r-1)}),(3,r)
        c['closure_base']+=1
    for x in range(4,5001):
        for r in range(1,x+21):
            assert cand_pred(x,r)==mex({cand_pred(x-1,r-1),child17y2_pred(x,r-1),1^child16y3_pred(x,r-1)}),(x,r)
            c['closure_sweep']+=1
    # deep sweep on the parameterized rows: band edges, pin, steady T, tail.
    for x in range(23,200001):
        for r in (x+21,x+23,x+30,x+40):
            assert cand_pred(x,r)==(x+3)%2,(x,r)
            c['formula_deep_consistency']+=1
        assert cand_pred(x,17)==2 and cand_pred(x,19)==0
        assert cand_pred(x,18)==1 and cand_pred(x,20)==1 and cand_pred(x,22)==1
        assert cand_pred(x,23)==2 and cand_pred(x,25)==1
        c['formula_deep_consistency']+=7
        if x%2:
            assert cand_pred(x,x+20)==1 and cand_pred(x,x+21)==0
            c['formula_deep_consistency']+=2
        else:
            assert cand_pred(x,x+19)==1 and cand_pred(x,x+20)==0 and cand_pred(x,x+21)==1
            c['formula_deep_consistency']+=3
    rng=random.Random(20261122)
    for _ in range(8000):
        x=rng.randint(3,90);r=rng.randint(0,x+55)
        a=H_ordered(r,(x,3),17);b=H_canonical(r,(x,3),17)
        assert a==b==cand(x,r),(x,r,a,b,cand(x,r))
        c['random']+=1
    return c

if __name__=='__main__':
    result=run();result['total_comparisons']=sum(result.values())
    result['finite_grid']='x=3..60, R=0..x+45; signature x=3..95, R=1..x+20; tail R=x+21..x+65'
    result['ordered_states']=H_ordered.cache_info().currsize
    result['canonical_states']=H_canonical.cache_info().currsize
    result['single_token_states']=single.cache_info().currsize
    result['verifier_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (Path(__file__).parent/'output').mkdir(exist_ok=True)
    (Path(__file__).parent/'output'/'audit.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True,indent=2))
