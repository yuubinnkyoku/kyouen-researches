"""Verify a DRAT proof for the shape-(c) CNF at size h+1 (the "h+1 stone").

The shape-(c) instance (0, exactly one complete pair, exactly one empty pair,
one element from every other pair) is the only class of size h+1 that survives
at p=2207; its UNSAT for a prime rules out every safe set of size h+1.  This
script turns an external solver's DRAT proof into a checked certificate:

  1. rebuild the CNF from scratch (same construction as search_1104_shape_c.py)
     and compare its SHA-256 with a recorded value when one is supplied;
  2. compile the fixed incremental checker (drat_check_incremental.cpp, K0707)
     if needed;
  3. run the checker on (cnf, proof), gzip the proof on success and write a
     receipt with all hashes.

Usage:
  certify_shape_c_unsat.py --p 3251 --proof D:\\tmp\\shapec\\shape_c_3251.drat
  certify_shape_c_unsat.py --p 3251 --proof proof.drat --expect-cnf-sha256 HEX
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

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "research/experiments/parabola-equality-extension-2143-2500-20261107"))
from edges_gen import run_edges  # noqa: E402
from search_1104_shape_c import build  # noqa: E402

OUT = HERE / "output"
CHECKER_SOURCE = HERE / "drat_check_incremental.cpp"
TMP = Path(tempfile.gettempdir())


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--p", type=int, required=True)
    ap.add_argument("--proof", required=True)
    ap.add_argument("--expect-cnf-sha256", default=None)
    ap.add_argument("--solver", default="")
    ap.add_argument("--checker-exe", default=None,
                    help="prebuilt checker binary (default: compile drat_check_incremental.cpp)")
    ap.add_argument("--checker-source", default="drat_check_incremental.cpp",
                    help="checker source the binary came from (recorded by sha256)")
    ap.add_argument("--no-gzip", action="store_true",
                    help="skip the .drat.gz copy (for proofs too large to commit)")
    args = ap.parse_args()
    p = args.p
    h = (p - 1) // 2
    size = h + 1
    proof = Path(args.proof)
    if not proof.exists():
        raise SystemExit(f"missing proof: {proof}")

    dest = OUT / f"cert-{p}-{size}-shapec"
    dest.mkdir(parents=True, exist_ok=True)
    edges = run_edges(p)
    clauses, nv, kept, trapezoid = build(p, edges)
    cnf = dest / f"a{p}_{size}.cnf"
    with cnf.open("w", encoding="ascii", newline="\n") as f:
        f.write(f"p cnf {nv} {len(clauses)}\n")
        for c in clauses:
            f.write(" ".join(map(str, c)) + " 0\n")
    cnf_sha = sha256(cnf)
    print(f"p={p} size={size} vars={nv} clauses={len(clauses)} kept={kept} "
          f"trapezoid={trapezoid} cnf_sha256={cnf_sha}", flush=True)
    if args.expect_cnf_sha256 and cnf_sha != args.expect_cnf_sha256:
        raise SystemExit(f"CNF mismatch: {cnf_sha} != {args.expect_cnf_sha256}")

    checker = Path(args.checker_exe) if args.checker_exe else TMP / "drat_inc_cert.exe"
    if args.checker_exe and not checker.exists():
        raise SystemExit(f"missing checker executable: {checker}")
    if not checker.exists():
        subprocess.run(["g++", "-O2", "-std=c++17", str(CHECKER_SOURCE), "-o", str(checker)],
                       check=True)
    checker_source = HERE / args.checker_source
    if not checker_source.exists():
        raise SystemExit(f"missing checker source: {checker_source}")
    proof_sha = sha256(proof)
    t0 = time.time()
    chk = subprocess.run([str(checker), str(cnf), str(proof)], capture_output=True, text=True)
    check_s = time.time() - t0
    out = chk.stdout.strip().splitlines()
    verified = chk.returncode == 0 and bool(out) and "VERIFIED" in out[-1]
    record = {
        "p": p, "h": h, "size": size, "shape": "c", "class": [1, 1, 1],
        "vars": nv, "clauses": len(clauses), "kept_edges": kept,
        "trapezoid_edges_dropped": trapezoid,
        "cnf_sha256": cnf_sha, "proof_sha256": proof_sha,
        "proof_lines": sum(1 for _ in proof.open("rb")),
        "proof_bytes": proof.stat().st_size,
        "checker_source_sha256": sha256(checker_source),
        "checker_exe": str(checker),
        "checker_rc": chk.returncode,
        "checker_last_line": out[-1] if out else chk.stderr.strip()[:300],
        "verified": verified,
        "check_seconds": round(check_s, 1),
        "solver": args.solver,
        "conclusion": (f"A({p}) <= {h}" if verified else "NOT VERIFIED"),
    }
    if verified and not args.no_gzip:
        gz = dest / f"a{p}_{size}.drat.gz"
        if not gz.exists():
            with gzip.open(gz, "wb", compresslevel=6) as g:
                with proof.open("rb") as f:
                    for chunk in iter(lambda: f.read(1 << 20), b""):
                        g.write(chunk)
        record["proof_gz_sha256"] = sha256(gz)
        record["proof_gz_bytes"] = gz.stat().st_size
    (dest / "receipt.json").write_text(json.dumps(record, indent=2) + "\n",
                                       encoding="utf-8", newline="\n")
    print(json.dumps(record, indent=2), flush=True)
    return 0 if verified else 1


if __name__ == "__main__":
    raise SystemExit(main())
