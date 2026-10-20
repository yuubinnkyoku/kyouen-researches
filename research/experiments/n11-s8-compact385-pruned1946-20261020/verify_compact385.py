#!/usr/bin/env python3
"""Independent selective-terminal 385-leaf global minimum proof.

Does not read or trust the original 6,446-entry C++ WIN/LOSS table.
Treats every unexcluded legal 10-stone state as a potential LOSS,
so omitting an exclusion cannot make a false lower bound.
"""
import json
import sys
from collections import defaultdict, Counter
from fractions import Fraction
from pathlib import Path
from concurrent.futures import ProcessPoolExecutor
from verify_core import canonical, safe, children, legal, next_player_wins_at_s10
B=Path(__file__).resolve().parent

def check(x,msg):
    if not x: raise ValueError(msg)

def connected_components(s9,coverage):
    adj={s:set() for s in s9}
    for cov in coverage.values():
        for s in cov:adj[s].update(cov)
    remaining=set(s9);components=[]
    while remaining:
        s=min(remaining);stack=[s];cc={s};remaining.remove(s)
        while stack:
            for t in adj[stack.pop()]&remaining:
                remaining.remove(t);cc.add(t);stack.append(t)
        components.append(cc)
    return components

def exact_tight_impossible(component,weights,coverage):
    """If the LP dual is attained by an integer cover, every selected
    column must be dual-tight and positive obligations covered exactly once.
    Exhaustively test these necessary conditions, also covering all zeros.
    """
    positive=sorted(s for s in component if weights.get(s,0)>0)
    zero=sorted(component-set(positive))
    pidx={s:i for i,s in enumerate(positive)}
    zidx={s:i for i,s in enumerate(zero)}
    cols=[]
    for h,cov in sorted(coverage.items()):
        if not cov&component:continue
        check(cov<=component,'cross-component candidate')
        if sum((weights.get(s,0) for s in cov),Fraction(0))!=1:continue
        pm=sum(1<<pidx[s] for s in cov if s in pidx)
        zm=sum(1<<zidx[s] for s in cov if s in zidx)
        cols.append((h,pm,zm))
    n=len(cols)
    byp=[0]*len(positive);byz=[0]*len(zero)
    for i,(_,pm,zm) in enumerate(cols):
        x=pm
        while x:
            bit=x&-x;x-=bit;byp[bit.bit_length()-1]|=1<<i
        x=zm
        while x:
            bit=x&-x;x-=bit;byz[bit.bit_length()-1]|=1<<i
    conflicts=[]
    for _,pm,_ in cols:
        mask=0;x=pm
        while x:
            bit=x&-x;x-=bit;mask|=byp[bit.bit_length()-1]
        conflicts.append(mask)
    memo=set();stat=Counter()
    def search(avail,needp,needz):
        stat['calls']+=1
        if not needp:return not needz
        key=(avail,needp,needz)
        if key in memo:stat['memo']+=1;return False
        best=0;bestcount=n+1
        x=needp
        while x:
            bit=x&-x;x-=bit;opt=avail&byp[bit.bit_length()-1];count=opt.bit_count()
            if count==0:stat['pruned']+=1;memo.add(key);return False
            if count<bestcount:best=opt;bestcount=count
            if count==1:break
        if bestcount!=1:
            x=needz
            while x:
                bit=x&-x;x-=bit;opt=avail&byz[bit.bit_length()-1];count=opt.bit_count()
                if count==0:stat['pruned']+=1;memo.add(key);return False
                if count<bestcount:best=opt;bestcount=count
                if count==1:break
        while best:
            bit=best&-best;best-=bit;i=bit.bit_length()-1
            _,pm,zm=cols[i];stat['branches']+=1
            if search(avail&~conflicts[i],needp&~pm,needz&~zm):return True
        memo.add(key);return False
    sat=search((1<<n)-1,(1<<len(positive))-1,(1<<len(zero))-1)
    check(not sat,'dual-tight exact cover exists; cannot prove +1')
    return {'positive':len(positive),'zero':len(zero),'tight_columns':n,'calls':stat['calls'],'branches':stat['branches']}

def check_win_witness(row):
    h,p=row;b=int(h,16)
    check(canonical(b)==b and safe(b) and b.bit_count()==10,'WIN witness unsafe/noncanonical')
    check(p in legal(b),'WIN witness illegal')
    result,_=next_player_wins_at_s10(b|(1<<p))
    check(not result,'WIN witness child is not LOSS: '+h)
    return True

def check_loss_leaf(h):
    b=int(h,16)
    check(canonical(b)==b and safe(b) and b.bit_count()==10,'invalid selected LOSS')
    result,_=next_player_wins_at_s10(b)
    check(not result,'selected LOSS is actually WIN: '+h)
    return _

