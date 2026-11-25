#!/usr/bin/env python3
"""Census for the z=17, y=2 two-token residual slice.

Raw double-recursion row extraction (order-preserving and descending
canonical engines must agree) for x=2..45, R=0..x+45, compared row by
row against the closed form, plus the general tail claim R>=x+20 over
the same range. Writes output/census.txt.
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
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)


# ---- engine-independent closed form (candidate transcription) ----
def q_odd(k):
    return k if k % 2 else k - 1


def single_token(x, z, R):
    if R == 0 or x <= 0:
        return 0
    if z == 0:
        return min(R, x) % 2
    if z == x:
        if R % 2 and R <= 2 * x - 1:
            return 2
        if R % 2 == 0 and R <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        m = q_odd(z)
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < x + z:
            return (R + z) % 2
        return x % 2
    if z >= x + 1:
        m = q_odd(x)
        if R <= m:
            return 2 if R % 2 else 0
        return x % 2
    raise ValueError((x, z, R))


def candidate_T(x, r):
    """Derived theorem candidate: z=17, y=2."""
    if x == 2:
        return r in (1, 3)
    if x in (3, 4):
        return 1 <= r <= 5 and r % 2 == 1
    if x in (5, 6):
        return 1 <= r <= 7 and r % 2 == 1
    if x in (7, 8):
        return 1 <= r <= 9 and r % 2 == 1
    if x in (9, 10):
        return 1 <= r <= 11 and r % 2 == 1
    if x in (11, 12):
        return 1 <= r <= 13 and r % 2 == 1
    if x in (13, 14):
        return 1 <= r <= 15 and r % 2 == 1
    if x == 15:
        return 1 <= r <= 19 and r % 2 == 1
    if x == 19:
        return (1 <= r <= 17 and r % 2 == 1) or r == 21
    if x == 20:
        return (r % 2 == 1 and (1 <= r <= 17 or 21 <= r <= 39))
    if x >= 21:
        return (1 <= r <= 17 and r % 2 == 1) or r == 21
    return 1 <= r <= 17 and r % 2 == 1


def candidate_P(x, r):
    if x % 2 == 0 and x <= 14:
        return False
    if x % 2 == 1 and x <= 13:
        return r >= x + 3
    if x == 15:
        return r in (18, 20) or r >= 21
    if x == 16:
        return r == 18
    if x == 17:
        return r in (18, 20) or r >= 21
    if x == 18:
        return r in (18, 20)
    if x == 19:
        return r in (18, 20) or r >= 22
    if x == 20:
        return r in (18, 20)
    if x % 2 == 1:
        return (r in (18, 20)
                or (r % 2 == 1 and 23 <= r <= x + 20)
                or r >= x + 21)
    return r in (18, 20) or (r % 2 == 1 and 23 <= r <= x + 19)


def candidate(x, R):
    assert not (candidate_T(x, R) and candidate_P(x, R)), (x, R)
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
    lines = ["z=17, y=2 two-token residual census (x=2..45, R=0..x+45)"]
    bad = 0
    formula_bad = 0
    for x in range(2, 46):
        T = []
        P = []
        for R in range(0, x + 46):
            a = H_ordered(R, (x, 2), 17)
            b = H_canonical(R, (x, 2), 17)
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
    for x in range(2, 46):
        for off in range(4):
            R = x + 20 + off
            v = H_ordered(R, (x, 2), 17)
            if v != (x + 2) % 2:
                tailbad += 1
                lines.append(f"TAIL MISS x={x} R={R} v={v}")
    lines.append(f"tail mismatches (R>=x+20 vs (x+2)%2): {tailbad}")
    payload = "\n".join(lines) + "\n"
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "census.txt").write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if bad == 0 and formula_bad == 0 and tailbad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
