#!/usr/bin/env python3
"""Minimise the set of not-yet-known exact S5 verdicts a LOSS proof must buy.

A two-stone root is LOSS once every one of its 119 third moves has at least one
LOSS-capable S4 response, and an S4 is LOSS once *all* of its exact-S5 children
are LOSS.  For a third move the planner may pick any non-WIN S4 response, so the
combinatorial problem is:

    choose one option per (root, third) group, minimising the size of the union
    of the still-unknown exact-S5 children of the chosen S4 classes.

The script reports a feasible upper bound (multi-start greedy plus alternating
refinement and union shrinking) and several valid lower bounds (per-group
minimum, threshold cover, element-only fractional dual, and a grouped
fractional dual solved by alternating packing).  Nothing here decides any
unknown S5 verdict: it is an optimistic proof plan.
"""
from __future__ import annotations

import argparse
import gzip
import json
import random
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"

GREEDY_KEYS = {
    "marginal_then_coverage": lambda out, n, s: (out, -n, s),
    "marginal_ratio": lambda out, n, s: (out / n, out, -n, s),
    "coverage_then_marginal": lambda out, n, s: (-n, out, s),
    "marginal_only": lambda out, n, s: (out, s),
}


class Instance:
    """Groups of S4 options with per-option unknown-S5 cost sets.

    ``labels[i]`` is the list of (first, reply, third) triples that share group
    ``i``.  Identical option sets are always safe to merge: covering one member
    with option ``s`` covers every member with the same ``s`` at no extra cost,
    so the minimum-union value is unchanged.
    """

    def __init__(self, groups: list[list[int]], labels: list, cost: list[set[int]]):
        self.groups = groups
        self.labels = [lab if isinstance(lab, list) else [lab] for lab in labels]
        self.cost = cost
        free = set(i for i, opts in enumerate(groups)
                   if any(not cost[s] for s in opts))
        self.free_groups = sorted(free)
        self.paid = [i for i in range(len(groups)) if i not in free]
        self.in_play = sorted({s for i in self.paid for s in groups[i]})
        self.cover: dict[int, set[int]] = defaultdict(set)
        for i in self.paid:
            for s in groups[i]:
                self.cover[s].add(i)
        self.elem_opts: dict[int, list[int]] = defaultdict(list)
        for s in self.in_play:
            for e in cost[s]:
                self.elem_opts[e].append(s)
        self.pool: dict[int, set[int]] = {}
        for i in self.paid:
            acc: set[int] = set()
            for s in groups[i]:
                acc |= cost[s]
            self.pool[i] = acc
        self.label_count = sum(len(x) for x in self.labels)


def greedy_solve(inst: Instance, key_fn, seed: int | None = None,
                 jitter: float = 0.0) -> tuple[list[int | None], set[int]]:
    groups = inst.groups
    rng = random.Random(seed) if seed is not None else None
    outside = {s: len(inst.cost[s]) for s in inst.in_play}
    live = {s: len(inst.cover[s]) for s in inst.in_play}
    active = set(inst.in_play)
    uncovered = set(inst.paid)
    assign: list[int | None] = [None] * len(groups)
    union: set[int] = set()
    while uncovered:
        best = None
        for s in active:
            n = live[s]
            if n <= 0:
                continue
            key = key_fn(outside[s] + (rng.random() * jitter if jitter else 0.0), n, s)
            if best is None or key < best[0]:
                best = (key, s)
        if best is None:
            raise ValueError("no option can cover a remaining group")
        s = best[1]
        fresh = inst.cost[s] - union
        union |= inst.cost[s]
        for e in fresh:
            for other in inst.elem_opts[e]:
                if outside[other] > 0:
                    outside[other] -= 1
        for i in inst.cover[s]:
            if i in uncovered:
                uncovered.discard(i)
                assign[i] = s
                for other in groups[i]:
                    live[other] -= 1
                    if live[other] <= 0:
                        active.discard(other)
        if not active and uncovered:
            raise ValueError("option pool exhausted")
    return assign, union


