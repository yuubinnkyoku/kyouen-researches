"""W14: re-solve the easy-UNSAT d values with solvers other than Cadical195.

Same encoding as the W7 sweep (`search_shape_class.build`: p=2647, size=1322,
class (1,1,3)); the only variable is the SAT solver. Targets:
easy-UNSAT {1, 300, 478, 851} and hard-UNKNOWN {100}.

Modes
  parent (default): build the class CNF once, cache it, then run every
      (solver, d) query in its own subprocess with a wall-clock cap. A query
      that exceeds the cap is recorded as ``timeout`` (UNKNOWN), never as UNSAT.
  --worker: internal; solves one query and prints one JSON record.

Budget policy
  Solvers with ``conf_budget`` + ``solve_limited(assumptions=[B_d])`` get the
  sweep's 100k conflict budget and assumption B_d, exactly like the sweep.
  Kissat404 has conflict limits but no assumptions (pysat ignores them), so it
  gets B_d as a unit clause; this is recorded per record as setup="unit-B_d".
  Every record carries the budget policy, and ``timeout`` records also carry
  whether the conflict budget or the wall cap ended the query.

Output: output/w14-cross-solver.json (own file; sweep JSON untouched).
Usage:
  python cross_solver_probe.py [--solvers Glucose4,Minisat22,...]
      [--device 120] [--deadline 900] [--output ...]
"""
from __future__ import annotations

import argparse
import json
import os
import pickle
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from search_shape_class import build  # noqa: E402

ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from probe_driver import run_gen  # noqa: E402

P, SIZE, X, C, E = 2647, 1322, 1, 1, 3
BUDGET = 100_000
DS = [1, 300, 478, 851, 100]
CACHE = HERE / "output" / "w14-cnf-cache.pkl"

# Assumption-capable, conflict-budget-capable solvers tried in W14.
ASSUMP_SOLVERS = ["Glucose4", "Glucose3", "Glucose42", "Minisat22",
                  "MinisatGH", "Maplesat", "MapleCM", "MapleChrono",
                  "Gluecard3", "Gluecard4", "Mergesat3", "Ergo"]
# Conflict-budget-capable but assumption-less: B_d goes in as a unit clause.
UNIT_SOLVERS = ["Kissat404"]
REFERENCE = "Cadical195"


def v(pair: int, kind: str) -> int:
    return 4 * pair - 4 + {"B": 1, "N": 2, "L": 3, "H": 4}[kind]


def decode(model, p: int, h: int, x: int) -> list[int]:
    pos = {i for i in model if i > 0}
    chosen = {0} if x else set()
    for t in range(1, p):
        pair = t if t <= h else p - t
        lit = 4 * pair - 4 + (1 if t <= h else 4)
        if lit in pos:
            chosen.add(t)
    return sorted(chosen)


def worker(solver_name: str, d: int, cache: Path, budget: int) -> int:
    import pysat.solvers as S

    blob = pickle.loads(cache.read_bytes())
    clauses, edges = blob["clauses"], blob["edges"]
    h = (P - 1) // 2
    cls = getattr(S, solver_name, None)
    if cls is None:
        print(json.dumps({"error": f"solver {solver_name} missing"}))
        return 1
    unit_mode = solver_name in UNIT_SOLVERS
    cnf = clauses + ([[v(d, "B")]] if unit_mode else [])
    t_build = time.time()
    solver = cls(bootstrap_with=cnf)
    build_s = time.time() - t_build
    rec: dict = {"solver": solver_name, "d": d,
                 "setup": "unit-B_d" if unit_mode else "assumption-B_d",
                 "budget": budget}
    try:
        solver.conf_budget(budget)
        t0 = time.time()
        res = solver.solve_limited(assumptions=[] if unit_mode else [v(d, "B")])
        dt = time.time() - t0
        rec.update({"sat": res, "unknown": res is None,
                    "seconds": round(dt, 3),
                    "build_seconds": round(build_s, 3)})
        if res:
            chosen = decode(solver.get_model(), P, h, X)
            cs = frozenset(chosen)
            rec.update({"witness_size": len(chosen),
                        "safe_against_edges": not any(frozenset(q) <= cs for q in edges),
                        "points": chosen})
    finally:
        solver.delete()
    print(json.dumps(rec))
    return 0


