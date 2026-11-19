#!/usr/bin/env python3
"""Independent audit for the proved z=14, y=5 two-token residual slice.

The universal proof is x-induction with the complete A/B/C signature-band
partition in report.md.  This file checks the transcription using two
independent direct mex recurrences, the published K1031/K1045 child anchors,
all signature bands on a large finite box, the K0832 low-R collapse and tail,
and deterministic scatter checks.  Finite checks are not the universal proof.
Standard library only; output is deterministic.
"""
from __future__ import annotations

from functools import lru_cache
import hashlib
import json
import random
import sys
from pathlib import Path

sys.setrecursionlimit(500000)


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
            opts.add(H_ordered(R - 1, X[:i] + (v - 1,) + X[i + 1 :], z))
        else:
            opts.add(H_ordered(R - 1, X[:i] + X[i + 1 :], z + 1))
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
            child = tuple(sorted(X[:i] + (v - 1,) + X[i + 1 :], reverse=True))
            opts.add(H_canonical(R - 1, child, z))
        else:
            child = tuple(sorted(X[:i] + X[i + 1 :], reverse=True))
            opts.add(H_canonical(R - 1, child, z + 1))
        while i + 1 < len(X) and X[i + 1] == v:
            i += 1
        i += 1
    if z >= 1:
        opts.add(1 ^ H_canonical(R - 1, X, z - 1))
    return mex(opts)


def clear_caches():
    H_ordered.cache_clear()
    H_canonical.cache_clear()


