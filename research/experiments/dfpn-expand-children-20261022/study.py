#!/usr/bin/env python3
"""Three-way bounded study, reusing the preceding experiment's validators."""
import argparse,hashlib,importlib.util,itertools,json,pathlib,random,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
PREVIOUS=HERE.parent/'dfpn-frame-children-20261022'
sys.path.insert(0,str(PREVIOUS))
spec=importlib.util.spec_from_file_location('frame_baseline_study',PREVIOUS/'study.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
from integration import parse,roots_csv
from dfpn_edge_classes import forbidden,d4_canonical_key
SETTINGS=('off','cache','expand')
def read(name):return json.loads((HERE/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
    p=HERE/name;assert not p.exists(),f'cannot overwrite {p}';p.write_text(json.dumps(data,indent=2)+'\n')
def committed(name):
    p=HERE/name;assert subprocess.check_output(['git','show',f'HEAD:{p.relative_to(ROOT)}'],cwd=ROOT)==p.read_bytes()
def fixtures():
    prior=json.loads((PREVIOUS/'fixtures.json').read_text())
    old=json.loads((HERE.parent/'residual-attempt-allocation-20261022/fixtures.json').read_text())
    rows=[dict(f,id=f'reused-{i}') for i,f in enumerate(prior[:3])]
    seen={d4_canonical_key(f['occupied']) for f in prior+old['confirm']}
    rng=random.Random(2026102204)
    while len(rows)<9:
        occ=sorted(rng.sample(range(121),5));key=d4_canonical_key(occ)
        if key in seen or any(forbidden(*q) for q in itertools.combinations(occ,4)):continue
        seen.add(key);legal=[v for v in range(121) if v not in occ and not any(forbidden(*t,v) for t in itertools.combinations(occ,3))]
        rows.append(dict(id=f'fresh-{len(rows)-3}',group='fresh',occupied=occ,legal=len(legal),expected=0))
    return rows+[f for f in prior if f['group']=='late']
def validate(raw,f,setting,limit,audit=False):
    r=base.validate(raw,f,setting!='off',limit,audit)
    assert r['frame_expand_reuse']==int(setting=='expand')
    assert 0<=r['frame_expand_uses']<=r['expansions']
    if setting!='expand':assert r['frame_expand_uses']==0
    return r
def compare(off,cache,expanded):
    base.pair(off,cache);base.pair(off,expanded)
    assert cache['geometry_builds']==expanded['geometry_builds']+expanded['frame_expand_uses']
    assert expanded['child_refreshes']==cache['child_refreshes']+expanded['frame_expand_uses']
    assert expanded['geometry_moves']<=cache['geometry_moves']
def freeze(solver):
    for p in base.CORE:assert subprocess.check_output(['git','show',f'HEAD:{p}'],cwd=ROOT)==(ROOT/p).read_bytes()
    data=fixtures();write('fixtures.json',data);(HERE/'roots').mkdir(exist_ok=True)
    for f in data:roots_csv(HERE/'roots'/f'{f["id"]}.csv',[f['occupied']])
    write('protocol.json',dict(seed=2026102204,settings=SETTINGS,repeats=3,deep_limits=[20000,100000],late_limit=20000,
        audit='first three reused roots, expand+audit at 2000 work; excluded from timing',
        design='no tuning; three reused deep roots, six newly generated safe S5 roots, 26 reused known late roots',
        defaults='all options remain explicit; native exact/residual OFF in timing; memo18, wall30s, fresh process/TT',
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source_hashes={p:sha(ROOT/p) for p in base.CORE},solver_sha256=sha(pathlib.Path(solver)),
        compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],compile_flags='-std=c++20 -O2',
        fixtures_sha256=sha(HERE/'fixtures.json'),helper_sha256=sha(PREVIOUS/'study.py'),
        roots_sha256={p.name:sha(p) for p in (HERE/'roots').glob('*.csv')},
        verdict_policy='stop and independently verify any newly decided deep root before adoption'))
def run(solver,data):
    (HERE/'raw').mkdir(exist_ok=True)
    def one(f,setting,limit,repeat,audit=False):
        stem=f'{f["id"]}-{setting}-n{limit}-r{repeat}'+('-audit' if audit else '')
        output=HERE/'raw'/f'{stem}.csv';assert not output.exists()
        cmd=[solver,'--n=11','--memo=18','--budget=30','--exact-legal=0','--residual-outcome-budget=128',
            f'--node-budget={limit}',f'--roots-csv={HERE/"roots"/(f["id"]+".csv")}',f'--csv={output}',f'--log={HERE/"raw"/(stem+".log")}']
        if setting!='off':cmd+=['--frame-children-expand-reuse' if setting=='expand' else '--frame-children-cache']
        if audit:cmd+=['--frame-children-audit']
        subprocess.run(cmd,check=True,timeout=45,stdout=subprocess.DEVNULL)
        r=validate(output.read_text(),f,setting,limit,audit)
        print(stem,r['solve_us'],r['geometry_builds'],r['frame_expand_uses'],flush=True)
        return dict(id=f['id'],group=f['group'],setting=setting,limit=limit,repeat=repeat,raw=str(output.relative_to(HERE)),**r)
    write('audits.json',[one(f,'expand',2000,0,True) for f in data[:3]])
    rows=[]
    for repeat in range(3):
        for j,limit in enumerate((20000,100000)):
            shift=(repeat+j)%3;order=SETTINGS[shift:]+SETTINGS[:shift]
            for setting in order:
                for f in data:
                    if f['group']=='late' and limit!=20000:continue
                    rows.append(one(f,setting,limit,repeat))
    write('records.json',rows);write('summary.json',dict(totals=base.aggregate(rows),protocol_sha256=sha(HERE/'protocol.json')))
def verify(p,data):
    assert data==fixtures()
    rows=read('records.json');assert len(rows)==396
    lookup={f['id']:f for f in data};keys=set();bykey={}
    for r in rows:
        key=(r['id'],r['setting'],r['limit'],r['repeat']);assert key not in keys;keys.add(key);bykey[key]=r
        actual=validate((HERE/r['raw']).read_text(),lookup[r['id']],r['setting'],r['limit'])
        assert actual=={k:v for k,v in r.items() if k in actual}
    assert keys=={(f['id'],s,n,r) for f in data for s in SETTINGS for n in ([20000] if f['group']=='late' else [20000,100000]) for r in range(3)}
    for i,s,n,r in keys:
        if s=='off':compare(*(bykey[i,setting,n,r] for setting in SETTINGS))
    audits=read('audits.json');assert len(audits)==3
    assert [r['id'] for r in audits]==[f['id'] for f in data[:3]]
    for r in audits:
        actual=validate((HERE/r['raw']).read_text(),lookup[r['id']],'expand',2000,True)
        assert actual=={k:v for k,v in r.items() if k in actual}
    assert base.aggregate(rows)==read('summary.json')['totals']
    assert read('summary.json')['protocol_sha256']==sha(HERE/'protocol.json')
    for name,value in p['source_hashes'].items():
        blob=subprocess.run(['git','show',f'{p["source_commit"]}:{name}'],cwd=ROOT,capture_output=True)
        if blob.returncode==0:assert hashlib.sha256(blob.stdout).hexdigest()==value
    print('VERIFIED 396 three-way timed evaluations + 3 audits; identical work and exact initial/revisit build substitutions')
def main():
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['freeze','run','verify']);p.add_argument('--solver',default='/tmp/dfpn-expand');a=p.parse_args()
    if a.phase=='freeze':freeze(a.solver);return
    p=read('protocol.json');data=read('fixtures.json')
    assert p['settings']==list(SETTINGS) and p['seed']==2026102204 and p['repeats']==3 and p['deep_limits']==[20000,100000] and p['late_limit']==20000
    assert p['helper_sha256']==sha(PREVIOUS/'study.py') and p['fixtures_sha256']==sha(HERE/'fixtures.json')
    assert set(p['roots_sha256'])=={f'{f["id"]}.csv' for f in data}
    for name,value in p['roots_sha256'].items():assert sha(HERE/'roots'/name)==value
    if a.phase=='run':
        committed('protocol.json');committed('fixtures.json');assert sha(pathlib.Path(a.solver))==p['solver_sha256'];run(a.solver,data)
    else:verify(p,data)
if __name__=='__main__':main()
