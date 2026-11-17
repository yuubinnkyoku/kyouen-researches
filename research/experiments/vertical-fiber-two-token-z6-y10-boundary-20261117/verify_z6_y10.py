#!/usr/bin/env python3
"""Independent finite audit for the proved two-token residual slice z=6,y=10."""
from __future__ import annotations
import hashlib
import json
import random
import runpy
from pathlib import Path

HERE = Path(__file__).resolve().parent
ANCHOR = runpy.run_path(str(HERE.parent / "vertical-fiber-two-token-z6-y9-boundary-20261117" / "verify_z6_y9.py"))
mex = ANCHOR["mex"]
even = ANCHOR["even"]
odd = ANCHOR["odd"]
exact_ordered = ANCHOR["exact_ordered"]
exact_canonical = ANCHOR["exact_canonical"]
h5 = ANCHOR["h5"]
h6_y9 = ANCHOR["h6_y9"]


def h6_y10(x: int, r: int) -> int:
    if r == 0:
        return 0
    base = {1, 3, 5}
    if x == 10:
        extra = {23}
    elif x == 14:
        extra = {25}
    elif x == 17:
        extra = {27, 29, 31, 33}
    elif x >= 18:
        extra = {27}
    else:
        extra = set()
    if r in base | extra:
        return 2
    if x == 10:
        p = odd(r, 7, 21)
    elif x == 11:
        p = odd(r, 7, 27) or r >= 24
    elif x == 12:
        p = odd(r, 7, 23)
    elif x == 13:
        p = odd(r, 7, 29) or r >= 26
    elif x == 14:
        p = odd(r, 7, 23)
    elif x == 15:
        p = odd(r, 7, 31) or r >= 26
    elif x == 16:
        p = odd(r, 7, 25)
    elif x == 17:
        p = odd(r, 7, 25) or even(r, 28, 34) or r >= 35
    elif x >= 18 and x % 2 == 0:
        p = odd(r, 7, 25) or even(r, 28, x + 16)
    else:
        p = odd(r, 7, 25) or even(r, 28, x + 17) or r >= x + 18
    return int(p)


# Each interval is read only at the parity of its table column.
# The rows cover exactly 1 <= R < x+17.
SMALL_SIGNATURES = {
    10: {1: [(1, 5, "01"), (7, 21, "0"), (23, 23, "01"), (25, 25, "1")],
         0: [(2, 6, "23"), (8, 26, "1")]},
    11: {1: [(1, 5, "01"), (7, 27, "0")],
         0: [(2, 6, "23"), (8, 22, "1"), (24, 24, "023"), (26, 26, "0")]},
    12: {1: [(1, 5, "01"), (7, 23, "0"), (25, 27, "1")],
         0: [(2, 6, "23"), (8, 28, "1")]},
    13: {1: [(1, 5, "01"), (7, 29, "0")],
         0: [(2, 6, "23"), (8, 22, "1"), (24, 24, "12"), (26, 28, "0")]},
    14: {1: [(1, 5, "01"), (7, 23, "0"), (25, 25, "01"), (27, 29, "1")],
         0: [(2, 6, "23"), (8, 30, "1")]},
    15: {1: [(1, 5, "01"), (7, 31, "0")],
         0: [(2, 6, "23"), (8, 24, "1"), (26, 26, "023"), (28, 30, "0")]},
    16: {1: [(1, 5, "01"), (7, 25, "0"), (27, 31, "1")],
         0: [(2, 6, "23"), (8, 24, "1"), (26, 32, "123")]},
    17: {1: [(1, 5, "01"), (7, 25, "0"), (27, 33, "01")],
         0: [(2, 6, "23"), (8, 24, "1"), (26, 26, "123"), (28, 32, "0")]},
    18: {1: [(1, 5, "01"), (7, 25, "0"), (27, 27, "01"), (29, 33, "1")],
         0: [(2, 6, "23"), (8, 24, "1"), (26, 26, "123"), (28, 34, "02")]},
}


def expected_signature(x: int, r: int) -> set[int]:
    if x in SMALL_SIGNATURES:
        rows = SMALL_SIGNATURES[x][r % 2]
    else:
        assert x >= 19
        if r % 2:
            upper = x + 15 if x % 2 == 0 else x + 16
            rows = [(1, 5, "01"), (7, 25, "0"), (27, 27, "01"), (29, upper, "1")]
        else:
            upper = x + 16 if x % 2 == 0 else x + 15
            rows = [(2, 6, "23"), (8, 24, "1"), (26, 26, "123"),
                    (28, 28, "02"), (30, upper, "0")]
    for lo, hi, digits in rows:
        if lo <= r <= hi and (r - lo) % 2 == 0:
            return {int(ch) for ch in digits}
    return set()


