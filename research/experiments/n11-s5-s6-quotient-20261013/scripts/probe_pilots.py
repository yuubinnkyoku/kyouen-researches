"""Cold, node-bounded exact probes of two geometry-audited S5 pilots."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
ROOT=Path(__file__).resolve().parents[4]
EXP=Path(__file__).resolve().parents[1]


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--solver',type=Path,required=True)
    parser.add_argument('--budget',type=int,default=10000000)
    parser.add_argument('--prefix',default='budget10m')
    args=parser.parse_args()
    assert args.budget>0
    rows=json.loads((EXP/'output/pilots.json').read_text())['rows']
    by_index={r['s5_index']:r for r in rows}
    receipts=[]
    for i in (558600,209644):
        row=by_index[i]
        source=EXP/f'input/pilot-{i}.csv'
        source.write_text(f'pilot,{i},5,{row["mask"][0]},{row["mask"][1]},{row["legal"]},5,0,0,0,0\n')
        out=EXP/f'output/{args.prefix}-{i}-replay.csv'
        proof=EXP/f'output/{args.prefix}-{i}-proof.csv'
        if out.exists() or proof.exists():raise RuntimeError('refusing to overwrite probe outputs; choose new prefix')
        command=[str(args.solver.resolve()),'--n=11','--memo=20','--only=5','--exact-order=count',
                 f'--exact-replay={source}',f'--exact-replay-budget={args.budget}',
                 '--exact-replay-profile',f'--proof-dag={proof}',f'--csv={out}']
        proc=subprocess.run(command,text=True,capture_output=True,check=True)
        output=out.read_text()
        assert 'replay_error,' not in output and '# replay_done rows=1' in output
        result=[line.split(',') for line in output.splitlines() if line.startswith('replay,')]
        assert len(result)==1
        r=result[0]
        assert int(r[2])==5 and int(r[3])==row['legal'] and [int(r[9]),int(r[10])]==row['mask']
        verdict=int(r[6]);nodes=int(r[7])
        assert verdict in (0,1,2) and 0<nodes<=args.budget
        if verdict==0:
            assert nodes==args.budget and not proof.exists()
        else:assert proof.exists()
        receipts.append(dict(s5_index=i,legal=row['legal'],canonical_children=row['canonical_children'],
                             result=verdict,verdict={0:'UNKNOWN',1:'first-player-WIN',2:'first-player-LOSS'}[verdict],
                             nodes=nodes,wall_seconds_reported=int(r[8]),
                             input_sha256=digest(source),output_sha256=digest(out),proof_present=proof.exists()))
        print(receipts[-1],flush=True)
    manifest=dict(schema='n11-cold-pilot-probes-v1',budget=args.budget,order='count-asc',memo_power=20,
                  solver_source_sha256=digest(ROOT/'cpp/solvers/kyouen_dfpn_root.cpp'),
                  solver_binary_sha256=digest(args.solver),rows=receipts,
                  trust='exact solver verdicts only; any completed trace still requires independent terminal-only verification')
    (EXP/f'output/{args.prefix}-manifest.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')

if __name__=='__main__':main()
