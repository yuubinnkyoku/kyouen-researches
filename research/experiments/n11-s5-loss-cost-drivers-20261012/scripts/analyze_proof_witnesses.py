"""Inventory the S6 LOSS witnesses selected by the six terminal-only DAG roots."""
from __future__ import annotations

import gzip
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
EXP = Path(__file__).resolve().parents[1]
FOLLOWUP = ROOT / "research/experiments/n11-proof-dag-engine-followup-20261011"
INCREMENTAL = ROOT / "research/experiments/n11-proof-dag-incremental-20261011"
WITNESS = ROOT / "research/experiments/n11-s5-loss-witness-20261012"
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, mask_from_key  # noqa: E402


SOURCES = [
    {
        "group": "latest-s4",
        "certificate": FOLLOWUP / "output/current-s4-proof-bundle-reverse-v1/proof-dag-bundle.json.gz",
        "receipt": FOLLOWUP / "output/current-s4-proof-bundle-reverse-v1/verification.json",
        "certificate_sha256": "48edffe570591e7196c2021353342a05ba058d70b141f05128bd17c207d4e922",
        "receipt_sha256": "56e334a9a59421661facecb10a53fcb84665e4f7e16863e1412e155317c9e2bc",
    },
    {
        "group": "previous-s4",
        "certificate": FOLLOWUP / "output/shared-s5-proof-bundle-reverse-v1/proof-dag-bundle.json.gz",
        "receipt": FOLLOWUP / "output/shared-s5-proof-bundle-reverse-v1/verification.json",
        "certificate_sha256": "9f55e6997f62ee2bae31d286b98ad2b89b6306e18df5091eac081b05d5d10af6",
        "receipt_sha256": "2eaca0f3410c489e1e1b5cf06a22ac6308b8edc6a4f5bcc4c6a2fdc4b9106b77",
    },
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def closure(nodes: dict, root: str) -> tuple[set[str], int]:
    reached: set[str] = set()
    stack = [root]
    edge_count = 0
    while stack:
        ident = stack.pop()
        if ident in reached:
            continue
        node = nodes.get(ident)
        if node is None:
            raise ValueError(f"missing proof dependency {ident}")
        reached.add(ident)
        edges = node["edges"]
        edge_count += len(edges)
        stack.extend(edge["child"] for edge in edges)
    return reached, edge_count


def target_provenance() -> dict[str, dict]:
    targets = json.loads((WITNESS / "input/targets.json").read_text(encoding="utf-8"))
    result = {}
    for row in targets["positions"]:
        key = str((row["hi"] << 64) | row["lo"])
        result[key] = row
    return result


def analyze_source(source: dict, board: Board, provenance: dict[str, dict]) -> dict:
    for field in ("certificate", "receipt"):
        path = source[field]
        want = source["certificate_sha256" if field == "certificate" else "receipt_sha256"]
        if sha256(path) != want:
            raise ValueError(f"{field} SHA-256 mismatch: {path}")
    receipt = json.loads(source["receipt"].read_text(encoding="utf-8"))
    if receipt["trusted_leaves"] != 0 or any(root["verdict"] != 2 for root in receipt["roots"]):
        raise ValueError("source receipt is not a terminal-only LOSS proof for every root")

    with gzip.open(source["certificate"], "rt", encoding="utf-8") as stream:
        certificate = json.load(stream)
    if certificate.get("board_size") != 11 or certificate.get("schema") != "kyouen-proof-dag-multi-root-v1":
        raise ValueError("unexpected proof DAG format or board size")
    nodes = certificate["nodes"]
    root_rows = []
    witness_closures: dict[str, set[str]] = {}
    for root_row in certificate["roots"]:
        s5_key = root_row["root"]
        s5 = nodes[s5_key]
        s5_mask = int(s5_key)
        if s5_mask.bit_count() != 5 or s5["stones"] != 5 or s5["verdict"] != 2:
            raise ValueError(f"not a five-stone LOSS root: {s5_key}")
        s5_moves = board.children(s5_mask)
        if len(s5["edges"]) != 1:
            raise ValueError(f"S5 LOSS root must contain one existential witness: {s5_key}")
        chosen = s5["edges"][0]["child"]
        if chosen not in {str(mask) for mask in s5_moves}:
            raise ValueError(f"proof witness is not a legal S6 child of {s5_key}")

        available = []
        for mask in sorted(s5_moves):
            ident = str(mask)
            node = nodes.get(ident)
            if node is not None and node["verdict"] == 2:
                witness_nodes, witness_edges = closure(nodes, ident)
                s6 = node
                if (s6["stones"] != 6 or len(s6["edges"]) != s6["legal_count"]
                        or any(nodes[edge["child"]]["verdict"] != 2 for edge in s6["edges"])):
                    raise ValueError(f"S6 LOSS witness is not fully closed: {ident}")
                available.append({
                    "s6_key": ident,
                    "legal_s7_children": s6["legal_count"],
                    "proof_dag_nodes": len(witness_nodes),
                    "proof_dag_edges": witness_edges,
                    "is_selected_by_s5_root": ident == chosen,
                })
        if not any(candidate["s6_key"] == chosen for candidate in available):
            raise ValueError(f"selected witness is absent from closed proof DAG: {chosen}")
        witness_nodes, witness_edges = closure(nodes, chosen)
        witness_closures[s5_key] = witness_nodes
        row = {
            "group": source["group"],
            "s5_key": s5_key,
            "s5_legal_s6_children": len(s5_moves),
            "s5_dag_outdegree": len(s5["edges"]),
            "selected_s6_key": chosen,
            "selected_s6_legal_s7_children": nodes[chosen]["legal_count"],
            "selected_s6_dag_nodes": len(witness_nodes),
            "selected_s6_dag_edges": witness_edges,
            "all_stored_s6_loss_candidates": available,
            "historical_direct_s5_raw": provenance.get(s5_key),
        }
        root_rows.append(row)

    shared = {}
    for s5_key, reached in witness_closures.items():
        shared[s5_key] = {
            "reachable_nodes": len(reached),
            "nodes_shared_with_other_s5_witness_closures": len(
                reached.intersection(set.union(*(v for k, v in witness_closures.items() if k != s5_key)))
            ) if len(witness_closures) > 1 else 0,
        }
    union = set().union(*witness_closures.values()) if witness_closures else set()
    return {
        "source_group": source["group"],
        "certificate_path": str(source["certificate"].relative_to(ROOT)).replace("\\", "/"),
        "certificate_sha256": source["certificate_sha256"],
        "receipt_path": str(source["receipt"].relative_to(ROOT)).replace("\\", "/"),
        "receipt_sha256": source["receipt_sha256"],
        "receipt_nodes": receipt["nodes"],
        "receipt_edges": receipt["edges"],
        "receipt_trusted_leaves": receipt["trusted_leaves"],
        "witness_closure_union_nodes": len(union),
        "witness_closure_union_edges": sum(len(nodes[node]["edges"]) for node in union),
        "cross_root_witness_sharing": shared,
        "roots": root_rows,
    }


def main() -> None:
    out = EXP / "input/proof-witness-inventory.json"
    if out.exists():
        raise FileExistsError(out)
    board = Board(11)
    provenance = target_provenance()
    sources = [analyze_source(source, board, provenance) for source in SOURCES]
    integration_path = INCREMENTAL / "output/integration-audit.json"
    if sha256(integration_path) != "ecb0157e76521948601ce1d2ffeb74d34c35f7e1143ee93811a913ab25e0475d":
        raise ValueError("six-root integration audit SHA-256 mismatch")
    integration = json.loads(integration_path.read_text(encoding="utf-8"))
    independent = integration["independent_verification"]
    if (independent["trusted_leaves"] != 0 or independent["nodes"] != 2_720_770
            or independent["edges"] != 4_065_013
            or integration["six_root_integration"]["duplicate_positions_shared"] != 0):
        raise ValueError("six-root independent integration receipt does not match K0378")
    result = {
        "schema": "n11-s5-loss-proof-witness-inventory-v1",
        "method": "Read only the two independently verified terminal-only proof DAGs; count the reachable S6 proof sub-DAG and identify every saved legal S6 LOSS node among each S5 root's legal S6 children.",
        "solver_node_counts_are_not_proof_dag_node_counts": True,
        "board_size": 11,
        "six_root_integration_audit": {
            "path": str(integration_path.relative_to(ROOT)).replace("\\", "/"),
            "sha256": "ecb0157e76521948601ce1d2ffeb74d34c35f7e1143ee93811a913ab25e0475d",
            "roots": 6, "nodes": independent["nodes"], "edges": independent["edges"],
            "trusted_leaves": independent["trusted_leaves"],
            "cross_bundle_duplicate_positions": integration["six_root_integration"]["duplicate_positions_shared"],
        },
        "sources": sources,
    }
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(result, sort_keys=True, separators=(",", ":")) + "\n", encoding="utf-8")
    print(json.dumps({"path": str(out.relative_to(ROOT)).replace("\\", "/"),
                      "sha256": sha256(out), "roots": [r for s in sources for r in s["roots"]]},
                     sort_keys=True))


if __name__ == "__main__":
    main()
