from pathlib import Path
from tempfile import TemporaryDirectory
from verify_s6_win import verify
lines=Path('s8_38_win_proof.tsv').read_text().splitlines()
variants=[]
variants.append([r for i,r in enumerate(lines) if i!=next(j for j,x in enumerate(lines) if x.startswith('ROOT\t'))])
variants.append([r for i,r in enumerate(lines) if i!=next(j for j,x in enumerate(lines) if x.startswith('S10_WIN\t'))])
for marker in ('ROOT\t','S9_LOSS\t'):
 arr=lines[:];i=next(j for j,x in enumerate(arr) if x.startswith(marker));v=arr[i].split('\t');v[2 if marker.startswith('ROOT') else 1]='00000000000000000000000000000000';arr[i]='\t'.join(v);variants.append(arr)
with TemporaryDirectory() as d:
 for i,rows in enumerate(variants):
  p=Path(d)/f'bad{i}.tsv';p.write_text('\n'.join(rows)+'\n')
  try:verify(p)
  except ValueError:print('PASS reject mutation',i)
  else:raise AssertionError(f'accepted mutation {i}')
