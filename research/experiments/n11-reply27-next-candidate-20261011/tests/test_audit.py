"""Mutation regressions for reply27 three-S5 raw audit."""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
SCRIPT=ROOT/"research/experiments/n11-reply27-next-candidate-20261011/scripts/audit.py"
spec=importlib.util.spec_from_file_location("three_s5_audit",SCRIPT)
a=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

class Tests(unittest.TestCase):
    def test_polarity(self):
        children=[(1,0),(2,0)]
        self.assertEqual(a.status(children,{(1,0):2,(2,0):2}),"LOSS")
        self.assertEqual(a.status(children,{(1,0):1}),"WIN")
        self.assertEqual(a.status(children,{(1,0):2}),"UNKNOWN")

    def test_geometry(self):
        b=a.Board(11)
        for k,count in [((10412322338480590849,0),84),
                        ((1297036692750861312,0),92),
                        ((1301540292311122944,0),94)]:
            self.assertEqual(b.canonical(a.mask(k)),a.mask(k))
            self.assertEqual(b.legal(a.mask(k)).bit_count(),count)

    def test_rejects_forged_verdict(self):
        self.mutate("probe-15m.csv",6,"1")

    def test_rejects_legal_count(self):
        self.mutate("targets.csv",5,"85")

    def mutate(self,name,index,replacement):
        with tempfile.TemporaryDirectory(dir=ROOT/".local") as path:
            target=Path(path)/"raw"
            shutil.copytree(a.RAW,target)
            file=target/name
            rows=file.read_text().splitlines()
            first=next(i for i,r in enumerate(rows)
                       if r and r.startswith("replay,")) if name.startswith("probe") else 0
            parts=rows[first].split(",")
            parts[index]=replacement
            rows[first]=",".join(parts)
            file.write_text("\n".join(rows)+"\n")
            previous=a.RAW
            try:
                a.RAW=target
                with self.assertRaises(AssertionError):
                    a.main()
            finally:
                a.RAW=previous
