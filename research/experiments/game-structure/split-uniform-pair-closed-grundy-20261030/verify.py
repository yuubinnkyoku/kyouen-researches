#!/usr/bin/env python3
"""Independent named-vertex Node Kayles vs symmetric recurrence and closed forms."""
from functools import lru_cache

def mex(values):
    v = set(values)
    return next(i for i in range(len(v) + 1) if i not in v)

@lru_cache(None)
def recurrence(k, t, c):
    if k == 0:
        return 0
    options = [(c * ((k - 1) * (k - 2) // 2 + (k - 1) * t)) % 2]
    if t:
        options.append(recurrence(k - 1, t + 1, c) ^ ((c * t - 1) & 1))
    if k >= 2:
        options.append(recurrence(k - 2, t + 2, c) ^ ((c - 1) & 1))
    return mex(options)

def closed(k, t, c):
    if k == 0:
        return 0
    if c % 2 == 0:
        if k == 1:
            return 2 if t else 1
        if k == 2:
            return 2
        return 1
    if t == 0:
        return int(k % 4 in (1, 2))
    if t % 2 == 0:
        if k == 1:
            return 2
        if k == 2:
            return 1
        return int(k % 4 in (1, 2))
    if k == 2:
        return 3
    return int(k % 4 in (0, 1))

def named(k, t, c):
    neigh = [0] * k
    for i in range(k):
        neigh[i] = ((1 << k) - 1) ^ (1 << i)
    def add(ends):
        nonlocal neigh
        idx = len(neigh)
        for j in ends:
            neigh[j] |= 1 << idx
        neigh.append(sum(1 << j for j in ends))
    for i in range(k):
        for j in range(i + 1, k):
            for _ in range(c):
                add((i, j))
    for i in range(k):
        for _ in range(t * c):
            add((i,))
    n = len(neigh)
    close = [v | (1 << i) for i, v in enumerate(neigh)]
    @lru_cache(None)
    def g(mask):
        moves = []
        x = mask
        while x:
            low = x & -x
            i = low.bit_length() - 1
            x ^= low
            moves.append(g(mask & ~close[i]))
        return mex(moves)
    answer = g((1 << n) - 1)
    return answer, g.cache_info().currsize

def main():
    count = 0
    for c in range(1, 9):
        for k in range(0, 160):
            for t in range(0, 12):
                a = recurrence(k, t, c)
                b = closed(k, t, c)
                assert a == b, (k, t, c, a, b)
                count += 1
    print('symmetric_recurrence_vs_closed', count, 'all matched')
    total = 0
    states = 0
    max_n = 0
    for c in range(1, 5):
        for k in range(0, 8):
            for t in range(0, 6):
                n = k + c * (k * (k - 1) // 2 + k * t)
                if n > 22:
                    continue
                got, s = named(k, t, c)
                want = closed(k, t, c)
                assert got == want, (k, t, c, got, want)
                total += 1
                states += s
                max_n = max(max_n, n)
    print('named_vertex_independent', total, 'all matched', 'total_memo_states', states, 'max_vertices', max_n)
    print('uniform_pair_roots_odd', [closed(k, 0, 1) for k in range(1, 17)])
    print('uniform_pair_roots_even', [closed(k, 0, 2) for k in range(1, 17)])

if __name__ == '__main__':
    main()
