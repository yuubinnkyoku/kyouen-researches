#!/usr/bin/env python3
"""Independent audit for the t=2, q=2w-1 pure-fiber Grundy theorem.

Only the Python standard library is used.  The proof is in report.md; this
program checks the labelled game, a separately generated canonical game,
and the residual recurrence on a wide finite parameter box.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import combinations_with_replacement, product
from pathlib import Path
import hashlib
import json


def theorem_value(w: int, m: int, state: tuple[int, ...]) -> int:
    """Closed form for one safe labelled occupancy vector."""
    if m == 1:
        return 0 if w == 1 else (w - sum(state)) & 1

    saturated = [c for c in state if c >= 2]
    singletons = sum(c == 1 for c in state)
    s = len(saturated)
    R = 2 * w - 2 - 2 * s - singletons
    assert R >= 0
    assert (R - singletons) % 2 == 0
    assert w - s - singletons == 1 + (R - singletons) // 2

    chain_xor = 0
    for c in saturated:
        chain_xor ^= (m - c) & 1

    if m % 2 == 0:
        residual = R & 1
    elif R == 0:
        residual = 0
    elif R == 1:
        residual = 2 if singletons == 1 else 0
    else:
        residual = int((singletons - R) % 4 == 0)
    return chain_xor ^ residual


def audit_labelled_pair(w: int, m: int) -> dict:
    """Direct labelled-vector recursion; no symmetry quotient is used."""
    cap = 2 * w - 2

    @lru_cache(None)
    def grundy(c: tuple[int, ...]) -> int:
        options = set()
        for i in range(w):
            if c[i] == m:
                continue
            child = list(c)
            child[i] += 1
            child = tuple(child)
            if sum(min(v, 2) for v in child) <= cap:
                options.add(grundy(child))
        mex = 0
        while mex in options:
            mex += 1
        return mex

    states = 0
    histogram = [0, 0, 0, 0]
    for c in product(range(m + 1), repeat=w):
        if sum(min(v, 2) for v in c) > cap:
            continue
        states += 1
        actual = grundy(c)
        expected = theorem_value(w, m, c)
        if actual != expected:
            return {
                "ok": False, "w": w, "m": m, "state": list(c),
                "actual": actual, "expected": expected,
            }
        histogram[actual] += 1

    return {
        "ok": True, "w": w, "m": m, "states": states,
        "memo_states": grundy.cache_info().currsize,
        "grundy_histogram": histogram,
    }


def audit_canonical_pair(w: int, m: int) -> dict:
    """Independent recursion on descending positive occupancy multisets."""
    cap = 2 * w - 2

    @lru_cache(None)
    def grundy(c: tuple[int, ...]) -> int:
        options = set()

        # A zero column is represented by the implicit length bound w.
        if len(c) < w:
            child = tuple(sorted(c + (1,), reverse=True))
            if sum(min(v, 2) for v in child) <= cap:
                options.add(grundy(child))

        # Increment one occupied column; duplicate child multisets collapse.
        for i, value in enumerate(c):
            if value == m:
                continue
            child = list(c)
            child[i] += 1
            child = tuple(sorted(child, reverse=True))
            if sum(min(v, 2) for v in child) <= cap:
                options.add(grundy(child))

        mex = 0
        while mex in options:
            mex += 1
        return mex

    states = 0
    histogram = [0, 0, 0, 0]
    for length in range(w + 1):
        for ascending in combinations_with_replacement(range(1, m + 1), length):
            c = tuple(reversed(ascending))
            if sum(min(v, 2) for v in c) > cap:
                continue
            states += 1
            labelled = c + (0,) * (w - length)
            actual = grundy(c)
            expected = theorem_value(w, m, labelled)
            if actual != expected:
                return {
                    "ok": False, "w": w, "m": m, "state": list(c),
                    "actual": actual, "expected": expected,
                }
            histogram[actual] += 1

    return {
        "ok": True, "w": w, "m": m, "states": states,
        "memo_states": grundy.cache_info().currsize,
        "grundy_histogram": histogram,
    }


@lru_cache(None)
def residual_mex(p: int, e: int, ell: int, R: int) -> int:
    """The residual game H_p(e,ell,R), computed directly from its moves."""
    if R == 0 or e + ell == 0:
        return 0
    options = set()
    if e:
        options.add(residual_mex(p, e - 1, ell + 1, R - 1))
    if ell:
        options.add(p ^ residual_mex(p, e, ell - 1, R - 1))
    mex = 0
    while mex in options:
        mex += 1
    return mex


def residual_formula(p: int, ell: int, R: int) -> int:
    if p == 0:
        return R & 1
    if R == 0:
        return 0
    if R == 1:
        return 2 if ell == 1 else 0
    return int((ell - R) % 4 == 0)


def audit_residual(max_width: int = 120) -> dict:
    """Check every reachable residual state for 1<=w<=max_width."""
    checks = 0
    histogram = [0, 0, 0]
    for w in range(1, max_width + 1):
        for R in range(0, 2 * w - 1):
            for ell in range(R + 3):
                if (R - ell) & 1:
                    continue
                e = 1 + (R - ell) // 2
                s = w - e - ell
                if e < 0 or s < 0:
                    continue
                for p in (0, 1):
                    actual = residual_mex(p, e, ell, R)
                    expected = residual_formula(p, ell, R)
                    checks += 1
                    if actual != expected:
                        return {
                            "ok": False, "w": w, "p": p, "e": e,
                            "ell": ell, "R": R,
                            "actual": actual, "expected": expected,
                        }
                    histogram[actual] += 1
    return {
        "ok": True, "max_width": max_width, "checks": checks,
        "grundy_histogram": histogram,
        "memo_states": residual_mex.cache_info().currsize,
    }


def audit_height_one(max_width: int = 14) -> dict:
    """Check the separate m=1 fixed-terminal-length case."""
    checks = 0
    for w in range(1, max_width + 1):
        cap = 2 * w - 2

        @lru_cache(None)
        def grundy(c: tuple[int, ...]) -> int:
            options = set()
            for i in range(w):
                if c[i] == 1:
                    continue
                child = list(c)
                child[i] = 1
                child = tuple(child)
                if sum(child) <= cap:
                    options.add(grundy(child))
            mex = 0
            while mex in options:
                mex += 1
            return mex

        for c in product((0, 1), repeat=w):
            if sum(c) > cap:
                continue
            checks += 1
            actual = grundy(c)
            expected = 0 if w == 1 else (w - sum(c)) & 1
            if actual != expected:
                return {
                    "ok": False, "w": w, "state": list(c),
                    "actual": actual, "expected": expected,
                }
    return {"ok": True, "max_width": max_width, "checks": checks}


def main() -> None:
    labelled_pairs = (
        [(w, m) for w in range(1, 6) for m in range(2, 8)]
        + [(6, m) for m in range(2, 9)]
        + [(7, m) for m in range(2, 6)]
    )
    canonical_pairs = [(w, m) for w in range(1, 9) for m in range(2, 13)]

    labelled = [audit_labelled_pair(w, m) for w, m in labelled_pairs]
    canonical = [audit_canonical_pair(w, m) for w, m in canonical_pairs]
    residual = audit_residual()
    height_one = audit_height_one()

    assert all(row["ok"] for row in labelled)
    assert all(row["ok"] for row in canonical)
    assert residual["ok"] and height_one["ok"]

    def merged_hist(rows: list[dict]) -> list[int]:
        return [sum(row["grundy_histogram"][i] for row in rows) for i in range(4)]

    payload = {
        "theorem": "t=2, q=2w-1, all safe pure-fiber positions",
        "all_ok": True,
        "labelled": {
            "parameter_pairs": len(labelled),
            "width_range": [1, 7],
            "height_ranges": "w=1..5:m=2..7; w=6:m=2..8; w=7:m=2..5",
            "states": sum(row["states"] for row in labelled),
            "grundy_histogram": merged_hist(labelled),
        },
        "canonical": {
            "parameter_pairs": len(canonical),
            "width_range": [1, 8],
            "height_range": [2, 12],
            "states": sum(row["states"] for row in canonical),
            "grundy_histogram": merged_hist(canonical),
        },
        "residual_recurrence": residual,
        "height_one": height_one
    }
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "all_ok": True,
        "labelled_pairs": len(labelled),
        "labelled_states": payload["labelled"]["states"],
        "canonical_pairs": len(canonical),
        "canonical_states": payload["canonical"]["states"],
        "residual_checks": residual["checks"],
        "height_one_checks": height_one["checks"],
        "audit_sha256": hashlib.sha256(out.read_bytes()).hexdigest(),
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
