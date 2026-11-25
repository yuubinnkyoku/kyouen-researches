"""Merge independently closed proof bundles and optimize shared witnesses.

Inputs are restricted to the two SHA-pinned, terminal-only K0375 bundles.
No solver or cache evidence is read.  The first stage optimizes the existing
three-root bundle; the second imports the other verified bundle, preserves the
first-stage choices, adds its roots, and jointly improves witness choices.
"""
from __future__ import annotations

import argparse
from array import array
import hashlib
import itertools
import json
import math
from pathlib import Path
import sqlite3
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parents[4]
COMPACT = ROOT / "research/experiments/n11-proof-compact-20261011/scripts"
sys.path.insert(0, str(COMPACT))
from bundle_store import (  # noqa: E402
    PROPOSITION,
    SCHEMA,
    _blob,
    _file_sha256,
    _open_store,
    _parse_mask,
    load_json_bundle,
    write_compact,
)
from independent import Board  # noqa: E402

FOLLOWUP = ROOT / "research/experiments/n11-proof-dag-engine-followup-20261011"
MANIFEST = FOLLOWUP / "output/final-sha256.json"
MAX_SEQUENCE = 0xFFFFFFFF

SOURCES = (
    {
        "name": "latest-s4",
        "source_order": 0,
        "bundle": FOLLOWUP / "output/current-s4-proof-bundle-reverse-v1/proof-dag-bundle.json.gz",
        "bundle_relative": "output/current-s4-proof-bundle-reverse-v1/proof-dag-bundle.json.gz",
        "bundle_sha256": "48edffe570591e7196c2021353342a05ba058d70b141f05128bd17c207d4e922",
        "verification": FOLLOWUP / "output/current-s4-proof-bundle-reverse-v1/verification.json",
        "verification_relative": "output/current-s4-proof-bundle-reverse-v1/verification.json",
        "verification_sha256": "56e334a9a59421661facecb10a53fcb84665e4f7e16863e1412e155317c9e2bc",
        "nodes": 2_337_747,
        "edges": 3_484_437,
    },
    {
        "name": "previous-s4",
        "source_order": 1,
        "bundle": FOLLOWUP / "output/shared-s5-proof-bundle-reverse-v1/proof-dag-bundle.json.gz",
        "bundle_relative": "output/shared-s5-proof-bundle-reverse-v1/proof-dag-bundle.json.gz",
        "bundle_sha256": "9f55e6997f62ee2bae31d286b98ad2b89b6306e18df5091eac081b05d5d10af6",
        "verification": FOLLOWUP / "output/shared-s5-proof-bundle-reverse-v1/verification.json",
        "verification_relative": "output/shared-s5-proof-bundle-reverse-v1/verification.json",
        "verification_sha256": "2eaca0f3410c489e1e1b5cf06a22ac6308b8edc6a4f5bcc4c6a2fdc4b9106b77",
        "nodes": 1_002_511,
        "edges": 1_517_437,
    },
)


def _digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def preflight_sources() -> tuple[list[dict], dict]:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    by_path = {entry["path"]: entry for entry in manifest["files"]}
    receipts = []
    for source in SOURCES:
        bundle, verification = source["bundle"], source["verification"]
        bundle_entry = by_path.get(source["bundle_relative"])
        verification_entry = by_path.get(source["verification_relative"])
        if not bundle_entry or not verification_entry:
            raise ValueError(f"K0375 manifest omits {source['name']} artifacts")
        if (bundle_entry["sha256"] != source["bundle_sha256"]
                or verification_entry["sha256"] != source["verification_sha256"]):
            raise ValueError(f"K0375 hash inventory changed for {source['name']}")
        if (bundle.stat().st_size != bundle_entry["bytes"]
                or _digest(bundle) != source["bundle_sha256"]):
            raise ValueError(f"proof input hash mismatch: {bundle}")
        if (verification.stat().st_size != verification_entry["bytes"]
                or _digest(verification) != source["verification_sha256"]):
            raise ValueError(f"prior verifier receipt hash mismatch: {verification}")
        receipt = json.loads(verification.read_text(encoding="utf-8"))
        if (receipt.get("nodes") != source["nodes"]
                or receipt.get("edges") != source["edges"]
                or receipt.get("trusted_leaves") != 0
                or len(receipt.get("roots", [])) != 3
                or any(root.get("verdict") != 2 for root in receipt["roots"])):
            raise ValueError(f"prior independent receipt is not the expected closed bundle: {source['name']}")
        receipts.append({
            "name": source["name"],
            "bundle": str(bundle.relative_to(ROOT)).replace("\\", "/"),
            "bundle_bytes": bundle.stat().st_size,
            "bundle_sha256": source["bundle_sha256"],
            "prior_verification": str(verification.relative_to(ROOT)).replace("\\", "/"),
            "prior_verification_sha256": source["verification_sha256"],
            "nodes": source["nodes"],
            "edges": source["edges"],
            "roots": receipt["roots"],
            "trusted_leaves": 0,
            "verification_reused_by_hash": True,
        })
    return receipts, {entry["path"]: entry for entry in manifest["files"]}


