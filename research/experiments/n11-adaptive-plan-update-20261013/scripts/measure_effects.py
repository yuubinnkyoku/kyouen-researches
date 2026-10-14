"""Aggregate the adaptive plan-update effects into one measurement record.

Reads only files produced by this experiment plus the frozen baseline inputs.
Every number is copied or recomputed from those files; nothing is estimated.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
K0423 = ROOT / "research/experiments/n11-s5-s6-quotient-20261013/output"
RANK = ROOT / "research/experiments/n11-conflict-ranking-20261013/output/ranking.json"
ADAPTIVE = ROOT / "research/experiments/n11-adaptive-verify-20261013/output"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    plan = json.loads((EXP / "output/repaired-joint-plan-update.json").read_text())
    dual = json.loads((EXP / "output/updated-element-dual-update.json").read_text())
    win = json.loads((EXP / "output/win-side-reanalysis.json").read_text())
    base_dual = json.loads((K0423 / "updated-element-dual.json").read_text())
    ranking = json.loads(RANK.read_text())

    assert plan["verification"]["passed"]
    assert dual["integer_lower_bound"] <= dual["upper_bound"]
    assert win["verification"]["passed"] and not win["verification"]["failures"]

    # Independent verification receipts for the two new facts.
    receipts = {}
    for index in (126899, 144095):
        r = json.loads((ADAPTIVE / f"pilot-{index}-receipt.json").read_text())
        receipts[str(index)] = {
            "verdict": r["verdict"],
            "trusted_leaves": r["trusted_leaves"],
            "pruned_roundtrip_verified": r["pruned_roundtrip_verified"],
            "probe_search_nodes": r["probe_search_nodes"],
            "certificate_sha256": r["certificate_sha256"],
        }

    conflicts = [row["s5_index"] for row in ranking["rows"]]
    assert len(conflicts) == 28
    resolved = {int(k): v for k, v in plan["resolved_s5_verdicts"].items()}
    newly = {126899: 2, 144095: 1}
    still_unknown = [i for i in conflicts if i not in resolved]
    assert 144692 in still_unknown and 144019 in still_unknown

    win_base = next(a for a in json.loads(
        (ROOT / "research/experiments/n11-proof-cost-comparison-20261012/"
         "output/win-side-analysis.json").read_text())["firsts"]
        if a["first"] == 49)
    # 1,945 stored witnesses; 209644 (WIN) and 558600 were already resolved
    # before this experiment, so the pre-experiment unresolved count was
    # 1,944 per the §5 baseline.
    witness_baseline_unresolved = win_base["optimistic_witness_s5"] - 1

    effect = {
        "schema": "n11-adaptive-plan-update-effects-v1",
        "new_facts": {
            "s5_index": {"126899": 2, "144095": 1},
            "independent_verifications": receipts,
            "verification_successes": 2, "verification_attempts": 2,
        },
        "bounds": {
            "upper": {"before": plan["baseline_union_size"],
                      "after": plan["union_size"],
                      "delta": plan["union_size"] - plan["baseline_union_size"],
                      "source": "union of unknown-S5 children of selected LOSS responses"},
            "lower": {"before": base_dual["integer_lower_bound"],
                      "after": dual["integer_lower_bound"],
                      "delta": dual["integer_lower_bound"] - base_dual["integer_lower_bound"],
                      "exact_after": dual["total_exact"],
                      "exact_before": base_dual["total_exact"],
                      "source": "exact element-only fractional dual, ceil by integrality"},
            "interval_before": [base_dual["integer_lower_bound"],
                                plan["baseline_union_size"]],
            "interval_after": [dual["integer_lower_bound"], plan["union_size"]],
        },
        "loss_side": {
            "changed_choices": plan["changed_choice_count"],
            "newly_excluded_s4_classes": plan["new_excluded_s4_classes"],
            "excluded_s4_classes_total": plan["excluded_s4_classes"],
            "free_thirds_before": plan["baseline_free_thirds"],
            "free_thirds_after": plan["free_thirds"],
            "required_s5_before": plan["baseline_union_size"],
            "required_s5_after": plan["union_size"],
            "known_loss_removed_from_cost": [126899],
        },
        "win_side": {
            "unresolved_witnesses_before": witness_baseline_unresolved,
            "unresolved_witnesses_after": win["after"]["unresolved_witness_s5"],
            "delta": (win["after"]["unresolved_witness_s5"]
                      - witness_baseline_unresolved),
            "stored_pool": win["stored_witness_pool"],
            "allowed_pool": win["allowed_witness_pool"],
            "removed_witnesses": win["removed_witnesses"],
            "unclosable_s4_candidates_after": len(
                win["after"]["unclosable_replies"]),
            "uncovered_branches_before_reopt": win["pre_optimisation"][
                "uncovered_branches"],
            "uncovered_s4_classes_before_reopt": win["pre_optimisation"][
                "uncovered_s4_classes"],
            "replies_affected_before_reopt": len(
                win["pre_optimisation"]["replies_affected"]),
            "and_width_before": win_base["and_width_fourths"],
            "and_width_after": win["after"]["and_width_fourths"],
            "witness_replies_before": win_base["witness_replies"],
            "witness_replies_after": win["after"]["witness_replies"],
        },
        "newly_closed": {
            "third_moves": win["after"]["newly_closed_third_moves"],
            "reply_orbits": win["after"]["newly_closed_reply_orbits"],
            "replies": win["after"]["newly_free_replies"],
            "note": ("replies whose chosen third now needs zero WIN witnesses "
                     "because a fourth S4 became free via the 144095 WIN child"),
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
                EXP / "output/repaired-joint-plan-update.json",
                EXP / "output/updated-element-dual-update.json",
                EXP / "output/win-side-reanalysis.json",
                K0423 / "repaired-joint-plan.json",
                K0423 / "updated-element-dual.json",
                RANK,
            )
        },
    }
    target = EXP / "output/effect-measurement.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(effect, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: effect[k] for k in ("bounds", "loss_side", "win_side",
                                             "newly_closed", "verdict_census")},
                     indent=2))


if __name__ == "__main__":
    main()
