#!/usr/bin/env python3
"""Independent audit for the z=15, y=4 two-token residual-game slice.

The universal proof is x-outer induction with complete A/B/C signature bands.
This program audits transcription against two independently written direct mex
recurrences, published child slices K1034/K1031, the signature partition, the
height-only reduction, and the general tail. Finite checks are not the proof.
"""
from __future__ import annotations
import hashlib, json, random, sys
from functools import lru_cache
from pathlib import Path
sys.setrecursionlimit(1_000_000)


def mex(values):
    s=set(values); m=0
    while m in s: m+=1
    return m

def odd(r,a,b): return a<=r<=b and r%2==1
def even(r,a,b): return a<=r<=b and r%2==0

@lru_cache(None)
def H_ordered(R,X,z):
    if R==0: return 0
    opts=set()
    for i,v in enumerate(X):
        if v>1: opts.add(H_ordered(R-1,X[:i]+(v-1,)+X[i+1:],z))
        else: opts.add(H_ordered(R-1,X[:i]+X[i+1:],z+1))
    if z>=1: opts.add(1^H_ordered(R-1,X,z-1))
    return mex(opts)

@lru_cache(None)
def H_canonical(R,X,z):
    X=tuple(sorted(X,reverse=True))
    if R==0: return 0
    opts=set(); i=0
    while i<len(X):
        v=X[i]; j=i+1
        while j<len(X) and X[j]==v: j+=1
        if v>1:
            child=tuple(sorted(X[:i]+(v-1,)+X[i+1:],reverse=True))
            opts.add(H_canonical(R-1,child,z))
        else:
            child=tuple(sorted(X[:i]+X[i+1:],reverse=True))
            opts.add(H_canonical(R-1,child,z+1))
        i=j
    if z>=1: opts.add(1^H_canonical(R-1,X,z-1))
    return mex(opts)

# Published universal child K1031: H(R;(x,4);14), x>=4.
def K1031(x,r):
    if r==0: return 0
    if x==4: t=odd(r,1,7)
    elif x in (5,6): t=odd(r,1,9)
    elif x in (7,8): t=odd(r,1,11)
    elif x==9: t=odd(r,1,13)
    elif x==10: t=odd(r,1,17)
    elif x in (11,13,14,15,17,18): t=odd(r,1,13)
    elif x==12: t=odd(r,1,13) or r==19
    elif x==16: t=odd(r,1,13) or r==21
    elif x==19: t=odd(r,1,13) or odd(r,23,37)
    else: t=odd(r,1,13) or r==23
    p=False
    if x in (5,7,9): p=r>=x+5
    elif x in (11,13): p=r in (15,17) or r>=19
    elif x==12: p=r in (15,17)
    elif x==14: p=r in (15,17,19)
    elif x in (15,17): p=r in (15,17,19) or r>=21
    elif x==16: p=r in (15,17,19)
    elif x==18: p=r in (15,17,19,21)
    elif x>=19 and x%2: p=(r in (15,17,19,21) or even(r,24,x+17) or r>=x+19)
    elif x>=20 and x%2==0: p=(r in (15,17,19,21) or even(r,24,x+18))
    return 2 if t else 1 if p else 0

# Published universal child K1034: H(R;(x,3);15), x>=3.
def K1034(x,r):
    if r==0: return 0
    if x==3: t=odd(r,1,5)
    elif x in (4,5): t=odd(r,1,7)
    elif x in (6,7): t=odd(r,1,9)
    elif x in (8,9): t=odd(r,1,11)
    elif x in (10,11): t=odd(r,1,13)
    elif x==12: t=odd(r,1,17)
    elif x==13: t=odd(r,1,15)
    elif x==14: t=odd(r,1,15) or r==19
    elif x in (15,16,17): t=odd(r,1,15)
    elif x==18: t=odd(r,1,15) or r==21
    elif x==19: t=odd(r,1,15) or odd(r,21,37)
    else: t=odd(r,1,15) or r==21
    p=False
    if x%2 and x<=11: p=False
    elif x%2==0 and x<=10: p=r>=x+4
    elif x==12: p=r==16 or r>=18
    elif x==13: p=r in (16,18)
    elif x==14: p=r in (16,18,20) or r>=21
    elif x==15: p=r in (16,18)
    elif x==16: p=r in (16,18,20) or r>=21
    elif x==17: p=r in (16,18,20)
    elif x==18: p=r in (16,18,20,22) or r>=23
    elif x==19: p=r in (16,18,20)
    elif x>=21 and x%2: p=r in (16,18,20) or odd(r,23,x+18)
    elif x>=20 and x%2==0: p=r in (16,18,20) or odd(r,23,x+17) or r>=x+19
    return 2 if t else 1 if p else 0

# Candidate theorem H(R;(x,4);15), x>=4.
def T(x,r):
    if x==4: return odd(r,1,7)
    if x in (5,6): return odd(r,1,9)
    if x in (7,8): return odd(r,1,11)
    if x in (9,10): return odd(r,1,13)
    if x==11: return odd(r,1,19)
    if x in (12,13,14,16,17,18): return odd(r,1,15)
    if x==15: return odd(r,1,15) or r==21
    if x==19: return odd(r,1,15) or r==23
    if x==20: return odd(r,1,15) or odd(r,23,39)
    return odd(r,1,15) or r==23

