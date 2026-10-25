#!/usr/bin/env python3
"""Fail-closed regression tests for the independent S4 manifest's S5 inputs.

Run from the repository root:
  python3 -m unittest discover -s research/experiments/n11-search-methods/scripts -p 'test_dfpn_s4_manifest_verify_cache.py'
"""
import contextlib
import io
import json
import tempfile
import unittest
from unittest import mock
from pathlib import Path

from dfpn_edge_classes import d4_canonical_key, has_forbidden_quad, legal_after
from dfpn_s4_manifest_verify import (load_s5_cache, load_manifest,
                                     build_s4_edge_index, is_s5_child_of_s4)

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


class S4ManifestStructureTests(unittest.TestCase):
    """Structural rejection must happen before expensive board enumeration."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.manifest = Path(self.tmp.name) / 's4.csv'
        lo, hi = d4_canonical_key([60, 0, 1, 2])
        self.valid = (f's4verdict,60,0,{lo},{hi},2,2,2,'
                      f'{A[0]},{A[1]},{B[0]},{B[1]}\n')

    def parse(self, text):
        self.manifest.write_text(text, encoding='utf-8')
        return load_manifest(self.manifest)

    def test_valid_shape_and_comments(self):
        self.assertEqual(len(self.parse('# header\n' + self.valid)), 1)

    def test_empty_or_comment_only_is_not_verified(self):
        for data in ('', '# header\n', '\n'):
            with self.subTest(data=data):
                with self.assertRaisesRegex(ValueError, 'empty S4 manifest'):
                    self.parse(data)

    def test_unknown_rows_cannot_disappear_silently(self):
        for data in ('unexpected,1,2\n', self.valid + 'bad,0\n'):
            with self.subTest(data=data):
                with self.assertRaisesRegex(ValueError, 'unexpected S4'):
                    self.parse(data)

    def test_duplicate_root_class_claims_fail_closed(self):
        # A repeated certificate must not inflate the number of verified
        # classes, even when its verdict and children agree byte for byte.
        for data in (self.valid + self.valid,
                     self.valid + self.valid.replace(',2,2,2,', ',1,2,2,')):
            with self.subTest(data=data):
                with self.assertRaisesRegex(ValueError, 'duplicate S4'):
                    self.parse(data)

    def test_same_board_key_for_distinct_roots_is_not_a_duplicate(self):
        # The same four-stone board can occur under two ordered openings;
        # each root has its own edge coverage obligation.
        reversed_root = self.valid.replace('s4verdict,60,0,',
                                           's4verdict,0,60,')
        self.assertEqual(len(self.parse(self.valid + reversed_root)), 2)

    def test_child_count_and_header_truncation(self):
        for data in ('s4verdict,60,0,1,0,2,1\n',
                     self.valid.replace(',2,2,2,', ',2,-1,2,'),
                     self.valid.replace(',2,2,2,', ',2,3,2,'),
                     self.valid + 's4verdict,60,0,1\n'):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self.parse(data)

    def test_out_of_range_roots_and_masks(self):
        lo, hi = d4_canonical_key([60, 0, 1, 2])
        for data in (
            self.valid.replace('s4verdict,60,0,', 's4verdict,121,0,'),
            self.valid.replace('s4verdict,60,0,', 's4verdict,60,60,'),
            self.valid.replace(f',{lo},{hi},2,', ',0,0,2,'),
            self.valid.replace(f',{A[0]},{A[1]},', ',-1,0,'),
            self.valid.replace(',2,2,2,', ',0,2,2,'),
        ):
            with self.subTest(data=data):
                with self.assertRaises(ValueError):
                    self.parse(data)



class S4RootEdgeIndexTests(unittest.TestCase):
    """An independent full-four enumeration must agree with the new index."""

    def test_center_corner_complete_partition(self):
        got = build_s4_edge_index(60, 0)
        self.assertEqual(len(got), 3396)
        self.assertEqual(sum(map(len, got.values())), 6894)
        expected = {}
        vertices = legal_after({60, 0})
        for a in vertices:
            for b in vertices:
                if a >= b or has_forbidden_quad([60, 0, a, b]):
                    continue
                key = d4_canonical_key([60, 0, a, b])
                expected.setdefault(key, []).append((a, b))
        self.assertEqual(dict(got), expected)

    def test_loss_child_set_identical_across_d4_equivalent_edges(self):
        # The LOSS verifier enumerates fifth moves for only one raw edge.
        # Check the exact invariant against independently enumerated
        # children of every other edge in 12 deterministic classes per root.
        for root in ((60, 0), (60, 27)):
            index = build_s4_edge_index(*root)
            selected = [(key, edges) for key, edges in index.items()
                        if len(edges) > 1][:12]
            self.assertEqual(len(selected), 12)
            for key, edges in selected:
                with self.subTest(root=root, key=key, n_edges=len(edges)):
                    child_sets = []
                    for a, b in edges:
                        children = {
                            d4_canonical_key((*root, a, b, z))
                            for z in legal_after(set(root) | {a, b})
                        }
                        child_sets.append(children)
                    self.assertTrue(child_sets[0])
                    for children in child_sets[1:]:
                        self.assertEqual(children, child_sets[0])

    def test_win_subset_membership_matches_full_legal_children(self):
        # Independent, exhaustive child enumeration is the oracle.  The
        # optimized WIN check must accept exactly the same D4 child keys.
        root = (60, 0)
        index = build_s4_edge_index(*root)
        targets = [key for key, edges in index.items() if len(edges) == 2][:3]
        self.assertEqual(len(targets), 3)
        candidates = set()
        for other, edges in list(index.items())[:12]:
            a, b = edges[0]
            for z in legal_after(set(root) | {a, b})[:5]:
                candidates.add(d4_canonical_key((*root, a, b, z)))
        positive = negative = 0
        for key in targets:
            expected = set()
            for a, b in index[key]:
                for z in legal_after(set(root) | {a, b}):
                    expected.add(d4_canonical_key((*root, a, b, z)))
            for child in expected | candidates:
                observed = is_s5_child_of_s4(child, key)
                self.assertEqual(observed, child in expected,
                                 (key, child))
                positive += int(observed)
                negative += int(not observed)
        self.assertGreater(positive, 0)
        self.assertGreater(negative, 0)

    def test_reversed_root_and_reply27(self):
        self.assertEqual(build_s4_edge_index(60, 0),
                         build_s4_edge_index(0, 60))
        other = build_s4_edge_index(60, 27)
        self.assertEqual(len(other), 3384)
        self.assertEqual(sum(map(len, other.values())), 6871)

class S4ManifestExecutionTests(unittest.TestCase):
    """Exercise main() itself, not just its input parser and edge index.

    This is a synthetic single-edge certificate over real legal 11x11
    fifth moves. It checks the verifier's control flow, not a new verdict.
    """

    def test_loss_win_and_truncated_loss_end_to_end(self):
        from dfpn_s4_manifest_verify import main as verify_main

        root = (60, 0)
        edge = (1, 2)
        four = (*root, *edge)
        self.assertFalse(has_forbidden_quad(four))
        key = d4_canonical_key(four)
        children = sorted({d4_canonical_key((*four, z))
                           for z in legal_after(set(four))})
        self.assertGreater(len(children), 1)

        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / 'manifest.csv'
            cache_path = Path(tmp) / 'unused-cache.csv'
            for verdict, listed, cache, expected in (
                (2, children, {child: 2 for child in children}, 0),
                (1, children[:1], {children[0]: 1}, 0),
                (2, children[:-1], {child: 2 for child in children}, 1),
            ):
                with self.subTest(verdict=verdict, expected=expected):
                    fields = ['s4verdict', *map(str, root),
                              *map(str, key), str(verdict),
                              str(len(listed)), '2']
                    for lo, hi in listed:
                        fields.extend((str(lo), str(hi)))
                    manifest.write_text(','.join(fields) + '\n',
                                        encoding='utf-8')
                    with (mock.patch('dfpn_s4_manifest_verify.load_s5_cache',
                                     return_value=cache),
                          mock.patch('dfpn_s4_manifest_verify.build_s4_edge_index',
                                     return_value={key: [edge]}),
                          mock.patch('sys.argv', ['verify', str(manifest),
                                                  '--cache', str(cache_path)]),
                          contextlib.redirect_stdout(io.StringIO()) as output):
                        self.assertEqual(verify_main(), expected)
                    self.assertIn('MANIFEST_VERIFIED' if expected == 0
                                  else 'MANIFEST_INVALID', output.getvalue())


    def test_real_edge_index_and_real_s5_cache_end_to_end(self):
        """No mocked index or cache: two D4 classes share one real root.

        The root {0,60} has a two-element stabilizer (diagonal reflection).
        Each listed pair below is the complete raw-edge orbit of its class.
        Synthetic verdict labels exercise only certificate plumbing.
        """
        from dfpn_s4_manifest_verify import main as verify_main

        root = (60, 0)
        classes = (
            (((1, 2), (11, 22)), 2),  # universal LOSS certificate
            (((3, 4), (33, 44)), 1),  # existential WIN witness
        )
        manifest_rows = []
        cache_rows = {}
        for edges, verdict in classes:
            key = d4_canonical_key((*root, *edges[0]))
            self.assertEqual({d4_canonical_key((*root, *edge))
                              for edge in edges}, {key})
            children = sorted({
                d4_canonical_key((*root, *edge, z))
                for edge in edges
                for z in legal_after(set(root) | set(edge))
            })
            self.assertTrue(children)
            listed = children if verdict == 2 else children[:1]
            for child in listed:
                self.assertNotIn(child, cache_rows)
                cache_rows[child] = verdict
            fields = ['s4verdict', *map(str, root), *map(str, key),
                      str(verdict), str(len(listed)),
                      str(len({p for edge in edges for p in edge}))]
            for lo, hi in listed:
                fields.extend((str(lo), str(hi)))
            manifest_rows.append(','.join(fields))

        with tempfile.TemporaryDirectory() as tmp:
            manifest = Path(tmp) / 'manifest.csv'
            cache_path = Path(tmp) / 's5.csv'
            manifest.write_text('\n'.join(manifest_rows) + '\n',
                                encoding='utf-8')
            cache_path.write_text(
                ''.join(row(key, verdict)
                        for key, verdict in sorted(cache_rows.items())),
                encoding='utf-8')
            with (mock.patch('sys.argv', ['verify', str(manifest),
                                          '--cache', str(cache_path)]),
                  contextlib.redirect_stdout(io.StringIO()) as output):
                self.assertEqual(verify_main(), 0, output.getvalue())
            self.assertIn('classes verified  : LOSS=1 WIN=1',
                          output.getvalue())
            self.assertIn('MANIFEST_VERIFIED', output.getvalue())


if __name__ == '__main__':
    unittest.main()
