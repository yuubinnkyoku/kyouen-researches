#!/usr/bin/env python3
"""Fixed A/B study of immutable per-frame geometry; no search tuning."""
import argparse,hashlib,itertools,json,pathlib,random,statistics,subprocess,sys
HERE=pathlib.Path(__file__).resolve().parent;ROOT=HERE.parents[2]
PRIOR=HERE.parent/'residual-attempt-allocation-20261022/fixtures.json'
sys.path.insert(0,str(HERE.parent/'residual-dfpn-integration-20261021'))
from integration import parse,roots_csv
sys.path.insert(0,str(HERE.parent/'n11-search-methods/scripts'))
from dfpn_edge_classes import forbidden,d4_canonical_key
CORE=('cpp/solvers/kyouen_dfpn_root.cpp','cpp/solvers/kyouen_residual_micro.hpp')
LOGICAL=('result','reason','nodes','visited','expansions','exact_nodes','pn_nodes','residual_calls')
def read(name):return json.loads((HERE/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def write(name,data):
    path=HERE/name;assert not path.exists(),f'cannot overwrite {path}'
    path.write_text(json.dumps(data,indent=2)+'\n')
def committed(name):
    path=HERE/name
    assert subprocess.check_output(['git','show',f'HEAD:{path.relative_to(ROOT)}'],cwd=ROOT)==path.read_bytes()
def fixtures():
    old=json.loads(PRIOR.read_text())
    reused=[dict(f,id=f'reused-{i}',group='reused') for i,f in enumerate(old['train'])]
    seen={d4_canonical_key(f['occupied']) for f in old['train']+old['confirm']}
    rng=random.Random(2026102203);fresh=[]
    while len(fresh)<6:
        occ=sorted(rng.sample(range(121),5));key=d4_canonical_key(occ)
        if key in seen or any(forbidden(*q) for q in itertools.combinations(occ,4)):continue
        seen.add(key)
        legal=[v for v in range(121) if v not in occ and not any(forbidden(*t,v) for t in itertools.combinations(occ,3))]
        fresh.append(dict(id=f'fresh-{len(fresh)}',group='fresh',occupied=occ,legal=len(legal),expected=0))
    late=[dict(f,group='late') for f in old['late']]
    return reused+fresh+late
def freeze(solver):
    for name in CORE:assert subprocess.check_output(['git','show',f'HEAD:{name}'],cwd=ROOT)==(ROOT/name).read_bytes()
    data=fixtures();write('fixtures.json',data);(HERE/'roots').mkdir(exist_ok=True)
    for f in data:roots_csv(HERE/'roots'/f'{f["id"]}.csv',[f['occupied']])
    write('protocol.json',dict(seed=2026102203,settings=['off','cache'],repeats=3,deep_limits=[20000,100000],late_limit=20000,
        audit='first three reused roots, 2000 work each, cache + fresh-list audit; excluded from timing',
        design='parameter-free immutable frame geometry reuse; all inputs committed before measurements; no tuning/selection',
        pairing='require identical result/reason/work/expansions and off builds = cache builds + refreshes',
        defaults='cache remains explicit; residual and native exact handoffs OFF',memo_power=18,wall_guard=30,
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source_hashes={p:sha(ROOT/p) for p in CORE},solver_sha256=sha(pathlib.Path(solver)),
        compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],compile_flags='-std=c++20 -O2',
        fixtures_sha256=sha(HERE/'fixtures.json'),prior_sha256=sha(PRIOR),
        roots_sha256={p.name:sha(p) for p in (HERE/'roots').glob('*.csv')},
        verdict_policy='stop and independently verify any newly decided deep root before adoption'))
def validate(raw,f,cache,limit,audit=False):
    rows=parse(raw);assert len(rows)==1;r=rows[0]
    assert r['seq']==1 and r['stones']==len(f['occupied'])
    assert r['occupied_lo']==sum(1<<v for v in f['occupied'] if v<64)
    assert r['occupied_hi']==sum(1<<(v-64) for v in f['occupied'] if v>=64)
    assert r['node_limited']==1 and r['node_budget']==limit and r['exact_nodes']==0
    assert r['residual_gate']==r['residual_calls']==r['pn_enabled']==r['pn_nodes']==0
    assert r['frame_cache']==int(cache) and r['frame_audit']==int(audit)
    assert r['result']==f['expected'],'new deep verdict requires independent validation'
    assert r['build_ns']==r['structure_ns']==r['grundy_ns']==0
    assert r['geometry_builds']>=0 and r['geometry_moves']>=0 and r['child_refreshes']>=0
    if not cache:assert r['child_refreshes']==r['child_audits']==0
    elif audit:assert r['child_audits']==r['child_refreshes']>0
    else:assert r['child_audits']==0
    return r
def pair(off,on):
    for key in LOGICAL:assert off[key]==on[key],f'logical drift in {key}'
    assert off['geometry_builds']==on['geometry_builds']+on['child_refreshes']
    assert on['geometry_moves']<=off['geometry_moves']
def aggregate(rows):
    totals={}
    for group,limit,setting in sorted({(r['group'],r['limit'],r['setting']) for r in rows}):
        chosen=[r for r in rows if (r['group'],r['limit'],r['setting'])==(group,limit,setting)]
        groups=[[r for r in chosen if r['id']==i] for i in sorted({r['id'] for r in chosen})]
        for g in groups:
            assert len(g)==3 and {r['repeat'] for r in g}=={0,1,2}
            if not any(r['reason']=='TIME_BUDGET' for r in g):assert len({tuple(r[k] for k in LOGICAL) for r in g})==1
        totals[f'{group}-n{limit}-{setting}']=dict(unknown=sum(any(r['result']==0 for r in g) for g in groups),
            watchdogs=sum(r['reason']=='TIME_BUDGET' for r in chosen),
            **{k:sum(statistics.median(r[k] for r in g) for g in groups)
                for k in ('solve_us','nodes','expansions','geometry_builds','geometry_moves','child_refreshes')})
    return totals
def run(solver,data):
    (HERE/'raw').mkdir(exist_ok=True);rows=[];audits=[]
    def one(f,cache,limit,repeat,audit=False):
        setting='cache' if cache else 'off';stem=f'{f["id"]}-{setting}-n{limit}-r{repeat}'+('-audit' if audit else '')
        output=HERE/'raw'/f'{stem}.csv';assert not output.exists()
        cmd=[solver,'--n=11','--memo=18','--budget=30','--exact-legal=0','--residual-outcome-budget=128',
            f'--node-budget={limit}',f'--roots-csv={HERE/"roots"/(f["id"]+".csv")}',f'--csv={output}',f'--log={HERE/"raw"/(stem+".log")}']
        if cache:cmd+=['--frame-children-audit' if audit else '--frame-children-cache']
        subprocess.run(cmd,check=True,timeout=45,stdout=subprocess.DEVNULL)
        r=validate(output.read_text(),f,cache,limit,audit)
        print(stem,r['solve_us'],r['geometry_builds'],r['child_refreshes'],flush=True)
        return dict(id=f['id'],group=f['group'],setting=setting,limit=limit,repeat=repeat,raw=str(output.relative_to(HERE)),**r)
    for f in data[:3]:audits.append(one(f,True,2000,0,True))
    write('audits.json',audits)
    for repeat in range(3):
        for j,limit in enumerate((20000,100000)):
            order=(False,True) if (repeat+j)%2==0 else (True,False)
            for cache in order:
                for f in data:
                    if f['group']=='late' and limit!=20000:continue
                    rows.append(one(f,cache,limit,repeat))
    for f in data:
        for limit in ([20000] if f['group']=='late' else [20000,100000]):
            for repeat in range(3):
                selected=[r for r in rows if (r['id'],r['limit'],r['repeat'])==(f['id'],limit,repeat)]
                assert len(selected)==2;pair(next(r for r in selected if r['setting']=='off'),next(r for r in selected if r['setting']=='cache'))
    write('records.json',rows);write('summary.json',dict(totals=aggregate(rows),protocol_sha256=sha(HERE/'protocol.json')))
def verify(p,data):
    assert data==fixtures() and sha(PRIOR)==p['prior_sha256']
    for name,value in p['source_hashes'].items():
        blob=subprocess.run(['git','show',f'{p["source_commit"]}:{name}'],cwd=ROOT,capture_output=True)
        if blob.returncode==0:assert hashlib.sha256(blob.stdout).hexdigest()==value
    lookup={f['id']:f for f in data};rows=read('records.json');assert len(rows)==336
    keys=set()
    for r in rows:
        key=(r['id'],r['setting'],r['limit'],r['repeat']);assert key not in keys;keys.add(key)
        actual=validate((HERE/r['raw']).read_text(),lookup[r['id']],r['setting']=='cache',r['limit'])
        assert actual=={k:v for k,v in r.items() if k in actual}
    expected={(f['id'],s,n,r) for f in data for s in ('off','cache') for n in ([20000] if f['group']=='late' else [20000,100000]) for r in range(3)}
    assert keys==expected
    bykey={(r['id'],r['setting'],r['limit'],r['repeat']):r for r in rows}
    for i,s,n,r in keys:
        if s=='off':pair(bykey[i,'off',n,r],bykey[i,'cache',n,r])
    audits=read('audits.json');assert len(audits)==3 and [r['id'] for r in audits]==[f['id'] for f in data[:3]]
    for r in audits:
        actual=validate((HERE/r['raw']).read_text(),lookup[r['id']],True,2000,True)
        assert actual=={k:v for k,v in r.items() if k in actual}
    assert aggregate(rows)==read('summary.json')['totals']
    assert read('summary.json')['protocol_sha256']==sha(HERE/'protocol.json')
    print('VERIFIED 336 timed root evaluations + 3 fresh-list audits; identical logical work and geometry-build substitution')
def main():
    p=argparse.ArgumentParser();p.add_argument('phase',choices=['freeze','run','verify']);p.add_argument('--solver',default='/tmp/dfpn-frame');a=p.parse_args()
    if a.phase=='freeze':freeze(a.solver);return
    p=read('protocol.json');data=read('fixtures.json')
    assert p['seed']==2026102203 and p['settings']==['off','cache'] and p['repeats']==3 and p['deep_limits']==[20000,100000] and p['late_limit']==20000
    assert sha(HERE/'fixtures.json')==p['fixtures_sha256']
    assert set(p['roots_sha256'])=={f'{f["id"]}.csv' for f in data}
    for name,value in p['roots_sha256'].items():assert sha(HERE/'roots'/name)==value
    if a.phase=='run':
        committed('protocol.json');committed('fixtures.json');assert sha(pathlib.Path(a.solver))==p['solver_sha256']
        run(a.solver,data)
    else:verify(p,data)
if __name__=='__main__':main()
