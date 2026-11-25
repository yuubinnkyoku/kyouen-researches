#!/usr/bin/env python3
"""Independent finite audit for the t=3, q=3w-1 pure-fiber Grundy theorem."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
OUT = HERE / "output" / "audit.json"


def mex(values: set[int]) -> int:
    g = 0
    while g in values:
        g += 1
    return g


def small_h1(e0: int, e1: int, e2: int) -> int | None:
    n = e0 + e1 + e2
    if n == 1:
        return {(1, 0, 0): 1, (0, 1, 0): 0}.get((e0, e1, e2))
    if n == 2:
        return {
            (2, 0, 0): 0, (1, 1, 0): 2, (1, 0, 1): 1,
            (0, 2, 0): 0, (0, 1, 1): 2, (0, 0, 2): 0,
        }.get((e0, e1, e2))
    if n == 3:
        return {
            (3, 0, 0): 0, (2, 1, 0): 1, (2, 0, 1): 0,
            (1, 2, 0): 0, (1, 1, 1): 1, (1, 0, 2): 2,
            (0, 3, 0): 1, (0, 2, 1): 0, (0, 1, 2): 1,
            (0, 0, 3): 0,
        }.get((e0, e1, e2))
    return None


def formula(state: tuple[int, ...], m: int, w: int) -> int:
    if m == 1:
        ans = 0
        for c in state:
            ans ^= (1 - c) & 1
        return ans
    if m == 2:
        if w >= 2:
            ans = 0
            for c in state:
                ans ^= (2 - c) & 1
            return ans
        return (1 - state[0]) & 1

    chain_xor = 0
    e = [0, 0, 0]
    for c in state:
        if c >= 3:
            chain_xor ^= (m - c) & 1
        else:
            e[c] += 1
    e0, e1, e2 = e
    L = 3 * e0 + 2 * e1 + e2
    assert L >= 2, (state, w, e, L)
    if m & 1:
        residual = (L - 2) & 1
    else:
        n = e0 + e1 + e2
        residual = (e1 & 1) if n >= 4 else small_h1(e0, e1, e2)
        assert residual is not None, (state, w, e, L, n)
    return chain_xor ^ residual


def safe(state: tuple[int, ...], w: int) -> bool:
    return sum(min(c, 3) for c in state) <= 3 * w - 2


def run_multiset(w: int, m: int) -> dict:
    mismatches: list[tuple] = []
    max_seen = 0

    @lru_cache(None)
    def grundy(state: tuple[int, ...]) -> int:
        nonlocal max_seen
        options: set[int] = set()
        for value in sorted(set(state)):
            if value >= m:
                continue
            child = list(state)
            child[child.index(value)] = value + 1
            child_state = tuple(sorted(child))
            if safe(child_state, w):
                options.add(grundy(child_state))
        value = mex(options)
        expected = formula(state, m, w)
        max_seen = max(max_seen, value)
        if value != expected and len(mismatches) < 5:
            mismatches.append((state, value, expected))
        return value

    root = grundy((0,) * w)
    return {
        "states": grundy.cache_info().currsize,
        "root": root,
        "max_seen": max_seen,
        "mismatches": mismatches,
    }


def run_labelled(w: int, m: int) -> dict:
    mismatches: list[tuple] = []
    max_seen = 0

    @lru_cache(None)
    def grundy(state: tuple[int, ...]) -> int:
        nonlocal max_seen
        options: set[int] = set()
        for i, value in enumerate(state):
            if value >= m:
                continue
            child = list(state)
            child[i] += 1
            child_state = tuple(child)
            if safe(child_state, w):
                options.add(grundy(child_state))
        value = mex(options)
        expected = formula(state, m, w)
        max_seen = max(max_seen, value)
        if value != expected and len(mismatches) < 5:
            mismatches.append((state, value, expected))
        return value

    root = grundy((0,) * w)
    return {
        "states": grundy.cache_info().currsize,
        "root": root,
        "max_seen": max_seen,
        "mismatches": mismatches,
    }


def residual_recurrence(z: int):
    @lru_cache(None)
    def h(e0: int, e1: int, e2: int) -> int:
        L = 3 * e0 + 2 * e1 + e2
        assert L >= 2
        if L == 2:
            return 0
        options: set[int] = set()
        if e0:
            options.add(h(e0 - 1, e1 + 1, e2))
        if e1:
            options.add(h(e0, e1 - 1, e2 + 1))
        if e2:
            options.add(z ^ h(e0, e1, e2 - 1))
        return mex(options)
    return h


def build_audit() -> dict:
    multiset_runs = []
    multiset_states = 0
    multiset_bad = 0
    multiset_max = 0
    for w in range(1, 11):
        for m in range(3, 13):
            result = run_multiset(w, m)
            multiset_states += result["states"]
            multiset_bad += len(result["mismatches"])
            multiset_max = max(multiset_max, result["max_seen"])
            multiset_runs.append({
                "w": w, "m": m, "states": result["states"],
                "root": result["root"], "max": result["max_seen"],
            })
            if result["mismatches"]:
                raise AssertionError(("multiset", w, m, result["mismatches"]))

    labelled_runs = []
    labelled_states = 0
    labelled_bad = 0
    labelled_max = 0
    for w in range(1, 6):
        for m in range(1, 9):
            result = run_labelled(w, m)
            labelled_states += result["states"]
            labelled_bad += len(result["mismatches"])
            labelled_max = max(labelled_max, result["max_seen"])
            labelled_runs.append({
                "w": w, "m": m, "states": result["states"],
                "root": result["root"], "max": result["max_seen"],
            })
            if result["mismatches"]:
                raise AssertionError(("labelled", w, m, result["mismatches"]))

    residual_cases = 0
    residual_bad = 0
    residual_max = 0
    for z in (0, 1):
        h = residual_recurrence(z)
        for e0 in range(16):
            for e1 in range(16 - e0):
                for e2 in range(16 - e0 - e1):
                    L = 3 * e0 + 2 * e1 + e2
                    if L < 2:
                        continue
                    actual = h(e0, e1, e2)
                    if z == 0:
                        expected = (L - 2) & 1
                    else:
                        n = e0 + e1 + e2
                        expected = (e1 & 1) if n >= 4 else small_h1(e0, e1, e2)
                    residual_cases += 1
                    residual_max = max(residual_max, actual)
                    if actual != expected:
                        residual_bad += 1
                        raise AssertionError(("residual", z, e0, e1, e2, actual, expected))

    return {
        "item": "K0927",
        "title": "t=3, q=3w-1: all-safe-position Grundy classification",
        "scope": "pure fiber game, degree threshold t=3, width w>=1, height m>=1, q=3w-1",
        "checks": [
            {
                "name": "labelled direct recurrence versus closed form",
                "parameter_pairs": len(labelled_runs),
                "states": labelled_states,
                "mismatches": labelled_bad,
                "maximum_seen": labelled_max,
                "range": "w=1..5, m=1..8",
            },
            {
                "name": "canonical-multiset direct recurrence versus closed form",
                "parameter_pairs": len(multiset_runs),
                "states": multiset_states,
                "mismatches": multiset_bad,
                "maximum_seen": multiset_max,
                "range": "w=1..10, m=3..12",
            },
            {
                "name": "residual recurrence versus residual closed form",
                "states": residual_cases,
                "mismatches": residual_bad,
                "maximum_seen": residual_max,
                "range": "z=0,1; e0+e1+e2<=15; 3e0+2e1+e2>=2",
            },
        ],
        "totals": {
            "direct_states": labelled_states + multiset_states,
            "residual_states": residual_cases,
            "all_checks": labelled_states + multiset_states + residual_cases,
            "mismatches": labelled_bad + multiset_bad + residual_bad,
            "parameter_pairs": len(labelled_runs) + len(multiset_runs),
        },
        "residual_table_z1": [
            {"e0": e0, "e1": e1, "e2": e2, "H": small_h1(e0, e1, e2)}
            for n in (1, 2, 3)
            for e0 in range(n + 1)
            for e1 in range(n - e0 + 1)
            for e2 in (n - e0 - e1,)
            if 3 * e0 + 2 * e1 + e2 >= 2
        ],
        "all_ok": True,
        "finite_audit_is_not_the_universal_proof": True,
    }


def main() -> int:
    audit = build_audit()
    blob = json.dumps(audit, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(blob, encoding="utf-8")
    digest = hashlib.sha256(blob.encode("utf-8")).hexdigest()
    print("all_ok =", audit["all_ok"])
    print("totals =", audit["totals"])
    print("sha256 =", digest)
    print("bytes =", len(blob.encode("utf-8")))
    return 0 if audit["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
