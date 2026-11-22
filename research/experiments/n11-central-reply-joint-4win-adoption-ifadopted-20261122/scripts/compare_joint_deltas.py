#!/usr/bin/env python3
"""Joint 4-WIN adoption IF-ADOPTED delta extractor (fail-closed, analysis-only).

Reads the published refresh summaries (baseline re-audit + the four single
WIN if-adopted analyses) and this experiment's joint refresh summary, and
emits output/joint-deltas.json with the machine-computed delta table.

The joint increment is the 25-row unconsumed closure-lane packet (4 WINs
b018/d002/e002/f017 + 21 LOSS rows), NOT consumed: this is a what-if
computation only. Verdicts are unchanged; 11x11 stays UNKNOWN.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]

BASE = ROOT / "research/experiments/n11-central-reply-23963-closure-reaudit-20261122/output/refresh-summary.json"
B018 = ROOT / "research/experiments/n11-central-reply-16757-ifadopted-analysis-20261122/output/refresh-summary.json"
D002 = ROOT / "research/experiments/n11-central-reply-20421-win-d002-ifadopted-20261122/output/refresh-summary.json"
E002 = ROOT / "research/experiments/n11-central-reply-16371-win-e002-ifadopted-20261122/output/refresh-summary.json"
F017 = ROOT / "research/experiments/n11-central-reply-12264-win-f017-ifadopted-20261122/output/refresh-summary.json"
JOINT = EXP / "output/refresh-summary.json"
OUT = EXP / "output/joint-deltas.json"

METRICS = [
    ("excluded_now", lambda s: s["class_status_counts"]["excluded_now"]),
    ("free_now", lambda s: s["class_status_counts"]["free_now"]),
    ("unknown_classes", lambda s: s["class_status_counts"]["unknown"]),
    ("update8_remaining_now", lambda s: s["frozen_update8_refresh"]["remaining_now"]),
    ("update8_resolved_count", lambda s: s["frozen_update8_refresh"]["resolved_count"]),
    ("update8_win_hit_groups", lambda s: len(s["frozen_update8_refresh"]["win_hit_groups"])),
    ("joint_greedy_union_size", lambda s: s["joint_greedy"]["greedy_union_size"]),
    ("probe_worklist_total", lambda s: s["worklist_total"]),
    ("closure_classes_first_unknown<=12", lambda s: len(s["closure_classes_first"])),
    ("closure_classes_count", lambda s: s["closure_classes_count"]),
    ("baseline_root27_free_thirds", lambda s: s["roots"][0]["free_thirds_now"]),
]


def main():
    loads = {}
    for name, p in (("base", BASE), ("b018", B018), ("d002", D002), ("e002", E002), ("f017", F017), ("joint", JOINT)):
        if not p.is_file():
            raise SystemExit(f"missing summary {name}: {p}")
        loads[name] = json.loads(p.read_text())

    table = {}
    for m, fn in METRICS:
        table[m] = {name: fn(s) for name, s in loads.items()}
    # additivity gates: joint delta must equal the sum of single deltas
    additivity = {}
    for m, _ in METRICS:
        b, j = table[m]["base"], table[m]["joint"]
        single_sum = sum(table[m][k] - b for k in ("b018", "d002", "e002", "f017"))
        additivity[m] = {
            "base": b, "joint": j, "joint_delta": j - b,
            "single_deltas_sum": single_sum,
            "additive": (j - b) == single_sum,
        }
    # win-hit class union check
    def hit_classes(s):
        return sorted({g["s4_class_index"] for g in s["frozen_update8_refresh"]["win_hit_groups"]})
    union_single = sorted(set(hit_classes(loads["b018"])) | set(hit_classes(loads["d002"]))
                          | set(hit_classes(loads["e002"])) | set(hit_classes(loads["f017"])))
    if hit_classes(loads["joint"]) != union_single:
        raise SystemExit("joint win-hit class set != union of single adoption class sets")

    # per-root free coverage must be unchanged in every scenario
    def freemap(s):
        return {r["origin_first"]: r["free_thirds_now"] for r in s["roots"]}
    for name in ("b018", "d002", "e002", "f017", "joint"):
        if freemap(loads[name]) != freemap(loads["base"]):
            raise SystemExit(f"per-root free coverage changed in scenario {name}")

    # closure ranking status annotation (top of the joint ranking)
    joint_summary = loads["joint"]
    out = {
        "schema": "n11-central-reply-joint-4win-adoption-ifadopted-v1",
        "interpretation_guard": "IF-ADOPTED what-if analysis only; no verdict consumed; 11x11 UNKNOWN",
        "metric_table": table,
        "additivity_audit": additivity,
        "win_hit_class_union": union_single,
        "per_root_free_coverage": "identical to baseline in all five adoption scenarios (machine-verified)",
        "constraint_note": ("the closure-classes ranking is a scheduling quantity; it does NOT carry the "
                            "class status. Under joint adoption the ranked top carries excluded_now classes "
                            "(16757/12264/20421/16371 + 30345 holding b018's cost child); a probe batch must "
                            "first filter them (operator rule: skip candidates with refutation evidence; "
                            "the first clean candidate under joint adoption is rank 6 (class 5473))."),
    }
    OUT.write_text(json.dumps(out, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    bad = [m for m, a in additivity.items() if not a["additive"]]
    print(json.dumps({"additivity_gate_failures": bad, "output": str(OUT)}, indent=1))
    if bad:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