def refine(inst: Instance, assign: list[int | None], union: set[int],
           passes: int = 6) -> tuple[list[int | None], set[int]]:
    """Alternating minimisation: re-pick options that fit inside the current union."""
    for _ in range(passes):
        extra = {s: sum(1 for e in inst.cost[s] if e not in union) for s in inst.in_play}
        new_assign: list[int | None] = list(assign)
        accum: set[int] = set()
        for i in inst.paid:
            best_key = None
            best_s = None
            for s in inst.groups[i]:
                key = (extra[s], len(inst.cost[s] - accum))
                if best_key is None or key < best_key:
                    best_key = key
                    best_s = s
            assert best_s is not None
            new_assign[i] = best_s
            accum |= inst.cost[best_s]
        if len(accum) < len(union):
            assign, union = new_assign, accum
        else:
            if len(accum) == len(union):
                assign = new_assign
            break
    return assign, union


def shrink(inst: Instance, assign: list[int | None], union: set[int]) -> tuple[list[int | None], set[int]]:
    """Drop union elements that no longer belong to any forced option, with repair."""
    best_assign, best_union = list(assign), set(union)
    for _ in range(8):
        forced: set[int] = set()
        ok = True
        for i in inst.paid:
            subs = [inst.cost[s] for s in inst.groups[i] if inst.cost[s] <= union]
            if not subs:
                ok = False
                break
            inter = set(subs[0])
            for extra in subs[1:]:
                inter &= extra
            forced |= inter
        if not ok:
            break
        rest = union - forced
        if not rest:
            break
        candidate = union - rest
        feasible = True
        for i in inst.paid:
            if not any(inst.cost[s] <= candidate for s in inst.groups[i]):
                feasible = False
                break
        if not feasible:
            # restore the cheapest missing elements per failing group
            for i in inst.paid:
                if any(inst.cost[s] <= candidate for s in inst.groups[i]):
                    continue
                s = min(inst.groups[i], key=lambda opt: len(inst.cost[opt] - candidate))
                candidate |= inst.cost[s]
            for i in inst.paid:
                if not any(inst.cost[s] <= candidate for s in inst.groups[i]):
                    feasible = False
                    break
        if not feasible or len(candidate) >= len(union):
            break
        union = candidate
        for i in inst.paid:
            s = min(inst.groups[i], key=lambda opt: (len(inst.cost[opt] - union),
                                                     len(inst.cost[opt])))
            assign[i] = s
        union = set()
        for i in inst.paid:
            union |= inst.cost[assign[i]]  # type: ignore[index]
        if len(union) < len(best_union):
            best_assign, best_union = list(assign), set(union)
        if len(union) == len(best_union):
            break
    return best_assign, best_union


def upper_bound(inst: Instance, restarts: int = 6, log: bool = False) -> dict:
    started = time.time()
    best: tuple[list[int | None], set[int]] | None = None
    starts: list[tuple[str, int | None, float]] = []
    for name in GREEDY_KEYS:
        starts.append((name, None, 0.0))
        for seed in range(restarts):
            starts.append((name, seed, (seed % 4) * 1.0 + 0.5))
    for pos, (key_name, seed, jitter) in enumerate(starts):
        phase = time.time()
        try:
            assign, union = greedy_solve(inst, GREEDY_KEYS[key_name], seed=seed, jitter=jitter)
        except ValueError:
            continue
        assign, union = refine(inst, assign, union)
        assign, union = shrink(inst, assign, union)
        if best is None or len(union) < len(best[1]):
            best = (assign, union)
        if log:
            _log(f"    start {pos + 1}/{len(starts)} {key_name} seed={seed} "
                 f"union={len(union)} best={len(best[1])} "
                 f"({time.time() - phase:.1f}s)")
    if best is None:
        raise ValueError("every greedy start failed")
    assign, union = best
    assign, union = refine(inst, assign, union)
    assign, union = shrink(inst, assign, union)
    return {
        "union_size": len(union),
        "assign": assign,
        "union": union,
        "seconds": round(time.time() - started, 3),
        "starts_tried": len(starts),
        "sum_of_chosen_option_sizes": sum(len(inst.cost[assign[i]]) for i in inst.paid),  # type: ignore[index]
        "free_groups": len(inst.free_groups),
        "paid_groups": len(inst.paid),
    }


