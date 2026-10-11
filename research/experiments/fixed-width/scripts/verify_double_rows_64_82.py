#!/usr/bin/env python3
"""Finite exact modular obstruction for T(w)=16, 64<=w<=82.

Mathematical reduction in the companion report. No circle search is assumed:
all possible mod-p discriminant masks are enumerated, and only supersets
are kept under intersections. A second mask builder checks each local mask.
"""
from math import isqrt

FIRST, LAST, TARGET = 64, 82, 17
BASE_MODULI = (9, 11, 19, 23, 7, 49)
STEP_MODULI = (9, 7, 49, 11, 19, 23, 31, 43)


def masks_discriminant(w, p):
    sq = {x*x % p for x in range(p)}
    result = set()
    for c in range(p):
        z = [(2*y+c)**2 % p for y in range(w)]
        for n in range(p):
            result.add(sum(1<<y for y,v in enumerate(z) if (n-v)%p in sq))
    return result


def masks_roots(w, p):
    result = set()
    for c in range(p):
        by_row = []
        for y in range(w):
            z = (2*y+c)**2 % p
            by_row.append({(z+t*t)%p for t in range(p)})
        for n in range(p):
            result.add(sum(1<<y for y,ns in enumerate(by_row) if n in ns))
    return result


def maximal(masks):
    result = []
    for a in sorted(set(masks), key=int.bit_count, reverse=True):
        if all(a & b != a for b in result):
            result.append(a)
    return result


def exclude(w, moduli, force_endpoints, residue3=False):
    full = (1<<w)-1
    required = (1 | 1<<(w-1)) if force_endpoints else 0
    allowed = (sum(1<<y for y in range(0,w,3)) if residue3 else full)
    states = [allowed]
    trace = []
    for p in moduli:
        assert p % 3 != 0 if residue3 else True
        first = masks_discriminant(w,p)
        assert first == masks_roots(w,p), ('independent mask disagreement',w,p)
        local = maximal(a & allowed for a in first
                        if (a & required)==required and (a & allowed).bit_count()>=TARGET)
        states = maximal(a & b for a in states for b in local
                         if (a & b).bit_count()>=TARGET)
        trace.append((p,len(local),len(states)))
        if not states:
            break
    assert not states, ('unexcluded',w,force_endpoints,residue3,trace)
    return trace


def witness():
    ys = []
    for y in range(LAST):
        d = 1-4*(y*y-47*y)
        if d <= 0: continue
        z = isqrt(d)
        if z*z != d or z%2 != 1: continue
        for x in ((-1-z)//2,(-1+z)//2):
            assert x*x+y*y+x-47*y == 0
        ys.append(y)
    assert len(ys)==16
    return ys


def main():
    # For 17 rows in 64, the gcd g of their differences is <=3.
    # For g=3, at most 22 rows in a fixed class mod3, hence at least
    # 17-(22-19)=14 distinct residues mod19; a circle allows <=11.
    assert (FIRST-1)//(TARGET-1)==3
    assert TARGET-(22-19) > (19+3)//2
    base = exclude(FIRST,BASE_MODULI,False)
    print('BASE',FIRST,base,flush=True)
    all_traces = {FIRST:base}
    for w in range(FIRST+1,LAST+1):
        # If T(w-1)<=16, a 17-hit circle in w rows must hit BOTH
        # endpoint rows: otherwise it fits in a shifted w-1 window.
        # With endpoints fixed, g divides w-1, and g<=floor((w-1)/16)<=5.
        assert (w-1)//16<=5
        trace = exclude(w,STEP_MODULI,True)
        # All moduli above are coprime to g=1,2,4,5. For g=3,
        # both endpoints must be 0 mod3, and mod11,19 suffice.
        if (w-1)%3 == 0:
            trace3 = exclude(w,(11,19),True,True)
        else:
            trace3 = []
        all_traces[w] = (trace,trace3)
        print('PASS',w,'generic',trace[-1], 'g3',trace3[-1] if trace3 else 'impossible',flush=True)
    ys=witness()
    print('PASS T(w)=16 for every 64<=w<=82; witness rows',ys,flush=True)
    return all_traces


if __name__ == '__main__':
    main()
