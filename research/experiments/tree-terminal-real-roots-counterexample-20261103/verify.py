#!/usr/bin/env python3
"""Independent exhaustive check of star terminal polynomial against the closed form."""
from itertools import combinations

def exhaustive(d, r):
    edges = [(0, i) for i in range(1, d + 1)]
    out = {}
    for bits in range(1 << (d + 1)):
        X = {i for i in range(d + 1) if bits >> i & 1}
        if any(not any((v not in X) for a, b in edges for v in ([b] if a == x else ([a] if b == x else []))) for x in X):
            continue
        remain = sum(a not in X and b not in X for a, b in edges)
        k = d - len(X) - remain
        out[k] = out.get(k, 0) + r ** remain
    return out

def main():
    count = 0
    for d in range(2, 11):
        for r in range(1, 8):
            expected = {0: (r + 1) ** d, d - 1: 1}
            assert exhaustive(d, r) == expected, (d, r)
            count += 1
    print(f"PASS: {count} complete star enumerations")

if __name__ == "__main__":
    main()
