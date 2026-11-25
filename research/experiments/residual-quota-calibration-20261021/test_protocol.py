import copy,pathlib,unittest
from calibrate import CONFIGS,select,adoption,parse
HERE=pathlib.Path(__file__).resolve().parent

def records():
    return [dict(split='train',config=c['name'],repeat=r,id=i,result=1,nodes=1,solve_us=100,setup_us=1000,pn_nodes=1,pn_aborts=0)
        for c in CONFIGS for r in range(3) for i in range(26)]

class Protocol(unittest.TestCase):
    def test_control_is_not_pn_candidate(self):
        rows=records()
        for r in rows:
            if r['config']=='off':r['solve_us']=0
        self.assertEqual(select(rows)['candidate']['name'],'q128-g6')
    def test_no_confirmation_leakage(self):
        rows=records();rows[0]['split']='new'
        with self.assertRaises(AssertionError):select(rows)
    def test_complete_three_repeats_required(self):
        rows=records()
        with self.assertRaises(AssertionError):select(rows[:-1])
        rows[0]['repeat']=1
        with self.assertRaises(AssertionError):select(rows)
    def test_unknown_priority(self):
        rows=records()
        for r in rows:
            if r['config']=='q128-g6':r['solve_us']=1;r['result']=0
        self.assertEqual(select(rows)['candidate']['name'],'q128-g12')
    def test_median_not_best_run(self):
        rows=records()
        for r in rows:
            if r['config']=='q128-g6':r['solve_us']=[1,100,100][r['repeat']]
            if r['config']=='q512-g6':r['solve_us']=50
        self.assertEqual(select(rows)['candidate']['name'],'q512-g6')
    def test_tie_quota_before_gate(self):
        rows=records()
        for r in rows:
            if r['config']=='q128-g6':r['solve_us']=101
        self.assertEqual(select(rows)['candidate']['name'],'q128-g12')
    def test_both_speed_checks_and_unknown(self):
        c=CONFIGS[1];p=c['name']
        good={s:{'off':dict(unknown=0,solve_us=100),p:dict(unknown=0,solve_us=90)} for s in ('new','stress')}
        self.assertTrue(adoption(good,c))
        bad=copy.deepcopy(good);bad['stress'][p]['solve_us']=101
        self.assertFalse(adoption(bad,c))
        bad=copy.deepcopy(good);bad['new'][p]['unknown']=1
        self.assertFalse(adoption(bad,c))
    def test_deep_new_verdict_stops(self):
        raw=(HERE.parent/'residual-outcome-search-20261021/raw/pn6-stress-r0.csv').read_text()
        c=dict(name='unit',gate=6,quota=100000)
        self.assertEqual(len(parse(raw,[{}]*3,'stress',c,0)),3)
        lines=raw.splitlines();i=next(i for i,s in enumerate(lines) if s.startswith('replay,'))
        row=lines[i].split(',');row[6]='1';lines[i]=','.join(row)
        with self.assertRaises(AssertionError):parse('\n'.join(lines),[{}]*3,'stress',c,0)
    def test_wrong_quota_stops(self):
        raw=(HERE.parent/'residual-outcome-search-20261021/raw/pn6-stress-r0.csv').read_text()
        with self.assertRaises(AssertionError):parse(raw,[{}]*3,'stress',CONFIGS[1],0)
if __name__=='__main__':unittest.main()
