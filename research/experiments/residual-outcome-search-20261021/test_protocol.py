import pathlib,unittest
import run
HERE=pathlib.Path(__file__).resolve().parent
class Protocol(unittest.TestCase):
    def setUp(self):
        self.raw=(HERE/'raw/pn6-saved-r0.csv').read_text()
        self.config=('pn6',6,'outcome')
    def test_complete(self):
        self.assertEqual(len(run.parse(self.raw,'saved',self.config,0)),52)
    def test_missing_outcome_counter(self):
        raw='\n'.join(s for s in self.raw.splitlines() if not s.startswith('# residual_outcome row=0 '))
        with self.assertRaises(AssertionError):run.parse(raw,'saved',self.config,0)
    def test_wrong_quota(self):
        lines=self.raw.splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('# residual_outcome '))
        lines[i]=lines[i].replace('nodes=','nodes=1',1)
        with self.assertRaises(AssertionError):run.parse('\n'.join(lines),'saved',self.config,0)
    def test_aborted_with_unused_credit(self):
        raw=self.raw.replace('aborts=0','aborts=1')
        with self.assertRaises(AssertionError):run.parse(raw,'saved',self.config,0)
    def test_wrong_verdict(self):
        lines=self.raw.splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('replay,'))
        row=lines[i].split(',');row[6]='0';lines[i]=','.join(row)
        with self.assertRaises(AssertionError):run.parse('\n'.join(lines),'saved',self.config,0)
    def test_incomplete_or_duplicate(self):
        raw='\n'.join(s for s in self.raw.splitlines() if not s.startswith('# replay_done '))
        with self.assertRaises(AssertionError):run.parse(raw,'saved',self.config,0)
        with self.assertRaises(AssertionError):run.parse(self.raw+self.raw,'saved',self.config,0)
    def test_new_stress_verdict(self):
        raw=(HERE/'raw/pn6-stress-r0.csv').read_text();lines=raw.splitlines()
        i=next(i for i,s in enumerate(lines) if s.startswith('replay,'));row=lines[i].split(',');row[6]='1';lines[i]=','.join(row)
        with self.assertRaises(AssertionError):run.parse('\n'.join(lines),'stress',self.config,0)
if __name__=='__main__':unittest.main()
