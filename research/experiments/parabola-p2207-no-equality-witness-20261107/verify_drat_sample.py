"""Audit DRAT proofs for a sample of d values of the p=2207 equality CNFs.

Pipeline per d: build the CNF with the exact encoder, ask cadical (WSL) for a
text-format DRAT proof, and check it with the independent RUP/RAT checker
``drat_check.cpp`` (built by this script if needed).  The proof file is removed
after checking, but its line count and size are recorded.

A verified proof is a solver-independent certificate that the CNF for that d is
UNSAT -- the audit step that K0693 currently lacks.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from parabola_half_bound import clauses_for_pair  # noqa: E402
from probe_driver import run_gen  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
TMP = Path(os.environ.get("TEMP", "/tmp"))
PD = TMP / "p2207_drat"


def to_wsl(path: Path) -> str:
    p = Path(path).resolve()
    return "/mnt/" + p.drive.rstrip(":").lower() + str(p)[len(p.drive):].replace("\\", "/")


def build_checker() -> Path:
    exe = TMP / "drat_check.exe"
    subprocess.run(["g++", "-O2", "-std=c++17", str(HERE / "drat_check.cpp"), "-o", str(exe)],
                   check=True)
    return exe


def main() -> int:
    p = 2207
    ds = [int(x) for x in sys.argv[1:]] or [1, 1050, 1103]
    PD.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(exist_ok=True)
    chk = build_checker()
    edges = run_gen(str(TMP / "forbidden_edges.exe"), p)
    records = []
    for d in ds:
        clauses = clauses_for_pair(p, edges, d)
        cnf = PD / f"d{d}.cnf"
        with cnf.open("w", encoding="ascii") as f:
            f.write(f"p cnf {(p - 1) // 2} {len(clauses)}\n")
            for c in clauses:
                f.write(" ".join(map(str, c)) + " 0\n")
        proof = PD / f"d{d}.txt.drat"
        res = subprocess.run(["wsl", "-d", "Ubuntu", "-u", "root", "--", "bash", "-c",
                              f"cadical -q --binary=false {to_wsl(cnf)} {to_wsl(proof)}"],
                             capture_output=True, text=True)
        lines = sum(1 for _ in proof.open(encoding="ascii", errors="replace")) if proof.exists() else 0
        size = proof.stat().st_size if proof.exists() else 0
        audit = subprocess.run([str(chk), str(cnf), str(proof)],
                               capture_output=True, text=True)
        rec = {"d": d, "clauses": len(clauses), "proof_lines": lines, "proof_bytes": size,
               "solver_said": "UNSAT" if "s UNKNOWN" not in res.stdout else "UNKNOWN",
               "checker_rc": audit.returncode,
               "checker_out": audit.stdout.strip().splitlines()[-1] if audit.stdout.strip() else ""}
        records.append(rec)
        print(json.dumps(rec, ensure_ascii=False), flush=True)
        try:
            proof.unlink()
        except OSError:
            pass
    (OUT / "drat_audit_sample.json").write_text(
        json.dumps({"p": p, "records": records,
                    "note": "verified proofs are certificates that the CNF is UNSAT"},
                   indent=2) + "\n", encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
