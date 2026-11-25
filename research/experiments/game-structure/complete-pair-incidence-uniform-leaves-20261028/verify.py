#!/usr/bin/env python3
"""Two independent exact solvers for clique + all pair nodes + uniform leaves."""
from functools import lru_cache
from itertools import combinations


def closed_form(x, t):
    assert x >= 0 and t >= 0
    if x == 0:
        return 0
    if x == 1:
        return 2 if t > 0 and t % 2 == 0 else 1
    if x == 2:
        return 3 if t % 2 else 1
    if x == 3:
        return 0
    if x == 4:
        return t % 2
    if t % 2:
        return int(x % 4 in (0, 1))
    return int(x % 4 in (1, 2))


@lru_cache(None)
def two_parameter_mex(x, t):
    """Uses the three symmetry classes of moves, not the proposed formula."""
    if x == 0:
        return 0
    seen = {((x - 1) * t + (x - 1) * (x - 2) // 2) & 1}
    if t:
        seen.add(two_parameter_mex(x - 1, t + 1) ^ ((t - 1) & 1))
    if x >= 2:
        seen.add(two_parameter_mex(x - 2, t + 2))
    return next(v for v in range(4) if v not in seen)


def named_vertex_mex(x, t):
    """Direct closed-neighborhood deletion on named vertices; no symmetry quotient."""
    n = x + x * t + x * (x - 1) // 2
    adj = [0] * n
    for a in range(x):
        adj[a] = ((1 << x) - 1) ^ (1 << a)
    at = x
    for a in range(x):
        for _ in range(t):
            adj[at] |= 1 << a
            adj[a] |= 1 << at
            at += 1
    for a, b in combinations(range(x), 2):
        adj[at] |= (1 << a) | (1 << b)
        adj[a] |= 1 << at
        adj[b] |= 1 << at
        at += 1
    assert at == n

    @lru_cache(None)
    def sg(mask):
        values = set()
        rest = mask
        while rest:
            bit = rest & -rest
            rest -= bit
            vertex = bit.bit_length() - 1
            values.add(sg(mask & ~(bit | adj[vertex])))
        result = 0
        while result in values:
            result += 1
        return result

    return sg((1 << n) - 1), sg.cache_info().currsize


def main():
    count, states = 0, 0
    for x in range(0, 9):
        for t in range(0, 9):
            n = x + x * t + x * (x - 1) // 2
            if n > 21:
                continue
            via_graph, visited = named_vertex_mex(x, t)
            via_symmetry = two_parameter_mex(x, t)
            assert via_graph == via_symmetry == closed_form(x, t), (x, t, via_graph, via_symmetry)
            count += 1
            states += visited
    more = 0
    for x in range(0, 401):
        for t in range(0, 21):
            assert two_parameter_mex(x, t) == closed_form(x, t), (x, t)
            more += 1
    print(f"direct graph cases={count}, visited named-vertex states={states}; "
          f"symmetry recurrence/formula cases={more}; all agree")
    print("no leaves, x=1..20:", [closed_form(x, 0) for x in range(1, 21)])


if __name__ == '__main__':
    main()
