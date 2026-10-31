"""Two independent exact Grundy recurrences for the seven-center split witness."""
from functools import lru_cache

K = 7
SIGNATURES = (3, 3, 4, 4, 5, 9, 9, 16, 33, 33, 64, 64, 68, 80, 84)
EXPECTED_CHILDREN = (0, 1, 0, 1, 0, 1, 0, 2, 2, 4, 4, 2, 2, 2, 6, 2, 2, 7, 7, 4, 5, 3)


def mex(values):
    value = 0
    while value in values:
        value += 1
    return value


def signature_recurrence(k, signatures):
    """DP over center subsets, without individual independent-vertex states."""
    limit = 1 << k
    parity = [sum(bool(s & x) for s in signatures) % 2 for x in range(limit)]
    values = [0] * limit
    for x in range(1, limit):
        options = {parity[x] ^ parity[1 << c] for c in range(k) if x & (1 << c)}
        for s in set(signatures):
            if s & x:
                nxt = x & ~s
                options.add(values[nxt] ^ parity[x] ^ parity[nxt] ^ 1)
        values[x] = mex(options)
    full = limit - 1
    children = [parity[full] ^ parity[1 << c] for c in range(k)]
    children += [values[full & ~s] ^ parity[full] ^ parity[full & ~s] ^ 1 for s in signatures]
    return values[full], tuple(children)


def named_vertex_recurrence(k, signatures):
    """Adjacency-bitset closed-neighborhood deletion, no signature DP."""
    n = k + len(signatures)
    adj = [0] * n
    for c in range(k):
        adj[c] = ((1 << k) - 1) ^ (1 << c)
    for j, s in enumerate(signatures):
        v = k + j
        adj[v] = s
        for c in range(k):
            if s & (1 << c):
                adj[c] |= 1 << v

    @lru_cache(maxsize=None)
    def grundy(remaining):
        if not remaining:
            return 0
        options = set()
        bits = remaining
        while bits:
            bit = bits & -bits
            bits -= bit
            v = bit.bit_length() - 1
            options.add(grundy(remaining & ~(bit | adj[v])))
        return mex(options)

    full = (1 << n) - 1
    children = tuple(grundy(full & ~((1 << v) | adj[v])) for v in range(n))
    deletion_values = tuple(grundy(full & ~(1 << v)) for v in range(n))
    return grundy(full), children, deletion_values, grundy.cache_info().currsize


def main():
    a, ac = signature_recurrence(K, SIGNATURES)
    b, bc, deletion, states = named_vertex_recurrence(K, SIGNATURES)
    assert a == b == 8
    assert ac == bc == EXPECTED_CHILDREN
    assert set(ac) == set(range(8))
    assert all(g < 8 for g in deletion), deletion
    assert max(s.bit_count() for s in SIGNATURES) == 3
    assert len(SIGNATURES) == 15
    assert len(set(SIGNATURES)) == 10
    print('centers=7 independent=15 vertices=22 edges=', 21 + sum(s.bit_count() for s in SIGNATURES))
    print('grundy=8 children=', list(ac))
    print('single_vertex_deletions=', list(deletion))
    print('named_memo_states=', states)
    iso, _, _, iso_states = named_vertex_recurrence(K, SIGNATURES + (0,))
    assert iso == 9
    print('with_one_isolated_vertex=9 named_memo_states=', iso_states)
    print('all checks passed')


if __name__ == '__main__':
    main()
