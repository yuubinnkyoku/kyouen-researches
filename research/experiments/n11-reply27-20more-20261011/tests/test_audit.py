"""Independent proof boundary and raw-evidence failure-mode tests."""
import importlib.util
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
SCRIPT=ROOT/"research/experiments/n11-reply27-20more-20261011/scripts/audit.py"
spec=importlib.util.spec_from_file_location("n11_more20_audit",SCRIPT)
a=importlib.util.module_from_spec(spec)
spec.loader.exec_module(a)

class AuditTests(unittest.TestCase):
    def test_complete_audit(self):
        result=a.audit()
        self.assertEqual(result["new_s5_verdicts"],{"LOSS":20,"WIN":0,"UNKNOWN":0})
        self.assertEqual(result["target_s4_after"],{"UNKNOWN":66,"WIN":0,"LOSS":40})
        self.assertEqual(result["s5_cache_conflicts"],0)

    def test_polarity(self):
        ch=[[1,0],[2,0]]
        self.assertEqual(a.status(ch,{(1,0):2,(2,0):2}),"LOSS")
        self.assertEqual(a.status(ch,{(1,0):1}),"WIN")
        self.assertEqual(a.status(ch,{(1,0):2}),"UNKNOWN")

    def mutation(self,name,op):
        # Work inside a temp copy so the real evidence cannot be modified.
        with tempfile.TemporaryDirectory(dir=ROOT/".local") as path:
            tmp=Path(path)/"raw"
            shutil.copytree(a.RAW,tmp)
            file=tmp/name
            lines=file.read_text().splitlines()
            idx=next(i for i,line in enumerate(lines)
                     if line.startswith("replay,")) if name.startswith("probe") else 0
            if op=="drop":
                del lines[idx]
            else:
                values=lines[idx].split(",")
                if op=="fake_win":values[6]="1"
                elif op=="invalid_legal":values[5]="0"
                elif op=="invalid_key":values[3]="0"
                else:raise AssertionError(op)
                lines[idx]=",".join(values)
            file.write_text("\n".join(lines)+"\n")
            original=a.RAW
            try:
                a.RAW=tmp
                with self.assertRaises(AssertionError):
                    a.audit()
            finally:
                a.RAW=original

    def test_reject_forged_s5_win(self):
        self.mutation("probe-00.csv","fake_win")

    def test_reject_truncated_replay(self):
        self.mutation("probe-01.csv","drop")

    def test_reject_changed_legal_count(self):
        self.mutation("target-03.csv","invalid_legal")

    def test_reject_changed_bitmask(self):
        self.mutation("target-04.csv","invalid_key")
