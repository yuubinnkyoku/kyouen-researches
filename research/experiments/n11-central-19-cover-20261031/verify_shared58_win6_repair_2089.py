#!/usr/bin/env python3
"""Independent exact-geometry audit of the fixed-44 repair after two WIN6 proofs.

The old 1980-S7 conditional LOSS plan was refuted by terminal-proved WIN6.
Reconstruct its 46 witnesses, retain the 44 non-refuted ones, exhaustively
enumerate every two-for-two S6 repair, and independently count all S7 children
with a 4x4 integer Bareiss determinant. A cover is NOT a LOSS certificate.
"""
import argparse
import copy
import hashlib
import itertools
import json
from pathlib import Path

import verify_conditional_s6_cover_46 as base
import verify_s6_cover_exclude_certified_win6 as source_audit
import verify_repaired_s6_1980 as old_chain
import verify_conditional_s6_distinct_s7_1984 as historical
import verify_s7_shared_frontier_46 as independent
import verify_shared58_s6_win_strategy as terminal

HERE = Path(__file__).resolve().parent
CERT = HERE / "conditional_s6_cover_46_after_shared58_win6_repair_2089.json"
OLD_SOURCE = HERE / "conditional_s6_cover_46_exclude_certified_win6.json"
UNKNOWN = {"s6": "UNKNOWN", "s4": "UNKNOWN",
           "two_stone_root": "UNKNOWN", "empty_board": "UNKNOWN"}
EXPECTED_REMOVED = [terminal.ROOT_KEY, terminal.DERIVED_ROOT_KEY]
EXPECTED_ADDED = [
    "0000000000000000380c200000000000",
    "00000000000000203804200000000000",
]
EXPECTED_OPTIONS = [
    (("0000000000000000380c200000000000",
      "00000000000000203804200000000000"), 2978, 2089),
    (("00000000000000083801800000000000",
      "00000000000000403808200000000000"), 2989, 2100),
    (("00000000000000083820800000000000",
      "0000000000000040380c000000000000"), 2988, 2100),
]


def need(ok, message):
    if not ok:
        raise ValueError(message)


def reconstruct():
    data = base.reconstruct()
    _, s5, incidence, cost, *_ = data
    source = json.loads(OLD_SOURCE.read_text(encoding="utf-8"))
    old_win6, old_win7, _ = historical.known_comparisons()
    source_audit.verify(source, data, {base.key(m) for m in old_win6})
    initial = {base.decode(k) for k in source["selected_s6_classes"]}
    rows = old_chain.load_rows()
    result = old_chain.audit(rows, data, initial, old_win6, old_win7, {})
    need(result["final_distinct_s7"] == 1980, "old 18-swap chain changed")
    current = set(initial)
    for row in rows:
        removed = {base.decode(k) for k in row[:2]}
        added = {base.decode(k) for k in row[2:4]}
        need(removed <= current and not (added & current), "old swap invalid")
        current = (current - removed) | added
    need(len(current) == 46 and all(base.decode(k) in current
         for k in EXPECTED_REMOVED), "terminal-proved WIN6 not in old cover")
    need(hashlib.sha256(terminal.CERT.read_bytes()).hexdigest()
         == terminal.EXPECTED_SHA256, "WIN6 terminal certificate hash changed")
    need(independent.canonical(terminal.ROOT | (1 << 70))
         == independent.canonical(terminal.DERIVED_ROOT | (1 << 75)),
         "shared terminal WIN7 is not identical up to D4")
    fixed = current - {base.decode(k) for k in EXPECTED_REMOVED}
    need(len(fixed) == 44, "wrong fixed witness count")
    covered = set().union(*(incidence[m] for m in fixed))
    missing = set(range(len(s5))) - covered
    need(len(s5) == 94 and len(missing) == 4
         and sorted(missing) == [35, 38, 41, 92],
         "four uncovered S5 obligations changed")
    # The candidate universe is all 3868 geometrically reachable S6 classes,
    # not merely the old 46 witnesses or a heuristic shortlist.
    candidates = sorted(m for m, parents in incidence.items()
                        if m not in current and parents & missing)
    need(len(incidence) == 3868 and len(candidates) == 319,
         "candidate incidence universe changed")
    pairs = [(u, v) for u, v in itertools.combinations(candidates, 2)
             if missing <= incidence[u] | incidence[v]]
    need(len(pairs) == 3, "exhaustive two-for-two repair count changed")
    known_win6 = set(old_win6) | {source_audit.REFUTED and
                  base.decode(source_audit.REFUTED),
                  terminal.ROOT, terminal.DERIVED_ROOT}
    known_win7 = set(old_win7)
    shared_win7 = base.key(independent.canonical(terminal.ROOT | (1 << 70)))
    known_win7.add(shared_win7)
    need(len(old_win6) == 117 and len(old_win7) == 19
         and shared_win7 not in old_win7,
         "known WIN6/WIN7 inventory changed")
    return incidence, cost, fixed, pairs, known_win6, known_win7, shared_win7


