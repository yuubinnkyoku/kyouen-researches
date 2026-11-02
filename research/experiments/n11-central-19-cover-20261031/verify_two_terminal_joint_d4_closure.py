#!/usr/bin/env python3
"""Audit the joint WIN closure of two fixed terminal strategies on n11.

The two inputs are individually replayed by an exact-integer C++ checker.
Its D4-quotient predecessor closure uses ranked AND/OR induction and proves
the joint result contains each individual closure. UNKNOWN is preserved.
"""
import base64
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile
import zlib

HERE = Path(__file__).resolve().parent
SOURCES = [
    ("terminal_s6_55_strategy.b64",
     "83bdd3c89555bd80eadae802d47a8dc8289f0aee1a935440fb325f7f9ce25b2b", 12068),
    ("terminal_s6_60_strategy.b64",
     "debb5464282eb28e6a30496f8728515433d6f9507ffdeeda1eeaf04e3c5d7de4", 14440),
]


def decode_and_check(data, expected_hash, expected_length):
    raw = zlib.decompress(base64.b64decode(b"".join(data.split()), validate=True))
    if len(raw) != expected_length or hashlib.sha256(raw).hexdigest() != expected_hash:
        raise ValueError("terminal strategy identity mismatch")
    return raw


def main():
    raws = [decode_and_check((HERE / filename).read_bytes(), digest, size)
            for filename, digest, size in SOURCES]
    for raw, (_, digest, size) in zip(raws, SOURCES):
        for damaged in (raw[:-1], raw + b"\0", bytes([raw[0] ^ 1]) + raw[1:]):
            try:
                decode_and_check(zlib.compress(damaged).hex().encode(), digest, size)
            except (ValueError, zlib.error, base64.binascii.Error):
                pass
            else:
                raise AssertionError("mutated strategy was accepted")
    with tempfile.TemporaryDirectory() as temp:
        temp = Path(temp)
        exe = temp / "joint"
        inputs = [temp / "first.bin", temp / "second.bin"]
        for path, raw in zip(inputs, raws):
            path.write_bytes(raw)
        subprocess.run(["g++", "-std=c++20", "-O3", "-Wall", "-Wextra",
                        str(HERE / "verify_two_terminal_joint_d4_closure.cpp"),
                        "-o", str(exe)], check=True)
        result = json.loads(subprocess.check_output([str(exe), *(str(p) for p in inputs)],
                                                    text=True))
    assert result["first_reached"] == 18649
    assert result["second_reached"] == 22364
    assert result["second_only_classes"] == 256744
    assert result["joint_classes"] >= result["separate_union_classes"]
    assert result["joint_classes"] == sum(result["layer_counts_6_to_19"])
    assert result["synergy_classes"] == sum(result["new_beyond_either_6_to_19"])
    assert result["two_stone_root"] == result["empty_board"] == "UNKNOWN"
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
