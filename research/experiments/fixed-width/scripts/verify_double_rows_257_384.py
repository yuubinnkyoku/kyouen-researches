#!/usr/bin/env python3
"""Independent verifier: enumerate integer points by horizontal x, not Gaussian products."""
import csv
from math import isqrt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NORMS = (6319594450, 25764500450)


def enumerate_v_by_x(n):
    """Enumerate every v with u != 0, u^2+v^2=n, by integer square roots."""
    out = set()
    for u in range(1, isqrt(n) + 1):
        rem = n - u * u
        v = isqrt(rem)
        if v * v == rem:
            out.add(v)
            out.add(-v)
    return sorted(v for v in out if v % 2 == 1)


def verify():
    by_norm = {n: enumerate_v_by_x(n) for n in NORMS}
    assert [len(by_norm[n]) for n in NORMS] == [288, 384]
    csv_path = ROOT / 'output' / 'double_rows_257_384.csv'
    with csv_path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    assert len(rows) == 128
    for idx, rec in enumerate(rows):
        k, w, n, b, c, d, lo, hi = [int(rec[key]) for key in
                                  ('k', 'width', 'norm', 'B', 'C', 'D', 'first_v', 'last_v')]
        assert k == idx + 257 and n in by_norm and b == 1
        assert n == b * b + c * c - 4 * d and c == lo
        assert hi - lo == 2 * (w - 1)
        # Independent x-coordinate enumeration for the two fixed norms.
        vals = by_norm[n]
        assert sum(lo <= v <= hi for v in vals) >= k
        # Direct discriminant and integer substitution in every row of the witness.
        hits = 0
        for y in range(w):
            delta = b * b - 4 * (y * y + c * y + d)
            if delta <= 0:
                continue
            root = isqrt(delta)
            if root * root != delta or (b + root) % 2:
                continue
            x1, x2 = (-b - root) // 2, (-b + root) // 2
            assert x1 != x2
            assert x1*x1 + y*y + b*x1 + c*y + d == 0
            assert x2*x2 + y*y + b*x2 + c*y + d == 0
            hits += 1
        assert hits >= k, (k, w, hits)
        # For the two chosen norms, independently verify no shorter interval works.
        shortest = min((vs[j+k-1]-vs[j])//2+1
                       for vs in by_norm.values() if len(vs) >= k
                       for j in range(len(vs)-k+1))
        assert shortest == w, (k, w, shortest)
    print('PASS: 128/128 witnesses; 288+384 independent x-enumerated row ordinates')
    print('PASS: direct integer-square-root and substitution on every witness row')
    print('PASS: minimal widths among the two explicitly chosen norms (not global)')


if __name__ == '__main__':
    verify()
