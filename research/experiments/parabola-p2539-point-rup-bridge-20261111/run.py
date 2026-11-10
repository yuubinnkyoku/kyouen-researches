"""Resume distinct point-proof children without restarting existing evidence."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import subprocess
import sys
import time
from produce import HERE,OBSTRUCTIONS,save


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--points',type=int,nargs='*');ap.add_argument('--budget',type=int,default=10000)
    a=ap.parse_args();a.output.mkdir(parents=True,exist_ok=True);points=json.loads(OBSTRUCTIONS.read_bytes())['excluded'] if a.points is None else a.points
    assert len(points)==len(set(points))
    def one(u):
        d=a.output/str(u)
        if d.exists():print('PRESERVED existing',u,flush=True);return
        cmd=[sys.executable,str(HERE/'produce.py'),'--point',str(u),'--budget',str(a.budget),'--output',str(d)];started=time.monotonic()
        try:
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=120);rec=dict(returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,timed_out=False)
        except subprocess.TimeoutExpired as exc:
            dec=lambda x:x.decode(errors='replace') if isinstance(x,bytes) else x or ''
            rec=dict(returncode=None,stdout=dec(exc.stdout),stderr=dec(exc.stderr),timed_out=True)
        rec.update(arguments=cmd,elapsed_seconds=time.monotonic()-started);assert d.exists();save(d/'launch.json',rec);print(u,rec['returncode'],rec['stdout'].strip(),flush=True)
    with ThreadPoolExecutor(max_workers=3) as pool:list(pool.map(one,points))


if __name__=='__main__':main()
