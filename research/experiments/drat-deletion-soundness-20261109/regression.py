"""Build old/fixed/naive checkers and test deletion soundness without a SAT solver."""
from __future__ import annotations

import argparse
import hashlib
import itertools
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
PRIOR = ROOT / "research/experiments/parabola-p2207-no-equality-witness-20261107"
BASE = "a7bdd689f5e0e88bd361202e1b04c2c908ebf9c3"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tmp", type=Path, default=Path(tempfile.gettempdir()))
    args = ap.parse_args()
    args.tmp.mkdir(parents=True, exist_ok=True)
    old = subprocess.check_output([
        "git", "show", f"{BASE}:{(PRIOR / 'drat_check_incremental.cpp').relative_to(ROOT).as_posix()}"
    ], cwd=ROOT)
    sources = {"old": old, "fixed": (PRIOR / "drat_check_incremental.cpp").read_bytes(),
               "naive": (PRIOR / "drat_check.cpp").read_bytes()}
    records = []
    with tempfile.TemporaryDirectory(prefix="drat-deletion-", dir=args.tmp) as td:
        tmp = Path(td)
        bins = {}
        for name, data in sources.items():
            src = tmp / f"{name}.cpp"
            src.write_bytes(data)
            exe = tmp / f"{name}.exe"
            subprocess.run(["g++", "-O2", "-std=c++17", str(src), "-o", str(exe)], check=True)
            bins[name] = exe
        # Each formula is satisfiable (a unit, or a binary implication chain).
        # Prime the level-zero cache, delete its premise, add its opposite by
        # vacuous RAT, then attempt a forged empty clause.
        for sign, chain in itertools.product((1, -1), (False, True)):
            unit = sign
            implied = 2 * sign if chain else unit
            clauses = [[unit]] + ([[-unit, implied]] if chain else [])
            cnf = f"p cnf 3 {len(clauses)}\n" + "".join(
                " ".join(map(str, c)) + " 0\n" for c in clauses)
            proof = f"3 0\nd {unit} 0\n{-unit} 0\n0\n"
            assert any(all(any((lit > 0) == vals[abs(lit)-1] for lit in c) for c in clauses)
                       for vals in itertools.product((False, True), repeat=3))
            records.append(run_case(tmp, bins, f"sat-delete-{sign}-{chain}", cnf, proof, False))
        records.append(run_case(tmp, bins, "unsat-positive", "p cnf 2 3\n1 0\n-1 0\n2 0\n",
                                "d 2 0\n0\n", True))
        records.append(run_case(tmp, bins, "sat-no-proof", "p cnf 2 1\n1 0\n", "2 0\n", False))
        records.append(run_case(tmp, bins, "sat-forged-unit", "p cnf 2 1\n1 0\n", "-1 0\n0\n", False))
        # Replay saved small real proofs, if present; these are optional local
        # controls, identified by content hashes rather than assumed available.
        for d in (2, 180, 253, 268, 391, 700):
            cnf, proof = args.tmp / f"x_2531_{d}.cnf", args.tmp / f"x_2531_{d}.drat"
            if cnf.exists() and proof.exists():
                records.append(run_case(tmp, bins, f"p2531-d{d}", cnf.read_text(encoding="ascii"),
                                        proof.read_text(encoding="ascii"), True))
    output = {"baseline_commit": BASE, "source_sha256": {k: sha(v) for k, v in sources.items()},
              "cases": records}
    (HERE / "regression.json").write_text(json.dumps(output, indent=2) + "\n", encoding="utf-8")
    assert all(r["results"]["fixed"]["accepted"] == r["expected_accept"] and
               r["results"]["naive"]["accepted"] == r["expected_accept"] for r in records)
    assert all(r["results"]["old"]["accepted"] for r in records[:4])
    print(f"PASS {len(records)} cases; old checker falsely accepts all four deletion controls")


def run_case(tmp, bins, name, cnf, proof, expected):
    cp, pp = tmp / "input.cnf", tmp / "input.drat"
    cp.write_text(cnf, encoding="ascii")
    pp.write_text(proof, encoding="ascii")
    results = {}
    for kind, exe in bins.items():
        run = subprocess.run([str(exe), str(cp), str(pp)], capture_output=True, text=True, timeout=60)
        results[kind] = {"rc": run.returncode, "accepted": run.returncode == 0,
                         "stdout": run.stdout.strip(), "stderr": run.stderr.strip()}
    return {"name": name, "expected_accept": expected, "cnf_sha256": sha(cp.read_bytes()),
            "proof_sha256": sha(pp.read_bytes()), "results": results}


if __name__ == "__main__":
    main()
