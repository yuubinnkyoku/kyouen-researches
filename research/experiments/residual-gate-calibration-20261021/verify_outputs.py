#!/usr/bin/env python3
"""Verify the archived inputs and summaries without rerunning timed searches."""
import csv,hashlib,json,pathlib
import run
HERE=pathlib.Path(__file__).resolve().parent

def main():
    protocol=json.loads((HERE/'protocol.json').read_text())
    for key,path in [('source_sha256',run.SOURCE),('fixtures_sha256',HERE/'fixtures.json'),('input_sha256',HERE/'input.csv')]:
        assert hashlib.sha256(path.read_bytes()).hexdigest()==protocol[key],key
    fixtures=json.loads((HERE/'fixtures.json').read_text())
    snapshots=json.loads(run.SOURCE.read_text())['snapshots']
    # Re-run the independent subset oracle, not the optimized C++ evaluator.
    for e in fixtures:
        original=snapshots[e['source_index']]
        assert original['occupied']==e['occupied'] and original['legal']==e['legal']
        assert original['trial']==e['trial']
        g,states=run.oracle(original)
        assert (g,states)==(e['grundy'],e['oracle_states'])
        assert e['result']==(1 if (g!=0)==(len(e['occupied'])%2==0) else 2)
    records=[]
    for repeat in range(protocol['repeats']):
        shift=2*repeat%len(run.GATES)
        for gate in run.GATES[shift:]+run.GATES[:shift]:
            raw=(HERE/'raw'/f'gate-{gate}-repeat-{repeat}.csv').read_text()
            records.extend(run.parse(raw,fixtures,gate,repeat,protocol['budget_per_root']))
    with (HERE/'measurements.csv').open() as f:
        archived=[{k:v if k=='split' else int(v) for k,v in row.items()} for row in csv.DictReader(f)]
    assert archived==records
    expected=run.summarize(records,protocol['repeats'],protocol['budget_per_root'])
    assert json.loads((HERE/'summary.json').read_text())==expected
    stress=json.loads((HERE/'stress-summary.json').read_text())
    for gate in run.GATES:
        lines=(HERE/'raw'/f'stress-gate-{gate}.csv').read_text().splitlines()
        assert any(x.startswith('# replay_done rows=3 ') for x in lines)
        assert not any(x.startswith('replay_error,') for x in lines)
        rows=list(csv.reader(x for x in lines if x.startswith('replay,')))
        times=[dict(term.split('=') for term in x.split()[2:]) for x in lines if x.startswith('# replay_timing ')]
        assert len(rows)==len(times)==3
        assert all(int(r[5])==5000 and 0<=int(r[7])<=5000 for r in rows)
        actual=dict(results=[int(r[6]) for r in rows],unknown=sum(int(r[6])==0 for r in rows),
                    nodes=sum(int(r[7]) for r in rows),solve_us=sum(int(t['solve_us']) for t in times),
                    total_us=sum(int(t['total_us']) for t in times))
        assert actual==stress['gates'][str(gate)]
    print('PASS: frozen hashes, 52 independent oracles, 780 measurements, training selection, and 15 stress replays')

if __name__=='__main__':main()
