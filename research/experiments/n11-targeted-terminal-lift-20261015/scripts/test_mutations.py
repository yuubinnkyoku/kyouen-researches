#!/usr/bin/env python3
"""Negative controls: malformed or falsified proofs must fail both verifiers."""
import subprocess,sys,tempfile
from pathlib import Path
from fifth_verify_standalone import children

def run(py,cpp,cert):
 src=Path(cert).read_text();lines=src.splitlines()
 cases={}
 cases['bad board']=src.replace('BOARD 11','BOARD 10',1)
 cases['bad count']=src.replace('ROOTS 3','ROOTS 4',1) if 'LOSS' in src.splitlines()[0] else src.replace('ROOTS 16','ROOTS 17',1)
 if 'LOSS' in lines[0]:
  w=next(i for i,s in enumerate(lines) if s.startswith('WITNESS '))
  cases['missing witness']='\n'.join(lines[:w]+lines[w+1:])+'\n'
  cases['duplicate witness']='\n'.join(lines[:w+1]+[lines[w]]+lines[w+1:])+'\n'
  tampered=lines.copy();a=tampered[w].split();a[2]='0'*32;tampered[w]=' '.join(a)
  cases['bad leaf']='\n'.join(tampered)+'\n'
  # A *legal* but WIN S10 child must not count as a LOSS witness.
  witness=lines[w].split();s9=int(witness[1],16)
  known_win={x.split()[0] for x in Path('../data/s10_merged_51571.tsv').read_text().splitlines() if x.endswith('WIN')}
  win=next((x for x in children(s9) if f'{x:032x}' in known_win),None)
  assert win is not None
  tampered=lines.copy();tampered[w]=f'WITNESS {s9:032x} {win:032x}'
  cases['legal wrong verdict']='\n'.join(tampered)+'\n'
 else:
  e=next(i for i,s in enumerate(lines) if s.startswith('EDGE '))
  cases['missing edge']='\n'.join(lines[:e]+lines[e+1:])+'\n'
  cases['duplicate edge']='\n'.join(lines[:e+1]+[lines[e]]+lines[e+1:])+'\n'
  tampered=lines.copy();a=tampered[e].split();a[2]='0'*32;tampered[e]=' '.join(a)
  cases['bad S9']='\n'.join(tampered)+'\n'
 with tempfile.TemporaryDirectory() as td:
  for label,content in cases.items():
   p=Path(td)/'bad.cert';p.write_text(content)
   for cmd in ([sys.executable,py,str(p)],[cpp,str(p)]):
    r=subprocess.run(cmd,capture_output=True,text=True,timeout=30)
    if r.returncode==0:raise AssertionError(f'{label} ACCEPTED by {cmd[0]}')
 print('PASS negative controls',len(cases),'cases x 2 independent verifiers')

if __name__=='__main__':run(*sys.argv[1:])
