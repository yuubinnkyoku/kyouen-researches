#!/usr/bin/env python3
"""Independent audit of the exact finite-window central 2+1+1 formula.

No external dependencies.  Direct check uses the 4x4 lifted determinant,
not the quadratic equation used by the representation enumerator.
"""
import itertools
import json
from math import isqrt
from pathlib import Path


def representations(h, d):
    n = d * d - 4 * h * h
    if n < 0:
        return
    for a in range(-isqrt(n), isqrt(n) + 1):
        b2 = n - a * a
        b = isqrt(b2)
        if b * b == b2:
            yield a, b
            if b:
                yield a, -b


def decode(d, a, b):
    assert (d + a + b) % 2 == 0
    return (d + a + b) // 2, (d + a - b) // 2


def span(d, u, v):
    return max(d, u, v) - min(0, u, v)


def overhang(d, a, b):
    z = abs(a) + abs(b) - d
    assert z % 2 == 0
    return max(0, z // 2)


def count_by_representations(h, m):
    result = 0
    by_d = {}
    for d in range(1, m):
        n = 0
        for a, b in representations(h, d):
            u, v = decode(d, a, b)
            s = span(d, u, v)
            assert s == d + overhang(d, a, b)
            n += max(0, m - s)
        by_d[d] = n
        result += n
    return result, by_d


def determinant4(points):
    rows = [(x * x + y * y, x, y, 1) for x, y in points]
    total = 0
    for perm in itertools.permutations(range(4)):
        inversions = sum(perm[i] > perm[j] for i in range(4) for j in range(i + 1, 4))
        prod = 1
        for i in range(4):
            prod *= rows[i][perm[i]]
        total += -prod if inversions % 2 else prod
    return total


def count_direct(h, m):
    by_d = {d: 0 for d in range(1, m)}
    for a in range(m):
        for b in range(a + 1, m):
            d = b - a
            for u in range(m):
                for v in range(m):
                    if determinant4(((a, 0), (b, 0), (u, -h), (v, h))) == 0:
                        by_d[d] += 1
    return sum(by_d.values()), by_d


def audit():
    direct_cases = 0
    total_direct = 0
    examples = {}
    for h in range(1, 6):
        for m in range(2, 13):
            formula, formula_by_d = count_by_representations(h, m)
            direct, direct_by_d = count_direct(h, m)
            assert formula == direct, (h, m, formula, direct)
            assert formula_by_d == direct_by_d, (h, m, formula_by_d, direct_by_d)
            direct_cases += 1
            total_direct += direct
            if h == 1 and m in (4, 6, 8, 10, 12):
                examples[str(m)] = {'total': direct, 'by_chord': {str(k): v for k, v in direct_by_d.items() if v}}
    rep_cases = 0
    rep_count = 0
    for h in range(1, 17):
        for d in range(1, 301):
            reps = list(representations(h, d))
            rep_cases += 1
            rep_count += len(reps)
            for a, b in reps:
                u, v = decode(d, a, b)
                assert span(d, u, v) == d + overhang(d, a, b)
                assert (0 <= u <= d and 0 <= v <= d) == (abs(a * b) <= 2 * h * h)
                assert (0 < u < d and 0 < v < d) == (abs(a * b) < 2 * h * h)
                assert determinant4(((0, 0), (d, 0), (u, -h), (v, h))) == 0
    return {'direct_conditions': direct_cases, 'direct_cocircular_quads': total_direct,
            'representation_conditions': rep_cases, 'representations_checked': rep_count,
            'h1_board_counts': examples, 'status': 'all matched'}


if __name__ == '__main__':
    out = audit()
    target = Path(__file__).resolve().parents[1] / 'output' / 'central_211_finite_width_audit_20261011.json'
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(out, ensure_ascii=False, indent=2))
