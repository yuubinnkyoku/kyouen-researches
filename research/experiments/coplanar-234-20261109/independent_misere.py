"""Independent misere audit for the 2x3x4 coplanar-four prohibition game.

Run: python research/experiments/coplanar-234-20261109/independent_misere.py
No imports from the original experiment. Exact integer 3x3 determinant,
direct forbidden triples per candidate move, memoized game recursion.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations

points = [(x, y, z) for x in range(2) for y in range(3) for z in range(4)]


def subtract(a, b):
    return tuple(x - y for x, y in zip(a, b))


def determinant(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


forbidden = []
for ids in combinations(range(24), 4):
    a, b, c, d = (points[i] for i in ids)
    if determinant(subtract(b, a), subtract(c, a), subtract(d, a)) == 0:
        forbidden.append(sum(1 << i for i in ids))

triples = [[] for _ in points]
for quad in forbidden:
    for i in range(24):
        if quad & (1 << i):
            triples[i].append(quad ^ (1 << i))


@lru_cache(None)
def winning(mask):
    """Misere: terminal position is winning for player to move."""
    children = []
    for i in range(24):
        if mask & (1 << i):
            continue
        if any(mask & triple == triple for triple in triples[i]):
            continue
        children.append(winning(mask | (1 << i)))
    return not all(children) if children else True


if __name__ == "__main__":
    root = winning(0)
    first = Counter(winning(1 << i) for i in range(24))
    print("forbidden:", len(forbidden))
    print("safe states:", winning.cache_info().currsize)
    print("misere root winning:", root)
    print("misere first-child results:", dict(first))
    assert len(forbidden) == 2126
    assert winning.cache_info().currsize == 31529
    assert root is True
    assert first == {False: 24}
