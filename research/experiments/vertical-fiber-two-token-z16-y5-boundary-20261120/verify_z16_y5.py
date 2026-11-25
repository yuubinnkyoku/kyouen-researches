#!/usr/bin/env python3
"""Independent finite audit for the z=16, y=5 two-token slice (K1073).

Checks:
- two independent raw recursion engines (order-preserving and
  descending-canonical) against the closed-form candidate
- child anchors: K1064 (z=16,y=4) and K1049 (z=15,y=5) transcriptions
- full-parity signature band table (static rows x=5..23, generic rows
  x>=24), mex mapping, disjoint coverage of 1<=R<=x+21
- height-only reduction (K0832 proven bound R<=z+1=17; finite observation
  extends to R<=21, first counterexample R=22 at row x=12)
- general tail R>=x+22 -> (x+5) mod 2
- closed-form logic predicates vs set forms, the induction step
  mex{A,B,C} itself (closure base + closure sweep x<=5000),
  deep band edge / pin / steady / tail samples (x<=200000), fixed-seed scatter
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

# ---------- parent closed form: z=16, y=5 ----------
BASE5={17,19,21,23,25}
def T(x):
    if x==5: return O(1,9)
    if x in (6,7): return O(1,11)
    if x in (8,9): return O(1,13)
    if x==10: return O(1,15)
    if x==11: return O(1,21)          # x+y=z row, continuous cap 21=2y+(d+z)/2
    if x==15: return O(1,15)|{23}     # advance point, d+z=26==2 mod 4
    if x==19: return O(1,15)|{25}     # advance point, d+z=30==2 mod 4
    if x==22: return O(1,15)|O(27,43) # sweep row z+y+1: O[pin,x+y+z]
    if x>=23: return O(1,15)|{27}     # steady pin 27=2y+z+1
    return O(1,15)

def P(x):
    if x in (5,7,9,11): return set()
    if x==6: return I(12)
    if x==8: return I(14)
    if x==10: return I(16)
    if x==12: return {17,19,21}|I(22)
    if x in (13,15): return {17,19,21}
    if x==19: return {17,19,21,23}
    if x==14: return {17,19,21,23}|I(24)
    if x==16: return {17,19,21,23}|I(24)
    if x==17: return {17,19,21,23}
    if x==18: return BASE5|I(26)
    if x==20: return BASE5|I(26)
    if x==21: return BASE5
    if x%2: return BASE5|E(28,x+21)
    return BASE5|E(28,x+22)|I(x+23)

def cand(x,r):
    if r==0: return 0
    if r in T(x): return 2
    return 1 if r in P(x) else 0

# ---------- B anchor: K1064 (z=16, y=4) transcription ----------
def child16y4_T(x):
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

def child16y4_P(x):
    if x in (4,6,8,10,12): return set()
    if x==5: return I(10)
    if x==7: return I(12)
    if x==9: return I(14)
    if x==11: return I(16)
    if x in (13,15): return {17,19}|I(21)
    if x==14: return {17,19}
    if x in (16,18): return {17,19,21}
    if x in (17,19): return {17,19,21}|I(23)
    if x==20: return {17,19,21,23}
    if x%2: return {17,19,21,23}|E(26,x+19)|I(x+21)
    return {17,19,21,23}|E(26,x+20)

def child16y4(x,r):
    if r==0: return 0
    if r in child16y4_T(x): return 2
    return 1 if r in child16y4_P(x) else 0

# ---------- C anchor: K1049 (z=15, y=5) transcription ----------
def child15y5_T(x):
    if x==5: return O(1,9)
    if x in (6,7): return O(1,11)
    if x in (8,9): return O(1,13)
    if x==10: return O(1,19)
    if x==11: return O(1,15)
    if x==12: return O(1,15)|{21}
    if x in (13,14,15): return O(1,15)
    if x==16: return O(1,15)|{23}
    if x in (17,18,19): return O(1,15)
    if x==20: return O(1,15)|{25}
    if x==21: return O(1,15)|O(25,41)
    return O(1,15)|{25}

def child15y5_P(x):
    if x in (5,7,9): return set()
    if x==6: return I(12)
    if x==8: return I(14)
    if x==10: return {16,18,20}|I(21)
    if x==11: return {16,18,20}
    if x==12: return {16,18,20}|I(22)
    if x==13: return {16,18,20}
    if x==14: return {16,18,20,22}|I(23)
    if x==15: return {16,18,20,22}
    if x==16: return {16,18,20,22}|I(24)
    if x==17: return {16,18,20,22}
    if x==18: return {16,18,20,22,24}|I(25)
    if x==19: return {16,18,20,22,24}
    if x==20: return {16,18,20,22,24,26}|I(27)
    if x==21: return {16,18,20,22,24}
    if x%2==0: return {16,18,20,22,24}|O(27,x+21)|I(x+22)
    return {16,18,20,22,24}|O(27,x+20)

def child15y5(x,r):
    if r==0: return 0
    if r in child15y5_T(x): return 2
    return 1 if r in child15y5_P(x) else 0

# ---------- signature bands ----------
# rows x=5..23 static; for x>=24 generic. Band list per R parity covers
# 1<=R<=x+21 disjointly. Signature = sorted digit string of the option
# value multiset {A, B, 1 xor C-child}.
STATIC={
5:  ([(1,9,'01'),(11,25,'1')],[(2,10,'23'),(12,26,'1')]),
6:  ([(1,11,'01'),(13,27,'0')],[(2,10,'23'),(12,12,'03'),(14,26,'0')]),
7:  ([(1,11,'01'),(13,27,'1')],[(2,12,'23'),(14,28,'1')]),
8:  ([(1,13,'01'),(15,29,'0')],[(2,12,'23'),(14,14,'03'),(16,28,'0')]),
9:  ([(1,13,'01'),(15,29,'1')],[(2,14,'23'),(16,30,'1')]),
10: ([(1,15,'01'),(17,31,'0')],[(2,14,'23'),(16,20,'03'),(22,30,'0')]),
11: ([(1,15,'01'),(17,21,'01'),(23,31,'1')],[(2,16,'23'),(18,32,'1')]),
12: ([(1,15,'01'),(17,33,'0')],[(2,16,'23'),(18,20,'12'),(22,22,'023'),(24,32,'0')]),
13: ([(1,15,'01'),(17,21,'0'),(23,33,'1')],[(2,16,'23'),(18,34,'1')]),
14: ([(1,15,'01'),(17,35,'0')],[(2,16,'23'),(18,20,'1'),(22,22,'12'),(24,34,'0')]),
15: ([(1,15,'01'),(17,21,'0'),(23,23,'01'),(25,35,'1')],[(2,16,'23'),(18,36,'1')]),
16: ([(1,15,'01'),(17,37,'0')],[(2,16,'23'),(18,22,'1'),(24,24,'023'),(26,36,'0')]),
17: ([(1,15,'01'),(17,23,'0'),(25,37,'1')],[(2,16,'23'),(18,38,'1')]),
18: ([(1,15,'01'),(17,39,'0')],[(2,16,'23'),(18,22,'1'),(24,24,'12'),(26,38,'0')]),
19: ([(1,15,'01'),(17,23,'0'),(25,25,'01'),(27,39,'1')],[(2,16,'23'),(18,40,'1')]),
20: ([(1,15,'01'),(17,41,'0')],[(2,16,'23'),(18,24,'1'),(26,26,'023'),(28,40,'0')]),
21: ([(1,15,'01'),(17,25,'0'),(27,41,'1')],[(2,16,'23'),(18,24,'1'),(26,42,'123')]),
22: ([(1,15,'01'),(17,25,'0'),(27,43,'01')],[(2,16,'23'),(18,24,'1'),(26,26,'123'),(28,42,'0')]),
23: ([(1,15,'01'),(17,25,'0'),(27,27,'01'),(29,43,'1')],[(2,16,'23'),(18,24,'1'),(26,26,'123'),(28,44,'02')]),
}
def expected_sig(x,r):
    if x<=23:
        bands=STATIC[x][0 if r%2 else 1]
    elif r%2:
        bands=[(1,15,'01'),(17,25,'0'),(27,27,'01'),(29,x+(21 if x%2==0 else 20),'1')]
    else:
        bands=[(2,16,'23'),(18,24,'1'),(26,26,'123'),(28,28,'02'),(30,x+(20 if x%2==0 else 21),'0')]
    for lo,hi,s in bands:
        if lo<=r<=hi: return s
    raise AssertionError((x,r,bands))

def actual_sig(x,r):
    vals={H_ordered(r-1,(x-1,5),16),H_ordered(r-1,(x,4),16),1^H_ordered(r-1,(x,5),15)}
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
    if x==5: t=(r%2==1 and r<=9)
    elif x in (6,7): t=(r%2==1 and r<=11)
    elif x in (8,9): t=(r%2==1 and r<=13)
    elif x==10: t=(r%2==1 and r<=15)
    elif x==11: t=(r%2==1 and r<=21)
    elif x==15: t=(r%2==1 and r<=15) or r==23
    elif x==19: t=(r%2==1 and r<=15) or r==25
    elif x==22: t=(r%2==1 and r<=15) or (r%2==1 and 27<=r<=43)
    elif x>=23: t=(r%2==1 and r<=15) or r==27
    else: t=(r%2==1 and r<=15)
    if t: return 2
    # --- P(x) ---
    if x in (5,7,9,11): return 0
    if x==6: return 1 if r>=12 else 0
    if x==8: return 1 if r>=14 else 0
    if x==10: return 1 if r>=16 else 0
    if x==12: return 1 if (r in (17,19,21) or r>=22) else 0
    if x in (13,15): return 1 if r in (17,19,21) else 0
    if x==19: return 1 if r in (17,19,21,23) else 0
    if x in (14,16): return 1 if (r in (17,19,21,23) or r>=24) else 0
    if x==17: return 1 if r in (17,19,21,23) else 0
    if x==18: return 1 if (r in BASE5 or r>=26) else 0
    if x==20: return 1 if (r in BASE5 or r>=26) else 0
    if x==21: return 1 if r in BASE5 else 0
    if x%2: return 1 if (r in BASE5 or (r%2==0 and 28<=r<=x+21)) else 0
    return 1 if (r in BASE5 or (r%2==0 and 28<=r<=x+22) or r>=x+23) else 0

def child16y4_pred(x,r):
    if r==0: return 0
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

def child15y5_pred(x,r):
    if r==0: return 0
    if x==5: t=(r%2==1 and r<=9)
    elif x in (6,7): t=(r%2==1 and r<=11)
    elif x in (8,9): t=(r%2==1 and r<=13)
    elif x==10: t=(r%2==1 and r<=19)
    elif x==11: t=(r%2==1 and r<=15)
    elif x==12: t=(r%2==1 and r<=15) or r==21
    elif x in (13,14,15): t=(r%2==1 and r<=15)
    elif x==16: t=(r%2==1 and r<=15) or r==23
    elif x in (17,18,19): t=(r%2==1 and r<=15)
    elif x==20: t=(r%2==1 and r<=15) or r==25
    elif x==21: t=(r%2==1 and r<=15) or (r%2==1 and 25<=r<=41)
    else: t=(r%2==1 and r<=15) or r==25
    if t: return 2
    if x in (5,7,9): return 0
    if x==6: return 1 if r>=12 else 0
    if x==8: return 1 if r>=14 else 0
    if x==10: return 1 if (r in (16,18,20) or r>=21) else 0
    if x in (11,13): return 1 if r in (16,18,20) else 0
    if x==12: return 1 if (r in (16,18,20) or r>=22) else 0
    if x==14: return 1 if (r in (16,18,20,22) or r>=23) else 0
    if x in (15,17): return 1 if r in (16,18,20,22) else 0
    if x==16: return 1 if (r in (16,18,20,22) or r>=24) else 0
    if x==18: return 1 if (r in (16,18,20,22,24) or r>=25) else 0
    if x in (19,21): return 1 if r in (16,18,20,22,24) else 0
    if x==20: return 1 if (r in (16,18,20,22,24,26) or r>=27) else 0
    if x%2==0: return 1 if (r in (16,18,20,22,24) or (r%2==1 and 27<=r<=x+21) or r>=x+22) else 0
    return 1 if (r in (16,18,20,22,24) or (r%2==1 and 27<=r<=x+20)) else 0

def run():
    c={'direct_ordered_vs_formula':0,'direct_canonical_vs_formula':0,'ordered_vs_canonical':0,
       'signature_band_and_mex':0,'tail':0,'height_only_proven':0,'height_only_R18_21':0,
       'random':0,'K1064_child_anchor':0,'K1049_child_anchor':0,
       'closure_base':0,'closure_sweep':0,'pred_vs_formula':0,'formula_deep_consistency':0,
       'band_coverage':0}
    for x in range(5,61):
        for r in range(x+46):
            v=cand(x,r);a=H_ordered(r,(x,5),16);b=H_canonical(r,(x,5),16)
            assert a==v and b==v and a==b,(x,r,a,b,v)
            c['direct_ordered_vs_formula']+=1;c['direct_canonical_vs_formula']+=1;c['ordered_vs_canonical']+=1
    for x in range(4,61):
        for r in range(x+46):
            v=child16y4(x,r)
            assert H_ordered(r,(x,4),16)==v and H_canonical(r,(x,4),16)==v,(x,r)
            c['K1064_child_anchor']+=2
    for x in range(5,61):
        for r in range(x+46):
            v=child15y5(x,r)
            assert H_ordered(r,(x,5),15)==v and H_canonical(r,(x,5),15)==v,(x,r)
            c['K1049_child_anchor']+=2
    mm={'01':2,'23':0,'03':1,'0':1,'1':0,'12':0,'023':1,'123':0,'02':1}
    for x in range(5,96):
        # disjoint band coverage of 1..x+21 per parity
        for par in (0,1):
            bands=STATIC[x][0 if par else 1] if x<=23 else (
                [(1,15,'01'),(17,25,'0'),(27,27,'01'),(29,x+(21 if x%2==0 else 20),'1')] if par else
                [(2,16,'23'),(18,24,'1'),(26,26,'123'),(28,28,'02'),(30,x+(20 if x%2==0 else 21),'0')])
            assert bands[0][0]==(2 if par==0 else 1),(x,par,bands[0])
            prev_hi=None
            for lo,hi,s in bands:
                if prev_hi is not None: assert lo==prev_hi+2,(x,par,lo,prev_hi)
                prev_hi=hi
            assert prev_hi==x+21 or prev_hi==x+20,(x,par,prev_hi)
            assert prev_hi==x+21 or prev_hi==x+20
        c['band_coverage']+=1
        for r in range(1,x+22):
            s=actual_sig(x,r)
            assert s==expected_sig(x,r),(x,r,s,expected_sig(x,r))
            val=mex(set(map(int,s)))
            assert val==mm[s]==cand(x,r),(x,r,s,val,cand(x,r))
            if r%2: assert val<=2
            else: assert val<=1
            c['signature_band_and_mex']+=1
        for r in range(x+22,x+67):
            assert H_ordered(r,(x,5),16)==(x+5)%2;c['tail']+=1
        for r in range(18):
            assert H_ordered(r,(x,5),16)==single(x+5,16,r);c['height_only_proven']+=1
        for r in range(18,22):
            assert H_ordered(r,(x,5),16)==single(x+5,16,r);c['height_only_R18_21']+=1
    # equi-transcription: logic predicates vs set-based closed forms (engine domain).
    for x in range(5,61):
        for r in range(0,x+47):
            assert cand_pred(x,r)==cand(x,r),(x,r)
            c['pred_vs_formula']+=1
    for x in range(4,61):
        for r in range(0,x+47):
            assert child16y4_pred(x,r)==child16y4(x,r),(x,r)
            c['pred_vs_formula']+=1
    for x in range(5,61):
        for r in range(0,x+47):
            assert child15y5_pred(x,r)==child15y5(x,r),(x,r)
            c['pred_vs_formula']+=1
    # closure identity sweep: the induction step itself on the parameterized forms.
    # base row x=5: A-child (4,5);16 and B-child (5,4);16 coincide as the multiset {4,5}.
    for r in range(1,26):
        assert cand_pred(5,r)==mex({child16y4_pred(5,r-1),1^child15y5_pred(5,r-1)}),(5,r)
        c['closure_base']+=1
    for x in range(6,5001):
        for r in range(1,x+22):
            assert cand_pred(x,r)==mex({cand_pred(x-1,r-1),child16y4_pred(x,r-1),1^child15y5_pred(x,r-1)}),(x,r)
            c['closure_sweep']+=1
    # deep sweep on the parameterized rows: band edges, pin, steady T, tail.
    for x in range(24,200001):
        for r in (x+22,x+23,x+30,x+40):
            assert cand_pred(x,r)==(x+5)%2,(x,r)
            c['formula_deep_consistency']+=1
        if x%2:
            assert cand_pred(x,28)==1 and cand_pred(x,x+21)==1 and cand_pred(x,x+22)==0
        else:
            assert cand_pred(x,28)==1 and cand_pred(x,x+21)==0 and cand_pred(x,x+22)==1 and cand_pred(x,x+23)==1
        assert cand_pred(x,25)==1 and cand_pred(x,26)==0 and cand_pred(x,27)==2
        assert cand_pred(x,15)==2 and cand_pred(x,16)==0 and cand_pred(x,17)==1
        c['formula_deep_consistency']+=7
    rng=random.Random(20261122)
    for _ in range(8000):
        x=rng.randint(5,90);r=rng.randint(0,x+55)
        a=H_ordered(r,(x,5),16);b=H_canonical(r,(x,5),16)
        assert a==b==cand(x,r),(x,r,a,b,cand(x,r))
        c['random']+=1
    return c

if __name__=='__main__':
    result=run();result['total_comparisons']=sum(result.values())
    result['finite_grid']='x=5..60, R=0..x+45; signature x=5..95, R=1..x+21; tail R=x+22..x+66'
    result['ordered_states']=H_ordered.cache_info().currsize
    result['canonical_states']=H_canonical.cache_info().currsize
    result['single_token_states']=single.cache_info().currsize
    result['verifier_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    (Path(__file__).parent/'output').mkdir(exist_ok=True)
    (Path(__file__).parent/'output'/'audit.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True,indent=2))
