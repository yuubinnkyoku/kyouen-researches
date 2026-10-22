#!/usr/bin/env python3
"""Known-board compatibility matrix, not a timing or unknown-board study."""
import argparse,hashlib,itertools,json,pathlib,subprocess,sys,tempfile
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
sys.path.insert(0,str(HERE.parent/'residual-dfpn-integration-20261021'))
from integration import parse,roots_csv,expected_late
ROOTS={'empty':[], 'odd':[0,1,2,4,9], 'even':[0,1,3,5,8,14]}
N11_SOURCE=HERE.parent/'dfpn-frame-children-20261022/fixtures.json'
N11_ROWS=[f for f in json.loads(N11_SOURCE.read_text()) if f['group']=='late']
N11={f'n11-{parity}':next(f for f in N11_ROWS if len(f['occupied'])%2==parity) for parity in (0,1)}
ROOTS.update({name:f['occupied'] for name,f in N11.items()})
PUBLISH=('all','root','separate');RESIDUAL=('none','sg6','pn6','slice8')
CORE=('cpp/solvers/kyouen_dfpn_root.cpp','cpp/solvers/kyouen_residual_micro.hpp','cpp/tests/test_kyouen_frame_children.cpp',str(N11_SOURCE.relative_to(ROOT)))
LOGICAL=('result','reason','nodes','visited','expansions','exact_nodes','residual_calls','pn_nodes','pn_aborts','pn_remaining','pn_attempted','pn_attempt_skips')
def read(name):return json.loads((HERE/name).read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def write(name,data):
    p=HERE/name;assert not p.exists();p.write_text(json.dumps(data,indent=2)+'\n')
def cases():
    out=[]
    for publish,residual,limit,root,fast in itertools.product(PUBLISH,RESIDUAL,(0,7,2000),('empty','odd','even'),(False,True)):
        out.append(dict(id=len(out),group='matrix',n=4,publish=publish,residual=residual,limit=limit,roots=[root],fast=fast))
    for publish,residual,fast in itertools.product(PUBLISH,RESIDUAL,(False,True)):
        out.append(dict(id=len(out),group='repeat',n=4,publish=publish,residual=residual,limit=2000,roots=['odd','odd','even','even'],fast=fast))
    for fast in (False,True):out.append(dict(id=len(out),group='deadline',n=4,publish='all',residual='none',limit=2000,roots=['empty'],fast=fast))
    for name,publish,residual,fast in itertools.product(N11,('all','separate'),('none','pn6'),(False,True)):
        out.append(dict(id=len(out),group='n11',n=11,publish=publish,residual=residual,limit=2000,roots=[name],fast=fast))
    assert len(out)==258
    return out
def expected(name):return N11[name]['expected'] if name in N11 else (2 if name=='empty' else expected_late(ROOTS[name]))
def validate(raw,header,case):
    fields=dict(token.split('=',1) for token in header.split() if '=' in token)
    assert fields.get('n')==str(case['n']) and fields.get('exact_publish')==case['publish']
    assert all(fields.get(key)==value for key,value in [('exact_legal','8'),('exact_budget','8'),('exact_retries','2')])
    rows=parse(raw);assert len(rows)==len(case['roots'])
    residual=case['residual'];quota=23 if residual=='slice8' else 128
    for seq,(r,name) in enumerate(zip(rows,case['roots']),1):
        root=ROOTS[name]
        assert r['seq']==seq and r['stones']==len(root) and r['occupied_lo']==sum(1<<v for v in root if v<64) and r['occupied_hi']==sum(1<<(v-64) for v in root if v>=64)
        assert r['node_limited']==1 and r['node_budget']==case['limit']
        assert r['frame_expand_reuse']==r['frame_cache']==int(case['fast']) and r['frame_audit']==r['child_audits']==0
        assert r['frame_expand_uses']<=r['expansions']
        if not case['fast']:assert r['child_refreshes']==r['frame_expand_uses']==0
        assert r['residual_gate']==({'none':0,'sg6':6,'pn6':6,'slice8':16}[residual])
        assert r['pn_enabled']==int(residual in ('pn6','slice8')) and r['pn_budget']==quota
        assert r['pn_attempt_budget']==(8 if residual=='slice8' else 0)
        if residual=='slice8':
            assert r['residual_calls']==r['pn_attempted'] and r['pn_attempt_max']<=8
            assert r['pn_aborts']<=r['pn_attempted']<=r['pn_nodes']<=8*r['pn_attempted']
        else:assert r['pn_aborts']<=1 and r['pn_attempted']==r['pn_attempt_skips']==0
        if case['group']=='deadline':assert r['result']==0 and r['reason']=='TIME_BUDGET' and r['nodes']==0
        else:
            assert r['reason'] in ('DONE','NODE_BUDGET')
            assert r['result']==0 or r['result']==expected(name)
        if case['group']=='n11':assert r['result']==expected(name)
        if case['group']=='repeat':
            assert r['result']==expected(name)
            if seq in (2,4):
                assert r['pn_nodes']==r['residual_calls']==r['exact_nodes']==0
                assert r['geometry_builds']==r['geometry_moves']==r['child_refreshes']==r['frame_expand_uses']==0
                assert r['pn_remaining']==quota and r['pn_attempted']==r['pn_attempt_skips']==0
    return rows
def compare(off,fast):
    assert len(off)==len(fast)
    for a,b in zip(off,fast):
        for key in LOGICAL:assert a[key]==b[key],key
        assert a['geometry_builds']==b['geometry_builds']+b['child_refreshes']
        assert b['geometry_moves']<=a['geometry_moves']
def verify_records(records):
    byid={r['case']['id']:r for r in records};assert len(byid)==len(records)==258
    for case in cases():
        r=byid[case['id']];assert r['case']==case
        assert validate(r['raw_csv'],r['header'],case)==r['rows']
    paired={}
    for record in records:
        c=record['case'];key=(c['group'],c['publish'],c['residual'],c['limit'],tuple(c['roots']))
        paired.setdefault(key,{})[c['fast']]=record['rows']
    for modes in paired.values():assert set(modes)=={False,True};compare(modes[False],modes[True])
    assert len(paired)==129 and sum(len(r['rows']) for r in records)==330
    flat=[(record['case'],row) for record in records for row in record['rows']]
    assert any(row['exact_nodes']>0 for case,row in flat)
    assert any(case['residual']=='sg6' and row['residual_calls']>0 for case,row in flat)
    assert any(case['residual']=='pn6' and row['pn_nodes']>0 for case,row in flat)
    assert any(case['residual']=='slice8' and row['pn_aborts']>1 for case,row in flat)
    assert any(case['fast'] and row['frame_expand_uses']>0 for case,row in flat)
    return dict(processes=258,root_evaluations=330,pairs=129,matrix=216,repeated_roots=96,deadline_roots=2,n11_known_roots=16)
def freeze(solver):
    for name in CORE:assert subprocess.check_output(['git','show',f'HEAD:{name}'],cwd=ROOT)==(ROOT/name).read_bytes()
    write('protocol.json',dict(cases=cases(),roots=ROOTS,expected={k:expected(k) for k in ROOTS},
        design='known n4 regression and two known n11 late roots; no performance inference, no unknown n11 search',
        cpp_matrix='192 configurations x baseline/audited-expand x budgets7/2000, with persistent solver per resume',
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source_hashes={p:sha(ROOT/p) for p in CORE},solver_sha256=sha(pathlib.Path(solver)),
        compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],compile_flags='-std=c++20 -O2 -DNDEBUG'))
