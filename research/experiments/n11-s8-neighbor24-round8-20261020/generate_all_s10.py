from pathlib import Path
from verify_core import canonical,legal
B=Path(__file__).resolve().parent
roots=[(int(a[1],16),a[2]) for line in (B/'proof24.tsv').read_text().splitlines() if (a:=line.split('\t'))[0]=='ROOT']
assert len(roots)==24
s9={canonical(r|1<<p) for r,v in roots for p in legal(r)}
s10=sorted({canonical(s|1<<p) for s in s9 for p in legal(s)})
(B/'all_s10.txt').write_text('\n'.join(f'{x:032x}' for x in s10)+'\n')
print('s9',len(s9),'s10',len(s10))
