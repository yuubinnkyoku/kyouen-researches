import pathlib,unittest
from integration import expected_late
from bench import parse_root
HERE=pathlib.Path(__file__).resolve().parent

class Protocol(unittest.TestCase):
    def setUp(self):
        raw=(HERE/'raw/integration-late-0.csv').read_text()
        self.raw=next(s for s in raw.splitlines() if s.startswith('# dfpn_root '))+'\n'
        # The integration CLI record has phase profiling enabled; the timed
        # comparison must reject it until the synthetic test clears clocks.
        words=self.raw.split()
        self.raw=' '.join(w.split('=')[0]+'=0' if w.startswith(('build_ns=','structure_ns=','grundy_ns=')) else w for w in words)+'\n'
        self.fixture=dict(id=0,group='late',occupied=[0,1,2,4,9],expected=expected_late([0,1,2,4,9]))
    def parse(self,raw):return parse_root(raw,self.fixture,'pn128-g6',1,0)
    def replace(self,raw,key,value):
        return ' '.join(f'{key}={value}' if w.startswith(key+'=') else w for w in raw.split())+'\n'
    def test_valid_record(self):
        r=self.parse(self.raw);self.assertEqual(r['nodes'],1);self.assertEqual(r['pn_nodes'],1)
    def test_wrong_position(self):
        with self.assertRaises(AssertionError):self.parse(self.replace(self.raw,'occupied_lo',0))
    def test_wrong_verdict(self):
        with self.assertRaises(AssertionError):self.parse(self.replace(self.raw,'result',3-self.fixture['expected']))
    def test_extra_record(self):
        with self.assertRaises(AssertionError):self.parse(self.raw+self.raw)
    def test_budget_overrun(self):
        with self.assertRaises(AssertionError):self.parse(self.replace(self.raw,'nodes',2))
    def test_quota_drift(self):
        with self.assertRaises(AssertionError):self.parse(self.replace(self.raw,'pn_budget',512))
    def test_profile_is_excluded(self):
        with self.assertRaises(AssertionError):self.parse(self.replace(self.raw,'build_ns',1))
    def test_new_deep_verdict_stops(self):
        f={**self.fixture,'group':'deep','expected':0}
        with self.assertRaises(AssertionError):parse_root(self.raw,f,'pn128-g6',1,0)
if __name__=='__main__':unittest.main()
