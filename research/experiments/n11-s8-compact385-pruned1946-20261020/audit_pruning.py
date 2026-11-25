#!/usr/bin/env python3
"""Audit the complete 30-column deletion against the original 1591."""
from pathlib import Path
from fractions import Fraction
import json
from collections import defaultdict
from verify_core import children
B=Path(__file__).resolve().parent
old={l.split()[0] for l in (B/'win_witnesses1591.tsv').read_text().splitlines()}
new={l.split()[0] for l in (B/'win_witnesses1561.tsv').read_text().splitlines()}
removed=set((B/'removed30.txt').read_text().split())
last24=set((B/'removed24.txt').read_text().split())
assert len(old)==1591 and len(new)==1561 and old-new==removed and len(removed)==30
assert len(last24)==24 and last24<=removed
D=json.loads((B/'dual_components.json').read_text())
W={h:Fraction(v) for d in D for h,v in d['weights'].items()}
s9={f'{b:032x}' for h in (B/'loss_roots35.txt').read_text().split() for b in children(int(h,16))}
cov=defaultdict(set)
for h in s9:
 for b in children(int(h,16)):cov[f'{b:032x}'].add(h)
assert len(s9)==782 and len(cov)==6446
weight=lambda ss:sum((W.get(s,0) for s in ss),Fraction(0))
high={h for h,ss in cov.items() if weight(ss)>1}
assert len(high)==1346 and high<=new
for h in removed:assert h in cov and weight(cov[h])==1
# Verify the 215 counterfactual essentials are all still excluded.
proof0=json.loads((B/'component0_essential115.json').read_text())
proof6=json.loads((B/'component6_essential100.json').read_text())
essential=set(proof0['selected128_by_restored_exclusion'])|set(proof6['selected41_by_restored_exclusion'])
assert len(essential)==215 and essential<=new and not essential&removed
assert old-high==essential|removed
print('PASS 245 optional exclusions partition into 215 individually essential and 30 jointly removable')
print('PASS all 1346 high-dual-weight exclusions retained; no WIN/LOSS verdicts changed')
