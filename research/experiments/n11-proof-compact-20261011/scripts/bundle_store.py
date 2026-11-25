"""Disk-backed independent verifier and compact codec for shared proof bundles.

The JSON reader materializes one node at a time and keeps the proof graph in a
temporary SQLite index.  The compact format is a deterministic, checksummed
binary encoding of the same roots, canonical positions, verdicts, legal-move
counts, terminal markers, and move-labelled child dependencies.
"""
from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import os
from pathlib import Path
import sqlite3
import sys
import tempfile
import time
from typing import BinaryIO, TextIO

ROOT = Path(__file__).resolve().parents[4]
INDEPENDENT = ROOT / "research/experiments/n11-independent-exact-audit-20261010/scripts"
sys.path.insert(0, str(INDEPENDENT))
from independent import Board, aggregate  # noqa: E402

SCHEMA = "kyouen-proof-dag-multi-root-v1"
PROPOSITION = "original_first_player_wins"
MAGIC = b"KYPRFDG\x01"
CHECKSUM_SIZE = 32
MAX_MASK_BITS = 121
HASH_CHUNK = 64 * 1024


def _blob(mask: int) -> bytes:
    if type(mask) is not int or mask < 0 or mask >= 1 << MAX_MASK_BITS:
        raise ValueError("position mask is outside the supported 121-cell board")
    return mask.to_bytes(16, "big")


def _mask(blob: bytes) -> int:
    return int.from_bytes(blob, "big")


def _parse_mask(value) -> int:
    try:
        mask = int(value)
    except (TypeError, ValueError, OverflowError) as exc:
        raise ValueError("malformed position mask") from exc
    if mask < 0 or mask >= 1 << MAX_MASK_BITS:
        raise ValueError("position mask is outside the supported 121-cell board")
    return mask


def _open_text(path: Path) -> TextIO:
    if path.suffix == ".gz":
        return gzip.open(path, "rt", encoding="utf-8", newline="")
    return path.open("rt", encoding="utf-8", newline="")


class _JsonStream:
    """Incremental JSON decoder for a top-level object with a large `nodes` map."""

    def __init__(self, stream: TextIO):
        self.stream = stream
        self.decoder = json.JSONDecoder()
        self.buffer = ""
        self.pos = 0
        self.eof = False

    def _fill(self) -> bool:
        if self.pos:
            self.buffer = self.buffer[self.pos:]
            self.pos = 0
        chunk = self.stream.read(128 * 1024)
        if not chunk:
            self.eof = True
            return False
        self.buffer += chunk
        return True

    def _space(self) -> None:
        while True:
            while self.pos < len(self.buffer) and self.buffer[self.pos] in " \t\r\n":
                self.pos += 1
            if self.pos < len(self.buffer) or self.eof or not self._fill():
                return

    def peek(self) -> str | None:
        self._space()
        return self.buffer[self.pos] if self.pos < len(self.buffer) else None

    def expect(self, expected: str) -> None:
        actual = self.peek()
        if actual != expected:
            raise ValueError(f"malformed JSON bundle: expected {expected!r}")
        self.pos += 1

    def value(self):
        while True:
            self._space()
            if self.pos >= len(self.buffer):
                raise ValueError("unexpected end of JSON bundle")
            try:
                value, end = self.decoder.raw_decode(self.buffer, self.pos)
            except json.JSONDecodeError as exc:
                if self.eof or not self._fill():
                    raise ValueError("malformed or truncated JSON bundle") from exc
                continue
            self.pos = end
            return value

    def finish(self) -> None:
        if self.peek() is not None:
            raise ValueError("trailing data after JSON bundle")


def _open_store(path: Path) -> sqlite3.Connection:
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA journal_mode=OFF")
    connection.execute("PRAGMA synchronous=OFF")
    connection.execute("PRAGMA temp_store=FILE")
    connection.execute("PRAGMA cache_size=-65536")
    connection.execute("PRAGMA mmap_size=0")
    connection.execute("""
        CREATE TABLE nodes (
            mask BLOB PRIMARY KEY,
            ident TEXT NOT NULL UNIQUE,
            stones INTEGER NOT NULL,
            verdict INTEGER NOT NULL,
            terminal INTEGER NOT NULL,
            legal_count INTEGER NOT NULL,
            edge_count INTEGER NOT NULL,
            sequence INTEGER UNIQUE
        ) WITHOUT ROWID
    """)
    connection.execute("""
        CREATE TABLE edges (
            parent BLOB NOT NULL,
            move INTEGER NOT NULL,
            child BLOB,
            child_sequence INTEGER,
            PRIMARY KEY (parent, move)
        ) WITHOUT ROWID
    """)
    return connection


def _insert_json_node(connection: sqlite3.Connection, ident, node) -> int:
    if not isinstance(ident, str) or not isinstance(node, dict):
        raise ValueError("malformed proof node")
    try:
        mask = _parse_mask(node["mask"])
        verdict = node["verdict"]
        stones = node["stones"]
        terminal = node["terminal"]
        legal_count = node["legal_count"]
        edges = node["edges"]
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError("malformed proof node") from exc
    if ident != str(mask) or type(verdict) is not int or verdict not in (1, 2):
        raise ValueError("noncanonical identifier or invalid verdict")
    if type(stones) is not int or stones != mask.bit_count():
        raise ValueError("wrong stone count")
    if type(terminal) is not bool or not isinstance(edges, list):
        raise ValueError("malformed terminal/edge fields")
    if type(legal_count) is not int:
        raise ValueError("missing or malformed legal move count")
    if node.get("trusted") or node.get("trusted_leaf"):
        raise ValueError("trusted leaves are forbidden")
    try:
        connection.execute(
            "INSERT INTO nodes(mask,ident,stones,verdict,terminal,legal_count,edge_count) "
            "VALUES(?,?,?,?,?,?,?)",
            (_blob(mask), ident, stones, verdict, int(terminal), legal_count, len(edges)))
    except sqlite3.IntegrityError as exc:
        raise ValueError("duplicate proof node") from exc

    edge_rows = []
    for edge in edges:
        if not isinstance(edge, dict) or set(edge) != {"move", "child"}:
            raise ValueError("malformed edge")
        move, child_id = edge["move"], edge["child"]
        if type(move) is not int or not isinstance(child_id, str):
            raise ValueError("illegal move label or child reference")
        child_mask = _parse_mask(child_id)
        if child_id != str(child_mask):
            raise ValueError("noncanonical child identifier")
        edge_rows.append((_blob(mask), move, _blob(child_mask), None))
    try:
        connection.executemany(
            "INSERT INTO edges(parent,move,child,child_sequence) VALUES(?,?,?,?)",
            edge_rows)
    except sqlite3.IntegrityError as exc:
        raise ValueError("duplicate move label") from exc
    return len(edge_rows)


