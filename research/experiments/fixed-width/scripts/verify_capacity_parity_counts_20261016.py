#!/usr/bin/env python3
"""Finite exhaustive audits of exact capacity-game P/N counting formulas."""
from itertools import product
from math import comb


def formula(w, m, r):
    r = min(r, m)
    s = sum(comb(m, k) for k in range(r+1))
    a = comb(m-1, r) if r <= m-1 else 0
    edges = w*m*sum(comb(m-1,k) for k in range(r))*s**(w-1)
    return (s**w - a**w)//2, (s**w + a**w)//2, comb(m,r)**w, edges


def direct(w, m, r):
    counts = [0,0]
    terminal = 0
    edges = 0
    for row_masks in product(range(1<<m), repeat=w):
        pop = [mask.bit_count() for mask in row_masks]
        if any(k>r for k in pop):
            continue
        remaining = sum(min(r,m)-k for k in pop)
        counts[remaining%2] += 1  # index 0: losing, 1: winning
        terminal += (remaining==0)
        edges += sum(m-k for k in pop if k < r)
    return counts[1], counts[0], terminal, edges


def main():
    cases=0
    for w in range(1,4):
        for m in range(1,6):
            for r in range(1,6):
                got = direct(w,m,r)
                expected = formula(w,m,r)
                assert got == expected, (w,m,r,got,expected)
                cases+=1
    print('independent exhaustive Boolean-subset audits:',cases,'PASS')
    for m in (7,8,9,10,12,30,100,1000):
        win,loss,terminal,edges=formula(5,m,8)
        total=win+loss
        print(f'q59 m={m}: total={total}, winning={win}, losing={loss}, terminal={terminal}, edges={edges}, win_fraction={win/total:.12g}')
    print('PASS')

if __name__ == '__main__':
    main()
