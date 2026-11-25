#!/usr/bin/env python3
"""Independent finite audit for the 3-row, 69-column extension theorem.

Finite audit only. The unbounded result follows from the README proof.
"""
from fractions import Fraction
from itertools import combinations, permutations
from random import Random
from math import comb

PERMS = [(p, (-1)**sum(p[i] > p[j] for i in range(4) for j in range(i+1,4)))
         for p in permutations(range(4))]


def determinant(points, lam):
    p, q = lam.numerator, lam.denominator
    rows = [[q*x*x + p*y*y, x, y, 1] for x,y in points]
    return sum(sign * rows[0][perm[0]] * rows[1][perm[1]] *
               rows[2][perm[2]] * rows[3][perm[3]] for perm,sign in PERMS)


def rank2_triple(triple, lam):
    # A triple is rank 2 precisely when every fourth point is forbidden.
    return all(determinant((*triple, (x,y)),lam)==0
               for y in range(3) for x in range(6) if (x,y) not in triple)


def audit_polynomial():
    board = [(x,y) for y in range(3) for x in range(6)]
    total = 0
    for lam in map(Fraction, ['-4','-1','-1/4','0','1/3','1/2','1','3/2','2']):
        for triple in combinations(board,3):
            if rank2_triple(triple,lam):
                continue
            for y in range(3):
                k = sum(t[1] == y for t in triple)
                if k > 2:
                    continue
                values = [determinant((*triple,(x,y)),lam) for x in range(3)]
                a = (values[2] - 2*values[1] + values[0]) // 2
                b = values[1]-values[0]-a
                c = values[0]
                assert all(a*x*x+b*x+c == determinant((*triple,(x,y)),lam)
                           for x in range(6))
                assert (a,b,c) != (0,0,0), (lam,triple,y)
                zeros = [x for x in range(6) if a*x*x+b*x+c == 0]
                if k==2:
                    assert len(zeros)<=2 and all(t[0] in zeros for t in triple if t[1]==y)
                elif k==1:
                    assert len(zeros)<=2 and all(t[0] in zeros for t in triple if t[1]==y)
                else:
                    assert len(zeros)<=2
                total += 1
    return total


def safe_add(S, pt, lam):
    return all(determinant((*triple,pt),lam) != 0 for triple in combinations(S,3))


def audit_large_board():
    rng=Random(20261024)
    m=69
    checked=0
    for lam in map(Fraction, ['-4','-1','-1/4','0','1/3','1/2','1','2']):
        board=[(x,y) for y in range(3) for x in range(m)]
        for _ in range(20):
            S=[]
            for pt in rng.sample(board,len(board)):
                if len(S)>=8:break
                if sum(t[1]==pt[1] for t in S)>=3:continue
                if safe_add(S,pt,lam):S.append(pt)
            if len(S)<4:continue
            assert any(safe_add(S,pt,lam) for pt in board if pt not in S), (lam,S)
            checked+=1
    return checked

if __name__=='__main__':
    print('row-polynomial triples checked:', audit_polynomial())
    print('safe 4..8-stone states at m=69 with an extension:',audit_large_board())
    print('combinatorial blocking cap: k=2:', 2*(comb(6,3)-2)+2*comb(6,2)+2)
