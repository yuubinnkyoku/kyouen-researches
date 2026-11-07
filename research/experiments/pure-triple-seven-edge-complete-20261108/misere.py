#!/usr/bin/env python3
"""Normal/misere values of every seven-edge core with both free parities."""
from collections import Counter
import hashlib
import importlib.util
import json
from pathlib import Path
import random
import shutil
import subprocess
import tempfile

ROOT=Path(__file__).resolve().parents[3]
SPEC=importlib.util.spec_from_file_location('six_misere',ROOT/'research/experiments/pure-triple-six-edge-complete-20261108/misere.py')
PY=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(PY)


def signature_of(n,edges):
    counts=[0]*127
    for v in range(n):counts[sum(1<<e for e,edge in enumerate(edges) if edge>>v&1)-1]+=1
    return tuple(counts)


def main():
    directory=Path(__file__).resolve().parent;source=directory/'output/audit.json'
    census=json.loads(source.read_text());rows=census['records'];cases=[]
    for row in rows:
        for free in (0,1):cases.append((row['n']+free,row['edges']))
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-seven-edge-misere-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';cell=temp/'cell.exe';raw=temp/'raw.exe';a=temp/'cell.bin';b=temp/'raw.bin';meta=temp/'raw.json'
        data.write_text(str(len(cases))+'\n'+'\n'.join(' '.join(map(str,[n,7,*edges])) for n,edges in cases)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O3',str(directory/'cell_both.cpp'),'-o',str(cell)],check=True)
        first_report=json.loads(subprocess.check_output([str(cell),str(data),str(a)],text=True));print(first_report,flush=True)
        cpp=ROOT/'research/experiments/common-pivot-misere-bound-20261108/independent.cpp'
        subprocess.run([compiler,'-std=c++17','-O3','-DMAX_LEGAL_POINTS=22',str(cpp),'-o',str(raw)],check=True)
        subprocess.run([str(raw),str(data),str(b),str(meta)],check=True)
        second_report=json.loads(meta.read_text());print(second_report,flush=True)
        values=a.read_bytes();assert values==b.read_bytes() and len(values)==2*len(cases)
    assert first_report['cell_states']==3*census['cpp_cell_states']
    assert second_report['safe_states']==3*census['cpp_raw_safe_states']
    for i,row in enumerate(rows):
        assert values[4*i]==row['grundy'] and values[4*i+2]==row['grundy']^1
    selected=random.Random(20261108).sample(range(len(rows)),400)
    for i in selected:
        row=rows[i];signature=signature_of(row['n'],row['edges'])
        for free in (0,1):assert PY.cell_values(signature,free)==tuple(values[4*i+2*free:4*i+2*free+2])
    histogram=Counter((values[i],values[i+1]) for i in range(0,len(values),2));maximum=max(h for g,h in histogram)
    best={}
    for i,row in enumerate(rows):
        for free in (0,1):
            g,h=values[4*i+2*free:4*i+2*free+2]
            if h not in best or row['n']+free<best[h]['n']:
                best[h]=dict(n=row['n']+free,edges=row['edges'],normal=g,misere_aux=h,free_parity=free)
    output=dict(audit='PASS',census_sha256=hashlib.sha256(source.read_text(encoding='utf-8').encode('utf-8')).hexdigest(),kernel_types=len(rows),
                cases_compared=len(cases),cpp_cell_states=first_report['cell_states'],cpp_safe_states=second_report['safe_states'],
                python_sample_kernel_types=400,maximum_misere=maximum,
                pair_histogram={str(g)+','+str(h):count for (g,h),count in sorted(histogram.items())},
                minimum_point_witnesses_within_seven_edges=best,
                misere_values_free_zero=list(values[1::4]),misere_values_free_one=list(values[3::4]))
    target=directory/'output/misere.json'
    # Compact arrays preserve a complete per-kernel record without duplicating the census.
    head={k:v for k,v in output.items() if not k.startswith('misere_values_')}
    text=json.dumps(head,indent=2)[:-2]+',\n  "misere_values_free_zero": '+json.dumps(output['misere_values_free_zero'],separators=(',',':'))+',\n  "misere_values_free_one": '+json.dumps(output['misere_values_free_one'],separators=(',',':'))+'\n}\n'
    json.loads(text);target.write_text(text,encoding='utf-8')
    print(json.dumps({k:v for k,v in head.items() if k not in ('pair_histogram','minimum_point_witnesses_within_seven_edges')},indent=2),flush=True)


if __name__=='__main__':main()
