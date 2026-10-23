#!/usr/bin/env python3
"""Independent 4x4 permutation determinants; no shared pair-sum classifier."""
from itertools import combinations, permutations
from math import comb

PERMS = [(p, (-1) ** sum(p[i] > p[j] for i in range(4)
                          for j in range(i + 1, 4)))
         for p in permutations(range(4))]

def determinant(rows):
    return sum(sign * rows[0][p[0]] * rows[1][p[1]]
               * rows[2][p[2]] * rows[3][p[3]]
               for p, sign in PERMS)

def actual(points):
    a = determinant([(x*x, x, y, 1) for x, y in points])
    b = determinant([(y*y, x, y, 1) for x, y in points])
    return a == b == 0

def predicted(points):
    rows = {}
    for x, y in points:
        rows.setdefault(y, []).append(x)
    if len(rows) == 1:
        return True
    if len(rows) != 2 or sorted(map(len, rows.values())) != [2, 2]:
        return False
    a, b = rows.values()
    return sum(a) == sum(b)

def witness_ok(m=14):
    rows = [{1, 8}, {3, 5, 7}, {5, 6, 8}]
    chosen = [(x, y) for y, xs in enumerate(rows) for x in xs]
    assert len(chosen) == 8
    for four in combinations(chosen, 4):
        assert not actual(four), four
    for y in range(3):
        for x in range(m):
            if x in rows[y]:
                continue
            assert any(actual(four) for four in
                       combinations(chosen + [(x, y)], 4)), (x, y)
    return True

def main():
    for m in [3, 4, 5, 6, 7, 8, 14, 15]:
        points = [(x, y) for x in range(m) for y in range(3)]
        count = 0
        for four in combinations(points, 4):
            value = actual(four)
            assert value == predicted(four), (m, four, value)
            count += value
        pair_square_sum = sum(
            sum(a+b == s for a, b in combinations(range(m), 2)) ** 2
            for s in range(1, 2*m-2)
        )
        expected = 3*comb(m, 4) + 3*pair_square_sum
        assert count == expected, (m, count, expected)
        print(f"m={m}: checked={comb(3*m,4)} universal_forbidden={count}")
    assert witness_ok()
    print("m=14: independent determinant witness safe and maximal PASS")

if __name__ == "__main__":
    main()
