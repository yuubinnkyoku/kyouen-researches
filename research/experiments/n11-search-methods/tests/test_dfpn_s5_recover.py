"""S5 cache recovery must not promote unknowns or hide contradictory results."""
import contextlib
import io
import json
import tempfile
import unittest
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from unittest.mock import patch

import dfpn_s5_recover as r
import s5_evidence_policy as policy

KEY=(1152921504606848001, 16777220)
KEY2=(1152921504606848001, 16777224)

def vertical_reflection(key):
    points = [i for i in range(121)
              if ((key[0] if i < 64 else key[1]) >> (i % 64)) & 1]
    mask = sum(1 << (11*(p//11) + (10-p%11)) for p in points)
    return (mask & ((1<<64)-1), mask>>64)

def qdone(key, verdict, nodes=20):
    return f'[q-done] q=7 key={key[0]},{key[1]} result={verdict} nodes={nodes} ms=1\n'

def replay(key, verdict, nodes=30, stones=5, is_or=0):
    return f'replay,0,{stones},80,{is_or},100,{verdict},{nodes},0.125,{key[0]},{key[1]}\n'

class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.registry = Path(self.tmpdir.name) / 'quarantine.json'
        self.write_registry([])
        self.registry_patch = patch.object(policy, 'REGISTRY', self.registry)
        self.registry_patch.start()
        self.addCleanup(self.registry_patch.stop)

    def write_registry(self, entries):
        self.registry.write_text(json.dumps({
            'schema': 'n11-s5-evidence-quarantine-v1',
            'entries': entries,
        }))

    def invoke(self, logs, cache=None):
        with tempfile.TemporaryDirectory() as tmp:
            files=[]
            for i, data in enumerate(logs):
                p=Path(tmp)/f'log{i}.txt';p.write_text(data);files.append(str(p))
            out=Path(tmp)/'worker.csv'
            args=files+['--out',str(out)]
            if cache is not None:
                p=Path(tmp)/'existing.csv';p.write_text(cache);args+=['--cache',str(p)]
            with patch('sys.argv',['recover.py']+args),contextlib.redirect_stdout(io.StringIO()) as stdout:
                code=r.main()
            return code, out.read_text() if out.exists() else None, stdout.getvalue()

    def test_float_wall_time_replay(self):
        code,out,_=self.invoke([replay(KEY,2,123)])
        self.assertEqual(code,0)
        self.assertIn(f's5verdict,{KEY[0]},{KEY[1]},5,2,123',out)

    def test_unknown_not_written(self):
        code,out,_=self.invoke([qdone(KEY,0)+replay(KEY2,0)])
        self.assertEqual(code,0)
        self.assertNotIn('s5verdict,',out)

    def test_conflicting_rows_in_one_log_refused(self):
        code,out,msg=self.invoke([qdone(KEY,1)+qdone(KEY,2)])
        self.assertEqual(code,1)
        self.assertIsNone(out)
        self.assertIn('CONFLICT',msg)

    def test_conflicting_rows_across_logs_refused(self):
        code,out,msg=self.invoke([qdone(KEY,1),replay(KEY,2)])
        self.assertEqual(code,1)
        self.assertIsNone(out)
        self.assertIn('CONFLICT',msg)

    def test_unknown_does_not_erase_decided(self):
        code,out,_=self.invoke([qdone(KEY,1)+qdone(KEY,0),qdone(KEY,0)])
        self.assertEqual(code,0)
        self.assertIn(f's5verdict,{KEY[0]},{KEY[1]},5,1,20',out)

    def test_wrong_layer_replay_refused(self):
        code,out,msg=self.invoke([replay(KEY,2,stones=6)])
        self.assertEqual(code,1)
        self.assertIsNone(out)
        self.assertIn('not an S5',msg)

    def test_duplicate_existing_cache_conflict_refused(self):
        existing=(f's5verdict,{KEY[0]},{KEY[1]},5,1,0\n'
                  f's5verdict,{KEY[0]},{KEY[1]},5,2,0\n')
        code,out,msg=self.invoke([qdone(KEY2,2)],existing)
        self.assertEqual(code,1)
        self.assertIsNone(out)
        self.assertIn('CONFLICT',msg)

    def test_existing_cache_conflict_refused(self):
        existing=f's5verdict,{KEY[0]},{KEY[1]},5,1,0\n'
        code,out,msg=self.invoke([qdone(KEY,2)],existing)
        self.assertEqual(code,1)
        self.assertIsNone(out)
        self.assertIn('CONFLICT',msg)

    def test_noncanonical_log_key_refused(self):
        alias = vertical_reflection(KEY)
        self.assertNotEqual(alias, KEY)
        self.assertFalse(policy.is_canonical_safe_s5_key(alias))
        code, out, msg = self.invoke([qdone(alias, 2)])
        self.assertEqual(code, 1)
        self.assertIsNone(out)
        self.assertIn('noncanonical or unsafe S5 key', msg)

    def test_unsafe_log_key_refused(self):
        # Canonical five points, but all are collinear on one row.
        key = (31, 0)
        self.assertFalse(policy.is_canonical_safe_s5_key(key))
        code, out, msg = self.invoke([qdone(key, 2)])
        self.assertEqual(code, 1)
        self.assertIsNone(out)
        self.assertIn('noncanonical or unsafe S5 key', msg)

    def test_malformed_existing_cache_refused(self):
        malformed = 's5verdict,1152921504606848001,16777220,5,2\n'
        code, out, msg = self.invoke([qdone(KEY2, 2)], malformed)
        self.assertEqual(code, 1)
        self.assertIsNone(out)
        self.assertIn('invalid S5 cache row', msg)

    def test_unknown_existing_cache_row_refused(self):
        unknown = f's5verdict,{KEY[0]},{KEY[1]},5,0,10\n'
        code, out, msg = self.invoke([qdone(KEY2, 2)], unknown)
        self.assertEqual(code, 1)
        self.assertIsNone(out)
        self.assertIn('invalid S5 evidence', msg)

    def test_quarantine_excluded_before_conflict_check(self):
        self.write_registry([{
            'key': list(KEY), 'active': True, 'unsupported_verdict': 1,
        }])
        existing = f's5verdict,{KEY[0]},{KEY[1]},5,1,0\n'
        code, out, msg = self.invoke([qdone(KEY, 2) + qdone(KEY2, 2)], existing)
        self.assertEqual(code, 0)
        self.assertNotIn(f's5verdict,{KEY[0]},{KEY[1]},5,', out)
        self.assertIn(f's5verdict,{KEY2[0]},{KEY2[1]},5,2,20', out)
        self.assertIn('quarantined verdicts : 1', msg)

    def test_missing_quarantine_registry_refused(self):
        self.registry.unlink()
        code, out, msg = self.invoke([qdone(KEY, 2)])
        self.assertEqual(code, 1)
        self.assertIsNone(out)
        self.assertIn('required S5 evidence quarantine registry missing', msg)

    def test_noncanonical_existing_cache_refused(self):
        cache = 's5verdict,31,0,5,2,10\n'
        code, out, msg = self.invoke([qdone(KEY2, 2)], cache)
        self.assertEqual(code, 1)
        self.assertIsNone(out)
        self.assertIn('noncanonical or unsafe S5 key', msg)

if __name__=='__main__':
    unittest.main()
