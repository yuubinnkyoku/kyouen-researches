"""Measure the disk-backed verifier's wall time, peak RSS and scratch disk use."""
from __future__ import annotations

import argparse
import ctypes
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-20261011/scripts"))
from certify import process_peak_rss  # noqa: E402


def process_tree_rss_bytes(proc) -> int | None:
    """Sample resident memory for a subprocess and all live descendants.

    On Windows, the venv's python.exe can be a launcher that starts the actual
    interpreter as a child. Sampling only Popen.pid then measures the small
    launcher and misses nearly all verifier memory.
    """
    if os.name != "nt":
        return process_peak_rss(proc)

    DWORD = ctypes.c_ulong
    ULONG_PTR = ctypes.c_size_t

    class ProcessEntry32W(ctypes.Structure):
        _fields_ = [
            ("dwSize", DWORD), ("cntUsage", DWORD), ("th32ProcessID", DWORD),
            ("th32DefaultHeapID", ULONG_PTR), ("th32ModuleID", DWORD),
            ("cntThreads", DWORD), ("th32ParentProcessID", DWORD),
            ("pcPriClassBase", ctypes.c_long), ("dwFlags", DWORD),
            ("szExeFile", ctypes.c_wchar * 260),
        ]

    class ProcessMemoryCounters(ctypes.Structure):
        _fields_ = [("cb", DWORD), ("faults", DWORD)] + [
            (name, ULONG_PTR) for name in
            ("peak_working_set", "working_set", "peak_pool_paged",
             "pool_paged", "peak_pool_nonpaged", "pool_nonpaged",
             "pagefile", "peak_pagefile")
        ]

    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    psapi = ctypes.WinDLL("psapi", use_last_error=True)
    kernel32.CreateToolhelp32Snapshot.argtypes = [DWORD, DWORD]
    kernel32.CreateToolhelp32Snapshot.restype = ctypes.c_void_p
    kernel32.Process32FirstW.argtypes = [ctypes.c_void_p,
                                         ctypes.POINTER(ProcessEntry32W)]
    kernel32.Process32FirstW.restype = ctypes.c_int
    kernel32.Process32NextW.argtypes = [ctypes.c_void_p,
                                        ctypes.POINTER(ProcessEntry32W)]
    kernel32.Process32NextW.restype = ctypes.c_int
    kernel32.OpenProcess.argtypes = [DWORD, ctypes.c_int, DWORD]
    kernel32.OpenProcess.restype = ctypes.c_void_p
    kernel32.CloseHandle.argtypes = [ctypes.c_void_p]
    kernel32.CloseHandle.restype = ctypes.c_int
    psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p,
                                           DWORD]
    psapi.GetProcessMemoryInfo.restype = ctypes.c_int

    snapshot = kernel32.CreateToolhelp32Snapshot(0x00000002, 0)
    invalid_handle = ctypes.c_void_p(-1).value
    if snapshot in (None, invalid_handle):
        return process_peak_rss(proc)
    try:
        entry = ProcessEntry32W()
        entry.dwSize = ctypes.sizeof(entry)
        parents = {}
        if kernel32.Process32FirstW(snapshot, ctypes.byref(entry)):
            while True:
                parents[int(entry.th32ProcessID)] = int(entry.th32ParentProcessID)
                if not kernel32.Process32NextW(snapshot, ctypes.byref(entry)):
                    break
    finally:
        kernel32.CloseHandle(snapshot)

    descendants = {int(proc.pid)}
    changed = True
    while changed:
        changed = False
        for pid, parent in parents.items():
            if parent in descendants and pid not in descendants:
                descendants.add(pid)
                changed = True

    total = 0
    queried = False
    for pid in descendants:
        handle = kernel32.OpenProcess(0x0410, 0, pid)  # QUERY_INFORMATION | VM_READ
        if not handle:
            continue
        try:
            counters = ProcessMemoryCounters()
            counters.cb = ctypes.sizeof(counters)
            if psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters),
                                          counters.cb):
                total += int(counters.working_set)
                queried = True
        finally:
            kernel32.CloseHandle(handle)
    return total if queried else process_peak_rss(proc)


def tree_bytes(path: Path) -> int:
    total = 0
    if path.exists():
        for item in path.rglob("*"):
            if item.is_file():
                try:
                    total += item.stat().st_size
                except FileNotFoundError:
                    pass
    return total


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "compact"), required=True)
    parser.add_argument("--certificate", type=Path, required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--poll-ms", type=int, default=250)
    args = parser.parse_args()
    out_dir = args.out_dir.resolve()
    certificate = args.certificate.resolve()
    if out_dir.exists():
        parser.error(f"refusing to overwrite {out_dir}")
    if not certificate.is_file() or args.poll_ms <= 0:
        parser.error("certificate must exist and poll interval must be positive")
    out_dir.mkdir(parents=True)
    scratch = out_dir / "scratch"
    scratch.mkdir()
    log_path = out_dir / "verifier.log"
    mode = "verify-json" if args.format == "json" else "verify-compact"
    command = [sys.executable,
               str(Path(__file__).with_name("bundle_store.py")),
               "--scratch-dir", str(scratch), mode,
               "--certificate", str(certificate)]
    environment = os.environ.copy()
    environment["TEMP"] = str(scratch)
    environment["TMP"] = str(scratch)
    peak_rss = 0
    peak_scratch = 0
    started = time.monotonic()
    with log_path.open("x", encoding="utf-8") as log:
        process = subprocess.Popen(command, stdout=log, stderr=subprocess.STDOUT,
                                   env=environment)
        while process.poll() is None:
            peak_rss = max(peak_rss, process_tree_rss_bytes(process) or 0)
            peak_scratch = max(peak_scratch, tree_bytes(scratch))
            time.sleep(args.poll_ms / 1000)
        return_code = process.returncode
    elapsed = time.monotonic() - started
    lines = log_path.read_text(encoding="utf-8").splitlines()
    child_receipt = None
    for line in reversed(lines):
        try:
            parsed = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict) and "nodes" in parsed and "edges" in parsed:
            child_receipt = parsed
            break
    result = {
        "schema": "n11-proof-verifier-benchmark-v1",
        "format": args.format,
        "certificate": str(certificate),
        "certificate_bytes": certificate.stat().st_size,
        "returncode": return_code,
        "wall_seconds": round(elapsed, 3),
        "peak_rss_bytes": peak_rss or None,
        "rss_measurement": "sampled_process_tree_working_set",
        "poll_ms": args.poll_ms,
        "peak_scratch_bytes": peak_scratch,
        "verifier_receipt": child_receipt,
        "command": command,
        "log": log_path.name,
    }
    receipt_path = out_dir / "benchmark.json"
    receipt_path.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n",
                            encoding="utf-8")
    print(json.dumps(result, sort_keys=True, separators=(",", ":")), flush=True)
    if return_code != 0 or child_receipt is None:
        raise SystemExit(return_code or 1)


if __name__ == "__main__":
    main()
