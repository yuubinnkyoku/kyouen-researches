"""Freeze a small, certificate-backed cost-driver benchmark before solver runs."""
from __future__ import annotations

import csv
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
PREVIOUS = ROOT / "research/experiments/n11-s5-loss-witness-20261012"
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, mask_from_key  # noqa: E402


SELECTED_IDS = ["previous-s4/second", "latest-s4/legal84", "latest-s4/legal92"]
S5_CAP = 6_000_000
S6_PREFIX = 6
S6_CAP = S5_CAP // S6_PREFIX


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def read_one_raw(target: dict) -> dict:
    path = ROOT / target["source_csv"]
    if sha256(path) != target["source_csv_sha256"]:
        raise ValueError(f"historical raw SHA mismatch: {path}")
    matches = []
    with path.open(encoding="utf-8", newline="") as stream:
        for row in csv.reader(stream):
            if row and row[0] == "replay" and len(row) == 11:
                if (int(row[9]), int(row[10])) == (target["lo"], target["hi"]):
                    matches.append(row)
    if len(matches) != 1:
        raise ValueError(f"expected one historical solver row for {target['id']}")
    row = matches[0]
    if (int(row[2]), int(row[3]), int(row[6]), int(row[7])) != (
            target["stones"], target["legal"], target["expected_verdict"], target["prior_nodes"]):
        raise ValueError(f"historical raw row differs from fixed target: {target['id']}")
    return {"path": target["source_csv"], "sha256": target["source_csv_sha256"],
            "nodes": int(row[7]), "verdict": int(row[6]), "reported_seconds": int(row[8])}


