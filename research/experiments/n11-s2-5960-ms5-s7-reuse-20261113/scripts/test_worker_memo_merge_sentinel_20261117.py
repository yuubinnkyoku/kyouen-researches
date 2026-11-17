import itertools
import unittest

from worker_memo_merge import UNBOUND, combine_values, conflict_kind, max_bound


class SentinelAwareMemoMergeTests(unittest.TestCase):
    def test_max_bound_is_a_join_on_all_depths(self):
        domain = list(range(65)) + [UNBOUND]
        for a, b in itertools.product(domain, repeat=2):
            self.assertEqual(max_bound(a, b), max_bound(b, a))
            expected = b if a == UNBOUND else a if b == UNBOUND else max(a, b)
            self.assertEqual(max_bound(a, b), expected)
            self.assertEqual(max_bound(a, a), a)
        for a, b, c in itertools.product(domain, repeat=3):
            self.assertEqual(max_bound(max_bound(a, b), c),
                             max_bound(a, max_bound(b, c)))

    def test_unbound_is_identity_for_negative_bounds(self):
        for d in range(65):
            self.assertEqual(max_bound(d, UNBOUND), d)
            self.assertEqual(max_bound(UNBOUND, d), d)
        self.assertEqual(max_bound(UNBOUND, UNBOUND), UNBOUND)

    def test_cross_worker_contradictions_are_not_hidden(self):
        merged = combine_values(3, UNBOUND, UNBOUND, UNBOUND,
                                (UNBOUND, UNBOUND, 4, UNBOUND))
        self.assertEqual(merged, (3, UNBOUND, 4, UNBOUND))
        self.assertEqual(conflict_kind(*merged), "win_le_nowin")

        merged = combine_values(UNBOUND, 5, UNBOUND, UNBOUND,
                                (UNBOUND, UNBOUND, UNBOUND, 6))
        self.assertEqual(merged, (UNBOUND, 5, UNBOUND, 6))
        self.assertEqual(conflict_kind(*merged), "lose_le_nolose")

    def test_f5_information_is_preserved_without_false_conflict(self):
        nowin = combine_values(7, UNBOUND, UNBOUND, UNBOUND,
                               (UNBOUND, UNBOUND, 4, UNBOUND))
        nolose6 = combine_values(UNBOUND, 6, UNBOUND, UNBOUND,
                                 (UNBOUND, UNBOUND, UNBOUND, 2))
        nolose4 = combine_values(UNBOUND, 4, UNBOUND, UNBOUND,
                                 (UNBOUND, UNBOUND, UNBOUND, 2))
        self.assertEqual(nowin, (7, UNBOUND, 4, UNBOUND))
        self.assertEqual(nolose6, (UNBOUND, 6, UNBOUND, 2))
        self.assertEqual(nolose4, (UNBOUND, 4, UNBOUND, 2))
        self.assertIsNone(conflict_kind(*nowin))
        self.assertIsNone(conflict_kind(*nolose6))
        self.assertIsNone(conflict_kind(*nolose4))

    def test_existing_verbatim_measurement_values_are_unchanged(self):
        self.assertEqual(combine_values(3, 7, 255, 255, (5, 2, 255, 255)),
                         (3, 2, 255, 255))
        self.assertEqual(combine_values(255, 255, 255, 255,
                                        (255, 255, 255, 255)),
                         (255, 255, 255, 255))

    def test_merge_is_associative_for_complete_records(self):
        samples = [
            (255, 255, 255, 255),
            (3, 255, 4, 255),
            (255, 5, 255, 6),
            (2, 7, 1, 8),
            (64, 64, 0, 0),
        ]

        def merge(a, b):
            return combine_values(*a, b)

        for a, b, c in itertools.product(samples, repeat=3):
            self.assertEqual(merge(merge(a, b), c),
                             merge(a, merge(b, c)))


if __name__ == "__main__":
    unittest.main(verbosity=2)
