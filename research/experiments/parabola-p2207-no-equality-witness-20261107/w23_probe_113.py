"""W23: difficulty probe for the last p=2647 size-1322 shape class (1,1,3).

The class CNF is built by ``search_shape_class.build`` (imported, never
executed as a script, so its receipts are not touched).  Unlike W20 this keeps
the (1,1,3) CNF under its own output directory and is reusable by the budget
ladder designed in the W23 log: it takes ``--budget`` and writes every stage to
its own file so an interrupted run resumes.

Stages per budget directory ``class-113-b<budget>``:
  init.json   - CNF, encoding and input hashes
  solver.json - proof hash, solver statistics/status
  proof.drat.gz
  audit-drat-trim.json - drat-trim verdict

Usage:
  python w23_probe_113.py --budget 1000000
  python w23_probe_113.py --budget 10000000 --solve-timeout 7200
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from search_shape_class import build  # noqa: E402

EDGE_SOURCE = HERE.parent / "parabola-hplus1-drat-20261109/input/verified_edges.txt.gz"
EDGE_RECEIPT = HERE.parent / "parabola-hplus1-drat-20261109/input/geometry.json"
OUTPUT = HERE / "output/w23-113-probe"
P = 2647
CLASS = (1, 1, 3)

# drat-trim: https://github.com/marijnheule/drat-trim, commit
# 2e3b2dc0ecf938addbd779d42877b6ed69d9a985, `gcc drat-trim.c -std=c99 -O2 -o drat-trim`
DRAT_TRIM = Path("/home/hatch/workspace/kyouen-omp/tasks/drat-trim-src/drat-trim")
DRAT_TRIM_SHA = "92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a"


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def save_gz(path: Path, raw: bytes) -> None:
    with path.open("wb") as stream, gzip.GzipFile(filename="", fileobj=stream,
                                                  mode="wb", mtime=0) as zipped:
        zipped.write(raw)


def dimacs(clauses, nv):
    return (f"p cnf {nv} {len(clauses)}\n" + "".join(
        " ".join(map(str, clause)) + " 0\n" for clause in clauses)).encode("ascii")


def load_edges():
    raw = gzip.decompress(EDGE_SOURCE.read_bytes())
    receipt = json.loads(EDGE_RECEIPT.read_text())
    assert receipt["returncode"] == 0 and sha(raw) == receipt["edge_input_sha256"]
    rows = raw.decode("ascii").splitlines()
    p, count = map(int, rows[0].split())
    assert p == P and count == len(rows) - 1
    return raw, [tuple(map(int, line.split())) for line in rows[1:]]


def run_drat_trim(input_path: Path, proof_path: Path, timeout: float):
    started = time.monotonic()
    try:
        run = subprocess.run([str(DRAT_TRIM), str(input_path), str(proof_path)],
                             capture_output=True, text=True, timeout=timeout)
        out, err, rc, timed = run.stdout, run.stderr, run.returncode, False
    except subprocess.TimeoutExpired as exc:
        def dec(v):
            return v.decode(errors="replace") if isinstance(v, bytes) else v or ""
        out, err, rc, timed = dec(exc.stdout), dec(exc.stderr), None, True
    lines = out.splitlines()
    verified = rc == 0 and any(l.strip() == "s VERIFIED" for l in lines)
    return {"checker": "drat-trim", "returncode": rc, "stdout": out, "stderr": err,
            "seconds": time.monotonic() - started, "timed_out": timed,
            "verified": verified}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", type=int, default=1_000_000)
    ap.add_argument("--solve-timeout", type=float, default=3600)
    ap.add_argument("--check-timeout", type=float, default=7200)
    ap.add_argument("--recheck", action="store_true")
    args = ap.parse_args()
    x, c, e = CLASS
    out = OUTPUT / f"class-{x}{c}{e}-b{args.budget}"
    out.mkdir(parents=True, exist_ok=True)

    raw_edges, edges = load_edges()
    clauses, nv, kept = build(P, edges, x, c, e)
    raw_cnf = dimacs(clauses, nv)
    save_gz(out / "input.cnf.gz", raw_cnf)
    init = {"p": P, "h": (P - 1) // 2, "target_size": 1322, "class": [x, c, e],
            "variables": nv, "clauses": len(clauses), "kept_edges": kept,
            "encoded_edges": len(edges),
            "input_sha256": sha(raw_cnf), "edge_input_sha256": sha(raw_edges),
            "builder": "search_shape_class.build",
            "builder_source_sha256": sha((HERE / "search_shape_class.py").read_bytes()),
            "generator_source_sha256": sha(Path(__file__).read_bytes())}
    save(out / "init.json", init)
    print(f"class={x},{c},{e} vars={nv} clauses={len(clauses)} kept={kept} "
          f"cnf_sha256={sha(raw_cnf)[:16]}", flush=True)

    if not (out / "solver.json").exists():
        started = time.monotonic()
        timed_out = False
        try:
            with Cadical195(bootstrap_with=clauses, with_proof=True) as solver:
                solver.conf_budget(args.budget)
                answer = solver.solve_limited()
                proof = solver.get_proof() if answer is False else None
                stats = solver.accum_stats()
        except TimeoutError:
            timed_out = True
            answer, proof, stats = None, None, {}
        solve_seconds = time.monotonic() - started
        solver_record = dict(init, solve_seconds=solve_seconds,
                             conflict_budget=args.budget, statistics=stats,
                             solver_status=("SAT" if answer is True else
                                            "SOLVER_UNSAT" if answer is False else "UNKNOWN"),
                             timed_out=timed_out)
        if proof:
            data = ("\n".join(proof) + "\n").encode("ascii")
            save_gz(out / "proof.drat.gz", data)
            solver_record.update(proof_sha256=sha(data), proof_lines=len(proof),
                                 proof_bytes=len(data))
        save(out / "solver.json", solver_record)
        print(f"class={x},{c},{e} status={solver_record['solver_status']} "
              f"seconds={solve_seconds:.1f} proof_lines={len(proof or [])}", flush=True)

    solver_record = json.loads((out / "solver.json").read_text())
    if (solver_record["solver_status"] != "SOLVER_UNSAT"
            or not (out / "proof.drat.gz").exists()):
        print(f"class={x},{c},{e} NO_PROOF status={solver_record['solver_status']}",
              flush=True)
        return 0

    assert sha(DRAT_TRIM.read_bytes()) == DRAT_TRIM_SHA
    proof = gzip.decompress((out / "proof.drat.gz").read_bytes())
    assert sha(raw_cnf) == solver_record["input_sha256"]
    assert sha(proof) == solver_record["proof_sha256"]

    audit_path = out / "audit-drat-trim.json"
    if audit_path.exists() and not args.recheck:
        old = json.loads(audit_path.read_text())
        if (old.get("verified") is True and old.get("input_sha256") == sha(raw_cnf)
                and old.get("proof_sha256") == sha(proof)
                and old.get("checker_binary_sha256") == DRAT_TRIM_SHA):
            print(f"class={x},{c},{e} VERIFIED (saved receipt)", flush=True)
            return 0

    with tempfile.TemporaryDirectory(prefix=f"w23-{x}{c}{e}-", dir=out) as temporary:
        temporary = Path(temporary)
        (temporary / "input.cnf").write_bytes(raw_cnf)
        (temporary / "proof.drat").write_bytes(proof)
        result = run_drat_trim(temporary / "input.cnf", temporary / "proof.drat",
                               args.check_timeout)
    result.update(p=P, target_size=1322, shape_class=[x, c, e],
                  checker_source="https://github.com/marijnheule/drat-trim",
                  checker_source_commit="2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
                  checker_build="gcc drat-trim.c -std=c99 -O2 -o drat-trim",
                  checker_binary_sha256=DRAT_TRIM_SHA,
                  input_sha256=sha(raw_cnf), proof_sha256=sha(proof),
                  proof_lines=solver_record["proof_lines"])
    save(audit_path, result)
    print(f"class={x},{c},{e} verified={result['verified']} "
          f"check_seconds={result['seconds']:.1f} "
          f"proof_lines={solver_record['proof_lines']}", flush=True)
    for line in result["stdout"].splitlines():
        if line.strip():
            print("  drat-trim| " + line, flush=True)
    return 0 if result["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
