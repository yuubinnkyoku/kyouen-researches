#!/usr/bin/env python3
"""Independent finite audit for the proved z=6, y=36 two-token slice.

The universal proof is the x-induction and explicit A/B/C signature table in
report.md. This script corroborates it with ordered and canonical direct
recursions, a separate A/B/C recursion, signature/mex checks, and the K0832
tail. Finite checks are not the source of universal quantification.
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
    """K0873: proved full two-token z=5 formula."""
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


def T35(x):
    result = {1, 3, 5}
    if x == 35:
        result.add(73)
    elif x == 39:
        result.add(75)
    elif x == 42:
        result.update({77, 79, 81, 83})
    elif x >= 43:
        result.add(77)
    return result


def P35(x, r):
    if x == 35:
        return O(r, 7, 71)
    if x == 36:
        return O(r, 7) or E(r, 74)
    if x == 37:
        return O(r, 7, 73)
    if x == 38:
        return O(r, 7) or E(r, 76)
    if x == 39:
        return O(r, 7, 73)
    if x == 40:
        return O(r, 7) or E(r, 76)
    if x == 41:
        return O(r, 7, 75)
    if x == 42:
        return O(r, 7, 75) or E(r, 78) or r >= 85
    if x == 43:
        return O(r, 7, 75) or E(r, 78, 84)
    if x % 2 == 0:
        return O(r, 7, 75) or E(r, 78) or r >= x + 43
    return O(r, 7, 75) or E(r, 78, x + 41)


def h35(x, r):
    if r == 0:
        return 0
    if r in T35(x):
        return 2
    return int(P35(x, r))


def T36(x):
    result = {1, 3, 5}
    if x == 36:
        result.add(75)
    elif x == 40:
        result.add(77)
    elif x == 43:
        result.update({79, 81, 83, 85})
    elif x >= 44:
        result.add(79)
    return result


def P36(x, r):
    if x == 36:
        return O(r, 7, 73)
    if x == 37:
        return O(r, 7) or E(r, 76)
    if x == 38:
        return O(r, 7, 75)
    if x == 39:
        return O(r, 7) or E(r, 78)
    if x == 40:
        return O(r, 7, 75)
    if x == 41:
        return O(r, 7) or E(r, 78)
    if x == 42:
        return O(r, 7, 77)
    if x == 43:
        return O(r, 7, 77) or E(r, 80) or O(r, 87)
    if x == 44:
        return O(r, 7, 77) or E(r, 80, 86)
    if x % 2 == 0:
        return O(r, 7, 77) or E(r, 80, x + 42)
    return O(r, 7, 77) or E(r, 80) or O(r, x + 44)


def h36_closed(x, r):
    if r == 0:
        return 0
    if r in T36(x):
        return 2
    return int(P36(x, r))


@lru_cache(None)
def h36_induction(x, r):
    if r == 0:
        return 0
    a = h35(36, r - 1) if x == 36 else h36_induction(x - 1, r - 1)
    b = h35(x, r - 1)
    c = 1 ^ h5(x, 36, r - 1)
    return mex((a, b, c))


def expected_signature(x, r):
    """Exact distinct child-value set {A,B,C} for 1 <= r < x+43."""
    if x == 36:
        rows = ([(1, 5, (0, 1)), (7, 73, (0,)), (75, 75, (0, 1)), (77, 77, (1,))]
                if r & 1 else [(2, 6, (2, 3)), (8, 78, (1,))])
    elif x == 37:
        rows = ([(1, 5, (0, 1)), (7, 79, (0,))]
                if r & 1 else [(2, 6, (2, 3)), (8, 74, (1,)), (76, 76, (0, 2, 3)), (78, 78, (0,))])
    elif x == 38:
        rows = ([(1, 5, (0, 1)), (7, 75, (0,)), (77, 79, (1,))]
                if r & 1 else [(2, 6, (2, 3)), (8, 80, (1,))])
    elif x == 39:
        rows = ([(1, 5, (0, 1)), (7, 81, (0,))]
                if r & 1 else [(2, 6, (2, 3)), (8, 74, (1,)), (76, 76, (1, 2)), (78, 80, (0,))])
    elif x == 40:
        rows = ([(1, 5, (0, 1)), (7, 75, (0,)), (77, 77, (0, 1)), (79, 81, (1,))]
                if r & 1 else [(2, 6, (2, 3)), (8, 82, (1,))])
    elif x == 41:
        rows = ([(1, 5, (0, 1)), (7, 83, (0,))]
                if r & 1 else [(2, 6, (2, 3)), (8, 76, (1,)), (78, 78, (0, 2, 3)), (80, 82, (0,))])
    elif x == 42:
        rows = ([(1, 5, (0, 1)), (7, 77, (0,)), (79, 83, (1,))]
                if r & 1 else [(2, 6, (2, 3)), (8, 76, (1,)), (78, 84, (1, 2, 3))])
    elif x == 43:
        rows = ([(1, 5, (0, 1)), (7, 77, (0,)), (79, 85, (0, 1))]
                if r & 1 else [(2, 6, (2, 3)), (8, 76, (1,)), (78, 78, (1, 2, 3)), (80, 84, (0,))])
    elif x == 44:
        rows = ([(1, 5, (0, 1)), (7, 77, (0,)), (79, 79, (0, 1)), (81, 85, (1,))]
                if r & 1 else [(2, 6, (2, 3)), (8, 76, (1,)), (78, 78, (1, 2, 3)), (80, 86, (0, 2))])
    elif r & 1:
        if x % 2 == 0:
            rows = [(1, 5, (0, 1)), (7, 77, (0,)), (79, 79, (0, 1)), (81, x + 41, (1,))]
        else:
            rows = [(1, 5, (0, 1)), (7, 77, (0,)), (79, 79, (0, 1)), (81, x + 42, (1,))]
    elif x % 2 == 0:
        rows = [(2, 6, (2, 3)), (8, 76, (1,)), (78, 78, (1, 2, 3)),
                (80, 80, (0, 2)), (82, x + 42, (0,))]
    else:
        rows = [(2, 6, (2, 3)), (8, 76, (1,)), (78, 78, (1, 2, 3)),
                (80, 80, (0, 2)), (82, x + 41, (0,))]
    for lo, hi, signature in rows:
        if lo <= r <= hi and (r - lo) % 2 == 0:
            return signature
    return None


def direct_engines():
    @lru_cache(None)
    def ordered(r, tokens, z):
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
            children.append(ordered(r - 1, tuple(child), next_z))
        if z:
            children.append(1 ^ ordered(r - 1, tokens, z - 1))
        return mex(children)

    @lru_cache(None)
    def canonical(r, tokens, z):
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
            children.append(canonical(r - 1, tuple(sorted(child, reverse=True)), next_z))
        if z:
            children.append(1 ^ canonical(r - 1, tokens, z - 1))
        return mex(children)

    return ordered, canonical


def audit_once():
    failures = []
    ordered, canonical = direct_engines()
    direct_calls = 0
    for x in range(36, 60):
        for r in range(x + 61):
            expected = h36_closed(x, r)
            got_ordered = ordered(r, (x, 36), 6)
            got_canonical = canonical(r, (x, 36), 6)
            direct_calls += 2
            if (got_ordered, got_canonical) != (expected, expected):
                failures.append(("direct", x, r, got_ordered, got_canonical, expected))

    induction_count = 0
    for x in range(36, 81):
        for r in range(x + 61):
            got = h36_induction(x, r)
            expected = h36_closed(x, r)
            induction_count += 1
            if got != expected:
                failures.append(("induction", x, r, got, expected))

    signature_count = mex_count = odd_bound_count = even_bound_count = 0
    parameter_count = 0
    for x in range(36, 2001):
        twos = set()
        for r in range(1, x + 43):
            q = r - 1
            a = h35(36, q) if x == 36 else h36_closed(x - 1, q)
            b = h35(x, q)
            c = 1 ^ h5(x, 36, q)
            actual = tuple(sorted({a, b, c}))
            expected = expected_signature(x, r)
            signature_count += 1
            if actual != expected:
                failures.append(("signature", x, r, actual, expected))
                continue
            value = mex(actual)
            mex_count += 1
            if value != h36_closed(x, r):
                failures.append(("mex", x, r, value, h36_closed(x, r)))
            if r & 1:
                odd_bound_count += 1
                if not set(actual) <= {0, 1}:
                    failures.append(("odd-parent-bound", x, r, actual))
            else:
                even_bound_count += 1
                if value > 1:
                    failures.append(("even-parent-value-bound", x, r, value, actual))
            if value == 2:
                twos.add(r)
        parameter_count += 1
        if twos != T36(x):
            failures.append(("T36", x, sorted(twos), sorted(T36(x))))

    tail_count = 0
    for x in range(36, 2001):
        expected = (x + 36) & 1
        for r in range(x + 43, x + 106):
            tail_count += 1
            if h36_closed(x, r) != expected:
                failures.append(("tail", x, r, h36_closed(x, r), expected))

    return {
        "schema": "kyouen-z6-y36-audit-v1",
        "range": {
            "direct_x": [36, 59],
            "direct_r": "0..x+60",
            "induction_x": [36, 80],
            "induction_r": "0..x+60",
            "signature_x": [36, 2000],
            "signature_r": "1..x+42",
            "tail_r": "x+43..x+105",
        },
        "checks": {
            "ordered_and_canonical_direct_calls": direct_calls,
            "independent_ABC_recurrence": induction_count,
            "ABC_signatures": signature_count,
            "mex_equals_closed_formula": mex_count,
            "odd_parent_child_bound": odd_bound_count,
            "even_parent_value_bound": even_bound_count,
            "tail_parity": tail_count,
            "x_parameters": parameter_count,
        },
        "failures": failures[:30],
        "failure_count": len(failures),
        "cache": {
            "induction_states": h36_induction.cache_info().currsize,
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
    if body["failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
