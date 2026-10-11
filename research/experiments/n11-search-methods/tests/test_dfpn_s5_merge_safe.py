"""Regression tests for fail-closed, atomic S5 cache merge."""
import json
import os
import stat
from concurrent.futures import ThreadPoolExecutor
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

    @unittest.skipIf(os.name == 'nt', 'POSIX permission bits are not portable to Windows')
    def test_existing_output_permission_bits_survive_atomic_replace(self):
        self.base.write_text(row(GOOD, 2))
        for mode in (0o640, 0o664, 0o600):
            with self.subTest(mode=oct(mode)):
                self.out.write_text('# existing exact cache\n' + row(GOOD, 2))
                os.chmod(self.out, mode)
                self.assertEqual(stat.S_IMODE(self.out.stat().st_mode), mode)
                result = self.runmerge(self.base)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(stat.S_IMODE(self.out.stat().st_mode), mode)
                self.assertIn(row(GOOD, 2), self.out.read_text())

    @unittest.skipIf(os.name == 'nt', 'POSIX permission bits are not portable to Windows')
    def test_new_output_stays_private_by_default(self):
        self.base.write_text(row(GOOD, 2))
        self.assertFalse(self.out.exists())
        result = self.runmerge(self.base)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(stat.S_IMODE(self.out.stat().st_mode), 0o600)

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
        self.base.write_text('s5verdict,123,0,5,2,1\n')  # only six bits? actually 6? 123 has 6
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
        # Mirror a known valid canonical key; the resulting bitset is legal
        # but must never enter the cache under a noncanonical alias.
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
        # Five stones on one row are forbidden, even if the mask is canonical.
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


    def test_duplicate_exact_metadata_commutative(self):
        self.base.write_text(row(GOOD, 2, 900))
        self.worker.write_text(row(GOOD, 2, 100))
        a = self.runmerge(self.base, self.worker)
        self.assertEqual(a.returncode, 0, a.stderr)
        self.assertIn(row(GOOD, 2, 100), self.out.read_text())
        b = self.runmerge(self.worker, self.base)
        self.assertEqual(b.returncode, 0, b.stderr)
        self.assertIn(row(GOOD, 2, 100), self.out.read_text())

    def test_existing_output_not_silently_discarded(self):
        self.base.write_text(row(GOOD, 2))
        self.assertEqual(self.runmerge(self.base).returncode, 0)
        self.worker.write_text(row(OTHER, 1))
        self.assertEqual(self.runmerge(self.worker).returncode, 0)
        self.assertIn(row(GOOD, 2), self.out.read_text())
        self.assertIn(row(OTHER, 1), self.out.read_text())

    def test_preexisting_output_conflict_refused(self):
        self.base.write_text(row(GOOD, 2))
        self.assertEqual(self.runmerge(self.base).returncode, 0)
        self.worker.write_text(row(GOOD, 1))
        old = self.out.read_bytes()
        r = self.runmerge(self.worker)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('CONFLICT', r.stderr)
        self.assertEqual(old, self.out.read_bytes())

    def test_preexisting_corrupt_destination_refuses_without_overwrite(self):
        self.base.write_text(row(GOOD, 2))
        self.out.write_text('CORRUPT\n')
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('invalid S5 cache row', r.stderr)
        self.assertEqual(self.out.read_text(), 'CORRUPT\n')

    def test_concurrent_conflicting_workers_refuse_second_verdict(self):
        self.base.write_text(row(GOOD, 1))
        self.worker.write_text(row(GOOD, 2))
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda p: self.runmerge(p),
                                    [self.base, self.worker]))
        self.assertEqual(sorted(r.returncode for r in results), [0, 1])
        self.assertIn('CONFLICT', next(r.stderr for r in results if r.returncode))
        saved = self.out.read_text()
        self.assertEqual(sum(row(GOOD, verdict) in saved for verdict in (1, 2)), 1)

    def test_concurrent_merges_preserve_both_workers(self):
        self.base.write_text(row(GOOD, 2))
        self.worker.write_text(row(OTHER, 1))
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda p: self.runmerge(p),
                                    [self.base, self.worker]))
        for r in results:
            self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn(row(GOOD, 2), self.out.read_text())
        self.assertIn(row(OTHER, 1), self.out.read_text())

    @unittest.skipUnless(hasattr(__import__('os'), 'mkfifo'), 'requires POSIX FIFO')
    def test_nonregular_output_fifo_refused_without_replacement(self):
        import os
        os.mkfifo(self.out)
        self.base.write_text(row(GOOD, 2))
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('nonregular S5 cache output', r.stderr)
        self.assertTrue(self.out.is_fifo())

    @unittest.skipUnless(hasattr(__import__('os'), 'mkfifo'), 'requires POSIX FIFO')
    def test_symlink_to_nonregular_output_refused_without_replacement(self):
        import os
        fifo = self.root / 'fifo-target'
        os.mkfifo(fifo)
        self.out.symlink_to(fifo)
        self.base.write_text(row(GOOD, 2))
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('nonregular S5 cache output', r.stderr)
        self.assertTrue(self.out.is_symlink())
        self.assertTrue(fifo.is_fifo())

    def test_hardlink_alias_refuses_before_inode_split(self):
        import os
        self.base.write_text(row(GOOD, 2))
        self.out.write_text('# initial\n')
        alias = self.root / 'alias-hardlink.csv'
        try:
            os.link(self.out, alias)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'hardlinks unavailable: {exc}')
        old = self.out.read_bytes()
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('hard-linked', r.stderr)
        self.assertEqual(self.out.read_bytes(), old)
        self.assertEqual(alias.read_bytes(), old)
        self.assertEqual(self.out.stat().st_ino, alias.stat().st_ino)

    @unittest.skipUnless(hasattr(__import__('os'), 'symlink'), 'symlinks unavailable')
    def test_symlink_aliases_share_lock_and_destination(self):
        self.base.write_text(row(GOOD, 2))
        self.worker.write_text(row(OTHER, 1))
        self.out.write_text('# initial\n')
        alias = self.root / 'alias.csv'
        try:
            alias.symlink_to(self.out)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'symlinks unavailable: {exc}')
        def merge(path, source):
            return subprocess.run(['bash', str(self.script), str(path), str(source)],
                                  capture_output=True, text=True)
        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(merge, self.out, self.base),
                       pool.submit(merge, alias, self.worker)]
            results = [f.result() for f in futures]
        for result in results:
            self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(alias.is_symlink(), 'the alias must not be replaced')
        self.assertIn(row(GOOD, 2), self.out.read_text())
        self.assertIn(row(OTHER, 1), self.out.read_text())
        self.assertEqual(alias.read_bytes(), self.out.read_bytes())

    def test_symlinked_lock_refused_without_modifying_external_file(self):
        self.base.write_text(row(GOOD, 2))
        self.out.write_text('# previous\n')
        external = self.root / 'external.txt'
        external.write_text('DO NOT TOUCH\n')
        lock = self.root / 'out.csv.lock'
        try:
            lock.symlink_to(external)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'symlinks unavailable: {exc}')
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('lock', r.stderr)
        self.assertEqual(self.out.read_text(), '# previous\n')
        self.assertEqual(external.read_text(), 'DO NOT TOUCH\n')
        self.assertTrue(lock.is_symlink())

    def test_symlinked_lock_to_output_refused(self):
        self.base.write_text(row(GOOD, 2))
        self.out.write_text('# previous\n')
        lock = self.root / 'out.csv.lock'
        try:
            lock.symlink_to(self.out)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'symlinks unavailable: {exc}')
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('lock', r.stderr)
        self.assertEqual(self.out.read_text(), '# previous\n')
        self.assertTrue(lock.is_symlink())

    def test_hardlinked_lock_refused_without_modifying_external_file(self):
        import os
        self.base.write_text(row(GOOD, 2))
        self.out.write_text('# previous\n')
        external = self.root / 'external.txt'
        external.write_text('DO NOT TOUCH\n')
        lock = self.root / 'out.csv.lock'
        try:
            os.link(external, lock)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f'hardlinks unavailable: {exc}')
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('lock', r.stderr)
        self.assertEqual(self.out.read_text(), '# previous\n')
        self.assertEqual(external.read_text(), 'DO NOT TOUCH\n')
        self.assertEqual(lock.stat().st_ino, external.stat().st_ino)

    @unittest.skipUnless(hasattr(__import__('os'), 'mkfifo'), 'FIFO unavailable')
    def test_nonregular_lock_refused(self):
        import os
        self.base.write_text(row(GOOD, 2))
        self.out.write_text('# previous\n')
        os.mkfifo(self.root / 'out.csv.lock')
        r = self.runmerge(self.base)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn('lock', r.stderr)
        self.assertEqual(self.out.read_text(), '# previous\n')


if __name__ == '__main__':
    unittest.main()
