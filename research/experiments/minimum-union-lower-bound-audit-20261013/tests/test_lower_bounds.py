"""Regression cases for an invalid option constraint and its pool replacement."""
from pathlib import Path
import sys
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))
from audit_lower_bounds import check_instance, make_instance, historical_bound  # noqa: E402


class LowerBoundRegression(unittest.TestCase):
    def test_unchosen_option_need_not_intersect_union(self):
        inst = make_instance([[0, 1]], [{0}, {1}])
        self.assertEqual(historical_bound(inst), 2)
        result = check_instance(inst)
        self.assertEqual(result["optimum"], 1)
        self.assertEqual(result["pool_bound_exact"], [1, 1])

    def test_fractional_pool_packing_triangle(self):
        inst = make_instance([[0, 1], [0, 2], [1, 2]], [{0}, {1}, {2}])
        result = check_instance(inst)
        self.assertEqual(result["optimum"], 2)
        self.assertEqual(result["pool_bound_exact"], [3, 2])

    def test_disjoint_groups_and_shared_alternatives(self):
        inst = make_instance([[0, 1], [2, 3], [0, 1]], [{0}, {1}, {2, 3}, {4, 5}])
        result = check_instance(inst)
        self.assertEqual(result["optimum"], 3)
        self.assertEqual(result["pool_bound_exact"], [3, 1])

    def test_free_and_empty_group_collections(self):
        for groups, cost in (([], []), ([[0, 1]], [set(), {0}]),
                             ([[0], [1, 2]], [set(), {0}, {1}])):
            with self.subTest(groups=groups):
                check_instance(make_instance(groups, cost))


if __name__ == "__main__":
    unittest.main()
