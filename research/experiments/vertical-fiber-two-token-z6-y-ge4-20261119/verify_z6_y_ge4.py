#!/usr/bin/env python3
"""Finite audit for the universal z=6, y>=4 two-token classification.

The proof is the strong induction on S=x+y and the explicit ten-case
A/B/C signature table in report.md. This program checks the formulas and
recurrence on a large finite region and compares selected states with two
independent direct recursions. It does not supply the universal quantifier.
"""
from __future__ import annotations

import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(10000)


def mex(values):
    values = set(values)
    n = 0
    while n in values:
        n += 1
    return n


def O(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 1


def E(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 0


def h5(x, y, r):
    """K0873: proved complete two-token z=5 formula."""
    if r == 0:
        return 0
    s, d = x + y, x - y
    twos = {1, 3, 5}
    if d == 1 and y >= 2:
        twos.add(2 * y + 3)
    elif d == 5:
        twos.add(2 * y + 5)
    elif d == 6:
        twos.update({2 * y + 5, 2 * y + 7, 2 * y + 9, 2 * y + 11})
    elif d >= 7:
        twos.add(2 * y + 5)
    if r in twos:
        return 2
    if d == 0:
        one = E(r, 6, s + 2) if y >= 3 else False
    elif d == 1:
        one = (E(r, 6, s + 3) or r >= s + 4) if y >= 2 else r >= 4
    elif d == 2:
        one = E(r, 6, s) if y >= 2 else False
    elif d == 3:
        one = E(r, 6, s + 1) or r >= s + 2
    elif d == 4:
        one = E(r, 6, s)
    elif d == 5:
        one = E(r, 6, s - 1) or r >= s + 1
    elif d == 6:
        one = E(r, 6, s - 2)
    elif d % 2:
        one = E(r, 6, 2 * y + 4) or O(r, 2 * y + 7, s + 4) or r >= s + 6
    else:
        one = E(r, 6, 2 * y + 4) or O(r, 2 * y + 7, s + 5)
    return int(one)


def h6(y, d, r):
    """Proved formula for H(R;(y+d,y);6), y>=4."""
    x, s = y + d, 2 * y + d
    if r == 0:
        return 0
    if r in {1, 3, 5}:
        return 2
    if d == 0 and r == 2 * y + 3:
        return 2
    if d == 4 and r == 2 * y + 5:
        return 2
    if d == 7 and r in {2 * y + 7, 2 * y + 9, 2 * y + 11, 2 * y + 13}:
        return 2
    if d >= 8 and r == 2 * y + 7:
        return 2

    if d == 0:
        one = O(r, 7, 2 * y + 1)
    elif d == 1:
        one = O(r, 7) or E(r, 2 * y + 4)
    elif d == 2:
        one = O(r, 7, 2 * y + 3)
    elif d == 3:
        one = O(r, 7) or E(r, 2 * y + 6)
    elif d == 4:
        one = O(r, 7, 2 * y + 3)
    elif d == 5:
        one = O(r, 7) or E(r, 2 * y + 6)
    elif d == 6:
        one = O(r, 7, 2 * y + 5)
    elif d % 2:
        one = O(r, 7, 2 * y + 5) or E(r, 2 * y + 8) or O(r, s + 8)
    else:
        one = O(r, 7, 2 * y + 5) or E(r, 2 * y + 8, s + 6)
    return int(one)


def expected_signature(y, d, r):
    """The ten-case A/B/C signature table, as a disjoint interval partition."""
    if d == 0:
        odd = [(1, 5, (0, 1)), (7, 2*y+1, (0,)),
               (2*y+3, 2*y+3, (0, 1)), (2*y+5, 2*y+5, (1,))]
        even = [(2, 6, (2, 3)), (8, 2*y+6, (1,))]
    elif d == 1:
        odd = [(1, 5, (0, 1)), (7, 2*y+7, (0,))]
        even = [(2, 6, (2, 3)), (8, 2*y+2, (1,)),
                (2*y+4, 2*y+4, (0, 2, 3)), (2*y+6, 2*y+6, (0,))]
    elif d == 2:
        odd = [(1, 5, (0, 1)), (7, 2*y+3, (0,)),
               (2*y+5, 2*y+7, (1,))]
        even = [(2, 6, (2, 3)), (8, 2*y+8, (1,))]
    elif d == 3:
        odd = [(1, 5, (0, 1)), (7, 2*y+9, (0,))]
        even = [(2, 6, (2, 3)), (8, 2*y+2, (1,)),
                (2*y+4, 2*y+4, (1, 2)), (2*y+6, 2*y+8, (0,))]
    elif d == 4:
        odd = [(1, 5, (0, 1)), (7, 2*y+3, (0,)),
               (2*y+5, 2*y+5, (0, 1)), (2*y+7, 2*y+9, (1,))]
        even = [(2, 6, (2, 3)), (8, 2*y+10, (1,))]
    elif d == 5:
        odd = [(1, 5, (0, 1)), (7, 2*y+11, (0,))]
        even = [(2, 6, (2, 3)), (8, 2*y+4, (1,)),
                (2*y+6, 2*y+6, (0, 2, 3)), (2*y+8, 2*y+10, (0,))]
    elif d == 6:
        odd = [(1, 5, (0, 1)), (7, 2*y+5, (0,)),
               (2*y+7, 2*y+11, (1,))]
        even = [(2, 6, (2, 3)), (8, 2*y+4, (1,)),
                (2*y+6, 2*y+12, (1, 2, 3))]
    elif d == 7:
        odd = [(1, 5, (0, 1)), (7, 2*y+5, (0,)),
               (2*y+7, 2*y+13, (0, 1))]
        even = [(2, 6, (2, 3)), (8, 2*y+4, (1,)),
                (2*y+6, 2*y+6, (1, 2, 3)), (2*y+8, 2*y+12, (0,))]
    elif d == 8:
        odd = [(1, 5, (0, 1)), (7, 2*y+5, (0,)),
               (2*y+7, 2*y+7, (0, 1)), (2*y+9, 2*y+13, (1,))]
        even = [(2, 6, (2, 3)), (8, 2*y+4, (1,)),
                (2*y+6, 2*y+6, (1, 2, 3)), (2*y+8, 2*y+14, (0, 2))]
    else:
        s = 2*y + d
        odd = [(1, 5, (0, 1)), (7, 2*y+5, (0,)),
               (2*y+7, 2*y+7, (0, 1)), (2*y+9, s+6, (1,))]
        even = [(2, 6, (2, 3)), (8, 2*y+4, (1,)),
                (2*y+6, 2*y+6, (1, 2, 3)), (2*y+8, 2*y+8, (0, 2)),
                (2*y+10, s+6, (0,))]
    rows = odd if r % 2 else even
    for lo, hi, signature in rows:
        if lo <= r <= hi and (r - lo) % 2 == 0:
            return signature
    return None


def h4_anchor(x, r):
    """K0880 base slice, independently written from its published cases."""
    if r == 0:
        return 0
    twos = {1, 3, 5}
    if x == 4:
        twos.add(11)
    elif x == 8:
        twos.add(13)
    elif x == 11:
        twos.update({15, 17, 19, 21})
    elif x >= 12:
        twos.add(15)
    if r in twos:
        return 2
    if x == 4:
        one = r in {7, 9}
    elif x == 5:
        one = r in {7, 9} or r >= 11
    elif x == 6:
        one = r in {7, 9, 11}
    elif x == 7:
        one = r in {7, 9, 11} or r >= 13
    elif x == 8:
        one = r in {7, 9, 11}
    elif x == 9:
        one = r in {7, 9, 11} or r >= 13
    elif x == 10:
        one = r in {7, 9, 11, 13}
    elif x == 11:
        one = r in {7, 9, 11, 13} or E(r, 16, 20) or r >= 22
    elif x % 2 == 0:
        one = r in {7, 9, 11, 13} or E(r, 16, x + 10)
    else:
        one = r in {7, 9, 11, 13} or E(r, 16, x + 9) or r >= x + 11
    return int(one)


def make_direct(canonical=False):
    @lru_cache(None)
    def g(r, tokens, z):
        if r == 0:
            return 0
        children = []
        for i, value in enumerate(tokens):
            child = list(tokens)
            next_z = z
            if value >= 2:
                child[i] -= 1
            else:
                child.pop(i)
                next_z += 1
            if canonical:
                child.sort(reverse=True)
            children.append(g(r - 1, tuple(child), next_z))
        if z:
            children.append(1 ^ g(r - 1, tokens, z - 1))
        return mex(children)
    return g


def audit_once():
    failures = []
    counts = {
        "base_y4_formula": 0,
        "inductive_signatures": 0,
        "inductive_mex": 0,
        "tail_parity": 0,
        "ordered_and_canonical_direct_calls": 0,
    }

    # The induction base y=4 is compared with K0880's separately encoded cases.
    for x in range(4, 2001):
        for r in range(0, x + 76):
            counts["base_y4_formula"] += 1
            if h6(4, x - 4, r) != h4_anchor(x, r):
                failures.append(("base-y4", x, r, h6(4, x-4, r), h4_anchor(x, r)))
                break
        if failures:
            break

    # For y>=5, both z=6 children have smaller x+y and stay in y>=4.
    for y in range(5, 121):
        for d in range(0, 101):
            x, s = y + d, 2*y + d
            for r in range(1, s + 7):
                if d == 0:
                    a = h6(y - 1, 1, r - 1)  # (y,y-1), after sorting
                else:
                    a = h6(y, d - 1, r - 1)
                b = h6(y - 1, d + 1, r - 1)
                c = 1 ^ h5(x, y, r - 1)
                actual = tuple(sorted({a, b, c}))
                expected = expected_signature(y, d, r)
                counts["inductive_signatures"] += 1
                if actual != expected:
                    failures.append(("signature", y, d, r, actual, expected))
                    break
                value = mex(actual)
                counts["inductive_mex"] += 1
                if value != h6(y, d, r):
                    failures.append(("mex", y, d, r, actual, value, h6(y, d, r)))
                    break
                if r & 1 and not set(actual) <= {0, 1}:
                    failures.append(("odd-parent-bound", y, d, r, actual))
                    break
                if not (r & 1) and value > 1:
                    failures.append(("even-parent-bound", y, d, r, actual, value))
                    break
            if failures:
                break
        if failures:
            break

    # Direct ordered and sorted-state recursions on selected two-token states.
    ordered, canonical = make_direct(False), make_direct(True)
    pairs = [(4, 4), (5, 4), (5, 5), (6, 4), (8, 5),
             (10, 4), (10, 8), (12, 4), (15, 5), (17, 17),
             (18, 4), (22, 14), (30, 20)]
    for y, d in pairs:
        x = y + d
        for r in range(45):
            got_o = ordered(r, (x, y), 6)
            got_c = canonical(r, (x, y), 6)
            want = h6(y, d, r)
            counts["ordered_and_canonical_direct_calls"] += 2
            if (got_o, got_c) != (want, want):
                failures.append(("direct", x, y, r, got_o, got_c, want))
                break
        if failures:
            break

    # The K0832 general tail starts at R=x+y+7 and equals (x+y) mod 2.
    for y in range(5, 121):
        for d in range(0, 101):
            s = 2*y + d
            expected = s & 1
            for r in range(s + 7, s + 48):
                counts["tail_parity"] += 1
                if h6(y, d, r) != expected:
                    failures.append(("tail", y, d, r, h6(y, d, r), expected))
                    break
            if failures:
                break
        if failures:
            break

    return {
        "schema": "kyouen-z6-y-ge4-audit-v1",
        "ranges": {
            "base_y4": "x=4..2000; R=0..x+75",
            "inductive_signature_and_mex": "y=5..120; d=x-y=0..100; R=1..x+y+6",
            "direct_recursions": "13 selected (x,y) pairs; R=0..44; ordered and sorted-state engines",
            "tail": "y=5..120; d=0..100; R=x+y+7..x+y+47",
        },
        "checks": counts,
        "failure_count": len(failures),
        "failures": failures[:30],
        "direct_engine_cache": {
            "ordered_states": ordered.cache_info().currsize,
            "canonical_states": canonical.cache_info().currsize,
        },
    }


def main():
    body = audit_once()
    body["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    body["audit_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    output = Path(__file__).with_name("output")
    output.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    (output / "audit.json").write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()
