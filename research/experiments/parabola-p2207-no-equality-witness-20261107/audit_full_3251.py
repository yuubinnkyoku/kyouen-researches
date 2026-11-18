"""Resumable DRAT audit driver for p=3251, all d=1..1625 (W41, adapts audit_full_2207.py
per research/log/2026-11-17-p3251-full-audit-design-omp.md; the p=2207 driver is untouched).

Per d: generate the CNF with ``clauses_for_pair(3251, edges, d)``, get a DRAT proof
(main path: pysat Cadical195 with_proof; fallback: native CaDiCaL writing the proof
straight to disk), gzip the proof, check with drat-trim (main checker), and append an
atomic receipt.  A d that already has a VERIFIED receipt (with matching proof hash and
an existing proof.drat.gz) is skipped, so a restart or a re-run loses at most one d.

Layout (all under the experiment output dir):

  output/drat_trim_audit_full_3251_<checker_sha16>.json   aggregate receipts (atomic)
  output/p3251-drat-full/d<d>/input.cnf.gz                CNF (DIMACS, mtime-free gzip)
  output/p3251-drat-full/d<d>/proof.drat.gz               proof (text DRAT, mtime-free gzip)
  output/p3251-drat-full/d<d>/receipt.json                per-d receipt (atomic)
  output/p3251-drat-full/d<d>/drat-trim.log               checker stdout/stderr
  output/p3251-drat-full/progress.log                     append-only progress
  output/p3251-drat-full/unknown.json                     d left undecided (no receipt)

Usage:
  audit_full_3251.py --ds 21-25 [--wall-budget 2400] [--budgets 5000000,20000000,100000000]
                     [--native-ds 21,22] [--mem-avail-floor-mib 1536]
                     [--cross-check-ds 21] [--recheck]

Exit codes: 0 = ran to completion (or wall budget hit), 3 = SAT found (counterexample),
4 = at least one UNKNOWN recorded, 1 = usage/setup error.

This module needs python-sat (pysat); run it as
  uv run --locked --with python-sat==1.9.dev21 python audit_full_3251.py ...
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "research/experiments/structural-lemmas-2026-10-02/checks"))
sys.path.insert(0, str(HERE))
from parabola_half_bound import clauses_for_pair  # noqa: E402

P = 3251
H = (P - 1) // 2
EDGES_SHA = "11c8966a75615b3cd92b719cae55c2babfc0920e5adceedd35f5c88538d6fd0f"
CHECKER_SOURCE = Path("/home/hatch/workspace/kyouen-omp/tasks/drat-trim-src/drat-trim.c")
CHECKER_BIN = Path("/home/hatch/workspace/kyouen-omp/tasks/drat-trim-src/drat-trim")
CHECKER_BIN_SHA = "92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a"
CADICAL = Path("/home/hatch/workspace/kyouen-omp/bin/cadical-src/build/cadical")
INCREMENTAL_SOURCE = HERE / "drat_check_incremental.cpp"
INCREMENTAL_SHA = "34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b"
OUT = HERE / "output"
FULL = OUT / "p3251-drat-full"
PROGRESS = FULL / "progress.log"
UNKNOWN = FULL / "unknown.json"
RECEIPTS = OUT / f"drat_trim_audit_full_{P}_{CHECKER_BIN_SHA[:16]}.json"

PROCEDURE = {
    "target": "K0708 (p=3251 equality A(p)=(p+3)/2 not attained), full DRAT audit of "
              "the 1,541 unaudited d of 1..1625 following the W38 design "
              "(research/log/2026-11-17-p3251-full-audit-design-omp.md); the other 84 d "
              "already carry drat_check_incremental receipts "
              "(output/drat_audit_full_3251_34249932790a9e9d.json)",
    "cnf": "parabola_half_bound.clauses_for_pair(3251, edges, d); edges from "
           "$TEMP/p3251_drat/edges_3251.txt, sha256 11c8966a... (1,379,766 edges, "
           "p cnf 1625 60266)",
    "solve_main": "pysat Cadical195(bootstrap_with=clauses, with_proof=True).solve_limited() "
                  "with the conflict budget ladder; proof text captured in RAM then written "
                  "to proof.drat (discarded after gzip), gzip mtime=0",
    "solve_fallback": "native CaDiCaL (proof written straight to disk, no RAM retention) "
                      "--binary=false text DRAT, exit 20=UNSAT/10=SAT/0=UNKNOWN; used when "
                      "MemAvailable is below the floor, on MemoryError, or for --native-ds",
    "check": "drat-trim input.cnf proof.drat (text DRAT, no flag); verdict VERIFIED iff "
             "stdout contains 's VERIFIED' and exit code is 0",
    "receipt": "one atomic JSON receipt per d plus an aggregate atomic JSON; a d with a "
               "VERIFIED receipt and a matching proof.drat.gz sha256 is skipped on re-run",
}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def save(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, indent=1, sort_keys=True) + "\n",
                   encoding="utf-8", newline="\n")
    os.replace(tmp, path)


def save_gz(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as stream, gzip.GzipFile(
            filename="", fileobj=stream, mode="wb", mtime=0) as zipped:
        zipped.write(raw)


def log(message: str) -> None:
    FULL.mkdir(parents=True, exist_ok=True)
    line = f"{time.strftime('%Y-%m-%dT%H:%M:%S%z')} {message}\n"
    with PROGRESS.open("a", encoding="utf-8") as handle:
        handle.write(line)
    print(line.rstrip(), flush=True)


def mem_available_mib() -> int:
    try:
        for line in Path("/proc/meminfo").read_text().splitlines():
            if line.startswith("MemAvailable:"):
                return int(line.split()[1]) // 1024
    except OSError:
        pass
    return -1


def parse_ds(text: str) -> list[int]:
    out: list[int] = []
    for part in text.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            a, b = part.split("-", 1)
            out.extend(range(int(a), int(b) + 1))
        else:
            out.append(int(part))
    return sorted(set(out))


def dimacs(clauses, nv: int) -> bytes:
    body = "".join(" ".join(map(str, clause)) + " 0\n" for clause in clauses)
    return (f"p cnf {nv} {len(clauses)}\n" + body).encode("ascii")


def load_receipts() -> tuple[dict, dict]:
    records: dict[int, dict] = {}
    if RECEIPTS.exists():
        data = json.loads(RECEIPTS.read_text(encoding="utf-8"))
        records = {r["d"]: r for r in data.get("records", [])}
    unknowns = {}
    if UNKNOWN.exists():
        unknowns = {r["d"]: r for r in json.loads(UNKNOWN.read_text()).get("records", [])}
    return records, unknowns


def write_receipts(records: dict) -> None:
    save(RECEIPTS, {"p": P, "h": H, "checker": "drat-trim",
                    "checker_source": "https://github.com/marijnheule/drat-trim",
                    "checker_source_commit": "2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
                    "checker_binary_sha256": CHECKER_BIN_SHA,
                    "checker_source_sha256": sha(CHECKER_SOURCE.read_bytes()),
                    "cadical_solver_used_for": "solve only (proofs are checked by drat-trim)",
                    "procedure": PROCEDURE,
                    "records": sorted(records.values(), key=lambda r: r["d"])})


def write_unknowns(unknowns: dict) -> None:
    save(UNKNOWN, {"p": P, "h": H, "records": sorted(unknowns.values(), key=lambda r: r["d"])})


def already_done(record: dict | None, directory: Path) -> bool:
    if not record or record.get("verdict") != "VERIFIED":
        return False
    proof = directory / "proof.drat.gz"
    return proof.exists() and sha(proof.read_bytes()) == record.get("proof_gz_sha256")


def solve_pysat(clauses, budget: int) -> dict:
    from pysat.solvers import Cadical195
    started = time.monotonic()
    solver = Cadical195(bootstrap_with=clauses, with_proof=True)
    solver.conf_budget(budget)
    try:
        answer = solver.solve_limited()
        proof = solver.get_proof() if answer is False else None
        stats = solver.accum_stats()
    finally:
        solver.delete()
    elapsed = time.monotonic() - started
    hwm = None
    try:
        for line in Path("/proc/self/status").read_text().splitlines():
            if line.startswith("VmHWM:"):
                hwm = int(line.split()[1])
    except OSError:
        pass
    return {"solver": "pysat-Cadical195", "solver_status":
            "SAT" if answer is True else "SOLVER_UNSAT" if answer is False else "UNKNOWN",
            "conflict_budget": budget, "conflicts": stats.get("conflicts"),
            "solve_seconds": round(elapsed, 2), "proof": proof,
            "vm_hwm_kib": hwm}


def solve_native(cnf_path: Path, proof_path: Path, budget: int) -> dict:
    started = time.monotonic()
    run = subprocess.run(
        ["setsid", "--wait", str(CADICAL), "--binary=false", "-c", str(budget),
         str(cnf_path), str(proof_path)],
        capture_output=True, text=True)
    elapsed = time.monotonic() - started
    status = {20: "SOLVER_UNSAT", 10: "SAT", 0: "UNKNOWN"}.get(run.returncode,
                                                              f"EXIT_{run.returncode}")
    conflicts = None
    for line in run.stdout.splitlines():
        if "conflicts:" in line:
            digits = [int(t) for t in line.replace(":", " ").split() if t.isdigit()]
            if digits:
                conflicts = max(digits)
    return {"solver": "cadical-native", "solver_status": status, "conflict_budget": budget,
            "conflicts": conflicts, "solve_seconds": round(elapsed, 2),
            "native_exit_code": run.returncode, "proof_path": str(proof_path),
            "solver_stdout_tail": run.stdout.strip().splitlines()[-1:] or None}


def check_drat_trim(cnf_path: Path, proof_path: Path, directory: Path) -> dict:
    started = time.monotonic()
    run = subprocess.run([str(CHECKER_BIN), str(cnf_path), str(proof_path)],
                         capture_output=True, text=True)
    elapsed = time.monotonic() - started
    log_text = run.stdout + ("\n--- stderr ---\n" + run.stderr if run.stderr else "")
    (directory / "drat-trim.log").write_text(log_text, encoding="utf-8", newline="\n")
    verified = run.returncode == 0 and "s VERIFIED" in run.stdout
    return {"checker": "drat-trim", "checker_binary_sha256": CHECKER_BIN_SHA,
            "check_seconds": round(elapsed, 2), "exit_code": run.returncode,
            "verdict": "VERIFIED" if verified else "REJECTED",
            "checker_tail": run.stdout.strip().splitlines()[-1:] or None}


def cross_check_incremental(cnf_path: Path, proof_path: Path, directory: Path) -> dict | None:
    if sha(INCREMENTAL_SOURCE.read_bytes()) != INCREMENTAL_SHA:
        return {"error": "incremental checker source sha mismatch"}
    exe = Path(tempfile.gettempdir()) / f"w31-drat-inc-{INCREMENTAL_SHA[:16]}.exe"
    if not exe.exists():
        subprocess.run(["g++", "-O2", "-std=c++17", str(INCREMENTAL_SOURCE), "-o", str(exe)],
                       check=True)
    started = time.monotonic()
    run = subprocess.run([str(exe), str(cnf_path), str(proof_path)],
                         capture_output=True, text=True)
    lines = run.stdout.strip().splitlines()
    (directory / "drat-inc.log").write_text(run.stdout + run.stderr, encoding="utf-8")
    return {"checker": "drat_check_incremental", "checker_source_sha256": INCREMENTAL_SHA,
            "check_seconds": round(time.monotonic() - started, 2),
            "exit_code": run.returncode,
            "verdict": "VERIFIED" if run.returncode == 0 and lines and lines[-1] == "VERIFIED"
                       else "REJECTED"}


def audit_one(d: int, edges, args, records: dict) -> str:
    directory = FULL / f"d{d}"
    directory.mkdir(parents=True, exist_ok=True)
    clauses = clauses_for_pair(P, edges, d)
    raw_cnf = dimacs(clauses, H)
    input_sha = sha(raw_cnf)
    save_gz(directory / "input.cnf.gz", raw_cnf)
    cnf_path = directory / "input.cnf"
    cnf_path.write_bytes(raw_cnf)

    force_native = d in args.native_ds
    avail = mem_available_mib()
    native = force_native or (0 <= avail < args.mem_avail_floor_mib)
    reason = ("forced by --native-ds" if force_native else
              f"MemAvailable={avail}MiB < floor={args.mem_avail_floor_mib}MiB" if native else
              f"main path (MemAvailable={avail}MiB)")
    log(f"d={d} clauses={len(clauses)} native={native} reason={reason}")

    result: dict | None = None
    proof_bytes: bytes | None = None
    for budget in args.budgets:
        use_native = native
        if use_native:
            proof_path = directory / "proof.drat"
            proof_path.unlink(missing_ok=True)
            outcome = solve_native(cnf_path, proof_path, budget)
            if outcome["solver_status"] == "SOLVER_UNSAT":
                proof_bytes = proof_path.read_bytes()
        else:
            try:
                outcome = solve_pysat(clauses, budget)
            except MemoryError:
                log(f"d={d} pysat MemoryError at budget={budget}; switching to native cadical")
                native = True
                use_native = True
                proof_path = directory / "proof.drat"
                proof_path.unlink(missing_ok=True)
                outcome = solve_native(cnf_path, proof_path, budget)
                if outcome["solver_status"] == "SOLVER_UNSAT":
                    proof_bytes = proof_path.read_bytes()
            else:
                if outcome["solver_status"] == "SOLVER_UNSAT":
                    proof_bytes = ("\n".join(outcome["proof"]) + "\n").encode("ascii")
        result = outcome
        if outcome["solver_status"] == "SOLVER_UNSAT":
            if not use_native:
                (directory / "proof.drat").write_bytes(proof_bytes)
            break
        if outcome["solver_status"] == "SAT":
            break
        # UNKNOWN: fall through to the next (larger) conflict budget
    assert result is not None

    if result["solver_status"] != "SOLVER_UNSAT":
        proof_path = directory / "proof.drat"
        if result["solver_status"] == "SAT":
            proof_path.unlink(missing_ok=True)
            record = {"d": d, "input_sha256": input_sha, "clauses": len(clauses),
                      "verdict": "SAT", **{k: v for k, v in result.items() if k != "proof"}}
            save(directory / "receipt.json", record)
            records[d] = record
            write_receipts(records)
            log(f"d={d} SAT FOUND (counterexample to K0708) solver={result['solver']} "
                f"budget={result['conflict_budget']} -- stopping")
            return "SAT"
        proof_path.unlink(missing_ok=True)
        unknown_record = {"d": d, "input_sha256": input_sha, "clauses": len(clauses),
                          **{k: v for k, v in result.items() if k != "proof"}}
        unknowns = {r["d"]: r for r in
                    (json.loads(UNKNOWN.read_text())["records"] if UNKNOWN.exists() else [])}
        unknowns[d] = unknown_record
        write_unknowns(unknowns)
        log(f"d={d} UNKNOWN after budgets={args.budgets} solver={result['solver']} "
            f"(not receipted; recorded in unknown.json)")
        return "UNKNOWN"

    proof_lines = proof_bytes.count(b"\n")
    save_gz(directory / "proof.drat.gz", proof_bytes)
    proof_path = directory / "proof.drat"
    proof_path.write_bytes(proof_bytes)
    record = {"d": d, "input_sha256": input_sha, "input_bytes": len(raw_cnf),
              "clauses": len(clauses),
              "solver": result["solver"], "solver_status": result["solver_status"],
              "conflict_budget": result["conflict_budget"], "conflicts": result["conflicts"],
              "solve_seconds": result["solve_seconds"], "proof_lines": proof_lines,
              "proof_bytes": len(proof_bytes),
              "proof_sha256": sha(proof_bytes),
              "proof_gz_sha256": sha((directory / "proof.drat.gz").read_bytes()),
              "vm_hwm_kib": result.get("vm_hwm_kib")}
    check = check_drat_trim(cnf_path, proof_path, directory)
    record.update(check)
    if d in args.cross_check_ds:
        record["cross_check"] = cross_check_incremental(cnf_path, proof_path, directory)
    proof_path.unlink(missing_ok=True)
    cnf_path.unlink(missing_ok=True)
    save(directory / "receipt.json", record)
    records[d] = record
    write_receipts(records)
    log(f"d={d} verdict={record['verdict']} solver={record['solver']} "
        f"lines={proof_lines} solve={record['solve_seconds']}s "
        f"check={record['check_seconds']}s budget={record['conflict_budget']}")
    return record["verdict"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--ds", required=True, help="e.g. 2-6 or 2,3,4,5,6")
    ap.add_argument("--budgets", default="5000000,20000000,100000000")
    ap.add_argument("--wall-budget", type=float, default=0.0,
                    help="soft wall seconds; the driver stops between d values (0 = none)")
    ap.add_argument("--native-ds", default="", help="force native cadical for these d")
    ap.add_argument("--mem-avail-floor-mib", type=int, default=1536,
                    help="use native cadical when MemAvailable is below this")
    ap.add_argument("--cross-check-ds", default="", help="also run the incremental checker")
    ap.add_argument("--recheck", action="store_true",
                    help="ignore existing VERIFIED receipts and redo the given d")
    args = ap.parse_args()
    args.budgets = [int(b) for b in args.budgets.split(",") if b.strip()]
    args.native_ds = set(parse_ds(args.native_ds))
    args.cross_check_ds = set(parse_ds(args.cross_check_ds))
    ds = parse_ds(args.ds)

    if sha(CHECKER_BIN.read_bytes()) != CHECKER_BIN_SHA:
        print(f"drat-trim binary sha mismatch at {CHECKER_BIN}", file=sys.stderr)
        return 1

    edges_path = Path(os.environ.get("TEMP", tempfile.gettempdir())) / "p3251_drat/edges_3251.txt"
    if not edges_path.exists():
        print(f"edges file missing: {edges_path}", file=sys.stderr)
        return 1
    raw_edges = edges_path.read_bytes()
    if sha(raw_edges) != EDGES_SHA:
        print(f"edges sha mismatch: {sha(raw_edges)}", file=sys.stderr)
        return 1
    edges = [tuple(map(int, line.split())) for line in raw_edges.decode("ascii").splitlines()]
    FULL.mkdir(parents=True, exist_ok=True)

    records, _ = load_receipts()
    todo = [d for d in ds if args.recheck or not already_done(records.get(d), FULL / f"d{d}")]
    log(f"p={P} h={H} edges={len(edges)} requested={len(ds)} todo={len(todo)} "
        f"budgets={args.budgets} wall_budget={args.wall_budget}")
    started = time.monotonic()
    unknown_seen = 0
    for d in todo:
        if args.wall_budget and time.monotonic() - started > args.wall_budget:
            log(f"wall budget {args.wall_budget}s reached; {len(todo) - todo.index(d)} left"
                f" in this batch")
            break
        outcome = audit_one(d, edges, args, records)
        if outcome == "SAT":
            log("driver stopping: SAT counterexample recorded")
            return 3
        if outcome == "UNKNOWN":
            unknown_seen += 1
    log("driver done")
    return 4 if unknown_seen else 0


if __name__ == "__main__":
    raise SystemExit(main())
