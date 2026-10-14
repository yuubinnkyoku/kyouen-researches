"""Aggregate the second joint-plan update effects into one measurement record.

Reads only files produced by this experiment plus the frozen baselines (the
first update output and the original K0423 output).  Every number is copied or
recomputed from those files; nothing is estimated.  §5 effects are reported on
both criteria: "from_previous" (vs n11-adaptive-plan-update-20261013) and
"from_initial" (vs n11-s5-s6-quotient-20261013).
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
PREV = ROOT / "research/experiments/n11-adaptive-plan-update-20261013/output"
K0423 = ROOT / "research/experiments/n11-s5-s6-quotient-20261013/output"
COST_CMP = ROOT / "research/experiments/n11-proof-cost-comparison-20261012/output"
RANK = ROOT / "research/experiments/n11-conflict-ranking-20261013/output/ranking.json"
PROBE = ROOT / "research/experiments/n11-adaptive-probe-20261013/output"
NEW = (121263, 145001)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    plan = json.loads((EXP / "output/repaired-joint-plan-update2.json").read_text())
    dual = json.loads((EXP / "output/updated-element-dual-update2.json").read_text())
    win = json.loads((EXP / "output/win-side-reanalysis2.json").read_text())
    prev_plan = json.loads((PREV / "repaired-joint-plan-update.json").read_text())
    prev_dual = json.loads((PREV / "updated-element-dual-update.json").read_text())
    prev_win = json.loads((PREV / "win-side-reanalysis.json").read_text())
    init_plan = json.loads((K0423 / "repaired-joint-plan.json").read_text())
    init_dual = json.loads((K0423 / "updated-element-dual.json").read_text())
    ranking = json.loads(RANK.read_text())
    manifest = json.loads((PROBE / "adaptive10m-manifest.json").read_text())

    assert plan["verification"]["passed"]
    assert plan["verification"]["complete_third_boundaries"] == 19
    assert plan["third_moves_covered"] == 2261
    assert plan["verification"]["known_win_selected"] == 0
    assert dual["integer_lower_bound"] <= dual["upper_bound"]
    assert win["verification"]["passed"] and not win["verification"]["failures"]
    assert prev_win["verification"]["passed"]

    # Independent terminal verification receipts for this round's two facts.
    receipts = {}
    nodes_by_index = {row["s5_index"]: row["nodes"] for row in manifest["rows"]}
    for index in NEW:
        r = json.loads((PROBE / f"adaptive-{index}-receipt.json").read_text())
        receipts[str(index)] = {
            "verdict": r["verdict"],
            "trusted_leaves": r["trusted_leaves"],
            "pruned_roundtrip_verified": r["pruned_roundtrip_verified"],
            "manifest_trace_sha256_match": r["manifest_trace_sha256_match"],
            "probe_search_nodes": nodes_by_index[index],
            "certificate_sha256": r["certificate_sha256"],
            "certificate_bytes": r["certificate_bytes"],
        }
        assert r["verdict"] == 2 and r["trusted_leaves"] == 0
        assert r["pruned_roundtrip_verified"] and r["manifest_trace_sha256_match"]

    conflicts = [row["s5_index"] for row in ranking["rows"]]
    assert len(conflicts) == 28
    resolved = {int(k): v for k, v in plan["resolved_s5_verdicts"].items()}
    assert plan["known_loss_removed_from_cost"] == sorted(NEW)
    still_unknown = [i for i in conflicts if i not in resolved]
    assert 144692 in still_unknown and 144019 in still_unknown
    assert resolved == {558600: 2, 209644: 1, 126899: 2, 144095: 1,
                        121263: 2, 145001: 2}

    win_base = next(a for a in json.loads(
        (COST_CMP / "win-side-analysis.json").read_text())["firsts"]
        if a["first"] == 49)
    # 1,945 stored witnesses; 209644 (WIN) was resolved before the first update,
    # so the pre-first-update unresolved count was 1,944 per the §5 baseline.
    witness_baseline_unresolved = win_base["optimistic_witness_s5"] - 1

    effect = {
        "schema": "n11-adaptive-plan-update2-effects-v1",
        "new_facts": {
            "s5_index": {"121263": 2, "145001": 2},
            "independent_verifications": receipts,
            "verification_attempts": 2,
            "verification_successes": 2,
            "cumulative_adaptive_line": {
                "attempts": 4, "successes": 4,
                "indices": [126899, 144095, 121263, 145001],
                "note": "first-update line (126899, 144095) plus this round",
            },
            "cumulative_with_k0423_pilot_receipts": {
                "attempts": 6, "successes": 6,
                "indices": [558600, 209644, 126899, 144095, 121263, 145001],
            },
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
        "verdict_census": {
            "conflict_candidates_total": len(conflicts),
            "win": sorted(k for k, v in resolved.items() if v == 1),
            "loss": sorted(k for k, v in resolved.items() if v == 2),
            "win_count": sum(1 for v in resolved.values() if v == 1),
            "loss_count": sum(1 for v in resolved.values() if v == 2),
            "unknown_count_among_candidates": len(still_unknown),
            "unknown_candidates": sorted(still_unknown),
            "unknown_unchanged": {"144692": 144692 in still_unknown,
                                  "144019": 144019 in still_unknown},
            "empty_board": "UNKNOWN (11x11); no whole-board leap performed",
        },
        "source_sha256": {
            str(p.relative_to(ROOT)): sha(p) for p in (
                EXP / "output/repaired-joint-plan-update2.json",
                EXP / "output/updated-element-dual-update2.json",
                EXP / "output/win-side-reanalysis2.json",
                PREV / "repaired-joint-plan-update.json",
                PREV / "updated-element-dual-update.json",
                PREV / "win-side-reanalysis.json",
                K0423 / "repaired-joint-plan.json",
                K0423 / "updated-element-dual.json",
                RANK,
                PROBE / "adaptive10m-manifest.json",
            )
        },
    }
    target = EXP / "output/effect-measurement2.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(effect, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: effect[k] for k in ("new_facts", "bounds", "loss_side",
                                             "win_side", "newly_closed",
                                             "verdict_census")},
                     indent=2))


if __name__ == "__main__":
    main()
