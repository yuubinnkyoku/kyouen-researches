from pathlib import Path
from verify_proof import parse,verify
B=Path(__file__).resolve().parent
mapping={a:b for a,b in (line.split('\t') for line in (B/'loss6_all_cover_mapping.tsv').read_text().splitlines())}
blocks=parse(B/'round9_proof.tsv')
with (B/'round9_proof_optimized.tsv').open('w') as f:
 for block in blocks:
  f.write(f"ROOT\t{block['root']}\t{block['result']}\t{block['legal']}\t0\n")
  if block['result']=='LOSS':
   for x in block['children']:
    assert x[0]=='S9_WIN' and x[1] in mapping
    f.write(f'S9_WIN\t{x[1]}\t{mapping[x[1]]}\n')
  else:
   for x in block['children']:f.write('\t'.join(x)+'\n')
verify(B/'round9_proof_optimized.tsv')
