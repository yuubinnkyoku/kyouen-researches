#!/usr/bin/env python3
"""Known-board outcomes and negative tests of independent certificate checks."""
from itertools import combinations, permutations, product
from pathlib import Path
import argparse
import json
import subprocess
import tempfile


def run(*args, success=True):
    result = subprocess.run(list(map(str, args)), text=True, capture_output=True)
    assert (result.returncode == 0) == success, (args, result.stdout, result.stderr)
    return result.stdout


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("solver", type=Path)
    parser.add_argument("verifier", type=Path)
    args = parser.parse_args()
    points = list(product(range(3), repeat=3))
    lookup = {p: i for i, p in enumerate(points)}
    transforms = []
    for axes in permutations(range(3)):
        for flips in product((False, True), repeat=3):
            transforms.append([lookup[tuple(2-p[axes[j]] if flips[j] else p[axes[j]]
                                            for j in range(3))] for p in points])
    representatives = sorted({min(tuple(sorted((m[a], m[b]))) for m in transforms)
                              for a, b in combinations(range(27), 2)})
    assert len(representatives) == 20
    with tempfile.TemporaryDirectory() as directory:
        temp = Path(directory)
        pairs = temp / "pairs.txt"
        pairs.write_text("".join(f"{a} {b}\n" for a, b in representatives))
        output = run(args.solver, 3, 1000000, temp / "pair", "--batch", pairs)
        records = [json.loads(line) for line in output.splitlines()]
        assert len(records) == 20 and all(r["outcome"] == "P" for r in records)
        certificates = [temp / f"pair-{a}-{b}.cert" for a, b in representatives]
        for path in certificates:
            assert json.loads(run(args.verifier, path))["verified"]
        merged = temp / "empty.cert"
        run(args.solver, "--merge", 3, merged, *certificates)
        summary = json.loads(run(args.verifier, merged))
        assert summary["outcome"] == "P" and summary["layers"]["0"] == 1
        zero_path = temp / "zero.cert"
        zero = json.loads(run(args.solver, 3, 0, zero_path, 0, 1))
        assert zero["outcome"] == "UNKNOWN" and not zero_path.exists()
        lines = merged.read_text().splitlines()
        for name, altered in {
            "missing-child": lines[:-1],
            "duplicate": [*lines, lines[1]],
            "wrong-root-label": [lines[0], "0 0 1 0 0", *lines[2:]],
            "truncated": [lines[0], "0 0"],
            "outside-board": [*lines, f"0 {1 << 40} 0 0 0"],
            "outside-root": [f"Q5CUBE1 3 0 {1 << 40}", *lines[1:]],
        }.items():
            path = temp / f"{name}.cert"
            path.write_text("\n".join(altered)+"\n")
            run(args.verifier, path, success=False)
    print(json.dumps({"three_cube_pair_orbits": 20, "all_outcomes_match_K0435": True,
                      "independent_certificates": 21, "negative_cases": 6,
                      "budget_zero_unknown": True}, indent=2))


if __name__ == "__main__":
    main()
