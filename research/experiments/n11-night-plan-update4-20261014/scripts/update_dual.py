"""Exact element-only dual for the fourth (night-batch2) updated plan instance.

Same method as n11-night-plan-update3-20261014/scripts/update_dual.py (itself a
copy of the second-update dual, which copied the first-update dual and
n11-s5-s6-quotient-20261013/scripts/updated_dual.py): every option inequality
is checked with Fraction (no floating argmin), the certificate records every
group once, and --verify reconstructs the certificate from the plan instead of
trusting it.

The dual is a pure function of the plan's legal candidate sets and element-cost
obligations; those are identical for the batch and the (degenerate) staged
reflection (see repaired-joint-plan-update4.json / batch_vs_staged), so one
certificate covers both reflections.
"""
from __future__ import annotations

import argparse
from collections import Counter
from fractions import Fraction
import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OLD = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012"
sys.path.insert(0, str(OLD / "scripts"))
from optimize_s5_selection import Instance, _dedup  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--verify", type=Path)
    args = parser.parse_args()
    plan_path = EXP / "output/repaired-joint-plan-update4.json"
    plan = json.loads(plan_path.read_text())
    assert plan["verification"]["passed"]
    for path, digest in plan["source_sha256"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest
    with gzip.open(OLD / "output/dependency-graph.json.gz", "rt") as stream:
        g = json.load(stream)
    verdicts = {int(k): v for k, v in plan["resolved_s5_verdicts"].items()}
    losses = {e for e, v in verdicts.items() if v == 2}
    excluded = set(plan["excluded_s4_classes"])
    cost = [set(c) - losses for c in g["s4_cost"]]
    groups = []
    labels = []
    for root in g["roots"]:
        if root["role"] == "known-loss-baseline":
            continue
        for row in root["thirds"]:
            groups.append([s for s in row["options"] if s not in excluded])
            labels.append((root["origin_first"], root["origin_reply"], row["third"]))
    inst = Instance(*_dedup(groups, labels), cost)
    deg = Counter()
    for i in inst.paid:
        for s in inst.groups[i]:
            deg.update(cost[s])
    scores = {s: sum((Fraction(1, deg[e]) for e in cost[s]), Fraction())
              for s in inst.in_play}
    rows = []
    total = Fraction()
    for i in inst.paid:
        value, s = min((scores[s], s) for s in inst.groups[i])
        assert all(value <= scores[t] for t in inst.groups[i])
        rows.append(dict(group=i, option=s, labels=inst.labels[i],
                         alpha=[value.numerator, value.denominator]))
        total += value
    degree_hash = hashlib.sha256(
        json.dumps(sorted(deg.items()), separators=(",", ":")).encode()).hexdigest()
    result = dict(
        schema="n11-night-updated-exact-element-dual-update4-v1",
        repaired_plan_sha256=hashlib.sha256(plan_path.read_bytes()).hexdigest(),
        baseline_dual_schema="n11-night-updated-exact-element-dual-update3-v1",
        groups=rows, distinct_groups=len(inst.groups), paid_groups=len(inst.paid),
        options_scored=len(scores), elements=len(deg), degree_sha256=degree_hash,
        total_exact=[total.numerator, total.denominator], total_float=float(total),
        integer_lower_bound=-(-total.numerator // total.denominator),
        upper_bound=plan["union_size"],
        method=("beta[t,s,e]=1/deg[e]; exact minimum over ALL options in each paid "
                "group; all degree capacities equal 1; ceil by integrality"),
        note=("identical certificate for the batch and the degenerate staged "
              "reflection: the dual depends only on legal candidate sets and "
              "element-cost obligations, which batch_vs_staged shows to be "
              "identical"),
    )
    assert result["integer_lower_bound"] <= result["upper_bound"]
    if args.verify:
        cert = json.loads(args.verify.read_text())
        # JSON turns tuple labels into lists; normalize for exact comparison.
        assert cert == json.loads(json.dumps(result)), "certificate mismatch"
        print(json.dumps(dict(verified=True, groups_checked=len(rows),
                              option_inequalities_checked=sum(
                                  len(inst.groups[i]) for i in inst.paid),
                              total_exact=result["total_exact"],
                              integer_lower_bound=result["integer_lower_bound"]),
                         indent=2))
    else:
        target = EXP / "output/updated-element-dual-update4.json"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(result, sort_keys=True, indent=2) + "\n")
        print(json.dumps({k: v for k, v in result.items() if k != "groups"}, indent=2))


if __name__ == "__main__":
    main()
