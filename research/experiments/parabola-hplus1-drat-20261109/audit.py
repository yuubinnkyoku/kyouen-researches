"""Bounded solver generation and independent DRAT checks, preserving raw evidence."""
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

HERE = Path(__file__).resolve().parent
CHECKER_SOURCE = HERE.parent/"parabola-p2207-no-equality-witness-20261107/drat_check_incremental.cpp"
CHECKER_SHA = "34249932790a9e9d924e9403b75563a2ff051277923301e34ace33e2a5a3650b"


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, indent=2)+"\n", encoding="utf-8", newline="\n")


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--shapes", default="abc")
    ap.add_argument("--solve-timeout", type=float, default=90)
    ap.add_argument("--check-timeout", type=float, default=120)
    ap.add_argument("--recheck", action="store_true")
    args = ap.parse_args()
    assert args.shapes and set(args.shapes) <= set("abc")
    edges = gzip.decompress((HERE/"input/verified_edges.txt.gz").read_bytes())
    edge_receipt = json.loads((HERE/"input/geometry.json").read_text())
    assert edge_receipt["returncode"] == 0 and sha(edges) == edge_receipt["edge_input_sha256"]
    assert edge_receipt["stdout"].strip() == f"VERIFIED_EDGES 2647 {edge_receipt['provided_edges']}"
    assert sha((HERE/"verify_edges.cpp").read_bytes()) == edge_receipt["wrapper_sha256"]
    assert sha((HERE.parent/"parabola-local-repair-20261109/verify_subset.cpp").read_bytes()) == edge_receipt["included_verifier_sha256"]
    assert sha(CHECKER_SOURCE.read_bytes()) == CHECKER_SHA
    checker = Path(tempfile.gettempdir())/f"hplus1-drat-{CHECKER_SHA[:16]}.exe"
    subprocess.run(["g++", "-O2", "-std=c++17", str(CHECKER_SOURCE), "-o", str(checker)], check=True, timeout=60)
    binary_sha = sha(checker.read_bytes())
    env = os.environ.copy()
    env["PYTHONPATH"] = os.pathsep.join(str(Path(p or os.getcwd()).resolve()) for p in sys.path)
    executable = getattr(sys, "_base_executable", None) or sys.executable
    for shape in args.shapes:
        out = HERE/"output"/f"shape-{shape}"
        if not out.exists():
            run = bounded([executable, str(HERE/"generate.py"), "--shape", shape, "--output", str(out)],
                          args.solve_timeout, env=env)
            out.mkdir(parents=True, exist_ok=True)
            save(out/"generation.json", run)
            print(f"shape={shape} generation_timeout={run['timed_out']}", flush=True)
        if not (out/"solver.json").exists() or not (out/"proof.drat.gz").exists():
            print(f"shape={shape} NO_PROOF_READY", flush=True)
            continue
        solver = json.loads((out/"solver.json").read_text())
        assert solver["solver_status"] == "SOLVER_UNSAT"
        cnf = gzip.decompress((out/"input.cnf.gz").read_bytes())
        proof = gzip.decompress((out/"proof.drat.gz").read_bytes())
        assert sha(cnf) == solver["input_sha256"] and sha(proof) == solver["proof_sha256"]
        assert solver["edge_input_sha256"] == sha(edges)
        assert solver["encoding_source_sha256"] == sha((HERE/"encoding.py").read_bytes())
        assert solver["generator_source_sha256"] == sha((HERE/"generate.py").read_bytes())
        if (out/"audit.json").exists() and not args.recheck:
            old = json.loads((out/"audit.json").read_text())
            if old.get("verified") is True and old.get("input_sha256") == sha(cnf) and old.get("proof_sha256") == sha(proof) and old.get("checker_source_sha256") == CHECKER_SHA:
                print(f"shape={shape} VERIFIED (saved receipt)", flush=True)
                continue
        with tempfile.TemporaryDirectory(prefix=f"hplus1-{shape}-") as temporary:
            temporary = Path(temporary)
            input_path, proof_path = temporary/"input.cnf", temporary/"proof.drat"
            input_path.write_bytes(cnf)
            proof_path.write_bytes(proof)
            run = bounded([str(checker), str(input_path), str(proof_path)], args.check_timeout)
        lines = run["stdout"].splitlines()
        verified = run["returncode"] == 0 and bool(lines) and lines[-1] == "VERIFIED"
        run.update(verified=verified, shape=shape, p=2647, target_size=1324,
                   checker_source_sha256=CHECKER_SHA, checker_binary_sha256=binary_sha,
                   input_sha256=sha(cnf), proof_sha256=sha(proof), proof_lines=solver["proof_lines"])
        save(out/"audit.json", run)
        print(f"shape={shape} verified={verified} check_seconds={run['seconds']:.1f} proof_lines={solver['proof_lines']}", flush=True)


if __name__ == "__main__":
    main()
