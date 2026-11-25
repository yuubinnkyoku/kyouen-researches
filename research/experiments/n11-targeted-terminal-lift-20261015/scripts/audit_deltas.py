#!/usr/bin/env python3
"""Cross-check the newly certified roots and all reported counts."""
from pathlib import Path
from collections import Counter
import csv
p=Path(__file__).resolve().parent.parent
D=p/'data';C=p/'certificates'
def lines(name):return set((D/name).read_text().split())
def roots(name,tag):
 return {a[1] for line in (C/name).read_text().splitlines() if (a:=line.split()) and a[0]==tag}
old8=lines('lift_s8_win_after_49095.txt');mid8=lines('lifted_s8_win_51164.txt');new8=lines('lifted_s8_win_51571.txt')
assert len(old8)==13314 and len(mid8)==13485 and len(new8)==13501
assert mid8-old8==roots('new_s8_171_terminal.cert','EDGE')
assert new8-mid8==roots('new_s8_win_sixteen_terminal.cert','EDGE')
oldloss8=lines('all_s8_loss_291.txt');newloss8=lines('all_s8_loss_294.txt')
assert len(oldloss8)==291 and len(newloss8)==294
assert newloss8-oldloss8==roots('new_s8_loss_three_terminal.cert','ROOT')
oldloss7=lines('all_s7_loss_2213.txt');newloss7=lines('all_s7_loss_2232.txt')
assert len(oldloss7)==2213 and len(newloss7)==2232
assert newloss7-oldloss7==lines('new_s7_loss_from_three.txt')
assert not newloss8&new8 and not newloss7&lines('all_s7_win_17.txt')
old9=lines('lifted_s9_win_51164.txt');new9=lines('lifted_s9_win_51571.txt')
assert len(old9)==1609 and len(new9)==1611
assert len(new9-old9)==2
base=dict(line.split() for line in (D/'s10_merged_51164.tsv').read_text().splitlines())
new=dict(line.split() for line in (D/'s10_merged_51571.tsv').read_text().splitlines())
assert len(base)==51164 and len(new)==51571
assert all(new[k]==v for k,v in base.items())
delta={k:v for k,v in new.items() if k not in base}
assert len(delta)==407 and Counter(delta.values())=={'WIN':364,'LOSS':43}
rank=list(csv.DictReader((D/'s8_loss_rank_candidates.tsv').open(),delimiter='\t'))
assert len([r for r in rank if 1<=int(r['missing'])<=3])==120
assert all(r['s8'] in mid8 for r in rank if 1<=int(r['missing'])<=3)
print('PASS delta audit: +407 S10, +187 S8 WIN, +3 S8 LOSS, +19 S7 LOSS, 120 false near-LOSS candidates pruned')
