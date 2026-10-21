#!/usr/bin/env python3
"""Validate frozen fixtures, pure training selection, and recorded replays."""
import argparse,json,pathlib
import calibrate as c
import prepare as p
HERE=pathlib.Path(__file__).resolve().parent

def verify_fixtures(full_geometry):
    protocol=json.loads((HERE/'protocol.json').read_text());fixtures=json.loads((HERE/'fixtures.json').read_text())
    for name,value in protocol['hashes'].items():assert c.digest(HERE/name)==value
    assert protocol['quotas']==[128,512,2048] and protocol['gates']==[6,12] and protocol['repeats']==3 and protocol['board_budget']==5000
    assert c.digest(p.SOURCE)==protocol['source_sha256']
    assert c.digest(p.OLD/'fixtures.json')==protocol['old_fixtures_sha256']
    assert c.digest(p.OLD/'stress-input.csv')==protocol['stress_sha256']
    old=json.loads(p.SOURCE.read_text())['snapshots']
    pool=json.loads((HERE/'candidate-pool.json').read_text())
    chosen=p.choose(pool,old)
    assert len(fixtures['train'])==len(fixtures['new'])==len(chosen)==26
    assert fixtures['train']==[e for e in json.loads((p.OLD/'fixtures.json').read_text()) if e['split']=='train']
    for i,(f,s) in enumerate(zip(fixtures['new'],chosen)):
        assert f['id']==i and f['split']=='new'
        assert all(f[k]==v for k,v in s.items())
        independent=p.evaluate(s)
        assert independent['g']==f['grundy'] and independent['states']==f['oracle_states']
        assert f['result']==(1 if (f['grundy']!=0)==(len(f['occupied'])%2==0) else 2)
        if full_geometry:
            checked=p.geometry(s['occupied'])
            assert checked['legal']==s['legal']
            assert {frozenset(e) for e in checked['minimal_residual_edges']}=={frozenset(e) for e in s['minimal_residual_edges']}
    for split in ('train','new'):assert (HERE/f'{split}-input.csv').read_text()==p.rows(fixtures[split])
    return protocol,fixtures

def collect(fixtures,configs,splits):
    result=[]
    for repeat in range(3):
        for config in configs:
            for split in splits:
                expected=[{}]*3 if split=='stress' else fixtures[split]
                result.extend(c.parse((HERE/'raw'/f'{split}-{config["name"]}-r{repeat}.csv').read_text(),expected,split,config,repeat))
    return result

def same(a,b):
    key=lambda r:(r['split'],r['config'],r['repeat'],r['id'])
    assert sorted(a,key=key)==sorted(b,key=key)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--geometry',action='store_true');args=parser.parse_args()
    protocol,fixtures=verify_fixtures(args.geometry)
    count=0
    if (HERE/'selection.json').exists():
        train=collect(fixtures,c.CONFIGS,('train',));assert len(train)==546
        same(train,json.loads((HERE/'training-records.json').read_text()))
        selected=json.loads((HERE/'selection.json').read_text());actual=c.select(train)
        assert all(selected[k]==v for k,v in actual.items())
        assert selected['protocol_sha256']==c.digest(HERE/'protocol.json')
        assert selected['training_sha256']==c.digest(HERE/'training-records.json')
        count+=len(train)
    if (HERE/'summary.json').exists():
        configs=[c.CONFIGS[0],selected['candidate']]
        confirmed=collect(fixtures,configs,('new','stress'));assert len(confirmed)==174
        same(confirmed,json.loads((HERE/'confirmation-records.json').read_text()))
        summary=json.loads((HERE/'summary.json').read_text())
        totals={split:c.aggregate(confirmed,configs,split) for split in ('new','stress')}
        assert summary['totals']==totals and summary['candidate']==selected['candidate']
        assert summary['selection_sha256']==c.digest(HERE/'selection.json')
        assert len(summary['selection_commit'])==40
        assert summary['passed']==c.adoption(totals,selected['candidate'])
        count+=len(confirmed)
    print(f'VERIFIED frozen train=26 new=26, D4 disjointness, independent oracles, training-only selection, archived rows={count}, geometry={args.geometry}')
if __name__=='__main__':main()