def _pack(q: dict[int, float], counts: dict[int, dict[int, int]],
          budget: dict[int, float], order: list[int]) -> dict[int, float]:
    """Greedy feasible point for max sum q[c] with sum_t n[t,e]*c[t] <= budget[e]."""
    slack = dict(budget)
    c: dict[int, float] = {}
    for t in order:
        limit = min((slack[e] / n for e, n in counts[t].items()), default=1.0)
        limit = max(limit, 0.0)
        c[t] = limit
        for e, n in counts[t].items():
            slack[e] -= n * limit
    return c


def _group_pool_packing(inst: Instance) -> tuple[dict[int, int], int]:
    """Return exact integer numerators k[t] and a common denominator D.

    The represented dual weights lambda[t] = k[t]/D satisfy
    sum_{t: e in pool[t]} k[t] <= D for every element.  Starting with either
    zero weights or k[t] = 1, greedily fill the remaining integer capacities.
    All feasibility arithmetic is integral; floating point only orders groups.
    """
    if not inst.paid:
        return {}, 1
    minimum = {i: min(len(inst.cost[s]) for s in inst.groups[i]) for i in inst.paid}
    degree: Counter[int] = Counter()
    for i in inst.paid:
        degree.update(inst.pool[i])
    denominator = max(degree.values())
    orders = (
        sorted(inst.paid, key=lambda i: (len(inst.pool[i]), -minimum[i], i)),
        sorted(inst.paid, key=lambda i: (-minimum[i] / len(inst.pool[i]),
                                         len(inst.pool[i]), i)),
        sorted(inst.paid, key=lambda i: (-minimum[i], len(inst.pool[i]), i)),
    )
    best: dict[int, int] = {}
    best_value = -1
    for initial in (0, 1):
        for order in orders:
            weight = {i: initial for i in inst.paid}
            slack = {e: denominator - initial * n for e, n in degree.items()}
            for i in order:
                extra = denominator
                for e in inst.pool[i]:
                    extra = min(extra, slack[e])
                    if not extra:
                        break
                if not extra:
                    continue
                weight[i] += extra
                for e in inst.pool[i]:
                    slack[e] -= extra
            value = sum(minimum[i] * weight[i] for i in inst.paid)
            if value > best_value:
                best, best_value = weight, value
    return best, denominator


def _lp_relaxation_dual(inst: Instance) -> float:
    """Feasible dual bound for the group-pool relaxation of minimum union.

    Let P[t] be the union of all option cost sets in group t and let m[t] be
    their minimum size.  Every feasible union U contains a full chosen option
    in P[t], hence |U intersect P[t]| >= m[t].  The relaxation is therefore
    min sum_e x[e] subject to sum_{e in P[t]} x[e] >= m[t], x >= 0.
    Its dual maximises sum_t m[t]*lambda[t] subject to
    sum_{t: e in P[t]} lambda[t] <= 1, lambda >= 0.

    The old per-option intersection constraints were invalid: U need not
    intersect an unchosen option.  Keep this helper name and output field for
    compatibility, but pack group pools with exact integer capacities instead.
    """
    weight, denominator = _group_pool_packing(inst)
    value = sum(min(len(inst.cost[s]) for s in inst.groups[i]) * weight[i]
                for i in inst.paid)
    return value / denominator


