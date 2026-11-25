#!/usr/bin/env python3
from pathlib import Path
from verify_core import canonical,legal,points,safe
B=Path(__file__).resolve().parent
prior={int(x,16) for x in (B/'previous_s8_roots.txt').read_text().split()}
seeds={int(x,16) for x in (B/'seed_s8_loss6.txt').read_text().split()}
assert len(prior)==139 and len(seeds)==6 and seeds<=prior
candidates=set()
for root in seeds:
 assert safe(root) and canonical(root)==root and root.bit_count()==8
 for p in points(root):
  s7=root^(1<<p)
  for q in legal(s7):
   if not (root>>q&1):
    s8=canonical(s7|(1<<q))
    if s8 not in prior:candidates.add(s8)
rank=sorted((len(legal(c)),c) for c in candidates)
selected=[f'{c:032x}' for _,c in rank[:24]]
(B/'roots24.txt').write_text('\n'.join(selected)+'\n')
print('candidates',len(candidates),'selected',len(selected),'s9legal', [v for v,_ in rank[:24]])
