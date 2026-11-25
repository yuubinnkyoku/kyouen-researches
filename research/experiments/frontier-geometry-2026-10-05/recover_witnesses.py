"""Persist the missing p=131..251 witnesses using the existing pair SAT core.

The faster edge generator is optional; the Python generator remains the
repository's established implementation. No SAT package is needed here.
"""
from __future__ import annotations

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
from parabola_half_bound import clauses_for_pair, forbidden, solve  # noqa: E402
from quadratic_modular_barrier import det4, prime  # noqa: E402


def recover(p: int, generator: str | None) -> dict:
    if generator:
        output = subprocess.check_output([generator, str(p)], text=True)
        edges = [tuple(map(int, line.split())) for line in output.splitlines()]
    else:
        _, edges, _ = forbidden(p)
    h = (p - 1) // 2
    for d in range(h, 0, -1):
        clauses = clauses_for_pair(p, edges, d)
        calls = [0]
        solution = solve(clauses, counter=calls)
        if solution is None:
            continue
        parameters = sorted([0, d, p-d] + [
            p-i if solution.get(i, False) else i
            for i in range(1, h+1) if i != d
        ])
        assert len(parameters) == h + 2
        # This check deliberately tests every selected quadruple, rather
        # than trusting the modular filter, edge list, or SAT clauses.
        for q in combinations(parameters, 4):
            assert det4([(t, t*t % p) for t in q]) != 0
        return {"p": p, "maximum_proved": h+2, "double_pair": d,
                "parameters": parameters, "forbidden_quadruples": len(edges),
                "clauses_by_size": dict(sorted(Counter(map(len, clauses)).items())),
                "sat_calls": calls[0], "selected_quadruples_checked":
                (h+2)*(h+1)*h*(h-1)//24}
    raise RuntimeError(f"No equality witness at p={p}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generator", help="compiled forbidden_edges.cpp")
    parser.add_argument("--min-prime", type=int, default=131)
    parser.add_argument("--max-prime", type=int, default=251)
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).with_name("recovered-witnesses.json"))
    args = parser.parse_args()
    records = []
    for p in range(args.min_prime, args.max_prime+1):
        if not prime(p):
            continue
        record = recover(p, args.generator)
        records.append(record)
        print(p, record["maximum_proved"], record["sat_calls"], flush=True)
        args.output.write_text(json.dumps(records, indent=2)+"\n", encoding="utf-8")


if __name__ == "__main__":
    main()
