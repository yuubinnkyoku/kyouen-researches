#!/usr/bin/env python3
"""Finite independent audits for K0619; not a proof of the limit theorem."""
from collections import Counter
from fractions import Fraction
from itertools import product


def arm_dp(length, center, first=None):
    states = Counter()
    for bit in (0, 1):
        if first is None or bit == first:
            states[(center, bit, int(center == 0 and bit == 1))] += 1
    for _ in range(1, length):
        new = Counter()
        for (a, b, k), count in states.items():
            for c in (0, 1):
                if (a, b, c) != (0, 0, 0):
                    new[(b, c, k + (b == 0 and c == 1))] += count
        states = new
    out = Counter()
    for (a, b, k), count in states.items():
        if a or b:
            out[k - (center == 0)] += count
    return +out


def arm_words(length, center, first=None):
    out = Counter()
    for bits in product((0, 1), repeat=length):
        if first is not None and bits[0] != first:
            continue
        seq = (center,) + bits + (0,)
        if any(seq[i-1:i+2] == (0, 0, 0) for i in range(1, length+1)):
            continue
        exponent = sum(seq[i-1:i+1] == (0, 1) for i in range(1, length+1)) - (center == 0)
        out[exponent] += 1
    return +out


def multiply(a, b):
    out = Counter()
    for i, x in a.items():
        for j, y in b.items():
            out[i+j] += x*y
    return +out


def predicted(arms):
    E, d = sum(arms), len(arms)
    s = 2+E
    F, G, J = Counter({0:1}), Counter({0:1}), Counter({0:1})
    for ell in arms:
        F = multiply(F, arm_dp(ell, 1))
        G = multiply(G, arm_dp(ell, 0))
        J = multiply(J, arm_dp(ell, 0, first=0))
    out = Counter({s+E-1:1})
    for k, v in F.items():
        out[s+k] += v
    for k, v in G.items():
        out[s+d-1+k] += v
    for k, v in J.items():
        out[s+d-1+k] -= v
    return +out


def graph_direct(arms):
    edges, nxt = [], 1
    for ell in arms:
        p = 0
        for _ in range(ell):
            edges.append((p, nxt))
            p, nxt = nxt, nxt+1
    adj = [0]*nxt
    for a, b in edges:
        adj[a] |= 1<<b
        adj[b] |= 1<<a
    E = len(edges)
    N = 2+2*E
    out = Counter({N-1:1})
    for removed in range(1<<nxt):
        kept = ((1<<nxt)-1)^removed
        if any((removed>>v)&1 and not (adj[v]&kept) for v in range(nxt)):
            continue
        kept_edges = sum(bool((kept>>a)&1 and (kept>>b)&1) for a,b in edges)
        out[N-removed.bit_count()-kept_edges] += 1
    return +out


def moments(poly):
    total = sum(poly.values())
    mean = Fraction(sum(k*v for k,v in poly.items()), total)
    var = sum((Fraction(k)-mean)**2*v for k,v in poly.items())/total
    return mean, var


def main():
    words_checked = 0
    for ell in range(1, 13):
        for center, first in ((1,None),(0,None),(0,0)):
            assert arm_dp(ell,center,first)==arm_words(ell,center,first)
            words_checked += 1
    graph_cases, subsets = 0, 0
    for n in range(1,4):
        for extras in ((1,), (3,), (4,), (1,3), (3,3), (4,1)):
            arms = (2,)*n + extras
            if sum(arms)>11:
                continue
            assert predicted(arms)==graph_direct(arms), arms
            graph_cases += 1
            subsets += 1 << (1+sum(arms))
    root=1.8392867552141612
    ratios=[]
    variances=[]
    for ell in range(1,301):
        f,g=arm_dp(ell,1),arm_dp(ell,0)
        a,b=sum(f.values()),sum(g.values())
        if ell!=2:
            assert Fraction(b,a) <= Fraction(17,20)
        if ell>=2:
            mu,var=moments(f)
            assert var>0
            variances.append(float(var/ell))
        if ell in (10,50,100,300):
            ratios.append((ell,float(Fraction(b,a))))
    print(f"PASS: {words_checked} direct word comparisons; {graph_cases} direct graph cases ({subsets:,} vertex subsets)")
    print(f"PASS: 300 finite variance positivity and ratio checks; min observed Var(Y_l)/l={min(variances):.9f}")
    print(f"B_l/A_l samples={ratios}; predicted asymptotic ratio={root-1:.12f}")


if __name__=='__main__':
    main()
