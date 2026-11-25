#!/usr/bin/env python3
"""Independently refute the 2090 conditional S6-LOSS cover with a WIN6.

The 2090 frontier is replayed from its frozen certificate; the 1984
complete terminal strategy is replayed independently with 4x4 Bareiss.
An S6 proven original-first WIN cannot be a LOSS witness, regardless of
the number of distinct S7 proof obligations in the geometric cover.
"""
import hashlib
import json

import focus_s7_worker_2090 as current
import verify_focus_s6_win_strategy as win
import verify_s6_cover_exclude_certified_win6 as original


def need(ok, why):
    if not ok:
        raise ValueError(why)


def require_excluded(selected, refuted):
    need(refuted not in selected,
         "CERTIFIED_WIN6_SELECTED_AS_LOSS_WITNESS")


def audit():
    frontiers, multiplicity, secured = current.geometry()
    need(len(frontiers) == 46 and len(multiplicity) == 2090
         and sum(multiplicity.values()) == 2983 and len(secured) == 6,
         "2090 source certificate identity changed")
    need(f"{win.ROOT:032x}" == original.REFUTED,
         "1984 independently proved WIN6 identity changed")
    raw = win.CERT.read_bytes()
    need(hashlib.sha256(raw).hexdigest() == original.WIN_SHA,
         "1984 WIN6 terminal certificate SHA256 changed")
    terminal = win.replay(win.read_certificate(raw.decode("utf-8")))
    need(terminal["root"] == original.REFUTED
         and terminal["s6_original_first_outcome"] == "WIN"
         and terminal["visited_states"] == 8949
         and terminal["odd_terminal_win_leaves"] == 951,
         "complete terminal WIN6 replay changed")
    need(win.ROOT in frontiers, "2090 no longer contains the refuted S6")
    try:
        require_excluded(set(frontiers), win.ROOT)
    except ValueError:
        rejected = True
    else:
        raise AssertionError("certified WIN6 accepted as a LOSS witness")
    # Control: a plan without the refuted witness passes this single gate.
    require_excluded(set(frontiers) - {win.ROOT}, win.ROOT)
    return {
        "schema": "n11-central49-2090-certified-win6-refutation-v1",
        "selected_s6": len(frontiers),
        "distinct_s7_geometric_obligations": len(multiplicity),
        "terminal_proved_loss7_children": len(secured),
        "refuting_s6": original.REFUTED,
        "refuting_s6_original_first_outcome": "WIN",
        "winning_first_move": terminal["first_player_winning_move"],
        "terminal_strategy_nodes": terminal["even_strategy_nodes"],
        "terminal_visited_states": terminal["visited_states"],
        "terminal_winning_leaves": terminal["odd_terminal_win_leaves"],
        "source_certificate_sha256": original.WIN_SHA,
        "refutation_gate_rejected": rejected,
        "conditional_2090_loss_cover_valid": False,
        "s4_outcome": "UNKNOWN",
        "two_stone_root_outcome": "UNKNOWN",
        "empty_board_outcome": "UNKNOWN",
    }


if __name__ == "__main__":
    print(json.dumps(audit(), ensure_ascii=False, sort_keys=True))
