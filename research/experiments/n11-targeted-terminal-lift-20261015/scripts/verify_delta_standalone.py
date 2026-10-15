#!/usr/bin/env python3
"""Independent Python terminal replay of C++ S10 verdict, state count and legal moves."""
if not __debug__:raise SystemExit('python -O forbidden')
import sys
from pathlib import Path
from multiprocessing import Pool
from fifth_verify_standalone import canonical,safe,terminal_s10

def check(record):
 h,v,states,moves=record
 m=int(h,16)
 if m.bit_count()!=10 or canonical(m)!=m or not safe(m):raise ValueError(f'bad S10 {h}')
 loss,n,k=terminal_s10(m)
 if ('LOSS' if loss else 'WIN',n,k)!=(v,states,moves):raise ValueError(f'CONFLICT {h}: Python {loss,n,k} C++ {v,states,moves}')
 return v,n

def main(path):
 records=[];seen=set()
 for line in Path(path).read_text().splitlines():
  a=line.split()
  if len(a)!=4 or len(a[0])!=32 or a[1] not in ('LOSS','WIN') or not a[2].isdigit() or not a[3].isdigit():raise ValueError(f'bad record {line}')
  if a[0] in seen:raise ValueError('duplicate')
  seen.add(a[0]);records.append((a[0],a[1],int(a[2]),int(a[3])))
 wins=losses=states=0
 with Pool(processes=4) as pool:
  for v,n in pool.imap_unordered(check,records,chunksize=8):
   wins+=v=='WIN';losses+=v=='LOSS';states+=n
 print('PASS independent Python/C++',len(records),'WIN',wins,'LOSS',losses,'terminal states',states)
if __name__=='__main__':main(sys.argv[1])
