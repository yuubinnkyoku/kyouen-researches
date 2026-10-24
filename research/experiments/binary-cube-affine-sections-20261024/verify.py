"""Independent exact rational-rowspace audit of maximal Boolean cube sections."""
from fractions import Fraction
from itertools import combinations


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
        if num == (1 << k):sat+=1
        elif num > (1 << k):raise AssertionError('affine section too large')
    expect = (1 << (d-k)) * stirling(d+1,k+1)
    print(f'd={d} k={k} distinct_flats={len(seen)} saturated={sat} formula={expect}', flush=True)
    assert sat == expect

if __name__ == '__main__':
    for d,k in [(2,1),(3,1),(3,2),(4,1),(4,2),(4,3),(5,1),(5,2),(5,3),(5,4)]:
        verify(d,k)
