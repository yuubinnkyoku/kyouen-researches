"""Independent exact-integer witness audit for F(33)<=743."""
from math import gcd, isqrt
from functools import reduce

N = 143650
W = 743
expected = [-379, -377, -375, -363, -351, -333, -325, -305, -269,
            -267, -225, -195, -181, -143, -109, -55, -39, -3, 3,
            39, 55, 109, 143, 181, 195, 225, 267, 269, 305,
            325, 333, 351, 363]
rows = []
for y in range(-isqrt(N), isqrt(N) + 1):
    x2 = N - y*y
    x = isqrt(x2)
    if x > 0 and x*x == x2:
        assert x*x + y*y == N and (-x)**2 + y*y == N
        rows.append(y)
chosen = [y for y in rows if -379 <= y <= 363]
assert chosen == expected, (chosen, expected)
assert len(chosen) == 33
assert chosen[-1] - chosen[0] + 1 == W
assert reduce(gcd, (y - chosen[0] for y in chosen)) == 2
print(f'PASS N={N} total_double_hit_rows={len(rows)} selected=33 width={W} gcd=2')
print('selected_y=' + ','.join(map(str, chosen)))
