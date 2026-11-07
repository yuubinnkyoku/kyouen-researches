"""Audit DRAT proofs for every d of the p=2207 equality CNFs.

For each d: build the exact CNF, solve with pysat's native CaDiCaL asking for a
DRAT proof (``with_proof=True``), write the proof to a temp file, and check it
with the independent incremental checker ``drat_check_incremental.cpp``.
Results are appended to ``output/drat_audit_full.json`` (resumable; finished d
values are skipped on restart).

A ``VERIFIED`` record certifies that the CNF for that d is UNSAT without
trusting the solver: the checker re-derives every learned clause.
"""
from __future__ import annotations

import argparse
import json
import multiprocessing as mp
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from parabola_half_bound import clauses_for_pair  # noqa: E402
from probe_driver import run_gen  # noqa: E402
from pysat.solvers import Cadical195  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "output"
TMP = Path(tempfile.gettempdir()) / "p2207_drat"
EDGES_PATH = None  # set per prime in main (edges are prime-specific)
RESULT_PATH = None  # set per prime in main


def load_edges(path: str):
    with open(path, encoding="ascii") as f:
        return [tuple(map(int, line.split())) for line in f]


def audit_one(args):
    p, d, checker, budget, edges_path = args
    edges = load_edges(edges_path)
    clauses = clauses_for_pair(p, edges, d)
    solver = Cadical195(bootstrap_with=clauses, with_proof=True)
    solver.conf_budget(budget)
    t0 = time.time()
    res = solver.solve_limited()
    proof = solver.get_proof() if res is False else None
    solver.delete()
    solve_s = time.time() - t0
    if res is not False or not proof:
        return {"d": d, "solver": "SAT" if res else "UNKNOWN", "verified": False,
                "seconds": round(solve_s, 1)}
    cnf = TMP / f"{p}_d{d}.cnf"
    pf = TMP / f"{p}_d{d}.drat"
    with cnf.open("w", encoding="ascii") as f:
        f.write(f"p cnf {(p - 1) // 2} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
    pf.write_text("\n".join(proof) + "\n", encoding="ascii")
    t1 = time.time()
    chk = subprocess.run([checker, str(cnf), str(pf)], capture_output=True, text=True)
    check_s = time.time() - t1
    out = chk.stdout.strip().splitlines()
    rec = {"d": d, "solver": "UNSAT", "proof_lines": len(proof),
           "checker_rc": chk.returncode,
           "verified": chk.returncode == 0 and "VERIFIED" in (out[-1] if out else ""),
           "checker_out": out[-1] if out else chk.stderr.strip()[:200],
           "solve_seconds": round(solve_s, 1), "check_seconds": round(check_s, 1)}
    for f in (cnf, pf):
        try:
            f.unlink(missing_ok=True)
        except OSError:
            pass
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, default=2207)
    ap.add_argument("--from-d", type=int, default=1)
    ap.add_argument("--to-d", type=int, default=None)
    ap.add_argument("--workers", type=int, default=12)
    ap.add_argument("--budget", type=int, default=5_000_000)
    ap.add_argument("--ds", default=None, help="comma separated d list (overrides the range)")
    args = ap.parse_args()
    p = args.p
    h = (p - 1) // 2
    to_d = args.to_d or h
    OUT.mkdir(exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    global EDGES_PATH
    EDGES_PATH = TMP / f"edges_{p}.txt"
    if not EDGES_PATH.exists():
        edges = run_gen(str(Path(os.environ["TEMP"]) / "forbidden_edges.exe"), p)
        EDGES_PATH.write_text("".join(" ".join(map(str, e)) + "\n" for e in edges),
                              encoding="ascii")
    global RESULT_PATH
    RESULT_PATH = OUT / f"drat_audit_full_{p}.json"
    checker = str(Path(os.environ["TEMP"]) / "drat_inc.exe")
    if not Path(checker).exists():
        subprocess.run(["g++", "-O2", "-std=c++17",
                        str(HERE / "drat_check_incremental.cpp"), "-o", checker], check=True)

    results = {}
    if RESULT_PATH.exists():
        for rec in json.loads(RESULT_PATH.read_text(encoding="utf-8"))["records"]:
            results[rec["d"]] = rec
    rng = ([int(x) for x in args.ds.split(",")] if args.ds
           else list(range(args.from_d, to_d + 1)))
    todo = [d for d in rng if results.get(d, {}).get("verified") is not True]
    print(f"p={p} h={h} todo={len(todo)} done={len(results)}", flush=True)
    tasks = [(p, d, checker, args.budget, str(EDGES_PATH)) for d in todo]
    t0 = time.time()
    done = 0
    with mp.Pool(processes=args.workers) as pool:
        for rec in pool.imap_unordered(audit_one, tasks, chunksize=1):
            results[rec["d"]] = rec
            done += 1
            if done % 5 == 0 or not rec["verified"]:
                verified = sum(1 for r in results.values() if r.get("verified"))
                print(f"progress {done}/{len(todo)} verified={verified} "
                      f"last_d={rec['d']} ({time.time()-t0:.0f}s)", flush=True)
                RESULT_PATH.write_text(json.dumps(
                    {"p": p, "h": h, "records": sorted(results.values(), key=lambda r: r["d"])},
                    indent=1) + "\n", encoding="utf-8", newline="\n")
    RESULT_PATH.write_text(json.dumps(
        {"p": p, "h": h, "records": sorted(results.values(), key=lambda r: r["d"])},
        indent=1) + "\n", encoding="utf-8", newline="\n")
    verified = sum(1 for r in results.values() if r.get("verified"))
    print(f"done: verified={verified}/{len(results)} in {time.time()-t0:.0f}s", flush=True)
    return 0


if __name__ == "__main__":
    mp.freeze_support()
    raise SystemExit(main())
