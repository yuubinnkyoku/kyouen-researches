"""Independent exhaustive finite checks of graph-to-circle fault reduction."""
from __future__ import annotations

import argparse
from itertools import combinations
import json
from math import comb, lcm
from pathlib import Path

from verify_cubic_fault_family import determinant3, determinant4, is_forbidden_quad


def vertex_cover_number(n, edges):
    for size in range(n+1):
        for subset in combinations(range(n), size):
            cover = set(subset)
            if all(cover.intersection(edge) for edge in edges):
                return size
    raise AssertionError("all vertices cover the graph")


def transversal_number(k, triples):
    masks = [sum(1 << i for i in triple) for triple in triples]
    inspected = 0
    for size in range(k+1):
        for subset in combinations(range(k), size):
            inspected += 1
            cover = sum(1 << i for i in subset)
            if all(cover & mask for mask in masks):
                return size, inspected
    raise AssertionError("all stones hit all blockers")


def audit_graph(n, edges, geometry):
    parameters = [10**v for v in range(n)] + [-(10**u+10**v) for u, v in edges]
    assert len(set(parameters)) == len(parameters)
    assert not any(-t in parameters for t in parameters)
    actual = {indices for indices in combinations(range(len(parameters)), 3)
              if sum(parameters[i] for i in indices) == 0}
    expected = {(u, v, n+i) for i, (u, v) in enumerate(edges)}
    assert actual == expected
    graph_minimum = vertex_cover_number(n, edges)
    hypergraph_minimum, inspected = transversal_number(len(parameters), actual)
    assert graph_minimum == hypergraph_minimum
    result = dict(n=n, edges=edges, vertex_cover=graph_minimum,
                  blocker_transversal=hypergraph_minimum,
                  candidate_transversals_inspected=inspected)
    if geometry:
        assert edges, "rho is only defined here when p starts blocked"
        scale = lcm(*(abs(t)*(1+4*t**4) for t in parameters))
        stones = [(scale // (t*(1+4*t**4)), 2*scale*t // (1+4*t**4))
                  for t in parameters]
        points = [(0, 0), *stones]
        forbidden = set()
        for indices in combinations(range(len(points)), 4):
            quad = [points[i] for i in indices]
            independent = determinant4(quad) == 0
            assert independent == is_forbidden_quad(quad)
            if independent:
                forbidden.add(indices)
        assert forbidden == {(0, u+1, v+1, private+1) for u, v, private in actual}
        assert all(determinant3([points[i] for i in indices])
                   for indices in combinations(range(len(points)), 3))
        result.update(points=points, scale=scale,
                      four_sets_checked=comb(len(points), 4),
                      three_sets_checked=comb(len(points), 3),
                      forbidden_quadruples=sorted(forbidden))
    return result


def main():
    if not __debug__:
        raise SystemExit("Assertions must remain enabled.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("graph-cover-audit.json"))
    args = parser.parse_args()
    records = []
    for n in range(6):
        possible = list(combinations(range(n), 2))
        for graph_mask in range(1 << len(possible)):
            edges = [edge for i, edge in enumerate(possible) if graph_mask >> i & 1]
            geometry = bool(edges) and (n <= 4 or graph_mask % 41 == 0
                                        or graph_mask in (1, 31, (1 << len(possible))-1))
            record = audit_graph(n, edges, geometry)
            record["graph_mask"] = graph_mask
            records.append(record)
        print("all graphs", n, 1 << len(possible), flush=True)
    # The promised unique-maximum NP-hardness uses two disjoint K2 components.
    augmented = []
    for n, edges in [(0, []), (3, [(0, 1), (1, 2)]),
                     (4, list(combinations(range(4), 2)))]:
        enlarged = edges + [(n, n+1), (n+2, n+3)]
        record = audit_graph(n+4, enlarged, True)
        assert record["vertex_cover"] == vertex_cover_number(n, edges)+2
        assert record["vertex_cover"] >= 2
        augmented.append(record)
    result = dict(scope="Finite checks of the universal reduction in graph_cover_reduction.md",
                  all_graphs=records, unique_maximum_augmented_cases=augmented,
                  graphs_checked=len(records),
                  graph_geometry_checks=sum("points" in record for record in records)+len(augmented),
                  four_sets_checked=sum(record.get("four_sets_checked", 0)
                                        for record in records+augmented),
                  three_sets_checked=sum(record.get("three_sets_checked", 0)
                                         for record in records+augmented),
                  candidate_transversals_inspected=sum(record["candidate_transversals_inspected"]
                                                       for record in records+augmented))
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print({key: value for key, value in result.items()
           if key not in ("all_graphs", "unique_maximum_augmented_cases")}, flush=True)


if __name__ == "__main__":
    main()
