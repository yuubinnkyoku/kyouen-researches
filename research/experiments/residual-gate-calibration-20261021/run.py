#!/usr/bin/env python3
"""Cold-root handoff-gate comparison on a frozen, independently solved corpus."""
import argparse
import csv
import functools
import hashlib
import io
import json
import pathlib
import statistics
import subprocess
import tempfile
import time

HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json'
GATES=(0,6,8,10,12)

def oracle(s):
    labels={v:i for i,v in enumerate(s['legal'])}
    edges=[sum(1<<labels[v] for v in e) for e in s['minimal_residual_edges']]
    @functools.lru_cache(None)
    def g(mask):
        values=set()
        for v in range(len(labels)):
            if mask>>v&1: continue
            child=mask|1<<v
            if not any(child&e==e for e in edges): values.add(g(child))
        value=0
        while value in values: value+=1
        return value
    return g(0),g.cache_info().currsize

def fixtures():
    snapshots=json.loads(SOURCE.read_text())['snapshots']
    chosen=[];used=set();training={}
    for split in ('train','holdout'):
        for n in range(6,19):
            for parity in (0,1):
                pool=[(i,s) for i,s in enumerate(snapshots)
                      if len(s['legal'])==n and len(s['occupied'])%2==parity]
                if split=='holdout': pool.reverse()
                for i,s in pool:
                    key=tuple(s['occupied'])
                    if key in used: continue
                    if split=='holdout' and s['trial']==training[n,parity]: continue
                    used.add(key)
                    if split=='train':training[n,parity]=s['trial']
                    grundy,states=oracle(s)
                    stones=len(s['occupied'])
                    chosen.append(dict(id=len(chosen),split=split,source_index=i,trial=s['trial'],
                        occupied=s['occupied'],legal=s['legal'],grundy=grundy,oracle_states=states,
                        result=1 if (grundy!=0)==(stones%2==0) else 2))
                    break
                else:raise AssertionError((split,n,parity))
    assert len(chosen)==52
    return chosen

def parse(raw,expected,gate,repeat,budget):
    lines=raw.splitlines();timing={};counters={}
    assert any(x.startswith('# replay_done rows=52 ') for x in lines)
    assert not any(x.startswith('replay_error,') for x in lines)
    for line in lines:
        if line.startswith('# replay_timing '):
            d=dict(x.split('=') for x in line.split()[2:]);timing[int(d['row'])]=d
        if line.startswith('# residual_shadow '):
            d=dict(x.split('=') for x in line.split()[2:]);counters[int(d['row'])]=d
    rows=list(csv.reader(x for x in lines if x.startswith('replay,')))
    assert len(rows)==len(expected)==len(timing)==52
    records=[]
    for row,e in zip(rows,expected):
        idx=int(row[1]);result=int(row[6]);t=timing[idx];c=counters.get(idx,{})
        assert idx==e['id'] and int(row[2])==len(e['occupied']) and int(row[3])==len(e['legal'])
        assert int(row[5])==budget and int(t['residual_gate'])==gate
        assert result==0 or result==e['result'],(gate,idx,result,e['result'])
        assert int(t['total_us'])+2>=int(t['setup_us'])+int(t['solve_us'])
        records.append(dict(id=idx,split=e['split'],legal=len(e['legal']),gate=gate,repeat=repeat,
            expected=e['result'],result=result,nodes=int(row[7]),setup_us=int(t['setup_us']),
            solve_us=int(t['solve_us']),total_us=int(t['total_us']),
            residual_calls=int(c.get('exact_calls',0)),residual_memo=int(c.get('residual_memo_states',0))))
    return records

