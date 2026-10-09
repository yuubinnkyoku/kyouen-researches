import itertools
import random
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT/'research/experiments/n11-boundary-recovery-20261006/scripts'
sys.path.insert(0,str(SCRIPTS))
from fixed_player_outcome import outcome
from run_s7_witness_probe_local import s6_outcome
sys.path.insert(0,str(ROOT/'research/experiments/n11-strategy-redesign-20261010/scripts'))
from audit import forbidden, determinant, canonical
from study import canon
sys.path.insert(0,str(ROOT/'research/experiments/n11-frontier-selection-20261005/scripts'))
from cache_aware_reply27_cover import load_cache
from merge_exact_s5_evidence import merge
from study import BASE, SUSPECT

class PolarityTests(unittest.TestCase):
    def test_every_partial_two_child_boundary_at_layers_four_to_ten(self):
        # Evaluate all Boolean completions of UNKNOWN. A proof is decisive
        # only when every completion agrees with the AND/OR proposition.
        for n in range(4,11):
            for values in itertools.product((0,1,2),repeat=2):
                completions = itertools.product(*[(False,True) if v==0 else (v==1,) for v in values])
                results = {any(v) if n%2==0 else all(v) for v in completions}
                expected = 'UNKNOWN' if len(results)==2 else ('WIN' if True in results else 'LOSS')
                self.assertEqual(outcome(n,range(2),dict(enumerate(values))),expected,(n,values))

    def test_terminal_parity(self):
        for n in range(4,11):
            self.assertEqual(outcome(n,[],{}),'LOSS' if n%2==0 else 'WIN')

    def test_s7_loss_does_not_prove_s6_win(self):
        self.assertEqual(s6_outcome({1,2},{1:2}),'UNKNOWN')
        self.assertEqual(s6_outcome({1,2},{1:2,2:2}),'LOSS')
        self.assertEqual(s6_outcome({1,2},{1:1}),'WIN')

    def test_independent_determinant_row_reduction_and_d4(self):
        rng=random.Random(20261010)
        for _ in range(200):
            p=tuple(rng.sample(range(121),4))
            rows=[[((v%11)**2+(v//11)**2),v%11,v//11,1] for v in p]
            self.assertEqual(forbidden(p),determinant(rows)==0)
            self.assertEqual(canonical(p),canon(p))
        self.assertTrue(forbidden((0,5,55,60)))
        self.assertTrue(forbidden((0,1,2,3)))

    def test_withdrawn_cache_ancestry_cannot_reenter_union(self):
        cached=load_cache(BASE)
        self.assertFalse(SUSPECT.intersection(cached))
        merged,receipt=merge([BASE],[])
        self.assertEqual(merged,cached)
        self.assertEqual(receipt['sources'][0]['quarantined_cache_rows'],2)

if __name__=='__main__':
    unittest.main()
