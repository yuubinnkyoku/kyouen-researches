#!/usr/bin/env python3
"""Independent finite audit for the universally proved z=6, y=22 slice."""
from __future__ import annotations
import hashlib, json, random
from functools import lru_cache
from pathlib import Path

def mex(values):
    s=set(values); n=0
    while n in s: n+=1
    return n

def odd(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==1
def even(r,a,b=None): return r>=a and (b is None or r<=b) and r%2==0

def h5(x,y,r):
    if r==0:return 0
    s,d=x+y,x-y; t={1,3,5}
    if d==1:t.add(2*y+3)
    elif d==5:t.add(2*y+5)
    elif d==6:t.update({2*y+5,2*y+7,2*y+9,2*y+11})
    elif d>=7:t.add(2*y+5)
    if r in t:return 2
    if d==0:o=even(r,6,s+2)
    elif d==1:o=even(r,6,s+3) or r>=s+4
    elif d==2:o=even(r,6,s)
    elif d==3:o=even(r,6,s+1) or r>=s+2
    elif d==4:o=even(r,6,s)
    elif d==5:o=even(r,6,s-1) or r>=s+1
    elif d==6:o=even(r,6,s-2)
    elif d>=7 and d%2:o=even(r,6,2*y+4) or odd(r,2*y+7,s+4) or r>=s+6
    else:o=even(r,6,2*y+4) or odd(r,2*y+7,s+5)
    return int(o)

def h21(x,r):
    if r==0:return 0
    t={1,3,5}
    if x==21:t.add(45)
    elif x==25:t.add(47)
    elif x==28:t.update({49,51,53,55})
    elif x>=29:t.add(49)
    if r in t:return 2
    if x==21:o=odd(r,7,43)
    elif x==22:o=odd(r,7) or even(r,46)
    elif x==23:o=odd(r,7,45)
    elif x==24:o=odd(r,7) or even(r,48)
    elif x==25:o=odd(r,7,45)
    elif x==26:o=odd(r,7) or even(r,48)
    elif x==27:o=odd(r,7,47)
    elif x==28:o=odd(r,7,47) or even(r,50) or odd(r,57)
    elif x==29:o=odd(r,7,47) or even(r,50,56)
    elif x>=30 and x%2:o=odd(r,7,47) or even(r,50,x+27)
    else:o=odd(r,7,47) or even(r,50) or odd(r,x+29)
    return int(o)

def twos22(x):
    t={1,3,5}
    if x==22:t.add(47)
    elif x==26:t.add(49)
    elif x==29:t.update({51,53,55,57})
    elif x>=30:t.add(51)
    return t

def ones22(x,r):
    if x==22:return odd(r,7,45)
    if x==23:return odd(r,7) or even(r,48)
    if x==24:return odd(r,7,47)
    if x==25:return odd(r,7) or even(r,50)
    if x==26:return odd(r,7,47)
    if x==27:return odd(r,7) or even(r,50)
    if x==28:return odd(r,7,49)
    if x%2:return odd(r,7,49) or even(r,52) or odd(r,x+30)
    return odd(r,7,49) or even(r,52,x+28)

def h22(x,r): return 2 if r in twos22(x) else int(ones22(x,r))

def family22(x):
    d=x-22; t={1,3,5}
    if d<=6 and d%2==0 and (6+d)%4==2:t.add(44+(6+d)//2)
    elif d==7:t.update({51,53,55,57})
    elif d>=8:t.add(51)
    return t

ROWS={
22: ([(1,5,'01'),(7,45,'0'),(47,47,'01'),(49,49,'1')],[(2,6,'23'),(8,50,'1')]),
23: ([(1,5,'01'),(7,51,'0')],[(2,6,'23'),(8,46,'1'),(48,48,'023'),(50,50,'0')]),
24: ([(1,5,'01'),(7,47,'0'),(49,51,'1')],[(2,6,'23'),(8,52,'1')]),
25: ([(1,5,'01'),(7,53,'0')],[(2,6,'23'),(8,46,'1'),(48,48,'12'),(50,52,'0')]),
26: ([(1,5,'01'),(7,47,'0'),(49,49,'01'),(51,53,'1')],[(2,6,'23'),(8,54,'1')]),
27: ([(1,5,'01'),(7,55,'0')],[(2,6,'23'),(8,48,'1'),(50,50,'023'),(52,54,'0')]),
28: ([(1,5,'01'),(7,49,'0'),(51,55,'1')],[(2,6,'23'),(8,48,'1'),(50,56,'123')]),
29: ([(1,5,'01'),(7,49,'0'),(51,57,'01')],[(2,6,'23'),(8,48,'1'),(50,50,'123'),(52,56,'0')]),
30: ([(1,5,'01'),(7,49,'0'),(51,51,'01'),(53,57,'1')],[(2,6,'23'),(8,48,'1'),(50,50,'123'),(52,58,'02')]),
}

def expected_sig(x,r):
    if x in ROWS: ints=ROWS[x][0 if r%2 else 1]
    elif r%2:
        u=x+28 if x%2 else x+27
        ints=[(1,5,'01'),(7,49,'0'),(51,51,'01'),(53,u,'1')]
    else:
        u=x+27 if x%2 else x+28
        ints=[(2,6,'23'),(8,48,'1'),(50,50,'123'),(52,52,'02'),(54,u,'0')]
    for a,b,s in ints:
        if a<=r<=b and (r-a)%2==0:return tuple(map(int,s))
    return None

def actual_sig(x,R):
    r=R-1
    a=h21(22,r) if x==22 else h22(x-1,r)
    b=h21(x,r); c=1^h5(x,22,r)
    return tuple(sorted({a,b,c}))

@lru_cache(None)
def ordered(r,toks,z):
    if r==0:return 0
    opts=[]
    for i,t in enumerate(toks):
        a=list(toks); zz=z
        if t>=2:a[i]-=1
        else:a.pop(i);zz+=1
        opts.append(ordered(r-1,tuple(a),zz))
    if z:opts.append(1^ordered(r-1,toks,z-1))
    return mex(opts)

@lru_cache(None)
def canonical(r,toks,z):
    if r==0:return 0
    opts=[]
    for i,t in enumerate(toks):
        a=list(toks); zz=z
        if t>=2:a[i]-=1
        else:a.pop(i);zz+=1
        opts.append(canonical(r-1,tuple(sorted(a,reverse=True)),zz))
    if z:opts.append(1^canonical(r-1,tuple(sorted(toks,reverse=True)),z-1))
    return mex(opts)

def run():
    failures=[]; direct=0; ordered.cache_clear(); canonical.cache_clear()
    for x in range(22,61):
        for r in range(x+51):
            for toks,z,expected in (((x,22),6,h22(x,r)),((x,21),6,h21(x,r)),((x,22),5,h5(x,22,r))):
                a=ordered(r,toks,z); b=canonical(r,tuple(sorted(toks,reverse=True)),z); direct+=1
                if a!=b or a!=expected:failures.append(('direct',x,r,toks,z,a,b,expected))
    sigs=mexes=ob=eb=v2=family=0
    for x in range(22,2001):
        seen=set()
        for r in range(1,x+29):
            a=actual_sig(x,r); e=expected_sig(x,r); sigs+=1
            if a!=e:failures.append(('signature',x,r,a,e));continue
            v=mex(a); mexes+=1
            if v!=h22(x,r):failures.append(('mex',x,r,v,h22(x,r)))
            if r%2:
                ob+=1
                if not set(a)<={0,1}:failures.append(('odd-bound',x,r,a))
            else:
                eb+=1
                if v>1:failures.append(('even-bound',x,r,v))
            if v==2:seen.add(r)
        v2+=1
        if seen!=twos22(x):failures.append(('value2',x,sorted(seen),sorted(twos22(x))))
        family+=1
        if seen!=family22(x):failures.append(('family',x,sorted(seen),sorted(family22(x))))
    tail=0
    for x in range(22,2001):
        for off in range(65):
            r=x+29+off;tail+=1
            if h22(x,r)!=(x+22)%2:failures.append(('tail',x,r,h22(x,r)))
    rng=random.Random(20261117); far=0
    for _ in range(2000):
        x=rng.randint(22,100000);r=x+29+rng.randint(0,100000);far+=1
        if h22(x,r)!=(x+22)%2:failures.append(('far-tail',x,r,h22(x,r)))
    counts={'choice_signatures':sigs,'direct_ordered_canonical_formula_anchors':direct,'even_parent_upper_bound':eb,'fixed_seed_far_tail':far,'mex_identities':mexes,'odd_parent_upper_bound':ob,'tail':tail,'three_family_specialization':family,'value2_locus':v2}
    payload={'all_pass':not failures,'audit_scope':{'direct_r':'0 <= R < x+51','direct_x':[22,60],'far_tail_samples':far,'far_tail_seed':20261117,'signature_r':'1 <= R <= x+28','signature_x':[22,2000],'tail_offsets':[0,64],'tail_x':[22,2000]},'classification':'universal proof by signature table, Theorem T, general tail, and strong induction on R','counts':counts,'failures':failures,'target':'H(R;(x,22);6), x>=22, R>=0','total_checks':sum(counts.values())}
    raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
    payload['sha256_without_hash_field']=hashlib.sha256(raw).hexdigest()
    out=Path(__file__).with_name('output');out.mkdir(parents=True,exist_ok=True)
    (out/'audit.json').write_text(json.dumps(payload,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'all_pass':payload['all_pass'],'total_checks':payload['total_checks'],'counts':counts,'failures':len(failures),'sha256_without_hash_field':payload['sha256_without_hash_field']},ensure_ascii=False,sort_keys=True))
    if failures:raise SystemExit(1)

if __name__=='__main__':run()
