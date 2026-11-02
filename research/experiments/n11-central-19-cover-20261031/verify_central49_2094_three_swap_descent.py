#!/usr/bin/env python3
"""Audit two exact three-S6 exchanges from K0646's 2154-class N11 cover.

The K0637 five complete terminal strategies are regenerated and independently
checked before K0644 LOSS7 classes count as secured. The replacement frontier
uses independent 4x4 Bareiss geometry and a separate 3x3 determinant check.
This is a conditional LOSS-witness plan, never a game verdict.
"""
import copy
from functools import lru_cache
import hashlib
import json
from pathlib import Path

import focus_s7_worker_2154 as focus
import verify_central49_2154_two_swap_descent as source
import verify_conditional_s6_cover_46 as base

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_post_seven_win6_2094_three_swaps.json"
SCHEMA = "n11-central49-2154-to-2094-two-three-swaps-v1"
SOURCE_SHA = "49a95ddc351d761a4b6906c84c1a97daa9c7eb65a610e67d1b70c946889c42f4"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}


def need(ok, why):
    if not ok:
        raise ValueError(why)


def key(s):
    return f"{s:032x}"


def digest(keys):
    return hashlib.sha256(
        "".join(key(s) + "\n" for s in sorted(keys)).encode("ascii")
    ).hexdigest()


@lru_cache(maxsize=1)
def context():
    # Replays the entire 2154 source, including the exhaustive two-swap
    # neighborhood, and all five fixed terminal strategies via 4x4 Bareiss.
    frontiers, multiplicity, secured = focus.geometry()
    selected = set(frontiers)
    need(len(selected) == 46 and digest(selected) == SOURCE_SHA,
         "source 2154 selection identity changed")
    need(len(multiplicity) == 2154 and sum(multiplicity.values()) == 2990
         and len(secured) == 6, "source 2154 coverage changed")
    data = base.reconstruct()
    s5, incidence, costs = data[1:4]
    need(len(s5) == 94 and len(incidence) == 3868,
         "priority five-stone incidence changed")
    _, _, win6, win7, _ = source.current.comparison_inventories()
    win6 = {int(k, 16) for k in win6}
    win7 = {int(k, 16) for k in win7}
    need(len(win6) == 145 and len(win7) == 23,
         "certified WIN exclusions changed")
    # The 23 parent-lifted LOSS7 are legitimate only after focus.geometry()
    # has regenerated and verified the five pinned complete strategies.
    loss7 = source.terminal_loss7()
    need(len(loss7) == 23 and secured == set(multiplicity) & loss7
         and not (loss7 & win7), "K0644 certified overlap changed")
    return selected, s5, incidence, costs, win6, win7, loss7, frontiers


@lru_cache(maxsize=None)
def four_frontier(s):
    # Separate 4x4 Bareiss geometry; the 3x3 implementation is checked
    # against it, but neither result is taken from a worker receipt.
    raw = source.current.geometry.children(s)
    children = {source.current.geometry.canonical(c) for c in raw}
    need(len(raw) == len(children), "duplicate canonical child")
    need(children == set(source.fast_frontier(s)),
         "4x4/3x3 geometry disagreement")
    return frozenset(children)


