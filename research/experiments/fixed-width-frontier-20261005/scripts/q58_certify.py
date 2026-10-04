#!/usr/bin/env python3
"""Generate and independently DRAT-check every finite q=8,w=5 exclusion.

The saved manifest contains hashes of exact inputs and generated traces.
Trace retention is optional; the reproduction regenerates and checks them.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

if not __debug__:
    raise SystemExit('Certificate validation requires assertions; do not run Python with -O.')

from q58_sat import encode


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pysat-path',default='/workspace/research-tools/python-sat')
    ap.add_argument('--cadical',required=True)
    ap.add_argument('--drat-trim',required=True)
    ap.add_argument('--work-dir',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--low',type=int,default=16)
    ap.add_argument('--high',type=int,default=185)
    ap.add_argument('--seconds',type=int,default=60)
    ap.add_argument('--keep-critical',type=Path)
    args=ap.parse_args()
    sys.path.insert(0,args.pysat_path)
    import pysat
    args.work_dir.mkdir(parents=True,exist_ok=True)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    meta=dict(schema=1,statement='M_{5,8}=16',
              finite_scope={'m':[args.low,args.high],'target_rows':[0,1,2]},
              python_sat_version=pysat.__version__,
              cadical_version=subprocess.check_output([args.cadical,'--version'],text=True).strip(),
              cadical_binary_sha256=sha(Path(args.cadical)),
              drat_trim_source_revision='2e3b2dc0ecf938addbd779d42877b6ed69d9a985',
              drat_trim_binary_sha256=sha(Path(args.drat_trim)),
              records=[])
    for m in range(args.low,args.high+1):
        for target in range(3):
            started=time.monotonic()
            clauses,nv,cs=encode(m,target)
            cnf=args.work_dir/'current.cnf'
            proof=args.work_dir/'current.drat'
            cnf.write_text(f'p cnf {nv} {len(clauses)}\n'+''.join(
                ' '.join(map(str,c))+' 0\n' for c in clauses))
            solver=subprocess.run([args.cadical,'-q','-t',str(args.seconds),str(cnf),str(proof)],
                                  capture_output=True,text=True)
            assert solver.returncode==20 and 's UNSATISFIABLE' in solver.stdout, (m,target,solver.stdout,solver.stderr)
            checked=subprocess.run([args.drat_trim,str(cnf),str(proof)],capture_output=True,text=True)
            assert checked.returncode==0 and 's VERIFIED' in checked.stdout, (m,target,checked.stdout,checked.stderr)
            record=dict(m=m,target_row=target,status='UNSAT',drat_status='VERIFIED',
                        variables=nv,clauses=len(clauses),circles=len(cs),
                        cnf_sha256=sha(cnf),drat_sha256=sha(proof),drat_bytes=proof.stat().st_size,
                        wall_seconds=round(time.monotonic()-started,6))
            if args.keep_critical and m==args.low:
                args.keep_critical.mkdir(parents=True,exist_ok=True)
                for source,suffix in [(cnf,'cnf'),(proof,'drat')]:
                    destination=args.keep_critical/f'm{m}-r{target}.{suffix}.gz'
                    with destination.open('wb') as raw:
                        with gzip.GzipFile(filename='',fileobj=raw,mode='wb',mtime=0) as gz:
                            gz.write(source.read_bytes())
                    record[suffix+'_retained_sha256']=sha(destination)
            meta['records'].append(record)
            args.output.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'m':m,'all_rows':'DRAT VERIFIED','records':len(meta['records'])}),flush=True)
    meta['all_finite_cases_verified']=True
    args.output.write_text(json.dumps(meta,ensure_ascii=False,indent=2)+'\n')


if __name__=='__main__':main()
