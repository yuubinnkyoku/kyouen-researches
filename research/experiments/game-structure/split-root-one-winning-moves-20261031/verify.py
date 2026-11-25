#!/usr/bin/env python3
"""Independent named-vertex Node Kayles audit of the root-g=1 move criterion."""
from functools import lru_cache
from itertools import product
from random import Random


def verify(k, masks):
    m = len(masks)
    n = k + m
    closed = [1 << v for v in range(n)]
    for a in range(k):
        for b in range(a + 1, k):
            closed[a] |= 1 << b
            closed[b] |= 1 << a
    for j, signature in enumerate(masks):
        for a in range(k):
            if signature >> a & 1:
                closed[a] |= 1 << (k + j)
                closed[k + j] |= 1 << a

    @lru_cache(None)
    def grundy(state):
        if not state:
            return 0
        child_values = 0
        todo = state
        while todo:
            v = (todo & -todo).bit_length() - 1
            todo &= todo - 1
            child_values |= 1 << grundy(state & ~closed[v])
        answer = 0
        while child_values >> answer & 1:
            answer += 1
        return answer

    full = (1 << n) - 1
    actual = grundy(full)
    degrees = [sum((signature >> a) & 1 for signature in masks) for a in range(k)]
    parities = {d % 2 for d in degrees}
    universal = any(signature == (1 << k) - 1 for signature in masks)
    low = k == 0 or (len(parities) == 1 and (1 in parities or not universal))
    if low:
        expected = (m & 1) if k == 0 else (1 ^ (m & 1) ^ next(iter(parities)))
        assert actual == expected, (k, masks, actual, expected)
    elif k > 0:
        assert actual >= 2, (k, masks, actual)

    if actual == 1:
        if k == 0:
            predicted = set(range(m))
        else:
            degree_parity = next(iter(parities))
            predicted = set(range(k))
            for j, signature in enumerate(masks):
                if degree_parity == 1 or not any(
                    (signature | other) == (1 << k) - 1
                    for h, other in enumerate(masks) if h != j
                ):
                    predicted.add(k + j)
        observed = {
            v for v in range(n)
            if grundy(full & ~closed[v]) == 0
        }
        assert observed == predicted, (k, masks, observed, predicted)
    return actual == 1


def main():
    total = root_one = 0
    for k in range(1, 5):
        for m in range(5):
            for masks in product(range(1 << k), repeat=m):
                root_one += verify(k, masks)
                total += 1
    for m in range(4):
        for masks in product(range(1 << 5), repeat=m):
            root_one += verify(5, masks)
            total += 1

    rng = Random(20261031)
    for _ in range(5000):
        k = rng.randint(1, 9)
        m = rng.randint(0, 14)
        masks = [rng.randrange(1 << k) for _ in range(m)]
        root_one += verify(k, masks)
        total += 1

    assert total == 113783, total
    assert root_one == 5538, root_one
    print(f"checked={total} root_one={root_one} mismatches=0")


if __name__ == "__main__":
    main()
