#!/usr/bin/env python3
"""Exact 2-square witness enumeration and shortest k-row windows for four fixed norms."""
import csv
from math import isqrt
from pathlib import Path

NORMS = (59283250, 296416250, 770682250, 2430613250)
OUTPUT = Path(__file__).resolve().parents[1] / 'output' / 'double_rows_97_256.csv'

def rows_y(n):
    r = isqrt(n)
    ys = []
    for y in range(-r, r + 1):
        v = n - y * y
        x = isqrt(v)
        if v > 0 and x * x == v and x % 2 and y % 2:
            ys.append(y)
    return ys

def best_window(ys, k):
    return min(((ys[i+k-1]-ys[i])//2+1, ys[i], ys[i+k-1])
               for i in range(len(ys)-k+1))

def main():
    rows = {n: rows_y(n) for n in NORMS}
    assert [len(rows[n]) for n in NORMS] == [128,160,192,256]
    records = []
    for k in range(97, 257):
        w, lo, hi, n = min(((*best_window(ys, k), n)
                            for n, ys in rows.items() if len(ys) >= k))
        assert lo % 2 == hi % 2 == 1 and (hi-lo)//2+1 == w
        c = -lo
        d = (1+c*c-n)//4
        assert (1+c*c-n) % 4 == 0
        # Independently check the 2 integer points on each of k rows.
        within = [y for y in rows[n] if lo <= y <= hi]
        assert len(within) == k
        for Y in within:
            X = isqrt(n-Y*Y)
            for x in ((X-1)//2, (-X-1)//2):
                y = (Y-lo)//2
                assert 0 <= y < w and x*x+y*y+x-c*y+d == 0
        records.append((k,w,n,lo,hi,c,d))
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT.open('w', newline='') as f:
        wr=csv.writer(f); wr.writerow(('k','w','N','Ylo','Yhi','C','D')); wr.writerows(records)
    for k in (97,100,112,128,129,144,160,161,192,193,224,256):
        print('BOUND', *records[k-97])
    print('PASS',len(records),'constructive lower bounds, four exact norm scans')

if __name__=='__main__':main()
