"""Certify that no size h+2 set exists in Q_p with one DRAT proof.

For size h+2 the counting x + c - e = 2 leaves the single class (1,1,0):
the origin, one complete pair and one element of every other pair.  The class is
encoded as one CNF (4-valued pair variables, exactly one BOTH, no NONE), solved
with CaDiCaL asking for a DRAT proof, and the proof is checked with the fixed
(deletion-sound) incremental checker.  A VERIFIED receipt gives A(p) <= h+1
without auditing the per-d CNFs.

Usage: certify_equality_failure.py --p 2531 [--budget 5000000]
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402
from search_shape_class import build  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
CHECKER_SOURCE = HERE / "drat_check_incremental.cpp"
TMP = Path(tempfile.gettempdir())


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--budget", type=int, default=5_000_000)
    args = ap.parse_args()
    p = args.p
    h = (p - 1) // 2
    size = h + 2
    dest = OUT / f"cert-{p}-{size}"
    dest.mkdir(parents=True, exist_ok=True)
    checker = TMP / "drat_inc_cert.exe"
    if not checker.exists():
        subprocess.run(["g++", "-O2", "-std=c++17", str(CHECKER_SOURCE), "-o", str(checker)],
                       check=True)
    edges = run_gen(str(TMP / "forbidden_edges.exe"), p)
    clauses, nv, kept = build(p, edges, 1, 1, 0)
    print(f"p={p} h={h} size={size} vars={nv} clauses={len(clauses)} kept={kept}", flush=True)
    cnf = dest / f"a{p}_{size}.cnf"
    with cnf.open("w", encoding="ascii") as f:
        f.write(f"p cnf {nv} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
    solver = Cadical195(bootstrap_with=clauses, with_proof=True)
    solver.conf_budget(args.budget)
    t0 = time.time()
    res = solver.solve_limited()
    proof = solver.get_proof() if res is False else None
    solver.delete()
    solve_s = time.time() - t0
    print(f"solve={res} secs={solve_s:.1f} proof_lines={len(proof) if proof else 0}", flush=True)
    record = {"p": p, "h": h, "size": size, "class": [1, 1, 0], "vars": nv,
              "clauses": len(clauses), "kept_edges": kept, "sat": res,
              "unknown": res is None, "solve_seconds": round(solve_s, 1)}
    if proof:
        pf = dest / f"a{p}_{size}.drat"
        pf.write_text("\n".join(proof) + "\n", encoding="ascii")
        sha = hashlib.sha256(pf.read_bytes()).hexdigest()
        t1 = time.time()
        chk = subprocess.run([str(checker), str(cnf), str(pf)], capture_output=True, text=True)
        check_s = time.time() - t1
        out = chk.stdout.strip().splitlines()
        record.update({"proof_lines": len(proof), "proof_sha256": sha,
                       "checker_rc": chk.returncode,
                       "verified": chk.returncode == 0 and bool(out) and "VERIFIED" in out[-1],
                       "checker_out": out[-1] if out else chk.stderr.strip()[:200],
                       "check_seconds": round(check_s, 1)})
        print(f"verified={record['verified']} check_secs={check_s:.1f}", flush=True)
        if record["verified"]:
            with gzip.open(dest / f"a{p}_{size}.drat.gz", "wb", compresslevel=6) as g:
                g.write(pf.read_bytes())
            pf.unlink()
    (dest / "receipt.json").write_text(json.dumps(record, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    print("done", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
