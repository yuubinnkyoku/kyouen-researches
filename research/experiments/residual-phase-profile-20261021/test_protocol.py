import pathlib,unittest
import run
HERE=pathlib.Path(__file__).resolve().parent
class Protocol(unittest.TestCase):
    def setUp(self):
        self.raw=(HERE/'raw/scan-profile-saved-g6-r0.csv').read_text()
    def test_archive(self):
        self.assertEqual(len(run.parse(self.raw,'saved',6,True)),52)
    def test_missing_phase(self):
        raw='\n'.join(s for s in self.raw.splitlines() if not s.startswith('# residual_profile row=0 '))
        with self.assertRaises(AssertionError):run.parse(raw,'saved',6,True)
    def test_error(self):
        with self.assertRaises(AssertionError):run.parse(self.raw+'\nreplay_error,0,bad','saved',6,True)
    def test_wrong_verdict(self):
        lines=self.raw.splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('replay,'))
        row=lines[i].split(',');row[6]='0';lines[i]=','.join(row)
        with self.assertRaises(AssertionError):run.parse('\n'.join(lines),'saved',6,True)
    def test_wrong_budget(self):
        raw=self.raw.replace(',5000,',',5001,')
        with self.assertRaises(AssertionError):run.parse(raw,'saved',6,True)
    def test_new_stress_verdict_stops(self):
        raw=(HERE/'raw/scan-profile-stress-g6-r0.csv').read_text()
        lines=raw.splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('replay,'))
        row=lines[i].split(',');row[6]='1';lines[i]=','.join(row)
        with self.assertRaises(AssertionError):run.parse('\n'.join(lines),'stress',6,True)
if __name__=='__main__':unittest.main()
