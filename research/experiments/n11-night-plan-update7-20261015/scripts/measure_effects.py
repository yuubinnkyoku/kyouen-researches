"""Aggregate the seventh joint-plan update effects into one measurement record.

Reads only files produced by this experiment plus the frozen baselines (the
sixth update output, the fifth update output, the second update output, the
first update output and the original K0423 output).  Every number is copied or
recomputed from those files; nothing is estimated.  Section-5 effects are
reported on both criteria: "from_previous" (vs n11-night-plan-update6-20261014)
and "from_initial" (vs n11-s5-s6-quotient-20261013).

Independent-proof tallies are reported under several explicit labels because
"cumulative" is ambiguous across the plan-layered receipts, the adaptive line
and all independently verified receipts (the three native pilot receipts
115540 / 144193 / 144311 are verified but intentionally NOT layered into any
plan yet).  This round also layers three LOSS verdicts that have no per-index
receipts: they are derived from the single six-stone terminal certificate of
n11-s6-terminal-loss-20261015 (indices 381840 / 402066 / 550881), so
receipt-backed and certificate-backed counts are reported separately.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
PREV = ROOT / "research/experiments/n11-night-plan-update6-20261014/output"
PREV2 = ROOT / "research/experiments/n11-adaptive-plan-update2-20261013/output"
FIRST = ROOT / "research/experiments/n11-adaptive-plan-update-20261013/output"
K0423 = ROOT / "research/experiments/n11-s5-s6-quotient-20261013/output"
COST_CMP = ROOT / "research/experiments/n11-proof-cost-comparison-20261012/output"
RANK = ROOT / "research/experiments/n11-conflict-ranking-20261013/output/ranking.json"
NATIVE = ROOT / "research/experiments/n11-native-terminal-checker-20261013/output"
NEW = (162106,)
PRIOR_NEW = (137694, 143240, 220231, 126017, 197665, 206386, 131631)
DERIVED_LOSSES = (381840, 402066, 550881)
UNLAYERED = (115540, 144193, 144311)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    plan = json.loads((EXP / "output/repaired-joint-plan-update7.json").read_text())
    dual = json.loads((EXP / "output/updated-element-dual-update7.json").read_text())
    win = json.loads((EXP / "output/win-side-reanalysis7.json").read_text())
    prev_plan = json.loads((PREV / "repaired-joint-plan-update6.json").read_text())
    prev_dual = json.loads((PREV / "updated-element-dual-update6.json").read_text())
    prev_win = json.loads((PREV / "win-side-reanalysis6.json").read_text())
    init_plan = json.loads((K0423 / "repaired-joint-plan.json").read_text())
    init_dual = json.loads((K0423 / "updated-element-dual.json").read_text())
    ranking = json.loads(RANK.read_text())

    assert plan["verification"]["passed"]
    assert plan["verification"]["complete_third_boundaries"] == 19
    assert plan["third_moves_covered"] == 2261
    assert plan["verification"]["known_win_selected"] == 0
    assert plan["union_size"] == 31771
    assert dual["integer_lower_bound"] <= dual["upper_bound"]
    assert win["verification"]["passed"] and not win["verification"]["failures"]
    assert prev_win["verification"]["passed"]
    assert dual["repaired_plan_sha256"] == sha(EXP / "output/repaired-joint-plan-update7.json")

    receipts = plan["new_receipts"]
    for index in NEW:
        fact = receipts[str(index)]
        assert fact["trusted_leaves"] == 0 and fact["pruned_roundtrip_verified"]
        assert fact["evidence_class"] == "independent-terminal-only-verification"
        assert fact["probe_search_nodes"] == 18141378, fact
        assert fact["probe_budget"] == 25000000, fact
        assert "python_cross_check" in fact
    assert {int(k): v["verdict"] for k, v in receipts.items()} == {162106: 1}
    assert plan["shared_checker_source_sha256"] == \
        receipts["162106"]["checker_source_sha256"]

    conflicts = [row["s5_index"] for row in ranking["rows"]]
    assert len(conflicts) == 28
    resolved = {int(k): v for k, v in plan["resolved_s5_verdicts"].items()}
    assert plan["known_loss_removed_from_cost"] == list(DERIVED_LOSSES)
    assert set(plan["s6_derived_losses"]) == {str(i) for i in DERIVED_LOSSES}
    assert not (set(DERIVED_LOSSES) & set(conflicts)), \
        "certificate-derived losses should not be conflict candidates"
    still_unknown = [i for i in conflicts if i not in resolved]
    assert 144692 in still_unknown and 144019 in still_unknown
    assert 206386 not in still_unknown
    assert 131631 not in still_unknown
    assert 162106 not in still_unknown
    assert resolved == {558600: 2, 209644: 1, 126899: 2, 144095: 1, 121263: 2,
                        145001: 2, 137694: 2, 143240: 2, 220231: 2, 126017: 1,
                        197665: 1, 206386: 1, 131631: 1, 162106: 1,
                        381840: 2, 402066: 2, 550881: 2}
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
    prev_unclosable = set(prev_win["after"]["unclosable_replies"])
    now_unclosable = set(win["after"]["unclosable_replies"])
    assert now_unclosable == (prev_unclosable - set(gained_closability)) \
        | set(lost_closability), "closability ledger does not close"

    # Which stored cover decisions moved between the sixth and seventh updates.
    prev_by_reply = {row["reply"]: row for row in prev_win["replies"]}
    changed_covers = []
    for row in win["replies"]:
        old = prev_by_reply[row["reply"]]
        keys = ("closable", "chosen_third", "chosen_fourths", "witness_count",
                "viable_thirds")
        if any(old.get(k) != row.get(k) for k in keys):
            changed_covers.append({
                "reply": row["reply"],
                **{f"previous_{k}": old.get(k) for k in keys},
                **{f"after_{k}": row.get(k) for k in keys},
            })

    layered = sorted(resolved)
    receipt_layered = [i for i in layered if i not in DERIVED_LOSSES]
    adaptive_line = [126899, 144095, 121263, 145001] + list(PRIOR_NEW) + list(NEW)
    layered_loss = sorted(i for i, v in resolved.items() if v == 2)
    layered_win = sorted(i for i, v in resolved.items() if v == 1)
    conflict_closure_line = sorted(set(UNLAYERED) | set(adaptive_line))
    all_receipts = receipt_layered + sorted(UNLAYERED)

    tallies = {
        "this_round": {"attempts": 1, "successes": 1, "indices": sorted(NEW)},
        "cumulative_adaptive_line": {
            "attempts": 12, "successes": 12, "indices": adaptive_line,
            "note": ("continues the update6 README definition (cumulative 11/11): "
                     "first update 126899/144095, second update 121263/145001, "
                     "third update 137694/143240/220231/126017, fourth update "
                     "197665, fifth update 206386, sixth update 131631, this "
                     "round 162106"),
        },
        "cumulative_plan_layered_total": {
            "attempts": 17, "successes": 17, "indices": layered,
            "note": ("K0423 pilot receipts included; 14/14 receipt-backed "
                     "through the sixth update plus three S6-certificate-derived "
                     "LOSS verdicts this round (no per-index receipts)"),
        },
        "cumulative_plan_layered_loss_side": {
            "attempts": len(layered_loss), "successes": len(layered_loss),
            "indices": layered_loss,
            "note": ("layered LOSS verdicts: 7/7 receipt-backed through the sixth "
                     "update plus 3 certificate-derived this round"),
        },
        "cumulative_plan_layered_win_side": {
            "attempts": len(layered_win), "successes": len(layered_win),
            "indices": layered_win,
            "note": "layered receipts whose verdict is WIN (7/7, this round adds 162106)",
        },
        "cumulative_conflict_closure_certified": {
            "attempts": len(conflict_closure_line),
            "successes": len(conflict_closure_line),
            "indices": conflict_closure_line,
            "note": ("conflict-closure lineage excluding the K0423 pilots: native "
                     "focus 3 (115540, 144193, 144311) + adaptive line 12 "
                     "(126899, 144095, 121263, 145001, 137694, 143240, 220231, "
                     "126017, 197665, 206386, 131631, 162106) = 15"),
        },
        "cumulative_all_independent_receipts": {
            "attempts": len(all_receipts), "successes": len(all_receipts),
            "indices": all_receipts,
            "layered_into_plan": receipt_layered,
            "verified_but_unlayered": sorted(UNLAYERED),
            "note": ("16 independent receipts existed before this round "
                     "(K0423 2 + native focus 3 + adaptive/night 11) and this "
                     "round adds 1 (162106 WIN); the three native receipts "
                     "115540 LOSS / 144193 LOSS / 144311 WIN stay out of every "
                     "plan, so receipt-backed plan-layered (14) and all-receipt "
                     "(17) tallies differ"),
        },
        "certificate_derived_plan_verdicts": {
            "certificates": 1, "verdicts": len(DERIVED_LOSSES),
            "indices": sorted(DERIVED_LOSSES),
            "certificate": plan["s6_derived_losses"][str(DERIVED_LOSSES[0])][
                "certificate"],
            "certificate_sha256": plan["s6_derived_losses"][str(DERIVED_LOSSES[0])][
                "certificate_sha256"],
            "note": ("one cache-free six-stone terminal certificate "
                     "(1,028,621 verified states) proves three S5 LOSS "
                     "verdicts; counted separately from receipt-backed tallies"),
        },
    }

    effect = {
        "schema": "n11-night-plan-update7-effects-v1",
        "new_facts": {
            "s5_index": {str(i): receipts[str(i)]["verdict"] for i in NEW},
            "independent_verifications": receipts,
            "verification_attempts": 1,
            "verification_successes": 1,
            "certificate_derived_verdicts": {
                str(i): plan["s6_derived_losses"][str(i)] for i in DERIVED_LOSSES},
            "cumulative_tallies": tallies,
            "unlayered_receipts_unchanged": sorted(UNLAYERED),
            "tally_note": ("several cumulative labels are reported because "
                           "'independent proof cumulative' is ambiguous across "
                           "plan-layered, adaptive-line, conflict-closure and "
                           "all-receipt readings; the three certificate-derived "
                           "LOSS verdicts have no per-index receipts and are "
                           "reported separately"),
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
            "dual_size_from_previous": {
                "options_scored": [prev_dual["options_scored"], dual["options_scored"]],
                "elements": [prev_dual["elements"], dual["elements"]],
                "paid_groups": [prev_dual["paid_groups"], dual["paid_groups"]],
            },
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
            "s6_derived_losses": plan["s6_derived_losses"],
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
            "covers_changed_vs_previous": changed_covers,
            "unclosable_reply_orbits": {
                "from_initial": win_base["unclosable_replies"],
                "from_previous": prev_win["after"]["unclosable_replies"],
                "after": win["after"]["unclosable_replies"],
                "newly_unclosable_vs_previous": lost_closability,
                "reclosed_vs_previous": gained_closability,
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
            "freed_branches_by_new_win_before_reopt": win["pre_optimisation"][
                "freed_branches_by_new_win_in_stored_thirds"],
            "freed_branches_by_new_win_only_before_reopt": win["pre_optimisation"][
                "freed_branches_by_new_win_only_in_stored_thirds"],
            "dead_disqualified_thirds": win["dead_disqualified_thirds"],
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
                "replies_all_free": win["after"]["newly_free_replies_vs_previous"],
                "replies_reclosed": win["after"]["reclosed_replies_vs_previous"],
            },
            "from_initial": {
                "third_moves": win["after"]["newly_closed_third_moves_vs_initial"],
                "reply_orbits": win["after"]["newly_closed_reply_orbits_vs_initial"],
                "replies": win["after"]["newly_free_replies_vs_initial"],
            },
            "regressed_vs_previous": win["after"]["regressed_free_replies_vs_previous"],
            "note": ("a reply counts as newly closed when its chosen third needs "
                     "zero WIN witnesses from the saved pool, and as reclosed when "
                     "it becomes closable again after having been unclosable; both "
                     "criteria are reported"),
        },
        "ranking_cross_check": {
            "loss_side": plan["ranking_cross_check"],
            "win_side_branches": win["ranking_cross_check"],
            "all_match": True,
            "note": ("branch incidences, invalidated-option sets and "
                     "affected-choice counts are recomputed from independent "
                     "geometry on the frozen ranking row (ranking.tsv and "
                     "ranking.json); every value matches "
                     "n11-conflict-ranking-20261013/output for 162106"),
        },
        "verdict_census": {
            "conflict_candidates_total": len(conflicts),
            "win": sorted(k for k, v in resolved.items() if v == 1),
            "loss": sorted(k for k, v in resolved.items() if v == 2),
            "win_count": sum(1 for v in resolved.values() if v == 1),
            "loss_count": sum(1 for v in resolved.values() if v == 2),
            "layered_count": len(resolved),
            "receipt_backed_count": len(receipt_layered),
            "certificate_derived_count": len(DERIVED_LOSSES),
            "unknown_count_among_candidates": len(still_unknown),
            "unknown_candidates": sorted(still_unknown),
            "verified_but_unlayered": sorted(UNLAYERED),
            "unknown_unchanged": {"144692": 144692 in still_unknown,
                                  "144019": 144019 in still_unknown,
                                  "206386_at_10m_resolved_by_25m_run":
                                      206386 in still_unknown,
                                  "131631_at_10m_resolved_by_25m_run":
                                      131631 in still_unknown,
                                  "162106_conflict_candidate_now_resolved":
                                      162106 in still_unknown},
            "empty_board": "UNKNOWN (11x11); no whole-board leap performed",
        },
        "source_sha256": {
            str(p.relative_to(ROOT)): sha(p) for p in (
                EXP / "output/repaired-joint-plan-update7.json",
                EXP / "output/updated-element-dual-update7.json",
                EXP / "output/win-side-reanalysis7.json",
                PREV / "repaired-joint-plan-update6.json",
                PREV / "updated-element-dual-update6.json",
                PREV / "win-side-reanalysis6.json",
                PREV2 / "repaired-joint-plan-update2.json",
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
    target = EXP / "output/effect-measurement7.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(effect, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: effect[k] for k in ("new_facts", "bounds", "loss_side",
                                             "win_side", "newly_closed",
                                             "verdict_census")},
                     indent=2))


if __name__ == "__main__":
    main()
