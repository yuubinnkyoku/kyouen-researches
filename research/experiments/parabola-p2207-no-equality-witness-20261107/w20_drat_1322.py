"""W20: DRAT receipts for the remaining p=2647 size-1322 shape classes.

The class CNF is built by ``search_shape_class.build`` (imported, never executed
as a script, so its receipts are not touched).  Each class is solved by a
proof-logging CaDiCaL (pysat Cadical195) and the proof is checked by the
independent incremental RUP/RAT checker used in the p=2207 audits.

Every stage is written to its own file so an interrupted run resumes:
  init.json   - CNF, encoding and input hashes
  solver.json - proof hash, solver statistics/status
  audit.json  - independent checker verdict

Usage:
  python w20_drat_1322.py --class 0,1,2 [--solve-timeout 3600]
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from search_shape_class import build  # noqa: E402

EDGE_SOURCE = HERE.parent/"parabola-hplus1-drat-20261109/input/verified_edges.txt.gz"
EDGE_RECEIPT = HERE.parent/"parabola-hplus1-drat-20261109/input/geometry.json"
CHECKER_SOURCE = HERE/"drat_check_incremental.cpp"
CHECKER_SHA = "34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b"
OUTPUT = HERE/"output/w20-drat-1322"
P = 2647


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2)+"\n", encoding="utf-8", newline="\n")


def save_gz(path: Path, raw: bytes) -> None:
    with path.open("wb") as stream, gzip.GzipFile(filename="", fileobj=stream, mode="wb", mtime=0) as zipped:
        zipped.write(raw)


def bounded(command, timeout, **kwargs):
    started = time.monotonic()
    try:
        run = subprocess.run(command, timeout=timeout, capture_output=True, text=True, **kwargs)
        return {"returncode": run.returncode, "stdout": run.stdout, "stderr": run.stderr,
                "seconds": time.monotonic()-started, "timed_out": False}
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        return {"returncode": None, "stdout": decoded(exc.stdout), "stderr": decoded(exc.stderr),
                "seconds": time.monotonic()-started, "timed_out": True}


def load_edges():
    raw = gzip.decompress(EDGE_SOURCE.read_bytes())
    receipt = json.loads(EDGE_RECEIPT.read_text())
    assert receipt["returncode"] == 0 and sha(raw) == receipt["edge_input_sha256"]
    rows = raw.decode("ascii").splitlines()
    p, count = map(int, rows[0].split())
    assert p == P and count == len(rows)-1
    return raw, [tuple(map(int, line.split())) for line in rows[1:]]


def dimacs(clauses, nv):
    return (f"p cnf {nv} {len(clauses)}\n"+"".join(
        " ".join(map(str, clause))+" 0\n" for clause in clauses)).encode("ascii")


PROCEDURE = {
    "cnf": "search_shape_class.build(p=2647, edges, x, c, e): one clause "
           "B|N|L|H per pair, pairwise exclusivity, CardEnc.equals(both, c) and "
           "CardEnc.equals(none, e) over SeqCounter, t-auxiliary linking, and one "
           "negative clause per supplied forbidden quadruple; written as DIMACS",
    "edges": "parabola-hplus1-drat-20261109/input/verified_edges.txt.gz, whose "
             "geometry.json receipt records VERIFIED_EDGES 2647 53886 from the exact "
             "integer verifier; every supplied edge is forbidden, completeness not claimed",
    "solve": "pysat Cadical195(with_proof=True).solve_limited() with conflict budget; "
             "proof lines written verbatim to proof.drat.gz (gzip, mtime=0)",
    "check": "g++ -O2 -std=c++17 drat_check_incremental.cpp, then "
             "drat_check_incremental <input.cnf> <proof.drat>; VERIFIED on stdout and "
             "exit code 0 required, with an empty clause derived by RUP",
}


def write_index() -> int:
    records = []
    for directory in sorted(OUTPUT.glob("class-*")):
        record = {"class": [int(v) for v in directory.name.split("-")[1]],
                  "directory": directory.name}
        for name in ("init.json", "solver.json", "audit.json",
                     "input.cnf.gz", "proof.drat.gz"):
            path = directory/name
            record[name] = ({"sha256": sha(path.read_bytes()), "bytes": path.stat().st_size}
                            if path.exists() else None)
        for name in ("input.cnf.gz", "proof.drat.gz"):
            item = record[name]
            if item is not None:
                item["uncompressed_sha256"] = sha(gzip.decompress(
                    (directory/name).read_bytes()))
                item["uncompressed_bytes"] = len(gzip.decompress(
                    (directory/name).read_bytes()))
        for name in ("init.json", "solver.json", "audit.json"):
            item = record[name]
            if item is not None:
                item["content"] = json.loads((directory/name).read_text())
        audit = record["audit.json"]
        record["status"] = ("VERIFIED" if audit is not None
                            and audit["content"].get("verified") is True else
                            "PROOF_UNCHECKED" if record["proof.drat.gz"] is not None
                            else "NO_PROOF")
        records.append(record)
    index = {"p": P, "h": (P-1)//2, "target_size": 1322,
             "procedure": PROCEDURE,
             "generator_sha256": sha(Path(__file__).read_bytes()),
             "builder_source_sha256": sha((HERE/"search_shape_class.py").read_bytes()),
             "checker_source_sha256": CHECKER_SHA,
             "classes": records}
    save(OUTPUT/"index.json", index)
    for record in records:
        print(f"class={record['class']} status={record['status']}", flush=True)
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--class", dest="shape_class", help="x,c,e")
    ap.add_argument("--index-only", action="store_true")
    ap.add_argument("--solve-timeout", type=float, default=3600)
    ap.add_argument("--check-timeout", type=float, default=3600)
    ap.add_argument("--budget", type=int, default=200_000_000)
    ap.add_argument("--recheck", action="store_true")
    args = ap.parse_args()
    x, c, e = (int(v) for v in args.shape_class.split(","))
    out = OUTPUT/f"class-{x}{c}{e}"
    out.mkdir(parents=True, exist_ok=True)

    raw_edges, edges = load_edges()
    clauses, nv, kept = build(P, edges, x, c, e)
    raw_cnf = dimacs(clauses, nv)
    save_gz(out/"input.cnf.gz", raw_cnf)
    init = {"p": P, "h": (P-1)//2, "target_size": 1322, "class": [x, c, e],
            "variables": nv, "clauses": len(clauses), "kept_edges": kept,
            "encoded_edges": len(edges),
            "input_sha256": sha(raw_cnf), "edge_input_sha256": sha(raw_edges),
            "builder": "search_shape_class.build",
            "builder_source_sha256": sha((HERE/"search_shape_class.py").read_bytes()),
            "generator_source_sha256": sha(Path(__file__).read_bytes())}
    save(out/"init.json", init)
    print(f"class={x},{c},{e} vars={nv} clauses={len(clauses)} kept={kept}", flush=True)

    if not (out/"solver.json").exists():
        started = time.monotonic()
        with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
            solver.conf_budget(args.budget)
            answer = solver.solve_limited()
            proof = solver.get_proof() if answer is False else None
            stats = solver.accum_stats()
        solver_record = dict(init, solve_seconds=time.monotonic()-started,
                             conflict_budget=args.budget, statistics=stats,
                             solver_status=("SAT" if answer is True else
                                            "SOLVER_UNSAT" if answer is False else "UNKNOWN"))
        if proof:
            data = ("\n".join(proof)+"\n").encode("ascii")
            save_gz(out/"proof.drat.gz", data)
            solver_record.update(proof_sha256=sha(data), proof_lines=len(proof))
        save(out/"solver.json", solver_record)
        print(f"class={x},{c},{e} status={solver_record['solver_status']} "
              f"seconds={solver_record['solve_seconds']:.1f} proof_lines={len(proof or [])}", flush=True)

    solver_record = json.loads((out/"solver.json").read_text())
    if solver_record["solver_status"] != "SOLVER_UNSAT" or not (out/"proof.drat.gz").exists():
        print(f"class={x},{c},{e} NO_PROOF status={solver_record['solver_status']}", flush=True)
        return 0
    assert sha(CHECKER_SOURCE.read_bytes()) == CHECKER_SHA
    proof = gzip.decompress((out/"proof.drat.gz").read_bytes())
    assert sha(raw_cnf) == solver_record["input_sha256"]
    assert sha(proof) == solver_record["proof_sha256"]
    if (out/"audit.json").exists() and not args.recheck:
        old = json.loads((out/"audit.json").read_text())
        if (old.get("verified") is True and old.get("input_sha256") == sha(raw_cnf)
                and old.get("proof_sha256") == sha(proof)
                and old.get("checker_source_sha256") == CHECKER_SHA):
            print(f"class={x},{c},{e} VERIFIED (saved receipt)", flush=True)
            return 0

    checker = Path(tempfile.gettempdir())/f"w20-drat-{CHECKER_SHA[:16]}.exe"
    binary_sha = None
    if not checker.exists():
        subprocess.run(["g++", "-O2", "-std=c++17", str(CHECKER_SOURCE), "-o", str(checker)],
                       check=True, timeout=120)
    binary_sha = sha(checker.read_bytes())
    with tempfile.TemporaryDirectory(prefix=f"w20-{x}{c}{e}-", dir=out) as temporary:
        temporary = Path(temporary)
        (temporary/"input.cnf").write_bytes(raw_cnf)
        (temporary/"proof.drat").write_bytes(proof)
        run = bounded([str(checker), str(temporary/"input.cnf"), str(temporary/"proof.drat")],
                      args.check_timeout)
    lines = run["stdout"].splitlines()
    verified = run["returncode"] == 0 and bool(lines) and lines[-1] == "VERIFIED"
    run.update(verified=verified, p=P, target_size=1322, shape_class=[x, c, e],
               checker_source_sha256=CHECKER_SHA, checker_binary_sha256=binary_sha,
               input_sha256=sha(raw_cnf), proof_sha256=sha(proof),
               proof_lines=solver_record["proof_lines"])
    save(out/"audit.json", run)
    print(f"class={x},{c},{e} verified={verified} check_seconds={run['seconds']:.1f} "
          f"proof_lines={solver_record['proof_lines']}", flush=True)
    return 0 if verified else 1


if __name__ == "__main__":
    raise SystemExit(main())