def _open_candidate_store(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA journal_mode=OFF")
    connection.execute("PRAGMA synchronous=OFF")
    connection.execute("PRAGMA temp_store=FILE")
    connection.execute("PRAGMA cache_size=-65536")
    connection.execute("PRAGMA mmap_size=0")
    connection.executescript("""
        CREATE TABLE nodes (
            mask BLOB PRIMARY KEY,
            ident TEXT NOT NULL UNIQUE,
            stones INTEGER NOT NULL,
            verdict INTEGER NOT NULL,
            terminal INTEGER NOT NULL,
            legal_count INTEGER NOT NULL,
            sequence INTEGER UNIQUE
        ) WITHOUT ROWID;
        CREATE TABLE universal_edges (
            parent BLOB NOT NULL,
            move INTEGER NOT NULL,
            child BLOB NOT NULL,
            PRIMARY KEY(parent,move)
        ) WITHOUT ROWID;
        CREATE TABLE witnesses (
            parent BLOB NOT NULL,
            child BLOB NOT NULL,
            move INTEGER NOT NULL,
            source_order INTEGER NOT NULL,
            source TEXT NOT NULL,
            PRIMARY KEY(parent,child)
        ) WITHOUT ROWID;
        CREATE TABLE roots (
            source TEXT NOT NULL,
            root_id TEXT NOT NULL,
            raw_id TEXT NOT NULL,
            mask BLOB NOT NULL,
            verdict INTEGER NOT NULL,
            source_order INTEGER NOT NULL,
            PRIMARY KEY(source,root_id)
        ) WITHOUT ROWID;
    """)
    return connection


def _import_source(connection: sqlite3.Connection, source: dict,
                   stage_path: Path) -> dict:
    if stage_path.exists():
        stage_path.unlink()
    staged = _open_store(stage_path)
    metadata = load_json_bundle(source["bundle"], staged)
    staged_counts = staged.execute(
        "SELECT COUNT(*),SUM(edge_count) FROM nodes").fetchone()
    if staged_counts != (source["nodes"], source["edges"]):
        raise ValueError(f"streamed input counts changed for {source['name']}")
    if (metadata.get("schema") != SCHEMA
            or metadata.get("board_size") != 11
            or metadata.get("proposition") != PROPOSITION
            or len(metadata["roots_parsed"]) != 3):
        raise ValueError(f"unsupported or unexpected proof source: {source['name']}")

    connection.execute("ATTACH DATABASE ? AS source_db", (str(stage_path),))
    mismatch = connection.execute("""
        SELECT COUNT(*) FROM source_db.nodes s JOIN main.nodes n ON n.mask=s.mask
        WHERE n.ident<>s.ident OR n.stones<>s.stones OR n.verdict<>s.verdict
           OR n.terminal<>s.terminal OR n.legal_count<>s.legal_count
    """).fetchone()[0]
    if mismatch:
        raise ValueError(f"same canonical position has conflicting metadata ({source['name']})")
    connection.execute("""
        INSERT OR IGNORE INTO main.nodes(mask,ident,stones,verdict,terminal,legal_count)
        SELECT mask,ident,stones,verdict,terminal,legal_count FROM source_db.nodes
    """)
    universal_conflicts = connection.execute("""
        SELECT COUNT(*) FROM source_db.edges e
        JOIN source_db.nodes p ON p.mask=e.parent
        JOIN main.universal_edges u ON u.parent=e.parent AND u.move=e.move
        WHERE p.verdict <> CASE WHEN p.stones % 2=0 THEN 1 ELSE 2 END
          AND u.child<>e.child
    """).fetchone()[0]
    if universal_conflicts:
        raise ValueError(f"universal-child conflict while merging {source['name']}")
    connection.execute("""
        INSERT OR IGNORE INTO main.witnesses(parent,child,move,source_order,source)
        SELECT e.parent,e.child,e.move,?,?
        FROM source_db.edges e JOIN source_db.nodes p ON p.mask=e.parent
        WHERE p.verdict = CASE WHEN p.stones % 2=0 THEN 1 ELSE 2 END
    """, (source["source_order"], source["name"]))
    connection.execute("""
        INSERT OR IGNORE INTO main.universal_edges(parent,move,child)
        SELECT e.parent,e.move,e.child
        FROM source_db.edges e JOIN source_db.nodes p ON p.mask=e.parent
        WHERE p.verdict <> CASE WHEN p.stones % 2=0 THEN 1 ELSE 2 END
    """)
    for root in metadata["roots_parsed"]:
        combined_id = f"{source['name']}/{root['id']}"
        connection.execute(
            "INSERT INTO roots VALUES(?,?,?,?,?,?)",
            (source["name"], combined_id, root["id"], _blob(root["mask"]),
             root["verdict"], source["source_order"]))
    connection.commit()
    connection.execute("DETACH DATABASE source_db")
    staged.close()
    stage_path.unlink()
    return {
        "name": source["name"],
        "roots": [{"id": f"{source['name']}/{root['id']}",
                   "raw_id": root["id"], "root": str(root["mask"]),
                   "verdict": root["verdict"]}
                  for root in metadata["roots_parsed"]],
        "nodes": source["nodes"],
        "edges": source["edges"],
    }


def _add_root_witness_candidates(connection: sqlite3.Connection,
                                 roots: list[dict]) -> dict:
    """Find any already-closed same-verdict child in the imported node union."""
    board = Board(11)
    added = 0
    by_root = []
    for root in roots:
        parent = root["mask"]
        parent_blob = _blob(parent)
        row = connection.execute(
            "SELECT stones,verdict FROM nodes WHERE mask=?", (parent_blob,)).fetchone()
        if row is None or row != (5, root["verdict"]):
            raise ValueError("a root is missing or no longer an S5 LOSS")
        legal = board.legal(parent)
        children = {}
        for move in board.points(legal):
            child = board.canonical(parent | (1 << move))
            child_blob = _blob(child)
            candidate = connection.execute(
                "SELECT stones,verdict FROM nodes WHERE mask=?", (child_blob,)).fetchone()
            if candidate == (6, root["verdict"]):
                children[child_blob] = min(move, children.get(child_blob, move))
        before = connection.execute(
            "SELECT COUNT(*) FROM witnesses WHERE parent=?", (parent_blob,)).fetchone()[0]
        for child_blob, move in children.items():
            cursor = connection.execute(
                "INSERT OR IGNORE INTO witnesses VALUES(?,?,?,?,?)",
                (parent_blob, child_blob, move, 100, "closed-union-child"))
            added += cursor.rowcount
        after = connection.execute(
            "SELECT COUNT(*) FROM witnesses WHERE parent=?", (parent_blob,)).fetchone()[0]
        by_root.append({"root_id": root["id"], "root": str(parent),
                        "closed_same_verdict_children": len(children),
                        "new_options_added": after - before})
    connection.commit()
    return {"new_witness_options": added, "roots": by_root}


def _sequence_nodes(connection: sqlite3.Connection) -> int:
    connection.execute("DROP TABLE IF EXISTS temp.node_order")
    connection.execute("""
        CREATE TEMP TABLE node_order(mask BLOB PRIMARY KEY,sequence INTEGER NOT NULL UNIQUE)
        WITHOUT ROWID
    """)
    connection.execute("""
        INSERT INTO node_order(mask,sequence)
        SELECT mask,ROW_NUMBER() OVER (ORDER BY mask)-1 FROM nodes
    """)
    count = connection.execute("SELECT COUNT(*) FROM node_order").fetchone()[0]
    if count > MAX_SEQUENCE:
        raise ValueError("node count exceeds the compact v1 sequence width")
    connection.execute("UPDATE nodes SET sequence=NULL")
    connection.execute("""
        UPDATE nodes SET sequence=(SELECT sequence FROM node_order
                                   WHERE node_order.mask=nodes.mask)
    """)
    connection.commit()
    return count


class DecisionGraph:
    """Compact in-memory adjacency over the disk-interned candidate positions."""

    def __init__(self, connection: sqlite3.Connection, roots: list[dict]):
        self.connection = connection
        self.node_count = _sequence_nodes(connection)
        self.existential = bytearray(self.node_count)
        self.legal_counts = bytearray(self.node_count)
        self.masks = bytearray(16 * self.node_count)
        self.default_child = array("I", [MAX_SEQUENCE]) * self.node_count
        self.default_move = bytearray(self.node_count)
        self.universal_offsets = array("I", [0]) * (self.node_count + 1)
        self.universal_children = array("I")
        self.universal_moves = bytearray()
        cursor = connection.execute(
            "SELECT mask,stones,verdict,terminal,legal_count,sequence FROM nodes ORDER BY sequence")
        for mask_blob, stones, verdict, _terminal, legal_count, sequence in cursor:
            start = sequence * 16
            self.masks[start:start + 16] = mask_blob
            decisive = 2 if stones % 2 else 1
            self.existential[sequence] = int(verdict == decisive)
            self.legal_counts[sequence] = legal_count

        options: dict[int, list[tuple[int, int]]] = {}
        cursor = connection.execute("""
            SELECT p.sequence,w.move,c.sequence,w.source_order
            FROM witnesses w
            JOIN nodes p ON p.mask=w.parent
            JOIN nodes c ON c.mask=w.child
            ORDER BY p.sequence,w.source_order,w.move,c.sequence
        """)
        current_parent = None
        current_choices = []
        for parent, move, child, _order in cursor:
            if current_parent is not None and parent != current_parent:
                if len(current_choices) > 1:
                    options[current_parent] = current_choices
                else:
                    self.default_child[current_parent], self.default_move[current_parent] = current_choices[0]
                current_choices = []
            current_parent = parent
            current_choices.append((child, move))
        if current_parent is not None:
            if len(current_choices) > 1:
                options[current_parent] = current_choices
            else:
                self.default_child[current_parent], self.default_move[current_parent] = current_choices[0]
        self.options = options
        for parent, choices in options.items():
            if not self.existential[parent] or not choices:
                raise ValueError("witness candidate attached to a universal/empty node")
            self.default_child[parent], self.default_move[parent] = choices[0]

        cursor = iter(connection.execute("""
            SELECT p.sequence,e.move,c.sequence
            FROM universal_edges e
            JOIN nodes p ON p.mask=e.parent
            JOIN nodes c ON c.mask=e.child
            ORDER BY p.sequence,e.move
        """))
        edge = next(cursor, None)
        for parent in range(self.node_count):
            self.universal_offsets[parent] = len(self.universal_children)
            if edge is not None and edge[0] < parent:
                raise ValueError("universal edge parent order is inconsistent")
            while edge is not None and edge[0] == parent:
                self.universal_moves.append(edge[1])
                self.universal_children.append(edge[2])
                edge = next(cursor, None)
            if self.existential[parent]:
                if self.default_child[parent] == MAX_SEQUENCE:
                    raise ValueError("existential candidate node has no witness")
            else:
                if len(self.universal_children) - self.universal_offsets[parent] != self.legal_counts[parent]:
                    raise ValueError("input sources omit a universal child")
        self.universal_offsets[self.node_count] = len(self.universal_children)
        if edge is not None:
            raise ValueError("universal edge has no parent in the node index")
        self.roots = []
        for root in roots:
            row = connection.execute("SELECT sequence FROM nodes WHERE mask=?",
                                     (_blob(root["mask"]),)).fetchone()
            if row is None:
                raise ValueError("missing root in candidate index")
            self.roots.append({**root, "sequence": row[0]})

    def mask_blob(self, sequence: int) -> bytes:
        start = sequence * 16
        return bytes(self.masks[start:start + 16])

    def reachable(self, selected_child: array, roots: list[dict]) -> tuple[bytearray, array, int]:
        visited = bytearray(self.node_count)
        queue = array("I")
        for root in roots:
            sequence = root["sequence"]
            if not visited[sequence]:
                visited[sequence] = 1
                queue.append(sequence)
        edge_count = 0
        cursor = 0
        while cursor < len(queue):
            parent = queue[cursor]
            cursor += 1
            if self.existential[parent]:
                child = selected_child[parent]
                if child == MAX_SEQUENCE:
                    raise ValueError("selected existential witness is missing")
                edge_count += 1
                if not visited[child]:
                    visited[child] = 1
                    queue.append(child)
            else:
                for edge_index in range(self.universal_offsets[parent],
                                        self.universal_offsets[parent + 1]):
                    child = self.universal_children[edge_index]
                    edge_count += 1
                    if not visited[child]:
                        visited[child] = 1
                        queue.append(child)
        return visited, queue, edge_count

    def stats(self, selected_child: array, roots: list[dict]) -> dict:
        visited, queue, edges = self.reachable(selected_child, roots)
        return {"nodes": len(queue), "edges": edges,
                "visited": visited, "queue": queue}

    def root_decision_sequences(self, roots: list[dict]) -> list[int]:
        return sorted({root["sequence"] for root in roots
                       if len(self.options.get(root["sequence"], ())) > 1})


def _score(stats: dict) -> tuple[int, int]:
    return stats["nodes"], stats["edges"]


def greedy_add_roots(graph: DecisionGraph, selected_child: array,
                     existing_roots: list[dict], new_roots: list[dict]) -> tuple[dict, list[dict]]:
    accepted = list(existing_roots)
    before = graph.stats(selected_child, accepted) if accepted else {
        "nodes": 0, "edges": 0, "visited": bytearray(graph.node_count), "queue": array("I")}
    steps = []
    for root in new_roots:
        parent = root["sequence"]
        choices = graph.options.get(parent, [])
        best = None
        if len(choices) > 1:
            for child, move in choices:
                selected_child[parent] = child
                selected_stats = graph.stats(selected_child, accepted + [root])
                score = _score(selected_stats)
                candidate = (score, child, move, selected_stats)
                if best is None or candidate[:3] < best[:3]:
                    best = candidate
            selected_child[parent] = best[1]
        accepted.append(root)
        after = graph.stats(selected_child, accepted)
        steps.append({"root_id": root["id"], "roots_after_add": len(accepted),
                      "selected_move": (next((move for child, move in choices
                                              if child == selected_child[parent]), None)),
                      "new_reachable_nodes": after["nodes"] - before["nodes"],
                      "new_reachable_edges": after["edges"] - before["edges"],
                      "reachable_nodes": after["nodes"], "reachable_edges": after["edges"]})
        before = after
    return before, steps


def local_improve(graph: DecisionGraph, selected_child: array, roots: list[dict],
                  *, max_trials: int = 2_000) -> tuple[dict, dict]:
    current = graph.stats(selected_child, roots)
    variable_parents = [parent for parent, choices in graph.options.items()
                        if len(choices) > 1]
    trials = 0
    passes = 0
    improvements = []
    stopped_at_limit = False
    while True:
        best = None
        for parent in variable_parents:
            if not current["visited"][parent]:
                continue
            old = selected_child[parent]
            for child, move in graph.options[parent]:
                if child == old:
                    continue
                if trials >= max_trials:
                    stopped_at_limit = True
                    break
                selected_child[parent] = child
                candidate = graph.stats(selected_child, roots)
                trials += 1
                rank = (_score(candidate), parent, move, child)
                if rank[0] < _score(current) and (best is None or rank < best[0]):
                    best = (rank, parent, child, move, candidate)
                selected_child[parent] = old
            if stopped_at_limit:
                break
        if best is None:
            break
        _, parent, child, move, current = best
        selected_child[parent] = child
        passes += 1
        improvements.append({"parent": str(int.from_bytes(graph.mask_blob(parent), "big")),
                             "move": move, "nodes": current["nodes"],
                             "edges": current["edges"]})
    return current, {"trials": trials, "passes": passes,
                     "stopped_at_trial_limit": stopped_at_limit,
                     "variable_parent_count": len(variable_parents),
                     "improvements": improvements}


def exact_root_choices(graph: DecisionGraph, selected_child: array,
                       roots: list[dict], *, max_combinations: int = 4096) -> tuple[dict, dict]:
    decisions = graph.root_decision_sequences(roots)
    products = [graph.options[parent] for parent in decisions]
    combinations = math.prod(len(options) for options in products) if products else 1
    if combinations > max_combinations:
        return graph.stats(selected_child, roots), {
            "status": "skipped_combination_limit", "root_decision_count": len(decisions),
            "combinations": combinations, "limit": max_combinations,
            "scope": "exact only over root-level witness choices; deeper choices remain fixed"}
    best_stats = None
    best_choice = None
    evaluated = 0
    for choices in itertools.product(*products) if products else [()]:
        for parent, (child, _move) in zip(decisions, choices):
            selected_child[parent] = child
        candidate = graph.stats(selected_child, roots)
        evaluated += 1
        if best_stats is None or _score(candidate) < _score(best_stats):
            best_stats = candidate
            best_choice = tuple(choices)
    for parent, (child, _move) in zip(decisions, best_choice or ()):
        selected_child[parent] = child
    return best_stats or graph.stats(selected_child, roots), {
        "status": "exact_root_choice_optimum", "root_decision_count": len(decisions),
        "combinations": combinations, "evaluated": evaluated,
        "limit": max_combinations,
        "scope": "exact only over root-level witness choices with all deeper choices fixed"}


def _source_roots(connection: sqlite3.Connection, source: str | None = None) -> list[dict]:
    if source is None:
        rows = connection.execute(
            "SELECT root_id,raw_id,mask,verdict,source_order FROM roots ORDER BY source_order,raw_id")
    else:
        rows = connection.execute(
            "SELECT root_id,raw_id,mask,verdict,source_order FROM roots WHERE source=? ORDER BY raw_id",
            (source,))
    return [{"id": row[0], "raw_id": row[1], "mask": int.from_bytes(row[2], "big"),
             "verdict": row[3], "source_order": row[4]} for row in rows]


def _selection_overrides(graph: DecisionGraph, selected: array) -> dict[bytes, tuple[bytes, int]]:
    overrides = {}
    for parent, choices in graph.options.items():
        if len(choices) <= 1 or selected[parent] == graph.default_child[parent]:
            continue
        choice = next((option for option in choices if option[0] == selected[parent]), None)
        if choice is None:
            raise ValueError("optimized witness not in candidate set")
        overrides[graph.mask_blob(parent)] = (graph.mask_blob(choice[0]), choice[1])
    return overrides


def _apply_overrides(graph: DecisionGraph, selected: array,
                     overrides: dict[bytes, tuple[bytes, int]]) -> dict:
    applied = 0
    for parent_blob, (child_blob, move) in overrides.items():
        parent_row = graph.connection.execute("SELECT sequence FROM nodes WHERE mask=?",
                                              (parent_blob,)).fetchone()
        child_row = graph.connection.execute("SELECT sequence FROM nodes WHERE mask=?",
                                             (child_blob,)).fetchone()
        if parent_row is None or child_row is None:
            continue
        parent, child = parent_row[0], child_row[0]
        if not any(option == (child, move) for option in graph.options.get(parent, [])):
            raise ValueError("stage-one optimized witness disappeared during source integration")
        selected[parent] = child
        applied += 1
    return {"overrides": len(overrides), "applied": applied}


def _write_variant(connection: sqlite3.Connection, graph: DecisionGraph,
                   selected: array, roots: list[dict], stats: dict,
                   output: Path, *, raw_root_ids: bool = False) -> dict:
    visited = stats["visited"]
    queue = stats["queue"]
    if output.exists():
        raise FileExistsError(f"refusing to overwrite {output}")
    out = _open_store(output.with_suffix(output.suffix + ".sqlite"))
    count = 0
    cursor = connection.execute(
        "SELECT mask,ident,stones,verdict,terminal,legal_count,sequence FROM nodes ORDER BY sequence")
    for mask_blob, ident, stones, verdict, terminal, legal_count, sequence in cursor:
        if not visited[sequence]:
            continue
        edge_count = (1 if graph.existential[sequence] else legal_count)
        out.execute("""
            INSERT INTO nodes(mask,ident,stones,verdict,terminal,legal_count,edge_count)
            VALUES(?,?,?,?,?,?,?)
        """, (mask_blob, ident, stones, verdict, terminal, legal_count, edge_count))
        count += 1
        if count % 50_000 == 0:
            out.commit()
    out.commit()

    node_edges = 0
    edge_batch = []
    for parent in queue:
        parent_blob = graph.mask_blob(parent)
        if graph.existential[parent]:
            child = selected[parent]
            edge_batch.append((parent_blob, selected_move_for(graph, parent, child),
                               graph.mask_blob(child), None))
            node_edges += 1
        else:
            start, stop = graph.universal_offsets[parent:parent + 2]
            for index in range(start, stop):
                edge_batch.append((parent_blob, graph.universal_moves[index],
                                   graph.mask_blob(graph.universal_children[index]), None))
            node_edges += stop - start
        if len(edge_batch) >= 20_000:
            out.executemany("INSERT INTO edges(parent,move,child,child_sequence) VALUES(?,?,?,?)",
                            edge_batch)
            edge_batch.clear()
            out.commit()
    if edge_batch:
        out.executemany("INSERT INTO edges(parent,move,child,child_sequence) VALUES(?,?,?,?)",
                        edge_batch)
    out.commit()
    metadata_roots = []
    for root in roots:
        root_id = root["raw_id"] if raw_root_ids else root["id"]
        metadata_roots.append({"id": root_id, "mask": root["mask"],
                               "verdict": root["verdict"]})
    metadata = {"schema": SCHEMA, "board_size": 11, "proposition": PROPOSITION,
                "roots_parsed": metadata_roots}
    compact_receipt = write_compact(out, metadata, output)
    out.close()
    output.with_suffix(output.suffix + ".sqlite").unlink(missing_ok=True)
    return {**compact_receipt, "nodes": count, "edges": node_edges,
            "roots": [{"id": root["id"], "root": str(root["mask"]),
                       "verdict": root["verdict"]} for root in roots],
            "certificate_sha256": _digest(output), "certificate_bytes": output.stat().st_size}


def selected_move_for(graph: DecisionGraph, parent: int, child: int) -> int:
    if graph.default_child[parent] == child:
        return graph.default_move[parent]
    for candidate, move in graph.options.get(parent, []):
        if candidate == child:
            return move
    raise ValueError("selected child has no concrete legal move label")


def _reachable_counts(graph: DecisionGraph, selection: array,
                      roots: list[dict]) -> dict:
    stats = graph.stats(selection, roots)
    return {"nodes": stats["nodes"], "edges": stats["edges"],
            "visited": stats["visited"], "queue": stats["queue"]}


def _stage_metadata(connection: sqlite3.Connection, graph: DecisionGraph,
                    source_receipts: list[dict], source_imports: list[dict],
                    outputs: dict, algorithms: dict,
                    verifier_receipts: dict | None = None) -> dict:
    node_union = connection.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    universal_count = connection.execute("SELECT COUNT(*) FROM universal_edges").fetchone()[0]
    witness_count = connection.execute("SELECT COUNT(*) FROM witnesses").fetchone()[0]
    variable_count = connection.execute("""
        SELECT COUNT(*) FROM (
            SELECT parent FROM witnesses GROUP BY parent HAVING COUNT(*)>1
        )
    """).fetchone()[0]
    roots = _source_roots(connection)
    return {
        "schema": "n11-incremental-proof-integration-plan-v1",
        "board_size": 11,
        "proposition": PROPOSITION,
        "source_verification": source_receipts,
        "source_imports": source_imports,
        "source_bundle_node_sum": sum(item["nodes"] for item in source_imports),
        "interned_candidate_nodes": node_union,
        "duplicate_positions_shared_on_import": sum(item["nodes"] for item in source_imports) - node_union,
        "universal_dependency_edges_in_candidate_union": universal_count,
        "source_witness_edges_in_candidate_union": witness_count,
        "existential_nodes_with_multiple_witness_options": variable_count,
        "root_count": len(roots),
        "root_masks": [{"id": root["id"], "root": str(root["mask"]),
                        "verdict": root["verdict"]} for root in roots],
        "root_child_candidates": outputs.get("root_child_candidates"),
        "variants": outputs,
        "optimization_methods": algorithms,
        "verifier_receipts": verifier_receipts or {},
        "trusted_leaves": 0,
        "solver_or_cache_evidence_imported": False,
        "search_or_probe_launched": False,
    }


def run(output_dir: Path, *, max_local_trials: int = 2_000,
        max_exact_combinations: int = 4_096) -> dict:
    source_receipts, _ = preflight_sources()
    if output_dir.exists():
        raise FileExistsError(f"refusing to overwrite output directory {output_dir}")
    output_dir.mkdir(parents=True)
    started = time.perf_counter()
    report: dict = {"schema": "n11-incremental-proof-integration-run-v1",
                    "sources": source_receipts, "stages": {},
                    "search_or_probe_launched": False,
                    "solver_or_cache_evidence_imported": False}

    with tempfile.TemporaryDirectory(prefix="n11-proof-incremental-", dir=output_dir) as temp:
        temp_path = Path(temp)
        connection = _open_candidate_store(temp_path / "candidates.sqlite")
        current = SOURCES[0]
        print(json.dumps({"event": "import_start", "source": current["name"]}),
              file=sys.stderr, flush=True)
        current_import_started = time.perf_counter()
        current_import = _import_source(connection, current, temp_path / "stage-current.sqlite")
        current_import_seconds = round(time.perf_counter() - current_import_started, 3)
        print(json.dumps({"event": "import_complete", "source": current["name"],
                          "candidate_nodes": connection.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]}),
              file=sys.stderr, flush=True)
        _add_root_witness_candidates(connection, _source_roots(connection, current["name"]))
        roots_current = _source_roots(connection, current["name"])
        graph_current = DecisionGraph(connection, roots_current)
        selection_current = array("I", graph_current.default_child)

        started_greedy = time.perf_counter()
        greedy_current, greedy_steps_current = greedy_add_roots(
            graph_current, selection_current, [], graph_current.roots)
        local_current, local_current_report = local_improve(
            graph_current, selection_current, graph_current.roots,
            max_trials=max_local_trials)
        exact_current, exact_current_report = exact_root_choices(
            graph_current, selection_current, graph_current.roots,
            max_combinations=max_exact_combinations)
        if _score(exact_current) < _score(local_current):
            local_current = exact_current
            local_current_report["exact_root_choice_applied"] = True
        else:
            local_current_report["exact_root_choice_applied"] = False
        selected_current = array("I", selection_current)
        stage_three_output = output_dir / "three-root-start.kpd.gz"
        stage_three_receipt = _write_variant(
            connection, graph_current, selected_current, graph_current.roots,
            local_current, stage_three_output, raw_root_ids=True)
        source_overrides = _selection_overrides(graph_current, selected_current)
        report["stages"]["three_root_start"] = {
            "source": current_import,
            "source_import_seconds": current_import_seconds,
            "input_nodes": current["nodes"], "input_edges": current["edges"],
            "input_certificate_bytes": current["bundle"].stat().st_size,
            "greedy_reachable_nodes": greedy_current["nodes"],
            "greedy_reachable_edges": greedy_current["edges"],
            "greedy_root_steps": greedy_steps_current,
            "local_reachable_nodes": local_current["nodes"],
            "local_reachable_edges": local_current["edges"],
            "local_search": local_current_report,
            "exact_root_search": exact_current_report,
            "optimized_certificate": stage_three_receipt,
            "prior_k0377_optimized_nodes": 1_718_259,
            "prior_k0377_optimized_edges": 2_547_576,
            "prior_k0377_optimized_bytes": 16_080_927,
            "prior_k0377_optimized_sha256": "478fc29e51ffd7e18158f74f0032b7e7756446e11c5d0819b000e19e79474fc2",
            "matches_k0377_size_and_edges": (
                stage_three_receipt["nodes"] == 1_718_259
                and stage_three_receipt["edges"] == 2_547_576),
            "optimization_seconds": round(time.perf_counter() - started_greedy, 3),
        }

        previous = SOURCES[1]
        six_root_started = time.perf_counter()
        print(json.dumps({"event": "import_start", "source": previous["name"]}),
              file=sys.stderr, flush=True)
        previous_import_started = time.perf_counter()
        previous_import = _import_source(
            connection, previous, temp_path / "stage-previous.sqlite")
        previous_import_seconds = round(time.perf_counter() - previous_import_started, 3)
        print(json.dumps({"event": "import_complete", "source": previous["name"],
                          "candidate_nodes": connection.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]}),
              file=sys.stderr, flush=True)
        root_candidates = _add_root_witness_candidates(
            connection, _source_roots(connection))
        graph = DecisionGraph(connection, _source_roots(connection))
        roots_all = graph.roots
        roots_existing = [root for root in roots_all if root["source_order"] == current["source_order"]]
        roots_new = [root for root in roots_all if root["source_order"] == previous["source_order"]]
        default_selection = array("I", graph.default_child)
        base_with_prior = array("I", default_selection)
        override_audit = _apply_overrides(graph, base_with_prior, source_overrides)
        existing_stats = _reachable_counts(graph, base_with_prior, roots_existing)

        unoptimized_stats = _reachable_counts(graph, default_selection, roots_all)
        incremental_stats = _reachable_counts(graph, base_with_prior, roots_all)

        greedy_selection = array("I", base_with_prior)
        greedy_stats, incremental_steps = greedy_add_roots(
            graph, greedy_selection, roots_existing, roots_new)
        local_stats, local_search = local_improve(
            graph, greedy_selection, roots_all, max_trials=max_local_trials)
        exact_stats, exact_search = exact_root_choices(
            graph, greedy_selection, roots_all,
            max_combinations=max_exact_combinations)
        if _score(exact_stats) < _score(local_stats):
            local_stats = exact_stats
            local_search["exact_root_choice_applied"] = True
        else:
            local_search["exact_root_choice_applied"] = False

        baseline_path = output_dir / "six-root-incremental.kpd.gz"
        baseline_receipt = _write_variant(
            connection, graph, base_with_prior, roots_all,
            incremental_stats, baseline_path)
        optimized_path = output_dir / "six-root-joint-optimized.kpd.gz"
        optimized_receipt = _write_variant(
            connection, graph, greedy_selection, roots_all,
            local_stats, optimized_path)

        input_nodes_sum = current["nodes"] + previous["nodes"]
        interned_nodes = connection.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
        report["stages"]["six_root_increment"] = {
            "added_source": previous_import,
            "previous_source_import_seconds": previous_import_seconds,
            "source_node_sum_without_interning": input_nodes_sum,
            "interned_candidate_nodes": interned_nodes,
            "duplicate_positions_shared": input_nodes_sum - interned_nodes,
            "base_three_root_nodes_preserved": existing_stats["nodes"],
            "base_three_root_edges_preserved": existing_stats["edges"],
            "stage_one_witness_overrides_reused": override_audit,
            "input_order_union": {"nodes": unoptimized_stats["nodes"],
                                  "edges": unoptimized_stats["edges"]},
            "incremental_before_joint_optimization": {
                "nodes": incremental_stats["nodes"], "edges": incremental_stats["edges"]},
            "greedy_root_add": {"nodes": greedy_stats["nodes"],
                                "edges": greedy_stats["edges"],
                                "root_steps": incremental_steps},
            "local_improvement": {"nodes": local_stats["nodes"],
                                  "edges": local_stats["edges"],
                                  **local_search},
            "exact_root_choice": {"nodes": exact_stats["nodes"],
                                  "edges": exact_stats["edges"], **exact_search},
            "root_child_candidates": root_candidates,
            "incremental_certificate": baseline_receipt,
            "jointly_optimized_certificate": optimized_receipt,
            "six_root_stage_seconds": round(time.perf_counter() - six_root_started, 3),
            "node_reduction_vs_incremental": incremental_stats["nodes"] - local_stats["nodes"],
            "edge_reduction_vs_incremental": incremental_stats["edges"] - local_stats["edges"],
        }
        report["elapsed_optimizer_seconds"] = round(time.perf_counter() - started, 3)
        report["final_root_count"] = len(roots_all)
        report["final_root_masks"] = [{"id": root["id"], "root": str(root["mask"]),
                                       "verdict": root["verdict"]}
                                      for root in roots_all]
        report["trusted_leaves"] = 0
        connection.close()

    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="new local directory for compact variants; must not exist")
    parser.add_argument("--max-local-trials", type=int, default=100)
    parser.add_argument("--max-exact-combinations", type=int, default=4_096)
    parser.add_argument("--receipt", type=Path,
                        help="write a small plan receipt; existing files are refused")
    args = parser.parse_args()
    if args.max_local_trials < 0 or args.max_exact_combinations < 1:
        parser.error("optimization limits must be positive")
    report = run(args.output_dir.resolve(), max_local_trials=args.max_local_trials,
                 max_exact_combinations=args.max_exact_combinations)
    payload = json.dumps(report, sort_keys=True, separators=(",", ":")) + "\n"
    if args.receipt is not None:
        if args.receipt.exists():
            parser.error(f"refusing to overwrite {args.receipt}")
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(payload, encoding="utf-8")
    print(payload.rstrip(), flush=True)


if __name__ == "__main__":
    main()
