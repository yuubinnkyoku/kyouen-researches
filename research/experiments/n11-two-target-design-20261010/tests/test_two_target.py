"""Fast regressions for the reflection equivalence and raw replay parsing."""
import csv
import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
SCRIPT=ROOT/"research/experiments/n11-two-target-design-20261010/scripts/verify_and_merge.py"
spec=importlib.util.spec_from_file_location("two_target_verify", SCRIPT)
module=importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

class Tests(unittest.TestCase):
    def test_reflection_swaps_remnant_but_fixes_root(self):
        reflect=lambda n:11*(n//11)+10-n%11
        self.assertEqual([reflect(i) for i in (60,27,100,108)],[60,27,108,100])
        self.assertEqual([reflect(reflect(i)) for i in range(121)], list(range(121)))
        board=module.Board(11)
        root=(1<<60)|(1<<27)
        self.assertEqual(board.legal(root).bit_count(),119)
        a=board.legal(root|(1<<100))
        b=board.legal(root|(1<<108))
        self.assertEqual({reflect(x) for x in board.points(a)},set(board.points(b)))

    def test_exact_raw_rejects_non_exact_and_changed_verdict(self):
        key,legal,nodes=module.TARGETS[0]
        base=module.RAW/f"first-15m-s5-{key[0]}-{key[1]}.out.csv"
        with base.open() as stream:
            r=next(x for x in csv.reader(stream) if x and x[0]=="replay")
        self.assertEqual(module.read_run(base,key,legal,15_000_000,2),nodes)
        for idx,val in [(6,"1"),(6,"0"),(7,str(nodes+1)),(3,str(legal+1))]:
            mutant=r.copy();mutant[idx]=val
            with tempfile.TemporaryDirectory() as temp:
                p=Path(temp)/"corrupt.csv"
                with p.open("w",newline="") as f:csv.writer(f).writerow(mutant)
                with self.assertRaises(AssertionError):
                    got=module.read_run(p,key,legal,15_000_000,2)
                    self.assertEqual(got,nodes)
