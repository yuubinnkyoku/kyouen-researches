"""Exact all-real-parameter census. Standard library only; no floating point.

Run: python verify.py [--output results.json]
Two determinant constructions and two independent game recurrences are compared.
"""
import argparse
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, permutations
import json
from pathlib import Path


def det_permutation(rows):
    n = len(rows)
    total = 0
    for p in permutations(range(n)):
        term = (-1) ** sum(p[i] > p[j] for i in range(n) for j in range(i + 1, n))
        for i in range(n):
            term *= rows[i][p[i]]
        total += term
    return total


def det3(a, b, c):
    return (a[0] * (b[1] * c[2] - b[2] * c[1])
            - a[1] * (b[0] * c[2] - b[2] * c[0])
            + a[2] * (b[0] * c[1] - b[1] * c[0]))


def coefficients(points):
    b = det_permutation([[x*x, x, y, 1] for x, y in points])
    a = det_permutation([[y*y, x, y, 1] for x, y in points])
    affine = [(x, y, 1) for x, y in points]
    weights = [(-1)**i * det3(*[r for j, r in enumerate(affine) if i != j])
               for i in range(4)]
    independent_b = sum(w*x*x for w, (x, y) in zip(weights, points))
    independent_a = sum(w*y*y for w, (x, y) in zip(weights, points))
    assert (a, b) == (independent_a, independent_b)
    return a, b


def mex(values):
    ans = 0
    while ans in values:
        ans += 1
    return ans


def occupied_game(n, edges):
    """Full subset DP; safety tested when the highest occupied bit is added."""
    size = 1 << n
    incident = [[] for _ in range(n)]
    for e in edges:
        for i in range(n):
            if e & (1 << i):
                incident[i].append(e)
    safe = bytearray(size)
    safe[0] = 1
    for s in range(1, size):
        i = s.bit_length() - 1
        safe[s] = safe[s ^ (1 << i)] and not any(s & e == e for e in incident[i])
    grundy = [-1] * size
    layers = Counter()
    hist = Counter()
    terminals = Counter()
    full = size - 1
    for s in range(size - 1, -1, -1):
        if not safe[s]:
            continue
        values = set()
        vacant = full ^ s
        while vacant:
            bit = vacant & -vacant
            vacant ^= bit
            if safe[s | bit]:
                values.add(grundy[s | bit])
        g = mex(values)
        grundy[s] = g
        layers[s.bit_count()] += 1
        hist[g] += 1
        if not values:
            terminals[s.bit_count()] += 1
    return grundy, {
        "empty_grundy": grundy[0],
        "first_move_grundy": [grundy[1 << i] for i in range(n)],
        "winning_first_moves": [i for i in range(n) if grundy[1 << i] == 0],
        "safe_count": sum(safe),
        "safe_layers": dict(sorted(layers.items())),
        "grundy_histogram": dict(sorted(hist.items())),
        "terminal_sizes": dict(sorted(terminals.items())),
    }


def residual_game(n, edges):
    """Recursive residual forbidden-set reduction, independent of subset safety DP."""
    @lru_cache(None)
    def solve(available):
        family = [e & available for e in edges]
        assert 0 not in family
        blocked = 0
        for e in family:
            if e & (e - 1) == 0:
                blocked |= e
        values = set()
        bits = available & ~blocked
        while bits:
            bit = bits & -bits
            bits ^= bit
            values.add(solve(available ^ bit))
        return mex(values)

    full = (1 << n) - 1
    root = solve(full)
    values = {}
    # Every safe occupied subset occurs in solve's traversal from the empty board.
    # Reconstruct its residual constraints directly; compare every safe state.
    for available in range(1 << n):
        reduced = [e & available for e in edges]
        if 0 not in reduced:
            values[full ^ available] = solve(available)
    return root, values


def census(n):
    points = [(x, y) for y in range(n) for x in range(n)]
    universal = []
    exceptional = {}
    nonvanishing = 0
    for ids in combinations(range(n*n), 4):
        a, b = coefficients([points[i] for i in ids])
        mask = sum(1 << i for i in ids)
        if a == b == 0:
            universal.append(mask)
        elif a:
            exceptional.setdefault(Fraction(-b, a), []).append(mask)
        else:
            nonvanishing += 1
    # Transposition must map lambda to its reciprocal; zero is not invertible.
    def transpose(mask):
        return sum(1 << (x*n + y) for y in range(n) for x in range(n)
                   if mask & (1 << (y*n + x)))
    assert {transpose(e) for e in universal} == set(universal)
    for value, extra in exceptional.items():
        if value:
            assert {transpose(e) for e in extra} == set(exceptional[1 / value])
    output = {"side": n, "point_index": "i=y*n+x", "universal_edges": universal,
              "nonzero_constant_count": nonvanishing, "classes": []}
    families = [("generic", [])] + [(str(v), exceptional[v]) for v in sorted(exceptional)]
    for label, extra in families:
        edges = sorted(universal + extra)
        g, result = occupied_game(n*n, edges)
        other_root, other = residual_game(n*n, edges)
        assert other_root == g[0]
        assert len(other) == result["safe_count"]
        assert all(g[s] == value for s, value in other.items())
        output["classes"].append({"lambda": label, "edge_count": len(edges),
                                  "extra_edges": sorted(extra),
                                  "independently_compared_states": len(other), **result})
        print("checked", n, label, "g=", g[0], "safe=", len(other), flush=True)
    by_parameter = {row["lambda"]: row for row in output["classes"]}
    for value in exceptional:
        if value:
            left, right = by_parameter[str(value)], by_parameter[str(1/value)]
            assert left["grundy_histogram"] == right["grundy_histogram"]
            assert all(left["first_move_grundy"][y*n+x]
                       == right["first_move_grundy"][x*n+y]
                       for y in range(n) for x in range(n))
    return output


def structural_audit():
    # Two arbitrary horizontal rows, with holes and unequal candidate counts.
    horizontal = [(0, -2), (1, -2), (4, -2), (7, -2),
                  (-1, 3), (2, 3), (3, 3), (6, 3)]
    for quad in combinations(horizontal, 4):
        a, b = coefficients(quad)
        assert a == 0
        counts = Counter(y for x, y in quad)
        if len(counts) == 1:
            predicted = True
        elif sorted(counts.values()) == [1, 3]:
            predicted = False
        else:
            sums = [sum(x for x, yy in quad if yy == y) for y in counts]
            predicted = sums[0] == sums[1]
        assert (b == 0) == predicted
    # Singular lambda=0 behaves differently under a swap of axes.
    vertical = [(0, 0), (0, 1), (0, 2), (1, 0)]
    a, b = coefficients(vertical)
    assert b == 0 and a != 0
    return {"two_horizontal_rows_quads": 70,
            "vertical_singular_example": vertical,
            "vertical_coefficients_a_b": [a, b]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path(__file__).with_name("results.json"))
    args = parser.parse_args()
    result = {"rule": "det[x*x+lambda*y*y,x,y,1]=0 forbids four points",
              "arithmetic": "integer determinants and reduced exact rational parameters",
              "structural_audit": structural_audit(),
              "boards": []}
    for n in (2, 3, 4):
        board = census(n)
        result["boards"].append(board)
        print(n, "universal", len(board["universal_edges"]), "classes", len(board["classes"]), flush=True)
        for row in board["classes"]:
            print(row["lambda"], row["edge_count"], row["empty_grundy"],
                  row["safe_count"], row["winning_first_moves"], flush=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
