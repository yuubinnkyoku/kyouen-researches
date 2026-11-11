"""Run distinct point assumptions with preserved native exit status and resumable evidence."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from pathlib import Path
import subprocess
import sys
import time
from encoding import HERE,build,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--points',nargs='*',type=int);ap.add_argument('--budget',type=int,default=10000);ap.add_argument('--proof',action='store_true')
    a=ap.parse_args();body,meta=build();a.output.mkdir(parents=True,exist_ok=True)
    if not (a.output/'base.cnf.gz').exists():
        (a.output/'base.cnf.gz').write_bytes(gzip.compress(body,mtime=0));save(a.output/'base.json',meta)
    points=meta['gate_points'] if a.points is None else a.points;assert len(points)==len(set(points)) and set(points)<=set(meta['gate_points'])
    def one(u):
        d=a.output/str(u)
        if d.exists():print('PRESERVED existing',u,flush=True);return
        cmd=[sys.executable,str(HERE/'search.py'),'--point',str(u),'--budget',str(a.budget),'--output',str(d)]
        if a.proof:cmd.append('--proof')
        started=time.monotonic()
        try:
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=120);rec=dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False)
        except subprocess.TimeoutExpired as exc:
            dec=lambda x:x.decode(errors='replace') if isinstance(x,bytes) else x or ''
            rec=dict(returncode=None,stdout=dec(exc.stdout),stderr=dec(exc.stderr),timed_out=True)
        rec.update(arguments=cmd,elapsed_seconds=time.monotonic()-started);assert d.exists();save(d/'launch.json',rec);print(u,rec['returncode'],rec['stdout'].strip(),flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(one,points))


if __name__=='__main__':main()
