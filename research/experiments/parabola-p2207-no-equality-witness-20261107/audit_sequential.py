"""Sequential (pool-free) DRAT audit for a list of d values.

The multiprocessing driver ``audit_all_d.py`` occasionally stalls in the pool
wait, so this variant processes one d at a time in a single process: generate
the CNF, ask pysat's CaDiCaL for a DRAT proof, check it with the fixed
(deletion-sound) checker, and append the receipt to the same per-prime,
per-checker-hash result file.

Usage: audit_sequential.py --p 3251 --ds 1,26,51 [--budget 5000000]
"""
from __future__ import annotations

import argparse
import hashlib
import json
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
CHECKER_SOURCE = HERE / "drat_check_incremental.cpp"
CHECKER = Path(tempfile.gettempdir()) / "drat_inc_sequential.exe"


def save(path: Path, payload: dict) -> None:
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=1) + "\n", encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--ds", required=True)
    ap.add_argument("--budget", type=int, default=5_000_000)
    args = ap.parse_args()
    p = args.p
    h = (p - 1) // 2
    ds = [int(x) for x in args.ds.split(",") if x.strip()]
    OUT.mkdir(exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)
    sha = hashlib.sha256(CHECKER_SOURCE.read_bytes()).hexdigest()
    result_path = OUT / f"drat_audit_full_{p}_{sha[:16]}.json"
    saved = {}
    if result_path.exists():
        data = json.loads(result_path.read_text(encoding="utf-8"))
        saved = {r["d"]: r for r in data.get("records", [])}
    if not CHECKER.exists():
        subprocess.run(["g++", "-O2", "-std=c++17", str(CHECKER_SOURCE), "-o", str(CHECKER)], check=True)
    edges_path = TMP / f"edges_{p}.txt"
    if not edges_path.exists():
        edges = run_gen(str(Path(os.environ["TEMP"]) / "forbidden_edges.exe"), p)
        edges_path.write_text("".join(" ".join(map(str, e)) + "\n" for e in edges), encoding="ascii")
    with edges_path.open(encoding="ascii") as f:
        edges = [tuple(map(int, line.split())) for line in f]
    todo = [d for d in ds if saved.get(d, {}).get("verified") is not True]
    print(f"p={p} h={h} edges={len(edges)} todo={len(todo)}", flush=True)
    for d in todo:
        clauses = clauses_for_pair(p, edges, d)
        cnf = TMP / f"seq_{p}_{d}.cnf"
        pf = TMP / f"seq_{p}_{d}.drat"
        with cnf.open("w", encoding="ascii") as f:
            f.write(f"p cnf {h} {len(clauses)}\n")
            for c in clauses:
                f.write(" ".join(map(str, c)) + " 0\n")
        solver = Cadical195(bootstrap_with=clauses, with_proof=True)
        solver.conf_budget(args.budget)
        t0 = time.time()
        res = solver.solve_limited()
        proof = solver.get_proof() if res is False else None
        solver.delete()
        solve_s = time.time() - t0
        if res is not False or not proof:
            saved[d] = {"d": d, "solver": "SAT" if res else "UNKNOWN", "verified": False,
                        "solve_seconds": round(solve_s, 1)}
            print(f"d={d} solver={saved[d]['solver']}", flush=True)
            save(result_path, {"p": p, "h": h, "checker_source_sha256": sha,
                               "records": sorted(saved.values(), key=lambda r: r["d"])})
            continue
        pf.write_text("\n".join(proof) + "\n", encoding="ascii")
        t1 = time.time()
        chk = subprocess.run([str(CHECKER), str(cnf), str(pf)], capture_output=True, text=True)
        check_s = time.time() - t1
        out = chk.stdout.strip().splitlines()
        saved[d] = {"d": d, "solver": "UNSAT", "proof_lines": len(proof),
                    "checker_rc": chk.returncode,
                    "verified": chk.returncode == 0 and bool(out) and "VERIFIED" in out[-1],
                    "checker_out": out[-1] if out else chk.stderr.strip()[:200],
                    "solve_seconds": round(solve_s, 1), "check_seconds": round(check_s, 1)}
        print(f"d={d} verified={saved[d]['verified']} lines={len(proof)} check={check_s:.0f}s", flush=True)
        save(result_path, {"p": p, "h": h, "checker_source_sha256": sha,
                           "records": sorted(saved.values(), key=lambda r: r["d"])})
        for f in (cnf, pf):
            try:
                f.unlink(missing_ok=True)
            except OSError:
                pass
    print("done", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
