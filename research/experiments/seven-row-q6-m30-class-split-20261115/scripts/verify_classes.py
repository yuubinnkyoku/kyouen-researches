#!/usr/bin/env python3
"""Independently audit the row-reflection orbit partition in classes.txt.

This checks only the combinatorial coverage of deficient-row subsets.
It does not validate the SAT encoding, solver answers, or geometric witnesses.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def reflect(rows: tuple[int, ...], width: int) -> tuple[int, ...]:
    return tuple(sorted(width - 1 - y for y in rows))


def orbit_key(rows: tuple[int, ...], width: int) -> tuple[int, ...]:
    return min(rows, reflect(rows, width))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--classes",
        type=Path,
        default=Path(__file__).with_name("classes.txt"),
        help="path to the newline-separated representative list",
    )
    parser.add_argument("--width", type=int, default=7)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    width = args.width
    if width <= 0:
        parser.error("--width must be positive")

    raw = args.classes.read_text(encoding="utf-8").splitlines()
    listed: list[tuple[int, ...]] = []
    malformed: list[dict[str, object]] = []
    for line_no, line in enumerate(raw, 1):
        if not line.strip():
            continue
        try:
            rows = tuple(int(part) for part in line.split(","))
        except ValueError:
            malformed.append({"line": line_no, "text": line, "reason": "non-integer"})
            continue
        if not rows:
            malformed.append({"line": line_no, "text": line, "reason": "empty"})
            continue
        if tuple(sorted(set(rows))) != rows:
            malformed.append({"line": line_no, "text": line, "reason": "not strictly increasing"})
            continue
        if rows[0] < 0 or rows[-1] >= width:
            malformed.append({"line": line_no, "text": line, "reason": "row out of range"})
            continue
        listed.append(rows)

    all_subsets = [
        tuple(y for y in range(width) if mask & (1 << y))
        for mask in range(1, 1 << width)
    ]
    expected_orbits = {orbit_key(rows, width) for rows in all_subsets}
    listed_orbits = [orbit_key(rows, width) for rows in listed]
    duplicate_lines = len(listed) - len(set(listed))
    duplicate_orbits = len(listed_orbits) - len(set(listed_orbits))
    missing_orbits = sorted(expected_orbits - set(listed_orbits))
    extra_orbits = sorted(set(listed_orbits) - expected_orbits)
    noncanonical = sorted(rows for rows in listed if rows != orbit_key(rows, width))

    fixed_nonempty = sum(
        1 for rows in all_subsets if reflect(rows, width) == rows
    )
    expected_by_burnside = ((1 << width) - 1 + fixed_nonempty) // 2

    ok = (
        not malformed
        and duplicate_lines == 0
        and duplicate_orbits == 0
        and not missing_orbits
        and not extra_orbits
        and not noncanonical
        and len(expected_orbits) == expected_by_burnside
        and len(listed) == expected_by_burnside
    )
    result = {
        "status": "PASS" if ok else "FAIL",
        "width": width,
        "symmetry": "row reflection y -> width-1-y",
        "all_nonempty_subsets": len(all_subsets),
        "reflection_fixed_nonempty_subsets": fixed_nonempty,
        "two_element_orbits": (len(all_subsets) - fixed_nonempty) // 2,
        "burnside_orbit_count": expected_by_burnside,
        "enumerated_orbit_count": len(expected_orbits),
        "listed_representatives": len(listed),
        "duplicate_lines": duplicate_lines,
        "duplicate_orbits": duplicate_orbits,
        "missing_orbits": [list(x) for x in missing_orbits],
        "extra_orbits": [list(x) for x in extra_orbits],
        "noncanonical_representatives": [list(x) for x in noncanonical],
        "malformed_lines": malformed,
        "scope": (
            "Only the row-reflection orbit partition of nonempty deficient-row "
            "subsets is checked; SAT encoding, solver outcomes, and geometric "
            "witnesses are outside this audit."
        ),
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
