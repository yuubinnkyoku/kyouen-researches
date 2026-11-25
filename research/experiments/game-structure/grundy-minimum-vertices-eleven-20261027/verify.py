#!/usr/bin/env python3
"""Independent, exact verification of 13--17-vertex Node Kayles witnesses.

Run: python3 verify.py
No external dependencies. No randomized tests or heuristic pruning.
"""
from functools import lru_cache

BASE_EDGES = (
    (0, 2), (0, 7), (0, 8), (0, 9),
    (1, 3), (1, 4), (1, 5), (1, 7),
    (2, 4), (2, 5), (2, 7),
    (3, 4), (3, 6),
    (4, 11), (8, 11), (10, 11), (11, 12),
)


def verify(n: int, edges: tuple[tuple[int, int], ...], expected: int) -> None:
    closed = [1 << i for i in range(n)]
    for u, v in edges:
        assert 0 <= u < v < n
        closed[u] |= 1 << v
        closed[v] |= 1 << u

    # First evaluator: keep the set of vertices still present, delete N[v].
    @lru_cache(maxsize=None)
    def remaining_game(state: int) -> int:
        children = set()
        for v in range(n):
            if (state >> v) & 1:
                children.add(remaining_game(state & ~closed[v]))
        return next(k for k in range(n + 1) if k not in children)

    # Second evaluator: keep an independent set of already chosen vertices.
    # This does not call remaining_game and has a different state encoding.
    @lru_cache(maxsize=None)
    def occupied_game(occupied: int) -> int:
        children = set()
        for v in range(n):
            if not (closed[v] & occupied):
                children.add(occupied_game(occupied | (1 << v)))
        return next(k for k in range(n + 1) if k not in children)

    value1 = remaining_game((1 << n) - 1)
    value2 = occupied_game(0)
    assert value1 == value2 == expected, (n, value1, value2, expected)

    # Exhaustive independence-number computation, separate from the mex DPs.
    independent = [False] * (1 << n)
    independent[0] = True
    alpha = 0
    for state in range(1, 1 << n):
        bit = state & -state
        v = bit.bit_length() - 1
        rest = state ^ bit
        independent[state] = independent[rest] and not (closed[v] & rest)
        if independent[state]:
            alpha = max(alpha, state.bit_count())

    assert alpha == expected, (n, alpha, expected)
    tau = n - alpha
    assert tau == (n - expected)
    # Mathematical lower bound: g>=4 => n>=g+ceil((g+1)/2).
    lower_bound = expected + (expected + 2) // 2
    assert n == lower_bound, (n, lower_bound)
    children = [remaining_game(((1 << n) - 1) & ~closed[v]) for v in range(n)]
    assert set(range(expected)).issubset(children)
    print(f"n={n}, edges={len(edges)}, g={value1}, alpha={alpha}, tau={tau}, "
          f"lower_bound={lower_bound}, states=({remaining_game.cache_info().currsize},"
          f"{occupied_game.cache_info().currsize})")
    if n == 13:
        assert children == [1, 0, 2, 2, 1, 4, 6, 3, 5, 5, 7, 2, 7]
        print("g8 child nimbers:", children)


def main() -> None:
    # g=8, n=13: one explicit graph; g=9 is its disjoint union with K1.
    verify(13, BASE_EDGES, 8)
    verify(14, BASE_EDGES, 9)
    # g=10: disjoint union with P3, whose Grundy value is 2.
    path3 = ((13, 14), (14, 15))
    verify(16, BASE_EDGES + path3, 10)
    # g=11: also add one isolated vertex.
    verify(17, BASE_EDGES + path3, 11)


if __name__ == "__main__":
    main()
