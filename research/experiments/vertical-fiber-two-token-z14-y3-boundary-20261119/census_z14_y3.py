#!/usr/bin/env python3
"""Census for the z=14, y=3 two-token residual slice.

Raw double-recursion row extraction (order-preserving and descending
canonical engines must agree) for x=3..45, R=0..x+45, with every extracted
row compared against the candidate closed form (third derivation of the
row table), plus the general tail claim R>=x+18 over the same range.
Writes output/census.txt. Deterministic: two runs are byte-identical.
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
    X = tuple(sorted(X, reverse=True))
    if R == 0:
        return 0
    opts = set()
    i = 0
    while i < len(X):
        v = X[i]
        if v > 1:
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1:], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        j = i
        while j + 1 < len(X) and X[j + 1] == v:
            j += 1
        i = j + 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)


# Candidate closed form (transcription of the z=14, y=3 theorem statement).
def candidate_T(x, r):
    if x == 3:
        return r in (1, 3, 5)
    if x in (4, 5):
        return r in (1, 3, 5, 7)
    if x in (6, 7):
        return r in (1, 3, 5, 7, 9)
    if x in (8, 9):
        return r in (1, 3, 5, 7, 9, 11)
    if x == 10:
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x == 11:
        return r in (1, 3, 5, 7, 9, 11, 13, 15, 17)
    if x in (12, 13, 14, 16, 17):
        return r in (1, 3, 5, 7, 9, 11, 13)
    if x == 15:
        return r in (1, 3, 5, 7, 9, 11, 13) or r == 19
    if x == 18:
        return (r in (1, 3, 5, 7, 9, 11, 13)
                or (21 <= r <= 35 and r % 2 == 1))
    return r in (1, 3, 5, 7, 9, 11, 13) or r == 21


def candidate_P(x, r):
    if x % 2 == 1 and x <= 11:
        return False
    if x % 2 == 0 and x <= 10:
        return r >= x + 4
    if x == 12:
        return r == 15 or r >= 17
    if x in (13, 15):
        return r in (15, 17)
    if x in (14, 16):
        return r in (15, 17) or r >= 19
    if x == 17:
        return r in (15, 17, 19)
    if x == 18:
        return (r in (15, 17, 19)
                or (r % 2 == 0 and 22 <= r <= 34)
                or r >= 36)
    if x % 2 == 1:
        return (r in (15, 17, 19)
                or (r % 2 == 0 and 22 <= r <= x + 17))
    return (r in (15, 17, 19)
            or (r % 2 == 0 and 22 <= r <= x + 18)
            or r >= x + 19)


def candidate(x, R):
    if R == 0:
        return 0
    if candidate_T(x, R):
        return 2
    return 1 if candidate_P(x, R) else 0


def rle(nums):
    out = []
    for n in nums:
        if out and out[-1][1] == n - 1:
            out[-1][1] = n
        else:
            out.append([n, n])
    parts = []
    for a, b in out:
        if a == b:
            parts.append(str(a))
        else:
            parts.append(f"{a}-{b}")
    return ",".join(parts)


def main():
    lines = ["z=14, y=3 two-token residual census (x=3..45, R=0..x+45)"]
    bad = 0
    formula_bad = 0
    for x in range(3, 46):
        T = []
        P = []
        for R in range(0, x + 46):
            a = H_ordered(R, (x, 3), 14)
            b = H_canonical(R, (x, 3), 14)
            if a != b:
                bad += 1
                if bad <= 20:
                    lines.append(f"ENGINE MISS x={x} R={R} ordered={a} "
                                 f"canonical={b}")
            if a != candidate(x, R):
                formula_bad += 1
                if formula_bad <= 20:
                    lines.append(f"FORMULA MISS x={x} R={R} raw={a} "
                                 f"formula={candidate(x, R)}")
            if a == 2:
                T.append(R)
            elif a == 1:
                P.append(R)
        lines.append(f"x={x:2d} T=[{rle(T)}]")
        lines.append(f"       P=[{rle(P)}]")
    lines.append(f"engine mismatches: {bad}")
    lines.append(f"formula mismatches (raw vs closed form): {formula_bad}")
    tailbad = 0
    for x in range(3, 46):
        for off in range(4):
            R = x + 18 + off
            v = H_ordered(R, (x, 3), 14)
            if v != (x + 3) % 2:
                tailbad += 1
                lines.append(f"TAIL MISS x={x} R={R} v={v}")
    lines.append(f"tail mismatches (R>=x+18 vs (x+3)%2): {tailbad}")
    payload = "\n".join(lines) + "\n"
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "census.txt").write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if bad == 0 and formula_bad == 0 and tailbad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
