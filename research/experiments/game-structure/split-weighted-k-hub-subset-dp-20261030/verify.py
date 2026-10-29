"""Exact independent checks for the weighted k-hub no-center formula."""
from fractions import Fraction
from functools import lru_cache
from itertools import permutations, product


def predicted(t, neighborhoods):
    m, k = len(t), len(neighborhoods)
    w = [x + 1 for x in t]
    # Each independent vertex contributes to all subsets meeting its hub mask.
    by_mask = [0] * (1 << k)
    for j in range(m):
        mask = sum(1 << h for h, a in enumerate(neighborhoods) if j in a)
        by_mask[mask] += w[j]
    zeta = by_mask[:]
    for h in range(k):
        for mask in range(1 << k):
            if mask & (1 << h):
                zeta[mask] += zeta[mask ^ (1 << h)]
    all_mask = (1 << k) - 1
    total_weight = sum(w)
    H = [Fraction(0)] * (1 << k)
    H[0] = Fraction(1)
    for mask in range(1, 1 << k):
        union_weight = total_weight - zeta[all_mask ^ mask]
        numerator = sum((H[mask ^ (1 << h)] for h in range(k)
                         if mask & (1 << h)), Fraction(0))
        H[mask] = numerator / (mask.bit_count() + union_weight)
    answer = sum(((-1 if mask.bit_count() & 1 else 1) * H[mask]
                  for mask in range(1 << k)), Fraction(0))
    for count in t:
        answer /= count + 1
    return answer


def graph(t, neighborhoods):
    m = len(t)
    adj = [0] * (m + sum(t) + len(neighborhoods))
    centers = []
    for j, count in enumerate(t):
        for _ in range(count):
            v = m + len(centers)
            centers.append(v)
            adj[j] |= 1 << v
            adj[v] |= 1 << j
    for a in neighborhoods:
        v = m + len(centers)
        centers.append(v)
        for j in a:
            adj[j] |= 1 << v
            adj[v] |= 1 << j
    for v in centers:
        for u in centers:
            if u != v:
                adj[v] |= 1 << u
    return adj, m


def closed_neighborhood_dp(adj, m):
    n = len(adj)
    @lru_cache(None)
    def probability(mask):
        if mask == 0:
            return Fraction(1)
        ans = Fraction(0)
        for v in range(n):
            if mask & (1 << v) and v < m:
                ans += probability(mask & ~(adj[v] | (1 << v)))
        return ans / mask.bit_count()
    return probability((1 << n) - 1)


def permutation_count(adj, m):
    n = len(adj)
    success = total = 0
    for order in permutations(range(n)):
        remaining = (1 << n) - 1
        valid = True
        for v in order:
            if remaining & (1 << v):
                if v >= m:
                    valid = False
                    break
                remaining &= ~(adj[v] | (1 << v))
        success += valid
        total += 1
    # For failed orders we deliberately stop scanning but still count the order.
    return Fraction(success, total)


def run():
    cases = independent = 0
    for m in range(1, 5):
        choices = [frozenset(j for j in range(m) if mask & (1 << j))
                   for mask in range(1, 1 << m)]
        for k in range(4):
            for t in product(range(3), repeat=m):
                if m + k + sum(t) > 11:
                    continue
                for neighborhoods in product(choices, repeat=k):
                    expected = predicted(t, neighborhoods)
                    adj, n_independent = graph(t, neighborhoods)
                    actual = closed_neighborhood_dp(adj, n_independent)
                    assert expected == actual, (m, k, t, neighborhoods, expected, actual)
                    cases += 1
                    if independent < 200 and len(adj) <= 7 and k >= 1:
                        # This independently checks the random-priority coupling.
                        perm = permutation_count(adj, n_independent)
                        assert expected == perm, (t, neighborhoods, expected, perm)
                        independent += 1
    assert predicted((1, 2, 0), ({0, 1}, {1, 2}, {0, 2})) == Fraction(281, 3240)
    assert predicted((0, 0), (frozenset(),)) == 0
    print(f"exact labeled configurations: {cases}")
    print(f"independent full-priority enumerations: {independent}")
    print("three hubs, t=(1,2,0): 281/3240; mismatches: 0")


if __name__ == "__main__":
    run()
