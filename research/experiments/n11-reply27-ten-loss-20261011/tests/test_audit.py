"""Mutation tests for S5 exact evidence audit."""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
P = ROOT / "research/experiments/n11-reply27-ten-loss-20261011/scripts/audit.py"
spec = importlib.util.spec_from_file_location("n11_ten_loss", P)
audit = importlib.util.module_from_spec(spec)
spec.loader.exec_module(audit)

class Tests(unittest.TestCase):
    def test_true_geometry_and_polarity(self):
        board = audit.Board(11)
        for key, expected in [((3602879701897446400, 0),89),
                               ((1297036692683760640, 0),90),
                               ((10376293541461626881,65536),96)]:
            self.assertEqual(board.canonical(audit.asmask(key)),audit.asmask(key))
            self.assertEqual(board.legal(audit.asmask(key)).bit_count(),expected)
        children = [(1, 0), (2, 0)]
        self.assertEqual(audit.class_status(children,{(1,0):2, (2,0):2}),"LOSS")
        self.assertEqual(audit.class_status(children,{(1,0):2}),"UNKNOWN")
        self.assertEqual(audit.class_status(children,{(1,0):1}),"WIN")

    def mutation(self, name, which, replacement=None, drop=False):
        with tempfile.TemporaryDirectory(dir=ROOT/".local") as temp:
            target = Path(temp)/"raw"
            shutil.copytree(audit.RAW,target)
            path = target/name
            lines = path.read_text().splitlines()
            i = next(i for i,line in enumerate(lines) if line.startswith("replay,")) if name.startswith("group") or name.startswith("single") else 0
            if drop:
                del lines[i]
            else:
                items = lines[i].split(",")
                items[which] = str(replacement)
                lines[i] = ",".join(items)
            path.write_text("\n".join(lines)+"\n")
            original=audit.RAW
            try:
                audit.RAW=target
                with self.assertRaises(AssertionError):
                    audit.main()
            finally:
                audit.RAW=original

    def test_rejects_fake_s5_win(self):
        self.mutation("group1a-15m.csv",6,1)

    def test_rejects_wrong_geometry(self):
        self.mutation("input-group2.csv",5,40)

    def test_rejects_duplicate_solver_row(self):
        path="group1a-15m.csv"
        with tempfile.TemporaryDirectory(dir=ROOT/".local") as temp:
            target=Path(temp)/"raw"
            shutil.copytree(audit.RAW,target)
            file=target/path
            with file.open("a") as f:
                f.write("replay,0,5,89,0,15000000,2,2742740,8,3602879701897446400,0\n")
            original=audit.RAW
            try:
                audit.RAW=target
                with self.assertRaises(AssertionError):
                    audit.main()
            finally:
                audit.RAW=original

    def test_rejects_missing_solver_row(self):
        self.mutation("group2b-15m.csv",None,drop=True)
