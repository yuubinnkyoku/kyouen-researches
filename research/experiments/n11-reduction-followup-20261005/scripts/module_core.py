#!/usr/bin/env python3
"""Exact exchangeable-class kernels for the full residual clutter.

Imports the existing K0336 updater/reference; deliberately not integrated
with the shared DFPN solver, since residual-construction overhead is unknown.
"""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-residual-twins/scripts"))
from twin_core import bits, minimal, play  # noqa: E402

if not __debug__:
    raise SystemExit("exact module checks require assertions; do not use python -O")


def exchangeable_classes(vertices: int, edges: tuple[int, ...]) -> list[list[int]]:
    """Classes whose every internal transposition preserves ALL edges."""
    edge_set = set(edges)
    groups: list[list[int]] = []
    for vertex in bits(vertices):
        for group in groups:
            other = group[0]
            pair = (1 << vertex) | (1 << other)
            if all((edge ^ pair) in edge_set for edge in edges
                   if (edge & pair).bit_count() == 1):
                group.append(vertex)
                break
        else:
            groups.append([vertex])
    return groups


def class_kernel(group: list[int], edges: tuple[int, ...]) -> dict:
    mask = sum(1 << v for v in group)
    internal = [edge.bit_count() for edge in edges if edge & ~mask == 0]
    if internal:
        capacity = min(internal) - 1
        return {"kind": "capacity", "keep": min(len(group), capacity),
                "capacity": capacity}
    depth = max(((edge & mask).bit_count() for edge in edges), default=0)
    if depth == 0:
        return {"kind": "isolated-parity", "keep": len(group) % 2, "depth": 0}
    keep = depth + ((len(group) - depth) % 2)
    return {"kind": "mixed-depth-parity", "keep": min(len(group), keep),
            "depth": depth}


def compress(vertices: int, edges: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    """Sequential induced deletion; NEVER contract a deleted vertex."""
    while True:
        for group in exchangeable_classes(vertices, edges):
            keep = class_kernel(group, edges)["keep"]
            if len(group) > keep:
                removed = sum(1 << vertex for vertex in group[keep:])
                vertices &= ~removed
                edges = tuple(edge for edge in edges if not edge & removed)
                break
        else:
            return vertices, edges


def compress_fast(vertices: int, edges: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    """Incidence hashes for independent twins and capacity-one classes.

    Higher-capacity/depth modules may be missed; every performed deletion
    remains covered by the theorem. No quadratic transposition scan.
    """
    while True:
        links = {v: [] for v in bits(vertices)}
        closed_pair_neighbors = {v: 1 << v for v in links}
        higher_links = {v: [] for v in links}
        for edge in edges:
            pair = edge.bit_count() == 2
            for v in bits(edge):
                link = edge ^ (1 << v)
                links[v].append(link)
                if pair:
                    closed_pair_neighbors[v] |= link
                else:
                    higher_links[v].append(link)
        independent = defaultdict(list)
        cliques = defaultdict(list)
        for v in links:
            independent[tuple(sorted(links[v]))].append(v)
            cliques[(closed_pair_neighbors[v], tuple(sorted(higher_links[v])))].append(v)
        removed = 0
        for link, group in independent.items():
            keep = (1 if len(group) % 2 else 2) if link else len(group) % 2
            for v in group[keep:]:
                removed |= 1 << v
        for group in cliques.values():
            for v in group[1:]:
                removed |= 1 << v
        if not removed:
            return vertices, edges
        vertices &= ~removed
        edges = tuple(edge for edge in edges if not edge & removed)


def components(vertices: int, edges: tuple[int, ...]) -> list[tuple[int, tuple[int, ...]]]:
    """Full-incidence components, including isolated vertices."""
    result = []
    while vertices:
        seed = vertices & -vertices
        reached = seed
        previous = 0
        while reached != previous:
            previous = reached
            for edge in edges:
                if edge & reached:
                    reached |= edge
        result.append((reached, tuple(edge for edge in edges if edge & reached)))
        vertices &= ~reached
    return result


def grundy(vertices: int, edges: tuple[int, ...], mode: str) -> dict:
    assert mode in {"baseline", "modules", "modules-components", "fast-modules",
                    "fast-modules-components"}
    edges = minimal(edges)

    def evaluate(vs: int, es: tuple[int, ...]) -> int:
        if mode.startswith("fast-"):
            vs, es = compress_fast(vs, es)
        elif mode != "baseline":
            vs, es = compress(vs, es)
        if mode.endswith("-components"):
            parts = components(vs, es)
            if len(parts) > 1:
                answer = 0
                for component_vertices, component_edges in parts:
                    answer ^= evaluate(component_vertices, component_edges)
                return answer
        return memo(vs, es)

    @lru_cache(None)
    def memo(vs: int, es: tuple[int, ...]) -> int:
        values = {evaluate(*play(vs, es, v)) for v in bits(vs)}
        answer = 0
        while answer in values:
            answer += 1
        return answer

    result = evaluate(vertices, edges)
    return {"grundy": result, "memo_states": memo.cache_info().currsize,
            "memo_hits": memo.cache_info().hits}


def misere_auxiliary(vertices: int, edges: tuple[int, ...], reduce_modules: bool) -> int:
    """h(terminal)=1, h(nonterminal)=mex(child h); NOT a sum-xor value."""
    edges = minimal(edges)

    def evaluate(vs, es):
        if reduce_modules:
            vs, es = compress(vs, es)
        return memo(vs, es)

    @lru_cache(None)
    def memo(vs, es):
        if not vs:
            return 1
        values = {evaluate(*play(vs, es, v)) for v in bits(vs)}
        answer = 0
        while answer in values:
            answer += 1
        return answer

    return evaluate(vertices, edges)