def evaluate(incidence, cost, fixed, pairs, known_win6, known_win7):
    memo = {}
    def frontier(chosen):
        union, edges = set(), 0
        for m in sorted(chosen):
            if m not in memo:
                need(independent.canonical(m) == m, "noncanonical S6")
                children = independent.children(m)
                keys = {base.key(independent.canonical(c)) for c in children}
                need(len(children) == len(keys) == cost[m],
                     "4x4/3x3 disagreement in S6-to-S7 geometry")
                memo[m] = keys
            edges += len(memo[m])
            union.update(memo[m])
        return edges, union

    output = []
    for u, v in pairs:
        selected = fixed | {u, v}
        need(len(selected) == 46
             and set().union(*(incidence[m] for m in selected))
                 == set(range(94)), "incomplete repaired S5 cover")
        need(not (selected & known_win6),
             "known WIN6 cannot be used as conditional LOSS witness")
        edges, frontier_keys = frontier(selected)
        need(not (frontier_keys & known_win7),
             "known WIN7 contradicts a conditional LOSS7 obligation")
        output.append(((base.key(u), base.key(v)), edges, len(frontier_keys)))
    output.sort(key=lambda x: x[0])
    need(output == EXPECTED_OPTIONS, "exhaustive repair S7 costs changed")
    return output


def verify_doc(doc, options):
    need(doc.get("schema") == "n11-central49-fixed44-two-certified-win6-repair-v1"
         and doc.get("source") == old_chain.CERT.name
         and doc.get("terminal_win6_certificate") == terminal.CERT.name
         and doc.get("terminal_win6_sha256") == terminal.EXPECTED_SHA256
         and doc.get("removed_certified_win6") == EXPECTED_REMOVED
         and doc.get("added_s6_classes") == EXPECTED_ADDED
         and doc.get("evidence_level")
             == "GEOMETRY_ONLY_CONDITIONAL_S6_LOSS_WITNESS_COVER_NOT_VERDICTS"
         and doc.get("outcomes") == UNKNOWN,
         "source, terminal provenance or UNKNOWN outcome changed")
    need((doc.get("fixed_unchanged_s6"), doc.get("missing_s5_after_removal"),
          doc.get("s5_covered"), doc.get("selected_s6_count"),
          doc.get("raw_s7_edges"), doc.get("distinct_s7_classes"),
          doc.get("known_original_first_win6_conflicts"),
          doc.get("known_original_first_win7_conflicts"),
          doc.get("certified_shared_win7_conflicts"),
          doc.get("fixed44_exact_minimum_distinct_s7"))
         == (44, 4, 94, 46, 2978, 2089, 0, 0, 0, 2089),
         "repaired cover summary changed")
    expected = [{"added": list(pair), "raw_s7_edges": edges,
                 "distinct_s7_classes": distinct}
                for pair, edges, distinct in options]
    need(doc.get("exhaustive_two_replacement_options") == expected,
         "exhaustive two-replacement alternatives changed")
    need(min(x[2] for x in options) == 2089
         and options[0][0] == tuple(doc["added_s6_classes"]),
         "selected repair does not attain fixed-44 minimum")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--negative", action="store_true")
    parser.add_argument("--replay-terminal", action="store_true",
                        help="replay both full terminal WIN6 strategies as well")
    args = parser.parse_args()
    incidence, cost, fixed, pairs, win6, win7, shared = reconstruct()
    options = evaluate(incidence, cost, fixed, pairs, win6, win7)
    doc = json.loads(CERT.read_text(encoding="utf-8"))
    verify_doc(doc, options)
    if args.replay_terminal:
        strategy = terminal.parse_certificate(terminal.CERT.read_text())
        terminal.replay(strategy)
        terminal.replay(terminal.lifted_strategy(strategy),
                        terminal.DERIVED_ROOT, 75)
    result = {
        "schema": "n11-central49-fixed44-exhaustive-two-win6-repair-audit-v1",
        "s5_covered": 94, "fixed_s6": 44, "replaced_s6": 2,
        "exhaustive_replacement_pairs": len(pairs),
        "candidate_s6_touching_missing_s5": 319,
        "s7_costs": [x[2] for x in options],
        "selected_raw_s7_edges": 2978,
        "selected_distinct_s7": 2089,
        "fixed44_minimum_distinct_s7": 2089,
        "certified_shared_win7": shared,
        "terminal_strategies_replayed": args.replay_terminal,
        "conditional_only": True,
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
    }
    if args.negative:
        mutations = [
            lambda d: d["added_s6_classes"].__setitem__(1, d["added_s6_classes"][0]),
            lambda d: d["outcomes"].__setitem__("s6", "LOSS"),
            lambda d: d.__setitem__("distinct_s7_classes", 2088),
            lambda d: d["exhaustive_two_replacement_options"][1].__setitem__(
                "distinct_s7_classes", 2099),
            lambda d: d.__setitem__("terminal_win6_sha256", "0" * 64),
        ]
        for mutate in mutations:
            bad = copy.deepcopy(doc)
            mutate(bad)
            try:
                verify_doc(bad, options)
            except (ValueError, KeyError, TypeError):
                continue
            raise AssertionError("tampered certificate accepted")
        result["negative_tests"] = len(mutations)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