def load_json_bundle(path: Path, connection: sqlite3.Connection) -> dict:
    """Read a bundle incrementally; only one proof-node object is held at once."""
    metadata = {}
    nodes_seen = False
    edge_total = 0
    with _open_text(path) as stream:
        reader = _JsonStream(stream)
        reader.expect("{")
        first = True
        while reader.peek() != "}":
            if not first:
                reader.expect(",")
            first = False
            key = reader.value()
            if not isinstance(key, str) or key in metadata or (key == "nodes" and nodes_seen):
                raise ValueError("duplicate or malformed top-level field")
            reader.expect(":")
            if key == "nodes":
                reader.expect("{")
                nodes_seen = True
                first_node = True
                while reader.peek() != "}":
                    if not first_node:
                        reader.expect(",")
                    first_node = False
                    ident = reader.value()
                    reader.expect(":")
                    node = reader.value()
                    edge_total += _insert_json_node(connection, ident, node)
                    if edge_total and edge_total % 100_000 < len(node.get("edges", ())):
                        connection.commit()
                reader.expect("}")
            else:
                metadata[key] = reader.value()
        reader.expect("}")
        reader.finish()
    connection.commit()
    if not nodes_seen:
        raise ValueError("missing proof nodes")
    if "trusted" in metadata or "trusted_leaves" in metadata:
        raise ValueError("trusted leaves are forbidden")
    if not isinstance(metadata.get("roots"), list):
        raise ValueError("empty or malformed proof roots")
    roots = []
    seen_ids = set()
    for root in metadata["roots"]:
        if not isinstance(root, dict):
            raise ValueError("malformed proof root")
        try:
            root_id, ident, verdict = root["id"], root["root"], root["verdict"]
        except KeyError as exc:
            raise ValueError("malformed proof root") from exc
        if not isinstance(root_id, str) or root_id in seen_ids:
            raise ValueError("duplicate or malformed proof root id")
        if not isinstance(ident, str) or type(verdict) is not int or verdict not in (1, 2):
            raise ValueError("missing root or invalid root verdict")
        mask = _parse_mask(ident)
        if ident != str(mask):
            raise ValueError("noncanonical root identifier")
        seen_ids.add(root_id)
        roots.append({"id": root_id, "mask": mask, "verdict": verdict})
    metadata["roots_parsed"] = roots
    metadata["edge_count_parsed"] = edge_total
    return metadata


def _counts(connection: sqlite3.Connection) -> tuple[int, int]:
    nodes = connection.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    edges = connection.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    return nodes, edges


def verify_store(metadata: dict, connection: sqlite3.Connection,
                 progress=None, cache_clear_interval: int = 50_000) -> dict:
    """Verify all local proof rules and root reachability using bounded memory."""
    if metadata.get("schema") != SCHEMA:
        raise ValueError("unsupported shared proof bundle schema")
    n = metadata.get("board_size")
    if type(n) is not int or not 1 <= n <= 11:
        raise ValueError("invalid board size")
    if metadata.get("proposition") != PROPOSITION:
        raise ValueError("unsupported proposition")
    if not metadata.get("roots_parsed"):
        raise ValueError("empty proof bundle")
    node_count, edge_count = _counts(connection)
    if not node_count:
        raise ValueError("empty proof bundle")
    board = Board(n)
    node_cursor = connection.execute(
        "SELECT mask,ident,stones,verdict,terminal,legal_count,edge_count "
        "FROM nodes ORDER BY mask")
    edge_cursor = iter(connection.execute(
        "SELECT e.parent,e.move,e.child,c.stones,c.verdict "
        "FROM edges e LEFT JOIN nodes c ON c.mask=e.child "
        "ORDER BY e.parent,e.move"))
    edge = next(edge_cursor, None)
    terminal_count = 0
    for index, row in enumerate(node_cursor, 1):
        node_blob, ident, stones, verdict, terminal_int, legal_count, _stored_count = row
        if index % cache_clear_interval == 1:
            Board.legal.cache_clear()
            Board.canonical.cache_clear()
        mask = _mask(node_blob)
        if ident != str(mask) or type(verdict) is not int or verdict not in (1, 2):
            raise ValueError("noncanonical identifier or invalid verdict")
        if type(stones) is not int or stones != mask.bit_count():
            raise ValueError("wrong stone count")
        if terminal_int not in (0, 1) or type(legal_count) is not int:
            raise ValueError("malformed terminal/edge fields")
        try:
            legal = board.legal(mask)
        except (TypeError, ValueError) as exc:
            raise ValueError("unsafe or out-of-board position") from exc
        if board.canonical(mask) != mask:
            raise ValueError("position is not D4-canonical")
        if legal.bit_count() != legal_count:
            raise ValueError("wrong legal move count")
        is_terminal = legal == 0
        if bool(terminal_int) != is_terminal:
            raise ValueError("terminal marker disagrees with geometry")

        while edge is not None and edge[0] < node_blob:
            raise ValueError("edge appears without a node")
        node_edges = []
        while edge is not None and edge[0] == node_blob:
            node_edges.append(edge[1:])
            edge = next(edge_cursor, None)
        if len(node_edges) != _stored_count:
            raise ValueError("malformed proof node edge count")

        if is_terminal:
            terminal_count += 1
            if node_edges or aggregate(stones, ()) != verdict:
                raise ValueError("incorrect terminal verdict")
        else:
            decisive = 2 if stones % 2 else 1
            existential = verdict == decisive
            child_values = []
            previous_move = -1
            for move, child_blob, child_stones, child_verdict in node_edges:
                if (type(move) is not int or move <= previous_move
                        or not (legal >> move & 1)):
                    raise ValueError("illegal move label or child reference")
                previous_move = move
                if child_blob is None or child_stones is None:
                    raise ValueError("edge references a missing child")
                child_mask = _mask(child_blob)
                if (child_mask != board.canonical(mask | (1 << move))
                        or child_stones != stones + 1):
                    raise ValueError("edge has a nonlegal or incorrectly ranked transition")
                child_values.append(child_verdict)
            if existential:
                if len(node_edges) != 1 or child_values != [verdict]:
                    raise ValueError("existential node lacks one decisive witness")
            elif (len(node_edges) != legal_count
                  or aggregate(stones, child_values) != verdict):
                raise ValueError("universal node omits or duplicates a legal move or has an incorrect fixed-player verdict")
        if progress and index % 100_000 == 0:
            progress(index, node_count, edge_count)
    if edge is not None:
        raise ValueError("edge appears without a node")

    root_receipts = []
    root_masks = []
    for root in metadata["roots_parsed"]:
        value = connection.execute(
            "SELECT verdict FROM nodes WHERE mask=?", (_blob(root["mask"]),)).fetchone()
        if value is None or value[0] != root["verdict"]:
            raise ValueError("root verdict disagrees with its proof")
        root_receipts.append({"id": root["id"], "root": str(root["mask"]),
                              "verdict": root["verdict"]})
        root_masks.append(_blob(root["mask"]))

    connection.execute("CREATE TEMP TABLE reachable(mask BLOB PRIMARY KEY) WITHOUT ROWID")
    connection.execute("CREATE TEMP TABLE frontier(mask BLOB PRIMARY KEY) WITHOUT ROWID")
    connection.execute("CREATE TEMP TABLE next_frontier(mask BLOB PRIMARY KEY) WITHOUT ROWID")
    connection.executemany("INSERT OR IGNORE INTO frontier(mask) VALUES(?)",
                           ((mask,) for mask in root_masks))
    connection.execute("INSERT OR IGNORE INTO reachable SELECT mask FROM frontier")
    while connection.execute("SELECT 1 FROM frontier LIMIT 1").fetchone():
        connection.execute("DELETE FROM next_frontier")
        connection.execute("""
            INSERT OR IGNORE INTO next_frontier(mask)
            SELECT e.child FROM edges e JOIN frontier f ON f.mask=e.parent
            WHERE NOT EXISTS (SELECT 1 FROM reachable r WHERE r.mask=e.child)
        """)
        if not connection.execute("SELECT 1 FROM next_frontier LIMIT 1").fetchone():
            break
        connection.execute("INSERT OR IGNORE INTO reachable SELECT mask FROM next_frontier")
        connection.execute("DELETE FROM frontier")
        connection.execute("INSERT INTO frontier SELECT mask FROM next_frontier")
    reachable_count = connection.execute("SELECT COUNT(*) FROM reachable").fetchone()[0]
    if reachable_count != node_count:
        raise ValueError("proof bundle contains nodes unreachable from every root")
    return {"roots": root_receipts, "nodes": node_count, "edges": edge_count,
            "terminal_nodes": terminal_count, "trusted_leaves": 0}


