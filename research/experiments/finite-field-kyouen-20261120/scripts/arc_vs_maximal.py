"""COMPARING ARC COUNTS WITH MAXIMAL-SAFE-SET COUNTS.

Two independent enumerations were run:

  (A) arc_counts.py   -- counts k-arcs on the elliptic quadric
  (B) min_maximal2.py -- counts MAXIMAL safe sets by size

At size K the two must agree: a K-arc is automatically maximal (it cannot
be extended, since K is the maximum), and a maximal safe set of size K is
a K-arc.  So

    #{K-arcs} = #{maximal safe sets of size K}.

This script checks that, and looks for a closed form for the K-arc count.
"""

from __future__ import annotations

from math import comb

# (q, K, #arcs at K, #maximal sets at K)
DATA = [
    (3, 5, 72, 72),
    (4, 5, 2040, 2040),
    (5, 6, 5200, 5200),
    (7, 6, 1254400, 1254400),
    (8, 7, 1048320, 1048320),
]

print("=== agreement at size K ===")
print(f"{'q':>3} {'K':>3} {'#arcs':>12} {'#maximal':>12} {'equal':>6}")
for q, K, a, m in DATA:
    print(f"{q:>3} {K:>3} {a:>12} {m:>12} {str(a == m):>6}")

print()
print("=== normalised counts ===")
print(f"{'q':>3} {'n':>5} {'K':>3} {'#arcs':>12} {'#arcs/n':>10} "
      f"{'#arcs/(n*K)':>12}")
for q, K, a, m in DATA:
    n = q * q + 1
    print(f"{q:>3} {n:>5} {K:>3} {a:>12} {a/n:>10.1f} {a/(n*K):>12.4f}")

print()
print("=== is #arcs = n * (something integral)? ===")
for q, K, a, m in DATA:
    n = q * q + 1
    print(f"q={q}: {a} / {n} = {a/n}  (integer: {a % n == 0})")

print()
print("=== the full arc-count series ===")
SERIES = {
    3: {0: 1, 1: 10, 2: 45, 3: 120, 4: 180, 5: 72},
    4: {0: 1, 1: 17, 2: 136, 3: 680, 4: 2040, 5: 2040},
    5: {0: 1, 1: 26, 2: 325, 3: 2600, 4: 13000, 5: 26000, 6: 5200},
    7: {0: 1, 1: 50, 2: 1225, 3: 19600, 4: 205800, 5: 1070160,
        6: 1254400},
    8: {0: 1, 1: 65, 2: 2080, 3: 43680, 4: 611520, 5: 4525248,
        6: 9434880, 7: 1048320},
}
for q in sorted(SERIES):
    n = q * q + 1
    row = SERIES[q]
    print(f"q={q} (n={n}):")
    for k in sorted(row):
        c = row[k]
        # compare with C(n,k)
        ratio = c / comb(n, k) if comb(n, k) else 0
        print(f"   k={k}: {c:>10}   C(n,k)={comb(n,k):>12}   "
              f"ratio={ratio:.6f}")
