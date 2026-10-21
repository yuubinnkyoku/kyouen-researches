#!/usr/bin/env python3
"""Supplemental bounded replay of the three pre-existing deep CI roots."""
import argparse,csv,hashlib,json,pathlib,subprocess,sys,time
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
SOURCE=ROOT/'research/experiments/residual-closed-forms-20261021/replay-input.csv'
GATES=(0,6,8,10,12)

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);p.add_argument('--prepare-only',action='store_true');args=p.parse_args()
    sys.path.insert(0,str(ROOT/'research/experiments/n11-search-methods/scripts'))
    from dfpn_edge_classes import legal_after
    rows=[]
    for row in csv.reader(SOURCE.read_text().splitlines()):
        occ=[v for v in range(121) if (int(row[3])|(int(row[4])<<64))>>v&1]
        row[5]=str(len(legal_after(set(occ))));rows.append(row)
    assert len(rows)==3
    source=HERE/'stress-input.csv'
    with source.open('w') as f:csv.writer(f,lineterminator='\n').writerows(rows)
    protocol=dict(source=str(SOURCE.relative_to(ROOT)),source_sha256=hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
                  gates=list(GATES),budget_per_root=5000,repeats=1,
                  purpose='bounded UNKNOWN regression; supplemental only, not used for training selection',
                  newly_decided_policy='record and independently validate before adopting any new verdict')
    (HERE/'stress-protocol.json').write_text(json.dumps(protocol,indent=2)+'\n')
    if args.prepare_only:return
    summary={};known={}
    for gate in GATES:
        output=HERE/'raw'/f'stress-gate-{gate}.csv'
        start=time.monotonic()
        subprocess.run([args.solver,'--n=11','--memo=18',f'--exact-replay={source}',
                        '--exact-replay-budget=5000',f'--residual-exact-legal={gate}',f'--csv={output}'],check=True,timeout=120)
        lines=output.read_text().splitlines()
        assert any(x.startswith('# replay_done rows=3 ') for x in lines)
        assert not any(x.startswith('replay_error,') for x in lines)
        actual=list(csv.reader(x for x in lines if x.startswith('replay,')))
        assert len(actual)==3
        timing=[dict(x.split('=') for x in line.split()[2:]) for line in lines if line.startswith('# replay_timing ')]
        assert len(timing)==3
        for i,row in enumerate(actual):
            assert int(row[1])==i and int(row[5])==5000 and 0<=int(row[7])<=5000
            result=int(row[6]);assert result in (0,1,2)
            if result:
                assert i not in known or known[i]==result
                known[i]=result
        summary[str(gate)]=dict(results=[int(r[6]) for r in actual],unknown=sum(int(r[6])==0 for r in actual),
            nodes=sum(int(r[7]) for r in actual),solve_us=sum(int(t['solve_us']) for t in timing),
            total_us=sum(int(t['total_us']) for t in timing))
        print(f'stress gate={gate} rows=3 elapsed={time.monotonic()-start:.2f}s',flush=True)
    (HERE/'stress-summary.json').write_text(json.dumps({'gates':summary,'newly_decided_rows':known,'repeats':1},indent=2)+'\n')
if __name__=='__main__':main()
