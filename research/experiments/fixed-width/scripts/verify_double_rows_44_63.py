#!/usr/bin/env python3
"""Exact finite congruence certificate for T(w), 44 <= w <= 63.

Uses two independently built residue masks and dominance-preserving
intersections. The g=3 rational-denominator case is excluded
mathematically in the companion report.
"""
from math import isqrt

def cases():
    for w in range(44,64):
        k = 15 if w<=45 else 16 if w<=47 else 17
        mods = (9,11,19,23) + ((7,) if w>=57 else ()) + ((49,) if w>=61 else ())
        yield w,k,mods

def mask_direct(w,p):
    sq = {x*x%p for x in range(p)}
    out=set()
    for c in range(p):
        terms = [(2*y+c)**2%p for y in range(w)]
        for n in range(p):
            out.add(sum(1<<y for y,z in enumerate(terms) if (n-z)%p in sq))
    return out

def mask_transposed(w,p):
    out=set()
    for c in range(p):
        rows=[]
        for y in range(w):
            z=(2*y+c)**2%p
            bs=0
            for d in range(p):
                bs |= 1<<((z+d*d)%p)
            rows.append(bs)
        for n in range(p):
            out.add(sum(1<<y for y,b in enumerate(rows) if b&(1<<n)))
    return out

def undominated(masks):
    keep=[]
    for m in sorted(set(masks),key=int.bit_count,reverse=True):
        if all((m&a)!=m for a in keep):
            keep.append(m)
    return keep

def witness(w,c,d):
    ys=[]
    for y in range(w):
        delta=1-4*(y*y+c*y+d)
        if delta<=0:
            continue
        z=isqrt(delta)
        if z*z!=delta or z%2!=1:
            continue
        for x in [(-1-z)//2,(-1+z)//2]:
            assert x*x+y*y+x+c*y+d==0
        ys.append(y)
    return ys

def main():
    for w,k,mods in cases():
        assert (w-1)//(k-1) <= 3
        # g=3: mod19 gives at least k-2>11 distinct residues
        assert k-max(0,(w+2)//3-19)>11
        states=[(1<<w)-1]
        for p in mods:
            A=mask_direct(w,p)
            assert A==mask_transposed(w,p),(w,p)
            local=undominated(m for m in A if m.bit_count()>=k)
            states=undominated(a&b for a in states for b in local
                               if (a&b).bit_count()>=k)
            print('WIDTH',w,'TARGET',k,'MOD',p,
                  'LOCAL',len(local),'SURVIVORS',len(states),flush=True)
            if not states:
                break
        assert not states,(w,k,'CRT intersection nonempty')
        c,d=(-43,-90) if w<=45 else (-47,0)
        rows=witness(w,c,d)
        assert len(rows)==k-1,(w,rows)
        print('PASS WIDTH',w,'T',k-1,'C',c,'D',d,'ROWS',rows,flush=True)
    print('PASS: all 20 widths; both mask methods; explicit circle witnesses')

if __name__=='__main__':
    main()
