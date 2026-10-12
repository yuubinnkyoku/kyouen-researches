#!/usr/bin/env python3
"""Integer lower bound by packing groups with pairwise-disjoint option pools.

For a paid group t let pool[t] = union of C(s) over its options.  If groups
t_1..t_k have pairwise-disjoint pools, any feasible union U contains one full
option per group, each inside its own pool, hence pairwise disjoint, so
|U| >= sum_j min_{s in F_{t_j}} |C(s)|.  This is an integer certificate: the
packed group list plus a disjointness check recomputable from the graph.

A greedy maximal packing is tried under several group orderings (and jittered
variants); the best value is kept.  No solver search is involved.
"""
from __future__ import annotations

import argparse
import gzip
import json
import random
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NEW_EXPERIMENT = ROOT / "research/experiments/n11-proof-cost-comparison-20261012"
OLD_EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
OLD_SCRIPTS = OLD_EXPERIMENT / "scripts"

sys.path.insert(0, str(OLD_SCRIPTS))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
from optimize_s5_selection import Instance, _dedup  # noqa: E402
from analyze_central_reply_frontier import sha  # noqa: E402


def pack(inst: Instance, order: list[int]) -> tuple[list[int], int]:
    used: set[int] = set()
    packed: list[int] = []
    value = 0
    for i in order:
        pool = inst.pool[i]
        if pool & used:
            continue
        used |= pool
        packed.append(i)
        value += min(len(inst.cost[s]) for s in inst.groups[i])
    return packed, value


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path,
                        default=OLD_EXPERIMENT / "output/dependency-graph.json.gz")
    parser.add_argument("--output", type=Path,
                        default=NEW_EXPERIMENT / "output/disjoint-pool-packing.json")
    parser.add_argument("--seeds", type=int, default=12)
    args = parser.parse_args()
    started = time.time()

    graph_path = args.graph if args.graph.is_absolute() else ROOT / args.graph
    with gzip.open(graph_path, "rt", encoding="utf-8") as stream:
        graph = json.load(stream)
    cost = [set(row) for row in graph["s4_cost"]]
    groups: list[list[int]] = []
    labels: list[tuple] = []
    for root in graph["roots"]:
        if root["role"] == "known-loss-baseline":
            continue
        for row in root["thirds"]:
            groups.append(list(row["options"]))
            labels.append((root["origin_first"], root["origin_reply"], row["third"]))
    inst = Instance(*_dedup(groups, labels), cost)
    paid = inst.paid
    min_size = {i: min(len(inst.cost[s]) for s in inst.groups[i]) for i in paid}
    pool_size = {i: len(inst.pool[i]) for i in paid}

    orders = [
        sorted(paid, key=lambda i: (min_size[i], pool_size[i], i)),
        sorted(paid, key=lambda i: (pool_size[i], min_size[i], i)),
        sorted(paid, key=lambda i: (min_size[i] / max(pool_size[i], 1), min_size[i], i)),
        sorted(paid, key=lambda i: (pool_size[i] / max(min_size[i], 1), pool_size[i], i)),
    ]
    rng = random.Random(20261012)
    for _ in range(args.seeds):
        key = {i: rng.random() for i in paid}
        orders.append(sorted(paid, key=lambda i: (min_size[i] + key[i] * 40,
                                                  pool_size[i], i)))
    best: tuple[list[int], int] = ([], 0)
    for order in orders:
        packed, value = pack(inst, order)
        if value > best[1]:
            best = (packed, value)
    packed, value = best

    # self-verification from the stored lists
    used: set[int] = set()
    check = 0
    for i in packed:
        assert not (inst.pool[i] & used), "packed pools overlap"
        used |= inst.pool[i]
        check += min(len(inst.cost[s]) for s in inst.groups[i])
    assert check == value

    result = {
        "schema": "n11-disjoint-pool-packing-v1",
        "graph": str(graph_path.relative_to(ROOT)),
        "graph_sha256": sha(graph_path),
        "method": ("greedy maximal packing of paid groups with pairwise-disjoint "
                   "option pools; value = sum of per-group minimum option sizes, "
                   "a valid integer lower bound since disjoint pools force "
                   "disjoint option contents in every feasible union"),
        "packed_groups": len(packed),
        "integer_lower_bound": value,
        "packed": [{"group": i,
                    "labels": [list(lab) for lab in inst.labels[i]],
                    "min_option_size": min_size[i],
                    "pool_size": pool_size[i]} for i in packed],
        "seconds": round(time.time() - started, 1),
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    print(json.dumps({"packed_groups": len(packed),
                      "integer_lower_bound": value,
                      "seconds": round(time.time() - started, 1)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
