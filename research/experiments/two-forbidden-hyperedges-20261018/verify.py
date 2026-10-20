#!/usr/bin/env python3
"""Independently audit closed Grundy formula for any two forbidden subsets."""
from itertools import combinations
from collections import Counter
import random, json

def closed(mask, E, F, n):
    I = E & F
    A = E & ~F
    B = F & ~E
    free = ((1 << n)-1) & ~(E|F)
    c = (I & ~mask).bit_count()
    u = (A & ~mask).bit_count()
    v = (B & ~mask).bit_count()
    z = (free & ~mask).bit_count()
    if c == 0:
        assert u and v
        h = (u + v) % 2
    elif min(u, v) < c:
        h = (c - 1 + u + v) % 2
    elif min(u, v) == c:
        h = 2 + (max(u, v) - c) % 2
    else:
        h = (c + u + v) % 2
    return h ^ (z & 1)

def audit(n, E, F):
    lim = 1 << n
    g = [0] * lim
    ok = [not ((s & E) == E or (s & F) == F) for s in range(lim)]
    count = 0
    for s in range(lim - 1, -1, -1):
        if not ok[s]:
            continue
        child = {g[s | (1 << i)] for i in range(n)
                 if not (s >> i) & 1 and ok[s | (1 << i)]}
        x = 0
        while x in child: x += 1
        g[s] = x
        predicted = closed(s, E, F, n)
        assert x == predicted, (n, E, F, s, x, predicted)
        count += 1
    return count

def main():
    pairs = states = 0
    hist = Counter()
    for n in range(1, 8):
        for E in range(1, 1 << n):
            for F in range(E, 1 << n):
                if not F: continue
                states += audit(n, E, F)
                pairs += 1
                hist[n] += 1
    rng = random.Random(20261018)
    random_pairs = 3000
    for _ in range(random_pairs):
        n = rng.randint(8, 12)
        E = rng.randrange(1, 1 << n)
        F = rng.randrange(1, 1 << n)
        states += audit(n, E, F)
        pairs += 1
    print(json.dumps({'exhaustive_n':7, 'exhaustive_pairs_by_n':dict(hist),
                      'random_pairs_n8_to_12':random_pairs,
                      'audited_pairs':pairs,'audited_safe_states':states},indent=2))

if __name__ == '__main__': main()
