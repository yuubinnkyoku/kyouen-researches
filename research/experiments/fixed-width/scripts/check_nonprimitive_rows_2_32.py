#!/usr/bin/env python3
"""Independent exact integer-square-root witness check for nonprimitive F(k)."""
from math import gcd, isqrt

# Explicit norms N; the witness circle is x^2 + y^2 = N before translation.
FAMILIES = [
    (2, {2: 3}),
    (10, {3: 5, 4: 7}),
    (50, {5: 13, 6: 15}),
    (130, {7: 21, 8: 23}),
    (650, {10: 45, 11: 49, 12: 51}),
    (2210, {13: 85, 14: 87, 15: 91, 16: 95}),
    (11050, {17: 165, 18: 173, 19: 187, 20: 191,
             21: 199, 22: 201, 23: 209, 24: 211}),
    (55250, {25: 421, 26: 427, 27: 441, 28: 451,
             29: 463, 30: 465, 31: 469, 32: 471}),
]

def rows_for_norm(N):
    rows = []
    for y in range(-isqrt(N), isqrt(N) + 1):
        x = isqrt(N-y*y)
        if x > 0 and x*x + y*y == N:
            assert x*x+y*y == N and (-x)*(-x)+y*y == N
            rows.append(y)
    return rows

def main():
    checked = []
    for N, values in FAMILIES:
        rows = rows_for_norm(N)
        for k, expected in values.items():
            best = min((rows[i+k-1]-rows[i]+1, rows[i:i+k])
                       for i in range(len(rows)-k+1))
            width, subset = best
            assert width == expected, (k, width, expected)
            delta_gcd = 0
            for y in subset:
                delta_gcd = gcd(delta_gcd, y-subset[0])
            assert delta_gcd == 2, (k, delta_gcd)
            assert len(subset) == k and subset[-1]-subset[0] == width-1
            checked.append(k)
            print(f'WITNESS k={k} width={width} N={N} gcd={delta_gcd} first={subset[0]} last={subset[-1]}')
    assert sorted(checked) == [k for k in range(2,33) if k != 9]
    ys = rows_for_norm(650)
    k = 9
    width, subset = min((ys[i+k-1]-ys[i]+1, ys[i:i+k])
                        for i in range(len(ys)-k+1))
    assert width == 43
    delta_gcd = 0
    for y in subset:
        delta_gcd = gcd(delta_gcd, y-subset[0])
    assert delta_gcd == 2
    print(f'BOUND k=9 upper={width} N=650 gcd={delta_gcd}')
    print('PASS 30 exact witnesses and the F(9)<=43 witness')

if __name__ == '__main__':
    main()
