"""Compile an exact Q(alpha) verifier in a temporary directory and store its receipt."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent


def main():
    p=argparse.ArgumentParser();p.add_argument('--cxx',default=shutil.which('g++') or 'g++');args=p.parse_args()
    with tempfile.TemporaryDirectory(prefix='kyouen-irrational-q6-') as directory:
        binary=Path(directory)/('verify.exe' if sys.platform=='win32' else 'verify')
        subprocess.run([args.cxx,'-std=c++17','-O2',str(HERE/'verify.cpp'),'-o',str(binary)],check=True)
        result=subprocess.run([str(binary)],check=True,capture_output=True,text=True)
    records=json.loads(result.stdout);assert [r['m'] for r in records]==list(range(1,11))
    assert records[5]['safe_states']==246672 and records[6]['safe_states']==1692912
    for r in records:
        if r['m']<=7:assert r['pointwise_two_engine_match'] and r['max_grundy']==1
    receipt={'field':'Q(alpha), alpha^2-alpha-4=0','records':records,
             'safe_states_compared':sum(r.get('safe_states',0) for r in records),
             'six_subsets_compared':sum(r['six_subsets'] for r in records)}
    (HERE/'audit.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(receipt),flush=True)


if __name__=='__main__':main()
