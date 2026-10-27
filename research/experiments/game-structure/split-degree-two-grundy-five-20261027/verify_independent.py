"""Independent occupied/remaining-vertex recursion, not the clique-subset recurrence.

Usage:
  python3 verify_independent.py
  /tmp/split_census --dump-g4 > /tmp/g4.txt
  python3 verify_independent.py /tmp/g4.txt
"""
import functools
import random
import sys
from pathlib import Path

WITNESS = (1, 3, 3, 5, 5, 9, 9, 16, 48)
EXPECTED_CHILDREN = (0, 1, 1, 1, 1, 0, 2, 2, 2, 2, 2, 2, 2, 4, 3)


def direct(k, signatures):
    n = k + len(signatures)
    neighbors = [((1 << k)-1) ^ (1 << i) for i in range(k)]
    neighbors += [0] * len(signatures)
    for j, s in enumerate(signatures):
        v = k+j
        neighbors[v] = s
        for i in range(k):
            if s & (1 << i):
                neighbors[i] |= 1 << v
    closed = [neighbors[v] | (1 << v) for v in range(n)]

    @functools.lru_cache(None)
    def g(remaining):
        seen = set()
        todo = remaining
        while todo:
            bit = todo & -todo
            todo -= bit
            v = bit.bit_length()-1
            seen.add(g(remaining & ~closed[v]))
        value = 0
        while value in seen:
            value += 1
        return value

    all_vertices = (1 << n)-1
    return g(all_vertices), tuple(g(all_vertices & ~closed[v]) for v in range(n)), g.cache_info().currsize


def main():
    result, children, states = direct(6, WITNESS)
    assert result == 5 and children == EXPECTED_CHILDREN
    print('witness: vertices=15 edges=31 grundy=5 states=', states)
    print('witness children:', children)

    # Fixed-seed independent spot-checks for both boundary sizes.
    rng = random.Random(20261027)
    for n in (13,14):
        for _ in range(500):
            k = rng.randrange(5,n+1)
            m = n-k
            choices = [1<<i for i in range(k)] + [
                (1<<i)|(1<<j) for i in range(k) for j in range(i+1,k)]
            signatures = tuple(sorted(rng.choice(choices) for _ in range(m)))
            value, _, _ = direct(k, signatures)
            assert value <= 4, (n,k,signatures,value)
        print(f'n={n}: 500 independent direct-recursion samples have g<=4')

    if len(sys.argv) > 1:
        cases = Path(sys.argv[1]).read_text().splitlines()
        for line in cases:
            parts = line.split()
            assert parts[0] == 'g4'
            k,m = map(int,parts[1:3])
            signatures = tuple(map(int,parts[3:]))
            assert len(signatures) == m
            value, _, _ = direct(k, signatures)
            assert value == 4, (line,value)
        print('all census g=4 cases independently checked:',len(cases))

if __name__ == '__main__':
    main()
