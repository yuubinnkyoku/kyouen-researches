"""Regression tests for fail-closed, atomic S5 cache merge."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parents[1] / 'scripts/dfpn_s5_merge.sh'
POLICY = Path(__file__).resolve().parents[2] / 'n11-frontier-selection-20261005/scripts/s5_evidence_policy.py'
BAD = (1152925911243358208, 536870912)
BAD2 = (10448351135499552768, 128)
GOOD = (1152921504606848001, 16777220)
OTHER = (1152921504606848001, 16777224)


def row(key, verdict, nodes=10):
    return f's5verdict,{key[0]},{key[1]},5,{verdict},{nodes}\n'


class MergeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        scriptdir = self.root / 'research/experiments/n11-search-methods/scripts'
        policydir = self.root / 'research/experiments/n11-frontier-selection-20261005/scripts'
        scriptdir.mkdir(parents=True)
        policydir.mkdir(parents=True)
        self.script = scriptdir / 'dfpn_s5_merge.sh'
        shutil.copy2(SCRIPT, self.script)
        shutil.copy2(POLICY, policydir / 's5_evidence_policy.py')
        self.registry = self.root / 'results/n11-s5-evidence-quarantine.json'
        self.registry.parent.mkdir()
        self.registry.write_text(json.dumps({'schema': 'n11-s5-evidence-quarantine-v1',
            'entries': [{'key': list(k), 'active': True, 'unsupported_verdict': 1}
                        for k in (BAD, BAD2)]}))
        self.out = self.root / 'out.csv'
        self.base = self.root / 'base.csv'
        self.worker = self.root / 'worker.csv'

    def runmerge(self, *inputs):
        return subprocess.run(['bash', str(self.script), str(self.out), *map(str, inputs)],
                              capture_output=True, text=True)

    def test_quarantine_and_unknown_removed(self):
        self.base.write_text(row(BAD, 1) + row(BAD2, 1) + row(GOOD, 2) + row(OTHER, 0))
        r = self.runmerge(self.base)
        self.assertEqual(r.returncode, 0, r.stderr)
        data = self.out.read_text()
        self.assertIn(row(GOOD, 2), data)
        self.assertNotIn(row(BAD, 1), data)
        self.assertNotIn(row(BAD2, 1), data)
        self.assertNotIn(row(OTHER, 0), data)

    def test_missing_source_refuses_without_touching_output(self):
        self.out.write_text('EXISTING\n')
        r = self.runmerge(self.root / 'absent.csv')
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.out.read_text(), 'EXISTING\n')

    def test_missing_registry_refuses_without_touching_output(self):
        self.base.write_text(row(GOOD, 2))
        self.out.write_text('EXISTING\n')
        self.registry.unlink()
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.out.read_text(), 'EXISTING\n')

    def test_conflict_refuses_without_touching_output(self):
        self.base.write_text(row(GOOD, 1))
        self.worker.write_text(row(GOOD, 2))
        self.out.write_text('EXISTING\n')
        r = self.runmerge(self.base, self.worker)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('CONFLICT', r.stderr)
        self.assertEqual(self.out.read_text(), 'EXISTING\n')

    def test_invalid_cache_row_refuses_without_touching_output(self):
        self.base.write_text('s5verdict,123,0,5,2,1\n')
        self.out.write_text('EXISTING\n')
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.out.read_text(), 'EXISTING\n')

    def test_quarantined_conflict_still_refused(self):
        self.base.write_text(row(BAD, 1))
        self.worker.write_text(row(BAD, 2))
        self.out.write_text('EXISTING\n')
        r = self.runmerge(self.base, self.worker)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('CONFLICT', r.stderr)
        self.assertEqual(self.out.read_text(), 'EXISTING\n')

    def test_malformed_registry_refuses_without_touching_output(self):
        self.base.write_text(row(GOOD, 2))
        self.out.write_text('EXISTING\n')
        self.registry.write_text('{bad json')
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertEqual(self.out.read_text(), 'EXISTING\n')

    def test_noncanonical_alias_refused(self):
        pts = [i for i in range(121) if ((GOOD[0] if i < 64 else GOOD[1]) >> (i % 64)) & 1]
        alias = sum(1 << (11*(p//11) + (10-p%11)) for p in pts)
        self.assertNotEqual((alias & ((1<<64)-1), alias>>64), GOOD)
        self.base.write_text(row((alias & ((1<<64)-1), alias>>64), 1))
        self.out.write_text('EXISTING\n')
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('noncanonical', r.stderr)
        self.assertEqual(self.out.read_text(), 'EXISTING\n')

    def test_unsafe_five_stones_refused(self):
        mask = sum(1 << i for i in range(5))
        self.base.write_text(row((mask, 0), 2))
        self.out.write_text('EXISTING\n')
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('unsafe', r.stderr)
        self.assertEqual(self.out.read_text(), 'EXISTING\n')

    def test_deterministic_merge(self):
        self.base.write_text(row(GOOD, 2))
        self.worker.write_text(row(OTHER, 1) + row(GOOD, 2))
        a = self.runmerge(self.base, self.worker)
        self.assertEqual(a.returncode, 0, a.stderr)
        first = self.out.read_bytes()
        b = self.runmerge(self.worker, self.base)
        self.assertEqual(b.returncode, 0, b.stderr)
        self.assertEqual(self.out.read_bytes(), first)


if __name__ == '__main__':
    unittest.main()
