#!/usr/bin/env python3
"""Exact modular certificate for the 3-adic anisotropic circle-row bound.

For any 3-adic integral quadratic f(i) with leading coefficient -4,
occupied rows are restricted to f(i) mod 9 in QR(9).  This is a finite
necessary-condition certificate, not a finite search over circles.
"""
from collections import Counter

QR = {x*x % 9 for x in range(9)}
assert QR == {0,1,4,7}

def polynomial(a,b,i):
    return (a + i*(b-a) - 4*i*(i-1)) % 9

def recurrence(a,b,w):
    out=[a,b]
    while len(out)<w:
        out.append((2*out[-1]-out[-2]-8)%9)
    return out[:w]

def max_hits(w):
    return max(sum(polynomial(a,b,i) in QR for i in range(w))
               for a in range(9) for b in range(9))

def run():
    for a in range(9):
        for b in range(9):
            assert recurrence(a,b,90) == [polynomial(a,b,i) for i in range(90)]
            assert all(polynomial(a,b,i)==polynomial(a,b,i+9) for i in range(9))
    counts=Counter(sum(polynomial(a,b,i) in QR for i in range(9))
                   for a in range(9) for b in range(9))
    assert dict(counts)=={0:18,3:9,5:27,6:27},counts
    base={w:max_hits(w) for w in range(5,14)}
    assert base=={5:4,6:4,7:5,8:6,9:6,10:7,11:8,12:8,13:9},base
    for w in range(5,2001):
        # recurrence+periodicity reduces the infinite case to the 9 bases
        r=(w-5)%9+5
        predicted=base[r]+6*((w-r)//9)
        assert predicted==(2*w+2)//3,(w,predicted)
    print('QR9:',sorted(QR))
    print('81 pairs / 9-row count histogram:',sorted(counts.items()))
    print('5..13 exact maxima:',base)
    print('For all w>=5: max QR rows <= ceil(2w/3), by period-9 induction.')
    print('Independent recurrence and polynomial formulas agree for 81 pairs x 90 terms.')
    print('PASS')
if __name__=='__main__':run()
