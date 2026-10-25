#!/usr/bin/env python3
"""Aggregate exhaustive support counts into E(d,q) with exact integers.

Usage: python aggregate.py q3.txt q4.txt q5.txt\n       python aggregate.py --q5-tail
"""
import math
import re
import sys


def surjections(d: int, k: int) -> int:
    return sum((-1)**j * math.comb(k, j) * (k-j)**d
               for j in range(k+1))


def read_counts(path: str):
    counts = {}
    q_seen = set()
    with open(path, encoding="utf-8") as stream:
        for line in stream:
            m = re.fullmatch(r"q=(\d+) k=(\d+) good_supports=(\d+)\s*", line)
            if m is None:
                raise ValueError(f"unexpected line: {line!r}")
            q, k, value = map(int, m.groups())
            q_seen.add(q)
            counts[k] = value
    assert len(q_seen) == 1
    q = q_seen.pop()
    assert set(counts) == set(range(max(counts)+1))
    return q, counts


def count_sections(d: int, q: int, counts: dict[int, int]) -> int:
    assert d <= max(counts), "support sizes up to d are needed"
    numerator = sum(counts[k]*surjections(d, k) for k in range(d+1))
    assert numerator % math.factorial(q) == 0
    return numerator // math.factorial(q)



def verify_q5_tail() -> None:
    """Exact 40-container intersection audit for five binary-cube rows."""
    from collections import Counter
    from itertools import combinations

    def allowed_mask(weights):
        return sum(1 << v for v in range(32)
                   if sum(weights[i] * ((v >> i) & 1)
                          for i in range(5)) in (0, 1))

    large = []
    for plus in combinations(range(5), 2):
        for minus in range(5):
            if minus in plus:
                continue
            w = [0] * 5
            w[plus[0]] = w[plus[1]] = 1
            w[minus] = -1
            large.append(allowed_mask(w))
    medium = []
    for minus in combinations(range(5), 2):
        w = [1] * 5
        for i in minus:
            w[i] = -1
        medium.append(allowed_mask(w))

    assert len(large) == len(set(large)) == 30
    assert len(medium) == len(set(medium)) == 10
    assert not set(large) & set(medium)
    assert {s.bit_count() for s in large} == {24}
    assert {s.bit_count() for s in medium} == {20}
    ll = Counter((a & b).bit_count() for a, b in combinations(large, 2))
    lm = Counter((a & b).bit_count() for a in large for b in medium)
    mm = Counter((a & b).bit_count() for a, b in combinations(medium, 2))
    assert ll == {20: 150, 18: 135, 16: 150}, ll
    assert lm == {18: 90, 14: 210}, lm
    assert mm == {12: 45}, mm
    containers = large + medium
    triples = Counter((a & b & c).bit_count()
                      for a, b, c in combinations(containers, 3)
                      if (a & b & c).bit_count() >= 17)
    assert triples == {18: 90}, triples
    assert not any((a & b & c & d).bit_count() >= 17
                   for a, b, c, d in combinations(containers, 4))
    print("pairs large/large:", dict(sorted(ll.items())))
    print("pairs large/medium:", dict(sorted(lm.items())))
    print("pairs medium/medium:", dict(sorted(mm.items())))
    print("triples with intersection >=17:", dict(triples))
    for k in range(17, 33):
        choose = lambda n: math.comb(n, k) if k <= n else 0
        good = (choose(32) - 30 * choose(24)
                + 140 * choose(20) + 135 * choose(18))
        assert 0 <= good <= choose(32)
        print(f"q=5 k={k} good_supports={good}")


def main() -> None:
    if sys.argv[1:] == ['--q5-tail']:
        verify_q5_tail()
        return
    for path in sys.argv[1:]:
        q, counts = read_counts(path)
        print(f"q={q} support counts: {counts}")
        for d in range(q, min(max(counts), 8)+1):
            e = count_sections(d, q, counts)
            if q == 3:
                assert e == (8**d-3*6**d+3*4**d-2**d)//6
            if q == 4:
                assert e == (16**d-12*12**d+30*10**d-35*8**d
                             +27*6**d-16*4**d+5*2**d)//24
            print(f"  E_{{{d},{q}}}={e}")
        if q >= 3 and max(counts) >= 3*2**(q-2):
            s = 3*2**(q-2)
            assert counts[s] == math.comb(2**q,s)-3*math.comb(q,3)
            for k in range(s+1,max(counts)+1):
                assert counts[k] == math.comb(2**q,k)
            print("  sharp diversity boundary checked")


if __name__ == "__main__":
    main()
