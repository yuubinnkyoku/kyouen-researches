#!/usr/bin/env python3
"""Independent finite audit for the z=16, y=3 two-token slice."""
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

def T(x):
    if x==3: return O(1,5)
    if x in (4,5): return O(1,7)
    if x in (6,7): return O(1,9)
    if x in (8,9): return O(1,11)
    if x in (10,11): return O(1,13)
    if x==12: return O(1,15)
    if x==13: return O(1,19)
    if 14<=x<=16: return O(1,15)
    if x==17: return O(1,15)|{21}
    if x in (18,19): return O(1,15)
    if x==20: return O(1,15)|O(23,39)
    return O(1,15)|{23}

def P(x):
    if x==3 or (x%2 and x<=13): return set()
    if x==4: return set(range(8,10000))
    if x in (6,8,10,12): return set(range(x+4,10000))
    if x==14: return {17,19}|set(range(20,10000))
    if x in (15,17): return {17,19}
    if x in (16,18): return {17,19}|set(range(21,10000))
    if x==19: return {17,19,21}
    if x==20: return {17,19,21}|E(24,40)|set(range(41,10000))
    if x%2: return {17,19,21}|E(24,x+19)
    return {17,19,21}|E(24,x+20)|set(range(x+21,10000))

def child16y2(x,r):
    if r==0:return 0
    if x==2:t={1,3}
    elif x in (3,4):t=O(1,5)
    elif x in (5,6):t=O(1,7)
    elif x in (7,8):t=O(1,9)
    elif x in (9,10):t=O(1,11)
    elif x in (11,12):t=O(1,13)
    elif x==13:t=O(1,15)
    elif x==14:t=O(1,17)
    elif x==15:t=O(1,15)
    elif x==16:t=O(1,15)|{19}
    elif x in (17,18):t=O(1,15)
    elif x==19:t=O(1,15)|O(21,37)
    else:t=O(1,15)|{21}
    if r in t:return 2
    if x%2==0 and x<=14:p=set()
    elif x in (3,5,7,9,11,13):p=set(range(x+3,10000))
    elif x in (15,17):p={17,19}|set(range(20,10000))
    elif x==16:p={17}
    elif x==18:p={17,19}
    elif x%2:p={17,19}|E(22,x+19)|set(range(x+20,10000))
    else:p={17,19}|E(22,x+18)
    return 1 if r in p else 0

def child15y3(x,r):
    if r==0:return 0
    if x==3:t=O(1,5)
    elif x in (4,5):t=O(1,7)
    elif x in (6,7):t=O(1,9)
    elif x in (8,9):t=O(1,11)
    elif x in (10,11):t=O(1,13)
    elif x==12:t=O(1,17)
    elif x==13 or x in (15,16,17):t=O(1,15)
    elif x==14:t=O(1,15)|{19}
    elif x==18:t=O(1,15)|{21}
    elif x==19:t=O(1,15)|O(21,37)
    else:t=O(1,15)|{21}
    if r in t:return 2
    if x%2 and x<=11:p=set()
    elif x%2==0 and x<=10:p=set(range(x+4,10000))
    elif x==12:p={16}|set(range(18,10000))
    elif x==13:p={16,18}
    elif x==14:p={16,18,20}|set(range(21,10000))
    elif x==15:p={16,18}
    elif x==16:p={16,18,20}|set(range(21,10000))
    elif x==17:p={16,18,20}
    elif x==18:p={16,18,20,22}|set(range(23,10000))
    elif x==19:p={16,18,20}
    elif x%2:p={16,18,20}|O(23,x+18)
    else:p={16,18,20}|O(23,x+17)|set(range(x+19,10000))
    return 1 if r in p else 0

def cand(x,r):
    if r==0:return 0
    if r in T(x):return 2
    return 1 if r in P(x) else 0

