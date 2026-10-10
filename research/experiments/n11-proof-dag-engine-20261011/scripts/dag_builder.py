"""Build terminal-closed, move-labelled Kyouen proof DAGs.

The builder imports only the standalone Board implementation from K0372.  It
does not read solver tables, cache rows, or trusted verdicts.  Search ordering
and D4 state sharing affect cost only; every emitted edge is still checked by
dag_verifier.py.
"""
from __future__ import annotations

import time
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board, aggregate  # noqa: E402


class ProofLimitExceeded(RuntimeError):
    pass


class ProofTimeExceeded(RuntimeError):
    pass


ORDERS = {"count-asc", "count-desc", "key"}


def build_certificate(n: int, root: int, node_limit: int = 1_000_000,
                      order: str = "count-asc", state_sharing: str = "d4",
                      timeout_seconds: float | None = None):
    """Solve *root* and emit only a complete terminal proof DAG.

    `node_limit` counts recursive position evaluations. With D4 sharing on,
    only canonical positions are evaluated once. With sharing off, repeated
    canonical positions are re-evaluated to quantify the value of memoization;
    the final proof still deduplicates their nodes by canonical occupancy.
    """
    if type(n) is not int or not 1 <= n <= 11:
        raise ValueError("board size must be in 1..11")
    if type(root) is not int or root < 0 or root >> (n * n):
        raise ValueError("root mask is outside the board")
    if type(node_limit) is not int or node_limit < 1:
        raise ValueError("node_limit must be positive")
    if order not in ORDERS:
        raise ValueError(f"unsupported order: {order}")
    if state_sharing not in {"d4", "none"}:
        raise ValueError(f"unsupported state sharing: {state_sharing}")

    board = Board(n)
    root = board.canonical(root)
    board.legal(root)  # Fail closed on unsafe occupied input.
    solved: dict[int, int] = {}
    nodes: dict[str, dict] = {}
    active: set[int] = set()
    stats = dict(calls=0, expanded=0, memo_hits=0, edge_visits=0,
                 unique_positions=0, max_depth=0)
    started = time.monotonic()

    def solve(mask: int, depth: int) -> int:
        mask = board.canonical(mask)
        if state_sharing == "d4" and mask in solved:
            stats["memo_hits"] += 1
            return solved[mask]
        if mask in active:
            raise RuntimeError("cycle in increasing-stone game graph")
        if stats["calls"] >= node_limit:
            raise ProofLimitExceeded(f"proof node limit {node_limit} exceeded")
        if timeout_seconds is not None and time.monotonic() - started > timeout_seconds:
            raise ProofTimeExceeded(f"proof time limit {timeout_seconds}s exceeded")
        stats["calls"] += 1
        stats["expanded"] += 1
        stats["max_depth"] = max(stats["max_depth"], depth)
        active.add(mask)

        legal = board.legal(mask)
        moves = list(board.points(legal))
        stones = mask.bit_count()
        if not moves:
            verdict = aggregate(stones, ())
            nodes[str(mask)] = dict(mask=str(mask), stones=stones, verdict=verdict,
                                    terminal=True, legal_count=0, edges=[])
        else:
            children = [(move, board.canonical(mask | (1 << move))) for move in moves]
            if order == "count-asc":
                children.sort(key=lambda e: (board.legal(e[1]).bit_count(), e[1], e[0]))
            elif order == "count-desc":
                children.sort(key=lambda e: (-board.legal(e[1]).bit_count(), e[1], e[0]))
            else:
                children.sort(key=lambda e: (e[1], e[0]))

            decisive = 2 if stones % 2 else 1
            edge_rows = []
            child_values = []
            witness = None
            for move, child in children:
                stats["edge_visits"] += 1
                child_value = solve(child, depth + 1)
                child_values.append(child_value)
                edge_rows.append(dict(move=move, child=str(child)))
                if child_value == decisive:
                    witness = (move, child)
                    break

            if witness is not None:
                verdict = decisive
                edge_rows = [dict(move=witness[0], child=str(witness[1]))]
            else:
                verdict = aggregate(stones, child_values)
                if verdict == 0:
                    raise RuntimeError("complete search returned UNKNOWN")
                # The non-decisive outcome is proved only by every legal move.
                if len(edge_rows) != len(moves):
                    raise RuntimeError("universal proof omitted a legal move")
                edge_rows.sort(key=lambda e: e["move"])
            nodes[str(mask)] = dict(mask=str(mask), stones=stones, verdict=verdict,
                                    terminal=False, legal_count=len(moves), edges=edge_rows)

        active.remove(mask)
        solved[mask] = verdict
        stats["unique_positions"] = len(nodes)
        return verdict

    verdict = solve(root, 0)
    search_unique_positions = len(nodes)
    proof_nodes: dict[str, dict] = {}

    def retain(ident: str):
        if ident in proof_nodes:
            return
        node = nodes[ident]
        proof_nodes[ident] = node
        for edge in node["edges"]:
            retain(edge["child"])

    retain(str(root))
    certificate = dict(schema="kyouen-proof-dag-edge-v1", board_size=n,
                       proposition="original_first_player_wins", root=str(root),
                       nodes=proof_nodes)
    stats.update(verdict=verdict, elapsed_seconds=time.monotonic() - started,
                 search_unique_positions=search_unique_positions,
                 node_count=len(proof_nodes), edge_count=sum(len(x["edges"]) for x in proof_nodes.values()),
                 state_sharing=state_sharing, order=order)
    return certificate, stats
