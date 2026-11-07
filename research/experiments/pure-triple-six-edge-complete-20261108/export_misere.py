#!/usr/bin/env python3
"""Retain per-kernel auxiliary values for the <=6-edge Pareto analysis."""
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile


def main():
    directory=Path(__file__).resolve().parent;root=directory.parents[2]
    old=json.loads((root/'research/experiments/pure-triple-few-edge-grundy-20261107/output/audit.json').read_text())['records']
    six=json.loads((directory/'output/audit.json').read_text())['records']
    rows=[dict(h=r['h'],n=r['n'],edges=r['edges'],grundy=r['grundy']) for r in old]
    rows.extend(dict(h=6,n=r['n'],edges=r['edges'],grundy=r['grundy']) for r in six)
    cases=[(r['n']+free,r['h'],r['edges']) for r in rows for free in (0,1)]
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-six-misere-export-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';cell=temp/'cell.exe';raw=temp/'raw.exe';a=temp/'cell.bin';b=temp/'raw.bin';meta=temp/'meta.json'
        data.write_text(str(len(cases))+'\n'+'\n'.join(' '.join(map(str,[n,h,*edges])) for n,h,edges in cases)+'\n',encoding='ascii')
        cpp_cell=root/'research/experiments/pure-triple-seven-edge-complete-20261108/cell_both.cpp'
        cpp_raw=root/'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'
        subprocess.run([compiler,'-std=c++17','-O3',str(cpp_cell),'-o',str(cell)],check=True)
        cell_report=json.loads(subprocess.check_output([str(cell),str(data),str(a)],text=True))
        subprocess.run([compiler,'-std=c++17','-O3',str(cpp_raw),'-o',str(raw)],check=True)
        subprocess.run([str(raw),str(data),str(b),str(meta)],check=True)
        values=a.read_bytes();assert values==b.read_bytes() and len(values)==2*len(cases)
        raw_report=json.loads(meta.read_text())
    previous=json.loads((directory/'output/misere.json').read_text());assert raw_report['safe_states']==previous['cpp_safe_states']
    for h in range(1,7):
        observed=Counter()
        for i,r in enumerate(rows):
            for free in (0,1):
                g,aux=values[4*i+2*free:4*i+2*free+2];assert g==r['grundy']^free
                if r['h']==h:observed[g,aux]+=1
        expected=previous['summaries'][h-1]['pair_histogram']
        assert {str(g)+','+str(aux):count for (g,aux),count in observed.items()}==expected
    digest=hashlib.sha256(json.dumps(rows,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    output=dict(audit='PASS',canonical_rows_sha256=digest,kernel_types=len(rows),cases_compared=len(cases),
                cpp_cell_states=cell_report['cell_states'],cpp_safe_states=raw_report['safe_states'],
                misere_values_free_zero=list(values[1::4]),misere_values_free_one=list(values[3::4]))
    (directory/'output/misere_values.json').write_text(json.dumps(output,separators=(',',':'))+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in output.items() if not k.startswith('misere_values_')},indent=2))


if __name__=='__main__':main()