def run(solver):
    assert not (HERE/'records.json').exists()
    records=[]
    with tempfile.TemporaryDirectory() as directory:
        tmp=pathlib.Path(directory)
        for case in cases():
            output=tmp/'output.csv';log=tmp/'log.txt';output.unlink(missing_ok=True);log.unlink(missing_ok=True)
            cmd=[solver,f'--n={case["n"]}','--memo=12','--budget=5',f'--node-budget={case["limit"]}',f'--csv={output}',f'--log={log}',
                '--exact-legal=8','--exact-budget=8','--exact-retries=2','--residual-outcome-budget=128',f'--exact-publish={case["publish"]}']
            if case['roots']==['empty']:cmd+=['--empty']
            else:
                source=tmp/'roots.csv';roots_csv(source,[ROOTS[name] for name in case['roots']]);cmd+=[f'--roots-csv={source}']
            if case['fast']:cmd+=['--frame-children-expand-reuse']
            if case['residual']!='none':
                cmd += [f'--residual-exact-legal={16 if case["residual"]=="slice8" else 6}',
                    f'--residual-evaluator={"grundy" if case["residual"]=="sg6" else "outcome"}']
            if case['residual']=='slice8':cmd+=['--residual-outcome-budget=23','--residual-attempt-budget=8']
            if case['group']=='deadline':cmd+=['--budget=0.000000000001']
            subprocess.run(cmd,check=True,timeout=20,stdout=subprocess.DEVNULL)
            raw=output.read_text();header=log.read_text().splitlines()[0]
            records.append(dict(case=case,raw_csv=raw,header=header,rows=validate(raw,header,case)))
    totals=verify_records(records);write('records.json',records)
    write('summary.json',dict(totals=totals,protocol_sha256=sha(HERE/'protocol.json')))
    print('VERIFIED',totals)
def main():
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['freeze','run','verify']);p.add_argument('--solver',default='/tmp/dfpn-combined');a=p.parse_args()
    if a.phase=='freeze':freeze(a.solver);return
    protocol=read('protocol.json')
    assert protocol['cases']==cases() and protocol['roots']==ROOTS and protocol['expected']=={k:expected(k) for k in ROOTS}
    if a.phase=='run':
        path=HERE/'protocol.json';assert subprocess.check_output(['git','show',f'HEAD:{path.relative_to(ROOT)}'],cwd=ROOT)==path.read_bytes()
        assert sha(pathlib.Path(a.solver))==protocol['solver_sha256'];run(a.solver)
    else:
        totals=verify_records(read('records.json'));assert totals==read('summary.json')['totals']
        assert read('summary.json')['protocol_sha256']==sha(HERE/'protocol.json')
        for name,value in protocol['source_hashes'].items():
            blob=subprocess.run(['git','show',f'{protocol["source_commit"]}:{name}'],cwd=ROOT,capture_output=True)
            if blob.returncode==0:assert hashlib.sha256(blob.stdout).hexdigest()==value
        print('VERIFIED archived compatibility matrix',totals)
if __name__=='__main__':main()
