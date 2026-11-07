#!/usr/bin/env python3
"""Complete <=3-edge extensions of the fixed g8 witness by two new points."""
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
from verify import ROOT,NORMAL


def main():
    directory=Path(__file__).resolve().parent
    base=tuple(json.loads((directory/'output/audit.json').read_text())['records'][0]['edges'])
    n=12;fresh=(1<<10)|(1<<11)
    candidates=[sum(1<<v for v in edge) for edge in combinations(range(n),3)]
    candidates=[e for e in candidates if e&fresh and e&3]
    assert len(candidates)==36
    families=[base+extra for k in (1,2,3) for extra in combinations(candidates,k)]
    compiler=shutil.which('g++')
    if compiler is None:raise SystemExit('g++ is required')
    cpp=ROOT/'research/experiments/pure-triple-few-edge-grundy-20261107/independent.cpp'
    with tempfile.TemporaryDirectory(prefix='kyouen-eight-extensions-') as scratch:
        temp=Path(scratch).resolve();assert temp.parent==Path(tempfile.gettempdir()).resolve()
        data=temp/'cases.txt';exe=temp/'scan.exe';values=temp/'values.bin'
        data.write_text(str(len(families))+'\n'+'\n'.join(' '.join(map(str,[n,len(e),*e])) for e in families)+'\n',encoding='ascii')
        subprocess.run([compiler,'-std=c++17','-O3',str(cpp),'-o',str(exe)],check=True)
        native=json.loads(subprocess.check_output([str(exe),str(data),str(values)],text=True))
        result=values.read_bytes()
    assert len(result)==len(families)
    maximum=max(result);witness=[]
    if maximum>=10:
        i=next(i for i,g in enumerate(result) if g==maximum)
        actual=NORMAL.grundy(n,tuple(sorted(families[i])));assert actual==maximum
        witness=[dict(n=n,edges=families[i],grundy=actual)]
    output=dict(scope='all 1..3 new cover-two triples involving two new points above one fixed g8 family',
                cases=len(families),cpp_safe_states=native['safe_states'],histogram=dict(sorted(Counter(result).items())),
                maximum_found=maximum,witnesses=witness,limitation='not all twelve-point families')
    (directory/'output/extensions.json').write_text(json.dumps(output,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(output,indent=2),flush=True)


if __name__=='__main__':main()
