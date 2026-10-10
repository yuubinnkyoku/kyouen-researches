#!/usr/bin/env python3
"""Independent S6 shared-boundary census for the top five live S4 classes."""
import collections
import csv
import gzip
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[4]
EXP=ROOT/"research/experiments/n11-two-target-design-20261010"
GEOMETRY=ROOT/"research/experiments/n11-strategy-redesign-20261010/output/geometry.json.gz"
CACHE=EXP/"output/merged-exact-s5.cache"
PROFILE=EXP/"output/post-probe/strategy-analysis.json"
HISTORY=ROOT/"research/experiments/n11-strategy-redesign-20261010/output/history.json"
sys.path.insert(0,str(ROOT/"research/experiments/n11-independent-exact-audit-20261010/scripts"))
from independent import Board

def mask(k):
    return int(k[0])|(int(k[1])<<64)
def key(m):
    return (m&((1<<64)-1),m>>64)
def label(k):
    return f"{k[0]}:{k[1]}"

data=json.loads(PROFILE.read_text())
selected=[tuple(map(int,r["key"].split(":"))) for r in data["top_completion_proxy"][:5]]
assert len(set(selected))==5
geo={tuple(g["key"]):g for g in json.loads(gzip.open(GEOMETRY,"rt").read())}
cache={}
for r in csv.reader(CACHE.open()):
    if r and r[0]=="s5verdict": cache[tuple(map(int,r[1:3]))]=int(r[4])
board=Board(11)
s6_by_s5={}
s6_by_class={}
class_rows=[]
for c in selected:
    parent=geo[c]
    unknown=[tuple(x) for x in parent["children"] if tuple(x) not in cache]
    s6=set()
    incidences=0
    for k in unknown:
        if k not in s6_by_s5:
            assert board.canonical(mask(k))==mask(k)
            ch=board.children(mask(k))
            s6_by_s5[k]={key(m) for m in ch}
        s6.update(s6_by_s5[k])
        incidences+=len(s6_by_s5[k])
    s6_by_class[c]=s6
    class_rows.append({"class":label(c),"unknown_s5":len(unknown),
                       "s6_incidences":incidences,"unique_s6":len(s6),
                       "intra_class_s6_reuse":incidences-len(s6)})
pairs=[]
for i,a in enumerate(selected):
    for b in selected[i+1:]:
        sh=len(s6_by_class[a]&s6_by_class[b])
        ca={tuple(x) for x in geo[a]["children"] if tuple(x) not in cache}
        cb={tuple(x) for x in geo[b]["children"] if tuple(x) not in cache}
        pairs.append({"class_a":label(a),"class_b":label(b),
                      "shared_unknown_s5":len(ca&cb),"shared_s6":sh,
                      "fraction_of_smaller_s6_boundary":round(sh/min(len(s6_by_class[a]),len(s6_by_class[b])),5)})
all_s6=set().union(*s6_by_class.values())
history=json.loads(HISTORY.read_text())
saved={}
for r in history:
    if r["stones"]==6 and r["verdict"] in (1,2):
        saved[tuple(r["key"])]=r["verdict"]
out={"independent_11x11_geometry":"independent.Board with exact integer bisectors and D4",
     "scope":"Five cheapest capped-cost live S4 candidates; frozen history S6 only",
     "s6_unique_across_five":len(all_s6),
     "s6_incidence_sum":sum(r["s6_incidences"] for r in class_rows),
     "s6_repeated_across_classes":sum(len(s) for s in s6_by_class.values())-len(all_s6),
     "saved_s6_exact_overlap_frozen_history":sum(x in saved for x in all_s6),
     "saved_s6_loss_overlap_frozen_history":sum(saved.get(x)==2 for x in all_s6),
     "classes":class_rows,"pairs":pairs,
     "caveat":"No inference of S5/S4 verdicts; frozen S6 history lacks subsequent updates and terminal-only certificates."}
p=EXP/"output/post-probe/s6-sharing-top5.json"
p.write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n")
print(json.dumps(out,ensure_ascii=False,indent=2)[:12000])
