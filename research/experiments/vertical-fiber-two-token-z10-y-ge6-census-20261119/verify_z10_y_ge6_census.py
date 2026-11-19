#!/usr/bin/env python3
"""Finite independent census for the conjectural z=10, y>=6 two-token formula.

This script does not prove the unbounded conjecture. It compares a candidate
closed form with two separately represented direct mex recurrences:
  * ordered: preserve the token tuple order;
  * canonical: sort the token tuple after every token move.
The low-y scan is deliberately outside the conjectured range and records where
the same formula first fails.
"""
from __future__ import annotations

import hashlib
import json
from functools import lru_cache
from pathlib import Path


def mex(values: set[int]) -> int:
    n = 0
    while n in values:
        n += 1
    return n


def odd(r: int, lo: int, hi: int) -> bool:
    return r % 2 == 1 and lo <= r <= hi


def even(r: int, lo: int, hi: int) -> bool:
    return r % 2 == 0 and lo <= r <= hi


def make_engine(canonical: bool):
    @lru_cache(maxsize=None)
    def grundy(R: int, tokens: tuple[int, ...], z: int) -> int:
        if R == 0:
            return 0
        options: set[int] = set()
        for i, value in enumerate(tokens):
            if value > 1:
                child = tokens[:i] + (value - 1,) + tokens[i + 1 :]
                if canonical:
                    child = tuple(sorted(child, reverse=True))
                options.add(grundy(R - 1, child, z))
            else:
                child = tokens[:i] + tokens[i + 1 :]
                if canonical:
                    child = tuple(sorted(child, reverse=True))
                options.add(grundy(R - 1, child, z + 1))
        if z:
            options.add(1 ^ grundy(R - 1, tokens, z - 1))
        return mex(options)

    return grundy


def candidate(x: int, y: int, R: int) -> int:
    """Conjectural formula for all x>=y>=6 and R>=0."""
    d = x - y
    S = x + y
    tail = S + 11
    if R == 0:
        return 0
    if R >= tail:
        return S % 2

    # Grundy value 2 locus.
    in_T = R in (1, 3, 5, 7, 9)
    if d in (0, 4, 8):
        in_T = in_T or R == 2 * y + 5 + d // 2
    elif d == 11:
        in_T = in_T or odd(R, 2 * y + 11, S + 10)
    elif d >= 12:
        in_T = in_T or R == 2 * y + 11
    if in_T:
        return 2

    # Grundy value 1 locus.
    if d % 2 == 0:
        if d <= 10:
            upper = 2 * y + 3 + 2 * ((d + 3) // 4)  # ceil(d/4)
            in_P = odd(R, 11, upper)
        else:
            in_P = odd(R, 11, 2 * y + 9) or even(R, 2 * y + 12, S + 10)
    elif d <= 9:
        lower = 2 * y + 6 + 2 * ((d + 1) // 4)
        in_P = odd(R, 11, S + 10) or even(R, lower, S + 9)
    else:
        in_P = odd(R, 11, 2 * y + 9) or even(R, 2 * y + 12, S + 9)
    return 1 if in_P else 0


def t2_formula(x: int, y: int, R: int) -> bool:
    d = x - y
    S = x + y
    if R in (1, 3, 5, 7, 9):
        return True
    if d in (0, 4, 8) and R == 2 * y + 5 + d // 2:
        return True
    if d == 11 and odd(R, 2 * y + 11, S + 10):
        return True
    return d >= 12 and R == 2 * y + 11


def audit_once() -> dict:
    ordered = make_engine(canonical=False)
    canonical = make_engine(canonical=True)
    direct_checks = 0
    tail_checks = 0
    value2_checks = 0
    failures: list[list[object]] = []
    nimber_histogram = {"0": 0, "1": 0, "2": 0, ">2": 0}
    parity_points = {"even_parent": 0, "odd_parent": 0}

    for y in range(6, 29):
        for d in range(97):
            x = y + d
            S = x + y
            for R in range(S + 20):
                actual_ordered = ordered(R, (x, y), 10)
                actual_canonical = canonical(R, tuple(sorted((x, y), reverse=True)), 10)
                expected = candidate(x, y, R)
                direct_checks += 1
                if actual_ordered != actual_canonical or actual_ordered != expected:
                    failures.append([
                        "direct", y, d, R,
                        actual_ordered, actual_canonical, expected
                    ])

                nimber_histogram[str(actual_ordered) if actual_ordered <= 2 else ">2"] += 1
                if (actual_ordered == 2) != t2_formula(x, y, R):
                    failures.append(["T2-locus", y, d, R, actual_ordered])
                if actual_ordered == 2:
                    value2_checks += 1

                if R % 2 == 0:
                    parity_points["even_parent"] += 1
                    if actual_ordered > 1:
                        failures.append(["even-parent-bound", y, d, R, actual_ordered])
                else:
                    parity_points["odd_parent"] += 1
                    if actual_ordered > 2:
                        failures.append(["odd-parent-bound", y, d, R, actual_ordered])

            # The general tail begins at R=S+z+1=S+11.
            for offset in range(9):
                R = S + 11 + offset
                tail_checks += 1
                actual = ordered(R, (x, y), 10)
                if actual != S % 2:
                    failures.append(["tail", y, d, offset, actual, S % 2])

    # The same candidate is intentionally tested outside its proposed y>=6 range.
    low_y_mismatches: dict[str, dict[str, object]] = {}
    for y in range(1, 6):
        mismatches: list[list[int]] = []
        for d in range(25):
            x = y + d
            S = x + y
            for R in range(S + 20):
                actual = ordered(R, (x, y), 10)
                expected = candidate(x, y, R)
                if actual != expected:
                    mismatches.append([d, R, actual, expected])
        low_y_mismatches[str(y)] = {
            "count": len(mismatches),
            "first": mismatches[:8],
        }

    return {
        "all_pass": not failures,
        "target": "H(R;(x,y);10), x>=y>=6, R>=0",
        "candidate": "T2/P1/tail formula in report",
        "finite_scope": {
            "y": [6, 28],
            "diagonal_offset_d": [0, 96],
            "R": "0 <= R <= x+y+19",
        },
        "counts": {
            "ordered_vs_canonical_vs_formula": direct_checks,
            "tail_offsets_0_through_8": tail_checks,
            "nimber_histogram": nimber_histogram,
            "parent_parity_points": parity_points,
            "value2_locus_points": value2_checks,
        },
        "low_y_boundary_scan": {
            "scope": "1<=y<=5, 0<=d<=24, 0<=R<=x+y+19; compare with the unmodified y>=6 candidate",
            "mismatches": low_y_mismatches,
        },
        "failures": failures[:100],
        "failure_count": len(failures),
        "ordered_cache": ordered.cache_info()._asdict(),
        "canonical_cache": canonical.cache_info()._asdict(),
    }


def run() -> None:
    first = audit_once()
    second = audit_once()
    same = (
        json.dumps(first, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        == json.dumps(second, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    )
    base = dict(first, repeat_runs=2, repeat_byte_identical=same)
    raw = json.dumps(base, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
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
        "failure_count": result["failure_count"],
        "low_y_boundary_scan": result["low_y_boundary_scan"]["mismatches"],
        "repeat_byte_identical": same,
        "sha256_without_hash_field": result["sha256_without_hash_field"],
        "total_checks": sum(v for v in result["counts"].values() if isinstance(v, int)),
    }, ensure_ascii=False, sort_keys=True))
    if not result["all_pass"] or not same:
        raise SystemExit(1)


if __name__ == "__main__":
    run()
