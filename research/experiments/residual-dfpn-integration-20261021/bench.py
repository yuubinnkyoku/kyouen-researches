#!/usr/bin/env python3
"""Frozen normal df-pn comparison; each process has one root and a cold TT."""
import argparse,hashlib,json,pathlib,statistics,subprocess,time
from integration import parse,roots_csv
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
LATE=HERE.parent/'residual-quota-calibration-20261021/fixtures.json'
DEEP=HERE.parent/'residual-gate-calibration-20261021/stress-input.csv'
LIMITS=(20000,100000)
SETTINGS=('off','pn128-g6')
def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path,data):path.write_text(json.dumps(data,indent=2)+'\n')

def fixtures():
    rows=[]
    for f in json.loads(LATE.read_text())['new']:
        rows.append(dict(id=len(rows),group='late',occupied=f['occupied'],legal=len(f['legal']),expected=f['result']))
    for line in DEEP.read_text().splitlines():
        cells=line.split(',');mask=int(cells[3])|(int(cells[4])<<64)
        rows.append(dict(id=len(rows),group='deep',occupied=[v for v in range(121) if mask>>v&1],legal=int(cells[5]),expected=0))
    assert len(rows)==29
    return rows

def parse_root(raw,f,setting,limit,repeat):
    rows=parse(raw);assert len(rows)==1
    r=rows[0];assert r['seq']==1 and r['node_limited']==1 and r['node_budget']==limit
    assert r['exact_nodes']==0 and r['nodes']==r['visited']
    assert r['stones']==len(f['occupied'])
    assert r['occupied_lo']==sum(1<<v for v in f['occupied'] if v<64)
    assert r['occupied_hi']==sum(1<<(v-64) for v in f['occupied'] if v>=64)
    assert r['residual_gate']==(6 if setting=='pn128-g6' else 0)
    assert r['pn_enabled']==int(setting=='pn128-g6')
    if setting=='pn128-g6':assert r['pn_budget']==128
    else:assert r['pn_nodes']==r['residual_calls']==0
    assert r['pn_aborts']<=1
    assert r['build_ns']==r['structure_ns']==r['grundy_ns']==0 # no phase-clock overhead
    if f['group']=='deep':assert r['result']==0,'new deep verdict requires independent validation before adoption'
    else:assert r['result']==0 or r['result']==f['expected']
    if r['result']!=0:assert r['reason']=='DONE'
    return dict(id=f['id'],group=f['group'],setting=setting,limit=limit,repeat=repeat,**r)

def aggregate(records):
    totals={}
    for group in ('late','deep'):
        totals[group]={}
        for limit in LIMITS:
            totals[group][str(limit)]={}
            for setting in SETTINGS:
                selected=[r for r in records if r['group']==group and r['limit']==limit and r['setting']==setting]
                ids=sorted({r['id'] for r in selected});assert len(ids)==(26 if group=='late' else 3)
                med=[]
                for i in ids:
                    roots=[r for r in selected if r['id']==i];assert len(roots)==3 and {r['repeat'] for r in roots}=={0,1,2}
                    if not any(r['reason']=='TIME_BUDGET' for r in roots):
                        assert len({(r['result'],r['nodes'],r['residual_calls'],r['pn_nodes'],r['pn_aborts']) for r in roots})==1
                    med.append(dict(unknown=int(any(r['result']==0 for r in roots)),watchdog_runs=sum(r['reason']=='TIME_BUDGET' for r in roots),
                        **{k:statistics.median(r[k] for r in roots) for k in ('solve_us','process_us','nodes','visited','expansions','exact_nodes','pn_nodes','pn_aborts','residual_calls')}))
                totals[group][str(limit)][setting]={k:sum(r[k] for r in med) for k in med[0]}
    return totals

