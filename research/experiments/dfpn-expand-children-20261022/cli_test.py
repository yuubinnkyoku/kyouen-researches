#!/usr/bin/env python3
import argparse,pathlib,subprocess,tempfile
from study import parse,roots_csv,compare
def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);a=p.parse_args()
    with tempfile.TemporaryDirectory() as directory:
        tmp=pathlib.Path(directory)
        def run(name,flags):
            out=tmp/f'{name}.csv'
            subprocess.run([a.solver,'--n=4','--memo=12','--budget=10',f'--csv={out}',f'--log={tmp/(name+".log")}',*flags],check=True,timeout=20)
            return parse(out.read_text())
        common=['--empty','--node-budget=20000']
        off=run('off',common)[0];cache=run('cache',common+['--frame-children-cache'])[0]
        expanded=run('expand',common+['--frame-children-expand-reuse'])[0]
        compare(off,cache,expanded)
        assert expanded['result']==2 and expanded['frame_expand_reuse']==expanded['frame_cache']==1 and expanded['frame_expand_uses']>0
        audited=run('audit',common+['--frame-children-expand-reuse','--frame-children-audit'])[0]
        assert audited['child_audits']==audited['child_refreshes']>0 and audited['result']==2
        source=tmp/'roots.csv';roots_csv(source,[[0,1,2,4,9]]*2)
        rows=run('repeat',[f'--roots-csv={source}','--node-budget=2000','--frame-children-expand-reuse'])
        assert len(rows)==2 and rows[0]['result']==rows[1]['result']!=0
        assert rows[1]['geometry_builds']==rows[1]['child_refreshes']==rows[1]['frame_expand_uses']==0
        for value in ('--exact-replay=unused','--quant-replies=0'):
            r=subprocess.run([a.solver,value,'--frame-children-expand-reuse'],capture_output=True,text=True,timeout=5)
            assert r.returncode!=0 and 'requires normal df-pn' in r.stderr
    print('VERIFIED expand ownership CLI, three-way work/build equivalence, audited first refresh, root reset and mode rejection')
if __name__=='__main__':main()
