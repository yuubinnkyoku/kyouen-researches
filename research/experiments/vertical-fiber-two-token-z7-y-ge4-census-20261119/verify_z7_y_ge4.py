#!/usr/bin/env python3
"""Finite two-engine census for the conjectured z=7, y>=4 two-token formula.

The census is deliberately not presented as a proof.  It checks every state in
a stated finite box and several points in the already-proved tail.
"""
from collections import Counter
from functools import lru_cache
from pathlib import Path
import gc
import json


Y_MIN, Y_MAX = 4, 80
D_MIN, D_MAX = 0, 50


def in_parity_interval(r, lo, hi, parity):
    return lo <= r <= hi and (r & 1) == parity


def conjectured_value(x, y, r):
    """Candidate H(r;(x,y);7) for x>=y>=4, including the known tail."""
    if r == 0:
        return 0
    s = x + y
    d = x - y
    if r >= s + 8:
        return s & 1

    if r in (1, 3, 5, 7):
        return 2
    if d == 3 and r == 2 * y + 5:
        return 2
    if d == 7 and r == 2 * y + 7:
        return 2
    if d == 8 and in_parity_interval(r, 2 * y + 7, 2 * y + 15, 1):
        return 2
    if d >= 9 and r == 2 * y + 7:
        return 2

    if d == 0:
        one = in_parity_interval(r, 8, 2 * y + 2, 0)
    elif d in (2, 4):
        one = in_parity_interval(r, 8, 2 * y + 4, 0)
    elif d in (6, 8):
        one = in_parity_interval(r, 8, 2 * y + 6, 0)
    elif d == 1:
        one = (in_parity_interval(r, 8, 2 * y + 8, 0)
               or in_parity_interval(r, 2 * y + 5, 2 * y + 7, 1))
    elif d == 3:
        one = (in_parity_interval(r, 8, 2 * y + 10, 0)
               or in_parity_interval(r, 2 * y + 7, 2 * y + 9, 1))
    elif d == 5:
        one = (in_parity_interval(r, 8, 2 * y + 12, 0)
               or in_parity_interval(r, 2 * y + 7, 2 * y + 11, 1))
    elif d == 7:
        one = (in_parity_interval(r, 8, 2 * y + 14, 0)
               or in_parity_interval(r, 2 * y + 9, 2 * y + 13, 1))
    else:  # d >= 9
        one = (in_parity_interval(r, 8, 2 * y + 6, 0)
               or in_parity_interval(
                   r, 2 * y + 9, min(2 * y + 2 * d - 3, s + 7), 1))
    return 1 if one else 0


def run_engine(canonical):
    """Run either sorted-multiset or order-preserving labeled recursion."""
    @lru_cache(maxsize=None)
    def h(r, xs, z):
        if r == 0:
            return 0
        options = set()
        for i, a in enumerate(xs):
            if a >= 2:
                child = list(xs)
                child[i] -= 1
                if canonical:
                    child.sort(reverse=True)
                options.add(h(r - 1, tuple(child), z))
            elif a == 1:
                child = xs[:i] + xs[i + 1:]
                if canonical:
                    child = tuple(sorted(child, reverse=True))
                options.add(h(r - 1, child, z + 1))
        if z >= 1:
            options.add(1 ^ h(r - 1, xs, z - 1))
        mex = 0
        while mex in options:
            mex += 1
        return mex

    counts = Counter()
    mismatches = []
    states = 0
    tail_checks = 0

    for y in range(Y_MIN, Y_MAX + 1):
        for d in range(D_MIN, D_MAX + 1):
            x = y + d
            s = x + y
            initial = (x, y) if canonical else (y, x)
            for r in range(s + 8):
                got = h(r, initial, 7)
                want = conjectured_value(x, y, r)
                counts[str(got)] += 1
                states += 1
                if got != want and len(mismatches) < 10:
                    mismatches.append({
                        "x": x, "y": y, "d": d, "R": r,
                        "actual": got, "candidate": want,
                    })
            for r in (s + 8, s + 9, s + 20):
                got = h(r, initial, 7)
                tail_checks += 1
                if got != (s & 1) and len(mismatches) < 10:
                    mismatches.append({
                        "x": x, "y": y, "d": d, "R": r,
                        "actual": got, "candidate_tail": s & 1,
                    })

    boundary = h(7, (3, 3), 7)
    if boundary != 0 and len(mismatches) < 10:
        mismatches.append({
            "x": 3, "y": 3, "R": 7, "actual": boundary,
            "expected_boundary": 0,
        })

    cache_states = h.cache_info().currsize
    return {
        "engine": "sorted-multiset" if canonical else "ordered-labels",
        "states": states,
        "tail_checks": tail_checks,
        "boundary_checks": 1,
        "mismatches": mismatches,
        "value_counts": dict(sorted(counts.items())),
        "cache_states": cache_states,
        "boundary_actual_H_7_33": boundary,
    }


def main():
    results = []
    results.append(run_engine(canonical=True))
    gc.collect()
    results.append(run_engine(canonical=False))
    gc.collect()

    ok = all(not item["mismatches"] for item in results)
    audit = {
        "schema": "z7-yge4-two-token-census-v1",
        "scope": {
            "z": 7,
            "y": [Y_MIN, Y_MAX],
            "d_x_minus_y": [D_MIN, D_MAX],
            "R": "0..x+y+7 inclusive",
            "tail_points": ["x+y+8", "x+y+9", "x+y+20"],
        },
        "engines": results,
        "total_finite_states": sum(item["states"] for item in results),
        "total_tail_checks": sum(item["tail_checks"] for item in results),
        "total_boundary_checks": sum(item["boundary_checks"] for item in results),
        "result": "PASS" if ok else "FAIL",
        "interpretation": (
            "Finite exact recursion census only; it supports but does not prove "
            "the unbounded conjectured formula."
        ),
    }
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(json.dumps(audit, ensure_ascii=False, indent=2))
    if not ok:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
