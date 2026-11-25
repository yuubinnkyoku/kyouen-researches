#!/usr/bin/env python3
"""Frozen five-configuration, three-repeat cold-root comparison."""
import argparse,csv,hashlib,json,pathlib,statistics,subprocess
HERE=pathlib.Path(__file__).resolve().parent
BASE=HERE.parent/'residual-gate-calibration-20261021'
CONFIGS=(('off',0,'grundy'),('sg6',6,'grundy'),('sg12',12,'grundy'),('pn6',6,'outcome'),('pn12',12,'outcome'))
QUOTA=100000

def parse(raw,corpus,config,repeat):
    name,gate,method=config
    expected=json.loads((BASE/'fixtures.json').read_text()) if corpus=='saved' else None
    size=52 if expected else 3
    lines=raw.splitlines()
    assert sum(s.startswith(f'# replay_done rows={size} ') for s in lines)==1
    assert not any(s.startswith('replay_error,') for s in lines)
    def fields(prefix):
        rows=[dict(x.split('=') for x in s.split()[2:]) for s in lines if s.startswith(prefix)]
        assert len({int(r['row']) for r in rows})==len(rows)
        return {int(r['row']):r for r in rows}
    timing=fields('# replay_timing ');pn=fields('# residual_outcome ');shadow=fields('# residual_shadow ')
    rows=list(csv.reader(s for s in lines if s.startswith('replay,')))
    assert len(rows)==len(timing)==size and len(pn)==(size if method=='outcome' else 0)
    records=[]
    for i,row in enumerate(rows):
        t=timing[i];p=pn.get(i,{})
        assert int(row[1])==i and int(row[5])==5000 and 0<=int(row[7])<=5000
        assert int(row[6])==(expected[i]['result'] if expected else 0)
        assert int(t['residual_gate'])==gate
        assert int(t['total_us'])+2>=int(t['solve_us'])+int(t['setup_us'])
        if expected:assert int(row[2])==len(expected[i]['occupied']) and int(row[3])==len(expected[i]['legal'])
        if p:
            assert 0<=int(p['nodes'])<=QUOTA and 0<=int(p['remaining'])<=QUOTA
            assert 0<=int(p['cutoffs'])<=int(p['nodes'])
            assert int(p['nodes'])+int(p['remaining'])==QUOTA
            assert 0<=int(p['aborts'])<=1
            if int(p['aborts']):assert int(p['remaining'])==0
        records.append(dict(corpus=corpus,config=name,repeat=repeat,id=i,split=expected[i]['split'] if expected else 'stress',
            result=int(row[6]),nodes=int(row[7]),solve_us=int(t['solve_us']),setup_us=int(t['setup_us']),
            total_us=int(t['total_us']),pn_nodes=int(p.get('nodes',0)),pn_aborts=int(p.get('aborts',0)),
            pn_cutoffs=int(p.get('cutoffs',0)),residual_calls=int(shadow.get(i,{}).get('exact_calls',0))))
    return records

def aggregate(records):
    totals={}
    for split in ('train','holdout','saved','stress'):
        totals[split]={}
        for name,_,_ in CONFIGS:
            rows=[r for r in records if r['config']==name and (r['split']==split if split in ('train','holdout') else r['corpus']==split)]
            med=[]
            for i in sorted({r['id'] for r in rows}):
                roots=[r for r in rows if r['id']==i];assert len(roots)==3
                assert len({(r['result'],r['nodes'],r['pn_nodes'],r['pn_aborts'],r['residual_calls']) for r in roots})==1
                med.append({k:statistics.median(r[k] for r in roots) for k in ('nodes','solve_us','setup_us','pn_nodes','pn_aborts','residual_calls')})
            totals[split][name]={k:sum(r[k] for r in med) for k in med[0]}
    return totals

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);p.add_argument('--prepare-only',action='store_true');args=p.parse_args()
    protocol=dict(configs=CONFIGS,repeats=3,budget=5000,outcome_quota=QUOTA,
        inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (BASE/'input.csv',BASE/'stress-input.csv',BASE/'fixtures.json')},
        solver_sha256=hashlib.sha256(pathlib.Path(args.solver).read_bytes()).hexdigest(),
        source_commit=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),
        order='rotate configurations by repeat; saved then stress for each configuration; fresh solver per row; no shared caches',
        default_policy='handoff remains OFF; evaluator remains Grundy; no threshold selection from holdout',
        new_verdict_policy='stop if deep roots newly decided; independently validate before adopting')
    (HERE/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    if args.prepare_only:return
    records=[]
    for repeat in range(3):
        order=CONFIGS[repeat:]+CONFIGS[:repeat]
        for config in order:
            name,gate,method=config
            for corpus in ('saved','stress'):
                source=BASE/('input.csv' if corpus=='saved' else 'stress-input.csv')
                output=HERE/'raw'/f'{name}-{corpus}-r{repeat}.csv';output.unlink(missing_ok=True)
                subprocess.run([args.solver,'--n=11','--memo=18',f'--exact-replay={source}','--exact-replay-budget=5000',
                    f'--residual-exact-legal={gate}',f'--residual-evaluator={method}',
                    f'--residual-outcome-budget={QUOTA}',f'--csv={output}'],check=True,timeout=150)
                records.extend(parse(output.read_text(),corpus,config,repeat))
                print(f'{name} {corpus} repeat={repeat} validated',flush=True)
    (HERE/'records.json').write_text(json.dumps(records,indent=2)+'\n')
    summary=dict(protocol=protocol,totals=aggregate(records))
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
