#!/usr/bin/env python3
"""Independent 343-point geometry checks and known 27-point certificates."""
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import random
import subprocess
import tempfile


def run(*args):
    result = subprocess.run(list(map(str, args)), text=True, capture_output=True, check=True)
    return json.loads(result.stdout)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("probe", type=Path)
    parser.add_argument("verifier", type=Path)
    args = parser.parse_args()
    points = list(product(range(7), repeat=3))
    lifts = [(sum(t*t for t in p), *p) for p in points]
    terms = [(p, (-1)**sum(p[i] > p[j] for i in range(4) for j in range(i+1, 4)))
             for p in permutations(range(4))]

    def allowed(four, p):
        if p in four:
            return False
        base = lifts[four[0]]
        rows = [tuple(x-y for x, y in zip(lifts[i], base)) for i in (*four[1:], p)]
        return sum(sign*rows[0][perm[0]]*rows[1][perm[1]]*rows[2][perm[2]]*rows[3][perm[3]]
                   for perm, sign in terms) != 0

    rng = random.Random(20261022)
    samples = [(0, 294, 48, 342), (0, 1, 2, 3), (21, 27, 315, 321), (0, 1, 7, 49)]
    samples += [tuple(sorted(rng.sample(range(343), 4))) for _ in range(100)]
    for four in samples:
        observed = run(args.probe, 7, 0, 100, "--legal", *four)["legal_indices"]
        expected = [p for p in range(343) if allowed(four, p)]
        assert observed == expected, four

    small_points = list(product(range(3), repeat=3))
    lookup = {p: i for i, p in enumerate(small_points)}
    transforms = []
    for axes in permutations(range(3)):
        for flips in product((False, True), repeat=3):
            transforms.append([lookup[tuple(2-p[axes[j]] if flips[j] else p[axes[j]]
                                            for j in range(3))] for p in small_points])
    representatives = sorted({min(tuple(sorted((m[a], m[b]))) for m in transforms)
                              for a, b in combinations(range(27), 2)})
    assert len(representatives) == 20
    with tempfile.TemporaryDirectory() as directory:
        for a, b in representatives:
            certificate = Path(directory) / f"{a}-{b}.cert"
            record = run(args.probe, 3, 1000000, 100000, certificate, a, b)
            assert record["outcome"] == "P"
            assert run(args.verifier, certificate)["outcome"] == "P"
        certificate = Path(directory) / "unknown.cert"
        zero = run(args.probe, 7, 0, 100, certificate, 0, 5)
        assert zero["outcome"] == "UNKNOWN" and not certificate.exists()
    print(json.dumps({"seed": 20261022, "seven_cube_geometry_cases": len(samples),
                      "legal_candidates_compared": len(samples)*343,
                      "three_cube_pair_orbits_independently_verified": 20,
                      "budget_zero_unknown": True}, indent=2))


if __name__ == "__main__":
    main()
