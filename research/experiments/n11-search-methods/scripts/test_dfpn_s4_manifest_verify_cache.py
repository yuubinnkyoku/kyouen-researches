#!/usr/bin/env python3
"""Fail-closed regression tests for the independent S4 manifest's S5 inputs.

Run from the repository root:
  python3 -m unittest discover -s research/experiments/n11-search-methods/scripts -p 'test_dfpn_s4_manifest_verify_cache.py'
"""
import json
import tempfile
import unittest
from pathlib import Path

from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad
from dfpn_s4_manifest_verify import load_s5_cache

# Independently saved, canonical, safe S5 keys.  The tests never assume
# these labels are a proof of their game-theoretic verdicts.
A = (1152921504742115328, 536870912)
B = (3602879701897445376, 134217728)


def row(key, verdict, nodes=12):
    return f's5verdict,{key[0]},{key[1]},5,{verdict},{nodes}\n'


class S5ManifestInputTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.cache = Path(self.tmp.name) / 'worker.csv'

    def read(self, data):
        self.cache.write_text(data, encoding='utf-8')
        return load_s5_cache(self.cache)

    def test_valid_rows_and_same_verdict_duplicates(self):
        self.assertEqual(self.read(row(A, 2) + row(A, 2, 3) + row(B, 1)),
                         {A: 2, B: 1})

    def test_conflicting_duplicates_fail_in_both_orders(self):
        for left, right in ((1, 2), (2, 1)):
            with self.subTest(left=left):
                with self.assertRaisesRegex(ValueError, 'CONFLICT'):
                    self.read(row(A, left) + row(A, right))

    def test_unknown_never_certifies(self):
        self.assertEqual(self.read(row(A, 0) + row(B, 1)), {B: 1})

    def test_malformed_or_negative_evidence_fails(self):
        for data in ('other,1,2,3,4,5\n', row(A, 2, -1),
                     's5verdict,garbled,0,5,2,10\n',
                     f's5verdict,{A[0]},{A[1]},4,2,10\n'):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self.read(data)

    def test_noncanonical_d4_alias_fails(self):
        # Reflect A horizontally; it is safe but not the canonical key.
        pts = [11, 20, 27, 60, 93]
        reflected = [(10 - p % 11) + 11 * (p // 11) for p in pts]
        mask = sum(1 << p for p in reflected)
        alias = (mask & ((1 << 64) - 1), mask >> 64)
        self.assertNotEqual(alias, d4_canonical_key(reflected))
        with self.assertRaisesRegex(ValueError, 'noncanonical'):
            self.read(row(alias, 2))

    def test_unsafe_canonical_key_fails(self):
        pts = [0, 1, 2, 3, 4]  # Four collinear points are forbidden.
        self.assertTrue(has_forbidden_quad(pts))
        with self.assertRaisesRegex(ValueError, 'unsafe'):
            self.read(row(d4_canonical_key(pts), 2))

    def test_quarantined_verdict_is_not_a_witness(self):
        registry = (Path(__file__).resolve().parents[4]
                    / 'results/n11-s5-evidence-quarantine.json')
        doc = json.loads(registry.read_text(encoding='utf-8'))
        active = {tuple(row['key']) for row in doc['entries'] if row['active']}
        if not active:
            self.skipTest('no active quarantined keys')
        key = sorted(active)[0]
        self.assertEqual(self.read(row(key, 1) + row(A, 2)), {A: 2})


if __name__ == '__main__':
    unittest.main()
