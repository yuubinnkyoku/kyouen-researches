#!/usr/bin/env python3
"""Independent checks of cycle graph-star terminal polynomials and CLT parameters."""
from collections import Counter


def add(a, b):
    c = Counter(a)
    c.update(b)
    return +c


def shift(a, degree, scale=1):
    return {k + degree: v * scale for k, v in a.items()}


def by_recurrence(t, r):
    assert t >= 4 and r >= 1
    z = {1: {1: r}, 2: {2: r*r, 3: 2},
         3: {3: r**3, 4: 3*r+3}}
    for k in range(4, t+1):
        z[k] = add(add(shift(z[k-1], 1, r), shift(z[k-2], 3)),
                   shift(z[k-3], 4))
    return add(shift(z[t], 1+(r-1)*t), {(r+1)*t: 1})


def by_circular_words(t, r):
    hist = Counter({(r+1)*t: 1})
    for mask in range(1 << t):
        bits = [(mask >> i) & 1 for i in range(t)]
        if any(bits[i] and bits[(i-1) % t] and bits[(i+1) % t]
               for i in range(t)):
            continue
        e00 = sum((1-bits[i])*(1-bits[(i+1) % t]) for i in range(t))
        h = 1+(r+1)*t-sum(bits)-e00
        hist[h] += r**e00
    return dict(hist)


def by_transfer(t, r):
    states = ((0,0), (0,1), (1,0), (1,1))
    hist = Counter({(r+1)*t: 1})
    for start in states:
        paths = {(start, 0): 1}
        for _ in range(t):
            nxt = Counter()
            for (state, deg), ways in paths.items():
                a, b = state
                for c in (0, 1):
                    if a == b == c == 1:
                        continue
                    e00 = (1-b)*(1-c)
                    nxt[((b,c), deg+2-c-e00)] += ways*r**e00
            paths = nxt
        for (state, deg), ways in paths.items():
            if state == start:
                hist[deg+1+(r-1)*t] += ways
    return dict(hist)


def by_full_hypergraph(t, r):
    n = 1+(r+1)*t
    hyperedges = []
    for i in range(t):
        j = (i+1) % t
        edge = 1 | (1 << (1+i)) | (1 << (1+j))
        for k in range(r):
            edge |= 1 << (1+t+r*i+k)
        hyperedges.append(edge)
    full = (1 << n)-1
    hist = Counter()
    for mask in range(1 << n):
        if any((mask & edge) == edge for edge in hyperedges):
            continue
        missing = full ^ mask
        maximal = True
        while missing:
            bit = missing & -missing
            missing ^= bit
            if not any(((mask | bit) & edge) == edge for edge in hyperedges):
                maximal = False
                break
        if maximal:
            hist[mask.bit_count()] += 1
    return dict(hist)


def mean_variance(hist):
    total = sum(hist.values())
    mean = sum(k*v for k, v in hist.items())/total
    variance = sum((k-mean)**2*v for k, v in hist.items())/total
    return mean, variance


def dominant_root(r):
    lo, hi = float(r), float(r+2)
    for _ in range(80):
        m = (lo+hi)/2
        if m**3-r*m*m-m-1 > 0:
            hi = m
        else:
            lo = m
    return (lo+hi)/2


def main():
    word_cases = transfer_cases = hyper_cases = 0
    for r in range(1, 5):
        for t in range(4, 13):
            expected = by_recurrence(t, r)
            assert expected == by_circular_words(t, r), (t,r,'words')
            assert expected == by_transfer(t, r), (t,r,'transfer')
            assert expected[r*t+1] == r**t, (t,r,'minimum')
            assert expected[(r+1)*t] == 1, (t,r,'maximum')
            word_cases += 1
            transfer_cases += 1
    masks = 0
    for t,r in ((4,1),(5,1),(6,1),(4,2),(5,2),(6,2)):
        assert by_recurrence(t,r) == by_full_hypergraph(t,r), (t,r,'hypergraph')
        masks += 1 << (1+(r+1)*t)
        hyper_cases += 1
    for r in range(1,5):
        lam = dominant_root(r)
        alpha = r + 1/(lam*lam-lam+2)
        beta = lam*(lam-1)**2*(lam*lam+lam+1)/(
            (lam+1)*(lam*lam-lam+2)**3)
        assert beta > 0
        for t in (40, 60, 100):
            mu, var = mean_variance(by_recurrence(t,r))
            assert abs(mu-(1+alpha*t)) < 0.05, (r,t,mu,alpha)
            assert abs(var-beta*t) < 0.15, (r,t,var,beta)
        print('q=',r+3,'lambda=',round(lam,12),'alpha=',round(alpha,12),
              'beta=',round(beta,12))
    print('C6 q=5 histogram:', dict(sorted(by_recurrence(6,2).items())))
    print('PASS:',word_cases,'circular-word cases,',transfer_cases,
          'independent transfer cases,',hyper_cases,'full-hypergraph cases,',
          masks,'full-hypergraph subsets, 12 asymptotic-moment checks')


if __name__ == '__main__':
    main()
