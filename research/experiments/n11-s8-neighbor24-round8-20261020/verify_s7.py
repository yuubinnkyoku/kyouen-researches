#!/usr/bin/env python3
"""Verify S7 LOSS consequences of four terminal-proved S8 LOSS roots.
Labels are fixed-original-first-player (S7 AND, S8 OR).
"""
from pathlib import Path
from verify_core import canonical,points,safe,children
B=Path(__file__).resolve().parent
roots=[int(a[1],16) for line in (B/'proof24_optimized.tsv').read_text().splitlines() if (a:=line.split('\t'))[0]=='ROOT' and a[2]=='LOSS']
assert len(roots)==4 and len(set(roots))==4
assert all(r.bit_count()==8 and safe(r) and canonical(r)==r for r in roots)
parents={canonical(r^(1<<p)) for r in roots for p in points(r)}
assert len(parents)==31
assert parents=={int(x,16) for x in (B/'s7_parents_all.txt').read_text().split()}
assert all(safe(p) and p.bit_count()==7 and canonical(p)==p for p in parents)
for s in parents:
 assert children(s)&set(roots),f'S7 parent lacks proven S8 LOSS child {s:032x}'
prior={int(x,16) for x in (B/'prior_s8_loss26.txt').read_text().split()}
assert len(prior)==26 and all(safe(p) and p.bit_count()==8 and canonical(p)==p for p in prior)
prior_parents={canonical(r^(1<<p)) for r in prior for p in points(r)}
assert len(prior_parents)==182
new=parents-prior_parents
assert len(new)==28 and new=={int(x,16) for x in (B/'s7_new_vs_previous_proofs.txt').read_text().split()}
print('PASS 4 S8 LOSS -> 31 canonical S7 LOSS, 28 not derived from 26 prior archived S8 LOSS roots')
