#!/usr/bin/env python3
"""Exact q=5 cube-section 3-adic root lifting and finite-interval maxima.

Mathematical infinite-period/lifting theorem: K0567, theorem 11.
No full-dimensional hyperplane sections are enumerated here.
"""

# 120*(E_{d,5}/2**d) = sum coeff*base**d, d>=5 (K0561).
COEFF = {
    16: 1, 12: -30, 10: 140, 9: 135, 8: -1215, 7: 2205,
    6: -1977, 5: 780, 4: 250, 3: -495, 2: 255, 1: -49,
}


def normalized_via_composite_modulus(d: int, t: int) -> int:
    """Compute E_{d,5}/2^d modulo 3^t via exact division by 120."""
    assert d >= 5 and t >= 1
    modulus = 3**t
    numerator = sum(c * pow(a, d, 120 * modulus) for a, c in COEFF.items())
    numerator %= 120 * modulus
    assert numerator % 120 == 0
    return numerator // 120


def normalized_via_three_adic_inverse(d: int, t: int) -> int:
    """Independent modular route: divide numerator by 3, invert 40."""
    assert d >= 5 and t >= 1
    modulus = 3**t
    numerator = sum(c * pow(a, d, 3 * modulus) for a, c in COEFF.items())
    numerator %= 3 * modulus
    assert numerator % 3 == 0
    return (numerator // 3 * pow(40, -1, modulus)) % modulus


def direct_exact_small(d: int) -> int:
    assert d >= 5
    numerator = sum(c * a**d for a, c in COEFF.items())
    assert numerator % 120 == 0
    return numerator // 120


def root_classes(max_t: int = 42):
    """Four roots modulo P_t=2*3^(t-1), t=2,...,max_t.

    Every lifting test is performed at d>=D_(t+1), as the period is
    only eventual. Each residue has one valid child by K0567.
    """
    roots = (2, 3, 4, 5)
    table = {}
    for t in range(2, max_t + 1):
        period = 2 * 3**(t - 1)
        assert len(roots) == 4 and len(set(roots)) == 4
        assert all(0 <= r < period for r in roots)
        for r in roots:
            d = r if r >= max(5, t + 2) else r + period
            assert normalized_via_composite_modulus(d, t) == 0
            assert normalized_via_three_adic_inverse(d, t) == 0
        table[t] = (period, roots)
        if t == max_t:
            break
        new_period = 3 * period
        children = []
        for r in roots:
            accepted = []
            for j in range(3):
                candidate = r + j * period
                # Check above the onset of the eventual period.
                test = candidate if candidate >= max(5, t + 3) else candidate + new_period
                first = normalized_via_composite_modulus(test, t + 1)
                second = normalized_via_three_adic_inverse(test, t + 1)
                assert first == second, (t, candidate, first, second)
                if first == 0:
                    accepted.append(candidate)
            assert len(accepted) == 1, (t, r, accepted)
            children.extend(accepted)
        roots = tuple(sorted(children))
    return table


def hits_up_to(bound: int, period: int, roots: tuple[int, ...]) -> tuple[int, list[int]]:
    """Count solutions d>=5 in [5,bound] without scanning dimensions."""
    total, examples = 0, []
    for r in roots:
        first = r if r >= 5 else r + period
        if first > bound:
            continue
        count = 1 + (bound - first) // period
        total += count
        if count <= 4:
            examples.extend(first + i * period for i in range(count))
    return total, sorted(examples)


def verify():
    table = root_classes(42)
    expected = {
        2: (2, 3, 4, 5),
        3: (2, 3, 4, 5),
        4: (2, 4, 5, 39),
        5: (4, 93, 110, 113),
        6: (113, 328, 417, 434),
        38: (598841409424707995, 607800646991213230,
             800015958976071945, 863338084376830994),
        39: (800015958976071945, 863338084376830994,
             2399977032988697447, 2408936270555202682),
        40: (863338084376830994, 2399977032988697447,
             5110639705901186860, 6203422829668040301),
        41: (863338084376830994, 2399977032988697447,
             14308533135705992835, 21320860317977091928),
        42: (2399977032988697447, 14308533135705992835,
             45636191236090949530, 49493999920604546198),
    }
    for t, roots in expected.items():
        assert table[t][1] == roots, t

    # Small dimensions not covered by D_t are checked as exact integers.
    for d in range(5, 45):
        exact = direct_exact_small(d)
        assert exact % (3**42) == normalized_via_composite_modulus(d, 42)
        assert exact % (3**42) != 0
    for d in range(5, 100):
        for t in (2, 4, 7, 12):
            assert normalized_via_composite_modulus(d, t) == (
                normalized_via_three_adic_inverse(d, t))

    for bound, target_t, next_t, expected_hits in [
        (10**5, 13, 14, [55246, 79149]),
        (10**6, 14, 15, [920111]),
        (10**12, 26, 27, [134093761688, 970208334687]),
        (10**18, 41, 42, [863338084376830994]),
    ]:
        count, hits = hits_up_to(bound, *table[target_t])
        next_count, _ = hits_up_to(bound, *table[next_t])
        assert count == len(expected_hits) and hits == expected_hits
        assert next_count == 0
        for d in range(5, max(5, next_t + 2)):
            assert direct_exact_small(d) % (3**next_t) != 0
        for d in hits:
            assert normalized_via_composite_modulus(d, target_t) == 0
            assert normalized_via_three_adic_inverse(d, next_t) != 0
        print(f"5<=d<={bound}: max v3(E_{{d,5}})={target_t}, attained at {hits}")
    print("All four root branches checked through t=42 by two modular routes.")


if __name__ == "__main__":
    verify()