def actual_signature(x: int, r: int) -> set[int]:
    a = h6_y9(10, r - 1) if x == 10 else h6_y10(x - 1, r - 1)
    b = h6_y9(x, r - 1)
    c = 1 ^ h5(x, 10, r - 1)
    return {a, b, c}


def predicted_value2_positions(x: int) -> set[int]:
    if x == 10:
        extra = {23}
    elif x == 14:
        extra = {25}
    elif x == 17:
        extra = {27, 29, 31, 33}
    elif x >= 18:
        extra = {27}
    else:
        extra = set()
    return {1, 3, 5} | extra


def run_audit() -> dict:
    failures = []
    direct = 0
    for x in range(10, 61):
        for r in range(x + 36):
            cases = ((6, (x, 10), h6_y10(x, r)),
                     (6, (x, 9), h6_y9(x, r)),
                     (5, (x, 10), h5(x, 10, r)))
            for z, tokens, formula in cases:
                ordered = exact_ordered(r, tokens, z)
                canonical = exact_canonical(r, tuple(sorted(tokens, reverse=True)), z)
                direct += 1
                if ordered != canonical or ordered != formula:
                    failures.append({"kind": "direct-two-engine-anchor", "x": x, "r": r,
                                     "z": z, "tokens": tokens, "ordered": ordered,
                                     "canonical": canonical, "formula": formula})

    signature_checks = mex_checks = odd_checks = even_checks = 0
    family_checks = 0
    for x in range(10, 2001):
        actual_t = set()
        for r in range(1, x + 17):
            options = actual_signature(x, r)
            expected = expected_signature(x, r)
            signature_checks += 1
            if options != expected:
                failures.append({"kind": "signature", "x": x, "r": r,
                                 "actual": sorted(options), "expected": sorted(expected)})
            value = mex(options)
            mex_checks += 1
            if value != h6_y10(x, r):
                failures.append({"kind": "mex", "x": x, "r": r, "options": sorted(options),
                                 "actual": value, "formula": h6_y10(x, r)})
            if value == 2:
                actual_t.add(r)
            if r % 2:
                odd_checks += 1
                if not options <= {0, 1}:
                    failures.append({"kind": "odd-parent-bound", "x": x, "r": r,
                                     "options": sorted(options)})
            else:
                even_checks += 1
                if value > 1:
                    failures.append({"kind": "even-parent-bound", "x": x, "r": r,
                                     "value": value})
        family_checks += 1
        predicted = predicted_value2_positions(x)
        if actual_t != predicted:
            failures.append({"kind": "three-family-specialization", "x": x,
                             "actual": sorted(actual_t), "predicted": sorted(predicted)})

    tail_checks = 0
    for x in range(10, 2001):
        for offset in range(65):
            r = x + 17 + offset
            tail_checks += 1
            if h6_y10(x, r) != (x + 10) % 2:
                failures.append({"kind": "tail", "x": x, "r": r,
                                 "actual": h6_y10(x, r), "expected": (x + 10) % 2})

    rng = random.Random(20261117)
    random_tail_checks = 0
    for _ in range(2000):
        x = rng.randint(10, 100000)
        r = x + 17 + rng.randint(0, 100000)
        random_tail_checks += 1
        if h6_y10(x, r) != (x + 10) % 2:
            failures.append({"kind": "random-tail", "x": x, "r": r})

    counts = {
        "direct_two_engine_formula_anchor_checks": direct,
        "option_signature_checks": signature_checks,
        "mex_identity_checks": mex_checks,
        "odd_parent_option_bound_checks": odd_checks,
        "even_parent_value_bound_checks": even_checks,
        "three_family_value2_specialization_checks": family_checks,
        "tail_checks": tail_checks,
        "fixed_seed_random_tail_checks": random_tail_checks,
    }
    audit = {
        "schema": "two-token-z6-y10-audit-v1",
        "claim": "H(R;(x,10);6) is given by the complete formula for all x>=10,R>=0",
        "classification": "finite-independent-audit-not-proof",
        "counts": counts,
        "total_checks": sum(counts.values()),
        "seed": 20261117,
        "failures": failures,
        "pass": not failures,
    }
    encoded = json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    audit["sha256_without_hash_field"] = hashlib.sha256(encoded.encode("utf-8")).hexdigest()
    return audit


def main() -> None:
    audit = run_audit()
    output = HERE / "output" / "audit.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(audit, ensure_ascii=False, sort_keys=True, indent=2) + "\n",
                      encoding="utf-8")
    print(json.dumps({"pass": audit["pass"], "total_checks": audit["total_checks"],
                      "failures": len(audit["failures"]),
                      "sha256_without_hash_field": audit["sha256_without_hash_field"],
                      "output": str(output)}, ensure_ascii=False, sort_keys=True))
    if not audit["pass"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
