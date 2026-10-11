#!/usr/bin/env python3
"""Independent integer-only check of four explicit double-row witnesses."""
from math import isqrt

CIRCLES = ((-47,0),(-105,-6),(-95,-506),(-235,-6))
EXPECTED = [(212,213,25),(214,220,26),(221,225,27),(226,231,28),(232,232,29),(233,234,30),(235,235,31),(236,256,32)]

def rows(c,d,limit):
    good=[]
    for y in range(limit):
        v=1-4*(y*y+c*y+d)
        if v<=0:continue
        r=isqrt(v)
        if r*r!=v or r%2==0:continue
        xs=((-1-r)//2,(-1+r)//2)
        assert xs[0]!=xs[1]
        for x in xs:assert x*x+y*y+x+c*y+d==0
        good.append(y)
    return good

def main():
    table={}
    for w in range(211,257):
        counts=[len(rows(c,d,w)) for c,d in CIRCLES]
        table[w]=max(counts)
        if w>=212:
            target=next(k for lo,hi,k in EXPECTED if lo<=w<=hi)
            assert table[w]==target,(w,counts,target)
    assert table[211]==25
    for lo,hi,k in EXPECTED:
        print(f"{lo}..{hi}: T(w)>={k}, witness counts independently checked")
    c,d=CIRCLES[-1]
    print("last circle rows 0..255:",rows(c,d,256))
    print("PASS all 45 widths and both integer roots")
if __name__=='__main__':main()
