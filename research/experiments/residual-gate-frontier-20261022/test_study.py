import unittest
from study import histogram, validate


class ProtocolTests(unittest.TestCase):
    fixture = dict(occupied=[0, 1, 2, 11, 60], expected=0)

    def raw(self, **changes):
        fields = dict(seq=1, result=0, reason='NODE_BUDGET', stones=5,
            occupied_lo=sum(1 << v for v in self.fixture['occupied']), occupied_hi=0,
            nodes=10, visited=10, exact_nodes=0, node_limited=1, node_budget=10,
            residual_gate=0, residual_calls=0, pn_enabled=0, pn_budget=128,
            pn_nodes=0, pn_remaining=128, pn_aborts=0, build_ns=0, structure_ns=0, grundy_ns=0)
        fields.update(changes)
        return '# dfpn_root ' + ' '.join(f'{k}={v}' for k, v in fields.items()) + '\n'

    def test_valid(self):
        validate(self.raw(), self.fixture, 0, 10)

    def test_wrong_identity(self):
        with self.assertRaises(AssertionError):
            validate(self.raw(occupied_lo=1), self.fixture, 0, 10)

    def test_new_deep_verdict(self):
        with self.assertRaises(AssertionError):
            validate(self.raw(result=1, reason='DONE'), self.fixture, 0, 10)

    def test_histogram_bounds(self):
        for legal in (-1, 122):
            with self.assertRaises(AssertionError):
                histogram(f'# residual_gate_profile seq=1 legal={legal} frames=1')

    def test_histogram_duplicate(self):
        line = '# residual_gate_profile seq=1 legal=12 frames=2\n'
        with self.assertRaises(AssertionError):
            histogram(line + line)

    def test_histogram_partition(self):
        for count in (0, 11):
            with self.assertRaises(AssertionError):
                validate(self.raw() + f'# residual_gate_profile seq=1 legal=12 frames={count}', self.fixture, 0, 10, True)

    def test_profile_separate(self):
        raw = self.raw() + '# residual_gate_profile seq=1 legal=12 frames=5'
        self.assertEqual(validate(raw, self.fixture, 0, 10, True)['histogram'], {12: 5})
        with self.assertRaises(AssertionError):
            validate(raw, self.fixture, 0, 10)

    def test_quota_drift(self):
        with self.assertRaises(AssertionError):
            validate(self.raw(pn_remaining=127), self.fixture, 0, 10)


if __name__ == '__main__':
    unittest.main()
