#!/usr/bin/env python3
"""Independently check every kernel result, then validate archived replays."""
import csv,hashlib,json,pathlib
import oracle
import run
HERE=pathlib.Path(__file__).resolve().parent

def main():
    source=json.loads(oracle.SOURCE.read_text())['snapshots']
    expected=json.loads((HERE/'oracle.json').read_text())
    assert expected['sha256']==hashlib.sha256(oracle.SOURCE.read_bytes()).hexdigest()
    assert len(source)==len(expected['rows'])==826
    for i,s in enumerate(source):assert expected['rows'][i]==dict(id=i,**oracle.evaluate(s))
    assert expected['total_states']==sum(r['states'] for r in expected['rows'])
    kernel=list(csv.DictReader((HERE/'kernel.csv').open()));assert len(kernel)==826
    summary=json.loads((HERE/'kernel-summary.json').read_text())
    assert summary['sha256']==expected['sha256'] and summary['repeats']==7 and summary['quota']==run.QUOTA
    for i,(r,e,s) in enumerate(zip(kernel,expected['rows'],source)):
        assert int(r['id'])==i and int(r['n'])==len(s['legal']) and int(r['edges'])==len(s['minimal_residual_edges'])
        assert int(r['g'])==e['g'] and int(r['pn'])==(e['g']!=0)
        assert 1<=int(r['pn_calls'])<=run.QUOTA
    assert summary['totals']=={k:sum(float(r[k]) for r in kernel) for k in summary['totals']}
    assert summary['roots_faster']==sum(float(r['pn_us'])<float(r['sg_us']) for r in kernel)
    records=[]
    if (HERE/'summary.json').exists():
        p=json.loads((HERE/'protocol.json').read_text());stored=json.loads((HERE/'summary.json').read_text())
        assert p==stored['protocol'] and p['repeats']==3 and p['budget']==5000 and p['outcome_quota']==run.QUOTA
        assert p['configs']==[list(c) for c in run.CONFIGS]
        for name,digest in p['inputs'].items():assert hashlib.sha256((run.BASE/name).read_bytes()).hexdigest()==digest
        for repeat in range(3):
            for config in run.CONFIGS:
                for corpus in ('saved','stress'):
                    path=HERE/'raw'/f'{config[0]}-{corpus}-r{repeat}.csv'
                    records.extend(run.parse(path.read_text(),corpus,config,repeat))
        key=lambda r:(r['repeat'],r['config'],r['corpus'],r['id'])
        assert sorted(records,key=key)==sorted(json.loads((HERE/'records.json').read_text()),key=key)
        assert run.aggregate(records)==stored['totals']
    print(f'VERIFIED 826 independent oracle outcomes ({expected["total_states"]} states), archived replay rows={len(records)}')
if __name__=='__main__':main()
