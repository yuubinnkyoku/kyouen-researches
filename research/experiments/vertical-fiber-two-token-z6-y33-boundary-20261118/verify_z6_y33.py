#!/usr/bin/env python3
"""Independent audit for the proved two-token residual slice z=6, y=33.

The universal proof is in report.md. This verifier checks:
- two independent direct recursions (ordered and descending-canonical tokens),
- the A/B/C signatures on the explicit transient and parity-stable bands,
- mex against the closed form,
- the K0832 tail and the value-2 locus.
The finite audit is corroboration, not the source of universal quantification.
"""
from __future__ import annotations

import hashlib
import json
import sys
from functools import lru_cache
from pathlib import Path

sys.setrecursionlimit(10000)


def mex(values):
    s = set(values)
    n = 0
    while n in s:
        n += 1
    return n


def O(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 1


def E(r, a, b=None):
    return r >= a and (b is None or r <= b) and r % 2 == 0


def h5(x, y, r):
    """K0873: exact z=5 two-token formula."""
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


def T32(x):
    t = {1, 3, 5}
    if x == 32:
        t.add(67)
    elif x == 36:
        t.add(69)
    elif x == 39:
        t.update({71, 73, 75, 77})
    elif x >= 40:
        t.add(71)
    return t


def P32(x, r):
    if x == 32:
        return O(r, 7, 65)
    if x == 33:
        return O(r, 7, 71) or E(r, 68, 70) or r >= 72
    if x == 34:
        return O(r, 7, 67)
    if x == 35:
        return O(r, 7, 73) or E(r, 70, 72) or r >= 74
    if x == 36:
        return O(r, 7, 67)
    if x == 37:
        return O(r, 7, 75) or E(r, 70, 74) or r >= 76
    if x == 38:
        return O(r, 7, 69)
    if x == 39:
        return O(r, 7, 69) or E(r, 72, 76) or r >= 78
    if x % 2 == 0:
        return O(r, 7, 69) or E(r, 72, x + 38)
    return O(r, 7, 69) or E(r, 72, x + 37) or r >= x + 39


def h32(x, r):
    if r == 0:
        return 0
    if r in T32(x):
        return 2
    return int(P32(x, r))


def T33(x):
    t = {1, 3, 5}
    if x == 33:
        t.add(69)
    elif x == 37:
        t.add(71)
    elif x == 40:
        t.update({73, 75, 77, 79})
    elif x >= 41:
        t.add(73)
    return t


def P33(x, r):
    if x == 33:
        return O(r, 7, 67)
    if x == 34:
        return O(r, 7, 73) or E(r, 70, 72) or r >= 74
    if x == 35:
        return O(r, 7, 69)
    if x == 36:
        return O(r, 7, 75) or E(r, 72, 74) or r >= 76
    if x == 37:
        return O(r, 7, 69)
    if x == 38:
        return O(r, 7, 77) or E(r, 72, 76) or r >= 78
    if x == 39:
        return O(r, 7, 71)
    if x % 2 == 0:
        return O(r, 7, 71) or E(r, 74, x + 38) or r >= x + 40
    return O(r, 7, 71) or E(r, 74, x + 39)


def h33_closed(x, r):
    if r == 0:
        return 0
    if r in T33(x):
        return 2
    return int(P33(x, r))


@lru_cache(None)
def h33_rec(x, r):
    if r == 0:
        return 0
    if x == 33:
        a = h32(33, r - 1)  # (32,33) canonicalizes to (33,32), same as B
    else:
        a = h33_rec(x - 1, r - 1)
    b = h32(x, r - 1)
    c = 1 ^ h5(x, 33, r - 1)
    return mex((a, b, c))


ODD_SIG = {
    33: [(1, 5, (0, 1)), (7, 67, (0,)), (69, 69, (0, 1)), (71, 71, (1,))],
    34: [(1, 5, (0, 1)), (7, 73, (0,))],
    35: [(1, 5, (0, 1)), (7, 69, (0,)), (71, 73, (1,))],
    36: [(1, 5, (0, 1)), (7, 75, (0,))],
    37: [(1, 5, (0, 1)), (7, 69, (0,)), (71, 71, (0, 1)), (73, 75, (1,))],
    38: [(1, 5, (0, 1)), (7, 77, (0,))],
    39: [(1, 5, (0, 1)), (7, 71, (0,)), (73, 77, (1,))],
    40: [(1, 5, (0, 1)), (7, 71, (0,)), (73, 79, (0, 1))],
}
EVEN_SIG = {
    33: [(2, 6, (2, 3)), (8, 72, (1,))],
    34: [(2, 6, (2, 3)), (8, 68, (1,)), (70, 70, (0, 2, 3)), (72, 72, (0,))],
    35: [(2, 6, (2, 3)), (8, 74, (1,))],
    36: [(2, 6, (2, 3)), (8, 68, (1,)), (70, 70, (1, 2)), (72, 74, (0,))],
    37: [(2, 6, (2, 3)), (8, 76, (1,))],
    38: [(2, 6, (2, 3)), (8, 70, (1,)), (72, 72, (0, 2, 3)), (74, 76, (0,))],
    39: [(2, 6, (2, 3)), (8, 70, (1,)), (72, 78, (1, 2, 3))],
    40: [(2, 6, (2, 3)), (8, 70, (1,)), (72, 72, (1, 2, 3)), (74, 78, (0,))],
}


def expected_signature(x, r):
    if r & 1:
        rows = ODD_SIG.get(x)
        if rows is None:
            end = x + (38 if x & 1 else 39)
            rows = [(1, 5, (0, 1)), (7, 71, (0,)), (73, 73, (0, 1)), (75, end, (1,))]
    else:
        rows = EVEN_SIG.get(x)
        if rows is None:
            if x == 41:
                rows = [(2, 6, (2, 3)), (8, 70, (1,)), (72, 72, (1, 2, 3)),
                        (74, x + 39, (0, 2))]
            else:
                end = x + (39 if x & 1 else 38)
                rows = [(2, 6, (2, 3)), (8, 70, (1,)), (72, 72, (1, 2, 3)),
                        (74, 74, (0, 2)), (76, end, (0,))]
    for a, b, sig in rows:
        if a <= r <= b and (r - a) % 2 == 0:
            return sig
    return None


def direct_engines():
    @lru_cache(None)
    def ordered(r, tokens, z):
        if r == 0:
            return 0
        out = []
        for i, v in enumerate(tokens):
            c = list(tokens)
            nz = z
            if v >= 2:
                c[i] -= 1
            else:
                c.pop(i)
                nz += 1
            out.append(ordered(r - 1, tuple(c), nz))
        if z:
            out.append(1 ^ ordered(r - 1, tokens, z - 1))
        return mex(out)

    @lru_cache(None)
    def canonical(r, tokens, z):
        if r == 0:
            return 0
        out = []
        for i, v in enumerate(tokens):
            c = list(tokens)
            nz = z
            if v >= 2:
                c[i] -= 1
            else:
                c.pop(i)
                nz += 1
            out.append(canonical(r - 1, tuple(sorted(c, reverse=True)), nz))
        if z:
            out.append(1 ^ canonical(r - 1, tokens, z - 1))
        return mex(out)

    return ordered, canonical


def audit_once():
    failures = []
    ordered, canonical = direct_engines()
    direct_calls = 0
    for x in range(33, 57):
        for r in range(x + 51):
            want = h33_closed(x, r)
            a = ordered(r, (x, 33), 6)
            b = canonical(r, (x, 33), 6)
            direct_calls += 2
            if a != want or b != want:
                failures.append(("direct", x, r, a, b, want))

    signature_count = mex_count = recurrence_count = 0
    odd_count = even_count = parameter_count = 0
    for x in range(33, 81):
        for r in range(x + 51):
            value = h33_rec(x, r)
            if value != h33_closed(x, r):
                failures.append(("target-recurrence", x, r, value, h33_closed(x, r)))
            recurrence_count += 1
    for x in range(33, 2001):
        twos = set()
        for r in range(1, x + 40):
            q = r - 1
            a = h32(33, q) if x == 33 else h33_closed(x - 1, q)
            b = h32(x, q)
            c = 1 ^ h5(x, 33, q)
            actual = tuple(sorted({a, b, c}))
            expected = expected_signature(x, r)
            signature_count += 1
            if actual != expected:
                failures.append(("signature", x, r, actual, expected))
                continue
            v = mex(actual)
            mex_count += 1
            if v != h33_closed(x, r):
                failures.append(("closed", x, r, v, h33_closed(x, r)))
            if r & 1:
                odd_count += 1
                if not set(actual) <= {0, 1}:
                    failures.append(("odd-parent-bound", x, r, actual))
            else:
                even_count += 1
                if v > 1:
                    failures.append(("even-parent-bound", x, r, v, actual))
            if v == 2:
                twos.add(r)
        parameter_count += 1
        if twos != T33(x):
            failures.append(("T33", x, sorted(twos), sorted(T33(x))))

    tail_count = 0
    for x in range(33, 2001):
        tail_value = (x + 33) & 1
        for r in range(x + 40, x + 104):
            tail_count += 1
            if h33_closed(x, r) != tail_value:
                failures.append(("tail", x, r, h33_closed(x, r), tail_value))

    return {
        "schema": "kyouen-z6-y33-audit-v1",
        "range": {
            "direct_x": [33, 56],
            "direct_r": "0..x+50",
            "signature_x": [33, 2000],
            "signature_r": "1..x+39",
            "tail_r": "x+40..x+103",
        },
        "checks": {
            "ordered_and_canonical_direct_calls": direct_calls,
            "ABC_signatures": signature_count,
            "mex_equals_closed_formula": mex_count,
            "independent_target_recurrence": recurrence_count,
            "odd_parent_child_bound": odd_count,
            "even_parent_value_bound": even_count,
            "tail_parity": tail_count,
            "x_parameters": parameter_count,
        },
        "failures": failures[:20],
        "failure_count": len(failures),
        "cache": {
            "target_recurrence_states": h33_rec.cache_info().currsize,
            "ordered_states": ordered.cache_info().currsize,
            "canonical_states": canonical.cache_info().currsize,
        },
    }


def main():
    body = audit_once()
    body["verifier_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    canonical = json.dumps(body, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    body["audit_sha256"] = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    out = json.dumps(body, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    output = Path(__file__).with_name("output")
    output.mkdir(parents=True, exist_ok=True)
    (output / "audit.json").write_text(out, encoding="utf-8")
    print(out, end="")
    if body["failure_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
