#!/usr/bin/env python3
"""Batch-9 (class 1518) WIN-vs-LOSS decomposition delta extractor.

Fail-closed, analysis-only. Reads the baseline re-audit refresh summary and
the three batch-9 scenario summaries:

  * PWINJ033 = j033 WIN row only        (pwinj033/)
  * PLOSS32  = 32 batch-9 LOSS rows only (ploss32/)
  * PFULL33  = all 33 probed rows       (pfull33/)

and emits output/decomp-deltas-batch9.json with the machine-computed metric
table, measured additivity observations, excluded-flip class identification
(machine-derived from the frozen dependency graph: the classes that hold the
j033 S5 child index 69347 as a cost child) cross-checked against the
closure-classes ranking delta, and the per-root free coverage gate.

The increments are read-only what-if analysis inputs; no verdict is consumed
and no class, root, coverage or closure claim is made. 11x11 stays UNKNOWN.
"""
import csv
import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]

BASE = ROOT / "research/experiments/n11-central-reply-10324-closure-reaudit-20261122/output"
SCEN = {
    "PWINJ033": EXP / "pwinj033/output/refresh-summary.json",
    "PLOSS32": EXP / "ploss32/output/refresh-summary.json",
    "PFULL33": EXP / "pfull33/output/refresh-summary.json",
}
SCEN_DIR = {
    "PWINJ033": EXP / "pwinj033/output",
    "PLOSS32": EXP / "ploss32/output",
    "PFULL33": EXP / "pfull33/output",
}
GRAPH = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output/dependency-graph.json.gz"
J033_S5_INDEX = 69347
LOSS_RESOLVED_S5_INDEX = 69330  # j016, machine-identified from batch-keys.json
OUT = EXP / "output/decomp-deltas-batch9.json"

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
    ("class1518_unknown_now", lambda s: _cl(s).get(1518, {}).get("unknown_now", "ABSENT")),
]


def _cl(s):
    return s.get("_closure_index") or {}


def fail(msg):
    print("GATE FAILED: " + msg, file=sys.stderr)
    raise SystemExit(1)


