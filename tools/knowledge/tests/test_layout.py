import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from layout import LEGACY_DIRECTORIES, layout_errors


class LayoutTests(unittest.TestCase):
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
            self.assertTrue(any("broken local link" in e for e in layout_errors(root)))
            self.assertEqual(layout_errors(root, include_generated=False), [])
            (root / "README.md").write_text("[missing canonical source](gone.md)\n", encoding="utf-8")
            self.assertTrue(any("broken local link" in e for e in layout_errors(root, include_generated=False)))