def lower_bounds(inst: Instance) -> dict:
    groups = inst.groups
    paid = inst.paid
    per_group_min = [min(len(inst.cost[s]) for s in groups[i]) for i in paid]
    lb_min = max(per_group_min) if per_group_min else 0
    lb_sum_min = sum(per_group_min)

    lo, hi = 0, max(per_group_min, default=0)
    while lo < hi:
        mid = (lo + hi) // 2
        if all(any(len(inst.cost[s]) <= mid for s in groups[i]) for i in paid):
            hi = mid
        else:
            lo = mid + 1
    lb_threshold = lo

    deg = Counter()
    for i in paid:
        for s in groups[i]:
            for e in inst.cost[s]:
                deg[e] += 1
    lb_element = sum(min(sum(1.0 / deg[e] for e in inst.cost[s]) for s in groups[i])
                     for i in paid)

    counts: dict[int, dict[int, int]] = {}
    for i in paid:
        bag: Counter[int] = Counter()
        for s in groups[i]:
            for e in inst.cost[s]:
                bag[e] += 1
        counts[i] = dict(bag)

    def grouped_dual(c: dict[int, float], weight: dict[int, float]) -> float:
        # gamma_{t,e} = c_t * w_e;  alpha_t = c_t * min_s sum_{e in C(s)} w_e.
        # Feasibility of (c, weight) holds by construction: _pack keeps
        # sum_t n[t,e] c[t] <= 1/w[e], and weights are set as 1/used.  No
        # per-element re-verification here (that loop is quadratic in the
        # universe size); solve_instance cross-checks LB <= UB instead.
        total = 0.0
        for i in paid:
            total += c.get(i, 0.0) * min(sum(weight[e] for e in inst.cost[s])
                                         for s in groups[i])
        return total

    weight = {e: 1.0 for e in deg}
    best_grouped = 0.0
    for _ in range(5):
        q = {i: min(sum(weight[e] for e in inst.cost[s]) for s in groups[i]) for i in paid}
        budget = {e: (1.0 / weight[e]) for e in deg}
        orders = [
            sorted(paid, key=lambda i: -q[i]),
            sorted(paid, key=lambda i: (-q[i] / max(len(inst.pool[i]), 1))),
            sorted(paid, key=lambda i: (len(inst.pool[i]), -q[i])),
        ]
        c: dict[int, float] = {}
        for order in orders:
            trial = _pack(q, counts, budget, order)
            if sum(q[i] * trial[i] for i in paid) > sum(q[i] * c.get(i, 0.0) for i in paid):
                c = trial
        best_grouped = max(best_grouped, sum(q[i] * c[i] for i in paid))
        used: dict[int, float] = {}
        for i in paid:
            ci = c.get(i, 0.0)
            if ci <= 0.0:
                continue
            for e, n in counts[i].items():
                used[e] = used.get(e, 0.0) + n * ci
        weight = {e: (1.0 / used[e] if e in used else 1.0) for e in deg}
        best_grouped = max(best_grouped, grouped_dual(c, weight))

    lb_lp = _lp_relaxation_dual(inst)

    assert lb_threshold >= lb_min
    return {
        "per_group_min_max": int(lb_min),
        "per_group_min_sum_no_sharing_reference": int(lb_sum_min),
        "threshold_cover_max_of_min_option": int(lb_threshold),
        "element_only_fractional_dual": round(lb_element, 3),
        "grouped_fractional_dual_alternating_packing": round(best_grouped, 3),
        "lp_relaxation_dual_fractional_packing": round(lb_lp, 3),
        "best_valid_lower_bound": round(
            max(lb_min, lb_threshold, lb_element, best_grouped, lb_lp), 3),
    }


def solve_instance(inst: Instance, restarts: int = 6, log: bool = False) -> dict:
    if log:
        _log(f"  upper bound: {len(inst.paid)} paid groups, "
             f"{len(inst.in_play)} options, 4 + 4*{restarts} starts")
    ub = upper_bound(inst, restarts=restarts, log=log)
    if log:
        _log(f"  upper bound done: union={ub['union_size']} ({ub['seconds']}s); "
             f"computing lower bounds")
    lb = lower_bounds(inst)
    if log:
        _log(f"  lower bounds done: best={lb['best_valid_lower_bound']} "
             f"(lp={lb['lp_relaxation_dual_fractional_packing']}, "
             f"grouped={lb['grouped_fractional_dual_alternating_packing']}, "
             f"element={lb['element_only_fractional_dual']})")
    assert lb["best_valid_lower_bound"] <= ub["union_size"] + 1e-9, (
        f"lower bound {lb['best_valid_lower_bound']} exceeds feasible upper bound "
        f"{ub['union_size']}: dual construction is broken")
    return {"upper_bound": ub["union_size"],
            "lower_bound": lb["best_valid_lower_bound"],
            "lower_bounds": lb,
            "sum_of_chosen_option_sizes": ub["sum_of_chosen_option_sizes"],
            "free_groups": ub["free_groups"],
            "paid_groups": ub["paid_groups"],
            "distinct_groups": len(inst.groups),
            "starts_tried": ub["starts_tried"],
            "seconds": ub["seconds"],
            "_assign": ub["assign"],
            "_union": ub["union"]}


