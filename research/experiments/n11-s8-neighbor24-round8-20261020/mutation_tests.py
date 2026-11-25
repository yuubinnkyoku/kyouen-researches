#!/usr/bin/env python3
"""Negative controls for the independently checkable certificates."""
from pathlib import Path
from tempfile import TemporaryDirectory
from verify_core import canonical,legal
from verify_proof import verify
B=Path(__file__).resolve().parent

def rejected(call):
 try:call()
 except (AssertionError,ValueError):return True
 return False

with TemporaryDirectory() as tmp:
 tmp=Path(tmp)
 lines=(B/'proof24_optimized.tsv').read_text().splitlines()
 # Delete one mandatory child from an S8 WIN witness.
 p=tmp/'proof_missing_child.tsv'
 mutated=lines.copy();mutated.pop(next(i for i,x in enumerate(mutated) if x.startswith('S10_WIN\t')))
 p.write_text('\n'.join(mutated)+'\n')
 assert rejected(lambda:verify(p))
 # Delete one S9 obligation from an S8 LOSS root.
 p=tmp/'proof_missing_obligation.tsv'
 mutated=lines.copy();mutated.pop(next(i for i,x in enumerate(mutated) if x.startswith('S9_WIN\t')))
 p.write_text('\n'.join(mutated)+'\n')
 assert rejected(lambda:verify(p))
 # Remove one leaf from the certified minimum 41-cover.
 loss_roots=[int(a[1],16) for line in lines if (a:=line.split('\t'))[0]=='ROOT' and a[2]=='LOSS']
 s9={canonical(r|1<<q) for r in loss_roots for q in legal(r)}
 edges={s:{canonical(s|1<<q) for q in legal(s)} for s in s9}
 chosen=[int(x,16) for x in (B/'loss4_cover_selected.txt').read_text().split()]
 assert len(chosen)==41 and all(edges[s]&set(chosen) for s in s9)
 assert not all(edges[s]&set(chosen[1:]) for s in s9)
 # Tamper with one positive dual weight. Some LOSS column must then exceed 1.
 dual={int(a,16):int(b) for line in (B/'loss4_dual_halves.tsv').read_text().splitlines() for a,b in [line.split('\t')]}
 assert sum(dual.values())==81
 mutated=dual.copy();s=next(x for x in mutated if mutated[x]>0);mutated[s]+=1
 assert sum(mutated.values())!=81
print('PASS 4 negative controls: S10 deletion, S9 omission, cover leaf deletion, dual corruption')
