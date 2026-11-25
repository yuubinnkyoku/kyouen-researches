#!/usr/bin/env python3
"""Finite base of the rank-free theorem g <= legal_count-2 for legal_count >=5."""
from collections import Counter
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'research/experiments/rooted-core-tail-periodicity-20261107'))
from engine import canonical,ordinary
SPEC=importlib.util.spec_from_file_location('incidence_audit',ROOT/'research/experiments/incidence-weighted-grundy-bound-20261107/verify.py')
GENERATOR=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(GENERATOR)


def independent_clutters(n):
    possible=[s for s in range(1,1<<n) if s.bit_count()>=2]
    def search(remaining,chosen):
        if not remaining:
            yield tuple(sorted(chosen));return
        first,*rest=remaining
        yield from search(rest,chosen)
        compatible=[other for other in rest if first&other not in (first,other)]
        yield from search(compatible,chosen+[first])
    yield from search(possible,[])


def main():
    directory=Path(__file__).resolve().parent
    records=[];summary=[]
    for n in range(1,6):
        families={tuple(sorted(edges)) for edges in GENERATOR.clutters(n)}
        assert families==set(independent_clutters(n))
        histogram=Counter()
        for edges in sorted(families):
            value=ordinary(canonical(n,tuple(sorted(edges))))
            records.append((n,edges,value));histogram[value]+=1
        summary.append(dict(legal_points=n,clutters=len(families),histogram=dict(sorted(histogram.items())),maximum=max(histogram)))
    assert [s['clutters'] for s in summary]==[1,2,9,114,6894]
    assert [s['maximum'] for s in summary]==[1,1,2,3,3]
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-legal-gap-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';executable=temp/'native.exe';result=temp/'values.bin'
        data.write_text(str(len(records))+'\n'+'\n'.join(' '.join(map(str,[n,len(edges),*edges])) for n,edges,g in records)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O2',str(cpp),'-o',str(executable)],check=True)
        report=json.loads(subprocess.check_output([str(executable),str(data),str(result)],text=True))
        assert result.read_bytes()==bytes(g for n,edges,g in records)
    pure=json.loads((ROOT/'research/experiments/pure-triple-maximum-grundy-six-20261107/output/independent_audit.json').read_text())
    output=dict(audit='PASS',rank_unrestricted_base=summary,independent_generators_match=True,
        clutters_compared=len(records),cpp_safe_states=report['safe_states'],
        universal_theorem='for every finite forbidden-set placement game, legal_count >=5 implies g<=legal_count-2',
        sharp_at_six_and_seven=dict(six_value_four=pure['maximum_four_orbits'][0]['triples'],
                                   seven_value_five=pure['seven_point_value_five']['edges']))
    target=directory/'output/audit.json';target.parent.mkdir(exist_ok=True)
    target.write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2))


if __name__=='__main__':main()
