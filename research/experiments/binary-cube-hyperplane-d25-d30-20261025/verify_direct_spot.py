"""Independent integer Bareiss checks on 100 fixed maximal minors per dimension.
This is a spot check; exhaustive proof is verify_gale_mod.cpp.
"""
from pathlib import Path
from random import Random
import sys

def determinant(a):
    a = [row[:] for row in a]
    n = len(a)
    sign, prev = 1, 1
    for k in range(n - 1):
        t = next((i for i in range(k, n) if a[i][k]), None)
        if t is None:
            return 0
        if t != k:
            a[t], a[k] = a[k], a[t]
            sign = -sign
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                numerator = a[i][j] * pivot - a[i][k] * a[k][j]
                assert numerator % prev == 0
                a[i][j] = numerator // prev
            a[i][k] = 0
        prev = pivot
    return sign * a[-1][-1]

def main(path):
    for line in Path(path).read_text().splitlines():
        if not line.strip() or line.startswith('#'):
            continue
        d, *points = map(int, line.split())
        n = len(points)
        assert n == d + 7
        rng = Random(20261025 + d)
        omitted = {tuple(range(6)), tuple(range(n - 6, n))}
        while len(omitted) < 100:
            omitted.add(tuple(sorted(rng.sample(range(n), 6))))
        m = [[1] + [(x >> j) & 1 for j in range(d)] for x in points]
        for indices in sorted(omitted):
            excluded = set(indices)
            a = [row for i, row in enumerate(m) if i not in excluded]
            assert determinant(a) != 0, (d, indices)
        print(f'd={d} direct integer minors=100 PASS')

if __name__ == '__main__':
    main(sys.argv[1])
