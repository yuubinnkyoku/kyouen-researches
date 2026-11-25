#!/usr/bin/env python3
"""Independent small-cube audit of the circuit reduction used in K0568.

For d=3,4,5 and q=d+1, enumerate every subset of {0,1}^d of sizes
4..q. Two modular rank implementations (different primes and column orders)
are cross-checked. Hadamard's bound is below both primes, so the modular
ranks equal the rational ranks.

The audit checks that the dependent q-subsets are exactly the q-subsets
containing at least one enumerated inclusion-minimal dependent set (circuit).
This is the finite implementation check behind the general exactly-k lemma;
it does not audit the d=6 enumeration.
"""
from __future__ import annotations

from itertools import combinations
import json
import math

PRIMES = (1_000_003, 1_000_033)


def rank_mod(points: tuple[int, ...], dimension: int, prime: int,
             reverse_columns: bool = False) -> int:
    """Gaussian rank of augmented rows (1, x_1, ..., x_d) over F_prime."""
    width = dimension + 1
    rows = [[1] + [(v >> bit) & 1 for bit in range(dimension)]
            for v in points]
    if reverse_columns:
        rows = [row[::-1] for row in rows]

    rank = 0
    for col in range(width):
        pivot = rank
        while pivot < len(rows) and rows[pivot][col] % prime == 0:
            pivot += 1
        if pivot == len(rows):
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        inv = pow(rows[rank][col], prime - 2, prime)
        for j in range(col, width):
            rows[rank][j] = rows[rank][j] * inv % prime
        for i in range(rank + 1, len(rows)):
            factor = rows[i][col]
            if factor:
                for j in range(col, width):
                    rows[i][j] = (
                        rows[i][j] - factor * rows[rank][j]
                    ) % prime
        rank += 1
        if rank == len(rows):
            break
    return rank


def vertices(mask: int):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def audit_dimension(dimension: int) -> dict:
    q = dimension + 1
    n = 1 << dimension
    dependent: dict[int, set[int]] = {}
    circuits: dict[int, set[int]] = {}
    counts = {}

    # Every square minor has absolute value at most (d+1)^((d+1)/2).
    hadamard_bound = (dimension + 1) ** ((dimension + 1) / 2)
    assert hadamard_bound < min(PRIMES)

    for size in range(4, q + 1):
        dep: set[int] = set()
        for points in combinations(range(n), size):
            r1 = rank_mod(points, dimension, PRIMES[0], False)
            r2 = rank_mod(points, dimension, PRIMES[1], True)
            assert r1 == r2, (dimension, size, points, r1, r2)
            if r1 < size:
                mask = sum(1 << v for v in points)
                dep.add(mask)
        dependent[size] = dep

        if size == 4:
            # No three distinct binary-cube vertices are collinear.
            minimal = dep.copy()
        else:
            previous = dependent[size - 1]
            minimal = {
                mask for mask in dep
                if all((mask ^ (1 << v)) not in previous
                       for v in vertices(mask))
            }
        circuits[size] = minimal
        counts[str(size)] = {
            "all_subsets": math.comb(n, size),
            "dependent_subsets": len(dep),
            "circuits": len(minimal),
        }

    # Every dependent q-set must contain a generated circuit. Greedy deletion
    # through dependent immediate subsets terminates at a minimal dependent
    # subset; the final set must occur in the independently built circuit list.
    covered = 0
    for mask in dependent[q]:
        current = mask
        size = q
        while size > 4:
            for v in vertices(current):
                smaller = current ^ (1 << v)
                if smaller in dependent[size - 1]:
                    current = smaller
                    size -= 1
                    break
            else:
                break
        assert current in circuits[size], (dimension, mask, current, size)
        covered += 1

    # Conversely, every q-superset of a circuit must be dependent.
    supersets_checked = 0
    all_vertices = set(range(n))
    for size, family in circuits.items():
        for circuit in family:
            outside = sorted(all_vertices.difference(vertices(circuit)))
            for extra in combinations(outside, q - size):
                superset = circuit
                for v in extra:
                    superset |= 1 << v
                assert superset in dependent[q], (dimension, circuit, superset)
                supersets_checked += 1

    return {
        "dimension": dimension,
        "q": q,
        "vertices": n,
        "rank_primes": list(PRIMES),
        "hadamard_bound": hadamard_bound,
        "counts": counts,
        "dependent_q_sets": len(dependent[q]),
        "dependent_q_sets_with_circuit": covered,
        "circuit_to_dependent_q_supersets_checked": supersets_checked,
        "result": "PASS",
    }


def main() -> None:
    results = [audit_dimension(d) for d in (3, 4, 5)]
    print(json.dumps({
        "scope": "complete finite audit for d=3,4,5; not a d=6 audit",
        "results": results,
        "all_pass": all(item["result"] == "PASS" for item in results),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
