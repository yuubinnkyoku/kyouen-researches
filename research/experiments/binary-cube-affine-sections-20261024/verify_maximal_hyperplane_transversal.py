"""Exhaustive transversal audit for all maximal hypercube hyperplanes.

A flat is represented by the bit mask of its vertices.  For d<=7,
all (t-1)-point candidate transversals are checked, where t=1+bit_length(d).
"""
from itertools import combinations


def flats(d):
    n = 1 << d
    out = []
    for i in range(d):
        for b in (0, 1):
            out.append(sum(1 << x for x in range(n) if ((x >> i) & 1) == b))
    for i, j in combinations(range(d), 2):
        for b in (0, 1):
            out.append(sum(1 << x for x in range(n)
                           if (((x >> i) ^ (x >> j)) & 1) == b))
    assert len(set(out)) == d * (d + 1)
    assert all(m.bit_count() == n // 2 for m in out)
    return out


def witness(d):
    t = 1 + d.bit_length()
    return [0] + [sum(1 << j for j in range(d) if (j + 1) >> b & 1)
                  for b in range(t - 1)]


def check(d, exhaustive):
    family = flats(d)
    t = 1 + d.bit_length()
    chosen = witness(d)
    assert len(chosen) == len(set(chosen)) == t
    mask = sum(1 << x for x in chosen)
    assert all(mask & f for f in family)
    count = 0
    if exhaustive:
        # A smaller hitting set could be enlarged to t-1 points.
        for subset in combinations(range(1 << d), t - 1):
            candidate = sum(1 << x for x in subset)
            assert any((candidate & f) == 0 for f in family), (d, subset)
            count += 1
    print(f"d={d} flats={len(family)} t={t} K={2**d-t} "
          f"excluded_smaller={count} witness={chosen}")


if __name__ == "__main__":
    for dimension in range(1, 13):
        check(dimension, dimension <= 7)


# The following checks are independent of the affine-rank C++ verifier.
from collections import Counter
from itertools import permutations
from math import factorial


def audit_minimal_transversals(d):
    """Exhaust all minimal hitting sets of sizes 2..d+2 (d<=5)."""
    family = flats(d)
    n = 1 << d
    counts = Counter()
    extremal = set()
    for t in range(2, d + 3):
        for vertices in combinations(range(n), t):
            candidate = sum(1 << x for x in vertices)
            private = 0
            for plane in family:
                intersection = candidate & plane
                if not intersection:
                    break
                if intersection & (intersection - 1) == 0:
                    private |= intersection
            else:
                if private == candidate:
                    counts[t] += 1
                    if t == d + 1:
                        extremal.add(candidate)

    paths = set()
    for start in range(n):
        for order in permutations(range(d)):
            vertex = start
            mask = 1 << vertex
            for axis in order:
                vertex ^= 1 << axis
                mask |= 1 << vertex
            paths.add(mask)
    expected = (1 << (d - 1)) * factorial(d)
    assert len(paths) == expected
    assert extremal == paths, (d, len(extremal), len(paths))
    assert counts[d + 1] == expected
    assert counts[d + 2] == 0
    known = {
        1: {2: 1},
        2: {3: 4},
        3: {3: 8, 4: 24},
        4: {4: 560, 5: 192},
        5: {4: 3360, 5: 26496, 6: 1920},
    }
    assert dict(counts) == known[d], (d, counts)
    print(f"minimal d={d} distribution={dict(sorted(counts.items()))} "
          f"geodesic_sets={len(paths)} PASS")


def audit_strong_game(d):
    """Independent backward mex on all safe subsets for d=3,4."""
    n = 1 << d
    total = 1 << n
    family = flats(d)
    safe = bytearray(total)
    for mask in range(total):
        safe[mask] = all(mask & f != f for f in family)
    g = bytearray(total)
    h = bytearray(total)
    terminal = Counter()
    pairs = Counter()
    failure = 0
    full = total - 1
    for mask in range(total - 1, -1, -1):
        if not safe[mask]:
            continue
        options = []
        free = full ^ mask
        while free:
            bit = free & -free
            free -= bit
            child = mask | bit
            if safe[child]:
                options.append(child)
        if options:
            seen_g = {g[x] for x in options}
            seen_h = {h[x] for x in options}
            while g[mask] in seen_g:
                g[mask] += 1
            while h[mask] in seen_h:
                h[mask] += 1
        else:
            h[mask] = 1
            terminal[mask.bit_count()] += 1
        pair = (g[mask], h[mask])
        pairs[pair] += 1
        failure += (h[mask] != (1 - g[mask] if g[mask] <= 1 else g[mask]))
    expected = {
        3: (159, {4: 24, 5: 8}, (0, 0), 25,
            {(0, 0): 17, (0, 1): 40, (1, 0): 46,
             (2, 1): 8, (2, 2): 48}),
        4: (61719, {11: 192, 12: 560}, (0, 1), 0,
            {(0, 1): 29367, (1, 0): 30720, (2, 2): 1632}),
    }[d]
    actual = (sum(safe), dict(terminal), (g[0], h[0]), failure, dict(pairs))
    assert actual == expected, (d, actual, expected)
    print(f"strong d={d} q={n//2} safe={sum(safe)} "
          f"terminal={dict(sorted(terminal.items()))} "
          f"root={(g[0], h[0])} swap_fail={failure} pairs={dict(sorted(pairs.items()))} PASS")


if __name__ == "__main__":
    for dimension in range(1, 6):
        audit_minimal_transversals(dimension)
    for dimension in (3, 4):
        audit_strong_game(dimension)

# All-dimensional terminal spectrum and maximum-terminal count (Theorem 8).
def maximum_terminal_count(d):
    """Count minimum-cardinality transversals via injective normalized columns."""
    t = 1 + d.bit_length()
    possibilities = (1 << (t - 1)) - 1
    numerator = 1 << d
    for j in range(d):
        numerator *= possibilities - j
    assert numerator % factorial(t) == 0
    return numerator // factorial(t)


def spectrum_witness(d, t):
    """Construct a minimal transversal of exactly t distinct cube vertices."""
    assert 1 + d.bit_length() <= t <= d + 1
    limit = (1 << (t - 1)) - 1
    # First t-1 columns form the chain 00...0, 10...0, 110...0, ...
    columns = [limit ^ ((1 << j) - 1) for j in range(t - 1)]
    columns += [v for v in range(1, limit + 1) if v not in columns][:d - t + 1]
    assert len(columns) == len(set(columns)) == d
    rows = [0] * t
    for j, col in enumerate(columns):
        for i in range(1, t):
            if col & (1 << (i - 1)):
                rows[i] |= 1 << j
    assert len(set(rows)) == t
    return rows


def audit_terminal_spectrum(d):
    family = flats(d)
    t0 = 1 + d.bit_length()
    for t in range(t0, d + 2):
        rows = spectrum_witness(d, t)
        mask = sum(1 << x for x in rows)
        assert all(mask & f for f in family)
        for x in rows:
            assert any((mask & f) == (1 << x) for f in family)
    known = {1: 1, 2: 4, 3: 8, 4: 560, 5: 3360}
    if d in known:
        assert maximum_terminal_count(d) == known[d]
    print(f"spectrum d={d} terminal_sizes={list(range((1<<d)-d-1, (1<<d)-t0+1))} "
          f"max_terminal_count={maximum_terminal_count(d)} PASS")


if __name__ == "__main__":
    for dimension in range(1, 13):
        audit_terminal_spectrum(dimension)


# Theorem 11: exact counts for intermediate terminal sizes.
# This section uses normalized columns, not geometric face masks.
def intermediate_column_count(d, t):
    """Count minimal transversals via t colored difference directions."""
    assert d >= 3 and 1 + d.bit_length() <= t <= d + 1
    size = 1 << (t - 1)
    directions = {1 << j: 1 << j for j in range(t - 1)}
    directions[size - 1] = 1 << (t - 1)
    all_colors = (1 << t) - 1
    count = 0
    for chosen in combinations(range(1, size), d):
        words = (0,) + chosen
        covered = 0
        for i, x in enumerate(words):
            for y in words[i + 1:]:
                covered |= directions.get(x ^ y, 0)
        count += (covered == all_colors)
    numerator = (1 << d) * factorial(d) * count
    assert numerator % factorial(t) == 0
    return count, numerator // factorial(t)


def _independence_polynomial(j, folded=False):
    """Independence polynomial of Q_j or folded Q_j; j<=4 here."""
    n = 1 << j
    assert n <= 16
    dirs = [1 << k for k in range(j)]
    if folded:
        dirs.append(n - 1)
    neighbors = [sum(1 << (x ^ v) for v in dirs) for x in range(n)]
    coefficients = [0] * (n + 1)
    for mask in range(1 << n):
        remaining = mask
        while remaining:
            bit = remaining & -remaining
            remaining -= bit
            if mask & neighbors[bit.bit_length() - 1]:
                break
        else:
            coefficients[mask.bit_count()] += 1
    return coefficients


def _poly_multiply(a, b, limit=16):
    out = [0] * min(len(a) + len(b) - 1, limit + 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b[:len(out) - i]):
            out[i + j] += x * y
    return out


def _poly_power(a, k):
    out = [1]
    for _ in range(k):
        out = _poly_multiply(out, a)
    return out


def _rooted_independent(a, vertices):
    # By vertex transitivity, k*I[k]/vertices is an integer.
    assert all(k * a[k] % vertices == 0 for k in range(1, len(a)))
    return [0] + [k * a[k] // vertices for k in range(1, len(a))]


def t5_inclusion_exclusion():
    """Independently compute the full 16-vertex coefficient polynomial."""
    from math import comb
    t, n = 5, 16
    coefficients = [0] * 17
    for j in range(t):
        p = _independence_polynomial(j)
        term = _poly_multiply(
            _rooted_independent(p, 1 << j),
            _poly_power(p, (n >> j) - 1))
        for k, value in enumerate(term):
            coefficients[k] += (-1) ** j * comb(t, j) * value
    folded = _independence_polynomial(t - 1, folded=True)
    term = _rooted_independent(folded, n)
    for k, value in enumerate(term):
        coefficients[k] += (-1) ** t * value
    return coefficients


def audit_intermediate_columns():
    expected = {
        (5, 4): (21, 3360),
        (5, 5): (828, 26496),
        (5, 6): (360, 1920),
        (6, 4): (7, 13440),
        (6, 5): (3220, 1236480),
        (6, 6): (16387, 1048768),
        (7, 4): (1, 26880),
        (7, 5): (5860, 31503360),
        (7, 6): (249880, 223892480),
    }
    for (d, t), answer in expected.items():
        result = intermediate_column_count(d, t)
        assert result == answer, (d, t, result, answer)
        print(f"columns d={d} t={t} b={result[0]} terminal={result[1]} PASS")
    expected_t5 = [0] * 5 + [
        60, 828, 3220, 5860, 6435, 5005, 3003, 1365,
        455, 105, 15, 1]
    assert t5_inclusion_exclusion() == expected_t5
    print("t=5 inclusion-exclusion independent-set polynomial PASS")


if __name__ == "__main__" and "--intermediate" in __import__("sys").argv:
    audit_intermediate_columns()