def _log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def _dedup(groups: list[list[int]], labels: list[tuple]) -> tuple[list[list[int]], list[list[tuple]]]:
    """Merge identical option sets, keeping every (first, reply, third) label."""
    order: list[frozenset] = []
    index: dict[frozenset, int] = {}
    out_groups: list[list[int]] = []
    out_labels: list[list[tuple]] = []
    for opts, lab in zip(groups, labels):
        key = frozenset(opts)
        if key in index:
            out_labels[index[key]].append(lab)
        else:
            index[key] = len(order)
            order.append(key)
            out_groups.append(list(opts))
            out_labels.append([lab])
    return out_groups, out_labels


def build_instances(graph: dict) -> tuple[list[tuple[str, Instance]], Instance]:
    cost = [set(row) for row in graph["s4_cost"]]
    roots = graph["roots"]
    per_root = []
    all_groups: list[list[int]] = []
    all_labels: list[tuple] = []
    for root in roots:
        if root["role"] == "known-loss-baseline":
            continue
        groups = [list(row["options"]) for row in root["thirds"]]
        labels = [(root["origin_first"], root["origin_reply"], row["third"])
                  for row in root["thirds"]]
        d_groups, d_labels = _dedup(groups, labels)
        per_root.append((f"{root['origin_first']}/{root['origin_reply']}",
                         Instance(d_groups, d_labels, cost)))
        all_groups.extend(groups)
        all_labels.extend(labels)
    j_groups, j_labels = _dedup(all_groups, all_labels)
    joint = Instance(j_groups, j_labels, cost)
    return per_root, joint


