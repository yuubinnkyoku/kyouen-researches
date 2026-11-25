"""Seventh joint-plan update after the S6 terminal LOSS and the 162106 WIN.

Flow follows n11-night-plan-update6-20261014/scripts/update_loss_plan.py.
The baseline is the SIXTH update output (union 31,774) and the verdict set
gains, from frozen inputs:

* 162106 WIN (night-batch5 receipt, trusted leaves 0): every S4 class that
  needs 162106 (as a legal S5 child) to be a non-WIN verdict leaves the option
  sets; any baseline response still selected on those classes is re-selected
  greedily inside the remaining legal options.  The three newly excluded
  classes 4327 / 4328 / 5056 were never selected on the sixth-update baseline
  (and 5830 has been excluded since the third update), so the greedy repair is
  expected to be vacuous.
* three S5 LOSS verdicts derived from the terminal-verified six-stone LOSS
  `00000000040004001004000004010000` (n11-s6-terminal-loss-20261015, cache-free
  C++/Python agreement on 1,028,621 states): indices 381840 / 402066 / 550881
  are three of the six canonical S5 parents, and audit_joint_plan.py shows they
  are exactly the parents required by selected S4 class 16397.  They are
  removed from the element-cost obligations, so the required union shrinks by
  three while every selection stays fixed.

The reflection is computed as a batch from one frozen input set; the staged
reflection accumulates (162106, 381840, 402066, 550881) in that order from the
same frozen instance and must reproduce the batch choices and union exactly.

Historical inputs remain unchanged.  Every kept and every re-selected response
and every complete S5 boundary is rebuilt from independent geometry plus the
explicit exact-S5 cache augmented only by the terminal-verified verdicts.  No
unknown verdict is asserted; the output is still an optimistic plan, not a
root proof.  K0423, the existing outputs, the first- through sixth-update
outputs and the history are never written to.
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
NIGHT1 = ROOT / "research/experiments/n11-night-batch1-20261014/output"
NIGHT2 = ROOT / "research/experiments/n11-night-batch2-20261014/output"
NIGHT3 = ROOT / "research/experiments/n11-night-batch3-20261014/output"
NIGHT4 = ROOT / "research/experiments/n11-night-batch4-20261014/output"
NIGHT5 = ROOT / "research/experiments/n11-night-batch5-20261014/output"
S6DIR = ROOT / "research/experiments/n11-s6-terminal-loss-20261015"
BASE = ROOT / "research/experiments/n11-night-plan-update6-20261014/output"
RANK = ROOT / "research/experiments/n11-conflict-ranking-20261013/output"

sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-s7-fifth-terminal-20261015"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache  # noqa: E402
from fifth_verify_standalone import canonical, points  # noqa: E402

NEW_WIN = (162106,)
S6_LOSS_INDICES = (381840, 402066, 550881)
S6_ROOT = int("00000000040004001004000004010000", 16)
S6_CERT_SHA = "cb2e73c277c6fd526689db64b1d8c07ebd1ca1bd8c2a966e0757d22c4471ebf6"
NEW_ORDER = NEW_WIN + S6_LOSS_INDICES
ROUNDTRIP = (126899, 144095, 121263, 145001, 137694, 143240, 220231, 126017,
             197665, 206386, 131631, 162106)

# Receipt files of the thirteen verdicts the sixth update already used.
PRIOR_RECEIPTS = {
    558600: (K0423, "pilot-558600-terminal-verification.json",
             "pilot-558600-terminal-dag.json.gz"),
    209644: (K0423, "pilot-209644-terminal-verification.json",
             "pilot-209644-terminal-dag.json.gz"),
    126899: (ADAPTIVE, "pilot-126899-receipt.json",
             "pilot-126899-terminal-dag.json.gz"),
    144095: (ADAPTIVE, "pilot-144095-receipt.json",
             "pilot-144095-terminal-dag.json.gz"),
    121263: (PROBE, "adaptive-121263-receipt.json",
             "adaptive-121263-terminal-dag.json.gz"),
    145001: (PROBE, "adaptive-145001-receipt.json",
             "adaptive-145001-terminal-dag.json.gz"),
    137694: (NIGHT1, "night-a-137694-receipt.json",
             "night-a-137694-terminal-dag.json.gz"),
    143240: (NIGHT1, "night-a-143240-receipt.json",
             "night-a-143240-terminal-dag.json.gz"),
    220231: (NIGHT1, "night-a-220231-receipt.json",
             "night-a-220231-terminal-dag.json.gz"),
    126017: (NIGHT1, "nightb10m-126017-receipt.json",
             "nightb10m-126017-terminal-dag.json.gz"),
    197665: (NIGHT2, "nighta25m-197665-receipt.json",
             "nighta25m-197665-terminal-dag.json.gz"),
    206386: (NIGHT3, "nighta25m-206386-receipt.json",
             "nighta25m-206386-terminal-dag.json.gz"),
    131631: (NIGHT4, "nighta25m-131631-receipt.json",
             "nighta25m-131631-terminal-dag.json.gz"),
}
NEW_RECEIPTS = {
    162106: (NIGHT5, "nighta25m-162106-receipt.json",
             "nighta25m-162106-terminal-dag.json.gz"),
}
EXPECTED = {558600: 2, 209644: 1, 126899: 2, 144095: 1, 121263: 2, 145001: 2,
            137694: 2, 143240: 2, 220231: 2, 126017: 1, 197665: 1, 206386: 1,
            131631: 1, 162106: 1, 381840: 2, 402066: 2, 550881: 2}
# Shared terminal-checker source: all seventeen independent candidate receipts
# (K0423 pilots, native focus, adaptive line and night batches 1-5) name this
# same file.  The six-stone certificate package uses its own cache-free pair.
CHECKER_SOURCE_SHA = "0f890cb49e806880bb56de2147163dc3fcfb0d5eae44835d602160c16008cd96"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def key(mask: int):
    return mask & ((1 << 64) - 1), mask >> 64


def digests(payload) -> str:
    return hashlib.sha256(json.dumps(payload, sort_keys=True,
                                     separators=(",", ":")).encode()).hexdigest()


def load_receipt(receipt_path: Path, cert_path: Path, mask: int, index: int,
                 sources: dict, checker_shas: dict) -> int:
    receipt = json.loads(receipt_path.read_text())
    assert receipt["s5_index"] == index, receipt_path
    assert receipt["trusted_leaves"] == 0, receipt_path
    assert receipt["verdict"] in (1, 2), receipt_path
    assert sha(cert_path) == receipt["certificate_sha256"], receipt_path
    assert str(mask) == str(receipt["root_mask"]), receipt_path
    if index in ROUNDTRIP:
        assert receipt["pruned_roundtrip_verified"], index
    if "checker_source_sha256" in receipt:
        if "checker_source_path" in receipt:
            assert sha(ROOT / receipt["checker_source_path"]) == \
                receipt["checker_source_sha256"], receipt_path
        checker_shas[index] = receipt["checker_source_sha256"]
    sources.update({str(p.relative_to(ROOT)): sha(p) for p in (receipt_path, cert_path)})
    return receipt["verdict"]


def main() -> None:
    with gzip.open(OLD / "dependency-graph.json.gz", "rt") as stream:
        g = json.load(stream)
    baseline_path = BASE / "repaired-joint-plan-update6.json"
    baseline = json.loads(baseline_path.read_text())
    assert baseline["verification"]["passed"]
    assert baseline["union_size"] == 31774, baseline["union_size"]
    old_entries = {(e["first"], e["reply"], e["third"]): e for e in baseline["groups"]}
    baseline_choices = {ident: e["s4_class_index"] for ident, e in old_entries.items()}
    baseline_required = set(baseline["required_new_s5"])

    sources = {
        str((OLD / "dependency-graph.json.gz").relative_to(ROOT)):
            sha(OLD / "dependency-graph.json.gz"),
        str(baseline_path.relative_to(ROOT)): sha(baseline_path),
    }
    verdicts: dict[int, int] = {}
    checker_shas: dict[int, str] = {}
    for index, (directory, receipt_name, cert_name) in PRIOR_RECEIPTS.items():
        mask = g["s5_masks"][index][0] | g["s5_masks"][index][1] << 64
        verdicts[index] = load_receipt(directory / receipt_name, directory / cert_name,
                                       mask, index, sources, checker_shas)
    assert {str(k): v for k, v in verdicts.items()} == baseline["resolved_s5_verdicts"]
    receipt_facts = {}
    for index, (directory, receipt_name, cert_name) in NEW_RECEIPTS.items():
        mask = g["s5_masks"][index][0] | g["s5_masks"][index][1] << 64
        verdicts[index] = load_receipt(directory / receipt_name, directory / cert_name,
                                       mask, index, sources, checker_shas)
        receipt = json.loads((directory / receipt_name).read_text())
        assert sha(ROOT / receipt["probe_manifest"]) == receipt["probe_manifest_sha256"]
        # The night-batch5 Python cross-check must agree with the receipt.
        comparison_path = directory / f"{Path(receipt_name).stem.replace('-receipt', '')}-python-comparison.json"
        comparison = json.loads(comparison_path.read_text())
        assert comparison["s5_index"] == index, comparison_path
        assert comparison["fresh_python_verification"] == {
            "verdict": receipt["verdict"],
            "trusted_leaves": receipt["trusted_leaves"],
            "nodes": receipt["nodes"],
            "edges": receipt["edges"],
            "terminal_nodes": receipt["terminal_nodes"],
        }, comparison_path
        sources[str(comparison_path.relative_to(ROOT))] = sha(comparison_path)
        receipt_facts[str(index)] = dict(
            verdict=receipt["verdict"], trusted_leaves=receipt["trusted_leaves"],
            pruned_roundtrip_verified=receipt["pruned_roundtrip_verified"],
            evidence_class=receipt["evidence_class"],
            certificate_sha256=receipt["certificate_sha256"],
            certificate_bytes=receipt["certificate_bytes"],
            probe_search_nodes=receipt["probe_search_nodes"],
            probe_budget=receipt["probe_budget"],
            checker_source_sha256=receipt["checker_source_sha256"],
            python_cross_check=str(comparison_path.relative_to(ROOT)),
            receipt=str((directory / receipt_name).relative_to(ROOT)),
            certificate=str((directory / cert_name).relative_to(ROOT)),
        )

    # S6-derived S5 LOSS verdicts: parent masks are rebuilt from the frozen
    # six-stone root; only the three parents the sixth-update plan requires may
    # enter the verdict set.
    s6_cert = S6DIR / "s6-loss-optimized.cert"
    assert sha(s6_cert) == S6_CERT_SHA
    parents = {canonical(S6_ROOT ^ (1 << p)) for p in points(S6_ROOT)}
    assert len(parents) == 6
    assert S6_ROOT.bit_count() == 6 and canonical(S6_ROOT) == S6_ROOT
    s6_loss: dict[int, int] = {}
    for idx in S6_LOSS_INDICES:
        mask = g["s5_masks"][idx][0] | g["s5_masks"][idx][1] << 64
        assert mask in parents, (idx, "not an S6 parent")
        s6_loss[idx] = mask
    assert len(set(s6_loss.values())) == 3
    baseline_resolved_masks = {g["s5_masks"][int(k)][0] | g["s5_masks"][int(k)][1] << 64
                               for k in baseline["resolved_s5_verdicts"]}
    assert not (parents & baseline_resolved_masks), "S6 parent already resolved"
    baseline_required_masks = {g["s5_masks"][i][0] | g["s5_masks"][i][1] << 64
                               for i in baseline_required}
    assert set(s6_loss.values()) <= baseline_required_masks, \
        "S6 parents are not required by the frozen plan"
    assert (parents & baseline_required_masks) == set(s6_loss.values()), \
        "plan-relevant S6 parents changed; re-audit before proceeding"
    for idx in S6_LOSS_INDICES:
        verdicts[idx] = 2
    sources[str(s6_cert.relative_to(ROOT))] = sha(s6_cert)
    for extra in ("audit_joint_plan.py", "verify_s6_terminal.py"):
        extra_path = S6DIR / extra
        sources[str(extra_path.relative_to(ROOT))] = sha(extra_path)

    assert verdicts == EXPECTED, verdicts
    # Every receipt that names the terminal checker must name the same source.
    assert len(set(checker_shas.values())) == 1, checker_shas
    shared_checker_sha = next(iter(checker_shas.values()))
    assert shared_checker_sha == CHECKER_SOURCE_SHA, checker_shas

    losses = {i for i, v in verdicts.items() if v == 2}
    wins = {i for i, v in verdicts.items() if v == 1}
    assert set(NEW_WIN) <= wins
    baseline_losses = {int(k) for k, v in baseline["resolved_s5_verdicts"].items()
                       if v == 2}
    baseline_wins = {int(k) for k, v in baseline["resolved_s5_verdicts"].items()
                     if v == 1}
    assert losses == baseline_losses | set(S6_LOSS_INDICES), \
        "LOSS set drifted beyond the S6-derived three"
    assert wins == baseline_wins | set(NEW_WIN), "WIN set drifted"

    def instance(resolved: dict[int, int]):
        """Element-cost obligations and legal candidate sets for a verdict set."""
        known_losses = {i for i, v in resolved.items() if v == 2}
        known_wins = {i for i, v in resolved.items() if v == 1}
        cost = [set(c) - known_losses for c in g["s4_cost"]]
        excluded = {s for s, c in enumerate(g["s4_cost"]) if known_wins.intersection(c)}
        options = {}
        for root in g["roots"]:
            if root["role"] == "known-loss-baseline":
                continue
            for r in root["thirds"]:
                ident = (root["origin_first"], root["origin_reply"], r["third"])
                opts = [s for s in r["options"] if s not in excluded]
                assert opts, f"no optimistic response for {ident}"
                options[ident] = opts
        return cost, excluded, options

    cost, excluded, options = instance(verdicts)
    baseline_excluded = set(baseline["excluded_s4_classes"])
    assert baseline_excluded <= excluded, "WIN set shrank; exclusion set drifted"
    new_excluded = sorted(excluded - baseline_excluded)
    assert set(old_entries) == set(options), "baseline third coverage drift"
    pairs = {}
    for root in g["roots"]:
        if root["role"] == "known-loss-baseline":
            continue
        pairs[(root["origin_first"], root["origin_reply"])] = \
            root["pair_mask"][0] | root["pair_mask"][1] << 64
    assert len(pairs) == 19

    def select(seed: dict[tuple, int], cost, excluded, options):
        """Keep every still-legal seed response, greedy-fill the rest."""
        choices = {ident: s for ident, s in seed.items() if s not in excluded}
        union = set().union(*(cost[s] for s in choices.values())) if choices else set()
        changed = []
        for ident in sorted(options):
            if ident in choices:
                continue
            before = len(union)
            s = min(options[ident], key=lambda t: (len(cost[t] - union),
                                                   len(cost[t]), t))
            choices[ident] = s
            union |= cost[s]
            changed.append(dict(first=ident[0], reply=ident[1], third=ident[2],
                                old_s4=seed.get(ident), new_s4=s,
                                old_s4_was_excluded=seed.get(ident) in excluded,
                                marginal_new_elements=len(union) - before,
                                added_vs_baseline_union=len(cost[s] - baseline_required)))
        assert len(choices) == len(options)
        return choices, union, changed

    board = Board(11)
    cache = load_exact_s5_cache(board)
    for i, v in verdicts.items():
        cache[tuple(g["s5_masks"][i])] = {"verdict": v}

    def verify(choices: dict[tuple, int], union: set[int], cost):
        """Rebuild every selected fourth and every complete boundary from geometry."""
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
        assert len(entries) == 2261
        assert len(pairs) == 19
        return entries, dict(passed=True, checked_selected_s4=len(checked),
                             complete_third_boundaries=len(pairs),
                             complete_s5_boundaries=len(checked),
                             third_moves_checked=len(entries),
                             known_win_selected=0, known_loss_in_union=0)

    def signature(resolved, chosen, union, cost, excluded, options):
        in_play = sorted({s for opts in options.values() for s in opts})
        return dict(
            resolved_verdicts=sorted(resolved.items()),
            labels_sha=digests(sorted(resolved.items())),
            candidates_sha=digests(dict(excluded=sorted(excluded),
                                        options=[[list(k), v] for k, v in sorted(options.items())])),
            obligations_sha=digests(dict(excluded=sorted(excluded),
                                         verdicts=sorted(resolved.items()),
                                         options=[[list(k), v] for k, v in sorted(options.items())],
                                         cost={str(s): sorted(cost[s]) for s in in_play})),
            choices_sha=digests([[list(k), v] for k, v in sorted(chosen.items())]),
            union_sha=digests(sorted(union)), union_size=len(union),
            free_thirds=sum(not cost[s] for s in chosen.values()),
            changed_choice_count=sum(1 for k, s in chosen.items()
                                     if baseline_choices[k] != s),
            known_wins_in_union=sorted(set().union(*(cost[s] for s in chosen.values()))
                                       & {i for i, v in resolved.items() if v == 1}),
            known_losses_in_union=sorted(set().union(*(cost[s] for s in chosen.values()))
                                         & {i for i, v in resolved.items() if v == 2}),
        )

    # Batch reflection: the 162106 WIN plus the three S6-derived LOSS verdicts
    # on the sixth-update baseline.
    batch_choices, batch_union, batch_changed = select(baseline_choices, cost, excluded, options)
    assert not wins.intersection(batch_union) and not losses.intersection(batch_union)
    batch_entries, batch_verification = verify(batch_choices, batch_union, cost)

    # Staged reflection: accumulate the new verdicts in NEW_ORDER order.
    resolved: dict[int, int] = {k: v for k, v in verdicts.items() if k not in NEW_ORDER}
    seed = dict(baseline_choices)
    stages = []
    for index in NEW_ORDER:
        resolved[index] = verdicts[index]
        stage_cost, stage_excluded, stage_options = instance(resolved)
        seed, union, changed = select(seed, stage_cost, stage_excluded, stage_options)
        stages.append((dict(resolved), seed, union, changed))
    resolved, seed, union, changed = stages[-1]
    runs = {"batch": signature(verdicts, batch_choices, batch_union,
                               cost, excluded, options),
            "staged_forward": signature(resolved, seed, union,
                                        cost, excluded, options)}
    assert runs["batch"]["labels_sha"] == runs["staged_forward"]["labels_sha"]
    assert runs["batch"]["candidates_sha"] == runs["staged_forward"]["candidates_sha"]
    assert runs["batch"]["obligations_sha"] == runs["staged_forward"]["obligations_sha"]
    assert runs["batch"]["choices_sha"] == runs["staged_forward"]["choices_sha"]
    assert union == batch_union, "staged and batch reflections disagree on the union"

    # Cross-check against the frozen conflict-ranking row (ranking.tsv + .json).
    ranking = json.loads((RANK / "ranking.json").read_text())
    rank_rows = {row["s5_index"]: row for row in ranking["rows"]}
    tsv_lines = (RANK / "ranking.tsv").read_text().splitlines()
    tsv_header = tsv_lines[0].split("\t")
    tsv_rows = [dict(zip(tsv_header, line.split("\t"))) for line in tsv_lines[1:]]
    tsv_by_index = {int(row["s5_index"]): row for row in tsv_rows}
    cross_check = {}
    for index in NEW_WIN:
        row = rank_rows[index]
        affected_choices = sorted(k for k, s in baseline_choices.items()
                                  if index in g["s4_cost"][s])
        affected_s4 = sorted({baseline_choices[k] for k in affected_choices})
        all_invalidated = sorted(s for s, c in enumerate(g["s4_cost"])
                                 if index in c)
        rank_plan = row["loss_plan"]
        rank_cover = row["fixed_win_cover"]
        tsv_row = tsv_by_index[index]
        this_baseline = {
            "affected_choices": len(affected_choices),
            "affected_s4": affected_s4,
            "invalidated_options_total": len(all_invalidated),
            "newly_excluded_options": len(set(all_invalidated) - baseline_excluded),
        }
        ranking_ref = {
            "affected_choices": len(rank_plan["if_win_affected_choices"]),
            "affected_s4": rank_plan["if_win_invalidated_selected_s4"],
            "invalidated_options": len(rank_plan["if_win_invalidated_s4_options"]),
            "invalidated_s4_options": rank_plan["if_win_invalidated_s4_options"],
            "greedy_delta": rank_plan["if_win_greedy_delta"],
            "greedy_union": rank_plan["if_win_greedy_repaired_union_size"],
            "new_free_win_branches": len(rank_cover["if_win_newly_free_branches"]),
            "loss_uncovered_branches": len(rank_cover["if_loss_uncovered_branches"]),
        }
        tsv_ref = {
            "geometry_rank": int(tsv_row["geometry_rank"]),
            "if_win_loss_choices_invalidated": int(tsv_row["if_win_loss_choices_invalidated"]),
            "if_loss_fixed_win_branches_uncovered": int(tsv_row["if_loss_fixed_win_branches_uncovered"]),
            "if_win_new_free_win_branches": int(tsv_row["if_win_new_free_win_branches"]),
            "if_win_greedy_loss_union": int(tsv_row["if_win_greedy_loss_union"]),
            "if_win_greedy_delta": int(tsv_row["if_win_greedy_delta"]),
        }
        # ranking.tsv and ranking.json must describe the same counterfactual.
        assert tsv_ref["if_win_loss_choices_invalidated"] == ranking_ref["affected_choices"]
        assert tsv_ref["if_win_new_free_win_branches"] == ranking_ref["new_free_win_branches"]
        assert tsv_ref["if_win_greedy_delta"] == ranking_ref["greedy_delta"]
        assert tsv_ref["if_win_greedy_loss_union"] == ranking_ref["greedy_union"]
        assert tsv_ref["if_loss_fixed_win_branches_uncovered"] == \
            ranking_ref["loss_uncovered_branches"]
        cross_check[str(index)] = dict(
            verdict=verdicts[index],
            ranking_tsv_row=tsv_ref,
            ranking_on_k0423_baseline=ranking_ref,
            this_baseline=this_baseline,
            absorbed_by_baseline_updates=(
                "the ranking counterfactual (geometry_rank 25) invalidates the "
                "K0423-baseline selections on S4 class 5830 (3 responses: "
                "49/60/59, 49/60/61, 49/60/71) and removes the four options "
                "4327 / 4328 / 5056 / 5830; the third update already excluded "
                "5830 for 126017 WIN and re-selected those responses, so no "
                "selected response sits on any of the four invalidated options "
                "on the sixth-update baseline.  The three options 4327 / 4328 / "
                "5056 are excluded in this round, the greedy repair has no work "
                "to do (changed_choice_count 0) and the ranking's +49 remains "
                "the K0423-basis counterfactual"))
        assert this_baseline["invalidated_options_total"] == \
            ranking_ref["invalidated_options"], index
        assert sorted(all_invalidated) == sorted(
            rank_plan["if_win_invalidated_s4_options"]), index
        assert set(new_excluded) <= set(all_invalidated), index
        if this_baseline["affected_s4"] != ranking_ref["affected_s4"]:
            # The K0423-baseline selections on the ranking's affected class
            # were already invalidated and re-selected by the third update
            # (5830 is shared by 126017 / 197665 / 206386 / 131631 / 162106);
            # on this baseline the affected count is zero and the greedy repair
            # is vacuous.
            assert set(ranking_ref["affected_s4"]) <= baseline_excluded, index
            assert this_baseline["affected_choices"] == 0, index
        # Every option the ranking says must disappear did disappear here.
        assert set(ranking_ref["invalidated_s4_options"]) - set(new_excluded) \
            <= baseline_excluded, index

    for i in NEW_WIN:
        assert i not in batch_union, f"{i} still required"
    for i in S6_LOSS_INDICES:
        assert i not in batch_union, f"{i} still required"

    out = dict(
        schema="n11-night-repaired-joint-plan-update7-v1",
        baseline_plan_sha256=sha(baseline_path),
        baseline_schema=baseline["schema"],
        source_sha256=sources,
        baseline_union_size=baseline["union_size"], union_size=len(batch_union),
        union_delta_vs_baseline=len(batch_union) - baseline["union_size"],
        roots=len(pairs), third_moves_covered=len(batch_entries),
        baseline_free_thirds=baseline["free_thirds"],
        free_thirds=sum(e["unknown_s5_children"] == 0 for e in batch_entries),
        baseline_excluded_s4_classes=sorted(baseline_excluded),
        excluded_s4_classes=sorted(excluded),
        new_excluded_s4_classes=new_excluded,
        baseline_resolved_s5_verdicts=baseline["resolved_s5_verdicts"],
        resolved_s5_verdicts={str(k): v for k, v in sorted(verdicts.items())},
        known_loss_removed_from_cost=sorted(S6_LOSS_INDICES),
        s6_derived_losses={
            str(idx): {"mask": f"{mask:032x}", "certificate": str(s6_cert.relative_to(ROOT)),
                       "certificate_sha256": S6_CERT_SHA,
                       "audit": str((S6DIR / "audit_joint_plan.py").relative_to(ROOT))}
            for idx, mask in sorted(s6_loss.items())},
        changed_choice_count=len(batch_changed), changed_choices=batch_changed,
        groups=batch_entries, required_new_s5=sorted(batch_union),
        verification=batch_verification,
        new_receipts=receipt_facts,
        batch_vs_staged={
            "runs": runs,
            "resolved_verdicts": {str(k): v for k, v in sorted(verdicts.items())},
            "labels_equal": True, "candidates_equal": True,
            "obligations_equal": True,
            "choices_identical": {"staged_forward": True},
            "union_sizes": {name: runs[name]["union_size"] for name in runs},
            "upper_bound_differences": {},
            "verification": {"batch": batch_verification},
            "rule": ("identical resolved labels, identical legal candidate sets and "
                     "identical element-cost obligations are required; only the greedy "
                     "upper bound may differ.  This round carries one WIN and three "
                     "LOSS verdicts, staged in NEW_ORDER order (162106, 381840, "
                     "402066, 550881) from the same frozen instance and asserted to "
                     "reproduce the batch reflection exactly."),
        },
        ranking_cross_check=cross_check,
        shared_checker_source_sha256=shared_checker_sha,
        trust=("optimistic plan only: old exact-S5 leaves remain solver-trusted; fourteen "
               "candidate receipts (558600 LOSS, 209644 WIN, 126899 LOSS, 144095 WIN, "
               "121263 LOSS, 145001 LOSS, 137694 LOSS, 143240 LOSS, 220231 LOSS, "
               "126017 WIN, 197665 WIN, 206386 WIN, 131631 WIN, 162106 WIN) "
               "terminal-verified with trusted leaves 0; three S5 LOSS verdicts "
               "(381840 / 402066 / 550881) derived from one cache-free six-stone "
               "terminal certificate (1,028,621 states, independent C++/Python "
               "agreement); all remaining required S5 verdicts UNKNOWN; not a root "
               "proof"),
    )
    target = EXP / "output/repaired-joint-plan-update7.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(out, sort_keys=True, indent=2) + "\n")
    print(json.dumps({k: v for k, v in out.items()
                      if k not in ("groups", "required_new_s5", "source_sha256",
                                   "changed_choices", "batch_vs_staged",
                                   "ranking_cross_check", "new_receipts",
                                   "s6_derived_losses")}, indent=2))
    print(json.dumps(runs, indent=2))
    print(json.dumps(cross_check, indent=2))


if __name__ == "__main__":
    main()
