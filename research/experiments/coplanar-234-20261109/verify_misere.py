#!/usr/bin/env python3
"""Exact misere outcome audit for coplanar-four 2x3x4.

Run beside verify.py: python verify_misere.py
Terminal position is winning for the player to move (misere convention).
"""
from collections import Counter
from functools import lru_cache
from verify import N, moves

@lru_cache(None)
def winning(state):
    successors = tuple(moves(state))
    if not successors:
        return True
    return any(not winning(child) for child in successors)

assert winning(0)
assert all(not winning(1 << i) for i in range(N))
assert winning.cache_info().currsize == 31529

# Exhaustive position classification, not just the root's short-circuit.
counts = Counter()
visited = {0}
pending = [0]
while pending:
    state = pending.pop()
    counts[(state.bit_count(), winning(state))] += 1
    for child in moves(state):
        if child not in visited:
            visited.add(child)
            pending.append(child)

assert len(visited) == 31529
assert counts == {
    (0, True): 1,
    (1, False): 24,
    (2, True): 276,
    (3, False): 1952,
    (3, True): 72,
    (4, False): 8,
    (4, True): 8492,
    (5, False): 13872,
    (5, True): 1184,
    (6, True): 5648,
}
print("PASS: misere 2x3x4, 31529 states; root N; all 24 first moves P")
