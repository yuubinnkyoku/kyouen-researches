#!/usr/bin/env python3
"""Exhaustive named-vertex audit of the split-graph parity criterion."""
def verify(k, m, cross_mask):
    n = k + m
    adj = [0] * n
    for i in range(k):
        for j in range(i + 1, k):
            adj[i] |= 1 << j
            adj[j] |= 1 << i
    for i in range(k):
        for j in range(m):
            if cross_mask >> (i * m + j) & 1:
                adj[i] |= 1 << (k + j)
                adj[k + j] |= 1 << i
    degrees = [(adj[i] >> k).bit_count() for i in range(k)]
    if k == 0:
        predicted, epsilon = True, m & 1
    elif all(d & 1 for d in degrees):
        predicted, epsilon = True, m & 1
    elif all(d % 2 == 0 for d in degrees) and 0 in degrees:
        predicted, epsilon = True, (m + 1) & 1
    else:
        predicted, epsilon = False, None

    safe = [False] * (1 << n)
    safe[0] = True
    for mask in range(1, 1 << n):
        bit = mask & -mask
        v = bit.bit_length() - 1
        rest = mask ^ bit
        safe[mask] = safe[rest] and not (adj[v] & rest)
    grundy = [None] * (1 << n)
    terminal_parities = set()
    for mask in range((1 << n) - 1, -1, -1):
        if not safe[mask]:
            continue
        options = set()
        for v in range(n):
            bit = 1 << v
            if not mask & bit and not (adj[v] & mask):
                options.add(grundy[mask | bit])
        if not options:
            terminal_parities.add(mask.bit_count() & 1)
        g = 0
        while g in options:
            g += 1
        grundy[mask] = g
    locked = len(terminal_parities) == 1
    binary = all(g <= 1 for g in grundy if g is not None)
    if locked != predicted or binary != predicted:
        raise AssertionError((k, m, cross_mask, degrees, predicted, terminal_parities))
    if predicted:
        assert terminal_parities == {epsilon}
        for mask, g in enumerate(grundy):
            if g is not None and g != (epsilon ^ (mask.bit_count() & 1)):
                raise AssertionError((k, m, cross_mask, mask, g, epsilon))
    return predicted, grundy[0]

def main():
    cases = locked = max_root = 0
    sizes = [(k, m) for k in range(5) for m in range(5)] + [(3, 5), (5, 3)]
    for k, m in sizes:
        for mask in range(1 << (k * m)):
            is_locked, root = verify(k, m, mask)
            cases += 1
            locked += is_locked
            max_root = max(max_root, root)
    assert (cases, locked) == (140499, 13815)
    print(f"PASS labelled_split_graphs={cases} parity_locked={locked} "
          f"not_locked={cases-locked} max_root_grundy={max_root}")

if __name__ == "__main__":
    main()
