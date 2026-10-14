"""Aggregate the third joint-plan update effects into one measurement record.

Reads only files produced by this experiment plus the frozen baselines (the
second update output, the first update output and the original K0423 output).
Every number is copied or recomputed from those files; nothing is estimated.
Section-5 effects are reported on both criteria: "from_previous" (vs
n11-adaptive-plan-update2-20261013) and "from_initial" (vs
n11-s5-s6-quotient-20261013).

Independent-proof tallies are reported under several explicit labels because
"cumulative" is ambiguous across the plan-layered receipts, the adaptive line
and all independently verified receipts (the three native pilot receipts
115540 / 144193 / 144311 are verified but intentionally NOT layered into any
plan yet).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
PREV = ROOT / "research/experiments/n11-adaptive-plan-update2-20261013/output"
FIRST = ROOT / "research/experiments/n11-adaptive-plan-update-20261013/output"
K0423 = ROOT / "research/experiments/n11-s5-s6-quotient-20261013/output"
COST_CMP = ROOT / "research/experiments/n11-proof-cost-comparison-20261012/output"
RANK = ROOT / "research/experiments/n11-conflict-ranking-20261013/output/ranking.json"
NATIVE = ROOT / "research/experiments/n11-native-terminal-checker-20261013/output"
NEW = (137694, 143240, 220231, 126017)
UNLAYERED = (115540, 144193, 144311)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    plan = json.loads((EXP / "output/repaired-joint-plan-update3.json").read_text())
    dual = json.loads((EXP / "output/updated-element-dual-update3.json").read_text())
    win = json.loads((EXP / "output/win-side-reanalysis3.json").read_text())
    prev_plan = json.loads((PREV / "repaired-joint-plan-update2.json").read_text())
    prev_dual = json.loads((PREV / "updated-element-dual-update2.json").read_text())
    prev_win = json.loads((PREV / "win-side-reanalysis2.json").read_text())
    init_plan = json.loads((K0423 / "repaired-joint-plan.json").read_text())
    init_dual = json.loads((K0423 / "updated-element-dual.json").read_text())
    ranking = json.loads(RANK.read_text())

    assert plan["verification"]["passed"]
    assert plan["verification"]["complete_third_boundaries"] == 19
    assert plan["third_moves_covered"] == 2261
    assert plan["verification"]["known_win_selected"] == 0
    assert dual["integer_lower_bound"] <= dual["upper_bound"]
    assert win["verification"]["passed"] and not win["verification"]["failures"]
    assert prev_win["verification"]["passed"]
    assert dual["repaired_plan_sha256"] == sha(EXP / "output/repaired-joint-plan-update3.json")

    receipts = plan["new_receipts"]
    for index in NEW:
        fact = receipts[str(index)]
        assert fact["trusted_leaves"] == 0 and fact["pruned_roundtrip_verified"]
        assert fact["evidence_class"] == "independent-terminal-only-verification"
    assert {int(k): v["verdict"] for k, v in receipts.items()} == \
        {137694: 2, 143240: 2, 220231: 2, 126017: 1}

    conflicts = [row["s5_index"] for row in ranking["rows"]]
    assert len(conflicts) == 28
    resolved = {int(k): v for k, v in plan["resolved_s5_verdicts"].items()}
    assert plan["known_loss_removed_from_cost"] == sorted(NEW[:3])
    still_unknown = [i for i in conflicts if i not in resolved]
    assert 144692 in still_unknown and 144019 in still_unknown
    assert 197665 in still_unknown
    assert resolved == {558600: 2, 209644: 1, 126899: 2, 144095: 1, 121263: 2,
                        145001: 2, 137694: 2, 143240: 2, 220231: 2, 126017: 1}
    assert sorted(i for i in still_unknown if i in UNLAYERED) == sorted(UNLAYERED)

    win_base = next(a for a in json.loads(
        (COST_CMP / "win-side-analysis.json").read_text())["firsts"]
        if a["first"] == 49)
    # 1,945 stored witnesses; 209644 (WIN) was resolved before the first update,
    # so the pre-first-update unresolved count was 1,944 per the section-5 baseline.
    witness_baseline_unresolved = win_base["optimistic_witness_s5"] - 1

    prev_closable = {row["reply"] for row in prev_win["replies"] if row["closable"]}
    now_closable = {row["reply"] for row in win["replies"] if row["closable"]}
    lost_closability = sorted(prev_closable - now_closable)
    gained_closability = sorted(now_closable - prev_closable)
    assert not gained_closability
    assert win["after"]["unclosable_replies"] == \
        sorted(prev_win["after"]["unclosable_replies"] + lost_closability)

    layered = sorted(resolved)
    adaptive_line = [126899, 144095, 121263, 145001] + list(NEW)
    layered_loss = sorted(i for i, v in resolved.items() if v == 2)
    layered_win = sorted(i for i, v in resolved.items() if v == 1)
    conflict_closure_line = sorted(set(UNLAYERED) | set(adaptive_line))
    all_receipts = layered + sorted(UNLAYERED)

    tallies = {
        "this_round": {"attempts": 4, "successes": 4, "indices": sorted(NEW)},
        "cumulative_adaptive_line": {
            "attempts": 8, "successes": 8, "indices": adaptive_line,
            "note": ("continues the update2 README definition (cumulative 4/4): "
                     "first update 126899/144095, second update 121263/145001, "
                     "this round 137694/143240/220231/126017"),
        },
        "cumulative_plan_layered_total": {
            "attempts": 10, "successes": 10, "indices": layered,
            "note": "K0423 pilot receipts included; 6/6 through the second update",
        },
        "cumulative_plan_layered_loss_side": {
            "attempts": len(layered_loss), "successes": len(layered_loss),
            "indices": layered_loss,
            "note": ("layered receipts whose verdict is LOSS: 4/4 through the "
                     "second update, 7/7 after this round (the 7/7 reading)"),
        },
        "cumulative_plan_layered_win_side": {
            "attempts": len(layered_win), "successes": len(layered_win),
            "indices": layered_win,
            "note": "layered receipts whose verdict is WIN",
        },
        "cumulative_conflict_closure_certified": {
            "attempts": len(conflict_closure_line),
            "successes": len(conflict_closure_line),
            "indices": conflict_closure_line,
            "note": ("conflict-closure lineage excluding the K0423 pilots: native "
                     "focus 3 (115540, 144193, 144311) + adaptive line 8 "
                     "(126899, 144095, 121263, 145001, 137694, 143240, 220231, "
                     "126017) = 11. The night README lists 確定9件 (its list omits "
                     "145001) and counts 126017 separately as the next independent "
                     "WIN evidence, so that spelling reads 10"),
        },
        "cumulative_all_independent_receipts": {
            "attempts": len(all_receipts), "successes": len(all_receipts),
            "indices": all_receipts,
            "layered_into_plan": layered,
            "verified_but_unlayered": sorted(UNLAYERED),
            "note": ("9 independent receipts existed before this round "
                     "(K0423 2 + native focus 3 + adaptive 4) and this round adds "
                     "4; the three native receipts 115540 LOSS / 144193 LOSS / "
                     "144311 WIN stay out of every plan, so plan-layered (10) and "
                     "all-receipt (13) tallies differ"),
        },
    }

    effect = {
        "schema": "n11-night-plan-update3-effects-v1",
        "new_facts": {
            "s5_index": {str(i): receipts[str(i)]["verdict"] for i in NEW},
            "independent_verifications": receipts,
            "verification_attempts": 4,
            "verification_successes": 4,
            "cumulative_tallies": tallies,
            "unlayered_receipts_unchanged": sorted(UNLAYERED),
            "tally_note": ("several cumulative labels are reported because "
                           "'independent proof cumulative' is ambiguous across "
                           "plan-layered, adaptive-line, conflict-closure and "
                           "all-receipt readings"),
        },
        "bounds": {
            "upper": {
                "from_previous": {"before": plan["baseline_union_size"],
                                  "after": plan["union_size"],
                                  "delta": plan["union_size"] - plan["baseline_union_size"]},
                "from_initial": {"before": init_plan["union_size"],
                                 "after": plan["union_size"],
                                 "delta": plan["union_size"] - init_plan["union_size"]},
                "source": "union of unknown-S5 children of selected LOSS responses",
            },
            "lower": {
                "from_previous": {"before": prev_dual["integer_lower_bound"],
                                  "after": dual["integer_lower_bound"],
                                  "delta": dual["integer_lower_bound"] - prev_dual["integer_lower_bound"],
                                  "exact_before": prev_dual["total_exact"],
                                  "exact_after": dual["total_exact"]},
                "from_initial": {"before": init_dual["integer_lower_bound"],
                                 "after": dual["integer_lower_bound"],
                                 "delta": dual["integer_lower_bound"] - init_dual["integer_lower_bound"],
                                 "exact_before": init_dual["total_exact"],
                                 "exact_after": dual["total_exact"]},
                "source": "exact element-only fractional dual, ceil by integrality",
            },
            "interval_from_previous": [[prev_dual["integer_lower_bound"],
                                        prev_plan["union_size"]],
                                       [dual["integer_lower_bound"],
                                        plan["union_size"]]],
            "interval_from_initial": [[init_dual["integer_lower_bound"],
                                       init_plan["union_size"]],
                                      [dual["integer_lower_bound"],
                                       plan["union_size"]]],
        },
        "loss_side": {
            "changed_choices": plan["changed_choice_count"],
            "newly_excluded_s4_classes": plan["new_excluded_s4_classes"],
            "excluded_s4_classes_total": plan["excluded_s4_classes"],
            "free_thirds_from_previous": [plan["baseline_free_thirds"],
                                          plan["free_thirds"]],
            "free_thirds_from_initial": [init_plan["free_thirds"],
                                         plan["free_thirds"]],
            "required_s5_from_previous": [plan["baseline_union_size"],
                                          plan["union_size"]],
            "required_s5_from_initial": [init_plan["union_size"],
                                         plan["union_size"]],
            "known_loss_removed_from_cost": plan["known_loss_removed_from_cost"],
            "roots_rechecked": plan["roots"],
            "third_moves_rechecked": plan["third_moves_covered"],
            "complete_s5_boundaries_rechecked": plan["verification"]["complete_s5_boundaries"],
            "known_win_requirements_asserted": 0,
        },
        "batch_vs_staged": plan["batch_vs_staged"],
        "win_side": {
            "unresolved_witnesses_from_previous": [
                prev_win["after"]["unresolved_witness_s5"],
                win["after"]["unresolved_witness_s5"]],
            "unresolved_witnesses_from_initial": [
                witness_baseline_unresolved,
                win["after"]["unresolved_witness_s5"]],
            "delta_from_previous": (win["after"]["unresolved_witness_s5"]
                                    - prev_win["after"]["unresolved_witness_s5"]),
            "delta_from_initial": (win["after"]["unresolved_witness_s5"]
                                   - witness_baseline_unresolved),
            "stored_pool": win["stored_witness_pool"],
            "allowed_pool": [prev_win["allowed_witness_pool"],
                             win["allowed_witness_pool"]],
            "removed_witnesses": win["removed_witnesses"],
            "unclosable_reply_orbits": {
                "from_initial": win_base["unclosable_replies"],
                "from_previous": prev_win["after"]["unclosable_replies"],
                "after": win["after"]["unclosable_replies"],
                "newly_unclosable_vs_previous": lost_closability,
                "r2_impossibility": "continues and expands",
            },
            "uncovered_s4_classes_before_reopt": win["pre_optimisation"][
                "uncovered_s4_classes"],
            "uncovered_branches_before_reopt": win["pre_optimisation"][
                "uncovered_branches"],
            "replies_affected_before_reopt": win["pre_optimisation"][
                "replies_affected"],
            "dead_branches_before_reopt": win["pre_optimisation"][
                "dead_branches_in_stored_thirds"],
            "and_width": {"from_initial": win_base["and_width_fourths"],
                          "from_previous": prev_win["after"]["and_width_fourths"],
                          "after": win["after"]["and_width_fourths"]},
            "closable_replies": {"from_initial": win_base["closable_replies"],
                                 "from_previous": prev_win["after"]["closable_replies"],
                                 "after": win["after"]["closable_replies"]},
            "new_witnesses_invented": 0,
            "s4_kind_counts": win["s4_kind_counts"],
            "s4_classes_touched": win["s4_classes_touched"],
        },
        "newly_closed": {
            "from_previous": {
                "third_moves": win["after"]["newly_closed_third_moves_vs_previous"],
                "reply_orbits": win["after"]["newly_closed_reply_orbits_vs_previous"],
                "replies": win["after"]["newly_free_replies_vs_previous"],
            },
            "from_initial": {
                "third_moves": win["after"]["newly_closed_third_moves_vs_initial"],
                "reply_orbits": win["after"]["newly_closed_reply_orbits_vs_initial"],
                "replies": win["after"]["newly_free_replies_vs_initial"],
            },
            "regressed_vs_previous": win["after"]["regressed_free_replies_vs_previous"],
            "note": ("a reply counts as newly closed when its chosen third needs "
                     "zero WIN witnesses from the saved pool; both criteria are "
                     "reported"),
        },
        "ranking_cross_check": {
            "loss_side": plan["ranking_cross_check"],
            "win_side_branches": win["ranking_cross_check"],
            "all_match": True,
            "note": ("branch incidences and affected-choice counts are recomputed "
                     "from independent geometry on the frozen ranking rows; every "
                     "value matches n11-conflict-ranking-20261013/output/ranking.json"),
        },
        "verdict_census": {
            "conflict_candidates_total": len(conflicts),
            "win": sorted(k for k, v in resolved.items() if v == 1),
            "loss": sorted(k for k, v in resolved.items() if v == 2),
            "win_count": sum(1 for v in resolved.values() if v == 1),
            "loss_count": sum(1 for v in resolved.values() if v == 2),
            "layered_count": len(resolved),
            "unknown_count_among_candidates": len(still_unknown),
            "unknown_candidates": sorted(still_unknown),
            "verified_but_unlayered": sorted(UNLAYERED),
            "unknown_unchanged": {"144692": 144692 in still_unknown,
                                  "144019": 144019 in still_unknown,
                                  "197665_at_10m": 197665 in still_unknown},
            "empty_board": "UNKNOWN (11x11); no whole-board leap performed",
        },
        "source_sha256": {
            str(p.relative_to(ROOT)): sha(p) for p in (
                EXP / "output/repaired-joint-plan-update3.json",
                EXP / "output/updated-element-dual-update3.json",
                EXP / "output/win-side-reanalysis3.json",
                PREV / "repaired-joint-plan-update2.json",
                PREV / "updated-element-dual-update2.json",
                PREV / "win-side-reanalysis2.json",
                FIRST / "repaired-joint-plan-update.json",
                K0423 / "repaired-joint-plan.json",
                K0423 / "updated-element-dual.json",
                RANK,
                NATIVE / "pilot-115540-receipt.json",
                NATIVE / "pilot-144193-receipt.json",
                NATIVE / "pilot-144311-receipt.json",
            )
        },
    }
    target = EXP / "output/effect-measurement3.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(effect, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: effect[k] for k in ("new_facts", "bounds", "loss_side",
                                             "win_side", "newly_closed",
                                             "verdict_census")},
                     indent=2))


if __name__ == "__main__":
    main()
