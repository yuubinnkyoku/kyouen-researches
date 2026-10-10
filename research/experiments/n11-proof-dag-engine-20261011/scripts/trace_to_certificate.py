"""Turn solver dependency telemetry into the portable move-labelled DAG schema."""
from __future__ import annotations

import csv
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board  # noqa: E402


def trace_to_certificate(path: Path, n: int, expected_root: int,
                         expected_verdict: int) -> tuple[dict, dict]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or not lines[0].startswith("# kyouen-proof-trace-v1,"):
        raise ValueError("missing proof trace header")
    fields = dict(item.split("=", 1) for item in lines[0][2:].split(",")[1:])
    if int(fields["n"]) != n:
        raise ValueError("proof trace board size mismatch")
    root = int(fields["root_lo"]) | (int(fields["root_hi"]) << 64)
    verdict = int(fields["verdict"])
    if root != expected_root or verdict != expected_verdict or verdict not in (1, 2):
        raise ValueError("proof trace root/verdict does not match solver replay")

    board = Board(n)
    raw_nodes: dict[int, dict] = {}
    raw_edges: dict[int, list[dict]] = {}
    for row in csv.reader(lines[1:]):
        if not row:
            continue
        if row[0] == "N" and len(row) == 5:
            mask = int(row[1]) | (int(row[2]) << 64)
            node_verdict, terminal = int(row[3]), int(row[4])
            if mask in raw_nodes or node_verdict not in (1, 2) or terminal not in (0, 1):
                raise ValueError("duplicate or malformed proof node")
            raw_nodes[mask] = dict(mask=str(mask), stones=mask.bit_count(),
                                   verdict=node_verdict, terminal=bool(terminal),
                                   edges=[])
            raw_edges[mask] = []
        elif row[0] == "E" and len(row) == 6:
            parent = int(row[1]) | (int(row[2]) << 64)
            move = int(row[3])
            child = int(row[4]) | (int(row[5]) << 64)
            raw_edges.setdefault(parent, []).append(dict(move=move, child=str(child)))
        else:
            raise ValueError("malformed proof trace row")

    if root not in raw_nodes or raw_nodes[root]["verdict"] != verdict:
        raise ValueError("proof trace is missing its root")
    for parent, edges in raw_edges.items():
        if parent not in raw_nodes:
            raise ValueError("edge appears before or without its parent node")
        for edge in edges:
            if int(edge["child"]) not in raw_nodes:
                raise ValueError("proof trace references a missing child node")
        raw_nodes[parent]["edges"] = edges

    reachable: set[int] = set()
    pending = [root]
    while pending:
        mask = pending.pop()
        if mask in reachable:
            continue
        if mask not in raw_nodes:
            raise ValueError("proof trace references a missing child node")
        reachable.add(mask)
        for edge in raw_nodes[mask]["edges"]:
            child = int(edge["child"])
            if child not in raw_nodes:
                raise ValueError("proof trace references a missing child node")
            pending.append(child)
    # Geometry is expensive on 11x11. Only retained proof nodes need it here;
    # the independent verifier repeats these checks over the complete DAG.
    for mask in reachable:
        if board.canonical(mask) != mask:
            raise ValueError("solver trace contains a noncanonical proof position")
        raw_nodes[mask]["legal_count"] = len(board.points(board.legal(mask)))
    nodes = {str(mask): raw_nodes[mask] for mask in sorted(reachable)}
    certificate = dict(schema="kyouen-proof-dag-edge-v1", board_size=n,
                       proposition="original_first_player_wins", root=str(root), nodes=nodes)
    stats = dict(trace_nodes=len(raw_nodes), proof_nodes=len(nodes),
                 orphan_nodes=len(raw_nodes) - len(nodes),
                 trace_edges=sum(len(x) for x in raw_edges.values()),
                 proof_edges=sum(len(node["edges"]) for node in nodes.values()))
    return certificate, stats
