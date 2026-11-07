#!/usr/bin/env python3
"""Complete seven-edge census: incidence augmentation, GF count, two native SG engines."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import random
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[3]
SIX=ROOT/'research/experiments/pure-triple-six-edge-complete-20261108'
sys.path.insert(0,str(SIX))
from count_signatures import distinct_counts
SPEC=importlib.util.spec_from_file_location('few_edge',ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/audit.py')
OLD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(OLD)


def signature_of(n,edges):
    counts=[0]*127
    for v in range(n):
        mask=sum(1<<e for e,edge in enumerate(edges) if edge>>v&1);assert mask
        counts[mask-1]+=1
    return tuple(counts)


def main():
    directory=Path(__file__).resolve().parent
    previous=json.loads((SIX/'output/audit.json').read_text())['records'];assert len(previous)==4279
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-seven-triples-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'previous.txt';generated=temp/'signatures.txt';gen=temp/'generate.exe'
        data.write_text(str(len(previous))+'\n'+'\n'.join(' '.join(map(str,r['signature'])) for r in previous)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O3','-DEDGE_COUNT=7',str(SIX/'generate.cpp'),'-o',str(gen)],check=True)
        generation=json.loads(subprocess.check_output([str(gen),str(data),str(generated)],text=True));print(generation,flush=True)
        unrestricted,distinct=distinct_counts(7)
        assert generation['labeled_signatures']==distinct[7]
        lines=generated.read_text().splitlines();assert int(lines[0])==generation['unlabeled_types']==len(lines)-1
        records=[]
        for line in lines[1:]:
            aut,*signature=map(int,line.split());assert len(signature)==127 and 5040%aut==0
            members=[mask for mask,count in enumerate(signature,1) for _ in range(count)]
            edges=[sum(1<<v for v,mask in enumerate(members) if mask>>e&1) for e in range(7)]
            records.append(dict(n=len(members),edges=edges,edge_stabilizer_order=aut))
        cases=temp/'cases.txt';cell=temp/'cell.exe';raw=temp/'raw.exe';a=temp/'cell.bin';b=temp/'raw.bin'
        cases.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[r['n'],7,*r['edges']])) for r in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O3',str(directory/'cell.cpp'),'-o',str(cell)],check=True)
        cell_report=json.loads(subprocess.check_output([str(cell),str(cases),str(a)],text=True));print(cell_report,flush=True)
        subprocess.run([compiler,'-std=c++17','-O3',str(ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'),'-o',str(raw)],check=True)
        raw_report=json.loads(subprocess.check_output([str(raw),str(cases),str(b)],text=True));print(raw_report,flush=True)
        first=a.read_bytes();second=b.read_bytes();assert len(first)==len(records) and first==second
        for row,value in zip(records,first):row['grundy']=value
    selected=random.Random(20261108).sample(range(len(records)),min(400,len(records)))
    python_states=0
    for i in selected:
        row=records[i];value,states=OLD.quotient_grundy(signature_of(row['n'],row['edges']))
        assert value==row['grundy'];python_states+=states
    histogram=Counter(r['grundy'] for r in records);maximum=max(max(g,g^1) for g in histogram)
    output=dict(audit='PASS',generation=generation,independent_unrestricted_signature_counts=unrestricted,
                independent_distinct_signature_counts=distinct,core_histogram=dict(sorted(histogram.items())),
                maximum_with_free_points=maximum,cpp_cell_states=cell_report['cell_states'],
                cpp_raw_safe_states=raw_report['safe_states'],python_sample_types=len(selected),python_sample_states=python_states,
                maximum_witness=next(r for r in records if max(r['grundy'],r['grundy']^1)==maximum),records=records)
    target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True)
    head={k:v for k,v in output.items() if k!='records'}
    text=json.dumps(head,indent=2);text=text[:-2]+',\n  "records": [\n'+',\n'.join('    '+json.dumps(r,separators=(',',':')) for r in records)+'\n  ]\n}\n'
    json.loads(text);target.write_text(text,encoding='utf-8')
    print(json.dumps({k:v for k,v in head.items() if k!='maximum_witness'},indent=2),flush=True)


if __name__=='__main__':main()
