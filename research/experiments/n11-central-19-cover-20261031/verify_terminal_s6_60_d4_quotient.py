#!/usr/bin/env python3
"""Verify the second terminal strategy and its D4-quotient ranked WIN closure.

A verified strategy is the only seed. No saved verdict cache or solver proof
numbers are trusted. Each newly certified state is justified by an already
certified larger-stone child (even depth) or ALL such children (odd depth).
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
SOURCE = HERE / "verify_terminal_s6_60_d4_quotient.cpp"
SHA256 = "debb5464282eb28e6a30496f8728515433d6f9507ffdeeda1eeaf04e3c5d7de4"
LAYERS = [7, 1, 296, 36, 10294, 1124, 114567, 11369,
          104007, 9994, 4651, 378, 19, 1]


def verified_raw(data: bytes) -> bytes:
    raw = zlib.decompress(base64.b64decode(b"".join(data.split()), validate=True))
    if len(raw) != 14440 or hashlib.sha256(raw).hexdigest() != SHA256:
        raise ValueError("strategy bytes or SHA-256 changed")
    return raw


def main():
    encoded = CERT.read_bytes().strip()
    raw = verified_raw(encoded)
    # Deliberately altered strategy data must never be accepted.
    damaged = bytearray(raw)
    damaged[0] ^= 1
    if hashlib.sha256(damaged).hexdigest() == SHA256:
        raise AssertionError("strategy mutation went undetected")

    with tempfile.TemporaryDirectory() as temp:
        exe = Path(temp) / "d4_quotient"
        raw_file = Path(temp) / "strategy.bin"
        raw_file.write_bytes(raw)
        subprocess.run(["g++", "-std=c++20", "-O3", str(SOURCE), "-o", str(exe)],
                       check=True)
        result = json.loads(subprocess.check_output([str(exe), str(raw_file)],
                                                    text=True))
    if (result["source_reached"] != 22364
            or result["d4_quotient_win_classes"] != 256744
            or result["layer_counts_6_to_19"] != LAYERS
            or result["certified_s6_classes"] != 7
            or result["certified_s7_classes"] != 1
            or sum(result["added_6_to_18"]) != 256744 - 22364
            or result["two_stone_root"] != "UNKNOWN"
            or result["empty_board"] != "UNKNOWN"):
        raise AssertionError(f"D4 quotient closure regression: {result}")
    print(json.dumps({**result, "source_sha256": SHA256,
                      "previous_raw_closure_d4_classes": 256193,
                      "additional_d4_classes": 256744 - 256193},
                     indent=2))


if __name__ == "__main__":
    main()
