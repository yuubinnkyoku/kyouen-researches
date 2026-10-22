import unittest
from study import compare,validate
class ProtocolTests(unittest.TestCase):
    def rows(self):
        shared=dict(result=0,reason='NODE_BUDGET',nodes=10,visited=10,expansions=4,exact_nodes=0,pn_nodes=0,residual_calls=0)
        return [dict(shared,geometry_builds=10,geometry_moves=100,child_refreshes=0,frame_expand_uses=0),
                dict(shared,geometry_builds=6,geometry_moves=60,child_refreshes=4,frame_expand_uses=0),
                dict(shared,geometry_builds=3,geometry_moves=30,child_refreshes=7,frame_expand_uses=3)]
    def test_valid(self):compare(*self.rows())
    def test_initial_use_count(self):
        rows=self.rows();rows[2]['frame_expand_uses']=2
        with self.assertRaises(AssertionError):compare(*rows)
    def test_initial_refresh_count(self):
        rows=self.rows();rows[2]['child_refreshes']=6
        with self.assertRaises(AssertionError):compare(*rows)
    def test_logical_drift(self):
        rows=self.rows();rows[2]['expansions']=5
        with self.assertRaises(AssertionError):compare(*rows)
    def test_geometry_increase(self):
        rows=self.rows();rows[2]['geometry_moves']=61
        with self.assertRaises(AssertionError):compare(*rows)
if __name__=='__main__':unittest.main()
