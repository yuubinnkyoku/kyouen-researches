#!/usr/bin/env python3
"""Independent 4x4 integer replay of the 2049 -> 1994 three-witness swap.

A conditional geometric cover only.  Neither S6 LOSS nor root outcome follows.
"""
from collections import Counter
import hashlib
import json

import verify_central49_2092_two_swap_local_optimum as baseline
import verify_s7_shared_frontier_46 as geom
import verify_second_s7_repair_2092 as prior
import verify_terminal_s7_second_seven_win6 as second
from verify_central49_2049_three_swap import REMOVED as FIRST_RM, ADDED as FIRST_AD

SECOND_RM = (
    "00000000000000203800000010800000",
    "00000000000000801002002000100800",
    "00000000000040203800000000000200",
)
SECOND_AD = (
    "00000000000000203800000010001000",
    "00000000000000203808000000000200",
    "00000000000000801002002000084000",
)


def need(test, msg):
    if not test:
        raise ValueError(msg)


def digest(keys):
    return hashlib.sha256(
        "".join(f"{k:032x}\n" for k in sorted(keys)).encode("ascii")
    ).hexdigest()


def swap(selected, removed, added):
    rm = {int(k, 16) for k in removed}
    ad = {int(k, 16) for k in added}
    need(len(rm) == len(ad) == 3 and rm <= selected and not (ad & selected),
         "invalid exact three-witness exchange")
    return (selected - rm) | ad


def frontier(selected):
    counts = Counter()
    raw = 0
    for k in selected:
        cs = geom.children(k)
        keys = {geom.canonical(c) for c in cs}
        need(len(cs) == len(keys), "within-parent D4 duplicate")
        raw += len(cs)
        counts.update(keys)
    return raw, counts


def audit():
    initial = set(baseline.reconstruct())
    need(len(initial) == 46 and digest(initial)
         == "afb2a19dc297e87b4d803526277b08f0f9be8c69f533bd02d318865a9533b8f8",
         "source 2092 selection changed")
    first = swap(initial, FIRST_RM, FIRST_AD)
    need(digest(first)
         == "78e3ab27ffd9278b6172f935615b6a74ecd7abe85222fe4ab3eb71079ee54a3b",
         "source 2049 selection changed")
    final = swap(first, SECOND_RM, SECOND_AD)
    need(len(final) == 46 and all(geom.canonical(k) == k and k.bit_count() == 6
                                  for k in final), "invalid final S6 keys")
    s4 = int(baseline.read("conditional_s6_cover_46.json")["s4_key"], 16)
    s5 = {geom.canonical(c) for c in geom.children(s4)}
    parents = {geom.canonical(k ^ (1 << p)) for k in final for p in geom.points(k)}
    need(len(s5) == 94 and s5 <= parents, "S5 cover not complete")
    _, _, _, old_win6, first_parents, old_win7 = prior.previous.previous.reconstruct()
    win6 = old_win6 | first_parents | baseline.certified_win6()
    terminal_s7 = int("00000000000200801002000081000000", 16) | (1 << 43)
    win7 = {int(k, 16) for k in old_win7} | {
        geom.canonical(terminal_s7), geom.canonical(second.S7)
    }
    need(len(win6) == 139 and len(win7) == 22 and not (final & win6),
         "WIN6 conflict")
    old_raw, old = frontier(first)
    new_raw, new = frontier(final)
    need((old_raw, len(old)) == (3002, 2049), "2049 source changed")
    need(len(new) == 1994 and not (set(new) & win7), "1994 frontier mismatch")
    return {
        "schema": "n11-central49-1994-independent-4x4-audit-v1",
        "source_selected_s6_sha256": digest(first),
        "final_selected_s6_sha256": digest(final),
        "removed": list(SECOND_RM),
        "added": list(SECOND_AD),
        "selected_s6": 46,
        "s5_covered": len(s5 & parents),
        "source_raw_s7_edges": old_raw,
        "source_distinct_s7": len(old),
        "final_raw_s7_edges": new_raw,
        "final_distinct_s7": len(new),
        "distinct_s7_saved": len(old) - len(new),
        "source_s7_only": len(set(old) - set(new)),
        "new_s7_only": len(set(new) - set(old)),
        "known_win6_conflicts": len(final & win6),
        "known_win7_conflicts": len(set(new) & win7),
        "s7_parent_multiplicity": {
            str(k): v for k, v in sorted(Counter(new.values()).items())
        },
        "selected_s6_verdict": "UNKNOWN",
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
        "scope": "Conditional geometric cover only; no S6 LOSS or root verdict."
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
