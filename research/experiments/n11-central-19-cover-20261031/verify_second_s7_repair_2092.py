#!/usr/bin/env python3
"""Independent geometry replay of four 2-for-2 swaps: 2207 -> 2092 S7 classes.

This verifies a conditional LOSS-witness cover, NOT any S6 LOSS verdict.
The candidate list and each child frontier are recomputed; no solver verdict,
proof number, or incomplete search is promoted to a proof.
"""
import copy
import hashlib
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s7_shared_frontier_46 as geom
import verify_second_s7_repair_2207 as previous
import verify_terminal_s7_second_seven_win6 as second

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "conditional_s6_cover_46_after_second_s7_repair_2092_swaps.json"
SOURCE_SHA = "0392c0eeeb827f9cde0bc000f65b544d19e002ca77d500a1cc712468466f44f3"
FINAL_SHA = "afb2a19dc297e87b4d803526277b08f0f9be8c69f533bd02d318865a9533b8f8"
COUNTS = [(2995, 2152), (3002, 2104), (2992, 2094), (2989, 2092)]
OUTCOMES = {"selected_s6": "UNKNOWN", "s4": "UNKNOWN",
            "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}


def need(ok, message):
    if not ok:
        raise ValueError(message)


def digest(chosen):
    payload = "\n".join(sorted(base.key(x) for x in chosen)) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def replay(doc):
    # Reconstruct the earlier fixed-44/two-for-two repair, not a hand-picked
    # S6 list. The existing source audit independently checks the 2207 count.
    prior_summary = previous.audit()
    need(prior_summary["distinct_s7"] == 2207
         and prior_summary["raw_s7_edges"] == 2995,
         "2207 source audit changed")
    incidence, costs, prior, old_win6, first_seven, old_win7 = (
        previous.previous.reconstruct())
    old_selected = (
        prior - {base.decode(previous.previous.ROOT),
                 base.decode(previous.previous.OTHER)}
    ) | {base.decode(k) for k in previous.previous.ADDED}
    second_parents = {base.decode(row["canonical_s6"])
                      for row in second.audit()["parents"]}
    removed = old_selected & second_parents
    need(sorted(base.key(k) for k in removed) == previous.REMOVED,
         "second terminal refutation changed")
    current = (old_selected - removed) | {
        base.decode(k) for k in previous.ADDED}
    need(len(current) == 46 and digest(current) == SOURCE_SHA,
         "source S6 selection identity changed")

    known_win6 = old_win6 | first_seven | second_parents
    # Historical comparison inventory + both newly certified terminal S7.
    first_terminal_s7 = base.decode("00000000000200801002000081000000") | (1 << 43)
    known_win7 = set(old_win7) | {
        base.key(geom.canonical(first_terminal_s7)),
        base.key(geom.canonical(second.S7)),
    }
    need(len(known_win6) == 138 and len(known_win7) == 22,
         f"known WIN inventory changed: WIN6={len(known_win6)} WIN7={len(known_win7)}")

    cache = {}
    def frontier(selection):
        union = set()
        edges = 0
        for s6 in sorted(selection):
            if s6 not in cache:
                raw = geom.children(s6)  # Independent full 4x4 Bareiss.
                children = {base.key(geom.canonical(c)) for c in raw}
                need(len(raw) == len(children) == costs[s6],
                     "3x3/4x4 S7 child geometry mismatch")
                cache[s6] = children
            edges += len(cache[s6])
            union.update(cache[s6])
        return edges, union

    def audit_selection(selection, expected):
        need(len(selection) == 46 and not (selection & known_win6),
             "WIN6 conflict or incorrect witness count")
        covered = set().union(*(incidence[s6] for s6 in selection))
        need(covered == set(range(94)), "S5 cover incomplete")
        edges, union = frontier(selection)
        need((edges, len(union)) == expected, "S7 count changed")
        need(not (union & known_win7), "certified/comparison WIN7 conflict")
        return edges, len(union)

    need(audit_selection(current, (2995, 2207)) == (2995, 2207),
         "source frontier mismatch")
    need(len(doc["steps"]) == len(COUNTS) == 4, "step count changed")
    for index, step in enumerate(doc["steps"]):
        removed_keys = step["removed"]
        added_keys = step["added"]
        need(len(removed_keys) == len(set(removed_keys)) == 2
             and len(added_keys) == len(set(added_keys)) == 2
             and removed_keys == sorted(removed_keys)
             and added_keys == sorted(added_keys), "invalid swap encoding")
        rm = {base.decode(k) for k in removed_keys}
        ad = {base.decode(k) for k in added_keys}
        need(rm <= current and not (ad & current) and ad <= set(incidence),
             "invalid S6 replacement")
        current = (current - rm) | ad
        actual = audit_selection(current, COUNTS[index])
        need(actual == (step["raw_s7_edges"], step["distinct_s7"]),
             "step manifest count differs from independent geometry")
    need(digest(current) == FINAL_SHA, "final selected S6 identity changed")
    return {
        "schema": "n11-central49-post-second-terminal-four-two-swap-v1",
        "source": previous.MANIFEST.name,
        "source_selected_s6_sha256": SOURCE_SHA,
        "final_selected_s6_sha256": FINAL_SHA,
        "steps": doc["steps"],
        "selected_s6": 46,
        "s5_covered": 94,
        "raw_s7_edges": 2989,
        "distinct_s7": 2092,
        "distinct_s7_saved": 115,
        "known_win6_conflicts": 0,
        "known_win7_conflicts": 0,
        "evidence_level": "GEOMETRY_ONLY_CONDITIONAL_S6_LOSS_WITNESS_COVER_NOT_VERDICTS",
        "outcomes": OUTCOMES,
    }


def main():
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    result = replay(doc)
    need(doc == result, "2092 conditional manifest differs from replay")
    tests = 0
    for change in ("step_count", "step_move", "win6", "outcome", "final_sha"):
        bad = copy.deepcopy(doc)
        if change == "step_count":
            bad["steps"][2]["distinct_s7"] -= 1
        elif change == "step_move":
            bad["steps"][1]["added"][0] = bad["steps"][1]["removed"][0]
        elif change == "win6":
            bad["known_win6_conflicts"] = 1
        elif change == "outcome":
            bad["outcomes"]["empty_board"] = "WIN"
        else:
            bad["final_selected_s6_sha256"] = "0" * 64
        try:
            # The complete geometric replay is not necessary for mutations
            # to already-computed summary fields; step mutations are checked
            # against independently verified step records.
            need(bad == result, "altered certificate rejected")
        except ValueError:
            tests += 1
        else:
            raise AssertionError("tampering accepted")
    print(json.dumps({**result, "negative_tests": tests},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
