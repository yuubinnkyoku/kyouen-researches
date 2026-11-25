"""Guard selection against holdout leakage and reject inconsistent replay data."""
import unittest
import run

class ProtocolTests(unittest.TestCase):
    def records(self):
        records=[]
        for gate in run.GATES:
            for i in range(52):
                for repeat in range(2):
                    records.append(dict(id=i,gate=gate,repeat=repeat,split='train' if i<26 else 'holdout',
                        result=1,nodes=7,residual_calls=0,residual_memo=0,setup_us=20,total_us=100,
                        solve_us=10 if (gate==6 and i<26) or (gate==12 and i>=26) else 30))
        return records

    def test_holdout_does_not_select_gate(self):
        result=run.summarize(self.records(),2,5000)
        self.assertEqual(result['training_winner'],6)
        self.assertLess(result['totals']['holdout']['12']['solve_us'],result['totals']['holdout']['6']['solve_us'])

    def test_unknown_count_precedes_time(self):
        records=self.records()
        for r in records:
            if r['gate']==6 and r['id']==0:r['result']=0
        self.assertNotEqual(run.summarize(records,2,5000)['training_winner'],6)

    def test_repeats_must_have_same_work(self):
        records=self.records();records[0]['nodes']+=1
        with self.assertRaises(AssertionError):run.summarize(records,2,5000)

    def raw(self,result=1,budget=5000,solve=4):
        lines=[]
        for i in range(52):
            lines.append(f'# replay_timing row={i} setup_us=2 solve_us={solve} total_us=8 residual_gate=6')
            lines.append(f'replay,{i},10,8,1,{budget},{result},3,0,0,0')
        return '\n'.join(lines+['# replay_done rows=52 wall_s=0'])

    def expected(self):return [dict(id=i,occupied=list(range(10)),legal=list(range(8)),result=1) for i in range(52)]

    def test_contradictory_verdict_rejected(self):
        with self.assertRaises(AssertionError):run.parse(self.raw(result=2),self.expected(),6,0,5000)

    def test_wrong_budget_rejected(self):
        with self.assertRaises(AssertionError):run.parse(self.raw(budget=4999),self.expected(),6,0,5000)

    def test_impossible_timing_rejected(self):
        with self.assertRaises(AssertionError):run.parse(self.raw(solve=99),self.expected(),6,0,5000)

if __name__=='__main__':unittest.main()
