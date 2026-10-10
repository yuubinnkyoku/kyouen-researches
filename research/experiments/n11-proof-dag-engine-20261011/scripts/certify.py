"""Run one cold exact solver query, then turn its decisive result into a DAG.

UNKNOWN, solver timeout, proof-budget exhaustion, and result mismatch all
fail closed: no certificate is emitted. The independent proof search expands
positions from geometry and does not consume solver TT/cache leaves.
"""
from __future__ import annotations

import argparse
import csv
import ctypes
import gzip
import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

from dag_builder import (ProofLimitExceeded, ProofTimeExceeded,
                         build_certificate)
from dag_verifier import verify_certificate
from trace_to_certificate import trace_to_certificate

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, mask_from_key  # noqa: E402


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dump_json(path: Path, value) -> bytes:
    payload = (json.dumps(value, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False) + "\n").encode("utf-8")
    path.write_bytes(payload)
    return payload


def process_peak_rss(proc) -> int | None:
    if os.name == "nt":
        class Counters(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("faults", ctypes.c_ulong)] + [
                (name, ctypes.c_size_t) for name in
                ("peak_rss", "rss", "peak_pool_paged", "pool_paged",
                 "peak_pool_nonpaged", "pool_nonpaged", "pagefile", "peak_pagefile")]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        fn = ctypes.windll.psapi.GetProcessMemoryInfo
        fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
        if fn(int(proc._handle), ctypes.byref(counters), counters.cb):
            return int(counters.peak_rss)
    elif Path(f"/proc/{proc.pid}/status").exists():
        for line in Path(f"/proc/{proc.pid}/status").read_text().splitlines():
            if line.startswith("VmHWM:"):
                return int(line.split()[1]) * 1024
    return None


def self_peak_rss() -> int | None:
    if os.name == "nt":
        class Counters(ctypes.Structure):
            _fields_ = [("cb", ctypes.c_ulong), ("faults", ctypes.c_ulong)] + [
                (name, ctypes.c_size_t) for name in
                ("peak_rss", "rss", "peak_pool_paged", "pool_paged",
                 "peak_pool_nonpaged", "pool_nonpaged", "pagefile", "peak_pagefile")]
        counters = Counters()
        counters.cb = ctypes.sizeof(counters)
        fn = ctypes.windll.psapi.GetProcessMemoryInfo
        fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
        handle = ctypes.windll.kernel32.GetCurrentProcess()
        if fn(handle, ctypes.byref(counters), counters.cb):
            return int(counters.peak_rss)
    else:
        try:
            import resource
            value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            return int(value * (1024 if platform.system() != "Darwin" else 1))
        except (ImportError, AttributeError, OSError):
            pass
    return None