def main() -> None:
    out = EXP / "input/comparison-schedule.json"
    targets_path = PREVIOUS / "input/targets.json"
    inventory_path = EXP / "input/proof-witness-inventory.json"
    targets = json.loads(targets_path.read_text(encoding="utf-8"))
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if inventory["schema"] != "n11-s5-loss-proof-witness-inventory-v1":
        raise ValueError("unexpected proof witness inventory")
    proof_roots = {root["historical_direct_s5_raw"]["id"]: root
                   for source in inventory["sources"] for root in source["roots"]}
    source_targets = {row["id"]: row for row in targets["positions"]}
    if not set(SELECTED_IDS) <= source_targets.keys() or not set(SELECTED_IDS) <= proof_roots.keys():
        raise ValueError("selected target is missing from historical raw or independent proof inventory")

    board = Board(11)
    selected = []
    for ident in SELECTED_IDS:
        target = source_targets[ident]
        raw = read_one_raw(target)
        mask = mask_from_key(target["lo"], target["hi"], board.n)
        if (mask.bit_count() != 5 or board.canonical(mask) != mask
                or board.legal(mask).bit_count() != target["legal"]):
            raise ValueError(f"target is unsafe, noncanonical, or wrong rank: {ident}")
        inventory_row = proof_roots[ident]
        children = []
        for child in board.children(mask):
            children.append({
                "key": str(child), "lo": child & ((1 << 64) - 1),
                "hi": child >> 64, "stones": 6,
                "legal": board.legal(child).bit_count(),
            })
        if len(children) != target["legal"]:
            raise ValueError(f"S5/S6 geometry count mismatch: {ident}")
        ranked = sorted(children, key=lambda child: (child["legal"], int(child["key"])))
        proof_candidates = inventory_row["all_stored_s6_loss_candidates"]
        candidate_keys = {candidate["s6_key"] for candidate in proof_candidates}
        legal_child_keys = {child["key"] for child in children}
        if not candidate_keys or not candidate_keys <= legal_child_keys:
            raise ValueError(f"saved S6 LOSS witness is not a legal child: {ident}")
        enriched_candidates = []
        for candidate in proof_candidates:
            geometry_row = next(child for child in children if child["key"] == candidate["s6_key"])
            if geometry_row["legal"] != candidate["legal_s7_children"]:
                raise ValueError(f"S6 witness legal count mismatch: {candidate['s6_key']}")
            enriched_candidates.append({**candidate, "s6_lo": geometry_row["lo"],
                "s6_hi": geometry_row["hi"], "s6_stones": 6,
                "s6_legal": geometry_row["legal"]})
        selected.append({
            "id": ident,
            "s5": {"key": str(mask), "lo": target["lo"], "hi": target["hi"],
                   "stones": 5, "legal": target["legal"], "expected_verdict": 2},
            "historical_direct_s5": {"nodes": raw["nodes"], "reported_seconds": raw["reported_seconds"],
                                     "raw_path": raw["path"], "raw_sha256": raw["sha256"]},
            "saved_s6_loss_candidates": enriched_candidates,
            "all_s6_children_geometry": sorted(children, key=lambda child: int(child["key"])),
            "blind_legal_count_prefix": ranked[:S6_PREFIX],
        })

    audit_path = ROOT / "research/experiments/n11-reply27-20more-20261011/output/audit.json"
    if sha256(audit_path) != "87b155e3b18fa7f9456d8513b7edd5b43ced94872226943ee9c0ec31368c8e5e":
        raise ValueError("current-S4 audit SHA-256 mismatch")
    audit = json.loads(audit_path.read_text(encoding="utf-8"))
    boundary = audit["target_s4_after"]
    if boundary != {"LOSS": 40, "UNKNOWN": 66, "WIN": 0}:
        raise ValueError(f"latest current-S4 boundary differs from requested checkpoint: {boundary}")

    result = {
        "schema": "n11-s5-loss-cost-driver-schedule-v1",
        "selection_rule": "Three fixed, already independently terminal-closed roots: the minimum S6 proof-DAG closure among all six, one current-S4 root with two saved S6 LOSS alternatives, and the largest current-S4 witness closure. No current UNKNOWN S5 is searched.",
        "targets_source": str(targets_path.relative_to(ROOT)).replace("\\", "/"),
        "targets_sha256": sha256(targets_path),
        "proof_inventory": str(inventory_path.relative_to(ROOT)).replace("\\", "/"),
        "proof_inventory_sha256": sha256(inventory_path),
        "independent_boundary": {
            "path": str(audit_path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": sha256(audit_path), "s4_key": "1297036692683752448",
            "loss": boundary["LOSS"], "win": boundary["WIN"], "unknown": boundary["UNKNOWN"],
            "unresolved_third_moves": audit["unresolved_third_moves"],
        },
        "budget_protocol": {
            "stage1_s5_root_node_cap": S5_CAP,
            "stage1_s6_single_candidate_node_cap": S5_CAP,
            "stage1_ranked_s6_candidate_cap_per_candidate": S6_CAP,
            "stage1_ranked_prefix_length": S6_PREFIX,
            "stage1_ranked_total_cap_per_s5": S6_CAP * S6_PREFIX,
            "stage2_cap_if_unknown": 12_000_000,
            "stage2_cost_accounting": "A retry starts with a fresh TT and all stage-1 nodes remain charged; the stages are reported cumulatively, while each stage's cap remains a per-root cap.",
            "start_rationale": "Stage 1 is above every historical completed direct-S5 cost in the six-root sample (2,335,333–5,416,337 nodes); this avoids repeating K0380's all-UNKNOWN 250,000-node pilot.",
        },
        "common_solver_conditions": {
            "board_size": 11, "binary_for_all_arms": "built after adding opt-in replay profiling",
            "memo_power": 22, "exact_order": "count", "external_cache": "none",
            "persistent_s5_cache": "none", "initial_cache": "fresh solver/TT per direct S5 or known S6 arm; cold TT at the start of each ranked S5 batch",
            "proof_trust": "new solver outputs are measurement only; the pinned terminal-only proof DAGs remain the independent LOSS evidence",
        },
        "arms": {
            "A": "Direct S5 exact DFPN; fresh TT per root; one root row capped at 6M.",
            "B": "Each saved S6 LOSS witness exact DFPN in isolation; fresh TT per witness; 6M cap each. The target with two saved witnesses runs both as separate reference cases.",
            "C1": "Search the first six S6 children ordered only by ascending legal-S7 count then canonical key; fresh TT per child; 1M cap per child; stop only at exact S6 LOSS.",
            "C2": "Same geometry-only six-child order and per-child cap as C1, but share one initially empty TT across that S5's candidate rows; stop only at exact S6 LOSS.",
        },
        "targets": selected,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(out.relative_to(ROOT)).replace("\\", "/"),
                      "sha256": sha256(out), "targets": SELECTED_IDS,
                      "budget": result["budget_protocol"]}, sort_keys=True))


if __name__ == "__main__":
    main()