class _BinaryWriter:
    def __init__(self, stream: BinaryIO):
        self.stream = stream
        self.digest = hashlib.sha256()
        self.buffer = bytearray()

    def write(self, data: bytes) -> None:
        self.buffer.extend(data)
        if len(self.buffer) >= 1024 * 1024:
            self._flush()

    def byte(self, value: int) -> None:
        if not 0 <= value <= 255:
            raise ValueError("binary byte is out of range")
        self.buffer.append(value)
        if len(self.buffer) >= 1024 * 1024:
            self._flush()

    def varint(self, value: int) -> None:
        if type(value) is not int or value < 0:
            raise ValueError("binary integer must be nonnegative")
        while value >= 0x80:
            self.byte((value & 0x7F) | 0x80)
            value >>= 7
        self.byte(value)

    def string(self, value: str) -> None:
        data = value.encode("utf-8")
        self.varint(len(data))
        self.write(data)

    def _flush(self) -> None:
        if self.buffer:
            self.stream.write(self.buffer)
            self.digest.update(self.buffer)
            self.buffer.clear()

    def finish(self) -> None:
        self._flush()
        self.stream.write(self.digest.digest())


class _BinaryReader:
    def __init__(self, stream: BinaryIO):
        self.stream = stream
        self.digest = hashlib.sha256()
        self.buffer = bytearray()
        self.pos = 0

    def _commit(self) -> None:
        if self.pos:
            self.digest.update(memoryview(self.buffer)[:self.pos])
            del self.buffer[:self.pos]
            self.pos = 0

    def _fill(self) -> None:
        self._commit()
        block = self.stream.read(128 * 1024)
        if not block:
            raise ValueError("truncated compact proof bundle")
        self.buffer.extend(block)

    def byte(self) -> int:
        if self.pos >= len(self.buffer):
            self._fill()
        value = self.buffer[self.pos]
        self.pos += 1
        if self.pos >= HASH_CHUNK:
            self._commit()
        return value

    def exact(self, size: int, *, hash_data: bool = True) -> bytes:
        if size < 0:
            raise ValueError("negative binary read length")
        if not hash_data:
            self._commit()
        out = bytearray()
        remaining = size
        while remaining:
            if self.pos >= len(self.buffer):
                if not hash_data:
                    block = self.stream.read(max(128 * 1024, remaining))
                    if not block:
                        raise ValueError("truncated compact proof bundle")
                    self.buffer.extend(block)
                else:
                    self._fill()
            take = min(remaining, len(self.buffer) - self.pos)
            out.extend(memoryview(self.buffer)[self.pos:self.pos + take])
            self.pos += take
            remaining -= take
            if hash_data and self.pos >= HASH_CHUNK:
                self._commit()
        return bytes(out)

    def varint(self) -> int:
        value = 0
        shift = 0
        count = 0
        while True:
            item = self.byte()
            count += 1
            if count > 19:
                raise ValueError("oversized compact integer")
            value |= (item & 0x7F) << shift
            if item < 0x80:
                if count > 1 and item == 0:
                    raise ValueError("noncanonical compact integer")
                return value
            shift += 7

    def string(self) -> str:
        size = self.varint()
        if size > 1_000_000:
            raise ValueError("oversized compact root id")
        try:
            return self.exact(size).decode("utf-8")
        except UnicodeDecodeError as exc:
            raise ValueError("invalid compact root id") from exc

    def check_trailer(self) -> None:
        self._commit()
        expected = self.digest.digest()
        actual = self.exact(CHECKSUM_SIZE, hash_data=False)
        if actual != expected:
            raise ValueError("compact proof checksum mismatch")
        if self.pos < len(self.buffer) or self.stream.read(1):
            raise ValueError("trailing data after compact proof checksum")


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def _file_size(path: Path) -> int:
    return path.stat().st_size if path.exists() else 0


