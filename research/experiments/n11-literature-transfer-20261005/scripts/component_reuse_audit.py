#!/usr/bin/env python3
"""Audit cross-position reuse of exact residual components on saved n=11 snapshots.

Motivation: recent massively parallel PNS work on impartial games shares small
Grundy results among workers.  Kyouen's exact residual game already decomposes
by full-incidence connected components, so the relevant empirical question is
whether *the same residual component game* reappears across independent saved
trajectories.

This script uses exact full-clutter isomorphism labels, never pair-only
signatures.  Colour refinement is only a partitioning step; permutations inside
unresolved cells are exhaustively enumerated up to a conservative work gate.
The reported cross-trial repeated types in the saved corpus are all small and
fall below the gate.

The memo-state comparison is a structural estimate:
  naive = solve each repeated component occurrence independently
  shared = solve each exact isomorphism type once and reuse its Grundy number.
It is not a production wall-time benchmark.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import permutations, product
from math import factorial
from pathlib import Path


def bits(mask: int):
    while mask:
        b = mask & -mask
        yield b.bit_length() - 1
        mask ^= b


def minimal(edges):
    result = []
    for edge in sorted(set(edges), key=lambda e: (e.bit_count(), e)):
        if not any((sub & edge) == sub for sub in result):
            result.append(edge)
    return tuple(sorted(result))


def play(vertices: int, edges: tuple[int, ...], v: int):
    bit = 1 << v
    remaining = vertices ^ bit
    residuals = [edge & ~bit for edge in edges]
    banned = 0
    for edge in residuals:
        if edge.bit_count() == 1:
            banned |= edge
    remaining &= ~banned
    residuals = [
        edge
        for edge in residuals
        if edge.bit_count() >= 2 and not (edge & ~remaining)
    ]
    return remaining, minimal(residuals)


def component_list(snapshot):
    legal = set(snapshot["legal"])
    edges = [tuple(edge) for edge in snapshot["minimal_residual_edges"]]
    out = []
    while legal:
        seed = next(iter(legal))
        reached = {seed}
        changed = True
        while changed:
            changed = False
            for edge in edges:
                if reached.intersection(edge):
                    for v in edge:
                        if v not in reached:
                            reached.add(v)
                            changed = True
        comp_edges = [edge for edge in edges if reached.intersection(edge)]
        out.append((tuple(sorted(reached)), tuple(comp_edges)))
        legal.difference_update(reached)
    return out


def _refine(n: int, edges: tuple[tuple[int, ...], ...]):
    incidence = [[] for _ in range(n)]
    for ei, edge in enumerate(edges):
        for v in edge:
            incidence[v].append(ei)

    vcolor = [
        tuple(sum(v in edge for edge in edges if len(edge) == rank) for rank in (2, 3, 4))
        for v in range(n)
    ]
    while True:
        vu = {x: i for i, x in enumerate(sorted(set(vcolor)))}
        vc = [vu[x] for x in vcolor]
        esig = [(len(edge), tuple(sorted(vc[v] for v in edge))) for edge in edges]
        eu = {x: i for i, x in enumerate(sorted(set(esig)))}
        ec = [eu[x] for x in esig]
        nsig = [
            (vc[v], tuple(sorted(ec[ei] for ei in incidence[v])))
            for v in range(n)
        ]
        nu = {x: i for i, x in enumerate(sorted(set(nsig)))}
        nc = [nu[x] for x in nsig]
        if nc == vc:
            return nc
        vcolor = nc


def canonical_label(vertices, edge_lists, max_permutations: int):
    vertices = tuple(sorted(vertices))
    index = {v: i for i, v in enumerate(vertices)}
    edges = tuple(
        sorted(tuple(sorted(index[v] for v in edge)) for edge in edge_lists)
    )
    n = len(vertices)
    colors = _refine(n, edges)
    groups = defaultdict(list)
    for v, color in enumerate(colors):
        groups[color].append(v)
    cells = [groups[c] for c in sorted(groups)]

    work = 1
    for cell in cells:
        work *= factorial(len(cell))
        if work > max_permutations:
            return None

    best = None
    for choices in product(*(permutations(cell) for cell in cells)):
        order = tuple(v for choice in choices for v in choice)
        pos = {v: i for i, v in enumerate(order)}
        code = tuple(
            sorted(tuple(sorted(pos[v] for v in edge)) for edge in edges)
        )
        if best is None or code < best:
            best = code
    return (n, best)


def grundy_stats(vertices, edge_lists):
    vertices = tuple(sorted(vertices))
    index = {v: i for i, v in enumerate(vertices)}
    vs = (1 << len(vertices)) - 1
    edges = minimal(
        tuple(
            sum(1 << index[v] for v in edge)
            for edge in edge_lists
        )
    )

    @lru_cache(None)
    def g(cur_v: int, cur_e: tuple[int, ...]) -> int:
        values = {g(*play(cur_v, cur_e, v)) for v in bits(cur_v)}
        answer = 0
        while answer in values:
            answer += 1
        return answer

    answer = g(vs, edges)
    return answer, g.cache_info().currsize


def main() -> int:
    root = Path(__file__).resolve().parents[4]
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--snapshots",
        type=Path,
        default=root
        / "research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json",
    )
    ap.add_argument("--max-permutations", type=int, default=200_000)
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    doc = json.loads(args.snapshots.read_text(encoding="utf-8"))
    snapshots = doc["snapshots"]

    types = {}
    total_components = 0
    multi_component_snapshots = 0
    gated = 0

    for si, snapshot in enumerate(snapshots):
        comps = component_list(snapshot)
        total_components += len(comps)
        multi_component_snapshots += int(len(comps) > 1)
        for vertices, edges in comps:
            label = canonical_label(vertices, edges, args.max_permutations)
            if label is None:
                gated += 1
                continue
            row = types.setdefault(
                label,
                {
                    "occurrences": 0,
                    "trials": set(),
                    "snapshots": set(),
                    "representative": (vertices, edges),
                },
            )
            row["occurrences"] += 1
            row["trials"].add(snapshot["trial"])
            row["snapshots"].add(si)

    cross = []
    for label, row in types.items():
        if len(row["trials"]) < 2:
            continue
        vertices, edges = row["representative"]
        grundy, memo_states = grundy_stats(vertices, edges)
        cross.append(
            {
                "size": len(vertices),
                "grundy": grundy,
                "memo_states_per_fresh_solve": memo_states,
                "occurrences": row["occurrences"],
                "trials": len(row["trials"]),
                "snapshots": len(row["snapshots"]),
                "naive_memo_states": memo_states * row["occurrences"],
                "shared_once_memo_states": memo_states,
                "saved_memo_states": memo_states * (row["occurrences"] - 1),
            }
        )

    cross.sort(
        key=lambda row: (
            -row["saved_memo_states"],
            -row["trials"],
            -row["occurrences"],
            row["size"],
        )
    )

    by_size = defaultdict(lambda: {"types": 0, "occurrences": 0})
    by_grundy = defaultdict(lambda: {"types": 0, "occurrences": 0})
    for row in cross:
        by_size[row["size"]]["types"] += 1
        by_size[row["size"]]["occurrences"] += row["occurrences"]
        by_grundy[row["grundy"]]["types"] += 1
        by_grundy[row["grundy"]]["occurrences"] += row["occurrences"]

    naive = sum(row["naive_memo_states"] for row in cross)
    shared = sum(row["shared_once_memo_states"] for row in cross)
    nontrivial = [row for row in cross if row["size"] > 1]
    naive_nt = sum(row["naive_memo_states"] for row in nontrivial)
    shared_nt = sum(row["shared_once_memo_states"] for row in nontrivial)

    output = {
        "scope": "826 saved n11 late snapshots from 200 greedy trajectories",
        "n11_empty_root_outcome": "UNKNOWN",
        "method": "exact full minimal-residual-clutter isomorphism; cross-trial reuse only",
        "snapshots": len(snapshots),
        "total_components": total_components,
        "snapshots_with_multiple_components": multi_component_snapshots,
        "gated_components": gated,
        "cross_trial_exact_types": len(cross),
        "cross_trial_occurrences": sum(row["occurrences"] for row in cross),
        "nontrivial_occurrences_size_gt_1": sum(
            row["occurrences"] for row in nontrivial
        ),
        "memo_state_estimate": {
            "naive_recompute": naive,
            "shared_type_once": shared,
            "saved": naive - shared,
            "reduction_ratio": (1.0 - shared / naive) if naive else 0.0,
            "nontrivial_naive_recompute": naive_nt,
            "nontrivial_shared_type_once": shared_nt,
            "nontrivial_saved": naive_nt - shared_nt,
            "nontrivial_reduction_ratio": (
                1.0 - shared_nt / naive_nt if naive_nt else 0.0
            ),
        },
        "by_component_size": {str(k): by_size[k] for k in sorted(by_size)},
        "by_grundy": {str(k): by_grundy[k] for k in sorted(by_grundy)},
        "types": cross,
        "limitations": [
            "The corpus is greedy-trajectory biased, not the distribution of exact-search TT nodes.",
            "Memo-state reduction is not a wall-time benchmark and excludes residual construction/canonical-label overhead.",
            "Cross-trial repetition is required to reduce trivial reuse along one trajectory, but trials are not statistically independent samples of all reachable positions.",
        ],
    }

    text = json.dumps(output, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
