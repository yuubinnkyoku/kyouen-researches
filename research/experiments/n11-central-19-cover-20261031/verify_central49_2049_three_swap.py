#!/usr/bin/env python3
"""Independent 4x4-Bareiss verification of the 2092 -> 2049 S7 swap.

This is a conditional cover with UNKNOWN S6 verdicts, not a game proof.
The 3-for-3 optimizer uses a different 3x3 difference determinant.
"""
from collections import Counter, defaultdict
import hashlib
import json

import verify_central49_2092_two_swap_local_optimum as baseline
import verify_s7_shared_frontier_46 as independent
import verify_second_s7_repair_2092 as prior
import verify_terminal_s7_second_seven_win6 as second

REMOVED = (
    "00000000000000203800800000000200",
    "00000000000000801002002000204000",
    "00000000000000821082002000000000",
)
ADDED = (
    "00000000000000203800800000000020",
    "00000000000000203808000000000002",
    "00000000000040203800000000000200",
)
SOURCE_SHA = "afb2a19dc297e87b4d803526277b08f0f9be8c69f533bd02d318865a9533b8f8"


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def digest(keys):
    return hashlib.sha256(
        "".join(f"{k:032x}\n" for k in sorted(keys)).encode("ascii")
    ).hexdigest()


def audit():
    selected = set(baseline.reconstruct())
    rm = {int(k, 16) for k in REMOVED}
    ad = {int(k, 16) for k in ADDED}
    need(digest(selected) == SOURCE_SHA and len(selected) == 46,
         "2092 selection identity changed")
    need(len(rm) == len(ad) == 3 and rm <= selected and not (ad & selected),
         "invalid three-for-three exchange")
    need(all(independent.canonical(k) == k and k.bit_count() == 6
             for k in selected | ad), "noncanonical six-stone witness")

    _, _, _, historical_win6, first_terminal_parents, historical_win7 = (
        prior.previous.previous.reconstruct())
    terminal_win6 = baseline.certified_win6()
    win6 = historical_win6 | first_terminal_parents | terminal_win6
    first_terminal_s7 = int("00000000000200801002000081000000", 16) | (1 << 43)
    win7 = {int(k, 16) for k in historical_win7} | {
        independent.canonical(first_terminal_s7),
        independent.canonical(second.S7)
    }
    need(len(win6) == 139 and len(win7) == 22,
         "known WIN evidence inventory changed")
    new = (selected - rm) | ad
    need(len(new) == 46 and not (new & win6), "known WIN6 conflict")

    # Recompute the priority S5 incidence with the independent 4x4 geometry.
    source = baseline.read("conditional_s6_cover_46.json")
    s4 = int(source["s4_key"], 16)
    s5 = {independent.canonical(c) for c in independent.children(s4)}
    need(len(s5) == 94, "S5 frontier changed")
    def covered(selection):
        return {independent.canonical(c) for k in selection
                for c in independent.children(k)} & s5
    # S6 witnesses cover S5 via deleting one stone, not via forward S6 children.
    def parents(selection):
        return {independent.canonical(k ^ (1 << p))
                for k in selection for p in independent.points(k)}
    need(s5 <= parents(selected) and s5 <= parents(new),
         "S5 coverage lost")

    def frontier(selection):
        count = Counter()
        raw = 0
        for k in selection:
            children = independent.children(k)
            child_keys = {independent.canonical(c) for c in children}
            need(len(children) == len(child_keys),
                 "two S7 children of one S6 canonicalize together")
            raw += len(children)
            count.update(child_keys)
        return raw, count

    old_raw, old = frontier(selected)
    new_raw, updated = frontier(new)
    need((old_raw, len(old)) == (2989, 2092),
         "old S7 frontier changed")
    need(len(updated) == 2049 and not (set(updated) & win7),
         "new S7 frontier count or WIN7 conflict")
    need((set(old) - set(updated)) or (set(updated) - set(old)),
         "no actual frontier change")
    return {
        "schema": "n11-central49-2049-three-swap-independent-4x4-audit-v1",
        "source_selected_s6_sha256": SOURCE_SHA,
        "final_selected_s6_sha256": digest(new),
        "removed": list(REMOVED),
        "added": list(ADDED),
        "selected_s6": len(new),
        "covered_s5": len(s5 & parents(new)),
        "source_raw_s7_edges": old_raw,
        "source_distinct_s7": len(old),
        "final_raw_s7_edges": new_raw,
        "final_distinct_s7": len(updated),
        "distinct_s7_saved": len(old) - len(updated),
        "source_s7_only": len(set(old) - set(updated)),
        "new_s7_only": len(set(updated) - set(old)),
        "known_win6_conflicts": len(new & win6),
        "known_win7_conflicts": len(set(updated) & win7),
        "final_s7_parent_multiplicity": {
            str(k): v for k, v in sorted(Counter(updated.values()).items())
        },
        "selected_s6_verdict": "UNKNOWN",
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
        "scope": "Independent geometry audit of a conditional S6 cover; no S6 LOSS or root verdict."
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, indent=2))
