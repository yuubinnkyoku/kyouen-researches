#!/usr/bin/env python3
"""Verify a compact terminal strategy and compute its exact predecessor WIN closure.

No verdict cache is trusted. Requires Python 3 and a C++20 compiler.
The temporary decompressed certificate and executable are deleted on exit.
"""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zlib

HERE = Path(__file__).resolve().parent
CERT = HERE / "terminal_s6_60_strategy.b64"
SOURCE = HERE / "verify_terminal_s6_60_closure.cpp"
SHA256 = "debb5464282eb28e6a30496f8728515433d6f9507ffdeeda1eeaf04e3c5d7de4"
EXPECTED = {
    "source_reached": 22364,
    "closure_total_raw": 256561,
    "closure_new_raw": 234197,
    "closure_d4_classes": 256193,
    "new_s6_raw": 6,
    "new_s7_raw": 0,
    "rounds": [83556, 19589, 99467, 7567, 22511, 291, 1216, 0],
}


def main():
    data = zlib.decompress(base64.b64decode(CERT.read_text(encoding="ascii")))
    if len(data) != 14440 or hashlib.sha256(data).hexdigest() != SHA256:
        raise ValueError("source terminal strategy hash/length mismatch")
    with tempfile.TemporaryDirectory() as tmp:
        binary = Path(tmp) / "closure"
        raw = Path(tmp) / "strategy.bin"
        raw.write_bytes(data)
        subprocess.run(
            ["g++", "-std=c++20", "-O3", str(SOURCE), "-o", str(binary)],
            check=True,
        )
        result = json.loads(
            subprocess.check_output([str(binary), str(raw)], text=True)
        )
    if result != EXPECTED:
        raise ValueError(f"closure changed: {result}")
    print(json.dumps({
        **result,
        "source_sha256": SHA256,
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
    }, indent=2))


if __name__ == "__main__":
    main()