def P(x,r):
    if x==4: return False
    if x in (5,7,9): return r>=x+5
    if x in (6,8,10): return False
    if x==11: return r in (16,18,20) or r>=21
    if x==12: return r in (16,18)
    if x==13: return r in (16,18,20) or r>=21
    if x==14: return r in (16,18,20)
    if x in (15,17): return r in (16,18,20,22) or r>=23
    if x==16: return r in (16,18,20)
    if x==18: return r in (16,18,20,22)
    if x==19: return r in (16,18,20,22) or r>=24
    if x==20: return r in (16,18,20,22)
    if x>=21 and x%2: return r in (16,18,20,22) or odd(r,25,x+18) or r>=x+20
    if x>=22 and x%2==0: return r in (16,18,20,22) or odd(r,25,x+19)
    raise ValueError(x)

def candidate(x,r):
    if r==0: return 0
    if T(x,r): return 2
    return 1 if P(x,r) else 0

# Signature bands: (lo, hi, signature), split by parity of R.
FIXED={
4:{1:[(1,7,'01'),(9,23,'1')],0:[(2,8,'23'),(10,22,'1')]},
5:{1:[(1,9,'01'),(11,23,'0')],0:[(2,8,'23'),(10,10,'03'),(12,24,'0')]},
6:{1:[(1,9,'01'),(11,25,'1')],0:[(2,10,'23'),(12,24,'1')]},
7:{1:[(1,11,'01'),(13,25,'0')],0:[(2,10,'23'),(12,12,'03'),(14,26,'0')]},
8:{1:[(1,11,'01'),(13,27,'1')],0:[(2,12,'23'),(14,26,'1')]},
9:{1:[(1,13,'01'),(15,27,'0')],0:[(2,12,'23'),(14,14,'03'),(16,28,'0')]},
10:{1:[(1,13,'01'),(15,29,'1')],0:[(2,14,'23'),(16,18,'13'),(20,28,'1')]},
11:{1:[(1,19,'01'),(21,29,'0')],0:[(2,14,'23'),(16,30,'0')]},
12:{1:[(1,15,'01'),(17,31,'1')],0:[(2,14,'23'),(16,18,'02'),(20,20,'123'),(22,30,'1')]},
13:{1:[(1,15,'01'),(17,19,'1'),(21,31,'0')],0:[(2,14,'23'),(16,16,'02'),(18,32,'0')]},
14:{1:[(1,15,'01'),(17,33,'1')],0:[(2,14,'23'),(16,16,'02'),(18,18,'0'),(20,20,'02'),(22,32,'1')]},
15:{1:[(1,15,'01'),(17,19,'1'),(21,21,'01'),(23,33,'0')],0:[(2,14,'23'),(16,16,'02'),(18,34,'0')]},
16:{1:[(1,15,'01'),(17,35,'1')],0:[(2,14,'23'),(16,16,'02'),(18,20,'0'),(22,22,'123'),(24,34,'1')]},
17:{1:[(1,15,'01'),(17,21,'1'),(23,35,'0')],0:[(2,14,'23'),(16,16,'02'),(18,36,'0')]},
18:{1:[(1,15,'01'),(17,37,'1')],0:[(2,14,'23'),(16,16,'02'),(18,20,'0'),(22,22,'02'),(24,36,'1')]},
19:{1:[(1,15,'01'),(17,21,'1'),(23,23,'01'),(25,37,'0')],0:[(2,14,'23'),(16,16,'02'),(18,20,'0'),(22,22,'02'),(24,38,'023')]},
20:{1:[(1,15,'01'),(17,21,'1'),(23,39,'01')],0:[(2,14,'23'),(16,16,'02'),(18,20,'0'),(22,22,'02'),(24,24,'123'),(26,38,'1')]},
21:{1:[(1,15,'01'),(17,21,'1'),(23,23,'01'),(25,39,'0')],0:[(2,14,'23'),(16,16,'02'),(18,20,'0'),(22,22,'02'),(24,24,'123'),(26,40,'12')]},
}

def signature(x,r):
    if x in FIXED: bands=FIXED[x][r%2]
    elif x>=23 and x%2:
        bands=([(1,15,'01'),(17,21,'1'),(23,23,'01'),(25,x+18,'0')] if r%2 else
               [(2,14,'23'),(16,16,'02'),(18,20,'0'),(22,22,'02'),(24,24,'123'),(26,x+19,'1')])
    elif x>=22 and x%2==0:
        bands=([(1,15,'01'),(17,21,'1'),(23,23,'01'),(25,x+19,'0')] if r%2 else
               [(2,14,'23'),(16,16,'02'),(18,20,'0'),(22,22,'02'),(24,24,'123'),(26,x+18,'1')])
    else: raise ValueError(x)
    hits=[s for lo,hi,s in bands if lo<=r<=hi]
    return hits[0] if len(hits)==1 else None

