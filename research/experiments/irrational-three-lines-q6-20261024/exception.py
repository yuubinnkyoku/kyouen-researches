"""Audit the excluded prime c=3, including its exceptional m=6 strong solution."""
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
    with tempfile.TemporaryDirectory(prefix='kyouen-irrational-c3-') as directory:
        binary=Path(directory)/('verify.exe' if sys.platform=='win32' else 'verify')
        subprocess.run([args.cxx,'-std=c++17','-O2',str(HERE/'verify.cpp'),'-o',str(binary)],check=True)
        result=subprocess.run([str(binary),'3'],check=True,capture_output=True,text=True)
    records=json.loads(result.stdout)
    assert records[4]['root_grundy']==0 and records[4]['terminal_histogram']=={'14':6}
    assert records[5]['root_grundy']==1 and records[5]['max_grundy']==3
    assert set(records[5]['terminal_histogram'])=={'14','15'}
    assert records[5]['safe_states']==243324
    assert records[6]['terminal_histogram']=={'15':6369}
    receipt={'c':3,'records':records,'safe_states_compared':sum(r.get('safe_states',0) for r in records),
             'six_subsets_compared':sum(r['six_subsets'] for r in records)}
    (HERE/'audit-c3.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({'c':3,'m6':records[5],'safe_states_compared':receipt['safe_states_compared']}),flush=True)


if __name__=='__main__':main()
