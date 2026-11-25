#!/usr/bin/env python3
"""Audit six-stone parent frontiers of the 274 terminal-certified LOSS7 keys.

This is a coverage/bottleneck measurement, NOT a new WIN/LOSS proof.
The 274-key manifest must separately pass the complete 53-certificate
independent replay (verify_2096_focus_53_terminal_classes.py).
"""
import argparse
import copy
from itertools import combinations
import json
from pathlib import Path

import verify_five_terminal_loss7 as independent
from verify_2096_focus_six_win7_parent_lift import ROOTS, canonical

HERE = Path(__file__).resolve().parent
MANIFEST = HERE / "terminal_loss7_parent_lift_274_manifest.json"
FOCUS = "00000000000000203800000060000000"
SOURCE_DIGEST = "034bb4b162d67afa559bad0bbe7cff339c120eb35af0a6ff21e2ee914f5f9bd6"
EXPECTED_KEYS = {
    "schema", "source_focus_s6", "source_certificate_manifest_sha256",
    "source_terminal_loss7_roots", "distinct_certified_loss8_first_replies",
    "independent_restoration_edges", "lifted_loss7_keys",
    "previous_k0644_loss7_keys", "combined_terminal_loss7_keys",
    "new_loss7_beyond_previous_70", "two_stone_root", "empty_board",
}


def need(ok, reason):
    if not ok:
        raise ValueError(reason)


def points(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask -= bit


def verify_manifest(doc):
    need(type(doc) is dict and set(doc) == EXPECTED_KEYS,
         "manifest fields changed")
    need(doc["schema"] == "n11-central49-terminal-loss7-parent-lift-274-v1"
         and doc["source_focus_s6"] == FOCUS
         and doc["source_certificate_manifest_sha256"] == SOURCE_DIGEST
         and doc["source_terminal_loss7_roots"] == 47
         and doc["distinct_certified_loss8_first_replies"] == 34
         and doc["independent_restoration_edges"] == 376
         and doc["new_loss7_beyond_previous_70"] == 204
         and doc["two_stone_root"] == doc["empty_board"] == "UNKNOWN",
         "manifest provenance or outcome fields changed")
    result = []
    for name, size in (("lifted_loss7_keys", 251),
                       ("previous_k0644_loss7_keys", 23),
                       ("combined_terminal_loss7_keys", 274)):
        keys = doc[name]
        need(type(keys) is list and len(keys) == size
             and all(type(k) is str and len(k) == 32
                     and all(c in "0123456789abcdef" for c in k)
                     for k in keys)
             and keys == sorted(set(keys)), name + " keys invalid")
        result.append({int(k, 16) for k in keys})
    lifted, previous, combined = result
    need(not (lifted & previous) and lifted | previous == combined,
         "274-key union changed")
    for mask in combined:
        need(mask.bit_count() == 7 and canonical(mask) == mask,
             "not a canonical seven-stone board")
        need(all(independent.det4(q) != 0
                 for q in combinations(points(mask), 4)),
             "manifest contains an illegal seven-stone board")
    return combined


def audit(doc):
    certified = verify_manifest(doc)
    parents = set()
    for child in certified:
        for p in points(child):
            parents.add(canonical(child ^ (1 << p)))
    # The six independently certified WIN7 roots imply 37 WIN6 parents.
    # Compare those certificates' parent closure with the 274 LOSS7 frontier.
    proven_win6 = {
        canonical(int(key, 16) ^ (1 << p))
        for key in ROOTS for p in points(int(key, 16))
    }
    need(len(proven_win6) == 37
         and parents & proven_win6 == {int(FOCUS, 16)},
         "K0660 WIN6 overlap with LOSS7 six-parent inventory changed")
    rows = []
    for parent in sorted(parents):
        need(parent.bit_count() == 6 and canonical(parent) == parent,
             "noncanonical six-stone parent")
        legal = independent.legal(parent)
        children = {canonical(parent | (1 << p)) for p in points(legal)}
        secured = len(children & certified)
        rows.append({"key": f"{parent:032x}", "legal": len(children),
                     "secured": secured, "unsecured": len(children) - secured})
    rows.sort(key=lambda r: (r["unsecured"], -r["secured"],
                             r["legal"], r["key"]))
    need(len(parents) == 866, "six-parent inventory changed")
    focus = next(r for r in rows if r["key"] == FOCUS)
    need((focus["legal"], focus["secured"], focus["unsecured"]) == (53, 47, 6),
         "known refuted focus coverage changed")
    others = [r for r in rows if r["key"] != FOCUS]
    need(others[0]["unsecured"] == 42
         and (others[0]["legal"], others[0]["secured"]) == (44, 2),
         "nonfocus frontier minimum changed")
    need(not any(r["unsecured"] == 0 for r in rows),
         "unexpected complete six-parent frontier: independently verify verdict")
    return {
        "schema": "n11-274-loss7-six-parent-frontier-v1",
        "source_certified_loss7": len(certified),
        "distinct_six_parents_touched": len(parents),
        "six_parents_fully_covered": 0,
        "known_k0660_win6_parents": len(proven_win6),
        "known_k0660_win6_parent_overlap": 1,
        "known_refuted_win6_focus": focus,
        "best_other_parent": others[0],
        "top_ten_other_parents": others[:10],
        "interpretation": "GEOMETRY_ONLY; unsecured means absent from this 274-key inventory, not globally UNKNOWN",
        "six_parent_outcomes": "UNKNOWN_EXCEPT_K0660_FOCUS_WIN",
        "two_stone_root": "UNKNOWN",
        "empty_board": "UNKNOWN",
    }


def negative_tests(doc):
    bads = []
    bad = copy.deepcopy(doc)
    bad["combined_terminal_loss7_keys"].pop()
    bads.append(bad)
    bad = copy.deepcopy(doc)
    bad["combined_terminal_loss7_keys"][0] = bad["combined_terminal_loss7_keys"][1]
    bads.append(bad)
    bad = copy.deepcopy(doc)
    bad["two_stone_root"] = "WIN"
    bads.append(bad)
    bad = copy.deepcopy(doc)
    bad["source_certificate_manifest_sha256"] = "0" * 64
    bads.append(bad)
    for bad in bads:
        try:
            verify_manifest(bad)
        except ValueError:
            continue
        raise AssertionError("tampered manifest accepted")
    return len(bads)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--negative", action="store_true")
    args = parser.parse_args()
    doc = json.loads(MANIFEST.read_text(encoding="utf-8"))
    result = audit(doc)
    if args.negative:
        result["negative_tests_rejected"] = negative_tests(doc)
    print(json.dumps(result, sort_keys=True, ensure_ascii=False))
