#!/usr/bin/env python3
"""Exact structural classification of the forbidden circles in K1156's zero-row candidates."""
from __future__ import annotations
import argparse
import hashlib
import itertools
import json
from collections import Counter, defaultdict
from fractions import Fraction
from pathlib import Path

INPUT_SHA256 = "51e7a465e18646097073e4f8231f89cbff327d05f9bfeac102e57c754b4ff822"
AUDIT_SHA256 = "c4e55dbe8d937dce93430f5804296dcd5cf42a9d42de14f8e90bbebe262eb61f"
EXPECTED_ROWS = [
    "00000000000000003800000008002010",
    "0000000000000000380000000a080000",
    "00000000020000801202000000100000",
]
CENTER = (5, 5)

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def fmt(q: Fraction) -> str:
    return str(q.numerator) if q.denominator == 1 else f"{q.numerator}/{q.denominator}"

def point_list(mask: int) -> list[tuple[int, int]]:
    return [(p % 11, p // 11) for p in range(121) if (mask >> p) & 1]

def transform_xy(point, t: int):
    x, y = point
    if t == 0: return (x, y)
    if t == 1: return (10-y, x)
    if t == 2: return (10-x, 10-y)
    if t == 3: return (y, 10-x)
    if t == 4: return (10-x, y)
    if t == 5: return (x, 10-y)
    if t == 6: return (y, x)
    return (10-y, 10-x)

def transform_mask(mask: int, t: int) -> int:
    out = 0
    for x, y in point_list(mask):
        X, Y = transform_xy((x, y), t)
        out |= 1 << (11*Y + X)
    return out

def solve_circle(points):
    # Solve x^2+y^2 + A*x + B*y + C = 0 over Q using the first three points.
    matrix = [
        [Fraction(x), Fraction(y), Fraction(1), Fraction(-(x*x+y*y))]
        for x, y in points[:3]
    ]
    for col in range(3):
        pivot = next((r for r in range(col, 3) if matrix[r][col]), None)
        if pivot is None:
            raise SystemExit("FAIL-CLOSED: first three forbidden-quad points are collinear")
        matrix[col], matrix[pivot] = matrix[pivot], matrix[col]
        scale = matrix[col][col]
        matrix[col] = [v/scale for v in matrix[col]]
        for r in range(3):
            if r == col:
                continue
            factor = matrix[r][col]
            matrix[r] = [matrix[r][j] - factor*matrix[col][j] for j in range(4)]
    A, B, C = (matrix[i][3] for i in range(3))
    if any(Fraction(x*x+y*y) + A*x + B*y + C != 0 for x, y in points):
        raise SystemExit("FAIL-CLOSED: fourth point is not on the circle through the first three")
    center = (-A/2, -B/2)
    radius2 = center[0]*center[0] + center[1]*center[1] - C
    if radius2 <= 0:
        raise SystemExit("FAIL-CLOSED: non-positive circle radius")
    return {"A": A, "B": B, "C": C, "center": center, "radius2": radius2}

def d4_center_orbit(center):
    images = [transform_xy(center, t) for t in range(8)]
    return min(images)

def equation_from_center(center, radius2):
    cx, cy = center
    A, B = -2*cx, -2*cy
    C = cx*cx + cy*cy - radius2
    if any(v.denominator != 1 for v in (A, B, C)):
        raise SystemExit("FAIL-CLOSED: canonical circle equation is not integral")
    return {"x2": 1, "y2": 1, "x": int(A), "y": int(B), "constant": int(C)}

def equation_text(eq):
    def term(coef, var):
        if coef == 0: return ""
        sign = "+" if coef > 0 else "-"
        n = abs(coef)
        body = ("" if n == 1 else str(n)) + var
        return sign + body
    parts = ["x^2", "+y^2", term(eq["x"], "x"), term(eq["y"], "y"), term(eq["constant"], "")]
    s = "".join(parts)
    if s.startswith("+"): s = s[1:]
    s = s.replace("+-", "-")
    return s + "=0"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input", required=True)
    ap.add_argument("--audit", required=True)
    ap.add_argument("--output", required=True)
    args = ap.parse_args()

    input_bytes = Path(args.input).read_bytes()
    audit_bytes = Path(args.audit).read_bytes()
    if sha256(input_bytes) != INPUT_SHA256:
        raise SystemExit("FAIL-CLOSED: K1156 input fixture SHA-256 mismatch")
    if sha256(audit_bytes) != AUDIT_SHA256:
        raise SystemExit("FAIL-CLOSED: K1156 audit SHA-256 mismatch")

    fixture = json.loads(input_bytes)
    audit = json.loads(audit_bytes)
    if audit.get("status") != "direct-row-plus-two-point-fourth-geometry-passed" or not audit.get("checks_all_ok"):
        raise SystemExit("FAIL-CLOSED: K1156 audit is not PASS")
    zero_indices = [i for i, n in enumerate(fixture.get("expected_per_row_triple_availability", [])) if n == 0]
    zero_rows = [fixture["residual_rows"][i] for i in zero_indices]
    if zero_rows != EXPECTED_ROWS or zero_indices != [1,2,21]:
        raise SystemExit("FAIL-CLOSED: residual zero-row identities changed")
    if audit.get("enumeration", {}).get("zero_rows") != EXPECTED_ROWS:
        raise SystemExit("FAIL-CLOSED: audit zero-row identities changed")
    excluded = {int(x, 16) for x in fixture["refuted_d10_roots_excluded"]}

    per_row = []
    occurrence_rows = []
    canonical_quad_map = {}
    orbit_counts = Counter()
    orbit_roots = defaultdict(set)
    root_class = {}
    for row_record in audit["per_zero_row"]:
        row_hex = row_record["row"]
        if row_hex not in EXPECTED_ROWS:
            raise SystemExit("FAIL-CLOSED: unexpected zero row")
        row = int(row_hex, 16)
        row_points = point_list(row)
        if row.bit_count() != 6 or CENTER not in row_points:
            raise SystemExit("FAIL-CLOSED: zero row is not a six-stone row through (5,5)")
        horizontal = sorted(p for p in row_points if p[1] == 5)
        vertical = sorted(p for p in row_points if p[0] == 5)
        axis = None
        axis_points = None
        if horizontal == [(4,5),(5,5),(6,5)]:
            axis, axis_points = "horizontal", horizontal
        elif vertical == [(5,4),(5,5),(5,6)]:
            axis, axis_points = "vertical", vertical
        else:
            raise SystemExit("FAIL-CLOSED: zero row lacks the expected central three-point axis")

        row_occurrences = []
        for candidate in row_record["candidate_roots"]:
            root_hex = candidate["root"]
            root = int(root_hex, 16)
            if root.bit_count() != 8:
                raise SystemExit("FAIL-CLOSED: candidate root is not eight stones")
            if len(candidate["covered_row_indices"]) != 3:
                raise SystemExit("FAIL-CLOSED: candidate does not cover exactly three residual rows")
            transforms = [t for t in range(8) if transform_mask(root, t) & row == row]
            if not transforms:
                raise SystemExit("FAIL-CLOSED: no D4 image of candidate contains its source row")
            t = min(transforms)
            row_oriented_root = transform_mask(root, t)
            if row_oriented_root.bit_count() != 8 or row_oriented_root & row != row:
                raise SystemExit("FAIL-CLOSED: D4 row embedding is invalid")
            added = point_list(row_oriented_root ^ row)
            if len(added) != 2:
                raise SystemExit("FAIL-CLOSED: row extension does not add exactly two points")

            classification = candidate["classification"]
            if classification == "safe_but_refuted_d10_excluded":
                if root not in excluded or candidate["forbidden_quad_xy"] is not None:
                    raise SystemExit("FAIL-CLOSED: safe candidate is not in the pinned REFUTED-D10 exclusion set")
                occ = {
                    "root": root_hex,
                    "classification": classification,
                    "added_points_xy": [list(p) for p in added],
                    "covered_row_indices": candidate["covered_row_indices"],
                    "d4_transform_root_to_row": t,
                }
            elif classification == "unsafe_cocircular_quadruple":
                if root in excluded or candidate["forbidden_quad_xy"] is None:
                    raise SystemExit("FAIL-CLOSED: unsafe candidate classification conflicts with exclusion set")
                canonical_quad = [tuple(p) for p in candidate["forbidden_quad_xy"]]
                if len(canonical_quad) != 4:
                    raise SystemExit("FAIL-CLOSED: forbidden quadruple is malformed")
                row_quad = [transform_xy(p, t) for p in canonical_quad]
                circle_canonical = solve_circle(canonical_quad)
                circle_row = solve_circle(row_quad)
                if transform_xy(circle_canonical["center"], t) != circle_row["center"]:
                    raise SystemExit("FAIL-CLOSED: circle center does not follow the D4 embedding")
                if circle_canonical["radius2"] != circle_row["radius2"]:
                    raise SystemExit("FAIL-CLOSED: radius changed under D4")
                if CENTER not in row_quad:
                    raise SystemExit("FAIL-CLOSED: forbidden circle does not pass through board center")
                center_orbit = d4_center_orbit(circle_row["center"])
                orbit_key = (center_orbit, circle_row["radius2"])
                orbit_counts[orbit_key] += 1
                orbit_roots[orbit_key].add(root_hex)
                canonical_quad_key = tuple(sorted(canonical_quad))
                canonical_quad_map[canonical_quad_key] = circle_canonical
                eq_row = equation_from_center(circle_row["center"], circle_row["radius2"])
                occ = {
                    "root": root_hex,
                    "classification": classification,
                    "added_points_xy": [list(p) for p in added],
                    "covered_row_indices": candidate["covered_row_indices"],
                    "d4_transform_root_to_row": t,
                    "forbidden_quad_xy_in_root_orientation": [list(p) for p in canonical_quad],
                    "forbidden_quad_xy_in_row_orientation": [list(p) for p in row_quad],
                    "circle_equation_row_orientation": equation_text(eq_row),
                    "circle_center_xy": [fmt(v) for v in circle_row["center"]],
                    "circle_radius_squared": fmt(circle_row["radius2"]),
                    "circle_d4_orbit_center_xy": [fmt(v) for v in center_orbit],
                }
            else:
                raise SystemExit("FAIL-CLOSED: unknown candidate classification")
            row_occurrences.append(occ)
            occurrence_rows.append({"row": row_hex, "row_index": row_record["row_index"], **occ})
            old = root_class.setdefault(root_hex, classification)
            if old != classification:
                raise SystemExit("FAIL-CLOSED: candidate root has conflicting safety classifications")

        expected_count = {EXPECTED_ROWS[0]:4, EXPECTED_ROWS[1]:5, EXPECTED_ROWS[2]:5}[row_hex]
        if len(row_occurrences) != expected_count:
            raise SystemExit("FAIL-CLOSED: per-row candidate count changed")
        per_row.append({
            "row": row_hex,
            "row_index": row_record["row_index"],
            "stones_xy": [list(p) for p in row_points],
            "central_axis": axis,
            "central_three_collinear_points_xy": [list(p) for p in axis_points],
            "candidate_count": len(row_occurrences),
            "unsafe_cocircular_occurrences": sum(x["classification"] == "unsafe_cocircular_quadruple" for x in row_occurrences),
            "safe_but_refuted_occurrences": sum(x["classification"] == "safe_but_refuted_d10_excluded" for x in row_occurrences),
            "candidates": row_occurrences,
        })

    unsafe_occ = [x for x in occurrence_rows if x["classification"] == "unsafe_cocircular_quadruple"]
    safe_occ = [x for x in occurrence_rows if x["classification"] == "safe_but_refuted_d10_excluded"]
    if (len(occurrence_rows), len(unsafe_occ), len(safe_occ)) != (14,10,4):
        raise SystemExit("FAIL-CLOSED: candidate occurrence partition changed")
    if (len(root_class), sum(v == "unsafe_cocircular_quadruple" for v in root_class.values()),
        sum(v == "safe_but_refuted_d10_excluded" for v in root_class.values())) != (8,5,3):
        raise SystemExit("FAIL-CLOSED: unique-root classification changed")
    if len(canonical_quad_map) != 3 or len(orbit_counts) != 2:
        raise SystemExit("FAIL-CLOSED: expected three canonical quadruples in two D4 circle orbits")
    if sorted(orbit_counts.values()) != [5,5]:
        raise SystemExit("FAIL-CLOSED: forbidden-circle orbit occurrence counts are not 5/5")

    canonical_circles = []
    for quad_key, circle in sorted(canonical_quad_map.items()):
        center = circle["center"]
        r2 = circle["radius2"]
        eq = equation_from_center(center, r2)
        if 25+25+eq["x"]*5+eq["y"]*5+eq["constant"] != 0:
            raise SystemExit("FAIL-CLOSED: canonical circle does not contain (5,5)")
        orbit_center = d4_center_orbit(center)
        orbit_eq = equation_from_center(orbit_center, r2)
        canonical_circles.append({
            "forbidden_quad_xy": [list(p) for p in quad_key],
            "equation": equation_text(eq),
            "center_xy": [fmt(v) for v in center],
            "radius_squared": fmt(r2),
            "passes_through_board_center_5_5": True,
            "d4_orbit_center_xy": [fmt(v) for v in orbit_center],
            "d4_orbit_representative_equation": equation_text(orbit_eq),
        })

    orbit_summary = []
    for (center, r2), count in sorted(orbit_counts.items(), key=lambda kv:(kv[0][1],kv[0][0])):
        eq = equation_from_center(center, r2)
        orbit_summary.append({
            "canonical_center_xy": [fmt(v) for v in center],
            "radius_squared": fmt(r2),
            "representative_equation": equation_text(eq),
            "occurrence_count": count,
            "unique_root_count": len(orbit_roots[(center,r2)]),
            "unique_roots": sorted(orbit_roots[(center,r2)]),
        })

    script_bytes = Path(__file__).read_bytes()
    result = {
        "schema": "n11-residual23-zero-triple-forbidden-circle-structure-20261121-v1",
        "status": "two-circle-orbit-structure-verified",
        "source_pins": {
            "k1156_input_fixture_sha256": INPUT_SHA256,
            "k1156_direct_fourth_audit_sha256": AUDIT_SHA256,
        },
        "method": {
            "scope": "post-analysis of the exhaustive 14 listed triple-candidate occurrences in K1156; does not rerun the 6,555 root-generation loops",
            "circle_fit": "exact Fraction Gaussian elimination on x^2+y^2+A*x+B*y+C=0",
            "independence": "reconstructs each D4 embedding and refits all 10 forbidden circles from coordinates; does not trust stored circle centers or radii because K1156 stores only quadruple coordinates",
            "d4_circle_orbit": "canonicalize the exact circumcenter under all eight D4 maps while preserving radius squared",
        },
        "summary": {
            "zero_rows": 3,
            "all_zero_rows_contain_center_5_5": True,
            "all_zero_rows_have_centered_axis_triple": True,
            "candidate_occurrences": 14,
            "unsafe_cocircular_occurrences": 10,
            "safe_but_refuted_d10_occurrences": 4,
            "unique_candidate_roots": 8,
            "unique_unsafe_roots": 5,
            "unique_safe_excluded_roots": 3,
            "distinct_canonical_forbidden_quadruples": 3,
            "d4_circle_orbits": 2,
            "forbidden_circle_occurrences_per_orbit": [5,5],
            "all_forbidden_circles_pass_through_5_5": True,
        },
        "per_zero_row": per_row,
        "canonical_forbidden_circles": canonical_circles,
        "d4_circle_orbit_summary": orbit_summary,
        "interpretation_guard": [
            "The geometric obstruction covers only the unsafe candidate roots among the exhaustive K1156 triple-candidate list.",
            "The remaining safe candidate roots are excluded by pinned REFUTED-D10 facts, not by geometry.",
            "The global P''' maximum-three-row-provider premise is inherited from K1147 and is not re-proved here.",
            "No DFPN probe, certificate extraction, receipt fold, S6 row closure, or game-theoretic verdict is created.",
            "The standard 11x11 empty board, two-stone roots {49,60}/{59,60}, S2 {59,60}, and classes 1/2/4 remain UNKNOWN.",
        ],
        "script_sha256": sha256(script_bytes),
    }
    out = json.dumps(result, ensure_ascii=True, sort_keys=True, separators=(",",":")) + "\n"
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(out, encoding="utf-8")
    print(json.dumps({
        "status": result["status"],
        "summary": result["summary"],
        "d4_circle_orbit_summary": orbit_summary,
        "script_sha256": result["script_sha256"],
        "output_sha256": sha256(out.encode()),
        "output_bytes": len(out.encode()),
    }, ensure_ascii=True, sort_keys=True, indent=2))

if __name__ == "__main__":
    main()

