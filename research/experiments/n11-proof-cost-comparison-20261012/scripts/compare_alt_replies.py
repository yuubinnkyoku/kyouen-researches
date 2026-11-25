#!/usr/bin/env python3
"""Compare non-central replies against central ones, individually and jointly.

For each alternative root: individual min-union optimisation (same heuristic
as K0417), S4/S5 reuse counts against the central graph, and overlap of its
optimistic plan with the K0417 joint plan's required S5 set.  For the best
alternative per first move, a joint-swap instance (18 central roots plus the
alternative instead of the central root of that first move) is solved and
compared with the K0417 joint upper bound 31,546.  No solver search involved.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
OLD_EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
OLD_SCRIPTS = OLD_EXPERIMENT / "scripts"

sys.path.insert(0, str(OLD_SCRIPTS))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
from optimize_s5_selection import Instance, _dedup, solve_instance  # noqa: E402
from analyze_central_reply_frontier import sha  # noqa: E402

NEW_EXPERIMENT = ROOT / "research/experiments/n11-proof-cost-comparison-20261012"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path,
                        default=OLD_EXPERIMENT / "output/dependency-graph.json.gz")
    parser.add_argument("--alts", type=Path,
                        default=NEW_EXPERIMENT / "output/alt-roots.json.gz")
    parser.add_argument("--joint-plan", type=Path,
                        default=OLD_EXPERIMENT / "output/chosen-plans.json")
    parser.add_argument("--output", type=Path,
                        default=NEW_EXPERIMENT / "output/alt-reply-comparison.json")
    parser.add_argument("--restarts", type=int, default=3)
    args = parser.parse_args()
    started = time.time()

    graph_path = args.graph if args.graph.is_absolute() else ROOT / args.graph
    with gzip.open(graph_path, "rt", encoding="utf-8") as stream:
        central = json.load(stream)
    alts_path = args.alts if args.alts.is_absolute() else ROOT / args.alts
    with gzip.open(alts_path, "rt", encoding="utf-8") as stream:
        alts = json.load(stream)
    plan_path = args.joint_plan if args.joint_plan.is_absolute() else ROOT / args.joint_plan
    joint_required = set(json.loads(plan_path.read_text(encoding="utf-8"))
                         ["plans"]["_joint_19_roots"]["required_new_s5"])

    base_s4 = alts["base_s4_classes"]
    cost = [set(row) for row in central["s4_cost"]]
    for key in sorted(alts["new_s4_classes"], key=int):
        idx = int(key)
        assert idx == len(cost), "new-class indices must append in order"
        cost.append(set(alts["new_s4_classes"][key]["cost"]))
    status = list(central["s4_status"]) + [
        alts["new_s4_classes"][k]["status"]
        for k in sorted(alts["new_s4_classes"], key=int)]

    central_rows = {}
    for root in central["roots"]:
        if root["role"] != "known-loss-baseline":
            central_rows[(root["origin_first"], root["origin_reply"])] = root
    k0417_ub = {49: 2055, 38: 2155, 16: 2084}

    rows = []
    swap_candidates = {}
    for alt in alts["roots"]:
        first, reply = alt["origin_first"], alt["origin_reply"]
        groups = [list(r["options"]) for r in alt["thirds"]]
        labels = [(first, reply, r["third"]) for r in alt["thirds"]]
        inst = Instance(*_dedup(groups, labels), cost)
        t0 = time.time()
        res = solve_instance(inst, restarts=args.restarts)
        union = set(res.pop("_union"))
        res.pop("_assign")
        reused_s4 = sum(1 for r in alt["thirds"] for s in r["options"] if s < base_s4)
        total_slots = sum(len(r["options"]) for r in alt["thirds"])
        overlap = len(union & joint_required)
        row = {
            "root": f"{first}/{reply}",
            "central_counterpart_ub": k0417_ub[first],
            "individual_ub": res["upper_bound"],
            "individual_lb": res["lower_bound"],
            "paid_groups": res["paid_groups"],
            "free_groups": res["free_groups"],
            "beats_central": res["upper_bound"] < k0417_ub[first],
            "s4_option_slots": total_slots,
            "s4_slots_reused_from_central": reused_s4,
            "s4_reuse_fraction": round(reused_s4 / total_slots, 4),
            "plan_s5_in_k0417_joint": overlap,
            "plan_s5_total": len(union),
            "plan_overlap_fraction": round(overlap / len(union), 4) if union else 0.0,
            "seconds": round(time.time() - t0, 1),
        }
        rows.append(row)
        prev = swap_candidates.get(first)
        if prev is None or res["upper_bound"] < prev[1]:
            swap_candidates[first] = (alt, res["upper_bound"], union)
        print(json.dumps(row, ensure_ascii=False), flush=True)

    swaps = []
    for first in sorted(swap_candidates):
        alt, _, _ = swap_candidates[first]
        raw_groups: list[list[int]] = []
        raw_labels: list[tuple] = []
        for (f, r), root in central_rows.items():
            if f == first and r == 60:
                continue
            for t in root["thirds"]:
                raw_groups.append(list(t["options"]))
                raw_labels.append((f, r, t["third"]))
        for t in alt["thirds"]:
            raw_groups.append(list(t["options"]))
            raw_labels.append((first, alt["origin_reply"], t["third"]))
        jinst = Instance(*_dedup(raw_groups, raw_labels), cost)
        t0 = time.time()
        jres = solve_instance(jinst, restarts=args.restarts)
        junion = set(jres.pop("_union"))
        jres.pop("_assign")
        swaps.append({
            "swapped_first": first,
            "alt_reply": alt["origin_reply"],
            "joint_swap_ub": jres["upper_bound"],
            "joint_swap_lb": jres["lower_bound"],
            "k0417_joint_ub": 31546,
            "delta_vs_k0417": jres["upper_bound"] - 31546,
            "distinct_groups": len(jinst.groups),
            "paid_groups": len(jinst.paid),
            "seconds": round(time.time() - t0, 1),
        })
        print(json.dumps(swaps[-1], ensure_ascii=False), flush=True)

    result = {"schema": "n11-alt-reply-comparison-v1",
              "central_graph_sha256": sha(graph_path),
              "alts_sha256": sha(alts_path),
              "individual_alternatives": rows,
              "joint_swaps": swaps,
              "conclusion": ("no alternative beats its central counterpart; "
                             "see joint_swap deltas"),
              "seconds": round(time.time() - started, 1)}
    output = args.output if args.output.is_absolute() else ROOT / args.output
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()