def audit(doc):
    need(type(doc) is dict and doc.get("schema") == SCHEMA
         and doc.get("source_certificate") == source.CERT.name
         and doc.get("source_selected_s6_sha256") == SOURCE_SHA
         and doc.get("evidence_level") ==
         "GEOMETRY_ONLY_CONDITIONAL_COVER_WITH_TERMINAL_REPLAYED_S7_HITS"
         and doc.get("outcomes") == UNKNOWN, "plan identity or verdict changed")
    steps = doc.get("steps")
    need(type(steps) is list and len(steps) == 2, "expected two three-swaps")
    selected, s5, incidence, costs, win6, win7, loss7, source_frontiers = context()
    frontiers = dict(source_frontiers)
    expected = ((2991, 2098), (2987, 2094))
    for i, step in enumerate(steps):
        need(type(step) is dict and set(step) ==
             {"removed", "added", "raw_s7_edges",
              "distinct_s7_classes", "secured_loss7_classes"},
             "unexpected exchange fields")
        rm, ad = step["removed"], step["added"]
        need(type(rm) is list and type(ad) is list
             and len(rm) == len(ad) == 3
             and rm == sorted(set(rm)) and ad == sorted(set(ad))
             and all(type(k) is str and len(k) == 32
                     and all(c in "0123456789abcdef" for c in k)
                     for k in rm + ad), "invalid exchange encoding")
        removed, added = {int(k, 16) for k in rm}, {int(k, 16) for k in ad}
        need(removed <= selected and not (added & selected),
             "invalid three-for-three membership")
        need(added <= set(incidence) and not (added & win6),
             "out-of-scope or certified WIN6 witness")
        selected = (selected - removed) | added
        need(len(selected) == 46 and
             set().union(*(incidence[s] for s in selected)) ==
             set(range(len(s5))), "94 five-stone classes not covered")
        for s in removed:
            del frontiers[s]
        for s in added:
            ch = four_frontier(s)
            need(len(ch) == costs[s], "S6-to-S7 child count changed")
            frontiers[s] = ch
        need(set(frontiers) == selected, "frontier/selection mismatch")
        union = set().union(*frontiers.values())
        raw = sum(map(len, frontiers.values()))
        secured = union & loss7
        need(not (union & win7), "certified WIN7 in conditional LOSS7 frontier")
        need((raw, len(union)) == expected[i] ==
             (step["raw_s7_edges"], step["distinct_s7_classes"])
             and len(secured) == step["secured_loss7_classes"] == 6,
             f"exchange {i+1} count or secured coverage changed")
    need((doc.get("selected_s6_count"), doc.get("s5_covered"),
          doc.get("raw_s7_edges"), doc.get("distinct_s7_classes"),
          doc.get("saved_s7_classes"),
          doc.get("terminal_backed_loss7_hits_from_k0644"),
          doc.get("known_win6_conflicts"), doc.get("known_win7_conflicts")) ==
         (46, 94, 2987, 2094, 60, 6, 0, 0),
         "final manifest differs from independent geometry")
    return {
        "schema": "n11-central49-2094-independent-three-swap-audit-v1",
        "source_s7_classes": 2154,
        "final_s7_classes": len(union),
        "saved_s7_classes": 2154-len(union),
        "raw_s7_edges": raw,
        "selected_s6": len(selected),
        "covered_s5": len(s5),
        "secured_terminal_loss7": len(secured),
        "unsecured_by_k0644": len(union-secured),
        "known_win6_conflicts": len(selected & win6),
        "known_win7_conflicts": len(union & win7),
        "conditional_only": True,
        "outcomes": UNKNOWN,
    }


def negative_tests(doc):
    for mode in ("verdict", "source", "step", "member", "secured", "final"):
        bad = copy.deepcopy(doc)
        if mode == "verdict":
            bad["outcomes"]["s6"] = "LOSS"
        elif mode == "source":
            bad["source_selected_s6_sha256"] = "0" * 64
        elif mode == "step":
            bad["steps"][0]["distinct_s7_classes"] -= 1
        elif mode == "member":
            bad["steps"][0]["added"][0] = bad["steps"][0]["removed"][0]
        elif mode == "secured":
            bad["steps"][1]["secured_loss7_classes"] += 1
        else:
            bad["distinct_s7_classes"] -= 1
        try:
            audit(bad)
        except (ValueError, KeyError, TypeError):
            continue
        raise AssertionError("tampered certificate accepted: " + mode)
    return 6


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    result = audit(doc)
    if args.negative:
        result["negative_tests"] = negative_tests(doc)
    print(json.dumps(result, ensure_ascii=False, indent=2))
