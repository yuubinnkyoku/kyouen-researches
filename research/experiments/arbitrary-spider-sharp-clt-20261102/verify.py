#!/usr/bin/env python3
"""Finite independent checks for K0620 (not a proof of asymptotics)."""
from collections import Counter
from itertools import product
from math import isclose


def mul(a, b):
    c = Counter()
    for x, v in a.items():
        for y, w in b.items():
            c[x+y] += v*w
    return +c


def word_polys(ell):
    ans = [Counter(), Counter(), Counter()]
    for center in (0, 1):
        for bits in product((0, 1), repeat=ell):
            seq = (center,) + bits + (0,)
            if any(seq[i] == 0 and seq[i-1] == 0 and seq[i+1] == 0
                   for i in range(1, ell+1)):
                continue
            starts = sum(seq[i-1] == 0 and seq[i] == 1 for i in range(1, ell+1))
            if center:
                ans[0][starts] += 1
            else:
                ans[1][starts-1] += 1
                if bits[0] == 0:
                    ans[2][starts-1] += 1
    return tuple(+x for x in ans)


def dynamic_poly(ell, center, first=None):
    # Independent left-to-right automaton with trailing 0 boundary.
    dp = Counter({(center, center, 0): 1})
    for i in range(ell):
        nxt = Counter()
        for (a, b, score), cnt in dp.items():
            for c in (0, 1):
                if i == 0 and first is not None and c != first:
                    continue
                if i > 0 and a == b == c == 0:
                    continue
                nxt[(b, c, score + int(b == 0 and c == 1))] += cnt
        dp = nxt
    out = Counter()
    for (a, b, score), cnt in dp.items():
        if not (a == b == 0):
            out[score - int(center == 0)] += cnt
    return +out


def predicted(lengths):
    n = lengths.count(2)
    other = [ell for ell in lengths if ell != 2]
    s = 2 + sum(lengths)
    F, G, J = Counter({0:1}), Counter({0:1}), Counter({0:1})
    for ell in other:
        f,g,j = word_polys(ell)
        F, G, J = mul(F,f), mul(G,g), mul(J,j)
    f2,g2,j2 = word_polys(2)
    for _ in range(n):
        F, G, J = mul(F,f2), mul(G,g2), mul(J,j2)
    out = Counter()
    for k,v in F.items(): out[s+k] += v
    for k,v in G.items(): out[s+len(lengths)-1+k] += v
    for k,v in J.items(): out[s+len(lengths)-1+k] -= v
    out[s+sum(lengths)-1] += 1
    return +out


def brute_graph(lengths):
    edges=[]; nv=1
    for ell in lengths:
        parent=0
        for _ in range(ell):
            edges.append((parent,nv))
            parent=nv
            nv+=1
    adj=[0]*nv
    for a,b in edges:
        adj[a]|=1<<b; adj[b]|=1<<a
    N=1+nv+len(edges)
    out=Counter({N-1:1})
    full=(1<<nv)-1
    for deleted in range(1<<nv):
        kept=full^deleted
        if any((deleted>>i)&1 and not (adj[i]&kept) for i in range(nv)):
            continue
        e=sum(bool(kept&(1<<a)) and bool(kept&(1<<b)) for a,b in edges)
        out[N-deleted.bit_count()-e]+=1
    return +out


def moments(p):
    z=sum(p.values()); m=sum(x*v for x,v in p.items())/z
    return m, sum((x-m)**2*v for x,v in p.items())/z


def main():
    word_checks=0
    for ell in range(1,13):
        f,g,j=word_polys(ell)
        assert f==dynamic_poly(ell,1)
        assert g==dynamic_poly(ell,0)
        assert j==dynamic_poly(ell,0,first=0)
        word_checks+=3
    assert word_polys(2)==(Counter({0:2,1:1}),Counter({0:3}),Counter({0:1}))
    graph_cases=0; subsets=0
    for n in (1,2,3):
        for ell1,ell2 in product((1,3,4,5),repeat=2):
            lengths=[2]*n+[ell1,ell2]
            if 1+sum(lengths)>15:
                continue
            a=predicted(lengths); b=brute_graph(lengths)
            assert a==b, (lengths,a,b)
            graph_cases+=1; subsets+=1<<(1+sum(lengths))
    # Includes one-arm, no-arm, and multiple noncritical arms.
    for lengths in ([2,2],[1,2,2],[2,3],[2,2,3,4],[1,1,2,3]):
        a=predicted(lengths); b=brute_graph(lengths)
        assert a==b, lengths
        graph_cases+=1; subsets+=1<<(1+sum(lengths))
    # Independent finite tests of asymptotic input; not a proof of uniformity.
    for ell in range(1,301):
        f=dynamic_poly(ell,1); g=dynamic_poly(ell,0)
        A,B=sum(f.values()),sum(g.values())
        assert B>0 and A>0
        if ell!=2: assert 0.5 <= B/A <= 0.85+1e-12
        if ell>=80:
            mf,vf=moments(f); mg,vg=moments(g)
            assert abs(mf-mg)<2
            assert vf>0 and vg>0
            assert abs(vf/ell-0.063803198448)<0.02
            assert abs(vg/ell-0.063803198448)<0.02
    lam=1.8392867552141612
    for k in (1,2,3):
        lengths=[100+7*i for i in range(k)]
        ratio=1
        for ell in lengths:
            f=dynamic_poly(ell,1);g=dynamic_poly(ell,0)
            ratio*=sum(g.values())/sum(f.values())
        assert isclose(ratio,(lam-1)**k,rel_tol=1e-8)
    print(f'PASS: {word_checks} independent branch-word checks; '
          f'{graph_cases} direct graph cases / {subsets:,} subsets')
    print('PASS: 300 finite branch ratios, 221 moment checks, k=1..3 long-arm weights')


if __name__=='__main__': main()