def parent(args) -> int:
    out_path = Path(args.output)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    t_build = time.time()
    if args.cnf_cache and Path(args.cnf_cache).exists():
        blob = pickle.loads(Path(args.cnf_cache).read_bytes())
        build_src = f"cached:{args.cnf_cache}"
    else:
        gen = args.gen or str(Path(os.environ["TEMP"]) / "forbidden_edges.exe")
        edges = run_gen(gen, P)
        clauses, nv, kept = build(P, edges, X, C, E)
        blob = {"edges": edges, "clauses": clauses, "nv": nv, "kept": kept}
        CACHE.write_bytes(pickle.dumps(blob, protocol=5))
        build_src = "build()"
    build_s = time.time() - t_build
    edges = blob["edges"]
    nv, kept = blob["nv"], blob["kept"]
    print(f"class vars={nv} clauses={len(blob['clauses'])} kept_edges={kept} "
          f"build={build_s:.1f}s ({build_src})", flush=True)

    solvers = [s for s in args.solvers.split(",") if s]
    doc = {"p": P, "size": SIZE, "class": [X, C, E], "budget": BUDGET,
           "vars": nv, "clauses": len(blob["clauses"]), "kept_edges": kept,
           "build_seconds": round(build_s, 1), "build_source": build_src,
           "device_timeout": args.device, "caps": args.caps,
           "deadline": args.deadline, "jobs": args.jobs,
           "solvers": solvers, "records": []}

    if args.resume and out_path.exists():
        old = json.loads(out_path.read_text(encoding="utf-8"))
        doc["records"] = old.get("records", [])

    def flush() -> None:
        out_path.write_text(json.dumps(doc, indent=1) + "\n",
                            encoding="utf-8", newline="\n")

    flush()
    start = time.time()
    lock = threading.Lock()
    ds = [int(x) for x in args.ds.split(",") if x]
    caps = {}
    for part in args.caps.split(","):
        if part.strip():
            k, val = part.split(":")
            caps[int(k)] = float(val)

    def run_query(solver_name: str, d: int) -> dict:
        rec = {"solver": solver_name, "d": d}
        left = args.deadline - (time.time() - start)
        if left <= 5:
            rec.update({"verdict": "skipped", "reason": "global deadline",
                        "seconds": 0.0})
        else:
            cap = min(args.device, caps.get(d, args.device), left)
            cmd = [sys.executable, __file__, "--worker-run",
                   "--worker-solver", solver_name, "--worker-d", str(d),
                   "--worker-cache", str(CACHE), "--worker-budget", str(BUDGET)]
            t0 = time.time()
            try:
                proc = subprocess.run(cmd, capture_output=True, text=True,
                                      timeout=cap, stdin=subprocess.DEVNULL)
                dt = time.time() - t0
                lines = [ln for ln in proc.stdout.splitlines() if ln.startswith("{")]
                if proc.returncode != 0 or not lines:
                    rec.update({"verdict": "error", "seconds": round(dt, 3),
                                "stderr": (proc.stderr or "")[-500:]})
                else:
                    got = json.loads(lines[-1])
                    rec.update(got)
                    rec["verdict"] = ("sat" if got.get("sat") else
                                      "unknown" if got.get("unknown") else "unsat")
                    rec["seconds"] = round(dt, 3)
            except subprocess.TimeoutExpired:
                rec.update({"verdict": "timeout", "seconds": round(cap, 3),
                            "reason": f"wall cap {cap:.0f}s (conflict budget "
                                      f"{BUDGET} not reached)"})
        with lock:
            doc["records"].append(rec)
            flush()
            print(f"  {solver_name} d={d} {rec['verdict']} "
                  f"{rec.get('seconds')}s", flush=True)
            if rec["verdict"] == "sat":
                print(f"*** SAT {solver_name} d={d} *** {rec.get('points')}",
                      flush=True)
        return rec

    # d-major so cheap d are done before expensive ones if the deadline bites
    done_keys = {(r.get("solver"), r.get("d")) for r in doc["records"]}
    jobs = [q for q in ((_s, _d) for _d in ds for _s in solvers)
            if q not in done_keys]
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        list(pool.map(lambda q: run_query(*q), jobs))
    doc["elapsed"] = round(time.time() - start, 1)
    flush()
    print(f"wrote {out_path} ({len(doc['records'])} records, "
          f"{doc['elapsed']}s)", flush=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--solvers", default=",".join(ASSUMP_SOLVERS[:4] + UNIT_SOLVERS))
    ap.add_argument("--ds", default=",".join(map(str, DS)))
    ap.add_argument("--caps", default="",
                    help='per-d wall caps, e.g. "1:60,851:300"')
    ap.add_argument("--resume", action="store_true",
                    help="keep already recorded (solver, d) queries")
    ap.add_argument("--jobs", type=int, default=2,
                    help="parallel query subprocesses")
    ap.add_argument("--device", type=float, default=120.0,
                    help="per-query wall cap (seconds)")
    ap.add_argument("--deadline", type=float, default=900.0,
                    help="global wall budget for all queries (seconds)")
    ap.add_argument("--gen", default=None)
    ap.add_argument("--cnf-cache", default=None)
    ap.add_argument("--output", default=str(HERE / "output" / "w14-cross-solver.json"))
    ap.add_argument("--worker-run", action="store_true", help=argparse.SUPPRESS)
    ap.add_argument("--worker-solver", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--worker-d", type=int, default=None, help=argparse.SUPPRESS)
    ap.add_argument("--worker-cache", default=None, help=argparse.SUPPRESS)
    ap.add_argument("--worker-budget", type=int, default=BUDGET, help=argparse.SUPPRESS)
    args = ap.parse_args()
    if args.worker_run:
        return worker(args.worker_solver, args.worker_d,
                      Path(args.worker_cache), args.worker_budget)
    return parent(args)


if __name__ == "__main__":
    raise SystemExit(main())