def single_token(n,z,R):
    if R==0 or n<=0: return 0
    if z==0: return min(R,n)%2
    if z==n:
        if R%2 and R<=2*n-1: return 2
        if R%2==0 and R<=n-1: return 0
        return n%2
    if 1<=z<=n-1:
        m=z if z%2 else z-1
        if R<=m: return 2 if R%2 else 0
        if m<R<n+z: return (R+z)%2
        return n%2
    if z>=n+1:
        m=n if n%2 else n-1
        if R<=m: return 2 if R%2 else 0
        return n%2
    raise ValueError((n,z,R))

def audit_once():
    failures=[]; counts={}
    n=0
    for x in range(3,31):
        for R in range(0,x+21):
            for engine in (H_ordered,H_canonical):
                a=engine(R,(x,3),15); b=K1034(x,R); n+=1
                if a!=b: failures.append(('K1034-anchor',x,R,a,b))
    for x in range(4,31):
        for R in range(0,x+21):
            for engine in (H_ordered,H_canonical):
                a=engine(R,(x,4),14); b=K1031(x,R); n+=1
                if a!=b: failures.append(('K1031-anchor',x,R,a,b))
    counts['published_child_anchors_two_engines']=n

    n=0
    for x in range(4,41):
        for R in range(0,x+21):
            a=H_ordered(R,(x,4),15); b=H_canonical(R,(x,4),15); c=candidate(x,R); n+=1
            if a!=b or a!=c: failures.append(('root-direct',x,R,a,b,c))
    counts['root_two_direct_engines_vs_formula']=n

    n=0
    for x in range(4,2001):
        for R in range(1,x+20):
            s=signature(x,R)
            if s is None:
                failures.append(('band-coverage',x,R)); continue
            r=R-1
            A=candidate(x-1,r) if x>4 else K1034(4,r)
            B=K1034(x,r)
            C=1^K1031(x,r)
            actual=''.join(map(str,sorted({A,B,C})))
            if s!=actual: failures.append(('band-signature',x,R,s,actual))
            value=mex({int(ch) for ch in s})
            c=candidate(x,R)
            if value!=c: failures.append(('band-mex',x,R,s,value,c))
            if R%2==0 and value>1: failures.append(('Theorem-T-even',x,R,s,value))
            if R%2==1 and value>2: failures.append(('Theorem-T-odd',x,R,s,value))
            n+=1
    counts['complete_signature_coverage_identity_mex_and_Theorem_T']=n

    n=0
    for x in range(4,2001):
        for R in range(0,17):
            a=candidate(x,R); b=single_token(x+4,15,R); n+=1
            if a!=b: failures.append(('height-only',x,R,a,b))
    counts['height_only_reduction_R_le_16']=n

    n=0
    for x in range(4,10001):
        for off in range(4):
            R=x+20+off; a=candidate(x,R); b=(x+4)%2; n+=1
            if a!=b: failures.append(('tail',x,R,a,b))
    counts['general_tail']=n

    rng=random.Random(20261120); n=0
    for _ in range(10000):
        x=rng.randint(4,10000); R=rng.randint(0,x+100)
        if R==0: actual=0
        else:
            r=R-1
            A=candidate(x-1,r) if x>4 else K1034(4,r)
            actual=mex({A,K1034(x,r),1^K1031(x,r)})
        expected=candidate(x,R); n+=1
        if actual!=expected: failures.append(('scatter',x,R,actual,expected))
    counts['fixed_seed_child_mex_scatter']=n

    return {
      'all_pass':not failures,
      'theorem':'H(R;(x,4);15), x>=4, all R>=0: complete Grundy classification',
      'classification':'universal proof by x-outer induction and complete A/B/C signature bands',
      'finite_audit_role':'two direct recurrences, published child anchors, signature coverage/identity/mex, low-R collapse, tail, and fixed-seed scatter only',
      'scope':{'direct_child_x':[3,30],'direct_root_x':[4,40],
               'signature_x':[4,2000],'signature_R':'1 <= R <= x+19',
               'height_only':'x=4..2000, R=0..16',
               'tail':'x=4..10000, R=x+20..x+23',
               'scatter_points':10000,'scatter_seed':20261120},
      'counts':counts,'total_checks':sum(counts.values()),
      'failure_count':len(failures),'first_failures':failures[:20]
    }

def run():
    first=audit_once(); second=audit_once()
    a=json.dumps(first,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    b=json.dumps(second,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    same=a==b
    verifier_sha=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result={**first,'repeat_runs':2,'repeat_byte_identical':same,
            'verifier_sha256':verifier_sha,
            'sha256_without_hash_field':hashlib.sha256(a).hexdigest()}
    payload=json.dumps(result,ensure_ascii=False,sort_keys=True,indent=2)+chr(10)
    out=Path(__file__).with_name('output'); out.mkdir(parents=True,exist_ok=True)
    (out/'audit.json').write_text(payload,encoding='utf-8')
    print(payload,end='')
    return 0 if result['all_pass'] and same else 1

if __name__=='__main__': sys.exit(run())
