"""Re-run the historical 17-site proof's exact finite portions without editing them."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
from itertools import combinations
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=ROOT/'research/experiments/three-parallel-q6-17-20261018'


def witness():
    # Exact example showing why the E>=13 hypothesis cannot simply be dropped.
    b=(-40,-32,-24,-16,0);c=(-37,-35,-27,-5,13)
    u=F(2,5);a=F(-154,5);d2=F(71)
    cs=[]
    for x,y in combinations(b,2):
        for z,w in combinations(c,2):
            if x+y==z+w:cs.append((x+y,z*w-x*y,x*y))
    through=[row for row in cs if d2*u*(u-1)+a*a-row[0]*a+row[1]*u+row[2]==0]
    assert len(cs)==6 and len(through)==4
    # Also check the circle equation in unnormalized x=sqrt(71)*v coordinates.
    # x^2+y^2+A*x+B*y+C=0, with A*sqrt(71)=delta-d2, B=-s, C=p.
    for s,delta,p in through:
        assert sum(y*y-s*y+p==0 for y in b)==2
        assert sum(y*y-s*y+p+delta==0 for y in c)==2
        assert d2*u*u+a*a+(delta-d2)*u-s*a+p==0
    return {'B':list(b),'C':list(c),'d_squared':71,'u':'2/5','a':'-154/5',
            'energy':6,'circles_through_point':4,'circle_coefficients':through}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--cxx',default=shutil.which('g++') or 'g++')
    args=parser.parse_args();receipt={'python':{},'cpp':{},'source_sha256':{}}
    for name in ('proof.md','verify.py','verify_e13.py','audit_independent.cpp','audit_e13_independent.cpp'):
        receipt['source_sha256'][str((OLD/name).relative_to(ROOT)).replace('\\','/')]=hashlib.sha256((OLD/name).read_bytes()).hexdigest()
    for name in ('verify.py','verify_e13.py'):
        print('Checking',name,flush=True)
        result=subprocess.run([sys.executable,str(OLD/name)],check=True,text=True,capture_output=True)
        receipt['python'][name]=json.loads(result.stdout)
    p=receipt['python'];e=p['verify_e13.py']
    assert e['rational']=={'rational_candidates_after_safe_pruning':6173662,'matching_labeled_cases':60,
                         'unique_normalized_cases':1,'family_hit_counts':[0,0,60],'compatible_four_circle_sets':0}
    assert e['ap']['ap_partner_candidates']==5005 and e['ap']['energy13_partner_shapes']==8
    assert [r['symbolic_candidates'] for r in e['generic']]==[544]*3
    with tempfile.TemporaryDirectory(prefix='kyouen-q6-seventeen-') as temporary:
        for name in ('audit_independent.cpp','audit_e13_independent.cpp'):
            print('Checking',name,flush=True)
            binary=Path(temporary)/(Path(name).stem+('.exe' if sys.platform=='win32' else ''))
            subprocess.run([args.cxx,'-std=c++17','-O2',str(OLD/name),'-o',str(binary)],check=True)
            result=subprocess.run([str(binary)],check=True,text=True,capture_output=True)
            receipt['cpp'][name]={'stdout':result.stdout,'stderr':result.stderr}
    small=receipt['cpp']['audit_independent.cpp']['stdout']
    assert small.strip()=='candidates=182 mixed_hits=2 mixed_compatible_four=0 offset_compatible_four=2 offset_determinants=-320,320 same_AP_compatible_four=0 PASS'
    large=receipt['cpp']['audit_e13_independent.cpp']
    assert re.search(r'tested_candidates=6173662 hits=60 unique=1 compatible_four=0\b',large['stdout'])
    assert 'k=2 t=1/1 B=0,1,2,3,5, C2=-2,2,4,6,8, four=0' in large['stdout']
    for k in range(3):
        assert f'generic family={k} candidates=544 high_energy=1' in large['stderr']
        assert f'family={k} E13H14hits={60 if k==2 else 0}' in large['stderr']
    assert 'AP E13 candidates=5005 hits=8 compatible_four=0' in large['stderr']
    receipt['low_energy_four_circle_witness']=witness()
    receipt['status']='all finite portions independently reproduced; universal reductions audited in audit.md'
    (HERE/'audit.json').write_text(json.dumps(receipt,separators=(',',':'))+'\n',encoding='utf-8',newline='\n')
    print(receipt['status'],flush=True)


if __name__=='__main__':main()
