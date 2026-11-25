"""Audit several members of the prime/prime-square family with the exact verifier."""
import argparse
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cxx',default=shutil.which('g++') or 'g++');args=parser.parse_args()
    results=[]
    with tempfile.TemporaryDirectory(prefix='kyouen-irrational-family-') as temporary:
        binary=Path(temporary)/('verify.exe' if sys.platform=='win32' else 'verify')
        subprocess.run([args.cxx,'-std=c++17','-O2',str(HERE/'verify.cpp'),'-o',str(binary)],check=True)
        for c in (1,4,5,7,9,11):
            result=subprocess.run([str(binary),str(c)],check=True,text=True,capture_output=True)
            records=json.loads(result.stdout)
            assert len(records)==10 and all(r.get('pointwise_two_engine_match',True) for r in records)
            results.append({'c':c,'records':records})
    receipt={'parameters':[r['c'] for r in results],'results':results,
             'six_subsets_compared':sum(v['six_subsets'] for r in results for v in r['records']),
             'safe_states_compared':sum(v.get('safe_states',0) for r in results for v in r['records'])}
    (HERE/'family-audit.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='results'}),flush=True)


if __name__=='__main__':main()
