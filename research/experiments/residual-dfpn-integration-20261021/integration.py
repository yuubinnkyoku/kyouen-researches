#!/usr/bin/env python3
"""Small end-to-end normal-search CLI regressions; no deep exploration."""
import argparse,itertools,json,pathlib,subprocess,tempfile
HERE=pathlib.Path(__file__).resolve().parent

def forbidden(points):
    # Independent four-point circle/line determinant on the 4x4 board.
    rows=[(v%4,v//4,(v%4)**2+(v//4)**2) for v in points]
    base=rows[0];a,b,c=[tuple(row[i]-base[i] for i in range(3)) for row in rows[1:]]
    return a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0])==0

def expected_late(root):
    assert not any(forbidden(q) for q in itertools.combinations(root,4))
    legal=[v for v in range(16) if v not in root and not any(forbidden((*t,v)) for t in itertools.combinations(root,3))]
    assert len(legal)==2
    pair_forbidden=any(forbidden(q) for q in itertools.combinations([*root,*legal],4))
    g=int(pair_forbidden) # a forbidden pair: N; two free vertices: P
    return 1 if (g!=0)==(len(root)%2==0) else 2

def parse(raw):
    lines=raw.splitlines();rows=[]
    for line in lines:
        if line.startswith('# dfpn_root '):
            d=dict(x.split('=') for x in line.split()[2:])
            assert d['reason'] in ('DONE','NODE_BUDGET','TIME_BUDGET')
            for k in d.keys()-{'reason'}:d[k]=int(d[k])
            assert d['nodes']==d['visited']+d['exact_nodes']
            if d['node_limited']:assert d['nodes']<=d['node_budget']
            if d['reason']=='NODE_BUDGET':assert d['nodes']==d['node_budget'] and d['result']==0
            assert 0<=d['pn_nodes']<=d['pn_budget'] and d['pn_nodes']+d['pn_remaining']==d['pn_budget']
            rows.append(d)
    assert rows
    return rows

def roots_csv(path,roots):
    path.write_text('canonical_parent,move\n'+''.join('"'+','.join(map(str,r[:-1]))+'",'+str(r[-1])+'\n' for r in roots))

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);p.add_argument('--output',type=pathlib.Path,default=HERE);args=p.parse_args()
    (args.output/'raw').mkdir(parents=True,exist_ok=True);summary={}
    pn=['--residual-exact-legal=6','--residual-evaluator=outcome','--residual-outcome-budget=128']
    with tempfile.TemporaryDirectory() as tmp:
        tmp=pathlib.Path(tmp)
        def run(name,extra):
            output=args.output/'raw'/f'integration-{name}.csv';output.unlink(missing_ok=True)
            command=[args.solver,'--n=4','--memo=16','--budget=5',f'--csv={output}',f'--log={tmp/(name+".log")}',*extra]
            subprocess.run(command,check=True,timeout=15)
            rows=parse(output.read_text());summary[name]=rows;return rows
        off=run('off',['--empty','--node-budget=20000'])[0];assert off['result']==2
        on=run('on',['--empty','--node-budget=20000',*pn])[0];assert on['result']==2 and on['pn_nodes']>0
        disabled=run('quota-zero',['--empty','--node-budget=20000',*pn,'--residual-outcome-budget=0'])[0]
        assert disabled['result']==2 and disabled['nodes']==off['nodes'] and disabled['residual_calls']==0
        zero=run('node-zero',['--empty','--node-budget=0'])[0];assert zero['nodes']==0 and zero['result']==0
        hybrid=run('hybrid',['--empty','--node-budget=7','--exact-legal=16','--exact-budget=100000'])[0]
        assert hybrid['nodes']==7 and hybrid['exact_nodes']>0 and hybrid['result']==0
        default=run('default',['--empty'])[0]
        assert default['result']==2 and default['residual_gate']==0 and default['node_limited']==0
        for i,root in enumerate(([0,1,2,4,9],[0,1,3,5,8,14])):
            source=tmp/f'late-{i}.csv';roots_csv(source,[root,root])
            rows=run(f'late-{i}',[f'--roots-csv={source}','--node-budget=1',*pn,'--residual-profile'])
            assert len(rows)==2 and all(r['result']==expected_late(root) for r in rows)
            assert rows[0]['pn_nodes']==1 and rows[1]['pn_nodes']==0 and rows[1]['pn_remaining']==128
            assert rows[0]['build_ns']>0 and rows[1]['build_ns']==0
        for extra in (['--empty','--node-budget=-1'],['--exact-replay=unused','--node-budget=10']):
            r=subprocess.run([args.solver,*extra],capture_output=True,text=True,timeout=5)
            assert r.returncode!=0 and 'error:' in r.stderr
    (args.output/'integration-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    print('VERIFIED normal CLI direct PN, zero quota/cap, shared hybrid budget, default OFF, both turn parities, repeated-root reset and invalid modes')
if __name__=='__main__':main()
