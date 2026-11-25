#!/usr/bin/env python3
"""Exact finite exclusion for T(w), 5<=w<=43; uses two independent mask builders."""
from itertools import combinations
from math import isqrt
from verify_double_rows_44_63 import mask_direct, mask_transposed, undominated

CASES={
5:(5,(9,)),6:(5,(9,)),7:(6,(9,)),8:(7,(9,)),9:(7,(9,)),
10:(7,(9,11)),11:(8,(9,11)),12:(9,(9,)),
13:(9,(9,11,19)),14:(9,(9,11,19,23)),15:(9,(9,11,19,23)),
16:(9,(9,11,19,23,7)),17:(9,(9,11,19,23,7,43)),
18:(9,(9,11,19,23,7,43)),
19:(9,(9,11,19,23,7,49,43)),20:(9,(9,11,19,23,7,49,43)),
21:(9,(9,11,19,23,7,49,43,121)),22:(10,(9,11,19,23,7,49)),
23:(11,(9,11,19,23)),24:(11,(9,11,19,23)),
25:(12,(9,11,19)),26:(13,(9,11,19)),
43:(14,(9,11,19,23,7))}
for w in range(27,43):
    CASES[w]=(13,(9,11,19) if w<=31 else
                 (9,11,19,23) if w<=36 else (9,11,19,23,7))

def upper(w):
    if w<=6: return 4
    if w==7: return 5
    if w<=10: return 6
    if w==11: return 7
    if w<=21: return 8
    if w==22: return 9
    if w<=24: return 10
    if w==25: return 11
    if w<=42: return 12
    return 13

def witness_coeff(w):
    if w<=6: return (-3,0)
    if w<=10: return (-7,0)
    if w<=21: return (-11,-2)
    if w<=42: return (-25,-6)
    return (-47,0)

def check_witness(w):
    c,d=witness_coeff(w)
    ys=[]
    for y in range(w):
        delta=1-4*(y*y+c*y+d)
        if delta<=0: continue
        r=isqrt(delta)
        if r*r!=delta or r%2!=1: continue
        x1,x2=(-1-r)//2,(-1+r)//2
        assert x1!=x2
        assert x1*x1+y*y+x1+c*y+d==0
        assert x2*x2+y*y+x2+c*y+d==0
        ys.append(y)
    assert len(ys)==upper(w),(w,ys)
    return ys

def exclude_gcd3(w,k):
    if w<=36: return
    # All chosen rows lie in a single residue class mod 3; modulo 11
    # each set of k>=13 rows must have at least 9 different residues.
    for a in range(3):
        seq=list(range(a,w,3))
        for sel in combinations(seq,k):
            assert len({i%11 for i in sel})>=9,(w,sel)

def main():
    assert len(CASES)==39
    for w,(k,mods) in sorted(CASES.items()):
        assert upper(w)==k-1
        assert (w-1)//(k-1)<=3
        exclude_gcd3(w,k)
        states=[(1<<w)-1]
        for mod in mods:
            a=mask_direct(w,mod)
            b=mask_transposed(w,mod)
            assert a==b,(w,mod)
            local=undominated(x for x in a if x.bit_count()>=k)
            states=undominated(i&j for i in states for j in local
                              if (i&j).bit_count()>=k)
            print("WIDTH",w,"TARGET",k,"MOD",mod,
                  "LOCAL",len(local),"REMAINING",len(states),flush=True)
            if not states: break
        assert not states,("congruence survivor",w,k,mods)
        rows=check_witness(w)
        print("PASS",w,"T",len(rows),"ROWS",rows,flush=True)
    print("PASS all 39 widths and both mask builders")

if __name__=="__main__":
    main()