STATIC={
3: ([(1,5,'01'),(7,21,'1')],[(2,6,'23'),(8,22,'1')]),
4: ([(1,7,'01'),(9,23,'0')],[(2,6,'23'),(8,8,'03'),(10,22,'0')]),
5: ([(1,7,'01'),(9,23,'1')],[(2,8,'23'),(10,24,'1')]),
6: ([(1,9,'01'),(11,25,'0')],[(2,8,'23'),(10,10,'03'),(12,24,'0')]),
7: ([(1,9,'01'),(11,25,'1')],[(2,10,'23'),(12,26,'1')]),
8: ([(1,11,'01'),(13,27,'0')],[(2,10,'23'),(12,12,'03'),(14,26,'0')]),
9: ([(1,11,'01'),(13,27,'1')],[(2,12,'23'),(14,28,'1')]),
10: ([(1,13,'01'),(15,29,'0')],[(2,12,'23'),(14,14,'03'),(16,28,'0')]),
11: ([(1,13,'01'),(15,29,'1')],[(2,14,'23'),(16,30,'1')]),
12: ([(1,15,'01'),(17,31,'0')],[(2,14,'23'),(16,18,'03'),(20,30,'0')]),
13: ([(1,19,'01'),(21,31,'1')],[(2,16,'23'),(18,32,'1')]),
14: ([(1,15,'01'),(17,33,'0')],[(2,16,'23'),(18,18,'12'),(20,20,'023'),(22,32,'0')]),
15: ([(1,15,'01'),(17,19,'0'),(21,33,'1')],[(2,16,'23'),(18,34,'1')]),
16: ([(1,15,'01'),(17,35,'0')],[(2,16,'23'),(18,18,'1'),(20,20,'12'),(22,34,'0')]),
17: ([(1,15,'01'),(17,19,'0'),(21,21,'01'),(23,35,'1')],[(2,16,'23'),(18,36,'1')]),
18: ([(1,15,'01'),(17,37,'0')],[(2,16,'23'),(18,20,'1'),(22,22,'023'),(24,36,'0')]),
19: ([(1,15,'01'),(17,21,'0'),(23,37,'1')],[(2,16,'23'),(18,20,'1'),(22,38,'123')]),
20: ([(1,15,'01'),(17,21,'0'),(23,39,'01')],[(2,16,'23'),(18,20,'1'),(22,22,'123'),(24,38,'0')]),
21: ([(1,15,'01'),(17,21,'0'),(23,23,'01'),(25,39,'1')],[(2,16,'23'),(18,20,'1'),(22,22,'123'),(24,40,'02')]),
}
def expected_sig(x,r):
    if x<=21:bands=STATIC[x][0 if r%2 else 1]
    elif r%2:bands=[(1,15,'01'),(17,21,'0'),(23,23,'01'),(25,x+(19 if x%2==0 else 18),'1')]
    else:bands=[(2,16,'23'),(18,20,'1'),(22,22,'123'),(24,24,'02'),(26,x+(18 if x%2==0 else 19),'0')]
    for lo,hi,s in bands:
        if lo<=r<=hi:return s
    raise AssertionError((x,r,bands))

def actual_sig(x,r):
    vals={H_ordered(r-1,(x-1,3),16),H_ordered(r-1,(x,2),16),1^H_ordered(r-1,(x,3),15)}
    return ''.join(map(str,sorted(vals)))

@lru_cache(None)
def single(x,z,r):
    if r==0 or (x==0 and z==0):return 0
    opts=set()
    if x>1:opts.add(single(x-1,z,r-1))
    elif x==1:opts.add(single(0,z+1,r-1))
    if z:opts.add(1^single(x,z-1,r-1))
    return mex(opts)

def run():
    c={'direct_ordered_vs_formula':0,'direct_canonical_vs_formula':0,'ordered_vs_canonical':0,'signature_band_and_mex':0,'tail':0,'height_only':0,'random':0,'K1042_child_anchor':0,'K1034_child_anchor':0}
    for x in range(3,61):
        for r in range(x+46):
            v=cand(x,r);a=H_ordered(r,(x,3),16);b=H_canonical(r,(x,3),16)
            assert a==v and b==v and a==b,(x,r,a,b,v)
            c['direct_ordered_vs_formula']+=1;c['direct_canonical_vs_formula']+=1;c['ordered_vs_canonical']+=1
    for x in range(2,61):
        for r in range(x+46):
            v=child16y2(x,r)
            assert H_ordered(r,(x,2),16)==v and H_canonical(r,(x,2),16)==v
            c['K1042_child_anchor']+=2
    for x in range(3,61):
        for r in range(x+46):
            v=child15y3(x,r)
            assert H_ordered(r,(x,3),15)==v and H_canonical(r,(x,3),15)==v
            c['K1034_child_anchor']+=2
    mm={'01':2,'23':0,'03':1,'0':1,'1':0,'12':0,'023':1,'123':0,'02':1}
    for x in range(3,81):
        for r in range(1,x+20):
            s=actual_sig(x,r)
            assert s==expected_sig(x,r) and mex(set(map(int,s)))==mm[s]==cand(x,r),(x,r,s,expected_sig(x,r))
            c['signature_band_and_mex']+=1
        for r in range(x+20,x+60):
            assert H_ordered(r,(x,3),16)==(x+3)%2;c['tail']+=1
        for r in range(18):
            assert H_ordered(r,(x,3),16)==single(x+3,16,r);c['height_only']+=1
    rng=random.Random(20261120)
    for _ in range(5000):
        x=rng.randint(3,80);r=rng.randint(0,x+50)
        a=H_ordered(r,(x,3),16);b=H_canonical(r,(x,3),16)
        assert a==b==cand(x,r);c['random']+=1
    return c

if __name__=='__main__':
    result=run();result['total_comparisons']=sum(result.values())
    result['finite_grid']='x=3..60, R=0..x+45; signature x=3..80, R=1..x+19'
    result['ordered_states']=H_ordered.cache_info().currsize
    result['canonical_states']=H_canonical.cache_info().currsize
    result['single_token_states']=single.cache_info().currsize
    result['verifier_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    Path(__file__).with_name('audit.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(result,sort_keys=True,indent=2))