def main():
    roots=(B/'loss_roots35.txt').read_text().split()
    check(len(roots)==len(set(roots))==35,'35 roots')
    s9=set()
    for h in roots:
        b=int(h,16)
        check(len(h)==32 and f'{b:032x}'==h and b.bit_count()==8 and canonical(b)==b and safe(b),'invalid S8 root')
        s9.update(f'{c:032x}' for c in children(b))
    check(len(s9)==782,'782 obligations')
    allcov=defaultdict(set)
    for h in s9:
        for c in children(int(h,16)):
            allcov[f'{c:032x}'].add(h)
    check(len(allcov)==6446,'6446 complete S10 candidates')

    dual=json.loads((B/'dual_components.json').read_text())
    check(len(dual)==12,'12 dual components')
    weights={}
    for d in dual:
        for h,v in d['weights'].items():
            check(h in s9 and h not in weights,'dual weight key')
            w=Fraction(v)
            check(w>=0,'negative dual weight')
            weights[h]=w
    def weight(cov):return sum((weights.get(s,0) for s in cov),Fraction(0))
    high={h for h,cov in allcov.items() if weight(cov)>1}
    check(len(high)==1346,'expected high-weight candidates')
    # Non-high columns form 12 components, even before excluding extra WIN witnesses.
    possible={h:cov for h,cov in allcov.items() if h not in high}
    components=connected_components(s9,possible)
    check(len(components)==12,'12 independent components')
    matched={}
    exceptional=[]
    for i,comp in enumerate(components):
        matches=[d for d in dual if d['weights'] and set(d['weights'])<=comp]
        check(len(matches)==1,'dual matching')
        d=matches[0];check(d['id'] not in matched,'duplicate dual component')
        matched[d['id']]=(comp,d)
        lower=sum((weights.get(s,0) for s in comp),Fraction(0))
        ceil=(lower.numerator+lower.denominator-1)//lower.denominator
        check(str(lower)==d['dual'] and ceil==d['ceil'],'dual mismatch')
        if d['selected']>ceil:
            check(d['selected']==ceil+1 and lower==ceil,'unexpected gap')
            exceptional.append(comp)
    check(len(exceptional)==2 and sorted(map(len,exceptional))==[87,272],'exceptional components')

    witness={}
    for row in (B/'win_witnesses1561.tsv').read_text().splitlines():
        fields=row.split('\t')
        check(len(fields)==2,'witness format')
        h,p=fields;p=int(p)
        check(h in allcov and h not in witness and 0<=p<121,'duplicate/invalid WIN witness')
        witness[h]=p
    check(len(witness)==1561,'1561 WIN witnesses')
    check(high<=set(witness),'missing high-weight WIN exclusion')
    for h in witness:
        check(h in high or (weight(allcov[h])==1 and any(allcov[h]<=c for c in exceptional)),
              'irrelevant witness')

    possible={h:cov for h,cov in possible.items() if h not in witness}
    check(all(sum((weights.get(s,0) for s in cov),Fraction(0))<=1 for cov in possible.values()),
          'remaining dual violation')
    check(all(any(cov<=comp for comp in components) for cov in possible.values()),
          'cross-component candidate')
    chosen=(B/'selected385.txt').read_text().split()
    check(len(chosen)==len(set(chosen))==385 and set(chosen)<=set(possible),'selected leaves')
    covered=set().union(*(allcov[h] for h in chosen))
    check(covered==s9,'uncovered S9 obligation')
    with ProcessPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(check_win_witness, sorted(witness.items()), chunksize=8))
    check(all(results),'WIN witness independent verification')
    print('PASS 1561 independently checked S11 losing-child witnesses; 1346 high-weight exclusions')
    with ProcessPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(check_loss_leaf, chosen, chunksize=4))
    check(len(results)==385 and all(n>0 for n in results),'LOSS leaf independent verification')
    check(sum(results)==34709,'unexpected selected LOSS search-state total')
    print('PASS 385 independently checked terminal S10 LOSS leaves; 782 obligations covered; 34709 states')

    lower=0;extra=0
    for comp in components:
        d=[d for d in dual if set(d['weights'])<=comp and d['weights']][0]
        w={s:weights[s] for s in comp if s in weights}
        actual=sum(bool(allcov[h]&comp) for h in chosen)
        check(actual==d['selected'] and actual>=d['ceil'],'component count')
        lower+=d['ceil']
        if actual>d['ceil']:
            if '--skip-python-gap' in sys.argv:
                print('NOTE: Python exact gap search skipped; independent C++ exhaustive gap proof required')
            else:
                if len(comp)==272:
                    from core_gap import get_matrix,prove
                    cp,cz,cc=get_matrix()
                    prove(cp,cz,cc)
                    details={'positive':len(cp),'zero':len(cz),'columns':len(cc),'type':'independent sufficient UNSAT submatrix'}
                else:
                    details=exact_tight_impossible(comp,w,possible)
                print('PASS integrality gap',d['id'],details)
            extra+=1
    check(lower==383 and extra==2 and lower+extra==len(chosen)==385,'global optimality')
    print('PASS exact global minimum 385 over ALL legal S10 responses, no full verdict table' if '--skip-python-gap' not in sys.argv else 'PASS 385-leaf upper bound and dual lower bound 383; independently run C++ exact-gap verifier to establish minimum 385')
    print('Terminal proof obligations: 1561 WIN witnesses + 385 LOSS leaves = 1946 / 6446')

if __name__=='__main__': main()