def main():
    base = json.loads((BASE / "refresh-summary.json").read_text())
    sums = {name: json.loads(p.read_text()) for name, p in SCEN.items()}

    # graph-side machine identification of the j033 cost-child holders
    G = json.load(gzip.open(GRAPH, "rb"))
    cost = G["s4_cost"]
    holders = [i for i, c in enumerate(cost) if J033_S5_INDEX in c]
    statuses = {i: G["s4_status"][i] for i in holders}
    if len(holders) != 2 or set(statuses.values()) != {1}:
        fail(f"graph holders {holders} statuses {statuses} (expected 2 base-unknown)")

    def closure_rows(summary_dir):
        rows = {}
        with (Path(summary_dir) / "closure-classes.csv").open() as fh:
            for r in csv.DictReader(fh):
                rows[int(r["class_index"])] = r
        return rows

    def idx_attach(d, s):
        s["_closure_index"] = closure_rows(d)
        return s

    base_cl = closure_rows(BASE)
    base["_closure_index"] = base_cl
    for name, s in sums.items():
        idx_attach(SCEN_DIR[name], s)

    table = {}
    for metric, fn in METRICS:
        table[metric] = {"base": fn(base)}
        for name, s in sums.items():
            table[metric][name] = fn(s)

    for name, s in sums.items():
        groups = s["frozen_update8_refresh"]["win_hit_groups"]
        classes = {}
        for g in groups:
            c = g.get("s4_class_index")
            classes[str(c)] = classes.get(str(c), 0) + 1
        table.setdefault("win_hit_classes", {})[name] = classes
    table["win_hit_classes"].setdefault("base", {})

    additivity = {}
    for metric, _ in METRICS:
        if metric == "class1518_unknown_now":
            continue
        t = table[metric]
        w = t["PWINJ033"] - t["base"]
        l = t["PLOSS32"] - t["base"]
        f = t["PFULL33"] - t["base"]
        additivity[metric] = {
            "win_delta": w, "loss_delta": l, "full_delta": f,
            "full_eq_win_plus_loss": (w + l == f),
        }

    # closure ranking delta: rows that changed OR disappeared vs base
    flip = {}
    for name in SCEN_DIR:
        sc_cl = {k: v for k, v in closure_rows(SCEN_DIR[name]).items()}
        changed, disappeared = [], []
        for idx, r in base_cl.items():
            sr = sc_cl.get(idx)
            if sr is None:
                disappeared.append(idx)
            elif sr["class_rank"] != r["class_rank"] or sr["unknown_now"] != r["unknown_now"]:
                changed.append({
                    "class_index": idx, "base_unknown": int(r["unknown_now"]),
                    "scenario_unknown": int(sr["unknown_now"]),
                    "base_rank": int(r["class_rank"]), "scenario_rank": int(sr["class_rank"]),
                })
        flip[name] = {
            "rows_disappeared": sorted(disappeared),
            "rows_with_unknown_or_rank_changed": sorted(changed, key=lambda x: x["class_index"]),
            "scenario_status_counts": sums[name]["class_status_counts"],
        }

    # cross-check A: PWIN unknown-changed-row set (rank shifts excluded) must equal the graph holder set
    pwin_changed = sorted(x["class_index"] for x in flip["PWINJ033"]["rows_with_unknown_or_rank_changed"]
                          if x["scenario_unknown"] != x["base_unknown"])
    if pwin_changed != sorted(holders):
        fail(f"PWIN unknown-changed rows {pwin_changed} != graph holders {holders}")
    for x in flip["PWINJ033"]["rows_with_unknown_or_rank_changed"]:
        if x["class_index"] in pwin_changed and x["scenario_unknown"] - x["base_unknown"] != -1:
            fail(f"PWIN unknown delta for {x['class_index']} is {x['scenario_unknown'] - x['base_unknown']}, expected -1")
    # cross-check B: per-class unknown delta of PFULL vs PLOSS must be -1 on exactly holders
    ploss_cl = {int(r["class_index"]): r for r in csv.DictReader((SCEN_DIR["PLOSS32"] / "closure-classes.csv").open())}
    pfull_cl = {int(r["class_index"]): r for r in csv.DictReader((SCEN_DIR["PFULL33"] / "closure-classes.csv").open())}
    win_only_delta = sorted(
        idx for idx in pfull_cl
        if idx in ploss_cl and int(pfull_cl[idx]["unknown_now"]) != int(ploss_cl[idx]["unknown_now"])
    )
    for idx in win_only_delta:
        d = int(pfull_cl[idx]["unknown_now"]) - int(ploss_cl[idx]["unknown_now"])
        if d != -1:
            fail(f"PFULL vs PLOSS unknown delta for {idx} is {d}, expected -1")
    if win_only_delta != sorted(holders):
        fail(f"PFULL-PLOSS win-only delta rows {win_only_delta} != graph holders {holders}")

    # per-root free coverage equality gates
    cov = {}
    base_roots = {(r["role"], r.get("origin_first")): (r["free_thirds_now"], r["uncovered"]) for r in base["roots"]}
    base_prc = {}
    with (BASE / "per-root-coverage.csv").open() as fh:
        for r in csv.DictReader(fh):
            base_prc[(r["role"], r["first"])] = (r["free_now"], r["uncovered"])
    for name in SCEN_DIR:
        s = sums[name]
        roots = {(r["role"], r.get("origin_first")): (r["free_thirds_now"], r["uncovered"]) for r in s["roots"]}
        prc = {}
        with (SCEN_DIR[name] / "per-root-coverage.csv").open() as fh:
            for r in csv.DictReader(fh):
                prc[(r["role"], r["first"])] = (r["free_now"], r["uncovered"])
        ok = roots == base_roots and prc == base_prc
        cov[name] = {"identical_to_base": ok}
        if not ok:
            fail(f"per-root free coverage gate broken in {name}")

    out = {
        "schema": "n11-class1518-batch9-decomp-deltas-v1",
        "interpretation_guard": ("read-only what-if IF-ADOPTED planning deltas; "
                                 "verdicts NOT consumed; scheduling quantities "
                                 "only; 11x11 stays UNKNOWN"),
        "j033": {
            "s5_index": J033_S5_INDEX,
            "graph_cost_child_holder_classes": holders,
            "holder_base_statuses": {str(i): statuses[i] for i in holders},
            "batch9_win_row": "j033 (probe_order 364, 2-pass node-exact, nodes 4718280, rc=45 WIN-HALT pre-registered rule)",
        },
        "loss_side_resolved_baseline_requirement": {
            "s5_index": LOSS_RESOLVED_S5_INDEX, "key_id": "j016",
            "note": ("the single update8 baseline-requirement entry newly resolved "
                     "before update 8 under PLOSS32/PFULL33 "
                     "(resolved_count 23->24, remaining_now 31836->31835)"),
        },
        "metrics": table,
        "additivity_measured": additivity,
        "closure_class_deltas": flip,
        "excluded_flip_cross_check": {
            "graph_holders": holders,
            "pwin_changed_rows": pwin_changed,
            "pfull_vs_ploss_win_only_delta_rows": win_only_delta,
            "excluded_now_delta_pwin": table["excluded_now"]["PWINJ033"] - table["excluded_now"]["base"],
            "all_agree_with_membership_class_count_2": (sorted(holders) == pwin_changed == win_only_delta
                                                        and len(holders) == 2
                                                        and table["excluded_now"]["PWINJ033"] - table["excluded_now"]["base"] == 2),
        },
        "per_root_free_coverage_gate": cov,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    compact = {m: {k: v for k, v in t.items()} for m, t in table.items() if m != "class1518_unknown_now"}
    print(json.dumps(compact, indent=1))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
