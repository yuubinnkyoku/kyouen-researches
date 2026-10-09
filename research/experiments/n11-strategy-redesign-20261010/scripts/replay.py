"""Finite fresh-process exact replays, with history exclusion and RSS measurement.

No solver/pruning change. Each run has a fixed plan and a wall watchdog.
"""
import argparse
import csv
import ctypes
import json
import platform
import subprocess
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED
from pathlib import Path
from study import ROOT, EXP, pts, canon, legal_points, sha, dump

def memory(proc):
    if platform.system() != 'Windows':
        return None
    class Counters(ctypes.Structure):
        _fields_ = [('cb',ctypes.c_ulong),('faults',ctypes.c_ulong)] + [(s,ctypes.c_size_t) for s in
          ['peak_rss','rss','peak_pool_paged','pool_paged','peak_pool_nonpaged','pool_nonpaged','pagefile','peak_pagefile']]
    c = Counters()
    c.cb = ctypes.sizeof(c)
    fn = ctypes.windll.psapi.GetProcessMemoryInfo
    fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
    if fn(int(proc._handle),ctypes.byref(c),c.cb):
        return c.peak_rss
    return None

def run(plan_path, solver, outdir, watchdog=180):
    plan = json.loads(plan_path.read_text(encoding='utf-8'))
    history_path = EXP/'output/history.json'
    assert plan['history_sha256'] == sha(history_path)
    history = {(h['stones'],*h['key']):h for h in json.loads(history_path.read_text())}
    # Include all prior runs of this experiment, to prevent accidental repeats.
    for f in (EXP/'output').glob('*/summary.json'):
        for r in json.loads(f.read_text()).get('results',[]):
            if r.get('verdict') is None:
                continue
            k = (r['stones'],*r['key'])
            h = history.setdefault(k,dict(verdict=0,max_unknown_budget=0))
            if r['verdict']:
                assert h['verdict'] in (0,r['verdict'])
                h['verdict'] = r['verdict']
            else:
                h['max_unknown_budget'] = max(h['max_unknown_budget'],r['budget'])
    assert not outdir.exists(), 'refusing output directory reuse'
    assert len({(r['stones'],*r['key']) for r in plan['targets']}) == len(plan['targets'])
    # Check EVERY target before dispatch, including same/larger budget UNKNOWN.
    for r in plan['targets']:
        k = (r['stones'],*r['key'])
        h = history.get(k,{})
        assert not h.get('verdict'), ('already exact',k)
        assert h.get('max_unknown_budget',0) < r['budget'], ('same-budget UNKNOWN',k)
        p = pts(r['key'])
        assert len(p)==r['stones'] and canon(p)==tuple(r['key'])
        legal_points(p)  # raises for unsafe geometry
    outdir.mkdir()
    records = []
    receipt = dict(plan=plan_path.relative_to(ROOT).as_posix(), plan_sha256=sha(plan_path),
                   history_sha256=sha(history_path), solver_path=solver.relative_to(ROOT).as_posix(),
                   solver_sha256=sha(solver), solver_source_sha256=sha(ROOT/'cpp/solvers/kyouen_dfpn_root.cpp'),
                   residual_header_sha256=sha(ROOT/'cpp/solvers/kyouen_residual_micro.hpp'),
                   command_options=['--n=11','--memo=22','--exact-order=count'],
                   hardware=platform.uname()._asdict(), workers=1, watchdog_seconds=watchdog, results=records)
    stopped_groups = set()
    for r in plan['targets']:
        if r.get('group') in stopped_groups:
            records.append(r | {'skipped':'group WIN witness already found'})
            continue
        n, k, budget = r['stones'],r['key'],r['budget']
        legal = len(legal_points(pts(k)))
        stem = f's{n}-{k[0]}-{k[1]}'
        inp, raw, log = [outdir/(stem+s) for s in ('.input.csv','.out.csv','.log')]
        with inp.open('x',encoding='utf-8',newline='') as f:
            csv.writer(f,lineterminator='\n').writerow(['target',0,n,*k,legal,0,int(n%2==0),0,0,0])
        cmd = [str(solver),'--n=11','--memo=22',f'--exact-replay={inp}',f'--only={n}',
               '--exact-order=count',f'--exact-replay-budget={budget}',f'--csv={raw}']
        start = time.monotonic()
        peak = 0
        with log.open('x',encoding='utf-8') as f:
            p = subprocess.Popen(cmd,stdout=f,stderr=subprocess.STDOUT)
            aborted = False
            while p.poll() is None:
                peak = max(peak,memory(p) or 0)
                if time.monotonic()-start > watchdog:
                    p.kill()
                    p.wait()
                    aborted = True
                    break
                time.sleep(.1)
        elapsed = time.monotonic()-start
        rec = r | dict(legal=legal,wall_seconds=elapsed,peak_rss_bytes=peak,command=cmd,
                       input=inp.relative_to(ROOT).as_posix(),input_sha256=sha(inp),
                       raw=raw.relative_to(ROOT).as_posix(),raw_sha256=sha(raw) if raw.exists() else None,
                       log=log.relative_to(ROOT).as_posix(),log_sha256=sha(log),exit_code=p.returncode)
        if aborted:
            rec.update(verdict=None,nodes=None,aborted='wall watchdog; no verdict adopted')
        else:
            assert p.returncode == 0
            rows = [x for x in csv.reader(raw.open()) if x and x[0]=='replay']
            assert len(rows)==1 and len(rows[0])==11
            x = rows[0]
            assert [int(x[i]) for i in (2,3,4,5,9,10)] == [n,legal,int(n%2==0),budget,*k]
            verdict,nodes = int(x[6]),int(x[7])
            assert verdict in (0,1,2) and 0<=nodes<=budget
            rec.update(verdict=verdict,nodes=nodes)
            # S5 WIN is already a class rejection; no more sibling dispatch.
            if n==5 and verdict==1 and r.get('group'):
                stopped_groups.add(r['group'])
        records.append(rec)
        receipt.update(total_nodes=sum(x.get('nodes') or 0 for x in records),
                       verdict_counts=dict(Counter(x.get('verdict') for x in records if 'verdict' in x)))
        dump(outdir/'summary.json',receipt)
        print(r.get('arm'),n,k,rec.get('verdict'),rec.get('nodes'),round(elapsed,2),flush=True)
    return receipt