def plan_payload(inst: Instance, assign: list[int | None],
                 masks: list[str] | None = None) -> dict:
    """Canonical, human-checkable dump of one instance's chosen options."""
    entries = []
    for i in inst.paid:
        s = assign[i]
        assert s is not None
        for first, reply, third in inst.labels[i]:
            entries.append({"first": first, "reply": reply, "third": third,
                            "s4_class_index": s,
                            "s4_mask": masks[s] if masks else None,
                            "unknown_s5_children": len(inst.cost[s])})
    entries.sort(key=lambda row: (row["first"], row["reply"], row["third"]))
    return {"distinct_groups": len(inst.groups),
            "free_groups": len(inst.free_groups),
            "paid_groups": len(inst.paid),
            "third_moves_covered": inst.label_count,
            "union_size": len({e for i in inst.paid for e in inst.cost[assign[i]]}),  # type: ignore[index]
            "groups": entries}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path, default=EXPERIMENT / "output/dependency-graph.json.gz")
    parser.add_argument("--output", type=Path, default=EXPERIMENT / "output/optimization-results.json")
    parser.add_argument("--plan", type=Path, default=EXPERIMENT / "output/chosen-plans.json")
    parser.add_argument("--restarts", type=int, default=3,
                        help="jittered greedy restarts per key per instance")
    parser.add_argument("--verbose", action="store_true",
                        help="per-start progress on stderr")
    parser.add_argument("--skip-individual", action="store_true")
    parser.add_argument("--skip-joint", action="store_true")
    args = parser.parse_args()

    graph_path = args.graph if args.graph.is_absolute() else ROOT / args.graph
    with gzip.open(graph_path, "rt", encoding="utf-8") as stream:
        graph = json.load(stream)

    per_root, joint = build_instances(graph)
    s4_masks = graph["s4_masks"]
    _log(f"joint instance: {len(joint.groups)} distinct groups "
         f"({len(joint.paid)} paid, {len(joint.free_groups)} free), "
         f"{len(joint.in_play)} options in play")

    def union_of(inst: Instance, assign: list[int | None]) -> set[int]:
        out: set[int] = set()
        for i in inst.paid:
            out |= inst.cost[assign[i]]  # type: ignore[index]
        return out

    root_rows = []
    plans = {}
    total_individual = 0
    total_lower = 0
    cheapest = None
    if not args.skip_individual:
        for name, inst in per_root:
            _log(f"solving individual root {name} "
                 f"({len(inst.groups)} groups, {len(inst.in_play)} options)")
            result = solve_instance(inst, restarts=args.restarts, log=args.verbose)
            assign = result.pop("_assign")
            result.pop("_union")
            first = int(name.split("/")[0])
            row = {"root": name, "first_move": first,
                   "individual_upper_bound_new_s5": result["upper_bound"],
                   "individual_lower_bound_new_s5": result["lower_bound"],
                   **{k: v for k, v in result.items()
                      if k not in ("lower_bounds", "upper_bound", "lower_bound")}}
            row["lower_bounds"] = result["lower_bounds"]
            row["independent_sum_of_per_group_minima"] = result["lower_bounds"]["per_group_min_sum_no_sharing_reference"]
            total_individual += result["upper_bound"]
            total_lower += result["lower_bound"]
            if cheapest is None or result["upper_bound"] < cheapest[1]:
                cheapest = (first, result["upper_bound"])
            payload = plan_payload(inst, assign, s4_masks)
            payload["required_new_s5"] = sorted(union_of(inst, assign))
            plans[name] = payload
            root_rows.append(row)
            _log(f"  -> upper {result['upper_bound']}  lower {result['lower_bound']}")

    joint_result = None
    joint_assign: list[int | None] = []
    joint_union: set[int] = set()
    if not args.skip_joint:
        _log("solving joint 19-root instance")
        joint_result = solve_instance(joint, restarts=args.restarts, log=args.verbose)
        joint_assign = joint_result.pop("_assign")
        joint_union = joint_result.pop("_union")
        plans["_joint_19_roots"] = plan_payload(joint, joint_assign, s4_masks)
        plans["_joint_19_roots"]["required_new_s5"] = sorted(joint_union)
        _log(f"  -> upper {joint_result['upper_bound']}  lower {joint_result['lower_bound']}")

    group_count: Counter[int] = Counter()
    per_root_sets: dict[int, set[tuple]] = defaultdict(set)
    per_third_sets: dict[int, set[tuple]] = defaultdict(set)
    if joint_result is not None:
        for i in joint.paid:
            s = joint_assign[i]
            for label in joint.labels[i]:
                first_i, reply_i, third_i = label
                for e in joint.cost[s]:  # type: ignore[index]
                    group_count[e] += 1
                    per_root_sets[e].add((first_i, reply_i))
                    per_third_sets[e].add((first_i, reply_i, third_i))
    multi_group = sum(1 for v in group_count.values() if v > 1)
    multi_root = sum(1 for v in per_root_sets.values() if len(v) > 1)
    histogram = Counter(group_count.values())

    joint_payload = None
    if joint_result is not None:
        joint_payload = {
            "upper_bound_new_s5": joint_result["upper_bound"],
            "lower_bound_new_s5": joint_result["lower_bound"],
            "lower_bounds": joint_result["lower_bounds"],
            "free_groups": joint_result["free_groups"],
            "paid_groups": joint_result["paid_groups"],
            "distinct_groups": joint_result["distinct_groups"],
            "sum_of_chosen_option_sizes": joint_result["sum_of_chosen_option_sizes"],
            "starts_tried": joint_result["starts_tried"],
            "seconds": joint_result["seconds"],
            "independent_sum_of_per_group_minima":
                joint_result["lower_bounds"]["per_group_min_sum_no_sharing_reference"],
        }

    sharing = None
    if joint_result is not None and total_individual:
        sharing = {
            "individual_upper_bound_sum": total_individual,
            "joint_upper_bound": joint_result["upper_bound"],
            "saved_new_s5": total_individual - joint_result["upper_bound"],
            "saved_fraction": round(
                (total_individual - joint_result["upper_bound"]) / total_individual, 4),
        }

    result = {
        "schema": "n11-joint-s5-optimization-v1",
        "graph": str(graph_path.relative_to(ROOT)),
        "graph_counts": graph["counts"],
        "trust_boundary": (
            "Upper bounds are feasible optimistic LOSS proof plans that assume every "
            "listed unknown exact-S5 position eventually becomes LOSS. Lower bounds are "
            "valid for this finite selection problem only; they are not solver node "
            "counts, runtimes, or outcome proofs."
        ),
        "group_deduplication": (
            "Third moves whose option sets are identical share one group. Covering one "
            "member with option s covers every member at no extra cost, so the "
            "minimum-union value is unchanged by the merge."
        ),
        "individual_roots": root_rows,
        "individual_upper_bound_sum_over_19_roots": total_individual,
        "individual_lower_bound_sum_over_19_roots": total_lower,
        "joint_19_roots": joint_payload,
        "sharing_effect": sharing,
        "cheapest_single_new_loss_orbit": {
            "first_move": cheapest[0] if cheapest else None,
            "optimistic_new_s5_upper_bound": cheapest[1] if cheapest else None,
            "note": "Best individual upper bound among the evaluated reply candidates.",
        },
        "per_new_s5_contribution_in_joint_plan": {
            "distinct_new_s5": len(joint_union) if joint_result is not None else 0,
            "groups_per_s5_histogram": {str(k): v for k, v in sorted(histogram.items())},
            "s5_used_by_more_than_one_group": multi_group,
            "s5_used_by_more_than_one_root": multi_root,
            "max_groups_for_one_s5": max(group_count.values()) if group_count else 0,
            "max_roots_for_one_s5": max(map(len, per_root_sets.values())) if per_root_sets else 0,
            "max_thirds_for_one_s5": max(map(len, per_third_sets.values())) if per_third_sets else 0,
            "mean_groups_per_s5": round(sum(group_count.values()) / len(group_count), 3)
            if group_count else 0.0,
            "mean_roots_per_s5": round(sum(map(len, per_root_sets.values())) / len(per_root_sets), 3)
            if per_root_sets else 0.0,
            "mean_thirds_per_s5": round(sum(map(len, per_third_sets.values())) / len(per_third_sets), 3)
            if per_third_sets else 0.0,
        },
        "method": {
            "upper_bound": "multi-start marginal-cost greedy, alternating re-pick inside the "
                           "union, forced-element shrinking with repair",
            "lower_bounds": ["max over groups of min option size",
                             "smallest threshold whose options still cover every group",
                             "element-only fractional dual",
                             "grouped fractional dual by alternating packing",
                             "group-pool dual: sum_{e in pool[t]} x[e] >= min_s |C(s)|; "
                             "exact integer-capacity fractional packing"],
            "exactness": "no branch-and-bound optimality proof; upper and lower bounds are "
                         "reported separately and the gap is not closed",
        },
    }

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n")
    plan_path = args.plan if args.plan.is_absolute() else ROOT / args.plan
    with plan_path.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps({"schema": "n11-joint-s5-chosen-plans-v1",
                                 "source_graph": str(graph_path.relative_to(ROOT)),
                                 "plans": plans}, ensure_ascii=False,
                                separators=(",", ":")) + "\n")
    print(json.dumps({
        "individual_sum": total_individual,
        "joint": joint_result["upper_bound"] if joint_result else None,
        "joint_lower": joint_result["lower_bound"] if joint_result else None,
        "saved": (total_individual - joint_result["upper_bound"])
        if (joint_result and total_individual) else None,
        "cheapest_orbit": result["cheapest_single_new_loss_orbit"],
        "per_root": [(r["root"], r["individual_upper_bound_new_s5"],
                      r["individual_lower_bound_new_s5"]) for r in root_rows],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
