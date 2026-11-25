#!/usr/bin/env python3
"""Independent exact audit of the (4,21,5) row-0 blocker-circle split.

This implementation builds circles from all non-collinear triples using integer
coefficients; it does not import the JavaScript census or SA implementation.
"""
from __future__ import annotations

from collections import Counter
from itertools import combinations
from math import gcd
import hashlib
import json
from pathlib import Path

W, M, Q = 4, 21, 5
TARGET = (20, 0)


def circle_coeff(p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]):
    (x1, y1), (x2, y2), (x3, y3) = p1, p2, p3
    s1, s2, s3 = x1*x1 + y1*y1, x2*x2 + y2*y2, x3*x3 + y3*y3
    det = x1*(y2-y3) - y1*(x2-x3) + (x2*y3-x3*y2)
    if det == 0:
        return None
    b_num = s1*(y2-y3) - y1*(s2-s3) + (s2*y3-s3*y2)
    c_num = x1*(s2-s3) - s1*(x2-x3) + (x2*s3-x3*s2)
    d_num = x1*(y2*s3-y3*s2) - y1*(x2*s3-x3*s2) + s1*(x2*y3-x3*y2)
    co = [det, -b_num, -c_num, -d_num]
    g = 0
    for v in co:
        g = gcd(g, abs(v))
    co = [v // g for v in co]
    if co[0] < 0:
        co = [-v for v in co]
    return tuple(co)


def on_circle(co, p):
    x, y = p
    a, b, c, d = co
    return a*(x*x+y*y) + b*x + c*y + d == 0


def line_coeff(p1: tuple[int, int], p2: tuple[int, int]):
    (x1, y1), (x2, y2) = p1, p2
    a, b, c = y2-y1, x1-x2, x2*y1-x1*y2
    g = gcd(gcd(abs(a), abs(b)), abs(c))
    a, b, c = a//g, b//g, c//g
    if a < 0 or (a == 0 and b < 0):
        a, b, c = -a, -b, -c
    return (a, b, c)


def on_line(co, p):
    x, y = p
    a, b, c = co
    return a*x + b*y + c == 0


def census():
    points = [(x, y) for y in range(W) for x in range(M)]
    circles = {}
    triple_counts = Counter()
    for tri in combinations(points, 3):
        co = circle_coeff(*tri)
        if co is None:
            continue
        on = tuple(p for p in points if on_circle(co, p))
        if len(on) >= Q:
            circles[co] = on
            triple_counts[co] += 1
    for co, on in circles.items():
        if triple_counts[co] != len(on) * (len(on)-1) * (len(on)-2) // 6:
            raise AssertionError(f"circle triple count mismatch: {co}")
    return points, circles


def blocker_cases(circles: dict, bucket: str):
    if bucket == "p1":
        anchor, forbidden = (1, 0), {(0, 0)}
    elif bucket == "p0":
        anchor, forbidden = (0, 0), set()
    else:
        raise ValueError(bucket)

    cases = []
    circles_through_target = []
    for co, on in sorted(circles.items()):
        if TARGET not in on:
            continue
        circles_through_target.append((co, on))
        mandatory = [anchor] if anchor in on else []
        rest = [p for p in on if p != TARGET and p not in forbidden and p not in mandatory]
        need = Q - 1 - len(mandatory)
        for extra in combinations(rest, need):
            pins = tuple(sorted(set(mandatory + list(extra))))
            if len(pins) != Q - 1 or TARGET in pins or any(p in forbidden for p in pins):
                continue
            # The base bucket already fixes the anchor even when it is not on this circle.
            forced = set(pins) | {anchor}
            if sum(y == 0 for x, y in forced) > 3:
                continue
            if anchor in on and anchor not in pins:
                raise AssertionError("mandatory anchor omitted")
            cases.append({"circle": list(co), "pins": [list(p) for p in pins]})

    pin_keys = [tuple(tuple(p) for p in c["pins"]) for c in cases]
    if len(pin_keys) != len(set(pin_keys)):
        raise AssertionError(f"duplicate pin sets in {bucket}")
    return circles_through_target, cases


def case_digest(cases):
    payload = json.dumps(cases, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def legacy_p1_count(circles):
    """Reproduce the old SA enumerator: it forgot that (1,0) is pre-fixed."""
    cases = []
    for co, on in circles.items():
        if TARGET not in on:
            continue
        rest = [p for p in on if p != TARGET and p != (0, 0)]
        for extra in combinations(rest, 4):
            if sum(y == 0 for x, y in extra) <= 2:
                cases.append((co, tuple(sorted(extra))))
    return cases


def main():
    _, circles = census()
    p1_circles, p1 = blocker_cases(circles, "p1")
    p0_circles, p0 = blocker_cases(circles, "p0")
    through_target = [on for on in circles.values() if TARGET in on]
    hist = dict(sorted(Counter(map(len, through_target)).items()))

    points = [(x, y) for y in range(W) for x in range(M)]
    lines = {}
    for p in points:
        if p == TARGET:
            continue
        co = line_coeff(TARGET, p)
        if co not in lines:
            lines[co] = tuple(q for q in points if on_line(co, q))
    nonhorizontal = [on for co, on in lines.items() if co[0] != 0]
    horizontal = [on for co, on in lines.items() if co[0] == 0]
    max_nonhorizontal_line_points = max(map(len, nonhorizontal))
    row0_stones = 3

    p1_anchor_circles = [co for co, on in p1_circles if (1, 0) in on]
    p0_anchor_circles = [co for co, on in p0_circles if (0, 0) in on]
    legacy = legacy_p1_count(circles)
    legacy_invalid = []
    for co, pins in legacy:
        if (1, 0) in circles[co] and (1, 0) not in pins:
            legacy_invalid.append((co, pins))

    assert len(circles) == 538
    assert len(p1_circles) == len(p0_circles) == 19
    assert hist == {5: 2, 6: 17}
    assert len(p1_anchor_circles) == 2
    assert len(p0_anchor_circles) == 1
    assert len(p1) == 81 and len(p0) == 86
    assert max_nonhorizontal_line_points <= W
    assert len(horizontal) == 1 and len(horizontal[0]) == M
    assert row0_stones == Q - 2
    assert len(legacy) == 83 and len(legacy_invalid) == 2

    out = {
        "board": {"width": W, "length": M, "q": Q},
        "target_empty_cell": list(TARGET),
        "circle_census": {
            "all_ge5_circles": len(circles),
            "all_circle_triples_match_Ck3": True,
            "through_target": len(through_target),
            "through_target_point_count_histogram": {str(k): v for k, v in hist.items()},
        },
        "line_blocker_exclusion": {
            "nonhorizontal_lines_through_target": len(nonhorizontal),
            "max_grid_points_on_nonhorizontal_line": max_nonhorizontal_line_points,
            "horizontal_row0_line_grid_points": M,
            "row0_occupied_stones_in_bucket": row0_stones,
            "required_blocker_stones": Q - 1,
            "conclusion": "No line can block (20,0): a nonhorizontal line has at most 4 grid points including the target, while row 0 has only 3 stones."
        },
        "buckets": {
            "p1": {
                "anchor": [1, 0], "forbidden": [[0, 0]],
                "circles_through_target_and_anchor": len(p1_anchor_circles),
                "blocker_cases": len(p1), "occupied_target_case": 1,
                "total_instances": len(p1) + 1, "unique_pin_sets": True,
                "canonical_case_list_sha256": case_digest(p1),
            },
            "p0": {
                "anchor": [0, 0], "forbidden": [],
                "circles_through_target_and_anchor": len(p0_anchor_circles),
                "blocker_cases": len(p0), "occupied_target_case": 1,
                "total_instances": len(p0) + 1, "unique_pin_sets": True,
                "canonical_case_list_sha256": case_digest(p0),
            },
        },
        "correction": {
            "legacy_p1_raw_cases": len(legacy),
            "legacy_p1_invalid_cases": len(legacy_invalid),
            "corrected_p1_cases": len(p1),
            "reason": "The old enumerator omitted the already-forced (1,0) from its mandatory set on two circles through both (20,0) and (1,0), creating two five-stone-on-one-circle branches.",
            "invalid_cases": [
                {"circle": list(co), "circle_points": [list(p) for p in circles[co]], "pins": [list(p) for p in pins]}
                for co, pins in legacy_invalid
            ],
        },
        "scope": "Exact finite census and blocker-cover audit for the specified (4,21,5) buckets only; no SAT verdict and no conclusion about existence of a deficient maximal witness.",
    }
    Path("blocker_split_independent_audit.json").write_text(json.dumps(out, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "circles_ge5": len(circles),
        "through_target": len(through_target),
        "through_target_hist": hist,
        "p1_anchor_circles": len(p1_anchor_circles),
        "p0_anchor_circles": len(p0_anchor_circles),
        "nonhorizontal_lines_through_target": len(nonhorizontal),
        "max_nonhorizontal_line_points": max_nonhorizontal_line_points,
        "horizontal_row0_stones": row0_stones,
        "legacy_p1": len(legacy),
        "legacy_p1_invalid": len(legacy_invalid),
        "corrected_p1": len(p1),
        "p0": len(p0),
        "p1_total_instances": len(p1)+1,
        "p0_total_instances": len(p0)+1,
    }, indent=2))


if __name__ == "__main__":
    main()
