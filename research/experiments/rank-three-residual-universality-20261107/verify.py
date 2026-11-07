#!/usr/bin/env python3
"""Universal rank-three residual realization, with future-circle exclusion."""
from fractions import Fraction as F
import importlib.util
from itertools import combinations
import json
from math import comb, lcm
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
SPEC = importlib.util.spec_from_file_location("single_triple_geometry", ROOT /
    "research/experiments/tree-triple-broom-periodicity-20261107/verify_geometry.py")
BASE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(BASE)
OLD = BASE.OLD


def append_anchor(points, base, center, allowed, future):
    bound = 2 * comb(len(points), 3) + 2 * len(future) + len(points) + 6
    for slope in range(1, bound):
        candidate = OLD.point_on_circle(base, center, slope)
        if candidate in points or any(OLD.on_circle(candidate, cc, rr) for cc, rr in future):
            continue
        if OLD.new_bad_quads(points, candidate) == allowed:
            result = len(points)
            points.append(candidate)
            return result
    raise AssertionError("finite exclusion bound failed")


def realize(n, forbidden):
    vertices = [(F(i), F(i * i)) for i in range(1, n + 1)]
    points = vertices.copy()
    pairs, triples = [], []
    for edge in forbidden:
        members = tuple(i for i in range(n) if edge >> i & 1)
        (pairs if len(members) == 2 else triples).append(members)
    assert all(edge.bit_count() in (2, 3) for edge in forbidden)
    assert not any(a != b and a & b == a for a in forbidden for b in forbidden)
    circles = []
    for triple in triples:
        cc = BASE.center_of_three(*(vertices[i] for i in triple))
        rr = sum((vertices[triple[0]][j] - cc[j]) ** 2 for j in range(2))
        circles.append((cc, rr))
    occupied, expected = [], []
    for j, triple in enumerate(triples):
        cc, rr = circles[j]
        # This invariant is the additional ingredient beyond one triple.
        assert [i for i, point in enumerate(points) if OLD.on_circle(point, cc, rr)] == list(triple)
        anchor = append_anchor(points, vertices[triple[0]], cc, [triple], circles[j + 1:])
        occupied.append(anchor)
        expected.append((*triple, anchor))
    for a, b in pairs:
        for parameter in range(1, len(points) + 4):
            cc = OLD.circle_center(vertices[a], vertices[b], F(parameter))
            rr = sum((vertices[a][j] - cc[j]) ** 2 for j in range(2))
            if all(not OLD.on_circle(point, cc, rr) for i, point in enumerate(points) if i not in (a, b)):
                break
        else:
            raise AssertionError("no pair circle")
        first = append_anchor(points, vertices[a], cc, [], [])
        second = append_anchor(points, vertices[a], cc, [(a, b, first)], [])
        occupied.extend((first, second))
        expected.append((a, b, first, second))
    scale = lcm(*(coordinate.denominator for point in points for coordinate in point))
    integer_points = [tuple(int(coordinate * scale) for coordinate in point) for point in points]
    assert len(integer_points) == n + 2 * len(pairs) + len(triples)
    return integer_points, sorted(occupied), sorted(tuple(sorted(q)) for q in expected)


def audit(n, forbidden):
    points, occupied, expected = realize(n, forbidden)
    actual = [quad for quad in combinations(range(len(points)), 4)
              if BASE.independent_determinant([points[i] for i in quad]) == 0]
    assert actual == expected
    stone_mask = sum(1 << i for i in occupied)
    masks = [sum(1 << i for i in q) for q in actual]
    residual = sorted(q & ~stone_mask for q in masks)
    assert residual == sorted(forbidden)
    assert all((stone_mask & q) != q for q in masks)
    abstract_values = BASE.all_safe_values(n, forbidden)
    unsafe = [s for s in range(1 << n) if any((s | stone_mask) & q == q for q in masks)]
    assert BASE.all_safe_values(n, unsafe) == abstract_values
    return dict(n=n, forbidden=forbidden, points=points, occupied=occupied,
                actual_quads=actual, grundy=abstract_values[0], safe_states=len(abstract_values),
                quadruples=comb(len(points), 4))


def all_small():
    for n in range(1, 5):
        possible = [sum(1 << i for i in edge) for size in (2, 3) for edge in combinations(range(n), size)]
        for mask in range(1 << len(possible)):
            edges = tuple(sorted(possible[j] for j in range(len(possible)) if mask >> j & 1))
            if not any(a != b and a & b == a for a in edges for b in edges):
                yield n, edges


def main():
    records = [audit(n, edges) for n, edges in all_small()]
    assert len(records) == 125
    # Five/six point examples with overlapping triples, all triples, and mixed pairs.
    larger = [(5, tuple(sum(1 << i for i in edge) for edge in combinations(range(5), 3))),
              (6, (7, 11, 19, 35)), (6, (3, 28, 44, 52)),
              (6, (7, 25, 42, 52)), (5, (7, 11, 13, 14))]
    records.extend(audit(n, edges) for n, edges in larger)
    # A rank-four target with just two edges sharing three points is impossible:
    # circle/line closure would force all five four-subsets.
    rank_four_target = [15, 23]
    forced = [sum(1 << i for i in edge) for edge in combinations(range(5), 4)]
    assert set(rank_four_target) < set(forced) and len(forced) == 5
    output = dict(audit="PASS", all_rank_three_clutters_n1_through_n4=125,
                  geometric_cases=len(records),
                  integer_quadruples_checked=sum(row["quadruples"] for row in records),
                  all_safe_grundy_states_checked=sum(row["safe_states"] for row in records),
                  rank_four_obstruction=dict(target=rank_four_target, forced_closure=forced),
                  records=records)
    head = {key: value for key, value in output.items() if key != "records"}
    text = json.dumps(head, ensure_ascii=False, indent=2)
    text = text[:-2] + ',\n  "records": [\n' + ',\n'.join(
        '    ' + json.dumps(row, separators=(',', ':')) for row in records) + '\n  ]\n}\n'
    json.loads(text)
    target = Path(__file__).with_name("output") / "audit.json"
    target.parent.mkdir(exist_ok=True)
    target.write_text(text, encoding="utf-8")
    print(json.dumps(head, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
