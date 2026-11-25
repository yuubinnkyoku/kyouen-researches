"""Independent midpoint-pair audit of the 4-cube coplanar-q4 game.

No imports from the original verifier. The midpoint construction is compared
against an independent integer affine-rank test for *every* 4-subset.
"""
from collections import Counter
from itertools import combinations

P = [tuple((i >> k) & 1 for k in range(4)) for i in range(16)]
pairs = {}
for a, b in combinations(range(16), 2):
    midpoint_twice = tuple(P[a][k] + P[b][k] for k in range(4))
    pairs.setdefault(midpoint_twice, []).append((a, b))
forbidden = set()
for group in pairs.values():
    for x, y in combinations(group, 2):
        if len(set(x + y)) == 4:
            forbidden.add(sum(1 << i for i in x + y))

def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))

def affine_coplanar(q):
    v = [[P[i][k] - P[q[0]][k] for k in range(4)] for i in q[1:]]
    return all(det3(*[[row[k] for k in cols] for row in v]) == 0
               for cols in combinations(range(4), 3))

determinant_forbidden = {
    sum(1 << i for i in q)
    for q in combinations(range(16), 4) if affine_coplanar(q)
}
assert forbidden == determinant_forbidden
assert len(forbidden) == 100

safe = [False] * (1 << 16)
safe[0] = True
for mask in range(1, 1 << 16):
    safe[mask] = (safe[mask & (mask - 1)]
                  and not any(mask & f == f for f in forbidden))

grundy = [0] * (1 << 16)
misere_win = [False] * (1 << 16)
layers, maximal, misere_layers = Counter(), Counter(), Counter()
for mask in range((1 << 16) - 1, -1, -1):
    if not safe[mask]:
        continue
    children = [mask | (1 << i) for i in range(16)
                if not (mask >> i) & 1 and safe[mask | (1 << i)]]
    if not children:
        maximal[mask.bit_count()] += 1
    child_values = {grundy[c] for c in children}
    g = 0
    while g in child_values:
        g += 1
    grundy[mask] = g
    misere_win[mask] = not children or any(not misere_win[c] for c in children)
    layers[mask.bit_count()] += 1
    misere_layers[(mask.bit_count(), misere_win[mask])] += 1

assert sum(layers.values()) == 8193
assert dict(layers) == {0: 1, 1: 16, 2: 120, 3: 560,
                        4: 1720, 5: 3168, 6: 2368, 7: 240}
assert dict(maximal) == {6: 1008, 7: 240}
assert grundy[0] == 0 and not misere_win[0]
assert all(grundy[1 << i] == 1 and misere_win[1 << i]
           for i in range(16))
print("independent midpoint/determinant forbidden-set equality: PASS")
print("forbidden", len(forbidden), "safe", sum(layers.values()))
print("layers", sorted(layers.items()))
print("maximal", sorted(maximal.items()))
print("root grundy", grundy[0], "misere winning", misere_win[0])
print("misere layer outcomes", sorted(misere_layers.items()))
