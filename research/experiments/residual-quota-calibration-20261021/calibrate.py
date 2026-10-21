#!/usr/bin/env python3
"""Train on old roots; commit selection before timing any new root."""
import argparse,csv,hashlib,json,pathlib,statistics,subprocess
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]
OLD=HERE.parent/'residual-gate-calibration-20261021'
CONFIGS=[dict(name='off',gate=0,quota=0)]+[dict(name=f'q{q}-g{g}',gate=g,quota=q) for g in (6,12) for q in (128,512,2048)]
REPEATS=3

def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def dump(path,data):path.write_text(json.dumps(data,indent=2)+'\n')

def parse(raw,expected,split,config,repeat):
    lines=raw.splitlines();n=len(expected)
    assert sum(s.startswith(f'# replay_done rows={n} ') for s in lines)==1
    assert not any(s.startswith('replay_error,') for s in lines)
    def fields(prefix):
        rows=[dict(x.split('=') for x in s.split()[2:]) for s in lines if s.startswith(prefix)]
        assert len({int(r['row']) for r in rows})==len(rows)
        return {int(r['row']):r for r in rows}
    timing=fields('# replay_timing ');pn=fields('# residual_outcome ')
    rows=list(csv.reader(s for s in lines if s.startswith('replay,')))
    assert len(rows)==len(timing)==n and len(pn)==(n if config['gate'] else 0)
    records=[]
    for i,(row,e) in enumerate(zip(rows,expected)):
        assert int(row[1])==i and int(row[5])==5000 and 0<=int(row[7])<=5000
        result=int(row[6]);assert result in (0,1,2)
        if split=='stress':assert result==0,'new deep verdict needs independent validation'
        else:
            assert result==0 or result==e['result']
            assert int(row[2])==len(e['occupied']) and int(row[3])==len(e['legal'])
            assert int(row[9])==sum(1<<v for v in e['occupied'] if v<64)
            assert int(row[10])==sum(1<<(v-64) for v in e['occupied'] if v>=64)
        t=timing[i];assert int(t['residual_gate'])==config['gate']
        assert int(t['total_us'])+2>=int(t['setup_us'])+int(t['solve_us'])
        p=pn.get(i,{})
        if p:
            used,left,aborts,cutoffs=[int(p[k]) for k in ('nodes','remaining','aborts','cutoffs')]
            assert 0<=used<=config['quota'] and 0<=left<=config['quota'] and used+left==config['quota']
            assert 0<=cutoffs<=used and 0<=aborts<=1
            if aborts:assert left==0
        records.append(dict(split=split,config=config['name'],repeat=repeat,id=i,result=result,
            nodes=int(row[7]),solve_us=int(t['solve_us']),setup_us=int(t['setup_us']),total_us=int(t['total_us']),
            pn_nodes=int(p.get('nodes',0)),pn_aborts=int(p.get('aborts',0))))
    return records

def aggregate(records,configs,split):
    totals={}
    for config in configs:
        rows=[r for r in records if r['split']==split and r['config']==config['name']]
        ids=sorted({r['id'] for r in rows});assert ids==list(range(3 if split=='stress' else 26))
        med=[]
        for i in ids:
            roots=[r for r in rows if r['id']==i];assert len(roots)==REPEATS
            assert {r['repeat'] for r in roots}==set(range(REPEATS))
            assert len({(r['result'],r['nodes'],r['pn_nodes'],r['pn_aborts']) for r in roots})==1
            med.append(dict(unknown=int(roots[0]['result']==0),**{k:statistics.median(r[k] for r in roots) for k in ('nodes','solve_us','setup_us','pn_nodes','pn_aborts')}))
        totals[config['name']]={k:sum(r[k] for r in med) for k in med[0]}
    return totals

