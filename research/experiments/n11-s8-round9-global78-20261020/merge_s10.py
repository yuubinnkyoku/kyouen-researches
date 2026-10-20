#!/usr/bin/env python3
"""Atomic fail-closed merge of historical and new S10 cache snapshots.
Input values are not automatically trusted: verify their provenance separately.
"""
import argparse,os,tempfile
from pathlib import Path
from verify_core import canonical,safe
B=Path(__file__).resolve().parent

def read(path):
 out={}
 for line in Path(path).read_text().splitlines():
  a=line.split('\t')
  if len(a) not in (3,5):raise ValueError('bad row')
  h,v,n=a[:3]
  if len(h)!=32 or any(c not in '0123456789abcdef' for c in h) or v not in ('WIN','LOSS') or not n.isdecimal():raise ValueError('bad row values')
  x=int(h,16)
  if x.bit_count()!=10 or canonical(x)!=x or not safe(x):raise ValueError('invalid position')
  if h in out:raise ValueError('duplicate key '+h)
  out[h]=(v,int(n))
 return out

def merge(a,b):
 out=dict(a);overlap=0
 for k,v in b.items():
  if k in out:
   if out[k]!=v:raise ValueError('verdict or state conflict '+k)
   overlap+=1
  else:out[k]=v
 return out,overlap

def run(output):
 output=Path(output)
 if output.exists():raise ValueError('refusing overwrite')
 paths=[B/'prior_s10_5561.tsv',B/'round8_s10_3975.tsv',B/'round9_new_s10_cpp.tsv']
 sizes=[5561,3975,285];expected=[0,63,19]
 out={}
 for p,size,over in zip(paths,sizes,expected):
  rows=read(p)
  if len(rows)!=size:raise ValueError('unexpected source count')
  out,n=merge(out,rows)
  if n!=over:raise ValueError('unexpected overlap count')
 if len(out)!=9739:raise ValueError('unexpected merged count')
 payload=''.join(f'{k}\t{v}\t{n}\n' for k,(v,n) in sorted(out.items()))
 fd,tmp=tempfile.mkstemp(dir=output.parent,prefix='.n11-merge-',suffix='.tmp')
 try:
  with os.fdopen(fd,'w') as f:f.write(payload);f.flush();os.fsync(f.fileno())
  os.replace(tmp,output)
 finally:
  if os.path.exists(tmp):os.unlink(tmp)
 print('PASS safe merge 5561+3975+285-63-19=9739, no conflicts')
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('output');run(p.parse_args().output)
