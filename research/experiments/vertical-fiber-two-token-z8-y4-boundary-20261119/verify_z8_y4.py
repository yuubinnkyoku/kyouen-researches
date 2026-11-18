#!/usr/bin/env python3
"""Independent audit for the proved z=8, y=4 two-token residual slice.

The universal proof is by induction on x using explicit A/B/C signature bands,
K0986 (z=8,y=3), K0980 (z=7,y=4), K0832 Theorem T and its high-R tail.
Finite direct recursions below are independent audits, not the proof itself.
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path


def mex(values):
    seen = set(values)
    n = 0
    while n in seen:
        n += 1
    return n


def odd(r, lo, hi):
    return r % 2 == 1 and lo <= r <= hi


def even(r, lo, hi):
    return r % 2 == 0 and lo <= r <= hi


def at_least(r, lo):
    return r >= lo


def z8_y3(x, r):
    """K0986: H(r;(x,3);8), x>=3."""
    if r == 0:
        return 0
    t = p = False
    if x == 3:
        t = r in (1, 3, 5)
    elif x == 4:
        t, p = r in (1, 3, 5, 7), at_least(r, 8)
    elif x == 5:
        t = r in (1, 3, 5, 7, 9, 11)
    elif x == 6:
        t, p = r in (1, 3, 5, 7), (r == 9 or at_least(r, 11))
    elif x == 7:
        t, p = r in (1, 3, 5, 7), r in (9, 11)
    elif x == 8:
        t, p = r in (1, 3, 5, 7), (r in (9, 11) or at_least(r, 13))
    elif x == 9:
        t, p = r in (1, 3, 5, 7, 13), r in (9, 11)
    elif x == 10:
        t, p = r in (1, 3, 5, 7), (r in (9, 11) or at_least(r, 13))
    elif x == 11:
        t, p = r in (1, 3, 5, 7), r in (9, 11, 13)
    elif x == 12:
        t = r in (1, 3, 5, 7) or odd(r, 15, 23)
        p = r in (9, 11, 13) or even(r, 16, 22) or at_least(r, 24)
    elif x >= 13 and x % 2 == 1:
        t = r in (1, 3, 5, 7, 15)
        p = r in (9, 11, 13) or even(r, 16, x + 11)
    else:
        t = r in (1, 3, 5, 7, 15)
        p = r in (9, 11, 13) or even(r, 16, x + 10) or at_least(r, x + 12)
    return 2 if t else 1 if p else 0


def z7_y4(x, r):
    """K0980: H(r;(x,4);7), x>=4."""
    if r == 0:
        return 0
    if x in (4, 5, 6, 8, 9, 10):
        t = r in (1, 3, 5, 7)
    elif x == 7:
        t = r in (1, 3, 5, 7, 13)
    elif x == 11:
        t = r in (1, 3, 5, 7, 15)
    elif x == 12:
        t = r in (1, 3, 5, 7, 15) or odd(r, 17, 23)
    else:
        t = r in (1, 3, 5, 7, 15)

    if x == 4:
        p = r in (8, 10)
    elif x == 5:
        p = r in (8, 10) or at_least(r, 12)
    elif x in (6, 8):
        p = r in (8, 10, 12)
    elif x in (7, 9):
        p = r in (8, 10, 12) or at_least(r, 14)
    elif x in (10, 12):
        p = r in (8, 10, 12, 14)
    elif x == 11:
        p = r in (8, 10, 12, 14) or at_least(r, 16)
    elif x >= 13 and x % 2 == 0:
        p = r in (8, 10, 12, 14) or odd(r, 17, x + 11)
    else:
        p = (r in (8, 10, 12, 14)
             or odd(r, 17, x + 10)
             or at_least(r, x + 12))
    return 2 if t else 1 if p else 0


def candidate(x, r):
    """Claimed closed form H(r;(x,4);8), x>=4."""
    if r == 0:
        return 0

    if x == 4:
        t = r in (1, 3, 5, 7, 9, 11)
    elif x == 5:
        t = r in (1, 3, 5, 7)
    elif x == 6:
        t = r in (1, 3, 5, 7, 13)
    elif 7 <= x <= 9:
        t = r in (1, 3, 5, 7)
    elif x == 10:
        t = r in (1, 3, 5, 7, 15)
    elif x in (11, 12):
        t = r in (1, 3, 5, 7)
    elif x == 13:
        t = r in (1, 3, 5, 7) or odd(r, 17, 25)
    else:
        t = r in (1, 3, 5, 7, 17)

    if x == 4:
        p = False
    elif x in (5, 7):
        p = r in (9, 11, 13) or at_least(r, 14)
    elif x == 6:
        p = r in (9, 11)
    elif x == 8:
        p = r in (9, 11, 13)
    elif x in (9, 11):
        p = r in (9, 11, 13, 15) or at_least(r, 16)
    elif x == 10:
        p = r in (9, 11, 13)
    elif x == 12:
        p = r in (9, 11, 13, 15)
    elif x >= 13 and x % 2 == 0:
        p = r in (9, 11, 13, 15) or even(r, 18, x + 12)
    else:
        p = (r in (9, 11, 13, 15)
             or even(r, 18, x + 11)
             or at_least(r, x + 13))
    return 2 if t else 1 if p else 0


def make_engine(canonical):
    """Direct mex recursion; the two modes use different state encodings."""
    @lru_cache(None)
    def h(r, tokens, z):
        if r == 0:
            return 0
        state = tuple(sorted(tokens, reverse=True)) if canonical else tokens
        options = set()
        seen = set()
        for i, value in enumerate(state):
            if canonical and value in seen:
                continue
            seen.add(value)
            child = list(state)
            if value > 1:
                child[i] -= 1
                if canonical:
                    child.sort(reverse=True)
                options.add(h(r - 1, tuple(child), z))
            else:
                child.pop(i)
                if canonical:
                    child.sort(reverse=True)
                options.add(h(r - 1, tuple(child), z + 1))
        if z:
            options.add(1 ^ h(r - 1, state, z - 1))
        return mex(options)
    return h


def single_token(x, z, r):
    """K0832 single-token closed form used for the R<=z+1 collapse check."""
    if r == 0 or x <= 0:
        return 0
    qodd = z if z % 2 else z - 1
    length = x + z + 1
    if z == 0:
        return min(r, x) % 2
    if z == x:
        if r % 2 and r <= 2 * x - 1:
            return 2
        if r % 2 == 0 and r <= x - 1:
            return 0
        return x % 2
    if 1 <= z <= x - 1:
        if r <= qodd:
            return 2 if r % 2 else 0
        if qodd < r < length - 1:
            return (r + z) % 2
        return x % 2
    if z >= x + 1:
        qodd = x if x % 2 else x - 1
        if r <= qodd:
            return 2 if r % 2 else 0
        return x % 2
    raise ValueError("unhandled single-token parameters")


def bands_for(x):
    """(parity, lower, upper, child-value-set signature), 1<=R<=x+12."""
    if x == 4:
        return [(1, 1, 11, "01"), (1, 13, 15, "1"),
                (0, 2, 8, "23"), (0, 10, 16, "1")]
    if x == 5:
        return [(1, 1, 7, "01"), (1, 9, 17, "0"),
                (0, 2, 8, "23"), (0, 10, 12, "12"),
                (0, 14, 16, "0")]
    if x == 6:
        return [(1, 1, 7, "01"), (1, 9, 11, "0"),
                (1, 13, 13, "01"), (1, 15, 17, "1"),
                (0, 2, 8, "23"), (0, 10, 18, "1")]
    if x == 7:
        return [(1, 1, 7, "01"), (1, 9, 19, "0"),
                (0, 2, 8, "23"), (0, 10, 12, "1"),
                (0, 14, 14, "023"), (0, 16, 18, "0")]
    if x == 8:
        return [(1, 1, 7, "01"), (1, 9, 13, "0"),
                (1, 15, 19, "1"), (0, 2, 8, "23"),
                (0, 10, 20, "1")]
    if x == 9:
        return [(1, 1, 7, "01"), (1, 9, 21, "0"),
                (0, 2, 8, "23"), (0, 10, 12, "1"),
                (0, 14, 14, "12"), (0, 16, 20, "0")]
    if x == 10:
        return [(1, 1, 7, "01"), (1, 9, 13, "0"),
                (1, 15, 15, "01"), (1, 17, 21, "1"),
                (0, 2, 8, "23"), (0, 10, 22, "1")]
    if x == 11:
        return [(1, 1, 7, "01"), (1, 9, 23, "0"),
                (0, 2, 8, "23"), (0, 10, 14, "1"),
                (0, 16, 16, "023"), (0, 18, 22, "0")]
    if x == 12:
        return [(1, 1, 7, "01"), (1, 9, 15, "0"),
                (1, 17, 23, "1"), (0, 2, 8, "23"),
                (0, 10, 14, "1"), (0, 16, 24, "123")]
    if x == 13:
        return [(1, 1, 7, "01"), (1, 9, 15, "0"),
                (1, 17, 25, "01"), (0, 2, 8, "23"),
                (0, 10, 14, "1"), (0, 16, 16, "123"),
                (0, 18, 24, "0")]
    if x == 14:
        return [(1, 1, 7, "01"), (1, 9, 15, "0"),
                (1, 17, 17, "01"), (1, 19, 25, "1"),
                (0, 2, 8, "23"), (0, 10, 14, "1"),
                (0, 16, 16, "123"), (0, 18, 18, "02"),
                (0, 20, 26, "02")]
    return [(1, 1, 7, "01"), (1, 9, 15, "0"),
            (1, 17, 17, "01"), (1, 19, x + 12, "1"),
            (0, 2, 8, "23"), (0, 10, 14, "1"),
            (0, 16, 16, "123"), (0, 18, 18, "02"),
            (0, 20, x + 12, "0")]


def option_values(x, r):
    child_r = r - 1
    a = z8_y3(4, child_r) if x == 4 else candidate(x - 1, child_r)
    b = z8_y3(x, child_r)
    c = 1 ^ z7_y4(x, child_r)
    return (a, b, c)


def signature(x, r):
    return "".join(str(v) for v in sorted(set(option_values(x, r))))


def audit_once():
    ordered = make_engine(False)
    canonical = make_engine(True)
    direct_checks = direct_bad = 0
    for x in range(4, 61):
        for r in range(0, x + 41):
            expected = candidate(x, r)
            for engine in (ordered, canonical):
                direct_checks += 1
                if engine(r, (x, 4), 8) != expected:
                    direct_bad += 1

    anchor = make_engine(False)
    anchor_checks = anchor_bad = 0
    for x in range(3, 61):
        for r in range(0, x + 41):
            anchor_checks += 1
            if anchor(r, (x, 3), 8) != z8_y3(x, r):
                anchor_bad += 1
            if x >= 4:
                anchor_checks += 1
                if anchor(r, (x, 4), 7) != z7_y4(x, r):
                    anchor_bad += 1

    signature_checks = mex_checks = 0
    coverage_bad = signature_bad = mex_bad = 0
    odd_parent_checks = even_parent_checks = 0
    for x in range(4, 2001):
        bands = bands_for(x)
        for r in range(1, x + 13):
            signature_checks += 1
            matches = [row for row in bands
                       if row[0] == r % 2 and row[1] <= r <= row[2]]
            if len(matches) != 1:
                coverage_bad += 1
                continue
            actual = signature(x, r)
            if actual != matches[0][3]:
                signature_bad += 1
            value = mex(int(ch) for ch in actual)
            mex_checks += 1
            if value != candidate(x, r):
                mex_bad += 1
            if r % 2:
                odd_parent_checks += 1
                if any(ch not in "01" for ch in actual) or value > 2:
                    signature_bad += 1
            else:
                even_parent_checks += 1
                if value > 1:
                    signature_bad += 1

    tail_checks = tail_bad = 0
    for x in range(4, 5001):
        for offset in range(4):
            r = x + 13 + offset
            tail_checks += 1
            if candidate(x, r) != (x + 4) % 2:
                tail_bad += 1

    tail_signature_checks = tail_signature_bad = 0
    for x in range(4, 2001):
        for offset in range(4):
            r = x + 13 + offset
            tail_signature_checks += 1
            if signature(x, r) != str((x + 3) % 2):
                tail_signature_bad += 1

    theorem_checks = theorem_bad = 0
    for x in range(4, 2001):
        for r in range(0, x + 25):
            theorem_checks += 1
            value = candidate(x, r)
            if value not in (0, 1, 2):
                theorem_bad += 1
            if r % 2 == 0 and value > 1:
                theorem_bad += 1
            if value == 2 and r % 2 == 0:
                theorem_bad += 1

    height_checks = height_bad = 0
    for x in range(4, 501):
        for r in range(0, 10):
            height_checks += 1
            if candidate(x, r) != single_token(x + 4, 8, r):
                height_bad += 1

    counts = {
        "direct_formula_two_engines": direct_checks,
        "independent_z8y3_z7y4_anchor_direct": anchor_checks,
        "signature_coverage_identity": signature_checks,
        "mex_identity": mex_checks,
        "odd_parent_bound": odd_parent_checks,
        "even_parent_bound": even_parent_checks,
        "tail_formula": tail_checks,
        "tail_signature": tail_signature_checks,
        "Theorem_T_grid": theorem_checks,
        "height_only_collapse": height_checks,
    }
    failures = {
        "direct": direct_bad,
        "anchors": anchor_bad,
        "coverage": coverage_bad,
        "signature": signature_bad,
        "mex": mex_bad,
        "tail": tail_bad,
        "tail_signature": tail_signature_bad,
        "Theorem_T": theorem_bad,
        "height_only": height_bad,
    }
    return {
        "all_pass": all(value == 0 for value in failures.values()),
        "counts": counts,
        "failures": failures,
        "state_counts": {
            "ordered_target": ordered.cache_info().currsize,
            "canonical_target": canonical.cache_info().currsize,
            "ordered_anchor": anchor.cache_info().currsize,
        },
        "scope": {
            "direct_target": "4<=x<=60, 0<=R<=x+40; ordered and canonical engines",
            "anchor_direct": "z=8,y=3 for 3<=x<=60 and z=7,y=4 for 4<=x<=60, 0<=R<=x+40",
            "signature": "4<=x<=2000, 1<=R<=x+12",
            "tail": "4<=x<=5000, R=x+13..x+16",
            "tail_signature": "4<=x<=2000, R=x+13..x+16",
            "Theorem_T": "4<=x<=2000, 0<=R<=x+24",
            "height_only": "4<=x<=500, 0<=R<=9",
        },
        "target": "H(R;(x,4);8), x>=4, R>=0",
        "total_checks": sum(counts.values()),
    }


def run():
    first = audit_once()
    second = audit_once()
    same = (json.dumps(first, ensure_ascii=False, sort_keys=True,
                       separators=(",", ":"))
            == json.dumps(second, ensure_ascii=False, sort_keys=True,
                          separators=(",", ":")))
    base = dict(first, repeat_runs=2, repeat_byte_identical=same)
    raw = json.dumps(base, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":")).encode()
    result = dict(base, sha256_without_hash_field=hashlib.sha256(raw).hexdigest())
    out = Path(__file__).with_name("output")
    out.mkdir(exist_ok=True)
    (out / "audit.json").write_text(
        json.dumps(result, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
        encoding="utf-8",
    )
    print(json.dumps({
        "all_pass": result["all_pass"],
        "counts": result["counts"],
        "failures": result["failures"],
        "repeat_byte_identical": same,
        "sha256_without_hash_field": result["sha256_without_hash_field"],
        "total_checks": result["total_checks"],
        "state_counts": result["state_counts"],
    }, ensure_ascii=False, sort_keys=True))
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
