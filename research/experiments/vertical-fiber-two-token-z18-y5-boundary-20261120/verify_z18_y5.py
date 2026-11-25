#!/usr/bin/env python3
"""K1089 audit: H(R;(x,5);18), all x>=5, R>=0.
Two raw engines, K1083/K1080 anchors, exact A/B/C signature bands,
induction closure, low-R single-token collapse and sharpness, tail.
"""
import hashlib, json, random, sys
from functools import lru_cache
from pathlib import Path
sys.setrecursionlimit(1_000_000)

@lru_cache(None)
def H_ordered(R,X,z):
    if R==0: return 0
    opts=set()
    for i,a in enumerate(X):
        if a>1: opts.add(H_ordered(R-1,X[:i]+(a-1,)+X[i+1:],z))
        else: opts.add(H_ordered(R-1,X[:i]+X[i+1:],z+1))
    if z: opts.add(1^H_ordered(R-1,X,z-1))
    m=0
    while m in opts: m+=1
    return m

@lru_cache(None)
def H_canon(R,X,z):
    X=tuple(sorted(X,reverse=True))
    if R==0: return 0
    opts=set(); i=0
    while i<len(X):
        a=X[i]
        if a>1: opts.add(H_canon(R-1,tuple(sorted(X[:i]+(a-1,)+X[i+1:],reverse=True)),z))
        else: opts.add(H_canon(R-1,tuple(sorted(X[:i]+X[i+1:],reverse=True)),z+1))
        while i+1<len(X) and X[i+1]==a: i+=1
        i+=1
    if z: opts.add(1^H_canon(R-1,X,z-1))
    m=0
    while m in opts: m+=1
    return m

def qo(n): return n if n%2 else n-1
def qe(n): return n if n%2==0 else n-1
def O(r,a,b): return r%2==1 and a<=r<=b
def E(r,a,b): return r%2==0 and a<=r<=b

# K1083: z=18,y=4
def k1083_T(x,r):
    if x==4: return O(r,1,7)
    if x in (5,6): return O(r,1,9)
    if x in (7,8): return O(r,1,11)
    if x in (9,10): return O(r,1,13)
    if x in (11,12): return O(r,1,15)
    if x==13: return O(r,1,17)
    if x==14: return O(r,1,21)
    if x in (15,17,18,19,21,22): return O(r,1,17)
    if x==16: return O(r,1,17) or r==23
    if x==20: return O(r,1,17) or r==25
    if x==23: return O(r,1,17) or O(r,27,45)
    return O(r,1,17) or r==27

def k1083_P(x,r):
    if x in (4,6,8,10,12,14): return False
    if x in (5,7,9,11,13): return r>=x+5
    if x in (15,17): return r in (19,21,23) or r>=24
    if x==16: return r in (19,21)
    if x in (18,20): return r in (19,21,23)
    if x in (19,21): return r in (19,21,23) or r>=25
    if x==22: return r in (19,21,23,25)
    b=r in (19,21,23,25)
    if x>=23 and x%2: return b or E(r,28,qe(x+22)) or r>=x+23
    if x>=24: return b or E(r,28,qe(x+22))
    return False

def k1083(x,r):
    if r==0: return 0
    if k1083_T(x,r): return 2
    return 1 if k1083_P(x,r) else 0

# K1080: z=17,y=5
def k1080_T(x,r):
    if x==5: return O(r,1,9)
    if x in (6,7): return O(r,1,11)
    if x in (8,9): return O(r,1,13)
    if x in (10,11): return O(r,1,15)
    if x==12: return O(r,1,21)
    if x in (13,15,16,17,19,20,21): return O(r,1,17)
    if x==14: return O(r,1,17) or r==23
    if x==18: return O(r,1,17) or r==25
    if x==22: return O(r,1,17) or r==27
    if x==23: return O(r,1,17) or O(r,27,45)
    return O(r,1,17) or r==27

def k1080_P(x,r):
    if x in (5,7,9,11): return False
    if x==6: return r>=12
    if x==8: return r>=14
    if x==10: return r>=16
    if x==12: return r in (18,20,22) or r>=23
    if x in (13,15): return r in (18,20,22)
    if x in (14,16): return r in (18,20,22) or r>=24
    if x in (17,19): return r in (18,20,22,24)
    if x in (18,20): return r in (18,20,22,24) or r>=26
    if x==21: return r in (18,20,22,24,26)
    if x==22: return r in (18,20,22,24,26) or r>=28
    if x==23: return r in (18,20,22,24,26)
    b=r in (18,20,22,24,26)
    if x>=25 and x%2: return b or O(r,29,x+22)
    if x>=24: return b or O(r,29,x+23) or r>=x+24
    return False

