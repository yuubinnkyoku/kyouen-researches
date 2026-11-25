#!/usr/bin/env python3
"""Audit maker-breaker-style vertex domination on Kyouen residual games.

The 7-in-a-row literature uses incidence domination to discard moves in a
maker-breaker hypergraph.  Kyouen's late residual game is instead impartial
normal play, so that rule is not automatically sound.

Input is a JSON snapshot corpus with rows containing
  legal: live board vertices
  minimal_residual_edges: inclusion-minimal forbidden live sets.

For every residual incidence component containing a strict relation
  incident_edges(u) ⊃ incident_edges(v)
we solve the component exactly and test the one-sided pruning implication

  if playing v is winning (child Grundy 0), then playing u is also winning.

This implication is what would be needed to discard the incidence-dominated
move v in favour of u.  A counterexample is fatal to that pruning rule.

The script also checks a four-vertex abstract clutter counterexample, showing
that incidence domination is NOT valid for arbitrary impartial clutters even
before looking at geometric Kyouen positions.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
TWIN = ROOT / "research/experiments/n11-residual-twins/scripts"
sys.path.insert(0, str(TWIN))
from twin_core import bits, minimal, play  # noqa: E402


def components(vertices: int, edges: tuple[int, ...]):
    out = []
    rest = vertices
    while rest:
        seed = rest & -rest
        reached = seed
        prev = -1
        while reached != prev:
            prev = reached
            for edge in edges:
                if edge & reached:
                    reached |= edge
        out.append((reached, tuple(edge for edge in edges if edge & reached)))
        rest &= ~reached
    return out


def exact_solver():
    @lru_cache(None)
    def g(vertices: int, edges: tuple[int, ...]) -> int:
        edges = minimal(edges)
        values = {g(*play(vertices, edges, v)) for v in bits(vertices)}
        answer = 0
        while answer in values:
            answer += 1
        return answer
    return g


def domination_pairs(vertices: int, edges: tuple[int, ...]):
    es = tuple(edges)
    incidence = {
        v: frozenset(i for i, edge in enumerate(es) if edge & (1 << v))
        for v in bits(vertices)
    }
    for u in bits(vertices):
        for v in bits(vertices):
            if u == v:
                continue
            if incidence[u] > incidence[v]:
                yield u, v, incidence[u], incidence[v]


def localize(legal, edge_rows):
    order = sorted(legal)
    index = {v: i for i, v in enumerate(order)}
    vertices = (1 << len(order)) - 1
    edges = []
    for row in edge_rows:
        mask = 0
        for v in row:
            mask |= 1 << index[v]
        edges.append(mask)
    return order, vertices, minimal(edges)


def abstract_counterexample():
    # Minimal edges {0,1,2} and {0,1,3}.  Vertex 0 strictly dominates vertex
    # 2 by incidence, but 2 is a winning move while 0 is losing.
    vertices = 0b1111
    edges = minimal((0b0111, 0b1011))
    g = exact_solver()
    u, v = 0, 2
    gu = g(*play(vertices, edges, u))
    gv = g(*play(vertices, edges, v))
    assert gv == 0 and gu != 0
    return {
        "vertices": [0, 1, 2, 3],
        "minimal_edges": [[0, 1, 2], [0, 1, 3]],
        "dominating_vertex": u,
        "dominated_vertex": v,
        "child_grundy_after_dominating": gu,
        "child_grundy_after_dominated": gv,
        "status": "COUNTEREXAMPLE_TO_GENERAL_RULE",
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("snapshots", type=Path)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    doc = json.loads(args.snapshots.read_text(encoding="utf-8"))
    rows = doc["snapshots"]
    transition = Counter()
    size_hist = Counter()
    component_count = 0
    dominated_components = 0
    pair_count = 0
    max_memo = 0
    witness = None
    non_equal_examples = []

    for si, snap in enumerate(rows):
        order, vertices, edges = localize(
            snap["legal"], snap["minimal_residual_edges"]
        )
        for c_vertices, c_edges in components(vertices, edges):
            component_count += 1
            pairs = list(domination_pairs(c_vertices, c_edges))
            if not pairs:
                continue
            dominated_components += 1
            size = c_vertices.bit_count()
            size_hist[size] += 1

            g = exact_solver()
            root_g = g(c_vertices, minimal(c_edges))
            for u, v, iu, iv in pairs:
                pair_count += 1
                gu = g(*play(c_vertices, c_edges, u))
                gv = g(*play(c_vertices, c_edges, v))
                transition[f"{gv}->{gu}"] += 1
                if gu != gv and len(non_equal_examples) < 20:
                    non_equal_examples.append({
                        "snapshot_index": si,
                        "trial": snap.get("trial"),
                        "component_size": size,
                        "dominating_vertex": order[u],
                        "dominated_vertex": order[v],
                        "dominating_incidence_degree": len(iu),
                        "dominated_incidence_degree": len(iv),
                        "child_grundy_after_dominating": gu,
                        "child_grundy_after_dominated": gv,
                    })
                if gv == 0 and gu != 0 and witness is None:
                    witness = {
                        "snapshot_index": si,
                        "trial": snap.get("trial"),
                        "occupied": snap.get("occupied"),
                        "legal": snap["legal"],
                        "component_vertices": [
                            order[vv] for vv in bits(c_vertices)
                        ],
                        "component_edges": [
                            [order[vv] for vv in bits(edge)]
                            for edge in c_edges
                        ],
                        "component_grundy": root_g,
                        "dominating_vertex": order[u],
                        "dominated_vertex": order[v],
                        "dominating_incidence_degree": len(iu),
                        "dominated_incidence_degree": len(iv),
                        "child_grundy_after_dominating": gu,
                        "child_grundy_after_dominated": gv,
                    }
            max_memo = max(max_memo, g.cache_info().currsize)

    result = {
        "source": str(args.snapshots),
        "n": doc.get("n"),
        "trials": doc.get("trials"),
        "snapshots": len(rows),
        "abstract_counterexample": abstract_counterexample(),
        "residual_components": component_count,
        "components_with_strict_incidence_domination": dominated_components,
        "ordered_domination_pairs": pair_count,
        "dominated_component_size_histogram": dict(sorted(size_hist.items())),
        "child_grundy_transition_dominated_to_dominating":
            dict(sorted(transition.items())),
        "geometric_counterexample": witness,
        "geometric_implication_holds_on_sample": witness is None,
        "max_exact_memo_states_for_tested_component": max_memo,
        "non_equal_grundy_examples": non_equal_examples,
        "claim": (
            "a non-null geometric_counterexample refutes direct incidence-"
            "domination pruning for Kyouen; a null witness would only be a "
            "finite-sample non-refutation"
        ),
    }
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    print(text, end="")
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    return 1 if witness is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
