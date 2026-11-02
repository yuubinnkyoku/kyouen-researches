#!/usr/bin/env python3
"""Independent 4x4 integer verification of a multi-step N11 S6 cover chain.

Every swap is a conditional geometry transformation, never an S6 LOSS proof.
The source selection is reconstructed from historical manifests.  All S7
frontiers are recalculated with Bareiss 4x4 determinants, separately from the
3x3 optimizer.  D4 and the priority S5 cover are checked at every step.
"""
from collections import Counter
from pathlib import Path
import hashlib
import json

import verify_central49_2092_two_swap_local_optimum as baseline
import verify_s7_shared_frontier_46 as geom
import verify_second_s7_repair_2092 as prior
import verify_terminal_s7_second_seven_win6 as second

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "conditional_s6_cover_46_three_swap_chain.json"
SOURCE_SHA = "afb2a19dc297e87b4d803526277b08f0f9be8c69f533bd02d318865a9533b8f8"


def need(ok, msg):
    if not ok:
        raise ValueError(msg)


def digest(keys):
    return hashlib.sha256(
        "".join(f"{k:032x}\n" for k in sorted(keys)).encode("ascii")
    ).hexdigest()


def audit(doc):
    need(doc["schema"] == "n11-central49-conditional-s6-three-swap-chain-v1",
         "wrong chain schema")
    need(doc["source_selected_s6_sha256"] == SOURCE_SHA,
         "source hash mismatch")
    need(doc["outcomes"] == {"selected_s6": "UNKNOWN", "s4": "UNKNOWN",
                              "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
         "verdict must remain UNKNOWN")
    selected = set(baseline.reconstruct())
    need(len(selected) == 46 and digest(selected) == SOURCE_SHA,
         "source 2092 selection changed")
    s4 = int(baseline.read("conditional_s6_cover_46.json")["s4_key"], 16)
    s5 = {geom.canonical(c) for c in geom.children(s4)}
    need(len(s5) == 94, "S5 obligations changed")
    _, _, _, old_win6, first_parents, old_win7 = prior.previous.previous.reconstruct()
    win6 = old_win6 | first_parents | baseline.certified_win6()
    terminal_s7 = int("00000000000200801002000081000000", 16) | (1 << 43)
    win7 = {int(k, 16) for k in old_win7} | {
        geom.canonical(terminal_s7), geom.canonical(second.S7)
    }
    need(len(win6) == 139 and len(win7) == 22,
         "WIN comparison inventory changed")
    cache = {}
    def children(k):
        if k not in cache:
            need(k.bit_count() == 6 and geom.canonical(k) == k,
                 "invalid six-stone canonical key")
            cs = geom.children(k)
            keys = {geom.canonical(c) for c in cs}
            need(len(cs) == len(keys), "within-parent S7 duplicate")
            cache[k] = keys
        return cache[k]

    def metrics(selection):
        need(len(selection) == 46 and not (selection & win6),
             "known WIN6 selected")
        parents = {geom.canonical(k ^ (1 << p))
                   for k in selection for p in geom.points(k)}
        need(s5 <= parents, "priority S5 cover incomplete")
        counts = Counter(q for k in selection for q in children(k))
        need(not (set(counts) & win7), "known WIN7 in conditional frontier")
        return sum(len(children(k)) for k in selection), len(counts), counts

    raw, distinct, _ = metrics(selected)
    need((raw, distinct) == (2989, 2092), "baseline S7 count changed")
    rows = []
    for step in doc["steps"]:
        rm = step["removed"]
        ad = step["added"]
        need(len(rm) == len(ad) == 3 and rm == sorted(set(rm))
             and ad == sorted(set(ad)), "invalid three-swap encoding")
        old = {int(k, 16) for k in rm}
        new = {int(k, 16) for k in ad}
        need(old <= selected and not (new & selected), "invalid three-swap membership")
        selected = (selected - old) | new
        raw, distinct, counts = metrics(selected)
        row = {
            "removed": rm,
            "added": ad,
            "raw_s7_edges": raw,
            "distinct_s7": distinct,
        }
        need(row == step, "chain step differs from independent 4x4 geometry")
        rows.append(row)
    result = {
        "schema": "n11-central49-conditional-s6-three-swap-chain-v1",
        "source_selected_s6_sha256": SOURCE_SHA,
        "steps": rows,
        "final_selected_s6_sha256": digest(selected),
        "final_raw_s7_edges": raw,
        "final_distinct_s7": distinct,
        "s5_covered": 94,
        "selected_s6": 46,
        "known_win6_conflicts": 0,
        "known_win7_conflicts": 0,
        "outcomes": {"selected_s6": "UNKNOWN", "s4": "UNKNOWN",
                     "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"},
        "scope": "Exact independent geometry for a conditional LOSS-witness cover; no S6 LOSS or root proof."
    }
    need(result == doc, "chain manifest summary differs from replay")
    return result


if __name__ == "__main__":
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    print(json.dumps(audit(doc), ensure_ascii=False, indent=2))
