from pathlib import Path
from verify_core import children
B=Path(__file__).resolve().parent
obs=[int(x.split('\t')[0],16) for x in (B/'loss6_cover_mapping.tsv').read_text().splitlines()]
all10=set().union(*(children(s9) for s9 in obs))
(B/'loss6_all_s10.txt').write_text(''.join(f'{x:032x}\n' for x in sorted(all10)))
print('all S10 boundary',len(all10))
