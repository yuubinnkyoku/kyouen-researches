#!/usr/bin/env python3
"""Complete six-edge pure-triple cores by augmentation, with an independent orbit count."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from count_signatures import distinct_counts

ROOT=Path(__file__).resolve().parents[3]
SPEC=importlib.util.spec_from_file_location('few_edge',ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/audit.py')
OLD=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(OLD)


def main():
    directory=Path(__file__).resolve().parent
    old=json.loads((ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/output/audit.json').read_text())
    previous=[r for r in old['records'] if r['h']==5];assert len(previous)==445
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    with tempfile.TemporaryDirectory(prefix='kyouen-six-triples-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'previous.txt';generated=temp/'signatures.txt';exe=temp/'generate.exe'
        data.write_text(str(len(previous))+'\n'+'\n'.join(' '.join(map(str,r['signature'])) for r in previous)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O3',str(directory/'generate.cpp'),'-o',str(exe)],check=True)
        generation=json.loads(subprocess.check_output([str(exe),str(data),str(generated)],text=True));print(generation,flush=True)
        lines=generated.read_text().splitlines();assert int(lines[0])==generation['unlabeled_types']==len(lines)-1
        unrestricted,distinct=distinct_counts(6)
        assert distinct[1:6]==[1,3,29,666,28344]
        assert generation['labeled_signatures']==distinct[6]
        records=[];histogram=Counter()
        for index,line in enumerate(lines[1:]):
            aut,*signature=map(int,line.split());assert len(signature)==63 and 720%aut==0
            members=[mask for mask,count in enumerate(signature,1) for _ in range(count)]
            edges=[sum(1<<v for v,mask in enumerate(members) if mask>>e&1) for e in range(6)]
            value,states=OLD.quotient_grundy(tuple(signature));histogram[value]+=1
            records.append(dict(n=len(members),edges=edges,signature=signature,automorphism_order=aut,grundy=value,quotient_states=states))
            if (index+1)%500==0:print(dict(types_evaluated=index+1,maximum=max(histogram)),flush=True)
        cases=temp/'cases.txt';native_exe=temp/'verify.exe';values=temp/'values.bin'
        cases.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[r['n'],6,*r['edges']])) for r in records)+'\n',encoding='ascii')
        cpp=ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
        subprocess.run([compiler,'-std=c++17','-O3',str(cpp),'-o',str(native_exe)],check=True)
        native=json.loads(subprocess.check_output([str(native_exe),str(cases),str(values)],text=True))
        assert values.read_bytes()==bytes(r['grundy'] for r in records)
    maximum=max(max(r['grundy'],r['grundy']^1) for r in records)
    output=dict(audit='PASS',generation=generation,independent_unrestricted_signature_counts=unrestricted,
                independent_distinct_signature_counts=distinct,core_histogram=dict(sorted(histogram.items())),
                maximum_with_free_points=maximum,cpp_safe_states=native['safe_states'],
                maximum_witness=next(r for r in records if max(r['grundy'],r['grundy']^1)==maximum),records=records)
    target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True)
    head={k:v for k,v in output.items() if k!='records'}
    text=json.dumps(head,indent=2);text=text[:-2]+',\n  "records": [\n'+',\n'.join('    '+json.dumps(r,separators=(',',':')) for r in records)+'\n  ]\n}\n'
    json.loads(text);target.write_text(text,encoding='utf-8')
    print(json.dumps({k:v for k,v in head.items() if k!='maximum_witness'},indent=2),flush=True)


if __name__=='__main__':main()
