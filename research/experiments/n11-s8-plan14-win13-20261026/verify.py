#!/usr/bin/env python3
"""Standalone, cache-free N11 S8 WIN certificate verifier.

Original-first-player perspective: S8 WIN if an S9 child has all S10
children WIN. All S10 outcomes are re-solved from legal moves to terminal.
Independent 3x3 and 4x4 integer determinant implementations are compared.
"""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import sys

S8 = int('00000000000000821090a00000000020', 16)
S9 = int('000000000000408210a8400000000020', 16)
LEAVES = tuple(int(s, 16) for s in (Path(__file__).parent / 's10-win13.keys').read_text('ascii').split())
XY = [(i % 11, i // 11) for i in range(121)]


def det3(p):
    a, b, c, d = p
    x, y = XY[d]
    rows = [(XY[i][0]-x, XY[i][1]-y,
             XY[i][0]**2+XY[i][1]**2-x*x-y*y) for i in (a, b, c)]
    (u,v,w), (r,s,t), (f,g,h) = rows
    return u*(s*h-t*g)-v*(r*h-t*f)+w*(r*g-s*f)


def det4(p):
    m = [[XY[i][0], XY[i][1], XY[i][0]**2+XY[i][1]**2, 1] for i in p]
    sign, prev = 1, 1
    for k in range(3):
        if m[k][k] == 0:
            for j in range(k+1, 4):
                if m[j][k]:
                    m[k], m[j] = m[j], m[k]
                    sign = -sign
                    break
            else:
                return 0
        pivot = m[k][k]
        for i in range(k+1, 4):
            for j in range(k+1, 4):
                numerator = m[i][j]*pivot-m[i][k]*m[k][j]
                assert numerator % prev == 0
                m[i][j] = numerator//prev
        for i in range(k+1, 4):
            m[i][k] = 0
        prev = pivot
    return sign*m[3][3]


def points(b):
    return tuple(i for i in range(121) if b>>i&1)


def canonical(b):
    result = None
    for k in range(8):
        out = 0
        for p in points(b):
            x,y=XY[p]
            q=((x,y),(10-y,x),(10-x,10-y),(y,10-x),
               (10-x,y),(10-y,10-x),(x,10-y),(y,x))[k]
            out |= 1 << (q[0]+11*q[1])
        if result is None or out < result:
            result=out
    return result


def solver(det):
    @lru_cache(maxsize=None)
    def bad(q):
        return det(q) == 0
    @lru_cache(maxsize=None)
    def legal(b):
        pp = points(b)
        triples = tuple(combinations(pp, 3))
        return tuple(i for i in range(121) if not (b>>i)&1
                     and all(not bad(tuple(sorted(t+(i,)))) for t in triples))
    def safe(b):
        return all(not bad(q) for q in combinations(points(b), 4))
    def children(b):
        return {canonical(b|(1<<p)) for p in legal(b)}
    def terminal(b):
        @lru_cache(maxsize=None)
        def win(board):
            for p in legal(board):
                if not win(board|(1<<p)):
                    return True
            return False
        result=win(b)
        return result,win.cache_info().currsize
    return safe,children,terminal


def verify(leaves=LEAVES, root=S8, witness=S9, negative=False):
    assert len(leaves)==len(set(leaves))==13
    assert list(leaves)==sorted(leaves)
    assert root.bit_count()==8 and witness.bit_count()==9
    results=[]
    for det in (det3,det4):
        safe,children,terminal=solver(det)
        assert safe(root) and safe(witness)
        assert canonical(root)==root and canonical(witness)==witness
        assert witness in children(root)
        actual=children(witness)
        assert actual==set(leaves), 'missing or illegal S10 child'
        states=[]
        for b in leaves:
            assert b.bit_count()==10 and safe(b) and canonical(b)==b
            ans,count=terminal(b)
            assert ans, f'S10 child not WIN: {b:032x}'
            states.append(count)
        results.append(states)
    assert results[0]==results[1], 'independent terminal geometry disagrees'
    if negative:
        for altered,rt,wt in ((leaves[:-1],root,witness),
                               (leaves[1:]+leaves[:1],root,witness),
                               (leaves[:-1]+(root,),root,witness),
                               (leaves,root,root)):
            try:
                verify(altered,rt,wt)
            except (AssertionError,ValueError):
                continue
            raise AssertionError('tampered certificate accepted')
    return {'s8_win':f'{root:032x}', 's9_witness':f'{witness:032x}',
            's10_win_leaves':len(leaves),
            'terminal_states_each_geometry':sum(results[0]),
            'leaf_state_counts':results[0],
            'new_s7_win':0,'new_s5_verdict':0,'empty_board':'UNKNOWN'}


if __name__=='__main__':
    print(verify(negative='--negative' in sys.argv))
