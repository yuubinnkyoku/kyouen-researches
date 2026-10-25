#!/usr/bin/env python3
"""Aggregate exhaustive support counts into E(d,q) with exact integers.

Usage: python aggregate.py q3.txt q4.txt q5.txt
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


def main() -> None:
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
