#!/usr/bin/env python3
"""Independent LCA-charging audit for substitution-expression tree bounds."""
from collections import defaultdict
from functools import lru_cache
from itertools import combinations, product
from math import comb, prod
from random import Random


def compositions(n, h):
    if h == 1:
        yield (n,)
    else:
        for first in range(1, n-h+2):
            for rest in compositions(n-first, h-1):
                yield (first,) + rest


@lru_cache(None)
def shapes(n, max_arity=4):
    if n == 1:
        return (None,)
    out = []
    for h in range(2, min(max_arity, n)+1):
        for sizes in compositions(n, h):
            for children in product(*(shapes(s, max_arity) for s in sizes)):
                out.append(children)
    return tuple(out)


def audit(tree):
    next_leaf = [0]
    charged = defaultdict(set)
    counts = defaultdict(int)

    def visit(t):
        if t is None:
            idx = next_leaf[0]
            next_leaf[0] += 1
            return (idx,)
        children = [visit(x) for x in t]
        h = len(children)
        signatures = {tuple(sorted(v)) for v in product(*children)}
        assert len(signatures) == prod(len(c) for c in children)
        assert charged[h].isdisjoint(signatures), 'duplicate LCA charge'
        charged[h].update(signatures)
        counts[h] += len(signatures)
        return tuple(x for group in children for x in group)

    n = len(visit(tree))
    for h, count in counts.items():
        assert count == len(charged[h])
        assert count <= comb(n, h)
    assert sum((1 << h)*v for h,v in counts.items()) <= sum(
        (1 << h)*comb(n,h) for h in range(2,min(4,n)+1))


def random_tree(n, rng):
    if n == 1:
        return None
    h = rng.randint(2, min(n,4))
    cuts = sorted(rng.sample(range(1,n),h-1))
    sizes = [b-a for a,b in zip([0]+cuts,cuts+[n])]
    return tuple(random_tree(s,rng) for s in sizes)


def main():
    exact = 0
    for n in range(1,8):
        for tree in shapes(n):
            audit(tree)
            exact += 1
    rng = Random(20261102)
    random_cases = 0
    for n in (8,10,12,16,20,30):
        for _ in range(100):
            audit(random_tree(n,rng))
            random_cases += 1
    print(f'PASS {exact} exhaustive ordered trees n<=7; '
          f'{random_cases} random trees n<=30; zero LCA collisions')


if __name__ == '__main__':
    main()
