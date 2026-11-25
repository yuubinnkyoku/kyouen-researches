"""Classify every real lambda on 5x5, with two native all-safe-state solvers.

Uses the earlier independent Python determinant constructions for the catalog.
Binaries and temporary results live in the OS temporary directory, not D:.
"""
import argparse
from fractions import Fraction
import importlib.util
from itertools import combinations
import json
import os
from pathlib import Path
import subprocess
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]


def load_geometry():
    path=ROOT/'research/experiments/quadratic-lambda-20261024/verify.py'
    spec=importlib.util.spec_from_file_location('quadratic_geometry',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def build(directory):
    compiler=os.environ.get('CXX','g++')
    outputs=[]
    for stem in ('census','audit'):
        exe=directory/(stem+('.exe' if os.name=='nt' else ''))
        subprocess.run([compiler,'-std=c++17','-O3','-Wall','-Wextra',str(HERE/(stem+'.cpp')),'-o',str(exe)],check=True)
        outputs.append(exe)
    return outputs


def catalog(n,geometry):
    points=[(x,y) for y in range(n) for x in range(n)]
    common=[]; exceptional={}
    for ids in combinations(range(n*n),4):
        a,b=geometry.coefficients([points[i] for i in ids])
        mask=sum(1<<i for i in ids)
        if a==b==0:
            common.append(mask)
        elif a:
            exceptional.setdefault(Fraction(-b,a),[]).append(mask)
    return common,exceptional


def native(exe,n,value,dump=None):
    args=['generic'] if value=='generic' else [str(value.numerator),str(value.denominator)]
    env=os.environ.copy();env.pop('KYOUEN_GRUNDY_DUMP',None)
    if dump is not None:env['KYOUEN_GRUNDY_DUMP']=str(dump)
    return json.loads(subprocess.check_output([str(exe),str(n),*args],env=env))


def compare(exe,audit,n,value,edges):
    dump_a=exe.parent/'grundy-primary.bin';dump_b=exe.parent/'grundy-independent.bin'
    row=native(exe,n,value,dump=dump_a)
    assert sorted(row.pop('edges'))==sorted(edges),(n,str(value),'geometry')
    raw=f'{n*n} {len(edges)}\n'+' '.join(map(str,edges))+'\n'
    env=os.environ.copy();env['KYOUEN_GRUNDY_DUMP']=str(dump_b)
    other=json.loads(subprocess.check_output([str(audit)],input=raw.encode('ascii'),env=env))
    for key,expected in other.items():
        assert row[key]==expected,(n,str(value),key)
    assert dump_a.stat().st_size==dump_b.stat().st_size==1<<(n*n)
    with dump_a.open('rb') as left,dump_b.open('rb') as right:
        while True:
            a,b=left.read(1<<20),right.read(1<<20)
            assert a==b,(n,str(value),'individual Grundy values')
            if not a:break
    row['lambda']=str(value)
    row['independent_safe_count']=other['safe_count']
    row['individual_values_equal']=True
    return row


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=HERE/'results.json')
    args=parser.parse_args()
    directory=Path(tempfile.gettempdir())/'kyouen-quadratic-lambda-five-20261024'
    directory.mkdir(exist_ok=True)
    exe,audit=build(directory)
    geometry=load_geometry()
    old=json.loads((ROOT/'research/experiments/quadratic-lambda-20261024/results.json').read_text(encoding='utf-8'))
    old_count=0
    for board in old['boards']:
        for row in board['classes']:
            value='generic' if row['lambda']=='generic' else Fraction(row['lambda'])
            native_row=native(exe,board['side'],value)
            for key in ('empty_grundy','safe_count','first_move_grundy'):
                assert native_row[key]==row[key]
            for key in ('safe_layers','terminal_sizes','grundy_histogram'):
                assert {str(i):v for i,v in enumerate(native_row[key]) if v}==row[key]
            assert sorted(native_row['edges'])==sorted(board['universal_edges']+row['extra_edges'])
            old_count+=1
    print('Old classes matched:',old_count,flush=True)
    common,exceptional=catalog(5,geometry)
    result={'side':5,'rule':'det[x*x+lambda*y*y,x,y,1]=0','point_index':'i=y*5+x',
            'old_classes_native_matched':old_count,'universal_edges':common,'classes':[]}
    families=[('generic',[])]+[(v,exceptional[v]) for v in sorted(exceptional)]
    print('New parameter classes:',len(families),flush=True)
    for index,(value,extra) in enumerate(families):
        row=compare(exe,audit,5,value,common+extra)
        row['extra_edges']=sorted(extra)
        result['classes'].append(row)
        if index%10==0 or row['empty_grundy']!=1:
            print(index+1,'/',len(families),str(value),'g',row['empty_grundy'],'safe',row['safe_count'],flush=True)
        # A checkpoint allows the bounded finite census to resume inspection on failure.
        (directory/'checkpoint.json').write_text(json.dumps(result),encoding='utf-8')
    args.output.write_text(json.dumps(result,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    (directory/'grundy-primary.bin').unlink()
    (directory/'grundy-independent.bin').unlink()
    print('All classes independently matched; result:',args.output,flush=True)


if __name__=='__main__':
    main()
