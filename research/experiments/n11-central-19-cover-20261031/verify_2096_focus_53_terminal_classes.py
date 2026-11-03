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
EXPECTED_LIFT = (34, 376, 251, 204)
# K0644's five independently certified LOSS7 first replies. This is an
# existing proof input, not a newly inferred solver verdict.
K0644_FIRST_MOVES = {
    "00000000000000203808000000000120": 115,
    "0000000000000020380a000000004000": 76,
    "00000000000000a03808100000000000": 114,
    "00000000000002043800800000040000": 49,
    "00000000000200801082008100000000": 65,
}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def lift_loss7_parent(root, eight, removed):
    """A certified LOSS7 winning reply makes LOSS8; every safe S7 parent is LOSS7."""
    need(root.bit_count() == 7 and eight.bit_count() == 8
         and (root & eight) == root
         and (eight ^ root).bit_count() == 1,
         "not a certified seven-to-eight transition")
    need(independent.legal(root) & (eight ^ root),
         "winning reply is illegal under independent 4x4 geometry")
    need(eight & (1 << removed), "removed point absent from LOSS8")
    parent = eight ^ (1 << removed)
    need(parent.bit_count() == 7
         and independent.legal(parent) & (1 << removed),
         "parent cannot legally restore certified LOSS8")
    return canonical(parent)


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
    loss8 = set()
    lifted_loss7 = set()
    lifted_edges = 0
    original_loss7 = set()
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
            if not is_win:
                root = int(key, 16)
                original_loss7.add(root)
                need(root in strategy, "LOSS7 certificate has no winning first reply")
                eight = root | (1 << strategy[root])
                need(eight.bit_count() == 8, "invalid winning reply")
                loss8.add(canonical(eight))
                for removed in range(121):
                    if eight & (1 << removed):
                        lifted_loss7.add(lift_loss7_parent(root, eight, removed))
                        lifted_edges += 1
            certificate_manifest.append(
                key + " " + orientation + " "
                + hashlib.sha256(raw).hexdigest() + "\n")
            examples.setdefault(orientation, (key, raw, strategy))
    need(hashlib.sha256("".join(certificate_manifest).encode()).hexdigest()
         == EXPECTED_CERTIFICATE_DIGEST,
         "53 complete certificate digests differ from pinned evidence")
    need(tuple(totals) == EXPECTED_TOTALS,
         "53 independent 4x4 proof shapes changed")
    need(len(original_loss7) == 47 and
         {canonical(x) for x in original_loss7} <= lifted_loss7
         and lifted_edges == 47 * 8,
         "LOSS7 first-reply parent closure incomplete")
    need((len(loss8), lifted_edges, len(lifted_loss7),
          len(lifted_loss7 - {canonical(x) for x in original_loss7}))
         == EXPECTED_LIFT, "47-root parent-lift result changed")
    old_lifted = set()
    for key, move in K0644_FIRST_MOVES.items():
        root = int(key, 16)
        eight = root | (1 << move)
        for removed in range(121):
            if eight & (1 << removed):
                old_lifted.add(lift_loss7_parent(root, eight, removed))
    need(len(old_lifted) == 23 and not (old_lifted & lifted_loss7),
         "K0644 23-class closure overlaps or changed")
    need(len(old_lifted | lifted_loss7) == 274,
         "total terminal-derived LOSS7 inventory changed")
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
        "certified_loss8_first_replies": len(loss8),
        "loss8_to_loss7_restoration_edges_checked": lifted_edges,
        "distinct_terminal_derived_loss7_by_parent_lift": len(lifted_loss7),
        "new_loss7_beyond_47_original_roots":
            len(lifted_loss7 - {canonical(x) for x in original_loss7}),
        "previous_k0644_loss7_classes": len(old_lifted),
        "overlap_with_k0644": len(old_lifted & lifted_loss7),
        "combined_terminal_derived_loss7_classes": len(old_lifted | lifted_loss7),
        "new_loss7_beyond_previously_known_70": len(lifted_loss7) - 47,
        "terminal_derived_loss7_keys": [f"{x:032x}" for x in sorted(lifted_loss7)],
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
