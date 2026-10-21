#!/usr/bin/env python3
"""Small bounded fallback, parity, proof-capture and CLI regressions."""
import argparse,csv,json,pathlib,subprocess,sys,tempfile
HERE=pathlib.Path(__file__).resolve().parent
ROOT=HERE.parents[2]

def fields(lines,prefix):
    return [dict(x.split('=') for x in s.split()[2:]) for s in lines if s.startswith(prefix)]

def main():
    p=argparse.ArgumentParser();p.add_argument('--solver',required=True);args=p.parse_args()
    summaries={}
    with tempfile.TemporaryDirectory() as tmp:
        tmp=pathlib.Path(tmp);source=tmp/'input.csv';source.write_text('fixture,0,0,0,0,16,0,0,0,0,0\n')
        for name,quota,gate,extra in [('native',100000,0,[]),('grundy',100000,16,['--residual-evaluator=grundy']),
            *[(f'pn-{q}',q,16,['--residual-evaluator=outcome']) for q in (0,1,2,10,100000)],
            ('shadow',100000,16,['--residual-evaluator=outcome','--residual-crosscheck-legal=16']),
            ('proof',100000,0,['--residual-evaluator=outcome',f'--proof-dag={tmp/"proof.csv"}'])]:
            output=HERE/'raw'/f'integration-{name}.csv'
            output.unlink(missing_ok=True)
            subprocess.run([args.solver,'--n=4','--memo=16',f'--exact-replay={source}',
                '--exact-replay-budget=5000',f'--residual-exact-legal={gate}',
                f'--residual-outcome-budget={quota}',f'--csv={output}',*extra],check=True,timeout=30)
            lines=output.read_text().splitlines();assert not any(s.startswith('replay_error,') for s in lines)
            rows=list(csv.reader(s for s in lines if s.startswith('replay,')));assert len(rows)==1 and int(rows[0][6])==2
            stats=fields(lines,'# residual_outcome ')
            if stats:
                st=stats[0];assert int(st['nodes'])+int(st['remaining'])==quota
                if quota in (1,2,10):assert int(st['aborts'])==1 and int(st['remaining'])==0
            summaries[name]=dict(result=2,nodes=int(rows[0][7]),outcome=stats)
        assert summaries['native']['nodes']==summaries['pn-0']['nodes']
        assert summaries['proof']['outcome']==[]
        sys.path.insert(0,str(ROOT/'research/experiments/n11-proof-dag-engine-20261011/scripts'))
        from trace_to_certificate import trace_to_certificate
        from dag_verifier import verify_certificate
        cert,_=trace_to_certificate(tmp/'proof.csv',4,0,2)
        receipt=verify_certificate(cert);assert receipt['verdict']==2 and receipt['trusted_leaves']==0
        summaries['proof']['certificate_receipt']=receipt
        # Unknown roots do not create a proof or a solved result.
        output=tmp/'unknown.csv'
        subprocess.run([args.solver,'--n=4','--memo=16',f'--exact-replay={source}',
            '--exact-replay-budget=0','--residual-exact-legal=16','--residual-evaluator=outcome',
            '--residual-outcome-budget=1',f'--csv={output}'],check=True,timeout=30)
        rows=list(csv.reader(s for s in output.read_text().splitlines() if s.startswith('replay,')))
        assert len(rows)==1 and int(rows[0][6])==0 and int(rows[0][7])==0
        for extra in (['--residual-evaluator=outcome','--residual-share-gate=6'],
                      ['--residual-outcome-budget=-1'],['--residual-evaluator=bad'],
                      ['--residual-evaluator=outcome','--residual-exact-legal=16',f'--proof-dag={tmp/"forbidden.csv"}']):
            r=subprocess.run([args.solver,'--n=4',f'--exact-replay={source}',*extra],capture_output=True,text=True,timeout=5)
            assert r.returncode!=0 and 'error:' in r.stderr
    (HERE/'integration-summary.json').write_text(json.dumps(summaries,indent=2)+'\n')
    print('VERIFIED n4 native/SG/PN, quotas 0/1/2/10/100000, independent proof DAG, UNKNOWN and invalid flags')
if __name__=='__main__':main()
