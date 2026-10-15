#!/usr/bin/env python3
"""Derive all S7 LOSS parents of S8 LOSS roots by independent integer geometry."""
import sys
from pathlib import Path
from fifth_verify_standalone import canonical,children,points,safe

def main(cert,oldloss,oldwin,out):
 roots=[]
 for line in Path(cert).read_text().splitlines():
  a=line.split()
  if a and a[0]=='ROOT':roots.append(int(a[1],16))
 assert len(roots)==3 and len(set(roots))==3
 previous=set(Path(oldloss).read_text().split())
 wins=set(Path(oldwin).read_text().split())
 parents=set()
 for s8 in roots:
  assert s8.bit_count()==8 and safe(s8) and canonical(s8)==s8
  for p in points(s8):
   s7=canonical(s8^(1<<p))
   assert s8 in children(s7)
   parents.add(f'{s7:032x}')
 assert not parents&wins,'WIN/LOSS conflict'
 delta=parents-previous
 Path(out).write_text(''.join(x+'\n' for x in sorted(delta)))
 print('PASS S7 LOSS parents',len(parents),'new',len(delta),'overlap',len(parents&previous),'conflicts',0)
if __name__=='__main__':main(*sys.argv[1:])
