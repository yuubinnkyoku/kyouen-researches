"""Optional diagnostic SAT probes, not a proof of all-prime equality.

This run used python-sat==1.9.dev15 and its CaDiCaL195 backend. The saved
witnesses can be verified without installing any SAT package.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
from parabola_half_bound import clauses_for_pair  # noqa: E402
from quadratic_modular_barrier import prime  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--generator", required=True)
    parser.add_argument("--primes", nargs="+", type=int, default=[509,1009])
    args = parser.parse_args()
    from pysat.solvers import Solver
    records = []
    diagnostics = []
    for p in args.primes:
        assert prime(p) and p % 2
        edges = [tuple(map(int,line.split())) for line in
                 subprocess.check_output([args.generator,str(p)],text=True).splitlines()]
        h = (p-1)//2
        clauses = clauses_for_pair(p,edges,h)
        with Solver(name="cadical195",bootstrap_with=clauses) as solver:
            assert solver.solve(), "unsat for this double alone would not refute K0101"
            upper = {literal for literal in solver.get_model() if literal > 0}
            parameters = sorted([0,h,p-h]+[p-i if i in upper else i for i in range(1,h)])
        assert len(parameters) == h+2
        selected = set(parameters)
        assert not any(set(edge) <= selected for edge in edges)
        records.append({"p": p,"parameters": parameters,
                        "maximum_proved": h+2,"double_pair": h})
        diagnostics.append({"p":p,"forbidden_edges":len(edges),
                            "trapezoids":h*(h-1)//2,
                            "nontrapezoid_edges":len(edges)-h*(h-1)//2,
                            "clauses_by_size":dict(sorted(Counter(map(len,clauses)).items()))})
        print(p,len(edges),len(clauses),flush=True)
    here = Path(__file__).resolve().parent
    (here / "density-probe-witnesses.json").write_text(json.dumps(records,indent=2)+"\n")
    (here / "density-probe-diagnostics.json").write_text(json.dumps(diagnostics,indent=2)+"\n")


if __name__ == "__main__":
    main()
