#!/usr/bin/env python3
"""Census of the raw y=19 parametric family rows, all z.

For each z in [0, ZHI), x in [XMIN, XMAX), compute the full row of the
two-token residual game H(R;(x,19);z) for R in [0, x+z+RBUF] with the raw
order-preserving recursion and extract, per row:
  - the Thue-Morse index: the R converting each row to the 3-periodic
    odd/even tail ((x+19) mod 2 -> 0/1), with value-2 rows counted as
    still pending;
  - the value-2 support (T set) and value-1 support (P set), as the
    explicit list of R values.
Tail assertion: R >= x+z+20 => value == (x+19) mod 2 on every row.
Output: output/census.txt (one line per (z,x), deterministic).
Mirrors the published y=5/y=6/y=7/y=8/y=9/y=10/y=12/y=13/y=14/y=15/y=16/y=17/y=18
census_rows.py
(K1126/K1127/K1131/K1135/K1138/K1141/K1152/K1231/K1233/K1236/K1239/K1241/K1242
experiments).

Host adaptation (the y=15..y=18 runs used ~1.0 GiB cgroups and this y=19
host is similarly constrained; an unbounded z=40..79 scan OOMs here):
the memo table of the raw recursion is bounded (LRU, CENSUS_CACHE_MAXSIZE).
Memoization of a deterministic pure function is transparent and LRU eviction
is deterministic under the fixed visit order, so the row values are identical
to the unbounded recursion of the published
y=5..y=10/y=12/y=13/y=14/y=15/y=16/y=17/y=18 versions; only residency is bounded. cache_info (misses/currsize) is printed
so the state count is still recorded (misses = distinct-state computations
under this order).
"""
import sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)
ZHI = 80
XMIN = 19
XMAX = 70
RBUF = 21
CENSUS_CACHE_MAXSIZE = 1_600_000


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


@lru_cache(CENSUS_CACHE_MAXSIZE)
def H(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H(R - 1, X, z - 1))
    return mex(opts)


def row(z, x):
    values = [H(0, (x, 18), z)]
    for R in range(1, x + z + RBUF + 1):
        values.append(H(R, (x, 19), z))
    return values


def describe(z, x, values):
    tail = (x + 19) % 2
    tset = [R for R, g in enumerate(values) if g == 2]
    pset = [R for R, g in enumerate(values) if g == 1]
    hi = len(values) - 1
    idx = None
    for R0 in range(hi, -1, -1):
        ok = all(values[R] == (tail if (R - R0) % 2 == 0 else 1 - tail)
                 for R in range(R0, hi + 1))
        if ok:
            idx = R0
        elif idx is not None:
            break
    return idx, tset, pset


def main():
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    lines = []
    n = 0
    zeros = 0
    for z in range(ZHI):
        for x in range(XMIN, XMAX + 1):
            values = row(z, x)
            n += len(values)
            zeros += sum(1 for g in values if g == 0)
            idx, tset, pset = describe(z, x, values)
            tail = (x + 19) % 2
            for R in range(x + z + 20, len(values)):
                assert values[R] == tail, ("tail", z, x, R, values[R])
            lines.append(f"z={z} x={x} idx={idx} tail={tail} "
                         f"T={{{','.join(map(str, tset))}}} "
                         f"P={{{','.join(map(str, pset))}}}")
        lines.append("")
    (out / "census.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    ci = H.cache_info()
    print(f"rows={ZHI * (XMAX - XMIN + 1)} points={n} zero_points={zeros}")
    print("states(misses):", ci.misses, "currsize:", ci.currsize,
          "maxsize:", ci.maxsize, "hits:", ci.hits)
    return 0


if __name__ == "__main__":
    sys.exit(main())
