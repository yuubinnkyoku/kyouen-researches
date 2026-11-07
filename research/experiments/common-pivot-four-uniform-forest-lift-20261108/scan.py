#!/usr/bin/env python3
"""Bounded census of pivot lifts of the complete <=8-edge triple-tree corpus."""
from collections import Counter
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    directory=Path(__file__).resolve().parent;root=directory.parents[2]
    rows=json.loads((root/'research/experiments/pure-triple-hyperforests-20261107/output/audit.json').read_text())['records']
    records=[dict(n=row['n']+1,h=row['h'],edges=[(e<<1)|1 for e in row['edges']]) for row in rows]
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=root/'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-forest-lift-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'scan.exe';values=temp/'values.bin'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[r['n'],r['h'],*r['edges']])) for r in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(cpp),'-o',str(exe)],check=True)
        native=json.loads(subprocess.check_output([str(exe),str(data),str(values)],text=True))
        result=values.read_bytes();assert len(result)==len(records)
    for row,value in zip(records,result):row['grundy']=value
    summaries=[]
    for h in range(1,9):
        histogram=Counter(r['grundy'] for r in records if r['h']==h)
        summaries.append(dict(h=h,histogram=dict(sorted(histogram.items())),maximum=max(histogram)))
    output=dict(scope='all <=8-edge connected triple Berge-tree lifts; not all rank-four common-pivot clutters',
                cases=len(records),cpp_safe_states=native['safe_states'],summaries=summaries,
                maximum_witness=max(records,key=lambda r:r['grundy']),records=records)
    target=directory/'output/scan.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if k!='records'},indent=2),flush=True)


if __name__=='__main__':main()
