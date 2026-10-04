"""Exact independent audit of the explicit arbitrary-point-board family.

The theorem for every r is proved in proof.md. This script checks finite
instances by the existing integer geometry core, a generic Leibniz determinant,
brute-force deletion sets, and an uncompressed forbidden-hyperedge game search.
It requires only Python's standard library.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import cache
from hashlib import sha256
from itertools import combinations, permutations
import json
from math import comb, lcm, prod
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts/research"))
from kyouen_core import is_forbidden_quad  # noqa: E402

PERMUTATIONS = tuple(
    (permutation, (-1) ** sum(permutation[i] > permutation[j]
                              for i in range(4) for j in range(i + 1, 4)))
    for permutation in permutations(range(4))
)


def determinant4(points):
    """Generic 4x4 Leibniz formula, independent of the translated core."""
    rows = [(x, y, x*x + y*y, 1) for x, y in points]
    return sum(sign * prod(rows[i][permutation[i]] for i in range(4))
               for permutation, sign in PERMUTATIONS)


def determinant3(points):
    (x, y), (u, v), (s, t) = points
    return (u-x)*(t-y) - (v-y)*(s-x)


def schur31(parameters):
    e1 = sum(parameters)
    e2 = sum(prod(pair) for pair in combinations(parameters, 2))
    e3 = sum(prod(triple) for triple in combinations(parameters, 3))
    e4 = prod(parameters)
    return e1*e1*e2 - e2*e2 - e1*e3 + e4


def family(r):
    if r < 1:
        raise ValueError("r must be positive")
    parameters = [coefficient * 100**i for i in range(r)
                  for coefficient in (1, 10, -11)]
    scale = lcm(*(abs(t) * (1 + 4*t**4) for t in parameters))
    stones = [(scale // (t * (1 + 4*t**4)),
               2*scale*t // (1 + 4*t**4)) for t in parameters]
    # Inversion centre p remains the first point. Similarity preserves geometry.
    points = [(0, 0), *stones]
    expected = {(0, 3*i+1, 3*i+2, 3*i+3) for i in range(r)}
    return parameters, scale, points, expected


def audit_geometry(r):
    parameters, scale, points, expected = family(r)
    generic_edges = set()
    for indices in combinations(range(len(points)), 4):
        quad = [points[i] for i in indices]
        independent = determinant4(quad) == 0
        shared = is_forbidden_quad(quad)
        assert independent == shared, (r, indices)
        if independent:
            generic_edges.add(indices)
    assert generic_edges == expected, (r, generic_edges ^ expected)
    assert all(determinant3([points[i] for i in indices])
               for indices in combinations(range(len(points)), 3))
    # Directly enumerate the original cubic's collinear triples as well.
    cubic = [(t, 2*t**3) for t in parameters]
    cubic_triples = {indices for indices in combinations(range(3*r), 3)
                     if determinant3([cubic[i] for i in indices]) == 0}
    assert cubic_triples == {(3*i, 3*i+1, 3*i+2) for i in range(r)}
    # All deletion sets of size < r miss at least one blocker; r is achieved.
    block_masks = [sum(1 << j for j in range(3*i, 3*i+3)) for i in range(r)]
    deletions_checked = 0
    for size in range(r):
        for indices in combinations(range(3*r), size):
            removed = sum(1 << j for j in indices)
            assert not all(removed & block for block in block_masks)
            deletions_checked += 1
    witness = [3*i for i in range(r)]
    assert all(sum(1 << j for j in witness) & block for block in block_masks)
    return dict(r=r, points=points, parameters=parameters, scale=scale,
                cubic_triples=sorted(cubic_triples),
                forbidden_quadruples=sorted(generic_edges), rho=r,
                geometry_four_sets=comb(3*r+1, 4),
                geometry_three_sets=comb(3*r+1, 3),
                deletion_sets_below_r=deletions_checked,
                unlocking_deletion_indices=[j+1 for j in witness],
                maximum=3*r, minimum_maximal=2*r+1)


def predicted_grundy(r, state):
    occupancy = [(state >> (3*i+1) & 7).bit_count() for i in range(r)]
    occupied = sum(occupancy)
    if state & 1:
        return (2*r - occupied) % 2
    if 3 in occupancy:
        return (3*r - occupied) % 2
    a, b, c = (occupancy.count(i) for i in range(3))
    if r % 2:
        return (3*r - occupied) % 2
    if c:
        return 2 + b % 2
    return (a+1) % 2


def audit_game(r):
    # Generate edges from their index definition; generic subset legality only.
    edges = [(1 | (7 << (3*i+1))) for i in range(r)]
    full = (1 << (3*r+1)) - 1
    terminal_sizes = Counter()
    values = Counter()

    @cache
    def grundy(state):
        options = set()
        remaining = full ^ state
        while remaining:
            bit = remaining & -remaining
            remaining ^= bit
            child = state | bit
            if not any(child & edge == edge for edge in edges):
                options.add(grundy(child))
        mex = 0
        while mex in options:
            mex += 1
        assert mex == predicted_grundy(r, state), (r, state, mex)
        values[mex] += 1
        if not options:
            terminal_sizes[state.bit_count()] += 1
        return mex

    root = grundy(0)
    assert root == 1
    expected_terminals = Counter({2*r+1: 3**r})
    expected_terminals[3*r] += 1
    assert terminal_sizes == expected_terminals
    assert grundy.cache_info().currsize == 2**(3*r) + 7**r
    return dict(r=r, root_grundy=root, safe_states=grundy.cache_info().currsize,
                grundy_distribution=dict(sorted(values.items())),
                maximal_size_distribution=dict(sorted(terminal_sizes.items())))


def audit_cubic_identity():
    substitutions = 0
    for parameters in combinations(range(-6, 7), 4):
        vandermonde = prod(b-a for a, b in combinations(parameters, 2))
        for coefficient in (2, 3, -2):
            points = [(t, coefficient*t**3) for t in parameters]
            determinant = determinant4(points)
            assert determinant == coefficient*vandermonde*(1-coefficient**2*schur31(parameters))
            assert determinant
            substitutions += 1
    return dict(integer_parameters="all 4-subsets of [-6,6]",
                coefficients=[2, 3, -2], substitutions=substitutions)


def audit_symbolic_identity():
    """Expand all coefficients in Z[t1,t2,t3,t4,c], without sampling."""
    one = {(0, 0, 0, 0, 0): 1}

    def add(*polynomials):
        answer = Counter()
        for polynomial in polynomials:
            answer.update(polynomial)
        return {power: coefficient for power, coefficient in answer.items()
                if coefficient}

    def scale(coefficient, polynomial):
        return {power: coefficient*value for power, value in polynomial.items()
                if coefficient*value}

    def multiply(*polynomials):
        answer = one
        for polynomial in polynomials:
            result = Counter()
            for left, coefficient in answer.items():
                for right, value in polynomial.items():
                    result[tuple(a+b for a, b in zip(left, right))] += coefficient*value
            answer = {power: value for power, value in result.items() if value}
        return answer

    def power(polynomial, exponent):
        return multiply(*(polynomial for _ in range(exponent)))

    variables = [{tuple(int(i == j) for j in range(5)): 1} for i in range(5)]
    parameters, coefficient = variables[:4], variables[4]
    elementary = [one] + [add(*(multiply(*subset)
                              for subset in combinations(parameters, degree)))
                          for degree in range(1, 5)]
    e1, e2, e3, e4 = elementary[1:]
    schur = add(multiply(power(e1, 2), e2), scale(-1, power(e2, 2)),
                scale(-1, multiply(e1, e3)), e4)
    vandermonde = multiply(*(add(right, scale(-1, left))
                             for left, right in combinations(parameters, 2)))
    rows = []
    for parameter in parameters:
        y = multiply(coefficient, power(parameter, 3))
        norm = add(power(parameter, 2), power(y, 2))
        rows.append((parameter, y, norm, one))
    determinant = add(*(scale(sign, multiply(*(rows[i][permutation[i]] for i in range(4))))
                        for permutation, sign in PERMUTATIONS))
    expected = multiply(coefficient, vandermonde,
                        add(one, scale(-1, multiply(power(coefficient, 2), schur))))
    assert determinant == expected
    encoded = json.dumps(sorted(determinant.items()), separators=(",", ":")).encode()
    return dict(ring="Z[t1,t2,t3,t4,c]", method="exact sparse coefficient expansion",
                nonzero_monomials=len(determinant), identity_difference_monomials=0,
                expanded_determinant_sha256=sha256(encoded).hexdigest())


def main():
    if not __debug__:
        raise SystemExit("Assertions must remain enabled.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geometry-max", type=int, default=8)
    parser.add_argument("--game-max", type=int, default=6)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("audit.json"))
    args = parser.parse_args()
    if not (1 <= args.geometry_max <= 10 and 1 <= args.game_max <= 6):
        parser.error("bounded audit requires geometry-max <= 10, game-max <= 6")
    result = dict(scope="Finite independent checks supporting the universal proof in proof.md",
                  symbolic_identity=audit_symbolic_identity(),
                  cubic_identity=audit_cubic_identity(), geometry=[], games=[])
    for r in range(1, args.geometry_max+1):
        result["geometry"].append(audit_geometry(r))
        print("geometry", r, "rho", r, flush=True)
    for r in range(1, args.game_max+1):
        result["games"].append(audit_game(r))
        print("game", r, "all safe states", result["games"][-1]["safe_states"], flush=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n", encoding="utf-8")
    print(args.output, flush=True)


if __name__ == "__main__":
    main()