def _reuse_verification_receipt(path: Path, source: Path,
                                metadata: dict, connection: sqlite3.Connection) -> dict:
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        verified = receipt["verifier_receipt"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("malformed prior verification receipt") from exc
    if not isinstance(receipt, dict) or not isinstance(verified, dict):
        raise ValueError("malformed prior verification receipt")
    if receipt.get("returncode") != 0:
        raise ValueError("prior verification did not complete successfully")
    if receipt.get("format") != "json" or verified.get("format") != "json":
        raise ValueError("prior receipt does not certify a JSON bundle")
    if verified.get("input_sha256") != _file_sha256(source):
        raise ValueError("prior JSON verification receipt has a different source SHA-256")
    if verified.get("trusted_leaves") != 0:
        raise ValueError("prior JSON verification receipt includes trusted leaves")
    nodes, edges = _counts(connection)
    if verified.get("nodes") != nodes or verified.get("edges") != edges:
        raise ValueError("prior verification receipt counts disagree with the parsed source")
    roots = [{"id": root["id"], "root": str(root["mask"]),
              "verdict": root["verdict"]} for root in metadata["roots_parsed"]]
    if verified.get("roots") != roots:
        raise ValueError("prior verification receipt roots disagree with the parsed source")
    return verified


def _reuse_compact_verification_receipt(path: Path, source: Path,
                                       metadata: dict,
                                       connection: sqlite3.Connection) -> dict:
    try:
        receipt = json.loads(path.read_text(encoding="utf-8"))
        verified = receipt["verifier_receipt"]
    except (OSError, KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("malformed prior compact verification receipt") from exc
    if not isinstance(receipt, dict) or not isinstance(verified, dict):
        raise ValueError("malformed prior compact verification receipt")
    if receipt.get("returncode") != 0:
        raise ValueError("prior compact verification did not complete successfully")
    if receipt.get("format") != "compact" or verified.get("format") != "kyprfdg-v1":
        raise ValueError("prior receipt does not certify a compact bundle")
    if verified.get("input_sha256") != _file_sha256(source):
        raise ValueError("prior compact verification receipt has a different source SHA-256")
    if verified.get("trusted_leaves") != 0:
        raise ValueError("prior compact verification receipt includes trusted leaves")
    nodes, edges = _counts(connection)
    if verified.get("nodes") != nodes or verified.get("edges") != edges:
        raise ValueError("prior compact receipt counts disagree with the parsed source")
    roots = [{"id": root["id"], "root": str(root["mask"]),
              "verdict": root["verdict"]} for root in metadata["roots_parsed"]]
    if verified.get("roots") != roots:
        raise ValueError("prior compact receipt roots disagree with the parsed source")
    return verified


def apply_witness_switch_and_prune(connection: sqlite3.Connection, metadata: dict,
                                   root_id: str, new_move: int) -> dict:
    """Replace one verified existential witness and drop unreachable proof nodes."""
    roots_by_id = {root["id"]: root for root in metadata["roots_parsed"]}
    root = roots_by_id.get(root_id)
    if root is None:
        raise ValueError("unknown proof root id for witness switch")
    parent = root["mask"]
    stones = parent.bit_count()
    decisive = 2 if stones % 2 else 1
    if root["verdict"] != decisive:
        raise ValueError("witness switching requires an existential root")
    old_rows = connection.execute(
        "SELECT move,child FROM edges WHERE parent=? ORDER BY move", (_blob(parent),)).fetchall()
    if len(old_rows) != 1:
        raise ValueError("witness switching requires exactly one selected root edge")
    old_move, old_child_blob = old_rows[0]
    if type(new_move) is not int or new_move == old_move:
        raise ValueError("replacement move must differ from the selected witness")
    board = Board(metadata["board_size"])
    legal = board.legal(parent)
    if not (legal >> new_move & 1):
        raise ValueError("replacement witness move is illegal")
    new_child = board.canonical(parent | (1 << new_move))
    child_row = connection.execute(
        "SELECT stones,verdict FROM nodes WHERE mask=?", (_blob(new_child),)).fetchone()
    if child_row != (stones + 1, root["verdict"]):
        raise ValueError("replacement child is not a closed proof of the root's winning polarity")
    before_nodes, before_edges = _counts(connection)
    root_masks = [item["mask"] for item in metadata["roots_parsed"]]
    reachable_nodes, reachable_edges = _witness_switch_counts(
        connection, root_masks, parent, old_move, new_move, new_child, restore=False)
    connection.execute("DELETE FROM edges WHERE parent NOT IN (SELECT mask FROM switch_seen)")
    connection.execute("DELETE FROM nodes WHERE mask NOT IN (SELECT mask FROM switch_seen)")
    connection.commit()
    after_nodes, after_edges = _counts(connection)
    if (after_nodes, after_edges) != (reachable_nodes, reachable_edges):
        raise ValueError("pruned witness-switch graph disagrees with its reachable set")
    return {
        "root_id": root_id,
        "parent": str(parent),
        "selected_move": old_move,
        "selected_child": str(_mask(old_child_blob)),
        "replacement_move": new_move,
        "replacement_child": str(new_child),
        "nodes_before": before_nodes,
        "edges_before": before_edges,
        "nodes_after": after_nodes,
        "edges_after": after_edges,
        "removed_nodes": before_nodes - after_nodes,
        "removed_edges": before_edges - after_edges,
        "all_roots_retained": all(
            connection.execute("SELECT 1 FROM nodes WHERE mask=?", (_blob(mask),)).fetchone()
            is not None for mask in root_masks),
        "evidence_scope": "replacement child already existed as a fully verified closed node in the exact input certificate; no solver/cache evidence imported",
    }


def _index_sequence(connection: sqlite3.Connection) -> int:
    connection.execute("DROP TABLE IF EXISTS temp.node_order")
    connection.execute("DROP TABLE IF EXISTS temp.ordered_edges")
    connection.execute("""
        CREATE TEMP TABLE node_order (
            mask BLOB PRIMARY KEY,
            sequence INTEGER NOT NULL UNIQUE
        ) WITHOUT ROWID
    """)
    connection.execute("""
        INSERT INTO node_order(mask,sequence)
        SELECT mask, ROW_NUMBER() OVER (ORDER BY mask) - 1 FROM nodes
    """)
    connection.execute("UPDATE nodes SET sequence=(SELECT sequence FROM node_order WHERE node_order.mask=nodes.mask)")
    connection.execute("""
        CREATE TEMP TABLE ordered_edges (
            parent_sequence INTEGER NOT NULL,
            move INTEGER NOT NULL,
            child_sequence INTEGER NOT NULL,
            PRIMARY KEY(parent_sequence,move)
        ) WITHOUT ROWID
    """)
    connection.execute("""
        INSERT INTO ordered_edges(parent_sequence,move,child_sequence)
        SELECT p.sequence,e.move,c.sequence
        FROM edges e
        JOIN node_order p ON p.mask=e.parent
        JOIN node_order c ON c.mask=e.child
    """)
    count = connection.execute("SELECT COUNT(*) FROM ordered_edges").fetchone()[0]
    return count


def write_compact(connection: sqlite3.Connection, metadata: dict, path: Path) -> dict:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    node_count, edge_count = _counts(connection)
    indexed_edges = _index_sequence(connection)
    if indexed_edges != edge_count:
        raise ValueError("cannot compact a bundle with missing edge endpoints")
    roots = []
    for root in metadata["roots_parsed"]:
        row = connection.execute("SELECT sequence FROM nodes WHERE mask=?",
                                 (_blob(root["mask"]),)).fetchone()
        if row is None:
            raise ValueError("compact bundle references a missing root")
        roots.append((root["id"], row[0], root["verdict"]))

    path.parent.mkdir(parents=True, exist_ok=True)
    raw = path.open("wb")
    stream = gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) if path.suffix == ".gz" else raw
    writer = _BinaryWriter(stream)
    writer.write(MAGIC)
    writer.byte(metadata["board_size"])
    writer.varint(len(roots))
    writer.varint(node_count)
    writer.varint(edge_count)
    for root_id, sequence, verdict in roots:
        writer.string(root_id)
        writer.varint(sequence)
        writer.byte(verdict)

    nodes = iter(connection.execute(
        "SELECT n.mask,n.verdict,n.terminal,n.legal_count,n.edge_count,o.sequence "
        "FROM nodes n JOIN node_order o ON o.mask=n.mask ORDER BY o.sequence"))
    edge_cursor = iter(connection.execute(
        "SELECT parent_sequence,move,child_sequence FROM ordered_edges ORDER BY parent_sequence,move"))
    edge = next(edge_cursor, None)
    previous_mask = 0
    written_edges = 0
    for expected_sequence, row in enumerate(nodes):
        mask_blob, verdict, terminal, legal_count, stored_edge_count, sequence = row
        if sequence != expected_sequence:
            raise ValueError("compact node sequence is not contiguous")
        mask = _mask(mask_blob)
        if mask <= previous_mask and expected_sequence:
            raise ValueError("compact node masks are not strictly ordered")
        writer.varint(mask - previous_mask)
        previous_mask = mask
        writer.byte(verdict)
        writer.byte(terminal)
        writer.varint(legal_count)
        if edge is not None and edge[0] < sequence:
            raise ValueError("orphan edge in compact source")
        node_edges = []
        while edge is not None and edge[0] == sequence:
            node_edges.append(edge[1:])
            edge = next(edge_cursor, None)
        if len(node_edges) != stored_edge_count:
            raise ValueError("edge count changed during compaction")
        writer.varint(len(node_edges))
        for move, child_sequence in node_edges:
            if not 0 <= move < metadata["board_size"] ** 2:
                raise ValueError("invalid move in compact source")
            writer.byte(move)
            writer.varint(child_sequence)
        written_edges += len(node_edges)
    if edge is not None or written_edges != edge_count:
        raise ValueError("compact edge count mismatch")
    writer.finish()
    if stream is not raw:
        stream.close()
    raw.close()
    return {"compact_bytes": _file_size(path), "compact_sha256": _file_sha256(path),
            "compact_uncompressed_sha256": _compact_payload_sha256(path)}


def _compact_payload_sha256(path: Path) -> str:
    opener = gzip.open if path.suffix == ".gz" else open
    digest = hashlib.sha256()
    count = 0
    with opener(path, "rb") as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            count += len(block)
            if count > CHECKSUM_SIZE:
                # Keep a 32-byte tail out of the payload digest.
                pass
            digest.update(block)
    # The binary reader validates the internal trailer. The returned digest is
    # over the full uncompressed artifact for a simple reproducible receipt.
    return digest.hexdigest()


def read_compact(path: Path, connection: sqlite3.Connection) -> dict:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rb") as stream:
        reader = _BinaryReader(stream)
        if reader.exact(len(MAGIC)) != MAGIC:
            raise ValueError("unsupported compact proof bundle magic/version")
        n = reader.byte()
        root_count = reader.varint()
        node_count = reader.varint()
        expected_edges = reader.varint()
        if not 1 <= n <= 11 or not 1 <= root_count <= 100_000 or not node_count:
            raise ValueError("invalid compact proof bundle dimensions")
        if node_count > 0xFFFFFFFF or expected_edges > 0xFFFFFFFF:
            raise ValueError("compact proof bundle count exceeds v1 limits")
        roots_raw = []
        for _ in range(root_count):
            root_id = reader.string()
            sequence = reader.varint()
            verdict = reader.byte()
            if sequence >= node_count or verdict not in (1, 2):
                raise ValueError("invalid compact root reference")
            roots_raw.append((root_id, sequence, verdict))

        previous_mask = 0
        actual_edges = 0
        full = (1 << (n * n)) - 1
        for sequence in range(node_count):
            delta = reader.varint()
            if sequence and delta == 0:
                raise ValueError("duplicate or unsorted compact node mask")
            mask = previous_mask + delta
            if mask & ~full:
                raise ValueError("compact node mask is outside the board")
            previous_mask = mask
            verdict = reader.byte()
            terminal = reader.byte()
            legal_count = reader.varint()
            edge_count = reader.varint()
            if verdict not in (1, 2) or terminal not in (0, 1):
                raise ValueError("invalid compact node verdict or terminal marker")
            if legal_count > n * n or edge_count > n * n:
                raise ValueError("invalid compact node degree")
            blob = _blob(mask)
            try:
                connection.execute(
                    "INSERT INTO nodes(mask,ident,stones,verdict,terminal,legal_count,edge_count,sequence) "
                    "VALUES(?,?,?,?,?,?,?,?)",
                    (blob, str(mask), mask.bit_count(), verdict, terminal,
                     legal_count, edge_count, sequence))
            except sqlite3.IntegrityError as exc:
                raise ValueError("duplicate compact proof node") from exc
            previous_move = -1
            for _ in range(edge_count):
                move = reader.byte()
                child_sequence = reader.varint()
                if move <= previous_move or move >= n * n or child_sequence >= node_count:
                    raise ValueError("invalid compact edge reference")
                previous_move = move
                try:
                    connection.execute(
                        "INSERT INTO edges(parent,move,child,child_sequence) VALUES(?,?,NULL,?)",
                        (blob, move, child_sequence))
                except sqlite3.IntegrityError as exc:
                    raise ValueError("duplicate compact move label") from exc
            actual_edges += edge_count
            if sequence and sequence % 50_000 == 0:
                connection.commit()
        if actual_edges != expected_edges:
            raise ValueError("compact proof edge count mismatch")
        connection.commit()
        reader.check_trailer()

    connection.execute("""
        UPDATE edges SET child=(SELECT mask FROM nodes WHERE nodes.sequence=edges.child_sequence)
    """)
    if connection.execute("SELECT 1 FROM edges WHERE child IS NULL LIMIT 1").fetchone():
        raise ValueError("compact edge references a missing node")
    roots = []
    root_ids = set()
    for root_id, sequence, verdict in roots_raw:
        if root_id in root_ids:
            raise ValueError("duplicate compact proof root id")
        root_ids.add(root_id)
        row = connection.execute("SELECT mask FROM nodes WHERE sequence=?", (sequence,)).fetchone()
        if row is None:
            raise ValueError("compact root references a missing node")
        roots.append({"id": root_id, "mask": _mask(row[0]), "verdict": verdict})
    return {"schema": SCHEMA, "board_size": n, "proposition": PROPOSITION,
            "roots_parsed": roots}


def stores_equal(left_meta: dict, left: sqlite3.Connection,
                 right_meta: dict, right: sqlite3.Connection) -> bool:
    if any(left_meta.get(key) != right_meta.get(key)
           for key in ("schema", "board_size", "proposition")):
        return False
    if left_meta["roots_parsed"] != right_meta["roots_parsed"]:
        return False
    left_nodes, left_edges = _counts(left)
    right_nodes, right_edges = _counts(right)
    if (left_nodes, left_edges) != (right_nodes, right_edges):
        return False
    node_columns = "mask,stones,verdict,terminal,legal_count,edge_count"
    edge_columns = "parent,move,child"
    for connection in (left, right):
        connection.commit()
    # SQLite cannot attach two anonymous temporary connections portably. Compare
    # their sorted cursors with bounded memory instead.
    for query in (node_columns, edge_columns):
        table = "nodes" if query == node_columns else "edges"
        a = iter(left.execute(f"SELECT {query} FROM {table} ORDER BY {query}"))
        b = iter(right.execute(f"SELECT {query} FROM {table} ORDER BY {query}"))
        while True:
            row_a = next(a, None)
            row_b = next(b, None)
            if row_a != row_b:
                return False
            if row_a is None:
                break
    return True


def _closure_size(connection: sqlite3.Connection, start: bytes) -> int:
    connection.execute("CREATE TEMP TABLE IF NOT EXISTS candidate_seen(mask BLOB PRIMARY KEY) WITHOUT ROWID")
    connection.execute("CREATE TEMP TABLE IF NOT EXISTS candidate_frontier(mask BLOB PRIMARY KEY) WITHOUT ROWID")
    connection.execute("CREATE TEMP TABLE IF NOT EXISTS candidate_next(mask BLOB PRIMARY KEY) WITHOUT ROWID")
    connection.execute("DELETE FROM candidate_seen")
    connection.execute("DELETE FROM candidate_frontier")
    connection.execute("INSERT INTO candidate_seen(mask) VALUES(?)", (start,))
    connection.execute("INSERT INTO candidate_frontier(mask) VALUES(?)", (start,))
    while connection.execute("SELECT 1 FROM candidate_frontier LIMIT 1").fetchone():
        connection.execute("DELETE FROM candidate_next")
        connection.execute("""
            INSERT OR IGNORE INTO candidate_next(mask)
            SELECT e.child FROM edges e JOIN candidate_frontier f ON f.mask=e.parent
            WHERE NOT EXISTS (SELECT 1 FROM candidate_seen s WHERE s.mask=e.child)
        """)
        if not connection.execute("SELECT 1 FROM candidate_next LIMIT 1").fetchone():
            break
        connection.execute("INSERT OR IGNORE INTO candidate_seen SELECT mask FROM candidate_next")
        connection.execute("DELETE FROM candidate_frontier")
        connection.execute("INSERT INTO candidate_frontier SELECT mask FROM candidate_next")
    return connection.execute("SELECT COUNT(*) FROM candidate_seen").fetchone()[0]


def _witness_switch_counts(connection: sqlite3.Connection, roots: list[int],
                           parent: int, old_move: int, new_move: int,
                           new_child: int, *, restore: bool = True) -> tuple[int, int]:
    """Count the reachable graph after one local witness edge replacement."""
    connection.execute("CREATE TEMP TABLE IF NOT EXISTS switch_seen(mask BLOB PRIMARY KEY) WITHOUT ROWID")
    connection.execute("CREATE TEMP TABLE IF NOT EXISTS switch_frontier(mask BLOB PRIMARY KEY) WITHOUT ROWID")
    connection.execute("CREATE TEMP TABLE IF NOT EXISTS switch_next(mask BLOB PRIMARY KEY) WITHOUT ROWID")
    old_row = connection.execute(
        "SELECT child FROM edges WHERE parent=? AND move=?",
        (_blob(parent), old_move)).fetchone()
    if old_row is None:
        raise ValueError("selected S6 witness edge is missing during switch audit")
    changed_edge = False
    try:
        changed = connection.execute(
            "UPDATE edges SET move=?,child=? WHERE parent=? AND move=?",
            (new_move, _blob(new_child), _blob(parent), old_move)).rowcount
        if changed != 1:
            raise ValueError("selected S6 witness edge changed during switch audit")
        changed_edge = True
        connection.execute("DELETE FROM switch_seen")
        connection.execute("DELETE FROM switch_frontier")
        connection.execute("DELETE FROM switch_next")
        connection.executemany("INSERT OR IGNORE INTO switch_frontier(mask) VALUES(?)",
                               ((_blob(mask),) for mask in roots))
        connection.execute("INSERT OR IGNORE INTO switch_seen SELECT mask FROM switch_frontier")
        while connection.execute("SELECT 1 FROM switch_frontier LIMIT 1").fetchone():
            connection.execute("DELETE FROM switch_next")
            connection.execute("""
                INSERT OR IGNORE INTO switch_next(mask)
                SELECT e.child FROM edges e JOIN switch_frontier f ON f.mask=e.parent
                WHERE NOT EXISTS (SELECT 1 FROM switch_seen s WHERE s.mask=e.child)
            """)
            if not connection.execute("SELECT 1 FROM switch_next LIMIT 1").fetchone():
                break
            connection.execute("INSERT OR IGNORE INTO switch_seen SELECT mask FROM switch_next")
            connection.execute("DELETE FROM switch_frontier")
            connection.execute("INSERT INTO switch_frontier SELECT mask FROM switch_next")
        nodes = connection.execute("SELECT COUNT(*) FROM switch_seen").fetchone()[0]
        edges = connection.execute(
            "SELECT COUNT(*) FROM edges e JOIN switch_seen s ON s.mask=e.parent").fetchone()[0]
        return nodes, edges
    finally:
        # The temporary store uses journal_mode=OFF, where SQLite savepoint
        # rollback cannot be relied on. Restore explicitly for an audit; a
        # variant builder can keep the edge and prune to switch_seen instead.
        if changed_edge and restore:
            restored = connection.execute(
                "UPDATE edges SET move=?,child=? WHERE parent=? AND move=?",
                (old_move, old_row[0], _blob(parent), new_move)).rowcount
            if restored != 1:
                raise RuntimeError("failed to restore the original S6 witness edge")


def audit_captured_s6_witnesses(metadata: dict, connection: sqlite3.Connection) -> dict:
    """Compare only S6 LOSS witnesses whose closed proof is already in this DAG."""
    board = Board(metadata["board_size"])
    result = []
    for root in metadata["roots_parsed"]:
        mask = root["mask"]
        if mask.bit_count() != 5 or root["verdict"] != 2:
            continue
        selected_rows = connection.execute(
            "SELECT move,child FROM edges WHERE parent=? ORDER BY move", (_blob(mask),)).fetchall()
        selected = {_mask(child) for _move, child in selected_rows}
        legal = board.legal(mask)
        candidates = set()
        for move in board.points(legal):
            child = board.canonical(mask | (1 << move))
            row = connection.execute(
                "SELECT verdict,stones FROM nodes WHERE mask=?", (_blob(child),)).fetchone()
            if row is not None and row == (2, 6):
                candidates.add(child)
        if not selected or not selected <= candidates:
            raise ValueError("captured S5 LOSS witness is absent from its closed S6 LOSS candidates")
        alternatives = sorted(candidates - selected)
        # Closure sizes only inform a choice when there is a genuine alternate.
        # Avoid traversing the large proof repeatedly when the bundle contains
        # only the already selected decisive child.
        selected_sizes = ({str(child): _closure_size(connection, _blob(child))
                           for child in sorted(selected)} if alternatives else {})
        alternative_sizes = ({str(child): _closure_size(connection, _blob(child))
                              for child in alternatives} if alternatives else {})
        selected_move = selected_rows[0][0]
        root_masks = [item["mask"] for item in metadata["roots_parsed"]]
        switch_variants = []
        for child in alternatives:
            moves = [move for move in board.points(legal)
                     if board.canonical(mask | (1 << move)) == child]
            if not moves:
                raise ValueError("alternate closed S6 witness has no legal parent move")
            switched_nodes, switched_edges = _witness_switch_counts(
                connection, root_masks, mask, selected_move, moves[0], child)
            switch_variants.append({
                "replacement_move": moves[0],
                "replacement_s6_child": str(child),
                "reachable_nodes": switched_nodes,
                "reachable_edges": switched_edges,
                "removed_nodes_vs_current": _counts(connection)[0] - switched_nodes,
                "removed_edges_vs_current": _counts(connection)[1] - switched_edges,
                "all_original_roots_retained": True,
                "comparison": "exact reachable union for the frozen root list after replacing this one verified existential witness edge",
            })
        result.append({
            "root_id": root["id"],
            "s5_root": str(mask),
            "legal_s6_children": legal.bit_count(),
            "closed_s6_loss_witnesses_in_bundle": len(candidates),
            "selected_s6_witnesses": [str(child) for child in sorted(selected)],
            "alternative_s6_witnesses": [str(child) for child in alternatives],
            "selected_witness_closure_nodes": selected_sizes,
            "alternative_witness_closure_nodes": alternative_sizes,
            "alternative_witness_dag_switches": switch_variants,
        })
    return {
        "scope": "only S6 LOSS nodes already present and terminal-closed in the validated three-root bundle; no solver/cache evidence is imported",
        "roots": result,
        "roots_with_alternative_closed_s6_loss_witnesses": sum(
            bool(row["alternative_s6_witnesses"]) for row in result),
    }


def export_json(connection: sqlite3.Connection, metadata: dict, path: Path) -> None:
    if path.exists():
        raise FileExistsError(f"refusing to overwrite {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    raw = path.open("wb")
    stream = gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) if path.suffix == ".gz" else raw

    def write(value: str) -> None:
        stream.write(value.encode("utf-8"))

    write('{"board_size":' + str(metadata["board_size"]) + ',"nodes":{')
    node_cursor = iter(connection.execute(
        "SELECT mask,ident,stones,verdict,terminal,legal_count,edge_count "
        "FROM nodes ORDER BY mask"))
    edge_cursor = iter(connection.execute(
        "SELECT e.parent,e.move,c.ident FROM edges e LEFT JOIN nodes c ON c.mask=e.child "
        "ORDER BY e.parent,e.move"))
    edge = next(edge_cursor, None)
    first_node = True
    for mask_blob, ident, stones, verdict, terminal, legal_count, edge_count in node_cursor:
        if edge is not None and edge[0] < mask_blob:
            raise ValueError("edge appears without a node during JSON export")
        node_edges = []
        while edge is not None and edge[0] == mask_blob:
            if edge[2] is None:
                raise ValueError("missing edge child during JSON export")
            node_edges.append({"move": edge[1], "child": edge[2]})
            edge = next(edge_cursor, None)
        if len(node_edges) != edge_count:
            raise ValueError("edge count changed during JSON export")
        if not first_node:
            write(",")
        first_node = False
        write(json.dumps(ident, separators=(",", ":")) + ":")
        node = {"edges": node_edges, "legal_count": legal_count, "mask": ident,
                "stones": stones, "terminal": bool(terminal), "verdict": verdict}
        write(json.dumps(node, sort_keys=True, separators=(",", ":")))
    if edge is not None:
        raise ValueError("edge appears without a node during JSON export")
    roots = [{"id": root["id"], "root": str(root["mask"]), "verdict": root["verdict"]}
             for root in metadata["roots_parsed"]]
    write("},\"proposition\":" + json.dumps(PROPOSITION) + ",\"roots\":")
    write(json.dumps(roots, sort_keys=True, separators=(",", ":")))
    write(",\"schema\":" + json.dumps(SCHEMA) + "}\n")
    if stream is not raw:
        stream.close()
    raw.close()


def _write_receipt(path: Path | None, receipt: dict) -> None:
    payload = json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n"
    if path is not None:
        if path.exists():
            raise FileExistsError(f"refusing to overwrite {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(payload, encoding="utf-8")
    print(payload.rstrip())


def _progress(done: int, total: int, edges: int) -> None:
    print(json.dumps({"event": "proof_nodes_verified", "verified": done,
                      "total": total, "edges": edges}, separators=(",", ":")),
          file=sys.stderr, flush=True)


def _verify_json(path: Path, db_path: Path) -> tuple[dict, dict, sqlite3.Connection]:
    connection = _open_store(db_path)
    metadata = load_json_bundle(path, connection)
    receipt = verify_store(metadata, connection, progress=_progress)
    return metadata, receipt, connection


def _verify_compact(path: Path, db_path: Path) -> tuple[dict, dict, sqlite3.Connection]:
    connection = _open_store(db_path)
    metadata = read_compact(path, connection)
    receipt = verify_store(metadata, connection, progress=_progress)
    return metadata, receipt, connection


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scratch-dir", type=Path,
                        help="place temporary SQLite indexes under this directory")
    commands = parser.add_subparsers(dest="command", required=True)
    for name in ("verify-json", "verify-compact"):
        sub = commands.add_parser(name)
        sub.add_argument("--certificate", type=Path, required=True)
        sub.add_argument("--receipt", type=Path)
    convert = commands.add_parser("convert")
    convert.add_argument("--source", type=Path, required=True)
    convert.add_argument("--output", type=Path, required=True)
    convert.add_argument("--receipt", type=Path)
    convert.add_argument("--prior-verification", type=Path,
                         help="reuse a successful JSON receipt bound to the exact source SHA-256")
    switch = commands.add_parser("optimize-witness-switch")
    switch.add_argument("--certificate", type=Path, required=True)
    switch.add_argument("--prior-verification", type=Path, required=True,
                        help="successful compact verification receipt for this exact input")
    switch.add_argument("--root-id", required=True)
    switch.add_argument("--move", type=int, required=True,
                        help="legal move whose already-verified closed child replaces the witness")
    switch.add_argument("--output", type=Path, required=True)
    switch.add_argument("--receipt", type=Path)
    export = commands.add_parser("export-json")
    export.add_argument("--certificate", type=Path, required=True)
    export.add_argument("--output", type=Path, required=True)
    export.add_argument("--receipt", type=Path)
    args = parser.parse_args()
    started = time.perf_counter()
    if args.scratch_dir is not None:
        args.scratch_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="kyouen-proof-store-", dir=args.scratch_dir) as temporary:
        temp_path = Path(temporary)
        if args.command == "verify-json":
            metadata, receipt, connection = _verify_json(
                args.certificate, temp_path / "proof.sqlite")
            receipt.update({"format": "json", "input_bytes": _file_size(args.certificate),
                           "input_sha256": _file_sha256(args.certificate),
                           "scratch_index_bytes": _file_size(temp_path / "proof.sqlite")})
            connection.close()
        elif args.command == "verify-compact":
            metadata, receipt, connection = _verify_compact(
                args.certificate, temp_path / "proof.sqlite")
            receipt.update({"format": "kyprfdg-v1", "input_bytes": _file_size(args.certificate),
                           "input_sha256": _file_sha256(args.certificate),
                           "scratch_index_bytes": _file_size(temp_path / "proof.sqlite")})
            connection.close()
        elif args.command == "convert":
            source_db = temp_path / "source.sqlite"
            if args.prior_verification is None:
                source_meta, receipt, source_conn = _verify_json(args.source, source_db)
                validation_reused = False
                prior_receipt_hash = None
            else:
                source_conn = _open_store(source_db)
                source_meta = load_json_bundle(args.source, source_conn)
                receipt = _reuse_verification_receipt(
                    args.prior_verification, args.source, source_meta, source_conn)
                validation_reused = True
                prior_receipt_hash = _file_sha256(args.prior_verification)
            source_index_bytes = _file_size(source_db)
            s6_witness_audit = audit_captured_s6_witnesses(source_meta, source_conn)
            compact = write_compact(source_conn, source_meta, args.output)
            compact_db = temp_path / "compact.sqlite"
            compact_conn = _open_store(compact_db)
            compact_meta = read_compact(args.output, compact_conn)
            # The independently decoded binary and the validated JSON source
            # must have identical nodes, edges, root verdicts, and metadata.
            equal = stores_equal(source_meta, source_conn, compact_meta, compact_conn)
            if not equal:
                raise ValueError("compact round-trip graph differs from source JSON")
            receipt.update({"format": "kyprfdg-v1", "source_bytes": _file_size(args.source),
                            "source_sha256": _file_sha256(args.source), **compact,
                            "round_trip_graph_equal": True,
                            "source_verification_reused": validation_reused,
                            "prior_verification_receipt_sha256": prior_receipt_hash,
                            "captured_s6_witness_audit": s6_witness_audit,
                            "scratch_index_bytes": source_index_bytes + _file_size(compact_db),
                            "compact_decoded_nodes": _counts(compact_conn)[0]})
            compact_conn.close()
            source_conn.close()
        elif args.command == "optimize-witness-switch":
            source_conn = _open_store(temp_path / "source.sqlite")
            source_meta = read_compact(args.certificate, source_conn)
            verified = _reuse_compact_verification_receipt(
                args.prior_verification, args.certificate, source_meta, source_conn)
            source_bytes = _file_size(args.certificate)
            source_sha = _file_sha256(args.certificate)
            switch_receipt = apply_witness_switch_and_prune(
                source_conn, source_meta, args.root_id, args.move)
            compact = write_compact(source_conn, source_meta, args.output)
            variant_conn = _open_store(temp_path / "variant.sqlite")
            variant_meta = read_compact(args.output, variant_conn)
            equal = stores_equal(source_meta, source_conn, variant_meta, variant_conn)
            if not equal:
                raise ValueError("witness-switch compact graph differs from its pruned source index")
            node_count, edge_count = _counts(variant_conn)
            terminal_count = variant_conn.execute(
                "SELECT COUNT(*) FROM nodes WHERE terminal=1").fetchone()[0]
            receipt = {
                "schema": "n11-proof-witness-switch-v1",
                "format": "kyprfdg-v1",
                "source_bytes": source_bytes,
                "source_sha256": source_sha,
                "prior_verification_receipt_sha256": _file_sha256(args.prior_verification),
                "source_verification_reused": True,
                "source_verified_nodes": verified["nodes"],
                "source_verified_edges": verified["edges"],
                "witness_switch": switch_receipt,
                **compact,
                "nodes": node_count,
                "edges": edge_count,
                "roots": [{"id": root["id"], "root": str(root["mask"]),
                           "verdict": root["verdict"]}
                          for root in variant_meta["roots_parsed"]],
                "terminal_nodes": terminal_count,
                "trusted_leaves": 0,
                "round_trip_graph_equal": True,
                "scratch_index_bytes": _file_size(temp_path / "source.sqlite")
                + _file_size(temp_path / "variant.sqlite"),
            }
            variant_conn.close()
            source_conn.close()
        else:
            metadata, receipt, connection = _verify_compact(
                args.certificate, temp_path / "proof.sqlite")
            export_json(connection, metadata, args.output)
            receipt.update({"format": "json", "output_bytes": _file_size(args.output),
                            "output_sha256": _file_sha256(args.output)})
            connection.close()
        receipt["wall_seconds"] = round(time.perf_counter() - started, 3)
        _write_receipt(args.receipt, receipt)


if __name__ == "__main__":
    main()
