#!/usr/bin/env python3
"""Lift a second independently terminal-proved S7 WIN to seven S6 parents."""
import base64
import hashlib
import json
import zlib
from pathlib import Path

import verify_terminal_s6_55_compact as core
import verify_terminal_s6_60_compact as source
import verify_terminal_s7_seven_win6 as first
import verify_conditional_s6_distinct_s7_1984 as historical

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "terminal_s7_second_seven_s6_parents.json"
S7 = source.ROOT | (1 << 107)
EXPECTED_KEYS = [
    "00000000000000203808000000000020",
    "00000000000000203808000000002000",
    "00000000000000801082002080000000",
    "00000000000200021002008000800000",
    "00000000000200820002008000800000",
    "00000000000200821000008000800000",
    "00000000000200821002000000800000",
]


def require(ok, why):
    if not ok:
        raise ValueError(why)


def audit():
    raw = source.verify()
    require(raw[0] == 107 and core.safe(S7) and S7.bit_count() == 7,
            "second shared S7 source invalid")
    old_win6, _, _ = historical.known_comparisons()
    prior = {int(k, 16) for k in first.EXPECTED_KEYS}
    prior |= {int(k, 16) for k in (
        "00000000000000083801800000000000",
        "00000000000000203808200000000000",
        "0000000000000020380c000000000000",
        "00000000000000403808200000000000",
        "00000000000000601808200000000000",
        "00000000000000602808200000000000",
        "00000000000000603008200000000000",
        "00000000000000603800000000008000",
    )}
    rows = []
    for removed in first.points(S7):
        parent = S7 ^ (1 << removed)
        candidate = bytes([removed]) + raw[1:]
        require(core.verify(candidate, root=parent) == source.EXPECTED,
                "second S7 parent terminal replay failed")
        canonical = first.canonical(parent)
        require(canonical not in old_win6 and canonical not in prior,
                "second shared S7 parent overlaps previous WIN6 inventory")
        rows.append({"removed": removed,
                     "canonical_s6": f"{canonical:032x}"})
    require(sorted(r["canonical_s6"] for r in rows) == EXPECTED_KEYS,
            "second shared S7 parent canonical classes changed")
    return {
        "schema": "n11-central49-second-terminal-s7-seven-win6-v1",
        "shared_s7": f"{first.canonical(S7):032x}",
        "terminal_raw_sha256": source.SHA,
        "parents": rows,
        "new_original_first_win6": 7,
        "additional_after_second_s6_proof": 6,
        "per_parent_reached": source.EXPECTED[0],
        "per_parent_terminal": source.EXPECTED[3],
        "per_parent_losing_terminal": 0,
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
    }


def main():
    result = audit()
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    require(doc == result, "second seven-parent manifest altered")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
