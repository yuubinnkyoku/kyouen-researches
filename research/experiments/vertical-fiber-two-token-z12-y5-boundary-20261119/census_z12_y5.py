#!/usr/bin/env python3
"""Census for the z=12, y=5 two-token residual slice.

Raw double-recursion row extraction (order-preserving and descending
canonical engines must agree) for x=5..45, R=0..x+45, compared row by
row against the closed form, plus the general tail claim R>=x+18 over
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


# Candidate closed form (transcription of the z=12, y=5 theorem statement).
def candidate_T(x, r):
    if x == 5:
        return 1 <= r <= 9 and r % 2 == 1
    if x == 6:
        return 1 <= r <= 11 and r % 2 == 1
    if x == 7:
        return 1 <= r <= 17 and r % 2 == 1
    if not (1 <= r <= 11 and r % 2 == 1):
        if x == 11:
            return r == 19
        if x == 15:
            return r == 21
        if x == 18:
            return 23 <= r <= 35 and r % 2 == 1
        if x >= 19:
            return r == 23
        return False
    return True


def candidate_P(x, r):
    if x <= 17:
        base = {5: (), 6: (), 7: (), 8: (13, 15, 17), 9: (13, 15, 17),
                10: (13, 15, 17, 19), 11: (13, 15, 17),
                12: (13, 15, 17, 19), 13: (13, 15, 17, 19),
                14: (13, 15, 17, 19, 21), 15: (13, 15, 17, 19),
                16: (13, 15, 17, 19, 21), 17: (13, 15, 17, 19, 21)}[x]
        if r in base:
            return True
        pioneer = {6: 12, 8: 18, 10: 20, 12: 20, 14: 22, 16: 22}
        return x in pioneer and r >= pioneer[x]
    if r in (13, 15, 17, 19, 21):
        return True
    if x % 2 == 0:
        return (r % 2 == 0 and 24 <= r <= x + 18) or r >= x + 19
    return r % 2 == 0 and 24 <= r <= x + 17


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
    lines = ["z=12, y=5 two-token residual census (x=5..45, R=0..x+45)"]
    bad = 0
    formula_bad = 0
    for x in range(5, 46):
        T = []
        P = []
        for R in range(0, x + 46):
            a = H_ordered(R, (x, 5), 12)
            b = H_canonical(R, (x, 5), 12)
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
        H_ordered.cache_clear()
        H_canonical.cache_clear()
    lines.append(f"engine mismatches: {bad}")
    lines.append(f"formula mismatches (raw vs closed form): {formula_bad}")
    tailbad = 0
    for x in range(5, 46):
        for off in range(4):
            R = x + 18 + off
            v = H_ordered(R, (x, 5), 12)
            if v != (x + 5) % 2:
                tailbad += 1
                lines.append(f"TAIL MISS x={x} R={R} v={v}")
        H_ordered.cache_clear()
        H_canonical.cache_clear()
    lines.append(f"tail mismatches (R>=x+18 vs (x+5)%2): {tailbad}")
    payload = "\n".join(lines) + "\n"
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "census.txt").write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if bad == 0 and formula_bad == 0 and tailbad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
