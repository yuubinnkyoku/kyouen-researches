"""W33: native-CaDiCaL DRAT receipts for the candidate-A budget-ladder d.

Same receipt shape as `ladder_drat.py` (pysat Cadical195, proof buffered in RAM),
but the proof is written by the native tracer straight to disk.  Input CNF is
rebuilt with `ladder_drat.build_cnf(d)` and checked byte-for-byte against the
ladder receipt directory's `input.cnf.gz`.

Layout (fresh; never reuses a pysat receipt directory):
    output/ladder-drat-native-d<D>-budget<B>/
        init.json           CNF provenance + sha comparison with the ladder receipt
        input.cnf.gz        gzip, mtime=0 (byte-identical to the ladder's copy)
        input.cnf           decompressed DIMACS given to the solver
        phases.txt          warm-start phases, one signed literal per token
        run.log             native solver stdout/stderr
        native-result.json  shim output (exit code, statistics, RSS)
        solver.json         merged receipt (superset of the pysat solver.json)
        proof.drat          binary DRAT streamed by native CaDiCaL (not in RAM)
        proof.drat.gz       gzip of the proof
        drat-trim.log       checker stdout
        audit-drat-trim.json

Memory note for the big stage: drat-trim keeps every traced clause in RAM
(a `long` per proof step plus an `int` per literal), so a multi-GB binary proof
can exceed the 8 GiB VM during verification even though the solve streams fine.
Measured reference: the d=1258 pysat receipt has 262,889,867 proof literals
(1.45 GB ASCII) and verified in 1,564 s here; scale the d=820 estimate from
that ratio before trusting a local verify (see the W33 log).

Resume semantics: native CaDiCaL has no checkpoint.  A run killed mid-solve
leaves no solver.json and is restarted from scratch; the driver only skips a
stage when solver.json already exists, and only skips verification when a
matching VERIFIED audit is present (--recheck forces it).

Usage:
    uv run --locked --with python-sat==1.9.dev21 \
        python research/experiments/parabola-ternary-selection-20261109/ladder_drat_native.py \
        --d 1292 --budget 3000000
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import ladder_drat  # noqa: E402
import ternary_general as tg  # noqa: E402

OUTPUT = HERE / "output"
P, H = 2647, 1323
TARGET = 1322

# Native build used for every receipt (see research/log/2026-11-16-a2647-113-ladder-prep-omp.md).
CADICAL_DIR = Path.home() / "workspace/kyouen-omp/bin/cadical-src"
CADICAL_LIB = CADICAL_DIR / "build/libcadical.a"
CADICAL_BIN = CADICAL_DIR / "build/cadical"
CADICAL_COMMIT = "c60730422e758ef1cebe7aeddf2dda31c996bf04"
CADICAL_BIN_SHA = "26a5daca4f95b2fc4970e735e91fd18031d74e1dcef0f9435ce01c3f8d2fde41"

DRAT_TRIM = Path("/home/hatch/workspace/kyouen-omp/tasks/drat-trim-src/drat-trim")
DRAT_TRIM_SHA = "92f0aa9575ed519d66a99b8b1b3dde6ece4618ae4c202a3a4b200265dda0aa7a"
DRAT_TRIM_COMMIT = "2e3b2dc0ecf938addbd779d42877b6ed69d9a985"

SHIM_SOURCE = HERE / "native_solve.cpp"
SHIM_BUILD = HERE / "output/native-solve"

SCOPE = ("0 and complete pair d fixed; all other pairs low/high/empty. "
         "Re-run of the decided ladder stage with a DRAT proof; "
         "UNSAT restricted to this d.")


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def sha_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8", newline="\n")


def save_gz(path: Path, raw: bytes) -> None:
    with path.open("wb") as stream, gzip.GzipFile(filename="", fileobj=stream,
                                                  mode="wb", mtime=0) as zipped:
        zipped.write(raw)


def build_shim() -> Path:
    """Compile the libcadical shim once; rebuild when the source is newer."""
    SHIM_BUILD.parent.mkdir(parents=True, exist_ok=True)
    if (SHIM_BUILD.exists()
            and SHIM_BUILD.stat().st_mtime >= SHIM_SOURCE.stat().st_mtime):
        return SHIM_BUILD
    if not CADICAL_LIB.exists():
        raise SystemExit(f"missing {CADICAL_LIB}; build CaDiCaL first")
    command = ["g++", "-std=c++17", "-O2", "-DNDEBUG",
               f"-I{CADICAL_DIR / 'src'}", f"-I{CADICAL_DIR / 'build'}",
               str(SHIM_SOURCE), str(CADICAL_LIB), "-o", str(SHIM_BUILD)]
    print("building shim: " + " ".join(command), flush=True)
    run = subprocess.run(command, capture_output=True, text=True)
    if run.returncode != 0:
        raise SystemExit(f"shim build failed:\n{run.stdout}\n{run.stderr}")
    return SHIM_BUILD


def reference_receipt(d: int, budget: int) -> tuple[Path, dict | None]:
    """The pysat ladder receipt this CNF must match, if it exists."""
    out = OUTPUT / f"ladder-drat-d{d}-budget{budget}"
    init = out / "init.json"
    return out, (json.loads(init.read_text()) if init.exists() else None)


def parse_closing_proof(log: str) -> dict:
    """CaDiCaL prints the closing proof step counts; parse the last block."""
    import re
    def last(pattern):
        found = re.findall(pattern, log)
        return int(found[-1].replace(",", "")) if found else None
    return {"added": last(r"DRAT (\d+) added clauses"),
            "deleted": last(r"DRAT (\d+) deleted clauses"),
            "bytes": last(r"DRAT (\d+) bytes")}


def json_stat(log: str, pattern: str):
    """Last integer matching `pattern` in the native solver log."""
    import re
    found = re.findall(pattern, log)
    return found[-1] if found else None


def run_solve(d: int, budget: int, out: Path, shim: Path, phase_literals: list[int],
              cnf_sha: str, clauses: int, base_clauses: int) -> dict:
    record_path = out / "solver.json"
    if record_path.exists():
        print(f"d={d} budget={budget} solver.json present -> skip solve", flush=True)
        return json.loads(record_path.read_text())

    (out / "phases.txt").write_text(
        " ".join(str(lit) for lit in phase_literals) + "\n", encoding="ascii", newline="\n")

    command = [str(shim), "input.cnf", "proof.drat", str(budget),
               "phases.txt", "native-result.json", "witness.txt"]
    print("running: " + " ".join(command) + f"  (in {out})", flush=True)
    started = time.monotonic()
    with (out / "run.log").open("w", encoding="utf-8", newline="\n") as log:
        run = subprocess.run(command, cwd=out, stdout=log, stderr=subprocess.STDOUT)
    elapsed = time.monotonic() - started
    log_text = (out / "run.log").read_text(errors="replace")

    if not (out / "native-result.json").exists():
        tail = "\n".join(log_text.splitlines()[-5:])
        raise SystemExit(f"d={d} native solver produced no result (killed?); "
                         f"last log lines:\n{tail}")
    native = json.loads((out / "native-result.json").read_text())
    status = {10: "SAT", 20: "SOLVER_UNSAT", 0: "UNKNOWN"}.get(
        run.returncode, f"EXIT_{run.returncode}")
    proof = out / "proof.drat"
    proof_bytes = proof.stat().st_size if proof.exists() else 0
    proof_sha = sha_file(proof) if proof.exists() else None
    closing = parse_closing_proof(log_text)

    record = {
        "p": P, "d": d, "target": TARGET, "empty_bound": H + 2 - TARGET,
        "conflict_budget": budget,
        "variables": native["variables"],
        "clauses": int(json_stat(log_text, r"parsed (\d+) clauses")),
        "base_clauses": base_clauses,
        "encoded_cnf_sha256": cnf_sha,
        "solver": "cadical-native",
        "solver_version": native["solver_version"],
        "solver_source_commit": CADICAL_COMMIT,
        "solver_binary_sha256": CADICAL_BIN_SHA,
        "solver_shim_source_sha256": sha(SHIM_SOURCE.read_bytes()),
        "solver_shim_binary_sha256": sha_file(shim),
        "solver_exit_code": native["solver_exit_code"],
        "solver_status": status,
        "wall_seconds": round(elapsed, 3),
        "phase_hints": native["phase_hints"],
        "solve_seconds": native["solve_seconds"],
        "statistics": native["statistics"],
        "max_rss_kb": native["max_rss_kb"],
        "proof_format": "binary-drat",
        "proof_bytes": proof_bytes,
        "proof_sha256": proof_sha,
        "proof_steps": closing,
        "proof_lines": None,
        "scope": SCOPE,
    }
    save(record_path, record)
    print(f"d={d} status={status} exit={run.returncode} real={elapsed:.1f}s "
          f"conflicts={native['statistics']['conflicts']} proof_bytes={proof_bytes}", flush=True)
    return record


def run_verify(d: int, budget: int, out: Path, cnf_sha: str, record: dict,
               check_timeout: float, recheck: bool) -> dict:
    audit_path = out / "audit-drat-trim.json"
    proof = out / "proof.drat"
    if record["solver_status"] != "SOLVER_UNSAT" or not proof.exists():
        raise SystemExit(f"d={d} has no UNSAT proof to verify")

    if not (out / "proof.drat.gz").exists():
        started = time.monotonic()
        with (out / "proof.drat.gz").open("wb") as raw, \
                gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as zipped:
            with proof.open("rb") as source:
                shutil.copyfileobj(source, zipped, 1 << 20)
        print(f"gzip d={d}: {time.monotonic() - started:.1f}s", flush=True)

    proof_gz_sha = sha_file(out / "proof.drat.gz")
    if audit_path.exists() and not recheck:
        old = json.loads(audit_path.read_text())
        if (old.get("verified") is True
                and old.get("input_sha256") == cnf_sha
                and old.get("proof_sha256") == record["proof_sha256"]
                and old.get("proof_gz_sha256") == proof_gz_sha
                and old.get("checker_binary_sha256") == DRAT_TRIM_SHA):
            print(f"d={d} VERIFIED (saved audit)", flush=True)
            return old

    assert sha_file(DRAT_TRIM) == DRAT_TRIM_SHA, "drat-trim binary mismatch"
    env = {"TEMP": str(Path.home() / "workspace/kyouen-omp/bin"), "PATH": "/usr/bin:/bin"}
    started = time.monotonic()
    try:
        run = subprocess.run([str(DRAT_TRIM), "input.cnf", "proof.drat", "-i"],
                             cwd=out, capture_output=True, text=True,
                             timeout=check_timeout, env=env)
        stdout, stderr, rc, timed = run.stdout, run.stderr, run.returncode, False
    except subprocess.TimeoutExpired as exc:
        def decoded(value):
            return value.decode(errors="replace") if isinstance(value, bytes) else value or ""
        stdout, stderr, rc, timed = decoded(exc.stdout), decoded(exc.stderr), None, True
    seconds = time.monotonic() - started
    verified = rc == 0 and any(line.strip() == "s VERIFIED" for line in stdout.splitlines())
    (out / "drat-trim.log").write_text(stdout, encoding="utf-8", newline="\n")

    audit = {
        "checker": "drat-trim",
        "returncode": rc,
        "stdout": stdout,
        "stderr": stderr,
        "seconds": seconds,
        "timed_out": timed,
        "verified": verified,
        "not_verified": [line.strip() for line in stdout.splitlines()
                         if line.strip() in ("s NOT VERIFIED",)
                         or "MEMOUT" in line],
        "p": P,
        "target_size": TARGET,
        "d": d,
        "conflict_budget": budget,
        "checker_source": "https://github.com/marijnheule/drat-trim",
        "checker_source_commit": DRAT_TRIM_COMMIT,
        "checker_build": "gcc drat-trim.c -std=c99 -O2 -o drat-trim",
        "checker_binary_sha256": DRAT_TRIM_SHA,
        "input_sha256": cnf_sha,
        "proof_sha256": record["proof_sha256"],
        "proof_gz_sha256": proof_gz_sha,
        "proof_bytes": record["proof_bytes"],
        "proof_format": "binary-drat",
        "proof_steps": record["proof_steps"],
        "proof_lines": None,
        "log": "drat-trim.log",
    }
    save(audit_path, audit)
    print(f"d={d} verified={verified} check_seconds={seconds:.1f} "
          f"rc={rc} timed_out={timed}", flush=True)
    return audit


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--d", type=int, required=True)
    ap.add_argument("--budget", type=int, required=True)
    ap.add_argument("--check-timeout", type=float, default=7200)
    ap.add_argument("--recheck", action="store_true")
    ap.add_argument("--out-root", type=Path, default=OUTPUT,
                    help="receipt root (default: the experiment output directory)")
    ap.add_argument("--cnf-only", action="store_true",
                    help="write init.json/input.cnf only (identity check; no solve)")
    ap.add_argument("--solve-only", action="store_true")
    ap.add_argument("--verify-only", action="store_true")
    args = ap.parse_args()
    d, budget = args.d, args.budget

    out = args.out_root / f"ladder-drat-native-d{d}-budget{budget}"
    out.mkdir(parents=True, exist_ok=True)

    dimacs, nv, nclauses, base_clauses = ladder_drat.build_cnf(d)
    cnf_sha = sha(dimacs)
    gz = out / "input.cnf.gz"
    if not gz.exists():
        save_gz(gz, dimacs)
    elif sha(gzip.decompress(gz.read_bytes())) != cnf_sha:
        raise SystemExit(f"{gz} does not decompress to the rebuilt CNF")
    if not (out / "input.cnf").exists():
        (out / "input.cnf").write_bytes(dimacs)

    ref_out, ref_init = reference_receipt(d, budget)
    ref_gz = ref_out / "input.cnf.gz"
    ref_gz_sha = sha_file(ref_gz) if ref_gz.exists() else None
    gz_sha = sha_file(gz)
    reference = {
        "path": str(ref_out.relative_to(HERE.parents[2])),
        "present": ref_init is not None,
        "encoded_cnf_sha256": (ref_init or {}).get("encoded_cnf_sha256"),
        "input_cnf_gz_sha256": ref_gz_sha,
        "cnf_sha_match": None if ref_init is None
                         else ref_init.get("encoded_cnf_sha256") == cnf_sha,
        "gz_byte_match": None if ref_gz_sha is None else ref_gz_sha == gz_sha,
    }
    if reference["cnf_sha_match"] is False:
        raise SystemExit(f"rebuilt CNF sha {cnf_sha} != receipt "
                         f"{reference['encoded_cnf_sha256']}")
    if reference["cnf_sha_match"] is None:
        print(f"d={d} budget={budget}: no pysat receipt to compare against "
              f"(cnf_sha256={cnf_sha[:16]})", flush=True)

    warm_raw = tg.WARM.read_bytes()
    phase_literals = tg.phases(P, d, list(map(int, warm_raw.split()))[2:])

    init = {
        "p": P, "d": d, "target": TARGET, "empty_bound": H + 2 - TARGET,
        "conflict_budget": budget, "variables": nv, "clauses": nclauses,
        "base_clauses": base_clauses,
        "encoded_cnf_sha256": cnf_sha,
        "input_cnf_gz_sha256": gz_sha,
        "warm_input_sha256": sha(warm_raw),
        "phase_hints": len(phase_literals),
        "solver": "cadical-native",
        "solver_version": "3.0.1",
        "solver_source_commit": CADICAL_COMMIT,
        "solver_binary_sha256": CADICAL_BIN_SHA,
        "solver_shim_source_sha256": sha(SHIM_SOURCE.read_bytes()),
        "worker_source_sha256": sha((HERE / "ternary_general.py").read_bytes()),
        "generator_source_sha256": sha((HERE / "ladder_drat.py").read_bytes()),
        "cnf_generator": "ladder_drat.build_cnf(d) (same function the pysat receipt used)",
        "reference_receipt": reference,
        "scope": SCOPE,
    }
    if not (out / "init.json").exists():
        save(out / "init.json", init)

    if args.cnf_only:
        print(f"d={d} cnf_sha256={cnf_sha} reference={reference['path']} "
              f"cnf_sha_match={reference['cnf_sha_match']} "
              f"gz_byte_match={reference['gz_byte_match']}", flush=True)
        return 0

    if args.verify_only:
        record = json.loads((out / "solver.json").read_text())
        audit = run_verify(d, budget, out, cnf_sha, record, args.check_timeout, args.recheck)
        return 0 if audit["verified"] else 1

    shim = build_shim()
    record = run_solve(d, budget, out, shim, phase_literals, cnf_sha,
                       nclauses, base_clauses)
    if record["solver_status"] != "SOLVER_UNSAT":
        print(f"d={d} status={record['solver_status']} -> nothing to verify", flush=True)
        return 0
    if args.solve_only:
        return 0
    audit = run_verify(d, budget, out, cnf_sha, record, args.check_timeout, args.recheck)
    return 0 if audit["verified"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
