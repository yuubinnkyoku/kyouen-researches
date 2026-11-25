#!/usr/bin/env python3
"""Independent exhaustive checks for the three-forbidden-set gap theorem."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations


def terminal_counts(n, edges):
    forbidden = tuple(sum(1 << j for j in edge) if not isinstance(edge, int) else edge for edge in edges)
    safe = {s for s in range(1 << n) if all(s & e != e for e in forbidden)}
    maximal = [s for s in safe if all((s | (1 << i)) not in safe for i in range(n) if not s & (1 << i))]
    return Counter(s.bit_count() for s in maximal), safe


def predicted_gap(edges):
    a, b, c = edges
    common = a & b & c
    private = ((a & ~b & ~c), (b & ~a & ~c), (c & ~a & ~b))
    return bool(common and all(private) and (a & b) == common and (a & c) == common and (b & c) == common)


def det3(m):
    a, b, c = m
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def on_carrier(points):
    x0, y0 = points[0]
    q0 = x0*x0 + y0*y0
    m = []
    for x, y in points[1:]:
        m.append((x*x+y*y-q0, x-x0, y-y0))
    return det3(m) == 0


def rational_circle(beta, t):
    t = Fraction(t)
    x = (2 - beta*t) / (1 + t*t)
    return x, t*x


def construct(q):
    betas = (10, 6, -4)
    core = [(Fraction(0), Fraction(0)), (Fraction(2), Fraction(0))]
    points = core[:]
    colors = [-1, -1]
    for i, beta in enumerate(betas):
        for _ in range(q-2):
            for t in range(1, 5000):
                point = rational_circle(beta, Fraction(t, t+1))
                if point in points:
                    continue
                if all(not on_carrier([points[j] for j in triple] + [point])
                       or all(colors[j] in (-1, i) for j in triple)
                       for triple in combinations(range(len(points)), 3)):
                    points.append(point)
                    colors.append(i)
                    break
            else:
                raise AssertionError(f"could not construct q={q}, carrier={i}")
    # Exact determinant of EVERY four-point set; no unintended carrier.
    zero = [set(t) for t in combinations(range(len(points)), 4)
            if on_carrier([points[j] for j in t])]
    intended = [set((0,1)) | {j for j, color in enumerate(colors) if color == i}
                for i in range(3)]
    assert all(any(t <= carrier for carrier in intended) for t in zero)
    assert len(zero) == 3 * (q*(q-1)*(q-2)*(q-3)//24)
    return points, colors, zero


def verify():
    cases = 0
    for n in range(1, 7):
        nonempty = range(1, 1 << n)
        for edges in combinations(nonempty, 3):
            counts, _ = terminal_counts(n, edges)
            keys = sorted(counts)
            gap = keys[-1] - keys[0] + 1 != len(keys)
            assert gap == predicted_gap(edges), (n, edges, keys)
            cases += 1
    print(f"PASS all three-edge set systems n<=6: {cases} cases")

    planar_obstruction = 0
    for n in range(4, 8):
        edges = [sum(1 << i for i in t) for t in combinations(range(n), 4)]
        for triple in combinations(edges, 3):
            if any((a & b).bit_count() > 2 for a, b in combinations(triple, 2)):
                continue
            counts, _ = terminal_counts(n, triple)
            keys = sorted(counts)
            assert keys[-1] - keys[0] + 1 == len(keys)
            planar_obstruction += 1
    print(f"PASS three distinct four-point carriers n<=7: {planar_obstruction} cases")

    # The explicit eight-point integer witness (translated into 11x11).
    points = [(4,6),(6,6),(10,0),(0,0),(6,0),(8,4),(7,9),(3,7)]
    zero = [t for t in combinations(range(8),4)
            if on_carrier([points[i] for i in t])]
    expected = [(0,1,2,3),(0,1,4,5),(0,1,6,7)]
    assert zero == expected, zero
    edges = [sum(1 << i for i in t) for t in zero]
    counts, safe = terminal_counts(8, edges)
    assert counts == Counter({5:8,7:2}) and len(safe) == 219
    from functools import lru_cache
    @lru_cache(None)
    def gh(s):
        nxt = [s | (1 << i) for i in range(8)
               if not (s & (1 << i)) and (s | (1 << i)) in safe]
        def mex(vals):
            j = 0
            while j in vals: j += 1
            return j
        return (mex({gh(t)[0] for t in nxt}),
                mex({gh(t)[1] for t in nxt}) if nxt else 1)
    for s in safe:
        g, h = gh(s)
        assert (g, h) == ((7-s.bit_count())%2, (8-s.bit_count())%2)
    print("PASS eight-point integer grid witness: 70 determinants, 219 safe states, terminal {5:8,7:2}")

    for q in (4, 5, 6):
        pts, colors, zero = construct(q)
        edges = [sum(1 << j for j, color in enumerate(colors) if color in (-1, i))
                 for i in range(3)]
        counts, safe = terminal_counts(len(pts), edges)
        assert counts == Counter({3*q-7:(q-2)**3, 3*q-5:2}), (q, counts)
        print(f"PASS rational/integer-existence q={q}: N={len(pts)}, {len(zero)} intended 4-tuples, {len(safe)} safe states")


if __name__ == '__main__':
    verify()
