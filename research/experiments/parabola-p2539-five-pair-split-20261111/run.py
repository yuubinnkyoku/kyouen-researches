"""Bounded child launches with preserved actual exit status and timeout evidence."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import subprocess
import sys
import time
from search import HERE,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--proof',action='store_true');ap.add_argument('--case',choices=['retained','changed','both'],default='both');ap.add_argument('--budget',type=int,default=100000)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    def one(case):
        out=a.output/case;cmd=[sys.executable,str(HERE/'search.py'),'--case',case,'--budget',str(a.budget),'--output',str(out)]
        if a.proof:cmd.append('--proof')
        started=time.monotonic()
        try:
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=300);report=dict(arguments=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False)
        except subprocess.TimeoutExpired as exc:
            dec=lambda x:x.decode(errors='replace') if isinstance(x,bytes) else x or ''
            report=dict(arguments=cmd,returncode=None,stdout=dec(exc.stdout),stderr=dec(exc.stderr),timed_out=True)
        report['elapsed_seconds']=time.monotonic()-started
        assert out.exists();save(out/'launch.json',report);print(case,report['returncode'],report['stdout'],report['stderr'],flush=True)
    with ThreadPoolExecutor(max_workers=2) as pool:list(pool.map(one,['retained','changed'] if a.case=='both' else [a.case]))


if __name__=='__main__':main()
