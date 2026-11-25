#!/usr/bin/env python3
"""Independent exact 4x4 terminal check for a second selected S6 WIN."""
import base64
import hashlib
import json
import sys
import zlib
from pathlib import Path
import verify_terminal_s6_55_compact as core

ROOT = int("00000000000000203808000000000020", 16)
SHA = "debb5464282eb28e6a30496f8728515433d6f9507ffdeeda1eeaf04e3c5d7de4"
EXPECTED = (22364, 14440, 4982, 2942, 34055)
CERT = Path(__file__).with_name("terminal_s6_60_strategy.b64")


def verify():
    raw = zlib.decompress(base64.b64decode(CERT.read_text(encoding="ascii")))
    if hashlib.sha256(raw).hexdigest() != SHA:
        raise ValueError("second S6 certificate hash changed")
    result = core.verify(raw, root=ROOT)
    if result != EXPECTED:
        raise ValueError("independent 4x4 terminal replay totals changed")
    return raw


def main():
    raw = verify()
    negative = 0
    if "--negative" in sys.argv:
        for bad in (raw[:-1], raw+b"\x00", b"\x00"+raw[1:],
                    raw[:10]+b"\xff"+raw[11:]):
            try:
                core.verify(bad, root=ROOT)
            except ValueError:
                negative += 1
            else:
                raise AssertionError("tampered second S6 strategy accepted")
    print(json.dumps({
        "root": f"{ROOT:032x}", "original_first_player": "WIN",
        "reached": EXPECTED[0], "strategy_nodes": EXPECTED[1],
        "opponent_nonterminal": EXPECTED[2], "terminal": EXPECTED[3],
        "edges": EXPECTED[4], "losing_terminal": 0,
        "certificate_bytes": len(raw), "certificate_sha256": SHA,
        "independent_geometry": "exact 4x4 Laplace",
        "negative_tests": negative,
        "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"
    }, indent=2))


if __name__ == "__main__":
    main()
