import sys
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from layout import LEGACY_DIRECTORIES, layout_errors


class LayoutTests(unittest.TestCase):
    def frozen_fixture(self, root):
        source = root / "research/experiments/frozen/README.md"
        source.parent.mkdir(parents=True)
        source.write_text("[old](../../knowledge/items/K0001-old.md)\n", encoding="utf-8")
        target = root / "research/knowledge/items/K0002-new.md"
        target.parent.mkdir(parents=True)
        target.write_text("# Current\n", encoding="utf-8")
        manifest = root / "research/knowledge/frozen_links.json"
        data = {"version": 1, "files": {source.relative_to(root).as_posix(): {
            "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
            "targets": {"research/knowledge/items/K0001-old.md": target.relative_to(root).as_posix()}}}}
        manifest.write_text(json.dumps(data), encoding="utf-8")
        return source, target, manifest, data

    def test_frozen_reference_keeps_original_bytes_and_checks_successor(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, target, _, _ = self.frozen_fixture(root)
            before = source.read_bytes()
            self.assertEqual(layout_errors(root), [])
            self.assertEqual(source.read_bytes(), before)
            target.unlink()
            self.assertTrue(any("frozen target" in e for e in layout_errors(root)))
            self.assertTrue(any("broken local link" in e for e in layout_errors(root)))

    def test_frozen_hash_and_source_scope_fail_closed(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, _, _, _ = self.frozen_fixture(root)
            (source.parent / "other.md").write_bytes(source.read_bytes())
            self.assertTrue(any("other.md: broken local link" in e for e in layout_errors(root)))
            source.write_bytes(source.read_bytes() + b"changed\n")
            self.assertTrue(any("frozen source hash mismatch" in e for e in layout_errors(root)))
            self.assertTrue(any("README.md: broken local link" in e for e in layout_errors(root)))

    def test_frozen_manifest_rejects_unsafe_and_duplicate_entries(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            _, _, manifest, data = self.frozen_fixture(root)
            spec = next(iter(data["files"].values()))
            spec["targets"]["research/knowledge/items/K0001-old.md"] = "research/knowledge/items/../../../../outside.md"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("unsafe frozen target" in e for e in layout_errors(root)))
            other = root / "docs/outside-items.md"
            other.parent.mkdir()
            other.write_text("# Not a knowledge item\n", encoding="utf-8")
            spec["targets"]["research/knowledge/items/K0001-old.md"] = "research/knowledge/items/../../../docs/outside-items.md"
            manifest.write_text(json.dumps(data), encoding="utf-8")
            self.assertTrue(any("unsafe frozen target" in e for e in layout_errors(root)))
            manifest.write_text('{"version":1,"version":1,"files":{}}', encoding="utf-8")
            self.assertTrue(any("duplicate manifest key" in e for e in layout_errors(root)))

    def test_legacy_directory_or_file_is_rejected_but_historical_text_is_allowed(self):
        for name in LEGACY_DIRECTORIES:
            with self.subTest(name=name), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root / "README.md").write_text(f"Historical path: `{name}/old.json`", encoding="utf-8")
                self.assertEqual(layout_errors(root), [])
                target = root / name
                target.mkdir(parents=True)
                self.assertIn(f"forbidden legacy filesystem path: {name}", layout_errors(root))
                target.rmdir()
                target.touch()
                self.assertIn(f"forbidden legacy filesystem path: {name}", layout_errors(root))

    def test_missing_local_link_and_runner_are_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("[missing](docs/missing.md) [remote](https://example.com/)\n", encoding="utf-8")
            (root / "runner.py").write_text('command = "scripts/missing.py"\n', encoding="utf-8")
            errors = layout_errors(root)
            self.assertTrue(any("broken local link" in e for e in errors))
            self.assertTrue(any("missing source/runner" in e for e in errors))

    def test_relative_percent_encoded_link_and_fenced_example(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "docs").mkdir()
            (root / "docs/a b.md").write_text("# Target\n", encoding="utf-8")
            (root / "README.md").write_text('[ok](docs/a%20b.md#target)\n```md\n[example](absent.md)\n```\n', encoding="utf-8")
            self.assertEqual(layout_errors(root), [])

    def test_builder_can_replace_stale_generated_links_but_checks_still_reject_them(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            generated = root / "research/knowledge/generated"
            generated.mkdir(parents=True)
            (generated / "artifacts.md").write_text("[previous location](../../gone.md)\n", encoding="utf-8")
            readme = root / "README.md"
            readme.write_text(
                "<!-- BEGIN GENERATED SOLUTION STATUS -->\n"
                "[previous item](gone-item.md)\n"
                "<!-- END GENERATED SOLUTION STATUS -->\n", encoding="utf-8"
            )
            self.assertTrue(any("broken local link" in e for e in layout_errors(root)))
            self.assertTrue(any("README.md" in e for e in layout_errors(root)))
            self.assertEqual(layout_errors(root, include_generated=False), [])
            readme.write_text(readme.read_text(encoding="utf-8") + "[missing canonical source](gone.md)\n", encoding="utf-8")
            self.assertTrue(any("broken local link" in e for e in layout_errors(root, include_generated=False)))
