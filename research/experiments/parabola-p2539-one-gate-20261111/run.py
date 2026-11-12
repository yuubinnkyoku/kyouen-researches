"""Preserve native exit status and enforce a120-second limit on one new restricted shape."""
import argparse
import subprocess
import sys
import time
from pathlib import Path

HERE=Path(__file__).resolve().parent


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();assert not a.output.exists();started=time.monotonic()
    args=[sys.executable,str(HERE/'produce.py'),'--output',str(a.output),'--budget','100000']
    try:
        r=subprocess.run(args,capture_output=True,text=True,timeout=120);rec=dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False)
    except subprocess.TimeoutExpired as e:
        decode=lambda x:x.decode(errors='replace') if isinstance(x,bytes) else x or '';rec=dict(returncode=None,stdout=decode(e.stdout),stderr=decode(e.stderr),timed_out=True)
    import json
    rec.update(arguments=args,elapsed_seconds=time.monotonic()-started)
    with (a.output/'launch.json').open('x',encoding='utf-8',newline='\n') as f:f.write(json.dumps(rec,indent=2)+'\n')
    print(rec['returncode'],rec['timed_out'],rec['stdout'],rec['stderr'],flush=True)


if __name__=='__main__':main()
