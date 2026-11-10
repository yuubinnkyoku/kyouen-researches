"""One bounded child with actual native exit and timeout receipt."""
import argparse
from pathlib import Path
import subprocess
import sys
import time
from search import HERE,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--budget',type=int,default=100000);ap.add_argument('--proof',action='store_true')
    a=ap.parse_args();assert not a.output.exists();cmd=[sys.executable,str(HERE/'search.py'),'--output',str(a.output),'--budget',str(a.budget)]
    if a.proof:cmd.append('--proof')
    started=time.monotonic()
    try:
        r=subprocess.run(cmd,capture_output=True,text=True,timeout=300);report=dict(arguments=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False)
    except subprocess.TimeoutExpired as exc:
        dec=lambda x:x.decode(errors='replace') if isinstance(x,bytes) else x or ''
        report=dict(arguments=cmd,returncode=None,stdout=dec(exc.stdout),stderr=dec(exc.stderr),timed_out=True)
    report['elapsed_seconds']=time.monotonic()-started;save(a.output/'launch.json',report);print(report['returncode'],report['stdout'],report['stderr'],flush=True)


if __name__=='__main__':main()