def read_solver_row(path: Path):
    rows = []
    with path.open("r", encoding="utf-8", newline="") as f:
        for row in csv.reader(f):
            if row and row[0] == "replay":
                rows.append(row)
    if len(rows) != 1 or len(rows[0]) != 11:
        raise ValueError("solver did not emit exactly one well-formed replay row")
    row = rows[0]
    return dict(stones=int(row[2]), legal=int(row[3]), is_or=int(row[4]),
                budget=int(row[5]), verdict=int(row[6]), nodes=int(row[7]),
                reported_seconds=int(row[8]), key_lo=int(row[9]), key_hi=int(row[10]))


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--solver", required=True, type=Path)
    ap.add_argument("--n", type=int, default=11)
    ap.add_argument("--root-lo", required=True, type=int)
    ap.add_argument("--root-hi", required=True, type=int)
    ap.add_argument("--solver-budget", type=int, default=100_000)
    ap.add_argument("--solver-memo-power", type=int, default=22)
    ap.add_argument("--solver-order", choices=("count-asc", "count-desc", "key"), default="count-asc")
    ap.add_argument("--proof-order", choices=("count-asc", "count-desc", "key"), default="count-asc")
    ap.add_argument("--proof-sharing", choices=("d4", "none"), default="d4")
    ap.add_argument("--proof-limit", type=int, default=1_000_000)
    ap.add_argument("--solver-timeout", type=float, default=180)
    ap.add_argument("--proof-timeout", type=float, default=300)
    ap.add_argument("--native-proof-capture", action="store_true",
                    help="capture exact proof dependencies inside the modified C++ solver")
    ap.add_argument("--out-dir", required=True, type=Path)
    args = ap.parse_args(argv)
    pipeline_started = time.monotonic()

    solver = args.solver.resolve()
    out = args.out_dir.resolve()
    if not solver.is_file():
        ap.error(f"solver binary does not exist: {solver}")
    if out.exists():
        ap.error(f"refusing to overwrite output directory: {out}")
    if type(args.n) is not int or not 1 <= args.n <= 11:
        ap.error("--n must be in 1..11")
    if args.solver_budget < 1 or args.proof_limit < 1:
        ap.error("budgets must be positive")

    board = Board(args.n)
    root = mask_from_key(args.root_lo, args.root_hi, args.n)
    root = board.canonical(root)
    legal = board.points(board.legal(root))
    stones = root.bit_count()
    out.mkdir(parents=True)
    inp, raw, log = out / "solver-input.csv", out / "solver-raw.csv", out / "solver.log"
    trace = out / "solver-proof-trace.csv"
    with inp.open("x", encoding="utf-8", newline="") as f:
        csv.writer(f, lineterminator="\n").writerow(
            ["target", 0, stones, root & ((1 << 64) - 1), root >> 64,
             len(legal), 0, int(stones % 2 == 0), 0, 0, 0])

    solver_order = {"count-asc": "count", "count-desc": "countd", "key": "key"}[args.solver_order]
    command = [str(solver), f"--n={args.n}", f"--memo={args.solver_memo_power}",
               f"--exact-replay={inp}", f"--only={stones}",
               f"--exact-order={solver_order}",
               f"--exact-replay-budget={args.solver_budget}", f"--csv={raw}"]
    if args.native_proof_capture:
        command.append(f"--proof-dag={trace}")
    start = time.monotonic()
    peak = 0
    timed_out = False
    with log.open("x", encoding="utf-8") as log_file:
        proc = subprocess.Popen(command, stdout=log_file, stderr=subprocess.STDOUT)
        while proc.poll() is None:
            peak = max(peak, process_peak_rss(proc) or 0)
            if time.monotonic() - start > args.solver_timeout:
                proc.kill()
                proc.wait()
                timed_out = True
                break
            time.sleep(0.05)
    solver_wall = time.monotonic() - start
    solver_run = dict(command=command, exit_code=proc.returncode,
                      wall_seconds=solver_wall, peak_rss_bytes=peak or None,
                      timed_out=timed_out, budget=args.solver_budget,
                      order=args.solver_order)
    common = dict(n=args.n, root_mask=str(root), stones=stones,
                  proposition="original_first_player_wins", solver=solver_run,
                  solver_source_sha256=sha256(ROOT / "cpp/solvers/kyouen_dfpn_root.cpp"),
                  residual_header_sha256=sha256(ROOT / "cpp/solvers/kyouen_residual_micro.hpp"),
                  solver_binary=str(solver), solver_binary_sha256=sha256(solver),
                  solver_input_sha256=sha256(inp),
                  solver_raw_sha256=sha256(raw) if raw.exists() else None,
                  solver_log_sha256=sha256(log),
                  solver_proof_trace_sha256=sha256(trace) if trace.exists() else None,
                  native_proof_capture=args.native_proof_capture)
    if timed_out or proc.returncode != 0 or not raw.exists():
        run = common | dict(status="solver_failed_or_timed_out", certificate=None)
        dump_json(out / "run.json", run)
        return 2

    try:
        result = read_solver_row(raw)
    except Exception as exc:
        dump_json(out / "run.json", common | dict(status="invalid_solver_output",
                                                   error=str(exc), certificate=None))
        return 2
    if (result["stones"], result["key_lo"], result["key_hi"]) != (
            stones, root & ((1 << 64) - 1), root >> 64):
        dump_json(out / "run.json", common | dict(status="solver_root_mismatch",
                                                   solver_result=result, certificate=None))
        return 2
    if result["verdict"] not in (1, 2):
        dump_json(out / "run.json", common | dict(status="solver_unknown_or_cutoff",
                                                   solver_result=result, certificate=None))
        return 3

    proof_started = time.monotonic()
    if args.native_proof_capture:
        if not trace.exists():
            dump_json(out / "run.json", common | dict(status="missing_proof_trace",
                                                       solver_result=result, certificate=None))
            return 4
        try:
            certificate, proof_stats = trace_to_certificate(trace, args.n, root, result["verdict"])
        except Exception as exc:
            dump_json(out / "run.json", common | dict(status="invalid_proof_trace",
                                                       solver_result=result, proof_error=str(exc),
                                                       certificate=None))
            return 4
    else:
        try:
            certificate, proof_stats = build_certificate(
                args.n, root, node_limit=args.proof_limit, order=args.proof_order,
                state_sharing=args.proof_sharing, timeout_seconds=args.proof_timeout)
        except (ProofLimitExceeded, ProofTimeExceeded) as exc:
            dump_json(out / "run.json", common | dict(status="proof_incomplete",
                                                       solver_result=result, proof_error=str(exc),
                                                       certificate=None))
            return 4
    proof_wall = time.monotonic() - proof_started
    verification_started = time.monotonic()
    verification = verify_certificate(certificate)
    verification_wall = time.monotonic() - verification_started
    if verification["verdict"] != result["verdict"]:
        dump_json(out / "run.json", common | dict(status="solver_proof_disagreement",
                                                   solver_result=result, verification=verification,
                                                   certificate=None))
        return 5

    cert_path = out / "proof-dag.json.gz"
    payload = (json.dumps(certificate, sort_keys=True, separators=(",", ":"),
                          ensure_ascii=False) + "\n").encode("utf-8")
    with cert_path.open("xb") as f:
        with gzip.GzipFile(fileobj=f, mode="wb", filename="", mtime=0) as gz:
            gz.write(payload)
    verifier_path = out / "verification.json"
    dump_json(verifier_path, verification)
    run = common | dict(status="verified", solver_result=result,
                        proof_generation=dict(mode=("native-solver-trace" if args.native_proof_capture else "independent-research"),
                                              order=(args.solver_order if args.native_proof_capture else args.proof_order),
                                              state_sharing=("solver-canonical-TT" if args.native_proof_capture else args.proof_sharing),
                                              node_limit=(args.solver_budget if args.native_proof_capture else args.proof_limit),
                                              conversion_seconds=proof_wall,
                                              capture_inside_solver=args.native_proof_capture,
                                              peak_rss_bytes=(solver_run["peak_rss_bytes"] if args.native_proof_capture else self_peak_rss()),
                                              stats=proof_stats),
                        verification=verification,
                        verification_seconds=verification_wall,
                        pipeline_wall_seconds=time.monotonic() - pipeline_started,
                        certificate=dict(path=cert_path.name,
                                         sha256=sha256(cert_path),
                                         compressed_bytes=cert_path.stat().st_size,
                                         json_bytes=len(payload)))
    dump_json(out / "run.json", run)
    source_paths = [Path(__file__), Path(__file__).with_name("dag_builder.py"),
                    Path(__file__).with_name("dag_verifier.py"),
                    Path(__file__).with_name("trace_to_certificate.py"),
                    ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py",
                    ROOT / "cpp/solvers/kyouen_dfpn_root.cpp",
                    ROOT / "cpp/solvers/kyouen_residual_micro.hpp"]
    artifacts = [inp, raw, log, cert_path, verifier_path, out / "run.json"]
    if trace.exists():
        artifacts.append(trace)
    manifest = dict(schema="n11-proof-dag-artifact-manifest-v1",
                    files=[dict(path=str(p.relative_to(ROOT)) if p.is_relative_to(ROOT) else str(p),
                                bytes=p.stat().st_size, sha256=sha256(p))
                           for p in artifacts + source_paths])
    dump_json(out / "artifact-manifest.json", manifest)
    print(json.dumps(dict(status="verified", verdict=result["verdict"],
                          solver_nodes=result["nodes"], solver_seconds=solver_wall,
                          proof_nodes=verification["nodes"], proof_seconds=proof_wall,
                          certificate_bytes=cert_path.stat().st_size,
                          output=str(out)), sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
