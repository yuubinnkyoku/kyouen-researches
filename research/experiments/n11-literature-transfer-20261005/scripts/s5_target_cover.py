#!/usr/bin/env python3
"""Othello-style target selection for the n=11 center-corner s4 cover.

The weak-solve lesson transferred here is to minimize the *intermediate exact
positions that must be solved*, not merely the number of s4 classes.

For the fixed root {0,60}, regenerate every safe s4 D4 class, expand each raw
edge to its legal canonical s5 children, then build an optimistic LOSS cover.
An optional persistent s5 cache makes already-proved LOSS children free and
forbids any class that already contains a proved WIN child.

The greedy score is

    marginal new unknown canonical s5 keys / newly covered third moves.

This is a planning heuristic, not a proof of optimality and not an n=11
winner claim.  Any selected class still has to be proved LOSS by exact search.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path

N = 11
V = N * N
ROOT_PAIR = (0, 60)
VERTICES = tuple(v for v in range(V) if v not in ROOT_PAIR)


def xy(v: int) -> tuple[int, int]:
    return v % N, v // N


def det3(a):
    return (
        a[0][0] * (a[1][1] * a[2][2] - a[1][2] * a[2][1])
        - a[0][1] * (a[1][0] * a[2][2] - a[1][2] * a[2][0])
        + a[0][2] * (a[1][0] * a[2][1] - a[1][1] * a[2][0])
    )


def det4(ids) -> int:
    m = []
    for v in ids:
        x, y = xy(v)
        m.append([x * x + y * y, x, y, 1])
    answer = 0
    for col in range(4):
        sub = [[m[r][j] for j in range(4) if j != col] for r in range(1, 4)]
        answer += (1 if col % 2 == 0 else -1) * m[0][col] * det3(sub)
    return answer


def transforms(v: int) -> tuple[int, ...]:
    x, y = xy(v)
    pts = (
        (x, y),
        (N - 1 - x, y),
        (x, N - 1 - y),
        (N - 1 - x, N - 1 - y),
        (y, x),
        (N - 1 - y, x),
        (y, N - 1 - x),
        (N - 1 - y, N - 1 - x),
    )
    return tuple(yy * N + xx for xx, yy in pts)


D4 = tuple(transforms(v) for v in range(V))


def canonical_tuple(ids) -> tuple[int, ...]:
    return min(tuple(sorted(D4[v][k] for v in ids)) for k in range(8))


def bits_key(ids) -> tuple[int, int]:
    """Match the C++ Bits canonical ordering: minimum by (hi, lo)."""
    best = None
    for k in range(8):
        lo = hi = 0
        for v in ids:
            q = D4[v][k]
            if q < 64:
                lo |= 1 << q
            else:
                hi |= 1 << (q - 64)
        candidate = (hi, lo)
        if best is None or candidate < best:
            best = candidate
    assert best is not None
    hi, lo = best
    return lo, hi


def load_cache(path: Path | None) -> dict[tuple[int, int], int]:
    if path is None:
        return {}
    out = {}
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            if not line.startswith("s5verdict,"):
                continue
            f = line.strip().split(",")
            if len(f) < 6:
                continue
            lo, hi, stones, result = map(int, f[1:5])
            if stones != 5 or result not in (1, 2):
                continue
            key = (lo, hi)
            old = out.get(key)
            if old is not None and old != result:
                raise ValueError(f"conflicting cache verdict for {key}")
            out[key] = result
    return out


def enumerate_classes():
    groups = defaultdict(list)
    safe_edges = 0
    for i, u in enumerate(VERTICES):
        for v in VERTICES[i + 1 :]:
            quad = (*ROOT_PAIR, u, v)
            if det4(quad) == 0:
                continue
            safe_edges += 1
            groups[canonical_tuple(quad)].append((u, v))
    return groups, safe_edges


def legal_fifth_children(edge: tuple[int, int]) -> frozenset[tuple[int, int]]:
    u, v = edge
    occupied = (*ROOT_PAIR, u, v)
    occupied_set = set(occupied)
    triples = tuple(combinations(occupied, 3))
    children = set()
    for x in range(V):
        if x in occupied_set:
            continue
        if all(det4((*tri, x)) != 0 for tri in triples):
            children.add(bits_key((*occupied, x)))
    return frozenset(children)


def build_data(groups, cache):
    result = {}
    edge_child_cache = {}
    for key, edges in groups.items():
        coverage = set()
        unknown = set()
        known_win = False
        known_loss = 0
        child_union = set()
        for edge in edges:
            coverage.update(edge)
            children = edge_child_cache.get(edge)
            if children is None:
                children = legal_fifth_children(edge)
                edge_child_cache[edge] = children
            child_union.update(children)
            for child in children:
                verdict = cache.get(child)
                if verdict == 1:
                    known_win = True
                elif verdict == 2:
                    known_loss += 1
                else:
                    unknown.add(child)
        result[key] = {
            "coverage": frozenset(coverage),
            "children": frozenset(child_union),
            "unknown": frozenset(unknown),
            "known_win": known_win,
            "known_loss_observations": known_loss,
            "raw_edges": tuple(edges),
        }
    return result


def greedy_unknown_cover(data):
    uncovered = set(VERTICES)
    planned_unknown = set()
    remaining = {k for k, row in data.items() if not row["known_win"]}
    selected = []
    while uncovered:
        best = None
        for key in remaining:
            row = data[key]
            new_cov = row["coverage"] & uncovered
            if not new_cov:
                continue
            marginal = row["unknown"] - planned_unknown
            score = (
                len(marginal) / len(new_cov),
                len(marginal),
                -len(new_cov),
                key,
            )
            if best is None or score < best[0]:
                best = (score, key, new_cov, marginal)
        if best is None:
            return selected, planned_unknown, uncovered
        _, key, new_cov, marginal = best
        row = data[key]
        selected.append(
            {
                "key": list(key),
                "new_coverage": len(new_cov),
                "coverage": len(row["coverage"]),
                "marginal_unknown_s5": len(marginal),
                "class_unknown_s5": len(row["unknown"]),
                "class_all_s5": len(row["children"]),
                "covered_total": len(VERTICES) - len(uncovered) + len(new_cov),
                "planned_unknown_s5_total": len(planned_unknown | marginal),
            }
        )
        uncovered.difference_update(new_cov)
        planned_unknown.update(marginal)
        remaining.remove(key)
    return selected, planned_unknown, uncovered


def witness_cost(data, witness_keys, cache):
    children = set()
    unknown = set()
    forbidden = 0
    for key in witness_keys:
        row = data[tuple(key)]
        children.update(row["children"])
        unknown.update(row["unknown"])
        forbidden += int(row["known_win"])
    return {
        "classes": len(witness_keys),
        "all_canonical_s5": len(children),
        "unknown_canonical_s5": len(unknown),
        "classes_with_known_win": forbidden,
        "known_cache_entries": len(cache),
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--cache", type=Path)
    ap.add_argument("--out", type=Path)
    ap.add_argument(
        "--witness",
        type=Path,
        default=Path(__file__).resolve().parents[2]
        / "n11-cover-duality/output/center-corner-cover.json",
    )
    args = ap.parse_args()

    cache = load_cache(args.cache)
    groups, safe_edges = enumerate_classes()
    data = build_data(groups, cache)

    hist = Counter(len(row["coverage"]) for row in data.values())
    assert safe_edges == 6894
    assert len(groups) == 3396
    assert hist == Counter({2: 51, 3: 437, 4: 2832, 5: 33, 6: 43})

    cover_doc = json.loads(args.witness.read_text(encoding="utf-8"))
    case = next(row for row in cover_doc["cases"] if row["n"] == 11)
    witness_keys = [row["key"] for row in case["classes"]]
    assert case["optimal_class_count"] == 31
    assert len(witness_keys) == 31

    selected, planned_unknown, uncovered = greedy_unknown_cover(data)
    output = {
        "scope": "n11 center-corner root {0,60}; structural optimistic LOSS planning",
        "n11_empty_root_outcome": "UNKNOWN",
        "method": (
            "greedy marginal distinct unknown canonical s5 keys per newly covered "
            "third move; known WIN child forbids a class"
        ),
        "counts": {
            "safe_raw_edges": safe_edges,
            "s4_classes": len(groups),
            "third_moves": len(VERTICES),
            "coverage_histogram": {str(k): hist[k] for k in sorted(hist)},
            "cache_entries": len(cache),
        },
        "existing_31_class_witness": witness_cost(data, witness_keys, cache),
        "greedy_target_cover": {
            "classes": len(selected),
            "planned_unknown_canonical_s5": len(planned_unknown),
            "uncovered_third_moves": sorted(uncovered),
            "selected": selected,
        },
        "limitations": [
            "Selected classes are only optimistic LOSS candidates until every required s5 child is exactly proved LOSS.",
            "Greedy selection is not claimed optimal.",
            "A later WIN verdict can invalidate a selected class and requires replanning, exactly as in target-set weak solving.",
            "The structural no-cache run measures target count, not wall time; s5 positions have unequal exact-search costs.",
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
