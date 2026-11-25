from pathlib import Path
from verify_core import canonical,points,safe
from verify_proof import parse
B=Path(__file__).resolve().parent
roots=parse(B/'round9_proof_optimized.tsv')
loss={int(r['root'],16) for r in roots if r['result']=='LOSS'}
assert len(loss)==6
s7={canonical(r^(1<<p)) for r in loss for p in points(r)}
assert len(s7)==44 and all(safe(x) and x.bit_count()==7 for x in s7)
assert s7=={int(x,16) for x in (B/'round9_s7_parents.txt').read_text().split()}
s6={canonical(s^(1<<p)) for s in s7 for p in points(s)}
assert len(s6)==139 and all(safe(x) and x.bit_count()==6 for x in s6)
assert s6=={int(x,16) for x in (B/'round9_s6_win_parents.txt').read_text().split()}
print('PASS 44 S7 LOSS parents, 139 S6 WIN parents (fixed-first-player viewpoint)')
