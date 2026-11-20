#!/usr/bin/env python3
"""Census of the raw y=8 parametric family rows, all z.

For each z in [0, ZHI), x in [XMIN, XMAX], compute the full row of the
two-token residual game H(R;(x,8);z) for R in [0, x+z+RBUF] with the raw
order-preserving recursion and extract, per row:
  - the Thue-Morse index: the R converting each row to the 3-periodic
    odd/even tail ((x+8) mod 2 -> 0/1), with value-2 rows counted as
    still pending;
  - the value-2 support (T set) and value-1 support (P set), as the
    explicit list of R values.
Tail assertion: R >= x+z+9 => value == (x+8) % 2 on every row.
Output: output/census.txt (one line per (z,x), deterministic).
Mirrors the published y=5/y=6/y=7 census_rows.py
(K1126/K1127/K1131 experiments).
"""
import sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)
ZHI = 80
XMIN = 8
XMAX = 70
RBUF = 12


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


@lru_cache(None)
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
    values = [H(0, (x, 8), z)]
    for R in range(1, x + z + RBUF + 1):
        values.append(H(R, (x, 8), z))
    return values


def describe(z, x, values):
    tail = (x + 8) % 2
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
            tail = (x + 8) % 2
            for R in range(x + z + 9, len(values)):
                assert values[R] == tail, ("tail", z, x, R, values[R])
            lines.append(f"z={z} x={x} idx={idx} tail={tail} "
                         f"T={{{','.join(map(str, tset))}}} "
                         f"P={{{','.join(map(str, pset))}}}")
        lines.append("")
    (out / "census.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"rows={ZHI * (XMAX - XMIN + 1)} points={n} zero_points={zeros}")
    print("states:", H.cache_info().currsize)
    return 0


if __name__ == "__main__":
    sys.exit(main())
