"""Cold, finite exact search of remaining polarity-conflict S5 positions.

No UNKNOWN verdict enters the overlay. Native proof capture is a separate,
explicit flag: completed labels are solver-trusted until independently checked.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import hashlib
import json
from pathlib import Path
import subprocess
import time
ROOT=Path(__file__).resolve().parents[4]
EXP=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'research/experiments/n11-s5-s6-quotient-20261013/output/pilots.json'


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--solver',type=Path,default=ROOT/'build/kyouen-dfpn-root')
    p.add_argument('--budget',type=int,default=2000000)
    p.add_argument('--memo',type=int,default=20)
    p.add_argument('--order',choices=['count','countd','key','s5-countd','s5-target92'],default='count')
    p.add_argument('--workers',type=int,default=2)
    p.add_argument('--prefix',required=True)
    p.add_argument('--indices',type=int,nargs='*')
    p.add_argument('--capture',action='store_true')
    p.add_argument('--timeout',type=int,default=240)
    args=p.parse_args()
    assert 0<args.workers<=2 and args.budget>0 and 16<=args.memo<=24
    data=json.loads(SOURCE.read_text())
    candidates=[r for r in data['rows'] if 'polarity_conflicts' in r['labels'] and r['s5_index']!=209644]
    candidates.sort(key=lambda r:(r['canonical_children'],r['legal'],r['s5_index']))
    if args.indices is not None:
        candidates=[r for r in candidates if r['s5_index'] in args.indices]
        assert {r['s5_index'] for r in candidates}==set(args.indices)
    manifest=EXP/f'output/{args.prefix}-manifest.json'
    assert not manifest.exists(),'refusing to overwrite existing run'
    binary=args.solver.resolve()
    result=dict(schema='n11-conflict-probes-v1',budget=args.budget,memo_power=args.memo,
                order=args.order,workers=args.workers,source_sha256=sha(SOURCE),
                source=str(SOURCE.relative_to(ROOT)),solver_binary_sha256=sha(binary),
                solver_source_sha256=sha(ROOT/'cpp/solvers/kyouen_dfpn_root.cpp'),
                residual_header_sha256=sha(ROOT/'cpp/solvers/kyouen_residual_micro.hpp'),
                capture=args.capture,rows=[],trust='completed labels solver-trusted until independent terminal-only verification; UNKNOWN is not evidence')
    trace_dir=ROOT/'build/n11-conflict-native-traces'
    if args.capture:trace_dir.mkdir(exist_ok=True)
    def run(row):
        index=row['s5_index'];src=EXP/f'input/s5-{index}.csv'
        text=f'conflict,{index},5,{row["mask"][0]},{row["mask"][1]},{row["legal"]},5,0,0,0,0\n'
        if src.exists():assert src.read_text()==text
        else:src.write_text(text)
        out=EXP/f'output/{args.prefix}-{index}.csv'
        stderr=EXP/f'output/{args.prefix}-{index}.log'
        trace=trace_dir/f'{args.prefix}-{index}.csv'
        assert not out.exists() and not stderr.exists() and not trace.exists()
        command=[str(binary),'--n=11',f'--memo={args.memo}','--only=5',f'--exact-order={args.order}',
                 f'--exact-replay={src}',f'--exact-replay-budget={args.budget}',f'--csv={out}']
        if args.capture:command+=[f'--proof-dag={trace}']
        start=time.monotonic()
        try:
            proc=subprocess.run(command,capture_output=True,text=True,timeout=args.timeout)
        except subprocess.TimeoutExpired as exc:
            stderr.write_text('query timed out before completion\n')
            return dict(s5_index=index,mask=row['mask'],status='WALL_TIMEOUT',verdict=0,wall_seconds=time.monotonic()-start)
        stderr.write_text(proc.stderr+proc.stdout)
        assert proc.returncode==0,(index,proc.returncode)
        raw=out.read_text()
        assert 'replay_error,' not in raw and '# replay_done rows=1' in raw
        rows=[s.split(',') for s in raw.splitlines() if s.startswith('replay,')]
        assert len(rows)==1
        r=rows[0];v=int(r[6]);nodes=int(r[7])
        assert v in (0,1,2) and 0<nodes<=args.budget
        assert int(r[2])==5 and int(r[3])==row['legal'] and [int(r[9]),int(r[10])]==row['mask']
        if v==0:assert nodes==args.budget and not trace.exists()
        elif args.capture:assert trace.exists()
        return dict(s5_index=index,mask=row['mask'],legal=row['legal'],canonical_children=row['canonical_children'],
                    status='SOLVED' if v else 'NODE_LIMIT',verdict=v,nodes=nodes,
                    wall_seconds=round(time.monotonic()-start,3),input_sha256=sha(src),output_sha256=sha(out),
                    trace_sha256=sha(trace) if trace.exists() else None,
                    trace_path=str(trace.relative_to(ROOT)) if trace.exists() else None)
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures=[pool.submit(run,r) for r in candidates]
        for future in as_completed(futures):
            row=future.result();result['rows'].append(row);result['rows'].sort(key=lambda r:r['s5_index'])
            manifest.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
            print(json.dumps(row),flush=True)
    result['counts']={name:sum(r['verdict']==v for r in result['rows']) for name,v in [('UNKNOWN',0),('WIN',1),('LOSS',2)]}
    result['completed_candidates']=len(candidates)
    manifest.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result['counts']),flush=True)

if __name__=='__main__':main()
