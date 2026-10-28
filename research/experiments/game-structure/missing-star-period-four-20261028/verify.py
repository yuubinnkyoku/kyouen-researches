#!/usr/bin/env python3
"""Independent named-vertex Node Kayles vs two proven missing-star recurrences.

The named-vertex solver does not use the closed formulas. Induction-step
checks substitute the proposed formulas for smaller-a states and verify mex.
"""
from functools import lru_cache


def mex(options):
    values = set(options)
    result = 0
    while result in values:
        result += 1
    return result


def uniform_formula(a, b):
    assert a >= 0 and b >= 0
    if a == 0:
        return 1
    return ((3, 1, 2, 0) if b % 2 == 0 else (1, 2, 0, 3))[a % 4]


def marked_formula(a, b):
    assert a >= 1 and b >= 0
    if a == 1:
        return 2 if b % 2 == 0 else 1
    return ((2, 2, 3, 3) if b % 2 == 0 else (2, 3, 3, 2))[a % 4]


def uniform_options(a, b, child):
    options = [(a * (a - 1) // 2 + a * b) % 2]  # apex clique
    if a:
        options.append(((a - 1) * (a - 2) // 2 + (a - 1) * b) % 2)
    if a and b:
        options.append(child(a - 1, b + 1) ^ ((b - 1) % 2))
    if a >= 2:
        options.append(child(a - 2, b + 2))
    return options


def marked_options(a, b, uniform_child, marked_child):
    assert a >= 1
    if a == 1:
        return uniform_options(1, b + 1, uniform_child)
    pair_survivors = (a - 1) * (a - 2) // 2 + (a - 1) * b
    options = [
        (a * (a - 1) // 2 + a * b + 1) % 2,  # apex clique
        pair_survivors % 2,  # marked outer clique
        (pair_survivors + 1) % 2,  # unmarked outer clique
        uniform_child(a - 1, b + 1) ^ (b % 2),  # marked leaf
        uniform_child(a - 2, b + 2) ^ 1,  # marked-unmarked pair
    ]
    if b:
        options.append(marked_child(a - 1, b + 1) ^ ((b - 1) % 2))
    if a >= 3:
        options.append(marked_child(a - 2, b + 2))
    return options


@lru_cache(None)
def uniform_recurrence(a, b):
    return mex(uniform_options(a, b, uniform_recurrence))


@lru_cache(None)
def marked_recurrence(a, b):
    return mex(marked_options(a, b, uniform_recurrence, marked_recurrence))


def named_vertex_solver(a, b, marked=False):
    """Build all independent vertices separately; delete closed neighborhoods."""
    k = a + 1
    adjacency = [0] * k

    def new_vertex():
        adjacency.append(0)
        return len(adjacency) - 1

    def edge(i, j):
        adjacency[i] |= 1 << j
        adjacency[j] |= 1 << i

    for i in range(k):
        for j in range(i + 1, k):
            edge(i, j)
    for i in range(1, k):
        for j in range(i + 1, k):
            v = new_vertex()
            edge(v, i)
            edge(v, j)
    for i in range(1, k):
        for _ in range(b + int(marked and i == 1)):
            v = new_vertex()
            edge(v, i)

    @lru_cache(None)
    def grundy(mask):
        options = 0
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            i = bit.bit_length() - 1
            remaining ^= bit
            options |= 1 << grundy(mask & ~(adjacency[i] | bit))
        value = 0
        while (options >> value) & 1:
            value += 1
        return value

    value = grundy((1 << len(adjacency)) - 1)
    return value, len(adjacency), grundy.cache_info().currsize


def main():
    for a in range(121):
        for b in range(121):
            assert uniform_recurrence(a, b) == uniform_formula(a, b), (a, b)
            if a:
                assert marked_recurrence(a, b) == marked_formula(a, b), (a, b)
    print("PASS: 14,641 uniform + 14,520 marked recurrence states")

    # All 8 residue classes; distinguish b=0 from positive even b.
    for a in range(3, 11):
        for b in (0, 1, 2, 3):
            assert mex(uniform_options(a, b, uniform_formula)) == uniform_formula(a, b)
    for a in range(4, 12):
        for b in (0, 1, 2, 3):
            assert mex(marked_options(a, b, uniform_formula, marked_formula)) == marked_formula(a, b)
    print("PASS: 32 uniform + 32 marked symbolic induction-step cases")

    checked = 0
    total_states = 0
    for a in range(1, 7):
        for b in (0, 1):
            if a == 6 and b == 1:
                continue  # Avoid a four-million-state named-vertex case.
            for marked in (False, True):
                got, n, states = named_vertex_solver(a, b, marked)
                expected = marked_formula(a, b) if marked else uniform_formula(a, b)
                assert got == expected, (a, b, marked, got, expected)
                checked += 1
                total_states += states
                if a == 6 and b == 0:
                    print(f"apex+6, one extra leaf={marked}: vertices={n}, g={got}, named states={states}")
    print(f"PASS: {checked} named-vertex graphs; {total_states} memoized states (summed)")

    # Every d>=2 has a counterexample at k=d+1; the proof is by residues.
    for a in range(2, 102):
        u = ((a * (a - 1) // 2) + 1) & 1
        predicted = 2 + u
        assert marked_formula(a, 0) != predicted
    print("PASS: one-extra-leaf counterexample for every a>=2 (by four-residue theorem)")


if __name__ == "__main__":
    main()