def k1080(x,r):
    if r==0: return 0
    if k1080_T(x,r): return 2
    return 1 if k1080_P(x,r) else 0

# Target T/P predicates.
def T(x,r):
    if 5<=x<=12: return O(r,1,qo(x+5))
    if x==13: return O(r,1,23)
    if 14<=x<=16 or x in (18,19,20,22,23): return O(r,1,17)
    if x==17: return O(r,1,17) or r==25
    if x==21: return O(r,1,17) or r==27
    if x==24: return O(r,1,17) or O(r,29,47)
    return O(r,1,17) or r==29

def P(x,r):
    if x in (5,7,9,11,13): return False
    if x in (6,8,10,12): return r>=x+6
    if x==14: return r in (19,21) or r>=23
    if x==15: return r in (19,21,23)
    if x==16: return r in (19,21,23) or r>=25
    if x==17: return r in (19,21,23)
    if x==18: return r in (19,21,23) or r>=25
    if x==19: return r in (19,21,23,25)
    if x==20: return r in (19,21,23,25) or r>=27
    if x==21: return r in (19,21,23,25)
    if x==22: return r in (19,21,23,25) or r>=27
    if x==23: return r in (19,21,23,25,27)
    if x==24: return r in (19,21,23,25,27) or E(r,30,46) or r>=48
    b=r in (19,21,23,25,27)
    if x%2: return b or E(r,30,qe(x+23))
    return b or E(r,30,qe(x+23)) or r>=x+24

def F(x,r):
    if r==0: return 0
    t,p=T(x,r),P(x,r)
    assert not(t and p),(x,r)
    return 2 if t else 1 if p else 0

# Independently encoded set form.
def Tset(x):
    if 5<=x<=12: return set(range(1,qo(x+5)+1,2))
    if x==13: return set(range(1,24,2))
    if 14<=x<=16 or x in (18,19,20,22,23): return set(range(1,18,2))
    if x==17: return set(range(1,18,2))|{25}
    if x==21: return set(range(1,18,2))|{27}
    if x==24: return set(range(1,18,2))|set(range(29,48,2))
    return set(range(1,18,2))|{29}

def Pset(x,L):
    b={19,21,23,25,27}
    if x in (5,7,9,11,13): return set()
    if x in (6,8,10,12): return set(range(x+6,L+1))
    if x==14: return {19,21}|set(range(23,L+1))
    if x==15: return {19,21,23}
    if x==16: return {19,21,23}|set(range(25,L+1))
    if x==17: return {19,21,23}
    if x==18: return {19,21,23}|set(range(25,L+1))
    if x==19: return {19,21,23,25}
    if x==20: return {19,21,23,25}|set(range(27,L+1))
    if x==21: return {19,21,23,25}
    if x==22: return {19,21,23,25}|set(range(27,L+1))
    if x==23: return b
    if x==24: return b|set(range(30,47,2))|set(range(48,L+1))
    out=b|set(range(30,qe(x+23)+1,2))
    if x%2==0: out|=set(range(x+24,L+1))
    return out

# The finite rows are encoded as compact expected signatures; x>=26 is affine.
ODD_ROWS=(
'1-9:01,11-27:1;1-11:01,13-29:0;1-11:01,13-29:1;1-13:01,15-31:0;'
'1-13:01,15-31:1;1-15:01,17-33:0;1-15:01,17-33:1;1-17:01,19-35:0;'
'1-23:01,25-35:1;1-17:01,19-37:0;1-17:01,19-23:0,25-37:1;'
'1-17:01,19-39:0;1-17:01,19-23:0,25-25:01,27-39:1;'
'1-17:01,19-41:0;1-17:01,19-25:0,27-41:1;1-17:01,19-43:0;'
'1-17:01,19-25:0,27-27:01,29-43:1;1-17:01,19-45:0;'
'1-17:01,19-27:0,29-45:1;1-17:01,19-27:0,29-47:01;'
'1-17:01,19-27:0,29-29:01,31-47:1')
EVEN_ROWS=(
'2-10:23,12-28:1;2-10:23,12-12:03,14-28:0;2-12:23,14-30:1;'
'2-12:23,14-14:03,16-30:0;2-14:23,16-32:1;2-14:23,16-16:03,18-32:0;'
'2-16:23,18-34:1;2-16:23,18-22:03,24-34:0;2-18:23,20-36:1;'
'2-18:23,20-22:12,24-24:023,26-36:0;2-18:23,20-38:1;'
'2-18:23,20-22:1,24-24:12,26-38:0;2-18:23,20-40:1;'
'2-18:23,20-24:1,26-26:023,28-40:0;2-18:23,20-42:1;'
'2-18:23,20-24:1,26-26:12,28-42:0;2-18:23,20-44:1;'
'2-18:23,20-26:1,28-28:023,30-44:0;2-18:23,20-26:1,28-46:123;'
'2-18:23,20-26:1,28-28:123,30-46:0;'
'2-18:23,20-26:1,28-28:123,30-48:02')