def odd(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi


def even(r, lo, hi):
    return r % 2 == 0 and lo <= r <= hi


# K1031: z=14, y=4 (the B child of the present slice).
def K1031_T(x, r):
    if x == 4:
        return r in (1, 3, 5, 7)
    if x in (5, 6):
        return odd(r, 1, 9)
    if x in (7, 8):
        return odd(r, 1, 11)
    if x == 9:
        return odd(r, 1, 13)
    if x == 10:
        return odd(r, 1, 17)
    if x in (11, 13, 14, 15, 17, 18):
        return odd(r, 1, 13)
    if x == 12:
        return odd(r, 1, 13) or r == 19
    if x == 16:
        return odd(r, 1, 13) or r == 21
    if x == 19:
        return odd(r, 1, 13) or odd(r, 23, 37)
    return odd(r, 1, 13) or r == 23


def K1031_P(x, r):
    if x % 2 == 0 and x <= 10:
        return False
    if x % 2 == 1 and x <= 9:
        return r >= x + 5
    if x in (11, 13):
        return r in (15, 17) or r >= 19
    if x == 12:
        return r in (15, 17)
    if x == 14:
        return r in (15, 17, 19)
    if x in (15, 17):
        return r in (15, 17, 19) or r >= 21
    if x == 16:
        return r in (15, 17, 19)
    if x == 18:
        return r in (15, 17, 19, 21)
    if x % 2 == 1:
        return (r in (15, 17, 19, 21)
                or (r % 2 == 0 and 24 <= r <= x + 17)
                or r >= x + 19)
    return (r in (15, 17, 19, 21)
            or (r % 2 == 0 and 24 <= r <= x + 18))


def K1031(x, r):
    if r == 0:
        return 0
    if K1031_T(x, r):
        return 2
    return 1 if K1031_P(x, r) else 0


# K1045: z=13, y=5 (the C child before the 1-xor move).
def K1045_T(x, r):
    if x == 5:
        return odd(r, 1, 9)
    if x in (6, 7):
        return odd(r, 1, 11)
    if x == 8:
        return odd(r, 1, 17)
    if x == 9:
        return odd(r, 1, 13)
    if x == 10:
        return odd(r, 1, 13) or r == 19
    if x in (11, 12, 13, 15, 16, 17):
        return odd(r, 1, 13)
    if x == 14:
        return odd(r, 1, 13) or r == 21
    if x == 18:
        return odd(r, 1, 13) or r == 23
    if x == 19:
        return odd(r, 1, 13) or odd(r, 23, 37)
    return odd(r, 1, 13) or r == 23


def K1045_P(x, r):
    if x == 5:
        return False
    if x == 6:
        return r >= 12
    if x == 7:
        return False
    if x == 8:
        return r in (14, 16, 18) or r >= 19
    if x == 9:
        return r in (14, 16, 18)
    if x == 10:
        return r in (14, 16, 18, 20) or r >= 21
    if x == 11:
        return r in (14, 16, 18)
    if x == 12:
        return r in (14, 16, 18, 20) or r >= 21
    if x == 13:
        return r in (14, 16, 18, 20)
    if x == 14:
        return r in (14, 16, 18, 20, 22) or r >= 23
    if x == 15:
        return r in (14, 16, 18, 20)
    if x == 16:
        return r in (14, 16, 18, 20, 22) or r >= 23
    if x == 17:
        return r in (14, 16, 18, 20, 22)
    if x == 18:
        return r in (14, 16, 18, 20, 22) or r >= 24
    if x == 19:
        return r in (14, 16, 18, 20, 22)
    if x % 2 == 0:
        return (r in (14, 16, 18, 20, 22)
                or (r % 2 == 1 and 25 <= r <= x + 17)
                or r >= x + 19)
    return (r in (14, 16, 18, 20, 22)
            or (r % 2 == 1 and 25 <= r <= x + 18))


def K1045(x, r):
    if r == 0:
        return 0
    if K1045_T(x, r):
        return 2
    return 1 if K1045_P(x, r) else 0


# Candidate theorem: H(R;(x,5);14), x>=5.
def T(x, r):
    if x == 5:
        return odd(r, 1, 9)
    if x == 6:
        return odd(r, 1, 11)
    if x == 7:
        return odd(r, 1, 11)
    if x == 8:
        return odd(r, 1, 13)
    if x == 9:
        return odd(r, 1, 19)
    if x == 10:
        return odd(r, 1, 13)
    if x in (11, 12, 14, 15, 16, 18, 19):
        return odd(r, 1, 13)
    if x == 13:
        return odd(r, 1, 13) or r == 21
    if x == 17:
        return odd(r, 1, 13) or r == 23
    if x == 20:
        return odd(r, 1, 13) or odd(r, 25, 39)
    return odd(r, 1, 13) or r == 25


def P(x, r):
    if x == 5:
        return False
    if x == 6:
        return r >= 12
    if x == 7:
        return False
    if x == 8:
        return r >= 14
    if x == 9:
        return False
    if x == 10:
        return r in (15, 17, 19) or r >= 20
    if x == 11:
        return r in (15, 17, 19)
    if x == 12:
        return r in (15, 17, 19) or r >= 21
    if x == 13:
        return r in (15, 17, 19)
    if x == 14:
        return r in (15, 17, 19) or r >= 21
    if x == 15:
        return r in (15, 17, 19, 21)
    if x == 16:
        return r in (15, 17, 19, 21) or r >= 23
    if x == 17:
        return r in (15, 17, 19, 21)
    if x == 18:
        return r in (15, 17, 19, 21) or r >= 23
    if x == 19:
        return r in (15, 17, 19, 21, 23)
    if x % 2 == 0:
        return (r in (15, 17, 19, 21, 23)
                or (r % 2 == 0 and 26 <= r <= x + 18)
                or r >= x + 20)
    return (r in (15, 17, 19, 21, 23)
            or (r % 2 == 0 and 26 <= r <= x + 19))


def candidate(x, r):
    if r == 0:
        return 0
    if T(x, r):
        return 2
    return 1 if P(x, r) else 0


# Signature rows are (parity, lo, hi, signature), parity 1=odd, 0=even.
FIXED_BANDS = {
    5: [(1,1,9,"01"),(1,11,23,"1"),(0,2,10,"23"),(0,12,24,"1")],
    6: [(1,1,11,"01"),(1,13,25,"0"),(0,2,10,"23"),(0,12,12,"03"),(0,14,24,"0")],
    7: [(1,1,11,"01"),(1,13,25,"1"),(0,2,12,"23"),(0,14,26,"1")],
    8: [(1,1,13,"01"),(1,15,27,"0"),(0,2,12,"23"),(0,14,18,"03"),(0,20,26,"0")],
    9: [(1,1,19,"01"),(1,21,27,"1"),(0,2,14,"23"),(0,16,28,"1")],
    10:[(1,1,13,"01"),(1,15,29,"0"),(0,2,14,"23"),(0,16,18,"12"),(0,20,20,"023"),(0,22,28,"0")],
    11:[(1,1,13,"01"),(1,15,19,"0"),(1,21,29,"1"),(0,2,14,"23"),(0,16,30,"1")],
    12:[(1,1,13,"01"),(1,15,31,"0"),(0,2,14,"23"),(0,16,18,"1"),(0,20,20,"12"),(0,22,30,"0")],
    13:[(1,1,13,"01"),(1,15,19,"0"),(1,21,21,"01"),(1,23,31,"1"),(0,2,14,"23"),(0,16,32,"1")],
    14:[(1,1,13,"01"),(1,15,33,"0"),(0,2,14,"23"),(0,16,20,"1"),(0,22,22,"023"),(0,24,32,"0")],
    15:[(1,1,13,"01"),(1,15,21,"0"),(1,23,33,"1"),(0,2,14,"23"),(0,16,34,"1")],
    16:[(1,1,13,"01"),(1,15,35,"0"),(0,2,14,"23"),(0,16,20,"1"),(0,22,22,"12"),(0,24,34,"0")],
    17:[(1,1,13,"01"),(1,15,21,"0"),(1,23,23,"01"),(1,25,35,"1"),(0,2,14,"23"),(0,16,36,"1")],
    18:[(1,1,13,"01"),(1,15,37,"0"),(0,2,14,"23"),(0,16,22,"1"),(0,24,24,"023"),(0,26,36,"0")],
    19:[(1,1,13,"01"),(1,15,23,"0"),(1,25,37,"1"),(0,2,14,"23"),(0,16,22,"1"),(0,24,38,"123")],
    20:[(1,1,13,"01"),(1,15,23,"0"),(1,25,39,"01"),(0,2,14,"23"),(0,16,22,"1"),(0,24,24,"123"),(0,26,38,"0")],
    21:[(1,1,13,"01"),(1,15,23,"0"),(1,25,25,"01"),(1,27,39,"1"),(0,2,14,"23"),(0,16,22,"1"),(0,24,24,"123"),(0,26,40,"02")],
}


def bands_for(x):
    if x in FIXED_BANDS:
        return FIXED_BANDS[x]
    if x >= 22 and x % 2 == 0:
        return [(1,1,13,"01"),(1,15,23,"0"),(1,25,25,"01"),(1,27,x+19,"1"),
                (0,2,14,"23"),(0,16,22,"1"),(0,24,24,"123"),(0,26,26,"02"),(0,28,x+18,"0")]
    if x >= 23 and x % 2 == 1:
        return [(1,1,13,"01"),(1,15,23,"0"),(1,25,25,"01"),(1,27,x+18,"1"),
                (0,2,14,"23"),(0,16,22,"1"),(0,24,24,"123"),(0,26,26,"02"),(0,28,x+19,"0")]
    raise ValueError(x)


def signature_from_children(x, R):
    r = R - 1
    values = {K1031(x, r), 1 ^ K1045(x, r)}
    if x > 5:
        values.add(candidate(x - 1, r))
    else:
        # At x=5, decrementing either equal token gives the same multiset
        # (5,4);14, which is the B child after swapping token order.
        values.add(K1031(x, r))
    return "".join(str(v) for v in sorted(values))


def single_token(n, z, R):
    if R == 0 or n <= 0:
        return 0
    if z == 0:
        return min(R, n) % 2
    if z == n:
        if R % 2 and R <= 2 * n - 1:
            return 2
        if R % 2 == 0 and R <= n - 1:
            return 0
        return n % 2
    if 1 <= z <= n - 1:
        m = z if z % 2 else z - 1
        if R <= m:
            return 2 if R % 2 else 0
        if m < R < n + z:
            return (R + z) % 2
        return n % 2
    if z >= n + 1:
        m = n if n % 2 else n - 1
        if R <= m:
            return 2 if R % 2 else 0
        return n % 2
    raise ValueError((n, z, R))


def audit_once():
    clear_caches()
    failures = []
    counts = {}

    # Two direct recurrences against the candidate formula.
    n = 0
    for x in range(5, 36):
        for R in range(0, x + 23):
            a = H_ordered(R, (x, 5), 14)
            b = H_canonical(R, (x, 5), 14)
            c = candidate(x, R)
            n += 2
            if a != b or a != c:
                failures.append(("root-direct", x, R, a, b, c))
    counts["ordered_and_canonical_direct_vs_formula"] = n

    # Published B/C child anchors, each checked by both direct engines.
    anchors = 0
    for x in range(5, 36):
        for R in range(0, x + 23):
            for engine in (H_ordered, H_canonical):
                b = engine(R, (x, 4), 14)
                c = engine(R, (x, 5), 13)
                anchors += 2
                if b != K1031(x, R):
                    failures.append(("K1031-B-anchor", x, R, b, K1031(x, R)))
                if c != K1045(x, R):
                    failures.append(("K1045-C-anchor", x, R, c, K1045(x, R)))
    counts["K1031_and_K1045_child_anchor_checks"] = anchors

    # Complete A/B/C signature partition, identity and mex on x<=3000.
    sig_checks = parity_checks = 0
    for x in range(5, 1001):
        bands = bands_for(x)
        for R in range(1, x + 20):
            hits = [s for p, lo, hi, s in bands
                    if R % 2 == p and lo <= R <= hi]
            if len(hits) != 1:
                failures.append(("band-coverage", x, R, hits))
                continue
            actual = signature_from_children(x, R)
            if hits[0] != actual:
                failures.append(("band-signature", x, R, hits[0], actual))
                continue
            values = {int(ch) for ch in hits[0]}
            value = mex(values)
            expected = candidate(x, R)
            sig_checks += 1
            if value != expected:
                failures.append(("band-mex", x, R, hits[0], value, expected))
            if R % 2 == 0 and value > 1:
                failures.append(("Theorem-T-even", x, R, hits[0], value))
            if R % 2 == 1 and value > 2:
                failures.append(("Theorem-T-odd", x, R, hits[0], value))
            parity_checks += 1
    counts["complete_signature_coverage_identity_mex"] = sig_checks
    counts["Theorem_T_parity_bound"] = parity_checks

    # K0832 height-only reduction: R<=z+1=15.
    low = 0
    for x in range(5, 2001):
        for R in range(16):
            low += 1
            a = candidate(x, R)
            b = single_token(x + 5, 14, R)
            if a != b:
                failures.append(("height-only", x, R, a, b))
    counts["height_only_reduction_R_le_15"] = low

    # K0832 general tail: S=x+5, |X|=2, z=14, so R>=x+20.
    tail = 0
    for x in range(5, 5001):
        for offset in range(4):
            R = x + 20 + offset
            tail += 1
            expected = (x + 5) % 2
            actual = candidate(x, R)
            if actual != expected:
                failures.append(("tail", x, R, actual, expected))
    counts["general_tail"] = tail

    # Fixed-seed scatter checks the child mex identity outside the main box.
    rng = random.Random(20261119)
    scatter = 0
    for _ in range(8000):
        x = rng.randint(5, 3000)
        R = rng.randint(0, x + 120)
        scatter += 1
        actual = 0 if R == 0 else mex({K1031(x, R - 1),
                                      1 ^ K1045(x, R - 1),
                                      candidate(x - 1, R - 1) if x > 5 else K1031(x, R - 1)})
        expected = candidate(x, R)
        if actual != expected:
            failures.append(("scatter", x, R, actual, expected))
    counts["fixed_seed_child_mex_scatter"] = scatter

    return {
        "all_pass": not failures,
        "theorem": "z=14 y=5 two-token residual Grundy slice",
        "classification": "universal proof by x-induction and complete A/B/C signature bands",
        "finite_audit_role": "two direct mex recurrences, published child anchors, signature coverage/identity/mex, low-R collapse, general tail, and fixed-seed scatter only",
        "scope": {
            "target": "H(R;(x,5);14), x>=5, R>=0",
            "direct_x": [5, 35],
            "direct_R": "0 <= R <= x+22",
            "anchor_x": [5, 35],
            "anchor_R": "0 <= R <= x+22",
            "signature_x": [5, 1000],
            "signature_R": "1 <= R <= x+19",
            "low_R": "0 <= R <= 15",
            "low_x": [5, 2000],
            "tail_R": "x+20 <= R <= x+23",
            "tail_x": [5, 5000],
            "scatter_points": 8000,
            "scatter_seed": 20261119,
        },
        "counts": counts,
        "total_checks": sum(counts.values()),
        "failure_count": len(failures),
        "first_failures": failures[:20],
    }


def run():
    first = audit_once()
    second = audit_once()
    first_bytes = json.dumps(first, ensure_ascii=False, sort_keys=True,
                              separators=(",", ":")).encode()
    second_bytes = json.dumps(second, ensure_ascii=False, sort_keys=True,
                               separators=(",", ":")).encode()
    same = first_bytes == second_bytes
    verifier_sha = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    result = {
        **first,
        "repeat_runs": 2,
        "repeat_byte_identical": same,
        "verifier_sha256": verifier_sha,
        "sha256_without_hash_field": hashlib.sha256(first_bytes).hexdigest(),
    }
    payload = json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    out = Path(__file__).with_name("output")
    out.mkdir(parents=True, exist_ok=True)
    (out / "audit.json").write_text(payload, encoding="utf-8")
    print(payload, end="")
    return 0 if result["all_pass"] and same else 1


if __name__ == "__main__":
    sys.exit(run())
