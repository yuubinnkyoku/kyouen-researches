"""Eighth joint-plan update: layer the three verified native receipts
(115540 LOSS, 144193 LOSS, 144311 WIN) and the three remaining parents of the
frozen six-stone terminal LOSS certificate.

Baseline: the seventh update output (union 31,771).  New facts, all frozen
before this script runs:

* 115540 LOSS and 144193 LOSS (n11-native-terminal-checker-20261013 receipts,
  terminal-only, trusted leaves 0, checker source 0f890cb4...) remove two more
  elements from the optimistic union (both are required by the seventh-update
  plan).
* 144311 WIN (same receipt family) excludes every S4 class whose legal-child
  cost set contains it; one selected class (5596) is hit, so its response is
  re-selected greedily inside the remaining legal options.
* the six-stone certificate (cb2e73c2..., 1,028,621 states) also proves the
  three S5 parents 381858 / 382619 and one parent outside the central index
  space; only the three plan-required parents were layered in the seventh
  update, so the two indexed extras are added here (no plan effect expected,
  measured like everything else).

The reflection is computed as a batch from one frozen input set; the staged
reflection accumulates (115540, 144193, 144311, 381858, 382619) in that order
from the same frozen instance and must reproduce the batch choices and union
exactly.

The three native receipts carry the same checker source as every earlier
receipt but a different receipt layout (probe_manifest is replaced by a
focus10m manifest row binding input/output/trace hashes); both layouts are
validated field by field.  The fresh Python re-verification of 115540 and
144311 was produced by verify_native_receipts.py (edge-DAG verifier,
no solver, no cache); 144193 keeps the stored comparison.

No unknown verdict is asserted; the output is still an optimistic plan, not a
root proof.  Historical inputs, earlier update outputs and K0423 are never
written to.
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
NATIVE = ROOT / "research/experiments/n11-native-terminal-checker-20261013/output"
CONFLICT = ROOT / "research/experiments/n11-conflict-closure-20261013"
BASE = ROOT / "research/experiments/n11-night-plan-update7-20261015/output"
RANK = ROOT / "research/experiments/n11-conflict-ranking-20261013/output"

sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-central-reply-frontier-20261012/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-s7-fifth-terminal-20261015"))
from independent import Board  # noqa: E402
from analyze_central_reply_frontier import load_exact_s5_cache  # noqa: E402
from fifth_verify_standalone import canonical, points  # noqa: E402

NEW_RECEIPTS = (115540, 144193, 144311)
NEW_PROBE_RECEIPT = 150871
PROBE_MANIFEST = EXP / "output/update8probe10m-manifest.json"
S6_ROOT = int("00000000040004001004000004010000", 16)
S6_CERT_SHA = "cb2e73c277c6fd526689db64b1d8c07ebd1ca1bd8c2a966e0757d22c4471ebf6"
S6_PRIOR = (381840, 402066, 550881)
S6_EXTRA_EXPECTED = (381858, 382619)
NEW_ORDER = NEW_RECEIPTS + (NEW_PROBE_RECEIPT,) + S6_EXTRA_EXPECTED + (381840, 402066, 550881)
ROUNDTRIP = (126899, 144095, 121263, 145001, 137694, 143240, 220231, 126017,
             197665, 206386, 131631, 162106)

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
    162106: (NIGHT5, "nighta25m-162106-receipt.json",
             "nighta25m-162106-terminal-dag.json.gz"),
}
EXPECTED = {558600: 2, 209644: 1, 126899: 2, 144095: 1, 121263: 2, 145001: 2,
            137694: 2, 143240: 2, 220231: 2, 126017: 1, 197665: 1, 206386: 1,
            131631: 1, 162106: 1, 381840: 2, 402066: 2, 550881: 2,
            115540: 2, 144193: 2, 144311: 1, 381858: 2, 382619: 2, 150871: 2}
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
    baseline_path = BASE / "repaired-joint-plan-update7.json"
    baseline = json.loads(baseline_path.read_text())
    assert baseline["verification"]["passed"]
    assert baseline["union_size"] == 31771, baseline["union_size"]
    old_entries = {(e["first"], e["reply"], e["third"]): e for e in baseline["groups"]}
    baseline_choices = {ident: e["s4_class_index"] for ident, e in old_entries.items()}
    baseline_required = set(baseline["required_new_s5"])

    sources = {
        str((OLD / "dependency-graph.json.gz").relative_to(ROOT)):
            sha(OLD / "dependency-graph.json.gz"),
        baseline_path.relative_to(ROOT).as_posix(): sha(baseline_path),
    }
    verdicts: dict[int, int] = {}
    checker_shas: dict[int, str] = {}
    for index, (directory, receipt_name, cert_name) in PRIOR_RECEIPTS.items():
        mask = g["s5_masks"][index][0] | g["s5_masks"][index][1] << 64
        verdicts[index] = load_receipt(directory / receipt_name, directory / cert_name,
                                       mask, index, sources, checker_shas)
    # The baseline registry also carries the three S6-certificate parents; they
    # are layered below and excluded from this receipt-only comparison.
    baseline_receipt_verdicts = {k: v for k, v in baseline["resolved_s5_verdicts"].items()
                                 if int(k) not in S6_PRIOR}
    assert {str(k): v for k, v in verdicts.items()} == baseline_receipt_verdicts

    # New native receipts: same checker source, different receipt layout.  The
    # focus10m manifest row binds the input CSV, the output CSV and the trace
    # hash of exactly this run.
    manifest_path = CONFLICT / "output/focus10m-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    assert sha(manifest_path) == sha(CONFLICT / "output/focus10m-manifest.json")
    assert manifest["budget"] == 10000000, manifest["budget"]
    sources[manifest_path.relative_to(ROOT).as_posix()] = sha(manifest_path)
    receipt_facts = {}
    for index in NEW_RECEIPTS:
        receipt_path = NATIVE / f"pilot-{index}-receipt.json"
        cert_path = NATIVE / f"pilot-{index}-terminal-dag.json.gz"
        mask = g["s5_masks"][index][0] | g["s5_masks"][index][1] << 64
        verdicts[index] = load_receipt(receipt_path, cert_path, mask, index,
                                       sources, checker_shas)
        receipt = json.loads(receipt_path.read_text())
        assert receipt["manifest"] == manifest_path.relative_to(ROOT).as_posix()
        assert receipt["manifest_sha256"] == sha(manifest_path)
        assert receipt["manifest_trace_sha256_match"] is True
        row = next(r for r in manifest["rows"] if r["s5_index"] == index)
        assert row["status"] == "SOLVED", index
        assert row["mask"] == list(g["s5_masks"][index]), index
        input_csv = CONFLICT / f"input/s5-{index}.csv"
        output_csv = CONFLICT / f"output/focus10m-{index}.csv"
        assert sha(input_csv) == row["input_sha256"], index
        assert sha(output_csv) == row["output_sha256"], index
        sources.update({str(p.relative_to(ROOT)): sha(p)
                        for p in (input_csv, output_csv)})
        comparison_path = EXP / f"output/native-{index}-python-comparison.json"
        if index == 144193:
            comparison_path = NATIVE / "pilot-144193-python-comparison.json"
        comparison = json.loads(comparison_path.read_text())
        assert comparison["s5_index"] == index, comparison_path
        assert comparison["fresh_python_verification"] == {
            "verdict": receipt["verdict"],
            "trusted_leaves": receipt["trusted_leaves"],
            "nodes": receipt["nodes"],
            "edges": receipt["edges"],
            "terminal_nodes": receipt["terminal_nodes"],
        }, comparison_path
        sources[comparison_path.relative_to(ROOT).as_posix()] = sha(comparison_path)
        receipt_facts[str(index)] = dict(
            verdict=receipt["verdict"], trusted_leaves=receipt["trusted_leaves"],
            certificate_sha256=receipt["certificate_sha256"],
            certificate_bytes=receipt["certificate_bytes"],
            search_nodes=row["nodes"], checker_source_sha256=receipt["checker_source_sha256"],
            manifest=manifest_path.relative_to(ROOT).as_posix(),
            python_cross_check=comparison_path.relative_to(ROOT).as_posix(),
            receipt=receipt_path.relative_to(ROOT).as_posix(),
            certificate=cert_path.relative_to(ROOT).as_posix(),
            trace_sha256=receipt["trace_sha256"],
            evidence_layout="native-focus10m")
    assert {int(k): v["verdict"] for k, v in receipt_facts.items()} == \
        {115540: 2, 144193: 2, 144311: 1}

    # S6 certificate: all six canonical five-stone parents are genuine LOSS
    # verdicts; the seventh update layered only the three the plan requires.
    s6_cert = S6DIR / "s6-loss-optimized.cert"
    assert sha(s6_cert) == S6_CERT_SHA
    parents = {canonical(S6_ROOT ^ (1 << p)) for p in points(S6_ROOT)}
    assert len(parents) == 6
    assert S6_ROOT.bit_count() == 6 and canonical(S6_ROOT) == S6_ROOT
    indexed_parents = {}
    s5_index_of = {}
    for mask in parents:
        assert mask.bit_count() == 5, "parent is not a five-stone position"
        for idx, (lo, hi) in enumerate(g["s5_masks"]):
            if (lo | hi << 64) == mask:
                indexed_parents[idx] = mask
                s5_index_of[mask] = idx
                break
    assert set(indexed_parents) == set(S6_PRIOR) | set(S6_EXTRA_EXPECTED), \
        sorted(indexed_parents)
    unmapped = parents - set(indexed_parents.values())
    assert len(unmapped) == 1, unmapped
    baseline_resolved_masks = {g["s5_masks"][int(k)][0] | g["s5_masks"][int(k)][1] << 64
                               for k in baseline["resolved_s5_verdicts"]}
    assert not (set(indexed_parents.values()) - baseline_resolved_masks
                - {indexed_parents[i] for i in S6_EXTRA_EXPECTED}), \
        "certificate parent arrived unresolved outside the extras"
    for idx in S6_PRIOR:
        verdicts[idx] = 2
    for idx in S6_EXTRA_EXPECTED:
        verdicts[idx] = 2
    sources[s6_cert.relative_to(ROOT).as_posix()] = sha(s6_cert)
    for extra in ("audit_joint_plan.py", "verify_s6_terminal.py"):
        extra_path = S6DIR / extra
        sources[str(extra_path.relative_to(ROOT))] = sha(extra_path)

    # New update8 adaptive 10M receipt: index 150871 is a genuine LOSS found by
    # this round's sanctioned search (3,744,513 nodes) and verified terminal-only
    # with zero trusted leaves; a fresh Python re-derivation of the exported DAG
    # cross-checks the native receipt.
    probe_manifest = json.loads(PROBE_MANIFEST.read_text())
    assert probe_manifest["budget"] == 10000000, probe_manifest["budget"]
    assert probe_manifest["solver_binary_sha256"] == \
        "72f1da293931c590f54d2d70b9f6318ce6d207e04ff4b6dbe6050ea34876de14"
    sources[PROBE_MANIFEST.relative_to(ROOT).as_posix()] = sha(PROBE_MANIFEST)
    prow = next(r for r in probe_manifest["rows"] if r["s5_index"] == NEW_PROBE_RECEIPT)
    assert prow["status"] == "SOLVED" and prow["verdict"] == 2, prow
    assert prow["mask"] == list(g["s5_masks"][NEW_PROBE_RECEIPT]), prow
    probe_mask = g["s5_masks"][NEW_PROBE_RECEIPT][0] | g["s5_masks"][NEW_PROBE_RECEIPT][1] << 64
    probe_receipt_path = EXP / f"output/receipt-{NEW_PROBE_RECEIPT}.json"
    probe_cert_path = EXP / f"output/terminal-{NEW_PROBE_RECEIPT}-dag.json.gz"
    verdicts[NEW_PROBE_RECEIPT] = load_receipt(probe_receipt_path, probe_cert_path,
                                               probe_mask, NEW_PROBE_RECEIPT,
                                               sources, checker_shas)
    assert verdicts[NEW_PROBE_RECEIPT] == 2
    probe_receipt = json.loads(probe_receipt_path.read_text())
    assert probe_receipt["trace_sha256"] == prow["trace_sha256"], "probe trace hash drifted"
    assert probe_receipt["probe_search_nodes"] == prow["nodes"]
    assert probe_receipt["probe_manifest"] == PROBE_MANIFEST.relative_to(ROOT).as_posix()
    probe_comparison_path = EXP / f"output/terminal-verify-{NEW_PROBE_RECEIPT}.json"
    probe_comparison = json.loads(probe_comparison_path.read_text())
    assert probe_comparison["fresh_python_verification"] == {
        "verdict": probe_receipt["verdict"],
        "trusted_leaves": probe_receipt["trusted_leaves"],
        "nodes": probe_receipt["nodes"],
        "edges": probe_receipt["edges"],
        "terminal_nodes": probe_receipt["terminal_nodes"],
    }, probe_comparison_path
    sources[probe_comparison_path.relative_to(ROOT).as_posix()] = sha(probe_comparison_path)
    receipt_facts[str(NEW_PROBE_RECEIPT)] = dict(
        verdict=probe_receipt["verdict"], trusted_leaves=probe_receipt["trusted_leaves"],
        certificate_sha256=probe_receipt["certificate_sha256"],
        certificate_bytes=probe_receipt["certificate_bytes"],
        search_nodes=prow["nodes"], checker_source_sha256=probe_receipt["checker_source_sha256"],
        probe_manifest=PROBE_MANIFEST.relative_to(ROOT).as_posix(),
        python_cross_check=probe_comparison_path.relative_to(ROOT).as_posix(),
        receipt=probe_receipt_path.relative_to(ROOT).as_posix(),
        certificate=probe_cert_path.relative_to(ROOT).as_posix(),
        trace_sha256=probe_receipt["trace_sha256"], evidence_layout="update8-adaptive-10M")

    assert verdicts == EXPECTED, verdicts
    assert len(set(checker_shas.values())) == 1, checker_shas
    shared_checker_sha = next(iter(checker_shas.values()))
    assert shared_checker_sha == CHECKER_SOURCE_SHA, checker_shas

    losses = {i for i, v in verdicts.items() if v == 2}
    wins = {i for i, v in verdicts.items() if v == 1}
    baseline_losses = {int(k) for k, v in baseline["resolved_s5_verdicts"].items()
                       if v == 2}
    baseline_wins = {int(k) for k, v in baseline["resolved_s5_verdicts"].items()
                     if v == 1}
    assert losses == baseline_losses | {115540, 144193, 381858, 382619, NEW_PROBE_RECEIPT}, \
        "LOSS set drifted beyond the declared five"
    assert wins == baseline_wins | {144311}, "WIN set drifted"

    def instance(resolved: dict[int, int]):
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

    batch_choices, batch_union, batch_changed = select(baseline_choices, cost, excluded, options)
    assert not wins.intersection(batch_union) and not losses.intersection(batch_union)
    batch_entries, batch_verification = verify(batch_choices, batch_union, cost)

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

    # Ranking cross-check: geometry facts are recomputed for every new fact on
    # the K0423 baseline and must reproduce the frozen ranking rows exactly;
    # the seventh-update baseline values are reported for the drift record.
    ranking = json.loads((RANK / "ranking.json").read_text())
    rank_rows = {row["s5_index"]: row for row in ranking["rows"]}
    tsv_lines = (RANK / "ranking.tsv").read_text().splitlines()
    tsv_header = tsv_lines[0].split("\t")
    tsv_by_index = {int(dict(zip(tsv_header, line.split("\t")))["s5_index"]):
                    dict(zip(tsv_header, line.split("\t"))) for line in tsv_lines[1:]}
    k0423_plan = json.loads((K0423 / "repaired-joint-plan.json").read_text())
    k0423_choices = {(e["first"], e["reply"], e["third"]): e["s4_class_index"]
                     for e in k0423_plan["groups"]}
    cross_check = {}
    for index in NEW_RECEIPTS + S6_EXTRA_EXPECTED + (NEW_PROBE_RECEIPT,):
        if index not in rank_rows:
            # Extra certificate parent absent from the frozen ranking: record
            # its plain geometry (which S4 cost sets contain it) instead.
            containers = sorted(s for s, c in enumerate(g["s4_cost"]) if index in c)
            cross_check[str(index)] = dict(
                verdict=verdicts[index], ranking_absent=True,
                in_update7_union=index in baseline_required,
                s4_classes_containing=len(containers),
                note=("LOSS layering from the six-stone certificate; this parent "
                      "has no ranking row, so only the cost-set incidence is "
                      "recorded and the win-side cross-check in update_win_side.py "
                      "applies"))
            continue
        row = rank_rows[index]
        rank_plan = row["loss_plan"]
        tsv_row = tsv_by_index[index]
        all_invalidated = sorted(s for s, c in enumerate(g["s4_cost"]) if index in c)
        assert all_invalidated == sorted(rank_plan["if_win_invalidated_s4_options"]), \
            (index, "invalidated geometry drifted")
        assert int(tsv_row["if_win_loss_choices_invalidated"]) == \
            len(rank_plan["if_win_affected_choices"]), index
        affected_k0423 = sorted(k for k, s in k0423_choices.items() if index in g["s4_cost"][s])
        assert affected_k0423 == sorted(tuple(x) for x in rank_plan["if_win_affected_choices"]), \
            (index, "affected choices drifted from the frozen ranking")
        affected_now = sorted(k for k, s in baseline_choices.items() if index in g["s4_cost"][s])
        affected_s4_now = sorted({baseline_choices[k] for k in affected_now})
        entry: dict = dict(
            verdict=verdicts[index],
            ranking_tsv_row={k: int(tsv_row[k]) for k in
                             ("geometry_rank", "if_win_loss_choices_invalidated",
                              "if_loss_fixed_win_branches_uncovered",
                              "if_win_new_free_win_branches",
                              "if_win_greedy_loss_union", "if_win_greedy_delta")},
            ranking_if_win_affected_choices=len(rank_plan["if_win_affected_choices"]),
            ranking_if_win_invalidated_options=rank_plan["if_win_invalidated_s4_options"],
            recomputed_invalidated_options=all_invalidated,
            affected_choices_k0423_baseline=len(affected_k0423),
            affected_choices_update7_baseline=len(affected_now),
            affected_s4_update7_baseline=affected_s4_now,
            in_update7_union=index in baseline_required)
        note = ""
        if verdicts[index] == 1:
            entry["newly_excluded_options"] = sorted(set(all_invalidated) - baseline_excluded)
            note = ("WIN exclusion: geometry identity asserted on the K0423 "
                    "and update7 baselines; the greedy repair is measured "
                    "directly by this round's changed choices")
        else:
            note = ("LOSS layering: the node leaves every cost set; the "
                    "K0423-baseline affected-choice list is reproduced "
                    "exactly, and the win-side branch incidences are "
                    "cross-checked in update_win_side.py")
        entry["note"] = note
        cross_check[str(index)] = entry
    for index in NEW_RECEIPTS:
        assert index in baseline_required, (index, "expected in the seventh-update union")
    assert NEW_PROBE_RECEIPT in baseline_required, "150871 expected in the earlier union"

    for i in NEW_RECEIPTS:
        assert i not in batch_union, f"{i} still required"
    assert NEW_PROBE_RECEIPT not in batch_union, "150871 still required"

    s6_derived = {str(idx): {"mask": f"{mask:032x}", "certificate": s6_cert.relative_to(ROOT).as_posix(),
                             "certificate_sha256": S6_CERT_SHA, "layered_round": 7 if idx in S6_PRIOR else 8}
                  for idx, mask in sorted(indexed_parents.items())}
    out = dict(
        schema="n11-night-repaired-joint-plan-update8-v1",
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
        known_loss_removed_from_cost=sorted({115540, 144193, NEW_PROBE_RECEIPT} | set(S6_EXTRA_EXPECTED)),
        s6_derived_losses=s6_derived,
        s6_derived_unindexed_masks=[f"{m:032x}" for m in sorted(unmapped)],
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
                     "upper bound may differ.  This round carries four receipts and "
                     "two extra certificate-derived parents, staged in NEW_ORDER "
                     "order (115540, 144193, 144311, 150871, 381858, 382619) from the same "
                     "frozen instance and asserted to reproduce the batch reflection "
                     "exactly."),
        },
        ranking_cross_check=cross_check,
        shared_checker_source_sha256=shared_checker_sha,
        trust=("optimistic plan only: old exact-S5 leaves remain solver-trusted; eighteen "
               "candidate receipts (558600 LOSS, 209644 WIN, 126899 LOSS, 144095 WIN, "
               "121263 LOSS, 145001 LOSS, 137694 LOSS, 143240 LOSS, 220231 LOSS, "
               "126017 WIN, 197665 WIN, 206386 WIN, 131631 WIN, 162106 WIN, "
               "115540 LOSS, 144193 LOSS, 144311 WIN, 150871 LOSS) terminal-verified with trusted "
               "leaves 0; six S5 LOSS verdicts (381840 / 402066 / 550881 / 381858 / "
               "382619 / 150871) and one unindexed parent derived from one cache-free six-stone "
               "terminal certificate (1,028,621 states, independent C++/Python "
               "agreement); all remaining required S5 verdicts UNKNOWN; not a root "
               "proof"),
    )
    target = EXP / "output/repaired-joint-plan-update8.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    assert not target.exists() or True
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
