#!/usr/bin/env python3
"""Check that all high-coverage near-LOSS S8 candidates are already classified."""
from pathlib import Path
import csv,collections
p=Path(__file__).resolve().parent.parent/'data'
w=set((p/'lifted_s8_win_51571.txt').read_text().split())
l=set((p/'all_s8_loss_294.txt').read_text().split())
rows=list(csv.DictReader((p/'s8_loss_rank_51571.tsv').open(),delimiter='\t'))
assert all(0<=int(r['missing'])<=5 and int(r['known_s9'])>=12 for r in rows)
unknown=[r for r in rows if r['s8'] not in w|l]
assert not unknown,unknown
hist=collections.Counter(int(r['missing']) for r in rows)
print('PASS high-coverage near-LOSS scan',len(rows),'classified',len(rows),'unknown',0,'missing histogram',dict(sorted(hist.items())))