def parse_row(s):
    out=[]
    for part in s.split(','):
        span,sig=part.split(':')
        if '-' in span: a,b=map(int,span.split('-'))
        else: a=b=int(span)
        out.append((a,b,sig))
    return out

def expected_bands(x,p):
    if 5<=x<=25:
        rows=(ODD_ROWS if p else EVEN_ROWS).split(';')
        return parse_row(rows[x-5])
    if p: return [(1,17,'01'),(19,27,'0'),(29,29,'01'),(31,qo(x+23),'1')]
    return [(2,18,'23'),(20,26,'1'),(28,28,'123'),(30,30,'02'),(32,qe(x+23),'0')]

def sig(x,R):
    r=R-1
    if x==5: a=b=k1083(5,r)
    else: a=F(x-1,r); b=k1083(x,r)
    c=1^k1080(x,r)
    return ''.join(map(str,sorted({a,b,c})))

MEX={'01':2,'23':0,'03':1,'0':1,'1':0,'12':0,'023':1,'123':0,'02':1}

def single(s,z,r):
    if r==0 or s<=0: return 0
    if z==0: return min(r,s)%2
    if s==z:
        if r%2 and r<=2*s-1: return 2
        if r%2==0 and r<=s-1: return 0
        return s%2
    if 1<=z<=s-1:
        m=qo(z)
        if r<=m: return 2 if r%2 else 0
        if m<r<s+z: return (r+z)%2
        return s%2
    if z>=s+1:
        m=qo(s)
        if r<=m: return 2 if r%2 else 0
        return s%2
    raise ValueError((s,z,r))

