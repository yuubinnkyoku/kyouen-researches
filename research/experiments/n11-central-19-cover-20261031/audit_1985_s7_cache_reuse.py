#!/usr/bin/env python3
"""Cross-audit the current 1985-S7 conditional frontier against pinned S7 evidence.

The 2232 historical LOSS7 labels are solver-trusted, NOT independently
terminal-verified.  Overlap is cache reuse potential, never a proof or a
reason to remove an S7 from the independent certificate worklist.
"""
from collections import Counter
import json

import focus_s7_worker_1985 as focus
import verify_s7_shared_frontier_46 as geom


def need(ok, message):
    if not ok:
        raise ValueError(message)


def forbid_known_win(frontier, win):
    need(not (frontier & win), "certified/known WIN7 conflicts with LOSS plan")


def audit():
    # The full three-swap chain is independently replayed by the 4x4 Bareiss
    # checker before a single cached verdict is inspected.
    frontiers, multiplicity = focus.geometry()
    selected = set(frontiers)
    need(len(selected) == 46 and len(multiplicity) == 1985,
         "changed conditional frontier")
    need(Counter(multiplicity.values()) == {1: 981, 2: 1004},
         "changed S7 sharing distribution")

    # geom.inventory checks pinned Git blob identity, sorted unique keys,
    # 7-stone board bounds, and D4 canonical form. These are historical
    # solver-trusted verdicts, not newly checked game trees.
    historical_loss = geom.inventory(geom.BASE / "all_s7_loss_2232.txt", 2232)
    historical_win = geom.inventory(geom.BASE / "all_s7_win_17.txt", 17)
    lift = json.loads(geom.frozen(geom.LIFT))
    need(lift["schema"] == "n11-fixed14-direct37-s7-lift-v1"
         and (lift["win7"], lift["loss7"], lift["unknown7"],
              lift["winLossConflicts"]) == (13, 1, 0, 0)
         and len(lift["rows"]) == 14, "fixed14 evidence identity changed")
    # The fixed14 result is side-to-move. On odd S7, WIN means
    # original-first LOSS; LOSS means original-first WIN.
    lift_loss = {r["s7"] for r in lift["rows"] if r["verdict"] == "WIN"}
    lift_win = {r["s7"] for r in lift["rows"] if r["verdict"] == "LOSS"}
    need(len(lift_loss) == 13 and len(lift_win) == 1
         and not ((historical_loss | lift_loss) & (historical_win | lift_win)),
         "WIN/LOSS conflict between evidence inventories")

    frontier = set(multiplicity)
    forbid_known_win(frontier, historical_win | lift_win)
    cache_hits = frontier & historical_loss
    terminal_hits = frontier & lift_loss
    need(not (cache_hits & terminal_hits), "duplicate LOSS7 evidence provenance")

    priority = lambda k: (sum(multiplicity[c] == 1 for c in frontiers[k]),
                          len(frontiers[k]), k)
    chosen = min(selected, key=priority)
    children = frontiers[chosen]
    focus_cached = children & cache_hits
    hit_edges = sum(len(cs & cache_hits) for cs in frontiers.values())
    need((len(cache_hits), len(terminal_hits), hit_edges,
          chosen, len(children), len(focus_cached)) ==
         (5, 0, 8, "0000000000000020380a000000000000", 60, 2),
         "1985 cache intersection or focus changed")

    # Negative test: a known-WIN key cannot be selected as an assumed LOSS7.
    try:
        forbid_known_win(frontier, {next(iter(frontier))})
    except ValueError:
        rejected = 1
    else:
        raise AssertionError("known-WIN conflict accepted")

    return {
        "schema": "n11-central49-1985-s7-cache-reuse-cross-audit-v1",
        "selected_s6": 46,
        "raw_s7_edges": sum(map(len, frontiers.values())),
        "distinct_s7": len(frontier),
        "s7_parent_multiplicity": {"1": 981, "2": 1004},
        "historical_solver_trusted_loss7_inventory": len(historical_loss),
        "historical_solver_trusted_loss7_hits": len(cache_hits),
        "historical_solver_trusted_loss7_edge_hits": hit_edges,
        "historical_loss7_hit_keys": sorted(cache_hits),
        "fixed14_terminal_backed_loss7_hits": len(terminal_hits),
        "historical_and_fixed14_known_win7_conflicts": 0,
        "not_in_these_loss7_inventories": len(frontier - historical_loss - lift_loss),
        "focus_s6": f"{chosen:032x}",
        "focus_s7_children": len(children),
        "focus_shared_s7": sum(multiplicity[c] == 2 for c in children),
        "focus_unshared_s7": sum(multiplicity[c] == 1 for c in children),
        "focus_historical_solver_trusted_loss7_hits": len(focus_cached),
        "focus_historical_loss7_hit_keys": sorted(focus_cached),
        "focus_without_historical_loss7_cache_hits": len(children - historical_loss),
        "four_worker_loads": [len(list(sorted(children))[i::4]) for i in range(4)],
        "negative_tests_rejected": rejected,
        "evidence_level": "PINNED_HISTORICAL_CACHE_CROSS_AUDIT_NOT_TERMINAL_PROOF",
        "selected_s6_outcome": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), indent=2, ensure_ascii=False))