def select(records):
    assert records and all(r['split']=='train' for r in records),'selection accepts training rows only'
    assert len(records)==26*REPEATS*len(CONFIGS)
    assert {r['config'] for r in records}=={c['name'] for c in CONFIGS}
    totals=aggregate(records,CONFIGS,'train')
    candidate=min(CONFIGS[1:],key=lambda c:(totals[c['name']]['unknown'],totals[c['name']]['solve_us'],c['quota'],c['gate']))
    return dict(candidate=candidate,training_totals=totals,rule='UNKNOWN count, solve_us sum of root medians, quota, gate; PN candidates only')

def adoption(totals,config):
    name=config['name'];off='off'
    return all(totals[s][name]['unknown']<=totals[s][off]['unknown'] for s in ('new','stress')) and \
        totals['new'][name]['solve_us']<totals['new'][off]['solve_us'] and \
        totals['stress'][name]['solve_us']<=totals['stress'][off]['solve_us']

def assert_committed(path):
    rel=str(path.relative_to(ROOT))
    assert subprocess.check_output(['git','show',f'HEAD:{rel}'],cwd=ROOT)==path.read_bytes(),f'commit frozen file first: {rel}'

def run_phase(solver,phase,fixtures,configs):
    records=[]
    for repeat in range(REPEATS):
        shift=repeat%len(configs);order=configs[shift:]+configs[:shift]
        for config in order:
            for split in (('train',) if phase=='train' else ('new','stress')):
                source=OLD/'stress-input.csv' if split=='stress' else HERE/f'{split}-input.csv'
                expected=[{}]*3 if split=='stress' else fixtures[split]
                output=HERE/'raw'/f'{split}-{config["name"]}-r{repeat}.csv'
                output.unlink(missing_ok=True)
                subprocess.run([solver,'--n=11','--memo=18',f'--exact-replay={source}','--exact-replay-budget=5000',
                    f'--residual-exact-legal={config["gate"]}',f'--residual-evaluator={"outcome" if config["gate"] else "grundy"}',
                    f'--residual-outcome-budget={config["quota"]}',f'--csv={output}'],check=True,timeout=150)
                records.extend(parse(output.read_text(),expected,split,config,repeat))
                print(f'{phase} {split} {config["name"]} repeat={repeat} validated',flush=True)
    return records

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);p.add_argument('--phase',choices=('train','confirm'),required=True);args=p.parse_args()
    protocol=json.loads((HERE/'protocol.json').read_text());fixtures=json.loads((HERE/'fixtures.json').read_text())
    assert digest(pathlib.Path(args.solver))==protocol['solver_sha256']
    for name,value in protocol['hashes'].items():assert digest(HERE/name)==value
    for name in ('protocol.json','fixtures.json','train-input.csv','new-input.csv'):assert_committed(HERE/name)
    if args.phase=='train':
        assert not (HERE/'selection.json').exists(),'selection already frozen; use a new experiment for reselection'
        records=run_phase(args.solver,'train',fixtures,CONFIGS)
        dump(HERE/'training-records.json',records)
        selection=select(records)
        selection.update(protocol_sha256=digest(HERE/'protocol.json'),training_sha256=digest(HERE/'training-records.json'))
        dump(HERE/'selection.json',selection);print(json.dumps(selection,indent=2))
    else:
        assert_committed(HERE/'selection.json');assert_committed(HERE/'training-records.json')
        selection=json.loads((HERE/'selection.json').read_text())
        assert selection['protocol_sha256']==digest(HERE/'protocol.json')
        assert selection['training_sha256']==digest(HERE/'training-records.json')
        actual=select(json.loads((HERE/'training-records.json').read_text()))
        assert all(selection[k]==v for k,v in actual.items())
        configs=[CONFIGS[0],selection['candidate']]
        records=run_phase(args.solver,'confirm',fixtures,configs)
        dump(HERE/'confirmation-records.json',records)
        totals={s:aggregate(records,configs,s) for s in ('new','stress')}
        dump(HERE/'summary.json',dict(candidate=selection['candidate'],totals=totals,passed=adoption(totals,selection['candidate']),
            selection_sha256=digest(HERE/'selection.json')))
        print(json.dumps(json.loads((HERE/'summary.json').read_text()),indent=2))
if __name__=='__main__':main()
