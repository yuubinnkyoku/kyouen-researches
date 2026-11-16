#!/usr/bin/env python3
"""Verify the z=4 strong-induction option table and corroborating audits."""
from __future__ import annotations
import hashlib
import json
import sys
from pathlib import Path

# The finite-audit module is a sibling experiment directory, not this one.
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "vertical-fiber-two-token-z4-slice-20261116"))
from verify_z4_conjecture import audit as raw_audit
from verify_z4_conjecture import z4_options_from_closed_forms


def expected_small(x: int, y: int, R: int) -> set[int]:
    if R == 1: return {0, 1}
    if R == 2: return {2, 3}
    if R == 3: return {1} if (x, y) == (1, 1) else {0, 1}
    if R == 4:
        if (x, y) == (1, 1): return {1}
        if (x, y) == (2, 1): return {0, 3}
        return {2, 3}
    raise AssertionError((x, y, R))


def expected_odd(x: int, y: int, R: int) -> set[int]:
    d, S = x - y, x + y
    assert R >= 5 and R & 1
    if d == 0:
        if y == 1: return {1}
        if y == 2: return {0, 1} if R == 5 else {1}
        return {0} if R <= 2 * y + 1 else {1}
    if d in (1, 3): return {0}
    if d == 2:
        if R <= 2 * y + 1: return {0}
        if R == 2 * y + 3: return {0, 1}
        return {1}
    if d == 4: return {0} if R <= 2 * y + 3 else {1}
    if d == 5:
        if R <= 2 * y + 3: return {0}
        if R <= 2 * y + 9: return {0, 1}
        return {0}
    if d == 6:
        if R <= 2 * y + 3: return {0}
        if R == 2 * y + 5: return {0, 1}
        return {1}
    if d >= 7 and d & 1:
        if R <= 2 * y + 3: return {0}
        if R == 2 * y + 5: return {0, 1}
        if R <= S + 4: return {1}
        return {0}
    if d >= 8 and not (d & 1):
        if R <= 2 * y + 3: return {0}
        if R == 2 * y + 5: return {0, 1}
        return {1}
    raise AssertionError((x, y, R, d))


def expected_even_has_zero(x: int, y: int, R: int) -> bool:
    d = x - y
    assert R >= 6 and R % 2 == 0
    if d in (0, 2, 4): return False
    if d in (1, 3): return R >= 2 * y + 4
    if d >= 5 and d & 1: return R >= 2 * y + 6
    if d >= 6 and not (d & 1): return 2 * y + 6 <= R <= x + y + 4
    raise AssertionError((x, y, R, d))


def option_table_audit(max_x: int = 60, extra_after_S: int = 12) -> dict:
    small = odd = even = 0
    small_bad = odd_bad = even_bad = 0
    first_bad = None
    for x in range(1, max_x + 1):
        for y in range(1, x + 1):
            S = x + y
            for R in range(1, S + extra_after_S + 1):
                actual = z4_options_from_closed_forms(x, y, R)
                if R <= 4:
                    small += 1
                    expected = expected_small(x, y, R)
                    bad = actual != expected
                    small_bad += bad
                elif R & 1:
                    odd += 1
                    expected = expected_odd(x, y, R)
                    bad = actual != expected
                    odd_bad += bad
                else:
                    even += 1
                    expected = expected_even_has_zero(x, y, R)
                    bad = (0 in actual) != expected
                    even_bad += bad
                if bad and first_bad is None:
                    first_bad = {"x": x, "y": y, "R": R,
                                 "actual": sorted(actual),
                                 "expected": sorted(expected) if isinstance(expected, set) else expected}
    return {"max_x": max_x, "extra_R_after_S": extra_after_S,
            "small_option_checks": small, "small_option_mismatches": small_bad,
            "odd_option_set_checks": odd, "odd_option_set_mismatches": odd_bad,
            "even_zero_membership_checks": even, "even_zero_membership_mismatches": even_bad,
            "first_mismatch": first_bad}


def main() -> None:
    raw = raw_audit(max_x=24, extra=8, scatter=200)
    raw.pop("status", None)
    raw.pop("target", None)
    table = option_table_audit()
    bad_raw = not raw["all_zero_mismatch"]
    bad_table = any(table[k] for k in ("small_option_mismatches",
        "odd_option_set_mismatches", "even_zero_membership_mismatches"))
    result = {"date": "2026-11-16",
        "target": "two-token residual game z=4 full Grundy slice",
        "status": "proved by strong induction; finite audits are corroboration",
        "proof_method": "R-strong induction; exact small-R table; odd option-set signatures; even zero-membership signatures",
        "raw_two_engine_audit": raw,
        "all_parameter_option_table_audit": table,
        "all_checks_pass": not (bad_raw or bad_table),
        "verifier_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out = Path(__file__).resolve().parent / "output" / "audit.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"), end="")
    if not result["all_checks_pass"]: raise SystemExit(1)


if __name__ == "__main__":
    main()
