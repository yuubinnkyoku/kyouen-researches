#!/usr/bin/env python3
"""Exhaustive labelled-subset check of hypergraph blow-up parity recurrence.
No dependency on the quotient transition implementation for the brute game.
"""
from functools import lru_cache
from itertools import combinations, product
from collections import Counter
import json


def mex(vals):
    s = set(vals)
    i = 0
    while i in s:
        i += 1
    return i


def check_case(k, sizes, base_edges):
    # Expand every base edge into all pointwise transversal forbidden sets.
    parts = []
    pos = 0
    for n in sizes:
        parts.append(tuple(range(pos, pos+n)))
        pos += n
    forb = []
    for e in base_edges:
        ids = [i for i in range(k) if e & (1 << i)]
        for xs in product(*(parts[i] for i in ids)):
            forb.append(sum(1 << j for j in xs))
    n = sum(sizes)
    active = [0] * (1 << n)
    free_parity = [0] * (1 << n)
    for mask in range(1 << n):
        for i, group in enumerate(parts):
            num = sum(bool(mask & (1 << j)) for j in group)
            if num:
                active[mask] |= 1 << i
                free_parity[mask] ^= (sizes[i]-num) & 1
    safe = [all(mask & e != e for e in forb) for mask in range(1 << n)]
    @lru_cache(None)
    def g(mask):
        return mex(g(mask | (1 << j)) for j in range(n) if not mask & (1 << j) and safe[mask | (1 << j)])
    @lru_cache(None)
    def F(A):
        return mex(((sizes[i]-1)&1) ^ F(A | (1 << i))
                   for i in range(k) if not A & (1 << i)
                   and all(((A | (1 << i)) & e) != e for e in base_edges))
    cnt = 0
    for mask in range(1 << n):
        if not safe[mask]:
            continue
        A = active[mask]
        expected = free_parity[mask] ^ F(A)
        actual = g(mask)
        if actual != expected:
            raise AssertionError((k,sizes,base_edges,mask,A,expected,actual))
        if F(A) > k-A.bit_count():
            raise AssertionError('bound')
        cnt += 1
    # terminal configurations: whole groups for maximal independent group sets
    terminals = [mask for mask in range(1 << n) if safe[mask] and
                 not any(not mask & (1 << j) and safe[mask | (1 << j)] for j in range(n))]
    base_maximal = [A for A in range(1 << k) if all((A & e) != e for e in base_edges) and
                    all(any(((A | (1 << i)) & e) == e for e in base_edges)
                        for i in range(k) if not A & (1 << i))]
    expected_terminals = [sum(1 << j for i in range(k) if A & (1 << i) for j in parts[i]) for A in base_maximal]
    assert sorted(terminals) == sorted(expected_terminals)
    return cnt, g(0), len(terminals)


def main():
    cases=states=terminals=0
    root_values=Counter()
    for k in (2,3,4):
        eligible = [e for e in range(1, 1 << k) if e.bit_count()>=2]
        sizes_options = (1,2,3) if k<=3 else (1,2)
        for sizes in product(sizes_options, repeat=k):
            for flags in range(1 << len(eligible)):
                edges = tuple(eligible[j] for j in range(len(eligible)) if flags & (1 << j))
                c,g0,t=check_case(k,sizes,edges)
                cases+=1; states+=c; terminals+=t; root_values[g0]+=1
    # A deterministic nonuniform k=5 sample, independently generated.
    import random
    rng=random.Random(20261019)
    for _ in range(400):
        k=5
        sizes=tuple(rng.randint(1,2) for _ in range(k))
        eligible=[e for e in range(1,1<<k) if e.bit_count()>=2]
        edges=tuple(e for e in eligible if rng.randrange(5)==0)
        c,g0,t=check_case(k,sizes,edges)
        cases+=1;states+=c;terminals+=t;root_values[g0]+=1
    result={'cases':cases,'safe_labelled_states':states,'terminal_sets_checked':terminals,
            'root_grundy_histogram':dict(sorted(root_values.items())),
            'status':'all exact labelled subsets matched recurrence and maximal-group classification'}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result

if __name__=='__main__':
    main()
