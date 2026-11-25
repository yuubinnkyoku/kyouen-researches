import copy
import unittest
from joint_plan_checks import audit_joint_entries


class JointPlanChecksTests(unittest.TestCase):
    def setUp(self):
        self.entry = {"first": 49, "reply": 60, "third": 0,
                      "s4_class_index": 1, "s4_mask": [8, 0],
                      "unknown_s5_children": 2}
        self.options = {(49, 60, 0): {1}}
        self.masks = [4, 8]
        self.cost = [{20, 21}, {20, 21}]

    def audit(self, entries, expected=None):
        failures, checked = [], []
        union = audit_joint_entries(entries,
            {(49, 60, 0)} if expected is None else expected,
            self.options, self.masks, self.cost, checked.append, failures)
        return failures, union, checked

    def test_valid(self):
        errors, union, checked = self.audit([self.entry])
        self.assertEqual((errors, union, checked), ([], {20, 21}, [1]))

    def test_illegal_s4_same_union(self):
        bad = self.entry | {"s4_class_index": 0, "s4_mask": [4, 0]}
        self.assertEqual(self.cost[0], self.cost[1])
        self.assertTrue(any("not a legal response" in e for e in self.audit([bad])[0]))

    def test_duplicate_entry(self):
        self.assertTrue(any("duplicate" in e for e in self.audit([self.entry, copy.deepcopy(self.entry)])[0]))

    def test_missing_entry(self):
        self.assertTrue(any("missing=1" in e for e in self.audit([])[0]))

    def test_free_third_injected(self):
        self.assertTrue(any("unknown or free" in e for e in self.audit([self.entry, self.entry | {"third": 1}])[0]))

    def test_mask_mismatch(self):
        self.assertTrue(any("mask mismatch" in e for e in self.audit([self.entry | {"s4_mask": [4, 0]}])[0]))

    def test_cost_count_mismatch(self):
        self.assertTrue(any("count mismatch" in e for e in self.audit([self.entry | {"unknown_s5_children": 1}])[0]))

    def test_bool_index_rejected(self):
        self.assertTrue(any("invalid S4 index" in e for e in self.audit([self.entry | {"s4_class_index": True}])[0]))

    def test_noninteger_coordinates_rejected(self):
        self.assertTrue(any("invalid first" in e for e in self.audit([self.entry | {"first": 49.0}])[0]))


if __name__ == "__main__":
    unittest.main()
