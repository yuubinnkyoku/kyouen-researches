#!/usr/bin/env python3
"""Exact-rational certificate for the K0417 element-only fractional dual bound.

Primal (exact): choose one S4 option per paid third-move group, minimising the
number of distinct unknown exact-S5 children bought.  LP relaxation R1 uses a
convex choice y[t,s] per group and element variables x[e] with x[e] >= y[t,s]
for e in C(s).  Its dual is

    max sum_t alpha[t]
    s.t. alpha[t] <= sum_{e in C(s)} beta[t,s,e]   for every paid (t, s),
         sum_{(t,s) with e in C(s)} beta[t,s,e] <= 1   for every element e,
         alpha, beta >= 0.

The element-only family sets beta[t,s,e] = w[e].  Feasibility then needs
deg[e]*w[e] <= 1 with deg[e] = #{(t,s): e in C(s)}, and the objective
sum_t min_s sum_{e in C(s)} w[e] is monotone in w, so w[e] = 1/deg[e] is the
family optimum.  Any dual-feasible value L bounds the LP optimum, hence the
exact integer optimum OPT satisfies OPT >= ceil(L).

This script recomputes deg from the dependency graph, evaluates each group's
weight sum exactly with Fraction arithmetic on the float-argmin option (any
single option per group is dual-valid; the argmin only affects strength),
and stores {deg, per-group alpha as numerator/denominator, exact total}.
--verify reloads the certificate, recounts deg from the graph, and checks the
rational total, adopting ceil(total) as the integer lower bound.  No solver
search is involved; no unknown verdict is asserted.
"""
from __future__ import annotations

import argparse
import gzip
import json
import sys
import time
from collections import Counter
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
NEW_EXPERIMENT = ROOT / "research/experiments/n11-proof-cost-comparison-20261012"
OLD_EXPERIMENT = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
OLD_SCRIPTS = OLD_EXPERIMENT / "scripts"

sys.path.insert(0, str(OLD_SCRIPTS))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
from optimize_s5_selection import Instance, _dedup  # noqa: E402
from analyze_central_reply_frontier import sha  # noqa: E402


