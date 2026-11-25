#!/usr/bin/env python3
"""One independent triple + arbitrary graph: rational construction, integer audit."""
from fractions import Fraction as F
from functools import lru_cache
import importlib.util
from itertools import combinations, permutations
import json
from math import comb, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("old_circle_geometry", ROOT /
    "research/experiments/game-structure/scripts/verify_graph_realization_20261019.py")
OLD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(OLD)


def center_of_three(a, b, c):
    dx, dy = b[0] - a[0], b[1] - a[1]
    ex, ey = c[0] - a[0], c[1] - a[1]
    rhs = (b[0] ** 2 + b[1] ** 2 - a[0] ** 2 - a[1] ** 2) / 2
    shs = (c[0] ** 2 + c[1] ** 2 - a[0] ** 2 - a[1] ** 2) / 2
    determinant = dx * ey - dy * ex
    assert determinant
    return ((rhs * ey - dy * shs) / determinant,
            (dx * shs - rhs * ex) / determinant)


def append_anchor(points, base, center, allowed):
    # Every prohibited old triple contributes at most two points on this circle.
    for slope in range(1, 2 * comb(len(points), 3) + len(points) + 6):
        candidate = OLD.point_on_circle(base, center, slope)
        if candidate not in points and OLD.new_bad_quads(points, candidate) == allowed:
            index = len(points)
            points.append(candidate)
            return index
    raise AssertionError("finite-exclusion bound failed")


def realize(n, edges, triple):
    triple = tuple(sorted(triple))
    edges = sorted(tuple(sorted(edge)) for edge in edges)
    assert len(set(triple)) == 3 and all(0 <= i < n for i in triple)
    assert not any(set(edge) <= set(triple) for edge in edges)
    vertices = [(F(i), F(i * i)) for i in range(1, n + 1)]
    points = vertices.copy()
    triple_center = center_of_three(*(vertices[i] for i in triple))
    triple_anchor = append_anchor(points, vertices[triple[0]], triple_center, [triple])
    occupied = [triple_anchor]
    expected = [tuple(sorted((*triple, triple_anchor)))]
    for a, b in edges:
        for parameter in range(1, len(points) + 4):
            center = OLD.circle_center(vertices[a], vertices[b], F(parameter))
            radius2 = sum((vertices[a][j] - center[j]) ** 2 for j in range(2))
            if all(not OLD.on_circle(point, center, radius2)
                   for i, point in enumerate(points) if i not in (a, b)):
                break
        else:
            raise AssertionError("no edge circle")
        first = append_anchor(points, vertices[a], center, [])
        second = append_anchor(points, vertices[a], center, [(a, b, first)])
        occupied.extend((first, second))
        expected.append((a, b, first, second))
    scale = lcm(*(coordinate.denominator for point in points for coordinate in point))
    integer_points = [tuple(int(coordinate * scale) for coordinate in point) for point in points]
    assert len(set(integer_points)) == len(integer_points) == n + 2 * len(edges) + 1
    return integer_points, occupied, sorted(expected)


PERMUTATIONS = [(p, -1 if sum(p[i] > p[j] for i in range(4) for j in range(i + 1, 4)) % 2 else 1)
                for p in permutations(range(4))]


def independent_determinant(points):
    """Generic 4x4 Leibniz expansion, independent of OLD's translated det3."""
    rows = [(x * x + y * y, x, y, 1) for x, y in points]
    return sum(sign * rows[0][p[0]] * rows[1][p[1]] * rows[2][p[2]] * rows[3][p[3]]
               for p, sign in PERMUTATIONS)


def all_safe_values(n, forbidden):
    values = {}
    for size in range(n, -1, -1):
        for chosen in combinations(range(n), size):
            s = sum(1 << v for v in chosen)
            if any(s & h == h for h in forbidden):
                continue
            options = {values[s | (1 << v)] for v in range(n)
                       if not s >> v & 1 and s | (1 << v) in values}
            value = 0
            while value in options:
                value += 1
            values[s] = value
    return values


def audit(n, edges, triple):
    points, occupied, expected = realize(n, edges, triple)
    actual = [quad for quad in combinations(range(len(points)), 4)
              if independent_determinant([points[i] for i in quad]) == 0]
    assert actual == expected
    stone_mask = sum(1 << i for i in occupied)
    full_quads = [sum(1 << i for i in quad) for quad in actual]
    residual = [quad & ~stone_mask for quad in full_quads]
    abstract = [sum(1 << i for i in edge) for edge in edges] + [sum(1 << i for i in triple)]
    assert sorted(residual) == sorted(abstract)
    assert all((stone_mask & q) != q for q in full_quads)
    abstract_values = all_safe_values(n, abstract)
    # Construct a distinct safety table from occupied integer-board points.
    geometric_forbidden = []
    for s in range(1 << n):
        if any((stone_mask | s) & q == q for q in full_quads):
            geometric_forbidden.append(s)
    geometric_values = all_safe_values(n, geometric_forbidden)
    assert abstract_values == geometric_values
    return dict(n=n, edges=edges, triple=triple, points=points, occupied=occupied,
                forbidden_quads=actual, grundy=abstract_values[0],
                safe_states=len(abstract_values), quads_checked=comb(len(points), 4))


def main():
    cases = []
    for n in (3, 4):
        for triple in combinations(range(n), 3):
            possible = [edge for edge in combinations(range(n), 2) if not set(edge) <= set(triple)]
            for mask in range(1 << len(possible)):
                cases.append((n, [edge for i, edge in enumerate(possible) if mask >> i & 1], triple))
    triple = (1, 2, 3)
    possible = [edge for edge in combinations(range(5), 2) if not set(edge) <= set(triple)]
    # Fixed deterministic sample; this is not all five-vertex graphs.
    for mask in (0, 1, 3, 7, 15, 31, 63, 127, 85, 42, 21, 84, 73, 54, 109, 90):
        cases.append((5, [edge for i, edge in enumerate(possible) if mask >> i & 1], triple))
    for length in (2, 3, 4):
        n = length + 4
        edges = [(0, v) for v in triple] + [(0, 4)] + [(v, v + 1) for v in range(4, n - 1)]
        cases.append((n, edges, triple))
    records = [audit(*case) for case in cases]
    output = dict(audit="PASS", geometric_cases=len(records),
                  integer_quadruples_checked=sum(row["quads_checked"] for row in records),
                  all_safe_grundy_states_checked=sum(row["safe_states"] for row in records),
                  records=records)
    target = Path(__file__).with_name("output") / "geometry_audit.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in output.items() if key != "records"}, indent=2))


if __name__ == "__main__":
    main()
