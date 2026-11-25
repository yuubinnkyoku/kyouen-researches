import unittest
from study import validate,pair

class ProtocolTests(unittest.TestCase):
    fixture=dict(occupied=[0,1,2,11,60],expected=0)
    def row(self,**changes):
        r=dict(seq=1,result=0,reason='NODE_BUDGET',stones=5,
            occupied_lo=sum(1<<v for v in self.fixture['occupied']),occupied_hi=0,
            nodes=10,visited=10,expansions=4,exact_nodes=0,node_limited=1,node_budget=10,
            residual_gate=0,residual_calls=0,pn_enabled=0,pn_budget=128,pn_nodes=0,pn_remaining=128,
            frame_cache=1,frame_audit=0,geometry_builds=6,geometry_moves=100,child_refreshes=4,child_audits=0,
            build_ns=0,structure_ns=0,grundy_ns=0)
        r.update(changes);return r
    def raw(self,**changes):return '# dfpn_root '+' '.join(f'{k}={v}' for k,v in self.row(**changes).items())+'\n'
    def test_valid(self):validate(self.raw(),self.fixture,True,10)
    def test_identity(self):
        with self.assertRaises(AssertionError):validate(self.raw(occupied_lo=0),self.fixture,True,10)
    def test_new_deep_verdict(self):
        with self.assertRaises(AssertionError):validate(self.raw(result=1,reason='DONE'),self.fixture,True,10)
    def test_audit_mixed_into_timing(self):
        with self.assertRaises(AssertionError):validate(self.raw(child_audits=4),self.fixture,True,10)
    def test_audit_count(self):
        with self.assertRaises(AssertionError):validate(self.raw(frame_audit=1,child_audits=3),self.fixture,True,10,True)
    def test_pair(self):pair(self.row(frame_cache=0,geometry_builds=10,geometry_moves=150,child_refreshes=0),self.row())
    def test_logical_drift(self):
        with self.assertRaises(AssertionError):pair(self.row(geometry_builds=10),self.row(expansions=5))
    def test_substitution_drift(self):
        with self.assertRaises(AssertionError):pair(self.row(geometry_builds=11),self.row())
    def test_geometry_increase(self):
        with self.assertRaises(AssertionError):pair(self.row(geometry_builds=10,geometry_moves=90),self.row())

if __name__=='__main__':unittest.main()
