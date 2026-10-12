#!/usr/bin/env python3
"""Independently re-verify the chosen S5 proof plans against geometry and cache.

For every candidate root the script rebuilds, from the independent
integer-geometry Board and the solver-trusted exact-S5 cache only:

* the 119 legal third moves,
* each third move's canonical S4 response classes,
* each used S4 class's children split into cached-WIN / cached-LOSS / unknown,

and checks that

* every plan entry's chosen S4 is a legal response to its third move,
* no chosen S4 has a cached-WIN child,
* every chosen S4's unknown-children set equals the graph's recorded cost set,
* every third move absent from a plan is genuinely free (has a zero-cost S4),
* every plan's claimed union equals the union of its chosen options' costs.

Nothing here asserts any unknown verdict.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
BOARD_SOURCE = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts/independent.py"

sys.path.insert(0, str(BOARD_SOURCE.parent))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache  # noqa: E402


def _log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def key_of(mask: int) -> tuple[int, int]:
    return mask & ((1 << 64) - 1), mask >> 64


from joint_plan_checks import audit_joint_entries


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, default=EXPERIMENT / "output/dependency-graph.json.gz")
    parser.add_argument("--plan", type=Path, default=EXPERIMENT / "output/chosen-plans.json")
    parser.add_argument("--output", type=Path, default=EXPERIMENT / "output/plan-verification.json")
    args = parser.parse_args()
    started = time.time()

    graph_path = args.graph if args.graph.is_absolute() else ROOT / args.graph
    plan_path = args.plan if args.plan.is_absolute() else ROOT / args.plan
    with gzip.open(graph_path, "rt", encoding="utf-8") as stream:
        graph = json.load(stream)
    plans = json.loads(plan_path.read_text(encoding="utf-8"))["plans"]

    board = Board(11)
    cache = load_exact_s5_cache(board)
    s4_masks = [(pair[0] | (pair[1] << 64)) for pair in graph["s4_masks"]]
    s4_index = {mask: i for i, mask in enumerate(s4_masks)}
    s4_status = graph["s4_status"]
    s4_cost = [set(row) for row in graph["s4_cost"]]
    s5_masks = [(pair[0] | (pair[1] << 64)) for pair in graph["s5_masks"]]
    for mask in s4_masks:
        assert board.canonical(mask) == mask, "stored S4 mask is not canonical"
    for mask in s5_masks:
        assert board.canonical(mask) == mask, "stored S5 mask is not canonical"

    checked_s4: dict[int, tuple[str, frozenset]] = {}
    verified_paid_options: dict[tuple[int, int, int], set[int]] = {}
    failures: list[str] = []
    stats = {"roots": 0, "thirds": 0, "paid_entries": 0, "free_thirds": 0,
             "distinct_s4_checked": 0}

    def status_of(index: int) -> tuple[str, frozenset]:
        """Independently recompute an S4 class's status and unknown children."""
        hit = checked_s4.get(index)
        if hit is not None:
            return hit
        mask = s4_masks[index]
        children = board.children(mask)
        cached = {key_of(child): cache[key_of(child)]["verdict"]
                  for child in children if key_of(child) in cache}
        unknown = frozenset(child for child in children if key_of(child) not in cache)
        if 1 in cached.values():
            verdict = "WIN_EXCLUDED"
        elif unknown:
            verdict = "UNKNOWN"
        else:
            verdict = "LOSS"
        checked_s4[index] = (verdict, unknown)
        stats["distinct_s4_checked"] += 1
        return verdict, unknown

    def check_s4(index: int) -> None:
        verdict, unknown = status_of(index)
        recorded = ("WIN_EXCLUDED" if s4_status[index] == -1
                    else "LOSS" if s4_status[index] == 0 else "UNKNOWN")
        if verdict != recorded:
            failures.append(f"s4 {index}: recomputed {verdict} != recorded {recorded}")
        recorded_unknown = {s5_masks[e] for e in s4_cost[index]}
        if recorded == "WIN_EXCLUDED":
            if recorded_unknown:
                failures.append(f"s4 {index}: excluded WIN must have empty cost")
        elif set(unknown) != recorded_unknown:
            failures.append(
                f"s4 {index}: recomputed {len(unknown)} unknown children != "
                f"recorded {len(recorded_unknown)}")

    for root in graph["roots"]:
        if root["role"] == "known-loss-baseline":
            continue
        stats["roots"] += 1
        pair = root["pair_mask"][0] | (root["pair_mask"][1] << 64)
        thirds = set(board.points(board.legal(pair)))
        graph_thirds = {row["third"] for row in root["thirds"]}
        if thirds != graph_thirds:
            failures.append(f"root {root['origin_first']}/{root['origin_reply']}: "
                            f"recomputed {len(thirds)} thirds != graph {len(graph_thirds)}")
            continue
        stats["thirds"] += len(thirds)
        name = f"{root['origin_first']}/{root['origin_reply']}"
        entries = {(e["third"]): e for e in plans[name]["groups"]} \
            if name in plans and name != "_joint_19_roots" else {}
        for row in root["thirds"]:
            third = row["third"]
            s3 = pair | (1 << third)
            classes = {board.canonical(s3 | (1 << fourth))
                       for fourth in board.points(board.legal(s3))}
            recomputed = {s4_index[mask] for mask in classes
                          if status_of(s4_index[mask])[0] != "WIN_EXCLUDED"}
            if recomputed != set(row["options"]):
                missing = set(row["options"]) - recomputed
                extra = recomputed - set(row["options"])
                failures.append(f"root {name} third {third}: recomputed "
                                f"{len(recomputed)} non-WIN options != graph "
                                f"{len(row['options'])} "
                                f"(missing={sorted(missing)[:5]}, extra={sorted(extra)[:5]})")
                continue
            entry = entries.get(third)
            if entry is None:
                stats["free_thirds"] += 1
                witness = next((i for i in sorted(recomputed)
                                if s4_status[i] == 0 and not s4_cost[i]), None)
                if witness is None:
                    failures.append(f"root {name} third {third}: claimed free but no "
                                    f"zero-cost S4 among {len(recomputed)} options")
                else:
                    check_s4(witness)
            else:
                stats["paid_entries"] += 1
                verified_paid_options[(root["origin_first"], root["origin_reply"], third)] = recomputed
                chosen = entry["s4_class_index"]
                if chosen not in recomputed:
                    failures.append(f"root {name} third {third}: chosen s4 {chosen} "
                                    f"is not a legal response")
                    continue
                if s4_masks[chosen] != (entry["s4_mask"][0] | (entry["s4_mask"][1] << 64)):
                    failures.append(f"root {name} third {third}: stored s4 mask mismatch")
                if (type(entry.get("unknown_s5_children")) is not int or
                        entry["unknown_s5_children"] != len(s4_cost[chosen])):
                    failures.append(f"root {name} third {third}: unknown S5 count mismatch")
                check_s4(chosen)
        _log(f"root {name}: {len(thirds)} thirds ok "
             f"({len(entries)} paid, {len(thirds) - len(entries)} free)")

    # Check all S4 status/cost records, including those not selected.
    for index in range(len(s4_masks)):
        check_s4(index)

    individual_thirds: set[tuple[int, int, int]] = set()
    for name, plan in plans.items():
        if name == "_joint_19_roots":
            continue
        for entry in plan["groups"]:
            individual_thirds.add((entry["first"], entry["reply"], entry["third"]))
    joint = plans["_joint_19_roots"]["groups"]
    union = audit_joint_entries(joint, individual_thirds, verified_paid_options,
                                s4_masks, s4_cost, check_s4, failures)
    if sorted(union) != plans["_joint_19_roots"]["required_new_s5"]:
        failures.append("joint plan union does not match required_new_s5")
    if len(union) != plans["_joint_19_roots"]["union_size"]:
        failures.append("joint plan union size mismatch")

    result = {"schema": "n11-joint-s5-plan-verification-v1",
              "graph": str(graph_path.relative_to(ROOT)),
              "plan": str(plan_path.relative_to(ROOT)),
              "failures": failures,
              "passed": not failures,
              "statistics": stats,
              "seconds": round(time.time() - started, 1)}
    output = args.output if args.output.is_absolute() else ROOT / args.output
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
