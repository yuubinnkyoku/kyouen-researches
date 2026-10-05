"""Regression tests for normalization and the exact-evidence trust boundary."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from derive_shared_s6_witness_cache import canonical_safe_key, verify_relations
from merge_exact_s5_evidence import merge

OUTPUT=Path(__file__).resolve().parents[1]/"output"


class RecoveryTests(unittest.TestCase):
    def setUp(self):
        self.meta=json.loads((OUTPUT/"reply27-current-shared16-s6.json").read_text())

    def test_historical_representatives_are_equivalent(self):
        probes,relations,parents,normalized=verify_relations(self.meta)
        self.assertEqual((len(probes),relations,parents,normalized),(16,66,65,13))
        canonical=copy.deepcopy(self.meta)
        for p in canonical['probes']:
            p['key']=list(canonical_safe_key(tuple(p['key']),6))
        self.assertEqual(verify_relations(canonical)[:3],(probes,66,65))
        self.assertEqual(verify_relations(canonical)[3],0)

    def test_unsafe_and_out_of_board_rejected(self):
        for key in ((63,0),(-1,0),(0,1<<57)):
            with self.subTest(key=key), self.assertRaises(SystemExit):
                canonical_safe_key(key,6)

    def test_fabricated_parent_rejected(self):
        self.meta['probes'][0]['parents'][0]=self.meta['probes'][5]['parents'][0]
        with self.assertRaisesRegex(SystemExit,'invalid parent relation'):
            verify_relations(self.meta)

    def test_duplicate_d4_probe_rejected(self):
        self.meta['probes'][1]=copy.deepcopy(self.meta['probes'][0])
        with self.assertRaisesRegex(SystemExit,'duplicate D4 probe'):
            verify_relations(self.meta)

    def test_merge_unknown_is_not_a_verdict_and_conflict_fails(self):
        key=(1334191389609558016,0)
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp); cache=p/'s5.cache'; replay=p/'out.csv'
            cache.write_text(f's5verdict,{key[0]},0,5,2,0\n')
            replay.write_text(f'replay,0,5,92,0,100,0,100,0,{key[0]},0\n')
            verdict,receipt=merge([cache],[str(replay)])
            self.assertEqual(verdict,{key:2})
            self.assertEqual(receipt['sources'][1]['counts'],{0:1})
            replay.write_text(f'replay,0,5,92,0,100,1,20,0,{key[0]},0\n')
            with self.assertRaisesRegex(SystemExit,'CONFLICT'):
                merge([cache],[str(replay)])

    def test_wrong_replay_parity_and_error_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            replay=Path(tmp)/'out.csv'
            for text in ('replay,0,5,92,1,100,2,20,0,1334191389609558016,0\n',
                         'replay_error,0,5,0,unsafe\n'):
                replay.write_text(text)
                with self.assertRaisesRegex(SystemExit,'not an s5 AND replay row'):
                    merge([],[str(replay)])


if __name__=='__main__':
    unittest.main()
