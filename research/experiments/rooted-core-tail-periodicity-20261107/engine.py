#!/usr/bin/env python3
"""Exact rooted-clutter + one path recurrence. No geometric assumptions."""
from functools import lru_cache
from itertools import permutations


def mex(options):
    g = 0
    while g in options:
        g += 1
    return g


@lru_cache(None)
def canonical(n, forbidden):
    if n <= 1:
        return n, forbidden
    best = None
    for tail in permutations(range(1, n)):
        order = (0,) + tail
        inverse = {old: new for new, old in enumerate(order)}
        edges = tuple(sorted(sum(1 << inverse[v] for v in range(n) if edge >> v & 1)
                             for edge in forbidden))
        if best is None or edges < best:
            best = edges
    return n, best


def remap(active, forbidden, old_n):
    order = [v for v in range(old_n) if active >> v & 1]
    inverse = {old: new for new, old in enumerate(order)}
    edges = {sum(1 << inverse[v] for v in order if edge >> v & 1) for edge in forbidden
             if not edge & ~active}
    edges = tuple(sorted(edge for edge in edges if not any(other != edge and other & edge == other
                                                         for other in edges)))
    assert all(edge.bit_count() >= 2 for edge in edges)
    return canonical(len(order), edges)


@lru_cache(None)
def play(state, vertex):
    n, forbidden = state
    bit = 1 << vertex
    reduced = [edge & ~bit for edge in forbidden]
    blocked = sum({edge for edge in reduced if edge.bit_count() == 1})
    active = ((1 << n) - 1) & ~bit & ~blocked
    return remap(active, reduced, n), bool(active & 1)


@lru_cache(None)
def ordinary(state):
    return mex({ordinary(play(state, v)[0]) for v in range(state[0])})


def delete_root(state):
    n, forbidden = state
    return remap(((1 << n) - 1) & ~1, [edge for edge in forbidden if not edge & 1], n)


def path_values(limit):
    result = [0]
    for n in range(1, limit + 1):
        result.append(mex({result[max(j - 1, 0)] ^ result[max(n - j - 2, 0)] for j in range(n)}))
    return result


def closure(initial):
    found = set()
    pending = list(initial)
    while pending:
        state = pending.pop()
        if state in found:
            continue
        found.add(state)
        for v in range(1, state[0]):
            child, root_alive = play(state, v)
            if root_alive:
                pending.append(child)
    return sorted(found, key=lambda state: (state[0], state[1]))


def solve(initial, limit, progress=None):
    initial = [canonical(n, tuple(sorted(edges))) for n, edges in initial]
    states = closure(initial)
    path = path_values(limit + 1)
    values = {state: [] for state in states}
    data = {}
    for state in states:
        after_root = ordinary(play(state, 0)[0])
        without_root = ordinary(delete_root(state))
        retained, detached = [], []
        for v in range(1, state[0]):
            child, root_alive = play(state, v)
            if root_alive:
                retained.append(child)
            else:
                detached.append(ordinary(child))
        data[state] = after_root, without_root, set(retained), set(detached)
    for length in range(limit + 1):
        for state in states:
            after_root, without_root, retained, detached = data[state]
            seq = values[state]
            options = {after_root ^ path[max(length - 1, 0)]}
            options.update(values[child][length] for child in retained)
            options.update(g ^ path[length] for g in detached)
            if length >= 1:
                options.add(without_root ^ path[max(length - 2, 0)])
            if length >= 2:
                options.add(seq[length - 2])
                options.update(seq[i] ^ path[length - 3 - i] for i in range(length - 2))
            seq.append(mex(options))
        if progress is not None and length % 100 == 0:
            progress(length, len(states), max(values[state][-1] for state in states))
    return initial, states, values, path


def last_period_failure(sequence, period):
    return max((i for i in range(len(sequence) - period) if sequence[i] != sequence[i + period]), default=-1)
