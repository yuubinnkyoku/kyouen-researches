#!/usr/bin/env python3
"""Bounded, independently solved saved n11 positions through df-pn replay."""
import argparse, csv, functools, json, pathlib, subprocess, tempfile
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'research/experiments/n11-reduction-followup-20261005/output/n11-snapshots.json'

def oracle(s):
    labels={v:i for i,v in enumerate(s['legal'])}
    edges=[sum(1<<labels[v] for v in e) for e in s['minimal_residual_edges']]
    n=len(labels)
    @functools.lru_cache(None)
    def g(occupied):
        values=set()
        for i in range(n):
            if occupied>>i&1:continue
            child=occupied|1<<i
            if not any(child&e==e for e in edges):values.add(g(child))
        value=0
        while value in values:value+=1
        return value
    return g(0)

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);p.add_argument('--baseline',required=True)
    args=p.parse_args()
    selected=[];seen=set()
    for s in json.loads(SOURCE.read_text())['snapshots']:
        key=(len(s['legal']),len(s['occupied'])%2)
        if 3<=len(s['legal'])<=10 and key not in seen:
            seen.add(key);selected.append(s)
    rows=[];expected=[]
    for i,s in enumerate(selected):
        lo=sum(1<<v for v in s['occupied'] if v<64)
        hi=sum(1<<(v-64) for v in s['occupied'] if v>=64)
        n=len(s['occupied']);g=oracle(s)
        result=1 if (g!=0)==(n%2==0) else 2
        rows.append(f'saved,{i},{n},{lo},{hi},{len(s["legal"])},0,0,0,0,0')
        expected.append(dict(id=i,stones=n,legal=len(s['legal']),grundy=g,result=result))
    assert len(rows)==16
    source=HERE/'late-input.csv';source.write_text('\n'.join(rows)+'\n')
    (HERE/'late-expected.json').write_text(json.dumps(expected,indent=2)+'\n')
    summary={}
    modes=[('baseline',args.baseline,['--residual-exact-legal=10']),
           ('fast',args.solver,['--residual-exact-legal=10']),
           ('shared',args.solver,['--residual-exact-legal=10','--residual-share-gate=6']),
           ('shadow',args.solver,['--residual-audit-legal=10','--residual-crosscheck-legal=10'])]
    for name,exe,flags in modes:
        out=HERE/f'late-{name}.csv'
        subprocess.run([exe,'--n=11','--memo=18',f'--exact-replay={source}',
                        '--exact-replay-budget=20000',f'--csv={out}',*flags],check=True,timeout=120)
        lines=out.read_text().splitlines()
        assert not any(x.startswith('replay_error,') for x in lines),name
        actual=list(csv.reader(x for x in lines if x.startswith('replay,')))
        assert len(actual)==len(expected),name
        for row,e in zip(actual,expected):assert (int(row[1]),int(row[6]))==(e['id'],e['result']),(name,row,e)
        counters={}
        for line in lines:
            if line.startswith('# residual_shadow row='):
                for field in line.split()[3:]:
                    k,v=field.split('=');counters[k]=counters.get(k,0)+int(v)
        summary[name]={'rows':len(actual),'nodes':sum(int(r[7]) for r in actual),'counters':counters}
    assert summary['fast']['counters']['closed_two_edges']>0
    assert summary['shadow']['counters']['audit_calls']>0
    with tempfile.TemporaryDirectory() as tmp:
        guard=subprocess.run([args.solver,'--n=11','--memo=18',f'--exact-replay={source}',
                              '--residual-exact-legal=10',f'--proof-dag={tmp}/proof.cert'],capture_output=True,text=True,timeout=120)
        assert guard.returncode!=0 and 'proof capture forbids residual shortcuts' in guard.stderr
    summary['proof_capture_guard']='rejected residual shortcuts'
    (HERE/'integration-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
