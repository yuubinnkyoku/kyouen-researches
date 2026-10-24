"""Reproduce and cross-check the full algebraic audit using a temporary binary."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cxx',default=shutil.which('g++') or 'g++')
    args=parser.parse_args()
    for name in ('check_symbolic.py','fixed.py'):
        subprocess.run([sys.executable,str(HERE/name)],check=True)
    expected=json.loads((HERE/'fixed-audit.json').read_text(encoding='utf-8'))
    with tempfile.TemporaryDirectory(prefix='kyouen-q6-eighteen-') as temporary:
        binary=Path(temporary)/('audit.exe' if sys.platform=='win32' else 'audit')
        subprocess.run([args.cxx,'-std=c++17','-O2',str(HERE/'fixed_independent.cpp'),'-o',str(binary)],check=True)
        result=subprocess.run([str(binary)],check=True,text=True,capture_output=True)
    lines=result.stdout.splitlines();assert lines[0]=='near-ap 11628 2'
    assert lines[-1]=='all 4823 four-circle subsets excluded: PASS'
    actual={}
    for line in lines[1:-1]:
        name,kind,count=line.split();assert (name,kind) not in actual;actual[name,kind]=int(count)
    wanted={(row['name'],kind):count for row in expected['cases'] for kind,count in row['classifications'].items()}
    assert actual==wanted
    receipt={'symbolic_cases':156,'symbolic_negative_controls':2,
             'near_ap_integer_candidates':11628,'fixed_four_circle_subsets':4823,
             'cpp_classification_match':True,'arithmetic':'exact integers / rational polynomials'}
    (HERE/'audit.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':main()
