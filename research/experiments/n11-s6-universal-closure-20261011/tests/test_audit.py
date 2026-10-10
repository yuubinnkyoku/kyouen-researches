"""Mutation and logical-polarity regressions for the S5/S6 closure."""
import csv
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
SCRIPT=ROOT/"research/experiments/n11-s6-universal-closure-20261011/scripts/audit.py"
spec=importlib.util.spec_from_file_location("n11_s6_closure",SCRIPT)
m=importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

class Regression(unittest.TestCase):
    def test_fixed_player_polarity(self):
        self.assertEqual(m.aggregate(5,[1]*90),1)
        self.assertEqual(m.aggregate(5,[1]*89+[2]),2)
        self.assertEqual(m.aggregate(5,[1]*89+[0]),0)
        self.assertEqual(m.aggregate(4,[2,2,1]),1)
        self.assertEqual(m.aggregate(4,[2,2]),2)

    def test_canonical_complete_geometry(self):
        b=m.Board(11)
        s5=m.asmask(m.S5_HARD)
        self.assertEqual(b.canonical(s5),s5)
        kids={m.askey(k) for k in b.children(s5)}
        self.assertEqual(len(kids),90)
        self.assertEqual(b.legal(s5).bit_count(),90)

    def test_audit_rejects_missing_boundary_row(self):
        self.run_mutant(drop=True)

    def test_audit_rejects_forged_win(self):
        self.run_mutant(drop=False)

    def run_mutant(self,drop):
        with tempfile.TemporaryDirectory(dir=ROOT/".local") as temp:
            tmp=Path(temp)/"raw"
            shutil.copytree(m.RAW,tmp)
            p=tmp/"s6-batch1.out.csv"
            contents=p.read_text()
            rows=contents.splitlines(keepends=True)
            idx=next(i for i,row in enumerate(rows) if row.startswith("replay,"))
            if drop:
                del rows[idx]
            else:
                cols=rows[idx].rstrip("\r\n").split(",")
                self.assertEqual(cols[6],"1")
                cols[6]="2"
                rows[idx]=",".join(cols)+"\n"
            p.write_text("".join(rows))
            original=m.RAW
            try:
                m.RAW=tmp
                with self.assertRaises(AssertionError):
                    m.run(m.BASE)
            finally:
                m.RAW=original
