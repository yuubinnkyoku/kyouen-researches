import copy,unittest
from study import cases,compare,validate,expected
class ProtocolTests(unittest.TestCase):
    def rows(self):
        return [dict(result=0,reason='NODE_BUDGET',nodes=7,visited=1,expansions=1,exact_nodes=6,
            residual_calls=0,pn_nodes=0,pn_aborts=0,pn_remaining=128,pn_attempted=0,pn_attempt_skips=0,
            geometry_builds=3,geometry_moves=10,child_refreshes=0)]
    def test_matrix_coverage(self):
        data=cases();self.assertEqual(len(data),258)
        self.assertEqual(sum(len(c['roots']) for c in data),330)
        self.assertEqual(len({c['id'] for c in data}),258)
    def test_pair(self):
        a=self.rows();b=copy.deepcopy(a);b[0].update(geometry_builds=2,geometry_moves=7,child_refreshes=1);compare(a,b)
    def test_pn_usage_drift(self):
        a=self.rows();b=copy.deepcopy(a);b[0]['pn_nodes']=1
        with self.assertRaises(AssertionError):compare(a,b)
    def test_native_work_drift(self):
        a=self.rows();b=copy.deepcopy(a);b[0]['exact_nodes']=5
        with self.assertRaises(AssertionError):compare(a,b)
    def test_geometry_drift(self):
        a=self.rows();b=copy.deepcopy(a);b[0]['child_refreshes']=1
        with self.assertRaises(AssertionError):compare(a,b)
    def test_both_turns(self):
        self.assertIn(expected('odd'),(1,2));self.assertIn(expected('even'),(1,2))
    def test_wrong_publish_header(self):
        with self.assertRaises(AssertionError):validate('', 'exact_publish=root',cases()[0])
if __name__=='__main__':unittest.main()
