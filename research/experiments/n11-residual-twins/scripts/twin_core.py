#!/usr/bin/env python3
"""Exact residual games and positive-parity compression of equal links.

An edge is a minimal forbidden set of currently legal vertices. Equal
full hypergraph links define independent twins. This module is specific
to the experiment and is not wired into the shared df-pn solver.
"""
from __future__ import annotations

from collections import defaultdict
from functools import lru_cache

if not __debug__:
    raise SystemExit("exact residual checks require assertions; do not use python -O")


def bits(mask: int) -> list[int]:
    result = []
    while mask:
        bit = mask & -mask
        result.append(bit.bit_length() - 1)
        mask ^= bit
    return result


def minimal(edges) -> tuple[int, ...]:
    candidates = set(edges)
    result = []
    for edge in sorted(candidates, key=lambda e: (e.bit_count(), e)):
        assert edge.bit_count() >= 2
        if not any(sub & edge == sub for sub in result):
            result.append(edge)
    return tuple(sorted(result))


def twin_classes(vertices: int, edges: tuple[int, ...]) -> list[list[int]]:
    groups = defaultdict(list)
    for v in bits(vertices):
        bit = 1 << v
        link = tuple(sorted(edge ^ bit for edge in edges if edge & bit))
        groups[link].append(v)
    return [groups[key] for key in sorted(groups)]


def compress_once(vertices: int, edges: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    removed = 0
    for group in twin_classes(vertices, edges):
        keep = 1 if len(group) % 2 else 2
        for v in group[keep:]:
            removed |= 1 << v
    return vertices & ~removed, tuple(edge for edge in edges if not edge & removed)


def compress(vertices: int, edges: tuple[int, ...]) -> tuple[int, tuple[int, ...]]:
    while True:
        reduced, residual = compress_once(vertices, edges)
        if reduced == vertices:
            return vertices, edges
        vertices, edges = reduced, residual


def play(vertices: int, edges: tuple[int, ...], v: int) -> tuple[int, tuple[int, ...]]:
    bit = 1 << v
    assert vertices & bit
    remaining = vertices ^ bit
    residuals = [edge & ~bit for edge in edges]
    banned = 0
    for edge in residuals:
        if edge.bit_count() == 1:
            banned |= edge
    remaining &= ~banned
    residuals = [edge for edge in residuals if edge.bit_count() >= 2
                 and not edge & ~remaining]
    return remaining, minimal(residuals)


def grundy_residual(vertices: int, edges: tuple[int, ...], reduce_twins: bool) -> dict:
    assert all(edge & ~vertices == 0 and edge.bit_count() >= 2 for edge in edges)
    edges = minimal(edges)

    def evaluate(vs: int, es: tuple[int, ...]) -> int:
        if reduce_twins:
            vs, es = compress(vs, es)
        return memo(vs, es)

    @lru_cache(None)
    def memo(vs: int, es: tuple[int, ...]) -> int:
        values = {evaluate(*play(vs, es, v)) for v in bits(vs)}
        answer = 0
        while answer in values:
            answer += 1
        return answer

    answer = evaluate(vertices, edges)
    info = memo.cache_info()
    return {"grundy": answer, "memo_states": info.currsize, "memo_hits": info.hits}


def grundy_occupied(vertices: int, edges: tuple[int, ...]) -> dict:
    """Reference using the original forbidden edges and occupied subsets.

    Does not update residuals, delete redundant edges, or compress twins.
    """
    edges_at = {v: [edge for edge in edges if edge & (1 << v)] for v in bits(vertices)}

    @lru_cache(None)
    def evaluate(occupied: int) -> int:
        values = set()
        for v in bits(vertices & ~occupied):
            child = occupied | (1 << v)
            if not any(edge & child == edge for edge in edges_at[v]):
                values.add(evaluate(child))
        answer = 0
        while answer in values:
            answer += 1
        return answer

    answer = evaluate(0)
    return {"grundy": answer, "memo_states": evaluate.cache_info().currsize}
