"""Independent exact optimality check for a weighted perfect matching.

Every other perfect matching differs by disjoint alternating cycles. If a
cheaper matching existed, at least one such cycle would have negative cost.
The subset DP checks all simple alternating cycles of the supplied matching,
without invoking a matching optimizer or using floating point arithmetic.
"""
from __future__ import annotations


def verify_optimality(costs, pairs):
    """Return (matching cost, minimum alternate-cycle delta, DP states).

    costs maps sorted (u,v) edges to nonnegative integer weights.
    pairs is a complete perfect matching on vertices 0..2n-1.
    Raises ValueError on invalid input or an improving alternating cycle.
    """
    pairs = [tuple(sorted(p)) for p in pairs]
    n = len(pairs)
    vertices = [u for p in pairs for u in p]
    if n < 1 or len(set(vertices)) != 2*n or set(vertices) != set(range(2*n)):
        raise ValueError('not a perfect matching on vertices 0..2n-1')
    if any(not isinstance(w, int) or w < 0 for w in costs.values()):
        raise ValueError('edge weights must be nonnegative integers')
    if any(tuple(p) not in costs for p in pairs):
        raise ValueError('matched edge missing')
    matched_weights = [costs[p] for p in pairs]
    total = sum(matched_weights)
    best_delta = None
    states = 0
    # The smallest indexed matched pair uniquely anchors each cycle.
    for start in range(n):
        start_bit = 1 << start
        for start_out in (0, 1):
            # State = (visited matched-pair mask, last pair, outgoing endpoint).
            # Its score subtracts each traversed matched edge exactly once.
            dp = {start_bit: {(start, start_out): -matched_weights[start]}}
            for mask in range(start_bit, 1 << n):
                if mask not in dp:
                    continue
                states += len(dp[mask])
                for (last, last_out), score in dp[mask].items():
                    u = pairs[last][last_out]
                    if mask != start_bit:
                        v = pairs[start][1 - start_out]
                        edge = costs.get((min(u, v), max(u, v)))
                        if edge is not None:
                            delta = score + edge
                            if best_delta is None or delta < best_delta:
                                best_delta = delta
                            if delta < 0:
                                raise ValueError(
                                    f'negative alternating cycle: delta={delta}')
                    for nxt in range(start + 1, n):
                        bit = 1 << nxt
                        if mask & bit:
                            continue
                        for entering in (0, 1):
                            v = pairs[nxt][entering]
                            edge = costs.get((min(u, v), max(u, v)))
                            if edge is None:
                                continue
                            key = (nxt, 1 - entering)
                            new_score = score + edge - matched_weights[nxt]
                            target = dp.setdefault(mask | bit, {})
                            if key not in target or new_score < target[key]:
                                target[key] = new_score
    return total, best_delta, states


def self_test():
    costs = {(0, 1): 2, (2, 3): 2, (0, 2): 3, (1, 3): 3,
             (0, 3): 4, (1, 2): 4}
    total, delta, states = verify_optimality(costs, [(0, 1), (2, 3)])
    assert (total, delta) == (4, 2) and states > 0
    bad = dict(costs)
    bad[(0, 2)] = bad[(1, 3)] = 1
    try:
        verify_optimality(bad, [(0, 1), (2, 3)])
    except ValueError as e:
        assert 'negative alternating cycle' in str(e)
    else:
        raise AssertionError('cheaper matching was accepted')
    assert verify_optimality(
        {(0, 1): 7, (2, 3): 8}, [(0, 1), (2, 3)])[1] is None


if __name__ == '__main__':
    self_test()
    print('PASS alternating-cycle exact-optimality self-test')
