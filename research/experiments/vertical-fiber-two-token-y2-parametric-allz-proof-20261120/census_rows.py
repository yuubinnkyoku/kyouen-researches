#!/usr/bin/env python3
"""Raw census for the y=2 two-token parametric family across z=0..80.

For every z in 0..ZHI, x in 2..XMAX and R in 0..x+z+RBUF, the raw
order-preserving engine and the raw descending-canonical engine must
agree with each other and with the closed form cand2 of the parametric
all-z proof. Additionally the tail claim R >= x+z+3 with value
(x+2) % 2 is asserted on each row. Writes output/census.txt with the
T/P position rows and the mismatch counters.
Deterministic: two runs are byte-identical (no timestamps, fixed order).
"""
import sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(1_000_000)

ZHI = 80
XMAX = 70
RBUF = 12


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


# Closed form under test (same functions as verify_p2_universal.py).
def cand2_T(z, x):
    if z % 2 == 1:
        if x <= z - 3:
            top = 2 * ((x + 1) // 2) + 1
            return ("ladder", 1, top, None)
        if x == z - 2:
            return ("band", 1, z + 2, None)
        if x in (z - 1, z, z + 1):
            return ("band", 1, z, None)
        if x == z + 2:
            return ("pin", 1, z, z + 4)
        if x == z + 3:
            return ("sweep", 1, z, (z + 4, 2 * z + 5))
        return ("pin", 1, z, z + 4)
    else:
        if x <= z - 3:
            top = 2 * ((x + 1) // 2) + 1
            return ("ladder", 1, top, None)
        if x == z - 2:
            return ("band", 1, z + 1, None)
        if x in (z - 1, z + 1, z + 2):
            return ("band", 1, z - 1, None)
        if x == z:
            return ("pin", 1, z - 1, z + 3)
        if x == z + 3:
            return ("sweep", 1, z - 1, (z + 5, 2 * z + 5))
        return ("pin", 1, z - 1, z + 5)


def in_T(z, x, R):
    if R <= 0:
        return False
    kind, lo, hi, extra = cand2_T(z, x)
    if kind in ("ladder", "band"):
        return lo <= R <= hi and R % 2 == 1
    if kind == "pin":
        return (lo <= R <= hi and R % 2 == 1) or R == extra
    a, b = extra
    return (lo <= R <= hi and R % 2 == 1) or (a <= R <= b and R % 2 == 1)


def in_P(z, x, R):
    if R <= 0:
        return False
    p = z % 2
    if z % 2 == 1:
        if x % 2 == 0 and x <= z - 3:
            return False
        if x % 2 == 1 and x <= z - 3:
            return R >= x + 3
        if x in (z - 2, z):
            return R in (z + 1, z + 3) or R >= z + 4
        if x == z - 1:
            return R == z + 1
        if x == z + 1:
            return R in (z + 1, z + 3)
        if x == z + 2:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z + 3:
            return R in (z + 1, z + 3)
        if x % 2 == 1:
            return (R in (z + 1, z + 3)
                    or (z + 6 <= R <= x + z + 3 and R % 2 == 1)
                    or R >= x + z + 4)
        return (R in (z + 1, z + 3)
                or (z + 6 <= R <= x + z + 2 and R % 2 == 1))
    else:
        if x % 2 == 0 and x <= z - 2:
            return False
        if x % 2 == 1 and x <= z - 3:
            return R >= x + 3
        if x in (z - 1, z + 1):
            return R in (z + 1, z + 3) or R >= z + 4
        if x == z:
            return R == z + 1
        if x == z + 2:
            return R in (z + 1, z + 3)
        if x % 2 == 1:
            return (R in (z + 1, z + 3)
                    or (z + 6 <= R <= x + z + 3 and R % 2 == p)
                    or R >= x + z + 4)
        return (R in (z + 1, z + 3)
                or (z + 6 <= R <= x + z + 2 and R % 2 == p))


def cand2(z, x, R):
    t = in_T(z, x, R)
    pv = in_P(z, x, R)
    assert not (t and pv), ("T/P overlap", z, x, R)
    if R == 0:
        return 0
    if t:
        return 2
    return 1 if pv else 0


def rle(nums):
    out = []
    for n in nums:  # nums are ascending
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
    lines = ["y=2 two-token parametric all-z census "
             f"(z=0..{ZHI}, x=2..{XMAX}, R=0..x+z+{RBUF})"]
    pts = 0
    engine_bad = 0
    formula_bad = 0
    for z in range(0, ZHI + 1):
        for x in range(2, XMAX + 1):
            T = []
            P = []
            for R in range(0, x + z + RBUF + 1):
                a = H_ordered(R, (x, 2), z)
                b = H_canonical(R, (x, 2), z)
                c = cand2(z, x, R)
                pts += 1
                if a != b:
                    engine_bad += 1
                    lines.append(f"ENGINE MISS z={z} x={x} R={R} "
                                 f"ordered={a} canonical={b}")
                if a != c:
                    formula_bad += 1
                    lines.append(f"FORMULA MISS z={z} x={x} R={R} "
                                 f"raw={a} formula={c}")
                if a == 2:
                    T.append(R)
                elif a == 1:
                    P.append(R)
            lines.append(f"z={z} x={x:2d} T=[{rle(T)}]")
            lines.append(f"         P=[{rle(P)}]")
    tailbad = 0
    for z in range(0, ZHI + 1):
        for x in range(2, XMAX + 1):
            for off in range(3):
                R = x + z + 3 + off
                v = H_ordered(R, (x, 2), z)
                if v != (x + 2) % 2:
                    tailbad += 1
                    lines.append(f"TAIL MISS z={z} x={x} R={R} raw={v}")
    lines.append(f"points compared (two engines + closed form): {pts}")
    lines.append(f"engine mismatches: {engine_bad}")
    lines.append(f"formula mismatches (raw vs closed form): {formula_bad}")
    lines.append(f"tail mismatches (R>=x+z+3 vs (x+2)%2): {tailbad}")
    payload = "\n".join(lines) + "\n"
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "census.txt").write_text(payload, encoding="utf-8")
    print("\n".join(lines[:1] + lines[-4:]))
    return 0 if engine_bad == 0 and formula_bad == 0 and tailbad == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
