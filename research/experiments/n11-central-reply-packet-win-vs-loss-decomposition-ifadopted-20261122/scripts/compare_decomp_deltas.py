#!/usr/bin/env python3
"""WIN-vs-LOSS packet decomposition delta extractor (fail-closed, analysis-only).

Reads the published baseline refresh summary, the joint 25-row packet (P25)
summary, the packet-minus-f017 (P24) summary, and this experiment's three
decomposition scenario summaries (P4 WINs-only, P17 batch12264-LOSS-only,
P21 all-21-LOSS), and emits output/decomp-deltas.json with the
machine-computed table and gates.

The increments are read-only what-if analysis inputs; no verdict is consumed
and no class/root status is claimed. 11x11 stays UNKNOWN.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]

BASE = ROOT / "research/experiments/n11-central-reply-23963-closure-reaudit-20261122/output/refresh-summary.json"
P24 = ROOT / "research/experiments/n11-central-reply-packet-minus-f017-ifadopted-20261122/output/refresh-summary.json"
P25 = ROOT / "research/experiments/n11-central-reply-joint-4win-adoption-ifadopted-20261122/output/refresh-summary.json"
P4 = EXP / "p4/output/refresh-summary.json"
P17 = EXP / "p17/output/refresh-summary.json"
P21 = EXP / "p21/output/refresh-summary.json"
OUT = EXP / "output/decomp-deltas.json"

METRICS = [
    ("excluded_now", lambda s: s["class_status_counts"]["excluded_now"]),
    ("free_now", lambda s: s["class_status_counts"]["free_now"]),
    ("unknown_classes", lambda s: s["class_status_counts"]["unknown"]),
    ("update8_remaining_now", lambda s: s["frozen_update8_refresh"]["remaining_now"]),
    ("update8_resolved_count", lambda s: s["frozen_update8_refresh"]["resolved_count"]),
    ("update8_win_hit_groups", lambda s: len(s["frozen_update8_refresh"]["win_hit_groups"])),
    ("joint_greedy_union_size", lambda s: s["joint_greedy"]["greedy_union_size"]),
    ("probe_worklist_total", lambda s: s["worklist_total"]),
    ("baseline_root27_free_thirds", lambda s: s["roots"][0]["free_thirds_now"]),
]

# Exact measured scenario values (published in this experiment's README).
PINNED = {
    "excluded_now": {"base": 23, "P4": 37, "P17": 23, "P21": 23, "P24": 34, "P25": 37},
    "free_now": {"base": 33, "P4": 33, "P17": 33, "P21": 33, "P24": 33, "P25": 33},
    "unknown_classes": {"base": 34503, "P4": 34489, "P17": 34503, "P21": 34503, "P24": 34492, "P25": 34489},
    "update8_remaining_now": {"base": 31838, "P4": 31709, "P17": 31821, "P21": 31818, "P24": 31743, "P25": 31709},
    "update8_resolved_count": {"base": 21, "P4": 24, "P17": 38, "P21": 41, "P24": 43, "P25": 44},
    "update8_win_hit_groups": {"base": 0, "P4": 15, "P17": 0, "P21": 0, "P24": 9, "P25": 15},
    "joint_greedy_union_size": {"base": 35617, "P4": 35616, "P17": 36989, "P21": 36985, "P24": 36984, "P25": 36984},
    "probe_worklist_total": {"base": 65213, "P4": 65208, "P17": 65192, "P21": 65188, "P24": 65184, "P25": 65183},
    "baseline_root27_free_thirds": {"base": 119, "P4": 119, "P17": 119, "P21": 119, "P24": 119, "P25": 119},
}

WIN_HIT_CLASSES = {
    "P4": {12264: 6, 16757: 5, 20421: 4},
    "P17": {}, "P21": {}, "P24": {16757: 5, 20421: 4},
    "P25": {12264: 6, 16757: 5, 20421: 4},
}


def main():
    loads = {}
    for name, p in (("base", BASE), ("P4", P4), ("P17", P17), ("P21", P21), ("P24", P24), ("P25", P25)):
        if not p.is_file():
            raise SystemExit(f"missing summary {name}: {p}")
        loads[name] = json.loads(p.read_text())

    failures = []
    table = {}
    for m, fn in METRICS:
        table[m] = {name: fn(s) for name, s in loads.items()}
        for name, val in table[m].items():
            if val != PINNED[m][name]:
                failures.append(f"pin {m}/{name}: {val} != published {PINNED[m][name]}")

    def delta(m, name):
        return table[m][name] - table[m]["base"]

    # gate 1: per-root free coverage identical to baseline in every scenario
    basefree = {r["origin_first"]: r["free_thirds_now"] for r in loads["base"]["roots"]}
    for name in ("P4", "P17", "P21", "P24", "P25"):
        if {r["origin_first"]: r["free_thirds_now"] for r in loads[name]["roots"]} != basefree:
            failures.append(f"per-root free coverage changed in {name}")

    # gate 2: win-hit class multisets
    for name, expect in WIN_HIT_CLASSES.items():
        got = {}
        for g in loads[name]["frozen_update8_refresh"]["win_hit_groups"]:
            got[g["s4_class_index"]] = got.get(g["s4_class_index"], 0) + 1
        if got != expect:
            failures.append(f"win-hit class multiset {name}: {got} != {expect}")

    # gate 3: LOSS-only scenarios do not change class status counts
    for name in ("P17", "P21"):
        for m in ("excluded_now", "free_now", "unknown_classes"):
            if table[m][name] != table[m]["base"]:
                failures.append(f"LOSS-only scenario {name} changed {m}")

    # gate 4: the greedy plan-cost split
    if delta("joint_greedy_union_size", "P25") != delta("joint_greedy_union_size", "P4") + delta("joint_greedy_union_size", "P21"):
        failures.append("greedy: P25 delta != P4 delta + P21 delta")
    if delta("joint_greedy_union_size", "P17") != 1372:
        failures.append("greedy: P17 delta != +1372 (the batch12264 f-LOSS rows alone)")
    if delta("joint_greedy_union_size", "P4") != -1:
        failures.append("greedy: P4 delta != -1 (the four WINs are plan-cost neutral)")
    if table["joint_greedy_union_size"]["P24"] != table["joint_greedy_union_size"]["P25"]:
        failures.append("greedy: P24 != P25")

    # gate 5: excluded/unknown/whg are WIN-driven and identical P4 vs P25
    for m in ("excluded_now", "unknown_classes", "update8_win_hit_groups", "update8_remaining_now"):
        if table[m]["P4"] != table[m]["P25"]:
            failures.append(f"{m}: P4 != P25 (expected WIN-driven equality)")
    if delta("excluded_now", "P24") != 11:
        failures.append("excluded_now: P24 delta != +11 (= P25's +14 minus f017's +3)")

    # gate 6: rem8 non-additivity is exactly the measured subsumption
    #   delta(P4) + delta(P21) - delta(P25) = -129 - 20 + 129 = -20:
    #   the LOSS-side -20 remaining reduction is subsumed by the WIN-side resolutions.
    overlap = delta("update8_remaining_now", "P4") + delta("update8_remaining_now", "P21") - delta("update8_remaining_now", "P25")
    if overlap != -20:
        failures.append(f"rem8 WIN/LOSS subsumption != -20 (got {overlap})")
    add_ok = [m for m, _ in METRICS
              if m != "update8_remaining_now"
              and delta(m, "P25") != delta(m, "P4") + delta(m, "P21")]
    failures.extend(f"{m}: P25 delta not additive P4+P21" for m in add_ok)

    out = {
        "schema": "n11-central-reply-packet-win-vs-loss-decomposition-ifadopted-v1",
        "interpretation_guard": "IF-ADOPTED what-if analysis only; no verdict consumed; no class/root/closure claim; 11x11 UNKNOWN",
        "metric_table": table,
        "deltas_vs_base": {m: {name: delta(m, name) for name in ("P4", "P17", "P21", "P24", "P25")} for m, _ in METRICS},
        "gates": {
            "per_root_free_coverage": "identical to baseline in all five scenarios (machine-verified)" if not any("per-root" in f for f in failures) else "FAILED",
            "win_hit_class_multisets": "as pinned (P4=P25 {12264:6,16757:5,20421:4}; P17=P21 {}; P24 {16757:5,20421:4})" if not any("win-hit" in f for f in failures) else "FAILED",
            "loss_only_class_status_unchanged": "P17/P21 leave excluded/free/unknown at baseline (machine-verified)" if not any("LOSS-only" in f for f in failures) else "FAILED",
            "greedy_split": "joint +1367 == P17(+1372, the 17 batch12264 f-LOSS rows) + P4(-1, the four WINs are plan-cost neutral) + non-f-LOSS rows(-4); P24 == P25" if not any("greedy" in f for f in failures) else "FAILED",
            "win_driven_equality_P4_P25": "excluded_now/unknown/win-hit-groups/update8-remaining equal in P4 and P25 (WIN-driven)" if not any("P4 != P25" in f for f in failures) else "FAILED",
            "rem8_overlap_measured": "delta(P4)+delta(P21)-delta(P25) == 20 (WIN-side resolutions subsume the LOSS-side remaining reduction)" if not any("overlap" in f for f in failures) else "FAILED",
            "additivity_P4_plus_P21": "additive for 8 of 9 metrics; update8_remaining_now is the measured exception (overlap 20)",
        },
        "constraint_note": ("the closure-classes ranking is a scheduling quantity and does NOT carry class status; "
                            "in every packet scenario the ranked top-5 are the refuted quartet (16757/12264/20421/16371) plus 30345, "
                            "and the first clean closure candidate is rank 6 (class 5473, unknown 51)"),
        "erratum_note": ("this decomposition RETRACTS the Part H mechanism attribution: the +1367 joint greedy increase is NOT dominated by f017's adoption; "
                         "it is driven entirely by the 17 batch12264 LOSS rows (P17 alone +1372), while adopting all four WINs is plan-cost neutral (P4 -1). "
                         "Per-root free coverage never changed in any scenario." ),
    }
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"gate_failures": failures, "output": str(OUT)}, indent=1))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
