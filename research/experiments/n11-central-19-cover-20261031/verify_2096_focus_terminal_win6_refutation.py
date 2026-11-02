#!/usr/bin/env python3
"""Reproduce and independently audit a terminal WIN7 refuting 2096's focus S6.

The existing 3x3-determinant C++ generator emits a complete strategy.
The independent verifier recomputes every opponent reply with 4x4 Bareiss.
The generator's minimax labels and any worker receipts are not trusted.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

import verify_five_terminal_loss7 as independent
import focus_s7_worker_2096 as focus

HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "generate_five_terminal_loss7.cpp"
ROOT = "00000000000000303800000060000000"
PARENT = "00000000000000203800000060000000"
HEADER = "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"
EXPECTED_SHA256 = "a1051d9f30050b5c8f8d605351194eb2ffa897550bf55ee085d0bac6fa2a0762"
EXPECTED = (9750, 14848, 2245, 11755, (13, 17))


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def reproduce():
    with tempfile.TemporaryDirectory() as tmp:
        executable = Path(tmp) / "terminal_generator"
        certificate = Path(tmp) / "terminal_strategy.cert"
        subprocess.run(
            ["g++", "-O3", "-std=c++17", str(GENERATOR), "-o", str(executable)],
            check=True, timeout=120, capture_output=True, text=True,
        )
        subprocess.run(
            [str(executable), ROOT, str(certificate), "original_first_WIN7"],
            check=True, timeout=120, capture_output=True, text=True,
        )
        return certificate.read_bytes()


def audit(raw):
    need(hashlib.sha256(raw).hexdigest() == EXPECTED_SHA256,
         "generated complete strategy SHA256 changed")
    strategy = independent.parse(raw, ROOT, HEADER)
    stats = independent.verify(int(ROOT, 16), strategy, winner_parity=1)
    need(stats == EXPECTED, "independent terminal strategy shape changed")
    parent, child = int(PARENT, 16), int(ROOT, 16)
    need(parent.bit_count() == 6 and child.bit_count() == 7
         and parent & child == parent
         and (child ^ parent).bit_count() == 1
         and independent.legal(parent) & (child ^ parent),
         "WIN7 is not a legal child of the focused S6")
    frontiers, counts, secured = focus.geometry()
    need(parent in frontiers and child in frontiers[parent]
         and child in counts and child not in secured
         and len(frontiers) == 46 and len(counts) == 2096,
         "refuting WIN7 not in the verified 2096 focus")
    frozen = focus.freeze()
    need(frozen["focus_s6"] == PARENT
         and ROOT in frozen["unverified_s7"],
         "refuting child not assigned by the active 2096 dispatcher")
    return {
        "schema": "n11-central49-2096-focus-terminal-win6-refutation-v1",
        "refuted_s6": PARENT,
        "refuting_s7": ROOT,
        "cert_sha256": EXPECTED_SHA256,
        "strategy_states": stats[0],
        "reachable_states": stats[1],
        "terminal_states": stats[2],
        "opponent_edges": stats[3],
        "terminal_stones": list(stats[4]),
        "s7_original_first": "WIN",
        "s6_original_first": "WIN",
        "conditional_2096_loss_witness_plan_valid": False,
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
    }


def negative_tests(raw):
    strategy = independent.parse(raw, ROOT, HEADER)
    root = int(ROOT, 16)
    tests = []
    bad = dict(strategy)
    bad.pop(next(iter(bad)))
    tests.append(("missing winning reply", lambda: independent.verify(
        root, bad, winner_parity=1)))
    bad_move = dict(strategy)
    first_board = next(iter(bad_move))
    bad_move[first_board] = next(
        p for p in range(121) if first_board & (1 << p))
    tests.append(("occupied winning move", lambda: independent.verify(
        root, bad_move, winner_parity=1)))
    tests.append(("wrong orientation", lambda: independent.parse(
        raw, ROOT, independent.HEADER)))
    tests.append(("changed digest", lambda: audit(raw + b"\n")))
    for label, check in tests:
        try:
            check()
        except (ValueError, KeyError):
            continue
        raise AssertionError("negative case accepted: " + label)
    return len(tests)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    raw = reproduce()
    result = audit(raw)
    if args.negative:
        result["negative_tests_rejected"] = negative_tests(raw)
    print(json.dumps(result, sort_keys=True))


if __name__ == "__main__":
    main()
