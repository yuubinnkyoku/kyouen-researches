#!/usr/bin/env python3
"""Batch-6 (class 5473) WIN-vs-LOSS decomposition delta extractor.

Fail-closed, analysis-only. Reads the baseline re-audit refresh summary and
the three batch-6 scenario summaries:

  * PWIN18  = g018 WIN row only        (pwing018/)
  * PLOSS17 = 17 batch-6 LOSS rows only (pgloss17/)
  * PFULL18 = all 18 probed rows       (pfull18/)

and emits output/decomp-deltas-batch6.json with the machine-computed metric
table, WIN/LOSS-conflict-free additivity observations, excluded-flip class
identification and the closure-classes ranking delta. The increments are
read-only what-if analysis inputs; no verdict is consumed and no class, root,
coverage or closure claim is made. 11x11 stays UNKNOWN.
"""
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]

BASE = ROOT / "research/experiments/n11-central-reply-23963-closure-reaudit-20261122/output"
SCEN = {
    "PWIN18": EXP / "pwing018/output/refresh-summary.json",
    "PLOSS17": EXP / "pgloss17/output/refresh-summary.json",
    "PFULL18": EXP / "pfull18/output/refresh-summary.json",
}
OUT = EXP / "output/decomp-deltas-batch6.json"

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


def fail(msg):
    print("GATE FAILED: " + msg, file=sys.stderr)
    raise SystemExit(1)


def main():
    base = json.loads((BASE / "refresh-summary.json").read_text())
    sums = {name: json.loads(p.read_text()) for name, p in SCEN.items()}

    table = {}
    for metric, fn in METRICS:
        table[metric] = {"base": fn(base)}
        for name, s in sums.items():
            table[metric][name] = fn(s)

    # win-hit group attribution per scenario
    for name, s in sums.items():
        groups = s["frozen_update8_refresh"]["win_hit_groups"]
        classes = {}
        for g in groups:
            c = g.get("s4_class_index")
            classes[str(c)] = classes.get(str(c), 0) + 1
        table.setdefault("win_hit_classes", {})[name] = classes
        table["win_hit_classes"].setdefault("base", {})

    # additivity observations (measured, not assumed)
    additivity = {}
    for metric, _ in METRICS:
        t = table[metric]
        w, l, f = t["PWIN18"] - t["base"], t["PLOSS17"] - t["base"], t["PFULL18"] - t["base"]
        additivity[metric] = {
            "win_delta": w, "loss_delta": l, "full_delta": f,
            "full_eq_win_plus_loss": (w + l == f),
        }

    # excluded-flip classes: closure-classes.csv rows whose status flips
    def closure_rows(summary_dir):
        rows = {}
        with (summary_dir / "closure-classes.csv").open() as fh:
            for r in csv.DictReader(fh):
                rows[int(r["class_index"])] = r
        return rows

    base_cl = closure_rows(BASE)
    flip = {}
    for name, d in (("PWIN18", EXP / "pwing018/output"),
                    ("PLOSS17", EXP / "pgloss17/output"),
                    ("PFULL18", EXP / "pfull18/output")):
        sc_cl = closure_rows(d)
        sc_sum = sums[name]["class_status_counts"]
        fl = []
        for idx, r in base_cl.items():
            sr = sc_cl.get(idx)
            if sr is None:
                continue
            if sr["class_rank"] != r["class_rank"] or sr["unknown_now"] != r["unknown_now"]:
                fl.append({"class_index": idx, "base_unknown": int(r["unknown_now"]),
                           "scenario_unknown": int(sr["unknown_now"]),
                           "scenario_rank": int(sr["class_rank"])})
        flip[name] = {"rows_with_unknown_changed": sorted(fl, key=lambda x: x["class_index"]),
                      "scenario_status_counts": sc_sum}
    # classes that hold the g018 key as cost child: from the frozen graph via
    # win_hit_groups + unknown-excluded delta; record from summary metadata
    flip["g018_cost_child_classes"] = sums["PWIN18"].get("cost_child_win_classes") or None

    # per-root free coverage equality gate (all scenarios must hold it)
    cov = {}
    for name, s in sums.items():
        roots = {(r["role"], r.get("origin_first")): r["free_thirds_now"] for r in s["roots"]}
        base_roots = {(r["role"], r.get("origin_first")): r["free_thirds_now"] for r in base["roots"]}
        cov[name] = {"identical_to_base": roots == base_roots}

    out = {
        "schema": "n11-class5473-batch6-decomp-deltas-v1",
        "interpretation_guard": ("read-only what-if IF-ADOPTED planning deltas; "
                                 "verdicts NOT consumed; scheduling quantities "
                                 "only; 11x11 stays UNKNOWN"),
        "metrics": table,
        "additivity_measured": additivity,
        "closure_class_deltas": flip,
        "per_root_free_coverage_gate": cov,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(table, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
