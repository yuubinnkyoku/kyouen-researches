#!/usr/bin/env python3
"""Independent complete finite audit of parity/mobility generating polynomial."""
from itertools import product
from math import comb
from collections import Counter


def predicted(w,m,r):
    a=min(m,r)
    poly=Counter({(0,0):1})
    row=Counter({(0,0):comb(m,a)})
    for k in range(a):
        row[(a-k,m-k)]+=comb(m,k)
    for _ in range(w):
        nxt=Counter()
        for (d,l),v in poly.items():
            for (e,t),c in row.items():
                nxt[(d+e,l+t)]+=v*c
        poly=nxt
    return poly


def direct(w,m,r):
    a=min(m,r)
    masks=[i for i in range(1<<m) if i.bit_count()<=a]
    row=[(i.bit_count(), 0 if i.bit_count()==a else m-i.bit_count()) for i in masks]
    out=Counter()
    for state in product(row,repeat=w):
        deficit=sum(a-k for k,_ in state)
        legal=sum(v for _,v in state)
        out[(deficit,legal)]+=1
    return out


def closed(w,m,r,poly):
    a=min(m,r)
    N=sum(poly.values())
    W=sum(v for (d,l),v in poly.items() if d%2)
    L=N-W
    TW=sum(v*l for (d,l),v in poly.items() if d%2)
    TL=sum(v*l for (d,l),v in poly.items() if not d%2)
    if m<=r:
        assert N==2**(w*m) and W==L==N//2
        if w*m>=2:
            assert TW==TL==N*w*m//4
        return
    S=sum(comb(m,k) for k in range(r+1))
    D=comb(m-1,r)
    A=m*sum(comb(m-1,k) for k in range(r))
    B=m*comb(m-2,r-1)
    assert N==S**w
    assert 2*W==N-D**w and 2*L==N+D**w
    assert 2*TW==w*(A*S**(w-1)+B*D**(w-1))
    assert 2*TL==w*(A*S**(w-1)-B*D**(w-1))
    assert TW*L>TL*W


def main():
    cases=states=0
    for w in range(1,5):
        for m in range(1,6):
            for r in range(1,6):
                if w*m>16: continue
                p=predicted(w,m,r)
                q=direct(w,m,r)
                assert p==q,(w,m,r,p-q,q-p)
                closed(w,m,r,p)
                cases+=1; states+=sum(p.values())
    print(f'PASS cases={cases} safe_states={states} (complete direct enumeration; independent polynomial convolution)')
    for w,m,r in [(3,8,4),(5,10,6),(2,3,1)]:
        p=predicted(w,m,r)
        W=sum(v for (d,l),v in p.items() if d%2)
        L=sum(v for (d,l),v in p.items() if not d%2)
        TW=sum(l*v for (d,l),v in p.items() if d%2)
        TL=sum(l*v for (d,l),v in p.items() if not d%2)
        print(f'w={w} m={m} r={r}: W={W} L={L} W_moves={TW} L_moves={TL}')

if __name__=='__main__': main()
