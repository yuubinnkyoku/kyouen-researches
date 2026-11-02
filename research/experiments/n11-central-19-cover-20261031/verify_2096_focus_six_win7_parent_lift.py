#!/usr/bin/env python3
"""Six independent complete WIN7 strategies imply a 37-class WIN6 parent closure.

The pre-existing 3x3 C++ minimax generator is only a certificate producer.
A separate 4x4 Bareiss implementation checks every reply and terminal leaf.
Removing any point from a certified original-first WIN7 gives a WIN6 parent:
the first player can restore that point to reach a second-to-move LOSS.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

import verify_five_terminal_loss7 as independent
import focus_s7_worker_2096 as focus
import verify_central49_2094_three_swap_descent as geometry
import verify_focus_s6_win_strategy as earlier

HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "generate_five_terminal_loss7.cpp"
HEADER = "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"
ROOTS = {
    "00000000000000283800000060000000":
        ("c7cb54e8536c01530290948893d95cd0b92f90c2f5aa5ad3b1424cafa90b26f7",
         (11976, 18122, 2534, 15124, (13, 17))),
    "00000000000000303800000060000000":
        ("a1051d9f30050b5c8f8d605351194eb2ffa897550bf55ee085d0bac6fa2a0762",
         (9750, 14848, 2245, 11755, (13, 17))),
    "00000000000040203800000060000000":
        ("352347762b315b946785b0926a4d0fd3d6ee1a0a92b21fcf06b02393f42278e6",
         (16919, 25804, 3895, 20965, (13, 17))),
    "00000000000200801002020040000002":
        ("5c8d91845348de8b6d1a971620451ffb06b6e145c4740a9e83643e7594367a3f",
         (16857, 25645, 3715, 21167, (13, 19))),
    "00000000000200801002020040400000":
        ("7aae272575119e2250beab6857a0407fdd8b225144b1fea2f930d1f3eea667eb",
         (14168, 21523, 2975, 18052, (13, 17))),
    "00000000000200801002120040000000":
        ("c816620985fde284147e46e18c8ba8c3b091d692842b807b4696fbd2902cebaa",
         (10243, 15556, 2090, 13204, (13, 17))),
}
FOCUS_S6 = "00000000000000203800000060000000"


def need(ok, why):
    if not ok:
        raise ValueError(why)


def canonical(board):
    ps = [i for i in range(121) if board & (1 << i)]
    result = []
    for t in range(8):
        mask = 0
        for p in ps:
            x, y = p % 11, p // 11
            xy = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                  (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[t]
            mask |= 1 << (11 * xy[1] + xy[0])
        result.append(mask)
    return min(result)


def audit(negative=False):
    all_parents = set()
    stats = {}
    negative_count = 0
    with tempfile.TemporaryDirectory() as temp:
        executable = Path(temp) / "generator"
        certificate = Path(temp) / "strategy.cert"
        subprocess.run(["g++", "-O3", "-std=c++17", str(GENERATOR),
                        "-o", str(executable)], check=True, timeout=120,
                       capture_output=True, text=True)
        for key, (digest, expected) in ROOTS.items():
            subprocess.run([str(executable), key, str(certificate),
                            "original_first_WIN7"],
                           check=True, timeout=120, capture_output=True, text=True)
            raw = certificate.read_bytes()
            need(hashlib.sha256(raw).hexdigest() == digest,
                 "complete WIN7 strategy SHA changed: " + key)
            strategy = independent.parse(raw, key, HEADER)
            shape = independent.verify(int(key, 16), strategy, winner_parity=1)
            need(shape == expected, "independent 4x4 terminal replay changed: " + key)
            root = int(key, 16)
            need(root.bit_count() == 7 and canonical(root) == root,
                 "noncanonical or non-seven-stone root")
            for p in range(121):
                if not root & (1 << p):
                    continue
                parent = root ^ (1 << p)
                need(parent.bit_count() == 6
                     and independent.legal(parent) & (1 << p),
                     "illegal six-to-seven restoration")
                all_parents.add(canonical(parent))
            if negative:
                bad = dict(strategy)
                bad.pop(next(iter(bad)))
                try:
                    independent.verify(root, bad, winner_parity=1)
                except ValueError:
                    negative_count += 1
                else:
                    raise AssertionError("missing winning reply accepted")
            stats[key] = {
                "strategy_states": shape[0], "reachable_states": shape[1],
                "terminal_states": shape[2], "opponent_edges": shape[3],
                "terminal_stones": list(shape[4]),
                "certificate_sha256": digest,
            }
    need(len(all_parents) == 37, "37 distinct terminal-derived WIN6 changed")
    frontiers, counts, secured = focus.geometry()
    need(len(frontiers) == 46 and len(counts) == 2096,
         "repaired 2096 historical geometry changed")
    selected_hits = sorted(all_parents & set(frontiers))
    need(int(FOCUS_S6, 16) in all_parents & set(frontiers),
         "focus refutation missing")
    _, _, _, _, known6, _, _, _ = geometry.context()
    previous_inventory = known6 | {earlier.ROOT}
    newly_covered = all_parents - previous_inventory
    return {
        "schema": "n11-central49-six-terminal-win7-37-win6-parent-closure-v1",
        "terminal_win7_roots": stats,
        "certified_win7_roots": len(ROOTS),
        "six_to_seven_restoration_edges": 42,
        "distinct_terminal_derived_win6": len(all_parents),
        "terminal_derived_win6_keys": [f"{p:032x}" for p in sorted(all_parents)],
        "previously_inventoried_win6": len(previous_inventory),
        "additional_win6_beyond_previous_inventory": len(newly_covered),
        "additional_win6_keys": [f"{p:032x}" for p in sorted(newly_covered)],
        "selected_2096_s6_conflicts": [f"{p:032x}" for p in selected_hits],
        "conditional_2096_loss_witness_plan_valid": False,
        "negative_tests_rejected": negative_count,
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    print(json.dumps(audit(args.negative), ensure_ascii=False, sort_keys=True))