def parallel_run(plan_path, solver, outdir, workers):
    """Fresh solver per target; stop dispatch on a class WIN and drain active work."""
    assert 1<workers<=4 and not outdir.exists()
    plan=json.loads(plan_path.read_text())
    assert len({(r['stones'],*r['key']) for r in plan['targets']})==len(plan['targets'])
    outdir.mkdir()
    results=[]
    receipt=None
    cursor=0
    active={}
    stopped=set()
    with ThreadPoolExecutor(max_workers=workers) as pool:
        while True:
            while cursor<len(plan['targets']) and len(active)<workers:
                r=plan['targets'][cursor]
                seq=cursor
                cursor+=1
                if r.get('group') in stopped:
                    results.append(r|dict(skipped='class WIN witness; not dispatched'))
                    continue
                subplan=outdir/f'row-{seq}-plan.json'
                dump(subplan,dict(history_sha256=plan['history_sha256'],targets=[r],parent_plan_sha256=sha(plan_path)))
                future=pool.submit(run,subplan,solver,outdir/f'row-{seq}')
                active[future]=r
            if not active:
                break
            done,_=wait(active,return_when=FIRST_COMPLETED)
            for future in done:
                target=active.pop(future)
                child_receipt=future.result()
                if receipt is None:
                    receipt=child_receipt|dict(plan=plan_path.relative_to(ROOT).as_posix(),plan_sha256=sha(plan_path),workers=workers)
                r=child_receipt['results'][0]
                results.append(r)
                if r.get('verdict')==1 and r['stones']==5 and r.get('group'):
                    stopped.add(r['group'])
            receipt.update(results=results,total_nodes=sum(r.get('nodes') or 0 for r in results),
                           verdict_counts=dict(Counter(r['verdict'] for r in results if 'verdict' in r)))
            dump(outdir/'summary.json',receipt)
    return receipt

if __name__=='__main__':
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--plan',type=Path,required=True)
    ap.add_argument('--solver',type=Path,required=True)
    ap.add_argument('--out',type=Path,required=True)
    ap.add_argument('--workers',type=int,default=1)
    args=ap.parse_args()
    if args.workers==1:
        run(args.plan.resolve(),args.solver.resolve(),args.out.resolve())
    else:
        parallel_run(args.plan.resolve(),args.solver.resolve(),args.out.resolve(),args.workers)
