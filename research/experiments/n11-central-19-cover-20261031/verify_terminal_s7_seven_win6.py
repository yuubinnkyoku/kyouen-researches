#!/usr/bin/env python3
"""Lift one independently terminal-proved S7 WIN to all seven S6 parents.

No new search: for each of the seven points removed from the shared S7,
the original first player restores that point and follows the same strategy.
All seven six-stone roots are replayed to terminal with independent 4x4
integer geometry. The S6 canonical keys are checked independently under D4.
"""
import base64
import hashlib
import json
import zlib
from pathlib import Path

import verify_terminal_s6_55_compact as proof
import verify_conditional_s6_distinct_s7_1984 as historical

HERE = Path(__file__).resolve().parent
CERT = HERE / "terminal_s6_55_strategy.b64"
MANIFEST = HERE / "terminal_s7_seven_s6_parents.json"
S7 = proof.ROOT | (1 << 43)
EXPECTED_KEYS = [
    "00000000000000203800000000080080",
    "00000000000000801002000240800000",
    "00000000000200001002080081000000",
    "00000000000200800002080081000000",
    "00000000000200801000080081000000",
    "00000000000200801002000081000000",
    "00000000000200801002080001000000",
]


def require(ok, why):
    if not ok:
        raise ValueError(why)


def points(board):
    return tuple(i for i in range(121) if board >> i & 1)


def canonical(board):
    ps = points(board)
    values = []
    for mode in range(8):
        v = 0
        for p in ps:
            x, y = p % 11, p // 11
            u, w = ((x, y), (10-y, x), (10-x, 10-y), (y, 10-x),
                    (10-x, y), (10-y, 10-x), (x, 10-y), (y, x))[mode]
            v |= 1 << (11*w+u)
        values.append(v)
    return min(values)


def audit():
    raw = zlib.decompress(base64.b64decode(CERT.read_text(encoding="ascii")))
    require(hashlib.sha256(raw).hexdigest() == proof.EXPECTED_SHA256
            and raw[0] == 43 and proof.safe(S7), "shared S7 source invalid")
    require(len(points(S7)) == 7, "S7 cardinality changed")
    known, _, _ = historical.known_comparisons()
    prior_seven = {
        int(x, 16) for x in (
            "00000000000000083801800000000000",
            "00000000000000203808200000000000",
            "0000000000000020380c000000000000",
            "00000000000000403808200000000000",
            "00000000000000601808200000000000",
            "00000000000000602808200000000000",
            "00000000000000603008200000000000",
            "00000000000000603800000000008000",
        )
    }
    rows = []
    for removed in points(S7):
        parent = S7 ^ (1 << removed)
        # The first byte is the parent-to-S7 move; all remaining strategy
        # bytes are unchanged because the entire subtree is identical.
        candidate = bytes([removed]) + raw[1:]
        require(proof.verify(candidate, root=parent) == proof.EXPECTED,
                "independent terminal replay failed for parent")
        key = canonical(parent)
        require(key not in known and key not in prior_seven,
                "S6 parent was already in the comparison inventory")
        rows.append({"removed": removed, "canonical_s6": f"{key:032x}"})
    require(sorted(row["canonical_s6"] for row in rows) == EXPECTED_KEYS,
            "seven distinct canonical parents changed")
    return {
        "schema": "n11-central49-terminal-s7-seven-win6-v1",
        "shared_s7": f"{canonical(S7):032x}",
        "terminal_raw_sha256": proof.EXPECTED_SHA256,
        "parents": rows,
        "new_original_first_win6": 7,
        "additional_after_first_s6_proof": 6,
        "per_parent_reached": proof.EXPECTED[0],
        "per_parent_terminal": proof.EXPECTED[3],
        "per_parent_losing_terminal": 0,
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
    }


def main():
    result = audit()
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(doc == result, "manifest differs from independently rebuilt proof")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
