#!/usr/bin/env python3
"""Independent complete terminal audit of all 53 children of retired 2096 focus.

Generate deterministic strategies with the existing 3x3 C++ solver, but
validate every legal reply and every terminal with the separate 4x4 Bareiss
implementation. A pinned aggregate digest commits to all 53 certificates.
This does not resurrect the refuted conditional 2096 LOSS-witness plan.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

import verify_five_terminal_loss7 as independent
import focus_s7_worker_2096 as focus
from verify_2096_focus_six_win7_parent_lift import canonical

HERE = Path(__file__).resolve().parent
GENERATOR = HERE / "generate_five_terminal_loss7.cpp"
PARENT = "00000000000000203800000060000000"
WIN7 = {
    "00000000000000283800000060000000",
    "00000000000000303800000060000000",
    "00000000000040203800000060000000",
    "00000000000200801002020040000002",
    "00000000000200801002020040400000",
    "00000000000200801002120040000000",
}
HEADER_WIN = "n11-terminal-strategy-v1 original_first_WIN7 second_to_move_LOSS"
HEADER_LOSS = independent.HEADER
EXPECTED_CHILD_DIGEST = "5a49e2b9500722caa84e5222d31408d41cae242624f073ff7f6737cc4dce3648"
EXPECTED_CERTIFICATE_DIGEST = "034bb4b162d67afa559bad0bbe7cff339c120eb35af0a6ff21e2ee914f5f9bd6"
EXPECTED_TOTALS = (206668, 313388, 42058, 261323)


def need(ok, why):
    if not ok:
        raise ValueError(why)


def audit(negative=False):
    parent = int(PARENT, 16)
    need(parent.bit_count() == 6 and canonical(parent) == parent,
         "focus parent changed")
    # The independent 4x4 geometry must agree with the historical 2096
    # frontier. No retired plan is frozen or dispatched.
    raw_moves = independent.legal(parent)
    children = set()
    while raw_moves:
        bit = raw_moves & -raw_moves
        raw_moves -= bit
        children.add(canonical(parent | bit))
    frontiers, counts, secured = focus.geometry()
    need(parent in frontiers and children == frontiers[parent]
         and len(children) == 53 and not (children & secured)
         and len(frontiers) == 46 and len(counts) == 2096,
         "independent 4x4 focus geometry disagrees")
    roots = [f"{s:032x}" for s in sorted(children)]
    need(hashlib.sha256("".join(k + "\n" for k in roots).encode()).hexdigest()
         == EXPECTED_CHILD_DIGEST and WIN7 <= set(roots),
         "frozen focus child identity changed")
    totals = [0, 0, 0, 0]
    certificate_manifest = []
    examples = {}
    with tempfile.TemporaryDirectory() as temp:
        executable = Path(temp) / "generator"
        certificate = Path(temp) / "strategy.cert"
        subprocess.run(["g++", "-O3", "-std=c++17", str(GENERATOR),
                        "-o", str(executable)], check=True, timeout=120,
                       capture_output=True, text=True)
        for key in roots:
            is_win = key in WIN7
            command = [str(executable), key, str(certificate)]
            if is_win:
                command.append("original_first_WIN7")
            subprocess.run(command, check=True, timeout=120,
                           capture_output=True, text=True)
            raw = certificate.read_bytes()
            orientation = "WIN7" if is_win else "LOSS7"
            header = HEADER_WIN if is_win else HEADER_LOSS
            strategy = independent.parse(raw, key, header)
            stats = independent.verify(int(key, 16), strategy,
                                       winner_parity=1 if is_win else 0)
            for i in range(4):
                totals[i] += stats[i]
            certificate_manifest.append(
                key + " " + orientation + " "
                + hashlib.sha256(raw).hexdigest() + "\n")
            examples.setdefault(orientation, (key, raw, strategy))
    need(hashlib.sha256("".join(certificate_manifest).encode()).hexdigest()
         == EXPECTED_CERTIFICATE_DIGEST,
         "53 complete certificate digests differ from pinned evidence")
    need(tuple(totals) == EXPECTED_TOTALS,
         "53 independent 4x4 proof shapes changed")
    rejected = 0
    if negative:
        for orientation, (key, raw, strategy) in examples.items():
            bad = dict(strategy)
            bad.pop(next(iter(bad)))
            try:
                independent.verify(int(key, 16), bad,
                                   winner_parity=1 if orientation == "WIN7" else 0)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError("missing strategy reply accepted")
            try:
                independent.parse(raw, key,
                                  HEADER_LOSS if orientation == "WIN7"
                                  else HEADER_WIN)
            except ValueError:
                rejected += 1
            else:
                raise AssertionError("wrong certificate orientation accepted")
    return {
        "schema": "n11-central49-2096-focus-53-independent-terminal-audit-v1",
        "focus_s6": PARENT,
        "focused_s7": len(roots),
        "terminal_certified_original_first_loss7": len(roots) - len(WIN7),
        "terminal_certified_original_first_win7": len(WIN7),
        "new_loss7_vs_k0644": len(roots) - len(WIN7),
        "strategy_states": totals[0],
        "reachable_states": totals[1],
        "terminal_states": totals[2],
        "opponent_edges": totals[3],
        "certificate_manifest_sha256": EXPECTED_CERTIFICATE_DIGEST,
        "negative_tests_rejected": rejected,
        "s6_original_first": "WIN",
        "conditional_2096_loss_witness_plan_valid": False,
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    print(json.dumps(audit(args.negative), sort_keys=True))
