"""Independent exact rational-rowspace audit of maximal Boolean cube sections."""
from fractions import Fraction
from itertools import combinations
from collections import Counter
from math import comb


def canonical(points, d):
    a = [[Fraction(int(j == 0 or bool(v & (1 << (j - 1))))) for j in range(d + 1)] for v in points]
    r = 0
    for col in range(d + 1):
        pivot = next((i for i in range(r, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        q = a[r][col]
        a[r] = [z / q for z in a[r]]
        for i in range(len(a)):
            if i != r and a[i][col]:
                q = a[i][col]
                a[i] = [x - q*y for x, y in zip(a[i], a[r])]
        r += 1
        if r == len(a):
            break
    return tuple(tuple(row) for row in a[:r])


def stirling(n, k):
    a = [0]*(k+1); a[0] = 1
    for _ in range(n):
        b = [0]*(k+1)
        for j in range(1, k+1):
            b[j] = a[j-1] + j*a[j]
        a = b
    return a[k]


def verify(d, k):
    seen = set()
    for pts in combinations(range(1 << d), k + 1):
        rows = canonical(pts, d)
        if len(rows) == k+1:
            seen.add(rows)
    sat = 0
    sizes = Counter()
    for rows in seen:
        num = 0
        for v in range(1 << d):
            b = [Fraction(1)] + [Fraction((v >> j)&1) for j in range(d)]
            # membership by exact RREF row reduction: reduce against leading 1s
            for row in rows:
                pivot = next(i for i, z in enumerate(row) if z)
                q = b[pivot]
                if q:
                    b = [x-q*y for x,y in zip(b,row)]
            if not any(b):num+=1
        sizes[num] += 1
        if num == (1 << k):sat+=1
        elif num > (1 << k):raise AssertionError('affine section too large')
    expect = (1 << (d-k)) * stirling(d+1,k+1)
    print(f'd={d} k={k} distinct_flats={len(seen)} saturated={sat} formula={expect}', flush=True)
    assert sat == expect
    if k >= 2:
        gap = 3 * (1 << (k - 2))
        assert all(t == (1 << k) or t <= gap for t in sizes)
        if d > k:
            assert sizes[gap] > 0
        for q in range(gap + 1, (1 << k) + 1):
            counted = sum(number * comb(t, q) for t, number in sizes.items() if t >= q)
            assert counted == expect * comb(1 << k, q)
        print(f'  intersection_sizes={dict(sorted(sizes.items()))}', flush=True)
    if (d, k) == (5, 3):
        assert sizes == {4: 3840, 5: 480, 6: 1200, 8: 260}
        terminal_five = sum(number * comb(t, 5) for t, number in sizes.items() if t >= 5)
        assert terminal_five == 22240
        print(f'  independent_five_stone_terminal_count={terminal_five}', flush=True)

if __name__ == '__main__':
    for d,k in [(2,1),(3,1),(3,2),(4,1),(4,2),(4,3),(5,1),(5,2),(5,3),(5,4)]:
        verify(d,k)
