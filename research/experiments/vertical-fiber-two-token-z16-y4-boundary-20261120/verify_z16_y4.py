#!/usr/bin/env python3
"""Independent finite audit for the z=16, y=4 two-token slice.

Checks:
- two independent raw recursion engines (order-preserving and
  descending-canonical) against the closed-form candidate
- child anchors: K1050 (z=16,y=3) and K1048 (z=15,y=4) transcriptions
- full-parity signature band table (static rows x=4..22, generic rows
  even x>=24 / odd x>=23), mex mapping, Theorem T bounds
- height-only reduction (K0832 proven bound R<=z+1=17; finite observation
  extends to R<=20), general tail R>=x+21, fixed-seed scatter
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

# ---------- parent closed form: z=16, y=4 ----------
def T(x):
    if x==4: return O(1,7)
    if x in (5,6): return O(1,9)
    if x in (7,8): return O(1,11)
    if x in (9,10): return O(1,13)
    if x==11: return O(1,15)
    if x==12: return O(1,19)
    if x==13: return O(1,15)
    if x==14: return O(1,15)|{21}
    if 15<=x<=17: return O(1,15)
    if x==18: return O(1,15)|{23}
    if x in (19,20): return O(1,15)
    if x==21: return O(1,15)|O(25,41)
    return O(1,15)|{25}

def P(x):
    if x==4 or x==6 or x==8 or x==10 or x==12: return set()
    if x==5: return I(10)
    if x==7: return I(12)
    if x==9: return I(14)
    if x==11: return I(16)
    if x==13 or x==15: return {17,19}|I(21)
    if x==14: return {17,19}
    if x in (16,18): return {17,19,21}
    if x==17 or x==19: return {17,19,21}|I(23)
    if x==20: return {17,19,21,23}
    if x%2: return {17,19,21,23}|E(26,x+19)|I(x+21)
    return {17,19,21,23}|E(26,x+20)

def cand(x,r):
    if r==0: return 0
    if r in T(x): return 2
    return 1 if r in P(x) else 0

# ---------- B anchor: K1050 (z=16, y=3) transcription ----------
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

# ---------- C anchor: K1048 (z=15, y=4) transcription ----------
def child15y4(x,r):
    if r==0: return 0
    if x==4: t=O(1,7)
    elif x in (5,6): t=O(1,9)
    elif x in (7,8): t=O(1,11)
    elif x in (9,10): t=O(1,13)
    elif x==11: t=O(1,19)
    elif x in (12,13,14,16,17,18): t=O(1,15)
    elif x==15: t=O(1,15)|{21}
    elif x==19: t=O(1,15)|{23}
    elif x==20: t=O(1,15)|O(23,39)
    else: t=O(1,15)|{23}
    if r in t: return 2
    p=None
    if x==4 or x==6 or x==8 or x==10: p=set()
    elif x in (5,7,9): p=I(x+5)
    elif x in (11,13): p={16,18,20}|I(21)
    elif x==12: p={16,18}
    elif x in (14,16): p={16,18,20}
    elif x in (15,17): p={16,18,20,22}|I(23)
    elif x==18: p={16,18,20,22}
    elif x==19: p={16,18,20,22}|I(24)
    elif x==20: p={16,18,20,22}
    elif x%2: p={16,18,20,22}|O(25,x+18)|I(x+20)
    else: p={16,18,20,22}|O(25,x+19)
    return 1 if r in p else 0

# ---------- signature bands ----------
STATIC={
4:  ([(1,8,'01'),(9,23,'1')],[(2,9,'23'),(10,24,'1')]),
5:  ([(1,10,'01'),(11,25,'0')],[(2,9,'23'),(10,11,'03'),(12,24,'0')]),
6:  ([(1,10,'01'),(11,25,'1')],[(2,11,'23'),(12,26,'1')]),
7:  ([(1,12,'01'),(13,27,'0')],[(2,11,'23'),(12,13,'03'),(14,26,'0')]),
8:  ([(1,12,'01'),(13,27,'1')],[(2,13,'23'),(14,28,'1')]),
9:  ([(1,14,'01'),(15,29,'0')],[(2,13,'23'),(14,15,'03'),(16,28,'0')]),
10: ([(1,14,'01'),(15,29,'1')],[(2,15,'23'),(16,30,'1')]),
11: ([(1,16,'01'),(17,31,'0')],[(2,15,'23'),(16,21,'03'),(22,30,'0')]),
12: ([(1,20,'01'),(21,31,'1')],[(2,17,'23'),(18,32,'1')]),
13: ([(1,16,'01'),(17,33,'0')],[(2,17,'23'),(18,21,'12'),(22,32,'0')]),
14: ([(1,16,'01'),(17,20,'0'),(21,22,'01'),(23,33,'1')],[(2,17,'23'),(18,34,'1')]),
15: ([(1,16,'01'),(17,35,'0')],[(2,17,'23'),(18,21,'1'),(22,23,'023'),(24,34,'0')]),
16: ([(1,16,'01'),(17,22,'0'),(23,35,'1')],[(2,17,'23'),(18,36,'1')]),
17: ([(1,16,'01'),(17,37,'0')],[(2,17,'23'),(18,21,'1'),(22,23,'12'),(24,36,'0')]),
18: ([(1,16,'01'),(17,22,'0'),(23,24,'01'),(25,37,'1')],[(2,17,'23'),(18,38,'1')]),
19: ([(1,16,'01'),(17,39,'0')],[(2,17,'23'),(18,23,'1'),(24,25,'023'),(26,38,'0')]),
20: ([(1,16,'01'),(17,24,'0'),(25,39,'1')],[(2,17,'23'),(18,23,'1'),(24,40,'123')]),
21: ([(1,16,'01'),(17,24,'0'),(25,41,'01')],[(2,17,'23'),(18,23,'1'),(24,25,'123'),(26,40,'0')]),
22: ([(1,16,'01'),(17,24,'0'),(25,26,'01'),(27,41,'1')],[(2,17,'23'),(18,23,'1'),(24,25,'123'),(26,42,'02')]),
}
def expected_sig(x,r):
    odd=[(1,16,'01'),(17,24,'0'),(25,26,'01')]
    even=[(2,17,'23'),(18,23,'1'),(24,25,'123'),(26,27,'02')]
    if x<=22: bands=STATIC[x][0 if r%2 else 1]
    elif r%2: bands=odd+[(27,x+(20 if x%2 else 19),'1')]
    else: bands=even+[(28,x+(19 if x%2 else 20),'0')]
    for lo,hi,s in bands:
        if lo<=r<=hi: return s
    raise AssertionError((x,r,bands))

def actual_sig(x,r):
    vals={H_ordered(r-1,(x-1,4),16),H_ordered(r-1,(x,3),16),1^H_ordered(r-1,(x,4),15)}
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
    if x==4: t=(r%2==1 and r<=7)
    elif x in (5,6): t=(r%2==1 and r<=9)
    elif x in (7,8): t=(r%2==1 and r<=11)
    elif x in (9,10): t=(r%2==1 and r<=13)
    elif x==11: t=(r%2==1 and r<=15)
    elif x==12: t=(r%2==1 and r<=19)
    elif x==13: t=(r%2==1 and r<=15)
    elif x==14: t=(r%2==1 and r<=15) or r==21
    elif 15<=x<=17: t=(r%2==1 and r<=15)
    elif x==18: t=(r%2==1 and r<=15) or r==23
    elif x in (19,20): t=(r%2==1 and r<=15)
    elif x==21: t=(r%2==1 and r<=15) or (r%2==1 and 25<=r<=41)
    else: t=(r%2==1 and r<=15) or r==25
    if t: return 2
    # --- P(x) ---
    if x in (4,6,8,10,12): return 0
    if x==5: return 1 if r>=10 else 0
    if x==7: return 1 if r>=12 else 0
    if x==9: return 1 if r>=14 else 0
    if x==11: return 1 if r>=16 else 0
    if x in (13,15): return 1 if (r in (17,19) or r>=21) else 0
    if x==14: return 1 if r in (17,19) else 0
    if x in (16,18): return 1 if r in (17,19,21) else 0
    if x in (17,19): return 1 if (r in (17,19,21) or r>=23) else 0
    if x==20: return 1 if r in (17,19,21,23) else 0
    if x%2: return 1 if (r in (17,19,21,23) or (r%2==0 and 26<=r<=x+19) or r>=x+21) else 0
    return 1 if (r in (17,19,21,23) or (r%2==0 and 26<=r<=x+20)) else 0

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

def child15y4_pred(x,r):
    if r==0: return 0
    if x==4: t=(r%2==1 and r<=7)
    elif x in (5,6): t=(r%2==1 and r<=9)
    elif x in (7,8): t=(r%2==1 and r<=11)
    elif x in (9,10): t=(r%2==1 and r<=13)
    elif x==11: t=(r%2==1 and r<=19)
    elif x in (12,13,14,16,17,18): t=(r%2==1 and r<=15)
    elif x==15: t=(r%2==1 and r<=15) or r==21
    elif x==19: t=(r%2==1 and r<=15) or r==23
    elif x==20: t=(r%2==1 and r<=15) or (r%2==1 and 23<=r<=39)
    else: t=(r%2==1 and r<=15) or r==23
    if t: return 2
    if x in (4,6,8,10): return 0
    if x in (5,7,9): return 1 if r>=x+5 else 0
    if x in (11,13): return 1 if (r in (16,18,20) or r>=21) else 0
    if x==12: return 1 if r in (16,18) else 0
    if x in (14,16): return 1 if r in (16,18,20) else 0
    if x in (15,17): return 1 if (r in (16,18,20,22) or r>=23) else 0
    if x in (18,20): return 1 if r in (16,18,20,22) else 0
    if x==19: return 1 if (r in (16,18,20,22) or r>=24) else 0
    if x%2: return 1 if (r in (16,18,20,22) or (r%2==1 and 25<=r<=x+18) or r>=x+20) else 0
    return 1 if (r in (16,18,20,22) or (r%2==1 and 25<=r<=x+19)) else 0

def run():
    c={'direct_ordered_vs_formula':0,'direct_canonical_vs_formula':0,'ordered_vs_canonical':0,
       'signature_band_and_mex':0,'tail':0,'height_only_proven':0,'height_only_R20':0,
       'random':0,'K1050_child_anchor':0,'K1048_child_anchor':0,
       'closure_base':0,'closure_sweep':0,'formula_deep_consistency':0,'pred_vs_formula':0}
    for x in range(4,61):
        for r in range(x+46):
            v=cand(x,r);a=H_ordered(r,(x,4),16);b=H_canonical(r,(x,4),16)
            assert a==v and b==v and a==b,(x,r,a,b,v)
            c['direct_ordered_vs_formula']+=1;c['direct_canonical_vs_formula']+=1;c['ordered_vs_canonical']+=1
    for x in range(3,61):
        for r in range(x+46):
            v=child16y3(x,r)
            assert H_ordered(r,(x,3),16)==v and H_canonical(r,(x,3),16)==v,(x,r)
            c['K1050_child_anchor']+=2
    for x in range(4,61):
        for r in range(x+46):
            v=child15y4(x,r)
            assert H_ordered(r,(x,4),15)==v and H_canonical(r,(x,4),15)==v,(x,r)
            c['K1048_child_anchor']+=2
    mm={'01':2,'23':0,'03':1,'0':1,'1':0,'12':0,'023':1,'123':0,'02':1,'13':0}
    for x in range(4,96):
        for r in range(1,x+21):
            s=actual_sig(x,r)
            assert s==expected_sig(x,r),(x,r,s,expected_sig(x,r))
            val=mex(set(map(int,s)))
            assert val==mm[s]==cand(x,r),(x,r,s,val,cand(x,r))
            if r%2: assert val<=2
            else: assert val<=1
            c['signature_band_and_mex']+=1
        for r in range(x+21,x+66):
            assert H_ordered(r,(x,4),16)==(x+4)%2;c['tail']+=1
        for r in range(18):
            assert H_ordered(r,(x,4),16)==single(x+4,16,r);c['height_only_proven']+=1
        for r in range(18,21):
            assert H_ordered(r,(x,4),16)==single(x+4,16,r);c['height_only_R20']+=1
    # equi-transcription: logic predicates vs set-based closed forms (engine domain).
    for x in range(4,61):
        for r in range(0,x+47):
            assert cand_pred(x,r)==cand(x,r),(x,r)
            c['pred_vs_formula']+=1
    for x in range(3,61):
        for r in range(0,x+47):
            assert child16y3_pred(x,r)==child16y3(x,r),(x,r)
            assert child15y4_pred(x,r)==child15y4(x,r),(x,r)
            c['pred_vs_formula']+=2
    # closure identity sweep: the induction step itself on the parameterized forms.
    # base row x=4: A-child (3,4);16 and B-child (4,3);16 coincide as the multiset {3,4}.
    for r in range(1,25):
        assert cand_pred(4,r)==mex({child16y3_pred(4,r-1),1^child15y4_pred(4,r-1)}),(4,r)
        c['closure_base']+=1
    for x in range(5,5001):
        for r in range(1,x+21):
            assert cand_pred(x,r)==mex({cand_pred(x-1,r-1),child16y3_pred(x,r-1),1^child15y4_pred(x,r-1)}),(x,r)
            c['closure_sweep']+=1
    # deep sweep on the parameterized rows: band edges, pin, steady T, tail.
    for x in range(23,200001):
        for r in (x+21,x+23,x+30,x+40):
            assert cand_pred(x,r)==(x+4)%2,(x,r)
            c['formula_deep_consistency']+=1
        ehi=x+(19 if x%2 else 20)
        assert cand_pred(x,25)==2 and cand_pred(x,26)==1
        assert cand_pred(x,ehi)==1 and cand_pred(x,ehi+1)==0
        assert cand_pred(x,15)==2 and cand_pred(x,16)==0 and cand_pred(x,17)==1
        c['formula_deep_consistency']+=6
    rng=random.Random(20261121)
    for _ in range(8000):
        x=rng.randint(4,90);r=rng.randint(0,x+55)
        a=H_ordered(r,(x,4),16);b=H_canonical(r,(x,4),16)
        assert a==b==cand(x,r),(x,r,a,b,cand(x,r))
        c['random']+=1
    return c

if __name__=='__main__':
    result=run();result['total_comparisons']=sum(result.values())
    result['finite_grid']='x=4..60, R=0..x+45; signature x=4..95, R=1..x+20; tail R=x+21..x+65'
    result['ordered_states']=H_ordered.cache_info().currsize
    result['canonical_states']=H_canonical.cache_info().currsize
    result['single_token_states']=single.cache_info().currsize
    result['verifier_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (Path(__file__).parent/'output').mkdir(exist_ok=True)
    (Path(__file__).parent/'output'/'audit.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True,indent=2))
