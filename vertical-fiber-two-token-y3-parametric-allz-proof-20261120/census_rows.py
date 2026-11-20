#!/usr/bin/env python3
"""Raw census for the y=3 two-token parametric family across z=0..80.

For every z in 0..ZHI, x in 3..XMAX and R in 0..x+z+RBUF, the raw
order-preserving engine and the raw descending-canonical engine must
agree with each other and with the closed form cand3 of the parametric
all-z proof. Additionally the tail claim R >= x+z+4 with value
(x+3) % 2 is asserted on each row, and the merge-below-diagonal
corollary (x <= z-4 implies the single-token closed form) is asserted
on all merge rows. Writes output/census.txt with the T/P position rows
and the mismatch counters.
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


# Closed form under test (same functions as verify_y3_universal.py).
def in_T3(z, x, R):
    if R <= 0:
        return False
    S = x + 3
    if z % 2 == 1:
        if x <= z - 4:
            return R % 2 == 1 and R <= q_odd(S)
        if x == z - 3:
            return R % 2 == 1 and R <= z + 2
        if x == z - 2:
            return R % 2 == 1 and R <= z
        if x == z - 1:
            return (R % 2 == 1 and R <= z) or R == z + 4
        if x == z:
            return R % 2 == 1 and R <= z
        if x == z + 1:
            return R % 2 == 1 and R <= z
        if x == z + 2:
            return R % 2 == 1 and R <= z
        if x == z + 3:
            return (R % 2 == 1 and R <= z) or R == z + 6
        if x == z + 4:
            return (R % 2 == 1 and R <= z) or (R % 2 == 1 and z + 6 <= R <= 2 * z + 7)
        return (R % 2 == 1 and R <= z) or R == z + 6
    else:
        if x <= z - 4:
            return R % 2 == 1 and R <= q_odd(S)
        if x == z - 3:
            return R % 2 == 1 and R <= z + 3
        if x == z - 2:
            return R % 2 == 1 and R <= z - 1
        if x == z - 1:
            return R % 2 == 1 and R <= z - 1
        if x == z:
            return R % 2 == 1 and R <= z - 1
        if x == z + 1:
            return (R % 2 == 1 and R <= z - 1) or R == z + 5
        if x == z + 2:
            return R % 2 == 1 and R <= z - 1
        if x == z + 3:
            return R % 2 == 1 and R <= z - 1
        if x == z + 4:
            return (R % 2 == 1 and R <= z - 1) or (R % 2 == 1 and z + 7 <= R <= 2 * z + 7)
        return (R % 2 == 1 and R <= z - 1) or R == z + 7


def in_P3(z, x, R):
    if R <= 0:
        return False
    S = x + 3
    zn = z % 2
    if zn == 1:
        if x <= z - 4:
            return S % 2 == 1 and R >= q_odd(S) + 1
        if x == z - 3:
            return R == z + 1 or R >= z + 3
        if x == z - 2:
            return R in (z + 1, z + 3)
        if x == z - 1:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z:
            return R in (z + 1, z + 3)
        if x == z + 1:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z + 2:
            return R in (z + 1, z + 3, z + 5)
        if x == z + 3:
            return R in (z + 1, z + 3, z + 5) or R >= z + 7
        if x == z + 4:
            return R in (z + 1, z + 3, z + 5)
        base = R in (z + 1, z + 3, z + 5)
        band = z + 8 <= R <= x + z + 3 and R % 2 == 1
        tail = x % 2 == 0 and R >= x + z + 4
        return base or band or tail
    else:
        if x <= z - 4:
            return S % 2 == 1 and R >= q_odd(S) + 1
        if x == z - 3:
            return False
        if x == z - 2:
            return R == z + 1 or R >= z + 3
        if x == z - 1:
            return R in (z + 1, z + 3)
        if x == z:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z + 1:
            return R in (z + 1, z + 3)
        if x == z + 2:
            return R in (z + 1, z + 3) or R >= z + 5
        if x == z + 3:
            return R in (z + 1, z + 3, z + 5)
        base = R in (z + 1, z + 3, z + 5)
        band = z + 8 <= R <= x + z + 3 and R % 2 == 0
        tail = x % 2 == 0 and R >= x + z + 4
        return base or band or tail


def cand3(z, x, R):
    t = in_T3(z, x, R)
    pv = in_P3(z, x, R)
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
    lines = ["y=3 two-token parametric all-z census "
             f"(z=0..{ZHI}, x=3..{XMAX}, R=0..x+z+{RBUF})"]
    pts = 0
    engine_bad = 0
    formula_bad = 0
    m_pts = m_bad = 0
    for z in range(0, ZHI + 1):
        for x in range(3, XMAX + 1):
            T = []
            P = []
            for R in range(0, x + z + RBUF + 1):
                a = H_ordered(R, (x, 3), z)
                b = H_canonical(R, (x, 3), z)
                c = cand3(z, x, R)
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
                if x <= z - 4:
                    m_pts += 1
                    if a != single_token(x + 3, z, R):
                        m_bad += 1
                        lines.append(f"MERGE MISS z={z} x={x} R={R} raw={a}")
            lines.append(f"z={z} x={x:2d} T=[{rle(T)}]")
            lines.append(f"         P=[{rle(P)}]")
    tailbad = 0
    for z in range(0, ZHI + 1):
        for x in range(3, XMAX + 1):
            for off in range(3):
                R = x + z + 4 + off
                v = H_ordered(R, (x, 3), z)
                if v != (x + 3) % 2:
                    tailbad += 1
                    lines.append(f"TAIL MISS z={z} x={x} R={R} raw={v}")
    lines.append(f"points compared (two engines + closed form): {pts}")
    lines.append(f"engine mismatches: {engine_bad}")
    lines.append(f"formula mismatches (raw vs closed form): {formula_bad}")
    lines.append(f"merge rows checked (x<=z-4, vs single-token form): {m_pts}")
    lines.append(f"merge mismatches: {m_bad}")
    lines.append(f"tail mismatches (R>=x+z+4 vs (x+3)%2): {tailbad}")
    payload = "\n".join(lines) + "\n"
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "census.txt").write_text(payload, encoding="utf-8")
    print("\n".join(lines[-6:]))
    return (0 if engine_bad == 0 and formula_bad == 0 and tailbad == 0
            and m_bad == 0 else 1)


if __name__ == "__main__":
    sys.exit(main())