def freeze(solver):
    assert not (HERE/'protocol.json').exists(),'already frozen; use a new experiment'
    for name in ('cpp/solvers/kyouen_dfpn_root.cpp','cpp/solvers/kyouen_residual_micro.hpp'):
        assert subprocess.check_output(['git','show',f'HEAD:{name}'],cwd=ROOT)==(ROOT/name).read_bytes(),'commit solver source first'
    data=fixtures();(HERE/'roots').mkdir(exist_ok=True)
    for f in data:roots_csv(HERE/'roots'/f'{f["id"]:02}.csv',[f['occupied']])
    dump(HERE/'fixtures.json',data)
    protocol=dict(limits=list(LIMITS),settings=list(SETTINGS),repeats=3,memo_power=18,wall_guard_seconds=30,
        node_definition='df-pn frame iterations + admitted exact board nodes; P/N quota separate',quota=128,gate=6,
        late_sha256=digest(LATE),deep_sha256=digest(DEEP),fixtures_sha256=digest(HERE/'fixtures.json'),
        roots_sha256={p.name:digest(p) for p in sorted((HERE/'roots').glob('*.csv'))},
        solver_sha256=digest(pathlib.Path(solver)),source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        source_hashes={p:digest(ROOT/p) for p in ('cpp/solvers/kyouen_dfpn_root.cpp','cpp/solvers/kyouen_residual_micro.hpp')},
        compiler=subprocess.check_output(['g++','--version'],text=True).splitlines()[0],
        order='rotate settings by repeat and budget index; root order fixed; fresh process per root; exact-legal=0',
        newly_decided_policy='stop on a new deep verdict and independently validate before adopting',
        watchdog_policy='retain every watchdog row and report counts; require deterministic node counts only without watchdog',
        default_policy='residual gate remains OFF; no parameter tuning from this comparison')
    dump(HERE/'protocol.json',protocol);print('FROZEN 26 late + 3 deep, node limits 20000/100000, OFF/PN128-g6, three repeats')

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);p.add_argument('--freeze',action='store_true');args=p.parse_args()
    if args.freeze:freeze(args.solver);return
    assert not (HERE/'summary.json').exists(),'archived comparison cannot be overwritten'
    protocol=json.loads((HERE/'protocol.json').read_text());data=json.loads((HERE/'fixtures.json').read_text())
    assert digest(pathlib.Path(args.solver))==protocol['solver_sha256']
    for name in ('protocol.json','fixtures.json'):
        path=HERE/name
        assert subprocess.check_output(['git','show',f'HEAD:{path.relative_to(ROOT)}'],cwd=ROOT)==path.read_bytes(),'commit frozen inputs first'
    for name,value in protocol['roots_sha256'].items():assert digest(HERE/'roots'/name)==value
    (HERE/'raw').mkdir(exist_ok=True)
    records=[]
    for repeat in range(3):
        for j,limit in enumerate(LIMITS):
            shift=(repeat+j)%2;order=SETTINGS[shift:]+SETTINGS[:shift]
            for setting in order:
                for f in data:
                    prefix=f'{setting}-n{limit}-r{repeat}-id{f["id"]:02}'
                    output=HERE/'raw'/f'{prefix}.csv';log=HERE/'raw'/f'{prefix}.log'
                    output.unlink(missing_ok=True);log.unlink(missing_ok=True)
                    source=HERE/'roots'/f'{f["id"]:02}.csv'
                    cmd=[args.solver,'--n=11','--memo=18',f'--roots-csv={source}',
                        f'--node-budget={limit}','--exact-legal=0','--budget=30',f'--csv={output}',f'--log={log}']
                    if setting=='pn128-g6':cmd+=['--residual-exact-legal=6','--residual-evaluator=outcome','--residual-outcome-budget=128']
                    start=time.monotonic_ns();subprocess.run(cmd,check=True,timeout=45)
                    r=parse_root(output.read_text(),f,setting,limit,repeat);r['process_us']=(time.monotonic_ns()-start)//1000;records.append(r)
                    print(f'{setting} limit={limit} repeat={repeat} id={f["id"]} result={r["result"]} nodes={r["nodes"]} solve_us={r["solve_us"]}',flush=True)
    dump(HERE/'records.json',records);dump(HERE/'summary.json',dict(totals=aggregate(records),protocol_sha256=digest(HERE/'protocol.json')))
    print(json.dumps(json.loads((HERE/'summary.json').read_text()),indent=2))
if __name__=='__main__':main()
