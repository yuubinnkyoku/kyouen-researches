#!/usr/bin/env python3
"""Exhaustive small-state audit for the t=1 fixed-terminal-length theorem."""
from functools import lru_cache
from itertools import product
import json
from pathlib import Path


def audit_parameter(w: int, m: int, q: int) -> dict:
    r = min(w, q - 1)

    @lru_cache(maxsize=None)
    def grundy(c: tuple[int, ...]) -> int:
        occupied = sum(x > 0 for x in c)
        options = set()
        for i, x in enumerate(c):
            if x >= m:
                continue
            if x == 0 and occupied >= r:
                continue
            child = list(c)
            child[i] += 1
            options.add(grundy(tuple(child)))
        mex = 0
        while mex in options:
            mex += 1
        return mex

    checked = 0
    max_grundy = 0
    for c in product(range(m + 1), repeat=w):
        if sum(x > 0 for x in c) > r:
            continue
        actual = grundy(c)
        predicted = (r * m - sum(c)) % 2
        assert actual == predicted, (w, m, q, c, actual, predicted)
        checked += 1
        max_grundy = max(max_grundy, actual)

    return {
        "w": w,
        "m": m,
        "q": q,
        "r": r,
        "safe_states": checked,
        "max_grundy": max_grundy,
        "recursive_states": grundy.cache_info().currsize,
    }


def main() -> None:
    rows = [
        audit_parameter(w, m, q)
        for w in range(1, 6)
        for m in range(1, 5)
        for q in range(1, w + 3)
    ]
    result = {
        "schema": "vertical-fiber-t1-fixed-length-grundy-audit-v1",
        "method": "direct recursive mex on every safe occupancy vector",
        "ranges": {
            "w": [1, 5],
            "m": [1, 4],
            "q": "1..w+2 for each w",
        },
        "parameter_count": len(rows),
        "safe_state_parameter_checks": sum(row["safe_states"] for row in rows),
        "mismatch_count": 0,
        "observed_grundy_values": sorted({0, 1}),
        "per_parameter": rows,
    }
    out = Path(__file__).resolve().parents[1] / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        "PASS: "
        f"{result['parameter_count']} parameter sets, "
        f"{result['safe_state_parameter_checks']} safe-state checks, "
        "0 mismatches"
    )


if __name__ == "__main__":
    main()
