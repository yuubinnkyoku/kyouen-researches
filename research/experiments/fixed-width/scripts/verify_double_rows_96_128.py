#!/usr/bin/env python3
"""Exact T(96..128), conditional only on the proved base T(95)=19.

The upper bounds use mathematical induction and exhaustive modular NECESSARY
conditions; they do not enumerate bounded-radius circles.
"""
from functools import lru_cache
from math import gcd, isqrt

MODS = (9, 11, 7, 19, 23, 49, 31, 37, 41, 43, 47, 53)
EXPECTED = {**{w:20 for w in range(96,100)},100:21,**{w:22 for w in range(101,105)},105:23,**{w:24 for w in range(106,129)}}


def maximal(masks):
    keep=[]
    for a in sorted(set(masks), key=int.bit_count, reverse=True):
        if not any(a & b == a for b in keep):
            keep.append(a)
    return keep


@lru_cache(None)
def local_masks(length, modulus, target):
    qr={x*x % modulus for x in range(modulus)}
    out=[]
    for c in range(modulus):
        shifts=[(2*y+c)**2 % modulus for y in range(length)]
        for n in range(modulus):
            mask=sum(1<<y for y,s in enumerate(shifts) if (n-s)%modulus in qr)
            if mask.bit_count()>=target and mask & 1 and mask >> (length-1) & 1:
                out.append(mask)
    return maximal(out)


def excluded(width, g, target):
    length=(width-1)//g+1
    states=[(1<<length)-1]
    for p in MODS:
        if gcd(p,g)>1:continue
        loc=local_masks(length,p,target)
        states=maximal(a&b for a in states for b in loc if (a&b).bit_count()>=target)
        print('CASE',width,target,g,p,len(loc),len(states))
        if not states:return True
    return False


def witness_rows(width, c, d):
    out=[]
    for y in range(width):
        disc=1-4*(y*y+c*y+d)
        if disc<=0:continue
        s=isqrt(disc)
        if s*s==disc and s%2:
            xs=((-1-s)//2,(-1+s)//2)
            assert xs[0]!=xs[1]
            assert all(x*x+y*y+x+c*y+d==0 for x in xs)
            out.append(y)
    return out


def main():
    assert len(witness_rows(95,-105,-6))==19
    prev=19
    for w in range(96,129):
        # The -95,-506 circle is best through w=104, then the -105,-6 circle.
        choices=[(-95,-506),(-105,-6)]
        count,c,d=max((len(witness_rows(w,c,d)),c,d) for c,d in choices)
        assert count>=prev
        if count==prev+1:
            prev+=1
            print('WIDTH',w,'EXACT',prev,'WITNESS_STEP',c,d)
        else:
            assert count==prev
            target=prev+1
            gs=[g for g in range(1,(w-1)//(target-1)+1) if (w-1)%g==0]
            assert all(excluded(w,g,target) for g in gs)
            print('WIDTH',w,'EXACT',prev,'EXCLUDED',gs)
        assert prev==EXPECTED[w]
    print('PASS T(96..128)')

if __name__=='__main__':main()
