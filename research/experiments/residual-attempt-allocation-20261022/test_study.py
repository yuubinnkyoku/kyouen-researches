import unittest
from study import validate, select

class ProtocolTests(unittest.TestCase):
    fixture = dict(occupied=[0, 1, 2, 11, 60], expected=0)
    def raw(self, **changes):
        fields = dict(seq=1, result=0, reason='NODE_BUDGET', stones=5,
            occupied_lo=sum(1 << v for v in self.fixture['occupied']), occupied_hi=0,
            nodes=10, visited=10, exact_nodes=0, node_limited=1, node_budget=10,
            residual_gate=18, residual_calls=4, pn_enabled=1, pn_budget=128,
            pn_nodes=32, pn_remaining=96, pn_aborts=4, pn_attempt_budget=8, pn_attempted=4,
            pn_attempt_skips=2, pn_attempt_max=8, build_ns=0, structure_ns=0, grundy_ns=0)
        fields.update(changes)
        return '# dfpn_root ' + ' '.join(f'{k}={v}' for k, v in fields.items()) + '\n'
    def test_valid(self): validate(self.raw(), self.fixture, 'slice8', 10)
    def reject(self, **changes):
        with self.assertRaises(AssertionError): validate(self.raw(**changes), self.fixture, 'slice8', 10)
    def test_wrong_root(self): self.reject(occupied_lo=1)
    def test_quota_drift(self): self.reject(pn_remaining=95)
    def test_cap_exceeded(self): self.reject(pn_attempt_max=9)
    def test_attempt_count(self): self.reject(pn_attempted=3)
    def test_cap_total(self): self.reject(pn_nodes=33, pn_remaining=95)
    def test_fake_aborts(self): self.reject(pn_aborts=5)
    def test_partial_abort_without_exhaustion(self): self.reject(pn_nodes=31, pn_remaining=97)
    def test_new_deep_result(self): self.reject(result=1, reason='DONE')
    def test_clock(self): self.reject(build_ns=1)
    def test_selection_prefers_expansions(self):
        totals = {'n20000-slice8': dict(unknown=9, expansions=10, solve_us=200),
                  'n20000-slice32': dict(unknown=9, expansions=11, solve_us=100)}
        self.assertEqual(select(totals), 'slice8')

if __name__ == '__main__': unittest.main()
