"""Second joint-plan update after terminal-verified S5 121263 LOSS / 145001 LOSS.

Flow is the same as n11-adaptive-plan-update-20261013/scripts/update_loss_plan.py,
but the baseline is the FIRST update output (union 31,730) and the verdict set
gains the two adaptive-probe receipts:

* 121263 LOSS / 145001 LOSS: both are known LOSS children, so they are dropped
  from every cost set and can no longer appear in any required union.  The WIN
  side of the verdict set is unchanged, so the excluded S4 class set is
  unchanged and no response has to be re-selected around.

Historical inputs remain unchanged.  Every kept and every re-selected response
and every complete S5 boundary is rebuilt from independent geometry plus the
explicit exact-S5 cache augmented only by the six terminal-verified receipts.
No unknown verdict is asserted; the output is still an optimistic plan, not a
root proof.  K0423, the existing outputs, the first-update outputs and the
history are never written to.
"""
from __future__ import annotations

import gzip
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
OLD = ROOT / "research/experiments/n11-joint-s5-proof-planning-20261012/output"
K0423 = ROOT / "research/experiments/n11-s5-s6-quotient-20261013/output"
ADAPTIVE = ROOT / "research/experiments/n11-adaptive-verify-20261013/output"
PROBE = ROOT / "research/experiments/n11-adaptive-probe-20261013/output"
PREV = ROOT / "research/experiments/n11-adaptive-plan-update-20261013/output"

sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache  # noqa: E402

NEW_LOSSES = (121263, 145001)


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(mask: int):
    return mask & ((1 << 64) - 1), mask >> 64


def load_receipt(receipt_path: Path, cert_path: Path, mask: int, sources: dict) -> int:
    receipt = json.loads(receipt_path.read_text())
    assert receipt["trusted_leaves"] == 0, receipt_path
    assert sha(cert_path) == receipt["certificate_sha256"], receipt_path
    assert str(mask) == receipt["root_mask"], receipt_path
    sources.update({str(p.relative_to(ROOT)): sha(p) for p in (receipt_path, cert_path)})
    return receipt["verdict"]


