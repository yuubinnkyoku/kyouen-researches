#!/usr/bin/env python3
"""Compose K0344 modules, components and exact residual-isomorphism memoization.

Reference experiment only.  The residual-isomorphism key is enabled after
module reduction/component splitting and only when the remaining legal vertex
count is at most iso_gate.  A gated-out canonical label falls back to the exact
raw residual state key, so correctness never depends on a heuristic hash.
"""
from __future__ import annotations

import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from module_core import bits, minimal, play, compress, components  # noqa: E402
from residual_iso import canonical_label  # noqa: E402


def grundy_micro(vertices: int, edges: tuple[int, ...], iso_gate: int = 6,
                 max_permutations: int = 200_000) -> dict:
    edges = minimal(edges)
    raw_memo: dict[tuple[int, tuple[int, ...]], int] = {}
    iso_memo: dict[tuple, int] = {}
    stats = {"raw_hits": 0, "iso_attempts": 0, "iso_hits": 0,
             "iso_gated_out": 0, "component_splits": 0,
             "module_vertices_removed": 0}

    def evaluate(vs: int, es: tuple[int, ...]) -> int:
        before = vs.bit_count()
        vs, es = compress(vs, es)
        stats["module_vertices_removed"] += before - vs.bit_count()

        parts = components(vs, es)
        if len(parts) > 1:
            stats["component_splits"] += 1
            answer = 0
            for pvs, pes in parts:
                answer ^= evaluate(pvs, pes)
            return answer

        raw_key = (vs, es)
        if vs.bit_count() <= iso_gate:
            stats["iso_attempts"] += 1
            label = canonical_label(vs, es, max_permutations=max_permutations)
            if label is not None:
                if label in iso_memo:
                    stats["iso_hits"] += 1
                    return iso_memo[label]
                answer = recurse(vs, es)
                iso_memo[label] = answer
                # Also seed the raw memo so a later gated path cannot redo it.
                raw_memo[raw_key] = answer
                return answer
            stats["iso_gated_out"] += 1

        if raw_key in raw_memo:
            stats["raw_hits"] += 1
            return raw_memo[raw_key]
        answer = recurse(vs, es)
        raw_memo[raw_key] = answer
        return answer

    def recurse(vs: int, es: tuple[int, ...]) -> int:
        values = {evaluate(*play(vs, es, v)) for v in bits(vs)}
        answer = 0
        while answer in values:
            answer += 1
        return answer

    value = evaluate(vertices, edges)
    return {"grundy": value, "raw_memo_states": len(raw_memo),
            "iso_memo_states": len(iso_memo), **stats}


def self_test():
    # Isomorphic residual games with arbitrary labels must agree and can share
    # an iso key; baseline theorem-backed module/component solver is oracle.
    from module_core import grundy
    cases = [
        (0b1111, (0b0011, 0b1101)),
        (0b11111, (0b00111, 0b11001, 0b10110)),
        (0b111111, (0b000111, 0b011001, 0b101010, 0b110100)),
    ]
    for vs, es in cases:
        es = minimal(es)
        ref = grundy(vs, es, "modules-components")["grundy"]
        got = grundy_micro(vs, es, iso_gate=6)["grundy"]
        assert got == ref, (vs, es, ref, got)
    return "VERIFIED"


if __name__ == "__main__":
    print(self_test())
