"""S5 quarantine registry parsing must reject duplicate JSON object keys."""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import sys

POLICY_DIR = Path(__file__).resolve().parents[2] / 'n11-frontier-selection-20261005/scripts'
sys.path.insert(0, str(POLICY_DIR))
import s5_evidence_policy as policy

KEY = [1152921504606848001, 16777220]


class DuplicateRegistryKeyTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.registry = Path(self.tmp.name) / 'registry.json'
        self.patch = patch.object(policy, 'REGISTRY', self.registry)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_duplicate_root_schema_key_refused(self):
        self.registry.write_text(
            '{"schema":"n11-s5-evidence-quarantine-v1",'
            '"schema":"n11-s5-evidence-quarantine-v1","entries":[]}',
            encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'duplicate JSON key: schema'):
            policy.quarantined_cache_keys()

    def test_duplicate_nested_active_key_refused(self):
        self.registry.write_text(
            '{"schema":"n11-s5-evidence-quarantine-v1","entries":[{'
            '"key":['+str(KEY[0])+','+str(KEY[1])+'],"active":true,'
            '"active":false,"unsupported_verdict":1}]}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'duplicate JSON key: active'):
            policy.quarantined_cache_keys()


if __name__ == '__main__':
    unittest.main()