def run():
    c={}
    n=0
    for x in range(5,41):
        for r in range(x+36):
            a=H_ordered(r,(x,5),18); b=H_canon(r,(x,5),18); d=F(x,r)
            assert a==b==d,('parent',x,r,a,b,d); n+=1
    c['parent_two_raw_engines_vs_formula']=n
    n=0
    for x in range(4,51):
        for r in range(x+31):
            a=H_ordered(r,(x,4),18); b=H_canon(r,(x,4),18); d=k1083(x,r)
            assert a==b==d,('B',x,r,a,b,d); n+=1
    c['K1083_B_anchor']=n
    n=0
    for x in range(5,51):
        for r in range(x+31):
            a=H_ordered(r,(x,5),17); b=H_canon(r,(x,5),17); d=k1080(x,r)
            assert a==b==d,('C',x,r,a,b,d); n+=1
    c['K1080_C_anchor']=n
    n=0
    for x in range(5,101):
        for p in (1,0):
            row=expected_bands(x,p)
            assert row[0][0]==(1 if p else 2)
            prev=None
            for lo,hi,s in row:
                assert lo%2==p and hi%2==p and lo<=hi and s in MEX
                if prev is not None: assert lo==prev+2,('gap',x,p,row)
                prev=hi
                for r in range(lo,hi+1,2):
                    got=sig(x,r)
                    assert got==s,('band',x,r,s,got)
                    assert MEX[s]==F(x,r),('mex',x,r,s)
                    n+=1
            top=x+23; want=top if top%2==p else top-1
            assert prev==want,('top',x,p,prev,want)
    c['signature_band_coverage_identity_mex']=n
    n=0
    for x in range(6,501):
        for r in range(1,x+24):
            s=sig(x,r); assert MEX[s]==F(x,r),('closure',x,r,s)
            n+=1
    for r in range(1,29):
        s=sig(5,r); assert MEX[s]==F(5,r),('base',r,s); n+=1
    c['induction_closure_sweep']=n
    n=0
    for x in range(5,201):
        ts=Tset(x); ps=Pset(x,x+80)
        assert ts.isdisjoint(ps),('overlap',x)
        for r in range(x+81):
            assert (r in ts)==T(x,r),('Tset',x,r)
            assert (r in ps)==P(x,r),('Pset',x,r)
            n+=1
    c['set_vs_predicate']=n
    rowmax={13:24,14:23,15:24,16:25,17:24,18:25,19:26,20:27,21:26,22:27,23:28,24:28}
    n=0
    for x in range(5,201):
        upto=x+80 if x<=12 else rowmax[x] if x<=24 else 28
        for r in range(upto+1):
            assert F(x,r)==single(x+5,18,r),('low',x,r,F(x,r),single(x+5,18,r)); n+=1
    c['height_only_initial_intervals']=n
    witnesses={13:(25,0,2),14:(24,1,0),15:(25,0,1),16:(26,1,0),17:(25,2,1),18:(26,1,0),19:(27,0,1),20:(28,1,0),21:(27,2,1),22:(28,1,0),23:(29,0,1),24:(29,2,1),25:(29,2,1),26:(29,2,1),50:(29,2,1),200:(29,2,1)}
    for x,(r,a,b) in witnesses.items():
        assert F(x,r)==a and single(x+5,18,r)==b,('witness',x,r)
    c['height_only_sharpness_witnesses']=len(witnesses)
    n=0
    for x in range(5,51):
        for r in range(x+24,x+32):
            a=H_ordered(r,(x,5),18); b=H_canon(r,(x,5),18); d=(x+5)%2
            assert a==b==d,('tail',x,r); n+=1
    c['tail_direct']=n
    n=0
    for x in range(26,30001):
        for p in (1,0):
            for lo,hi,s in expected_bands(x,p):
                m=(lo+hi)//2; m+=(p-m)%2
                for r in {lo,hi,m}:
                    if lo<=r<=hi and r%2==p:
                        assert sig(x,r)==s and MEX[s]==F(x,r),('deep',x,r)
                        n+=1
        for r in (x+24,x+25,x+30,x+41):
            assert F(x,r)==(x+5)%2,('deep_tail',x,r); n+=1
    c['deep_affine_band_and_tail_samples']=n
    rng=random.Random(20261120); n=0
    for _ in range(3000):
        x=rng.randint(5,10000); r=rng.randint(0,x+60); v=F(x,r)
        assert v in (0,1,2) and not(T(x,r) and P(x,r))
        if r>=x+24: assert v==(x+5)%2
        elif r>=1: assert MEX[sig(x,r)]==v
        n+=1
    c['fixed_seed_scatter']=n
    c['total_checks']=sum(c.values())
    c['claim']='H(R;(x,5);18), all x>=5 and R>=0'
    c['proof_status']='proved_by_x_outer_induction_and_complete_symbolic_signature_bands'
    c['finite_audit_scope']={'parent':'5<=x<=40, 0<=R<=x+35, ordered/canonical/formula','B':'4<=x<=50, 0<=R<=x+30','C':'5<=x<=50, 0<=R<=x+30','bands':'5<=x<=100, complete 1<=R<=x+23','closure':'6<=x<=500, complete 1<=R<=x+23 plus x=5 base','sets':'5<=x<=200, 0<=R<=x+80','low_R':'x<=12 finite window plus algebraic tail; x=13..24 exact prefixes; x>=25 R<=28','tail':'5<=x<=50, x+24<=R<=x+31','deep':'26<=x<=30000, band endpoints/midpoints and tail','scatter_seed':20261120}
    c['ordered_states']=H_ordered.cache_info().currsize; c['canonical_states']=H_canon.cache_info().currsize
    c['height_only_row_max']={'5..12':'all R',**{str(k):v for k,v in rowmax.items()},'25+':28}
    c['sharpness_first_mismatch']={str(k):list(v) for k,v in witnesses.items()}
    c['verifier_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    out=Path(__file__).resolve().parent/'output'/'audit.json'; out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(c,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    return c

if __name__=='__main__': print(json.dumps(run(),ensure_ascii=False,sort_keys=True,indent=2))
