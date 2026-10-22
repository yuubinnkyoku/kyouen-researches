#!/usr/bin/env python3
import argparse, pathlib, subprocess, sys, tempfile
HERE=pathlib.Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'residual-dfpn-integration-20261021'))
from integration import parse,roots_csv

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);args=p.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        tmp=pathlib.Path(directory)
        def run(name,extra):
            output=tmp/f'{name}.csv'
            subprocess.run([args.solver,'--n=4','--memo=12','--budget=10',f'--csv={output}',
                f'--log={tmp/(name+".log")}',*extra],check=True,timeout=20)
            return parse(output.read_text())
        off=run('off',['--empty','--node-budget=20000'])[0]
        on=run('on',['--empty','--node-budget=20000','--frame-children-cache'])[0]
        audit=run('audit',['--empty','--node-budget=20000','--frame-children-audit'])[0]
        for r in (on,audit):
            assert r['result']==off['result']==2
            for k in ('nodes','expansions','visited','exact_nodes'):assert r[k]==off[k]
            assert r['child_refreshes']>0 and r['frame_cache']==1
        assert off['frame_cache']==off['child_refreshes']==off['child_audits']==0
        assert off['geometry_builds']==on['geometry_builds']+on['child_refreshes']
        assert on['geometry_moves']<off['geometry_moves'] and on['child_audits']==0
        assert audit['child_audits']==audit['child_refreshes'] and audit['frame_audit']==1
        source=tmp/'roots.csv';roots_csv(source,[[0,1,2,4,9]]*2)
        rows=run('reuse',[f'--roots-csv={source}','--node-budget=2000','--frame-children-cache'])
        assert len(rows)==2 and rows[0]['result']==rows[1]['result']!=0
        assert rows[1]['geometry_builds']==rows[1]['geometry_moves']==rows[1]['child_refreshes']==0
        zero=run('zero',['--empty','--node-budget=0','--frame-children-cache'])[0]
        assert zero['nodes']==zero['geometry_builds']==zero['child_refreshes']==0
        for flag in ('--frame-children-cache','--frame-children-audit'):
            r=subprocess.run([args.solver,'--exact-replay=unused',flag],capture_output=True,text=True,timeout=5)
            assert r.returncode!=0 and 'requires normal df-pn' in r.stderr
    print('VERIFIED frame cache CLI, exact work equivalence, audited refreshes, root reset, zero cap and invalid modes')
if __name__=='__main__':main()
