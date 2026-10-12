#!/usr/bin/env python3
"""Count solver-trusted dependencies of reply27 LOSS and rank small proof pilots."""
from __future__ import annotations

import argparse
import csv
import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
REPLY = ROOT / "research/experiments/n11-s4-boundary-direct-20261012"
PROOF = REPLY / "output/root-60-27-loss-proof.json"
CACHE = REPLY / "output/current-exact-s5.cache"
GEOMETRY = ROOT / "research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
K0375_INPUT = ROOT / "research/experiments/n11-proof-dag-engine-followup-20261011/input/current-s4-resolved-s5-positions.json"
K0378_PLAN = ROOT / "research/experiments/n11-proof-dag-incremental-20261011/output/integration-plan.json"
HELPER = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"


def sha(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def load_cache(path: Path) -> dict[tuple[int, int], dict]:
    rows = {}
    with path.open(encoding="utf-8-sig", newline="") as stream:
        for row in csv.reader(stream):
            if not row or row[0].lstrip().startswith("#"):
                continue
            if len(row) != 6 or row[0] != "s5verdict":
                raise ValueError(f"invalid S5 cache row: {row}")
            lo, hi, stones, verdict, nodes = map(int, row[1:])
            key = (lo, hi)
            if stones != 5 or verdict not in (1, 2) or nodes < 0 or key in rows:
                raise ValueError(f"invalid/duplicate S5 cache evidence: {key}")
            rows[key] = {"verdict": verdict, "nodes": nodes}
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path,
                        default=ROOT / "research/experiments/n11-reply27-terminal-proof-priority-20261012/output/terminal-proof-priority.json")
    args = parser.parse_args()

    sys.path.insert(0, str(HELPER))
    from independent import Board
    board = Board(11)
    proof = json.loads(PROOF.read_text(encoding="utf-8"))
    cache = load_cache(CACHE)
    if proof.get("root_outcome") != "LOSS" or len(proof.get("third_move_witnesses", [])) != 119:
        raise ValueError("root proof is not the complete 119-move LOSS certificate")

    s5_edges = 0
    dependencies = set()
    used_s4 = []
    for entry in proof["used_s4_loss_classes"]:
        key = tuple(entry["key"])
        mask = key[0] | (key[1] << 64)
        if mask.bit_count() != 4 or board.canonical(mask) != mask:
            raise ValueError(f"invalid S4 root in proof table: {key}")
        children = board.children(mask)
        if len(children) != entry["s5_children"]:
            raise ValueError(f"S4 child count changed for {key}")
        keys = {(child & ((1 << 64) - 1), child >> 64) for child in children}
        s5_edges += len(keys)
        dependencies.update(keys)
        used_s4.append({"key": list(key), "s5_children": len(keys)})
    if len(used_s4) != proof["distinct_s4_loss_classes_used"]:
        raise ValueError("S4 witness-class count mismatch")
    if any(cache.get(key, {}).get("verdict") != 2 for key in dependencies):
        raise ValueError("a required S5 child is missing or not exact LOSS in current cache")

    positive = []
    zero_node = []
    for key in dependencies:
        row = cache[key]
        mask = key[0] | (key[1] << 64)
        legal = board.legal(mask).bit_count()
        candidate = {"key": list(key), "legal": legal, "cache_nodes": row["nodes"], "verdict": "LOSS"}
        (positive if row["nodes"] > 0 else zero_node).append(candidate)
    positive.sort(key=lambda row: (row["cache_nodes"], row["legal"], row["key"]))
    zero_node.sort(key=lambda row: (row["legal"], row["key"]))

    current_roots = json.loads(K0375_INPUT.read_text(encoding="utf-8"))["positions"]
    current_bundle_roots = []
    for row in current_roots:
        key = (int(row["lo"]), int(row["hi"]))
        current_bundle_roots.append({"id": row["id"], "key": list(key), "in_reply27_dependency_set": key in dependencies})

    plan = json.loads(K0378_PLAN.read_text(encoding="utf-8"))
    six_bundle_roots = plan["final_root_masks"]
    reusable_roots = []
    for row in six_bundle_roots:
        mask = int(row["root"])
        key = (mask & ((1 << 64) - 1), mask >> 64)
        if board.canonical(mask) != mask or mask.bit_count() != 5:
            raise ValueError(f"invalid K0378 root mask: {row}")
        reusable_roots.append({"id": row["id"], "key": list(key),
                               "in_reply27_dependency_set": key in dependencies})
    closed_roots = {tuple(row["key"]) for row in reusable_roots if row["in_reply27_dependency_set"]}
    remaining = [row for row in positive if tuple(row["key"]) not in closed_roots]
    if not remaining:
        raise ValueError("no open solver-trusted S5 dependency remains for pilot selection")
    pilot_positive = [remaining[0], remaining[len(remaining) // 2], remaining[-1]]
    pilot_zero = [zero_node[0], zero_node[len(zero_node) // 2], zero_node[-1]] if zero_node else []

    target_s6_audit = json.loads((REPLY / "output/s6-fourteenth-batch-audit.json").read_text(encoding="utf-8"))
    target_s6_raw = target_s6_audit["loss_witnesses"]
    if target_s6_raw != [[1152921504675009536, 536870912]]:
        raise ValueError("target direct S6 LOSS witness changed")

    output = args.output if args.output.is_absolute() else ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    doc = {
        "schema": "n11-reply27-terminal-proof-gap-v1",
        "root": [60, 27],
        "root_outcome": "LOSS (solver-trusted leaves)",
        "s3_response_table_rows": 119,
        "s4_loss_witness_classes": len(used_s4),
        "s4_to_s5_dependency_edges": s5_edges,
        "unique_s5_loss_roots_required": len(dependencies),
        "all_required_s5_cache_verdicts_are_loss": True,
        "required_s5_rows_with_nonzero_cache_nodes": len(positive),
        "required_s5_rows_with_zero_cache_nodes": len(zero_node),
        "sum_of_nonzero_s5_cache_nodes": sum(row["cache_nodes"] for row in positive),
        "terminal_only_s5_roots_reusable_from_k0378": len(closed_roots),
        "terminal_only_s5_roots_remaining": len(dependencies) - len(closed_roots),
        "k0375_current_s4_roots": current_bundle_roots,
        "k0378_six_root_bundle_membership": reusable_roots,
        "small_solver_trusted_pilot_candidates_by_recorded_node_count": pilot_positive,
        "small_cache_only_or_derived_pilot_candidates_by_legal_count": pilot_zero,
        "target_s6_loss_witness": {"key": target_s6_raw[0], "audit": "research/experiments/n11-s4-boundary-direct-20261012/output/s6-fourteenth-batch-audit.json"},
        "reusable_assets": {
            "K0372": "Reuse independent.py Board/verify_dag, cache quarantine rules, and the explicit trusted-leaf distinction; its 10,407-node S6 WIN certificate is a method/validator asset, not one of this root's S5 LOSS roots.",
            "K0375": "Three current-S4 S5 LOSS roots with trusted-leaf-free proof bundle; membership is listed above.",
            "K0377": "Compact witness-switch variant for the same three current-S4 roots; use only if the root keys match the dependency set.",
            "K0378": "Six-root compact proof bundle; root-key overlap is listed above and is the directly reusable terminal-only subset.",
        },
        "priority": [
            "Keep the existing six verified S5 terminal-only roots as frozen reusable certificates.",
            "For a bounded next pilot, choose a low-, middle-, and high-recorded-node S5 LOSS root from the dependency set, excluding roots already closed by K0378; measure proof nodes, edges, terminals, RSS, and bytes before scaling.",
            "Then sample zero-node S5 cache claims by legal-count strata; generate only after the positive-node pilot establishes a practical capture and verification budget.",
            "Integrate shared terminal closures only after per-root independent verification; do not extrapolate a linear size or runtime from six roots.",
        ],
        "solver_search_launched": False,
        "limitation": "The 2,995 S5 roots are not terminally closed by this analysis. Existing solver exact/cache verdicts remain trusted for all roots outside the named closed proof-DAG subset.",
        "source_hashes": {
            "root_move_proof_sha256": sha(PROOF),
            "current_s5_cache_sha256": sha(CACHE),
            "k0375_current_root_manifest_sha256": sha(K0375_INPUT),
            "k0378_integration_plan_sha256": sha(K0378_PLAN),
            "independent_geometry_sha256": sha(HELPER / "independent.py"),
        },
    }
    output.write_text(json.dumps(doc, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in doc.items() if k not in ("k0375_current_s4_roots", "k0378_six_root_bundle_membership")},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
