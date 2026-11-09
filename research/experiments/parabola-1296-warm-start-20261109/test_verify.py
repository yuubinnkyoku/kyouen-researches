#!/usr/bin/env python3
"""Exercise independent audit against altered candidate, model, and provenance."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from verify import check

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'output/control-target1296'


class Tampering(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.path = Path(self.temp.name) / 'receipt'
        shutil.copytree(SOURCE, self.path)

    def tearDown(self):
        self.temp.cleanup()

    def test_candidate_changed(self):
        path = self.path / 'candidate.txt'
        parts = path.read_text().split()
        parts[-1] = parts[-2]
        path.write_text(' '.join(parts) + '\n')
        with self.assertRaises(AssertionError):
            check(self.path)

    def test_model_changed(self):
        path = self.path / 'model.json'
        obj = json.loads(path.read_text())
        obj['signed_model'][0] *= -1
        path.write_text(json.dumps(obj))
        with self.assertRaises(AssertionError):
            check(self.path)

    def test_worker_hash_changed(self):
        for name in ('init.json', 'result.json'):
            path = self.path / name
            obj = json.loads(path.read_text())
            obj['worker_sha256'] = '0' * 64
            path.write_text(json.dumps(obj))
        with self.assertRaises(AssertionError):
            check(self.path)


if __name__ == '__main__':
    unittest.main()
