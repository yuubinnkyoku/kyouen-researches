"""Prune a native proof trace and independently verify every retained node."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[4]
EXP=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'research/experiments/n11-proof-dag-engine-20261011/scripts'))
from trace_to_certificate import trace_to_certificate
from dag_verifier import verify_certificate


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('index',type=int)
    p.add_argument('--prefix',default='budget10m')
    p.add_argument('--trace-dir',type=Path,default=EXP/'output')
    p.add_argument('--output-dir',type=Path,default=EXP/'output')
    args=p.parse_args()
    manifest=json.loads((EXP/f'output/{args.prefix}-manifest.json').read_text())
    row=next(r for r in manifest['rows'] if r['s5_index']==args.index)
    parent=next(r for r in json.loads((EXP/'output/pilots.json').read_text())['rows'] if r['s5_index']==args.index)
    mask=parent['mask'][0]|parent['mask'][1]<<64
    trace=args.trace_dir/f'{args.prefix}-{args.index}-proof.csv'
    cert,stats=trace_to_certificate(trace,11,mask,row['result'])
    print(json.dumps(stats),flush=True)
    out=args.output_dir/f'pilot-{args.index}-terminal-dag.json.gz'
    with out.open('wb') as raw:
        with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as stream:
            stream.write((json.dumps(cert,sort_keys=True,separators=(',',':'))+'\n').encode())
    receipt=verify_certificate(cert)
    assert receipt['verdict']==row['result'] and receipt['trusted_leaves']==0
    receipt.update(stats=stats,trace_sha256=hashlib.sha256(trace.read_bytes()).hexdigest(),
                   certificate_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                   s5_index=args.index,root_mask=str(mask),
                   trust='all retained local geometry, ranked transitions, complete universal boundaries, existential witnesses and terminal payoffs checked; zero trusted leaves')
    (args.output_dir/f'pilot-{args.index}-terminal-verification.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(receipt,sort_keys=True,indent=2),flush=True)

if __name__=='__main__':main()
