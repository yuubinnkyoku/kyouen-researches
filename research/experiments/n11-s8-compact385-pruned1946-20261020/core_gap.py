#!/usr/bin/env python3
"""Rebuild a sufficient UNSAT submatrix from integer geometry and verify it.

Only an independently checked subset of the dual-tight obligations is used.
Dropping obligations and columns with no incidence in that subset is a
relaxation: UNSAT of this smaller problem implies UNSAT of the full problem.
The matrix is regenerated, not trusted from an optimizer or cached verdicts.
"""
import json,sys
from pathlib import Path
from collections import defaultdict
from fractions import Fraction
from verify_core import children
B=Path(__file__).resolve().parent

def get_matrix():
    D=json.loads((B/'dual_components.json').read_text())
    W={h:Fraction(v) for d in D for h,v in d['weights'].items()}
    roots=(B/'loss_roots35.txt').read_text().split()
    assert len(roots)==len(set(roots))==35
    s9={f'{b:032x}' for h in roots for b in children(int(h,16))}
    assert len(s9)==782
    cov=defaultdict(set)
    for h in s9:
        for b in children(int(h,16)):cov[f'{b:032x}'].add(h)
    assert len(cov)==6446
    weight=lambda ss:sum((W.get(s,0) for s in ss),Fraction(0))
    high={h for h,ss in cov.items() if weight(ss)>1}
    assert len(high)==1346
    witnesses={line.split()[0] for line in (B/'win_witnesses1561.tsv').read_text().splitlines()}
    assert len(witnesses)==1561 and high<=witnesses
    # The component containing D[0] is determined independently from all
    # non-high-weight columns, before any optional WIN exclusions.
    adj={s:set() for s in s9}
    for h,ss in cov.items():
        if h in high:continue
        for s in ss:adj[s].update(ss)
    comp=set(D[0]['weights']);stack=list(comp)
    while stack:
        s=stack.pop()
        for t in adj[s]-comp:
            comp.add(t);stack.append(t)
    assert len(comp)==272
    assert sum((W.get(s,0) for s in comp),Fraction(0))==128
    P=sorted((B/'core_positive78.txt').read_text().split())
    Z=sorted((B/'core_zero24.txt').read_text().split())
    assert len(P)==len(set(P))==78 and len(Z)==len(set(Z))==24
    assert set(P).isdisjoint(Z) and set(P+Z)<=comp
    assert all(W.get(s,0)>0 for s in P)
    assert all(W.get(s,0)==0 for s in Z)
    pi={s:i for i,s in enumerate(P)};zi={s:i for i,s in enumerate(Z)}
    cols=[]
    for h,ss in sorted(cov.items()):
        if h in witnesses or not ss<=comp or weight(ss)!=1:continue
        p=tuple(sorted(pi[s] for s in ss if s in pi))
        z=tuple(sorted(zi[s] for s in ss if s in zi))
        if p or z:cols.append((h,p,z))
    assert len(cols)==396,(len(cols),'unexpected columns')
    assert sum(not p for _,p,z in cols)==8
    return P,Z,cols

def matrix_text(P,Z,cols):
    lines=[f'{len(P)} {len(Z)} {len(cols)}']
    for _,p,z in cols:lines.append(' '.join(map(str,(len(p),len(z),*p,*z))))
    return '\n'.join(lines)+'\n'

def prove(P,Z,cols):
    n=len(cols);byp=[0]*len(P);byz=[0]*len(Z)
    masks=[]
    for i,(_,p,z) in enumerate(cols):
        pm=sum(1<<j for j in p);zm=sum(1<<j for j in z)
        masks.append((pm,zm))
        for j in p:byp[j]|=1<<i
        for j in z:byz[j]|=1<<i
    conflicts=[]
    for pm,zm in masks:
        conflict=0
        while pm:
            bit=pm&-pm;pm-=bit
            conflict|=byp[bit.bit_length()-1]
        conflicts.append(conflict)
    memo=set();calls=0;branches=0
    def dfs(avail,needp,needz):
        nonlocal calls,branches
        calls+=1
        if not needp and not needz:return True
        key=(avail,needp,needz)
        if key in memo:return False
        best=0;bestcount=n+1
        rem=needp
        while rem:
            bit=rem&-rem;rem-=bit
            opts=avail&byp[bit.bit_length()-1]
            count=opts.bit_count()
            if count==0:memo.add(key);return False
            if count<bestcount:best=opts;bestcount=count
            if bestcount==1:break
        if bestcount!=1:
            rem=needz
            while rem:
                bit=rem&-rem;rem-=bit
                opts=avail&byz[bit.bit_length()-1]
                count=opts.bit_count()
                if count==0:memo.add(key);return False
                if count<bestcount:best=opts;bestcount=count
                if bestcount==1:break
        while best:
            bit=best&-best;best-=bit
            i=bit.bit_length()-1
            branches+=1
            pm,zm=masks[i]
            if dfs(avail&~conflicts[i],needp&~pm,needz&~zm):return True
        memo.add(key)
        return False
    sat=dfs((1<<n)-1,(1<<len(P))-1,(1<<len(Z))-1)
    assert not sat,'UNSAT submatrix was actually SAT'
    assert calls==2473277 and branches==2473276,(calls,branches)
    print(f'PASS independently exhaustive Python UNSAT P={len(P)} Z={len(Z)} C={n} calls={calls} branches={branches} memo={len(memo)}')

if __name__=='__main__':
    P,Z,cols=get_matrix()
    if '--matrix' in sys.argv:sys.stdout.write(matrix_text(P,Z,cols))
    elif '--python' in sys.argv:prove(P,Z,cols)
    else:print(f'PASS regenerated exact-geometry UNSAT submatrix P={len(P)} Z={len(Z)} C={len(cols)}')
