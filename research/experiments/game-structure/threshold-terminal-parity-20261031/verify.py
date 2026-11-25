#!/usr/bin/env python3
"""Independent exhaustive check of threshold terminal-parity theorem.

Canonical words start with I. No prediction formula is used in reference recursion.
"""
from collections import Counter
from functools import lru_cache
from math import factorial


def reference(word):
    n = len(word)
    adj = [0] * n
    for j, kind in enumerate(word):
        if kind == "D":
            for i in range(j):
                adj[i] |= 1 << j
                adj[j] |= 1 << i
    closed = [adj[i] | (1 << i) for i in range(n)]
    full = (1 << n) - 1

    @lru_cache(None)
    def solve(available):
        if not available:
            return 0, 1, ((0, 1),)
        normal, misere, counts = set(), set(), Counter()
        rem = available
        while rem:
            bit = rem & -rem
            rem -= bit
            i = bit.bit_length() - 1
            g, h, child_counts = solve(available & ~closed[i])
            normal.add(g)
            misere.add(h)
            for length, number in child_counts:
                counts[length + 1] += number

        def mex(values):
            v = 0
            while v in values:
                v += 1
            return v

        return mex(normal), mex(misere), tuple(sorted(counts.items()))

    maximal = []
    for mask in range(1 << n):
        covered = 0
        ok = True
        for i in range(n):
            if mask >> i & 1:
                if mask & adj[i]:
                    ok = False
                    break
                covered |= closed[i]
        if ok and covered == full:
            maximal.append(mask)
    return solve(full), maximal


def prediction(word):
    n_i = word.count("I")
    prior_i = 0
    d_lengths = []
    first_break = None
    for j, kind in enumerate(word):
        if kind == "I":
            prior_i += 1
        else:
            d_lengths.append(1 + n_i - prior_i)
            if first_break is None and prior_i % 2 == 0:
                first_break = j
    lengths = [n_i] + d_lengths
    counts = Counter()
    counts[n_i] += factorial(n_i)
    for length in d_lengths:
        counts[length] += factorial(length)
    if first_break is None:
        g = n_i % 2
    else:
        suffix_i = word[first_break + 1:].count("I")
        g = 2 + suffix_i % 2
    h = 1 - g if g < 2 else g
    return g, h, counts, lengths, first_break


def run(max_n=11):
    tested = 0
    mixed = 0
    for n in range(max_n + 1):
        for suffix in range(1 << max(0, n - 1)):
            word = "" if n == 0 else "I" + "".join(
                "D" if suffix >> i & 1 else "I" for i in range(n - 1)
            )
            (g, h, histories), maximal = reference(word)
            pg, ph, expected, lengths, first_break = prediction(word)
            hist = Counter(dict(histories))
            actual_lengths = Counter(mask.bit_count() for mask in maximal)
            assert (g, h) == (pg, ph), (word, (g, h), (pg, ph))
            assert hist == expected, (word, hist, expected)
            assert actual_lengths == Counter(lengths), (word, actual_lengths, lengths)
            actual_mixed = len({v % 2 for v in actual_lengths}) == 2
            assert actual_mixed == (first_break is not None), word
            assert actual_mixed == (g >= 2), word
            tested += 1
            mixed += actual_mixed
    print(
        f"PASS canonical words n=0..{max_n}: {tested}; "
        f"mixed terminal parities: {mixed}; mismatches: 0"
    )


if __name__ == "__main__":
    run()
