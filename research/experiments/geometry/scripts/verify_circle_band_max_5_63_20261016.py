#!/usr/bin/env python3
"""Certify Q(w)=2T(w) for half-integral horizontal centers, 5<=w<=63, by a finite tangency obstruction.

This is a complete residue enumeration, NOT an enumeration of circles.
Run: python research/experiments/geometry/scripts/verify_circle_band_max_5_63_20261016.py
"""
from __future__ import annotations
import json
from math import isqrt

MODS = (16, 9, 5, 7)
MOD = 5040
ENDPOINTS = (6, 7, 10, 11, 21, 22, 24, 25, 42, 43, 45, 47, 63)
RANGES = ((5, 6, 4), (7, 7, 5), (8, 10, 6), (11, 11, 7),
          (12, 21, 8), (22, 22, 9), (23, 24, 10), (25, 25, 11),
          (26, 42, 12), (43, 43, 13), (44, 45, 14),
          (46, 47, 15), (48, 63, 16))
CIRCLES = ((-3, 0), (-7, 0), (-11, -2), (-25, -6), (-47, 0), (-43, -90))


def max_tangent_double_rows() -> dict[int, dict[int, int]]:
    """CRT bit-mask enumeration: H=s/g, g=1,2,3, all 5040 residues s."""
    result = {w: {g: 0 for g in (1, 2, 3)} for w in ENDPOINTS}
    prefix = {w: (1 << w) - 1 for w in ENDPOINTS}
    square_residues = {m: {x * x % m for x in range(m)} for m in MODS}
    for g in (1, 2, 3):
        for k in range(63):
            # Build independently for each modulus; intersection is equivalent
            # to square modulo 5040 by CRT, since 16,9,5,7 are coprime.
            local = {}
            for m in MODS:
                masks = [0] * m
                qr = square_residues[m]
                for y in range(63):
                    j = y - k
                    if j == 0 or j % g:
                        continue
                    t = j // g
                    for s in range(m):
                        if (t * (s - g * g * t)) % m in qr:
                            masks[s] |= 1 << y
                local[m] = masks
            for s in range(MOD):
                mask = (local[16][s % 16] & local[9][s % 9] &
                        local[5][s % 5] & local[7][s % 7])
                for w in ENDPOINTS:
                    if k >= w:
                        continue
                    cnt = (mask & prefix[w]).bit_count()
                    if cnt > result[w][g]:
                        result[w][g] = cnt
    return result


def circle_double_rows(w: int, C: int, D: int) -> int:
    # x^2+y^2+x+C*y+D=0; discriminant of x-quadratic.
    total = 0
    for y in range(w):
        disc = 1 - 4 * (y * y + C * y + D)
        if disc > 0:
            r = isqrt(disc)
            if r * r == disc and r % 2:
                # Both x=(-1+-r)/2 are distinct integers.
                for x in ((-1 - r) // 2, (-1 + r) // 2):
                    assert x * x + y * y + x + C * y + D == 0
                total += 1
    return total


def main() -> None:
    observed = max_tangent_double_rows()
    table = {}
    for a, b, t in RANGES:
        assert b in observed
        for g in (1, 2, 3):
            assert observed[b][g] < t, (b, g, observed[b][g], t)
        for w in range(a, b + 1):
            witness = max((circle_double_rows(w, C, D), (C, D)) for C, D in CIRCLES)
            assert witness[0] == t, (w, witness, t)
            # A reduced denominator g>=4 for the tangent H would force
            # every double row to be a nonzero multiple of g from k.
            assert (w - 1) // 4 < t
            table[w] = {'T': t, 'Q_half_integral_x_center': 2*t, 'witness_C_D': list(witness[1])}
    output = {'modulus': MOD, 'moduli': MODS, 'endpoints': observed,
              'half_integral_x_center_maxima': table}
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
