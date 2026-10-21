#!/usr/bin/env python3
"""Bounded replays of frozen roots; profiling is separate from timing comparisons."""
import argparse,csv,hashlib,json,pathlib,statistics,subprocess
HERE=pathlib.Path(__file__).resolve().parent
BASE=HERE.parent/'residual-gate-calibration-20261021'

def parse(raw,corpus,gate,profile):
    lines=raw.splitlines(); size=52 if corpus=='saved' else 3
    assert any(x.startswith(f'# replay_done rows={size} ') for x in lines)
    assert not any(x.startswith('replay_error,') for x in lines)
    rows=list(csv.reader(x for x in lines if x.startswith('replay,')))
    def fields(prefix):
        data=[dict(x.split('=') for x in s.split()[2:]) for s in lines if s.startswith(prefix)]
        assert len({int(d['row']) for d in data})==len(data)
        return {int(d['row']):d for d in data}
    timing=fields('# replay_timing '); phases=fields('# residual_profile ')
    expected=json.loads((BASE/'fixtures.json').read_text()) if corpus=='saved' else None
    assert len(rows)==len(timing)==size
    assert len(phases)==(size if profile and gate else 0)
    out=[]
    for i,r in enumerate(rows):
        t=timing[i]; p=phases.get(i,{})
        assert int(r[1])==i and int(r[5])==5000 and 0<=int(r[7])<=5000
        assert int(t['residual_gate'])==gate
        assert int(r[6])==(expected[i]['result'] if expected else 0)
        if expected:
            assert int(r[2])==len(expected[i]['occupied']) and int(r[3])==len(expected[i]['legal'])
        d=dict(id=i,split=expected[i]['split'] if expected else 'stress',result=int(r[6]),nodes=int(r[7]))
        d.update({k:int(t[k]) for k in ('setup_us','solve_us','total_us')})
        d.update({k:int(p.get(k,0)) for k in ('build_ns','structure_ns','grundy_ns')})
        assert sum(d[k] for k in ('build_ns','structure_ns','grundy_ns'))<=d['solve_us']*1000+1000
        out.append(d)
    return out

def aggregate(records,gates,repeats):
    totals={}
    for corpus in ('saved','stress'):
        totals[corpus]={}
        for gate in gates:
            selected=[r for r in records if r['corpus']==corpus and r['gate']==gate]
            med=[]
            for i in sorted({r['id'] for r in selected}):
                roots=[r for r in selected if r['id']==i]
                assert len(roots)==repeats and len({(r['result'],r['nodes']) for r in roots})==1
                med.append({k:statistics.median(r[k] for r in roots) for k in ('nodes','solve_us','setup_us','build_ns','structure_ns','grundy_ns')})
            totals[corpus][str(gate)]={k:sum(r[k] for r in med) for k in med[0]}
    return totals

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--solver',required=True);ap.add_argument('--label',required=True)
    ap.add_argument('--profile',action='store_true');ap.add_argument('--builder',choices=('scan','indexed','auto'))
    ap.add_argument('--repeats',type=int,default=1);args=ap.parse_args()
    assert 1<=args.repeats<=3 and args.label.replace('-','').isalnum()
    gates=(6,12) if args.profile else (0,6,12)
    records=[]
    for rep in range(args.repeats):
        order=gates[rep%len(gates):]+gates[:rep%len(gates)]
        for corpus in ('saved','stress'):
            source=BASE/('input.csv' if corpus=='saved' else 'stress-input.csv')
            for gate in order:
                path=HERE/'raw'/f'{args.label}-{corpus}-g{gate}-r{rep}.csv'
                cmd=[args.solver,'--n=11','--memo=18',f'--exact-replay={source}',
                    '--exact-replay-budget=5000',f'--residual-exact-legal={gate}',f'--csv={path}']
                if args.profile:cmd.append('--residual-profile')
                if args.builder:cmd.append(f'--residual-builder={args.builder}')
                subprocess.run(cmd,check=True,timeout=150)
                for r in parse(path.read_text(),corpus,gate,args.profile):
                    records.append(dict(corpus=corpus,gate=gate,repeat=rep,**r))
                print(f'{args.label} {corpus} gate={gate} repeat={rep} validated',flush=True)
    totals=aggregate(records,gates,args.repeats)
    summary=dict(label=args.label,profile=args.profile,builder=args.builder,repeats=args.repeats,gates=gates,
        budget=5000,inputs={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in (BASE/'input.csv',BASE/'stress-input.csv',BASE/'fixtures.json')},totals=totals)
    (HERE/f'{args.label}-records.json').write_text(json.dumps(records,indent=2)+'\n')
    (HERE/f'{args.label}-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