def load_joint_instance(graph: dict) -> Instance:
    cost = [set(row) for row in graph["s4_cost"]]
    groups: list[list[int]] = []
    labels: list[tuple] = []
    for root in graph["roots"]:
        if root["role"] == "known-loss-baseline":
            continue
        for row in root["thirds"]:
            groups.append(list(row["options"]))
            labels.append((root["origin_first"], root["origin_reply"], row["third"]))
    return Instance(*_dedup(groups, labels), cost)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--graph", type=Path,
                        default=OLD_EXPERIMENT / "output/dependency-graph.json.gz")
    parser.add_argument("--output", type=Path,
                        default=NEW_EXPERIMENT / "output/element-dual-certificate.json")
    parser.add_argument("--verify", type=Path, default=None,
                        help="verify this certificate file instead of building it")
    args = parser.parse_args()
    started = time.time()

    graph_path = args.graph if args.graph.is_absolute() else ROOT / args.graph
    with gzip.open(graph_path, "rt", encoding="utf-8") as stream:
        graph = json.load(stream)

    if args.verify is not None:
        cert = json.loads(args.verify.read_text(encoding="utf-8"))
        assert cert["schema"] == "n11-element-dual-certificate-v1"
        assert cert["graph_sha256"] == sha(graph_path), "graph file changed"
        inst = load_joint_instance(graph)
        assert len(inst.paid) == cert["paid_groups"], "paid group count changed"
        deg = Counter()
        for i in inst.paid:
            for s in inst.groups[i]:
                for e in inst.cost[s]:
                    deg[e] += 1
        stored_deg = {int(k): v for k, v in cert["deg"].items()}
        assert dict(deg) == stored_deg, "deg recount mismatch"
        total = Fraction(0)
        for row in cert["groups"]:
            i = row["group"]
            s = row["option"]
            exact = sum(Fraction(1, deg[e]) for e in inst.cost[s])
            assert [exact.numerator, exact.denominator] == row["alpha_exact"], \
                f"group {i}: alpha mismatch"
            total += exact
        assert [total.numerator, total.denominator] == cert["total_exact"], \
            "total mismatch"
        integer_lb = -(-total.numerator // total.denominator)
        assert integer_lb == cert["integer_lower_bound"], "ceil mismatch"
        print(json.dumps({"verified": True, "groups": len(cert["groups"]),
                          "total_exact": cert["total_exact"],
                          "total_float": float(total),
                          "integer_lower_bound": integer_lb,
                          "seconds": round(time.time() - started, 1)},
                         ensure_ascii=False, indent=2))
        return

    inst = load_joint_instance(graph)
    assert len(inst.paid) == 869 and len(inst.groups) == 948, \
        f"unexpected instance shape: {len(inst.groups)} groups, {len(inst.paid)} paid"
    deg = Counter()
    for i in inst.paid:
        for s in inst.groups[i]:
            for e in inst.cost[s]:
                deg[e] += 1
    assert len(deg) <= graph["counts"]["s5_cost_universe"], "deg exceeds universe"
    print(f"deg elements in paid play: {len(deg)} "
          f"(universe {graph['counts']['s5_cost_universe']}; the rest occur only "
          f"in free-group or win-excluded options and carry no dual constraint)",
          file=sys.stderr, flush=True)

    rows = []
    total = Fraction(0)
    total_float = 0.0
    for i in inst.paid:
        scored = [(sum(1.0 / deg[e] for e in inst.cost[s]), s)
                  for s in inst.groups[i]]
        _, s_best = min(scored)
        exact = sum(Fraction(1, deg[e]) for e in inst.cost[s_best])
        total += exact
        total_float += sum(1.0 / deg[e] for e in inst.cost[s_best])
        rows.append({"group": i, "labels": [list(lab) for lab in inst.labels[i]],
                     "option": s_best,
                     "option_size": len(inst.cost[s_best]),
                     "alpha_exact": [exact.numerator, exact.denominator],
                     "alpha_float": float(exact)})
    integer_lb = -(-total.numerator // total.denominator)
    assert abs(total_float - 6573.146) < 5e-4, \
        f"K0417 headline mismatch: {total_float}"
    cert = {
        "schema": "n11-element-dual-certificate-v1",
        "graph": str(graph_path.relative_to(ROOT)),
        "graph_sha256": sha(graph_path),
        "method": ("element-only dual beta[t,s,e]=1/deg[e], family-optimal by "
                   "monotonicity; per-group alpha is the exact rational weight "
                   "sum of the float-argmin option, dual-valid for any option"),
        "integer_bound_conditions": [
            "dual feasibility: deg[e]=#{(t,s): e in C(s)} recounted from the "
            "graph, alpha[t]<=sum_{e in C(s)} 1/deg[e] for every option s "
            "(checked by the verifier with exact rationals)",
            "integrality: the exact selection optimum is a union cardinality, "
            "hence an integer, so OPT >= ceil(total)",
        ],
        "paid_groups": len(inst.paid),
        "elements": len(deg),
        "deg": {str(e): d for e, d in sorted(deg.items())},
        "groups": rows,
        "total_exact": [total.numerator, total.denominator],
        "total_float": float(total),
        "total_float_check": total_float,
        "integer_lower_bound": integer_lb,
        "seconds": round(time.time() - started, 1),
    }
    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8", newline="\n") as stream:
        stream.write(json.dumps(cert, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({"certificate": str(output.relative_to(ROOT)),
                      "total_float": float(total),
                      "integer_lower_bound": integer_lb,
                      "k0417_reported": 6573.146,
                      "seconds": round(time.time() - started, 1)},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
