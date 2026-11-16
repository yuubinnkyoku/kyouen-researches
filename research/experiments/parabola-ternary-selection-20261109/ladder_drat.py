"""W28: DRAT receipts for the decided d of the candidate-A budget ladder.

The ladder (research/log/2026-11-13-a2647-candidate-a-ladder-result-omp.md)
resolved 8 d as SOLVER_UNSAT with no DRAT proof saved.  This script re-runs one
d at the same stage (same target, empty bound, conflict budget and phases) that
decided it, but with a proof-logging CaDiCaL (pysat Cadical195), then checks the
proof with drat-trim (the W20 checker).  It imports the CNF construction from
``ternary_general`` so the input is byte-identical to the ladder's input.cnf.gz.

Stages per d directory ``ladder-drat-d<D>-budget<B>``:
  init.json           - CNF, encoding, input hashes, stage metadata
  input.cnf.gz        - the DIMACS CNF (uncompressed bytes hashed in init.json)
  solver.json         - proof hash, solver status/statistics/seconds
  proof.drat.gz       - the DRAT proof (gzip, mtime=0), only when UNSAT
  audit-drat-trim.json - drat-trim verdict
  drat-trim.log       - verbatim drat-trim stdout

Usage:
  TEMP=$HOME/workspace/kyouen-omp/bin \
    uv run --locked --with python-sat==1.9.dev21 \
    python research/experiments/parabola-ternary-selection-20261109/ladder_drat.py \
      --d 1292 --budget 3000000
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

from pysat.card import CardEnc, EncType
from pysat.solvers import Cadical195

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ternary_general as tg  # noqa: E402

OUTPUT = HERE / "output"
P, H = 2647, 1323
TARGET = 1322

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


def build_cnf(d: int):
    """Reproduce the ladder CNF byte-for-byte (see ternary_general.main)."""
    edges = tg.load_edges()
    original = tg.base_clauses(P, d, edges)
    clauses, empty_vars = tg.encode(P, d, original)
    card = CardEnc.atmost(empty_vars, bound=H + 2 - TARGET, top_id=3 * H,
                          encoding=EncType.seqcounter)
    clauses.extend(card.clauses)
    nv = max(3 * H, card.nv)
    dimacs = (f"p cnf {nv} {len(clauses)}\n" + "".join(
        " ".join(map(str, c)) + " 0\n" for c in clauses)).encode("ascii")
    return dimacs, nv, len(clauses), len(original)


def run_drat_trim(input_path: Path, proof_path: Path, timeout: float):
    started = time.monotonic()
    env = {"TEMP": str(Path.home() / "workspace/kyouen-omp/bin")}
    try:
        run = subprocess.run([str(DRAT_TRIM), str(input_path), str(proof_path)],
                             capture_output=True, text=True, timeout=timeout,
                             env={**env, "PATH": "/usr/bin:/bin"})
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
    ap.add_argument("--d", type=int, required=True)
    ap.add_argument("--budget", type=int, required=True)
    ap.add_argument("--check-timeout", type=float, default=7200)
    ap.add_argument("--recheck", action="store_true")
    args = ap.parse_args()
    d = args.d

    out = OUTPUT / f"ladder-drat-d{d}-budget{args.budget}"
    out.mkdir(parents=True, exist_ok=True)

    dimacs, nv, nclauses, base_clauses = build_cnf(d)
    raw = tg.WARM.read_bytes()
    warm = list(map(int, raw.split()))
    save_gz(out / "input.cnf.gz", dimacs)
    init = {"p": P, "d": d, "target": TARGET, "empty_bound": H + 2 - TARGET,
            "conflict_budget": args.budget, "variables": nv, "clauses": nclauses,
            "base_clauses": base_clauses, "encoded_cnf_sha256": sha(dimacs),
            "warm_input_sha256": sha(raw), "solver": "Cadical195",
            "python_sat": __import__("importlib.metadata", fromlist=["version"]).version("python-sat"),
            "worker_source_sha256": sha((HERE / "ternary_general.py").read_bytes()),
            "generator_source_sha256": sha(Path(__file__).read_bytes()),
            "scope": "0 and complete pair d fixed; all other pairs low/high/empty. "
                     "Re-run of the decided ladder stage with a DRAT proof; "
                     "UNSAT restricted to this d."}
    save(out / "init.json", init)
    print(f"d={d} budget={args.budget} vars={nv} clauses={nclauses} "
          f"cnf_sha256={sha(dimacs)[:16]}", flush=True)

    if not (out / "solver.json").exists():
        started = time.monotonic()
        with Cadical195(bootstrap_with=[list(c) for c in _clauses(dimacs)], with_proof=True) as solver:
            solver.set_phases(tg.phases(P, d, warm[2:]))
            solver.conf_budget(args.budget)
            answer = solver.solve_limited()
            proof = solver.get_proof() if answer is False else None
            stats = solver.accum_stats()
        elapsed = time.monotonic() - started
        record = dict(init, solve_seconds=elapsed, statistics=stats,
                      solver_status=("SAT" if answer is True else
                                     "SOLVER_UNSAT" if answer is False else "UNKNOWN"))
        if proof:
            data = ("\n".join(proof) + "\n").encode("ascii")
            save_gz(out / "proof.drat.gz", data)
            record.update(proof_sha256=sha(data), proof_lines=len(proof),
                          proof_bytes=len(data))
        save(out / "solver.json", record)
        print(f"d={d} status={record['solver_status']} seconds={elapsed:.1f} "
              f"conflicts={stats.get('conflicts')} proof_lines={len(proof or [])}", flush=True)

    record = json.loads((out / "solver.json").read_text())
    if record["solver_status"] != "SOLVER_UNSAT" or not (out / "proof.drat.gz").exists():
        print(f"d={d} NO_PROOF status={record['solver_status']}", flush=True)
        return 0

    assert sha(DRAT_TRIM.read_bytes()) == DRAT_TRIM_SHA, "drat-trim binary mismatch"
    proof = gzip.decompress((out / "proof.drat.gz").read_bytes())
    assert sha(dimacs) == record["encoded_cnf_sha256"], "cnf sha mismatch"
    assert sha(proof) == record["proof_sha256"], "proof sha mismatch"

    audit_path = out / "audit-drat-trim.json"
    if audit_path.exists() and not args.recheck:
        old = json.loads(audit_path.read_text())
        if (old.get("verified") is True
                and old.get("input_sha256") == sha(dimacs)
                and old.get("proof_sha256") == sha(proof)
                and old.get("checker_binary_sha256") == DRAT_TRIM_SHA):
            print(f"d={d} VERIFIED (saved receipt)", flush=True)
            return 0

    with tempfile.TemporaryDirectory(prefix=f"w28-{d}-", dir=out) as temporary:
        temporary = Path(temporary)
        (temporary / "input.cnf").write_bytes(dimacs)
        (temporary / "proof.drat").write_bytes(proof)
        result = run_drat_trim(temporary / "input.cnf", temporary / "proof.drat",
                               args.check_timeout)
    (out / "drat-trim.log").write_text(result["stdout"], encoding="utf-8", newline="\n")
    result.update(p=P, target_size=TARGET, d=d, conflict_budget=args.budget,
                  checker_source="https://github.com/marijnheule/drat-trim",
                  checker_source_commit="2e3b2dc0ecf938addbd779d42877b6ed69d9a985",
                  checker_build="gcc drat-trim.c -std=c99 -O2 -o drat-trim",
                  checker_binary_sha256=DRAT_TRIM_SHA,
                  input_sha256=sha(dimacs), proof_sha256=sha(proof),
                  proof_lines=record["proof_lines"])
    save(audit_path, result)
    print(f"d={d} verified={result['verified']} check_seconds={result['seconds']:.1f} "
          f"proof_lines={record['proof_lines']}", flush=True)
    for line in result["stdout"].splitlines():
        if line.strip():
            print("  drat-trim| " + line, flush=True)
    return 0 if result["verified"] else 1


def _clauses(dimacs: bytes):
    for line in dimacs.decode("ascii").split("\n")[1:]:
        if line:
            yield [int(v) for v in line.split()[:-1]]


if __name__ == "__main__":
    raise SystemExit(main())