def summarize(records,repeats,budget):
    by_root=[]
    for gate in GATES:
        for idx in range(52):
            rows=[x for x in records if x['gate']==gate and x['id']==idx]
            assert len(rows)==repeats
            assert len({(x['result'],x['nodes'],x['residual_calls'],x['residual_memo']) for x in rows})==1
            med={k:statistics.median(x[k] for x in rows) for k in ('setup_us','solve_us','total_us')}
            by_root.append({**rows[0],**med})
    totals={}
    for split in ('train','holdout','all'):
        totals[split]={}
        for gate in GATES:
            rows=[x for x in by_root if x['gate']==gate and (split=='all' or x['split']==split)]
            totals[split][str(gate)]={'roots':len(rows),'unknown':sum(x['result']==0 for x in rows),
                **{k:sum(x[k] for x in rows) for k in ('nodes','setup_us','solve_us','total_us','residual_calls','residual_memo')}}
    winner=min(GATES,key=lambda g:(totals['train'][str(g)]['unknown'],totals['train'][str(g)]['solve_us']))
    return dict(source=str(SOURCE.relative_to(ROOT)),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                gates=list(GATES),budget_per_root=budget,repeats=repeats,
                protocol='fresh solver/memo per row; no shared caches; rotated gate order; sum of root timing medians',
                selection_rule='minimum UNKNOWN count, then solve_us on training only',training_winner=winner,
                totals=totals,n11_empty_root_outcome='UNKNOWN')

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver');p.add_argument('--repeats',type=int,default=3)
    p.add_argument('--budget',type=int,default=5000)
    p.add_argument('--prepare-only',action='store_true');args=p.parse_args()
    assert 1<=args.repeats<=7 and 1<=args.budget<=20000
    selected=fixtures()
    (HERE/'fixtures.json').write_text(json.dumps(selected,indent=2)+'\n')
    input_rows=[]
    for e in selected:
        lo=sum(1<<v for v in e['occupied'] if v<64);hi=sum(1<<(v-64) for v in e['occupied'] if v>=64)
        input_rows.append(f"saved,{e['id']},{len(e['occupied'])},{lo},{hi},{len(e['legal'])},0,0,0,0,0")
    input_path=HERE/'input.csv';input_path.write_text('\n'.join(input_rows)+'\n')
    protocol=dict(source=str(SOURCE.relative_to(ROOT)),
                  source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  fixtures_sha256=hashlib.sha256((HERE/'fixtures.json').read_bytes()).hexdigest(),
                  input_sha256=hashlib.sha256(input_path.read_bytes()).hexdigest(),
                  gates=list(GATES),repeats=args.repeats,budget_per_root=args.budget,
                  selection='first saved state in each legal=6..18 / turn parity stratum for train; last distinct trial for holdout',
                  selection_rule='minimum UNKNOWN count, then solve_us on training only')
    (HERE/'protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    if args.prepare_only:
        print('Prepared 26 training and 26 holdout roots with independent subset-mex verdicts.')
        return
    (HERE/'raw').mkdir(exist_ok=True)
    records=[]
    with tempfile.TemporaryDirectory() as tmp:
        exe=args.solver or str(pathlib.Path(tmp)/'solver')
        if not args.solver:
            subprocess.run(['g++','-std=c++20','-O2','-I'+str(ROOT/'cpp/solvers'),
                            str(ROOT/'cpp/solvers/kyouen_dfpn_root.cpp'),'-o',exe],check=True)
        for repeat in range(args.repeats):
            shift=2*repeat%len(GATES);order=GATES[shift:]+GATES[:shift]
            for gate in order:
                path=HERE/'raw'/f'gate-{gate}-repeat-{repeat}.csv'
                cmd=[exe,'--n=11','--memo=18',f'--exact-replay={input_path}',f'--exact-replay-budget={args.budget}',
                     f'--residual-exact-legal={gate}',f'--csv={path}']
                start=time.monotonic();subprocess.run(cmd,check=True,timeout=120)
                records.extend(parse(path.read_text(),selected,gate,repeat,args.budget))
                print(f'repeat={repeat} gate={gate} roots=52 elapsed={time.monotonic()-start:.2f}s',flush=True)
    with (HERE/'measurements.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(records[0]));writer.writeheader();writer.writerows(records)
    summary=summarize(records,args.repeats,args.budget)
    (HERE/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
