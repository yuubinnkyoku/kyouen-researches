#!/usr/bin/env python3
"""Audit current 2090-S7 certificate priorities against frozen older evidence.

Only K0644 terminal-replayed LOSS7 children are removed from proof obligations.
Historical solver-trusted labels and fixed14 results are kept in separate
columns; they may prioritize independent replay but are NOT proof shortcuts.
"""
from collections import Counter
from itertools import combinations
import json

import focus_s7_worker_2090 as current
import verify_s7_shared_frontier_46 as old


def need(condition, message):
    if not condition:
        raise ValueError(message)


def reject_conflict(proved_loss, other_win):
    need(not (proved_loss & other_win),
         "independent LOSS7 and external WIN7 conflict: investigate before dispatch")


def audit():
    # Replays the full 2090 certificate and the five terminal strategies
    # with independent 4x4 integer geometry before reading external caches.
    frontiers, multiplicity, proved_loss = current.geometry()
    selected = sorted(frontiers)
    all_s7 = set(multiplicity)
    need(len(selected) == 46 and len(all_s7) == 2090
         and sum(multiplicity.values()) == 2983
         and len(proved_loss) == 6 and proved_loss <= all_s7,
         "current 2090 certificate changed")
    need(all(set(cs) <= all_s7 for cs in frontiers.values()),
         "frontier is inconsistent with its multiplicity")

    # Git-blob-pinned inventories. They are not independently replayed
    # terminal certificates, even when a historical solver called them LOSS.
    old_loss = {int(k, 16) for k in old.inventory(
        old.BASE / "all_s7_loss_2232.txt", 2232)}
    old_win = {int(k, 16) for k in old.inventory(
        old.BASE / "all_s7_win_17.txt", 17)}
    fixed14 = json.loads(old.frozen(old.LIFT))
    need(fixed14["schema"] == "n11-fixed14-direct37-s7-lift-v1"
         and (fixed14["win7"], fixed14["loss7"],
              fixed14["unknown7"], fixed14["winLossConflicts"])
         == (13, 1, 0, 0) and len(fixed14["rows"]) == 14,
         "fixed14 evidence identity changed")
    # Fixed14 uses side-to-move, which reverses original-first labels at S7.
    fixed_loss = {int(r["s7"], 16) for r in fixed14["rows"]
                  if r["verdict"] == "WIN"}
    fixed_win = {int(r["s7"], 16) for r in fixed14["rows"]
                 if r["verdict"] == "LOSS"}
    need(len(fixed_loss) == 13 and len(fixed_win) == 1
         and not ((old_loss | fixed_loss) & (old_win | fixed_win)),
         "historical cache/fixed14 WIN/LOSS conflict")
    reject_conflict(proved_loss, old_win | fixed_win)
    # An old LOSS label matching K0644 is not new proof; count separately.
    old_hits = all_s7 & old_loss
    fixed_hits = all_s7 & fixed_loss
    win_candidates = all_s7 & (old_win | fixed_win)
    unproved = all_s7 - proved_loss
    need(len(unproved) == 2084, "terminal-backed worklist changed")

    def row(s):
        children = frontiers[s]
        pending = children - proved_loss
        return {
            "s6": f"{s:032x}",
            "total_s7": len(children),
            "terminal_proved_s7": len(children & proved_loss),
            "unproved_s7": len(pending),
            "historical_loss_cache_hits_not_proofs": len(pending & old_loss),
            "fixed14_loss_hits_not_replayed_here": len(pending & fixed_loss),
            "historical_win7_replay_candidates": len(pending & (old_win | fixed_win)),
            "shared_unproved_s7": sum(multiplicity[c] > 1 for c in pending),
        }

    rows = [row(s) for s in selected]
    # First close a single S6 with the fewest genuinely unproved children.
    # Cache reuse and sharing are only tie breakers, not secured coverage.
    def rank(r):
        return (r["unproved_s7"],
                -r["historical_loss_cache_hits_not_proofs"],
                -r["shared_unproved_s7"], r["s6"])

    ranking = sorted(rows, key=rank)
    pinned = next(r for r in rows if r["s6"] == current.FOCUS)
    need((pinned["total_s7"], pinned["terminal_proved_s7"],
          pinned["unproved_s7"]) == (64, 2, 62),
         "pinned focus changed")

    # Exhaustively optimize the number of distinct S7 proof obligations
    # needed to close two or three of the 46 S6 witnesses. This is an
    # objective on sets, not an assertion that any S7 is actually LOSS.
    pending = {s: frontiers[s] - proved_loss for s in selected}
    def best_group(size):
        best = None
        for group in combinations(selected, size):
            union = set().union(*(pending[s] for s in group))
            candidate = (len(union), tuple(f"{s:032x}" for s in group))
            if best is None or candidate < best:
                best = candidate
        return {
            "s6": list(best[1]),
            "distinct_unproved_s7": best[0],
            "sum_separate_unproved_s7": sum(len(pending[int(s, 16)])
                                              for s in best[1]),
        }

    best_two = best_group(2)
    best_three = best_group(3)
    need(best_two["distinct_unproved_s7"] >= ranking[0]["unproved_s7"],
         "two-S6 union smaller than one-S6 minimum")
    need(best_three["distinct_unproved_s7"] >= best_two["distinct_unproved_s7"],
         "three-S6 union smaller than two-S6 minimum")

    # Negative checks: a cached label never removes an unproved child.
    cache_only = (old_hits | fixed_hits) - proved_loss
    if cache_only:
        probe = next(iter(cache_only))
        need(probe in unproved, "unreplayed cache was promoted to proof")
    try:
        reject_conflict({1}, {1})
    except ValueError:
        conflict_rejected = True
    else:
        raise AssertionError("WIN/LOSS conflict was accepted")

    return {
        "schema": "n11-central49-2090-cache-and-terminal-focus-audit-v1",
        "selected_s6": 46,
        "distinct_s7": 2090,
        "terminal_proved_loss7": 6,
        "still_unproved_s7": 2084,
        "historical_solver_trusted_loss7_hits_not_proofs": len(old_hits),
        "historical_solver_trusted_win7_replay_candidates": len(all_s7 & old_win),
        "fixed14_loss7_hits_not_replayed_here": len(fixed_hits),
        "fixed14_win7_replay_candidates": len(all_s7 & fixed_win),
        "cache_only_keys_not_promoted": len(cache_only),
        "historical_loss7_edge_hits": sum(len(cs & old_loss)
                                         for cs in frontiers.values()),
        "s7_parent_multiplicity": dict(sorted(Counter(multiplicity.values()).items())),
        "pinned_focus": pinned,
        "best_first_focus": ranking[0],
        "top_five_first_focus": ranking[:5],
        "best_two_s6_union": best_two,
        "best_three_s6_union": best_three,
        "historical_win7_candidate_keys": sorted(
            f"{k:032x}" for k in win_candidates),
        "negative_conflict_rejected": conflict_rejected,
        "evidence_limit": "Only K0644 terminal-replayed LOSS7 counts as proved; cached labels and finite set unions cannot prove S6 or the empty board.",
        "s6_outcome": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, sort_keys=True))
