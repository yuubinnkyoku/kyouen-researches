#!/usr/bin/env python3
"""Rebuild the complete 24-root terminal certificate using shared S10 leaves."""
from pathlib import Path
from verify_core import canonical,legal
B=Path(__file__).resolve().parent
roots=[]
for line in (B/'proof24.tsv').read_text().splitlines():
 a=line.split('\t')
 if a[0]=='ROOT':roots.append((int(a[1],16),a[2],int(a[3])))
assert len(roots)==24
selected_loss={int(x,16) for x in (B/'loss4_cover_selected.txt').read_text().split()}
chosen_win={int(a,16):int(b,16) for line in (B/'win20_s9_selected.tsv').read_text().splitlines() for a,b in [line.split('\t')]}
verdict={int(a[0],16):(a[1],int(a[2])) for line in (B/'all_s10_cpp.tsv').read_text().splitlines() if (a:=line.split('\t'))}
rows=[]
for r,v,n in roots:
 rows.append(f'ROOT\t{r:032x}\t{v}\t{n}\t0')
 if v=='WIN':
  s9=chosen_win[r]
  assert s9 in {canonical(r|1<<p) for p in legal(r)}
  ch=sorted({canonical(s9|1<<p) for p in legal(s9)})
  assert ch and all(verdict[c][0]=='WIN' for c in ch)
  rows.append(f'S9_LOSS\t{s9:032x}')
  rows.extend(f'S10_WIN\t{c:032x}' for c in ch)
 else:
  for s9 in sorted({canonical(r|1<<p) for p in legal(r)}):
   ch={canonical(s9|1<<p) for p in legal(s9)}
   choices=ch&selected_loss
   assert choices
   c=min(choices,key=lambda x:(verdict[x][1],x))
   assert verdict[c][0]=='LOSS'
   rows.append(f'S9_WIN\t{s9:032x}\t{c:032x}')
(B/'proof24_optimized.tsv').write_text('\n'.join(rows)+'\n')
print('rewritten',len(roots),'roots',len(rows),'lines')
