import copy
import hashlib
import gzip
import json
import tempfile
import unittest
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-20261011/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-dag-engine-followup-20261011/scripts"))
sys.path.insert(0, str(ROOT / "research/experiments/n11-proof-compact-20261011/scripts"))
from dag_builder import build_certificate  # noqa: E402
from verify_shared_bundle import verify_bundle  # noqa: E402
from bundle_store import (  # noqa: E402
    _blob,
    _open_store,
    _witness_switch_counts,
    export_json,
    load_json_bundle,
    read_compact,
    _reuse_verification_receipt,
    stores_equal,
    verify_store,
    write_compact,
)


def _bundle():
    certificate, _stats = build_certificate(4, 0, order="count-asc",
                                             state_sharing="d4", node_limit=100_000)
    verdict = verify_bundle({
        "schema": "kyouen-proof-dag-multi-root-v1",
        "board_size": 4,
        "proposition": "original_first_player_wins",
        "roots": [{"id": "s0", "root": certificate["root"],
                   "verdict": 2}],
        "nodes": certificate["nodes"],
    })["roots"][0]["verdict"]
    return {
        "schema": "kyouen-proof-dag-multi-root-v1",
        "board_size": 4,
        "proposition": "original_first_player_wins",
        "roots": [{"id": "s0", "root": certificate["root"], "verdict": verdict}],
        "nodes": certificate["nodes"],
    }


def _normalized(bundle):
    nodes = {}
    for ident, node in bundle["nodes"].items():
        item = dict(node)
        item["edges"] = sorted((edge["move"], edge["child"]) for edge in node["edges"])
        nodes[ident] = item
    return {
        "schema": bundle["schema"],
        "board_size": bundle["board_size"],
        "proposition": bundle["proposition"],
        "roots": bundle["roots"],
        "nodes": nodes,
    }


class DiskBackedBundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = _bundle()

    def _write_source(self, path, bundle):
        path.write_text(json.dumps(bundle, sort_keys=True, separators=(",", ":")),
                        encoding="utf-8")

    def _verify_json(self, path):
        connection = _open_store(path.with_suffix(".sqlite"))
        try:
            metadata = load_json_bundle(path, connection)
            return verify_store(metadata, connection)
        finally:
            connection.close()

    def test_compact_round_trip_matches_independent_bundle_verifier(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            source = temp / "source.json"
            compact = temp / "bundle.kpd.gz"
            compact_copy = temp / "bundle-copy.kpd.gz"
            exported = temp / "exported.json"
            self._write_source(source, self.bundle)
            source_db = _open_store(temp / "source.sqlite")
            source_meta = load_json_bundle(source, source_db)
            source_receipt = verify_store(source_meta, source_db)
            write_compact(source_db, source_meta, compact)
            write_compact(source_db, source_meta, compact_copy)
            self.assertEqual(compact.read_bytes(), compact_copy.read_bytes())
            compact_db = _open_store(temp / "compact.sqlite")
            compact_meta = read_compact(compact, compact_db)
            compact_receipt = verify_store(compact_meta, compact_db)
            self.assertTrue(stores_equal(source_meta, source_db, compact_meta, compact_db))
            self.assertEqual(source_receipt, compact_receipt)
            export_json(compact_db, compact_meta, exported)
            with exported.open(encoding="utf-8") as stream:
                decoded = json.load(stream)
            self.assertEqual(_normalized(self.bundle), _normalized(decoded))
            self.assertEqual(verify_bundle(decoded), verify_bundle(self.bundle))
            source_db.close()
            compact_db.close()

    def test_missing_child_wrong_polarity_and_illegal_move_are_rejected(self):
        mutations = []
        missing = copy.deepcopy(self.bundle)
        missing["nodes"][missing["roots"][0]["root"]]["edges"].pop()
        mutations.append((missing, "omits or duplicates"))

        polarity = copy.deepcopy(self.bundle)
        polarity["nodes"][polarity["roots"][0]["root"]]["verdict"] = 1
        mutations.append((polarity, "existential node|root verdict"))

        illegal = copy.deepcopy(self.bundle)
        illegal["nodes"][illegal["roots"][0]["root"]]["edges"][0]["move"] = 99
        mutations.append((illegal, "illegal move"))

        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            for index, (broken, message) in enumerate(mutations):
                with self.subTest(mutation=index):
                    with self.assertRaisesRegex(ValueError, message):
                        verify_bundle(broken)
                    source = temp / f"broken-{index}.json"
                    self._write_source(source, broken)
                    with self.assertRaisesRegex(ValueError, message):
                        self._verify_json(source)

    def test_trusted_leaf_and_checksum_tamper_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            trusted = copy.deepcopy(self.bundle)
            terminal = next(key for key, node in trusted["nodes"].items()
                            if node["terminal"])
            trusted["nodes"][terminal]["trusted_leaf"] = True
            source = temp / "trusted.json"
            self._write_source(source, trusted)
            with self.assertRaisesRegex(ValueError, "trusted leaves"):
                self._verify_json(source)

            source = temp / "source.json"
            self._write_source(source, self.bundle)
            source_db = _open_store(temp / "source.sqlite")
            metadata = load_json_bundle(source, source_db)
            write_compact(source_db, metadata, temp / "bundle.kpd.gz")
            source_db.close()
            with gzip.open(temp / "bundle.kpd.gz", "rb") as stream:
                raw = bytearray(stream.read())
            raw[-33] ^= 0x01
            with (temp / "tampered.kpd.gz").open("wb") as raw_output:
                with gzip.GzipFile(fileobj=raw_output, mode="wb", mtime=0) as stream:
                    stream.write(raw)
            broken_db = _open_store(temp / "tampered.sqlite")
            try:
                with self.assertRaisesRegex(ValueError, "checksum|compact"):
                    read_compact(temp / "tampered.kpd.gz", broken_db)
            finally:
                broken_db.close()

    def test_compact_missing_edge_with_valid_checksum_is_rejected(self):
        broken = copy.deepcopy(self.bundle)
        broken["nodes"][broken["roots"][0]["root"]]["edges"].pop()
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            source = temp / "broken.json"
            self._write_source(source, broken)
            connection = _open_store(temp / "source.sqlite")
            try:
                metadata = load_json_bundle(source, connection)
                write_compact(connection, metadata, temp / "broken.kpd.gz")
            finally:
                connection.close()
            decoded = _open_store(temp / "decoded.sqlite")
            try:
                metadata = read_compact(temp / "broken.kpd.gz", decoded)
                with self.assertRaisesRegex(ValueError, "omits or duplicates"):
                    verify_store(metadata, decoded)
            finally:
                decoded.close()

    def test_compact_wrong_polarity_is_rejected_after_valid_encoding(self):
        broken = copy.deepcopy(self.bundle)
        root = broken["roots"][0]["root"]
        broken["nodes"][root]["verdict"] = 1 if broken["nodes"][root]["verdict"] == 2 else 2
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            source = temp / "wrong-polarity.json"
            self._write_source(source, broken)
            source_db = _open_store(temp / "source.sqlite")
            try:
                metadata = load_json_bundle(source, source_db)
                write_compact(source_db, metadata, temp / "wrong-polarity.kpd.gz")
            finally:
                source_db.close()
            decoded = _open_store(temp / "decoded.sqlite")
            try:
                metadata = read_compact(temp / "wrong-polarity.kpd.gz", decoded)
                with self.assertRaisesRegex(ValueError,
                                            "existential|incorrect|root verdict|polarity"):
                    verify_store(metadata, decoded)
            finally:
                decoded.close()

    def test_compact_unreachable_terminal_node_is_rejected(self):
        terminal_ids = [ident for ident, node in self.bundle["nodes"].items()
                        if node["terminal"]]
        self.assertGreaterEqual(len(terminal_ids), 2)
        root_id, isolated_id = terminal_ids[:2]
        isolated = {
            "schema": self.bundle["schema"],
            "board_size": self.bundle["board_size"],
            "proposition": self.bundle["proposition"],
            "roots": [{"id": "terminal-root", "root": root_id,
                       "verdict": self.bundle["nodes"][root_id]["verdict"]}],
            "nodes": {
                root_id: copy.deepcopy(self.bundle["nodes"][root_id]),
                isolated_id: copy.deepcopy(self.bundle["nodes"][isolated_id]),
            },
        }
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            source = temp / "unreachable.json"
            self._write_source(source, isolated)
            source_db = _open_store(temp / "source.sqlite")
            try:
                metadata = load_json_bundle(source, source_db)
                write_compact(source_db, metadata, temp / "unreachable.kpd.gz")
            finally:
                source_db.close()
            decoded = _open_store(temp / "decoded.sqlite")
            try:
                metadata = read_compact(temp / "unreachable.kpd.gz", decoded)
                with self.assertRaisesRegex(ValueError, "unreachable"):
                    verify_store(metadata, decoded)
            finally:
                decoded.close()

    def test_prior_receipt_can_only_be_reused_for_the_same_json_bytes(self):
        with tempfile.TemporaryDirectory() as temp:
            temp = Path(temp)
            source = temp / "source.json"
            receipt_path = temp / "verification.json"
            self._write_source(source, self.bundle)
            connection = _open_store(temp / "source.sqlite")
            try:
                metadata = load_json_bundle(source, connection)
                verified = verify_store(metadata, connection)
                verified.update({"format": "json",
                                 "input_sha256": hashlib.sha256(source.read_bytes()).hexdigest()})
                receipt_path.write_text(json.dumps({"format": "json", "returncode": 0,
                                                    "verifier_receipt": verified}),
                                        encoding="utf-8")
                self.assertEqual(_reuse_verification_receipt(
                    receipt_path, source, metadata, connection), verified)
                source.write_text(source.read_text(encoding="utf-8") + " ", encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "different source SHA-256"):
                    _reuse_verification_receipt(receipt_path, source, metadata, connection)
                source.write_bytes(source.read_bytes()[:-1])
                receipt_path.write_text(json.dumps({"format": "json", "returncode": 1,
                                                    "verifier_receipt": verified}),
                                        encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "did not complete successfully"):
                    _reuse_verification_receipt(receipt_path, source, metadata, connection)
            finally:
                connection.close()

    def test_witness_switch_audit_restores_original_edge_with_journal_off(self):
        connection = _open_store(Path(":memory:"))
        try:
            parent, old_child, new_child = 100, 101, 102
            for mask in (parent, old_child, new_child):
                connection.execute(
                    "INSERT INTO nodes(mask,ident,stones,verdict,terminal,legal_count,edge_count) "
                    "VALUES(?,?,?,?,?,?,?)",
                    (_blob(mask), str(mask), mask.bit_count(), 2, 0, 1, 0))
            connection.execute(
                "INSERT INTO edges(parent,move,child) VALUES(?,?,?)",
                (_blob(parent), 11, _blob(old_child)))
            before = connection.execute(
                "SELECT move,child FROM edges WHERE parent=?", (_blob(parent),)).fetchone()
            self.assertEqual(_witness_switch_counts(
                connection, [parent], parent, 11, 46, new_child), (2, 1))
            after = connection.execute(
                "SELECT move,child FROM edges WHERE parent=?", (_blob(parent),)).fetchone()
            self.assertEqual(after, before)
        finally:
            connection.close()


if __name__ == "__main__":
    unittest.main()
