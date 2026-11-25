#!/usr/bin/env python3
"""Independent audit for the z=18, y=4 two-token Grundy theorem.

The universal proof is x-induction plus the complete symbolic A/B/C signature
bands in report.md. This script checks the child anchors against the generic
multiset recursion, the parent formula against that recursion, every signature
band, the induction closure on a large finite range, the K0832 single-token
reduction boundary, and the general tail.
"""
from __future__ import annotations

import hashlib
import json
import random
from functools import lru_cache
from pathlib import Path


def odd(r: int, a: int, b: int) -> bool:
    return a <= r <= b and (r & 1) == 1


def even(r: int, a: int, b: int) -> bool:
    return a <= r <= b and (r & 1) == 0


def qodd(n: int) -> int:
    return n if n & 1 else n - 1


def qeven(n: int) -> int:
    return n if not (n & 1) else n - 1


def g18y3(x: int, r: int) -> int:
    """K1078: H(r;(x,3);18)."""
    if r == 0:
        return 0
    t = False
    if 3 <= x <= 14:
        t = odd(r, 1, 2 * (x // 2) + 3)
    elif x == 15:
        t = odd(r, 1, 21)
    elif 16 <= x <= 18:
        t = odd(r, 1, 17)
    elif x == 19:
        t = odd(r, 1, 17) or r == 23
    elif x in (20, 21):
        t = odd(r, 1, 17)
    elif x == 22:
        t = odd(r, 1, 17) or odd(r, 25, 43)
    elif x >= 23:
        t = odd(r, 1, 17) or r == 25
    if t:
        return 2

    p = False
    if x in (4, 6, 8, 10, 12, 14):
        p = r >= x + 4
    elif x in (5, 7, 9, 11, 13, 15, 3):
        p = False
    elif x == 16:
        p = r in (19, 21) or r >= 22
    elif x in (17, 19):
        p = r in (19, 21)
    elif x in (18, 20):
        p = r in (19, 21) or r >= 23
    elif x == 21:
        p = r in (19, 21, 23)
    elif x == 22:
        p = (r in (19, 21, 23) or even(r, 26, 42) or r >= 44)
    elif x >= 24 and not (x & 1):
        p = (r in (19, 21, 23) or even(r, 26, x + 20)
             or r >= x + 22)
    elif x >= 23 and (x & 1):
        p = r in (19, 21, 23) or even(r, 26, x + 21)
    if p:
        return 1
    if r >= x + 22:
        return (x + 3) & 1
    return 0


def g17y4(x: int, r: int) -> int:
    """K1076: H(r;(x,4);17)."""
    if r == 0:
        return 0
    t = False
    if x == 4:
        t = odd(r, 1, 7)
    elif x in (5, 6):
        t = odd(r, 1, 9)
    elif x in (7, 8):
        t = odd(r, 1, 11)
    elif x in (9, 10):
        t = odd(r, 1, 13)
    elif x in (11, 12):
        t = odd(r, 1, 15)
    elif x == 13:
        t = odd(r, 1, 21)
    elif x in (14, 15, 16):
        t = odd(r, 1, 17)
    elif x == 17:
        t = odd(r, 1, 17) or r == 23
    elif x in (18, 19, 20):
        t = odd(r, 1, 17)
    elif x == 21:
        t = odd(r, 1, 17) or r == 25
    elif x == 22:
        t = odd(r, 1, 17) or odd(r, 25, 43)
    elif x >= 23:
        t = odd(r, 1, 17) or r == 25
    if t:
        return 2

    p = False
    if x in (4, 6, 8, 10, 12):
        p = False
    elif x == 5:
        p = r >= 10
    elif x == 7:
        p = r >= 12
    elif x == 9:
        p = r >= 14
    elif x == 11:
        p = r >= 16
    elif x == 13:
        p = r in (18, 20, 22) or r >= 23
    elif x == 14:
        p = r in (18, 20)
    elif x == 15:
        p = r in (18, 20, 22) or r >= 23
    elif x in (16, 18):
        p = r in (18, 20, 22)
    elif x in (17, 19):
        p = r in (18, 20, 22, 24) or r >= 25
    elif x == 20:
        p = r in (18, 20, 22, 24)
    elif x == 21:
        p = r in (18, 20, 22, 24) or r >= 26
    elif x == 22:
        p = r in (18, 20, 22, 24)
    elif x >= 23 and (x & 1):
        p = (r in (18, 20, 22, 24) or odd(r, 27, x + 20)
             or r >= x + 22)
    elif x >= 24 and not (x & 1):
        p = r in (18, 20, 22, 24) or odd(r, 27, x + 21)
    if p:
        return 1
    if r >= x + 22:
        return (x + 4) & 1
    return 0


def in_parent_T(x: int, r: int) -> bool:
    if x == 4:
        return odd(r, 1, 7)
    if x in (5, 6):
        return odd(r, 1, 9)
    if x in (7, 8):
        return odd(r, 1, 11)
    if x in (9, 10):
        return odd(r, 1, 13)
    if x in (11, 12):
        return odd(r, 1, 15)
    if x == 13:
        return odd(r, 1, 17)
    if x == 14:
        return odd(r, 1, 21)
    if x == 16:
        return odd(r, 1, 17) or r == 23
    if x == 20:
        return odd(r, 1, 17) or r == 25
    if x == 23:
        return odd(r, 1, 17) or odd(r, 27, 45)
    if x >= 24:
        return odd(r, 1, 17) or r == 27
    return odd(r, 1, 17)


def in_parent_P(x: int, r: int) -> bool:
    if x == 5:
        return r >= 10
    if x == 7:
        return r >= 12
    if x == 9:
        return r >= 14
    if x == 11:
        return r >= 16
    if x == 13:
        return r >= 18
    if x == 15:
        return r in (19, 21, 23) or r >= 24
    if x == 16:
        return r in (19, 21)
    if x == 17:
        return r in (19, 21, 23) or r >= 24
    if x == 18:
        return r in (19, 21, 23)
    if x == 19:
        return r in (19, 21, 23) or r >= 25
    if x == 20:
        return r in (19, 21, 23)
    if x == 21:
        return r in (19, 21, 23) or r >= 25
    if x == 22:
        return r in (19, 21, 23, 25)
    if x >= 23:
        base = r in (19, 21, 23, 25)
        band = even(r, 28, qeven(x + 22))
        tail = bool(x & 1) and r >= x + 23
        return base or band or tail
    return False


def parent_formula(x: int, r: int) -> int:
    if r == 0:
        return 0
    if r >= x + 23:
        return (x + 4) & 1
    if in_parent_T(x, r):
        return 2
    if in_parent_P(x, r):
        return 1
    return 0


def mex(values) -> int:
    s = set(values)
    g = 0
    while g in s:
        g += 1
    return g


def signature(x: int, r: int) -> str:
    b = g18y3(x, r - 1)
    c = 1 ^ g17y4(x, r - 1)
    a = b if x == 4 else parent_formula(x - 1, r - 1)
    return "".join(map(str, sorted({a, b, c})))

# (odd/even) bands for the finite rows x=4,...,22.
SIG = {
4:  {1:[(1,7,"01"),(9,25,"1")], 0:[(2,8,"23"),(10,26,"1")]},
5:  {1:[(1,9,"01"),(11,27,"0")], 0:[(2,8,"23"),(10,10,"03"),(12,26,"0")]},
6:  {1:[(1,9,"01"),(11,27,"1")], 0:[(2,10,"23"),(12,28,"1")]},
7:  {1:[(1,11,"01"),(13,29,"0")], 0:[(2,10,"23"),(12,12,"03"),(14,28,"0")]},
8:  {1:[(1,11,"01"),(13,29,"1")], 0:[(2,12,"23"),(14,30,"1")]},
9:  {1:[(1,13,"01"),(15,31,"0")], 0:[(2,12,"23"),(14,14,"03"),(16,30,"0")]},
10: {1:[(1,13,"01"),(15,31,"1")], 0:[(2,14,"23"),(16,32,"1")]},
11: {1:[(1,15,"01"),(17,33,"0")], 0:[(2,14,"23"),(16,16,"03"),(18,32,"0")]},
12: {1:[(1,15,"01"),(17,33,"1")], 0:[(2,16,"23"),(18,34,"1")]},
13: {1:[(1,17,"01"),(19,35,"0")], 0:[(2,16,"23"),(18,22,"03"),(24,34,"0")]},
14: {1:[(1,21,"01"),(23,35,"1")], 0:[(2,18,"23"),(20,36,"1")]},
15: {1:[(1,17,"01"),(19,37,"0")], 0:[(2,18,"23"),(20,22,"12"),(24,36,"0")]},
16: {1:[(1,17,"01"),(19,21,"0"),(23,23,"01"),(25,37,"1")],
     0:[(2,18,"23"),(20,38,"1")]},
17: {1:[(1,17,"01"),(19,39,"0")],
     0:[(2,18,"23"),(20,22,"1"),(24,24,"023"),(26,38,"0")]},
18: {1:[(1,17,"01"),(19,23,"0"),(25,39,"1")],
     0:[(2,18,"23"),(20,40,"1")]},
19: {1:[(1,17,"01"),(19,41,"0")],
     0:[(2,18,"23"),(20,22,"1"),(24,24,"12"),(26,40,"0")]},
20: {1:[(1,17,"01"),(19,23,"0"),(25,25,"01"),(27,41,"1")],
     0:[(2,18,"23"),(20,42,"1")]},
21: {1:[(1,17,"01"),(19,43,"0")],
     0:[(2,18,"23"),(20,24,"1"),(26,26,"023"),(28,42,"0")]},
22: {1:[(1,17,"01"),(19,25,"0"),(27,43,"1")],
     0:[(2,18,"23"),(20,24,"1"),(26,44,"123")]},
}


def in_band(r: int, lo: int, hi: int) -> bool:
    return lo <= r <= hi and ((r - lo) & 1) == 0


def expected_signature(x: int, r: int) -> str | None:
    p = r & 1
    if x <= 22:
        for lo, hi, sig in SIG[x][p]:
            if in_band(r, lo, hi):
                return sig
        return None
    if x == 23:
        bands = ([(1,17,"01"),(19,25,"0"),(27,45,"01")] if p else
                 [(2,18,"23"),(20,24,"1"),(26,26,"123"),(28,44,"0")])
    elif x == 24:
        bands = ([(1,17,"01"),(19,25,"0"),(27,27,"01"),(29,45,"1")] if p else
                 [(2,18,"23"),(20,24,"1"),(26,26,"123"),(28,46,"02")])
    elif p:
        bands = [(1,17,"01"),(19,25,"0"),(27,27,"01"),(29,qodd(x+22),"1")]
    else:
        bands = [(2,18,"23"),(20,24,"1"),(26,26,"123"),(28,28,"02"),
                 (30,qeven(x+22),"0")]
    for lo, hi, sig in bands:
        if in_band(r, lo, hi):
            return sig
    return None


@lru_cache(maxsize=None)
def raw(R: int, X: tuple[int, ...], z: int) -> int:
    """Generic multiset recurrence, independent of all closed forms."""
    if R == 0:
        return 0
    opts = set()
    seen = set()
    for i, value in enumerate(X):
        if value in seen:
            continue
        seen.add(value)
        rest = list(X)
        rest.pop(i)
        if value >= 2:
            rest.append(value - 1)
            rest.sort()
            opts.add(raw(R - 1, tuple(rest), z))
        else:
            rest.sort()
            opts.add(raw(R - 1, tuple(rest), z + 1))
    if z >= 1:
        opts.add(1 ^ raw(R - 1, X, z - 1))
    return mex(opts)


def single_F(x: int, z: int, r: int) -> int:
    """K0832 single-token closed form."""
    L = x + z + 1
    if z == 0:
        return min(r, x) & 1
    if x == z:
        if (r & 1) and r <= 2*x - 1:
            return 2
        if not (r & 1) and r <= x - 1:
            return 0
        return x & 1
    if z <= x - 1:
        m = z if z & 1 else z - 1
        if r <= m:
            return 2 if (r & 1) else 0
        if r < L - 1:
            return (r + z) & 1
        return x & 1
    m = x if x & 1 else x - 1
    if r <= m:
        return 2 if (r & 1) else 0
    return x & 1


def main() -> None:
    rng = random.Random(20261120)
    counts = {
        "B_child_raw_checks": 0,
        "C_child_raw_checks": 0,
        "parent_raw_checks": 0,
        "signature_band_checks": 0,
        "signature_band_gaps": 0,
        "signature_band_mismatches": 0,
        "bottom_up_checks": 0,
        "induction_closure_checks": 0,
        "deep_sample_checks": 0,
        "tail_checks": 0,
        "low_R_reduction_checks": 0,
        "low_R_boundary_checks": 0,
        "small_total_full_reduction_checks": 0,
        "bad": [],
    }

    # Published B/C child formulas versus the generic multiset recursion.
    for x in range(3, 41):
        for r in range(0, x + 41):
            got, want = g18y3(x, r), raw(r, tuple(sorted((3, x))), 18)
            counts["B_child_raw_checks"] += 1
            if got != want:
                counts["bad"].append(["B-child", x, r, got, want])
    for x in range(4, 41):
        for r in range(0, x + 41):
            got, want = g17y4(x, r), raw(r, tuple(sorted((4, x))), 17)
            counts["C_child_raw_checks"] += 1
            if got != want:
                counts["bad"].append(["C-child", x, r, got, want])

    # Full parent recurrence versus the proposed closed form.
    for x in range(4, 46):
        for r in range(0, x + 46):
            got, want = raw(r, (4, x), 18), parent_formula(x, r)
            counts["parent_raw_checks"] += 1
            if got != want:
                counts["bad"].append(["parent-raw", x, r, got, want])

    # Every symbolic signature band must cover exactly the stated interval.
    for x in range(4, 201):
        for r in range(1, x + 23):
            exp, got = expected_signature(x, r), signature(x, r)
            counts["signature_band_checks"] += 1
            if exp is None:
                counts["signature_band_gaps"] += 1
                counts["bad"].append(["signature-gap", x, r])
            elif exp != got:
                counts["signature_band_mismatches"] += 1
                counts["bad"].append(["signature", x, r, exp, got])

    # A separate bottom-up row engine.
    previous = None
    for x in range(4, 151):
        row = [0] * (x + 47)
        for r in range(1, len(row)):
            b = g18y3(x, r - 1)
            c = 1 ^ g17y4(x, r - 1)
            a = b if x == 4 else previous[r - 1]
            row[r] = mex((a, b, c))
            counts["bottom_up_checks"] += 1
            if row[r] != parent_formula(x, r):
                counts["bad"].append(["bottom-up", x, r, row[r], parent_formula(x, r)])
        previous = row

    # Finite audit of the symbolic induction step over a large triangle.
    for x in range(4, 1501):
        for r in range(1, x + 23):
            b = g18y3(x, r - 1)
            c = 1 ^ g17y4(x, r - 1)
            a = b if x == 4 else parent_formula(x - 1, r - 1)
            got, want = mex((a, b, c)), parent_formula(x, r)
            counts["induction_closure_checks"] += 1
            if got != want:
                counts["bad"].append(["closure", x, r, got, want])
                if len(counts["bad"]) >= 100:
                    break
        if len(counts["bad"]) >= 100:
            break

    # Deep samples stress the affine upper endpoints far beyond the static table.
    for x in range(25, 200001, 97):
        rs = {1,2,16,17,18,19,20,22,23,24,25,26,27,28,29,30,
              x+20,x+21,x+22,x+23,x+24,x+50}
        rs.update(rng.randrange(1, x + 100) for _ in range(8))
        for r in sorted(rs):
            b = g18y3(x, r - 1)
            c = 1 ^ g17y4(x, r - 1)
            a = parent_formula(x - 1, r - 1)
            got, want = mex((a, b, c)), parent_formula(x, r)
            counts["deep_sample_checks"] += 1
            if got != want:
                counts["bad"].append(["deep", x, r, got, want])

    # K0832 tail: S=x+4, |X|=2, z=18, hence R>=x+23.
    for x in range(4, 1501):
        for r in (x + 23, x + 100):
            counts["tail_checks"] += 1
            if parent_formula(x, r) != ((x + 4) & 1):
                counts["bad"].append(["tail", x, r, parent_formula(x, r)])

    # Exact initial interval of the single-token reduction.
    row_bound = {14:22, 15:23, 16:22, 17:23, 18:24, 19:25, 20:24, 21:25}
    for x in range(22, 5001):
        for r in range(0, 27):
            got, want = parent_formula(x, r), single_F(x + 4, 18, r)
            counts["low_R_reduction_checks"] += 1
            if got != want:
                counts["bad"].append(["low-R", x, r, got, want])
        got, want = parent_formula(x, 27), single_F(x + 4, 18, 27)
        counts["low_R_boundary_checks"] += 1
        if got == want:
            counts["bad"].append(["low-R-not-sharp", x, 27, got, want])
        expected_parent = 0 if x == 22 else 2
        if got != expected_parent or want != 1:
            counts["bad"].append(["low-R-boundary-value", x, 27, got, want])

    for x, bound in row_bound.items():
        for r in range(0, bound + 1):
            got, want = parent_formula(x, r), single_F(x + 4, 18, r)
            counts["low_R_reduction_checks"] += 1
            if got != want:
                counts["bad"].append(["row-low-R", x, r, got, want])
        got, want = parent_formula(x, bound + 1), single_F(x + 4, 18, bound + 1)
        counts["low_R_boundary_checks"] += 1
        if got == want:
            counts["bad"].append(["row-low-R-not-sharp", x, bound + 1, got, want])

    # Small-total rows: finite spot checks; all-R equality follows by direct piecewise comparison.
    for x in range(4, 14):
        for r in range(0, 201):
            got, want = parent_formula(x, r), single_F(x + 4, 18, r)
            counts["small_total_full_reduction_checks"] += 1
            if got != want:
                counts["bad"].append(["small-total", x, r, got, want])

    audit = {
        "theorem": "two-token-z18-y4-full-grundy",
        "status": "pass" if not counts["bad"] else "fail",
        "scope": "finite audit only; universal proof is x-induction plus complete symbolic A/B/C bands",
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "counts": {k: v for k, v in counts.items() if k != "bad"},
        "bad": counts["bad"][:100],
        "raw_cache": {"hits": raw.cache_info().hits, "misses": raw.cache_info().misses},
    }
    out = Path(__file__).with_name("output") / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(audit, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
