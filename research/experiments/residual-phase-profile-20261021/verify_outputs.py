#!/usr/bin/env python3
"""Reaggregate complete archives without rerunning any timed search."""
import hashlib,json,pathlib
import run
HERE=pathlib.Path(__file__).resolve().parent

def main():
    count=0
    for p in sorted(HERE.glob('*-summary.json')):
        s=json.loads(p.read_text());label=s['label'];records=[]
        assert p.name==label+'-summary.json'
        assert s['budget']==5000 and 1<=s['repeats']<=3
        for name,digest in s['inputs'].items():
            assert hashlib.sha256((run.BASE/name).read_bytes()).hexdigest()==digest
        for repeat in range(s['repeats']):
            for corpus in ('saved','stress'):
                for gate in s['gates']:
                    raw=HERE/'raw'/f'{label}-{corpus}-g{gate}-r{repeat}.csv'
                    for r in run.parse(raw.read_text(),corpus,gate,s['profile']):
                        records.append(dict(corpus=corpus,gate=gate,repeat=repeat,**r))
        stored=json.loads((HERE/f'{label}-records.json').read_text())
        key=lambda r:(r['repeat'],r['corpus'],r['gate'],r['id'])
        assert sorted(records,key=key)==sorted(stored,key=key)
        assert run.aggregate(records,s['gates'],s['repeats'])==s['totals']
        count+=len(records)
    print(f'VERIFIED phase/timing archived rows={count}')
if __name__=='__main__':main()