def main() -> None:
    with gzip.open(OLD / "dependency-graph.json.gz", "rt") as stream:
        g = json.load(stream)
    baseline_path = PREV / "repaired-joint-plan-update.json"
    baseline = json.loads(baseline_path.read_text())
    assert baseline["verification"]["passed"]
    assert baseline["union_size"] == 31730, baseline["union_size"]
    old_entries = {(e["first"], e["reply"], e["third"]): e for e in baseline["groups"]}

    sources = {
        str((OLD / "dependency-graph.json.gz").relative_to(ROOT)):
            sha(OLD / "dependency-graph.json.gz"),
        str(baseline_path.relative_to(ROOT)): sha(baseline_path),
    }
    new_verdicts: dict[int, int] = {}
    for index in (558600, 209644):  # K0423 pilot receipts
        mask = g["s5_masks"][index][0] | g["s5_masks"][index][1] << 64
        new_verdicts[index] = load_receipt(
            K0423 / f"pilot-{index}-terminal-verification.json",
            K0423 / f"pilot-{index}-terminal-dag.json.gz", mask, sources)
    for index in (126899, 144095):  # adaptive-verify receipts
        mask = g["s5_masks"][index][0] | g["s5_masks"][index][1] << 64
        assert json.loads((ADAPTIVE / f"pilot-{index}-receipt.json").read_text())[
            "pruned_roundtrip_verified"], index
        new_verdicts[index] = load_receipt(
            ADAPTIVE / f"pilot-{index}-receipt.json",
            ADAPTIVE / f"pilot-{index}-terminal-dag.json.gz", mask, sources)
    assert {str(k): v for k, v in new_verdicts.items()} == baseline["resolved_s5_verdicts"]
    for index in NEW_LOSSES:  # adaptive-probe receipts (this round)
        mask = g["s5_masks"][index][0] | g["s5_masks"][index][1] << 64
        receipt = json.loads((PROBE / f"adaptive-{index}-receipt.json").read_text())
        assert receipt["s5_index"] == index
        assert receipt["manifest_trace_sha256_match"], index
        assert receipt["pruned_roundtrip_verified"], index
        new_verdicts[index] = load_receipt(
            PROBE / f"adaptive-{index}-receipt.json",
            PROBE / f"adaptive-{index}-terminal-dag.json.gz", mask, sources)
    assert new_verdicts == {558600: 2, 209644: 1, 126899: 2, 144095: 1,
                            121263: 2, 145001: 2}, new_verdicts

    losses = {i for i, v in new_verdicts.items() if v == 2}
    wins = {i for i, v in new_verdicts.items() if v == 1}
    assert set(NEW_LOSSES) <= losses and not set(NEW_LOSSES) & wins
    cost = [set(c) - losses for c in g["s4_cost"]]
    excluded = {s for s, c in enumerate(g["s4_cost"]) if wins.intersection(c)}
    baseline_excluded = set(baseline["excluded_s4_classes"])
    assert excluded == baseline_excluded, "WIN set changed; exclusion set drifted"

    options: dict[tuple, list[int]] = {}
    choices: dict[tuple, int] = {}
    pairs: dict[tuple, int] = {}
    changed = []
    for root in g["roots"]:
        if root["role"] == "known-loss-baseline":
            continue
        first, reply = root["origin_first"], root["origin_reply"]
        pairs[(first, reply)] = root["pair_mask"][0] | root["pair_mask"][1] << 64
        for r in root["thirds"]:
            ident = (first, reply, r["third"])
            opts = [s for s in r["options"] if s not in excluded]
            assert opts, f"no optimistic response for {ident}"
            options[ident] = opts
            if ident in old_entries:
                s = old_entries[ident]["s4_class_index"]
                if s not in excluded:
                    choices[ident] = s
    assert set(old_entries) == set(options), "baseline third coverage drift"

    union = set().union(*(cost[s] for s in choices.values()))
    baseline_required = set(baseline["required_new_s5"])
    for ident in sorted(options):
        if ident in choices:
            continue
        before = len(union)
        s = min(options[ident], key=lambda t: (len(cost[t] - union), len(cost[t]), t))
        choices[ident] = s
        union |= cost[s]
        changed.append(dict(first=ident[0], reply=ident[1], third=ident[2],
                            old_s4=old_entries[ident]["s4_class_index"], new_s4=s,
                            marginal_new_elements=len(union) - before,
                            added_vs_baseline_union=len(cost[s] - baseline_required)))
    assert not wins.intersection(union) and not losses.intersection(union), \
        "known WIN/LOSS child inside the required union"

    board = Board(11)
    cache = load_exact_s5_cache(board)
    for i, v in new_verdicts.items():
        cache[tuple(g["s5_masks"][i])] = {"verdict": v}

    s5 = {g["s5_masks"][i][0] | g["s5_masks"][i][1] << 64: i for i in union}
    checked: dict[int, int] = {}
    entries = []
    for pair, mask in pairs.items():
        expected = set(board.points(board.legal(mask)))
        actual = {ident[2] for ident in choices if ident[:2] == pair}
        assert actual == expected and len(actual) == 119, pair
    for ident, s in sorted(choices.items()):
        mask = g["s4_masks"][s][0] | g["s4_masks"][s][1] << 64
        s3 = pairs[ident[:2]] | 1 << ident[2]
        witness = next((p for p in board.points(board.legal(s3))
                        if board.canonical(s3 | 1 << p) == mask), None)
        assert witness is not None, (ident, s)
        if s not in checked:
            children = board.children(mask)
            assert all(cache.get(key(c), {}).get("verdict") != 1 for c in children), \
                (s, "known WIN child")
            unknown = {c for c in children if key(c) not in cache}
            expected = {g["s5_masks"][i][0] | g["s5_masks"][i][1] << 64 for i in cost[s]}
            assert unknown == expected, (s, "incomplete cost boundary")
            checked[s] = len(children)
        entries.append(dict(first=ident[0], reply=ident[1], third=ident[2], fourth=witness,
                            s4_class_index=s, s4_mask=g["s4_masks"][s],
                            unknown_s5_children=len(cost[s])))
    required = set().union(*(cost[e["s4_class_index"]] for e in entries))
    assert required == union
    assert len(entries) == baseline["third_moves_covered"] == 2261
    assert len(pairs) == 19
    for i in NEW_LOSSES:
        assert i not in s5, f"{i} still required"

    out = dict(
        schema="n11-adaptive-repaired-joint-plan-update2-v1",
        baseline_plan_sha256=sha(baseline_path),
        baseline_schema=baseline["schema"],
        source_sha256=sources,
        baseline_union_size=baseline["union_size"], union_size=len(union),
        union_delta_vs_baseline=len(union) - baseline["union_size"],
        roots=len(pairs), third_moves_covered=len(entries),
        baseline_free_thirds=baseline["free_thirds"],
        free_thirds=sum(e["unknown_s5_children"] == 0 for e in entries),
        baseline_excluded_s4_classes=sorted(baseline_excluded),
        excluded_s4_classes=sorted(excluded),
        new_excluded_s4_classes=sorted(excluded - baseline_excluded),
        baseline_resolved_s5_verdicts=baseline["resolved_s5_verdicts"],
        resolved_s5_verdicts={str(k): v for k, v in sorted(new_verdicts.items())},
        known_loss_removed_from_cost=sorted(NEW_LOSSES),
        changed_choice_count=len(changed), changed_choices=changed,
        groups=entries, required_new_s5=sorted(union),
        verification=dict(passed=True, checked_selected_s4=len(checked),
                          complete_third_boundaries=len(pairs),
                          complete_s5_boundaries=len(checked),
                          third_moves_checked=len(entries),
                          known_win_selected=0,
                          known_loss_in_union=0),
        trust=("optimistic plan only: old exact-S5 leaves remain solver-trusted; six "
               "additions (558600 LOSS, 209644 WIN, 126899 LOSS, 144095 WIN, "
               "121263 LOSS, 145001 LOSS) terminal-verified with trusted leaves 0; "
               "all remaining required S5 verdicts UNKNOWN; not a root proof"),
    )
    target = EXP / "output/repaired-joint-plan-update2.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("groups", "required_new_s5", "source_sha256",
                                   "changed_choices")}, indent=2))


if __name__ == "__main__":
    main()
