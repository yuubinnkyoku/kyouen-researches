#!/usr/bin/env python3
"""Census for the z=13, y=3 two-token residual slice.

Raw double-recursion row extraction (order-preserving and descending
canonical engines must agree) for x=3..45, R=0..x+45, plus the general
tail claim R>=x+17 over the same range. Writes output/census.txt.
Deterministic: two runs are byte-identical.
"""
import sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)


def mex(values):
    values = set(values)
    m = 0
    while m in values:
        m += 1
    return m


@lru_cache(None)
def H_ordered(R, X, z):
    if R == 0:
        return 0
    opts = set()
    for i, v in enumerate(X):
        if v > 1:
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1:], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1:], z + 1))
    if z >= 1:
        opts.add(1 ^ H_ordered(R - 1, X, z - 1))
    return mex(opts)


@lru_cache(None)
def H_canonical(R, X, z):
    X = tuple(sorted(X))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            opts.add(H_canonical(R - 1, tuple(sorted(X[:i] + (v - 1,) + X[i + 1:])), z))
        else:
            opts.add(H_canonical(R - 1, X[:i] + X[i + 1:], z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)


def compress(vals):
    if not vals:
        return "[]"
    parts = []
    s = p = vals[0]
    for v in vals[1:]:
        if v == p + 1:
            p = v
        else:
            parts.append(str(s) if s == p else f"{s}-{p}")
            s = p = v
    parts.append(str(s) if s == p else f"{s}-{p}")
    return "[" + ",".join(parts) + "]"


def main():
    lines = ["z=13, y=3 two-token residual census (x=3..45, R=0..x+45)"]
    for x in range(3, 46):
        Rmax = x + 45
        t, p = [], []
        for R in range(0, Rmax + 1):
            a = H_ordered(R, (x, 3), 13)
            b = H_canonical(R, (x, 3), 13)
            assert a == b, (x, R, a, b)
            if a == 2:
                t.append(R)
            elif a == 1:
                p.append(R)
        # general tail: R >= x+17 -> (x+3) mod 2 (checked where covered)
        for R in range(x + 17, Rmax + 1):
            a = H_ordered(R, (x, 3), 13)
            assert a == (x + 3) % 2, ("tail", x, R, a)
        lines.append(f"x={x:2d} T={compress(t)}")
        lines.append(f"      P={compress(p)}")
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "census.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("census written")


if __name__ == "__main__":
    main()
