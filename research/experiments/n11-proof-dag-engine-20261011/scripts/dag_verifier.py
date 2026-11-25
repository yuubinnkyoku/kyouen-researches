"""Independent checker for terminal-closed, move-labelled proof DAGs.

This module imports only K0372's standalone integer geometry Board.  It never
imports the builder or reads solver/cache verdicts.  Universal nodes must list
every concrete legal move; existential nodes carry exactly one legal witness.
"""
from __future__ import annotations

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, aggregate  # noqa: E402


def verify_certificate(certificate: dict) -> dict:
    if not isinstance(certificate, dict):
        raise ValueError("certificate must be an object")
    if certificate.get("schema") != "kyouen-proof-dag-edge-v1":
        raise ValueError("unsupported certificate schema")
    n = certificate.get("board_size")
    if type(n) is not int or not 1 <= n <= 11:
        raise ValueError("invalid board size")
    if certificate.get("proposition") != "original_first_player_wins":
        raise ValueError("unsupported proposition")
    if "trusted" in certificate or "trusted_leaves" in certificate:
        raise ValueError("trusted leaves are forbidden")
    nodes = certificate.get("nodes")
    root = certificate.get("root")
    if not isinstance(nodes, dict) or not nodes or not isinstance(root, str) or root not in nodes:
        raise ValueError("missing root or nodes")

    board = Board(n)
    visiting: set[str] = set()
    done: dict[str, int] = {}

    def visit(ident: str) -> int:
        if ident in visiting:
            raise ValueError("cycle in certificate")
        if ident in done:
            return done[ident]
        if ident not in nodes or not isinstance(nodes[ident], dict):
            raise ValueError("edge references a missing node")
        node = nodes[ident]
        try:
            mask = int(node["mask"])
            verdict = node["verdict"]
            stones = node["stones"]
            terminal = node["terminal"]
            edges = node["edges"]
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError("malformed node") from exc
        if ident != str(mask) or type(verdict) is not int or verdict not in (1, 2):
            raise ValueError("noncanonical identifier or invalid verdict")
        if type(stones) is not int or stones != mask.bit_count():
            raise ValueError("wrong stone count")
        if type(terminal) is not bool or not isinstance(edges, list):
            raise ValueError("malformed terminal/edge fields")
        if node.get("trusted") or node.get("trusted_leaf"):
            raise ValueError("trusted leaves are forbidden")
        try:
            legal = board.legal(mask)
        except (TypeError, ValueError) as exc:
            raise ValueError("unsafe or out-of-board position") from exc
        if board.canonical(mask) != mask:
            raise ValueError("position is not D4-canonical")
        moves = set(board.points(legal))
        legal_count = node.get("legal_count")
        if type(legal_count) is not int or legal_count != len(moves):
            raise ValueError("wrong legal move count")
        if terminal != (not moves):
            raise ValueError("terminal marker disagrees with geometry")
        visiting.add(ident)

        if not moves:
            if edges or aggregate(stones, ()) != verdict:
                raise ValueError("incorrect terminal verdict")
        else:
            labels = []
            child_values = []
            for edge in edges:
                if not isinstance(edge, dict) or set(edge) != {"move", "child"}:
                    raise ValueError("malformed edge")
                move, child_id = edge["move"], edge["child"]
                if type(move) is not int or move not in moves or not isinstance(child_id, str):
                    raise ValueError("illegal move label or child reference")
                if move in labels:
                    raise ValueError("duplicate move label")
                labels.append(move)
                child = nodes.get(child_id)
                if not isinstance(child, dict):
                    raise ValueError("edge references a missing child")
                try:
                    child_mask = int(child["mask"])
                except (KeyError, TypeError, ValueError) as exc:
                    raise ValueError("malformed child position") from exc
                expected = board.canonical(mask | (1 << move))
                if child_mask != expected or child_mask.bit_count() != stones + 1:
                    raise ValueError("edge has a nonlegal or incorrectly ranked transition")
                child_values.append(visit(child_id))

            decisive = 2 if stones % 2 else 1
            existential = verdict == decisive
            if existential:
                if len(edges) != 1 or child_values != [verdict]:
                    raise ValueError("existential node lacks one decisive witness")
            elif set(labels) != moves or len(labels) != len(moves):
                raise ValueError("universal node omits or duplicates a legal move")
            elif aggregate(stones, child_values) != verdict:
                raise ValueError("universal node has an incorrect fixed-player verdict")

        visiting.remove(ident)
        done[ident] = verdict
        return verdict

    result = visit(root)
    if len(done) != len(nodes):
        raise ValueError("certificate contains unreachable nodes")
    return dict(verdict=result, nodes=len(done),
                edges=sum(len(node["edges"]) for node in nodes.values()),
                terminal_nodes=sum(bool(node["terminal"]) for node in nodes.values()),
                trusted_leaves=0)
